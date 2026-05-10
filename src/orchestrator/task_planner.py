"""Stage 9 route-plus-hydrate-plus-plan orchestration."""

from __future__ import annotations

import json
import os
from typing import Any, Optional, cast

import httpx

from src.orchestrator.by_ref import generate_plan_for_by_ref_request
from src.orchestrator.pipeline import generate_plan_for_analysis_request
from src.orchestrator.planning_decision_store import save_task_planning_decision
from src.orchestrator.task_planning_schemas import (
    AoiCompositionHandoffPlan,
    DirectSectionsCompositionHandoffPlan,
    InlineDocumentsPlanningContext,
    PlanningTraceEntry,
    RegisteredCorpusPlanningContext,
    RejectedPlanningAlternative,
    SavedResultPlanningContext,
    TaskPlanningContext,
    TaskPlanningDecision,
    TaskPlanningRequest,
)
from src.orchestrator.task_router import route_composition_task
from src.orchestrator.task_routing_schemas import CompositionTaskRequest, CompositionTaskRoutingDecision
from src.orchestrator.genealogy_saved_result_bridge import (
    build_genealogy_saved_result_handoff_plan,
)
from src.presenter.schemas import AoiRejectedSourceInput, AoiSelectedSourceInput
from src.presenter.composition_source_bridge import (
    SOURCE_FAMILY_ENGAGEMENT_MAPPING,
    SOURCE_FAMILY_SIN_FINDINGS,
    SOURCE_FAMILY_THEMATIC_REPORT,
    SOURCE_FAMILY_THEMATIC_SYNTHESIS,
    ComposeFromSourceResolutionError,
    evaluate_compose_profile_feasibility,
    resolve_source_catalog,
)
from src.llm.client import GENERATION_MODEL, get_anthropic_client, parse_llm_json_response

AOI_SELECTION_PROMPT_VERSION = "aoi-selection-v1"
AOI_SELECTION_MODEL = os.environ.get("AOI_SELECTION_MODEL", GENERATION_MODEL)
AOI_SELECTION_TIMEOUT_S_DEFAULT = 45.0
AOI_SELECTION_MAX_RETRIES = 0
AOI_SELECTION_VALIDATOR_VERSION = "aoi-selection-validator-v1"
_AOI_PROFILE_FAMILY_SETS = {
    "dossier": (
        SOURCE_FAMILY_THEMATIC_SYNTHESIS,
        SOURCE_FAMILY_THEMATIC_REPORT,
    ),
    "comparison": (
        SOURCE_FAMILY_ENGAGEMENT_MAPPING,
        SOURCE_FAMILY_SIN_FINDINGS,
        SOURCE_FAMILY_THEMATIC_REPORT,
    ),
}


class _AoiSelectionBlocked(RuntimeError):
    def __init__(
        self,
        reason_code: str,
        detail: str,
        *,
        trace_details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(detail)
        self.reason_code = reason_code
        self.detail = detail
        self.trace_details = trace_details or _build_aoi_selection_trace_details(
            provider_outcome=reason_code,
            blocked_reason_code=reason_code,
            blocked_reason_detail=detail,
        )


def _get_env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except (TypeError, ValueError):
        return default


def _get_aoi_selection_timeout_s() -> float:
    return _get_env_float("AOI_SELECTION_TIMEOUT_S", AOI_SELECTION_TIMEOUT_S_DEFAULT)


def plan_composition_task(request: TaskPlanningRequest) -> TaskPlanningDecision:
    """Plan from the Stage 8 task envelope plus optional hydration context."""

    trace: list[PlanningTraceEntry] = []
    _validate_request_consistency(request)

    effective_task_request = _build_effective_task_request(request)
    trace.append(
        PlanningTraceEntry(
            stage="effective_task_request",
            details={
                "consumer_key": effective_task_request.consumer_key,
                "source_mode": getattr(effective_task_request.source_constraints, "source_mode", None),
                "context_mode": getattr(request.planning_context, "context_mode", None),
            },
        )
    )

    routing_decision = route_composition_task(effective_task_request)
    trace.append(_routing_reuse_trace(request.prior_routing_decision, routing_decision))

    if routing_decision.routing_outcome == "unsupported":
        if routing_decision.selected_objective_key and routing_decision.source_sufficiency_status == "insufficient":
            decision = _build_insufficient_context_decision(
                routing_decision=routing_decision,
                trace=trace,
                required_hydration=_required_hydration_from_request(effective_task_request, routing_decision),
                required_host_preparation=_remaining_host_preparation(
                    effective_task_request=effective_task_request,
                    routing_decision=routing_decision,
                ),
                decision_reason="routed_objective_missing_planner_ready_context",
            )
        else:
            decision = _build_unsupported_decision(
                routing_decision=routing_decision,
                trace=trace,
                decision_reason="routing_remained_unsupported",
            )
        return _finalize_planning_decision(
            request=request,
            effective_task_request=effective_task_request,
            routing_decision=routing_decision,
            decision=decision,
        )

    if routing_decision.selected_objective_key == "genealogical":
        decision = _plan_genealogy(
            request=request,
            effective_task_request=effective_task_request,
            routing_decision=routing_decision,
            trace=trace,
        )
        return _finalize_planning_decision(
            request=request,
            effective_task_request=effective_task_request,
            routing_decision=routing_decision,
            decision=decision,
        )

    if routing_decision.selected_objective_key == "influence_thematic":
        decision = _plan_aoi(
            request=request,
            effective_task_request=effective_task_request,
            routing_decision=routing_decision,
            trace=trace,
        )
        return _finalize_planning_decision(
            request=request,
            effective_task_request=effective_task_request,
            routing_decision=routing_decision,
            decision=decision,
        )

    decision = _build_unsupported_decision(
        routing_decision=routing_decision,
        trace=trace,
        decision_reason="objective_not_supported_for_stage9",
    )
    return _finalize_planning_decision(
        request=request,
        effective_task_request=effective_task_request,
        routing_decision=routing_decision,
        decision=decision,
    )


def _finalize_planning_decision(
    *,
    request: TaskPlanningRequest,
    effective_task_request: CompositionTaskRequest,
    routing_decision: CompositionTaskRoutingDecision,
    decision: TaskPlanningDecision,
) -> TaskPlanningDecision:
    if not request.persist_decision:
        return decision

    snapshot = save_task_planning_decision(
        task_request=effective_task_request,
        routing_decision=routing_decision,
        planning_decision=decision,
    )
    return decision.model_copy(update={"planning_decision_id": snapshot.planning_decision_id})


def _validate_request_consistency(request: TaskPlanningRequest) -> None:
    planning_context = request.planning_context
    task_request = request.task_request
    source_constraints = task_request.source_constraints

    if planning_context is None:
        return

    context_consumer_key = _context_consumer_key(planning_context)
    if task_request.consumer_key and context_consumer_key and task_request.consumer_key != context_consumer_key:
        raise ValueError(
            "task_request.consumer_key conflicts with planning_context.consumer_key."
        )

    if source_constraints is None:
        return

    if source_constraints.source_mode != planning_context.context_mode:
        raise ValueError(
            "task_request.source_constraints.source_mode conflicts with planning_context.context_mode."
        )

    if planning_context.context_mode == "registered_corpus":
        context = cast(RegisteredCorpusPlanningContext, planning_context)
        source = cast(Any, source_constraints)
        _raise_if_conflict("registered_corpus.consumer_key", source.consumer_key, context.consumer_key)
        _raise_if_conflict(
            "registered_corpus.external_project_id",
            source.external_project_id,
            context.external_project_id,
        )
        _raise_if_conflict(
            "registered_corpus.target_external_doc_key",
            source.target_external_doc_key,
            context.target_external_doc_key,
        )
        _raise_if_conflict(
            "registered_corpus.prior_work_external_doc_keys_count",
            source.prior_work_external_doc_keys_count,
            len(context.prior_works),
        )
        _raise_if_conflict(
            "registered_corpus.has_target_chapter_external_doc_keys",
            source.has_target_chapter_external_doc_keys,
            bool(context.target_chapter_external_doc_keys),
        )
        return

    if planning_context.context_mode == "inline_documents":
        context = cast(InlineDocumentsPlanningContext, planning_context)
        source = cast(Any, source_constraints)
        _raise_if_conflict(
            "inline_documents.has_target_work_text",
            source.has_target_work_text,
            bool(context.target_work_text.strip()),
        )
        _raise_if_conflict(
            "inline_documents.prior_work_count",
            source.prior_work_count,
            len(context.prior_works),
        )
        _raise_if_conflict(
            "inline_documents.has_target_work_chapters",
            source.has_target_work_chapters,
            bool(context.target_work_chapters),
        )
        return

    context = cast(SavedResultPlanningContext, planning_context)
    source = cast(Any, source_constraints)
    if context.source_v2_job_id is not None:
        _raise_if_conflict(
            "saved_result.source_v2_job_id",
            source.source_v2_job_id,
            context.source_v2_job_id,
        )


def _raise_if_conflict(label: str, left: Any, right: Any) -> None:
    if left is None:
        return
    if left != right:
        raise ValueError(f"{label} conflicts between task_request and planning_context.")


def _build_effective_task_request(request: TaskPlanningRequest) -> CompositionTaskRequest:
    task_data = request.task_request.model_dump(mode="python")
    planning_context = request.planning_context
    if planning_context is None:
        return CompositionTaskRequest.model_validate(task_data)

    context_consumer_key = _context_consumer_key(planning_context)
    if not task_data.get("consumer_key") and context_consumer_key:
        task_data["consumer_key"] = context_consumer_key

    derived_source_constraints = _derive_source_constraints(planning_context)
    if task_data.get("source_constraints") is None:
        task_data["source_constraints"] = derived_source_constraints
        return CompositionTaskRequest.model_validate(task_data)

    merged = dict(task_data["source_constraints"])
    for key, value in derived_source_constraints.items():
        if merged.get(key) is None:
            merged[key] = value
    task_data["source_constraints"] = merged
    return CompositionTaskRequest.model_validate(task_data)


def _derive_source_constraints(planning_context: TaskPlanningContext) -> dict[str, Any]:
    if planning_context.context_mode == "registered_corpus":
        context = cast(RegisteredCorpusPlanningContext, planning_context)
        return {
            "source_mode": "registered_corpus",
            "consumer_key": context.consumer_key,
            "external_project_id": context.external_project_id,
            "target_external_doc_key": context.target_external_doc_key,
            "prior_work_external_doc_keys_count": len(context.prior_works),
            "has_target_chapter_external_doc_keys": bool(context.target_chapter_external_doc_keys),
        }

    if planning_context.context_mode == "inline_documents":
        context = cast(InlineDocumentsPlanningContext, planning_context)
        return {
            "source_mode": "inline_documents",
            "has_target_work_text": bool(context.target_work_text.strip()),
            "prior_work_count": len(context.prior_works),
            "has_target_work_chapters": bool(context.target_work_chapters),
        }

    context = cast(SavedResultPlanningContext, planning_context)
    return {
        "source_mode": "saved_result",
        "source_v2_job_id": context.source_v2_job_id,
    }


def _context_consumer_key(planning_context: TaskPlanningContext) -> Optional[str]:
    if planning_context.context_mode == "registered_corpus":
        return cast(RegisteredCorpusPlanningContext, planning_context).consumer_key
    if planning_context.context_mode == "saved_result":
        return cast(SavedResultPlanningContext, planning_context).consumer_key
    return None


def _routing_reuse_trace(
    prior_routing_decision: Optional[CompositionTaskRoutingDecision],
    routing_decision: CompositionTaskRoutingDecision,
) -> PlanningTraceEntry:
    if prior_routing_decision is None:
        return PlanningTraceEntry(
            stage="routing_reuse",
            details={"status": "not_provided"},
        )

    comparable_fields = (
        "selected_objective_key",
        "selected_workflow_key",
        "routing_outcome",
        "launch_contract_kind",
        "source_sufficiency_status",
    )
    mismatches = [
        field
        for field in comparable_fields
        if getattr(prior_routing_decision, field) != getattr(routing_decision, field)
    ]
    if not mismatches:
        return PlanningTraceEntry(
            stage="routing_reuse",
            details={
                "status": "provided_and_validated",
                "reused_fields": list(comparable_fields),
            },
        )
    return PlanningTraceEntry(
        stage="routing_reuse",
        details={
            "status": "ignored_due_to_mismatch",
            "mismatched_fields": mismatches,
        },
    )


def _plan_genealogy(
    *,
    request: TaskPlanningRequest,
    effective_task_request: CompositionTaskRequest,
    routing_decision: CompositionTaskRoutingDecision,
    trace: list[PlanningTraceEntry],
) -> TaskPlanningDecision:
    planning_context = request.planning_context
    if planning_context is None or planning_context.context_mode not in {"saved_result", "registered_corpus", "inline_documents"}:
        return _build_insufficient_context_decision(
            routing_decision=routing_decision,
            trace=trace,
            required_hydration=_required_hydration_from_request(effective_task_request, routing_decision),
            required_host_preparation=[],
            decision_reason="genealogy_requires_saved_result_registered_or_inline_planning_context",
        )

    trace.append(
        PlanningTraceEntry(
            stage="hydration_evaluation",
            details={
                "status": "satisfied",
                "context_mode": planning_context.context_mode,
            },
        )
    )

    workflow_key = routing_decision.selected_workflow_key or "intellectual_genealogy"
    objective_key = routing_decision.selected_objective_key or "genealogical"
    if planning_context.context_mode == "saved_result":
        source_v2_job_id = _extract_source_v2_job_id(request, effective_task_request)
        if not source_v2_job_id:
            return _build_insufficient_context_decision(
                routing_decision=routing_decision,
                trace=trace,
                required_hydration=["source_v2_job_id"],
                required_host_preparation=_build_direct_sections_host_preparation(
                    consumer_key=effective_task_request.consumer_key,
                    lowering_required=False,
                ),
                decision_reason="genealogy_saved_result_requires_source_v2_job_id",
            )

        handoff_plan = build_genealogy_saved_result_handoff_plan(
            source_v2_job_id=source_v2_job_id,
            task_text=effective_task_request.task,
            consumer_key=effective_task_request.consumer_key,
            workflow_key=workflow_key,
            objective_key=objective_key,
        )
        trace.append(
            PlanningTraceEntry(
                stage="genealogy_saved_result_section_extraction",
                details={
                    "source_v2_job_id": source_v2_job_id,
                    "section_count": len(handoff_plan.prose_sections),
                    "sections": [
                        {
                            "engine_key": section.engine_key,
                            "title": section.title,
                        }
                        for section in handoff_plan.prose_sections
                    ],
                },
            )
        )

        decision = TaskPlanningDecision(
            normalized_task_summary=routing_decision.normalized_task_summary,
            routing_decision=routing_decision,
            planning_outcome_kind="direct_sections_composition_handoff_plan",
            planning_confidence=routing_decision.routing_confidence,
            hydration_status="satisfied",
            required_hydration=[],
            required_host_preparation=_build_direct_sections_host_preparation(
                consumer_key=effective_task_request.consumer_key,
                lowering_required=True,
            ),
            downstream_readiness="ready_for_direct_sections_compose_handoff",
            downstream_followup_contract={
                "method": "POST",
                "endpoint": "/v1/presenter/compose-from-intent",
                "handoff_kind": "direct_sections",
                "request_fields": {
                    "workflow_key": handoff_plan.workflow_key,
                    "consumer_key": handoff_plan.consumer_key or "<required>",
                    "user_intent": handoff_plan.resolved_intent_seed,
                    "prose_sections": "<lower from direct_sections_composition_handoff_plan>",
                },
            },
            hydrated_document_ids={},
            workflow_execution_plan=None,
            aoi_composition_handoff_plan=None,
            direct_sections_composition_handoff_plan=handoff_plan,
            rejected_planning_alternatives=_rejected_planning_alternatives(routing_decision),
            trace=trace,
        )
        decision.trace.append(
            PlanningTraceEntry(
                stage="planning_decision",
                details={
                    "planning_outcome_kind": decision.planning_outcome_kind,
                    "downstream_readiness": decision.downstream_readiness,
                },
            )
        )
        return decision

    if planning_context.context_mode == "registered_corpus":
        context = cast(RegisteredCorpusPlanningContext, planning_context)
        analyze_request = context.to_analyze_by_ref_request(
            workflow_key=workflow_key,
            objective_key=objective_key,
        )
        plan, document_ids = generate_plan_for_by_ref_request(analyze_request)
        project_id = context.project_id
    else:
        context = cast(InlineDocumentsPlanningContext, planning_context)
        analyze_request = context.to_analyze_request(
            workflow_key=workflow_key,
            objective_key=objective_key,
        )
        plan, document_ids = generate_plan_for_analysis_request(analyze_request)
        project_id = context.project_id

    trace.append(
        PlanningTraceEntry(
            stage="genealogy_plan_generated",
            details={
                "plan_id": plan.plan_id,
                "workflow_key": plan.workflow_key,
                "objective_key": plan.objective_key,
                "phase_count": len(plan.phases),
                "document_id_keys": sorted(document_ids.keys()),
            },
        )
    )

    decision = TaskPlanningDecision(
        normalized_task_summary=routing_decision.normalized_task_summary,
        routing_decision=routing_decision,
        planning_outcome_kind="genealogy_execution_plan",
        planning_confidence=routing_decision.routing_confidence,
        hydration_status="satisfied",
        required_hydration=[],
        required_host_preparation=[],
        downstream_readiness="ready_for_genealogy_execution",
        downstream_followup_contract={
            "method": "POST",
            "endpoint": "/v1/executor/jobs",
            "request_fields": {
                "plan_id": plan.plan_id,
                "document_ids": document_ids,
                "project_id": project_id or "<optional>",
            },
        },
        hydrated_document_ids=document_ids,
        workflow_execution_plan=plan,
        aoi_composition_handoff_plan=None,
        direct_sections_composition_handoff_plan=None,
        rejected_planning_alternatives=_rejected_planning_alternatives(routing_decision),
        trace=trace,
    )
    decision.trace.append(
        PlanningTraceEntry(
            stage="planning_decision",
            details={
                "planning_outcome_kind": decision.planning_outcome_kind,
                "downstream_readiness": decision.downstream_readiness,
            },
        )
    )
    return decision


def _plan_aoi(
    *,
    request: TaskPlanningRequest,
    effective_task_request: CompositionTaskRequest,
    routing_decision: CompositionTaskRoutingDecision,
    trace: list[PlanningTraceEntry],
) -> TaskPlanningDecision:
    source_v2_job_id = _extract_source_v2_job_id(request, effective_task_request)
    consumer_key = effective_task_request.consumer_key
    if not source_v2_job_id:
        return _build_insufficient_context_decision(
            routing_decision=routing_decision,
            trace=trace,
            required_hydration=["source_v2_job_id"],
            required_host_preparation=_build_aoi_host_preparation(consumer_key=consumer_key),
            decision_reason="aoi_requires_source_v2_job_id",
        )

    catalog = resolve_source_catalog(source_v2_job_id=source_v2_job_id)
    trace.append(
        PlanningTraceEntry(
            stage="source_catalog_resolution",
            details=catalog.to_trace_dict(),
        )
    )

    available_candidates = [
        candidate for candidate in catalog.candidates if candidate.candidate_state == "available"
    ]
    expected_source_families = [candidate.source_family_key for candidate in catalog.candidates]
    available_source_families = [candidate.source_family_key for candidate in available_candidates]
    expected_producer_engines = sorted({candidate.engine_key for candidate in catalog.candidates})
    allowed_profiles, blocked_profiles = evaluate_compose_profile_feasibility(catalog)

    if not available_candidates:
        return _build_aoi_selection_blocked_decision(
            routing_decision=routing_decision,
            trace=trace,
            consumer_key=consumer_key,
            source_v2_job_id=source_v2_job_id,
            reason_code="no_usable_source_families",
            reason_detail=(
                f"plan-task could not resolve any AOI source material for source_v2_job_id "
                f"'{source_v2_job_id}'."
            ),
            expected_source_families=expected_source_families,
            available_source_families=available_source_families,
            expected_producer_engines=expected_producer_engines,
            allowed_profiles=allowed_profiles,
            blocked_profiles=blocked_profiles,
            selection_trace_details=_build_aoi_selection_trace_details(
                provider_outcome="skipped_no_usable_source_families",
                blocked_reason_code="no_usable_source_families",
                blocked_reason_detail=(
                    f"plan-task could not resolve any AOI source material for source_v2_job_id "
                    f"'{source_v2_job_id}'."
                ),
                selected_sources=[],
                rejected_sources=[],
                selection_summary="",
                resolved_intent_seed="",
                legacy_profile_equivalent=None,
            ),
        )

    try:
        selection_result = _select_aoi_sources_with_llm(
            normalized_task_summary=routing_decision.normalized_task_summary,
            effective_task_request=effective_task_request,
            source_v2_job_id=source_v2_job_id,
            available_candidates=available_candidates,
            expected_source_families=expected_source_families,
        )
    except _AoiSelectionBlocked as exc:
        return _build_aoi_selection_blocked_decision(
            routing_decision=routing_decision,
            trace=trace,
            consumer_key=consumer_key,
            source_v2_job_id=source_v2_job_id,
            reason_code=exc.reason_code,
            reason_detail=exc.detail,
            expected_source_families=expected_source_families,
            available_source_families=available_source_families,
            expected_producer_engines=expected_producer_engines,
            allowed_profiles=allowed_profiles,
            blocked_profiles=blocked_profiles,
            selection_trace_details=exc.trace_details,
        )

    trace.append(
        PlanningTraceEntry(
            stage="source_selection",
            details=selection_result["trace_details"],
        )
    )

    handoff_notes = [
        "Stage 9 AOI planning resolves explicit source-family selection before transient composition handoff.",
    ]
    if not consumer_key:
        handoff_notes.append("Provide consumer_key before calling compose-from-selection.")
    handoff_notes.append(
        "allowed_profiles and blocked_profiles remain transition diagnostics only; the planner-primary proof path launches by explicit selection."
    )

    handoff_plan = AoiCompositionHandoffPlan(
        workflow_key=routing_decision.selected_workflow_key or catalog.workflow_key,
        objective_key=catalog.objective_key,
        consumer_key=consumer_key,
        source_v2_job_id=source_v2_job_id,
        selected_source_thinker_id=catalog.selected_source_thinker_id,
        selected_source_thinker_name=catalog.selected_source_thinker_name,
        selected_sources=selection_result["selected_sources"],
        rejected_sources=selection_result["rejected_sources"],
        selection_summary=selection_result["selection_summary"],
        resolved_intent_seed=selection_result["resolved_intent_seed"],
        legacy_profile_equivalent=selection_result["legacy_profile_equivalent"],
        expected_source_families=expected_source_families,
        available_source_families=available_source_families,
        expected_producer_engines=expected_producer_engines,
        allowed_profiles=allowed_profiles,
        blocked_profiles={key: value for key, value in blocked_profiles.items()},
        handoff_notes=handoff_notes,
    )

    decision = TaskPlanningDecision(
        normalized_task_summary=routing_decision.normalized_task_summary,
        routing_decision=routing_decision,
        planning_outcome_kind="aoi_composition_handoff_plan",
        planning_confidence=routing_decision.routing_confidence,
        hydration_status="satisfied",
        required_hydration=[],
        required_host_preparation=_build_aoi_host_preparation(
            consumer_key=consumer_key,
            selection_required=True,
        ),
        downstream_readiness="ready_for_aoi_compose_handoff",
        downstream_followup_contract={
            "method": "POST",
            "endpoint": "/v1/presenter/compose-from-selection",
            "selection_kind": "explicit",
            "legacy_profile_equivalent": selection_result["legacy_profile_equivalent"],
            "request_fields": {
                "workflow_key": handoff_plan.workflow_key,
                "consumer_key": consumer_key or "<required>",
                "source_v2_job_id": source_v2_job_id,
                "selection": [item.model_dump() for item in handoff_plan.selected_sources],
                "user_intent": handoff_plan.resolved_intent_seed or "<required>",
            },
        },
        hydrated_document_ids={},
        workflow_execution_plan=None,
        aoi_composition_handoff_plan=handoff_plan,
        direct_sections_composition_handoff_plan=None,
        rejected_planning_alternatives=_rejected_planning_alternatives(routing_decision),
        trace=trace,
    )
    decision.trace.append(
        PlanningTraceEntry(
            stage="planning_decision",
            details={
                "planning_outcome_kind": decision.planning_outcome_kind,
                "downstream_readiness": decision.downstream_readiness,
                "selection_summary": handoff_plan.selection_summary,
                "legacy_profile_equivalent": handoff_plan.legacy_profile_equivalent,
                "available_source_families": available_source_families,
            },
        )
    )
    return decision


def _select_aoi_sources_with_llm(
    *,
    normalized_task_summary: str,
    effective_task_request: CompositionTaskRequest,
    source_v2_job_id: str,
    available_candidates: list[Any],
    expected_source_families: list[str],
) -> dict[str, Any]:
    prompt = _build_aoi_selection_prompt(
        normalized_task_summary=normalized_task_summary,
        effective_task_request=effective_task_request,
        source_v2_job_id=source_v2_job_id,
        available_candidates=available_candidates,
        expected_source_families=expected_source_families,
    )
    raw_text, model_used = _call_aoi_selection_llm(prompt)
    try:
        parsed = parse_llm_json_response(raw_text)
    except Exception as exc:
        raise _AoiSelectionBlocked(
            "llm_invalid_output",
            f"AOI selector returned invalid JSON: {exc}",
        ) from exc
    if not isinstance(parsed, dict):
        raise _AoiSelectionBlocked(
            "llm_invalid_output",
            "AOI selector returned a non-object JSON payload.",
        )

    try:
        selected_sources = [
            AoiSelectedSourceInput.model_validate(item)
            for item in parsed.get("selected_sources", [])
        ]
        rejected_sources = [
            AoiRejectedSourceInput.model_validate(item)
            for item in parsed.get("rejected_sources", [])
        ]
    except Exception as exc:
        raise _AoiSelectionBlocked(
            "llm_selection_failed_validation",
            f"AOI selector returned invalid selection items: {exc}",
            trace_details=_build_aoi_selection_trace_details(
                provider_outcome="llm_selection_failed_validation",
                model_used=model_used,
                blocked_reason_code="llm_selection_failed_validation",
                blocked_reason_detail=f"AOI selector returned invalid selection items: {exc}",
            ),
        ) from exc

    selection_summary = str(parsed.get("selection_summary", "")).strip()
    resolved_intent_seed = str(parsed.get("resolved_intent_seed", "")).strip()
    if not selection_summary:
        raise _AoiSelectionBlocked(
            "llm_selection_failed_validation",
            "AOI selector omitted selection_summary.",
            trace_details=_build_aoi_selection_trace_details(
                provider_outcome="llm_selection_failed_validation",
                model_used=model_used,
                blocked_reason_code="llm_selection_failed_validation",
                blocked_reason_detail="AOI selector omitted selection_summary.",
                selected_sources=[item.model_dump() for item in selected_sources],
                rejected_sources=[item.model_dump() for item in rejected_sources],
                selection_summary="",
                resolved_intent_seed=resolved_intent_seed,
            ),
        )
    if not resolved_intent_seed:
        raise _AoiSelectionBlocked(
            "llm_selection_failed_validation",
            "AOI selector omitted resolved_intent_seed.",
            trace_details=_build_aoi_selection_trace_details(
                provider_outcome="llm_selection_failed_validation",
                model_used=model_used,
                blocked_reason_code="llm_selection_failed_validation",
                blocked_reason_detail="AOI selector omitted resolved_intent_seed.",
                selected_sources=[item.model_dump() for item in selected_sources],
                rejected_sources=[item.model_dump() for item in rejected_sources],
                selection_summary=selection_summary,
                resolved_intent_seed="",
            ),
        )

    try:
        _validate_aoi_selection_payload(
            selected_sources=selected_sources,
            rejected_sources=rejected_sources,
            available_candidates=available_candidates,
        )
    except _AoiSelectionBlocked as exc:
        raise _AoiSelectionBlocked(
            exc.reason_code,
            exc.detail,
            trace_details=_build_aoi_selection_trace_details(
                provider_outcome=exc.reason_code,
                model_used=model_used,
                blocked_reason_code=exc.reason_code,
                blocked_reason_detail=exc.detail,
                selected_sources=[item.model_dump() for item in selected_sources],
                rejected_sources=[item.model_dump() for item in rejected_sources],
                selection_summary=selection_summary,
                resolved_intent_seed=resolved_intent_seed,
            ),
        ) from exc

    legacy_profile_equivalent = _infer_legacy_profile_equivalent(
        tuple(item.source_family_key for item in sorted(selected_sources, key=lambda item: item.selection_rank))
    )
    return {
        "selected_sources": selected_sources,
        "rejected_sources": rejected_sources,
        "selection_summary": selection_summary,
        "resolved_intent_seed": resolved_intent_seed,
        "legacy_profile_equivalent": legacy_profile_equivalent,
        "trace_details": {
            **_build_aoi_selection_trace_details(
                provider_outcome="success",
                model_used=model_used,
                selected_sources=[item.model_dump() for item in selected_sources],
                rejected_sources=[item.model_dump() for item in rejected_sources],
                selection_summary=selection_summary,
                resolved_intent_seed=resolved_intent_seed,
                legacy_profile_equivalent=legacy_profile_equivalent,
            ),
        },
    }


def _call_aoi_selection_llm(prompt: str) -> tuple[str, str]:
    timeout_s = _get_aoi_selection_timeout_s()
    client = get_anthropic_client(
        read_timeout_s=timeout_s,
        max_retries=AOI_SELECTION_MAX_RETRIES,
    )
    if client is None:
        raise _AoiSelectionBlocked(
            "llm_provider_failure",
            "AOI selector LLM is unavailable. Set ANTHROPIC_API_KEY to enable planner-primary AOI selection.",
            trace_details=_build_aoi_selection_trace_details(
                provider_outcome="llm_provider_failure",
                blocked_reason_code="llm_provider_failure",
                blocked_reason_detail=(
                    "AOI selector LLM is unavailable. Set ANTHROPIC_API_KEY to enable planner-primary AOI selection."
                ),
                timeout_s=timeout_s,
            ),
        )

    try:
        import anthropic
    except ImportError:  # pragma: no cover - get_anthropic_client already guards this path.
        anthropic = None  # type: ignore[assignment]

    try:
        response = client.messages.create(
            model=AOI_SELECTION_MODEL,
            max_tokens=1200,
            system=(
                "You are selecting AOI source families for a bounded transient composition handoff.\n"
                "Return ONLY JSON. Reason about individual family relevance to the task.\n"
                "Do not infer or mention preset profiles as the primary decision rule."
            ),
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:
        exception_class_name = type(exc).__name__
        timeout_exceptions: tuple[type[BaseException], ...] = (httpx.TimeoutException, TimeoutError)
        provider_exceptions: tuple[type[BaseException], ...] = ()
        if anthropic is not None:
            timeout_exceptions = (anthropic.APITimeoutError, *timeout_exceptions)
            provider_exceptions = (anthropic.APIConnectionError,)

        if isinstance(exc, timeout_exceptions):
            raise _AoiSelectionBlocked(
                "llm_timeout",
                f"AOI selector timed out after {timeout_s:.0f}s.",
                trace_details=_build_aoi_selection_trace_details(
                    provider_outcome="llm_timeout",
                    blocked_reason_code="llm_timeout",
                    blocked_reason_detail=f"AOI selector timed out after {timeout_s:.0f}s.",
                    timeout_s=timeout_s,
                    exception_class_name=exception_class_name,
                ),
            ) from exc
        if isinstance(exc, provider_exceptions):
            raise _AoiSelectionBlocked(
                "llm_provider_failure",
                f"AOI selector provider call failed: {exc}",
                trace_details=_build_aoi_selection_trace_details(
                    provider_outcome="llm_provider_failure",
                    blocked_reason_code="llm_provider_failure",
                    blocked_reason_detail=f"AOI selector provider call failed: {exc}",
                    timeout_s=timeout_s,
                    exception_class_name=exception_class_name,
                ),
            ) from exc
        raise _AoiSelectionBlocked(
            "llm_provider_failure",
            f"AOI selector provider call failed: {exc}",
            trace_details=_build_aoi_selection_trace_details(
                provider_outcome="llm_provider_failure",
                blocked_reason_code="llm_provider_failure",
                blocked_reason_detail=f"AOI selector provider call failed: {exc}",
                timeout_s=timeout_s,
                exception_class_name=exception_class_name,
            ),
        ) from exc

    raw_parts = [
        getattr(block, "text", "")
        for block in getattr(response, "content", []) or []
        if getattr(block, "text", "")
    ]
    raw_text = "\n".join(raw_parts).strip()
    if not raw_text:
        raise _AoiSelectionBlocked(
            "llm_invalid_output",
            "AOI selector returned an empty response.",
            trace_details=_build_aoi_selection_trace_details(
                provider_outcome="llm_invalid_output",
                model_used=AOI_SELECTION_MODEL,
                blocked_reason_code="llm_invalid_output",
                blocked_reason_detail="AOI selector returned an empty response.",
                timeout_s=timeout_s,
            ),
        )
    return raw_text, AOI_SELECTION_MODEL


def _build_aoi_selection_prompt(
    *,
    normalized_task_summary: str,
    effective_task_request: CompositionTaskRequest,
    source_v2_job_id: str,
    available_candidates: list[Any],
    expected_source_families: list[str],
) -> str:
    available_catalog = [
        {
            "source_family_key": candidate.source_family_key,
            "title": candidate.title,
            "engine_key": candidate.engine_key,
            "composition_role_hint": candidate.composition_role_hint,
            "summary_metadata": candidate.summary_metadata,
        }
        for candidate in available_candidates
    ]
    task_context = {
        "task": normalized_task_summary,
        "audience": effective_task_request.audience,
        "desired_depth": effective_task_request.desired_depth,
        "style_expectations": effective_task_request.style_expectations,
        "workflow_hint": effective_task_request.workflow_hint,
        "source_v2_job_id": source_v2_job_id,
    }
    return (
        "Select the best AOI source families for one bounded transient composition handoff.\n\n"
        "Return JSON with this exact shape:\n"
        "{\n"
        '  "selected_sources": [{"source_family_key": "...", "selection_rank": 1, "rationale": "..."}],\n'
        '  "rejected_sources": [{"source_family_key": "...", "rejection_reason": "..."}],\n'
        '  "selection_summary": "...",\n'
        '  "resolved_intent_seed": "..."\n'
        "}\n\n"
        "Rules:\n"
        "- Choose from AVAILABLE_FAMILIES only.\n"
        "- Think in terms of individual family relevance to the task, not preset bundles.\n"
        "- selection_rank must start at 1 and be contiguous.\n"
        "- Select at least one family.\n"
        "- Reject every available family not selected.\n"
        "- resolved_intent_seed should be a concise non-empty compose intent the host can prefill and the user may edit.\n"
        "- Do not output markdown fences.\n\n"
        f"TASK_CONTEXT:\n{json.dumps(task_context, ensure_ascii=False, indent=2, sort_keys=True)}\n\n"
        f"EXPECTED_SOURCE_FAMILIES:\n{json.dumps(expected_source_families, ensure_ascii=False, indent=2)}\n\n"
        f"AVAILABLE_FAMILIES:\n{json.dumps(available_catalog, ensure_ascii=False, indent=2, sort_keys=True)}\n"
    )


def _validate_aoi_selection_payload(
    *,
    selected_sources: list[AoiSelectedSourceInput],
    rejected_sources: list[AoiRejectedSourceInput],
    available_candidates: list[Any],
) -> None:
    if not selected_sources:
        raise _AoiSelectionBlocked(
            "llm_selection_failed_validation",
            "AOI selector did not choose any source families.",
        )

    available_families = {candidate.source_family_key for candidate in available_candidates}
    selected_families = [item.source_family_key for item in selected_sources]
    rejected_families = [item.source_family_key for item in rejected_sources]

    if any(not item.rationale.strip() for item in selected_sources):
        raise _AoiSelectionBlocked(
            "llm_selection_failed_validation",
            "AOI selector returned blank rationale text in selected_sources.",
        )
    if any(not item.rejection_reason.strip() for item in rejected_sources):
        raise _AoiSelectionBlocked(
            "llm_selection_failed_validation",
            "AOI selector returned blank rejection_reason text in rejected_sources.",
        )
    if len(selected_families) != len(set(selected_families)):
        raise _AoiSelectionBlocked(
            "llm_selection_failed_validation",
            "AOI selector duplicated selected source families.",
        )
    if len(rejected_families) != len(set(rejected_families)):
        raise _AoiSelectionBlocked(
            "llm_selection_failed_validation",
            "AOI selector duplicated rejected source families.",
        )
    if any(family not in available_families for family in selected_families):
        raise _AoiSelectionBlocked(
            "llm_selection_failed_validation",
            "AOI selector referenced unavailable source families in selected_sources.",
        )
    if any(family not in available_families for family in rejected_families):
        raise _AoiSelectionBlocked(
            "llm_selection_failed_validation",
            "AOI selector referenced unavailable source families in rejected_sources.",
        )
    if set(selected_families) & set(rejected_families):
        raise _AoiSelectionBlocked(
            "llm_selection_failed_validation",
            "AOI selector overlapped selected and rejected source families.",
        )
    selection_ranks = sorted(item.selection_rank for item in selected_sources)
    if selection_ranks != list(range(1, len(selected_sources) + 1)):
        raise _AoiSelectionBlocked(
            "llm_selection_failed_validation",
            "AOI selector produced non-contiguous selection_rank values.",
        )
    expected_rejected_families = available_families - set(selected_families)
    actual_rejected_families = set(rejected_families)
    if actual_rejected_families != expected_rejected_families:
        missing = sorted(expected_rejected_families - actual_rejected_families)
        unexpected = sorted(actual_rejected_families - expected_rejected_families)
        detail_parts: list[str] = []
        if missing:
            detail_parts.append(f"missing rejected_sources for: {', '.join(missing)}")
        if unexpected:
            detail_parts.append(f"unexpected rejected_sources: {', '.join(unexpected)}")
        raise _AoiSelectionBlocked(
            "llm_selection_failed_validation",
            "AOI selector rejected_sources coverage mismatch"
            + (f" ({'; '.join(detail_parts)})" if detail_parts else "."),
        )


def _infer_legacy_profile_equivalent(
    selected_families: tuple[str, ...],
) -> Optional[str]:
    for profile, profile_families in _AOI_PROFILE_FAMILY_SETS.items():
        if selected_families == profile_families:
            return profile
    return None


def _extract_source_v2_job_id(
    request: TaskPlanningRequest,
    effective_task_request: CompositionTaskRequest,
) -> Optional[str]:
    if request.planning_context is not None and request.planning_context.context_mode == "saved_result":
        context = cast(SavedResultPlanningContext, request.planning_context)
        if context.source_v2_job_id:
            return context.source_v2_job_id

    source_constraints = effective_task_request.source_constraints
    if source_constraints is None or source_constraints.source_mode != "saved_result":
        return None
    return cast(Any, source_constraints).source_v2_job_id


def _required_hydration_from_request(
    effective_task_request: CompositionTaskRequest,
    routing_decision: CompositionTaskRoutingDecision,
) -> list[str]:
    if routing_decision.selected_objective_key == "influence_thematic":
        return ["source_v2_job_id"]

    source_constraints = effective_task_request.source_constraints
    if source_constraints is None:
        return ["planning_context.saved_result or planning_context.registered_corpus or planning_context.inline_documents"]
    if source_constraints.source_mode == "saved_result":
        return ["source_v2_job_id"]
    if source_constraints.source_mode == "registered_corpus":
        return ["planning_context.registered_corpus"]
    if source_constraints.source_mode == "inline_documents":
        return [
            "planning_context.inline_documents.target_work_text",
            "planning_context.inline_documents.prior_works",
        ]
    return ["planning_context.saved_result or planning_context.registered_corpus or planning_context.inline_documents"]


def _remaining_host_preparation(
    *,
    effective_task_request: CompositionTaskRequest,
    routing_decision: CompositionTaskRoutingDecision,
) -> list[str]:
    if routing_decision.selected_objective_key == "influence_thematic":
        return _build_aoi_host_preparation(consumer_key=effective_task_request.consumer_key)
    if (
        routing_decision.selected_objective_key == "genealogical"
        and getattr(effective_task_request.source_constraints, "source_mode", None) == "saved_result"
    ):
        return _build_direct_sections_host_preparation(
            consumer_key=effective_task_request.consumer_key,
            lowering_required=False,
        )
    return []


def _build_aoi_host_preparation(
    *,
    consumer_key: Optional[str],
    selection_required: bool = False,
) -> list[str]:
    steps: list[str] = []
    if not consumer_key:
        steps.append("Provide consumer_key for the downstream AOI compose call.")
    if selection_required:
        steps.append(
            "Carry planner-selected source families and the resolved intent seed into compose-from-selection."
        )
    else:
        steps.append("Call plan-task with saved_result planning context before launching planner-backed AOI compose.")
    return steps


def _build_direct_sections_host_preparation(
    *,
    consumer_key: Optional[str],
    lowering_required: bool,
) -> list[str]:
    steps: list[str] = []
    if not consumer_key:
        steps.append("Provide consumer_key for the downstream direct-sections compose call.")
    if lowering_required:
        steps.append(
            "Lower the persisted direct-sections handoff into compose-from-intent without host-side semantic reconstruction."
        )
    else:
        steps.append(
            "Call plan-task with saved_result planning context before launching planner-backed direct-sections compose."
        )
    return steps


def _build_aoi_selection_blocked_decision(
    *,
    routing_decision: CompositionTaskRoutingDecision,
    trace: list[PlanningTraceEntry],
    consumer_key: Optional[str],
    source_v2_job_id: str,
    reason_code: str,
    reason_detail: str,
    expected_source_families: list[str],
    available_source_families: list[str],
    expected_producer_engines: list[str],
    allowed_profiles: list[str],
    blocked_profiles: dict[str, list[str]],
    selection_trace_details: Optional[dict[str, Any]] = None,
) -> TaskPlanningDecision:
    blocked_trace = list(trace)
    if selection_trace_details is not None:
        blocked_trace.append(
            PlanningTraceEntry(
                stage="source_selection",
                details=selection_trace_details,
            )
        )
    decision = TaskPlanningDecision(
        normalized_task_summary=routing_decision.normalized_task_summary,
        routing_decision=routing_decision,
        planning_outcome_kind="aoi_selection_blocked",
        planning_confidence=routing_decision.routing_confidence,
        hydration_status="satisfied",
        required_hydration=[],
        required_host_preparation=_build_aoi_host_preparation(
            consumer_key=consumer_key,
            selection_required=False,
        ),
        downstream_readiness="blocked_for_aoi_selection",
        downstream_followup_contract={
            "method": None,
            "endpoint": None,
            "blocked_reason_code": reason_code,
            "blocked_reason_detail": reason_detail,
            "expected_source_families": expected_source_families,
            "available_source_families": available_source_families,
            "expected_producer_engines": expected_producer_engines,
            "allowed_profiles": allowed_profiles,
            "blocked_profiles": blocked_profiles,
            "request_fields": {
                "workflow_key": routing_decision.selected_workflow_key,
                "consumer_key": consumer_key or "<required>",
                "source_v2_job_id": source_v2_job_id,
            },
        },
        hydrated_document_ids={},
        workflow_execution_plan=None,
        aoi_composition_handoff_plan=None,
        direct_sections_composition_handoff_plan=None,
        aoi_selection_blocked_reason_code=reason_code,
        aoi_selection_blocked_reason_detail=reason_detail,
        rejected_planning_alternatives=_rejected_planning_alternatives(routing_decision),
        trace=blocked_trace + [
            PlanningTraceEntry(
                stage="planning_decision",
                details={
                    "planning_outcome_kind": "aoi_selection_blocked",
                    "downstream_readiness": "blocked_for_aoi_selection",
                    "blocked_reason_code": reason_code,
                    "blocked_reason_detail": reason_detail,
                },
            )
        ],
    )
    return decision


def _build_aoi_selection_trace_details(
    *,
    provider_outcome: str,
    model_used: Optional[str] = None,
    blocked_reason_code: Optional[str] = None,
    blocked_reason_detail: Optional[str] = None,
    selected_sources: Optional[list[dict[str, Any]]] = None,
    rejected_sources: Optional[list[dict[str, Any]]] = None,
    selection_summary: Optional[str] = None,
    resolved_intent_seed: Optional[str] = None,
    legacy_profile_equivalent: Optional[str] = None,
    timeout_s: Optional[float] = None,
    exception_class_name: Optional[str] = None,
) -> dict[str, Any]:
    details: dict[str, Any] = {
        "prompt_version": AOI_SELECTION_PROMPT_VERSION,
        "model_used": model_used or AOI_SELECTION_MODEL,
        "timeout_s": timeout_s if timeout_s is not None else _get_aoi_selection_timeout_s(),
        "retry_policy": {"max_retries": AOI_SELECTION_MAX_RETRIES},
        "provider_outcome": provider_outcome,
        "validator_version": AOI_SELECTION_VALIDATOR_VERSION,
    }
    if exception_class_name is not None:
        details["exception_class_name"] = exception_class_name
    if blocked_reason_code is not None:
        details["blocked_reason_code"] = blocked_reason_code
    if blocked_reason_detail is not None:
        details["blocked_reason_detail"] = blocked_reason_detail
    if selected_sources is not None:
        details["selected_sources"] = selected_sources
    if rejected_sources is not None:
        details["rejected_sources"] = rejected_sources
    if selection_summary is not None:
        details["selection_summary"] = selection_summary
    if resolved_intent_seed is not None:
        details["resolved_intent_seed"] = resolved_intent_seed
    if legacy_profile_equivalent is not None:
        details["legacy_profile_equivalent"] = legacy_profile_equivalent
    return details


def _rejected_planning_alternatives(
    routing_decision: CompositionTaskRoutingDecision,
) -> list[RejectedPlanningAlternative]:
    return [
        RejectedPlanningAlternative(
            alternative_key=candidate.objective_key,
            rejection_reason=candidate.rejection_reason,
            details=candidate.details,
        )
        for candidate in routing_decision.rejected_candidates
    ]


def _build_insufficient_context_decision(
    *,
    routing_decision: CompositionTaskRoutingDecision,
    trace: list[PlanningTraceEntry],
    required_hydration: list[str],
    required_host_preparation: list[str],
    decision_reason: str,
) -> TaskPlanningDecision:
    decision = TaskPlanningDecision(
        normalized_task_summary=routing_decision.normalized_task_summary,
        routing_decision=routing_decision,
        planning_outcome_kind="insufficient_context",
        planning_confidence=routing_decision.routing_confidence,
        hydration_status="required",
        required_hydration=required_hydration,
        required_host_preparation=required_host_preparation,
        downstream_readiness="needs_more_context",
        downstream_followup_contract={"method": None, "endpoint": None},
        hydrated_document_ids={},
        workflow_execution_plan=None,
        aoi_composition_handoff_plan=None,
        direct_sections_composition_handoff_plan=None,
        rejected_planning_alternatives=_rejected_planning_alternatives(routing_decision),
        trace=trace,
    )
    decision.trace.append(
        PlanningTraceEntry(
            stage="planning_decision",
            details={
                "planning_outcome_kind": decision.planning_outcome_kind,
                "downstream_readiness": decision.downstream_readiness,
                "decision_reason": decision_reason,
            },
        )
    )
    return decision


def _build_unsupported_decision(
    *,
    routing_decision: CompositionTaskRoutingDecision,
    trace: list[PlanningTraceEntry],
    decision_reason: str,
) -> TaskPlanningDecision:
    decision = TaskPlanningDecision(
        normalized_task_summary=routing_decision.normalized_task_summary,
        routing_decision=routing_decision,
        planning_outcome_kind="unsupported",
        planning_confidence=routing_decision.routing_confidence,
        hydration_status="unresolved",
        required_hydration=[],
        required_host_preparation=[],
        downstream_readiness="unsupported",
        downstream_followup_contract={"method": None, "endpoint": None},
        hydrated_document_ids={},
        workflow_execution_plan=None,
        aoi_composition_handoff_plan=None,
        direct_sections_composition_handoff_plan=None,
        rejected_planning_alternatives=_rejected_planning_alternatives(routing_decision),
        trace=trace,
    )
    decision.trace.append(
        PlanningTraceEntry(
            stage="planning_decision",
            details={
                "planning_outcome_kind": decision.planning_outcome_kind,
                "downstream_readiness": decision.downstream_readiness,
                "decision_reason": decision_reason,
            },
        )
    )
    return decision
