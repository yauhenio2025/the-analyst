import asyncio
import json

import anthropic
import pytest
from fastapi import HTTPException

from src.api.routes.orchestrator import (
    get_planning_decision as get_planning_decision_route,
    plan_task as plan_task_route,
)
from src.orchestrator.planning_decision_store import load_task_planning_decision
from src.orchestrator import task_planner as task_planner_module
from src.orchestrator.task_planner import plan_composition_task
from src.orchestrator.task_planning_schemas import (
    DirectSectionsCompositionHandoffPlan,
    DirectSectionsSectionTrace,
    TaskPlanningRequest,
)
from src.orchestrator.task_router import route_composition_task
from src.orchestrator.task_routing_schemas import CompositionTaskRequest
from src.orchestrator.schemas import PriorWork, TargetWork, WorkflowExecutionPlan
from src.presenter.composition_source_bridge import (
    CompositionSourceCandidate,
    CompositionSourceCatalog,
)
from src.presenter.schemas import AoiRejectedSourceInput, AoiSelectedSourceInput
from src.presenter.schemas import ComposeFromIntentSectionInput


def _fake_genealogy_plan(plan_id: str = "plan-stage9-inline") -> WorkflowExecutionPlan:
    return WorkflowExecutionPlan(
        plan_id=plan_id,
        workflow_key="intellectual_genealogy",
        thinker_name="Walter Benjamin",
        target_work=TargetWork(
            title="The Arcades Project",
            author="Walter Benjamin",
            description="Target work",
        ),
        prior_works=[
            PriorWork(
                title="Capital",
                author="Karl Marx",
                description="Prior work",
                relationship_hint="upstream influence",
            )
        ],
        strategy_summary="summary",
        phases=[],
        recommended_views=[],
        estimated_llm_calls=4,
        estimated_depth_profile="standard",
        objective_key="genealogical",
    )


def _fake_aoi_catalog() -> CompositionSourceCatalog:
    return CompositionSourceCatalog(
        source_v2_job_id="job-aoi-001",
        workflow_key="anxiety_of_influence_thematic_single_thinker",
        objective_key="influence_thematic",
        objective_source="plan_context",
        plan_context_found=True,
        plan_context_source="plan_file",
        selected_source_thinker_id="otto_neurath",
        selected_source_thinker_name="Otto Neurath",
        candidates=[
            CompositionSourceCandidate(
                source_family_key="thematic_synthesis",
                engine_key="aoi_thematic_synthesis",
                title="Thematic Synthesis",
                source_backend_kind="artifact",
                candidate_state="available",
                provenance_pointer={"job_id": "job-aoi-001"},
                composition_role_hint="synthesis_primary",
                summary_metadata={"payload_kind": "normalized_artifact"},
                plan_context_enrichment={"plan_context_found": True},
                resolution_note="Loaded",
                materialization_payload={"summary": "ok"},
            ),
            CompositionSourceCandidate(
                source_family_key="engagement_mapping",
                engine_key="aoi_engagement_mapping",
                title="Engagement Mapping",
                source_backend_kind="artifact",
                candidate_state="available",
                provenance_pointer={"job_id": "job-aoi-001"},
                composition_role_hint="comparison_map",
                summary_metadata={"payload_kind": "normalized_artifact"},
                plan_context_enrichment={"plan_context_found": True},
                resolution_note="Loaded",
                materialization_payload={"summary": "ok"},
            ),
            CompositionSourceCandidate(
                source_family_key="sin_findings",
                engine_key="aoi_sin_findings",
                title="Sin Findings",
                source_backend_kind="artifact",
                candidate_state="unavailable",
                provenance_pointer={"job_id": "job-aoi-001"},
                composition_role_hint="findings_bank",
                summary_metadata={"payload_kind": "normalized_artifact"},
                plan_context_enrichment={"plan_context_found": True},
                resolution_note="Missing",
                materialization_payload=None,
            ),
            CompositionSourceCandidate(
                source_family_key="thematic_report",
                engine_key="aoi_thematic_report",
                title="AOI Report",
                source_backend_kind="phase_output_metadata",
                candidate_state="available",
                provenance_pointer={"job_id": "job-aoi-001"},
                composition_role_hint="report_closeout",
                summary_metadata={"payload_kind": "report_sections"},
                plan_context_enrichment={"plan_context_found": True},
                resolution_note="Loaded",
                materialization_payload={"sections": []},
            ),
        ],
    )


def _fake_aoi_selection_result() -> dict[str, object]:
    return {
        "selected_sources": [
            AoiSelectedSourceInput(
                source_family_key="thematic_synthesis",
                selection_rank=1,
                rationale="Use the synthesis as the primary thematic frame.",
            ),
            AoiSelectedSourceInput(
                source_family_key="thematic_report",
                selection_rank=2,
                rationale="Use the report as the closeout without findings-bank overload.",
            ),
        ],
        "rejected_sources": [
            AoiRejectedSourceInput(
                source_family_key="engagement_mapping",
                rejection_reason="Not central for this task framing.",
            ),
        ],
        "selection_summary": "Use synthesis plus report for a compact thematic handoff.",
        "resolved_intent_seed": "Compose a concise AOI synthesis with a report closeout.",
        "legacy_profile_equivalent": "dossier",
        "trace_details": {
            "prompt_version": "aoi-selection-v1",
            "model_used": "stub-model",
            "timeout_s": task_planner_module._get_aoi_selection_timeout_s(),
            "retry_policy": {"max_retries": task_planner_module.AOI_SELECTION_MAX_RETRIES},
            "provider_outcome": "success",
            "validator_version": "aoi-selection-validator-v1",
        },
    }


def _fake_genealogy_direct_sections_handoff() -> DirectSectionsCompositionHandoffPlan:
    return DirectSectionsCompositionHandoffPlan(
        workflow_key="intellectual_genealogy",
        objective_key="genealogical",
        consumer_key="the-critic",
        source_v2_job_id="job-genealogy-001",
        resolved_intent_seed="Compose a concise genealogy briefing from the saved result.",
        prose_sections=[
            ComposeFromIntentSectionInput(
                engine_key="genealogy_relationship_classification",
                title="Relationship Comparison Map",
                prose="Structured comparison prose.",
            ),
            ComposeFromIntentSectionInput(
                engine_key="genealogy_final_synthesis",
                title="Genealogy Report",
                prose="Narrative genealogy closeout prose.",
            ),
        ],
        section_trace=[
            DirectSectionsSectionTrace(
                order=1,
                engine_key="genealogy_relationship_classification",
                title="Relationship Comparison Map",
                provenance_pointer={"job_id": "job-genealogy-001", "output_id": "po-1"},
                role_hint="comparison_map",
                rationale="Relationship comparison section.",
            ),
            DirectSectionsSectionTrace(
                order=2,
                engine_key="genealogy_final_synthesis",
                title="Genealogy Report",
                provenance_pointer={"job_id": "job-genealogy-001", "output_id": "po-2"},
                role_hint="report_closeout",
                rationale="Final synthesis section.",
            ),
        ],
        handoff_notes=["Derived from analyzer-owned saved-result truth."],
    )


def test_plan_task_returns_unsupported_for_ambiguous_task():
    decision = plan_composition_task(
        TaskPlanningRequest(
            task_request=CompositionTaskRequest(
                task="Compare how this work relates to earlier texts.",
            )
        )
    )

    assert decision.planning_outcome_kind == "unsupported"
    assert decision.downstream_readiness == "unsupported"


def test_plan_task_returns_insufficient_for_genealogy_without_planning_context():
    decision = plan_composition_task(
        TaskPlanningRequest(
            task_request=CompositionTaskRequest(
                task="Trace the genealogy and inheritance patterns in this target work.",
                source_constraints={
                    "source_mode": "inline_documents",
                    "has_target_work_text": True,
                    "prior_work_count": 2,
                    "has_target_work_chapters": False,
                },
            )
        )
    )

    assert decision.planning_outcome_kind == "insufficient_context"
    assert decision.hydration_status == "required"
    assert "planning_context.inline_documents.target_work_text" in decision.required_hydration


def test_plan_task_rejects_conflicting_inline_counts_with_400():
    request = TaskPlanningRequest(
        task_request=CompositionTaskRequest(
            task="Trace the genealogy of this work.",
            source_constraints={
                "source_mode": "inline_documents",
                "has_target_work_text": True,
                "prior_work_count": 1,
                "has_target_work_chapters": False,
            },
        ),
        planning_context={
            "context_mode": "inline_documents",
            "thinker_name": "Walter Benjamin",
            "target_work": {
                "title": "The Arcades Project",
                "author": "Walter Benjamin",
                "description": "Target work",
            },
            "target_work_text": "Target text",
            "prior_works": [
                {
                    "title": "Capital",
                    "author": "Karl Marx",
                    "description": "Prior",
                    "relationship_hint": "influence",
                    "text": "Prior text one",
                },
                {
                    "title": "History and Class Consciousness",
                    "author": "Georg Lukacs",
                    "description": "Prior",
                    "relationship_hint": "influence",
                    "text": "Prior text two",
                },
            ],
        },
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(plan_task_route(request))

    assert excinfo.value.status_code == 400
    assert "prior_work_count conflicts" in str(excinfo.value.detail)


def test_plan_task_generates_inline_genealogy_plan_and_validates_prior_route(monkeypatch):
    fake_plan = _fake_genealogy_plan("plan-inline-stage9")
    document_ids = {"target": "doc-target", "Capital": "doc-prior"}
    monkeypatch.setattr(
        "src.orchestrator.task_planner.generate_plan_for_analysis_request",
        lambda _request: (fake_plan, document_ids),
    )

    prior_routing_decision = route_composition_task(
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

    decision = plan_composition_task(
        TaskPlanningRequest(
            task_request=CompositionTaskRequest(
                task="Trace the genealogy and inheritance patterns in this target work.",
            ),
            prior_routing_decision=prior_routing_decision,
            planning_context={
                "context_mode": "inline_documents",
                "thinker_name": "Walter Benjamin",
                "target_work": {
                    "title": "The Arcades Project",
                    "author": "Walter Benjamin",
                    "description": "Target work",
                },
                "target_work_text": "Target text",
                "prior_works": [
                    {
                        "title": "Capital",
                        "author": "Karl Marx",
                        "description": "Prior",
                        "relationship_hint": "influence",
                        "text": "Prior text",
                    }
                ],
            },
        )
    )

    assert decision.planning_outcome_kind == "genealogy_execution_plan"
    assert decision.downstream_readiness == "ready_for_genealogy_execution"
    assert decision.workflow_execution_plan is not None
    assert decision.workflow_execution_plan.plan_id == "plan-inline-stage9"
    assert decision.hydrated_document_ids == document_ids
    assert decision.downstream_followup_contract["endpoint"] == "/v1/executor/jobs"
    reuse_trace = next(entry for entry in decision.trace if entry.stage == "routing_reuse")
    assert reuse_trace.details["status"] == "provided_and_validated"


def test_plan_task_ignores_mismatched_prior_routing_and_recomputes(monkeypatch):
    fake_plan = _fake_genealogy_plan("plan-recomputed-stage9")
    monkeypatch.setattr(
        "src.orchestrator.task_planner.generate_plan_for_analysis_request",
        lambda _request: (fake_plan, {"target": "doc-target", "Capital": "doc-prior"}),
    )

    stale_prior = route_composition_task(
        CompositionTaskRequest(
            task="Compose an anxiety of influence dossier about revision and misreading.",
            consumer_key="the-critic",
            source_constraints={"source_mode": "saved_result", "source_v2_job_id": "job-aoi-001"},
        )
    )

    decision = plan_composition_task(
        TaskPlanningRequest(
            task_request=CompositionTaskRequest(
                task="Trace the genealogy and inheritance patterns in this target work.",
            ),
            prior_routing_decision=stale_prior,
            planning_context={
                "context_mode": "inline_documents",
                "thinker_name": "Walter Benjamin",
                "target_work": {
                    "title": "The Arcades Project",
                    "author": "Walter Benjamin",
                    "description": "Target work",
                },
                "target_work_text": "Target text",
                "prior_works": [
                    {
                        "title": "Capital",
                        "author": "Karl Marx",
                        "description": "Prior",
                        "relationship_hint": "influence",
                        "text": "Prior text",
                    }
                ],
            },
        )
    )

    assert decision.planning_outcome_kind == "genealogy_execution_plan"
    reuse_trace = next(entry for entry in decision.trace if entry.stage == "routing_reuse")
    assert reuse_trace.details["status"] == "ignored_due_to_mismatch"


def test_plan_task_generates_by_ref_genealogy_plan(monkeypatch):
    fake_plan = _fake_genealogy_plan("plan-byref-stage9")
    monkeypatch.setattr(
        "src.orchestrator.task_planner.generate_plan_for_by_ref_request",
        lambda _request: (fake_plan, {"target": "doc-target", "Capital": "doc-prior"}),
    )

    decision = plan_composition_task(
        TaskPlanningRequest(
            task_request=CompositionTaskRequest(
                task="Trace the genealogy, lineage, and conditions of possibility behind this work.",
            ),
            planning_context={
                "context_mode": "registered_corpus",
                "consumer_key": "the-critic",
                "external_project_id": "proj-1",
                "thinker_name": "Walter Benjamin",
                "target_work": {
                    "title": "The Arcades Project",
                    "author": "Walter Benjamin",
                    "description": "Target work",
                },
                "target_external_doc_key": "target-doc",
                "prior_works": [
                    {
                        "external_doc_key": "capital-doc",
                        "description": "Prior",
                        "relationship_hint": "influence",
                    }
                ],
            },
        )
    )

    assert decision.planning_outcome_kind == "genealogy_execution_plan"
    assert decision.workflow_execution_plan is not None
    assert decision.workflow_execution_plan.plan_id == "plan-byref-stage9"


def test_plan_task_generates_genealogy_saved_result_direct_sections_handoff(monkeypatch):
    monkeypatch.setattr(
        "src.orchestrator.task_planner.build_genealogy_saved_result_handoff_plan",
        lambda **_kwargs: _fake_genealogy_direct_sections_handoff(),
    )

    decision = plan_composition_task(
        TaskPlanningRequest(
            task_request=CompositionTaskRequest(
                task="Trace the genealogy and intellectual development visible in this saved result.",
                consumer_key="the-critic",
                source_constraints={
                    "source_mode": "saved_result",
                    "source_v2_job_id": "job-genealogy-001",
                },
            ),
            planning_context={
                "context_mode": "saved_result",
                "source_v2_job_id": "job-genealogy-001",
                "consumer_key": "the-critic",
            },
        )
    )

    assert decision.planning_outcome_kind == "direct_sections_composition_handoff_plan"
    assert decision.downstream_readiness == "ready_for_direct_sections_compose_handoff"
    assert decision.direct_sections_composition_handoff_plan is not None
    assert decision.direct_sections_composition_handoff_plan.source_v2_job_id == "job-genealogy-001"
    assert decision.downstream_followup_contract["endpoint"] == "/v1/presenter/compose-from-intent"
    assert decision.required_host_preparation == [
        "Lower the persisted direct-sections handoff into compose-from-intent without host-side semantic reconstruction."
    ]


def test_plan_task_returns_insufficient_for_aoi_without_source_v2_job_id():
    decision = plan_composition_task(
        TaskPlanningRequest(
            task_request=CompositionTaskRequest(
                task="Compose an anxiety of influence dossier about misreading and revision.",
                consumer_key="the-critic",
                source_constraints={"source_mode": "saved_result", "source_analysis_id": "analysis-123"},
            )
        )
    )

    assert decision.planning_outcome_kind == "insufficient_context"
    assert decision.required_hydration == ["source_v2_job_id"]


def test_plan_task_generates_aoi_handoff_plan(monkeypatch):
    monkeypatch.setattr(
        "src.orchestrator.task_planner.resolve_source_catalog",
        lambda **_kwargs: _fake_aoi_catalog(),
    )
    monkeypatch.setattr(
        "src.orchestrator.task_planner._select_aoi_sources_with_llm",
        lambda **_kwargs: _fake_aoi_selection_result(),
    )

    decision = plan_composition_task(
        TaskPlanningRequest(
            task_request=CompositionTaskRequest(
                task="Compose an anxiety of influence dossier about revision and misreading.",
                consumer_key="the-critic",
            ),
            planning_context={
                "context_mode": "saved_result",
                "source_v2_job_id": "job-aoi-001",
                "consumer_key": "the-critic",
            },
        )
    )

    assert decision.planning_outcome_kind == "aoi_composition_handoff_plan"
    assert decision.downstream_readiness == "ready_for_aoi_compose_handoff"
    assert decision.aoi_composition_handoff_plan is not None
    assert decision.aoi_composition_handoff_plan.source_v2_job_id == "job-aoi-001"
    assert decision.aoi_composition_handoff_plan.available_source_families == [
        "thematic_synthesis",
        "engagement_mapping",
        "thematic_report",
    ]
    assert [item.source_family_key for item in decision.aoi_composition_handoff_plan.selected_sources] == [
        "thematic_synthesis",
        "thematic_report",
    ]
    assert decision.aoi_composition_handoff_plan.selection_summary == (
        "Use synthesis plus report for a compact thematic handoff."
    )
    assert decision.aoi_composition_handoff_plan.resolved_intent_seed == (
        "Compose a concise AOI synthesis with a report closeout."
    )
    assert decision.aoi_composition_handoff_plan.legacy_profile_equivalent == "dossier"
    assert decision.aoi_composition_handoff_plan.allowed_profiles == ["dossier"]
    assert decision.aoi_composition_handoff_plan.blocked_profiles == {
        "comparison": ["sin_findings (unavailable)"]
    }
    assert decision.downstream_followup_contract["endpoint"] == "/v1/presenter/compose-from-selection"
    assert decision.downstream_followup_contract["selection_kind"] == "explicit"
    assert decision.required_host_preparation == [
        "Carry planner-selected source families and the resolved intent seed into compose-from-selection."
    ]


def test_plan_task_persists_immutable_planning_snapshot_for_aoi_handoff(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.orchestrator.task_planner.resolve_source_catalog",
        lambda **_kwargs: _fake_aoi_catalog(),
    )
    monkeypatch.setattr(
        "src.orchestrator.task_planner._select_aoi_sources_with_llm",
        lambda **_kwargs: _fake_aoi_selection_result(),
    )
    monkeypatch.setattr(
        "src.orchestrator.planning_decision_store.PLANNING_DECISIONS_DIR",
        tmp_path,
    )

    decision = plan_composition_task(
        TaskPlanningRequest(
            task_request=CompositionTaskRequest(
                task="Compose an anxiety of influence dossier about revision and misreading.",
                consumer_key="the-critic",
            ),
            planning_context={
                "context_mode": "saved_result",
                "source_v2_job_id": "job-aoi-001",
                "consumer_key": "the-critic",
            },
            persist_decision=True,
        )
    )

    assert decision.planning_decision_id is not None
    stored = load_task_planning_decision(decision.planning_decision_id)
    assert stored is not None
    assert stored.planning_decision_id == decision.planning_decision_id
    assert stored.selected_source_thinker_id == "otto_neurath"
    assert stored.selected_source_thinker_name == "Otto Neurath"
    assert stored.source_v2_job_id == "job-aoi-001"
    assert stored.task_request.task == "Compose an anxiety of influence dossier about revision and misreading."
    assert stored.planning_decision.planning_decision_id == decision.planning_decision_id


def test_plan_task_persists_immutable_planning_snapshot_for_genealogy_direct_sections(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.orchestrator.task_planner.build_genealogy_saved_result_handoff_plan",
        lambda **_kwargs: _fake_genealogy_direct_sections_handoff(),
    )
    monkeypatch.setattr(
        "src.orchestrator.planning_decision_store.PLANNING_DECISIONS_DIR",
        tmp_path,
    )

    decision = plan_composition_task(
        TaskPlanningRequest(
            task_request=CompositionTaskRequest(
                task="Trace the genealogy and intellectual development visible in this saved result.",
                consumer_key="the-critic",
                source_constraints={
                    "source_mode": "saved_result",
                    "source_v2_job_id": "job-genealogy-001",
                },
            ),
            planning_context={
                "context_mode": "saved_result",
                "source_v2_job_id": "job-genealogy-001",
                "consumer_key": "the-critic",
            },
            persist_decision=True,
        )
    )

    assert decision.planning_decision_id is not None
    stored = load_task_planning_decision(decision.planning_decision_id)
    assert stored is not None
    assert stored.workflow_key == "intellectual_genealogy"
    assert stored.consumer_key == "the-critic"
    assert stored.source_v2_job_id == "job-genealogy-001"
    assert stored.planning_decision.planning_outcome_kind == "direct_sections_composition_handoff_plan"
    assert stored.planning_decision.direct_sections_composition_handoff_plan is not None


def test_get_planning_decision_route_returns_persisted_snapshot(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.orchestrator.task_planner.resolve_source_catalog",
        lambda **_kwargs: _fake_aoi_catalog(),
    )
    monkeypatch.setattr(
        "src.orchestrator.task_planner._select_aoi_sources_with_llm",
        lambda **_kwargs: _fake_aoi_selection_result(),
    )
    monkeypatch.setattr(
        "src.orchestrator.planning_decision_store.PLANNING_DECISIONS_DIR",
        tmp_path,
    )

    decision = plan_composition_task(
        TaskPlanningRequest(
            task_request=CompositionTaskRequest(
                task="Compose an anxiety of influence dossier about revision and misreading.",
                consumer_key="the-critic",
            ),
            planning_context={
                "context_mode": "saved_result",
                "source_v2_job_id": "job-aoi-001",
                "consumer_key": "the-critic",
            },
            persist_decision=True,
        )
    )

    response = asyncio.run(get_planning_decision_route(decision.planning_decision_id or ""))

    assert response.planning_decision_id == decision.planning_decision_id
    assert response.planning_decision.planning_decision_id == decision.planning_decision_id
    assert response.source_v2_job_id == "job-aoi-001"


def test_plan_task_returns_aoi_selection_blocked_when_no_usable_source_families(monkeypatch):
    partial_catalog = _fake_aoi_catalog()
    partial_catalog = CompositionSourceCatalog(
        source_v2_job_id=partial_catalog.source_v2_job_id,
        workflow_key=partial_catalog.workflow_key,
        objective_key=partial_catalog.objective_key,
        objective_source=partial_catalog.objective_source,
        plan_context_found=partial_catalog.plan_context_found,
        plan_context_source=partial_catalog.plan_context_source,
        selected_source_thinker_id=partial_catalog.selected_source_thinker_id,
        selected_source_thinker_name=partial_catalog.selected_source_thinker_name,
        candidates=[
            CompositionSourceCandidate(
                source_family_key="engagement_mapping",
                engine_key="aoi_engagement_mapping",
                title="Engagement Mapping",
                source_backend_kind="artifact",
                candidate_state="unavailable",
                provenance_pointer={"job_id": "job-aoi-001"},
                composition_role_hint="comparison_map",
                summary_metadata={"payload_kind": "normalized_artifact"},
                plan_context_enrichment={"plan_context_found": True},
                resolution_note="Missing",
                materialization_payload=None,
            ),
            CompositionSourceCandidate(
                source_family_key="sin_findings",
                engine_key="aoi_sin_findings",
                title="Sin Findings",
                source_backend_kind="artifact",
                candidate_state="unavailable",
                provenance_pointer={"job_id": "job-aoi-001"},
                composition_role_hint="findings_bank",
                summary_metadata={"payload_kind": "normalized_artifact"},
                plan_context_enrichment={"plan_context_found": True},
                resolution_note="Missing",
                materialization_payload=None,
            ),
            CompositionSourceCandidate(
                source_family_key="thematic_report",
                engine_key="aoi_thematic_report",
                title="AOI Report",
                source_backend_kind="phase_output_metadata",
                candidate_state="unavailable",
                provenance_pointer={"job_id": "job-aoi-001"},
                composition_role_hint="report_closeout",
                summary_metadata={"payload_kind": "report_sections"},
                plan_context_enrichment={"plan_context_found": True},
                resolution_note="Missing",
                materialization_payload=None,
            ),
        ],
    )
    monkeypatch.setattr(
        "src.orchestrator.task_planner.resolve_source_catalog",
        lambda **_kwargs: partial_catalog,
    )

    decision = plan_composition_task(
        TaskPlanningRequest(
            task_request=CompositionTaskRequest(
                task="Compose an anxiety of influence dossier about revision and misreading.",
                consumer_key="the-critic",
            ),
            planning_context={
                "context_mode": "saved_result",
                "source_v2_job_id": "job-aoi-001",
                "consumer_key": "the-critic",
            },
        )
    )

    assert decision.planning_outcome_kind == "aoi_selection_blocked"
    assert decision.aoi_selection_blocked_reason_code == "no_usable_source_families"
    assert decision.downstream_readiness == "blocked_for_aoi_selection"
    source_selection_trace = next(entry for entry in decision.trace if entry.stage == "source_selection")
    assert source_selection_trace.details["prompt_version"] == task_planner_module.AOI_SELECTION_PROMPT_VERSION
    assert source_selection_trace.details["provider_outcome"] == "skipped_no_usable_source_families"
    assert source_selection_trace.details["validator_version"] == task_planner_module.AOI_SELECTION_VALIDATOR_VERSION


def test_plan_task_returns_aoi_selection_blocked_for_provider_failure(monkeypatch):
    monkeypatch.setattr(
        "src.orchestrator.task_planner.resolve_source_catalog",
        lambda **_kwargs: _fake_aoi_catalog(),
    )

    def _raise_provider_failure(**_kwargs):
        raise task_planner_module._AoiSelectionBlocked(
            "llm_provider_failure",
            "Provider returned a 5xx.",
        )

    monkeypatch.setattr(
        "src.orchestrator.task_planner._select_aoi_sources_with_llm",
        _raise_provider_failure,
    )

    decision = plan_composition_task(
        TaskPlanningRequest(
            task_request=CompositionTaskRequest(
                task="Compose an anxiety of influence dossier about revision and misreading.",
                consumer_key="the-critic",
            ),
            planning_context={
                "context_mode": "saved_result",
                "source_v2_job_id": "job-aoi-001",
                "consumer_key": "the-critic",
            },
        )
    )

    assert decision.planning_outcome_kind == "aoi_selection_blocked"
    assert decision.aoi_selection_blocked_reason_code == "llm_provider_failure"
    assert decision.aoi_selection_blocked_reason_detail == "Provider returned a 5xx."
    source_selection_trace = next(entry for entry in decision.trace if entry.stage == "source_selection")
    assert source_selection_trace.details["prompt_version"] == task_planner_module.AOI_SELECTION_PROMPT_VERSION
    assert source_selection_trace.details["provider_outcome"] == "llm_provider_failure"
    assert source_selection_trace.details["blocked_reason_code"] == "llm_provider_failure"


def test_call_aoi_selection_llm_uses_env_timeout_and_no_retries(monkeypatch):
    captured: dict[str, object] = {}

    class _FakeMessages:
        def create(self, **kwargs):
            captured["create_kwargs"] = kwargs
            return type("Response", (), {"content": [type("Block", (), {"text": '{"ok": true}'})()]})()

    class _FakeClient:
        messages = _FakeMessages()

    monkeypatch.setenv("AOI_SELECTION_TIMEOUT_S", "12.5")

    def _fake_get_client(*, read_timeout_s: float, max_retries: int):
        captured["read_timeout_s"] = read_timeout_s
        captured["max_retries"] = max_retries
        return _FakeClient()

    monkeypatch.setattr("src.orchestrator.task_planner.get_anthropic_client", _fake_get_client)

    raw_text, model_used = task_planner_module._call_aoi_selection_llm("Select AOI sources.")

    assert raw_text == '{"ok": true}'
    assert model_used == task_planner_module.AOI_SELECTION_MODEL
    assert captured["read_timeout_s"] == 12.5
    assert captured["max_retries"] == 0
    assert captured["create_kwargs"]["model"] == task_planner_module.AOI_SELECTION_MODEL


def test_call_aoi_selection_llm_maps_api_timeout_to_llm_timeout(monkeypatch):
    class _FakeMessages:
        def create(self, **_kwargs):
            raise anthropic.APITimeoutError(request=None)

    class _FakeClient:
        messages = _FakeMessages()

    monkeypatch.setenv("AOI_SELECTION_TIMEOUT_S", "12.5")
    monkeypatch.setattr(
        "src.orchestrator.task_planner.get_anthropic_client",
        lambda **_kwargs: _FakeClient(),
    )

    with pytest.raises(task_planner_module._AoiSelectionBlocked) as exc_info:
        task_planner_module._call_aoi_selection_llm("Select AOI sources.")

    assert exc_info.value.reason_code == "llm_timeout"
    assert exc_info.value.trace_details["blocked_reason_code"] == "llm_timeout"
    assert exc_info.value.trace_details["exception_class_name"] == "APITimeoutError"
    assert exc_info.value.trace_details["timeout_s"] == 12.5
    assert exc_info.value.trace_details["retry_policy"] == {"max_retries": 0}


def test_call_aoi_selection_llm_maps_api_connection_error_to_provider_failure(monkeypatch):
    class _FakeMessages:
        def create(self, **_kwargs):
            raise anthropic.APIConnectionError(message="provider socket closed", request=None)

    class _FakeClient:
        messages = _FakeMessages()

    monkeypatch.setenv("AOI_SELECTION_TIMEOUT_S", "12.5")
    monkeypatch.setattr(
        "src.orchestrator.task_planner.get_anthropic_client",
        lambda **_kwargs: _FakeClient(),
    )

    with pytest.raises(task_planner_module._AoiSelectionBlocked) as exc_info:
        task_planner_module._call_aoi_selection_llm("Select AOI sources.")

    assert exc_info.value.reason_code == "llm_provider_failure"
    assert exc_info.value.trace_details["blocked_reason_code"] == "llm_provider_failure"
    assert exc_info.value.trace_details["exception_class_name"] == "APIConnectionError"
    assert exc_info.value.trace_details["timeout_s"] == 12.5
    assert exc_info.value.trace_details["retry_policy"] == {"max_retries": 0}


def test_select_aoi_sources_with_llm_rejects_incomplete_rejected_source_coverage(monkeypatch):
    available_candidates = [
        CompositionSourceCandidate(
            source_family_key="thematic_synthesis",
            engine_key="aoi_thematic_synthesis",
            title="Thematic Synthesis",
            source_backend_kind="artifact",
            candidate_state="available",
            provenance_pointer={"job_id": "job-aoi-001"},
            composition_role_hint="synthesis_primary",
            summary_metadata={"payload_kind": "normalized_artifact"},
            plan_context_enrichment={"plan_context_found": True},
            resolution_note="Loaded",
            materialization_payload={"summary": "ok"},
        ),
        CompositionSourceCandidate(
            source_family_key="engagement_mapping",
            engine_key="aoi_engagement_mapping",
            title="Engagement Mapping",
            source_backend_kind="artifact",
            candidate_state="available",
            provenance_pointer={"job_id": "job-aoi-001"},
            composition_role_hint="comparison_map",
            summary_metadata={"payload_kind": "normalized_artifact"},
            plan_context_enrichment={"plan_context_found": True},
            resolution_note="Loaded",
            materialization_payload={"summary": "ok"},
        ),
        CompositionSourceCandidate(
            source_family_key="thematic_report",
            engine_key="aoi_thematic_report",
            title="AOI Report",
            source_backend_kind="phase_output_metadata",
            candidate_state="available",
            provenance_pointer={"job_id": "job-aoi-001"},
            composition_role_hint="report_closeout",
            summary_metadata={"payload_kind": "report_sections"},
            plan_context_enrichment={"plan_context_found": True},
            resolution_note="Loaded",
            materialization_payload={"sections": []},
        ),
    ]
    monkeypatch.setattr(
        "src.orchestrator.task_planner._call_aoi_selection_llm",
        lambda _prompt: (
            json.dumps(
                {
                    "selected_sources": [
                        {
                            "source_family_key": "thematic_synthesis",
                            "selection_rank": 1,
                            "rationale": "Lead with synthesis.",
                        }
                    ],
                    "rejected_sources": [
                        {
                            "source_family_key": "thematic_report",
                            "rejection_reason": "Not needed for this task.",
                        }
                    ],
                    "selection_summary": "Use the synthesis only.",
                    "resolved_intent_seed": "Compose a synthesis-led AOI page.",
                }
            ),
            "stub-model",
        ),
    )

    with pytest.raises(task_planner_module._AoiSelectionBlocked) as exc_info:
        task_planner_module._select_aoi_sources_with_llm(
            normalized_task_summary="Compose an anxiety of influence page about revision and misreading.",
            effective_task_request=CompositionTaskRequest(
                task="Compose an anxiety of influence page about revision and misreading.",
                consumer_key="the-critic",
            ),
            source_v2_job_id="job-aoi-001",
            available_candidates=available_candidates,
            expected_source_families=[candidate.source_family_key for candidate in available_candidates],
        )

    assert exc_info.value.reason_code == "llm_selection_failed_validation"
    assert "rejected_sources coverage mismatch" in exc_info.value.detail
    assert exc_info.value.trace_details["provider_outcome"] == "llm_selection_failed_validation"


def test_select_aoi_sources_with_llm_rejects_blank_rejection_reason(monkeypatch):
    available_candidates = [
        CompositionSourceCandidate(
            source_family_key="thematic_synthesis",
            engine_key="aoi_thematic_synthesis",
            title="Thematic Synthesis",
            source_backend_kind="artifact",
            candidate_state="available",
            provenance_pointer={"job_id": "job-aoi-001"},
            composition_role_hint="synthesis_primary",
            summary_metadata={"payload_kind": "normalized_artifact"},
            plan_context_enrichment={"plan_context_found": True},
            resolution_note="Loaded",
            materialization_payload={"summary": "ok"},
        ),
        CompositionSourceCandidate(
            source_family_key="thematic_report",
            engine_key="aoi_thematic_report",
            title="AOI Report",
            source_backend_kind="phase_output_metadata",
            candidate_state="available",
            provenance_pointer={"job_id": "job-aoi-001"},
            composition_role_hint="report_closeout",
            summary_metadata={"payload_kind": "report_sections"},
            plan_context_enrichment={"plan_context_found": True},
            resolution_note="Loaded",
            materialization_payload={"sections": []},
        ),
    ]
    monkeypatch.setattr(
        "src.orchestrator.task_planner._call_aoi_selection_llm",
        lambda _prompt: (
            json.dumps(
                {
                    "selected_sources": [
                        {
                            "source_family_key": "thematic_synthesis",
                            "selection_rank": 1,
                            "rationale": "Lead with synthesis.",
                        }
                    ],
                    "rejected_sources": [
                        {
                            "source_family_key": "thematic_report",
                            "rejection_reason": "   ",
                        }
                    ],
                    "selection_summary": "Use the synthesis only.",
                    "resolved_intent_seed": "Compose a synthesis-led AOI page.",
                }
            ),
            "stub-model",
        ),
    )

    with pytest.raises(task_planner_module._AoiSelectionBlocked) as exc_info:
        task_planner_module._select_aoi_sources_with_llm(
            normalized_task_summary="Compose an anxiety of influence page about revision and misreading.",
            effective_task_request=CompositionTaskRequest(
                task="Compose an anxiety of influence page about revision and misreading.",
                consumer_key="the-critic",
            ),
            source_v2_job_id="job-aoi-001",
            available_candidates=available_candidates,
            expected_source_families=[candidate.source_family_key for candidate in available_candidates],
        )

    assert exc_info.value.reason_code == "llm_selection_failed_validation"
    assert "invalid selection items" in exc_info.value.detail


def test_plan_task_route_maps_aoi_resolution_conflict_to_409(monkeypatch):
    empty_catalog = _fake_aoi_catalog()
    empty_catalog = CompositionSourceCatalog(
        source_v2_job_id=empty_catalog.source_v2_job_id,
        workflow_key=empty_catalog.workflow_key,
        objective_key=empty_catalog.objective_key,
        objective_source=empty_catalog.objective_source,
        plan_context_found=empty_catalog.plan_context_found,
        plan_context_source=empty_catalog.plan_context_source,
        selected_source_thinker_id=empty_catalog.selected_source_thinker_id,
        selected_source_thinker_name=empty_catalog.selected_source_thinker_name,
        candidates=[
            CompositionSourceCandidate(
                source_family_key="thematic_synthesis",
                engine_key="aoi_thematic_synthesis",
                title="Thematic Synthesis",
                source_backend_kind="artifact",
                candidate_state="unavailable",
                provenance_pointer={"job_id": "job-aoi-001"},
                composition_role_hint="synthesis_primary",
                summary_metadata={},
                plan_context_enrichment={"plan_context_found": True},
                resolution_note="Missing",
                materialization_payload=None,
            )
        ],
    )
    monkeypatch.setattr(
        "src.orchestrator.task_planner.resolve_source_catalog",
        lambda **_kwargs: empty_catalog,
    )

    response = asyncio.run(plan_task_route(
        TaskPlanningRequest(
            task_request=CompositionTaskRequest(
                task="Compose an anxiety of influence dossier about revision and misreading.",
                consumer_key="the-critic",
            ),
            planning_context={
                "context_mode": "saved_result",
                "source_v2_job_id": "job-aoi-001",
                "consumer_key": "the-critic",
            },
        )
    ))

    assert response.planning_outcome_kind == "aoi_selection_blocked"
    assert response.aoi_selection_blocked_reason_code == "no_usable_source_families"
