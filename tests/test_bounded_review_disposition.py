import pytest

from src.evaluations.gate_schemas import (
    EvaluationGateRequiredCase,
    EvaluationGateRuleTable,
    PersistedEvaluationGateDecision,
)
from src.evaluations.gate_store import save_evaluation_gate_decision
from src.evaluations.review_builder import build_evaluation_review_decision
from src.evaluations.review_store import list_evaluation_review_decisions


def _gate(
    gate_id: str,
    *,
    verdict: str = "pass",
    gate_key: str = "bounded_platform_readiness_v1",
    gate_definition_version: str = "v1",
    evaluation_pack_key: str = "phase4_frozen_governance_v1",
    input_report_ids_by_case_key: dict[str, str] | None = None,
    required_cases: list[EvaluationGateRequiredCase] | None = None,
) -> PersistedEvaluationGateDecision:
    blocking_reasons = [] if verdict == "pass" else [f"gate verdict is {verdict}"]
    return PersistedEvaluationGateDecision(
        gate_decision_id=gate_id,
        created_at="2026-03-29T02:00:00+00:00",
        gate_key=gate_key,
        gate_definition_version=gate_definition_version,
        evaluation_pack_key=evaluation_pack_key,
        input_report_ids_by_case_key=input_report_ids_by_case_key
        or {
            "aoi_exemplar_march27_execution_backed": "evaluation-report-aoi",
            "genealogy_lifecycle_march28_session_reopen": "evaluation-report-genealogy",
        },
        contains_live_revalidation=True,
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
        blocking_reasons=blocking_reasons,
    )


def test_build_review_decision_accepts_passing_gate_and_derives_gate_fields(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path / "reviews")

    gate = save_evaluation_gate_decision(_gate("gate-decision-pass", verdict="pass"))

    review = build_evaluation_review_decision(
        review_key="bounded_platform_readiness_review_v1",
        gate_decision_id=gate.gate_decision_id,
        reviewer_name="Codex",
        reviewer_role="operator",
        disposition="accept",
        rationale="Accepting the passing retrospective frozen-pack gate.",
        save_decision=False,
    )

    assert review.gate_decision_id == gate.gate_decision_id
    assert review.gate_key == gate.gate_key
    assert review.gate_definition_version == gate.gate_definition_version
    assert review.evaluation_pack_key == gate.evaluation_pack_key
    assert review.observed_gate_verdict == "pass"
    assert review.contains_live_revalidation is True
    assert review.observed_gate_blocking_reasons == []


def test_build_review_decision_reject_succeeds_for_any_gate_verdict(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    for verdict in ("pass", "fail", "error"):
        gate = save_evaluation_gate_decision(_gate(f"gate-decision-{verdict}", verdict=verdict))
        review = build_evaluation_review_decision(
            review_key="bounded_platform_readiness_review_v1",
            gate_decision_id=gate.gate_decision_id,
            reviewer_name="Codex",
            reviewer_role="operator",
            disposition="reject",
            rationale=f"Rejecting gate with observed verdict {verdict}.",
            save_decision=False,
        )
        assert review.disposition == "reject"
        assert review.observed_gate_verdict == verdict


def test_build_review_decision_accepts_second_family_gate_without_builder_changes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    gate = save_evaluation_gate_decision(
        _gate(
            "gate-decision-genealogy-pass",
            gate_key="bounded_genealogy_lifecycle_readiness_v1",
            evaluation_pack_key="phase4_genealogy_lifecycle_governance_v1",
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

    review = build_evaluation_review_decision(
        review_key="bounded_genealogy_lifecycle_review_v1",
        gate_decision_id=gate.gate_decision_id,
        reviewer_name="Codex",
        reviewer_role="operator",
        disposition="accept",
        rationale="Accepting the passing second-family genealogy gate.",
        save_decision=False,
    )

    assert review.review_key == "bounded_genealogy_lifecycle_review_v1"
    assert review.gate_key == "bounded_genealogy_lifecycle_readiness_v1"
    assert review.evaluation_pack_key == "phase4_genealogy_lifecycle_governance_v1"


def test_build_review_decision_accepts_aoi_standalone_gate_without_builder_changes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    gate = save_evaluation_gate_decision(
        _gate(
            "gate-decision-aoi-pass",
            gate_key="bounded_aoi_exemplar_readiness_v1",
            evaluation_pack_key="phase4_aoi_exemplar_governance_v1",
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

    review = build_evaluation_review_decision(
        review_key="bounded_aoi_exemplar_review_v1",
        gate_decision_id=gate.gate_decision_id,
        reviewer_name="Codex",
        reviewer_role="operator",
        disposition="accept",
        rationale="Accepting the passing AOI-only standalone gate.",
        save_decision=False,
    )

    assert review.review_key == "bounded_aoi_exemplar_review_v1"
    assert review.gate_key == "bounded_aoi_exemplar_readiness_v1"
    assert review.evaluation_pack_key == "phase4_aoi_exemplar_governance_v1"


def test_build_review_decision_accepts_routing_planning_gate_without_builder_changes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    gate = save_evaluation_gate_decision(
        _gate(
            "gate-decision-routing-pass",
            gate_key="bounded_routing_planning_readiness_v1",
            evaluation_pack_key="phase4_routing_planning_governance_v1",
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

    review = build_evaluation_review_decision(
        review_key="bounded_routing_planning_review_v1",
        gate_decision_id=gate.gate_decision_id,
        reviewer_name="Codex",
        reviewer_role="operator",
        disposition="accept",
        rationale="Accepting the passing routing/planning governance gate.",
        save_decision=False,
    )

    assert review.review_key == "bounded_routing_planning_review_v1"
    assert review.gate_key == "bounded_routing_planning_readiness_v1"
    assert review.evaluation_pack_key == "phase4_routing_planning_governance_v1"


def test_build_review_decision_accepts_planner_to_presentation_gate_without_builder_changes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    gate = save_evaluation_gate_decision(
        _gate(
            "gate-decision-planner-presentation-pass",
            gate_key="bounded_planner_to_presentation_readiness_v1",
            evaluation_pack_key="phase4_planner_to_presentation_governance_v1",
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

    review = build_evaluation_review_decision(
        review_key="bounded_planner_to_presentation_review_v1",
        gate_decision_id=gate.gate_decision_id,
        reviewer_name="Codex",
        reviewer_role="operator",
        disposition="accept",
        rationale="Accepting the passing planner-to-presentation governance gate.",
        save_decision=False,
    )

    assert review.review_key == "bounded_planner_to_presentation_review_v1"
    assert review.gate_key == "bounded_planner_to_presentation_readiness_v1"
    assert review.evaluation_pack_key == "phase4_planner_to_presentation_governance_v1"


def test_build_review_decision_accepts_cross_campaign_planner_to_presentation_gate_without_builder_changes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    gate = save_evaluation_gate_decision(
        _gate(
            "gate-decision-planner-presentation-cross-campaign-pass",
            gate_key="bounded_planner_to_presentation_cross_campaign_readiness_v1",
            evaluation_pack_key="phase4_planner_to_presentation_cross_campaign_governance_v1",
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

    review = build_evaluation_review_decision(
        review_key="bounded_planner_to_presentation_cross_campaign_review_v1",
        gate_decision_id=gate.gate_decision_id,
        reviewer_name="Codex",
        reviewer_role="operator",
        disposition="accept",
        rationale="Accepting the passing cross-campaign planner-to-presentation governance gate.",
        save_decision=False,
    )

    assert review.review_key == "bounded_planner_to_presentation_cross_campaign_review_v1"
    assert review.gate_key == "bounded_planner_to_presentation_cross_campaign_readiness_v1"
    assert review.evaluation_pack_key == "phase4_planner_to_presentation_cross_campaign_governance_v1"


def test_build_review_decision_waive_requires_nonblank_rationale_and_waiver_reason(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")
    gate = save_evaluation_gate_decision(_gate("gate-decision-fail", verdict="fail"))

    review = build_evaluation_review_decision(
        review_key="bounded_platform_readiness_review_v1",
        gate_decision_id=gate.gate_decision_id,
        reviewer_name="Codex",
        reviewer_role="operator",
        disposition="waive",
        rationale="Recording a bounded exception over the failing gate.",
        waiver_reasons=["Known retrospective limitation"],
        save_decision=False,
    )

    assert review.disposition == "waive"
    assert review.waiver_reasons == ["Known retrospective limitation"]


@pytest.mark.parametrize(
    ("verdict", "disposition", "rationale", "waiver_reasons", "expected_message"),
    [
        ("fail", "accept", "Trying to accept a non-passing gate.", [], "valid only for gate verdict 'pass'"),
        ("error", "accept", "Trying to accept an error gate.", [], "valid only for gate verdict 'pass'"),
        ("pass", "waive", "Trying to waive a passing gate.", ["No need"], "valid only for gate verdicts 'fail' or 'error'"),
        ("fail", "waive", "", ["Reason"], "rationale must be non-blank"),
        ("fail", "waive", "Valid rationale.", [], "requires at least one non-blank waiver reason"),
        ("fail", "reject", "Valid rationale.", ["Unexpected"], "Waiver reasons are allowed only"),
        ("pass", "accept", "Valid rationale.", [], None),
    ],
)
def test_build_review_decision_enforces_disposition_law_and_input_validation(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    verdict: str,
    disposition: str,
    rationale: str,
    waiver_reasons: list[str],
    expected_message: str | None,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")
    gate = save_evaluation_gate_decision(_gate(f"gate-decision-{verdict}", verdict=verdict))

    if expected_message is None:
        review = build_evaluation_review_decision(
            review_key="bounded_platform_readiness_review_v1",
            gate_decision_id=gate.gate_decision_id,
            reviewer_name="Codex",
            reviewer_role="operator",
            disposition=disposition,
            rationale=rationale,
            waiver_reasons=waiver_reasons,
            save_decision=False,
        )
        assert review.disposition == disposition
        return

    with pytest.raises(ValueError) as excinfo:
        build_evaluation_review_decision(
            review_key="bounded_platform_readiness_review_v1",
            gate_decision_id=gate.gate_decision_id,
            reviewer_name="Codex",
            reviewer_role="operator",
            disposition=disposition,
            rationale=rationale,
            waiver_reasons=waiver_reasons,
            save_decision=False,
        )

    assert expected_message in str(excinfo.value)


def test_build_review_decision_fails_for_missing_gate(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    with pytest.raises(ValueError) as excinfo:
        build_evaluation_review_decision(
            review_key="bounded_platform_readiness_review_v1",
            gate_decision_id="gate-decision-missing",
            reviewer_name="Codex",
            reviewer_role="operator",
            disposition="accept",
            rationale="Cannot accept a missing gate.",
            save_decision=False,
        )

    assert "was not found" in str(excinfo.value)


@pytest.mark.parametrize(
    ("gate_key", "gate_definition_version", "evaluation_pack_key", "expected_message"),
    [
        ("other-gate", "v1", "phase4_frozen_governance_v1", "gate_key mismatch"),
        ("bounded_platform_readiness_v1", "v2", "phase4_frozen_governance_v1", "gate_definition_version mismatch"),
        ("bounded_platform_readiness_v1", "v1", "other-pack", "evaluation_pack_key mismatch"),
    ],
)
def test_build_review_decision_fails_on_gate_definition_mismatch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    gate_key: str,
    gate_definition_version: str,
    evaluation_pack_key: str,
    expected_message: str,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")
    gate = save_evaluation_gate_decision(
        _gate(
            "gate-decision-mismatch",
            verdict="pass",
            gate_key=gate_key,
            gate_definition_version=gate_definition_version,
            evaluation_pack_key=evaluation_pack_key,
        )
    )

    with pytest.raises(ValueError) as excinfo:
        build_evaluation_review_decision(
            review_key="bounded_platform_readiness_review_v1",
            gate_decision_id=gate.gate_decision_id,
            reviewer_name="Codex",
            reviewer_role="operator",
            disposition="accept",
            rationale="Attempting to accept a mismatched gate.",
            save_decision=False,
        )

    assert expected_message in str(excinfo.value)


def test_build_review_decision_persists_and_lists_review_decisions(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")
    monkeypatch.setattr("src.evaluations.review_store.EVALUATION_REVIEWS_DIR", tmp_path / "reviews")
    gate = save_evaluation_gate_decision(_gate("gate-decision-pass", verdict="pass"))

    review = build_evaluation_review_decision(
        review_key="bounded_platform_readiness_review_v1",
        gate_decision_id=gate.gate_decision_id,
        reviewer_name="Codex",
        reviewer_role="operator",
        disposition="accept",
        rationale="Accepting the passing gate as recorded.",
        save_decision=True,
    )

    stored = list_evaluation_review_decisions(limit=10)

    assert review.review_decision_id == stored[0].review_decision_id
    assert stored[0].review_definition_version == "v1"


@pytest.mark.parametrize(("reviewer_name", "reviewer_role", "expected_message"), [
    ("", "operator", "reviewer_name must be non-blank"),
    ("Codex", "", "reviewer_role must be non-blank"),
])
def test_build_review_decision_requires_nonblank_reviewer_identity_fields(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    reviewer_name: str,
    reviewer_role: str,
    expected_message: str,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")
    gate = save_evaluation_gate_decision(_gate("gate-decision-pass", verdict="pass"))

    with pytest.raises(ValueError) as excinfo:
        build_evaluation_review_decision(
            review_key="bounded_platform_readiness_review_v1",
            gate_decision_id=gate.gate_decision_id,
            reviewer_name=reviewer_name,
            reviewer_role=reviewer_role,
            disposition="accept",
            rationale="Accepting the passing gate as recorded.",
            save_decision=False,
        )

    assert expected_message in str(excinfo.value)
