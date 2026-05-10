import asyncio

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from src.api.routes.orchestrator import route_task as route_task_route
from src.orchestrator.task_router import route_composition_task
from src.orchestrator.task_routing_schemas import CompositionTaskRequest


def test_route_task_rejects_whitespace_only_task():
    with pytest.raises(ValidationError, match="task must not be empty"):
        CompositionTaskRequest.model_validate({"task": "   "})


def test_route_task_rejects_unknown_objective_hint_with_400():
    request = CompositionTaskRequest(task="Trace the genealogy of this work", objective_hint="unknown")

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(route_task_route(request))

    assert excinfo.value.status_code == 400
    assert "Unknown objective_hint" in str(excinfo.value.detail)


def test_route_task_rejects_cross_mode_source_constraints_payload():
    with pytest.raises(ValidationError):
        CompositionTaskRequest.model_validate(
            {
                "task": "Compose an AOI dossier",
                "source_constraints": {
                    "source_mode": "saved_result",
                    "source_v2_job_id": "job-123",
                    "consumer_key": "the-critic",
                    "external_project_id": "proj-1",
                    "target_external_doc_key": "doc-1",
                    "prior_work_external_doc_keys_count": 2,
                    "has_target_chapter_external_doc_keys": False,
                },
            }
        )


def test_route_task_routes_aoi_over_analyzer_native_contract():
    decision = route_composition_task(
        CompositionTaskRequest(
            task="Compose an anxiety of influence dossier about misreading, revision, and thematic influence.",
            consumer_key="the-critic",
            source_constraints={
                "source_mode": "saved_result",
                "selected_source_thinker_id": "otto_neurath",
                "source_v2_job_id": "job-aoi-001",
            },
        )
    )

    assert decision.selected_objective_key == "influence_thematic"
    assert decision.selected_workflow_key == "anxiety_of_influence_thematic_single_thinker"
    assert decision.routing_outcome == "aoi_transient_source_backed"
    assert decision.launch_contract_kind == "planner.aoi_compose_handoff"
    assert decision.routing_confidence == "high"
    assert decision.source_sufficiency_status == "sufficient"
    assert decision.required_fields == ["workflow_key", "consumer_key", "source_v2_job_id"]
    assert decision.downstream_launch_contract["endpoint"] == "/v1/orchestrator/plan-task"
    assert decision.downstream_launch_contract["request_fields"]["planning_context.source_v2_job_id"] == "job-aoi-001"


def test_route_task_treats_source_analysis_id_as_host_preparation_for_aoi():
    decision = route_composition_task(
        CompositionTaskRequest(
            task="Map influence in this work.",
            consumer_key="the-critic",
            source_constraints={
                "source_mode": "saved_result",
                "source_analysis_id": "analysis-123",
            },
        )
    )

    assert decision.routing_outcome == "aoi_transient_source_backed"
    assert decision.launch_contract_kind == "planner.aoi_compose_handoff"
    assert decision.routing_confidence == "medium"
    assert decision.source_sufficiency_status == "sufficient"
    assert decision.required_fields == ["workflow_key", "consumer_key", "source_v2_job_id"]
    assert any("Resolve source_v2_job_id" in step for step in decision.required_host_preparation)
    assert decision.downstream_launch_contract["request_fields"]["planning_context.source_v2_job_id"] == "<required>"


def test_route_task_routes_genealogy_registered_corpus_to_analyze_by_ref():
    decision = route_composition_task(
        CompositionTaskRequest(
            task="Trace the genealogy, lineage, and conditions of possibility behind this work.",
            source_constraints={
                "source_mode": "registered_corpus",
                "consumer_key": "the-critic",
                "external_project_id": "proj-1",
                "target_external_doc_key": "target-doc",
                "prior_work_external_doc_keys_count": 3,
                "has_target_chapter_external_doc_keys": True,
            },
        )
    )

    assert decision.selected_objective_key == "genealogical"
    assert decision.selected_workflow_key == "intellectual_genealogy"
    assert decision.routing_outcome == "genealogy_job_backed"
    assert decision.launch_contract_kind == "orchestrator.analyze_by_ref"
    assert decision.source_sufficiency_status == "sufficient"
    assert decision.required_fields == [
        "consumer_key",
        "external_project_id",
        "thinker_name",
        "target_work",
        "target_external_doc_key",
        "prior_works",
    ]
    assert decision.downstream_launch_contract["endpoint"] == "/v1/orchestrator/analyze-by-ref"
    assert decision.required_host_preparation


def test_route_task_routes_genealogy_saved_result_to_direct_sections_planner_handoff():
    decision = route_composition_task(
        CompositionTaskRequest(
            task="Trace the genealogy and intellectual development visible in this saved result.",
            consumer_key="the-critic",
            source_constraints={
                "source_mode": "saved_result",
                "source_v2_job_id": "job-genealogy-001",
            },
        )
    )

    assert decision.selected_objective_key == "genealogical"
    assert decision.selected_workflow_key == "intellectual_genealogy"
    assert decision.routing_outcome == "genealogy_transient_source_backed"
    assert decision.launch_contract_kind == "planner.direct_sections_compose_handoff"
    assert decision.required_fields == ["workflow_key", "consumer_key", "source_v2_job_id"]
    assert decision.downstream_launch_contract["endpoint"] == "/v1/orchestrator/plan-task"
    assert decision.downstream_launch_contract["advisory_only"] is True
    assert decision.downstream_launch_contract["request_fields"]["planning_context.context_mode"] == "saved_result"
    assert decision.downstream_launch_contract["request_fields"]["planning_context.source_v2_job_id"] == "job-genealogy-001"


def test_route_task_routes_genealogy_inline_documents_to_analyze():
    decision = route_composition_task(
        CompositionTaskRequest(
            task="Trace the genealogy and inheritance patterns in this target work.",
            source_constraints={
                "source_mode": "inline_documents",
                "has_target_work_text": True,
                "prior_work_count": 2,
                "has_target_work_chapters": False,
            },
        )
    )

    assert decision.selected_objective_key == "genealogical"
    assert decision.routing_outcome == "genealogy_job_backed"
    assert decision.launch_contract_kind == "orchestrator.analyze"
    assert decision.source_sufficiency_status == "sufficient"
    assert decision.required_fields == ["thinker_name", "target_work", "target_work_text", "prior_works"]
    assert decision.downstream_launch_contract["endpoint"] == "/v1/orchestrator/analyze"


def test_route_task_treats_source_analysis_id_as_insufficient_for_genealogy_saved_result():
    decision = route_composition_task(
        CompositionTaskRequest(
            task="Trace the genealogy visible in this saved result.",
            consumer_key="the-critic",
            source_constraints={
                "source_mode": "saved_result",
                "source_analysis_id": "analysis-123",
            },
        )
    )

    assert decision.selected_objective_key == "genealogical"
    assert decision.routing_outcome == "unsupported"
    assert decision.source_sufficiency_status == "insufficient"


def test_route_task_marks_aoi_without_saved_result_identity_as_insufficient():
    decision = route_composition_task(
        CompositionTaskRequest(
            task="Compose an anxiety of influence dossier about misreading and revision.",
        )
    )

    assert decision.selected_objective_key == "influence_thematic"
    assert decision.routing_outcome == "unsupported"
    assert decision.launch_contract_kind == "unsupported"
    assert decision.source_sufficiency_status == "insufficient"


def test_route_task_fails_closed_for_cross_signal_aoi_task_with_registered_corpus():
    decision = route_composition_task(
        CompositionTaskRequest(
            task="Compose an AOI dossier about misreading, revision, and source thinker engagement.",
            source_constraints={
                "source_mode": "registered_corpus",
                "consumer_key": "the-critic",
                "external_project_id": "proj-1",
                "target_external_doc_key": "target-doc",
                "prior_work_external_doc_keys_count": 4,
                "has_target_chapter_external_doc_keys": False,
            },
        )
    )

    assert decision.selected_objective_key == "influence_thematic"
    assert decision.routing_outcome == "unsupported"
    assert decision.source_sufficiency_status == "insufficient"
    assert decision.launch_contract_kind == "unsupported"
    assert all(candidate.objective_key != "genealogical" or candidate.rejection_reason for candidate in decision.rejected_candidates)


def test_route_task_returns_unsupported_for_ambiguous_borderline_task():
    decision = route_composition_task(
        CompositionTaskRequest(
            task="Compare how this work relates to earlier texts.",
        )
    )

    assert decision.selected_objective_key is None
    assert decision.routing_outcome == "unsupported"
    assert decision.routing_confidence == "low"
    assert decision.source_sufficiency_status == "ambiguous"


def test_route_task_objective_hint_incompatible_with_source_mode_fails_closed():
    decision = route_composition_task(
        CompositionTaskRequest(
            task="Map themes of influence.",
            objective_hint="influence_thematic",
            source_constraints={
                "source_mode": "inline_documents",
                "has_target_work_text": True,
                "prior_work_count": 2,
                "has_target_work_chapters": False,
            },
        )
    )

    assert decision.selected_objective_key == "influence_thematic"
    assert decision.routing_outcome == "unsupported"
    assert decision.source_sufficiency_status == "insufficient"


def test_route_task_workflow_hint_is_trace_only_and_never_overrides_objective():
    decision = route_composition_task(
        CompositionTaskRequest(
            task="Trace the genealogy of concept evolution in this corpus.",
            objective_hint="genealogical",
            workflow_hint="anxiety_of_influence_thematic_single_thinker",
            source_constraints={
                "source_mode": "inline_documents",
                "has_target_work_text": True,
                "prior_work_count": 2,
                "has_target_work_chapters": False,
            },
        )
    )

    assert decision.selected_objective_key == "genealogical"
    assert decision.selected_workflow_key == "intellectual_genealogy"
    assert decision.routing_outcome == "genealogy_job_backed"
    scoring_trace = next(entry for entry in decision.trace if entry.stage == "objective_candidate_scoring")
    assert scoring_trace.details["workflow_hint_status"] == "rejected_as_inconsistent"


def test_route_task_never_dispatches_into_execution_paths(monkeypatch):
    monkeypatch.setattr("src.api.routes.orchestrator.run_analysis_pipeline", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("analyze should not run")))
    monkeypatch.setattr("src.api.routes.orchestrator.run_analysis_by_ref", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("analyze-by-ref should not run")))

    decision = asyncio.run(
        route_task_route(
            CompositionTaskRequest(
                task="Trace the genealogy and inheritance patterns in this target work.",
                source_constraints={
                    "source_mode": "inline_documents",
                    "has_target_work_text": True,
                    "prior_work_count": 1,
                    "has_target_work_chapters": False,
                },
            )
        )
    )

    assert decision.launch_contract_kind == "orchestrator.analyze"
