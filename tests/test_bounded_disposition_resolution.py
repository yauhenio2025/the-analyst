import pytest

from src.evaluations.resolution_builder import build_evaluation_disposition_resolution
from src.evaluations.resolution_store import list_evaluation_disposition_resolutions
from src.evaluations.review_schemas import (
    EvaluationReviewerIdentity,
    PersistedEvaluationReviewDecision,
)
from src.evaluations.review_store import save_evaluation_review_decision


def _review(
    review_id: str,
    *,
    disposition: str = "accept",
    observed_gate_verdict: str = "pass",
    review_key: str = "bounded_platform_readiness_review_v1",
    review_definition_version: str = "v1",
    gate_key: str = "bounded_platform_readiness_v1",
    gate_definition_version: str = "v1",
    evaluation_pack_key: str = "phase4_frozen_governance_v1",
) -> PersistedEvaluationReviewDecision:
    return PersistedEvaluationReviewDecision(
        review_decision_id=review_id,
        created_at="2026-03-29T02:00:00+00:00",
        review_key=review_key,
        review_definition_version=review_definition_version,
        gate_decision_id="gate-decision-745c2cb7e090",
        gate_key=gate_key,
        gate_definition_version=gate_definition_version,
        evaluation_pack_key=evaluation_pack_key,
        reviewer_identity=EvaluationReviewerIdentity(
            reviewer_name="Codex",
            reviewer_role="operator",
        ),
        disposition=disposition,
        rationale=f"Recording a {disposition} disposition over the referenced gate.",
        observed_gate_verdict=observed_gate_verdict,
        contains_live_revalidation=True,
        observed_gate_blocking_reasons=[],
        waiver_reasons=["Known bounded exception"] if disposition == "waive" else [],
    )


@pytest.mark.parametrize(
    ("disposition", "observed_gate_verdict"),
    [("accept", "pass"), ("reject", "fail"), ("waive", "error")],
)
def test_build_resolution_succeeds_for_any_review_disposition(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    disposition: str,
    observed_gate_verdict: str,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path / "reviews")

    review = save_evaluation_review_decision(
        _review(
            f"review-decision-{disposition}",
            disposition=disposition,
            observed_gate_verdict=observed_gate_verdict,
        )
    )

    resolution = build_evaluation_disposition_resolution(
        resolution_key="bounded_platform_readiness_resolution_v1",
        review_decision_id=review.review_decision_id,
        resolver_name="Codex",
        resolver_role="operator",
        resolution_note="Adopting this exact review as the current stance.",
        save_resolution=False,
    )

    assert resolution.review_decision_id == review.review_decision_id
    assert resolution.review_key == review.review_key
    assert resolution.gate_decision_id == review.gate_decision_id
    assert resolution.gate_key == review.gate_key
    assert resolution.adopted_review_disposition == review.disposition
    assert resolution.observed_gate_verdict == review.observed_gate_verdict
    assert resolution.contains_live_revalidation is True


def test_build_resolution_fails_for_missing_review(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path / "reviews")

    with pytest.raises(ValueError) as excinfo:
        build_evaluation_disposition_resolution(
            resolution_key="bounded_platform_readiness_resolution_v1",
            review_decision_id="review-decision-missing",
            resolver_name="Codex",
            resolver_role="operator",
            resolution_note="Cannot resolve a missing review.",
            save_resolution=False,
        )

    assert "was not found" in str(excinfo.value)


@pytest.mark.parametrize(
    ("review_key", "review_definition_version", "gate_key", "gate_definition_version", "evaluation_pack_key", "expected_message"),
    [
        ("other-review", "v1", "bounded_platform_readiness_v1", "v1", "phase4_frozen_governance_v1", "review_key mismatch"),
        ("bounded_platform_readiness_review_v1", "v2", "bounded_platform_readiness_v1", "v1", "phase4_frozen_governance_v1", "review_definition_version mismatch"),
        ("bounded_platform_readiness_review_v1", "v1", "other-gate", "v1", "phase4_frozen_governance_v1", "gate_key mismatch"),
        ("bounded_platform_readiness_review_v1", "v1", "bounded_platform_readiness_v1", "v2", "phase4_frozen_governance_v1", "gate_definition_version mismatch"),
        ("bounded_platform_readiness_review_v1", "v1", "bounded_platform_readiness_v1", "v1", "other-pack", "evaluation_pack_key mismatch"),
    ],
)
def test_build_resolution_fails_on_review_definition_mismatch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    review_key: str,
    review_definition_version: str,
    gate_key: str,
    gate_definition_version: str,
    evaluation_pack_key: str,
    expected_message: str,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path / "reviews")
    review = save_evaluation_review_decision(
        _review(
            "review-decision-mismatch",
            review_key=review_key,
            review_definition_version=review_definition_version,
            gate_key=gate_key,
            gate_definition_version=gate_definition_version,
            evaluation_pack_key=evaluation_pack_key,
        )
    )

    with pytest.raises(ValueError) as excinfo:
        build_evaluation_disposition_resolution(
            resolution_key="bounded_platform_readiness_resolution_v1",
            review_decision_id=review.review_decision_id,
            resolver_name="Codex",
            resolver_role="operator",
            resolution_note="Attempting to adopt a mismatched review.",
            save_resolution=False,
        )

    assert expected_message in str(excinfo.value)


def test_build_resolution_requires_nonblank_resolver_fields_and_note(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path / "reviews")
    review = save_evaluation_review_decision(_review("review-decision-pass"))

    for resolver_name, resolver_role, resolution_note, expected_message in [
        ("", "operator", "note", "resolver_name must be non-blank"),
        ("Codex", "", "note", "resolver_role must be non-blank"),
        ("Codex", "operator", "", "resolution_note must be non-blank"),
    ]:
        with pytest.raises(ValueError) as excinfo:
            build_evaluation_disposition_resolution(
                resolution_key="bounded_platform_readiness_resolution_v1",
                review_decision_id=review.review_decision_id,
                resolver_name=resolver_name,
                resolver_role=resolver_role,
                resolution_note=resolution_note,
                save_resolution=False,
            )
        assert expected_message in str(excinfo.value)


def test_build_resolution_persists_without_requiring_gate_load(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path / "reviews")
    monkeypatch.setattr(
        "src.evaluations.resolution_store.EVALUATION_RESOLUTIONS_DIR",
        tmp_path / "resolutions",
    )
    review = save_evaluation_review_decision(
        _review(
            "review-decision-pass",
            disposition="accept",
            observed_gate_verdict="pass",
        )
    )

    resolution = build_evaluation_disposition_resolution(
        resolution_key="bounded_platform_readiness_resolution_v1",
        review_decision_id=review.review_decision_id,
        resolver_name="Codex",
        resolver_role="operator",
        resolution_note="Persist the adopted stance from the persisted review only.",
        save_resolution=True,
    )
    stored = list_evaluation_disposition_resolutions(limit=10)

    assert resolution.resolution_id == stored[0].resolution_id
    assert stored[0].review_key == "bounded_platform_readiness_review_v1"
    assert stored[0].gate_key == "bounded_platform_readiness_v1"


def test_build_resolution_accepts_second_family_review_without_gate_reload(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path / "reviews")

    review = save_evaluation_review_decision(
        _review(
            "review-decision-genealogy-pass",
            review_key="bounded_genealogy_lifecycle_review_v1",
            gate_key="bounded_genealogy_lifecycle_readiness_v1",
            evaluation_pack_key="phase4_genealogy_lifecycle_governance_v1",
        )
    )

    resolution = build_evaluation_disposition_resolution(
        resolution_key="bounded_genealogy_lifecycle_resolution_v1",
        review_decision_id=review.review_decision_id,
        resolver_name="Codex",
        resolver_role="operator",
        resolution_note="Adopting the second-family genealogy review as current.",
        save_resolution=False,
    )

    assert resolution.resolution_key == "bounded_genealogy_lifecycle_resolution_v1"
    assert resolution.review_key == "bounded_genealogy_lifecycle_review_v1"
    assert resolution.gate_key == "bounded_genealogy_lifecycle_readiness_v1"
    assert resolution.evaluation_pack_key == "phase4_genealogy_lifecycle_governance_v1"


def test_build_resolution_accepts_aoi_standalone_review_without_gate_reload(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path / "reviews")

    review = save_evaluation_review_decision(
        _review(
            "review-decision-aoi-pass",
            review_key="bounded_aoi_exemplar_review_v1",
            gate_key="bounded_aoi_exemplar_readiness_v1",
            evaluation_pack_key="phase4_aoi_exemplar_governance_v1",
        )
    )

    resolution = build_evaluation_disposition_resolution(
        resolution_key="bounded_aoi_exemplar_resolution_v1",
        review_decision_id=review.review_decision_id,
        resolver_name="Codex",
        resolver_role="operator",
        resolution_note="Adopting the AOI-only standalone review as current.",
        save_resolution=False,
    )

    assert resolution.resolution_key == "bounded_aoi_exemplar_resolution_v1"
    assert resolution.review_key == "bounded_aoi_exemplar_review_v1"
    assert resolution.gate_key == "bounded_aoi_exemplar_readiness_v1"
    assert resolution.evaluation_pack_key == "phase4_aoi_exemplar_governance_v1"


def test_build_resolution_accepts_routing_planning_review_without_gate_reload(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path / "reviews")

    review = save_evaluation_review_decision(
        _review(
            "review-decision-routing-pass",
            review_key="bounded_routing_planning_review_v1",
            gate_key="bounded_routing_planning_readiness_v1",
            evaluation_pack_key="phase4_routing_planning_governance_v1",
        )
    )

    resolution = build_evaluation_disposition_resolution(
        resolution_key="bounded_routing_planning_resolution_v1",
        review_decision_id=review.review_decision_id,
        resolver_name="Codex",
        resolver_role="operator",
        resolution_note="Adopting the routing/planning governance review as current.",
        save_resolution=False,
    )

    assert resolution.resolution_key == "bounded_routing_planning_resolution_v1"
    assert resolution.review_key == "bounded_routing_planning_review_v1"
    assert resolution.gate_key == "bounded_routing_planning_readiness_v1"
    assert resolution.evaluation_pack_key == "phase4_routing_planning_governance_v1"


def test_build_resolution_accepts_planner_to_presentation_review_without_gate_reload(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path / "reviews")

    review = save_evaluation_review_decision(
        _review(
            "review-decision-planner-presentation-pass",
            review_key="bounded_planner_to_presentation_review_v1",
            gate_key="bounded_planner_to_presentation_readiness_v1",
            evaluation_pack_key="phase4_planner_to_presentation_governance_v1",
        )
    )

    resolution = build_evaluation_disposition_resolution(
        resolution_key="bounded_planner_to_presentation_resolution_v1",
        review_decision_id=review.review_decision_id,
        resolver_name="Codex",
        resolver_role="operator",
        resolution_note="Adopting the planner-to-presentation governance review as current.",
        save_resolution=False,
    )

    assert resolution.resolution_key == "bounded_planner_to_presentation_resolution_v1"
    assert resolution.review_key == "bounded_planner_to_presentation_review_v1"
    assert resolution.gate_key == "bounded_planner_to_presentation_readiness_v1"
    assert resolution.evaluation_pack_key == "phase4_planner_to_presentation_governance_v1"


def test_build_resolution_accepts_cross_campaign_planner_to_presentation_review_without_gate_reload(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path / "reviews")

    review = save_evaluation_review_decision(
        _review(
            "review-decision-planner-presentation-cross-campaign-pass",
            review_key="bounded_planner_to_presentation_cross_campaign_review_v1",
            gate_key="bounded_planner_to_presentation_cross_campaign_readiness_v1",
            evaluation_pack_key="phase4_planner_to_presentation_cross_campaign_governance_v1",
        )
    )

    resolution = build_evaluation_disposition_resolution(
        resolution_key="bounded_planner_to_presentation_cross_campaign_resolution_v1",
        review_decision_id=review.review_decision_id,
        resolver_name="Codex",
        resolver_role="operator",
        resolution_note="Adopting the cross-campaign planner-to-presentation governance review as current.",
        save_resolution=False,
    )

    assert resolution.resolution_key == "bounded_planner_to_presentation_cross_campaign_resolution_v1"
    assert resolution.review_key == "bounded_planner_to_presentation_cross_campaign_review_v1"
    assert resolution.gate_key == "bounded_planner_to_presentation_cross_campaign_readiness_v1"
    assert resolution.evaluation_pack_key == "phase4_planner_to_presentation_cross_campaign_governance_v1"
