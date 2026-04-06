"""By-reference launch helpers for bounded concept-analysis workflows."""

from __future__ import annotations

import logging
from typing import Any

from src.executor.document_store import load_registered_documents_in_order, store_document
from src.executor.job_manager import create_job
from src.executor.workflow_runner import start_execution_thread
from src.orchestrator.pipeline_schemas import (
    ConceptAnalysisByRefRequest,
    ConceptAnalysisLaunchResponse,
)
from src.orchestrator.planner import _save_plan
from src.orchestrator.schemas import PhaseExecutionSpec, TargetWork, WorkflowExecutionPlan
from src.workflows.registry import get_workflow_registry

logger = logging.getLogger(__name__)


def _mode_display_name(analysis_mode: str) -> str:
    return "Inferential" if analysis_mode == "inferential" else "Logical"


def _default_depth_for_mode(analysis_mode: str) -> str:
    return "standard" if analysis_mode == "inferential" else "deep"


def _resolve_depth(request: ConceptAnalysisByRefRequest) -> str:
    normalized = (request.depth_preference or "").strip().lower()
    if normalized in {"surface", "standard", "deep"}:
        return normalized
    return _default_depth_for_mode(request.analysis_mode)


def _compose_analysis_packet(
    request: ConceptAnalysisByRefRequest,
    ordered_documents: list[dict[str, Any]],
) -> str:
    lines: list[str] = [
        "# Close Read Concept Analysis Packet",
        "",
        f"Target concept: {request.concept_name}",
        f"Analysis mode: {request.analysis_mode}",
        f"Subject author: {request.subject_author or 'Unknown author'}",
        f"Subject/work label: {request.subject_name or 'Unspecified project'}",
        "",
        "Instructions:",
        "- Analyze the named concept across the ordered sources below.",
        "- Use the source titles exactly as given when referring to document-specific evidence.",
        "- Treat the source ordering below as meaningful for evolution/comparison.",
        "",
        "Ordered sources:",
    ]

    for index, document in enumerate(ordered_documents, start=1):
        title = document.get("title") or document.get("external_doc_key") or f"Source {index}"
        binding_role = document.get("binding_role") or "context"
        external_doc_key = document.get("external_doc_key") or ""
        lines.append(
            f"{index}. {title} "
            f"[role={binding_role}, external_doc_key={external_doc_key}]"
        )

    for index, document in enumerate(ordered_documents, start=1):
        title = document.get("title") or document.get("external_doc_key") or f"Source {index}"
        author = document.get("author") or "Unknown author"
        binding_role = document.get("binding_role") or "context"
        external_doc_key = document.get("external_doc_key") or ""
        text = document.get("text") or ""
        lines.extend(
            [
                "",
                f"## Source {index}: {title}",
                f"Author: {author}",
                f"Binding role: {binding_role}",
                f"External doc key: {external_doc_key}",
                "",
                text,
            ]
        )

    return "\n".join(lines)


def _build_plan(
    request: ConceptAnalysisByRefRequest,
    *,
    depth: str,
) -> WorkflowExecutionPlan:
    workflow = get_workflow_registry().get(request.workflow_key)
    if workflow is None:
        raise ValueError(f"Workflow not found: {request.workflow_key}")
    if not workflow.phases:
        raise ValueError(f"Workflow '{request.workflow_key}' has no phases")

    workflow_phase = workflow.phases[0]
    phase_name = workflow_phase.phase_name or f"{_mode_display_name(request.analysis_mode)} Analysis"

    phase_spec = PhaseExecutionSpec(
        phase_number=workflow_phase.phase_number,
        phase_name=phase_name,
        skip=False,
        depth=depth,
        rationale=(
            f"Execute analyzer-v2 owned {request.analysis_mode} concept analysis for "
            f"'{request.concept_name}' over the registered project corpus."
        ),
        context_emphasis=(
            f"Focus analysis on the concept '{request.concept_name}' and preserve "
            "source-local distinctions from the ordered corpus packet."
        ),
        requires_full_documents=True,
        model_hint=None,
    )

    subject_label = request.subject_name or f"{request.concept_name} concept analysis"
    target_title = f"{request.concept_name}: {_mode_display_name(request.analysis_mode)}"

    return WorkflowExecutionPlan(
        workflow_key=request.workflow_key,
        thinker_name=request.subject_author or "Unknown author",
        target_work=TargetWork(
            title=target_title,
            author=request.subject_author,
            description=(
                f"{_mode_display_name(request.analysis_mode)} analysis of the concept "
                f"'{request.concept_name}' in {subject_label}."
            ),
        ),
        prior_works=[],
        research_question=(
            f"Analyze the concept '{request.concept_name}' in "
            f"{request.subject_author or 'the corpus'} using the "
            f"{request.analysis_mode} concept-analysis workflow."
        ),
        strategy_summary=(
            f"Bounded single-concept {_mode_display_name(request.analysis_mode).lower()} "
            "analysis over registered project documents. The execution packet preserves "
            "source ordering and source titles inside one analyzer-v2-owned run."
        ),
        phases=[phase_spec],
        recommended_views=[],
        estimated_llm_calls=workflow.estimated_phases or len(workflow.phases),
        estimated_depth_profile=depth,
        status="approved",
        execution_model=None,
    )


def run_concept_analysis_by_ref(
    request: ConceptAnalysisByRefRequest,
) -> ConceptAnalysisLaunchResponse:
    """Launch one explicit analyzer-v2 concept-analysis job over registered docs."""
    ordered_documents = load_registered_documents_in_order(
        consumer_key=request.consumer_key,
        external_project_id=request.external_project_id,
        external_doc_keys=request.external_doc_keys,
    )
    if not ordered_documents:
        raise ValueError("No registered documents found for concept analysis launch")

    depth = _resolve_depth(request)
    packet_text = _compose_analysis_packet(request, ordered_documents)
    packet_doc_id = store_document(
        title=f"{request.concept_name}::{request.analysis_mode}::packet",
        text=packet_text,
        author=request.subject_author,
        role="target",
    )

    plan = _build_plan(request, depth=depth)
    _save_plan(plan)
    plan_payload = plan.model_dump()
    plan_payload["_concept_by_ref_context"] = {
        "consumer_key": request.consumer_key,
        "external_project_id": request.external_project_id,
        "concept_name": request.concept_name,
        "analysis_mode": request.analysis_mode,
        "workflow_key": request.workflow_key,
        "subject_author": request.subject_author,
        "subject_name": request.subject_name,
        "depth": depth,
        "external_doc_keys": request.external_doc_keys,
    }

    document_ids = {"target": packet_doc_id}
    job_record = create_job(
        job_id=f"job-{plan.plan_id}",
        plan_id=plan.plan_id,
        plan_data=plan_payload,
        document_ids=document_ids,
        workflow_key=request.workflow_key,
        project_id=request.project_id,
    )

    start_execution_thread(
        job_id=job_record["job_id"],
        plan_id=plan.plan_id,
        document_ids=document_ids,
    )

    logger.info(
        "Concept by-ref launch: concept=%s mode=%s workflow=%s job=%s plan=%s docs=%s",
        request.concept_name,
        request.analysis_mode,
        request.workflow_key,
        job_record["job_id"],
        plan.plan_id,
        len(ordered_documents),
    )

    return ConceptAnalysisLaunchResponse(
        job_id=job_record["job_id"],
        plan_id=plan.plan_id,
        concept_name=request.concept_name,
        workflow_key=request.workflow_key,
        analysis_mode=request.analysis_mode,
        status="pending",
        cancel_token=job_record.get("cancel_token"),
        message="Concept analysis launched. Poll /v1/executor/jobs/{job_id} for progress.",
    )
