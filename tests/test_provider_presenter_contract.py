import asyncio
from types import SimpleNamespace
from unittest.mock import patch

from src.api.routes.presenter import (
    get_page_presentation,
    get_presentation_manifest,
    get_presentation_trace,
)
from src.presenter.schemas import ViewPayload


COMPLETED_GENEALOGY_FIXTURE_JOB_ID = "job-varoufakis-style-completed"


def _completed_genealogy_page_inputs() -> dict[str, object]:
    payload = ViewPayload(
        view_key="genealogy_tp_inferential_commitments",
        view_name="Inferential Commitments",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "commitments"}]},
        presentation_stance="diagnostic",
        priority="primary",
        rationale="Recover the commitments underlying the target's capitalism thesis.",
        data_quality="rich",
        selection_priority="primary",
        navigation_state="normal",
        phase_number=1.0,
        engine_key="inferential_commitment_mapper",
        scope="aggregated",
        has_structured_data=True,
        structured_data={
            "commitments": [
                {
                    "commitment": "Political relations determine the rate of return on investment.",
                    "epistemic_status": "provisional",
                }
            ]
        },
        visibility="if_data_exists",
        position=1.0,
    )
    return {
        "payloads": {payload.view_key: payload},
        "top_level": [payload],
        "job": {
            "job_id": COMPLETED_GENEALOGY_FIXTURE_JOB_ID,
            "plan_id": "plan-varoufakis-style",
            "status": "completed",
            "workflow_key": "intellectual_genealogy",
            "created_at": "2026-08-11T00:00:00Z",
        },
        "plan_id": "plan-varoufakis-style",
        "plan": None,
        "workflow_key": "intellectual_genealogy",
        "thinker_name": "Yanis Varoufakis",
        "strategy_summary": "Recover the genealogy and logical commitments of the target thesis.",
        "all_outputs": [],
    }


def test_completed_genealogy_fixture_serves_page_manifest_and_trace_routes():
    page_inputs = _completed_genealogy_page_inputs()
    payload = page_inputs["top_level"][0]
    view_def = SimpleNamespace(
        view_key=payload.view_key,
        view_name=payload.view_name,
        description=payload.description,
        renderer_type=payload.renderer_type,
        renderer_config=payload.renderer_config,
        presentation_stance=payload.presentation_stance,
        visibility=payload.visibility,
        position=payload.position,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=payload.phase_number,
            engine_key=payload.engine_key,
            chain_key=None,
            scope=payload.scope,
            result_path="",
        ),
    )
    registry = SimpleNamespace(
        get=lambda key: view_def if key == view_def.view_key else None,
        list_all=lambda: [],
    )
    recommendation = {
        "view_key": payload.view_key,
        "priority": "primary",
        "rationale": payload.rationale,
    }
    composition = SimpleNamespace(
        renderer_type=payload.renderer_type,
        renderer_config=payload.renderer_config,
        presentation_stance=payload.presentation_stance,
        data_quality=payload.data_quality,
        dropped_overrides=[],
        template_selection_reason=None,
    )

    with patch(
        "src.presenter.presentation_api._prepare_page_payloads",
        return_value=page_inputs,
    ), patch(
        "src.presenter.presentation_api._attach_reading_scaffolds",
        return_value=None,
    ), patch(
        "src.presenter.presentation_api._resolve_page_style_school",
        return_value="explanatory_narrative",
    ), patch(
        "src.presenter.presentation_api.apply_cached_polish_to_views",
        side_effect=lambda **kwargs: (kwargs["views"], "raw"),
    ), patch(
        "src.presenter.presentation_api.load_view_refinement",
        return_value=None,
    ), patch(
        "src.presenter.manifest_builder.resolve_scaffold_type",
        return_value="none",
    ), patch(
        "src.presenter.decision_trace.get_job",
        return_value=page_inputs["job"],
    ), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value="intellectual_genealogy",
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=registry,
    ), patch(
        "src.presenter.decision_trace.resolve_effective_composition",
        return_value=composition,
    ), patch(
        "src.presenter.decision_trace.resolve_effective_render_contract",
        return_value=composition,
    ), patch(
        "src.presenter.decision_trace.load_selected_variants",
        return_value=[],
    ):
        page = asyncio.run(
            get_page_presentation(
                COMPLETED_GENEALOGY_FIXTURE_JOB_ID,
                slim=True,
                consumer_key="the-critic",
                composition_mode=None,
            )
        )
        manifest = asyncio.run(
            get_presentation_manifest(
                COMPLETED_GENEALOGY_FIXTURE_JOB_ID,
                consumer_key="the-critic",
                slim=True,
                composition_mode=None,
            )
        )
        trace = asyncio.run(
            get_presentation_trace(
                COMPLETED_GENEALOGY_FIXTURE_JOB_ID,
                consumer_key="the-critic",
                composition_mode=None,
            )
        )

    assert page["job_id"] == COMPLETED_GENEALOGY_FIXTURE_JOB_ID
    assert page["consumer_key"] == "the-critic"
    assert page["presentation_contract_version"] == 1
    assert page["views"][0]["view_key"] == payload.view_key

    assert manifest.job_id == COMPLETED_GENEALOGY_FIXTURE_JOB_ID
    assert manifest.consumer_key == "the-critic"
    assert manifest.presentation_contract_version == 1
    assert manifest.views[0].view_key == payload.view_key

    assert trace.job_id == COMPLETED_GENEALOGY_FIXTURE_JOB_ID
    assert trace.consumer_key == "the-critic"
    assert trace.composition_status == "not_requested"
    assert trace.final_manifest.consumer_key == "the-critic"
