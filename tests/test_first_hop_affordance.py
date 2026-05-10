from __future__ import annotations

from src.presenter.first_hop_affordance import derive_first_hop_affordance
from src.presenter.schemas import FirstHopAffordance, ViewPayload


def _leaf_payload(
    *,
    view_key: str,
    engine_key: str | None,
    children: list[ViewPayload] | None = None,
) -> ViewPayload:
    return ViewPayload(
        view_key=view_key,
        view_name=view_key.replace("_", " ").title(),
        description="",
        renderer_type="tab",
        renderer_config={},
        presentation_stance="diagnostic",
        priority="primary",
        rationale="",
        data_quality="standard",
        source_parent_view_key=None,
        phase_number=1.0,
        engine_key=engine_key,
        chain_key=None,
        scope="aggregated",
        has_structured_data=True,
        structured_data={"summary": f"content for {view_key}"},
        reading_scaffold=None,
        raw_prose=None,
        prose_ref_view_key=None,
        items=None,
        tab_count=None,
        visibility="if_data_exists",
        position=1.0,
        children=children or [],
    )


def test_derive_first_hop_affordance_emits_generic_affordance_for_genealogy_idea_evolution_leaf() -> None:
    payload = _leaf_payload(
        view_key="genealogy_idea_evolution",
        engine_key="concept_synthesis",
    )

    affordance = derive_first_hop_affordance(payload, enabled=True)

    assert affordance == FirstHopAffordance(
        capturable=True,
        allowed_destinations=["arsenal", "research_todo"],
    )


def test_derive_first_hop_affordance_fails_closed_for_non_matching_genealogy_idea_evolution_cases() -> None:
    child = _leaf_payload(
        view_key="genealogy_idea_evolution_child",
        engine_key="concept_synthesis",
    )

    cases = [
        (
            _leaf_payload(
                view_key="genealogy_relationship_landscape",
                engine_key="concept_synthesis",
            ),
            True,
        ),
        (
            _leaf_payload(
                view_key="genealogy_idea_evolution",
                engine_key="custom_inventory_index",
            ),
            True,
        ),
        (
            _leaf_payload(
                view_key="genealogy_idea_evolution",
                engine_key="concept_synthesis",
                children=[child],
            ),
            True,
        ),
        (
            _leaf_payload(
                view_key="genealogy_idea_evolution",
                engine_key="concept_synthesis",
            ),
            False,
        ),
    ]

    for payload, enabled in cases:
        assert derive_first_hop_affordance(payload, enabled=enabled) is None
