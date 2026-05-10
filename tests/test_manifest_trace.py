import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from src.aoi.constants import AOI_WORKFLOW_KEY
from src.presenter.first_hop_affordance import (
    FIRST_HOP_SPECIALIZED_FAMILY_FINDINGS_BANK_ARSENAL_PROMOTION_V1,
)
from src.presenter.bounded_dynamic_composition import (
    BoundedCompositionValidationError,
    COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1,
    COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
    COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
    COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
    COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1,
    COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
    COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
)
from src.presenter.decision_trace import _diff_snapshots, build_presentation_trace
from src.presenter.manifest_builder import build_effective_manifest
from src.presenter.presentation_api import assemble_page, build_presentation_manifest
from src.presenter.renderer_contract_enforcement import (
    ServedIntent,
    is_renderer_contract_enforced_mode,
)
from src.presenter.schemas import (
    CompositionIssue,
    EffectiveManifestView,
    EffectivePresentationManifest,
    FirstHopAffordance,
    ViewPayload,
)
from src.renderers.validator import validate_all_schemas, validate_renderer_registry_artifacts

_COMMUNICATIONS_DIR = Path(__file__).resolve().parent.parent / "communications"
_ROUND6_AOI_TRACE_FILES = {
    "proof-round5-adaptive-aoi-dossier-final-1774100000": _COMMUNICATIONS_DIR / "PROOF_round6_dossier_final_trace_2026-03-21.json",
    "proof-round5-adaptive-aoi-comparison-final-1774100000": _COMMUNICATIONS_DIR / "PROOF_round6_comparison_final_trace_2026-03-21.json",
}


def _base_payload() -> ViewPayload:
    return ViewPayload(
        view_key="genealogy_tp_inferential_commitments",
        view_name="Inferential Commitments",
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "commitments"}]},
        presentation_stance="diagnostic",
        priority="primary",
        rationale="Rich content",
        data_quality="rich",
        top_level_group=None,
        source_parent_view_key=None,
        promoted_to_top_level=False,
        selection_priority="primary",
        navigation_state="normal",
        semantic_scaffold_type=None,
        scaffold_hosting_mode=None,
        phase_number=1.0,
        engine_key="inferential_commitment_mapper",
        chain_key=None,
        scope="aggregated",
        has_structured_data=True,
        structured_data={"commitments": [{"commitment": "A"}]},
        reading_scaffold={"surface_type": "argument_map", "brief": "Guide"},
        raw_prose=None,
        prose_ref_view_key=None,
        items=None,
        tab_count=None,
        visibility="if_data_exists",
        position=1.3,
        children=[],
    )


def _adaptive_relationship_payload() -> ViewPayload:
    return ViewPayload(
        view_key="genealogy_relationship_landscape",
        view_name="Relationship Landscape",
        description="",
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        priority="primary",
        rationale="Rich content",
        data_quality="rich",
        top_level_group=None,
        source_parent_view_key=None,
        promoted_to_top_level=False,
        selection_priority="primary",
        navigation_state="normal",
        semantic_scaffold_type=None,
        scaffold_hosting_mode=None,
        phase_number=1.5,
        engine_key="genealogy_relationship_classification",
        chain_key=None,
        scope="per_item",
        has_structured_data=False,
        structured_data=None,
        reading_scaffold=None,
        raw_prose=None,
        prose_ref_view_key=None,
        items=[
            {
                "work_key": "foundational_precursor",
                "has_structured_data": True,
                "structured_data": {
                    "work_title": "Foundational Precursor",
                    "relationship_type": "direct_precursor",
                    "relationship_strength": "strong",
                    "summary": "Sets the target's forcing problem.",
                    "centrality_assessment": "Sets the target's forcing problem.",
                    "influence_channels": [{"channel": "framework", "description": "Shared architecture"}],
                    "key_evidence": [{"evidence_type": "citation", "description": "Explicit uptake", "quote": "Quoted line"}],
                },
                "raw_prose": None,
            },
            {
                "work_key": "method_context",
                "has_structured_data": True,
                "structured_data": {
                    "work_title": "Method Context",
                    "relationship_type": "methodological_ancestor",
                    "relationship_strength": "moderate",
                    "summary": "Provides method but not the core problem.",
                    "centrality_assessment": "Provides method but not the core problem.",
                    "influence_channels": [{"channel": "methodology", "description": "Shared method"}],
                    "key_evidence": [{"evidence_type": "parallel", "description": "Method reuse", "quote": "Method quote"}],
                },
                "raw_prose": None,
            },
            {
                "work_key": "background_horizon",
                "has_structured_data": True,
                "structured_data": {
                    "work_title": "Background Horizon",
                    "relationship_type": "indirect_contextualizer",
                    "relationship_strength": "weak",
                    "summary": "Frames the debate.",
                    "centrality_assessment": "Frames the debate.",
                    "influence_channels": [{"channel": "authority", "description": "Context cue"}],
                    "key_evidence": [{"evidence_type": "context", "description": "Debate framing", "quote": "Context quote"}],
                },
                "raw_prose": None,
            },
        ],
        tab_count=3,
        visibility="if_data_exists",
        position=1.1,
        children=[],
    )


def _adaptive_conditions_payload() -> ViewPayload:
    return ViewPayload(
        view_key="genealogy_conditions",
        view_name="Conditions of Possibility",
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "conditions_snapshot", "title": "Conditions Snapshot"}]},
        presentation_stance="diagnostic",
        priority="primary",
        rationale="Rich content",
        data_quality="rich",
        top_level_group=None,
        source_parent_view_key=None,
        promoted_to_top_level=False,
        selection_priority="primary",
        navigation_state="normal",
        semantic_scaffold_type=None,
        scaffold_hosting_mode=None,
        phase_number=3.0,
        engine_key="conditions_of_possibility_analyzer",
        chain_key=None,
        scope="aggregated",
        has_structured_data=True,
        structured_data={
            "meta": {
                "overall_balance": "balanced",
                "enabling_conditions_count": 1,
                "constraining_conditions_count": 1,
                "path_dependencies_count": 2,
                "unacknowledged_debts_count": 0,
                "alternative_paths_count": 1,
            },
            "enabling_conditions": [
                {
                    "description": "Creates the first opening",
                    "condition_type": "conceptual_foundation",
                    "essentiality": "important",
                    "how_it_enables": "Opens the path.",
                }
            ],
            "constraining_conditions": [
                {
                    "description": "Keeps one commitment in place",
                    "constraint_type": "prior_commitment",
                    "binding_force": "moderate",
                    "how_navigated": "Reframed carefully.",
                }
            ],
            "path_dependencies": [
                {
                    "description": "Dependency chain one",
                    "chain": ["Work A", "Work B", "Target"],
                    "if_absent": "The current framing weakens.",
                    "is_acknowledged": False,
                },
                {
                    "description": "Dependency chain two",
                    "chain": ["Work C", "Target"],
                    "if_absent": "The method loosens.",
                    "is_acknowledged": True,
                },
            ],
            "alternative_paths": [
                {
                    "branching_point": "Method turn",
                    "path_not_taken": "A more reformist route",
                    "why_not_taken": "Continuity was institutionally safer",
                    "implications": "The argument would soften substantially",
                }
            ],
            "counterfactual_analysis": "Without the earlier path, the argument would lose its scaffolding.",
            "synthetic_judgment": "The overall field is balanced but path-dependent.",
        },
        reading_scaffold=None,
        raw_prose=None,
        prose_ref_view_key=None,
        items=None,
        tab_count=None,
        visibility="if_data_exists",
        position=4.0,
        children=[],
    )


def _adaptive_aoi_theme_payload() -> ViewPayload:
    return ViewPayload(
        view_key="aoi_by_theme",
        view_name="By Theme",
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "theme_a", "title": "Theme A"}]},
        presentation_stance="comparison",
        priority="primary",
        rationale="Rich content",
        data_quality="rich",
        top_level_group=None,
        source_parent_view_key="aoi_thematic_analysis",
        promoted_to_top_level=False,
        selection_priority="primary",
        navigation_state="normal",
        semantic_scaffold_type=None,
        scaffold_hosting_mode=None,
        phase_number=3.0,
        engine_key="aoi_sin_findings",
        chain_key=None,
        scope="aggregated",
        has_structured_data=True,
        structured_data={
            "_section_order": ["theme_a", "theme_b"],
            "_section_titles": {
                "theme_a": "Theme A",
                "theme_b": "Theme B",
            },
            "theme_a": {
                "overview": "Theme A overview",
                "engagement": "Engagement level: partial.",
                "key_claims": [{"title": "Claim 1", "description": "Primary claim"}],
                "philosophical_commitments": [{"title": "Commitment 1", "description": "Primary commitment"}],
                "argumentative_moves": [{"title": "Move 1", "description": "Primary move"}],
                "source_documents": ["Source A", "Source B"],
                "findings": [
                    {
                        "title": "A1",
                        "subtitle": "Finding subtitle",
                        "description": "Finding description",
                        "badge": "Theme finding",
                        "sin_type": "appropriation",
                        "sin_type_label": "Appropriation",
                    },
                    {
                        "title": "A2",
                        "subtitle": "Finding subtitle",
                        "description": "Finding description",
                        "badge": "Theme finding",
                        "sin_type": "appropriation",
                        "sin_type_label": "Appropriation",
                    },
                    {
                        "title": "A3",
                        "subtitle": "Finding subtitle",
                        "description": "Finding description",
                        "badge": "Theme finding",
                        "sin_type": "misreading",
                        "sin_type_label": "Misreading",
                    },
                ],
            },
            "theme_b": {
                "overview": "Theme B overview",
                "engagement": "Engagement level: partial.",
                "key_claims": [{"title": "Claim 1", "description": "Primary claim"}],
                "philosophical_commitments": [{"title": "Commitment 1", "description": "Primary commitment"}],
                "argumentative_moves": [{"title": "Move 1", "description": "Primary move"}],
                "source_documents": ["Source C"],
                "findings": [
                    {
                        "title": "B1",
                        "subtitle": "Finding subtitle",
                        "description": "Finding description",
                        "badge": "Theme finding",
                        "sin_type": "omission",
                        "sin_type_label": "Omission",
                    }
                ],
            },
        },
        reading_scaffold=None,
        raw_prose=None,
        prose_ref_view_key=None,
        items=None,
        tab_count=2,
        visibility="if_data_exists",
        position=1.2,
        children=[],
    )


def _adaptive_aoi_report_payload() -> ViewPayload:
    return ViewPayload(
        view_key="aoi_thematic_report",
        view_name="Report",
        description="",
        renderer_type="accordion",
        renderer_config={
            "sections": [
                {"key": "summary", "title": "Summary"},
                {"key": "engagement_pattern", "title": "Engagement Pattern"},
                {"key": "key_divergences", "title": "Key Divergences"},
                {"key": "sin_distribution", "title": "Sin Distribution"},
                {"key": "reading_implications", "title": "Reading Implications"},
            ]
        },
        presentation_stance="summary",
        priority="secondary",
        rationale="Rich content",
        data_quality="rich",
        top_level_group=None,
        source_parent_view_key="aoi_thematic_analysis",
        promoted_to_top_level=False,
        selection_priority="secondary",
        navigation_state="normal",
        semantic_scaffold_type=None,
        scaffold_hosting_mode=None,
        phase_number=4.0,
        engine_key="aoi_thematic_report",
        chain_key=None,
        scope="aggregated",
        has_structured_data=True,
        structured_data={
            "summary": "Distributed AOI report summary.",
            "engagement_pattern": "Distributed AOI engagement pattern.",
            "key_divergences": [
                {"title": "Divergence 1", "subtitle": "Theme A", "description": "Primary divergence.", "badge": "high"},
                {"title": "Divergence 2", "subtitle": "Theme B", "description": "Secondary divergence.", "badge": "medium"},
                {"title": "Divergence 3", "subtitle": "Theme C", "description": "Third divergence.", "badge": "low"},
                {"title": "Divergence 4", "description": "Fourth divergence."},
            ],
            "sin_distribution": [
                {"sin_type": "Appropriation", "count": 2, "description": "Borrowing dominates."},
                {"sin_type": "Misreading", "count": 1, "description": "Interpretive compression."},
                {"sin_type": "Omission", "count": 1},
            ],
            "reading_implications": "Distributed AOI reading implications.",
        },
        reading_scaffold=None,
        raw_prose=None,
        prose_ref_view_key=None,
        items=None,
        tab_count=None,
        visibility="if_data_exists",
        position=1.4,
        children=[],
    )


def _build_manifest_for_test(
    payloads: dict[str, ViewPayload],
    *,
    composition_mode: str | None = None,
    consumer_key: str = "the-critic",
) -> EffectivePresentationManifest:
    with patch("src.presenter.manifest_builder.resolve_scaffold_type", return_value=None):
        return build_effective_manifest(
            job_id="job-1",
            plan_id="plan-1",
            consumer_key=consumer_key,
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            composition_mode=composition_mode,
            thinker_name="Markus",
            strategy_summary="summary",
            payloads=payloads,
            all_outputs=[],
            job={"created_at": "2026-03-13T00:00:00"},
        )


def _normalize_root_metadata(payload: dict[str, object]) -> dict[str, object]:
    normalized = json.loads(json.dumps(payload))
    normalized.pop("presentation_hash", None)
    normalized.pop("presentation_content_hash", None)
    normalized.pop("prepared_at", None)
    return normalized


def test_effective_manifest_hash_includes_consumer_key():
    payload = _base_payload()
    payloads = {payload.view_key: payload}

    with patch("src.presenter.manifest_builder.resolve_scaffold_type", return_value=None):
        critic_manifest = build_effective_manifest(
            job_id="job-1",
            plan_id="plan-1",
            consumer_key="the-critic",
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            thinker_name="Markus",
            strategy_summary="summary",
            payloads=payloads,
            all_outputs=[],
            job={"created_at": "2026-03-13T00:00:00"},
        )
        mgmt_manifest = build_effective_manifest(
            job_id="job-1",
            plan_id="plan-1",
            consumer_key="analyzer-mgmt",
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            thinker_name="Markus",
            strategy_summary="summary",
            payloads=payloads,
            all_outputs=[],
            job={"created_at": "2026-03-13T00:00:00"},
        )

    assert critic_manifest.consumer_key == "the-critic"
    assert mgmt_manifest.consumer_key == "analyzer-mgmt"
    assert critic_manifest.presentation_hash != mgmt_manifest.presentation_hash


def test_effective_manifest_hash_includes_composition_mode():
    payload = _base_payload()
    payloads = {payload.view_key: payload}

    with patch("src.presenter.manifest_builder.resolve_scaffold_type", return_value=None):
        authored_manifest = build_effective_manifest(
            job_id="job-1",
            plan_id="plan-1",
            consumer_key="the-critic",
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            thinker_name="Markus",
            strategy_summary="summary",
            payloads=payloads,
            all_outputs=[],
            job={"created_at": "2026-03-13T00:00:00"},
            composition_mode=None,
        )
        composed_manifest = build_effective_manifest(
            job_id="job-1",
            plan_id="plan-1",
            consumer_key="the-critic",
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            thinker_name="Markus",
            strategy_summary="summary",
            payloads=payloads,
            all_outputs=[],
            job={"created_at": "2026-03-13T00:00:00"},
            composition_mode=COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1,
        )

    assert authored_manifest.composition_mode is None
    assert composed_manifest.composition_mode == COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1
    assert authored_manifest.presentation_hash != composed_manifest.presentation_hash
    assert authored_manifest.presentation_content_hash != composed_manifest.presentation_content_hash


def test_manifest_reports_phase2_resolver_version():
    payload = _base_payload()
    payloads = {payload.view_key: payload}

    with patch("src.presenter.manifest_builder.resolve_scaffold_type", return_value=None):
        manifest = build_effective_manifest(
            job_id="job-1",
            plan_id="plan-1",
            consumer_key="the-critic",
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            thinker_name="Markus",
            strategy_summary="summary",
            payloads=payloads,
            all_outputs=[],
            job={"created_at": "2026-03-13T00:00:00"},
        )

    assert manifest.resolver_version == "bounded-dynamism-phase2"


def test_effective_manifest_adapts_visualizer_unsupported_renderer_contracts():
    card_payload = _base_payload()
    card_payload.view_key = "genealogy_per_work_scan"
    card_payload.view_name = "Per-Work Scan"
    card_payload.renderer_type = "card"
    card_payload.renderer_config = {}

    section_payload = _base_payload()
    section_payload.view_key = "genealogy_cop_path_dependencies"
    section_payload.view_name = "Path Dependencies"
    section_payload.renderer_type = "timeline_strip"
    section_payload.renderer_config = {}

    payloads = {
        card_payload.view_key: card_payload,
        section_payload.view_key: section_payload,
    }

    with patch("src.presenter.manifest_builder.resolve_scaffold_type", return_value=None):
        manifest = build_effective_manifest(
            job_id="job-1",
            plan_id="plan-1",
            consumer_key="visualizer",
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            thinker_name="Markus",
            strategy_summary="summary",
            payloads=payloads,
            all_outputs=[],
            job={"created_at": "2026-03-13T00:00:00"},
        )

    by_key = {view.view_key: view for view in manifest.views}
    assert by_key["genealogy_per_work_scan"].renderer_type == "raw_json"
    assert by_key["genealogy_cop_path_dependencies"].renderer_type == "raw_json"


def test_renderer_registry_preflight_validates_repo_tracked_definitions():
    preflight = validate_renderer_registry_artifacts()
    schema_health = validate_all_schemas()

    assert preflight["valid"] is True
    assert preflight["count"] == 9
    assert preflight["issues"] == []
    assert all(
        entry["input_schema_valid"] and entry["config_schema_valid"]
        for entry in schema_health.values()
    )


def test_renderer_registry_preflight_check_command_succeeds():
    result = subprocess.run(
        [sys.executable, "scripts/check_renderer_contracts.py"],
        capture_output=True,
        text=True,
        cwd=_COMMUNICATIONS_DIR.parent,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["registry_preflight"]["valid"] is True
    assert payload["schema_issues"] == {}


def test_renderer_registry_preflight_reports_malformed_temp_definition(tmp_path):
    (tmp_path / "broken.json").write_text("{not valid json", encoding="utf-8")

    result = validate_renderer_registry_artifacts(tmp_path)

    assert result["valid"] is False
    assert result["count"] == 0
    assert result["issues"][0]["file"] == "broken.json"


@pytest.mark.parametrize(
    "job_id",
    [
        "proof-round5-adaptive-aoi-dossier-final-1774100000",
        "proof-round5-adaptive-aoi-comparison-final-1774100000",
    ],
)
def test_aoi_live_controls_keep_served_outputs_identical_with_and_without_renderer_enforcement(job_id):
    saved_round6_trace = json.loads(_ROUND6_AOI_TRACE_FILES[job_id].read_text(encoding="utf-8"))

    with patch(
        "src.presenter.manifest_builder.enforce_final_payload_contracts_or_raise",
        return_value=None,
    ):
        baseline_manifest = build_presentation_manifest(
            job_id,
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
        )
        baseline_page = assemble_page(
            job_id,
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
        )

    enforced_manifest = build_presentation_manifest(
        job_id,
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
    )
    enforced_page = assemble_page(
        job_id,
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
    )

    assert _normalize_root_metadata(baseline_manifest.model_dump()) == _normalize_root_metadata(
        enforced_manifest.model_dump()
    )
    assert _normalize_root_metadata(baseline_page.model_dump()) == _normalize_root_metadata(
        enforced_page.model_dump()
    )
    assert _normalize_root_metadata(saved_round6_trace["final_manifest"]) == _normalize_root_metadata(
        enforced_manifest.model_dump()
    )


def test_effective_manifest_strictly_rejects_missing_renderer_contract_for_allowlisted_aoi_mode():
    payload = _adaptive_aoi_theme_payload()
    payload.renderer_type = "mini_card_list"
    payload.renderer_config = {}
    payloads = {payload.view_key: payload}

    with pytest.raises(BoundedCompositionValidationError) as excinfo:
        _build_manifest_for_test(
            payloads,
            composition_mode=COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
        )

    assert excinfo.value.issues[0].reason == "renderer_definition_missing"
    assert excinfo.value.issues[0].field == "renderer_type"


def test_effective_manifest_strictly_rejects_invalid_renderer_config_for_allowlisted_aoi_mode():
    payload = _adaptive_aoi_theme_payload()
    payload.renderer_config = {"sections": "not-a-list"}
    payloads = {payload.view_key: payload}

    with pytest.raises(BoundedCompositionValidationError) as excinfo:
        _build_manifest_for_test(
            payloads,
            composition_mode=COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
        )

    assert excinfo.value.issues[0].reason == "renderer_config_validation_failed"
    assert excinfo.value.issues[0].field == "renderer_config"


def test_effective_manifest_strictly_rejects_invalid_renderer_data_for_allowlisted_aoi_mode():
    payload = _adaptive_aoi_report_payload()
    payload.structured_data = 123
    payloads = {payload.view_key: payload}

    with pytest.raises(BoundedCompositionValidationError) as excinfo:
        _build_manifest_for_test(
            payloads,
            composition_mode=COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
        )

    assert excinfo.value.issues[0].reason == "renderer_data_validation_failed"
    assert excinfo.value.issues[0].field == "structured_data"


def test_effective_manifest_skips_data_validation_for_container_host_without_structured_data():
    child_payload = _adaptive_aoi_theme_payload()
    payload = ViewPayload(
        view_key="aoi_thematic_analysis",
        view_name="Thematic Analysis",
        description="",
        renderer_type="tab",
        renderer_config={},
        presentation_stance="comparison",
        priority="primary",
        rationale="Rich content",
        data_quality="rich",
        top_level_group=None,
        source_parent_view_key=None,
        promoted_to_top_level=False,
        selection_priority="primary",
        navigation_state="normal",
        semantic_scaffold_type=None,
        scaffold_hosting_mode=None,
        phase_number=None,
        engine_key=None,
        chain_key=None,
        scope="aggregated",
        has_structured_data=False,
        structured_data=None,
        reading_scaffold=None,
        raw_prose=None,
        prose_ref_view_key=None,
        items=None,
        tab_count=None,
        visibility="if_data_exists",
        position=1.0,
        children=[child_payload],
    )

    manifest = _build_manifest_for_test(
        {payload.view_key: payload},
        composition_mode=COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
    )

    assert manifest.view_count == 1
    assert manifest.views[0].renderer_type == "tab"


def test_effective_manifest_keeps_non_allowlisted_modes_warn_only_for_renderer_contract_issues():
    payload = _adaptive_aoi_theme_payload()
    payload.renderer_type = "mini_card_list"
    payload.renderer_config = {}
    payloads = {payload.view_key: payload}

    manifest = _build_manifest_for_test(
        payloads,
        composition_mode=COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
    )

    assert manifest.view_count == 1
    assert manifest.views[0].renderer_type == "mini_card_list"
    assert not is_renderer_contract_enforced_mode(
        COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1
    )


def test_effective_manifest_derives_integrated_scaffold_hosting_from_python_renderer_capability():
    payload = _base_payload()
    payloads = {payload.view_key: payload}

    with patch("src.presenter.manifest_builder.resolve_scaffold_type", return_value="argument_map"):
        manifest = build_effective_manifest(
            job_id="job-1",
            plan_id="plan-1",
            consumer_key="the-critic",
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            thinker_name="Markus",
            strategy_summary="summary",
            payloads=payloads,
            all_outputs=[],
            job={"created_at": "2026-03-13T00:00:00"},
        )

    assert manifest.views[0].semantic_scaffold_type == "argument_map"
    assert manifest.views[0].scaffold_hosting_mode == "integrated"


def test_trace_final_stage_matches_manifest_and_page_semantics():
    payload = _base_payload()
    payload.first_hop_affordance = FirstHopAffordance(
        capturable=True,
        allowed_destinations=["arsenal", "research_todo"],
    )
    page_inputs = {
        "payloads": {payload.view_key: payload},
        "top_level": [payload],
        "job": {"plan_id": "plan-1", "created_at": "2026-03-13T00:00:00"},
        "plan_id": "plan-1",
        "thinker_name": "Markus",
        "strategy_summary": "summary",
        "all_outputs": [],
    }
    view_def = SimpleNamespace(
        view_key=payload.view_key,
        view_name=payload.view_name,
        description=payload.description,
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "commitments"}]},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=1.3,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=1.0,
            engine_key="inferential_commitment_mapper",
            chain_key=None,
            scope="aggregated",
            result_path="",
        ),
    )
    fake_registry = SimpleNamespace(get=lambda key: view_def if key == view_def.view_key else None)
    recommendation = {"view_key": payload.view_key, "priority": "primary", "rationale": "Rich content"}
    composition = SimpleNamespace(
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "commitments"}]},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )
    styled_payload = payload.model_copy(
        update={
            "semantic_scaffold_type": "argument_map",
            "scaffold_hosting_mode": "integrated",
        }
    )

    with patch(
        "src.presenter.presentation_api._prepare_page_payloads",
        return_value=page_inputs,
    ), patch(
        "src.presenter.presentation_api._attach_reading_scaffolds",
        return_value=None,
    ), patch(
        "src.presenter.presentation_api._build_execution_summary",
        return_value={},
    ), patch(
        "src.presenter.presentation_api._resolve_page_style_school",
        return_value="explanatory_narrative",
    ), patch(
        "src.presenter.presentation_api.apply_cached_polish_to_views",
        return_value=([styled_payload], "polished"),
    ), patch(
        "src.presenter.presentation_api.load_view_refinement",
        return_value=None,
    ), patch(
        "src.presenter.manifest_builder.resolve_scaffold_type",
        return_value="argument_map",
    ), patch(
        "src.presenter.decision_trace.get_job",
        return_value={"plan_id": "plan-1"},
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
        return_value=fake_registry,
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
        manifest = build_presentation_manifest("job-1", consumer_key="the-critic", slim=True)
        page = assemble_page("job-1", consumer_key="the-critic", slim=True)
        trace = build_presentation_trace("job-1", consumer_key="the-critic")

    assert [view.model_dump() for view in trace.entries[-1].snapshot] == [
        view.model_dump() for view in manifest.views
    ]
    assert trace.final_manifest.model_dump() == manifest.model_dump()
    assert page.style_school == "explanatory_narrative"
    assert page.polish_state == "polished"
    assert manifest.style_school == "explanatory_narrative"
    assert manifest.polish_state == "polished"
    assert trace.style_school == "explanatory_narrative"
    assert trace.polish_state == "polished"
    assert page.views[0].selection_priority == manifest.views[0].selection_priority
    assert page.views[0].navigation_state == manifest.views[0].navigation_state
    assert page.views[0].semantic_scaffold_type == manifest.views[0].semantic_scaffold_type
    assert page.views[0].scaffold_hosting_mode == manifest.views[0].scaffold_hosting_mode
    assert page.views[0].renderer_type == manifest.views[0].renderer_type
    assert page.views[0].first_hop_affordance == manifest.views[0].first_hop_affordance
    assert page.presentation_hash == manifest.presentation_hash
    assert page.presentation_content_hash == manifest.presentation_content_hash


def test_manifest_hash_includes_first_hop_affordance_but_content_hash_does_not():
    base_payload = _base_payload()
    afforded_payload = _base_payload()
    afforded_payload.first_hop_affordance = FirstHopAffordance(
        capturable=True,
        allowed_destinations=["arsenal", "research_todo"],
    )

    with patch("src.presenter.manifest_builder.resolve_scaffold_type", return_value="none"):
        baseline_manifest = build_effective_manifest(
            job_id="job-1",
            plan_id="plan-1",
            consumer_key="the-critic",
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            thinker_name="Markus",
            strategy_summary="summary",
            payloads={base_payload.view_key: base_payload},
            all_outputs=[],
            job={"created_at": "2026-03-13T00:00:00"},
        )
        afforded_manifest = build_effective_manifest(
            job_id="job-1",
            plan_id="plan-1",
            consumer_key="the-critic",
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            thinker_name="Markus",
            strategy_summary="summary",
            payloads={afforded_payload.view_key: afforded_payload},
            all_outputs=[],
            job={"created_at": "2026-03-13T00:00:00"},
        )

    assert baseline_manifest.presentation_hash != afforded_manifest.presentation_hash
    assert (
        baseline_manifest.presentation_content_hash
        == afforded_manifest.presentation_content_hash
    )
    assert afforded_manifest.views[0].first_hop_affordance == FirstHopAffordance(
        capturable=True,
        allowed_destinations=["arsenal", "research_todo"],
    )


def test_manifest_hash_ignores_unset_specialized_family_on_first_hop_affordance():
    base_payload = _base_payload()
    explicit_none_payload = _base_payload()
    base_payload.first_hop_affordance = FirstHopAffordance(
        capturable=True,
        allowed_destinations=["arsenal", "research_todo"],
    )
    explicit_none_payload.first_hop_affordance = FirstHopAffordance(
        capturable=True,
        allowed_destinations=["arsenal", "research_todo"],
        specialized_family=None,
    )

    with patch("src.presenter.manifest_builder.resolve_scaffold_type", return_value="none"):
        base_manifest = build_effective_manifest(
            job_id="job-1",
            plan_id="plan-1",
            consumer_key="the-critic",
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            thinker_name="Markus",
            strategy_summary="summary",
            payloads={base_payload.view_key: base_payload},
            all_outputs=[],
            job={"created_at": "2026-03-13T00:00:00"},
        )
        explicit_none_manifest = build_effective_manifest(
            job_id="job-1",
            plan_id="plan-1",
            consumer_key="the-critic",
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            thinker_name="Markus",
            strategy_summary="summary",
            payloads={explicit_none_payload.view_key: explicit_none_payload},
            all_outputs=[],
            job={"created_at": "2026-03-13T00:00:00"},
        )

    assert base_manifest.presentation_hash == explicit_none_manifest.presentation_hash
    assert (
        base_manifest.presentation_content_hash
        == explicit_none_manifest.presentation_content_hash
    )


def test_manifest_hash_includes_specialized_first_hop_affordance_but_content_hash_does_not():
    base_payload = _base_payload()
    specialized_payload = _base_payload()
    base_payload.first_hop_affordance = FirstHopAffordance(
        capturable=True,
        allowed_destinations=["arsenal", "research_todo"],
    )
    specialized_payload.first_hop_affordance = FirstHopAffordance(
        capturable=True,
        allowed_destinations=["arsenal", "research_todo"],
        specialized_family=FIRST_HOP_SPECIALIZED_FAMILY_FINDINGS_BANK_ARSENAL_PROMOTION_V1,
    )

    with patch("src.presenter.manifest_builder.resolve_scaffold_type", return_value="none"):
        base_manifest = build_effective_manifest(
            job_id="job-1",
            plan_id="plan-1",
            consumer_key="the-critic",
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            thinker_name="Markus",
            strategy_summary="summary",
            payloads={base_payload.view_key: base_payload},
            all_outputs=[],
            job={"created_at": "2026-03-13T00:00:00"},
        )
        specialized_manifest = build_effective_manifest(
            job_id="job-1",
            plan_id="plan-1",
            consumer_key="the-critic",
            served_intent=ServedIntent.EFFECTIVE_MANIFEST_SERVED,
            thinker_name="Markus",
            strategy_summary="summary",
            payloads={specialized_payload.view_key: specialized_payload},
            all_outputs=[],
            job={"created_at": "2026-03-13T00:00:00"},
        )

    assert base_manifest.presentation_hash != specialized_manifest.presentation_hash
    assert (
        base_manifest.presentation_content_hash
        == specialized_manifest.presentation_content_hash
    )


def test_diff_snapshots_surfaces_first_hop_affordance_changes():
    previous = [
        EffectiveManifestView(
            view_key="aoi_thematic_report",
            view_name="AOI Report",
            renderer_type="accordion",
            renderer_config={},
            position=1.0,
        )
    ]
    current = [
        EffectiveManifestView(
            view_key="aoi_thematic_report",
            view_name="AOI Report",
            renderer_type="accordion",
            renderer_config={},
            position=1.0,
            first_hop_affordance=FirstHopAffordance(
                capturable=True,
                allowed_destinations=["arsenal", "research_todo"],
            ),
        )
    ]

    changes = _diff_snapshots(previous, current)

    assert len(changes) == 1
    assert changes[0].field == "first_hop_affordance"
    assert changes[0].before is None
    assert changes[0].after == FirstHopAffordance(
        capturable=True,
        allowed_destinations=["arsenal", "research_todo"],
    )


def test_diff_snapshots_surfaces_specialized_first_hop_affordance_changes():
    previous = [
        EffectiveManifestView(
            view_key="aoi_by_sin_type",
            view_name="By Sin Type",
            renderer_type="card_grid",
            renderer_config={},
            position=1.0,
            first_hop_affordance=FirstHopAffordance(
                capturable=True,
                allowed_destinations=["arsenal", "research_todo"],
            ),
        )
    ]
    current = [
        EffectiveManifestView(
            view_key="aoi_by_sin_type",
            view_name="By Sin Type",
            renderer_type="card_grid",
            renderer_config={},
            position=1.0,
            first_hop_affordance=FirstHopAffordance(
                capturable=True,
                allowed_destinations=["arsenal", "research_todo"],
                specialized_family=FIRST_HOP_SPECIALIZED_FAMILY_FINDINGS_BANK_ARSENAL_PROMOTION_V1,
            ),
        )
    ]

    changes = _diff_snapshots(previous, current)

    assert len(changes) == 1
    assert changes[0].field == "first_hop_affordance"
    assert changes[0].after == FirstHopAffordance(
        capturable=True,
        allowed_destinations=["arsenal", "research_todo"],
        specialized_family=FIRST_HOP_SPECIALIZED_FAMILY_FINDINGS_BANK_ARSENAL_PROMOTION_V1,
    )


def test_trace_surfaces_ignored_runtime_overrides():
    payload = _base_payload()
    page_inputs = {
        "payloads": {payload.view_key: payload},
        "top_level": [payload],
        "job": {"plan_id": "plan-1", "created_at": "2026-03-13T00:00:00"},
        "plan_id": "plan-1",
        "thinker_name": "Markus",
        "strategy_summary": "summary",
        "all_outputs": [],
    }
    view_def = SimpleNamespace(
        view_key=payload.view_key,
        view_name=payload.view_name,
        description=payload.description,
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "commitments"}]},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=1.3,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=1.0,
            engine_key="inferential_commitment_mapper",
            chain_key=None,
            scope="aggregated",
            result_path="",
        ),
    )
    fake_registry = SimpleNamespace(get=lambda key: view_def if key == view_def.view_key else None)
    recommendation = {
        "view_key": payload.view_key,
        "priority": "primary",
        "rationale": "Rich content",
        "renderer_config_overrides": {"bad_key": True},
    }
    composition = SimpleNamespace(
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "commitments"}]},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[
            {
                "field": "renderer_config_overrides.bad_key",
                "value": True,
                "reason": "override_key_not_allowed_for_renderer:accordion",
            }
        ],
    )

    with patch(
        "src.presenter.presentation_api._prepare_page_payloads",
        return_value=page_inputs,
    ), patch(
        "src.presenter.presentation_api._attach_reading_scaffolds",
        return_value=None,
    ), patch(
        "src.presenter.presentation_api._build_execution_summary",
        return_value={},
    ), patch(
        "src.presenter.presentation_api.load_view_refinement",
        return_value=None,
    ), patch(
        "src.presenter.manifest_builder.resolve_scaffold_type",
        return_value="argument_map",
    ), patch(
        "src.presenter.decision_trace.get_job",
        return_value={"plan_id": "plan-1"},
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
        return_value=fake_registry,
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
        trace = build_presentation_trace("job-1", consumer_key="the-critic")

    assert any(
        ignored.field == "renderer_config_overrides.bad_key"
        and ignored.reason == "override_key_not_allowed_for_renderer:accordion"
        for entry in trace.entries
        for ignored in entry.ignored_changes
    )


def test_trace_records_consumer_capability_adaptation_reason():
    payload = _base_payload()
    payload.renderer_type = "raw_json"
    payload.renderer_config = {}
    page_inputs = {
        "payloads": {payload.view_key: payload},
        "top_level": [payload],
        "job": {"plan_id": "plan-1", "created_at": "2026-03-13T00:00:00"},
        "plan_id": "plan-1",
        "thinker_name": "Markus",
        "strategy_summary": "summary",
        "all_outputs": [],
    }
    view_def = SimpleNamespace(
        view_key=payload.view_key,
        view_name=payload.view_name,
        description=payload.description,
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "commitments"}]},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=1.3,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=1.0,
            engine_key="inferential_commitment_mapper",
            chain_key=None,
            scope="aggregated",
            result_path="",
        ),
    )
    fake_registry = SimpleNamespace(get=lambda key: view_def if key == view_def.view_key else None)
    recommendation = {"view_key": payload.view_key, "priority": "primary", "rationale": "Rich content"}
    composition = SimpleNamespace(
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "commitments"}]},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )

    with patch(
        "src.presenter.presentation_api._prepare_page_payloads",
        return_value=page_inputs,
    ), patch(
        "src.presenter.presentation_api._attach_reading_scaffolds",
        return_value=None,
    ), patch(
        "src.presenter.presentation_api._build_execution_summary",
        return_value={},
    ), patch(
        "src.presenter.presentation_api.load_view_refinement",
        return_value=None,
    ), patch(
        "src.presenter.manifest_builder.resolve_scaffold_type",
        return_value="argument_map",
    ), patch(
        "src.presenter.decision_trace.get_job",
        return_value={"plan_id": "plan-1"},
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
        return_value=fake_registry,
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
        trace = build_presentation_trace("job-1", consumer_key="visualizer")

    assert trace.entries[-1].snapshot[0].renderer_type == "raw_json"
    assert any(
        ignored.reason == "renderer_not_supported_by_consumer:visualizer"
        for ignored in trace.entries[-1].ignored_changes
    )


def test_trace_surfaces_selected_variant_rationale_for_variant_driven_changes():
    payload = _base_payload()
    page_inputs = {
        "payloads": {payload.view_key: payload},
        "top_level": [payload],
        "job": {"plan_id": "plan-1", "created_at": "2026-03-13T00:00:00"},
        "plan_id": "plan-1",
        "thinker_name": "Markus",
        "strategy_summary": "summary",
        "all_outputs": [],
    }
    view_def = SimpleNamespace(
        view_key=payload.view_key,
        view_name=payload.view_name,
        description=payload.description,
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "commitments"}]},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=1.3,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=1.0,
            engine_key="inferential_commitment_mapper",
            chain_key=None,
            scope="aggregated",
            result_path="",
        ),
    )
    fake_registry = SimpleNamespace(get=lambda key: view_def if key == view_def.view_key else None)
    recommendation = {"view_key": payload.view_key, "priority": "primary", "rationale": "Rich content"}
    refinement_composition = SimpleNamespace(
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "commitments"}]},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
        template_selection_reason=None,
    )
    deterministic_composition = SimpleNamespace(
        renderer_type="card_grid",
        renderer_config={"columns": 3},
        presentation_stance="diagnostic",
        data_quality="rich",
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
        "src.presenter.presentation_api._build_execution_summary",
        return_value={},
    ), patch(
        "src.presenter.presentation_api.load_view_refinement",
        return_value=None,
    ), patch(
        "src.presenter.manifest_builder.resolve_scaffold_type",
        return_value="argument_map",
    ), patch(
        "src.presenter.decision_trace.get_job",
        return_value={"plan_id": "plan-1"},
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
        return_value=fake_registry,
    ), patch(
        "src.presenter.decision_trace.resolve_effective_composition",
        return_value=refinement_composition,
    ), patch(
        "src.presenter.decision_trace.resolve_effective_render_contract",
        return_value=deterministic_composition,
    ), patch(
        "src.presenter.decision_trace.load_selected_variants",
        return_value=[
            {
                "dimension": "renderer_type",
                "renderer_type": "card_grid",
                "renderer_config": {"columns": 3},
                "rationale": "User preferred card_grid for this view after comparison",
            }
        ],
    ):
        trace = build_presentation_trace("job-1", consumer_key="the-critic")

    deterministic_entry = next(
        entry for entry in trace.entries if entry.stage == "deterministic_contract_resolution"
    )
    assert any(
        change.field == "renderer_type"
        and change.after == "card_grid"
        and change.reason == "User preferred card_grid for this view after comparison"
        for change in deterministic_entry.applied_changes
    )


def test_trace_adds_bounded_dynamic_composition_stage_when_proof_mode_is_applied():
    authored_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="genealogy_target_profile",
                view_name="Target Work Profile",
                renderer_type="accordion",
                renderer_config={},
                position=1.0,
            )
        ],
        view_count=1,
    )
    composed_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1,
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="dynamic_genealogy_briefing",
                view_name="Situation Map",
                renderer_type="accordion",
                renderer_config={},
                position=1.0,
                child_view_keys=["genealogy_target_profile"],
                derivation_kind="generated_runtime_parent",
            ),
            EffectiveManifestView(
                view_key="genealogy_target_profile",
                view_name="Target Work Profile",
                renderer_type="accordion",
                renderer_config={},
                source_parent_view_key="dynamic_genealogy_briefing",
                display_parent_view_key="dynamic_genealogy_briefing",
                position=1.1,
            ),
        ],
        view_count=2,
    )
    view_def = SimpleNamespace(
        view_key="genealogy_target_profile",
        view_name="Target Work Profile",
        description="",
        renderer_type="accordion",
        renderer_config={},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=1.0,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=1.0,
            engine_key="inferential_commitment_mapper",
            chain_key=None,
            scope="aggregated",
            result_path="",
        ),
    )
    recommendation = {"view_key": "genealogy_target_profile", "priority": "primary", "rationale": "Rich content"}
    composition = SimpleNamespace(
        renderer_type="accordion",
        renderer_config={},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )

    def _manifest(job_id, *, consumer_key, slim=True, composition_mode=None, served_intent=None):
        return composed_manifest if composition_mode else authored_manifest

    fake_registry = SimpleNamespace(
        get=lambda key: view_def if key == view_def.view_key else None,
        list_all=lambda: [],
    )

    with patch("src.presenter.decision_trace.get_job", return_value={"plan_id": "plan-1"}), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value="intellectual_genealogy",
    ), patch(
        "src.presenter.decision_trace.build_presentation_manifest",
        side_effect=_manifest,
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=fake_registry,
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
        trace = build_presentation_trace(
            "job-1",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1,
        )

    assert trace.composition_status == "applied"
    assert trace.entries[-1].stage == "bounded_dynamic_composition"
    assert trace.final_manifest.model_dump() == composed_manifest.model_dump()
    assert [view.view_key for view in trace.entries[-2].snapshot] == ["genealogy_target_profile"]
    assert [view.view_key for view in trace.entries[-1].snapshot] == [
        "dynamic_genealogy_briefing",
        "genealogy_target_profile",
    ]


def test_trace_adds_adaptive_surface_selection_stage_with_selector_details():
    authored_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="genealogy_relationship_landscape",
                view_name="Relationship Landscape",
                renderer_type="card_grid",
                renderer_config={"columns": 1},
                position=1.1,
            )
        ],
        view_count=1,
    )
    composed_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="genealogy_relationship_landscape",
                view_name="Relationship Dossier",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "focus_summary", "title": "Why This Relationship Dominates"}]},
                position=1.1,
                derivation_kind="runtime_surface_family",
            )
        ],
        view_count=1,
    )
    view_def = SimpleNamespace(
        view_key="genealogy_relationship_landscape",
        view_name="Relationship Landscape",
        description="",
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=1.1,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=1.5,
            engine_key="genealogy_relationship_classification",
            chain_key=None,
            scope="per_item",
            result_path="",
        ),
    )
    recommendation = {"view_key": "genealogy_relationship_landscape", "priority": "primary", "rationale": "Rich content"}
    composition = SimpleNamespace(
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )

    def _manifest(job_id, *, consumer_key, slim=True, composition_mode=None, served_intent=None):
        return composed_manifest if composition_mode else authored_manifest

    fake_registry = SimpleNamespace(
        get=lambda key: view_def if key == view_def.view_key else None,
        list_all=lambda: [],
    )

    with patch("src.presenter.decision_trace.get_job", return_value={"plan_id": "plan-1"}), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value="intellectual_genealogy",
    ), patch(
        "src.presenter.decision_trace.build_presentation_manifest",
        side_effect=_manifest,
    ), patch(
        "src.presenter.decision_trace._prepare_page_payloads",
        return_value={"payloads": {"genealogy_relationship_landscape": _adaptive_relationship_payload()}},
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=fake_registry,
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
        trace = build_presentation_trace(
            "job-1",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
        )

    assert trace.composition_status == "applied"
    assert trace.entries[-1].stage == "adaptive_surface_selection"
    assert trace.entries[-1].details["selected_family"] == "relationship_profile_dossier"
    assert trace.entries[-1].details["signal_summary"]["relationship_count"] == 3
    assert trace.final_manifest.model_dump() == composed_manifest.model_dump()


def test_trace_adds_adaptive_surface_selection_stage_with_declarative_selector_details():
    authored_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="genealogy_relationship_landscape",
                view_name="Relationship Landscape",
                renderer_type="card_grid",
                renderer_config={"columns": 1},
                position=1.1,
            )
        ],
        view_count=1,
    )
    composed_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="genealogy_relationship_landscape",
                view_name="Relationship Dossier",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "focus_summary", "title": "Why This Relationship Dominates"}]},
                position=1.1,
                derivation_kind="runtime_surface_family",
            )
        ],
        view_count=1,
    )
    view_def = SimpleNamespace(
        view_key="genealogy_relationship_landscape",
        view_name="Relationship Landscape",
        description="",
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=1.1,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=1.5,
            engine_key="genealogy_relationship_classification",
            chain_key=None,
            scope="per_item",
            result_path="",
        ),
    )
    recommendation = {"view_key": "genealogy_relationship_landscape", "priority": "primary", "rationale": "Rich content"}
    composition = SimpleNamespace(
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )

    def _manifest(job_id, *, consumer_key, slim=True, composition_mode=None, served_intent=None):
        return composed_manifest if composition_mode else authored_manifest

    fake_registry = SimpleNamespace(
        get=lambda key: view_def if key == view_def.view_key else None,
        list_all=lambda: [],
    )

    with patch("src.presenter.decision_trace.get_job", return_value={"plan_id": "plan-1"}), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value="intellectual_genealogy",
    ), patch(
        "src.presenter.decision_trace.build_presentation_manifest",
        side_effect=_manifest,
    ), patch(
        "src.presenter.decision_trace._prepare_page_payloads",
        return_value={"payloads": {"genealogy_relationship_landscape": _adaptive_relationship_payload()}},
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=fake_registry,
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
        trace = build_presentation_trace(
            "job-1",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
        )

    assert trace.composition_status == "applied"
    assert trace.entries[-1].stage == "adaptive_surface_selection"
    assert trace.entries[-1].details["selected_family"] == "relationship_profile_dossier"
    rejected_families = {item["family"] for item in trace.entries[-1].details["rejected_families"]}
    assert rejected_families == {"relationship_comparison_review"}
    assert trace.final_manifest.model_dump() == composed_manifest.model_dump()


def test_trace_adds_adaptive_surface_selection_stage_with_aoi_selector_details():
    authored_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="aoi_by_theme",
                view_name="By Theme",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "theme_a", "title": "Theme A"}]},
                position=1.2,
                parent_view_key="aoi_thematic_analysis",
            )
        ],
        view_count=1,
    )
    composed_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1,
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="aoi_by_theme",
                view_name="Theme Dossier",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "suite_summary", "title": "Theme Summary"}]},
                position=1.2,
                parent_view_key="aoi_thematic_analysis",
                derivation_kind="runtime_surface_family",
            )
        ],
        view_count=1,
    )
    view_def = SimpleNamespace(
        view_key="aoi_by_theme",
        view_name="By Theme",
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "theme_a", "title": "Theme A"}]},
        presentation_stance="comparison",
        visibility="if_data_exists",
        position=1.2,
        parent_view_key="aoi_thematic_analysis",
        data_source=SimpleNamespace(
            phase_number=3.0,
            engine_key="aoi_sin_findings",
            chain_key=None,
            scope="aggregated",
            result_path="",
        ),
    )
    recommendation = {"view_key": "aoi_by_theme", "priority": "primary", "rationale": "Rich content"}
    composition = SimpleNamespace(
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "theme_a", "title": "Theme A"}]},
        presentation_stance="comparison",
        data_quality="rich",
        dropped_overrides=[],
    )

    def _manifest(job_id, *, consumer_key, slim=True, composition_mode=None, served_intent=None):
        return composed_manifest if composition_mode else authored_manifest

    fake_registry = SimpleNamespace(
        get=lambda key: view_def if key == view_def.view_key else None,
        list_all=lambda: [],
    )

    with patch("src.presenter.decision_trace.get_job", return_value={"plan_id": "plan-1"}), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value=AOI_WORKFLOW_KEY,
    ), patch(
        "src.presenter.decision_trace.build_presentation_manifest",
        side_effect=_manifest,
    ), patch(
        "src.presenter.decision_trace._prepare_page_payloads",
        return_value={"payloads": {"aoi_by_theme": _adaptive_aoi_theme_payload()}},
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=fake_registry,
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
        trace = build_presentation_trace(
            "job-1",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1,
        )

    assert trace.composition_status == "applied"
    assert trace.entries[-1].stage == "adaptive_surface_selection"
    assert trace.entries[-1].details["target_surface"] == "aoi_by_theme"
    assert trace.entries[-1].details["selected_family"] == "aoi_theme_dossier"
    assert trace.entries[-1].details["signal_summary"]["theme_count"] == 2
    assert trace.final_manifest.model_dump() == composed_manifest.model_dump()


def test_trace_adds_adaptive_surface_suite_selection_stage_with_aoi_surface_decisions():
    authored_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="aoi_by_theme",
                view_name="By Theme",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "theme_a", "title": "Theme A"}]},
                position=1.2,
                parent_view_key="aoi_thematic_analysis",
            ),
            EffectiveManifestView(
                view_key="aoi_thematic_report",
                view_name="Report",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "summary", "title": "Summary"}]},
                position=1.4,
                parent_view_key="aoi_thematic_analysis",
            ),
        ],
        view_count=2,
    )
    composed_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="aoi_by_theme",
                view_name="Theme Dossier",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "suite_summary", "title": "Theme Summary"}]},
                position=1.2,
                parent_view_key="aoi_thematic_analysis",
                derivation_kind="runtime_surface_family",
            ),
            EffectiveManifestView(
                view_key="aoi_thematic_report",
                view_name="Report Evidence Review",
                renderer_type="table",
                renderer_config={"compact": True, "sortable": True},
                position=1.4,
                parent_view_key="aoi_thematic_analysis",
                derivation_kind="runtime_surface_family",
            ),
        ],
        view_count=2,
    )
    theme_view_def = SimpleNamespace(
        view_key="aoi_by_theme",
        view_name="By Theme",
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "theme_a", "title": "Theme A"}]},
        presentation_stance="comparison",
        visibility="if_data_exists",
        position=1.2,
        parent_view_key="aoi_thematic_analysis",
        data_source=SimpleNamespace(phase_number=3.0, engine_key="aoi_sin_findings", chain_key=None, scope="aggregated", result_path=""),
    )
    report_view_def = SimpleNamespace(
        view_key="aoi_thematic_report",
        view_name="Report",
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "summary", "title": "Summary"}]},
        presentation_stance="summary",
        visibility="if_data_exists",
        position=1.4,
        parent_view_key="aoi_thematic_analysis",
        data_source=SimpleNamespace(phase_number=4.0, engine_key="aoi_thematic_report", chain_key=None, scope="aggregated", result_path=""),
    )
    recommendation_theme = {"view_key": "aoi_by_theme", "priority": "primary", "rationale": "Rich content"}
    recommendation_report = {"view_key": "aoi_thematic_report", "priority": "secondary", "rationale": "Structured closeout"}
    composition = SimpleNamespace(
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "theme_a", "title": "Theme A"}]},
        presentation_stance="comparison",
        data_quality="rich",
        dropped_overrides=[],
    )

    def _manifest(job_id, *, consumer_key, slim=True, composition_mode=None, served_intent=None):
        return composed_manifest if composition_mode else authored_manifest

    fake_registry = SimpleNamespace(
        get=lambda key: (
            theme_view_def
            if key == theme_view_def.view_key
            else report_view_def
            if key == report_view_def.view_key
            else None
        ),
        list_all=lambda: [],
    )

    with patch("src.presenter.decision_trace.get_job", return_value={"plan_id": "plan-1"}), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value=AOI_WORKFLOW_KEY,
    ), patch(
        "src.presenter.decision_trace.build_presentation_manifest",
        side_effect=_manifest,
    ), patch(
        "src.presenter.decision_trace._prepare_page_payloads",
        return_value={"payloads": {"aoi_by_theme": _adaptive_aoi_theme_payload(), "aoi_thematic_report": _adaptive_aoi_report_payload()}},
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=[recommendation_theme, recommendation_report],
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=[recommendation_theme, recommendation_report],
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=fake_registry,
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
        trace = build_presentation_trace(
            "job-1",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
        )

    assert trace.composition_status == "applied"
    assert trace.entries[-1].stage == "adaptive_surface_suite_selection"
    decisions = trace.entries[-1].details["surface_decisions"]
    assert len(decisions) == 2
    assert decisions[0]["target_surface"] == "aoi_by_theme"
    assert decisions[1]["target_surface"] == "aoi_thematic_report"
    assert decisions[0]["selected_family"] == "aoi_theme_dossier"
    assert decisions[1]["selected_family"] == "aoi_report_evidence_review"
    assert trace.final_manifest.model_dump() == composed_manifest.model_dump()


def test_trace_returns_authored_final_manifest_when_aoi_suite_renderer_contract_is_invalid():
    authored_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="aoi_by_theme",
                view_name="By Theme",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "theme_a", "title": "Theme A"}]},
                position=1.2,
                parent_view_key="aoi_thematic_analysis",
            ),
            EffectiveManifestView(
                view_key="aoi_thematic_report",
                view_name="Report",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "summary", "title": "Summary"}]},
                position=1.4,
                parent_view_key="aoi_thematic_analysis",
            ),
        ],
        view_count=2,
    )
    issue = CompositionIssue(
        view_key="aoi_thematic_report",
        field="renderer_type",
        message="Renderer contract is missing for served renderer 'mini_card_list'.",
        reason="renderer_definition_missing",
    )
    theme_view_def = SimpleNamespace(
        view_key="aoi_by_theme",
        view_name="By Theme",
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "theme_a", "title": "Theme A"}]},
        presentation_stance="comparison",
        visibility="if_data_exists",
        position=1.2,
        parent_view_key="aoi_thematic_analysis",
        data_source=SimpleNamespace(phase_number=3.0, engine_key="aoi_sin_findings", chain_key=None, scope="aggregated", result_path=""),
    )
    report_view_def = SimpleNamespace(
        view_key="aoi_thematic_report",
        view_name="Report",
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "summary", "title": "Summary"}]},
        presentation_stance="summary",
        visibility="if_data_exists",
        position=1.4,
        parent_view_key="aoi_thematic_analysis",
        data_source=SimpleNamespace(phase_number=4.0, engine_key="aoi_thematic_report", chain_key=None, scope="aggregated", result_path=""),
    )
    recommendation_theme = {"view_key": "aoi_by_theme", "priority": "primary", "rationale": "Rich content"}
    recommendation_report = {"view_key": "aoi_thematic_report", "priority": "secondary", "rationale": "Structured closeout"}
    composition = SimpleNamespace(
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "theme_a", "title": "Theme A"}]},
        presentation_stance="comparison",
        data_quality="rich",
        dropped_overrides=[],
    )

    def _manifest(job_id, *, consumer_key, slim=True, composition_mode=None, served_intent=None):
        if composition_mode:
            raise BoundedCompositionValidationError([issue])
        return authored_manifest

    fake_registry = SimpleNamespace(
        get=lambda key: (
            theme_view_def
            if key == theme_view_def.view_key
            else report_view_def
            if key == report_view_def.view_key
            else None
        ),
        list_all=lambda: [],
    )

    with patch("src.presenter.decision_trace.get_job", return_value={"plan_id": "plan-1"}), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value=AOI_WORKFLOW_KEY,
    ), patch(
        "src.presenter.decision_trace.build_presentation_manifest",
        side_effect=_manifest,
    ), patch(
        "src.presenter.decision_trace._prepare_page_payloads",
        return_value={"payloads": {"aoi_by_theme": _adaptive_aoi_theme_payload(), "aoi_thematic_report": _adaptive_aoi_report_payload()}},
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=[recommendation_theme, recommendation_report],
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=[recommendation_theme, recommendation_report],
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=fake_registry,
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
        trace = build_presentation_trace(
            "job-1",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
        )

    assert trace.composition_status == "invalid"
    assert trace.composition_issues[0].reason == "renderer_definition_missing"
    assert trace.final_manifest.model_dump() == authored_manifest.model_dump()
    assert trace.entries[-1].stage == "adaptive_surface_suite_selection"
    assert trace.entries[-1].reason.endswith("authored pre-composition manifest retained.")


def test_trace_adds_adaptive_surface_suite_selection_stage_with_surface_decisions():
    authored_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="genealogy_relationship_landscape",
                view_name="Relationship Landscape",
                renderer_type="card_grid",
                renderer_config={"columns": 1},
                position=1.1,
            ),
            EffectiveManifestView(
                view_key="genealogy_conditions",
                view_name="Conditions of Possibility",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "conditions_snapshot", "title": "Conditions Snapshot"}]},
                position=4.0,
            ),
        ],
        view_count=2,
    )
    composed_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="genealogy_relationship_landscape",
                view_name="Relationship Dossier",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "focus_summary", "title": "Why This Relationship Dominates"}]},
                position=1.1,
                derivation_kind="runtime_surface_family",
            ),
            EffectiveManifestView(
                view_key="genealogy_conditions",
                view_name="Conditions Path-Dependency Matrix",
                renderer_type="table",
                renderer_config={"compact": True, "sortable": True},
                position=4.0,
                derivation_kind="runtime_surface_family",
            ),
        ],
        view_count=2,
    )
    relationship_view_def = SimpleNamespace(
        view_key="genealogy_relationship_landscape",
        view_name="Relationship Landscape",
        description="",
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=1.1,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=1.5,
            engine_key="genealogy_relationship_classification",
            chain_key=None,
            scope="per_item",
            result_path="",
        ),
    )
    conditions_view_def = SimpleNamespace(
        view_key="genealogy_conditions",
        view_name="Conditions of Possibility",
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "conditions_snapshot", "title": "Conditions Snapshot"}]},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=4.0,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=3.0,
            engine_key="conditions_of_possibility_analyzer",
            chain_key=None,
            scope="aggregated",
            result_path="",
        ),
    )
    recommendations = [
        {"view_key": "genealogy_relationship_landscape", "priority": "primary", "rationale": "Rich content"},
        {"view_key": "genealogy_conditions", "priority": "primary", "rationale": "Rich content"},
    ]
    relationship_composition = SimpleNamespace(
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )
    conditions_composition = SimpleNamespace(
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "conditions_snapshot", "title": "Conditions Snapshot"}]},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )

    def _manifest(job_id, *, consumer_key, slim=True, composition_mode=None, served_intent=None):
        return composed_manifest if composition_mode else authored_manifest

    fake_registry = SimpleNamespace(
        get=lambda key: {
            relationship_view_def.view_key: relationship_view_def,
            conditions_view_def.view_key: conditions_view_def,
        }.get(key),
        list_all=lambda: [],
    )

    with patch("src.presenter.decision_trace.get_job", return_value={"plan_id": "plan-1"}), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value="intellectual_genealogy",
    ), patch(
        "src.presenter.decision_trace.build_presentation_manifest",
        side_effect=_manifest,
    ), patch(
        "src.presenter.decision_trace._prepare_page_payloads",
        return_value={
            "payloads": {
                "genealogy_relationship_landscape": _adaptive_relationship_payload(),
                "genealogy_conditions": _adaptive_conditions_payload(),
            }
        },
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=recommendations,
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=recommendations,
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=fake_registry,
    ), patch(
        "src.presenter.decision_trace.resolve_effective_composition",
        side_effect=lambda view_def, **kwargs: (
            relationship_composition
            if view_def.view_key == "genealogy_relationship_landscape"
            else conditions_composition
        ),
    ), patch(
        "src.presenter.decision_trace.resolve_effective_render_contract",
        side_effect=lambda view_def, **kwargs: (
            relationship_composition
            if view_def.view_key == "genealogy_relationship_landscape"
            else conditions_composition
        ),
    ), patch(
        "src.presenter.decision_trace.load_selected_variants",
        return_value=[],
    ):
        trace = build_presentation_trace(
            "job-1",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
        )

    assert trace.composition_status == "applied"
    assert trace.entries[-1].stage == "adaptive_surface_suite_selection"
    assert trace.entries[-1].details["surface_decisions"][0]["selected_family"] == "relationship_profile_dossier"
    assert trace.entries[-1].details["surface_decisions"][1]["selected_family"] == "conditions_path_dependency_matrix"
    assert trace.final_manifest.model_dump() == composed_manifest.model_dump()


def test_trace_adds_adaptive_surface_suite_selection_stage_with_declarative_suite_surface_decisions():
    authored_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="genealogy_relationship_landscape",
                view_name="Relationship Landscape",
                renderer_type="card_grid",
                renderer_config={"columns": 1},
                position=1.1,
            ),
            EffectiveManifestView(
                view_key="genealogy_conditions",
                view_name="Conditions of Possibility",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "conditions_snapshot", "title": "Conditions Snapshot"}]},
                position=4.0,
            ),
        ],
        view_count=2,
    )
    composed_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="genealogy_relationship_landscape",
                view_name="Relationship Dossier",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "focus_summary", "title": "Why This Relationship Dominates"}]},
                position=1.1,
                derivation_kind="runtime_surface_family",
            ),
            EffectiveManifestView(
                view_key="genealogy_conditions",
                view_name="Conditions Path-Dependency Matrix",
                renderer_type="table",
                renderer_config={"compact": True, "sortable": True},
                position=4.0,
                derivation_kind="runtime_surface_family",
            ),
        ],
        view_count=2,
    )
    relationship_view_def = SimpleNamespace(
        view_key="genealogy_relationship_landscape",
        view_name="Relationship Landscape",
        description="",
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=1.1,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=1.5,
            engine_key="genealogy_relationship_classification",
            chain_key=None,
            scope="per_item",
            result_path="",
        ),
    )
    conditions_view_def = SimpleNamespace(
        view_key="genealogy_conditions",
        view_name="Conditions of Possibility",
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "conditions_snapshot", "title": "Conditions Snapshot"}]},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=4.0,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=3.0,
            engine_key="conditions_of_possibility_analyzer",
            chain_key=None,
            scope="aggregated",
            result_path="",
        ),
    )
    recommendations = [
        {"view_key": "genealogy_relationship_landscape", "priority": "primary", "rationale": "Rich content"},
        {"view_key": "genealogy_conditions", "priority": "primary", "rationale": "Rich content"},
    ]
    relationship_composition = SimpleNamespace(
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )
    conditions_composition = SimpleNamespace(
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "conditions_snapshot", "title": "Conditions Snapshot"}]},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )

    def _manifest(job_id, *, consumer_key, slim=True, composition_mode=None, served_intent=None):
        return composed_manifest if composition_mode else authored_manifest

    fake_registry = SimpleNamespace(
        get=lambda key: {
            relationship_view_def.view_key: relationship_view_def,
            conditions_view_def.view_key: conditions_view_def,
        }.get(key),
        list_all=lambda: [],
    )

    with patch("src.presenter.decision_trace.get_job", return_value={"plan_id": "plan-1"}), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value="intellectual_genealogy",
    ), patch(
        "src.presenter.decision_trace.build_presentation_manifest",
        side_effect=_manifest,
    ), patch(
        "src.presenter.decision_trace._prepare_page_payloads",
        return_value={
            "payloads": {
                "genealogy_relationship_landscape": _adaptive_relationship_payload(),
                "genealogy_conditions": _adaptive_conditions_payload(),
            }
        },
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=recommendations,
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=recommendations,
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=fake_registry,
    ), patch(
        "src.presenter.decision_trace.resolve_effective_composition",
        side_effect=lambda view_def, **kwargs: (
            relationship_composition
            if view_def.view_key == "genealogy_relationship_landscape"
            else conditions_composition
        ),
    ), patch(
        "src.presenter.decision_trace.resolve_effective_render_contract",
        side_effect=lambda view_def, **kwargs: (
            relationship_composition
            if view_def.view_key == "genealogy_relationship_landscape"
            else conditions_composition
        ),
    ), patch(
        "src.presenter.decision_trace.load_selected_variants",
        return_value=[],
    ):
        trace = build_presentation_trace(
            "job-1",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
        )

    assert trace.composition_status == "applied"
    assert trace.entries[-1].stage == "adaptive_surface_suite_selection"
    assert trace.entries[-1].details["surface_decisions"][0]["selected_family"] == "relationship_profile_dossier"
    assert trace.entries[-1].details["surface_decisions"][1]["selected_family"] == "conditions_path_dependency_matrix"
    relationship_rejections = {
        item["family"] for item in trace.entries[-1].details["surface_decisions"][0]["rejected_families"]
    }
    assert relationship_rejections == {"relationship_comparison_review"}
    assert trace.final_manifest.model_dump() == composed_manifest.model_dump()


def test_trace_returns_authored_final_manifest_when_proof_mode_is_invalid():
    authored_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="genealogy_target_profile",
                view_name="Target Work Profile",
                renderer_type="accordion",
                renderer_config={},
                position=1.0,
            )
        ],
        view_count=1,
    )
    issue = CompositionIssue(
        view_key="dynamic_genealogy_briefing",
        field="renderer_config",
        message="bad config",
        reason="renderer_config_validation_failed",
    )
    view_def = SimpleNamespace(
        view_key="genealogy_target_profile",
        view_name="Target Work Profile",
        description="",
        renderer_type="accordion",
        renderer_config={},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=1.0,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=1.0,
            engine_key="inferential_commitment_mapper",
            chain_key=None,
            scope="aggregated",
            result_path="",
        ),
    )
    recommendation = {"view_key": "genealogy_target_profile", "priority": "primary", "rationale": "Rich content"}
    composition = SimpleNamespace(
        renderer_type="accordion",
        renderer_config={},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )

    def _manifest(job_id, *, consumer_key, slim=True, composition_mode=None, served_intent=None):
        if composition_mode:
            raise BoundedCompositionValidationError([issue])
        return authored_manifest

    fake_registry = SimpleNamespace(
        get=lambda key: view_def if key == view_def.view_key else None,
        list_all=lambda: [],
    )

    with patch("src.presenter.decision_trace.get_job", return_value={"plan_id": "plan-1"}), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value="intellectual_genealogy",
    ), patch(
        "src.presenter.decision_trace.build_presentation_manifest",
        side_effect=_manifest,
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=fake_registry,
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
        trace = build_presentation_trace(
            "job-1",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1,
        )

    assert trace.composition_status == "invalid"
    assert trace.composition_issues[0].reason == "renderer_config_validation_failed"
    assert trace.final_manifest.model_dump() == authored_manifest.model_dump()
    assert trace.entries[-1].stage == "bounded_dynamic_composition"
    assert trace.entries[-1].reason.endswith("authored pre-composition manifest retained.")
    assert [view.view_key for view in trace.entries[-1].snapshot] == ["genealogy_target_profile"]


def test_trace_returns_authored_final_manifest_when_adaptive_surface_proof_is_invalid():
    authored_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="genealogy_relationship_landscape",
                view_name="Relationship Landscape",
                renderer_type="card_grid",
                renderer_config={"columns": 1},
                position=1.1,
            )
        ],
        view_count=1,
    )
    issue = CompositionIssue(
        view_key="genealogy_relationship_landscape",
        field="renderer_config",
        message="bad config",
        reason="renderer_config_validation_failed",
    )
    view_def = SimpleNamespace(
        view_key="genealogy_relationship_landscape",
        view_name="Relationship Landscape",
        description="",
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=1.1,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=1.5,
            engine_key="genealogy_relationship_classification",
            chain_key=None,
            scope="per_item",
            result_path="",
        ),
    )
    recommendation = {"view_key": "genealogy_relationship_landscape", "priority": "primary", "rationale": "Rich content"}
    composition = SimpleNamespace(
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )

    def _manifest(job_id, *, consumer_key, slim=True, composition_mode=None, served_intent=None):
        if composition_mode:
            raise BoundedCompositionValidationError([issue])
        return authored_manifest

    fake_registry = SimpleNamespace(
        get=lambda key: view_def if key == view_def.view_key else None,
        list_all=lambda: [],
    )

    with patch("src.presenter.decision_trace.get_job", return_value={"plan_id": "plan-1"}), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value="intellectual_genealogy",
    ), patch(
        "src.presenter.decision_trace.build_presentation_manifest",
        side_effect=_manifest,
    ), patch(
        "src.presenter.decision_trace._prepare_page_payloads",
        return_value={"payloads": {"genealogy_relationship_landscape": _adaptive_relationship_payload()}},
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=fake_registry,
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
        trace = build_presentation_trace(
            "job-1",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
        )

    assert trace.composition_status == "invalid"
    assert trace.composition_issues[0].reason == "renderer_config_validation_failed"
    assert trace.final_manifest.model_dump() == authored_manifest.model_dump()
    assert trace.entries[-1].stage == "adaptive_surface_selection"
    assert trace.entries[-1].details["selected_family"] == "relationship_profile_dossier"
    assert trace.entries[-1].reason.endswith("authored pre-composition manifest retained.")
    assert [view.view_key for view in trace.entries[-1].snapshot] == ["genealogy_relationship_landscape"]


def test_trace_records_composition_issues_for_invalid_declarative_spec_even_when_stage_details_are_empty():
    authored_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="genealogy_relationship_landscape",
                view_name="Relationship Landscape",
                renderer_type="card_grid",
                renderer_config={"columns": 1},
                position=1.1,
            )
        ],
        view_count=1,
    )
    issue = CompositionIssue(
        view_key="genealogy_relationship_landscape",
        field="composition_mode",
        message="Adaptive composition spec is invalid: declarative_relationship_surface_v1",
        reason="adaptive_spec_validation_failed",
    )
    view_def = SimpleNamespace(
        view_key="genealogy_relationship_landscape",
        view_name="Relationship Landscape",
        description="",
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=1.1,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=1.5,
            engine_key="genealogy_relationship_classification",
            chain_key=None,
            scope="per_item",
            result_path="",
        ),
    )
    recommendation = {"view_key": "genealogy_relationship_landscape", "priority": "primary", "rationale": "Rich content"}
    composition = SimpleNamespace(
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )

    def _manifest(job_id, *, consumer_key, slim=True, composition_mode=None, served_intent=None):
        if composition_mode:
            raise BoundedCompositionValidationError([issue])
        return authored_manifest

    fake_registry = SimpleNamespace(
        get=lambda key: view_def if key == view_def.view_key else None,
        list_all=lambda: [],
    )

    with patch("src.presenter.decision_trace.get_job", return_value={"plan_id": "plan-1"}), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value="intellectual_genealogy",
    ), patch(
        "src.presenter.decision_trace.build_presentation_manifest",
        side_effect=_manifest,
    ), patch(
        "src.presenter.decision_trace._prepare_page_payloads",
        return_value={"payloads": {"genealogy_relationship_landscape": _adaptive_relationship_payload()}},
    ), patch(
        "src.presenter.decision_trace.inspect_runtime_composition",
        side_effect=BoundedCompositionValidationError([issue]),
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=fake_registry,
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
        trace = build_presentation_trace(
            "job-1",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
        )

    assert trace.composition_status == "invalid"
    assert trace.composition_issues[0].reason == "adaptive_spec_validation_failed"
    assert trace.entries[-1].stage == "adaptive_surface_selection"
    assert trace.entries[-1].details == {}
    assert trace.final_manifest.model_dump() == authored_manifest.model_dump()


def test_trace_records_composition_issues_for_invalid_declarative_suite_spec_even_when_stage_details_are_empty():
    authored_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="genealogy_relationship_landscape",
                view_name="Relationship Landscape",
                renderer_type="card_grid",
                renderer_config={"columns": 1},
                position=1.1,
            ),
            EffectiveManifestView(
                view_key="genealogy_conditions",
                view_name="Conditions of Possibility",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "conditions_snapshot", "title": "Conditions Snapshot"}]},
                position=4.0,
            ),
        ],
        view_count=2,
    )
    issue = CompositionIssue(
        view_key="__suite_spec__:declarative_genealogy_relationship_conditions_suite_v1",
        field="composition_mode",
        message="Adaptive suite composition spec is invalid: declarative_genealogy_relationship_conditions_suite_v1",
        reason="adaptive_spec_validation_failed",
    )
    relationship_view_def = SimpleNamespace(
        view_key="genealogy_relationship_landscape",
        view_name="Relationship Landscape",
        description="",
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=1.1,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=1.5,
            engine_key="genealogy_relationship_classification",
            chain_key=None,
            scope="per_item",
            result_path="",
        ),
    )
    conditions_view_def = SimpleNamespace(
        view_key="genealogy_conditions",
        view_name="Conditions of Possibility",
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "conditions_snapshot", "title": "Conditions Snapshot"}]},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=4.0,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=3.0,
            engine_key="conditions_of_possibility_analyzer",
            chain_key=None,
            scope="aggregated",
            result_path="",
        ),
    )
    recommendations = [
        {"view_key": "genealogy_relationship_landscape", "priority": "primary", "rationale": "Rich content"},
        {"view_key": "genealogy_conditions", "priority": "primary", "rationale": "Rich content"},
    ]
    relationship_composition = SimpleNamespace(
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )
    conditions_composition = SimpleNamespace(
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "conditions_snapshot", "title": "Conditions Snapshot"}]},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )

    def _manifest(job_id, *, consumer_key, slim=True, composition_mode=None, served_intent=None):
        if composition_mode:
            raise BoundedCompositionValidationError([issue])
        return authored_manifest

    fake_registry = SimpleNamespace(
        get=lambda key: {
            relationship_view_def.view_key: relationship_view_def,
            conditions_view_def.view_key: conditions_view_def,
        }.get(key),
        list_all=lambda: [],
    )

    with patch("src.presenter.decision_trace.get_job", return_value={"plan_id": "plan-1"}), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value="intellectual_genealogy",
    ), patch(
        "src.presenter.decision_trace.build_presentation_manifest",
        side_effect=_manifest,
    ), patch(
        "src.presenter.decision_trace._prepare_page_payloads",
        return_value={
            "payloads": {
                "genealogy_relationship_landscape": _adaptive_relationship_payload(),
                "genealogy_conditions": _adaptive_conditions_payload(),
            }
        },
    ), patch(
        "src.presenter.decision_trace.inspect_runtime_composition",
        side_effect=BoundedCompositionValidationError([issue]),
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=recommendations,
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=recommendations,
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=fake_registry,
    ), patch(
        "src.presenter.decision_trace.resolve_effective_composition",
        side_effect=lambda view_def, **kwargs: (
            relationship_composition
            if view_def.view_key == "genealogy_relationship_landscape"
            else conditions_composition
        ),
    ), patch(
        "src.presenter.decision_trace.resolve_effective_render_contract",
        side_effect=lambda view_def, **kwargs: (
            relationship_composition
            if view_def.view_key == "genealogy_relationship_landscape"
            else conditions_composition
        ),
    ), patch(
        "src.presenter.decision_trace.load_selected_variants",
        return_value=[],
    ):
        trace = build_presentation_trace(
            "job-1",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
        )

    assert trace.composition_status == "invalid"
    assert trace.composition_issues[0].reason == "adaptive_spec_validation_failed"
    assert trace.composition_issues[0].view_key == "__suite_spec__:declarative_genealogy_relationship_conditions_suite_v1"
    assert trace.entries[-1].stage == "adaptive_surface_suite_selection"
    assert trace.entries[-1].details == {}
    assert trace.final_manifest.model_dump() == authored_manifest.model_dump()


def test_trace_returns_authored_final_manifest_when_adaptive_aoi_surface_proof_is_invalid():
    authored_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="aoi_by_theme",
                view_name="By Theme",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "theme_a", "title": "Theme A"}]},
                position=1.2,
                parent_view_key="aoi_thematic_analysis",
            )
        ],
        view_count=1,
    )
    issue = CompositionIssue(
        view_key="aoi_by_theme",
        field="renderer_config",
        message="bad config",
        reason="renderer_config_validation_failed",
    )
    view_def = SimpleNamespace(
        view_key="aoi_by_theme",
        view_name="By Theme",
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "theme_a", "title": "Theme A"}]},
        presentation_stance="comparison",
        visibility="if_data_exists",
        position=1.2,
        parent_view_key="aoi_thematic_analysis",
        data_source=SimpleNamespace(
            phase_number=3.0,
            engine_key="aoi_sin_findings",
            chain_key=None,
            scope="aggregated",
            result_path="",
        ),
    )
    recommendation = {"view_key": "aoi_by_theme", "priority": "primary", "rationale": "Rich content"}
    composition = SimpleNamespace(
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "theme_a", "title": "Theme A"}]},
        presentation_stance="comparison",
        data_quality="rich",
        dropped_overrides=[],
    )

    def _manifest(job_id, *, consumer_key, slim=True, composition_mode=None, served_intent=None):
        if composition_mode:
            raise BoundedCompositionValidationError([issue])
        return authored_manifest

    fake_registry = SimpleNamespace(
        get=lambda key: view_def if key == view_def.view_key else None,
        list_all=lambda: [],
    )

    with patch("src.presenter.decision_trace.get_job", return_value={"plan_id": "plan-1"}), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value=AOI_WORKFLOW_KEY,
    ), patch(
        "src.presenter.decision_trace.build_presentation_manifest",
        side_effect=_manifest,
    ), patch(
        "src.presenter.decision_trace._prepare_page_payloads",
        return_value={"payloads": {"aoi_by_theme": _adaptive_aoi_theme_payload()}},
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=[recommendation],
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=fake_registry,
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
        trace = build_presentation_trace(
            "job-1",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1,
        )

    assert trace.composition_status == "invalid"
    assert trace.composition_issues[0].reason == "renderer_config_validation_failed"
    assert trace.final_manifest.model_dump() == authored_manifest.model_dump()
    assert trace.entries[-1].stage == "adaptive_surface_selection"
    assert trace.entries[-1].details["target_surface"] == "aoi_by_theme"
    assert trace.entries[-1].details["selected_family"] == "aoi_theme_dossier"
    assert trace.entries[-1].reason.endswith("authored pre-composition manifest retained.")


def test_trace_returns_authored_final_manifest_when_adaptive_surface_suite_proof_is_invalid():
    authored_manifest = EffectivePresentationManifest(
        job_id="job-1",
        plan_id="plan-1",
        consumer_key="the-critic",
        style_school="explanatory_narrative",
        polish_state="polished",
        views=[
            EffectiveManifestView(
                view_key="genealogy_relationship_landscape",
                view_name="Relationship Landscape",
                renderer_type="card_grid",
                renderer_config={"columns": 1},
                position=1.1,
            ),
            EffectiveManifestView(
                view_key="genealogy_conditions",
                view_name="Conditions of Possibility",
                renderer_type="accordion",
                renderer_config={"sections": [{"key": "conditions_snapshot", "title": "Conditions Snapshot"}]},
                position=4.0,
            ),
        ],
        view_count=2,
    )
    issue = CompositionIssue(
        view_key="genealogy_conditions",
        field="renderer_config",
        message="bad config",
        reason="renderer_config_validation_failed",
    )
    relationship_view_def = SimpleNamespace(
        view_key="genealogy_relationship_landscape",
        view_name="Relationship Landscape",
        description="",
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=1.1,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=1.5,
            engine_key="genealogy_relationship_classification",
            chain_key=None,
            scope="per_item",
            result_path="",
        ),
    )
    conditions_view_def = SimpleNamespace(
        view_key="genealogy_conditions",
        view_name="Conditions of Possibility",
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "conditions_snapshot", "title": "Conditions Snapshot"}]},
        presentation_stance="diagnostic",
        visibility="if_data_exists",
        position=4.0,
        parent_view_key=None,
        data_source=SimpleNamespace(
            phase_number=3.0,
            engine_key="conditions_of_possibility_analyzer",
            chain_key=None,
            scope="aggregated",
            result_path="",
        ),
    )
    recommendations = [
        {"view_key": "genealogy_relationship_landscape", "priority": "primary", "rationale": "Rich content"},
        {"view_key": "genealogy_conditions", "priority": "primary", "rationale": "Rich content"},
    ]
    relationship_composition = SimpleNamespace(
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )
    conditions_composition = SimpleNamespace(
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "conditions_snapshot", "title": "Conditions Snapshot"}]},
        presentation_stance="diagnostic",
        data_quality="rich",
        dropped_overrides=[],
    )

    def _manifest(job_id, *, consumer_key, slim=True, composition_mode=None, served_intent=None):
        if composition_mode:
            raise BoundedCompositionValidationError([issue])
        return authored_manifest

    fake_registry = SimpleNamespace(
        get=lambda key: {
            relationship_view_def.view_key: relationship_view_def,
            conditions_view_def.view_key: conditions_view_def,
        }.get(key),
        list_all=lambda: [],
    )

    with patch("src.presenter.decision_trace.get_job", return_value={"plan_id": "plan-1"}), patch(
        "src.presenter.decision_trace.load_plan",
        return_value=SimpleNamespace(recommended_views=[]),
    ), patch(
        "src.presenter.decision_trace._resolve_workflow_key",
        return_value="intellectual_genealogy",
    ), patch(
        "src.presenter.decision_trace.build_presentation_manifest",
        side_effect=_manifest,
    ), patch(
        "src.presenter.decision_trace._prepare_page_payloads",
        return_value={
            "payloads": {
                "genealogy_relationship_landscape": _adaptive_relationship_payload(),
                "genealogy_conditions": _adaptive_conditions_payload(),
            }
        },
    ), patch(
        "src.presenter.decision_trace._get_recommendations",
        return_value=recommendations,
    ), patch(
        "src.presenter.decision_trace.get_default_recommendations_for_workflow",
        return_value=recommendations,
    ), patch(
        "src.presenter.decision_trace.get_view_registry",
        return_value=fake_registry,
    ), patch(
        "src.presenter.decision_trace.resolve_effective_composition",
        side_effect=lambda view_def, **kwargs: (
            relationship_composition
            if view_def.view_key == "genealogy_relationship_landscape"
            else conditions_composition
        ),
    ), patch(
        "src.presenter.decision_trace.resolve_effective_render_contract",
        side_effect=lambda view_def, **kwargs: (
            relationship_composition
            if view_def.view_key == "genealogy_relationship_landscape"
            else conditions_composition
        ),
    ), patch(
        "src.presenter.decision_trace.load_selected_variants",
        return_value=[],
    ):
        trace = build_presentation_trace(
            "job-1",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
        )

    assert trace.composition_status == "invalid"
    assert trace.composition_issues[0].reason == "renderer_config_validation_failed"
    assert trace.final_manifest.model_dump() == authored_manifest.model_dump()
    assert trace.entries[-1].stage == "adaptive_surface_suite_selection"
    assert trace.entries[-1].details["surface_decisions"][0]["selected_family"] == "relationship_profile_dossier"
    assert trace.entries[-1].details["surface_decisions"][1]["selected_family"] == "conditions_path_dependency_matrix"
    assert trace.entries[-1].reason.endswith("authored pre-composition manifest retained.")
