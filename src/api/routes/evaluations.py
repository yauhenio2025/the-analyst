"""Read-only routes for persisted evaluation reports, gates, reviews, and resolutions."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.evaluations.gate_schemas import (
    EvaluationGateDecisionListResponse,
    PersistedEvaluationGateDecision,
)
from src.evaluations.gate_store import (
    list_evaluation_gate_decisions,
    load_evaluation_gate_decision,
)
from src.evaluations.governance_status import (
    GovernanceStatusDerivationError,
    load_current_evaluation_governance_status,
)
from src.evaluations.governance_status_schemas import (
    EvaluationCurrentGovernanceStatusResponse,
)
from src.evaluations.review_schemas import (
    EvaluationReviewDecisionListResponse,
    PersistedEvaluationReviewDecision,
)
from src.evaluations.review_store import (
    list_evaluation_review_decisions,
    load_evaluation_review_decision,
)
from src.evaluations.resolution_schemas import (
    EvaluationCurrentDispositionResolutionResponse,
    EvaluationDispositionResolutionListResponse,
    PersistedEvaluationDispositionResolution,
)
from src.evaluations.resolution_store import (
    list_evaluation_disposition_resolutions,
    load_current_evaluation_disposition_resolution,
    load_evaluation_disposition_resolution,
)
from src.evaluations.report_store import (
    list_evaluation_reports,
    load_evaluation_report,
)
from src.evaluations.schemas import (
    EvaluationReportListResponse,
    PersistedEvaluationReport,
)


router = APIRouter(prefix="/evaluations", tags=["evaluations"])


@router.get("/reports/{evaluation_report_id}", response_model=PersistedEvaluationReport)
async def get_evaluation_report_endpoint(evaluation_report_id: str):
    """Fetch one persisted evaluation report by id."""

    report = load_evaluation_report(evaluation_report_id)
    if report is None:
        raise HTTPException(
            status_code=404,
            detail=f"Evaluation report '{evaluation_report_id}' not found",
        )
    return report


@router.get("/reports", response_model=EvaluationReportListResponse)
async def list_evaluation_reports_endpoint(
    evaluation_pack_key: str | None = None,
    case_key: str | None = None,
    limit: int = 20,
):
    """List persisted evaluation report summaries newest-first."""

    reports = list_evaluation_reports(
        evaluation_pack_key=evaluation_pack_key,
        case_key=case_key,
        limit=limit,
    )
    return EvaluationReportListResponse(reports=reports, count=len(reports))


@router.get(
    "/governance-status/current",
    response_model=EvaluationCurrentGovernanceStatusResponse,
)
async def get_current_evaluation_governance_status_endpoint(
    resolution_key: str,
    gate_decision_id: str,
):
    """Fetch the semantic current governance status for one bounded scope."""

    try:
        return load_current_evaluation_governance_status(
            resolution_key=resolution_key,
            gate_decision_id=gate_decision_id,
        )
    except GovernanceStatusDerivationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@router.get("/gates/{gate_decision_id}", response_model=PersistedEvaluationGateDecision)
async def get_evaluation_gate_decision_endpoint(gate_decision_id: str):
    """Fetch one persisted evaluation gate decision by id."""

    gate_decision = load_evaluation_gate_decision(gate_decision_id)
    if gate_decision is None:
        raise HTTPException(
            status_code=404,
            detail=f"Evaluation gate decision '{gate_decision_id}' not found",
        )
    return gate_decision


@router.get("/gates", response_model=EvaluationGateDecisionListResponse)
async def list_evaluation_gate_decisions_endpoint(
    gate_key: str | None = None,
    evaluation_pack_key: str | None = None,
    limit: int = 20,
):
    """List persisted gate-decision summaries newest-first."""

    gate_decisions = list_evaluation_gate_decisions(
        gate_key=gate_key,
        evaluation_pack_key=evaluation_pack_key,
        limit=limit,
    )
    return EvaluationGateDecisionListResponse(gates=gate_decisions, count=len(gate_decisions))


@router.get("/reviews/{review_decision_id}", response_model=PersistedEvaluationReviewDecision)
async def get_evaluation_review_decision_endpoint(review_decision_id: str):
    """Fetch one persisted evaluation review decision by id."""

    review_decision = load_evaluation_review_decision(review_decision_id)
    if review_decision is None:
        raise HTTPException(
            status_code=404,
            detail=f"Evaluation review decision '{review_decision_id}' not found",
        )
    return review_decision


@router.get("/reviews", response_model=EvaluationReviewDecisionListResponse)
async def list_evaluation_review_decisions_endpoint(
    gate_decision_id: str | None = None,
    gate_key: str | None = None,
    evaluation_pack_key: str | None = None,
    limit: int = 20,
):
    """List persisted review-decision summaries newest-first."""

    review_decisions = list_evaluation_review_decisions(
        gate_decision_id=gate_decision_id,
        gate_key=gate_key,
        evaluation_pack_key=evaluation_pack_key,
        limit=limit,
    )
    return EvaluationReviewDecisionListResponse(
        reviews=review_decisions,
        count=len(review_decisions),
    )


@router.get(
    "/resolutions/current",
    response_model=EvaluationCurrentDispositionResolutionResponse,
)
async def get_current_evaluation_disposition_resolution_endpoint(
    resolution_key: str,
    gate_decision_id: str,
):
    """Fetch the canonical current disposition resolution for one bounded scope."""

    resolution = load_current_evaluation_disposition_resolution(
        resolution_key=resolution_key,
        gate_decision_id=gate_decision_id,
    )
    if resolution is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "No current evaluation disposition resolution was found for "
                f"resolution_key='{resolution_key}' and gate_decision_id='{gate_decision_id}'"
            ),
        )
    return EvaluationCurrentDispositionResolutionResponse(
        resolution_key=resolution_key,
        gate_decision_id=gate_decision_id,
        resolution=resolution,
    )


@router.get(
    "/resolutions/{resolution_id}",
    response_model=PersistedEvaluationDispositionResolution,
)
async def get_evaluation_disposition_resolution_endpoint(resolution_id: str):
    """Fetch one persisted evaluation disposition resolution by id."""

    resolution = load_evaluation_disposition_resolution(resolution_id)
    if resolution is None:
        raise HTTPException(
            status_code=404,
            detail=f"Evaluation disposition resolution '{resolution_id}' not found",
        )
    return resolution


@router.get(
    "/resolutions",
    response_model=EvaluationDispositionResolutionListResponse,
)
async def list_evaluation_disposition_resolutions_endpoint(
    resolution_key: str | None = None,
    review_decision_id: str | None = None,
    gate_decision_id: str | None = None,
    evaluation_pack_key: str | None = None,
    limit: int = 20,
):
    """List persisted disposition-resolution summaries newest-first."""

    resolutions = list_evaluation_disposition_resolutions(
        resolution_key=resolution_key,
        review_decision_id=review_decision_id,
        gate_decision_id=gate_decision_id,
        evaluation_pack_key=evaluation_pack_key,
        limit=limit,
    )
    return EvaluationDispositionResolutionListResponse(
        resolutions=resolutions,
        count=len(resolutions),
    )
