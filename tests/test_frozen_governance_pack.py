import hashlib
import json

import pytest

from src.evaluations.frozen_pack_definitions import (
    FrozenArtifactDefinition,
    FrozenEvaluationCaseDefinition,
    FrozenEvaluationPackDefinition,
    get_frozen_pack_definition,
    iter_pack_artifacts,
)
from src.evaluations.frozen_pack_harness import run_frozen_pack, run_pack_definition
from src.evaluations.report_store import list_evaluation_reports


def test_phase4_frozen_pack_artifact_hashes_match_repo_contents() -> None:
    pack = get_frozen_pack_definition("phase4_frozen_governance_v1")

    for artifact in iter_pack_artifacts(pack):
        assert artifact.absolute_path.exists(), artifact.relative_path
        observed = hashlib.sha256(artifact.absolute_path.read_bytes()).hexdigest()
        assert observed == artifact.expected_sha256


def test_second_genealogy_pack_is_registered_as_one_case_on_supported_evaluator() -> None:
    pack = get_frozen_pack_definition("phase4_genealogy_lifecycle_governance_v1")

    assert pack.evaluation_pack_key == "phase4_genealogy_lifecycle_governance_v1"
    assert len(pack.cases) == 1
    assert pack.cases[0].case_key == "genealogy_lifecycle_march28_session_reopen"
    assert pack.cases[0].evaluator_key == "genealogy_lifecycle"


def test_aoi_standalone_pack_is_registered_as_one_case_on_supported_evaluator() -> None:
    pack = get_frozen_pack_definition("phase4_aoi_exemplar_governance_v1")

    assert pack.evaluation_pack_key == "phase4_aoi_exemplar_governance_v1"
    assert len(pack.cases) == 1
    assert pack.cases[0].case_key == "aoi_exemplar_march27_execution_backed"
    assert pack.cases[0].evaluator_key == "aoi_exemplar"


def test_routing_planning_pack_is_registered_as_two_cases_on_supported_evaluator() -> None:
    pack = get_frozen_pack_definition("phase4_routing_planning_governance_v1")

    assert pack.evaluation_pack_key == "phase4_routing_planning_governance_v1"
    assert [case.case_key for case in pack.cases] == [
        "aoi_saved_result_handoff_current_contract",
        "genealogy_saved_result_direct_sections_snapshot_march28",
    ]
    assert all(case.evaluator_key == "routing_planning_decision" for case in pack.cases)


def test_planner_to_presentation_pack_is_registered_as_two_cases_on_supported_evaluator() -> None:
    pack = get_frozen_pack_definition("phase4_planner_to_presentation_governance_v1")

    assert pack.evaluation_pack_key == "phase4_planner_to_presentation_governance_v1"
    assert [case.case_key for case in pack.cases] == [
        "aoi_compose_selection_current_contract",
        "genealogy_direct_sections_compose_snapshot_march28",
    ]
    assert all(case.evaluator_key == "planner_presentation_decision" for case in pack.cases)


def test_cross_campaign_planner_to_presentation_pack_is_registered_as_two_cases_on_supported_evaluator() -> None:
    pack = get_frozen_pack_definition("phase4_planner_to_presentation_cross_campaign_governance_v1")

    assert pack.evaluation_pack_key == "phase4_planner_to_presentation_cross_campaign_governance_v1"
    assert [case.case_key for case in pack.cases] == [
        "aoi_compose_selection_current_contract_fresh_campaign",
        "genealogy_direct_sections_compose_current_contract_fresh_campaign",
    ]
    assert all(case.evaluator_key == "planner_presentation_decision" for case in pack.cases)


def test_run_frozen_pack_persists_two_passing_reports_on_current_frozen_evidence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.evaluations.report_store.EVALUATION_REPORTS_DIR",
        tmp_path,
    )

    reports = run_frozen_pack("phase4_frozen_governance_v1", save_report=True)
    stored = list_evaluation_reports(limit=10)

    assert [report.case_key for report in reports] == [
        "aoi_exemplar_march27_execution_backed",
        "genealogy_lifecycle_march28_session_reopen",
    ]
    assert [report.overall_verdict for report in reports] == ["pass", "pass"]
    assert len(stored) == 2

    genealogy_report = next(
        report for report in reports if report.case_key == "genealogy_lifecycle_march28_session_reopen"
    )
    checks_by_key = {check.check_key: check for check in genealogy_report.checks}
    saved_truth_dimension = next(
        dimension
        for dimension in genealogy_report.dimension_summaries
        if dimension.dimension_key == "saved_truth_fidelity"
    )

    assert checks_by_key["stored_session_fidelity_fields_present"].evidence_mode == "stored_object"
    assert all(
        ref.source_kind == "stored_object"
        for ref in checks_by_key["stored_session_fidelity_fields_present"].evidence_refs
    )
    assert checks_by_key["frozen_saved_session_artifact_valid"].evidence_mode == "frozen_artifact"
    assert all(
        ref.source_kind == "frozen_artifact"
        for ref in checks_by_key["frozen_saved_session_artifact_valid"].evidence_refs
    )
    assert saved_truth_dimension.supporting_checks == [
        "stored_session_fidelity_fields_present",
        "frozen_saved_session_artifact_valid",
    ]


def test_run_second_genealogy_pack_persists_one_passing_report_on_current_frozen_evidence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.evaluations.report_store.EVALUATION_REPORTS_DIR",
        tmp_path,
    )

    reports = run_frozen_pack("phase4_genealogy_lifecycle_governance_v1", save_report=True)
    stored = list_evaluation_reports(limit=10)

    assert [report.case_key for report in reports] == ["genealogy_lifecycle_march28_session_reopen"]
    assert [report.overall_verdict for report in reports] == ["pass"]
    assert reports[0].evaluation_pack_key == "phase4_genealogy_lifecycle_governance_v1"
    assert len(stored) == 1


def test_run_aoi_standalone_pack_persists_one_passing_report_on_current_frozen_evidence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.evaluations.report_store.EVALUATION_REPORTS_DIR",
        tmp_path,
    )

    reports = run_frozen_pack("phase4_aoi_exemplar_governance_v1", save_report=True)
    stored = list_evaluation_reports(limit=10)

    assert [report.case_key for report in reports] == ["aoi_exemplar_march27_execution_backed"]
    assert [report.overall_verdict for report in reports] == ["pass"]
    assert reports[0].evaluation_pack_key == "phase4_aoi_exemplar_governance_v1"
    assert len(stored) == 1


def test_run_routing_planning_pack_persists_two_passing_reports_on_current_frozen_evidence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.evaluations.report_store.EVALUATION_REPORTS_DIR",
        tmp_path,
    )

    reports = run_frozen_pack("phase4_routing_planning_governance_v1", save_report=True)
    stored = list_evaluation_reports(limit=10)

    assert [report.case_key for report in reports] == [
        "aoi_saved_result_handoff_current_contract",
        "genealogy_saved_result_direct_sections_snapshot_march28",
    ]
    assert [report.overall_verdict for report in reports] == ["pass", "pass"]
    assert len(stored) == 2

    genealogy_report = next(
        report
        for report in reports
        if report.case_key == "genealogy_saved_result_direct_sections_snapshot_march28"
    )
    route_check = next(
        check for check in genealogy_report.checks if check.check_key == "route_fidelity"
    )
    planning_check = next(
        check for check in genealogy_report.checks if check.check_key == "planning_followup_fidelity"
    )

    assert any(
        ref.locator.endswith("PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json#routing_decision")
        for ref in route_check.evidence_refs
    )
    assert any(
        ref.locator.endswith("PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json#planning_decision")
        for ref in planning_check.evidence_refs
    )


def test_run_planner_to_presentation_pack_persists_two_passing_reports_on_current_frozen_evidence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.evaluations.report_store.EVALUATION_REPORTS_DIR",
        tmp_path,
    )

    reports = run_frozen_pack("phase4_planner_to_presentation_governance_v1", save_report=True)
    stored = list_evaluation_reports(limit=10)

    assert [report.case_key for report in reports] == [
        "aoi_compose_selection_current_contract",
        "genealogy_direct_sections_compose_snapshot_march28",
    ]
    assert [report.overall_verdict for report in reports] == ["pass", "pass"]
    assert len(stored) == 2

    aoi_report = next(
        report for report in reports if report.case_key == "aoi_compose_selection_current_contract"
    )
    presentation_check = next(
        check for check in aoi_report.checks if check.check_key == "presentation_contract_fidelity"
    )

    assert presentation_check.observed_values["presentation_view_count"] == (
        presentation_check.observed_values["generated_view_definition_count"]
    )
    assert any(
        ref.locator.endswith(
            "PROOF_phase_d_aoi_transient_compose_current_contract_2026-03-30.json#compose_from_selection.response_json"
        )
        for ref in presentation_check.evidence_refs
    )


def test_run_cross_campaign_planner_to_presentation_pack_persists_two_passing_reports_on_fresh_frozen_evidence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.evaluations.report_store.EVALUATION_REPORTS_DIR",
        tmp_path,
    )

    reports = run_frozen_pack(
        "phase4_planner_to_presentation_cross_campaign_governance_v1",
        save_report=True,
    )
    stored = list_evaluation_reports(limit=10)

    assert [report.case_key for report in reports] == [
        "aoi_compose_selection_current_contract_fresh_campaign",
        "genealogy_direct_sections_compose_current_contract_fresh_campaign",
    ]
    assert [report.overall_verdict for report in reports] == ["pass", "pass"]
    assert len(stored) == 2

    genealogy_report = next(
        report
        for report in reports
        if report.case_key == "genealogy_direct_sections_compose_current_contract_fresh_campaign"
    )
    agreement_check = next(
        check for check in genealogy_report.checks if check.check_key == "planner_presentation_agreement"
    )

    assert agreement_check.observed_values["bundle_planning_decision_id"] == "planning-decision-5f5b0182f2f9"
    assert any(
        ref.locator.endswith(
            "PROOF_phase_d_cross_campaign_genealogy_transient_compose_2026-03-30.json#compose_from_intent.planning_decision_id"
        )
        for ref in agreement_check.evidence_refs
    )


def test_planner_to_presentation_aoi_case_fails_when_bundle_binding_id_drifts(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    original = (
        get_frozen_pack_definition("phase4_planner_to_presentation_governance_v1")
        .cases[0]
        .artifacts[0]
        .absolute_path
    )
    payload = json.loads(original.read_text(encoding="utf-8"))
    payload["compose_from_selection"]["planning_decision_id"] = "planning-decision-mismatch"

    artifact_path = tmp_path / "aoi_bad_bundle.json"
    artifact_path.write_text(json.dumps(payload), encoding="utf-8")
    observed_hash = hashlib.sha256(artifact_path.read_bytes()).hexdigest()

    monkeypatch.setattr("src.evaluations.frozen_pack_definitions.COMMUNICATIONS_DIR", tmp_path)
    pack = FrozenEvaluationPackDefinition(
        evaluation_pack_key="test-planner-presentation-pack",
        cases=(
            FrozenEvaluationCaseDefinition(
                case_key="aoi_compose_selection_current_contract",
                evaluator_key="planner_presentation_decision",
                subject_kind="planning_decision",
                subject_identity="planning-decision-1b0dbef41b28",
                workflow_key="anxiety_of_influence_thematic_single_thinker",
                consumer_key="the-critic",
                artifacts=(
                    FrozenArtifactDefinition(
                        ref_key="aoi_transient_compose_current_contract",
                        relative_path="aoi_bad_bundle.json",
                        expected_sha256=observed_hash,
                    ),
                ),
            ),
        ),
    )

    reports = run_pack_definition(pack, save_report=False)

    assert len(reports) == 1
    assert reports[0].overall_verdict == "fail"
    agreement_check = next(
        check for check in reports[0].checks if check.check_key == "planner_presentation_agreement"
    )
    assert agreement_check.status == "fail"


@pytest.mark.parametrize(
    ("mutator", "artifact_name"),
    [
        (
            lambda payload: payload.__setitem__("planning_decision_id", "planning-decision-mismatch"),
            "aoi_bad_top_level_bundle.json",
        ),
        (
            lambda payload: payload["compose_from_selection"].__setitem__(
                "planning_decision_id", "planning-decision-mismatch"
            ),
            "aoi_bad_nested_bundle.json",
        ),
    ],
)
def test_cross_campaign_planner_to_presentation_aoi_case_fails_when_binding_id_drifts(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    mutator,
    artifact_name: str,
) -> None:
    original = (
        get_frozen_pack_definition("phase4_planner_to_presentation_cross_campaign_governance_v1")
        .cases[0]
        .artifacts[0]
        .absolute_path
    )
    payload = json.loads(original.read_text(encoding="utf-8"))
    mutator(payload)

    artifact_path = tmp_path / artifact_name
    artifact_path.write_text(json.dumps(payload), encoding="utf-8")
    observed_hash = hashlib.sha256(artifact_path.read_bytes()).hexdigest()

    monkeypatch.setattr("src.evaluations.frozen_pack_definitions.COMMUNICATIONS_DIR", tmp_path)
    pack = FrozenEvaluationPackDefinition(
        evaluation_pack_key="test-planner-presentation-cross-campaign-pack",
        cases=(
            FrozenEvaluationCaseDefinition(
                case_key="aoi_compose_selection_current_contract_fresh_campaign",
                evaluator_key="planner_presentation_decision",
                subject_kind="planning_decision",
                subject_identity="planning-decision-d6b6bb0cd7ac",
                workflow_key="anxiety_of_influence_thematic_single_thinker",
                consumer_key="the-critic",
                artifacts=(
                    FrozenArtifactDefinition(
                        ref_key="aoi_transient_compose_cross_campaign",
                        relative_path=artifact_name,
                        expected_sha256=observed_hash,
                    ),
                ),
            ),
        ),
    )

    reports = run_pack_definition(pack, save_report=False)

    assert len(reports) == 1
    assert reports[0].overall_verdict == "fail"
    agreement_check = next(
        check for check in reports[0].checks if check.check_key == "planner_presentation_agreement"
    )
    assert agreement_check.status == "fail"


def test_planner_to_presentation_genealogy_case_fails_when_user_intent_drifts(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    source_case = get_frozen_pack_definition("phase4_planner_to_presentation_governance_v1").cases[1]
    trace_source = next(
        artifact.absolute_path for artifact in source_case.artifacts if artifact.ref_key == "phase2_trace_multi_surface"
    )
    snapshot_source = next(
        artifact.absolute_path for artifact in source_case.artifacts if artifact.ref_key == "genealogy_planning_snapshot"
    )

    trace_payload = json.loads(trace_source.read_text(encoding="utf-8"))
    trace_payload["lowered_compose_request"]["user_intent"] = "Trace a different genealogy."

    trace_path = tmp_path / "genealogy_bad_trace.json"
    trace_path.write_text(json.dumps(trace_payload), encoding="utf-8")
    trace_hash = hashlib.sha256(trace_path.read_bytes()).hexdigest()

    snapshot_path = tmp_path / "genealogy_snapshot.json"
    snapshot_path.write_text(snapshot_source.read_text(encoding="utf-8"), encoding="utf-8")
    snapshot_hash = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()

    monkeypatch.setattr("src.evaluations.frozen_pack_definitions.COMMUNICATIONS_DIR", tmp_path)
    pack = FrozenEvaluationPackDefinition(
        evaluation_pack_key="test-planner-presentation-pack",
        cases=(
            FrozenEvaluationCaseDefinition(
                case_key="genealogy_direct_sections_compose_snapshot_march28",
                evaluator_key="planner_presentation_decision",
                subject_kind="planning_decision",
                subject_identity="planning-decision-b1600d054991",
                workflow_key="intellectual_genealogy",
                consumer_key="the-critic",
                artifacts=(
                    FrozenArtifactDefinition(
                        ref_key="phase2_trace_multi_surface",
                        relative_path="genealogy_bad_trace.json",
                        expected_sha256=trace_hash,
                    ),
                    FrozenArtifactDefinition(
                        ref_key="genealogy_planning_snapshot",
                        relative_path="genealogy_snapshot.json",
                        expected_sha256=snapshot_hash,
                    ),
                ),
            ),
        ),
    )

    reports = run_pack_definition(pack, save_report=False)

    assert len(reports) == 1
    assert reports[0].overall_verdict == "fail"
    agreement_check = next(
        check for check in reports[0].checks if check.check_key == "planner_presentation_agreement"
    )
    assert agreement_check.status == "fail"


def test_planner_to_presentation_genealogy_case_fails_when_section_payload_drifts(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    source_case = get_frozen_pack_definition("phase4_planner_to_presentation_governance_v1").cases[1]
    trace_source = next(
        artifact.absolute_path for artifact in source_case.artifacts if artifact.ref_key == "phase2_trace_multi_surface"
    )
    snapshot_source = next(
        artifact.absolute_path for artifact in source_case.artifacts if artifact.ref_key == "genealogy_planning_snapshot"
    )

    trace_payload = json.loads(trace_source.read_text(encoding="utf-8"))
    trace_payload["lowered_compose_request"]["prose_sections"][0]["title"] = "Mutated section title"

    trace_path = tmp_path / "genealogy_bad_trace.json"
    trace_path.write_text(json.dumps(trace_payload), encoding="utf-8")
    trace_hash = hashlib.sha256(trace_path.read_bytes()).hexdigest()

    snapshot_path = tmp_path / "genealogy_snapshot.json"
    snapshot_path.write_text(snapshot_source.read_text(encoding="utf-8"), encoding="utf-8")
    snapshot_hash = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()

    monkeypatch.setattr("src.evaluations.frozen_pack_definitions.COMMUNICATIONS_DIR", tmp_path)
    pack = FrozenEvaluationPackDefinition(
        evaluation_pack_key="test-planner-presentation-pack",
        cases=(
            FrozenEvaluationCaseDefinition(
                case_key="genealogy_direct_sections_compose_snapshot_march28",
                evaluator_key="planner_presentation_decision",
                subject_kind="planning_decision",
                subject_identity="planning-decision-b1600d054991",
                workflow_key="intellectual_genealogy",
                consumer_key="the-critic",
                artifacts=(
                    FrozenArtifactDefinition(
                        ref_key="phase2_trace_multi_surface",
                        relative_path="genealogy_bad_trace.json",
                        expected_sha256=trace_hash,
                    ),
                    FrozenArtifactDefinition(
                        ref_key="genealogy_planning_snapshot",
                        relative_path="genealogy_snapshot.json",
                        expected_sha256=snapshot_hash,
                    ),
                ),
            ),
        ),
    )

    reports = run_pack_definition(pack, save_report=False)

    assert len(reports) == 1
    assert reports[0].overall_verdict == "fail"
    agreement_check = next(
        check for check in reports[0].checks if check.check_key == "planner_presentation_agreement"
    )
    assert agreement_check.status == "fail"


def test_cross_campaign_planner_to_presentation_genealogy_bundle_keeps_request_route_faithful() -> None:
    bundle_path = get_frozen_pack_definition(
        "phase4_planner_to_presentation_cross_campaign_governance_v1"
    ).cases[1].artifacts[0].absolute_path
    payload = json.loads(bundle_path.read_text(encoding="utf-8"))

    assert payload["planning_decision_id"] == "planning-decision-5f5b0182f2f9"
    assert payload["compose_from_intent"]["planning_decision_id"] == "planning-decision-5f5b0182f2f9"
    assert "planning_decision_id" not in payload["compose_from_intent"]["request_json"]


@pytest.mark.parametrize(
    ("mutator", "artifact_name"),
    [
        (
            lambda payload: payload.__setitem__("planning_decision_id", "planning-decision-mismatch"),
            "genealogy_bad_top_level_bundle.json",
        ),
        (
            lambda payload: payload["compose_from_intent"].__setitem__(
                "planning_decision_id", "planning-decision-mismatch"
            ),
            "genealogy_bad_nested_bundle.json",
        ),
    ],
)
def test_cross_campaign_planner_to_presentation_genealogy_case_fails_when_binding_id_drifts(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    mutator,
    artifact_name: str,
) -> None:
    source_case = get_frozen_pack_definition(
        "phase4_planner_to_presentation_cross_campaign_governance_v1"
    ).cases[1]
    bundle_source = source_case.artifacts[0].absolute_path

    bundle_payload = json.loads(bundle_source.read_text(encoding="utf-8"))
    mutator(bundle_payload)

    bundle_path = tmp_path / artifact_name
    bundle_path.write_text(json.dumps(bundle_payload), encoding="utf-8")
    bundle_hash = hashlib.sha256(bundle_path.read_bytes()).hexdigest()

    monkeypatch.setattr("src.evaluations.frozen_pack_definitions.COMMUNICATIONS_DIR", tmp_path)
    pack = FrozenEvaluationPackDefinition(
        evaluation_pack_key="test-planner-presentation-cross-campaign-pack",
        cases=(
            FrozenEvaluationCaseDefinition(
                case_key="genealogy_direct_sections_compose_current_contract_fresh_campaign",
                evaluator_key="planner_presentation_decision",
                subject_kind="planning_decision",
                subject_identity="planning-decision-5f5b0182f2f9",
                workflow_key="intellectual_genealogy",
                consumer_key="the-critic",
                artifacts=(
                    FrozenArtifactDefinition(
                        ref_key="genealogy_transient_compose_cross_campaign",
                        relative_path=artifact_name,
                        expected_sha256=bundle_hash,
                    ),
                ),
            ),
        ),
    )

    reports = run_pack_definition(pack, save_report=False)

    assert len(reports) == 1
    assert reports[0].overall_verdict == "fail"
    agreement_check = next(
        check for check in reports[0].checks if check.check_key == "planner_presentation_agreement"
    )
    assert agreement_check.status == "fail"


def test_hash_drift_produces_error_report(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    artifact_path = tmp_path / "artifact.json"
    artifact_path.write_text(json.dumps({"ok": True}), encoding="utf-8")

    monkeypatch.setattr(
        "src.evaluations.frozen_pack_definitions.COMMUNICATIONS_DIR",
        tmp_path,
    )
    pack = FrozenEvaluationPackDefinition(
        evaluation_pack_key="test-pack",
        cases=(
            FrozenEvaluationCaseDefinition(
                case_key="bad-hash-case",
                evaluator_key="aoi_exemplar",
                subject_kind="executor_job",
                subject_identity="job-test",
                workflow_key="anxiety_of_influence_thematic_single_thinker",
                consumer_key="the-critic",
                artifacts=(
                    FrozenArtifactDefinition(
                        ref_key="bad_artifact",
                        relative_path="artifact.json",
                        expected_sha256="not-the-real-hash",
                    ),
                ),
            ),
        ),
    )

    reports = run_pack_definition(pack, save_report=False)

    assert len(reports) == 1
    assert reports[0].overall_verdict == "error"
    assert reports[0].checks[0].status == "error"
