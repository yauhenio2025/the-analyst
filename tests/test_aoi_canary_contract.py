import json
from pathlib import Path

from src.presenter.composition_resolver import resolve_effective_render_contract
from src.presenter.manifest_builder import adapt_renderer_for_consumer
from src.views.registry import get_view_registry


ROOT = Path(__file__).resolve().parents[1]
CONSUMER_PATH = ROOT / "src" / "consumers" / "definitions" / "aoi-canary.json"
PHASE_E_TRANSIENT_PROOF_PATH = (
    ROOT / "communications" / "PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json"
)
PHASE_E_SOURCE_PROFILE_TRANSIENT_PROOF_PATH = (
    ROOT
    / "communications"
    / "PROOF_phase_e_transient_second_consumer_aoi_canary_source_profile_dossier_2026-03-31.json"
)
PHASE_E_SOURCE_PROFILE_COMPARISON_TRANSIENT_PROOF_PATH = (
    ROOT
    / "communications"
    / "PROOF_phase_e_transient_second_consumer_aoi_canary_source_profile_comparison_2026-03-31.json"
)
PHASE_E_GENEALOGY_DIRECT_SECTIONS_TRANSIENT_PROOF_PATH = (
    ROOT
    / "communications"
    / "PROOF_phase_e_transient_second_consumer_aoi_canary_genealogy_direct_sections_2026-03-31.json"
)

EXPECTED_VIEW_RENDERERS = {
    "aoi_thematic_analysis": "tab",
    "aoi_source_documents": "card_grid",
    "aoi_by_theme": "accordion",
    "aoi_by_sin_type": "card_grid",
    "aoi_thematic_report": "accordion",
}

EXPECTED_REPORT_SECTION_RENDERERS = {
    "summary": "annotated_prose",
    "engagement_pattern": "annotated_prose",
    "key_divergences": "mini_card_list",
    "sin_distribution": "mini_card_list",
    "reading_implications": "annotated_prose",
}

EXPECTED_THEME_DEFAULT_SUB_RENDERERS = {
    "overview": "annotated_prose",
    "engagement": "annotated_prose",
    "key_claims": "rich_description_list",
    "philosophical_commitments": "rich_description_list",
    "argumentative_moves": "rich_description_list",
    "source_documents": "chip_grid",
    "findings": "mini_card_list",
}


def _supported_contracts() -> set[str]:
    consumer = json.loads(CONSUMER_PATH.read_text(encoding="utf-8"))
    return set(consumer["supported_renderers"]) | set(consumer["supported_sub_renderers"])


def _load_phase_e_transient_proof() -> dict[str, object]:
    return json.loads(PHASE_E_TRANSIENT_PROOF_PATH.read_text(encoding="utf-8"))


def _load_phase_e_source_profile_transient_proof() -> dict[str, object]:
    return json.loads(PHASE_E_SOURCE_PROFILE_TRANSIENT_PROOF_PATH.read_text(encoding="utf-8"))


def _load_phase_e_source_profile_comparison_transient_proof() -> dict[str, object]:
    return json.loads(PHASE_E_SOURCE_PROFILE_COMPARISON_TRANSIENT_PROOF_PATH.read_text(encoding="utf-8"))


def _load_phase_e_genealogy_direct_sections_transient_proof() -> dict[str, object]:
    return json.loads(PHASE_E_GENEALOGY_DIRECT_SECTIONS_TRANSIENT_PROOF_PATH.read_text(encoding="utf-8"))


def test_aoi_canary_supports_pinned_neurath_aoi_surface_without_raw_json_adaptation():
    supported = _supported_contracts()
    view_registry = get_view_registry()

    for view_key, expected_renderer in EXPECTED_VIEW_RENDERERS.items():
        view_def = view_registry.get(view_key)
        effective = resolve_effective_render_contract(
            view_def=view_def,
            rec={},
            consumer_key="aoi-canary",
            view_registry=view_registry,
        )
        renderer_type, renderer_config, _ = adapt_renderer_for_consumer(
            renderer_type=effective.renderer_type,
            renderer_config=effective.renderer_config,
            consumer_key="aoi-canary",
        )

        assert renderer_type == expected_renderer
        assert renderer_type in supported
        assert renderer_type != "raw_json"

        if view_key == "aoi_by_theme":
            default_section = (renderer_config.get("section_renderers") or {}).get("_default") or {}
            actual_sub_renderers = {
                field_key: spec.get("renderer_type")
                for field_key, spec in (default_section.get("sub_renderers") or {}).items()
                if isinstance(spec, dict)
            }
            assert actual_sub_renderers == EXPECTED_THEME_DEFAULT_SUB_RENDERERS
            assert set(actual_sub_renderers.values()) <= supported

        if view_key == "aoi_by_sin_type":
            assert renderer_config.get("group_by") == "_category"
            assert renderer_config.get("group_style_map") == "sin_type"
            assert renderer_config.get("columns") == 1

        if view_key == "aoi_source_documents":
            assert renderer_config.get("expandable") is False

        if view_key != "aoi_thematic_report":
            continue

        actual_sections = {
            section_key: spec.get("renderer_type")
            for section_key, spec in (renderer_config.get("section_renderers") or {}).items()
            if isinstance(spec, dict)
        }
        assert actual_sections == EXPECTED_REPORT_SECTION_RENDERERS
        assert set(actual_sections.values()) <= supported


def test_aoi_canary_transient_source_selection_proof_stays_within_bounded_raw_json_fallback():
    proof = _load_phase_e_transient_proof()
    response = proof["response_json"]
    presentation = response["presentation"]
    root_view = presentation["views"][0]
    leaf_views = root_view["children"]
    raw_json_leaf_keys = [
        view["view_key"]
        for view in leaf_views
        if not view.get("children") and view.get("renderer_type") == "raw_json"
    ]

    assert proof["consumer_key"] == "aoi-canary"
    assert proof["request_json"]["consumer_key"] == "aoi-canary"
    assert proof["consumer_adaptation_truth"]["root_renderer_type"] == "tab"
    assert root_view["renderer_type"] == "tab"
    assert raw_json_leaf_keys == ["compose_intent_04_aoi_thematic_report"]
    assert proof["consumer_adaptation_truth"]["raw_json_leaf_count"] == 1
    assert proof["consumer_adaptation_truth"]["raw_json_leaf_keys"] == raw_json_leaf_keys
    adapted_views = [
        entry["view_key"]
        for entry in proof["consumer_adaptation_truth"]["adaptation_details"]
        if entry["adapted"]
    ]
    assert adapted_views == ["compose_intent_04_aoi_thematic_report"]


def test_aoi_canary_transient_source_profile_dossier_proof_stays_within_bounded_raw_json_fallback():
    proof = _load_phase_e_source_profile_transient_proof()
    response = proof["response_json"]
    presentation = response["presentation"]
    root_view = presentation["views"][0]
    leaf_views = root_view["children"]
    raw_json_leaf_keys = [
        view["view_key"]
        for view in leaf_views
        if not view.get("children") and view.get("renderer_type") == "raw_json"
    ]

    assert proof["consumer_key"] == "aoi-canary"
    assert proof["route_family"] == "source_profile"
    assert proof["profile"] == "dossier"
    assert proof["source_v2_job_id"] == "job-744edf255ad5"
    assert proof["request_json"]["consumer_key"] == "aoi-canary"
    assert proof["request_json"]["profile"] == "dossier"
    assert proof["request_json"]["source_v2_job_id"] == "job-744edf255ad5"
    assert proof["consumer_adaptation_truth"]["root_renderer_type"] == "tab"
    assert root_view["renderer_type"] == "tab"
    assert raw_json_leaf_keys == ["compose_intent_02_aoi_thematic_report"]
    assert proof["consumer_adaptation_truth"]["raw_json_leaf_count"] == 1
    assert proof["consumer_adaptation_truth"]["raw_json_leaf_keys"] == raw_json_leaf_keys
    adapted_views = [
        entry["view_key"]
        for entry in proof["consumer_adaptation_truth"]["adaptation_details"]
        if entry["adapted"]
    ]
    assert adapted_views == ["compose_intent_02_aoi_thematic_report"]


def test_aoi_canary_transient_source_profile_comparison_proof_stays_within_bounded_raw_json_fallback():
    proof = _load_phase_e_source_profile_comparison_transient_proof()
    response = proof["response_json"]
    presentation = response["presentation"]
    root_view = presentation["views"][0]
    leaf_views = root_view["children"]
    raw_json_leaf_keys = [
        view["view_key"]
        for view in leaf_views
        if not view.get("children") and view.get("renderer_type") == "raw_json"
    ]

    assert proof["consumer_key"] == "aoi-canary"
    assert proof["route_family"] == "source_profile"
    assert proof["profile"] == "comparison"
    assert proof["source_v2_job_id"] == "job-744edf255ad5"
    assert proof["request_json"]["consumer_key"] == "aoi-canary"
    assert proof["request_json"]["profile"] == "comparison"
    assert proof["request_json"]["source_v2_job_id"] == "job-744edf255ad5"
    assert proof["consumer_adaptation_truth"]["root_renderer_type"] == "tab"
    assert root_view["renderer_type"] == "tab"
    assert raw_json_leaf_keys == ["compose_intent_03_aoi_thematic_report"]
    assert proof["consumer_adaptation_truth"]["raw_json_leaf_count"] == 1
    assert proof["consumer_adaptation_truth"]["raw_json_leaf_keys"] == raw_json_leaf_keys
    adapted_views = [
        entry["view_key"]
        for entry in proof["consumer_adaptation_truth"]["adaptation_details"]
        if entry["adapted"]
    ]
    assert adapted_views == ["compose_intent_03_aoi_thematic_report"]


def test_aoi_canary_transient_genealogy_direct_sections_proof_preserves_non_aoi_root_truth():
    proof = _load_phase_e_genealogy_direct_sections_transient_proof()
    response = proof["response_json"]
    presentation = response["presentation"]
    root_view = presentation["views"][0]

    assert proof["consumer_key"] == "aoi-canary"
    assert proof["route_family"] == "direct_sections"
    assert proof["workflow_key"] == "intellectual_genealogy"
    assert proof["request_json"]["consumer_key"] == "aoi-canary"
    assert proof["request_json"]["workflow_key"] == "intellectual_genealogy"
    assert proof["consumer_adaptation_truth"]["expected_root_renderer"] == "card_grid"
    assert proof["consumer_adaptation_truth"]["observed_root_renderer"] == "card_grid"
    assert proof["consumer_adaptation_truth"]["root_renderer_matches"] is True
    assert root_view["renderer_type"] == "card_grid"
    assert proof["consumer_adaptation_truth"]["expected_raw_json_view_keys"] == []
    assert proof["consumer_adaptation_truth"]["observed_raw_json_view_keys"] == []
    assert proof["consumer_adaptation_truth"]["raw_json_set_matches"] is True
