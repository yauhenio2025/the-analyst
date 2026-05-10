import pytest

from src.evaluations.resolution_schemas import (
    EvaluationResolverIdentity,
    PersistedEvaluationDispositionResolution,
)
from src.evaluations.resolution_store import (
    list_evaluation_disposition_resolutions,
    load_current_evaluation_disposition_resolution,
    load_evaluation_disposition_resolution,
    save_evaluation_disposition_resolution,
)


def _resolution(
    resolution_id: str,
    *,
    created_at: str,
    resolution_key: str = "bounded_platform_readiness_resolution_v1",
    review_decision_id: str = "review-decision-21edf9b955ee",
    gate_decision_id: str = "gate-decision-745c2cb7e090",
    evaluation_pack_key: str = "phase4_frozen_governance_v1",
) -> PersistedEvaluationDispositionResolution:
    return PersistedEvaluationDispositionResolution(
        resolution_id=resolution_id,
        resolution_key=resolution_key,
        created_at=created_at,
        resolution_definition_version="v1",
        review_decision_id=review_decision_id,
        review_key="bounded_platform_readiness_review_v1",
        review_definition_version="v1",
        gate_decision_id=gate_decision_id,
        gate_key="bounded_platform_readiness_v1",
        gate_definition_version="v1",
        evaluation_pack_key=evaluation_pack_key,
        resolver_identity=EvaluationResolverIdentity(
            resolver_name="Codex",
            resolver_role="operator",
        ),
        resolution_note="Adopting this review as the current bounded governance stance.",
        adopted_review_disposition="accept",
        observed_gate_verdict="pass",
        contains_live_revalidation=True,
    )


def test_evaluation_resolution_store_round_trips_lists_and_loads_current(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.resolution_store.EVALUATION_RESOLUTIONS_DIR", tmp_path)

    older = save_evaluation_disposition_resolution(
        _resolution("resolution-older", created_at="2026-03-29T00:00:00+00:00")
    )
    newer = save_evaluation_disposition_resolution(
        _resolution("resolution-newer", created_at="2026-03-29T01:00:00+00:00")
    )

    loaded = load_evaluation_disposition_resolution(older.resolution_id)
    summaries = list_evaluation_disposition_resolutions(limit=10)
    current = load_current_evaluation_disposition_resolution(
        "bounded_platform_readiness_resolution_v1",
        "gate-decision-745c2cb7e090",
    )

    assert loaded is not None
    assert loaded.resolution_id == older.resolution_id
    assert [summary.resolution_id for summary in summaries] == [
        newer.resolution_id,
        older.resolution_id,
    ]
    assert current is not None
    assert current.resolution_id == newer.resolution_id


def test_evaluation_resolution_store_filters_by_resolution_review_gate_and_pack(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.resolution_store.EVALUATION_RESOLUTIONS_DIR", tmp_path)

    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-a",
            created_at="2026-03-29T00:00:00+00:00",
            resolution_key="bounded_platform_readiness_resolution_v1",
            review_decision_id="review-decision-a",
            gate_decision_id="gate-decision-a",
        )
    )
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-b",
            created_at="2026-03-29T01:00:00+00:00",
            resolution_key="other-resolution",
            review_decision_id="review-decision-b",
            gate_decision_id="gate-decision-b",
            evaluation_pack_key="other-pack",
        )
    )

    filtered = list_evaluation_disposition_resolutions(
        resolution_key="bounded_platform_readiness_resolution_v1",
        review_decision_id="review-decision-a",
        gate_decision_id="gate-decision-a",
        evaluation_pack_key="phase4_frozen_governance_v1",
        limit=10,
    )

    assert len(filtered) == 1
    assert filtered[0].resolution_id == "resolution-a"
    assert filtered[0].review_key == "bounded_platform_readiness_review_v1"
    assert filtered[0].gate_key == "bounded_platform_readiness_v1"


def test_current_resolution_returns_none_when_other_scopes_exist_only(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.resolution_store.EVALUATION_RESOLUTIONS_DIR", tmp_path)

    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-other-gate",
            created_at="2026-03-29T00:00:00+00:00",
            gate_decision_id="gate-decision-other",
        )
    )
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-other-key",
            created_at="2026-03-29T01:00:00+00:00",
            resolution_key="other-resolution",
        )
    )

    current = load_current_evaluation_disposition_resolution(
        "bounded_platform_readiness_resolution_v1",
        "gate-decision-745c2cb7e090",
    )

    assert current is None
