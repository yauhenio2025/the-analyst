"""File-backed persistence for evaluation review/disposition decisions."""

from __future__ import annotations

from pathlib import Path
from typing import Optional
from uuid import uuid4

from src.evaluations.review_schemas import (
    EvaluationReviewDecisionSummary,
    PersistedEvaluationReviewDecision,
)


EVALUATION_REVIEWS_DIR = Path(__file__).parent / "reviews"


def build_evaluation_review_decision_id() -> str:
    """Create one analyzer-owned evaluation review-decision id."""

    return f"review-decision-{uuid4().hex[:12]}"


def save_evaluation_review_decision(
    review_decision: PersistedEvaluationReviewDecision,
) -> PersistedEvaluationReviewDecision:
    """Persist one evaluation review decision."""

    EVALUATION_REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    review_path = EVALUATION_REVIEWS_DIR / f"{review_decision.review_decision_id}.json"
    review_path.write_text(review_decision.model_dump_json(indent=2), encoding="utf-8")
    return review_decision


def load_evaluation_review_decision(
    review_decision_id: str,
) -> Optional[PersistedEvaluationReviewDecision]:
    """Load one evaluation review decision by id."""

    normalized_id = review_decision_id.strip()
    if not normalized_id:
        return None
    review_path = EVALUATION_REVIEWS_DIR / f"{normalized_id}.json"
    if not review_path.exists():
        return None
    return PersistedEvaluationReviewDecision.model_validate_json(
        review_path.read_text(encoding="utf-8")
    )


def list_evaluation_review_decisions(
    *,
    gate_decision_id: Optional[str] = None,
    gate_key: Optional[str] = None,
    evaluation_pack_key: Optional[str] = None,
    limit: int = 20,
) -> list[EvaluationReviewDecisionSummary]:
    """List persisted review-decision summaries newest-first."""

    reviews: list[EvaluationReviewDecisionSummary] = []
    if not EVALUATION_REVIEWS_DIR.exists():
        return reviews

    for review_path in sorted(EVALUATION_REVIEWS_DIR.glob("review-decision-*.json")):
        review_decision = PersistedEvaluationReviewDecision.model_validate_json(
            review_path.read_text(encoding="utf-8")
        )
        if gate_decision_id and review_decision.gate_decision_id != gate_decision_id:
            continue
        if gate_key and review_decision.gate_key != gate_key:
            continue
        if evaluation_pack_key and review_decision.evaluation_pack_key != evaluation_pack_key:
            continue
        reviews.append(summarize_evaluation_review_decision(review_decision))

    reviews.sort(key=lambda item: item.created_at, reverse=True)
    return reviews[: max(limit, 0)]


def summarize_evaluation_review_decision(
    review_decision: PersistedEvaluationReviewDecision,
) -> EvaluationReviewDecisionSummary:
    """Project one persisted review decision into a lightweight summary."""

    return EvaluationReviewDecisionSummary(
        review_decision_id=review_decision.review_decision_id,
        created_at=review_decision.created_at,
        review_key=review_decision.review_key,
        review_definition_version=review_decision.review_definition_version,
        gate_decision_id=review_decision.gate_decision_id,
        gate_key=review_decision.gate_key,
        evaluation_pack_key=review_decision.evaluation_pack_key,
        disposition=review_decision.disposition,
        observed_gate_verdict=review_decision.observed_gate_verdict,
        contains_live_revalidation=review_decision.contains_live_revalidation,
    )
