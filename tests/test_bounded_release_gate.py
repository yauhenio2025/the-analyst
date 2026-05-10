import pytest

from src.evaluations.gate_builder import (
    _parse_report_mapping,
    build_evaluation_gate_decision,
    generate_then_build_evaluation_gate_decision,
)
from src.evaluations.gate_store import list_evaluation_gate_decisions
from src.evaluations.report_store import save_evaluation_report
from src.evaluations.schemas import (
    EvaluationCheck,
    EvaluationDimensionSummary,
    PersistedEvaluationReport,
)


def _report(
    report_id: str,
    *,
    case_key: str,
    subject_kind: str,
    subject_identity: str,
    workflow_key: str,
    consumer_key: str,
    overall_verdict: str = "pass",
    dimension_statuses: dict[str, str],
    live_revalidation: bool = False,
) -> PersistedEvaluationReport:
    return PersistedEvaluationReport(
        evaluation_report_id=report_id,
        created_at="2026-03-29T02:00:00+00:00",
        evaluation_pack_key="phase4_frozen_governance_v1",
        case_key=case_key,
        subject_kind=subject_kind,
        subject_identity=subject_identity,
        workflow_key=workflow_key,
        consumer_key=consumer_key,
        checks=[
            EvaluationCheck(
                check_key="supporting-check",
                label="supporting check",
                status="pass",
                summary="supporting live check",
                evidence_mode="stored_object",
                evidence_observed_at="2026-03-29T02:00:00+00:00",
                live_revalidation_performed=live_revalidation,
            )
        ],
        dimension_summaries=[
            EvaluationDimensionSummary(
                dimension_key=dimension_key,
                status=dimension_status,
                summary=f"{dimension_key}={dimension_status}",
                supporting_checks=["supporting-check"],
            )
            for dimension_key, dimension_status in dimension_statuses.items()
        ],
        overall_verdict=overall_verdict,
    )


def _save_required_reports() -> dict[str, str]:
    aoi = save_evaluation_report(
        _report(
            "evaluation-report-aoi",
            case_key="aoi_exemplar_march27_execution_backed",
            subject_kind="executor_job",
            subject_identity="job-744edf255ad5",
            workflow_key="anxiety_of_influence_thematic_single_thinker",
            consumer_key="the-critic",
            dimension_statuses={
                "selection_fit": "pass",
                "rationale_clarity": "pass",
                "rendered_usefulness": "pass",
                "operational_behavior": "pass",
            },
            live_revalidation=True,
        )
    )
    genealogy = save_evaluation_report(
        _report(
            "evaluation-report-genealogy",
            case_key="genealogy_lifecycle_march28_session_reopen",
            subject_kind="compose_session",
            subject_identity="compose-session-0877864dcca7",
            workflow_key="intellectual_genealogy",
            consumer_key="the-critic",
            dimension_statuses={
                "identity_integrity": "pass",
                "saved_truth_fidelity": "pass",
                "reopen_integrity": "pass",
                "boundary_observance": "pass",
            },
        )
    )
    return {
        aoi.case_key: aoi.evaluation_report_id,
        genealogy.case_key: genealogy.evaluation_report_id,
    }


def test_build_gate_decision_passes_for_matching_reports(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.report_store.EVALUATION_REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")
    input_ids = _save_required_reports()

    gate_decision = build_evaluation_gate_decision(
        gate_key="bounded_platform_readiness_v1",
        evaluation_pack_key="phase4_frozen_governance_v1",
        input_report_ids_by_case_key=input_ids,
        save_decision=False,
    )

    assert gate_decision.overall_verdict == "pass"
    assert gate_decision.contains_live_revalidation is True
    assert gate_decision.input_report_ids_by_case_key == input_ids
    assert [case.case_verdict for case in gate_decision.case_summaries] == ["pass", "pass"]


def test_build_gate_decision_errors_on_missing_required_dimension(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.report_store.EVALUATION_REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    aoi = save_evaluation_report(
        _report(
            "evaluation-report-aoi",
            case_key="aoi_exemplar_march27_execution_backed",
            subject_kind="executor_job",
            subject_identity="job-744edf255ad5",
            workflow_key="anxiety_of_influence_thematic_single_thinker",
            consumer_key="the-critic",
            dimension_statuses={
                "selection_fit": "pass",
                "rationale_clarity": "pass",
                "rendered_usefulness": "pass",
                "operational_behavior": "pass",
            },
        )
    )
    genealogy = save_evaluation_report(
        _report(
            "evaluation-report-genealogy",
            case_key="genealogy_lifecycle_march28_session_reopen",
            subject_kind="compose_session",
            subject_identity="compose-session-0877864dcca7",
            workflow_key="intellectual_genealogy",
            consumer_key="the-critic",
            dimension_statuses={
                "identity_integrity": "pass",
                "saved_truth_fidelity": "pass",
                "reopen_integrity": "pass",
            },
        )
    )

    gate_decision = build_evaluation_gate_decision(
        gate_key="bounded_platform_readiness_v1",
        evaluation_pack_key="phase4_frozen_governance_v1",
        input_report_ids_by_case_key={
            aoi.case_key: aoi.evaluation_report_id,
            genealogy.case_key: genealogy.evaluation_report_id,
        },
        save_decision=False,
    )

    assert gate_decision.overall_verdict == "error"
    assert any(
        "boundary_observance" in reason for reason in gate_decision.blocking_reasons
    )


def test_build_gate_decision_fails_when_required_report_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.report_store.EVALUATION_REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    aoi = save_evaluation_report(
        _report(
            "evaluation-report-aoi",
            case_key="aoi_exemplar_march27_execution_backed",
            subject_kind="executor_job",
            subject_identity="job-744edf255ad5",
            workflow_key="anxiety_of_influence_thematic_single_thinker",
            consumer_key="the-critic",
            overall_verdict="fail",
            dimension_statuses={
                "selection_fit": "pass",
                "rationale_clarity": "pass",
                "rendered_usefulness": "pass",
                "operational_behavior": "pass",
            },
        )
    )
    genealogy = save_evaluation_report(
        _report(
            "evaluation-report-genealogy",
            case_key="genealogy_lifecycle_march28_session_reopen",
            subject_kind="compose_session",
            subject_identity="compose-session-0877864dcca7",
            workflow_key="intellectual_genealogy",
            consumer_key="the-critic",
            dimension_statuses={
                "identity_integrity": "pass",
                "saved_truth_fidelity": "pass",
                "reopen_integrity": "pass",
                "boundary_observance": "pass",
            },
        )
    )

    gate_decision = build_evaluation_gate_decision(
        gate_key="bounded_platform_readiness_v1",
        evaluation_pack_key="phase4_frozen_governance_v1",
        input_report_ids_by_case_key={
            aoi.case_key: aoi.evaluation_report_id,
            genealogy.case_key: genealogy.evaluation_report_id,
        },
        save_decision=False,
    )

    assert gate_decision.overall_verdict == "fail"
    assert any("overall_verdict='fail'" in reason for reason in gate_decision.blocking_reasons)


def test_build_gate_decision_errors_on_unexpected_input_case(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.report_store.EVALUATION_REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")
    input_ids = _save_required_reports()
    input_ids["extra_case"] = "evaluation-report-extra"

    gate_decision = build_evaluation_gate_decision(
        gate_key="bounded_platform_readiness_v1",
        evaluation_pack_key="phase4_frozen_governance_v1",
        input_report_ids_by_case_key=input_ids,
        save_decision=False,
    )

    assert gate_decision.overall_verdict == "error"
    assert any("unexpected input case_key 'extra_case'" in reason for reason in gate_decision.blocking_reasons)


def test_generate_then_gate_persists_one_passing_gate_on_current_frozen_pack(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.report_store.EVALUATION_REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    gate_decision = generate_then_build_evaluation_gate_decision(
        gate_key="bounded_platform_readiness_v1",
        evaluation_pack_key="phase4_frozen_governance_v1",
        save_reports=True,
        save_decision=True,
    )
    stored = list_evaluation_gate_decisions(limit=10)

    assert gate_decision.overall_verdict == "pass"
    assert set(gate_decision.input_report_ids_by_case_key) == {
        "aoi_exemplar_march27_execution_backed",
        "genealogy_lifecycle_march28_session_reopen",
    }
    assert len(stored) == 1


def test_generate_then_gate_passes_for_second_family_genealogy_pack(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.report_store.EVALUATION_REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    gate_decision = generate_then_build_evaluation_gate_decision(
        gate_key="bounded_genealogy_lifecycle_readiness_v1",
        evaluation_pack_key="phase4_genealogy_lifecycle_governance_v1",
        save_reports=True,
        save_decision=False,
    )

    assert gate_decision.overall_verdict == "pass"
    assert gate_decision.gate_key == "bounded_genealogy_lifecycle_readiness_v1"
    assert gate_decision.evaluation_pack_key == "phase4_genealogy_lifecycle_governance_v1"
    assert len(gate_decision.case_summaries) == 1
    assert len(gate_decision.input_report_ids_by_case_key) == 1
    assert [case.case_key for case in gate_decision.case_summaries] == [
        "genealogy_lifecycle_march28_session_reopen"
    ]
    assert set(gate_decision.input_report_ids_by_case_key) == {
        "genealogy_lifecycle_march28_session_reopen"
    }


def test_generate_then_gate_passes_for_aoi_standalone_family_pack(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.report_store.EVALUATION_REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    gate_decision = generate_then_build_evaluation_gate_decision(
        gate_key="bounded_aoi_exemplar_readiness_v1",
        evaluation_pack_key="phase4_aoi_exemplar_governance_v1",
        save_reports=True,
        save_decision=False,
    )

    assert gate_decision.overall_verdict == "pass"
    assert gate_decision.gate_key == "bounded_aoi_exemplar_readiness_v1"
    assert gate_decision.evaluation_pack_key == "phase4_aoi_exemplar_governance_v1"
    assert len(gate_decision.case_summaries) == 1
    assert len(gate_decision.input_report_ids_by_case_key) == 1
    assert [case.case_key for case in gate_decision.case_summaries] == [
        "aoi_exemplar_march27_execution_backed"
    ]
    assert set(gate_decision.input_report_ids_by_case_key) == {
        "aoi_exemplar_march27_execution_backed"
    }


def test_generate_then_gate_passes_for_routing_planning_family_pack(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.report_store.EVALUATION_REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    gate_decision = generate_then_build_evaluation_gate_decision(
        gate_key="bounded_routing_planning_readiness_v1",
        evaluation_pack_key="phase4_routing_planning_governance_v1",
        save_reports=True,
        save_decision=False,
    )

    assert gate_decision.overall_verdict == "pass"
    assert gate_decision.gate_key == "bounded_routing_planning_readiness_v1"
    assert gate_decision.evaluation_pack_key == "phase4_routing_planning_governance_v1"
    assert len(gate_decision.case_summaries) == 2
    assert len(gate_decision.input_report_ids_by_case_key) == 2
    assert [case.case_key for case in gate_decision.case_summaries] == [
        "aoi_saved_result_handoff_current_contract",
        "genealogy_saved_result_direct_sections_snapshot_march28",
    ]
    assert set(gate_decision.input_report_ids_by_case_key) == {
        "aoi_saved_result_handoff_current_contract",
        "genealogy_saved_result_direct_sections_snapshot_march28",
    }


def test_generate_then_gate_passes_for_planner_to_presentation_family_pack(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.report_store.EVALUATION_REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    gate_decision = generate_then_build_evaluation_gate_decision(
        gate_key="bounded_planner_to_presentation_readiness_v1",
        evaluation_pack_key="phase4_planner_to_presentation_governance_v1",
        save_reports=True,
        save_decision=False,
    )

    assert gate_decision.overall_verdict == "pass"
    assert gate_decision.gate_key == "bounded_planner_to_presentation_readiness_v1"
    assert gate_decision.evaluation_pack_key == "phase4_planner_to_presentation_governance_v1"
    assert len(gate_decision.case_summaries) == 2
    assert len(gate_decision.input_report_ids_by_case_key) == 2
    assert [case.case_key for case in gate_decision.case_summaries] == [
        "aoi_compose_selection_current_contract",
        "genealogy_direct_sections_compose_snapshot_march28",
    ]
    assert set(gate_decision.input_report_ids_by_case_key) == {
        "aoi_compose_selection_current_contract",
        "genealogy_direct_sections_compose_snapshot_march28",
    }


def test_generate_then_gate_passes_for_cross_campaign_planner_to_presentation_family_pack(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.report_store.EVALUATION_REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path / "gates")

    gate_decision = generate_then_build_evaluation_gate_decision(
        gate_key="bounded_planner_to_presentation_cross_campaign_readiness_v1",
        evaluation_pack_key="phase4_planner_to_presentation_cross_campaign_governance_v1",
        save_reports=True,
        save_decision=False,
    )

    assert gate_decision.overall_verdict == "pass"
    assert gate_decision.gate_key == "bounded_planner_to_presentation_cross_campaign_readiness_v1"
    assert gate_decision.evaluation_pack_key == "phase4_planner_to_presentation_cross_campaign_governance_v1"
    assert len(gate_decision.case_summaries) == 2
    assert len(gate_decision.input_report_ids_by_case_key) == 2
    assert [case.case_key for case in gate_decision.case_summaries] == [
        "aoi_compose_selection_current_contract_fresh_campaign",
        "genealogy_direct_sections_compose_current_contract_fresh_campaign",
    ]
    assert set(gate_decision.input_report_ids_by_case_key) == {
        "aoi_compose_selection_current_contract_fresh_campaign",
        "genealogy_direct_sections_compose_current_contract_fresh_campaign",
    }


def test_parse_report_mapping_rejects_duplicate_case_keys() -> None:
    with pytest.raises(ValueError) as excinfo:
        _parse_report_mapping(
            [
                "aoi_exemplar_march27_execution_backed=evaluation-report-first",
                "aoi_exemplar_march27_execution_backed=evaluation-report-second",
            ]
        )

    assert "Duplicate --report-id input" in str(excinfo.value)
