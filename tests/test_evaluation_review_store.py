import pytest

from src.evaluations.review_schemas import (
    EvaluationReviewerIdentity,
    PersistedEvaluationReviewDecision,
)
from src.evaluations.review_store import (
    list_evaluation_review_decisions,
    load_evaluation_review_decision,
    save_evaluation_review_decision,
)


def _review(
    review_id: str,
    *,
    created_at: str,
    gate_decision_id: str = "gate-decision-745c2cb7e090",
    gate_key: str = "bounded_platform_readiness_v1",
    evaluation_pack_key: str = "phase4_frozen_governance_v1",
) -> PersistedEvaluationReviewDecision:
    return PersistedEvaluationReviewDecision(
        review_decision_id=review_id,
        created_at=created_at,
        review_key="bounded_platform_readiness_review_v1",
        review_definition_version="v1",
        gate_decision_id=gate_decision_id,
        gate_key=gate_key,
        gate_definition_version="v1",
        evaluation_pack_key=evaluation_pack_key,
        reviewer_identity=EvaluationReviewerIdentity(
            reviewer_name="Codex",
            reviewer_role="operator",
        ),
        disposition="accept",
        rationale="Accepting the referenced passing gate as recorded.",
        observed_gate_verdict="pass",
        contains_live_revalidation=True,
    )


def test_evaluation_review_store_round_trips_and_lists_newest_first(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path)

    older = save_evaluation_review_decision(
        _review("review-decision-older", created_at="2026-03-29T00:00:00+00:00")
    )
    newer = save_evaluation_review_decision(
        _review("review-decision-newer", created_at="2026-03-29T01:00:00+00:00")
    )

    loaded = load_evaluation_review_decision(older.review_decision_id)
    summaries = list_evaluation_review_decisions(limit=10)

    assert loaded is not None
    assert loaded.review_decision_id == older.review_decision_id
    assert [summary.review_decision_id for summary in summaries] == [
        newer.review_decision_id,
        older.review_decision_id,
    ]


def test_evaluation_review_store_filters_by_gate_and_pack(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path)

    save_evaluation_review_decision(
        _review(
            "review-decision-a",
            created_at="2026-03-29T00:00:00+00:00",
            gate_decision_id="gate-decision-a",
        )
    )
    save_evaluation_review_decision(
        _review(
            "review-decision-b",
            created_at="2026-03-29T01:00:00+00:00",
            gate_decision_id="gate-decision-b",
            gate_key="other-gate",
            evaluation_pack_key="other-pack",
        )
    )

    filtered = list_evaluation_review_decisions(
        gate_decision_id="gate-decision-a",
        gate_key="bounded_platform_readiness_v1",
        evaluation_pack_key="phase4_frozen_governance_v1",
        limit=10,
    )

    assert len(filtered) == 1
    assert filtered[0].review_decision_id == "review-decision-a"
