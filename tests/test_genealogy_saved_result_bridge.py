import pytest

from src.engines.discovery import resolve_capability_definition
from src.engines.registry import get_engine_registry
from src.orchestrator.direct_sections_compose_harness import (
    DirectSectionsLoweringError,
    lower_direct_sections_handoff_plan,
)
from src.orchestrator.genealogy_saved_result_bridge import (
    GenealogySavedResultBridgeError,
    build_genealogy_saved_result_handoff_plan,
)


def test_build_genealogy_saved_result_handoff_plan_extracts_bounded_sections(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "src.orchestrator.genealogy_saved_result_bridge.get_job",
        lambda job_id: {
            "job_id": job_id,
            "workflow_key": "intellectual_genealogy",
            "status": "completed",
        },
    )
    monkeypatch.setattr(
        "src.orchestrator.genealogy_saved_result_bridge.load_phase_outputs",
        lambda job_id: [
            {
                "id": "po-1",
                "engine_key": "genealogy_relationship_classification",
                "phase_number": 1.5,
                "pass_number": 1,
                "content": "Relationship comparison prose.",
            },
            {
                "id": "po-2",
                "engine_key": "genealogy_final_synthesis",
                "phase_number": 4.0,
                "pass_number": 1,
                "content": "Narrative genealogy closeout prose.",
            },
        ],
    )

    handoff = build_genealogy_saved_result_handoff_plan(
        source_v2_job_id="job-genealogy-001",
        task_text="Trace the genealogy in this saved result.",
        consumer_key="the-critic",
    )

    assert handoff.workflow_key == "intellectual_genealogy"
    assert [section.title for section in handoff.prose_sections] == [
        "Relationship Comparison Map",
        "Genealogy Report",
    ]
    assert [trace.role_hint for trace in handoff.section_trace] == [
        "comparison_map",
        "report_closeout",
    ]
    lowered = lower_direct_sections_handoff_plan(handoff)
    assert lowered.workflow_key == "intellectual_genealogy"
    assert lowered.user_intent == "Trace the genealogy in this saved result."


def test_build_genealogy_saved_result_handoff_plan_fails_for_non_genealogy_job(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "src.orchestrator.genealogy_saved_result_bridge.get_job",
        lambda _job_id: {
            "workflow_key": "anxiety_of_influence_thematic_single_thinker",
            "status": "completed",
        },
    )

    with pytest.raises(GenealogySavedResultBridgeError):
        build_genealogy_saved_result_handoff_plan(
            source_v2_job_id="job-wrong-001",
            task_text="Trace the genealogy in this saved result.",
            consumer_key="the-critic",
        )


def test_lower_direct_sections_handoff_plan_fails_closed_when_role_hint_is_not_recoverable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "src.orchestrator.genealogy_saved_result_bridge.get_job",
        lambda job_id: {
            "job_id": job_id,
            "workflow_key": "intellectual_genealogy",
            "status": "completed",
        },
    )
    monkeypatch.setattr(
        "src.orchestrator.genealogy_saved_result_bridge.load_phase_outputs",
        lambda job_id: [
            {
                "id": "po-1",
                "engine_key": "genealogy_final_synthesis",
                "phase_number": 4.0,
                "pass_number": 1,
                "content": "Narrative genealogy closeout prose.",
            },
        ],
    )

    handoff = build_genealogy_saved_result_handoff_plan(
        source_v2_job_id="job-genealogy-001",
        task_text="Trace the genealogy in this saved result.",
        consumer_key="the-critic",
    )
    handoff.section_trace[0].role_hint = "comparison_map"  # type: ignore[misc]

    with pytest.raises(DirectSectionsLoweringError):
        lower_direct_sections_handoff_plan(handoff)


def test_genealogy_saved_result_bridge_emitted_role_hints_match_capability_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "src.orchestrator.genealogy_saved_result_bridge.get_job",
        lambda job_id: {
            "job_id": job_id,
            "workflow_key": "intellectual_genealogy",
            "status": "completed",
        },
    )
    monkeypatch.setattr(
        "src.orchestrator.genealogy_saved_result_bridge.load_phase_outputs",
        lambda job_id: [
            {
                "id": "po-1",
                "engine_key": "genealogy_relationship_classification",
                "phase_number": 1.5,
                "pass_number": 1,
                "content": "Relationship comparison prose.",
            },
            {
                "id": "po-2",
                "engine_key": "genealogy_pass7_final_synthesis",
                "phase_number": 4.0,
                "pass_number": 1,
                "content": "Narrative genealogy closeout prose.",
            },
        ],
    )

    handoff = build_genealogy_saved_result_handoff_plan(
        source_v2_job_id="job-genealogy-role-hints",
        task_text="Trace the genealogy in this saved result.",
        consumer_key="the-critic",
    )
    registry = get_engine_registry()

    for trace in handoff.section_trace:
        resolved = resolve_capability_definition(registry, trace.engine_key)
        assert resolved is not None
        assert trace.role_hint == resolved.composition_role


def test_lower_direct_sections_handoff_plan_supports_legacy_genealogy_alias_with_neutral_title(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "src.orchestrator.genealogy_saved_result_bridge.get_job",
        lambda job_id: {
            "job_id": job_id,
            "workflow_key": "intellectual_genealogy",
            "status": "completed",
        },
    )
    monkeypatch.setattr(
        "src.orchestrator.genealogy_saved_result_bridge.load_phase_outputs",
        lambda job_id: [
            {
                "id": "po-1",
                "engine_key": "genealogy_pass7_final_synthesis",
                "phase_number": 4.0,
                "pass_number": 1,
                "content": "Narrative genealogy closeout prose.",
            },
        ],
    )
    monkeypatch.setattr(
        "src.orchestrator.genealogy_saved_result_bridge._derive_section_title",
        lambda *_args, **_kwargs: "Neutral Surface",
    )

    handoff = build_genealogy_saved_result_handoff_plan(
        source_v2_job_id="job-genealogy-legacy-001",
        task_text="Trace the genealogy in this saved result.",
        consumer_key="the-critic",
    )

    assert handoff.section_trace[0].role_hint == "report_closeout"
    lowered = lower_direct_sections_handoff_plan(handoff)

    assert lowered.prose_sections[0].engine_key == "genealogy_pass7_final_synthesis"
    assert lowered.prose_sections[0].title == "Neutral Surface"


def test_build_genealogy_saved_result_handoff_plan_fails_when_matched_legacy_row_lacks_valid_role_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "src.orchestrator.genealogy_saved_result_bridge.get_job",
        lambda job_id: {
            "job_id": job_id,
            "workflow_key": "intellectual_genealogy",
            "status": "completed",
        },
    )
    monkeypatch.setattr(
        "src.orchestrator.genealogy_saved_result_bridge.load_phase_outputs",
        lambda job_id: [
            {
                "id": "po-1",
                "engine_key": "genealogy_pass7_final_synthesis",
                "phase_number": 4.0,
                "pass_number": 1,
                "content": "Narrative genealogy closeout prose.",
            },
        ],
    )

    class _Registry:
        def get_capability_definition(self, _engine_key):
            return None

        def list_capability_definitions(self):
            return []

        def get(self, _engine_key):
            return None

    monkeypatch.setattr(
        "src.orchestrator.genealogy_saved_result_bridge.get_engine_registry",
        lambda: _Registry(),
    )

    with pytest.raises(GenealogySavedResultBridgeError) as excinfo:
        build_genealogy_saved_result_handoff_plan(
            source_v2_job_id="job-genealogy-metadata-fail",
            task_text="Trace the genealogy in this saved result.",
            consumer_key="the-critic",
        )

    assert "role_hint" in str(excinfo.value)
    assert "genealogy_pass7_final_synthesis" in str(excinfo.value)
