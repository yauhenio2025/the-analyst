"""Deterministic frozen-pack governance harness."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Optional

from src.analysis_products.result_contract import build_result_manifest
from src.analysis_products.source_backed_readiness import build_source_backed_readiness
from src.evaluations.frozen_pack_definitions import (
    FrozenArtifactDefinition,
    FrozenEvaluationCaseDefinition,
    FrozenEvaluationPackDefinition,
    get_frozen_pack_definition,
)
from src.evaluations.report_store import build_evaluation_report_id, save_evaluation_report
from src.evaluations.schemas import (
    EvaluationCheck,
    EvaluationDimensionSummary,
    EvaluationEvidenceRef,
    EvaluationReportSummary,
    PersistedEvaluationReport,
)
from src.executor.job_manager import get_job
from src.orchestrator.planning_decision_store import load_task_planning_decision
from src.presenter.compose_session_store import load_compose_session


class FrozenEvidenceIntegrityError(ValueError):
    """Raised when a pinned frozen artifact is missing or drifted."""


@dataclass(frozen=True)
class _RoutingPlanningCaseSpec:
    objective_key: str
    routing_outcome: str
    launch_contract_kind: str
    planning_outcome_kind: str
    downstream_readiness: str
    downstream_followup_endpoint: str
    downstream_followup_handoff_kind: str | None
    source_v2_job_id: str
    route_trace_stages: tuple[str, ...]
    planning_trace_stages: tuple[str, ...]


@dataclass(frozen=True)
class _RoutingPlanningCaseEvidence:
    route_artifact: dict[str, Any]
    planning_artifact: dict[str, Any]
    snapshot_artifact: dict[str, Any]
    embedded_snapshot_artifact: dict[str, Any] | None
    route_refs: list[EvaluationEvidenceRef]
    planning_refs: list[EvaluationEvidenceRef]
    snapshot_refs: list[EvaluationEvidenceRef]


@dataclass(frozen=True)
class _PlannerPresentationCaseSpec:
    source_v2_job_id: str
    planning_outcome_kind: str
    downstream_readiness: str
    downstream_followup_endpoint: str
    compose_entrypoint_kind: str | None
    downstream_followup_handoff_kind: str | None
    compose_resolver_version: str
    compose_trace_stages: tuple[str, ...]


@dataclass(frozen=True)
class _PlannerPresentationCaseEvidence:
    planning_artifact: dict[str, Any]
    snapshot_artifact: dict[str, Any]
    embedded_snapshot_artifact: dict[str, Any] | None
    compose_request_artifact: dict[str, Any]
    compose_response_artifact: dict[str, Any]
    bundle_planning_decision_id: str | None
    compose_binding_planning_decision_id: str | None
    planning_refs: list[EvaluationEvidenceRef]
    snapshot_refs: list[EvaluationEvidenceRef]
    compose_request_refs: list[EvaluationEvidenceRef]
    compose_response_refs: list[EvaluationEvidenceRef]


_ROUTING_PLANNING_CASE_SPECS: dict[str, _RoutingPlanningCaseSpec] = {
    "aoi_saved_result_handoff_current_contract": _RoutingPlanningCaseSpec(
        objective_key="influence_thematic",
        routing_outcome="aoi_transient_source_backed",
        launch_contract_kind="planner.aoi_compose_handoff",
        planning_outcome_kind="aoi_composition_handoff_plan",
        downstream_readiness="ready_for_aoi_compose_handoff",
        downstream_followup_endpoint="/v1/presenter/compose-from-selection",
        downstream_followup_handoff_kind=None,
        source_v2_job_id="job-744edf255ad5",
        route_trace_stages=(
            "task_normalization",
            "objective_candidate_scoring",
            "source_sufficiency_evaluation",
            "routing_decision",
        ),
        planning_trace_stages=(
            "effective_task_request",
            "source_catalog_resolution",
            "source_selection",
            "planning_decision",
        ),
    ),
    "genealogy_saved_result_direct_sections_snapshot_march28": _RoutingPlanningCaseSpec(
        objective_key="genealogical",
        routing_outcome="genealogy_transient_source_backed",
        launch_contract_kind="planner.direct_sections_compose_handoff",
        planning_outcome_kind="direct_sections_composition_handoff_plan",
        downstream_readiness="ready_for_direct_sections_compose_handoff",
        downstream_followup_endpoint="/v1/presenter/compose-from-intent",
        downstream_followup_handoff_kind="direct_sections",
        source_v2_job_id="proof-round4-adaptive-balance-final-1774012011",
        route_trace_stages=(
            "task_normalization",
            "objective_candidate_scoring",
            "source_sufficiency_evaluation",
            "routing_decision",
        ),
        planning_trace_stages=(
            "effective_task_request",
            "routing_reuse",
            "hydration_evaluation",
            "genealogy_saved_result_section_extraction",
            "planning_decision",
        ),
    ),
}


_PLANNER_PRESENTATION_CASE_SPECS: dict[str, _PlannerPresentationCaseSpec] = {
    "aoi_compose_selection_current_contract": _PlannerPresentationCaseSpec(
        source_v2_job_id="job-744edf255ad5",
        planning_outcome_kind="aoi_composition_handoff_plan",
        downstream_readiness="ready_for_aoi_compose_handoff",
        downstream_followup_endpoint="/v1/presenter/compose-from-selection",
        compose_entrypoint_kind="presenter.compose_from_selection",
        downstream_followup_handoff_kind=None,
        compose_resolver_version="compose-from-selection-v1",
        compose_trace_stages=(
            "source_catalog_resolution",
            "source_selection",
            "section_materialization",
            "semantic_surface_matching",
            "hierarchy_planning",
            "page_plan",
            "view_generation",
            "transformation_execution",
            "consumer_adaptation",
            "contract_validation",
        ),
    ),
    "aoi_compose_selection_current_contract_fresh_campaign": _PlannerPresentationCaseSpec(
        source_v2_job_id="job-744edf255ad5",
        planning_outcome_kind="aoi_composition_handoff_plan",
        downstream_readiness="ready_for_aoi_compose_handoff",
        downstream_followup_endpoint="/v1/presenter/compose-from-selection",
        compose_entrypoint_kind="presenter.compose_from_selection",
        downstream_followup_handoff_kind=None,
        compose_resolver_version="compose-from-selection-v1",
        compose_trace_stages=(
            "source_catalog_resolution",
            "source_selection",
            "section_materialization",
            "semantic_surface_matching",
            "hierarchy_planning",
            "page_plan",
            "view_generation",
            "transformation_execution",
            "consumer_adaptation",
            "contract_validation",
        ),
    ),
    "genealogy_direct_sections_compose_snapshot_march28": _PlannerPresentationCaseSpec(
        source_v2_job_id="proof-round4-adaptive-balance-final-1774012011",
        planning_outcome_kind="direct_sections_composition_handoff_plan",
        downstream_readiness="ready_for_direct_sections_compose_handoff",
        downstream_followup_endpoint="/v1/presenter/compose-from-intent",
        compose_entrypoint_kind=None,
        downstream_followup_handoff_kind="direct_sections",
        compose_resolver_version="compose-from-intent-v2",
        compose_trace_stages=(
            "semantic_surface_matching",
            "hierarchy_planning",
            "page_plan",
            "view_generation",
            "transformation_execution",
            "consumer_adaptation",
            "contract_validation",
        ),
    ),
    "genealogy_direct_sections_compose_current_contract_fresh_campaign": _PlannerPresentationCaseSpec(
        source_v2_job_id="proof-round4-adaptive-balance-final-1774012011",
        planning_outcome_kind="direct_sections_composition_handoff_plan",
        downstream_readiness="ready_for_direct_sections_compose_handoff",
        downstream_followup_endpoint="/v1/presenter/compose-from-intent",
        compose_entrypoint_kind=None,
        downstream_followup_handoff_kind="direct_sections",
        compose_resolver_version="compose-from-intent-v2",
        compose_trace_stages=(
            "semantic_surface_matching",
            "hierarchy_planning",
            "page_plan",
            "view_generation",
            "transformation_execution",
            "consumer_adaptation",
            "contract_validation",
        ),
    ),
}


def run_frozen_pack(
    evaluation_pack_key: str,
    *,
    save_report: bool = True,
) -> list[PersistedEvaluationReport]:
    """Evaluate all cases in one named frozen pack."""

    pack_definition = get_frozen_pack_definition(evaluation_pack_key)
    return run_pack_definition(pack_definition, save_report=save_report)


def run_pack_definition(
    pack_definition: FrozenEvaluationPackDefinition,
    *,
    save_report: bool = True,
) -> list[PersistedEvaluationReport]:
    """Evaluate and optionally persist all reports for one pack definition."""

    reports: list[PersistedEvaluationReport] = []
    for case_definition in pack_definition.cases:
        report = evaluate_case_definition(
            pack_definition=pack_definition,
            case_definition=case_definition,
        )
        if save_report:
            save_evaluation_report(report)
        reports.append(report)
    return reports


def evaluate_case_definition(
    *,
    pack_definition: FrozenEvaluationPackDefinition,
    case_definition: FrozenEvaluationCaseDefinition,
) -> PersistedEvaluationReport:
    """Evaluate one frozen case into a persisted report shape."""

    created_at = _now_iso()
    report_id = build_evaluation_report_id()
    try:
        frozen_artifacts = _load_case_artifacts(case_definition)
        if case_definition.evaluator_key == "aoi_exemplar":
            return _evaluate_aoi_case(
                report_id=report_id,
                created_at=created_at,
                pack_definition=pack_definition,
                case_definition=case_definition,
                frozen_artifacts=frozen_artifacts,
            )
        if case_definition.evaluator_key == "genealogy_lifecycle":
            return _evaluate_genealogy_case(
                report_id=report_id,
                created_at=created_at,
                pack_definition=pack_definition,
                case_definition=case_definition,
                frozen_artifacts=frozen_artifacts,
            )
        if case_definition.evaluator_key == "routing_planning_decision":
            return _evaluate_routing_planning_case(
                report_id=report_id,
                created_at=created_at,
                pack_definition=pack_definition,
                case_definition=case_definition,
                frozen_artifacts=frozen_artifacts,
            )
        if case_definition.evaluator_key == "planner_presentation_decision":
            return _evaluate_planner_presentation_case(
                report_id=report_id,
                created_at=created_at,
                pack_definition=pack_definition,
                case_definition=case_definition,
                frozen_artifacts=frozen_artifacts,
            )
        raise ValueError(f"Unknown evaluator_key: {case_definition.evaluator_key}")
    except FrozenEvidenceIntegrityError as exc:
        return _error_report(
            report_id=report_id,
            created_at=created_at,
            pack_definition=pack_definition,
            case_definition=case_definition,
            summary=str(exc),
        )
    except Exception as exc:  # pragma: no cover - defensive guard
        return _error_report(
            report_id=report_id,
            created_at=created_at,
            pack_definition=pack_definition,
            case_definition=case_definition,
            summary=f"Case evaluation crashed: {exc}",
        )


def _evaluate_aoi_case(
    *,
    report_id: str,
    created_at: str,
    pack_definition: FrozenEvaluationPackDefinition,
    case_definition: FrozenEvaluationCaseDefinition,
    frozen_artifacts: dict[str, tuple[dict[str, Any], EvaluationEvidenceRef]],
) -> PersistedEvaluationReport:
    exemplar_summary, exemplar_ref = frozen_artifacts["stage5_exemplar_eval_summary"]
    pack_rerun_summary, pack_rerun_ref = frozen_artifacts["stage5_pack_rerun_summary"]
    ready_manifest_artifact, ready_manifest_ref = frozen_artifacts["march27_ready_manifest"]
    completed_boundary_core, completed_boundary_ref = frozen_artifacts["march27_completed_boundary_core"]
    requests_artifact, requests_ref = frozen_artifacts["march27_requests"]

    observed_at = _now_iso()
    job = get_job(case_definition.subject_identity)
    manifest, manifest_error = _safe_call(
        build_result_manifest,
        case_definition.subject_identity,
        consumer_key=case_definition.consumer_key or "the-critic",
    )
    readiness, readiness_error = _safe_call(
        build_source_backed_readiness,
        case_definition.subject_identity,
        consumer_key=case_definition.consumer_key or "the-critic",
    )

    exemplar_case = _find_case(exemplar_summary, "evolution_ready")
    rerun_case = _find_case(pack_rerun_summary, "evolution_ready")

    checks = [
        EvaluationCheck(
            check_key="executor_job_completed",
            label="Executor job is completed under the AOI workflow",
            status=(
                "pass"
                if job is not None
                and job.get("status") == "completed"
                and job.get("workflow_key") == case_definition.workflow_key
                else "fail"
            ),
            summary=(
                f"job status={job.get('status')} workflow_key={job.get('workflow_key')}"
                if job is not None
                else "executor job not found"
            ),
            evidence_mode="executor_read_contract",
            evidence_observed_at=observed_at,
            live_revalidation_performed=True,
            evidence_refs=[
                EvaluationEvidenceRef(
                    ref_key="executor_job_status",
                    source_kind="executor_read_contract",
                    locator=f"job_manager.get_job({case_definition.subject_identity})",
                )
            ],
            observed_values={
                "job_id": case_definition.subject_identity,
                "status": job.get("status") if job else None,
                "workflow_key": job.get("workflow_key") if job else None,
            },
        ),
        EvaluationCheck(
            check_key="result_manifest_ready",
            label="AOI result manifest is ready and restorable",
            status=(
                "pass"
                if manifest is not None
                and manifest.result_state == "ready"
                and manifest.presentation_status == "completed"
                and manifest.restore_available is True
                else "fail"
            ),
            summary=(
                f"result_state={manifest.result_state} presentation_status={manifest.presentation_status} "
                f"restore_available={manifest.restore_available}"
                if manifest is not None
                else f"manifest read failed: {manifest_error}"
            ),
            evidence_mode="inspection_route",
            evidence_observed_at=observed_at,
            live_revalidation_performed=True,
            evidence_refs=[
                EvaluationEvidenceRef(
                    ref_key="result_manifest",
                    source_kind="inspection_route",
                    locator=(
                        f"build_result_manifest({case_definition.subject_identity}, "
                        f"consumer_key={case_definition.consumer_key or 'the-critic'})"
                    ),
                )
            ],
            observed_values={
                "job_id": case_definition.subject_identity,
                "result_state": manifest.result_state if manifest else None,
                "presentation_status": manifest.presentation_status if manifest else None,
                "restore_available": manifest.restore_available if manifest else None,
            },
        ),
        EvaluationCheck(
            check_key="source_backed_readiness_ready",
            label="AOI source-backed readiness remains ready",
            status=(
                "pass"
                if readiness is not None and readiness.readiness_status == "ready"
                else "fail"
            ),
            summary=(
                f"readiness_status={readiness.readiness_status} selectors={readiness.allowed_selectors}"
                if readiness is not None
                else f"source-backed readiness read failed: {readiness_error}"
            ),
            evidence_mode="inspection_route",
            evidence_observed_at=observed_at,
            live_revalidation_performed=True,
            evidence_refs=[
                EvaluationEvidenceRef(
                    ref_key="source_backed_readiness",
                    source_kind="inspection_route",
                    locator=(
                        f"build_source_backed_readiness({case_definition.subject_identity}, "
                        f"consumer_key={case_definition.consumer_key or 'the-critic'})"
                    ),
                )
            ],
            observed_values={
                "job_id": case_definition.subject_identity,
                "readiness_status": readiness.readiness_status if readiness else None,
                "allowed_selectors": list(readiness.allowed_selectors) if readiness else None,
            },
        ),
        EvaluationCheck(
            check_key="stage5_seam_gate_pass",
            label="Stage 5 frozen seam-gate evidence passes",
            status=(
                "pass"
                if exemplar_summary.get("stage5_seam_gate_pass") is True
                and pack_rerun_summary.get("stage5_seam_gate_pass") is True
                and rerun_case.get("expectation_met") is True
                else "fail"
            ),
            summary=(
                "Stage 5 exemplar and rerun summaries both report a passing seam gate for evolution_ready."
            ),
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=[exemplar_ref, pack_rerun_ref],
            observed_values={
                "stage5_exemplar_seam_gate_pass": exemplar_summary.get("stage5_seam_gate_pass"),
                "stage5_pack_seam_gate_pass": pack_rerun_summary.get("stage5_seam_gate_pass"),
                "evolution_ready_expectation_met": rerun_case.get("expectation_met"),
            },
        ),
        EvaluationCheck(
            check_key="selection_fit_carried_forward",
            label="Stage 5 carried-forward selection_fit dimension passes",
            status="pass" if exemplar_case.get("selection_fit") is True else "fail",
            summary="selection_fit was carried forward from the frozen Stage 5 exemplar summary.",
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=[exemplar_ref],
            observed_values={"selection_fit": exemplar_case.get("selection_fit")},
        ),
        EvaluationCheck(
            check_key="rationale_clarity_carried_forward",
            label="Stage 5 carried-forward rationale_clarity dimension passes",
            status="pass" if exemplar_case.get("rationale_clarity") is True else "fail",
            summary="rationale_clarity was carried forward from the frozen Stage 5 exemplar summary.",
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=[exemplar_ref],
            observed_values={"rationale_clarity": exemplar_case.get("rationale_clarity")},
        ),
        EvaluationCheck(
            check_key="rendered_usefulness_carried_forward",
            label="Stage 5 carried-forward rendered_usefulness dimension passes",
            status="pass" if exemplar_case.get("rendered_usefulness") is True else "fail",
            summary="rendered_usefulness was carried forward from the frozen Stage 5 exemplar summary.",
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=[exemplar_ref],
            observed_values={"rendered_usefulness": exemplar_case.get("rendered_usefulness")},
        ),
        EvaluationCheck(
            check_key="aoi_browser_chain_success",
            label="March 27 browser-chain proof preserves the planner-primary AOI path",
            status=(
                "pass"
                if requests_artifact.get("success") is True
                and requests_artifact.get("source_v2_job_id") == case_definition.subject_identity
                and requests_artifact.get("planner_request", {}).get("status") == 200
                and requests_artifact.get("plan_task_request", {}).get("status") == 200
                and requests_artifact.get("compose_from_selection", {}).get("status") == 200
                else "fail"
            ),
            summary="The frozen March 27 request chain shows successful planner, plan-task, and compose-from-selection calls for the AOI exemplar.",
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=[requests_ref],
            observed_values={
                "success": requests_artifact.get("success"),
                "source_v2_job_id": requests_artifact.get("source_v2_job_id"),
                "planner_request_status": requests_artifact.get("planner_request", {}).get("status"),
                "plan_task_request_status": requests_artifact.get("plan_task_request", {}).get("status"),
                "compose_from_selection_status": requests_artifact.get("compose_from_selection", {}).get("status"),
            },
        ),
        EvaluationCheck(
            check_key="aoi_completed_boundary_core",
            label="Completed-boundary core artifact validates the same AOI run",
            status=(
                "pass"
                if completed_boundary_core.get("exit_code") == 0
                and completed_boundary_core.get("validated_run_job_id") == case_definition.subject_identity
                else "fail"
            ),
            summary="The frozen completed-boundary core artifact exits cleanly for the AOI exemplar job.",
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=[completed_boundary_ref],
            observed_values={
                "exit_code": completed_boundary_core.get("exit_code"),
                "validated_run_job_id": completed_boundary_core.get("validated_run_job_id"),
            },
        ),
        EvaluationCheck(
            check_key="aoi_ready_manifest_artifact",
            label="March 27 ready-manifest artifact records ready/completed/restoreable truth",
            status=(
                "pass"
                if ready_manifest_artifact.get("job_id") == case_definition.subject_identity
                and ready_manifest_artifact.get("result_state") == "ready"
                and ready_manifest_artifact.get("presentation_status") == "completed"
                and ready_manifest_artifact.get("restore_available") is True
                else "fail"
            ),
            summary="The frozen ready-manifest artifact records the AOI exemplar as ready and restoreable.",
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=[ready_manifest_ref],
            observed_values={
                "job_id": ready_manifest_artifact.get("job_id"),
                "result_state": ready_manifest_artifact.get("result_state"),
                "presentation_status": ready_manifest_artifact.get("presentation_status"),
                "restore_available": ready_manifest_artifact.get("restore_available"),
            },
        ),
    ]

    dimension_summaries = [
        _single_check_dimension("selection_fit", checks, "selection_fit_carried_forward"),
        _single_check_dimension("rationale_clarity", checks, "rationale_clarity_carried_forward"),
        _single_check_dimension("rendered_usefulness", checks, "rendered_usefulness_carried_forward"),
        _multi_check_dimension(
            "operational_behavior",
            checks,
            [
                "aoi_browser_chain_success",
                "aoi_completed_boundary_core",
                "aoi_ready_manifest_artifact",
            ],
            pass_summary="Operational behavior remains supported by the March 27 browser-chain and completed-boundary evidence.",
            fail_summary="Operational behavior evidence is incomplete or contradictory.",
        ),
    ]

    return _build_report(
        report_id=report_id,
        created_at=created_at,
        pack_definition=pack_definition,
        case_definition=case_definition,
        checks=checks,
        dimension_summaries=dimension_summaries,
        input_evidence_refs=[ref for _, ref in frozen_artifacts.values()],
    )


def _evaluate_genealogy_case(
    *,
    report_id: str,
    created_at: str,
    pack_definition: FrozenEvaluationPackDefinition,
    case_definition: FrozenEvaluationCaseDefinition,
    frozen_artifacts: dict[str, tuple[dict[str, Any], EvaluationEvidenceRef]],
) -> PersistedEvaluationReport:
    preflight_artifact, preflight_ref = frozen_artifacts["phase3_preflight"]
    saved_session_artifact, saved_session_ref = frozen_artifacts["phase3_saved_session"]
    reopen_segment_artifact, reopen_segment_ref = frozen_artifacts["phase3_reopen_segment"]
    invalid_session_artifact, invalid_session_ref = frozen_artifacts["phase3_invalid_session"]

    observed_at = _now_iso()
    session = load_compose_session(case_definition.subject_identity)
    planning = load_task_planning_decision(
        case_definition.supporting_subjects.get("planning_decision_id", "")
    )
    source_job_id = session.source_v2_job_id if session is not None else case_definition.supporting_subjects.get("source_v2_job_id")
    manifest, manifest_error = _safe_call(
        build_result_manifest,
        source_job_id,
        consumer_key=case_definition.consumer_key or "the-critic",
    ) if source_job_id else (None, "source_v2_job_id unavailable")
    readiness, readiness_error = _safe_call(
        build_source_backed_readiness,
        source_job_id,
        consumer_key=case_definition.consumer_key or "the-critic",
    ) if source_job_id else (None, "source_v2_job_id unavailable")

    checks = [
        EvaluationCheck(
            check_key="compose_session_exists",
            label="Compose session exists and matches workflow/consumer truth",
            status=(
                "pass"
                if session is not None
                and session.workflow_key == case_definition.workflow_key
                and session.consumer_key == case_definition.consumer_key
                else "fail"
            ),
            summary=(
                f"workflow_key={session.workflow_key} consumer_key={session.consumer_key}"
                if session is not None
                else "compose session not found"
            ),
            evidence_mode="stored_object",
            evidence_observed_at=observed_at,
            live_revalidation_performed=True,
            evidence_refs=[
                EvaluationEvidenceRef(
                    ref_key="compose_session_store",
                    source_kind="stored_object",
                    locator=f"compose_session_store.load_compose_session({case_definition.subject_identity})",
                )
            ],
            observed_values={
                "session_id": case_definition.subject_identity,
                "workflow_key": session.workflow_key if session else None,
                "consumer_key": session.consumer_key if session else None,
                "planning_decision_id": session.planning_decision_id if session else None,
                "source_v2_job_id": session.source_v2_job_id if session else None,
            },
        ),
        EvaluationCheck(
            check_key="planning_decision_exists",
            label="Referenced planning decision exists as provenance",
            status=(
                "pass"
                if planning is not None
                and session is not None
                and planning.planning_decision_id == session.planning_decision_id
                else "fail"
            ),
            summary=(
                f"planning_decision_id={planning.planning_decision_id}"
                if planning is not None
                else "referenced planning decision not found"
            ),
            evidence_mode="stored_object",
            evidence_observed_at=observed_at,
            live_revalidation_performed=True,
            evidence_refs=[
                EvaluationEvidenceRef(
                    ref_key="planning_decision_store",
                    source_kind="stored_object",
                    locator=(
                        "planning_decision_store.load_task_planning_decision("
                        f"{case_definition.supporting_subjects.get('planning_decision_id', '')})"
                    ),
                )
            ],
            observed_values={
                "planning_decision_id": planning.planning_decision_id if planning else None,
                "workflow_key": planning.workflow_key if planning else None,
                "source_v2_job_id": planning.source_v2_job_id if planning else None,
            },
        ),
        EvaluationCheck(
            check_key="source_manifest_ready",
            label="Supporting source result remains ready and restorable",
            status=(
                "pass"
                if manifest is not None
                and manifest.result_state == "ready"
                and manifest.presentation_status == "completed"
                and manifest.restore_available is True
                else "fail"
            ),
            summary=(
                f"result_state={manifest.result_state} presentation_status={manifest.presentation_status} "
                f"restore_available={manifest.restore_available}"
                if manifest is not None
                else f"manifest read failed: {manifest_error}"
            ),
            evidence_mode="inspection_route",
            evidence_observed_at=observed_at,
            live_revalidation_performed=True,
            evidence_refs=[
                EvaluationEvidenceRef(
                    ref_key="result_manifest",
                    source_kind="inspection_route",
                    locator=(
                        f"build_result_manifest({source_job_id}, "
                        f"consumer_key={case_definition.consumer_key or 'the-critic'})"
                    ),
                )
            ],
            observed_values={
                "source_v2_job_id": source_job_id,
                "result_state": manifest.result_state if manifest else None,
                "presentation_status": manifest.presentation_status if manifest else None,
                "restore_available": manifest.restore_available if manifest else None,
            },
        ),
        EvaluationCheck(
            check_key="source_readiness_bounded_dynamic_genealogy",
            label="Source-backed readiness still exposes bounded dynamic genealogy",
            status=(
                "pass"
                if readiness is not None
                and "bounded_dynamic_genealogy_v1" in list(readiness.allowed_selectors)
                else "fail"
            ),
            summary=(
                f"readiness_status={readiness.readiness_status} selectors={readiness.allowed_selectors}"
                if readiness is not None
                else f"source-backed readiness read failed: {readiness_error}"
            ),
            evidence_mode="inspection_route",
            evidence_observed_at=observed_at,
            live_revalidation_performed=True,
            evidence_refs=[
                EvaluationEvidenceRef(
                    ref_key="source_backed_readiness",
                    source_kind="inspection_route",
                    locator=(
                        f"build_source_backed_readiness({source_job_id}, "
                        f"consumer_key={case_definition.consumer_key or 'the-critic'})"
                    ),
                )
            ],
            observed_values={
                "source_v2_job_id": source_job_id,
                "readiness_status": readiness.readiness_status if readiness else None,
                "allowed_selectors": list(readiness.allowed_selectors) if readiness else None,
            },
        ),
        EvaluationCheck(
            check_key="preflight_artifact_valid",
            label="Frozen preflight artifact records the expected ready genealogy source job",
            status=(
                "pass"
                if preflight_artifact.get("source_v2_job_id")
                == case_definition.supporting_subjects.get("source_v2_job_id")
                and preflight_artifact.get("preflight_fields", {}).get("workflow_key")
                == case_definition.workflow_key
                and preflight_artifact.get("preflight_fields", {}).get("result_state") == "ready"
                and preflight_artifact.get("preflight_fields", {}).get("presentation_status") == "completed"
                and preflight_artifact.get("preflight_fields", {}).get("restore_available") is True
                else "fail"
            ),
            summary="The frozen preflight artifact records a completed, ready, restorable genealogy source result.",
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=[preflight_ref],
            observed_values={
                "source_v2_job_id": preflight_artifact.get("source_v2_job_id"),
                "workflow_key": preflight_artifact.get("preflight_fields", {}).get("workflow_key"),
                "result_state": preflight_artifact.get("preflight_fields", {}).get("result_state"),
                "presentation_status": preflight_artifact.get("preflight_fields", {}).get("presentation_status"),
                "restore_available": preflight_artifact.get("preflight_fields", {}).get("restore_available"),
            },
        ),
        EvaluationCheck(
            check_key="stored_session_fidelity_fields_present",
            label="Stored compose session carries the expected lifecycle identity and fidelity fields",
            status=(
                "pass"
                if session is not None
                and session.session_id == case_definition.subject_identity
                and session.workflow_key == case_definition.workflow_key
                and session.consumer_key == case_definition.consumer_key
                and bool(session.presentation_hash.strip())
                and bool(session.presentation_content_hash.strip())
                and bool(session.resolver_version.strip())
                else "fail"
            ),
            summary="The stored compose session carries the expected lifecycle identity and non-empty fidelity hashes.",
            evidence_mode="stored_object",
            evidence_observed_at=observed_at,
            live_revalidation_performed=True,
            evidence_refs=[
                EvaluationEvidenceRef(
                    ref_key="compose_session_store",
                    source_kind="stored_object",
                    locator=f"compose_session_store.load_compose_session({case_definition.subject_identity})",
                )
            ],
            observed_values={
                "stored_session_id": session.session_id if session else None,
                "stored_workflow_key": session.workflow_key if session else None,
                "stored_consumer_key": session.consumer_key if session else None,
                "stored_presentation_hash": session.presentation_hash if session else None,
                "stored_presentation_content_hash": session.presentation_content_hash if session else None,
                "stored_resolver_version": session.resolver_version if session else None,
            },
        ),
        EvaluationCheck(
            check_key="frozen_saved_session_artifact_valid",
            label="Frozen saved-session artifact records the expected lifecycle identity and fidelity fields",
            status=(
                "pass"
                if saved_session_artifact.get("session_id") == case_definition.subject_identity
                and saved_session_artifact.get("workflow_key") == case_definition.workflow_key
                and saved_session_artifact.get("consumer_key") == case_definition.consumer_key
                and saved_session_artifact.get("planning_decision_id")
                == case_definition.supporting_subjects.get("planning_decision_id")
                and saved_session_artifact.get("source_v2_job_id")
                == case_definition.supporting_subjects.get("source_v2_job_id")
                and bool(str(saved_session_artifact.get("presentation_hash", "")).strip())
                and bool(str(saved_session_artifact.get("presentation_content_hash", "")).strip())
                and bool(str(saved_session_artifact.get("resolver_version", "")).strip())
                else "fail"
            ),
            summary="The frozen saved-session artifact records the expected session identity, provenance, and fidelity hashes.",
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=[saved_session_ref],
            observed_values={
                "artifact_session_id": saved_session_artifact.get("session_id"),
                "artifact_workflow_key": saved_session_artifact.get("workflow_key"),
                "artifact_consumer_key": saved_session_artifact.get("consumer_key"),
                "artifact_planning_decision_id": saved_session_artifact.get("planning_decision_id"),
                "artifact_source_v2_job_id": saved_session_artifact.get("source_v2_job_id"),
                "artifact_presentation_hash": saved_session_artifact.get("presentation_hash"),
                "artifact_presentation_content_hash": saved_session_artifact.get("presentation_content_hash"),
                "artifact_resolver_version": saved_session_artifact.get("resolver_version"),
            },
        ),
        EvaluationCheck(
            check_key="reopen_segment_no_recompute",
            label="Frozen reopen segment shows one session fetch and zero recomputation endpoints",
            status=(
                "pass"
                if reopen_segment_artifact.get("required_session_fetch_count") == 1
                and reopen_segment_artifact.get("forbidden_endpoint_matches") == []
                else "fail"
            ),
            summary="The frozen reopen segment shows session-based reopen without planner or composition replay.",
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=[reopen_segment_ref],
            observed_values={
                "required_session_fetch_count": reopen_segment_artifact.get("required_session_fetch_count"),
                "forbidden_endpoint_matches": reopen_segment_artifact.get("forbidden_endpoint_matches"),
            },
        ),
        EvaluationCheck(
            check_key="invalid_session_fails_closed",
            label="Frozen invalid-session proof fails closed without recomputation",
            status=(
                "pass"
                if invalid_session_artifact.get("forbidden_endpoint_matches") == []
                and "not found" in str(invalid_session_artifact.get("alert_text", "")).lower()
                else "fail"
            ),
            summary="The frozen invalid-session proof shows a visible not-found error and no fallback recomputation.",
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=[invalid_session_ref],
            observed_values={
                "alert_text": invalid_session_artifact.get("alert_text"),
                "forbidden_endpoint_matches": invalid_session_artifact.get("forbidden_endpoint_matches"),
            },
        ),
    ]

    dimension_summaries = [
        _multi_check_dimension(
            "identity_integrity",
            checks,
            ["compose_session_exists", "planning_decision_exists", "source_manifest_ready"],
            pass_summary="Lifecycle identity stays anchored on the saved compose session with valid provenance and source truth.",
            fail_summary="Lifecycle identity or its supporting provenance/source truth is inconsistent.",
        ),
        _multi_check_dimension(
            "saved_truth_fidelity",
            checks,
            [
                "stored_session_fidelity_fields_present",
                "frozen_saved_session_artifact_valid",
            ],
            pass_summary="Stored compose-session truth and the frozen saved-session artifact independently record the expected lifecycle identity and fidelity hashes.",
            fail_summary="Stored compose-session fidelity or frozen saved-session fidelity evidence is incomplete or contradictory.",
        ),
        _single_check_dimension("reopen_integrity", checks, "reopen_segment_no_recompute"),
        _multi_check_dimension(
            "boundary_observance",
            checks,
            ["invalid_session_fails_closed", "source_readiness_bounded_dynamic_genealogy"],
            pass_summary="The lifecycle proof stays within the bounded genealogy transient surface and fails closed on invalid reopen identity.",
            fail_summary="Boundary observance evidence is missing or contradictory.",
        ),
    ]

    return _build_report(
        report_id=report_id,
        created_at=created_at,
        pack_definition=pack_definition,
        case_definition=case_definition,
        checks=checks,
        dimension_summaries=dimension_summaries,
        input_evidence_refs=[ref for _, ref in frozen_artifacts.values()],
    )


def _evaluate_routing_planning_case(
    *,
    report_id: str,
    created_at: str,
    pack_definition: FrozenEvaluationPackDefinition,
    case_definition: FrozenEvaluationCaseDefinition,
    frozen_artifacts: dict[str, tuple[dict[str, Any], EvaluationEvidenceRef]],
) -> PersistedEvaluationReport:
    observed_at = _now_iso()
    spec = _ROUTING_PLANNING_CASE_SPECS.get(case_definition.case_key)
    if spec is None:
        raise ValueError(f"Unknown routing/planning case_key: {case_definition.case_key}")

    evidence = _extract_routing_planning_evidence(
        case_definition=case_definition,
        frozen_artifacts=frozen_artifacts,
    )
    route_artifact = evidence.route_artifact
    planning_artifact = evidence.planning_artifact
    snapshot_artifact = evidence.snapshot_artifact
    embedded_snapshot_artifact = evidence.embedded_snapshot_artifact

    route_required_fields = route_artifact.get("required_fields") or []
    route_has_required_fields = all(
        field in route_required_fields
        for field in ("workflow_key", "consumer_key", "source_v2_job_id")
    )
    route_trace_stages = _trace_stage_names(route_artifact.get("trace"))
    planning_trace_stages = _trace_stage_names(planning_artifact.get("trace"))

    route_fidelity_status = (
        "pass"
        if route_artifact.get("selected_objective_key") == spec.objective_key
        and route_artifact.get("selected_workflow_key") == case_definition.workflow_key
        and route_artifact.get("routing_outcome") == spec.routing_outcome
        and route_artifact.get("launch_contract_kind") == spec.launch_contract_kind
        else "fail"
    )

    snapshot_task_request = snapshot_artifact.get("task_request", {})
    snapshot_source_constraints = snapshot_task_request.get("source_constraints", {})
    planning_handoff = (
        planning_artifact.get("aoi_composition_handoff_plan")
        if case_definition.case_key == "aoi_saved_result_handoff_current_contract"
        else planning_artifact.get("direct_sections_composition_handoff_plan")
    )
    source_contract_status = (
        "pass"
        if route_artifact.get("source_sufficiency_status") == "sufficient"
        and route_has_required_fields
        and route_artifact.get("downstream_launch_contract", {}).get("endpoint") == "/v1/orchestrator/plan-task"
        and snapshot_artifact.get("workflow_key") == case_definition.workflow_key
        and snapshot_artifact.get("consumer_key") == case_definition.consumer_key
        and snapshot_artifact.get("source_v2_job_id") == spec.source_v2_job_id
        and snapshot_source_constraints.get("source_mode") == "saved_result"
        and snapshot_source_constraints.get("source_v2_job_id") == spec.source_v2_job_id
        and planning_handoff is not None
        and (
            (
                case_definition.case_key == "aoi_saved_result_handoff_current_contract"
                and bool(snapshot_artifact.get("selected_source_thinker_id"))
                and bool(snapshot_artifact.get("selected_source_thinker_name"))
                and bool(planning_handoff.get("selected_sources"))
            )
            or (
                case_definition.case_key == "genealogy_saved_result_direct_sections_snapshot_march28"
                and bool(planning_handoff.get("prose_sections"))
                and bool(planning_handoff.get("section_trace"))
            )
        )
        else "fail"
    )

    followup_contract = planning_artifact.get("downstream_followup_contract", {})
    planning_followup_status = (
        "pass"
        if planning_artifact.get("planning_outcome_kind") == spec.planning_outcome_kind
        and planning_artifact.get("downstream_readiness") == spec.downstream_readiness
        and followup_contract.get("endpoint") == spec.downstream_followup_endpoint
        and (
            spec.downstream_followup_handoff_kind is None
            or followup_contract.get("handoff_kind") == spec.downstream_followup_handoff_kind
        )
        else "fail"
    )

    route_match = snapshot_artifact.get("routing_decision", {})
    planning_match = snapshot_artifact.get("planning_decision", {})
    decision_trace_status = (
        "pass"
        if route_artifact.get("selected_objective_key")
        == planning_artifact.get("routing_decision", {}).get("selected_objective_key")
        and route_artifact.get("launch_contract_kind")
        == planning_artifact.get("routing_decision", {}).get("launch_contract_kind")
        and all(stage in route_trace_stages for stage in spec.route_trace_stages)
        and all(stage in planning_trace_stages for stage in spec.planning_trace_stages)
        and snapshot_artifact.get("planning_decision_id") == case_definition.subject_identity
        and route_match.get("selected_objective_key") == route_artifact.get("selected_objective_key")
        and route_match.get("launch_contract_kind") == route_artifact.get("launch_contract_kind")
        and planning_match.get("planning_outcome_kind") == planning_artifact.get("planning_outcome_kind")
        and (
            embedded_snapshot_artifact is None
            or (
                embedded_snapshot_artifact.get("planning_decision_id")
                == snapshot_artifact.get("planning_decision_id")
                and embedded_snapshot_artifact.get("workflow_key")
                == snapshot_artifact.get("workflow_key")
                and embedded_snapshot_artifact.get("consumer_key")
                == snapshot_artifact.get("consumer_key")
                and embedded_snapshot_artifact.get("source_v2_job_id")
                == snapshot_artifact.get("source_v2_job_id")
            )
        )
        else "fail"
    )

    checks = [
        EvaluationCheck(
            check_key="route_fidelity",
            label="Routing decision matches the declared objective/workflow/contract law",
            status=route_fidelity_status,
            summary=(
                "selected_objective_key={selected_objective_key} "
                "selected_workflow_key={selected_workflow_key} "
                "routing_outcome={routing_outcome} "
                "launch_contract_kind={launch_contract_kind}"
            ).format(
                selected_objective_key=route_artifact.get("selected_objective_key"),
                selected_workflow_key=route_artifact.get("selected_workflow_key"),
                routing_outcome=route_artifact.get("routing_outcome"),
                launch_contract_kind=route_artifact.get("launch_contract_kind"),
            ),
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=evidence.route_refs,
            observed_values={
                "selected_objective_key": route_artifact.get("selected_objective_key"),
                "selected_workflow_key": route_artifact.get("selected_workflow_key"),
                "routing_outcome": route_artifact.get("routing_outcome"),
                "launch_contract_kind": route_artifact.get("launch_contract_kind"),
            },
        ),
        EvaluationCheck(
            check_key="source_contract_fidelity",
            label="Source-contract fields stay coherent for the declared route/planning mode",
            status=source_contract_status,
            summary=(
                "source_sufficiency_status={source_sufficiency_status} "
                "required_fields={required_fields} "
                "snapshot_source_v2_job_id={source_v2_job_id}"
            ).format(
                source_sufficiency_status=route_artifact.get("source_sufficiency_status"),
                required_fields=route_required_fields,
                source_v2_job_id=snapshot_artifact.get("source_v2_job_id"),
            ),
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=evidence.route_refs + evidence.planning_refs + evidence.snapshot_refs,
            observed_values={
                "source_sufficiency_status": route_artifact.get("source_sufficiency_status"),
                "required_fields": route_required_fields,
                "snapshot_workflow_key": snapshot_artifact.get("workflow_key"),
                "snapshot_consumer_key": snapshot_artifact.get("consumer_key"),
                "snapshot_source_v2_job_id": snapshot_artifact.get("source_v2_job_id"),
                "snapshot_selected_source_thinker_id": snapshot_artifact.get("selected_source_thinker_id"),
                "snapshot_selected_source_thinker_name": snapshot_artifact.get("selected_source_thinker_name"),
            },
        ),
        EvaluationCheck(
            check_key="planning_followup_fidelity",
            label="Planning outcome and downstream followup contract match the declared case",
            status=planning_followup_status,
            summary=(
                "planning_outcome_kind={planning_outcome_kind} "
                "downstream_readiness={downstream_readiness} "
                "followup_endpoint={followup_endpoint}"
            ).format(
                planning_outcome_kind=planning_artifact.get("planning_outcome_kind"),
                downstream_readiness=planning_artifact.get("downstream_readiness"),
                followup_endpoint=followup_contract.get("endpoint"),
            ),
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=evidence.planning_refs,
            observed_values={
                "planning_outcome_kind": planning_artifact.get("planning_outcome_kind"),
                "downstream_readiness": planning_artifact.get("downstream_readiness"),
                "downstream_followup_contract": followup_contract,
            },
        ),
        EvaluationCheck(
            check_key="decision_trace_integrity",
            label="Trace stages and persisted snapshot agree across the decision surfaces",
            status=decision_trace_status,
            summary=(
                "route_trace_stages={route_trace_stages} "
                "planning_trace_stages={planning_trace_stages} "
                "planning_decision_id={planning_decision_id}"
            ).format(
                route_trace_stages=route_trace_stages,
                planning_trace_stages=planning_trace_stages,
                planning_decision_id=snapshot_artifact.get("planning_decision_id"),
            ),
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=evidence.route_refs + evidence.planning_refs + evidence.snapshot_refs,
            observed_values={
                "route_trace_stages": route_trace_stages,
                "planning_trace_stages": planning_trace_stages,
                "snapshot_planning_decision_id": snapshot_artifact.get("planning_decision_id"),
                "snapshot_workflow_key": snapshot_artifact.get("workflow_key"),
                "snapshot_consumer_key": snapshot_artifact.get("consumer_key"),
                "snapshot_source_v2_job_id": snapshot_artifact.get("source_v2_job_id"),
                "embedded_snapshot_planning_decision_id": (
                    embedded_snapshot_artifact.get("planning_decision_id")
                    if embedded_snapshot_artifact is not None
                    else None
                ),
            },
        ),
    ]

    dimension_summaries = [
        _single_check_dimension("route_fidelity", checks, "route_fidelity"),
        _single_check_dimension("source_contract_fidelity", checks, "source_contract_fidelity"),
        _single_check_dimension("planning_followup_fidelity", checks, "planning_followup_fidelity"),
        _single_check_dimension("decision_trace_integrity", checks, "decision_trace_integrity"),
    ]

    return _build_report(
        report_id=report_id,
        created_at=created_at,
        pack_definition=pack_definition,
        case_definition=case_definition,
        checks=checks,
        dimension_summaries=dimension_summaries,
        input_evidence_refs=[ref for _, ref in frozen_artifacts.values()],
    )


def _evaluate_planner_presentation_case(
    *,
    report_id: str,
    created_at: str,
    pack_definition: FrozenEvaluationPackDefinition,
    case_definition: FrozenEvaluationCaseDefinition,
    frozen_artifacts: dict[str, tuple[dict[str, Any], EvaluationEvidenceRef]],
) -> PersistedEvaluationReport:
    observed_at = _now_iso()
    spec = _PLANNER_PRESENTATION_CASE_SPECS.get(case_definition.case_key)
    if spec is None:
        raise ValueError(f"Unknown planner/presentation case_key: {case_definition.case_key}")

    evidence = _extract_planner_presentation_evidence(
        case_definition=case_definition,
        frozen_artifacts=frozen_artifacts,
    )
    planning_artifact = evidence.planning_artifact
    snapshot_artifact = evidence.snapshot_artifact
    compose_request_artifact = evidence.compose_request_artifact
    compose_response_artifact = evidence.compose_response_artifact
    compose_presentation = compose_response_artifact.get("presentation", {})
    generated_view_definitions = compose_response_artifact.get("generated_view_definitions") or []
    compose_trace_stages = _trace_stage_names(compose_response_artifact.get("trace"))
    followup_contract = planning_artifact.get("downstream_followup_contract", {})
    aoi_handoff = planning_artifact.get("aoi_composition_handoff_plan") or {}
    direct_sections_handoff = planning_artifact.get("direct_sections_composition_handoff_plan") or {}
    support_snapshot_artifact = evidence.embedded_snapshot_artifact
    requires_bundle_binding = case_definition.case_key in {
        "aoi_compose_selection_current_contract_fresh_campaign",
        "genealogy_direct_sections_compose_current_contract_fresh_campaign",
    }

    if case_definition.case_key in {
        "aoi_compose_selection_current_contract",
        "aoi_compose_selection_current_contract_fresh_campaign",
    }:
        handoff_contract_status = (
            "pass"
            if planning_artifact.get("planning_outcome_kind") == spec.planning_outcome_kind
            and planning_artifact.get("downstream_readiness") == spec.downstream_readiness
            and followup_contract.get("endpoint") == spec.downstream_followup_endpoint
            and aoi_handoff.get("compose_entrypoint_kind") == spec.compose_entrypoint_kind
            else "fail"
        )
        planner_presentation_status = (
            "pass"
            if snapshot_artifact.get("planning_decision_id") == case_definition.subject_identity
            and planning_artifact.get("planning_decision_id") == case_definition.subject_identity
            and (
                not requires_bundle_binding
                or evidence.bundle_planning_decision_id == case_definition.subject_identity
            )
            and evidence.compose_binding_planning_decision_id == case_definition.subject_identity
            and snapshot_artifact.get("workflow_key") == case_definition.workflow_key
            and snapshot_artifact.get("consumer_key") == case_definition.consumer_key
            and snapshot_artifact.get("source_v2_job_id") == spec.source_v2_job_id
            and compose_request_artifact.get("workflow_key") == case_definition.workflow_key
            and compose_request_artifact.get("consumer_key") == case_definition.consumer_key
            and compose_request_artifact.get("source_v2_job_id") == spec.source_v2_job_id
            and aoi_handoff.get("source_v2_job_id") == spec.source_v2_job_id
            and aoi_handoff.get("selected_source_thinker_id")
            == snapshot_artifact.get("selected_source_thinker_id")
            and aoi_handoff.get("selected_source_thinker_name")
            == snapshot_artifact.get("selected_source_thinker_name")
            and compose_request_artifact.get("selection")
            == aoi_handoff.get("selected_sources")
            and compose_request_artifact.get("selection_summary")
            == aoi_handoff.get("selection_summary")
            and compose_presentation.get("workflow_key") == case_definition.workflow_key
            and compose_presentation.get("consumer_key") == case_definition.consumer_key
            else "fail"
        )
    else:
        handoff_contract_status = (
            "pass"
            if planning_artifact.get("planning_outcome_kind") == spec.planning_outcome_kind
            and planning_artifact.get("downstream_readiness") == spec.downstream_readiness
            and followup_contract.get("endpoint") == spec.downstream_followup_endpoint
            and followup_contract.get("handoff_kind") == spec.downstream_followup_handoff_kind
            else "fail"
        )
        planner_presentation_status = (
            "pass"
            if snapshot_artifact.get("planning_decision_id") == case_definition.subject_identity
            and planning_artifact.get("planning_decision_id") == case_definition.subject_identity
            and (
                not requires_bundle_binding
                or evidence.bundle_planning_decision_id == case_definition.subject_identity
            )
            and (
                not requires_bundle_binding
                or evidence.compose_binding_planning_decision_id == case_definition.subject_identity
            )
            and snapshot_artifact.get("workflow_key") == case_definition.workflow_key
            and snapshot_artifact.get("consumer_key") == case_definition.consumer_key
            and snapshot_artifact.get("source_v2_job_id") == spec.source_v2_job_id
            and compose_request_artifact.get("workflow_key") == case_definition.workflow_key
            and compose_request_artifact.get("consumer_key") == case_definition.consumer_key
            and direct_sections_handoff.get("source_v2_job_id") == spec.source_v2_job_id
            and compose_request_artifact.get("user_intent")
            == direct_sections_handoff.get("resolved_intent_seed")
            and bool(compose_request_artifact.get("prose_sections"))
            and bool(direct_sections_handoff.get("prose_sections"))
            and compose_request_artifact.get("prose_sections")
            == direct_sections_handoff.get("prose_sections")
            and compose_presentation.get("workflow_key") == case_definition.workflow_key
            and compose_presentation.get("consumer_key") == case_definition.consumer_key
            and (
                support_snapshot_artifact is None
                or (
                    support_snapshot_artifact.get("planning_decision", {}).get("planning_decision_id")
                    == case_definition.subject_identity
                    and support_snapshot_artifact.get("workflow_key") == case_definition.workflow_key
                    and support_snapshot_artifact.get("consumer_key") == case_definition.consumer_key
                    and support_snapshot_artifact.get("source_v2_job_id") == spec.source_v2_job_id
                )
            )
            else "fail"
        )

    presentation_contract_status = (
        "pass"
        if compose_presentation.get("workflow_key") == case_definition.workflow_key
        and compose_presentation.get("consumer_key") == case_definition.consumer_key
        and compose_presentation.get("resolver_version") == spec.compose_resolver_version
        and compose_presentation.get("view_count") == len(generated_view_definitions)
        else "fail"
    )

    composition_trace_status = (
        "pass"
        if all(stage in compose_trace_stages for stage in spec.compose_trace_stages)
        else "fail"
    )

    checks = [
        EvaluationCheck(
            check_key="handoff_contract_fidelity",
            label="Planner handoff contract matches the declared composition surface",
            status=handoff_contract_status,
            summary=(
                "planning_outcome_kind={planning_outcome_kind} "
                "downstream_readiness={downstream_readiness} "
                "followup_endpoint={followup_endpoint}"
            ).format(
                planning_outcome_kind=planning_artifact.get("planning_outcome_kind"),
                downstream_readiness=planning_artifact.get("downstream_readiness"),
                followup_endpoint=followup_contract.get("endpoint"),
            ),
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=evidence.planning_refs,
            observed_values={
                "planning_outcome_kind": planning_artifact.get("planning_outcome_kind"),
                "downstream_readiness": planning_artifact.get("downstream_readiness"),
                "downstream_followup_contract": followup_contract,
                "aoi_compose_entrypoint_kind": aoi_handoff.get("compose_entrypoint_kind"),
                "genealogy_handoff_kind": followup_contract.get("handoff_kind"),
            },
        ),
        EvaluationCheck(
            check_key="planner_presentation_agreement",
            label="Planning truth, compose request, and served presentation agree for the declared case",
            status=planner_presentation_status,
            summary=(
                "bundle_planning_decision_id={bundle_planning_decision_id} "
                "planning_decision_id={planning_decision_id} "
                "compose_binding_planning_decision_id={compose_binding_planning_decision_id} "
                "presentation_workflow_key={presentation_workflow_key} "
                "presentation_consumer_key={presentation_consumer_key}"
            ).format(
                bundle_planning_decision_id=evidence.bundle_planning_decision_id,
                planning_decision_id=snapshot_artifact.get("planning_decision_id"),
                compose_binding_planning_decision_id=evidence.compose_binding_planning_decision_id,
                presentation_workflow_key=compose_presentation.get("workflow_key"),
                presentation_consumer_key=compose_presentation.get("consumer_key"),
            ),
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=(
                evidence.planning_refs
                + evidence.snapshot_refs
                + evidence.compose_request_refs
                + evidence.compose_response_refs
            ),
            observed_values={
                "bundle_planning_decision_id": evidence.bundle_planning_decision_id,
                "snapshot_planning_decision_id": snapshot_artifact.get("planning_decision_id"),
                "compose_binding_planning_decision_id": evidence.compose_binding_planning_decision_id,
                "snapshot_workflow_key": snapshot_artifact.get("workflow_key"),
                "snapshot_consumer_key": snapshot_artifact.get("consumer_key"),
                "snapshot_source_v2_job_id": snapshot_artifact.get("source_v2_job_id"),
                "compose_request_workflow_key": compose_request_artifact.get("workflow_key"),
                "compose_request_consumer_key": compose_request_artifact.get("consumer_key"),
                "compose_request_source_v2_job_id": compose_request_artifact.get("source_v2_job_id"),
                "presentation_workflow_key": compose_presentation.get("workflow_key"),
                "presentation_consumer_key": compose_presentation.get("consumer_key"),
                "selected_source_thinker_id": snapshot_artifact.get("selected_source_thinker_id"),
                "selected_source_thinker_name": snapshot_artifact.get("selected_source_thinker_name"),
            },
        ),
        EvaluationCheck(
            check_key="presentation_contract_fidelity",
            label="Compose response presentation contract matches the declared case",
            status=presentation_contract_status,
            summary=(
                "presentation_workflow_key={presentation_workflow_key} "
                "presentation_consumer_key={presentation_consumer_key} "
                "resolver_version={resolver_version} "
                "view_count={view_count} "
                "generated_view_definition_count={generated_view_definition_count}"
            ).format(
                presentation_workflow_key=compose_presentation.get("workflow_key"),
                presentation_consumer_key=compose_presentation.get("consumer_key"),
                resolver_version=compose_presentation.get("resolver_version"),
                view_count=compose_presentation.get("view_count"),
                generated_view_definition_count=len(generated_view_definitions),
            ),
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=evidence.compose_response_refs,
            observed_values={
                "presentation_workflow_key": compose_presentation.get("workflow_key"),
                "presentation_consumer_key": compose_presentation.get("consumer_key"),
                "resolver_version": compose_presentation.get("resolver_version"),
                "presentation_view_count": compose_presentation.get("view_count"),
                "generated_view_definition_count": len(generated_view_definitions),
            },
        ),
        EvaluationCheck(
            check_key="composition_trace_integrity",
            label="Compose trace includes the required stages for the declared composition surface",
            status=composition_trace_status,
            summary=f"compose_trace_stages={compose_trace_stages}",
            evidence_mode="frozen_artifact",
            evidence_observed_at=observed_at,
            live_revalidation_performed=False,
            evidence_refs=evidence.compose_response_refs,
            observed_values={
                "compose_trace_stages": compose_trace_stages,
            },
        ),
    ]

    dimension_summaries = [
        _single_check_dimension("handoff_contract_fidelity", checks, "handoff_contract_fidelity"),
        _single_check_dimension(
            "planner_presentation_agreement", checks, "planner_presentation_agreement"
        ),
        _single_check_dimension(
            "presentation_contract_fidelity", checks, "presentation_contract_fidelity"
        ),
        _single_check_dimension("composition_trace_integrity", checks, "composition_trace_integrity"),
    ]

    return _build_report(
        report_id=report_id,
        created_at=created_at,
        pack_definition=pack_definition,
        case_definition=case_definition,
        checks=checks,
        dimension_summaries=dimension_summaries,
        input_evidence_refs=[ref for _, ref in frozen_artifacts.values()],
    )


def _build_report(
    *,
    report_id: str,
    created_at: str,
    pack_definition: FrozenEvaluationPackDefinition,
    case_definition: FrozenEvaluationCaseDefinition,
    checks: list[EvaluationCheck],
    dimension_summaries: list[EvaluationDimensionSummary],
    input_evidence_refs: list[EvaluationEvidenceRef],
) -> PersistedEvaluationReport:
    return PersistedEvaluationReport(
        evaluation_report_id=report_id,
        created_at=created_at,
        evaluation_pack_key=pack_definition.evaluation_pack_key,
        case_key=case_definition.case_key,
        subject_kind=case_definition.subject_kind,
        subject_identity=case_definition.subject_identity,
        workflow_key=case_definition.workflow_key,
        consumer_key=case_definition.consumer_key,
        supporting_subjects=case_definition.supporting_subjects,
        input_evidence_refs=input_evidence_refs,
        checks=checks,
        dimension_summaries=dimension_summaries,
        overall_verdict=_derive_overall_verdict(checks),
    )


def _error_report(
    *,
    report_id: str,
    created_at: str,
    pack_definition: FrozenEvaluationPackDefinition,
    case_definition: FrozenEvaluationCaseDefinition,
    summary: str,
) -> PersistedEvaluationReport:
    check = EvaluationCheck(
        check_key="evaluation_error",
        label="Evaluation completed with an evidence or harness error",
        status="error",
        summary=summary,
        evidence_mode="frozen_artifact",
        evidence_observed_at=created_at,
        live_revalidation_performed=False,
        evidence_refs=[],
        observed_values={},
    )
    return PersistedEvaluationReport(
        evaluation_report_id=report_id,
        created_at=created_at,
        evaluation_pack_key=pack_definition.evaluation_pack_key,
        case_key=case_definition.case_key,
        subject_kind=case_definition.subject_kind,
        subject_identity=case_definition.subject_identity,
        workflow_key=case_definition.workflow_key,
        consumer_key=case_definition.consumer_key,
        supporting_subjects=case_definition.supporting_subjects,
        checks=[check],
        dimension_summaries=[],
        overall_verdict="error",
    )


def _load_case_artifacts(
    case_definition: FrozenEvaluationCaseDefinition,
) -> dict[str, tuple[dict[str, Any], EvaluationEvidenceRef]]:
    artifacts: dict[str, tuple[dict[str, Any], EvaluationEvidenceRef]] = {}
    for artifact_definition in case_definition.artifacts:
        data, ref = _load_frozen_artifact(artifact_definition)
        artifacts[artifact_definition.ref_key] = (data, ref)
    return artifacts


def _load_frozen_artifact(
    artifact_definition: FrozenArtifactDefinition,
) -> tuple[dict[str, Any], EvaluationEvidenceRef]:
    artifact_path = artifact_definition.absolute_path
    if not artifact_path.exists():
        raise FrozenEvidenceIntegrityError(
            f"Frozen artifact missing: {artifact_definition.relative_path}"
        )
    observed_sha256 = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
    if observed_sha256 != artifact_definition.expected_sha256:
        raise FrozenEvidenceIntegrityError(
            f"Frozen artifact hash mismatch for {artifact_definition.relative_path}: "
            f"expected {artifact_definition.expected_sha256}, observed {observed_sha256}"
        )
    try:
        data = json.loads(artifact_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise FrozenEvidenceIntegrityError(
            f"Frozen artifact is not valid JSON: {artifact_definition.relative_path}"
        ) from exc
    return data, EvaluationEvidenceRef(
        ref_key=artifact_definition.ref_key,
        source_kind="frozen_artifact",
        locator=str(artifact_path),
        expected_sha256=artifact_definition.expected_sha256,
        observed_sha256=observed_sha256,
    )


def _find_case(summary_data: dict[str, Any], case_key: str) -> dict[str, Any]:
    for case in summary_data.get("cases", []):
        if case.get("case_key") == case_key:
            return case
    return {}


def _safe_call(func: Callable[..., Any], *args: Any, **kwargs: Any) -> tuple[Optional[Any], Optional[str]]:
    try:
        return func(*args, **kwargs), None
    except Exception as exc:
        return None, str(exc)


def _extract_routing_planning_evidence(
    *,
    case_definition: FrozenEvaluationCaseDefinition,
    frozen_artifacts: dict[str, tuple[dict[str, Any], EvaluationEvidenceRef]],
) -> _RoutingPlanningCaseEvidence:
    if case_definition.case_key == "aoi_saved_result_handoff_current_contract":
        route_artifact, route_ref = frozen_artifacts["aoi_route_current_contract"]
        planning_artifact, planning_ref = frozen_artifacts["aoi_planning_current_contract"]
        snapshot_artifact, snapshot_ref = frozen_artifacts["aoi_planning_snapshot_current_contract"]
        return _RoutingPlanningCaseEvidence(
            route_artifact=route_artifact,
            planning_artifact=planning_artifact,
            snapshot_artifact=snapshot_artifact,
            embedded_snapshot_artifact=None,
            route_refs=[route_ref],
            planning_refs=[planning_ref],
            snapshot_refs=[snapshot_ref],
        )
    if case_definition.case_key == "genealogy_saved_result_direct_sections_snapshot_march28":
        trace_artifact, trace_ref = frozen_artifacts["phase2_trace_multi_surface"]
        snapshot_artifact, snapshot_ref = frozen_artifacts["genealogy_planning_snapshot"]
        return _RoutingPlanningCaseEvidence(
            route_artifact=trace_artifact.get("routing_decision", {}),
            planning_artifact=trace_artifact.get("planning_decision", {}),
            snapshot_artifact=snapshot_artifact,
            embedded_snapshot_artifact=trace_artifact.get("planning_snapshot"),
            route_refs=[
                _surface_ref(
                    trace_ref,
                    surface="routing_decision",
                    note="Multi-surface genealogy trace artifact supplying routing evidence.",
                )
            ],
            planning_refs=[
                _surface_ref(
                    trace_ref,
                    surface="planning_decision",
                    note="Multi-surface genealogy trace artifact supplying planning evidence.",
                )
            ],
            snapshot_refs=[
                _surface_ref(
                    trace_ref,
                    surface="planning_snapshot",
                    note="Embedded planning snapshot from the multi-surface genealogy trace artifact.",
                ),
                snapshot_ref,
            ],
        )
    raise ValueError(f"Unknown routing/planning case_key: {case_definition.case_key}")


def _extract_planner_presentation_evidence(
    *,
    case_definition: FrozenEvaluationCaseDefinition,
    frozen_artifacts: dict[str, tuple[dict[str, Any], EvaluationEvidenceRef]],
) -> _PlannerPresentationCaseEvidence:
    if case_definition.case_key == "aoi_compose_selection_current_contract":
        bundle_artifact, bundle_ref = frozen_artifacts["aoi_transient_compose_current_contract"]
        return _PlannerPresentationCaseEvidence(
            planning_artifact=bundle_artifact.get("planning_decision", {}),
            snapshot_artifact=bundle_artifact.get("planning_snapshot", {}),
            embedded_snapshot_artifact=None,
            compose_request_artifact=bundle_artifact.get("compose_from_selection", {}).get(
                "request_json", {}
            ),
            compose_response_artifact=bundle_artifact.get("compose_from_selection", {}).get(
                "response_json", {}
            ),
            bundle_planning_decision_id=bundle_artifact.get("planning_decision_id"),
            compose_binding_planning_decision_id=bundle_artifact.get("compose_from_selection", {}).get(
                "planning_decision_id"
            ),
            planning_refs=[
                _surface_ref(
                    bundle_ref,
                    surface="planning_decision",
                    note="AOI transient compose bundle supplying planning evidence.",
                )
            ],
            snapshot_refs=[
                _surface_ref(
                    bundle_ref,
                    surface="planning_snapshot",
                    note="AOI transient compose bundle supplying persisted planning snapshot evidence.",
                )
            ],
            compose_request_refs=[
                _surface_ref(
                    bundle_ref,
                    surface="compose_from_selection.request_json",
                    note="AOI transient compose bundle supplying compose-from-selection request evidence.",
                ),
                _surface_ref(
                    bundle_ref,
                    surface="compose_from_selection.planning_decision_id",
                    note="AOI transient compose bundle binding compose execution to the persisted planning decision.",
                ),
                _surface_ref(
                    bundle_ref,
                    surface="planning_decision_id",
                    note="AOI transient compose bundle top-level binding to the persisted planning decision.",
                ),
            ],
            compose_response_refs=[
                _surface_ref(
                    bundle_ref,
                    surface="compose_from_selection.response_json",
                    note="AOI transient compose bundle supplying compose-from-selection response evidence.",
                )
            ],
        )
    if case_definition.case_key == "aoi_compose_selection_current_contract_fresh_campaign":
        bundle_artifact, bundle_ref = frozen_artifacts["aoi_transient_compose_cross_campaign"]
        return _PlannerPresentationCaseEvidence(
            planning_artifact=bundle_artifact.get("planning_decision", {}),
            snapshot_artifact=bundle_artifact.get("planning_snapshot", {}),
            embedded_snapshot_artifact=None,
            compose_request_artifact=bundle_artifact.get("compose_from_selection", {}).get(
                "request_json", {}
            ),
            compose_response_artifact=bundle_artifact.get("compose_from_selection", {}).get(
                "response_json", {}
            ),
            bundle_planning_decision_id=bundle_artifact.get("planning_decision_id"),
            compose_binding_planning_decision_id=bundle_artifact.get("compose_from_selection", {}).get(
                "planning_decision_id"
            ),
            planning_refs=[
                _surface_ref(
                    bundle_ref,
                    surface="planning_decision",
                    note="Cross-campaign AOI transient compose bundle supplying planning evidence.",
                )
            ],
            snapshot_refs=[
                _surface_ref(
                    bundle_ref,
                    surface="planning_snapshot",
                    note="Cross-campaign AOI transient compose bundle supplying persisted planning snapshot evidence.",
                )
            ],
            compose_request_refs=[
                _surface_ref(
                    bundle_ref,
                    surface="compose_from_selection.request_json",
                    note="Cross-campaign AOI transient compose bundle supplying compose-from-selection request evidence.",
                ),
                _surface_ref(
                    bundle_ref,
                    surface="compose_from_selection.planning_decision_id",
                    note="Cross-campaign AOI transient compose bundle nested binding to the persisted planning decision.",
                ),
                _surface_ref(
                    bundle_ref,
                    surface="planning_decision_id",
                    note="Cross-campaign AOI transient compose bundle top-level binding to the persisted planning decision.",
                ),
            ],
            compose_response_refs=[
                _surface_ref(
                    bundle_ref,
                    surface="compose_from_selection.response_json",
                    note="Cross-campaign AOI transient compose bundle supplying compose-from-selection response evidence.",
                )
            ],
        )
    if case_definition.case_key == "genealogy_direct_sections_compose_snapshot_march28":
        trace_artifact, trace_ref = frozen_artifacts["phase2_trace_multi_surface"]
        snapshot_artifact, snapshot_ref = frozen_artifacts["genealogy_planning_snapshot"]
        return _PlannerPresentationCaseEvidence(
            planning_artifact=trace_artifact.get("planning_decision", {}),
            snapshot_artifact=trace_artifact.get("planning_snapshot", {}),
            embedded_snapshot_artifact=snapshot_artifact,
            compose_request_artifact=trace_artifact.get("lowered_compose_request", {}),
            compose_response_artifact=trace_artifact.get("compose_response", {}),
            bundle_planning_decision_id=None,
            compose_binding_planning_decision_id=trace_artifact.get("planning_snapshot", {}).get(
                "planning_decision_id"
            ),
            planning_refs=[
                _surface_ref(
                    trace_ref,
                    surface="planning_decision",
                    note="Multi-surface genealogy trace artifact supplying planning evidence.",
                )
            ],
            snapshot_refs=[
                _surface_ref(
                    trace_ref,
                    surface="planning_snapshot",
                    note="Multi-surface genealogy trace artifact supplying embedded planning snapshot evidence.",
                ),
                snapshot_ref,
            ],
            compose_request_refs=[
                _surface_ref(
                    trace_ref,
                    surface="lowered_compose_request",
                    note="Multi-surface genealogy trace artifact supplying lowered compose request evidence.",
                )
            ],
            compose_response_refs=[
                _surface_ref(
                    trace_ref,
                    surface="compose_response",
                    note="Multi-surface genealogy trace artifact supplying compose response evidence.",
                )
            ],
        )
    if case_definition.case_key == "genealogy_direct_sections_compose_current_contract_fresh_campaign":
        bundle_artifact, bundle_ref = frozen_artifacts["genealogy_transient_compose_cross_campaign"]
        return _PlannerPresentationCaseEvidence(
            planning_artifact=bundle_artifact.get("planning_decision", {}),
            snapshot_artifact=bundle_artifact.get("planning_snapshot", {}),
            embedded_snapshot_artifact=None,
            compose_request_artifact=bundle_artifact.get("compose_from_intent", {}).get(
                "request_json", {}
            ),
            compose_response_artifact=bundle_artifact.get("compose_from_intent", {}).get(
                "response_json", {}
            ),
            bundle_planning_decision_id=bundle_artifact.get("planning_decision_id"),
            compose_binding_planning_decision_id=bundle_artifact.get("compose_from_intent", {}).get(
                "planning_decision_id"
            ),
            planning_refs=[
                _surface_ref(
                    bundle_ref,
                    surface="planning_decision",
                    note="Cross-campaign genealogy transient compose bundle supplying planning evidence.",
                )
            ],
            snapshot_refs=[
                _surface_ref(
                    bundle_ref,
                    surface="planning_snapshot",
                    note="Cross-campaign genealogy transient compose bundle supplying persisted planning snapshot evidence.",
                )
            ],
            compose_request_refs=[
                _surface_ref(
                    bundle_ref,
                    surface="compose_from_intent.request_json",
                    note="Cross-campaign genealogy transient compose bundle supplying compose-from-intent request evidence.",
                ),
                _surface_ref(
                    bundle_ref,
                    surface="compose_from_intent.planning_decision_id",
                    note="Cross-campaign genealogy transient compose bundle nested wrapper binding to the persisted planning decision.",
                ),
                _surface_ref(
                    bundle_ref,
                    surface="planning_decision_id",
                    note="Cross-campaign genealogy transient compose bundle top-level binding to the persisted planning decision.",
                ),
            ],
            compose_response_refs=[
                _surface_ref(
                    bundle_ref,
                    surface="compose_from_intent.response_json",
                    note="Cross-campaign genealogy transient compose bundle supplying compose-from-intent response evidence.",
                )
            ],
        )
    raise ValueError(f"Unknown planner/presentation case_key: {case_definition.case_key}")


def _surface_ref(
    ref: EvaluationEvidenceRef,
    *,
    surface: str,
    note: str | None = None,
) -> EvaluationEvidenceRef:
    return EvaluationEvidenceRef(
        ref_key=f"{ref.ref_key}:{surface}",
        source_kind=ref.source_kind,
        locator=f"{ref.locator}#{surface}",
        expected_sha256=ref.expected_sha256,
        observed_sha256=ref.observed_sha256,
        note=note,
    )


def _trace_stage_names(trace_entries: Any) -> list[str]:
    if isinstance(trace_entries, dict):
        trace_entries = trace_entries.get("entries")
    if not isinstance(trace_entries, list):
        return []
    stages: list[str] = []
    for entry in trace_entries:
        if isinstance(entry, dict):
            stage = entry.get("stage")
            if isinstance(stage, str):
                stages.append(stage)
    return stages


def _derive_overall_verdict(checks: list[EvaluationCheck]) -> str:
    required_checks = [check for check in checks if check.required]
    if any(check.status == "error" for check in required_checks):
        return "error"
    if any(check.status == "fail" for check in required_checks):
        return "fail"
    return "pass"


def _single_check_dimension(
    dimension_key: str,
    checks: list[EvaluationCheck],
    check_key: str,
) -> EvaluationDimensionSummary:
    by_key = {check.check_key: check for check in checks}
    check = by_key[check_key]
    return EvaluationDimensionSummary(
        dimension_key=dimension_key,
        status=check.status,
        summary=check.summary,
        supporting_checks=[check_key],
    )


def _multi_check_dimension(
    dimension_key: str,
    checks: list[EvaluationCheck],
    check_keys: list[str],
    *,
    pass_summary: str,
    fail_summary: str,
) -> EvaluationDimensionSummary:
    by_key = {check.check_key: check for check in checks}
    statuses = [by_key[key].status for key in check_keys]
    if any(status == "error" for status in statuses):
        status = "error"
        summary = fail_summary
    elif any(status == "fail" for status in statuses):
        status = "fail"
        summary = fail_summary
    elif all(status == "not_applicable" for status in statuses):
        status = "not_applicable"
        summary = "All supporting checks were not applicable."
    else:
        status = "pass"
        summary = pass_summary
    return EvaluationDimensionSummary(
        dimension_key=dimension_key,
        status=status,
        summary=summary,
        supporting_checks=check_keys,
    )


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def main(argv: Optional[list[str]] = None) -> int:
    """CLI entrypoint for deterministic frozen-pack report generation."""

    parser = argparse.ArgumentParser(description="Generate governance reports for one frozen pack.")
    parser.add_argument("--pack-key", required=True, help="Frozen evaluation pack key")
    args = parser.parse_args(argv)

    reports = run_frozen_pack(args.pack_key, save_report=True)
    for report in reports:
        summary = EvaluationReportSummary(
            evaluation_report_id=report.evaluation_report_id,
            created_at=report.created_at,
            evaluation_pack_key=report.evaluation_pack_key,
            case_key=report.case_key,
            subject_kind=report.subject_kind,
            subject_identity=report.subject_identity,
            workflow_key=report.workflow_key,
            consumer_key=report.consumer_key,
            overall_verdict=report.overall_verdict,
        )
        print(summary.model_dump_json())
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
