"""Stage 10 read-only source-backed readiness inspection."""

from __future__ import annotations

from typing import Optional, get_args

from src.analysis_products.result_contract import (
    DEFAULT_CONSUMER_KEY,
    GENEALOGY_WORKFLOW_KEY,
    build_result_manifest,
)
from src.analysis_products.schemas import (
    AoiSourceBackedReadinessDetail,
    GenealogySourceBackedReadinessDetail,
    SourceBackedReadinessDecision,
    SourceBackedReadinessTraceEntry,
)
from src.aoi.constants import AOI_WORKFLOW_KEY
from src.executor.job_manager import get_job
from src.presenter.bounded_dynamic_composition import (
    BoundedCompositionValidationError,
    CompositionIssue,
    inspect_runtime_composition_on_payload_copy,
    list_supported_composition_modes_for_workflow,
)
from src.presenter.compose_from_intent import (
    get_transient_handoff_capability_error,
)
from src.presenter.composition_source_bridge import (
    evaluate_compose_profile_feasibility,
    resolve_source_catalog,
)
from src.presenter.presentation_api import _prepare_page_payloads
from src.presenter.schemas import ComposeFromSourceProfile


class SourceBackedReadinessRequestError(ValueError):
    """Raised when the readiness request is malformed for the bounded Stage 10 slice."""


class SourceBackedReadinessNotFoundError(ValueError):
    """Raised when the requested job does not exist."""


_AOI_PROFILES = tuple(get_args(ComposeFromSourceProfile))
_AOI_SOURCE_PROFILE_HANDOFF_KIND = "source_profile"


def build_source_backed_readiness(
    job_id: str,
    *,
    consumer_key: str = DEFAULT_CONSUMER_KEY,
    profile: Optional[str] = None,
    composition_mode: Optional[str] = None,
) -> SourceBackedReadinessDecision:
    """Inspect source-backed readiness without mutating presenter-owned state."""

    if profile and composition_mode:
        raise SourceBackedReadinessRequestError("Provide either profile or composition_mode, not both.")

    job = get_job(job_id)
    if job is None:
        raise SourceBackedReadinessNotFoundError(f"Job not found: {job_id}")

    workflow_key = job.get("workflow_key") or ""
    trace = [
        SourceBackedReadinessTraceEntry(
            stage="job_lookup",
            details={
                "job_id": job_id,
                "workflow_key": workflow_key,
                "consumer_key": consumer_key,
            },
        )
    ]

    if workflow_key == AOI_WORKFLOW_KEY:
        return _build_aoi_readiness(
            job_id=job_id,
            consumer_key=consumer_key,
            profile=profile,
            composition_mode=composition_mode,
            trace=trace,
        )

    if workflow_key == GENEALOGY_WORKFLOW_KEY:
        return _build_genealogy_readiness(
            job_id=job_id,
            consumer_key=consumer_key,
            profile=profile,
            composition_mode=composition_mode,
            trace=trace,
        )

    raise SourceBackedReadinessRequestError(
        "source-backed readiness is only supported for AOI and intellectual_genealogy workflows in Stage 10."
    )


def _build_aoi_readiness(
    *,
    job_id: str,
    consumer_key: str,
    profile: Optional[str],
    composition_mode: Optional[str],
    trace: list[SourceBackedReadinessTraceEntry],
) -> SourceBackedReadinessDecision:
    if composition_mode is not None:
        raise SourceBackedReadinessRequestError(
            "composition_mode readiness is out of scope for AOI Stage 10; use profile for AOI jobs."
        )
    if profile is not None and profile not in _AOI_PROFILES:
        raise SourceBackedReadinessRequestError("unknown_aoi_profile")

    inspected_profiles = list(_AOI_PROFILES)
    trace.append(
        SourceBackedReadinessTraceEntry(
            stage="selector_validation",
            details={
                "selector_kind": "profile",
                "requested_selector": profile,
                "inspected_selectors": inspected_profiles,
            },
        )
    )

    catalog = resolve_source_catalog(source_v2_job_id=job_id)
    trace.append(
        SourceBackedReadinessTraceEntry(
            stage="source_catalog_resolution",
            details=catalog.to_trace_dict(),
        )
    )

    allowed_profiles, blocked_profiles = evaluate_compose_profile_feasibility(catalog)
    feasible_selectors = [candidate for candidate in inspected_profiles if candidate in allowed_profiles]
    allowed_selectors: list[str] = []
    blocked_selectors: dict[str, list[str]] = {}
    consumer_profile_errors: list[str] = []

    for candidate in inspected_profiles:
        feasibility_blockers = list(blocked_profiles.get(candidate, []))
        if feasibility_blockers:
            blocked_selectors[candidate] = feasibility_blockers
            continue

        consumer_handoff_error = get_transient_handoff_capability_error(
            workflow_key=AOI_WORKFLOW_KEY,
            consumer_key=consumer_key,
            handoff_kind=_AOI_SOURCE_PROFILE_HANDOFF_KIND,
            route_label="compose-from-source",
            profile=candidate,
        )
        if consumer_handoff_error is not None:
            blocked_selectors[candidate] = [consumer_handoff_error]
            if consumer_handoff_error not in consumer_profile_errors:
                consumer_profile_errors.append(consumer_handoff_error)
            continue

        allowed_selectors.append(candidate)

    requested_selector_status = _requested_selector_status(
        requested_selector=profile,
        allowed_selectors=allowed_selectors,
    )

    followup_blockers: list[str] = []
    if not feasible_selectors:
        followup_blockers.append("no_feasible_profiles")
    elif not allowed_selectors:
        followup_blockers.extend(consumer_profile_errors)
    followup_readiness_status = "ready" if not followup_blockers else "blocked"

    trace.append(
        SourceBackedReadinessTraceEntry(
            stage="profile_feasibility",
            details={
                "allowed_profiles": list(allowed_profiles),
                "blocked_profiles": blocked_profiles,
                "consumer_allowed_profiles": allowed_selectors,
                "followup_blockers": followup_blockers,
            },
        )
    )

    downstream_followup_contract = {
        "method": "POST",
        "endpoint": "/v1/presenter/compose-from-source",
        "allowed_profiles": allowed_selectors,
        "request_fields": {
            "workflow_key": AOI_WORKFLOW_KEY,
            "consumer_key": consumer_key,
            "source_v2_job_id": job_id,
            "profile": profile if profile in allowed_selectors else "<required_from_allowed_profiles>",
        },
    }
    if followup_blockers:
        downstream_followup_contract["blocking_reasons"] = followup_blockers

    return SourceBackedReadinessDecision(
        job_id=job_id,
        workflow_key=AOI_WORKFLOW_KEY,
        consumer_key=consumer_key,
        implementation_kind="aoi_source_reconstruction",
        selector_lifecycle_phase="source_selection",
        requested_selector=profile,
        requested_selector_status=requested_selector_status,
        followup_readiness_status=followup_readiness_status,
        readiness_status=_rollup_readiness_status(
            requested_selector=profile,
            requested_selector_status=requested_selector_status,
            followup_readiness_status=followup_readiness_status,
            allowed_selectors=allowed_selectors,
            blocked_selectors=blocked_selectors,
        ),
        allowed_selectors=allowed_selectors,
        blocked_selectors=blocked_selectors,
        downstream_followup_contract=downstream_followup_contract,
        trace=trace,
        aoi_readiness_detail=AoiSourceBackedReadinessDetail(
            source_v2_job_id=job_id,
            selected_source_thinker_id=catalog.selected_source_thinker_id,
            selected_source_thinker_name=catalog.selected_source_thinker_name,
            expected_source_families=[candidate.source_family_key for candidate in catalog.candidates],
            available_source_families=[
                candidate.source_family_key
                for candidate in catalog.candidates
                if candidate.candidate_state == "available"
            ],
            expected_producer_engines=sorted({candidate.engine_key for candidate in catalog.candidates}),
        ),
    )


def _build_genealogy_readiness(
    *,
    job_id: str,
    consumer_key: str,
    profile: Optional[str],
    composition_mode: Optional[str],
    trace: list[SourceBackedReadinessTraceEntry],
) -> SourceBackedReadinessDecision:
    if profile is not None:
        raise SourceBackedReadinessRequestError(
            "profile readiness is only supported for AOI workflows."
        )

    supported_modes = list_supported_composition_modes_for_workflow(GENEALOGY_WORKFLOW_KEY)
    if composition_mode is not None and composition_mode not in supported_modes:
        raise SourceBackedReadinessRequestError("unknown_genealogy_composition_mode")

    inspected_modes = supported_modes
    trace.append(
        SourceBackedReadinessTraceEntry(
            stage="selector_validation",
            details={
                "selector_kind": "composition_mode",
                "requested_selector": composition_mode,
                "inspected_selectors": inspected_modes,
            },
        )
    )

    try:
        manifest = build_result_manifest(job_id, consumer_key=consumer_key)
    except BoundedCompositionValidationError as error:
        blockers = _composition_issue_blockers(error.issues)
        return _build_genealogy_decision(
            job_id=job_id,
            consumer_key=consumer_key,
            manifest_result_state="blocked_by_manifest_validation",
            presentation_status="validation_failed",
            restore_available=False,
            restore_reason="manifest_validation_failed",
            inspected_modes=inspected_modes,
            requested_mode=composition_mode,
            allowed_modes=[],
            blocked_modes={mode: list(blockers) for mode in inspected_modes},
            runtime_inspection_details={},
            trace=trace + [
                SourceBackedReadinessTraceEntry(
                    stage="manifest_gate",
                    details={"validation_issues": [issue.model_dump() for issue in error.issues]},
                )
            ],
            followup_blockers=list(blockers),
        )

    trace.append(
        SourceBackedReadinessTraceEntry(
            stage="manifest_gate",
            details={
                "result_state": manifest.result_state,
                "presentation_status": manifest.presentation_status,
                "restore_available": manifest.restore_available,
                "restore_reason": manifest.restore_reason,
            },
        )
    )

    manifest_blockers = _genealogy_manifest_blockers(manifest)
    if manifest_blockers:
        return _build_genealogy_decision(
            job_id=job_id,
            consumer_key=consumer_key,
            manifest_result_state=manifest.result_state,
            presentation_status=manifest.presentation_status,
            restore_available=manifest.restore_available,
            restore_reason=manifest.restore_reason,
            inspected_modes=inspected_modes,
            requested_mode=composition_mode,
            allowed_modes=[],
            blocked_modes={mode: list(manifest_blockers) for mode in inspected_modes},
            runtime_inspection_details={},
            trace=trace,
            followup_blockers=list(manifest_blockers),
        )

    try:
        page_inputs = _prepare_page_payloads(
            job_id,
            consumer_key=consumer_key,
            slim=False,
            read_only=True,
        )
    except BoundedCompositionValidationError as error:
        blockers = _composition_issue_blockers(error.issues)
        return _build_genealogy_decision(
            job_id=job_id,
            consumer_key=consumer_key,
            manifest_result_state=manifest.result_state,
            presentation_status=manifest.presentation_status,
            restore_available=manifest.restore_available,
            restore_reason=manifest.restore_reason,
            inspected_modes=inspected_modes,
            requested_mode=composition_mode,
            allowed_modes=[],
            blocked_modes={mode: list(blockers) for mode in inspected_modes},
            runtime_inspection_details={},
            trace=trace + [
                SourceBackedReadinessTraceEntry(
                    stage="payload_preparation",
                    details={
                        "read_only": True,
                        "validation_issues": [issue.model_dump() for issue in error.issues],
                    },
                )
            ],
            followup_blockers=list(blockers),
        )

    payloads = page_inputs["payloads"]
    workflow_key = page_inputs.get("workflow_key") or GENEALOGY_WORKFLOW_KEY
    trace.append(
        SourceBackedReadinessTraceEntry(
            stage="payload_preparation",
            details={
                "read_only": True,
                "payload_count": len(payloads),
                "workflow_key": workflow_key,
            },
        )
    )

    allowed_modes: list[str] = []
    blocked_modes: dict[str, list[str]] = {}
    runtime_inspection_details: dict[str, dict[str, object]] = {}
    for mode in inspected_modes:
        composition_applied, inspection_details, issues = inspect_runtime_composition_on_payload_copy(
            payloads=payloads,
            workflow_key=workflow_key,
            consumer_key=consumer_key,
            composition_mode=mode,
        )
        if issues:
            blocked_modes[mode] = _composition_issue_blockers(issues)
            continue
        allowed_modes.append(mode)
        runtime_inspection_details[mode] = {
            "composition_applied": composition_applied,
            **({"inspection_details": inspection_details} if inspection_details is not None else {}),
        }

    trace.append(
        SourceBackedReadinessTraceEntry(
            stage="runtime_mode_readiness",
            details={
                "allowed_modes": allowed_modes,
                "blocked_modes": blocked_modes,
            },
        )
    )

    followup_blockers = [] if allowed_modes else ["no_feasible_composition_modes"]
    return _build_genealogy_decision(
        job_id=job_id,
        consumer_key=consumer_key,
        manifest_result_state=manifest.result_state,
        presentation_status=manifest.presentation_status,
        restore_available=manifest.restore_available,
        restore_reason=manifest.restore_reason,
        inspected_modes=inspected_modes,
        requested_mode=composition_mode,
        allowed_modes=allowed_modes,
        blocked_modes=blocked_modes,
        runtime_inspection_details=runtime_inspection_details,
        trace=trace,
        followup_blockers=followup_blockers,
    )


def _build_genealogy_decision(
    *,
    job_id: str,
    consumer_key: str,
    manifest_result_state: str,
    presentation_status: str,
    restore_available: bool,
    restore_reason: str,
    inspected_modes: list[str],
    requested_mode: Optional[str],
    allowed_modes: list[str],
    blocked_modes: dict[str, list[str]],
    runtime_inspection_details: dict[str, dict[str, object]],
    trace: list[SourceBackedReadinessTraceEntry],
    followup_blockers: list[str],
) -> SourceBackedReadinessDecision:
    requested_selector_status = _requested_selector_status(
        requested_selector=requested_mode,
        allowed_selectors=allowed_modes,
    )
    followup_readiness_status = "ready" if not followup_blockers else "blocked"
    downstream_followup_contract = {
        "method": "GET",
        "endpoint": f"/v1/results/by-job/{job_id}/presentation",
        "allowed_composition_modes": allowed_modes,
        "query_fields": {
            "consumer_key": consumer_key,
            "composition_mode": (
                requested_mode
                if requested_mode in allowed_modes
                else "<required_from_allowed_composition_modes>"
            ),
        },
    }
    if followup_blockers:
        downstream_followup_contract["blocking_reasons"] = followup_blockers

    return SourceBackedReadinessDecision(
        job_id=job_id,
        workflow_key=GENEALOGY_WORKFLOW_KEY,
        consumer_key=consumer_key,
        implementation_kind="genealogy_restore_runtime",
        selector_lifecycle_phase="restore_runtime",
        requested_selector=requested_mode,
        requested_selector_status=requested_selector_status,
        followup_readiness_status=followup_readiness_status,
        readiness_status=_rollup_readiness_status(
            requested_selector=requested_mode,
            requested_selector_status=requested_selector_status,
            followup_readiness_status=followup_readiness_status,
            allowed_selectors=allowed_modes,
            blocked_selectors=blocked_modes,
        ),
        allowed_selectors=allowed_modes,
        blocked_selectors=blocked_modes,
        downstream_followup_contract=downstream_followup_contract,
        trace=trace,
        genealogy_readiness_detail=GenealogySourceBackedReadinessDetail(
            result_state=manifest_result_state,
            presentation_status=presentation_status,
            restore_available=restore_available,
            restore_reason=restore_reason,
            inspected_modes=inspected_modes,
            allowed_modes=allowed_modes,
            blocked_modes=blocked_modes,
            runtime_inspection_details=runtime_inspection_details,
        ),
    )


def _requested_selector_status(
    *,
    requested_selector: Optional[str],
    allowed_selectors: list[str],
) -> str:
    if requested_selector is None:
        return "not_requested"
    return "ready" if requested_selector in allowed_selectors else "blocked"


def _rollup_readiness_status(
    *,
    requested_selector: Optional[str],
    requested_selector_status: str,
    followup_readiness_status: str,
    allowed_selectors: list[str],
    blocked_selectors: dict[str, list[str]],
) -> str:
    if requested_selector is not None:
        if requested_selector_status == "ready":
            return "ready" if followup_readiness_status == "ready" else "partially_ready"
        return "partially_ready" if allowed_selectors else "blocked"

    if followup_readiness_status == "ready":
        if allowed_selectors and not blocked_selectors:
            return "ready"
        if allowed_selectors:
            return "partially_ready"
        return "blocked"

    return "partially_ready" if allowed_selectors else "blocked"


def _composition_issue_blockers(issues: list[CompositionIssue]) -> list[str]:
    blockers: list[str] = []
    for issue in issues:
        parts = [issue.reason]
        if issue.view_key:
            parts.append(f"view={issue.view_key}")
        if issue.field:
            parts.append(f"field={issue.field}")
        if issue.message:
            parts.append(issue.message)
        blockers.append(" | ".join(parts))
    return blockers


def _genealogy_manifest_blockers(manifest) -> list[str]:
    blockers: list[str] = []
    if manifest.presentation_status != "completed":
        blockers.append(f"presentation_status={manifest.presentation_status}")
    if not manifest.restore_available:
        blockers.append(f"restore_reason={manifest.restore_reason}")
    return blockers
