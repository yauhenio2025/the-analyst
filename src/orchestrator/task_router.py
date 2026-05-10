"""Deterministic advisory router for composition-facing tasks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, cast

from src.objectives.registry import get_objective
from src.orchestrator.task_routing_schemas import (
    CompositionTaskRequest,
    CompositionTaskRoutingDecision,
    CompositionTaskSourceConstraints,
    LaunchContractKind,
    RejectedRoutingCandidate,
    RoutingConfidence,
    RoutingTraceEntry,
    RoutingOutcome,
    SourceSufficiencyStatus,
)

SUPPORTED_OBJECTIVES = ("influence_thematic", "genealogical")

AOI_SIGNALS = (
    "anxiety of influence",
    "aoi",
    "source thinker",
    "misreading",
    "revision",
    "appropriation",
    "engagement",
    "thematic influence",
    "influence",
)
GENEALOGY_SIGNALS = (
    "genealogy",
    "lineage",
    "precursor",
    "inheritance",
    "descent",
    "emergence",
    "concept evolution",
    "conditions of possibility",
)


@dataclass(frozen=True)
class CandidateAssessment:
    objective_key: str
    workflow_key: str | None
    signal_score: int
    positive_signals: list[str]
    source_mode: str | None
    source_mode_compatible: bool
    source_sufficiency_status: Literal["sufficient", "insufficient"]
    sufficiency_reasons: list[str]


def route_composition_task(request: CompositionTaskRequest) -> CompositionTaskRoutingDecision:
    """Deterministically choose a downstream family for a composition-facing task."""

    normalized_task = " ".join(request.task.split())
    trace: list[RoutingTraceEntry] = [
        RoutingTraceEntry(
            stage="task_normalization",
            details={
                "normalized_task_summary": normalized_task,
                "audience": request.audience,
                "desired_depth": request.desired_depth,
                "style_expectations": request.style_expectations,
            },
        )
    ]

    if request.objective_hint is not None:
        objective = get_objective(request.objective_hint)
        if objective is None or request.objective_hint not in SUPPORTED_OBJECTIVES:
            valid_keys = ", ".join(SUPPORTED_OBJECTIVES)
            raise ValueError(
                f"Unknown objective_hint: '{request.objective_hint}'. Supported keys: {valid_keys}"
            )

    assessments = [_assess_candidate(request, objective_key) for objective_key in SUPPORTED_OBJECTIVES]
    trace.append(
        RoutingTraceEntry(
            stage="objective_candidate_scoring",
            details={
                "objective_hint": request.objective_hint,
                "objective_hint_status": _objective_hint_status(request),
                "workflow_hint": request.workflow_hint,
                "workflow_hint_status": "pending",
                "candidates": [
                    {
                        "objective_key": assessment.objective_key,
                        "workflow_key": assessment.workflow_key,
                        "signal_score": assessment.signal_score,
                        "positive_signals": assessment.positive_signals,
                        "source_mode": assessment.source_mode,
                        "source_mode_compatible": assessment.source_mode_compatible,
                    }
                    for assessment in assessments
                ],
            },
        )
    )

    selected_assessment, outcome_kind = _select_assessment(request, assessments)
    trace[-1].details["workflow_hint_status"] = _workflow_hint_status(request, selected_assessment)

    trace.append(
        RoutingTraceEntry(
            stage="source_sufficiency_evaluation",
            details={
                "selected_objective_key": selected_assessment.objective_key if selected_assessment else None,
                "selected_workflow_key": selected_assessment.workflow_key if selected_assessment else None,
                "source_mode": getattr(request.source_constraints, "source_mode", None),
                "source_sufficiency_status": _derive_source_sufficiency_status(
                    outcome_kind,
                    selected_assessment,
                ),
                "sufficiency_reasons": selected_assessment.sufficiency_reasons if selected_assessment else [],
            },
        )
    )

    decision = _build_decision(request, normalized_task, assessments, selected_assessment, outcome_kind, trace)
    decision.trace.append(
        RoutingTraceEntry(
            stage="routing_decision",
            details={
                "routing_outcome": decision.routing_outcome,
                "routing_confidence": decision.routing_confidence,
                "launch_contract_kind": decision.launch_contract_kind,
                "selected_objective_key": decision.selected_objective_key,
                "selected_workflow_key": decision.selected_workflow_key,
                "required_fields": decision.required_fields,
                "required_host_preparation": decision.required_host_preparation,
            },
        )
    )
    return decision


def _assess_candidate(
    request: CompositionTaskRequest,
    objective_key: str,
) -> CandidateAssessment:
    objective = get_objective(objective_key)
    workflow_key = objective.baseline_workflow_key if objective else None
    normalized_task = request.task.lower()
    source_constraints = request.source_constraints
    source_mode = getattr(source_constraints, "source_mode", None)
    positive_signals = _collect_positive_signals(normalized_task, objective_key)
    source_mode_compatible = _is_source_mode_compatible(objective_key, source_mode)
    source_sufficiency_status, sufficiency_reasons = _assess_source_sufficiency(objective_key, source_constraints)
    return CandidateAssessment(
        objective_key=objective_key,
        workflow_key=workflow_key,
        signal_score=len(positive_signals),
        positive_signals=positive_signals,
        source_mode=source_mode,
        source_mode_compatible=source_mode_compatible,
        source_sufficiency_status=source_sufficiency_status,
        sufficiency_reasons=sufficiency_reasons,
    )


def _collect_positive_signals(normalized_task: str, objective_key: str) -> list[str]:
    signal_pool = AOI_SIGNALS if objective_key == "influence_thematic" else GENEALOGY_SIGNALS
    return [signal for signal in signal_pool if signal in normalized_task]


def _is_source_mode_compatible(objective_key: str, source_mode: str | None) -> bool:
    if objective_key == "influence_thematic":
        return source_mode in {None, "saved_result"}
    return source_mode in {None, "saved_result", "registered_corpus", "inline_documents"}


def _assess_source_sufficiency(
    objective_key: str,
    source_constraints: CompositionTaskSourceConstraints | None,
) -> tuple[Literal["sufficient", "insufficient"], list[str]]:
    if objective_key == "influence_thematic":
        return _assess_aoi_source_sufficiency(source_constraints)
    return _assess_genealogy_source_sufficiency(source_constraints)


def _assess_aoi_source_sufficiency(
    source_constraints: CompositionTaskSourceConstraints | None,
) -> tuple[Literal["sufficient", "insufficient"], list[str]]:
    if source_constraints is None:
        return "insufficient", ["AOI routing requires saved_result source constraints."]
    if source_constraints.source_mode != "saved_result":
        return "insufficient", ["AOI routing is only compatible with saved_result source mode."]
    if source_constraints.source_v2_job_id:
        return "sufficient", []
    if source_constraints.source_analysis_id:
        return "sufficient", ["Resolve source_v2_job_id from local saved-result identity before launch."]
    return "insufficient", [
        "AOI routing requires source_v2_job_id or source_analysis_id in saved_result source constraints."
    ]


def _assess_genealogy_source_sufficiency(
    source_constraints: CompositionTaskSourceConstraints | None,
) -> tuple[Literal["sufficient", "insufficient"], list[str]]:
    if source_constraints is None:
        return "insufficient", ["Genealogy routing requires saved_result, registered_corpus, or inline_documents source constraints."]
    if source_constraints.source_mode == "saved_result":
        if source_constraints.source_v2_job_id:
            return "sufficient", []
        if source_constraints.source_analysis_id:
            return "insufficient", [
                "Resolve source_v2_job_id from local saved-result identity before launching genealogy direct-sections planning.",
            ]
        return "insufficient", [
            "saved_result genealogy routing requires source_v2_job_id."
        ]
    if source_constraints.source_mode == "registered_corpus":
        reasons: list[str] = []
        if source_constraints.prior_work_external_doc_keys_count <= 0:
            reasons.append("registered_corpus routing requires at least one prior work external doc key.")
        if reasons:
            return "insufficient", reasons
        return "sufficient", []
    if source_constraints.source_mode == "inline_documents":
        reasons = []
        if not source_constraints.has_target_work_text:
            reasons.append("inline_documents routing requires target work text.")
        if source_constraints.prior_work_count <= 0:
            reasons.append("inline_documents routing requires at least one prior work.")
        if reasons:
            return "insufficient", reasons
        return "sufficient", []
    return "insufficient", ["Genealogy routing received an unsupported source mode."]


def _objective_hint_status(request: CompositionTaskRequest) -> str:
    if request.objective_hint is None:
        return "not_provided"
    return "provided_and_validated"


def _workflow_hint_status(
    request: CompositionTaskRequest,
    selected_assessment: CandidateAssessment | None,
) -> str:
    if request.workflow_hint is None:
        return "not_provided"
    if selected_assessment is None:
        return "provided_but_no_objective_selected"
    if request.workflow_hint == selected_assessment.workflow_key:
        return "accepted_as_consistent"
    return "rejected_as_inconsistent"


def _select_assessment(
    request: CompositionTaskRequest,
    assessments: list[CandidateAssessment],
) -> tuple[CandidateAssessment | None, str]:
    by_key = {assessment.objective_key: assessment for assessment in assessments}

    if request.objective_hint is not None:
        selected = by_key[request.objective_hint]
        if not selected.source_mode_compatible:
            return selected, "unsupported_source_mismatch"
        if selected.source_sufficiency_status != "sufficient":
            return selected, "unsupported_insufficient"
        return selected, "supported"

    ranked = sorted(assessments, key=lambda item: item.signal_score, reverse=True)
    best = ranked[0]
    second = ranked[1]

    if best.signal_score <= 0:
        return None, "unsupported_ambiguous"
    if best.signal_score == second.signal_score:
        return None, "unsupported_ambiguous"
    if not best.source_mode_compatible:
        return best, "unsupported_source_mismatch"
    if best.source_sufficiency_status != "sufficient":
        return best, "unsupported_insufficient"
    return best, "supported"


def _build_decision(
    request: CompositionTaskRequest,
    normalized_task: str,
    assessments: list[CandidateAssessment],
    selected_assessment: CandidateAssessment | None,
    outcome_kind: str,
    trace: list[RoutingTraceEntry],
) -> CompositionTaskRoutingDecision:
    source_sufficiency_status = _derive_source_sufficiency_status(outcome_kind, selected_assessment)
    rejected = _build_rejected_candidates(assessments, selected_assessment, outcome_kind)

    if selected_assessment is None:
        return CompositionTaskRoutingDecision(
            normalized_task_summary=normalized_task,
            routing_outcome="unsupported",
            routing_confidence="low",
            launch_contract_kind="unsupported",
            source_sufficiency_status=source_sufficiency_status,
            required_fields=[],
            required_host_preparation=[],
            downstream_launch_contract={"method": None, "endpoint": None},
            rejected_candidates=rejected,
            trace=trace,
        )

    if outcome_kind != "supported":
        return CompositionTaskRoutingDecision(
            normalized_task_summary=normalized_task,
            selected_objective_key=selected_assessment.objective_key,
            selected_workflow_key=selected_assessment.workflow_key,
            routing_outcome="unsupported",
            routing_confidence="low",
            launch_contract_kind="unsupported",
            source_sufficiency_status=source_sufficiency_status,
            required_fields=[],
            required_host_preparation=[],
            downstream_launch_contract={"method": None, "endpoint": None},
            rejected_candidates=rejected,
            trace=trace,
        )

    routing_outcome, launch_contract_kind = _supported_outcome(selected_assessment, request.source_constraints)
    required_fields, required_host_preparation, downstream_launch_contract = _build_launch_contract(
        request,
        selected_assessment,
        launch_contract_kind,
    )

    return CompositionTaskRoutingDecision(
        normalized_task_summary=normalized_task,
        selected_objective_key=selected_assessment.objective_key,
        selected_workflow_key=selected_assessment.workflow_key,
        routing_outcome=routing_outcome,
        routing_confidence=_derive_routing_confidence(request, selected_assessment),
        launch_contract_kind=launch_contract_kind,
        source_sufficiency_status=source_sufficiency_status,
        required_fields=required_fields,
        required_host_preparation=required_host_preparation,
        downstream_launch_contract=downstream_launch_contract,
        rejected_candidates=rejected,
        trace=trace,
    )


def _derive_source_sufficiency_status(
    outcome_kind: str,
    selected_assessment: CandidateAssessment | None,
) -> SourceSufficiencyStatus:
    if outcome_kind == "unsupported_ambiguous":
        return "ambiguous"
    if selected_assessment is None:
        return "ambiguous"
    return cast(SourceSufficiencyStatus, selected_assessment.source_sufficiency_status)


def _build_rejected_candidates(
    assessments: list[CandidateAssessment],
    selected_assessment: CandidateAssessment | None,
    outcome_kind: str,
) -> list[RejectedRoutingCandidate]:
    rejected: list[RejectedRoutingCandidate] = []
    for assessment in assessments:
        if selected_assessment is not None and outcome_kind == "supported" and assessment.objective_key == selected_assessment.objective_key:
            continue

        details = []
        if assessment.positive_signals:
            details.append(f"positive_signals={assessment.positive_signals}")
        if not assessment.source_mode_compatible:
            details.append(f"source_mode '{assessment.source_mode}' is incompatible")
        if assessment.source_sufficiency_status != "sufficient":
            details.extend(assessment.sufficiency_reasons)

        if outcome_kind == "unsupported_ambiguous":
            reason = "ambiguous_or_weak_task_signals"
        elif selected_assessment is not None and assessment.objective_key == selected_assessment.objective_key:
            reason = "selected_candidate_failed_contract_checks"
        elif selected_assessment is not None and assessment.signal_score < selected_assessment.signal_score:
            reason = "lower_signal_score_than_selected_candidate"
        else:
            reason = "not_selected"

        rejected.append(
            RejectedRoutingCandidate(
                objective_key=assessment.objective_key,
                rejection_reason=reason,
                details=details,
            )
        )
    return rejected


def _supported_outcome(
    selected_assessment: CandidateAssessment,
    source_constraints: CompositionTaskSourceConstraints | None,
) -> tuple[RoutingOutcome, LaunchContractKind]:
    if selected_assessment.objective_key == "influence_thematic":
        return "aoi_transient_source_backed", "planner.aoi_compose_handoff"
    if source_constraints is not None and source_constraints.source_mode == "saved_result":
        return "genealogy_transient_source_backed", "planner.direct_sections_compose_handoff"
    if source_constraints is not None and source_constraints.source_mode == "registered_corpus":
        return "genealogy_job_backed", "orchestrator.analyze_by_ref"
    return "genealogy_job_backed", "orchestrator.analyze"


def _build_launch_contract(
    request: CompositionTaskRequest,
    selected_assessment: CandidateAssessment,
    launch_contract_kind: LaunchContractKind,
) -> tuple[list[str], list[str], dict[str, Any]]:
    if launch_contract_kind == "planner.aoi_compose_handoff":
        source_constraints = cast(Any, request.source_constraints)
        required_host_preparation = []
        if not request.consumer_key:
            required_host_preparation.append("Provide consumer_key for the AOI planner handoff.")
        if getattr(source_constraints, "source_v2_job_id", None) is None:
            required_host_preparation.append(
                "Resolve source_v2_job_id from local saved-result identity before calling plan-task."
            )
        required_host_preparation.append(
            "Call plan-task with saved_result planning context to resolve AOI source selection before launch."
        )
        return (
            ["workflow_key", "consumer_key", "source_v2_job_id"],
            required_host_preparation,
            {
                "method": "POST",
                "endpoint": "/v1/orchestrator/plan-task",
                "request_fields": {
                    "task_request.workflow_hint": selected_assessment.workflow_key,
                    "task_request.consumer_key": request.consumer_key or "<required>",
                    "planning_context.context_mode": "saved_result",
                    "planning_context.source_v2_job_id": getattr(source_constraints, "source_v2_job_id", None) or "<required>",
                },
            },
        )

    if launch_contract_kind == "planner.direct_sections_compose_handoff":
        source_constraints = cast(Any, request.source_constraints)
        required_host_preparation = []
        if not request.consumer_key:
            required_host_preparation.append("Provide consumer_key for the genealogy direct-sections planner handoff.")
        if getattr(source_constraints, "source_v2_job_id", None) is None:
            required_host_preparation.append(
                "Resolve source_v2_job_id from local saved-result identity before calling plan-task."
            )
        required_host_preparation.append(
            "Call plan-task with saved_result planning context to resolve a bounded direct-sections handoff before launch."
        )
        return (
            ["workflow_key", "consumer_key", "source_v2_job_id"],
            required_host_preparation,
            {
                "method": "POST",
                "endpoint": "/v1/orchestrator/plan-task",
                "request_fields": {
                    "task_request.workflow_hint": selected_assessment.workflow_key,
                    "task_request.consumer_key": request.consumer_key or "<required>",
                    "planning_context.context_mode": "saved_result",
                    "planning_context.source_v2_job_id": getattr(source_constraints, "source_v2_job_id", None) or "<required>",
                },
                "followup_contract_kind": "planner.direct_sections_compose_handoff",
                "advisory_only": True,
            },
        )

    if launch_contract_kind == "orchestrator.analyze_by_ref":
        source_constraints = cast(Any, request.source_constraints)
        return (
            [
                "consumer_key",
                "external_project_id",
                "thinker_name",
                "target_work",
                "target_external_doc_key",
                "prior_works",
            ],
            [
                "Assemble the registered-corpus analyze-by-ref payload.",
                "Provide genealogy chapter refs via target_chapter_external_doc_keys if chapter-targeting is needed.",
            ],
            {
                "method": "POST",
                "endpoint": "/v1/orchestrator/analyze-by-ref",
                "request_fields": {
                    "workflow_key": selected_assessment.workflow_key,
                    "consumer_key": getattr(source_constraints, "consumer_key", None),
                    "external_project_id": getattr(source_constraints, "external_project_id", None),
                    "target_external_doc_key": getattr(source_constraints, "target_external_doc_key", None),
                    "thinker_name": "<required>",
                    "target_work": "<required>",
                    "prior_works": "<required>",
                },
            },
        )

    return (
        ["thinker_name", "target_work", "target_work_text", "prior_works"],
        ["Assemble the inline-documents analyze payload."],
        {
            "method": "POST",
            "endpoint": "/v1/orchestrator/analyze",
            "request_fields": {
                "workflow_key": selected_assessment.workflow_key,
                "thinker_name": "<required>",
                "target_work": "<required>",
                "target_work_text": "<required>",
                "prior_works": "<required>",
            },
        },
    )


def _derive_routing_confidence(
    request: CompositionTaskRequest,
    selected_assessment: CandidateAssessment,
) -> RoutingConfidence:
    if request.objective_hint is not None:
        return "high"
    if selected_assessment.signal_score >= 2:
        return "high"
    return "medium"
