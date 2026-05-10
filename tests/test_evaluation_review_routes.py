import asyncio

import pytest
from fastapi import HTTPException

from src.api.routes.evaluations import (
    get_evaluation_review_decision_endpoint,
    list_evaluation_review_decisions_endpoint,
)
from src.evaluations.review_schemas import (
    EvaluationReviewerIdentity,
    PersistedEvaluationReviewDecision,
)
from src.evaluations.review_store import save_evaluation_review_decision


def _review(review_id: str, *, created_at: str) -> PersistedEvaluationReviewDecision:
    return PersistedEvaluationReviewDecision(
        review_decision_id=review_id,
        created_at=created_at,
        review_key="bounded_platform_readiness_review_v1",
        review_definition_version="v1",
        gate_decision_id="gate-decision-745c2cb7e090",
        gate_key="bounded_platform_readiness_v1",
        gate_definition_version="v1",
        evaluation_pack_key="phase4_frozen_governance_v1",
        reviewer_identity=EvaluationReviewerIdentity(
            reviewer_name="Codex",
            reviewer_role="operator",
        ),
        disposition="accept",
        rationale="Accepting the referenced passing gate as recorded.",
        observed_gate_verdict="pass",
        contains_live_revalidation=True,
    )


def test_get_evaluation_review_decision_endpoint_returns_review(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path)
    review = save_evaluation_review_decision(
        _review("review-decision-route", created_at="2026-03-29T01:00:00+00:00")
    )

    fetched = asyncio.run(get_evaluation_review_decision_endpoint(review.review_decision_id))

    assert fetched.review_decision_id == review.review_decision_id
    assert fetched.review_key == "bounded_platform_readiness_review_v1"


def test_list_evaluation_review_decisions_endpoint_returns_filtered_summaries(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path)
    save_evaluation_review_decision(
        _review("review-decision-a", created_at="2026-03-29T00:00:00+00:00")
    )
    save_evaluation_review_decision(
        PersistedEvaluationReviewDecision(
            review_decision_id="review-decision-b",
            created_at="2026-03-29T01:00:00+00:00",
            review_key="other-review",
            review_definition_version="v2",
            gate_decision_id="other-gate-decision",
            gate_key="other-gate",
            gate_definition_version="v2",
            evaluation_pack_key="other-pack",
            reviewer_identity=EvaluationReviewerIdentity(
                reviewer_name="Other",
                reviewer_role="reviewer",
            ),
            disposition="reject",
            rationale="Rejecting a different gate.",
            observed_gate_verdict="fail",
            contains_live_revalidation=False,
        )
    )

    response = asyncio.run(
        list_evaluation_review_decisions_endpoint(
            gate_decision_id="gate-decision-745c2cb7e090",
            gate_key="bounded_platform_readiness_v1",
            evaluation_pack_key="phase4_frozen_governance_v1",
            limit=10,
        )
    )

    assert response.count == 1
    assert response.reviews[0].review_decision_id == "review-decision-a"
    assert response.reviews[0].review_definition_version == "v1"


def test_get_evaluation_review_decision_endpoint_returns_404_for_missing_review(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path)

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(get_evaluation_review_decision_endpoint("review-decision-missing"))

    assert excinfo.value.status_code == 404
