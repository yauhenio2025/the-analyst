from __future__ import annotations

from types import SimpleNamespace

import httpx
import pytest
from fastapi import HTTPException

from src.aoi.constants import AOI_WORKFLOW_KEY
from src.presenter.bounded_dynamic_composition import BoundedCompositionValidationError
from src.presenter.compose_from_intent import (
    ComposeFromIntentClientError,
    ComposeFromIntentDependencyUnavailable,
    ComposeFromIntentUpstreamError,
    ComposeFromSourceResolutionError,
    TRANSIENT_COMPOSE_SELECTION_RESOLVER_VERSION,
    TRANSIENT_COMPOSE_RESOLVER_VERSION,
    TRANSIENT_COMPOSE_SOURCE_RESOLVER_VERSION,
    TRANSIENT_COMPOSE_TARGET_PAGE,
    _REGISTERED_TRANSIENT_CONSUMER_ADAPTERS,
    _REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER,
    _PlannerRow,
    _PlannerSectionContext,
    _adapt_payloads_for_consumer,
    _build_dynamic_transient_config,
    _build_transient_presentation,
    _handoff_supports_first_hop_affordance,
    _to_transient_view,
    _generate_view_definition,
    _match_section_to_planner_row,
    _normalize_card_grid_contract_shape,
    _normalize_transient_served_payloads,
    _validate_request,
    compose_from_intent,
    compose_from_selection,
    compose_from_source,
)
from src.presenter.composition_source_bridge import CompositionMaterializedSection
from src.presenter.schemas import (
    AoiSelectedSourceInput,
    ComposeFromIntentRequest,
    ComposeFromIntentResponse,
    ComposeFromSelectionRequest,
    ComposeFromSourceRequest,
    CompositionIssue,
    FirstHopAffordance,
    TransientIntentView,
    ViewPayload,
)
from src.views.generator import (
    ViewGenerateResponse,
    _build_capability_engine_proxy,
    _resolve_view_generation_engine,
)
from src.views.schemas import DataSourceRef, TransformationSpec, ViewDefinition


def _request(
    *,
    sections: list[dict[str, str]] | None = None,
    workflow_key: str = AOI_WORKFLOW_KEY,
    consumer_key: str = "the-critic",
    style_school: str | None = None,
) -> ComposeFromIntentRequest:
    if sections is None:
        sections = [
            {
                "engine_key": "aoi_thematic_report",
                "title": "AOI Report",
                "prose": "This is a narrative-heavy AOI report section.",
            },
            {
                "engine_key": "aoi_sin_findings",
                "title": "Sin Findings",
                "prose": "This section contains grouped findings and themes.",
            },
        ]
    return ComposeFromIntentRequest.model_validate(
        {
            "workflow_key": workflow_key,
            "consumer_key": consumer_key,
            "user_intent": "Compose a concise AOI page for a skeptical reader.",
            "prose_sections": sections,
            "style_school": style_school,
        }
    )


def _source_request(
    *,
    profile: str = "dossier",
    source_v2_job_id: str = "v2-job-123",
    user_intent: str | None = None,
    style_school: str | None = None,
    consumer_key: str = "the-critic",
) -> ComposeFromSourceRequest:
    payload: dict[str, object] = {
        "workflow_key": AOI_WORKFLOW_KEY,
        "consumer_key": consumer_key,
        "source_v2_job_id": source_v2_job_id,
        "profile": profile,
        "style_school": style_school,
    }
    if user_intent is not None:
        payload["user_intent"] = user_intent
    return ComposeFromSourceRequest.model_validate(payload)


def _selection_request(
    *,
    source_v2_job_id: str = "v2-job-123",
    user_intent: str = "Compose an AOI page with synthesis, engagement, and report.",
    selection_summary: str | None = None,
    legacy_profile_equivalent: str | None = None,
    style_school: str | None = None,
    consumer_key: str = "the-critic",
) -> ComposeFromSelectionRequest:
    payload: dict[str, object] = {
        "workflow_key": AOI_WORKFLOW_KEY,
        "consumer_key": consumer_key,
        "source_v2_job_id": source_v2_job_id,
        "selection": [
            {
                "source_family_key": "thematic_synthesis",
                "selection_rank": 1,
                "rationale": "Lead with synthesis.",
            },
            {
                "source_family_key": "engagement_mapping",
                "selection_rank": 2,
                "rationale": "Include the engagement map.",
            },
            {
                "source_family_key": "thematic_report",
                "selection_rank": 3,
                "rationale": "Close with the report.",
            },
        ],
        "user_intent": user_intent,
        "style_school": style_school,
    }
    if selection_summary is not None:
        payload["selection_summary"] = selection_summary
    if legacy_profile_equivalent is not None:
        payload["legacy_profile_equivalent"] = legacy_profile_equivalent
    return ComposeFromSelectionRequest.model_validate(payload)


def _raw_view(
    *,
    engine_key: str,
    renderer_type: str,
    view_key: str = "raw_generated_key",
    view_name: str = "Raw View",
    description: str = "Raw description",
) -> ViewDefinition:
    return ViewDefinition(
        view_key=view_key,
        view_name=view_name,
        description=description,
        target_app="other-app",
        target_page="wrong_page",
        renderer_type=renderer_type,
        renderer_config={
            "show_section_nav": False
        }
        if renderer_type == "prose"
        else {"sections": [{"key": "summary", "title": "Summary"}]},
        data_source=DataSourceRef(
            workflow_key=AOI_WORKFLOW_KEY,
            phase_number=1.0,
            engine_key=engine_key,
            result_path="",
            scope="aggregated",
        ),
        transformation=TransformationSpec(type="none"),
        presentation_stance="diagnostic",
        position=99.0,
        parent_view_key="bad_parent",
        visibility="always",
        status="active",
        generation_mode="generated",
    )


def _payload(
    *,
    view_key: str,
    renderer_type: str,
    structured_data: object,
    renderer_config: dict[str, object] | None = None,
    children: list[ViewPayload] | None = None,
    engine_key: str | None = "aoi_thematic_report",
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
        derivation_kind="compose_from_intent_transient",
        phase_number=None,
        engine_key=engine_key,
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


def test_compose_from_intent_groups_mixed_sections_into_parent_tab_and_counts_tree(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = _request(
        sections=[
            {
                "engine_key": "aoi_thematic_report",
                "title": "AOI Report",
                "prose": "This is a narrative-heavy AOI report section.",
            },
            {
                "engine_key": "aoi_sin_findings",
                "title": "Sin Findings",
                "prose": "This section contains grouped findings and themes.",
            },
        ]
    )

    generated = {
        "accordion_sections": _raw_view(
            engine_key="aoi_sin_findings",
            renderer_type="accordion",
        ),
        "prose_narrative": _raw_view(
            engine_key="aoi_thematic_report",
            renderer_type="prose",
        ),
    }

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._generate_view_definition",
        lambda planner_row, section, planner_position, consumer_key, workflow_key: generated[planner_row.pattern_key].model_copy(deep=True),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent._transform_section_prose",
        lambda section, view_def, planner_row, executor: (
            {"items": [{"title": "One"}]}
            if view_def.renderer_type == "accordion"
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

    response = compose_from_intent(request)

    assert response.presentation.resolver_version == TRANSIENT_COMPOSE_RESOLVER_VERSION
    assert response.presentation.view_count == 3
    assert [entry.stage for entry in response.trace.entries[:3]] == [
        "semantic_surface_matching",
        "hierarchy_planning",
        "page_plan",
    ]

    parent = response.presentation.views[0]
    assert parent.view_key == "compose_intent_parent_aoi_comparison"
    assert parent.renderer_type == "tab"
    assert parent.first_hop_affordance is None
    assert [child.view_key for child in parent.children] == [
        "compose_intent_01_aoi_sin_findings",
        "compose_intent_02_aoi_thematic_report",
    ]
    assert all(child.first_hop_affordance is None for child in parent.children)
    assert parent.structured_data == {
        "compose_intent_01_aoi_sin_findings": {
            "label": "Sin Findings",
            "description": "Structured findings bank for Sin Findings.",
            "semantic_role": "findings_bank",
            "position": 1,
        },
        "compose_intent_02_aoi_thematic_report": {
            "label": "AOI Report",
            "description": "Narrative report closeout for AOI Report.",
            "semantic_role": "report_closeout",
            "position": 2,
        },
    }
    assert [view.view_key for view in response.generated_view_definitions] == [
        "compose_intent_parent_aoi_comparison",
        "compose_intent_01_aoi_sin_findings",
        "compose_intent_02_aoi_thematic_report",
    ]
    assert response.generated_view_definitions[0].child_display_mode == "deep_dives"
    assert [view.parent_view_key for view in response.generated_view_definitions[1:]] == [
        parent.view_key,
        parent.view_key,
    ]


def test_compose_from_intent_uses_workflow_neutral_parent_labels_for_non_aoi_mixed_sections(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = _request(
        workflow_key="intellectual_genealogy",
        sections=[
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
    )

    generated = {
        "card_grid_grouped": _raw_view(
            engine_key="genealogy_relationship_classification",
            renderer_type="card_grid",
        ),
        "prose_narrative": _raw_view(
            engine_key="genealogy_final_synthesis",
            renderer_type="prose",
        ),
    }

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._generate_view_definition",
        lambda planner_row, section, planner_position, consumer_key, workflow_key: generated[planner_row.pattern_key].model_copy(deep=True),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent._transform_section_prose",
        lambda section, view_def, planner_row, executor: (
            {"items": [{"title": "One"}]}
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

    response = compose_from_intent(request)

    parent = response.presentation.views[0]
    assert parent.view_name == "Analytical Comparison"
    assert parent.view_key == "compose_intent_parent_analytical_comparison"


def test_compose_from_intent_all_closeout_stays_flat(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = _request(
        sections=[
            {
                "engine_key": "aoi_thematic_report",
                "title": "AOI Report",
                "prose": "This is a narrative-heavy AOI report section.",
            }
        ]
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._generate_view_definition",
        lambda planner_row, section, planner_position, consumer_key, workflow_key: _raw_view(
            engine_key=section.engine_key,
            renderer_type="prose",
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent._transform_section_prose",
        lambda section, view_def, planner_row, executor: (
            section.prose,
            {
                "view_key": view_def.view_key,
                "engine_key": section.engine_key,
                "renderer_type": view_def.renderer_type,
                "extraction_source": "passthrough",
                "template_key": None,
            },
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent.enforce_final_payload_contracts_or_raise",
        lambda *args, **kwargs: [],
    )

    response = compose_from_intent(request)

    assert [view.view_key for view in response.presentation.views] == [
        "compose_intent_01_aoi_thematic_report"
    ]
    assert response.presentation.views[0].children == []
    assert response.presentation.views[0].first_hop_affordance is None
    assert response.presentation.view_count == 1
    assert [entry.stage for entry in response.trace.entries[:2]] == [
        "semantic_surface_matching",
        "hierarchy_planning",
    ]
    assert response.trace.entries[1].details["grouping_reason"] == "flat_all_closeout"


def test_compose_from_intent_all_working_content_stays_flat(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = _request(
        sections=[
            {
                "engine_key": "aoi_thematic_synthesis",
                "title": "Thematic Synthesis",
                "prose": "Thematic synthesis prose.",
            },
            {
                "engine_key": "aoi_sin_findings",
                "title": "Sin Findings",
                "prose": "Findings prose.",
            },
        ]
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._generate_view_definition",
        lambda planner_row, section, planner_position, consumer_key, workflow_key: _raw_view(
            engine_key=section.engine_key,
            renderer_type="accordion",
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent._transform_section_prose",
        lambda section, view_def, planner_row, executor: (
            {"sections": [{"title": section.title}]},
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

    response = compose_from_intent(request)

    assert [view.view_key for view in response.presentation.views] == [
        "compose_intent_01_aoi_thematic_synthesis",
        "compose_intent_02_aoi_sin_findings",
    ]
    assert all(view.children == [] for view in response.presentation.views)
    assert all(view.first_hop_affordance is None for view in response.presentation.views)
    assert response.presentation.view_count == 2
    assert response.trace.entries[1].details["grouping_reason"] == "flat_all_working_content"


def test_compose_from_intent_duplicate_engine_keys_still_produce_unique_normalized_view_keys(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = _request(
        sections=[
            {
                "engine_key": "aoi_thematic_report",
                "title": "Section One",
                "prose": "First section prose.",
            },
            {
                "engine_key": "aoi_thematic_report",
                "title": "Section Two",
                "prose": "Second section prose.",
            },
        ]
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._generate_view_definition",
        lambda planner_row, section, planner_position, consumer_key, workflow_key: _raw_view(
            engine_key=section.engine_key,
            renderer_type="prose",
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent._transform_section_prose",
        lambda section, view_def, planner_row, executor: (
            section.prose,
            {
                "view_key": view_def.view_key,
                "engine_key": section.engine_key,
                "renderer_type": view_def.renderer_type,
                "extraction_source": "passthrough",
                "template_key": None,
            },
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent.enforce_final_payload_contracts_or_raise",
        lambda *args, **kwargs: [],
    )

    response = compose_from_intent(request)

    assert [view.view_key for view in response.generated_view_definitions] == [
        "compose_intent_01_aoi_thematic_report",
        "compose_intent_02_aoi_thematic_report",
    ]


def test_inventory_listing_rule_is_deterministic() -> None:
    planner_row = _match_section_to_planner_row(
        _PlannerSectionContext(
            section_index=0,
            engine_key="custom_inventory_index",
            title="Inventory Register",
            prose="Inventory prose.",
        )
    )

    assert planner_row.semantic_role == "inventory_listing"
    assert planner_row.pattern_key == "card_grid_simple"
    assert planner_row.presentation_stance == "diagnostic"


def test_match_section_to_planner_row_uses_capability_metadata_for_migrated_engine_with_neutral_title(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _Registry:
        def get_capability_definition(self, engine_key):
            if engine_key == "aoi_thematic_synthesis":
                return SimpleNamespace(
                    engine_key=engine_key,
                    composition_role="synthesis_primary",
                    legacy_engine_key=None,
                )
            return None

        def list_capability_definitions(self):
            return []

    monkeypatch.setattr(
        "src.engines.registry.get_engine_registry",
        lambda: _Registry(),
    )

    planner_row = _match_section_to_planner_row(
        _PlannerSectionContext(
            section_index=0,
            engine_key="aoi_thematic_synthesis",
            title="Neutral Surface",
            prose="Neutral prose.",
        )
    )

    assert planner_row.semantic_role == "synthesis_primary"
    assert planner_row.pattern_key == "accordion_sections"
    assert planner_row.presentation_stance == "summary"


def test_match_section_to_planner_row_fails_closed_for_migrated_engine_missing_composition_role_with_neutral_title(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _Registry:
        def get_capability_definition(self, engine_key):
            if engine_key == "aoi_thematic_synthesis":
                return SimpleNamespace(
                    engine_key=engine_key,
                    composition_role=None,
                    legacy_engine_key=None,
                )
            return None

        def list_capability_definitions(self):
            return []

    monkeypatch.setattr(
        "src.engines.registry.get_engine_registry",
        lambda: _Registry(),
    )

    with pytest.raises(ComposeFromIntentUpstreamError) as excinfo:
        _match_section_to_planner_row(
            _PlannerSectionContext(
                section_index=0,
                engine_key="aoi_thematic_synthesis",
                title="Neutral Surface",
                prose="Neutral prose.",
            )
        )

    assert "composition_role metadata" in str(excinfo.value)
    assert "aoi_thematic_synthesis" in str(excinfo.value)


def test_match_section_to_planner_row_fails_closed_for_migrated_engine_missing_capability_metadata_with_neutral_title(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _Registry:
        def get_capability_definition(self, _engine_key):
            return None

        def list_capability_definitions(self):
            return []

    monkeypatch.setattr(
        "src.engines.registry.get_engine_registry",
        lambda: _Registry(),
    )

    with pytest.raises(ComposeFromIntentUpstreamError) as excinfo:
        _match_section_to_planner_row(
            _PlannerSectionContext(
                section_index=0,
                engine_key="aoi_thematic_synthesis",
                title="Neutral Surface",
                prose="Neutral prose.",
            )
        )

    assert "composition_role metadata" in str(excinfo.value)
    assert "aoi_thematic_synthesis" in str(excinfo.value)


def test_match_section_to_planner_row_fails_closed_for_migrated_legacy_alias_missing_capability_metadata_with_neutral_title(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _Registry:
        def get_capability_definition(self, _engine_key):
            return None

        def list_capability_definitions(self):
            return []

    monkeypatch.setattr(
        "src.engines.registry.get_engine_registry",
        lambda: _Registry(),
    )

    with pytest.raises(ComposeFromIntentUpstreamError) as excinfo:
        _match_section_to_planner_row(
            _PlannerSectionContext(
                section_index=0,
                engine_key="genealogy_pass7_final_synthesis",
                title="Neutral Surface",
                prose="Neutral prose.",
            )
        )

    assert "composition_role metadata" in str(excinfo.value)
    assert "genealogy_pass7_final_synthesis" in str(excinfo.value)


def test_compose_from_intent_fails_closed_for_valid_unclassified_engine() -> None:
    request = _request(
        sections=[
            {
                "engine_key": "theory_construction_analyzer",
                "title": "Opaque Surface",
                "prose": "Unclassifiable prose.",
            }
        ]
    )

    with pytest.raises(ComposeFromIntentUpstreamError) as excinfo:
        compose_from_intent(request)

    assert "allowed leaf family" in str(excinfo.value)
    assert "theory_construction_analyzer" in str(excinfo.value)


def test_compose_from_intent_supports_genealogy_direct_sections(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = _request(
        workflow_key="intellectual_genealogy",
        sections=[
            {
                "engine_key": "genealogy_final_synthesis",
                "title": "Genealogy Report",
                "prose": "Narrative genealogy closeout prose.",
            }
        ],
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._generate_view_definition",
        lambda planner_row, section, planner_position, consumer_key, workflow_key: _raw_view(
            engine_key=section.engine_key,
            renderer_type="prose",
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent._transform_section_prose",
        lambda section, view_def, planner_row, executor: (
            section.prose,
            {
                "view_key": view_def.view_key,
                "engine_key": section.engine_key,
                "renderer_type": view_def.renderer_type,
                "extraction_source": "passthrough",
                "template_key": None,
            },
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent.enforce_final_payload_contracts_or_raise",
        lambda *args, **kwargs: [],
    )

    response = compose_from_intent(request)

    assert response.presentation.workflow_key == "intellectual_genealogy"
    assert response.presentation.consumer_key == "the-critic"
    assert response.presentation.resolver_version == TRANSIENT_COMPOSE_RESOLVER_VERSION
    assert response.presentation.view_count == 1
    assert response.presentation.views[0].first_hop_affordance == FirstHopAffordance(
        capturable=True,
        allowed_destinations=["arsenal", "research_todo"],
    )


@pytest.mark.parametrize(
    "engine_key",
    [
        "aoi_thematic_synthesis",
        "aoi_engagement_mapping",
        "aoi_sin_findings",
        "aoi_thematic_report",
        "genealogy_relationship_classification",
        "genealogy_final_synthesis",
        "genealogy_pass1b_relationship_classification",
        "genealogy_pass7_final_synthesis",
    ],
)
def test_to_transient_view_emits_first_hop_affordance_for_migrated_family_leaf_views(
    engine_key: str,
) -> None:
    payload = _payload(
        view_key=f"leaf_{engine_key}",
        renderer_type="prose",
        structured_data="body",
        engine_key=engine_key,
    )

    view = _to_transient_view(payload, first_hop_affordance_enabled=True)

    assert view.first_hop_affordance == FirstHopAffordance(
        capturable=True,
        allowed_destinations=["arsenal", "research_todo"],
    )


def test_to_transient_view_emits_first_hop_affordance_for_genealogy_idea_evolution_concept_synthesis_leaf() -> None:
    payload = _payload(
        view_key="genealogy_idea_evolution",
        renderer_type="tab",
        structured_data={"summary": "Idea evolution"},
        engine_key="concept_synthesis",
    )

    view = _to_transient_view(payload, first_hop_affordance_enabled=True)

    assert view.first_hop_affordance == FirstHopAffordance(
        capturable=True,
        allowed_destinations=["arsenal", "research_todo"],
    )


def test_to_transient_view_omits_first_hop_affordance_for_parent_container_views() -> None:
    payload = _payload(
        view_key="parent",
        renderer_type="tab",
        structured_data={"child": {"label": "Child"}},
        engine_key=None,
        children=[
            _payload(
                view_key="child",
                renderer_type="prose",
                structured_data="child body",
                engine_key="aoi_thematic_report",
            )
        ],
    )

    view = _to_transient_view(payload, first_hop_affordance_enabled=True)

    assert view.first_hop_affordance is None
    assert view.children[0].first_hop_affordance == FirstHopAffordance(
        capturable=True,
        allowed_destinations=["arsenal", "research_todo"],
    )


def test_to_transient_view_omits_first_hop_affordance_for_non_migrated_leaf_views() -> None:
    payload = _payload(
        view_key="leaf_custom_inventory",
        renderer_type="prose",
        structured_data="body",
        engine_key="custom_inventory_index",
    )

    view = _to_transient_view(payload, first_hop_affordance_enabled=True)

    assert view.first_hop_affordance is None


def test_to_transient_view_omits_first_hop_affordance_for_disabled_route_on_migrated_leaf() -> None:
    payload = _payload(
        view_key="leaf_aoi_thematic_report",
        renderer_type="prose",
        structured_data="body",
        engine_key="aoi_thematic_report",
    )

    view = _to_transient_view(payload, first_hop_affordance_enabled=False)

    assert view.first_hop_affordance is None


@pytest.mark.parametrize(
    ("workflow_key", "handoff_kind", "expected"),
    [
        (AOI_WORKFLOW_KEY, "source_profile", True),
        (AOI_WORKFLOW_KEY, "source_selection", True),
        (AOI_WORKFLOW_KEY, "direct_sections", False),
        ("intellectual_genealogy", "direct_sections", True),
    ],
)
def test_handoff_supports_first_hop_affordance_only_for_scoped_routes(
    workflow_key: str,
    handoff_kind: str,
    expected: bool,
) -> None:
    assert (
        _handoff_supports_first_hop_affordance(
            workflow_key=workflow_key,
            handoff_kind=handoff_kind,
        )
        is expected
    )


def test_compose_from_source_rejects_unsupported_genealogy_profile_handoff() -> None:
    request = ComposeFromSourceRequest.model_validate(
        {
            "workflow_key": "intellectual_genealogy",
            "consumer_key": "the-critic",
            "source_v2_job_id": "v2-job-123",
            "profile": "dossier",
        }
    )

    with pytest.raises(ComposeFromIntentClientError) as excinfo:
        compose_from_source(request)

    assert "handoff_kind='source_profile'" in str(excinfo.value)


def test_compose_from_source_builds_dossier_sections_and_threads_planning_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    build_args: dict[str, object] = {}

    bridge = SimpleNamespace(
        catalog=SimpleNamespace(to_trace_dict=lambda: {"candidates": []}),
        selection=SimpleNamespace(
            to_trace_dict=lambda: {
                "selected": [],
                "selection_summary": "Use synthesis, engagement, and report for a fuller AOI page.",
                "legacy_profile_equivalent": "comparison",
            }
        ),
        materialized_sections=[
            CompositionMaterializedSection(
                source_family_key="thematic_synthesis",
                engine_key="aoi_thematic_synthesis",
                title="Thematic Synthesis",
                materialization_position=1,
                profile="dossier",
                composition_role_hint="synthesis_primary",
                section=SimpleNamespace(
                    model_dump=lambda: {
                        "engine_key": "aoi_thematic_synthesis",
                        "title": "Thematic Synthesis",
                        "prose": '{"themes": [{"theme_name": "Planning"}]}',
                    }
                ),
            ),
            CompositionMaterializedSection(
                source_family_key="thematic_report",
                engine_key="aoi_thematic_report",
                title="AOI Report",
                materialization_position=2,
                profile="dossier",
                composition_role_hint="report_closeout",
                section=SimpleNamespace(
                    model_dump=lambda: {
                        "engine_key": "aoi_thematic_report",
                        "title": "AOI Report",
                        "prose": '{"report_sections": {"summary": "Summary"}}',
                    }
                ),
            ),
        ],
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.build_source_composition_bridge",
        lambda source_v2_job_id, profile: bridge,
    )

    def _fake_internal(request, *, handoff_kind, resolver_version, planning_sections=None, trace_prefix=None):
        captured["request"] = request
        captured["handoff_kind"] = handoff_kind
        captured["resolver_version"] = resolver_version
        captured["planning_sections"] = planning_sections
        captured["trace_prefix"] = trace_prefix
        return {"ok": True}

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._compose_handoff_sections",
        _fake_internal,
    )

    result = compose_from_source(_source_request(profile="dossier"))

    assert result == {"ok": True}
    rewritten_request = captured["request"]
    assert rewritten_request.user_intent.startswith("Compose a compact AOI briefing page")
    assert captured["handoff_kind"] == "source_profile"
    assert [section.engine_key for section in rewritten_request.prose_sections] == [
        "aoi_thematic_synthesis",
        "aoi_thematic_report",
    ]
    assert captured["resolver_version"] == TRANSIENT_COMPOSE_SOURCE_RESOLVER_VERSION
    planning_sections = captured["planning_sections"]
    assert [section.composition_role_hint for section in planning_sections] == [
        "synthesis_primary",
        "report_closeout",
    ]
    assert [section.profile for section in planning_sections] == ["dossier", "dossier"]
    assert [entry.stage for entry in captured["trace_prefix"]] == [
        "source_catalog_resolution",
        "source_selection",
        "section_materialization",
    ]


def test_compose_from_selection_builds_sections_and_threads_planning_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    build_args: dict[str, object] = {}

    bridge = SimpleNamespace(
        catalog=SimpleNamespace(to_trace_dict=lambda: {"candidates": []}),
        selection=SimpleNamespace(
            to_trace_dict=lambda: {
                "selected": [],
                "selection_summary": "Use synthesis, engagement, and report for a fuller AOI page.",
                "legacy_profile_equivalent": "comparison",
            }
        ),
        materialized_sections=[
            CompositionMaterializedSection(
                source_family_key="thematic_synthesis",
                engine_key="aoi_thematic_synthesis",
                title="Thematic Synthesis",
                materialization_position=1,
                profile=None,
                composition_role_hint="synthesis_primary",
                section=SimpleNamespace(
                    model_dump=lambda: {
                        "engine_key": "aoi_thematic_synthesis",
                        "title": "Thematic Synthesis",
                        "prose": '{"themes": [{"theme_name": "Planning"}]}',
                    }
                ),
            ),
            CompositionMaterializedSection(
                source_family_key="engagement_mapping",
                engine_key="aoi_engagement_mapping",
                title="Engagement Mapping",
                materialization_position=2,
                profile=None,
                composition_role_hint="comparison_map",
                section=SimpleNamespace(
                    model_dump=lambda: {
                        "engine_key": "aoi_engagement_mapping",
                        "title": "Engagement Mapping",
                        "prose": '{"engagements": [{"theme": "Planning"}]}',
                    }
                ),
            ),
            CompositionMaterializedSection(
                source_family_key="thematic_report",
                engine_key="aoi_thematic_report",
                title="AOI Report",
                materialization_position=3,
                profile=None,
                composition_role_hint="report_closeout",
                section=SimpleNamespace(
                    model_dump=lambda: {
                        "engine_key": "aoi_thematic_report",
                        "title": "AOI Report",
                        "prose": '{"report_sections": {"summary": "Summary"}}',
                    }
                ),
            ),
        ],
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.build_selection_composition_bridge",
        lambda **kwargs: build_args.update(kwargs) or bridge,
    )

    def _fake_internal(request, *, handoff_kind, resolver_version, planning_sections=None, trace_prefix=None):
        captured["request"] = request
        captured["handoff_kind"] = handoff_kind
        captured["resolver_version"] = resolver_version
        captured["planning_sections"] = planning_sections
        captured["trace_prefix"] = trace_prefix
        return {"ok": True}

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._compose_handoff_sections",
        _fake_internal,
    )

    result = compose_from_selection(
        _selection_request(
            selection_summary="Use synthesis, engagement, and report for a fuller AOI page.",
            legacy_profile_equivalent="comparison",
        )
    )

    assert result == {"ok": True}
    assert captured["handoff_kind"] == "source_selection"
    assert build_args["selection_summary"] == "Use synthesis, engagement, and report for a fuller AOI page."
    assert build_args["legacy_profile_equivalent"] == "comparison"
    rewritten_request = captured["request"]
    assert rewritten_request.user_intent == "Compose an AOI page with synthesis, engagement, and report."
    assert [section.engine_key for section in rewritten_request.prose_sections] == [
        "aoi_thematic_synthesis",
        "aoi_engagement_mapping",
        "aoi_thematic_report",
    ]
    assert captured["resolver_version"] == TRANSIENT_COMPOSE_SELECTION_RESOLVER_VERSION
    planning_sections = captured["planning_sections"]
    assert [section.profile for section in planning_sections] == [None, None, None]
    assert [entry.stage for entry in captured["trace_prefix"]] == [
        "source_catalog_resolution",
        "source_selection",
        "section_materialization",
    ]
    assert captured["trace_prefix"][1].details["selection_summary"] == (
        "Use synthesis, engagement, and report for a fuller AOI page."
    )
    assert captured["trace_prefix"][1].details["legacy_profile_equivalent"] == "comparison"


def test_compose_from_selection_populates_persistable_compose_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bridge = SimpleNamespace(
        catalog=SimpleNamespace(to_trace_dict=lambda: {"candidates": []}),
        selection=SimpleNamespace(
            to_trace_dict=lambda: {"selected": [], "selection_summary": "Use synthesis."}
        ),
        materialized_sections=[
            CompositionMaterializedSection(
                source_family_key="thematic_synthesis",
                engine_key="aoi_thematic_synthesis",
                title="Thematic Synthesis",
                materialization_position=1,
                profile=None,
                composition_role_hint="synthesis_primary",
                section=SimpleNamespace(
                    model_dump=lambda: {
                        "engine_key": "aoi_thematic_synthesis",
                        "title": "Thematic Synthesis",
                        "prose": '{"themes": [{"theme_name": "Planning"}]}',
                    }
                ),
            )
        ],
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.build_selection_composition_bridge",
        lambda **kwargs: bridge,
    )

    def _fake_internal(request, *, handoff_kind, resolver_version, planning_sections=None, trace_prefix=None):
        return ComposeFromIntentResponse.model_validate(
            {
                "presentation": {
                    "workflow_key": request.workflow_key,
                    "consumer_key": request.consumer_key,
                    "presentation_contract_version": 1,
                    "presentation_hash": "hash-1",
                    "presentation_content_hash": "content-hash-1",
                    "resolver_version": resolver_version,
                    "style_school": request.style_school or "",
                    "views": [],
                    "view_count": 0,
                },
                "generated_view_definitions": [],
                "trace": {
                    "resolver_version": resolver_version,
                    "entries": [],
                },
            }
        )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._compose_handoff_sections",
        _fake_internal,
    )

    request = _selection_request(
        consumer_key="transient-proof-harness",
        user_intent="Compose an AOI page with synthesis.",
        style_school="explanatory_narrative",
    )
    result = compose_from_selection(request)

    assert result.persistable_compose_request is not None
    assert result.persistable_compose_request.model_dump(mode="python") == {
        "workflow_key": AOI_WORKFLOW_KEY,
        "consumer_key": "transient-proof-harness",
        "user_intent": "Compose an AOI page with synthesis.",
        "prose_sections": [
            {
                "engine_key": "aoi_thematic_synthesis",
                "title": "Thematic Synthesis",
                "prose": '{"themes": [{"theme_name": "Planning"}]}',
            }
        ],
        "style_school": "explanatory_narrative",
        "audience": None,
    }


def test_compose_from_intent_response_defaults_persistable_compose_request_to_none() -> None:
    response = ComposeFromIntentResponse.model_validate(
        {
            "presentation": {
                "workflow_key": "intellectual_genealogy",
                "consumer_key": "transient-proof-harness",
                "presentation_contract_version": 1,
                "presentation_hash": "hash-1",
                "presentation_content_hash": "content-hash-1",
                "resolver_version": "compose-from-intent-v2",
                "style_school": "explanatory_narrative",
                "views": [],
                "view_count": 0,
            },
            "generated_view_definitions": [],
            "trace": {
                "resolver_version": "compose-from-intent-v2",
                "entries": [],
            },
        }
    )

    assert response.persistable_compose_request is None


def test_compose_from_intent_rejects_unknown_workflow() -> None:
    with pytest.raises(ComposeFromIntentClientError):
        compose_from_intent(_request(workflow_key="unknown_workflow"))


def test_compose_from_intent_accepts_aoi_canary_for_genealogy_direct_sections(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = _request(
        workflow_key="intellectual_genealogy",
        consumer_key="aoi-canary",
        sections=[
            {
                "engine_key": "genealogy_final_synthesis",
                "title": "Genealogy Report",
                "prose": "Narrative genealogy closeout prose.",
            }
        ],
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._generate_view_definition",
        lambda planner_row, section, planner_position, consumer_key, workflow_key: _raw_view(
            engine_key=section.engine_key,
            renderer_type="prose",
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent._transform_section_prose",
        lambda section, view_def, planner_row, executor: (
            section.prose,
            {
                "view_key": view_def.view_key,
                "engine_key": section.engine_key,
                "renderer_type": view_def.renderer_type,
                "extraction_source": "passthrough",
                "template_key": None,
            },
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent.enforce_final_payload_contracts_or_raise",
        lambda *args, **kwargs: [],
    )

    response = compose_from_intent(request)

    assert response.presentation.workflow_key == "intellectual_genealogy"
    assert response.presentation.consumer_key == "aoi-canary"
    assert response.presentation.resolver_version == TRANSIENT_COMPOSE_RESOLVER_VERSION
    assert response.presentation.view_count == 1


def test_validate_request_accepts_aoi_capability_definition_engine_keys() -> None:
    _validate_request(_request(), handoff_kind="direct_sections")


def test_compose_from_selection_accepts_aoi_canary_consumer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    build_args: dict[str, object] = {}
    captured: dict[str, object] = {}
    bridge = SimpleNamespace(
        catalog=SimpleNamespace(to_trace_dict=lambda: {"candidates": []}),
        selection=SimpleNamespace(
            to_trace_dict=lambda: {"selected": [], "selection_summary": "all four"}
        ),
        materialized_sections=[
            CompositionMaterializedSection(
                source_family_key="thematic_synthesis",
                engine_key="aoi_thematic_synthesis",
                title="Thematic Synthesis",
                materialization_position=1,
                profile=None,
                composition_role_hint="synthesis_primary",
                section=SimpleNamespace(
                    model_dump=lambda: {
                        "engine_key": "aoi_thematic_synthesis",
                        "title": "Thematic Synthesis",
                        "prose": '{"themes": [{"theme_name": "Planning"}]}',
                    }
                ),
            )
        ],
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.build_selection_composition_bridge",
        lambda **kwargs: build_args.update(kwargs) or bridge,
    )

    def _fake_internal(request, *, handoff_kind, resolver_version, planning_sections=None, trace_prefix=None):
        captured["request"] = request
        captured["handoff_kind"] = handoff_kind
        captured["resolver_version"] = resolver_version
        captured["planning_sections"] = planning_sections
        captured["trace_prefix"] = trace_prefix
        return {"ok": True}

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._compose_handoff_sections",
        _fake_internal,
    )

    result = compose_from_selection(
        _selection_request(
            consumer_key="aoi-canary",
        )
    )

    assert result == {"ok": True}
    rewritten_request = captured["request"]
    assert rewritten_request.consumer_key == "aoi-canary"
    assert captured["handoff_kind"] == "source_selection"
    assert captured["resolver_version"] == TRANSIENT_COMPOSE_SELECTION_RESOLVER_VERSION
    assert build_args["source_v2_job_id"] == "v2-job-123"


def test_transient_proof_harness_admission_shape_is_bounded() -> None:
    assert _REGISTERED_TRANSIENT_CONSUMER_ADAPTERS["transient-proof-harness"] == frozenset(
        {
            "source_selection",
            "direct_sections",
        }
    )
    assert "source_profile" not in _REGISTERED_TRANSIENT_CONSUMER_ADAPTERS["transient-proof-harness"]


def test_transient_proof_probe_admission_shape_is_bounded() -> None:
    assert _REGISTERED_TRANSIENT_CONSUMER_ADAPTERS["transient-proof-probe"] == frozenset(
        {
            "source_selection",
            "direct_sections",
        }
    )
    assert "source_profile" not in _REGISTERED_TRANSIENT_CONSUMER_ADAPTERS["transient-proof-probe"]
    assert "transient-proof-probe" not in _REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER


def test_compose_from_selection_accepts_transient_proof_harness_consumer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    build_args: dict[str, object] = {}
    captured: dict[str, object] = {}
    bridge = SimpleNamespace(
        catalog=SimpleNamespace(to_trace_dict=lambda: {"candidates": []}),
        selection=SimpleNamespace(
            to_trace_dict=lambda: {"selected": [], "selection_summary": "all four"}
        ),
        materialized_sections=[
            CompositionMaterializedSection(
                source_family_key="thematic_synthesis",
                engine_key="aoi_thematic_synthesis",
                title="Thematic Synthesis",
                materialization_position=1,
                profile=None,
                composition_role_hint="synthesis_primary",
                section=SimpleNamespace(
                    model_dump=lambda: {
                        "engine_key": "aoi_thematic_synthesis",
                        "title": "Thematic Synthesis",
                        "prose": '{"themes": [{"theme_name": "Planning"}]}',
                    }
                ),
            )
        ],
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.build_selection_composition_bridge",
        lambda **kwargs: build_args.update(kwargs) or bridge,
    )

    def _fake_internal(request, *, handoff_kind, resolver_version, planning_sections=None, trace_prefix=None):
        captured["request"] = request
        captured["handoff_kind"] = handoff_kind
        captured["resolver_version"] = resolver_version
        captured["planning_sections"] = planning_sections
        captured["trace_prefix"] = trace_prefix
        return {"ok": True}

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._compose_handoff_sections",
        _fake_internal,
    )

    result = compose_from_selection(
        _selection_request(
            consumer_key="transient-proof-harness",
        )
    )

    assert result == {"ok": True}
    rewritten_request = captured["request"]
    assert rewritten_request.consumer_key == "transient-proof-harness"
    assert captured["handoff_kind"] == "source_selection"
    assert captured["resolver_version"] == TRANSIENT_COMPOSE_SELECTION_RESOLVER_VERSION
    assert build_args["source_v2_job_id"] == "v2-job-123"


def test_compose_from_selection_accepts_transient_proof_probe_consumer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    build_args: dict[str, object] = {}
    captured: dict[str, object] = {}
    bridge = SimpleNamespace(
        catalog=SimpleNamespace(to_trace_dict=lambda: {"candidates": []}),
        selection=SimpleNamespace(
            to_trace_dict=lambda: {"selected": [], "selection_summary": "all four"}
        ),
        materialized_sections=[
            CompositionMaterializedSection(
                source_family_key="thematic_synthesis",
                engine_key="aoi_thematic_synthesis",
                title="Thematic Synthesis",
                materialization_position=1,
                profile=None,
                composition_role_hint="synthesis_primary",
                section=SimpleNamespace(
                    model_dump=lambda: {
                        "engine_key": "aoi_thematic_synthesis",
                        "title": "Thematic Synthesis",
                        "prose": '{"themes": [{"theme_name": "Planning"}]}',
                    }
                ),
            )
        ],
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.build_selection_composition_bridge",
        lambda **kwargs: build_args.update(kwargs) or bridge,
    )

    def _fake_internal(request, *, handoff_kind, resolver_version, planning_sections=None, trace_prefix=None):
        captured["request"] = request
        captured["handoff_kind"] = handoff_kind
        captured["resolver_version"] = resolver_version
        captured["planning_sections"] = planning_sections
        captured["trace_prefix"] = trace_prefix
        return {"ok": True}

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._compose_handoff_sections",
        _fake_internal,
    )

    result = compose_from_selection(
        _selection_request(
            consumer_key="transient-proof-probe",
        )
    )

    assert result == {"ok": True}
    rewritten_request = captured["request"]
    assert rewritten_request.consumer_key == "transient-proof-probe"
    assert captured["handoff_kind"] == "source_selection"
    assert captured["resolver_version"] == TRANSIENT_COMPOSE_SELECTION_RESOLVER_VERSION
    assert build_args["source_v2_job_id"] == "v2-job-123"


def test_compose_from_source_accepts_aoi_canary_for_source_profile_dossier(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    bridge = SimpleNamespace(
        catalog=SimpleNamespace(to_trace_dict=lambda: {"candidates": []}),
        selection=SimpleNamespace(
            to_trace_dict=lambda: {
                "selected": [],
                "selection_summary": "Use synthesis and report for a compact dossier.",
                "legacy_profile_equivalent": "dossier",
            }
        ),
        materialized_sections=[
            CompositionMaterializedSection(
                source_family_key="thematic_synthesis",
                engine_key="aoi_thematic_synthesis",
                title="Thematic Synthesis",
                materialization_position=1,
                profile="dossier",
                composition_role_hint="synthesis_primary",
                section=SimpleNamespace(
                    model_dump=lambda: {
                        "engine_key": "aoi_thematic_synthesis",
                        "title": "Thematic Synthesis",
                        "prose": '{"themes": [{"theme_name": "Planning"}]}',
                    }
                ),
            ),
            CompositionMaterializedSection(
                source_family_key="thematic_report",
                engine_key="aoi_thematic_report",
                title="AOI Report",
                materialization_position=2,
                profile="dossier",
                composition_role_hint="report_closeout",
                section=SimpleNamespace(
                    model_dump=lambda: {
                        "engine_key": "aoi_thematic_report",
                        "title": "AOI Report",
                        "prose": '{"report_sections": {"summary": "Summary"}}',
                    }
                ),
            ),
        ],
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.build_source_composition_bridge",
        lambda source_v2_job_id, profile: bridge,
    )

    def _fake_internal(request, *, handoff_kind, resolver_version, planning_sections=None, trace_prefix=None):
        captured["request"] = request
        captured["handoff_kind"] = handoff_kind
        captured["resolver_version"] = resolver_version
        captured["planning_sections"] = planning_sections
        captured["trace_prefix"] = trace_prefix
        return {"ok": True}

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._compose_handoff_sections",
        _fake_internal,
    )

    result = compose_from_source(_source_request(consumer_key="aoi-canary", source_v2_job_id="job-744edf255ad5"))

    assert result == {"ok": True}
    rewritten_request = captured["request"]
    assert rewritten_request.consumer_key == "aoi-canary"
    assert rewritten_request.workflow_key == AOI_WORKFLOW_KEY
    assert captured["handoff_kind"] == "source_profile"
    assert captured["resolver_version"] == TRANSIENT_COMPOSE_SOURCE_RESOLVER_VERSION
    assert [section.engine_key for section in rewritten_request.prose_sections] == [
        "aoi_thematic_synthesis",
        "aoi_thematic_report",
    ]


def test_compose_from_source_accepts_aoi_canary_for_source_profile_comparison(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    bridge = SimpleNamespace(
        catalog=SimpleNamespace(to_trace_dict=lambda: {"candidates": []}),
        selection=SimpleNamespace(
            to_trace_dict=lambda: {
                "selected": [],
                "selection_summary": "Use engagement, findings, and report for a bounded comparison.",
                "legacy_profile_equivalent": "comparison",
            }
        ),
        materialized_sections=[
            CompositionMaterializedSection(
                source_family_key="engagement_mapping",
                engine_key="aoi_engagement_mapping",
                title="Engagement Mapping",
                materialization_position=1,
                profile="comparison",
                composition_role_hint="comparison_map",
                section=SimpleNamespace(
                    model_dump=lambda: {
                        "engine_key": "aoi_engagement_mapping",
                        "title": "Engagement Mapping",
                        "prose": '{"groups": [{"title": "Debt"}]}',
                    }
                ),
            ),
            CompositionMaterializedSection(
                source_family_key="sin_findings",
                engine_key="aoi_sin_findings",
                title="Sin Findings",
                materialization_position=2,
                profile="comparison",
                composition_role_hint="findings_bank",
                section=SimpleNamespace(
                    model_dump=lambda: {
                        "engine_key": "aoi_sin_findings",
                        "title": "Sin Findings",
                        "prose": '{"sections": [{"title": "Section A"}]}',
                    }
                ),
            ),
            CompositionMaterializedSection(
                source_family_key="thematic_report",
                engine_key="aoi_thematic_report",
                title="AOI Report",
                materialization_position=3,
                profile="comparison",
                composition_role_hint="report_closeout",
                section=SimpleNamespace(
                    model_dump=lambda: {
                        "engine_key": "aoi_thematic_report",
                        "title": "AOI Report",
                        "prose": '{"report_sections": {"summary": "Summary"}}',
                    }
                ),
            ),
        ],
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.build_source_composition_bridge",
        lambda source_v2_job_id, profile: bridge,
    )

    def _fake_internal(request, *, handoff_kind, resolver_version, planning_sections=None, trace_prefix=None):
        captured["request"] = request
        captured["handoff_kind"] = handoff_kind
        captured["resolver_version"] = resolver_version
        captured["planning_sections"] = planning_sections
        captured["trace_prefix"] = trace_prefix
        return {"ok": True}

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._compose_handoff_sections",
        _fake_internal,
    )

    result = compose_from_source(
        _source_request(
            consumer_key="aoi-canary",
            profile="comparison",
            source_v2_job_id="job-744edf255ad5",
        )
    )

    assert result == {"ok": True}
    rewritten_request = captured["request"]
    assert rewritten_request.consumer_key == "aoi-canary"
    assert rewritten_request.workflow_key == AOI_WORKFLOW_KEY
    assert captured["handoff_kind"] == "source_profile"
    assert captured["resolver_version"] == TRANSIENT_COMPOSE_SOURCE_RESOLVER_VERSION
    assert [section.engine_key for section in rewritten_request.prose_sections] == [
        "aoi_engagement_mapping",
        "aoi_sin_findings",
        "aoi_thematic_report",
    ]


def test_compose_from_source_rejects_transient_proof_harness_for_source_profile() -> None:
    with pytest.raises(
        ComposeFromIntentClientError,
        match="compose-from-source does not support consumer_key='transient-proof-harness' for handoff_kind='source_profile'",
    ):
        compose_from_source(
            _source_request(
                consumer_key="transient-proof-harness",
                profile="dossier",
                source_v2_job_id="job-744edf255ad5",
            )
        )


def test_compose_from_source_rejects_transient_proof_probe_for_source_profile() -> None:
    with pytest.raises(
        ComposeFromIntentClientError,
        match="compose-from-source does not support consumer_key='transient-proof-probe' for handoff_kind='source_profile'",
    ):
        compose_from_source(
            _source_request(
                consumer_key="transient-proof-probe",
                profile="dossier",
                source_v2_job_id="job-744edf255ad5",
            )
        )


def test_compose_from_intent_accepts_transient_proof_harness_for_genealogy_direct_sections(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = _request(
        workflow_key="intellectual_genealogy",
        consumer_key="transient-proof-harness",
        sections=[
            {
                "engine_key": "genealogy_final_synthesis",
                "title": "Genealogy Report",
                "prose": "Narrative genealogy closeout prose.",
            }
        ],
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._generate_view_definition",
        lambda planner_row, section, planner_position, consumer_key, workflow_key: _raw_view(
            engine_key=section.engine_key,
            renderer_type="prose",
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent._transform_section_prose",
        lambda section, view_def, planner_row, executor: (
            section.prose,
            {
                "view_key": view_def.view_key,
                "engine_key": section.engine_key,
                "renderer_type": view_def.renderer_type,
                "extraction_source": "passthrough",
                "template_key": None,
            },
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent.enforce_final_payload_contracts_or_raise",
        lambda *args, **kwargs: [],
    )

    response = compose_from_intent(request)

    assert response.presentation.workflow_key == "intellectual_genealogy"
    assert response.presentation.consumer_key == "transient-proof-harness"
    assert response.presentation.resolver_version == TRANSIENT_COMPOSE_RESOLVER_VERSION
    assert response.presentation.view_count == 1


def test_compose_from_intent_accepts_transient_proof_probe_for_genealogy_direct_sections(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = _request(
        workflow_key="intellectual_genealogy",
        consumer_key="transient-proof-probe",
        sections=[
            {
                "engine_key": "genealogy_final_synthesis",
                "title": "Genealogy Report",
                "prose": "Narrative genealogy closeout prose.",
            }
        ],
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._generate_view_definition",
        lambda planner_row, section, planner_position, consumer_key, workflow_key: _raw_view(
            engine_key=section.engine_key,
            renderer_type="prose",
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent._transform_section_prose",
        lambda section, view_def, planner_row, executor: (
            section.prose,
            {
                "view_key": view_def.view_key,
                "engine_key": section.engine_key,
                "renderer_type": view_def.renderer_type,
                "extraction_source": "passthrough",
                "template_key": None,
            },
        ),
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent.enforce_final_payload_contracts_or_raise",
        lambda *args, **kwargs: [],
    )

    response = compose_from_intent(request)

    assert response.presentation.workflow_key == "intellectual_genealogy"
    assert response.presentation.consumer_key == "transient-proof-probe"
    assert response.presentation.resolver_version == TRANSIENT_COMPOSE_RESOLVER_VERSION
    assert response.presentation.view_count == 1


def test_capability_engine_proxy_exposes_extraction_focus_for_view_generation() -> None:
    class _Registry:
        def get_capability_definition(self, engine_key):
            assert engine_key == "aoi_thematic_report"
            return SimpleNamespace(
                engine_key=engine_key,
                engine_name="AOI Thematic Report",
                problematique="Summarize the AOI findings.",
                researcher_question="What does the AOI result imply?",
                analytical_dimensions=[
                    SimpleNamespace(key="summary", description="Summary field"),
                    SimpleNamespace(key="implications", description="Implications field"),
                ],
                composability=SimpleNamespace(shares_with={"aoi_sin_findings": {}}),
                kind=SimpleNamespace(value="synthesis"),
                output_contract={"type": "object"},
            )

    proxy = _build_capability_engine_proxy(_Registry(), "aoi_thematic_report")

    assert proxy is not None
    assert proxy.extraction_focus == ["summary", "implications"]
    assert proxy.stage_context.extraction.key_fields == {
        "summary": "Summary field",
        "implications": "Implications field",
    }


def test_capability_engine_proxy_resolves_legacy_alias_through_capability_metadata() -> None:
    capability = SimpleNamespace(
        engine_key="genealogy_final_synthesis",
        legacy_engine_key="genealogy_pass7_final_synthesis",
        engine_name="Genealogy Final Synthesis",
        problematique="Synthesize the genealogy.",
        researcher_question="What does the genealogy show?",
        analytical_dimensions=[
            SimpleNamespace(key="summary", description="Summary field"),
        ],
        composability=SimpleNamespace(shares_with={"summary": "Summary field"}),
        kind=SimpleNamespace(value="genealogy"),
        output_contract={"type": "object"},
    )

    class _Registry:
        def get_capability_definition(self, _engine_key):
            return None

        def list_capability_definitions(self):
            return [capability]

    proxy = _build_capability_engine_proxy(
        _Registry(),
        "genealogy_pass7_final_synthesis",
    )

    assert proxy is not None
    assert proxy.engine_key == "genealogy_final_synthesis"
    assert proxy.engine_name == "Genealogy Final Synthesis"
    assert proxy.extraction_focus == ["summary"]


def test_view_generation_engine_prefers_capability_metadata_for_legacy_alias() -> None:
    capability = SimpleNamespace(
        engine_key="genealogy_final_synthesis",
        legacy_engine_key="genealogy_pass7_final_synthesis",
        engine_name="Genealogy Final Synthesis",
        problematique="Synthesize the genealogy.",
        researcher_question="What does the genealogy show?",
        analytical_dimensions=[
            SimpleNamespace(key="summary", description="Summary field"),
        ],
        composability=SimpleNamespace(shares_with={"summary": "Summary field"}),
        kind=SimpleNamespace(value="genealogy"),
        output_contract={"type": "object"},
    )
    legacy = SimpleNamespace(
        engine_key="genealogy_pass7_final_synthesis",
        engine_name="Legacy Genealogy Final Synthesis",
        description="Legacy JSON engine.",
        extraction_focus=["legacy_only"],
        canonical_schema={"legacy": True},
        stage_context=SimpleNamespace(
            extraction=SimpleNamespace(
                core_question="Legacy question",
                key_fields={"legacy": "Legacy field"},
                key_relationships=[],
                id_field="item_id",
                analysis_type="genealogy",
            )
        ),
    )

    class _Registry:
        def get(self, engine_key):
            if engine_key == "genealogy_pass7_final_synthesis":
                return legacy
            return None

        def get_capability_definition(self, _engine_key):
            return None

        def list_capability_definitions(self):
            return [capability]

    engine = _resolve_view_generation_engine(
        _Registry(),
        "genealogy_pass7_final_synthesis",
    )

    assert engine is not None
    assert engine.engine_key == "genealogy_final_synthesis"
    assert engine.engine_name == "Genealogy Final Synthesis"
    assert engine.extraction_focus == ["summary"]


def test_dynamic_prompt_engine_context_prefers_capability_metadata_for_legacy_alias(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from src.presenter.dynamic_prompt import _build_engine_context

    capability = SimpleNamespace(
        engine_key="genealogy_final_synthesis",
        legacy_engine_key="genealogy_pass7_final_synthesis",
        engine_name="Canonical Genealogy Final Synthesis",
        problematique="Canonical genealogy synthesis description.",
        researcher_question="What does the canonical genealogy synthesis reveal?",
        analytical_dimensions=[
            SimpleNamespace(key="summary", description="Summary field"),
        ],
        composability=SimpleNamespace(shares_with={"summary": "Summary field"}),
        kind=SimpleNamespace(value="genealogy"),
        output_contract={"type": "object"},
    )
    legacy = SimpleNamespace(
        engine_name="Legacy Engine Name",
        description="Legacy description",
        extraction_focus=["legacy_only"],
        canonical_schema={"legacy": True},
    )

    class _Registry:
        def get(self, engine_key):
            if engine_key == "genealogy_pass7_final_synthesis":
                return legacy
            return None

        def get_capability_definition(self, _engine_key):
            return None

        def list_capability_definitions(self):
            return [capability]

    monkeypatch.setattr(
        "src.engines.registry.get_engine_registry",
        lambda: _Registry(),
    )

    context = _build_engine_context("genealogy_pass7_final_synthesis")

    assert context["engine_name"] == "Canonical Genealogy Final Synthesis"
    assert context["extraction_focus"] == ["summary"]
    assert context["canonical_schema_text"].startswith("{")


def test_generate_view_definition_always_uses_save_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    async def _fake_generate_view(request):
        captured["request"] = request
        return ViewGenerateResponse(
            view=_raw_view(engine_key=request.engine_key, renderer_type="prose"),
            transformation_generated=False,
            notes="stub",
        )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.generate_view",
        _fake_generate_view,
    )

    result = _generate_view_definition(
        planner_row=_PlannerRow(
            section_index=0,
            pattern_key="prose_narrative",
            view_name="Narrative",
            description="Narrative view",
            presentation_stance="narrative",
            rationale="Keep it prose.",
        ),
        section=SimpleNamespace(
            engine_key="aoi_thematic_report",
            title="Report",
            prose="Report prose",
        ),
        planner_position=0,
        consumer_key="the-critic",
        workflow_key=AOI_WORKFLOW_KEY,
    )

    generated_request = captured["request"]
    assert generated_request.save is False
    assert generated_request.workflow_key == AOI_WORKFLOW_KEY
    assert generated_request.target_page == TRANSIENT_COMPOSE_TARGET_PAGE
    assert generated_request.target_app == "the-critic"
    assert generated_request.position == 1.0
    assert result.renderer_type == "prose"


def test_build_dynamic_transient_config_includes_renderer_config_and_schema(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "src.presenter.compose_from_intent.compose_dynamic_extraction_prompt",
        lambda engine_key, renderer_type, stance_key=None: {
            "system_prompt": "base prompt",
            "transformation_type": "llm_extract",
            "model": "model-a",
            "model_fallback": "model-b",
            "max_tokens": 1234,
        },
    )

    config = _build_dynamic_transient_config(
        engine_key="aoi_sin_findings",
        renderer_type="card_grid",
        renderer_config={"title_field": "title", "columns": 2},
        pattern_key="card_grid_simple",
        stance_key="evidence",
        renderer_input_schema={"type": "array"},
    )

    assert "card_grid_simple" in config["system_prompt"]
    assert '"columns": 2' in config["system_prompt"]
    assert '"type": "array"' in config["system_prompt"]
    assert config["source"] == "compose_from_intent_dynamic"


def test_normalize_card_grid_contract_shape_extracts_array_groups_from_items_path() -> None:
    normalized = _normalize_card_grid_contract_shape(
        structured_data={
            "report_sections": {
                "summary": "Narrative header",
                "key_divergences": [{"title": "A"}],
                "sin_distribution": [{"sin_type": "Appropriation"}],
            }
        },
        renderer_config={
            "items_path": "report_sections",
            "group_by": "section_type",
            "columns": 2,
        },
    )

    assert normalized == {
        "structured_data": {
            "key_divergences": [{"title": "A"}],
            "sin_distribution": [{"sin_type": "Appropriation"}],
        },
        "renderer_config": {
            "group_by": "_category",
            "columns": 2,
        },
    }


def test_recursive_consumer_adaptation_reaches_children(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    parent = _payload(
        view_key="parent",
        renderer_type="tab",
        structured_data={"child": {"label": "Child"}},
        children=[
            _payload(
                view_key="child",
                renderer_type="card_grid",
                structured_data={"report_sections": {"rows": [{"title": "A"}]}},
                renderer_config={"items_path": "report_sections"},
            )
        ],
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.adapt_renderer_for_consumer",
        lambda renderer_type, renderer_config, consumer_key: (
            renderer_type,
            {**renderer_config, "adapted_for": consumer_key},
            {"consumer_key": consumer_key},
        ),
    )

    adapted, details = _adapt_payloads_for_consumer([parent], consumer_key="the-critic")

    assert adapted[0].renderer_config["adapted_for"] == "the-critic"
    assert adapted[0].children[0].renderer_config["adapted_for"] == "the-critic"
    assert [entry["view_key"] for entry in details] == ["child", "parent"]


def test_recursive_served_payload_normalization_reaches_children() -> None:
    payload = _payload(
        view_key="parent",
        renderer_type="tab",
        structured_data={"child": {"label": "Child"}},
        children=[
            _payload(
                view_key="child",
                renderer_type="card_grid",
                structured_data={
                    "report_sections": {
                        "rows": [{"title": "A"}],
                        "groups": [{"title": "B"}],
                    }
                },
                renderer_config={"items_path": "report_sections"},
            )
        ],
    )

    _normalize_transient_served_payloads([payload])

    assert payload.children[0].structured_data == {
        "rows": [{"title": "A"}],
        "groups": [{"title": "B"}],
    }
    assert payload.children[0].renderer_config["group_by"] == "_category"


def test_transient_presentation_hash_and_count_include_children() -> None:
    first = _build_transient_presentation(
        workflow_key=AOI_WORKFLOW_KEY,
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        resolver_version=TRANSIENT_COMPOSE_RESOLVER_VERSION,
        views=[
            TransientIntentView(
                view_key="parent",
                view_name="Parent",
                description="Parent",
                renderer_type="tab",
                renderer_config={},
                presentation_stance="summary",
                rationale="because",
                engine_key=None,
                position=1.0,
                visibility="if_data_exists",
                has_structured_data=True,
                structured_data={"child": {"label": "Child"}},
                items=None,
                children=[
                    TransientIntentView(
                        view_key="child",
                        view_name="Child",
                        description="Child",
                        renderer_type="prose",
                        renderer_config={},
                        presentation_stance="narrative",
                        rationale="because",
                        engine_key="aoi_thematic_report",
                        position=1.0,
                        visibility="if_data_exists",
                        has_structured_data=True,
                        structured_data="child body",
                        items=None,
                        children=[],
                    )
                ],
            )
        ],
    )
    second = _build_transient_presentation(
        workflow_key=AOI_WORKFLOW_KEY,
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        resolver_version=TRANSIENT_COMPOSE_RESOLVER_VERSION,
        views=[
            TransientIntentView(
                view_key="parent",
                view_name="Parent",
                description="Parent",
                renderer_type="tab",
                renderer_config={},
                presentation_stance="summary",
                rationale="because",
                engine_key=None,
                position=1.0,
                visibility="if_data_exists",
                has_structured_data=True,
                structured_data={"child": {"label": "Child"}},
                items=None,
                children=[
                    TransientIntentView(
                        view_key="child",
                        view_name="Child",
                        description="Child",
                        renderer_type="accordion",
                        renderer_config={},
                        presentation_stance="narrative",
                        rationale="because",
                        engine_key="aoi_thematic_report",
                        position=1.0,
                        visibility="if_data_exists",
                        has_structured_data=True,
                        structured_data="child body",
                        items=None,
                        children=[],
                    )
                ],
            )
        ],
    )

    assert first.view_count == 2
    assert first.presentation_hash != second.presentation_hash


def test_transient_presentation_hash_includes_first_hop_affordance_but_content_hash_does_not() -> None:
    first = _build_transient_presentation(
        workflow_key=AOI_WORKFLOW_KEY,
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        resolver_version=TRANSIENT_COMPOSE_RESOLVER_VERSION,
        views=[
            TransientIntentView(
                view_key="leaf",
                view_name="Leaf",
                description="Leaf",
                renderer_type="prose",
                renderer_config={},
                presentation_stance="summary",
                rationale="because",
                engine_key="aoi_thematic_report",
                position=1.0,
                visibility="if_data_exists",
                has_structured_data=True,
                structured_data="body",
                items=None,
                first_hop_affordance=FirstHopAffordance(
                    capturable=True,
                    allowed_destinations=["arsenal", "research_todo"],
                ),
                children=[],
            )
        ],
    )
    second = _build_transient_presentation(
        workflow_key=AOI_WORKFLOW_KEY,
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        resolver_version=TRANSIENT_COMPOSE_RESOLVER_VERSION,
        views=[
            TransientIntentView(
                view_key="leaf",
                view_name="Leaf",
                description="Leaf",
                renderer_type="prose",
                renderer_config={},
                presentation_stance="summary",
                rationale="because",
                engine_key="aoi_thematic_report",
                position=1.0,
                visibility="if_data_exists",
                has_structured_data=True,
                structured_data="body",
                items=None,
                first_hop_affordance=None,
                children=[],
            )
        ],
    )

    assert first.presentation_hash != second.presentation_hash
    assert first.presentation_content_hash == second.presentation_content_hash


def test_transient_presentation_hash_ignores_unset_specialized_family() -> None:
    first = _build_transient_presentation(
        workflow_key=AOI_WORKFLOW_KEY,
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        resolver_version=TRANSIENT_COMPOSE_RESOLVER_VERSION,
        views=[
            TransientIntentView(
                view_key="leaf",
                view_name="Leaf",
                description="Leaf",
                renderer_type="prose",
                renderer_config={},
                presentation_stance="summary",
                rationale="because",
                engine_key="aoi_thematic_report",
                position=1.0,
                visibility="if_data_exists",
                has_structured_data=True,
                structured_data="body",
                items=None,
                first_hop_affordance=FirstHopAffordance(
                    capturable=True,
                    allowed_destinations=["arsenal", "research_todo"],
                ),
                children=[],
            )
        ],
    )
    second = _build_transient_presentation(
        workflow_key=AOI_WORKFLOW_KEY,
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        resolver_version=TRANSIENT_COMPOSE_RESOLVER_VERSION,
        views=[
            TransientIntentView(
                view_key="leaf",
                view_name="Leaf",
                description="Leaf",
                renderer_type="prose",
                renderer_config={},
                presentation_stance="summary",
                rationale="because",
                engine_key="aoi_thematic_report",
                position=1.0,
                visibility="if_data_exists",
                has_structured_data=True,
                structured_data="body",
                items=None,
                first_hop_affordance=FirstHopAffordance(
                    capturable=True,
                    allowed_destinations=["arsenal", "research_todo"],
                    specialized_family=None,
                ),
                children=[],
            )
        ],
    )

    assert first.presentation_hash == second.presentation_hash
    assert first.presentation_content_hash == second.presentation_content_hash


def test_compose_from_intent_endpoint_maps_dependency_unavailable_to_503(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import asyncio

    from src.api.routes.presenter import compose_from_intent_endpoint

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.compose_from_intent",
        lambda request: (_ for _ in ()).throw(
            ComposeFromIntentDependencyUnavailable("LLM service unavailable")
        ),
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(compose_from_intent_endpoint(_request().model_dump()))

    assert excinfo.value.status_code == 503
    assert "LLM service unavailable" in str(excinfo.value.detail)


def test_compose_from_intent_endpoint_maps_upstream_failure_to_502(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import asyncio

    from src.api.routes.presenter import compose_from_intent_endpoint

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.compose_from_intent",
        lambda request: (_ for _ in ()).throw(
            ComposeFromIntentUpstreamError("planner returned bad JSON")
        ),
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(compose_from_intent_endpoint(_request().model_dump()))

    assert excinfo.value.status_code == 502
    assert "bad JSON" in str(excinfo.value.detail)


def test_compose_from_intent_endpoint_maps_wrapped_transport_failure_to_500(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import asyncio

    from src.api.routes.presenter import compose_from_intent_endpoint

    def _fail(request):
        try:
            raise httpx.ConnectError("network down")
        except httpx.ConnectError as exc:
            raise RuntimeError("transport failed") from exc

    monkeypatch.setattr("src.presenter.compose_from_intent.compose_from_intent", _fail)

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(compose_from_intent_endpoint(_request().model_dump()))

    assert excinfo.value.status_code == 500
    assert "transport failed" in str(excinfo.value.detail)


def test_compose_from_intent_endpoint_maps_contract_failure_to_409(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import asyncio

    from src.api.routes.presenter import compose_from_intent_endpoint

    issue = CompositionIssue(
        view_key="compose_intent_01_aoi_thematic_report",
        field="structured_data",
        message="invalid shape",
        reason="renderer_data_validation_failed",
    )
    monkeypatch.setattr(
        "src.presenter.compose_from_intent.compose_from_intent",
        lambda request: (_ for _ in ()).throw(
            BoundedCompositionValidationError([issue])
        ),
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(compose_from_intent_endpoint(_request().model_dump()))

    assert excinfo.value.status_code == 409
    assert excinfo.value.detail["issues"][0]["reason"] == "renderer_data_validation_failed"


def test_compose_from_source_endpoint_maps_source_resolution_failure_to_409(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import asyncio

    from src.api.routes.presenter import compose_from_source_endpoint

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.compose_from_source",
        lambda request: (_ for _ in ()).throw(
            ComposeFromSourceResolutionError("missing required thematic report output")
        ),
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(compose_from_source_endpoint(_source_request().model_dump()))

    assert excinfo.value.status_code == 409
    assert "thematic report" in str(excinfo.value.detail)


def test_compose_from_selection_endpoint_maps_source_resolution_failure_to_409(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import asyncio

    from src.api.routes.presenter import compose_from_selection_endpoint

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.compose_from_selection",
        lambda request: (_ for _ in ()).throw(
            ComposeFromSourceResolutionError("selection referenced missing source family")
        ),
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(compose_from_selection_endpoint(_selection_request().model_dump()))

    assert excinfo.value.status_code == 409
    assert "missing source family" in str(excinfo.value.detail)


# ---------------------------------------------------------------------------
# Regression: source-family preservation for compose-from-selection
# ---------------------------------------------------------------------------


def _four_family_artifact_thematic_synthesis() -> dict[str, object]:
    """Realistic minimal AOI thematic synthesis artifact payload."""
    return {
        "themes": [
            {"theme_name": "Planning", "claim_count": 3},
            {"theme_name": "Calculation", "claim_count": 2},
        ],
        "source_documents": [
            {"title": "In-Kind", "role": "primary"},
        ],
        "selected_source_thinker": {
            "id": "otto_neurath",
            "name": "Otto Neurath",
        },
    }


def _four_family_artifact_engagement_mapping() -> dict[str, object]:
    """Realistic minimal AOI engagement mapping artifact payload."""
    return {
        "engagements": [
            {"theme": "Planning", "engagement_type": "adoption"},
        ],
    }


def _four_family_artifact_sin_findings() -> dict[str, object]:
    """Realistic minimal AOI sin findings artifact payload."""
    return {
        "findings_overview": {
            "total_findings": 3,
            "dominant_sin_type": "selective_borrowing",
        },
        "severity_classification": [
            {"finding_id": "f1", "severity": "high"},
        ],
        "target_provenance": [
            {"finding_id": "f1", "target_passage": "..."},
        ],
        "source_provenance": [
            {"finding_id": "f1", "source_passage": "..."},
        ],
        "discrepancy_and_consequence": [
            {"finding_id": "f1", "consequence": "..."},
        ],
    }


def _four_family_report_payload() -> dict[str, object]:
    """Realistic minimal AOI report payload."""
    return {
        "report_sections": {
            "summary": "Summary text.",
            "implications": "Implications text.",
        },
    }


def _accordion_view_for_engine(
    engine_key: str,
    section_keys: list[str],
) -> ViewDefinition:
    """Build an accordion view definition whose section_renderers reference the given keys."""
    return ViewDefinition(
        view_key="raw_generated_key",
        view_name="Raw View",
        description="Raw description",
        target_app="other-app",
        target_page="wrong_page",
        renderer_type="accordion",
        renderer_config={
            "sections": [{"key": k, "title": k.replace("_", " ").title()} for k in section_keys],
            "expand_first": True,
            "section_renderers": {
                k: {"renderer_type": "prose_block", "config": {}}
                for k in section_keys
            },
        },
        data_source=DataSourceRef(
            workflow_key=AOI_WORKFLOW_KEY,
            phase_number=1.0,
            engine_key=engine_key,
            result_path="",
            scope="aggregated",
        ),
        transformation=TransformationSpec(type="llm_extract"),
        presentation_stance="diagnostic",
        position=99.0,
        parent_view_key="bad_parent",
        visibility="always",
        status="active",
        generation_mode="generated",
    )


def _card_grid_view_for_engine(engine_key: str) -> ViewDefinition:
    """Build a card_grid view definition for engagement mapping."""
    return ViewDefinition(
        view_key="raw_generated_key",
        view_name="Raw View",
        description="Raw description",
        target_app="other-app",
        target_page="wrong_page",
        renderer_type="card_grid",
        renderer_config={
            "card_fields": ["theme", "engagement_type"],
        },
        data_source=DataSourceRef(
            workflow_key=AOI_WORKFLOW_KEY,
            phase_number=1.0,
            engine_key=engine_key,
            result_path="",
            scope="aggregated",
        ),
        transformation=TransformationSpec(type="llm_extract"),
        presentation_stance="diagnostic",
        position=99.0,
        parent_view_key="bad_parent",
        visibility="always",
        status="active",
        generation_mode="generated",
    )


def test_source_family_preservation_skips_llm_extraction_for_accordion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Source-family-backed sections with parsable JSON skip LLM extraction."""
    from src.presenter.compose_from_intent import (
        _PlannerRow,
        _transform_section_prose,
    )

    artifact = _four_family_artifact_thematic_synthesis()
    import json

    prose_json = json.dumps(artifact, sort_keys=True, ensure_ascii=False)
    section = SimpleNamespace(
        engine_key="aoi_thematic_synthesis",
        title="Thematic Synthesis",
        prose=prose_json,
    )
    view_def = _accordion_view_for_engine(
        "aoi_thematic_synthesis",
        section_keys=["themes", "source_documents", "selected_source_thinker"],
    )
    planner_row = _PlannerRow(
        section_index=0,
        pattern_key="accordion_sections",
        view_name="Thematic Synthesis",
        description="Structured thematic synthesis.",
        presentation_stance="summary",
        rationale="test",
        semantic_role="synthesis_primary",
        source_family_key="thematic_synthesis",
    )

    transformed_data, meta = _transform_section_prose(
        section=section,
        view_def=view_def,
        planner_row=planner_row,
        executor=None,  # should not be used
    )

    assert meta["extraction_source"] == "source_family_preserved"
    assert meta["source_family_key"] == "thematic_synthesis"
    assert isinstance(transformed_data, dict)
    assert "themes" in transformed_data
    assert "source_documents" in transformed_data
    assert "selected_source_thinker" in transformed_data
    assert transformed_data["themes"] == artifact["themes"]
    assert view_def.transformation.type == "none"


def test_source_family_preservation_reconciles_stale_section_renderers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Section_renderers keys not in structured_data are removed by reconciliation."""
    from src.presenter.compose_from_intent import (
        _PlannerRow,
        _transform_section_prose,
    )

    artifact = {"themes": [{"theme_name": "Planning"}]}
    import json

    prose_json = json.dumps(artifact, sort_keys=True, ensure_ascii=False)
    section = SimpleNamespace(
        engine_key="aoi_thematic_synthesis",
        title="Thematic Synthesis",
        prose=prose_json,
    )
    view_def = _accordion_view_for_engine(
        "aoi_thematic_synthesis",
        section_keys=["themes", "nonexistent_key", "also_missing"],
    )
    planner_row = _PlannerRow(
        section_index=0,
        pattern_key="accordion_sections",
        view_name="Thematic Synthesis",
        description="Structured thematic synthesis.",
        presentation_stance="summary",
        rationale="test",
        semantic_role="synthesis_primary",
        source_family_key="thematic_synthesis",
    )

    transformed_data, meta = _transform_section_prose(
        section=section,
        view_def=view_def,
        planner_row=planner_row,
        executor=None,
    )

    assert meta["extraction_source"] == "source_family_preserved"
    section_renderers = view_def.renderer_config["section_renderers"]
    assert "themes" in section_renderers
    assert "nonexistent_key" not in section_renderers
    assert "also_missing" not in section_renderers
    sections_keys = [s["key"] for s in view_def.renderer_config["sections"]]
    assert "themes" in sections_keys
    assert "nonexistent_key" not in sections_keys


def test_source_family_preservation_sin_findings_contract_valid(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Sin-findings preserved artifact produces contract-valid payload."""
    from src.presenter.compose_from_intent import (
        _PlannerRow,
        _build_transient_payload,
        _transform_section_prose,
    )
    from src.presenter.renderer_contract_enforcement import (
        collect_served_payload_contract_issues,
    )

    artifact = _four_family_artifact_sin_findings()
    sin_keys = list(artifact.keys())
    import json

    prose_json = json.dumps(artifact, sort_keys=True, ensure_ascii=False)
    section = SimpleNamespace(
        engine_key="aoi_sin_findings",
        title="Sin Findings",
        prose=prose_json,
    )
    view_def = _accordion_view_for_engine("aoi_sin_findings", section_keys=sin_keys)
    planner_row = _PlannerRow(
        section_index=0,
        pattern_key="accordion_sections",
        view_name="Sin Findings",
        description="Structured findings bank.",
        presentation_stance="evidence",
        rationale="test",
        semantic_role="findings_bank",
        source_family_key="sin_findings",
    )

    transformed_data, meta = _transform_section_prose(
        section=section,
        view_def=view_def,
        planner_row=planner_row,
        executor=None,
    )

    payload = _build_transient_payload(
        view_def=view_def,
        planner_row=planner_row,
        section=section,
        planner_position=2,
        transformed_data=transformed_data,
    )

    issues = collect_served_payload_contract_issues([payload], consumer_key="the-critic")
    section_data_issues = [
        i for i in issues
        if i.reason == "section_renderer_missing_structured_data_key"
    ]
    assert section_data_issues == [], (
        f"Sin-findings preserved data still has section_renderer alignment issues: "
        f"{[i.message for i in section_data_issues]}"
    )


def test_compose_from_selection_four_family_evolution_ready_contract_valid(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Full four-family compose-from-selection with preserved source data passes contract."""
    import json

    from src.presenter.compose_from_intent import _reconcile_renderer_config_with_data

    thematic = _four_family_artifact_thematic_synthesis()
    engagement = _four_family_artifact_engagement_mapping()
    sin = _four_family_artifact_sin_findings()
    report = _four_family_report_payload()

    bridge = SimpleNamespace(
        catalog=SimpleNamespace(to_trace_dict=lambda: {"candidates": []}),
        selection=SimpleNamespace(
            to_trace_dict=lambda: {"selected": [], "selection_summary": "all four"},
        ),
        materialized_sections=[
            CompositionMaterializedSection(
                source_family_key="thematic_synthesis",
                engine_key="aoi_thematic_synthesis",
                title="Thematic Synthesis",
                materialization_position=1,
                profile=None,
                composition_role_hint="synthesis_primary",
                section=SimpleNamespace(
                    model_dump=lambda payload=thematic: {
                        "engine_key": "aoi_thematic_synthesis",
                        "title": "Thematic Synthesis",
                        "prose": json.dumps(payload, sort_keys=True, ensure_ascii=False),
                    }
                ),
            ),
            CompositionMaterializedSection(
                source_family_key="engagement_mapping",
                engine_key="aoi_engagement_mapping",
                title="Engagement Mapping",
                materialization_position=2,
                profile=None,
                composition_role_hint="comparison_map",
                section=SimpleNamespace(
                    model_dump=lambda payload=engagement: {
                        "engine_key": "aoi_engagement_mapping",
                        "title": "Engagement Mapping",
                        "prose": json.dumps(payload, sort_keys=True, ensure_ascii=False),
                    }
                ),
            ),
            CompositionMaterializedSection(
                source_family_key="sin_findings",
                engine_key="aoi_sin_findings",
                title="Sin Findings",
                materialization_position=3,
                profile=None,
                composition_role_hint="findings_bank",
                section=SimpleNamespace(
                    model_dump=lambda payload=sin: {
                        "engine_key": "aoi_sin_findings",
                        "title": "Sin Findings",
                        "prose": json.dumps(payload, sort_keys=True, ensure_ascii=False),
                    }
                ),
            ),
            CompositionMaterializedSection(
                source_family_key="thematic_report",
                engine_key="aoi_thematic_report",
                title="AOI Report",
                materialization_position=4,
                profile=None,
                composition_role_hint="report_closeout",
                section=SimpleNamespace(
                    model_dump=lambda payload=report: {
                        "engine_key": "aoi_thematic_report",
                        "title": "AOI Report",
                        "prose": json.dumps(payload, sort_keys=True, ensure_ascii=False),
                    }
                ),
            ),
        ],
    )

    monkeypatch.setattr(
        "src.presenter.compose_from_intent.build_selection_composition_bridge",
        lambda **kwargs: bridge,
    )

    view_dispatch = {
        "accordion_sections": lambda engine_key, section_keys: _accordion_view_for_engine(
            engine_key, section_keys
        ),
        "card_grid_grouped": lambda engine_key, **kw: _card_grid_view_for_engine(engine_key),
        "prose_narrative": lambda engine_key, **kw: _raw_view(
            engine_key=engine_key, renderer_type="prose"
        ),
    }

    def _fake_generate(planner_row, section, planner_position, consumer_key, workflow_key):
        pattern_key = planner_row.pattern_key
        engine_key = section.engine_key
        if pattern_key == "accordion_sections":
            artifact_source = {
                "aoi_thematic_synthesis": thematic,
                "aoi_sin_findings": sin,
            }[engine_key]
            return _accordion_view_for_engine(engine_key, list(artifact_source.keys()))
        if pattern_key == "card_grid_grouped":
            return _card_grid_view_for_engine(engine_key)
        return _raw_view(engine_key=engine_key, renderer_type="prose")

    monkeypatch.setattr(
        "src.presenter.compose_from_intent._generate_view_definition",
        _fake_generate,
    )

    request = ComposeFromSelectionRequest.model_validate(
        {
            "workflow_key": AOI_WORKFLOW_KEY,
            "consumer_key": "the-critic",
            "source_v2_job_id": "v2-job-evolution-ready",
            "user_intent": "Show how Benanav uses Neurath's planning argument across the corpus.",
            "selection": [
                {"source_family_key": "thematic_synthesis", "selection_rank": 1, "rationale": "Lead."},
                {"source_family_key": "engagement_mapping", "selection_rank": 2, "rationale": "Map."},
                {"source_family_key": "sin_findings", "selection_rank": 3, "rationale": "Evidence."},
                {"source_family_key": "thematic_report", "selection_rank": 4, "rationale": "Close."},
            ],
        }
    )

    response = compose_from_selection(request)

    assert response.presentation is not None
    assert response.presentation.resolver_version == TRANSIENT_COMPOSE_SELECTION_RESOLVER_VERSION

    # Find the transformation_execution trace to verify preservation
    transform_entry = next(
        (e for e in response.trace.entries if e.stage == "transformation_execution"),
        None,
    )
    assert transform_entry is not None
    extraction_sources = {
        v["engine_key"]: v["extraction_source"]
        for v in transform_entry.details["views"]
    }
    assert extraction_sources["aoi_thematic_synthesis"] == "source_family_preserved"
    assert extraction_sources["aoi_sin_findings"] == "source_family_preserved"
    assert extraction_sources["aoi_thematic_report"] == "passthrough"

    # Contract enforcement passed (no BoundedCompositionValidationError raised)
    contract_entry = next(
        (e for e in response.trace.entries if e.stage == "contract_validation"),
        None,
    )
    assert contract_entry is not None
    assert contract_entry.details["issues"] == 0
