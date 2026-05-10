from __future__ import annotations

import asyncio
import logging
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from src.aoi.constants import AOI_WORKFLOW_KEY
from src.api.routes.presenter import compose_presentation
from src.presenter.bounded_dynamic_composition import (
    BoundedCompositionValidationError,
    COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
    COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
    COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
    get_supported_composition_modes_for_workflow,
)
from src.presenter.renderer_contract_enforcement import (
    ServedIntent,
    enforce_final_payload_contracts_or_raise,
    resolve_served_renderer_contract_policy,
)
from src.presenter.schemas import ComposeRequest, CompositionIssue, ViewPayload


GENEALOGY_WORKFLOW_KEY = "intellectual_genealogy"


def _payload(
    *,
    view_key: str = "genealogy_tp_inferential_commitments",
    renderer_type: str = "accordion",
    structured_data: object = None,
    renderer_config: dict[str, object] | None = None,
    children: list[ViewPayload] | None = None,
) -> ViewPayload:
    return ViewPayload(
        view_key=view_key,
        view_name=view_key,
        description="payload",
        renderer_type=renderer_type,
        renderer_config=renderer_config or {},
        presentation_stance="diagnostic",
        priority="primary",
        rationale="because",
        data_quality="generated",
        top_level_group=None,
        source_parent_view_key=None,
        promoted_to_top_level=False,
        selection_priority="primary",
        navigation_state="normal",
        structuring_policy=None,
        semantic_scaffold_type=None,
        scaffold_hosting_mode=None,
        derivation_kind="stage12_test",
        phase_number=1.0,
        engine_key="inferential_commitment_mapper",
        chain_key=None,
        scope="aggregated",
        has_structured_data=structured_data is not None,
        structured_data=structured_data,
        reading_scaffold=None,
        raw_prose=None,
        prose_ref_view_key=None,
        items=None,
        tab_count=None,
        visibility="if_data_exists",
        position=1.0,
        children=children or [],
    )


def test_served_intent_enum_is_fully_enumerated() -> None:
    assert {intent.value for intent in ServedIntent} == {
        "transient_compose_output",
        "effective_manifest_served",
        "full_page_presentation_served",
        "single_view_presentation_served",
        "manifest_inspection_for_status",
        "manifest_inspection_for_trace",
        "manifest_preview_for_discovery",
        "view_source_for_polish",
        "page_source_for_delivery_style",
        "view_source_for_delivery_style",
        "page_source_for_scaffold_generation",
        "view_source_for_variant_generation",
        "page_preview_for_orchestrator_status",
    }


def test_policy_resolver_distinguishes_strict_shadow_and_warn_modes() -> None:
    assert resolve_served_renderer_contract_policy(
        served_intent=ServedIntent.TRANSIENT_COMPOSE_OUTPUT,
        workflow_key=AOI_WORKFLOW_KEY,
        consumer_key="the-critic",
        composition_mode=None,
    ).mode == "strict"
    assert resolve_served_renderer_contract_policy(
        served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
        workflow_key=GENEALOGY_WORKFLOW_KEY,
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
    ).mode == "shadow"
    assert resolve_served_renderer_contract_policy(
        served_intent=ServedIntent.MANIFEST_INSPECTION_FOR_TRACE,
        workflow_key=GENEALOGY_WORKFLOW_KEY,
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
    ).mode == "warn"


@pytest.mark.parametrize(
    "served_intent",
    [
        ServedIntent.EFFECTIVE_MANIFEST_SERVED,
        ServedIntent.FULL_PAGE_PRESENTATION_SERVED,
        ServedIntent.SINGLE_VIEW_PRESENTATION_SERVED,
    ],
)
def test_registered_runtime_modes_do_not_silently_fall_back_to_warn(served_intent: ServedIntent) -> None:
    for composition_mode in get_supported_composition_modes_for_workflow(AOI_WORKFLOW_KEY):
        policy = resolve_served_renderer_contract_policy(
            served_intent=served_intent,
            workflow_key=AOI_WORKFLOW_KEY,
            consumer_key="the-critic",
            composition_mode=composition_mode,
        )
        assert policy.mode == "strict"

    for composition_mode in get_supported_composition_modes_for_workflow(GENEALOGY_WORKFLOW_KEY):
        policy = resolve_served_renderer_contract_policy(
            served_intent=served_intent,
            workflow_key=GENEALOGY_WORKFLOW_KEY,
            consumer_key="the-critic",
            composition_mode=composition_mode,
        )
        assert policy.mode in {"strict", "shadow"}


def test_genealogy_served_manifest_fails_closed_for_strict_mode() -> None:
    payload = _payload(renderer_type="mini_card_list", structured_data={"summary": "bad renderer"})

    with pytest.raises(BoundedCompositionValidationError) as excinfo:
        enforce_final_payload_contracts_or_raise(
            [payload],
            composition_mode=COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            workflow_key=GENEALOGY_WORKFLOW_KEY,
            consumer_key="the-critic",
        )

    assert excinfo.value.issues[0].reason == "renderer_definition_missing"


def test_genealogy_served_manifest_runs_shadow_validation_without_raising(
    caplog: pytest.LogCaptureFixture,
) -> None:
    payload = _payload(renderer_type="mini_card_list", structured_data={"summary": "bad renderer"})

    with caplog.at_level(logging.WARNING):
        issues = enforce_final_payload_contracts_or_raise(
            [payload],
            composition_mode=COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            workflow_key=GENEALOGY_WORKFLOW_KEY,
            consumer_key="the-critic",
        )

    assert issues
    assert issues[0].reason == "renderer_definition_missing"
    assert "served_renderer_contract_shadow_issues" in caplog.text


def test_transient_tab_alignment_is_strictly_validated() -> None:
    child = _payload(
        view_key="compose_intent_01_aoi_thematic_report",
        renderer_type="prose",
        structured_data="Narrative closeout",
        renderer_config={},
    )
    parent = _payload(
        view_key="compose_intent_parent_aoi_briefing",
        renderer_type="tab",
        structured_data={"wrong_child": {"label": "Wrong"}},
        renderer_config={},
        children=[child],
    )

    with pytest.raises(BoundedCompositionValidationError) as excinfo:
        enforce_final_payload_contracts_or_raise(
            [parent],
            composition_mode=None,
            served_intent=ServedIntent.TRANSIENT_COMPOSE_OUTPUT,
            workflow_key=AOI_WORKFLOW_KEY,
            consumer_key="the-critic",
        )

    assert excinfo.value.issues[0].reason == "tab_child_alignment_mismatch"


def test_get_presentation_status_uses_non_strict_status_intent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from src.presenter.presentation_api import get_presentation_status

    captured: dict[str, object] = {}
    payload = _payload(structured_data={"summary": "Ready"})
    fake_registry = SimpleNamespace(
        get=lambda key: SimpleNamespace(
            view_key="genealogy_tp_inferential_commitments",
            data_source=SimpleNamespace(phase_number=1.0, engine_key="inferential_commitment_mapper", chain_key=None, scope="aggregated", result_path=""),
            parent_view_key=None,
        ),
    )

    monkeypatch.setattr(
        "src.presenter.presentation_api.get_job",
        lambda job_id: {"job_id": job_id, "plan_id": "plan-1", "workflow_key": GENEALOGY_WORKFLOW_KEY},
    )
    monkeypatch.setattr(
        "src.presenter.presentation_api._prepare_page_payloads",
        lambda job_id, consumer_key, slim=True: {
            "payloads": {payload.view_key: payload},
            "plan_id": "plan-1",
            "thinker_name": "Markus",
            "strategy_summary": "summary",
            "all_outputs": [],
            "composition_mode": None,
        },
    )
    monkeypatch.setattr("src.presenter.presentation_api._attach_reading_scaffolds", lambda job_id, payloads: None)

    def _build_manifest(**kwargs):
        captured["served_intent"] = kwargs["served_intent"]
        raise RuntimeError("stop_after_manifest")

    monkeypatch.setattr("src.presenter.presentation_api.build_effective_manifest", _build_manifest)
    monkeypatch.setattr("src.presenter.presentation_api.get_view_registry", lambda: fake_registry)

    with pytest.raises(RuntimeError, match="stop_after_manifest"):
        get_presentation_status("job-1", consumer_key="the-critic")

    assert captured["served_intent"] == ServedIntent.MANIFEST_INSPECTION_FOR_STATUS


def test_compose_route_maps_renderer_contract_failure_to_409(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    issue = CompositionIssue(
        view_key="genealogy_relationship_landscape",
        field="renderer_config",
        message="bad config",
        reason="renderer_config_validation_failed",
    )

    monkeypatch.setattr(
        "src.presenter.preparation_coordinator.run_presentation_pipeline_sync",
        lambda *args, **kwargs: {"status": "completed", "stats": {}},
    )
    monkeypatch.setattr(
        "src.presenter.presentation_api.assemble_page",
        lambda *args, **kwargs: (_ for _ in ()).throw(BoundedCompositionValidationError([issue])),
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(
            compose_presentation(
                ComposeRequest(
                    job_id="job-1",
                    plan_id="plan-1",
                    consumer_key="the-critic",
                )
            )
        )

    assert excinfo.value.status_code == 409
    assert excinfo.value.detail == {
        "detail": "bounded_dynamic_composition_validation_failed",
        "issues": [issue.model_dump()],
    }
