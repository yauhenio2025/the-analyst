"""File-backed persistence for evaluation disposition resolutions."""

from __future__ import annotations

from pathlib import Path
from typing import Optional
from uuid import uuid4

from src.evaluations.resolution_schemas import (
    EvaluationDispositionResolutionSummary,
    PersistedEvaluationDispositionResolution,
)


EVALUATION_RESOLUTIONS_DIR = Path(__file__).parent / "resolutions"


def build_evaluation_disposition_resolution_id() -> str:
    """Create one analyzer-owned evaluation disposition-resolution id."""

    return f"resolution-{uuid4().hex[:12]}"


def save_evaluation_disposition_resolution(
    resolution: PersistedEvaluationDispositionResolution,
) -> PersistedEvaluationDispositionResolution:
    """Persist one evaluation disposition resolution."""

    EVALUATION_RESOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    resolution_path = EVALUATION_RESOLUTIONS_DIR / f"{resolution.resolution_id}.json"
    resolution_path.write_text(resolution.model_dump_json(indent=2), encoding="utf-8")
    return resolution


def load_evaluation_disposition_resolution(
    resolution_id: str,
) -> Optional[PersistedEvaluationDispositionResolution]:
    """Load one evaluation disposition resolution by id."""

    normalized_id = resolution_id.strip()
    if not normalized_id:
        return None
    resolution_path = EVALUATION_RESOLUTIONS_DIR / f"{normalized_id}.json"
    if not resolution_path.exists():
        return None
    return PersistedEvaluationDispositionResolution.model_validate_json(
        resolution_path.read_text(encoding="utf-8")
    )


def load_current_evaluation_disposition_resolution(
    resolution_key: str,
    gate_decision_id: str,
) -> Optional[PersistedEvaluationDispositionResolution]:
    """Load the authoritative current resolution for one resolution_key + gate_decision_id pair."""

    normalized_resolution_key = resolution_key.strip()
    normalized_gate_decision_id = gate_decision_id.strip()
    if not normalized_resolution_key or not normalized_gate_decision_id:
        return None

    current_resolution: Optional[PersistedEvaluationDispositionResolution] = None
    if not EVALUATION_RESOLUTIONS_DIR.exists():
        return None

    for resolution_path in sorted(EVALUATION_RESOLUTIONS_DIR.glob("resolution-*.json")):
        resolution = PersistedEvaluationDispositionResolution.model_validate_json(
            resolution_path.read_text(encoding="utf-8")
        )
        if resolution.resolution_key != normalized_resolution_key:
            continue
        if resolution.gate_decision_id != normalized_gate_decision_id:
            continue
        if current_resolution is None or resolution.created_at > current_resolution.created_at:
            current_resolution = resolution
    return current_resolution


def list_evaluation_disposition_resolutions(
    *,
    resolution_key: Optional[str] = None,
    review_decision_id: Optional[str] = None,
    gate_decision_id: Optional[str] = None,
    evaluation_pack_key: Optional[str] = None,
    limit: int = 20,
) -> list[EvaluationDispositionResolutionSummary]:
    """List persisted disposition-resolution summaries newest-first."""

    resolutions: list[EvaluationDispositionResolutionSummary] = []
    if not EVALUATION_RESOLUTIONS_DIR.exists():
        return resolutions

    for resolution_path in sorted(EVALUATION_RESOLUTIONS_DIR.glob("resolution-*.json")):
        resolution = PersistedEvaluationDispositionResolution.model_validate_json(
            resolution_path.read_text(encoding="utf-8")
        )
        if resolution_key and resolution.resolution_key != resolution_key:
            continue
        if review_decision_id and resolution.review_decision_id != review_decision_id:
            continue
        if gate_decision_id and resolution.gate_decision_id != gate_decision_id:
            continue
        if evaluation_pack_key and resolution.evaluation_pack_key != evaluation_pack_key:
            continue
        resolutions.append(summarize_evaluation_disposition_resolution(resolution))

    resolutions.sort(key=lambda item: item.created_at, reverse=True)
    return resolutions[: max(limit, 0)]


def summarize_evaluation_disposition_resolution(
    resolution: PersistedEvaluationDispositionResolution,
) -> EvaluationDispositionResolutionSummary:
    """Project one persisted disposition resolution into a lightweight summary."""

    return EvaluationDispositionResolutionSummary(
        resolution_id=resolution.resolution_id,
        resolution_key=resolution.resolution_key,
        created_at=resolution.created_at,
        resolution_definition_version=resolution.resolution_definition_version,
        review_decision_id=resolution.review_decision_id,
        review_key=resolution.review_key,
        gate_decision_id=resolution.gate_decision_id,
        gate_key=resolution.gate_key,
        evaluation_pack_key=resolution.evaluation_pack_key,
        adopted_review_disposition=resolution.adopted_review_disposition,
        observed_gate_verdict=resolution.observed_gate_verdict,
        contains_live_revalidation=resolution.contains_live_revalidation,
    )
