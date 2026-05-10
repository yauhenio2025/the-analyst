import asyncio

from fastapi import HTTPException

from src.api.routes.engines import (
    get_capability_definition,
    get_capability_history,
    get_engine,
    get_engine_count,
    list_engine_keys,
    list_engines,
)
from src.api.routes.operationalizations import (
    ComposePreviewRequest,
    compose_preview,
    get_operationalization,
)
from src.api.routes.workflows import get_workflow_phase_prompt


def test_list_engines_includes_capability_only_and_canonical_hybrid_keys():
    rows = asyncio.run(list_engines(None, None, None, None, None))
    keys = [row.engine_key for row in rows]

    assert "aoi_thematic_synthesis" in keys
    assert "genealogy_final_synthesis" in keys
    assert "genealogy_pass7_final_synthesis" not in keys
    assert keys.count("concept_synthesis") == 1


def test_engine_key_and_count_surfaces_share_the_merged_discoverable_set():
    keys = asyncio.run(list_engine_keys())
    count = asyncio.run(get_engine_count())

    assert "aoi_thematic_report" in keys
    assert "genealogy_pass7_final_synthesis" not in keys
    assert count["count"] == len(keys)


def test_function_filter_uses_capability_metadata_for_aoi_engines():
    influence_rows = asyncio.run(list_engines(None, None, None, "influence", None))
    influence_keys = {row.engine_key for row in influence_rows}

    assert {
        "aoi_thematic_synthesis",
        "aoi_engagement_mapping",
        "aoi_sin_findings",
        "aoi_thematic_report",
    }.issubset(influence_keys)


def test_capability_definition_and_history_are_alias_aware():
    cap_def = asyncio.run(get_capability_definition("genealogy_pass7_final_synthesis"))
    history = asyncio.run(get_capability_history("genealogy_pass7_final_synthesis", limit=1))

    assert cap_def.engine_key == "genealogy_final_synthesis"
    assert history["engine_key"] == "genealogy_final_synthesis"


def test_operationalization_lookup_is_alias_aware_for_hybrid_engines():
    op = asyncio.run(get_operationalization("genealogy_pass7_final_synthesis"))
    preview = asyncio.run(
        compose_preview(
            "genealogy_pass7_final_synthesis",
            ComposePreviewRequest(depth_key="surface", pass_number=1),
        )
    )

    assert op.engine_key == "genealogy_final_synthesis"
    assert preview.engine_key == "genealogy_final_synthesis"
    assert preview.pass_number == 1


def test_legacy_detail_404_points_capability_only_keys_to_capability_definition():
    try:
        asyncio.run(get_engine("aoi_thematic_synthesis"))
    except HTTPException as exc:
        assert exc.status_code == 404
        assert "/v1/engines/aoi_thematic_synthesis/capability-definition" in exc.detail
    else:
        raise AssertionError("Expected capability-only legacy detail lookup to fail")


def test_workflow_prompt_preview_supports_capability_only_and_chain_phases():
    aoi_preview = asyncio.run(
        get_workflow_phase_prompt(
            "anxiety_of_influence_thematic_single_thinker",
            1.0,
            "analyst",
        )
    )
    chain_preview = asyncio.run(
        get_workflow_phase_prompt(
            "intellectual_genealogy",
            1.0,
            "analyst",
        )
    )

    assert aoi_preview["prompt_type"] == "capability"
    assert aoi_preview["engine_key"] == "aoi_thematic_synthesis"
    assert isinstance(aoi_preview["prompt"], str) and aoi_preview["prompt"]

    assert chain_preview["prompt_type"] == "chain"
    assert isinstance(chain_preview["prompt"], str) and chain_preview["prompt"]
    assert len(chain_preview["engine_prompts"]) >= 1
