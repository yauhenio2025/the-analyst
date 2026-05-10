import asyncio

import pytest
from fastapi import HTTPException

from src.api.routes.orchestrator import (
    get_planning_decision_compose_from_intent_request as get_planning_decision_compose_request_route,
    get_planning_decision as get_planning_decision_route,
    plan_task as plan_task_route,
    route_task as route_task_route,
)
from src.api.routes.presenter import compose_from_intent_endpoint
from src.orchestrator.direct_sections_compose_harness import (
    DirectSectionsLoweringError,
)
from src.orchestrator.task_planning_schemas import (
    DirectSectionsCompositionHandoffPlan,
    TaskPlanningRequest,
)
from src.orchestrator.task_routing_schemas import CompositionTaskRequest
from src.views.schemas import DataSourceRef, TransformationSpec, ViewDefinition


def _raw_view(*, engine_key: str, renderer_type: str) -> ViewDefinition:
    return ViewDefinition(
        view_key="raw_generated_key",
        view_name="Raw View",
        description="Raw description",
        target_app="other-app",
        target_page="wrong_page",
        renderer_type=renderer_type,
        renderer_config={
            "show_section_nav": False
        } if renderer_type == "prose" else {},
        data_source=DataSourceRef(
            workflow_key="intellectual_genealogy",
            phase_number=1.0,
            engine_key=engine_key,
            result_path="",
            scope="aggregated",
        ),
        transformation=TransformationSpec(type="none"),
        presentation_stance="diagnostic",
        position=1.0,
        parent_view_key=None,
        visibility="always",
        status="active",
        generation_mode="generated",
    )


def test_genealogy_saved_result_direct_sections_chain_executes_end_to_end(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.orchestrator.planning_decision_store.PLANNING_DECISIONS_DIR",
        tmp_path,
    )
    monkeypatch.setattr(
        "src.orchestrator.task_planner.build_genealogy_saved_result_handoff_plan",
        lambda **_kwargs: DirectSectionsCompositionHandoffPlan.model_validate(
            {
                "workflow_key": "intellectual_genealogy",
                "objective_key": "genealogical",
                "consumer_key": "the-critic",
                "source_v2_job_id": "job-genealogy-001",
                "compose_entrypoint_kind": "presenter.compose_from_intent",
                "resolved_intent_seed": "Compose a concise genealogy briefing from the saved result.",
                "prose_sections": [
                    {
                        "engine_key": "genealogy_relationship_classification",
                        "title": "Relationship Comparison Map",
                        "prose": "Comparison prose.",
                    },
                    {
                        "engine_key": "genealogy_final_synthesis",
                        "title": "Genealogy Report",
                        "prose": "Closeout prose.",
                    },
                ],
                "section_trace": [
                    {
                        "order": 1,
                        "engine_key": "genealogy_relationship_classification",
                        "title": "Relationship Comparison Map",
                        "provenance_pointer": {"job_id": "job-genealogy-001", "output_id": "po-1"},
                        "role_hint": "comparison_map",
                        "rationale": "Relationship comparison section.",
                    },
                    {
                        "order": 2,
                        "engine_key": "genealogy_final_synthesis",
                        "title": "Genealogy Report",
                        "provenance_pointer": {"job_id": "job-genealogy-001", "output_id": "po-2"},
                        "role_hint": "report_closeout",
                        "rationale": "Final synthesis section.",
                    },
                ],
                "handoff_notes": ["Derived from analyzer-owned saved-result truth."],
            }
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent._generate_view_definition",
        lambda planner_row, section, planner_position, consumer_key, workflow_key: _raw_view(
            engine_key=section.engine_key,
            renderer_type="card_grid" if planner_row.pattern_key == "card_grid_grouped" else "prose",
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent._transform_section_prose",
        lambda section, view_def, planner_row, executor: (
            {"items": [{"title": section.title}]}
            if view_def.renderer_type == "card_grid"
            else section.prose,
            {
                "view_key": view_def.view_key,
                "engine_key": section.engine_key,
                "renderer_type": view_def.renderer_type,
                "extraction_source": "stub",
                "template_key": None,
            },
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent.enforce_final_payload_contracts_or_raise",
        lambda *args, **kwargs: [],
    )

    routed = asyncio.run(
        route_task_route(
            CompositionTaskRequest(
                task="Trace the genealogy and intellectual development visible in this saved result.",
                consumer_key="the-critic",
                source_constraints={
                    "source_mode": "saved_result",
                    "source_v2_job_id": "job-genealogy-001",
                },
            )
        )
    )
    assert routed.routing_outcome == "genealogy_transient_source_backed"

    planned = asyncio.run(
        plan_task_route(
            TaskPlanningRequest(
                task_request=CompositionTaskRequest(
                    task="Trace the genealogy and intellectual development visible in this saved result.",
                    consumer_key="the-critic",
                    source_constraints={
                        "source_mode": "saved_result",
                        "source_v2_job_id": "job-genealogy-001",
                    },
                ),
                prior_routing_decision=routed,
                planning_context={
                    "context_mode": "saved_result",
                    "source_v2_job_id": "job-genealogy-001",
                    "consumer_key": "the-critic",
                },
                persist_decision=True,
            )
        )
    )
    assert planned.planning_outcome_kind == "direct_sections_composition_handoff_plan"
    assert planned.planning_decision_id is not None

    snapshot = asyncio.run(get_planning_decision_route(planned.planning_decision_id or ""))
    lowered = asyncio.run(
        get_planning_decision_compose_request_route(
            snapshot.planning_decision_id,
            consumer_key="the-critic",
        )
    )
    response = asyncio.run(compose_from_intent_endpoint(lowered.model_dump(mode="python")))

    assert response.presentation.workflow_key == "intellectual_genealogy"
    assert response.presentation.view_count == 3
    assert response.presentation.views[0].view_name == "Analytical Comparison"
    assert lowered.consumer_key == "the-critic"


def test_lowered_compose_request_route_returns_404_for_unknown_planning_decision() -> None:
    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(
            get_planning_decision_compose_request_route(
                "planning-decision-missing",
                consumer_key="the-critic",
            )
        )

    assert excinfo.value.status_code == 404


def test_lowered_compose_request_route_returns_409_when_lowering_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "src.api.routes.orchestrator.load_task_planning_decision",
        lambda _planning_decision_id: object(),
    )
    monkeypatch.setattr(
        "src.api.routes.orchestrator.lower_persisted_planning_snapshot",
        lambda _snapshot: (_ for _ in ()).throw(
            DirectSectionsLoweringError("Cannot lower persisted snapshot.")
        ),
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(
            get_planning_decision_compose_request_route(
                "planning-decision-123",
                consumer_key="the-critic",
            )
        )

    assert excinfo.value.status_code == 409


def test_lowered_compose_request_route_returns_409_for_consumer_mismatch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "src.api.routes.orchestrator.load_task_planning_decision",
        lambda _planning_decision_id: object(),
    )
    monkeypatch.setattr(
        "src.api.routes.orchestrator.lower_persisted_planning_snapshot",
        lambda _snapshot: type(
            "LoweredComposeRequest",
            (),
            {"consumer_key": "the-critic"},
        )(),
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(
            get_planning_decision_compose_request_route(
                "planning-decision-123",
                consumer_key="other-consumer",
            )
        )

    assert excinfo.value.status_code == 409
