import pytest

from src.evaluations.gate_schemas import (
    EvaluationGateRequiredCase,
    EvaluationGateRuleTable,
    PersistedEvaluationGateDecision,
)
from src.evaluations.gate_store import save_evaluation_gate_decision
from src.evaluations.governance_status import (
    GovernanceStatusDerivationError,
    load_current_evaluation_governance_status,
)
from src.evaluations.resolution_schemas import (
    EvaluationResolverIdentity,
    PersistedEvaluationDispositionResolution,
)
from src.evaluations.resolution_store import save_evaluation_disposition_resolution
from src.evaluations.review_schemas import (
    EvaluationReviewerIdentity,
    PersistedEvaluationReviewDecision,
)
from src.evaluations.review_store import save_evaluation_review_decision


def _gate(
    gate_id: str,
    *,
    verdict: str = "pass",
    gate_key: str = "bounded_platform_readiness_v1",
    gate_definition_version: str = "v1",
    evaluation_pack_key: str = "phase4_frozen_governance_v1",
    contains_live_revalidation: bool = True,
    input_report_ids_by_case_key: dict[str, str] | None = None,
    required_cases: list[EvaluationGateRequiredCase] | None = None,
) -> PersistedEvaluationGateDecision:
    return PersistedEvaluationGateDecision(
        gate_decision_id=gate_id,
        created_at="2026-03-29T02:00:00+00:00",
        gate_key=gate_key,
        gate_definition_version=gate_definition_version,
        evaluation_pack_key=evaluation_pack_key,
        input_report_ids_by_case_key=input_report_ids_by_case_key
        or {
            "aoi_exemplar_march27_execution_backed": "evaluation-report-aoi",
        },
        contains_live_revalidation=contains_live_revalidation,
        rule_table=EvaluationGateRuleTable(
            required_cases=required_cases
            or [
                EvaluationGateRequiredCase(
                    case_key="aoi_exemplar_march27_execution_backed",
                    required_dimensions=["selection_fit"],
                )
            ]
        ),
        overall_verdict=verdict,
    )


def _review(
    review_id: str,
    *,
    gate_decision_id: str = "gate-decision-pass",
    disposition: str = "accept",
    observed_gate_verdict: str = "pass",
    review_key: str = "bounded_platform_readiness_review_v1",
    review_definition_version: str = "v1",
    gate_key: str = "bounded_platform_readiness_v1",
    gate_definition_version: str = "v1",
    evaluation_pack_key: str = "phase4_frozen_governance_v1",
    contains_live_revalidation: bool = True,
) -> PersistedEvaluationReviewDecision:
    return PersistedEvaluationReviewDecision(
        review_decision_id=review_id,
        created_at="2026-03-29T03:00:00+00:00",
        review_key=review_key,
        review_definition_version=review_definition_version,
        gate_decision_id=gate_decision_id,
        gate_key=gate_key,
        gate_definition_version=gate_definition_version,
        evaluation_pack_key=evaluation_pack_key,
        reviewer_identity=EvaluationReviewerIdentity(
            reviewer_name="Codex",
            reviewer_role="operator",
        ),
        disposition=disposition,
        rationale=f"Recording {disposition} for the referenced gate.",
        observed_gate_verdict=observed_gate_verdict,
        contains_live_revalidation=contains_live_revalidation,
        observed_gate_blocking_reasons=[],
        waiver_reasons=["Known bounded exception"] if disposition == "waive" else [],
    )


def _resolution(
    resolution_id: str,
    *,
    review_decision_id: str = "review-decision-pass",
    gate_decision_id: str = "gate-decision-pass",
    disposition: str = "accept",
    observed_gate_verdict: str = "pass",
    resolution_key: str = "bounded_platform_readiness_resolution_v1",
    review_key: str = "bounded_platform_readiness_review_v1",
    review_definition_version: str = "v1",
    gate_key: str = "bounded_platform_readiness_v1",
    gate_definition_version: str = "v1",
    evaluation_pack_key: str = "phase4_frozen_governance_v1",
    contains_live_revalidation: bool = True,
    created_at: str = "2026-03-29T04:00:00+00:00",
) -> PersistedEvaluationDispositionResolution:
    return PersistedEvaluationDispositionResolution(
        resolution_id=resolution_id,
        resolution_key=resolution_key,
        created_at=created_at,
        resolution_definition_version="v1",
        review_decision_id=review_decision_id,
        review_key=review_key,
        review_definition_version=review_definition_version,
        gate_decision_id=gate_decision_id,
        gate_key=gate_key,
        gate_definition_version=gate_definition_version,
        evaluation_pack_key=evaluation_pack_key,
        resolver_identity=EvaluationResolverIdentity(
            resolver_name="Codex",
            resolver_role="operator",
        ),
        resolution_note="Adopting this review as the current governance stance.",
        adopted_review_disposition=disposition,
        observed_gate_verdict=observed_gate_verdict,
        contains_live_revalidation=contains_live_revalidation,
    )


def _patch_dirs(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path / "reviews")
    monkeypatch.setattr(
        "src.evaluations.resolution_store.EVALUATION_RESOLUTIONS_DIR",
        tmp_path / "resolutions",
    )


@pytest.mark.parametrize(
    ("disposition", "gate_verdict", "expected_status"),
    [
        ("accept", "pass", "approved"),
        ("reject", "fail", "blocked"),
        ("waive", "error", "exception_recorded"),
    ],
)
def test_load_current_governance_status_maps_resolution_disposition_semantically(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    disposition: str,
    gate_verdict: str,
    expected_status: str,
) -> None:
    _patch_dirs(monkeypatch, tmp_path)
    gate = save_evaluation_gate_decision(
        _gate("gate-decision-pass", verdict=gate_verdict)
    )
    review = save_evaluation_review_decision(
        _review(
            "review-decision-pass",
            gate_decision_id=gate.gate_decision_id,
            disposition=disposition,
            observed_gate_verdict=gate_verdict,
        )
    )
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-current",
            review_decision_id=review.review_decision_id,
            gate_decision_id=gate.gate_decision_id,
            disposition=disposition,
            observed_gate_verdict=gate_verdict,
        )
    )

    status = load_current_evaluation_governance_status(
        "bounded_platform_readiness_resolution_v1",
        gate.gate_decision_id,
    )

    assert status.effective_governance_status == expected_status
    assert status.scope_label == "retrospective_frozen_pack_resolution"
    assert status.resolution.review_decision_id == review.review_decision_id


def test_load_current_governance_status_404s_when_no_current_resolution_exists(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    _patch_dirs(monkeypatch, tmp_path)

    with pytest.raises(GovernanceStatusDerivationError) as excinfo:
        load_current_evaluation_governance_status(
            "bounded_platform_readiness_resolution_v1",
            "gate-decision-missing",
        )

    assert excinfo.value.status_code == 404


def test_load_current_governance_status_409s_when_review_is_missing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    _patch_dirs(monkeypatch, tmp_path)
    gate = save_evaluation_gate_decision(_gate("gate-decision-pass"))
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-current",
            review_decision_id="review-decision-missing",
            gate_decision_id=gate.gate_decision_id,
        )
    )

    with pytest.raises(GovernanceStatusDerivationError) as excinfo:
        load_current_evaluation_governance_status(
            "bounded_platform_readiness_resolution_v1",
            gate.gate_decision_id,
        )

    assert excinfo.value.status_code == 409
    assert "review 'review-decision-missing'" in excinfo.value.detail


def test_load_current_governance_status_409s_when_gate_is_missing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    _patch_dirs(monkeypatch, tmp_path)
    review = save_evaluation_review_decision(_review("review-decision-pass"))
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-current",
            review_decision_id=review.review_decision_id,
            gate_decision_id="gate-decision-missing",
        )
    )

    with pytest.raises(GovernanceStatusDerivationError) as excinfo:
        load_current_evaluation_governance_status(
            "bounded_platform_readiness_resolution_v1",
            "gate-decision-missing",
        )

    assert excinfo.value.status_code == 409
    assert "gate 'gate-decision-missing'" in excinfo.value.detail


def test_load_current_governance_status_409s_on_resolution_review_mismatch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    _patch_dirs(monkeypatch, tmp_path)
    gate = save_evaluation_gate_decision(_gate("gate-decision-pass"))
    review = save_evaluation_review_decision(
        _review("review-decision-pass", gate_decision_id=gate.gate_decision_id)
    )
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-current",
            review_decision_id=review.review_decision_id,
            gate_decision_id=gate.gate_decision_id,
            review_key="other-review",
        )
    )

    with pytest.raises(GovernanceStatusDerivationError) as excinfo:
        load_current_evaluation_governance_status(
            "bounded_platform_readiness_resolution_v1",
            gate.gate_decision_id,
        )

    assert excinfo.value.status_code == 409
    assert "review_key expected 'bounded_platform_readiness_review_v1' observed 'other-review'" in excinfo.value.detail


def test_load_current_governance_status_409s_for_unknown_resolution_definition(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    _patch_dirs(monkeypatch, tmp_path)
    gate = save_evaluation_gate_decision(_gate("gate-decision-pass"))
    review = save_evaluation_review_decision(
        _review("review-decision-pass", gate_decision_id=gate.gate_decision_id)
    )
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-current",
            resolution_key="unknown-resolution",
            review_decision_id=review.review_decision_id,
            gate_decision_id=gate.gate_decision_id,
        )
    )

    with pytest.raises(GovernanceStatusDerivationError) as excinfo:
        load_current_evaluation_governance_status(
            "unknown-resolution",
            gate.gate_decision_id,
        )

    assert excinfo.value.status_code == 409
    assert "Unknown evaluation disposition resolution definition" in excinfo.value.detail


def test_load_current_governance_status_409s_on_resolution_definition_version_drift(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    _patch_dirs(monkeypatch, tmp_path)
    gate = save_evaluation_gate_decision(_gate("gate-decision-pass"))
    review = save_evaluation_review_decision(
        _review("review-decision-pass", gate_decision_id=gate.gate_decision_id)
    )
    save_evaluation_disposition_resolution(
        PersistedEvaluationDispositionResolution(
            **_resolution(
                "resolution-current",
                review_decision_id=review.review_decision_id,
                gate_decision_id=gate.gate_decision_id,
            ).model_dump()
            | {"resolution_definition_version": "v999"}
        )
    )

    with pytest.raises(GovernanceStatusDerivationError) as excinfo:
        load_current_evaluation_governance_status(
            "bounded_platform_readiness_resolution_v1",
            gate.gate_decision_id,
        )

    assert excinfo.value.status_code == 409
    assert "resolution_definition_version expected 'v1' observed 'v999'" in excinfo.value.detail


def test_load_current_governance_status_409s_on_review_gate_mismatch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    _patch_dirs(monkeypatch, tmp_path)
    gate = save_evaluation_gate_decision(_gate("gate-decision-pass"))
    review = save_evaluation_review_decision(
        _review(
            "review-decision-pass",
            gate_decision_id=gate.gate_decision_id,
            observed_gate_verdict="fail",
        )
    )
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-current",
            review_decision_id=review.review_decision_id,
            gate_decision_id=gate.gate_decision_id,
            observed_gate_verdict="fail",
        )
    )

    with pytest.raises(GovernanceStatusDerivationError) as excinfo:
        load_current_evaluation_governance_status(
            "bounded_platform_readiness_resolution_v1",
            gate.gate_decision_id,
        )

    assert excinfo.value.status_code == 409
    assert "observed_gate_verdict expected 'fail' observed 'pass'" in excinfo.value.detail


def test_load_current_governance_status_supports_second_family_keys_unchanged(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    _patch_dirs(monkeypatch, tmp_path)
    gate = save_evaluation_gate_decision(
        _gate(
            "gate-decision-genealogy-pass",
            gate_key="bounded_genealogy_lifecycle_readiness_v1",
            evaluation_pack_key="phase4_genealogy_lifecycle_governance_v1",
            contains_live_revalidation=False,
            input_report_ids_by_case_key={
                "genealogy_lifecycle_march28_session_reopen": "evaluation-report-genealogy"
            },
            required_cases=[
                EvaluationGateRequiredCase(
                    case_key="genealogy_lifecycle_march28_session_reopen",
                    required_dimensions=["identity_integrity"],
                )
            ],
        )
    )
    review = save_evaluation_review_decision(
        _review(
            "review-decision-genealogy-pass",
            gate_decision_id=gate.gate_decision_id,
            review_key="bounded_genealogy_lifecycle_review_v1",
            gate_key="bounded_genealogy_lifecycle_readiness_v1",
            evaluation_pack_key="phase4_genealogy_lifecycle_governance_v1",
            contains_live_revalidation=False,
        )
    )
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-genealogy-current",
            review_decision_id=review.review_decision_id,
            gate_decision_id=gate.gate_decision_id,
            resolution_key="bounded_genealogy_lifecycle_resolution_v1",
            review_key="bounded_genealogy_lifecycle_review_v1",
            gate_key="bounded_genealogy_lifecycle_readiness_v1",
            evaluation_pack_key="phase4_genealogy_lifecycle_governance_v1",
            contains_live_revalidation=False,
        )
    )

    status = load_current_evaluation_governance_status(
        "bounded_genealogy_lifecycle_resolution_v1",
        gate.gate_decision_id,
    )

    assert status.effective_governance_status == "approved"
    assert status.resolution.resolution_key == "bounded_genealogy_lifecycle_resolution_v1"
    assert status.resolution.review_key == "bounded_genealogy_lifecycle_review_v1"
    assert status.resolution.gate_key == "bounded_genealogy_lifecycle_readiness_v1"
    assert status.resolution.evaluation_pack_key == "phase4_genealogy_lifecycle_governance_v1"


def test_load_current_governance_status_supports_aoi_standalone_family_keys_unchanged(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    _patch_dirs(monkeypatch, tmp_path)
    gate = save_evaluation_gate_decision(
        _gate(
            "gate-decision-aoi-pass",
            gate_key="bounded_aoi_exemplar_readiness_v1",
            evaluation_pack_key="phase4_aoi_exemplar_governance_v1",
            contains_live_revalidation=False,
            input_report_ids_by_case_key={
                "aoi_exemplar_march27_execution_backed": "evaluation-report-aoi"
            },
            required_cases=[
                EvaluationGateRequiredCase(
                    case_key="aoi_exemplar_march27_execution_backed",
                    required_dimensions=["selection_fit"],
                )
            ],
        )
    )
    review = save_evaluation_review_decision(
        _review(
            "review-decision-aoi-pass",
            gate_decision_id=gate.gate_decision_id,
            review_key="bounded_aoi_exemplar_review_v1",
            gate_key="bounded_aoi_exemplar_readiness_v1",
            evaluation_pack_key="phase4_aoi_exemplar_governance_v1",
            contains_live_revalidation=False,
        )
    )
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-aoi-current",
            review_decision_id=review.review_decision_id,
            gate_decision_id=gate.gate_decision_id,
            resolution_key="bounded_aoi_exemplar_resolution_v1",
            review_key="bounded_aoi_exemplar_review_v1",
            gate_key="bounded_aoi_exemplar_readiness_v1",
            evaluation_pack_key="phase4_aoi_exemplar_governance_v1",
            contains_live_revalidation=False,
        )
    )

    status = load_current_evaluation_governance_status(
        "bounded_aoi_exemplar_resolution_v1",
        gate.gate_decision_id,
    )

    assert status.effective_governance_status == "approved"
    assert status.resolution.resolution_key == "bounded_aoi_exemplar_resolution_v1"
    assert status.resolution.review_key == "bounded_aoi_exemplar_review_v1"
    assert status.resolution.gate_key == "bounded_aoi_exemplar_readiness_v1"
    assert status.resolution.evaluation_pack_key == "phase4_aoi_exemplar_governance_v1"


def test_load_current_governance_status_supports_routing_planning_family_keys_unchanged(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    _patch_dirs(monkeypatch, tmp_path)
    gate = save_evaluation_gate_decision(
        _gate(
            "gate-decision-routing-pass",
            gate_key="bounded_routing_planning_readiness_v1",
            evaluation_pack_key="phase4_routing_planning_governance_v1",
            contains_live_revalidation=False,
            input_report_ids_by_case_key={
                "aoi_saved_result_handoff_current_contract": "evaluation-report-routing-aoi",
                "genealogy_saved_result_direct_sections_snapshot_march28": "evaluation-report-routing-genealogy",
            },
            required_cases=[
                EvaluationGateRequiredCase(
                    case_key="aoi_saved_result_handoff_current_contract",
                    required_dimensions=["route_fidelity"],
                ),
                EvaluationGateRequiredCase(
                    case_key="genealogy_saved_result_direct_sections_snapshot_march28",
                    required_dimensions=["route_fidelity"],
                ),
            ],
        )
    )
    review = save_evaluation_review_decision(
        _review(
            "review-decision-routing-pass",
            gate_decision_id=gate.gate_decision_id,
            review_key="bounded_routing_planning_review_v1",
            gate_key="bounded_routing_planning_readiness_v1",
            evaluation_pack_key="phase4_routing_planning_governance_v1",
            contains_live_revalidation=False,
        )
    )
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-routing-current",
            review_decision_id=review.review_decision_id,
            gate_decision_id=gate.gate_decision_id,
            resolution_key="bounded_routing_planning_resolution_v1",
            review_key="bounded_routing_planning_review_v1",
            gate_key="bounded_routing_planning_readiness_v1",
            evaluation_pack_key="phase4_routing_planning_governance_v1",
            contains_live_revalidation=False,
        )
    )

    status = load_current_evaluation_governance_status(
        "bounded_routing_planning_resolution_v1",
        gate.gate_decision_id,
    )

    assert status.effective_governance_status == "approved"
    assert status.resolution.resolution_key == "bounded_routing_planning_resolution_v1"
    assert status.resolution.review_key == "bounded_routing_planning_review_v1"
    assert status.resolution.gate_key == "bounded_routing_planning_readiness_v1"
    assert status.resolution.evaluation_pack_key == "phase4_routing_planning_governance_v1"


def test_load_current_governance_status_supports_planner_to_presentation_family_keys_unchanged(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    _patch_dirs(monkeypatch, tmp_path)
    gate = save_evaluation_gate_decision(
        _gate(
            "gate-decision-planner-presentation-pass",
            gate_key="bounded_planner_to_presentation_readiness_v1",
            evaluation_pack_key="phase4_planner_to_presentation_governance_v1",
            contains_live_revalidation=False,
            input_report_ids_by_case_key={
                "aoi_compose_selection_current_contract": "evaluation-report-planner-aoi",
                "genealogy_direct_sections_compose_snapshot_march28": "evaluation-report-planner-genealogy",
            },
            required_cases=[
                EvaluationGateRequiredCase(
                    case_key="aoi_compose_selection_current_contract",
                    required_dimensions=["handoff_contract_fidelity"],
                ),
                EvaluationGateRequiredCase(
                    case_key="genealogy_direct_sections_compose_snapshot_march28",
                    required_dimensions=["handoff_contract_fidelity"],
                ),
            ],
        )
    )
    review = save_evaluation_review_decision(
        _review(
            "review-decision-planner-presentation-pass",
            gate_decision_id=gate.gate_decision_id,
            review_key="bounded_planner_to_presentation_review_v1",
            gate_key="bounded_planner_to_presentation_readiness_v1",
            evaluation_pack_key="phase4_planner_to_presentation_governance_v1",
            contains_live_revalidation=False,
        )
    )
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-planner-presentation-current",
            review_decision_id=review.review_decision_id,
            gate_decision_id=gate.gate_decision_id,
            resolution_key="bounded_planner_to_presentation_resolution_v1",
            review_key="bounded_planner_to_presentation_review_v1",
            gate_key="bounded_planner_to_presentation_readiness_v1",
            evaluation_pack_key="phase4_planner_to_presentation_governance_v1",
            contains_live_revalidation=False,
        )
    )

    status = load_current_evaluation_governance_status(
        "bounded_planner_to_presentation_resolution_v1",
        gate.gate_decision_id,
    )

    assert status.effective_governance_status == "approved"
    assert status.resolution.resolution_key == "bounded_planner_to_presentation_resolution_v1"
    assert status.resolution.review_key == "bounded_planner_to_presentation_review_v1"
    assert status.resolution.gate_key == "bounded_planner_to_presentation_readiness_v1"
    assert status.resolution.evaluation_pack_key == "phase4_planner_to_presentation_governance_v1"


def test_load_current_governance_status_supports_cross_campaign_planner_to_presentation_family_keys_unchanged(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    _patch_dirs(monkeypatch, tmp_path)
    gate = save_evaluation_gate_decision(
        _gate(
            "gate-decision-planner-presentation-cross-campaign-pass",
            gate_key="bounded_planner_to_presentation_cross_campaign_readiness_v1",
            evaluation_pack_key="phase4_planner_to_presentation_cross_campaign_governance_v1",
            contains_live_revalidation=False,
            input_report_ids_by_case_key={
                "aoi_compose_selection_current_contract_fresh_campaign": "evaluation-report-planner-aoi-fresh",
                "genealogy_direct_sections_compose_current_contract_fresh_campaign": "evaluation-report-planner-genealogy-fresh",
            },
            required_cases=[
                EvaluationGateRequiredCase(
                    case_key="aoi_compose_selection_current_contract_fresh_campaign",
                    required_dimensions=["handoff_contract_fidelity"],
                ),
                EvaluationGateRequiredCase(
                    case_key="genealogy_direct_sections_compose_current_contract_fresh_campaign",
                    required_dimensions=["handoff_contract_fidelity"],
                ),
            ],
        )
    )
    review = save_evaluation_review_decision(
        _review(
            "review-decision-planner-presentation-cross-campaign-pass",
            gate_decision_id=gate.gate_decision_id,
            review_key="bounded_planner_to_presentation_cross_campaign_review_v1",
            gate_key="bounded_planner_to_presentation_cross_campaign_readiness_v1",
            evaluation_pack_key="phase4_planner_to_presentation_cross_campaign_governance_v1",
            contains_live_revalidation=False,
        )
    )
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-planner-presentation-cross-campaign-current",
            review_decision_id=review.review_decision_id,
            gate_decision_id=gate.gate_decision_id,
            resolution_key="bounded_planner_to_presentation_cross_campaign_resolution_v1",
            review_key="bounded_planner_to_presentation_cross_campaign_review_v1",
            gate_key="bounded_planner_to_presentation_cross_campaign_readiness_v1",
            evaluation_pack_key="phase4_planner_to_presentation_cross_campaign_governance_v1",
            contains_live_revalidation=False,
        )
    )

    status = load_current_evaluation_governance_status(
        "bounded_planner_to_presentation_cross_campaign_resolution_v1",
        gate.gate_decision_id,
    )

    assert status.effective_governance_status == "approved"
    assert (
        status.resolution.resolution_key
        == "bounded_planner_to_presentation_cross_campaign_resolution_v1"
    )
    assert status.resolution.review_key == "bounded_planner_to_presentation_cross_campaign_review_v1"
    assert status.resolution.gate_key == "bounded_planner_to_presentation_cross_campaign_readiness_v1"
    assert (
        status.resolution.evaluation_pack_key
        == "phase4_planner_to_presentation_cross_campaign_governance_v1"
    )
