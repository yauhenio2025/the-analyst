from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.presenter import bounded_dynamic_composition as composition_module
from src.presenter.adaptive_specs import registry as adaptive_registry
from src.presenter.adaptive_specs.registry import AdaptiveSpecRegistryError
from src.presenter.bounded_dynamic_composition import (
    ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY,
    ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY,
    BoundedCompositionValidationError,
    COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
    COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
    COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
    COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
    DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_ISSUE_TARGET,
    _extract_conditions_surface_signals,
    _select_adaptive_conditions_surface,
    apply_bounded_dynamic_composition,
    inspect_runtime_composition,
)
from src.presenter.schemas import ViewPayload


def _relationship_item(
    title: str,
    *,
    relationship_type: str,
    relationship_strength: str,
    summary: str,
) -> dict[str, object]:
    return {
        "work_key": title.lower().replace(" ", "_"),
        "has_structured_data": True,
        "structured_data": {
            "work_title": title,
            "relationship_type": relationship_type,
            "relationship_strength": relationship_strength,
            "summary": summary,
            "centrality_assessment": summary,
            "influence_channels": [{"channel": "framework", "description": "Shared architecture"}],
            "key_evidence": [{"evidence_type": "citation", "description": "Explicit uptake", "quote": "Quoted line"}],
            "counterfactual_loss": "The target would lose its framing anchor.",
        },
        "raw_prose": None,
    }


def _relationship_surface_payload(items: list[dict[str, object]]) -> ViewPayload:
    return ViewPayload(
        view_key=ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY,
        view_name="Relationship Landscape",
        description="",
        renderer_type="card_grid",
        renderer_config={"columns": 1},
        presentation_stance="diagnostic",
        priority="primary",
        rationale="",
        data_quality="standard",
        source_parent_view_key=None,
        phase_number=1.5,
        engine_key="genealogy_relationship_classification",
        chain_key=None,
        scope="per_item",
        has_structured_data=False,
        structured_data=None,
        reading_scaffold=None,
        raw_prose=None,
        prose_ref_view_key=None,
        items=items,
        tab_count=len(items),
        visibility="if_data_exists",
        position=1.1,
        children=[],
    )


def _conditions_surface_payload(
    *,
    enabling_conditions: list[dict[str, object]] | None = None,
    constraining_conditions: list[dict[str, object]] | None = None,
    path_dependencies: list[dict[str, object]] | None = None,
    unacknowledged_debts: list[dict[str, object]] | None = None,
    alternative_paths: list[dict[str, object]] | None = None,
    counterfactual_analysis: str = "Without the prior trajectory, the argument would lose its scaffolding.",
    synthetic_judgment: str = "The prior trajectory mostly enables the current synthesis.",
    meta: dict[str, object] | None = None,
) -> ViewPayload:
    enabling_conditions = enabling_conditions or []
    constraining_conditions = constraining_conditions or []
    path_dependencies = path_dependencies or []
    unacknowledged_debts = unacknowledged_debts or []
    alternative_paths = alternative_paths or []
    if meta is None:
        if len(enabling_conditions) > len(constraining_conditions):
            overall_balance = "enabling_dominant"
        elif len(constraining_conditions) > len(enabling_conditions):
            overall_balance = "constraining_dominant"
        else:
            overall_balance = "balanced"
        meta = {
            "overall_balance": overall_balance,
            "enabling_conditions_count": len(enabling_conditions),
            "constraining_conditions_count": len(constraining_conditions),
            "path_dependencies_count": len(path_dependencies),
            "unacknowledged_debts_count": len(unacknowledged_debts),
            "alternative_paths_count": len(alternative_paths),
        }

    return ViewPayload(
        view_key=ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY,
        view_name="Conditions of Possibility",
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "conditions_snapshot", "title": "Conditions Snapshot"}]},
        presentation_stance="diagnostic",
        priority="primary",
        rationale="",
        data_quality="standard",
        source_parent_view_key=None,
        phase_number=3.0,
        engine_key="conditions_of_possibility_analyzer",
        chain_key=None,
        scope="aggregated",
        has_structured_data=True,
        structured_data={
            "meta": meta,
            "enabling_conditions": enabling_conditions,
            "constraining_conditions": constraining_conditions,
            "path_dependencies": path_dependencies,
            "unacknowledged_debts": unacknowledged_debts,
            "alternative_paths": alternative_paths,
            "counterfactual_analysis": counterfactual_analysis,
            "synthetic_judgment": synthetic_judgment,
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


def _write_spec(directory: Path, composition_mode: str, payload: dict, *, filename_stem: str | None = None) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    stem = filename_stem or composition_mode
    (directory / f"{stem}.json").write_text(json.dumps(payload), encoding="utf-8")


def _round8_suite_payload() -> dict[str, object]:
    return {
        "composition_mode": COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
        "workflow_key": "intellectual_genealogy",
        "surfaces": [
            {
                "target_surface": "genealogy_relationship_landscape",
                "signal_extractor_key": "relationship_surface_signals_v1",
                "default_family": "relationship_comparison_review",
                "families": [
                    {
                        "family_key": "relationship_profile_dossier",
                        "builder_template_key": "relationship_profile_dossier",
                        "view_name": "Relationship Dossier",
                    },
                    {
                        "family_key": "relationship_comparison_review",
                        "builder_template_key": "relationship_comparison_review",
                        "view_name": "Relationship Comparison Review",
                    },
                ],
                "decision_rules": [
                    {
                        "family_key": "relationship_profile_dossier",
                        "match_any": [
                            [{"metric": "relationship_count", "operator": "eq", "value": 1}],
                            [
                                {"metric": "top_share", "operator": "gte", "value": 0.45},
                                {"metric": "score_gap", "operator": "gte", "value": 5},
                            ],
                        ],
                    }
                ],
            },
            {
                "target_surface": "genealogy_conditions",
                "signal_extractor_key": "conditions_surface_signals_v1",
                "default_family": "conditions_balance_sheet",
                "families": [
                    {
                        "family_key": "conditions_balance_sheet",
                        "builder_template_key": "conditions_balance_sheet",
                        "view_name": "Conditions Balance Sheet",
                    },
                    {
                        "family_key": "conditions_path_dependency_matrix",
                        "builder_template_key": "conditions_path_dependency_matrix",
                        "view_name": "Conditions Path-Dependency Matrix",
                    },
                ],
                "decision_rules": [
                    {
                        "family_key": "conditions_path_dependency_matrix",
                        "match_any": [
                            [
                                {"metric": "path_dependencies_count", "operator": "gte", "value": 2},
                                {
                                    "metric": "path_signal_minus_balance_signal",
                                    "operator": "gte",
                                    "value": 0,
                                },
                            ]
                        ],
                    }
                ],
            },
        ],
    }


def _decision_by_target(details: dict[str, object], target_surface: str) -> dict[str, object]:
    decisions = details.get("surface_decisions")
    assert isinstance(decisions, list)
    for decision in decisions:
        if isinstance(decision, dict) and decision.get("target_surface") == target_surface:
            return decision
    raise AssertionError(f"Missing surface decision for {target_surface}")


@pytest.fixture(autouse=True)
def _clear_adaptive_registry_cache():
    adaptive_registry._SPEC_CACHE.clear()
    adaptive_registry._SUITE_SPEC_CACHE.clear()
    yield
    adaptive_registry._SPEC_CACHE.clear()
    adaptive_registry._SUITE_SPEC_CACHE.clear()


def test_load_all_adaptive_specs_loads_repo_tracked_round7_spec_and_excludes_suite_specs():
    specs = adaptive_registry.load_all_adaptive_specs()

    spec = specs["declarative_relationship_surface_v1"]
    assert spec.composition_mode == "declarative_relationship_surface_v1"
    assert spec.target_surface == "genealogy_relationship_landscape"
    assert spec.default_family == "relationship_comparison_review"
    assert COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1 not in specs


def test_load_all_adaptive_suite_specs_loads_repo_tracked_round8_spec():
    specs = adaptive_registry.load_all_adaptive_suite_specs()

    spec = specs[COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1]
    assert spec.composition_mode == COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1
    assert [surface.target_surface for surface in spec.surfaces] == [
        "genealogy_relationship_landscape",
        "genealogy_conditions",
    ]


@pytest.mark.parametrize(
    ("composition_mode", "spec_payload"),
    [
        (
            "missing_default_family",
            {
                "composition_mode": "missing_default_family",
                "workflow_key": "intellectual_genealogy",
                "target_surface": "genealogy_relationship_landscape",
                "signal_extractor_key": "relationship_surface_signals_v1",
                "families": [
                    {
                        "family_key": "relationship_profile_dossier",
                        "builder_template_key": "relationship_profile_dossier",
                        "view_name": "Relationship Dossier",
                    }
                ],
                "decision_rules": [],
            },
        ),
        (
            "undeclared_default_family",
            {
                "composition_mode": "undeclared_default_family",
                "workflow_key": "intellectual_genealogy",
                "target_surface": "genealogy_relationship_landscape",
                "signal_extractor_key": "relationship_surface_signals_v1",
                "default_family": "relationship_comparison_review",
                "families": [
                    {
                        "family_key": "relationship_profile_dossier",
                        "builder_template_key": "relationship_profile_dossier",
                        "view_name": "Relationship Dossier",
                    }
                ],
                "decision_rules": [],
            },
        ),
        (
            "duplicate_family_key",
            {
                "composition_mode": "duplicate_family_key",
                "workflow_key": "intellectual_genealogy",
                "target_surface": "genealogy_relationship_landscape",
                "signal_extractor_key": "relationship_surface_signals_v1",
                "default_family": "relationship_profile_dossier",
                "families": [
                    {
                        "family_key": "relationship_profile_dossier",
                        "builder_template_key": "relationship_profile_dossier",
                        "view_name": "Relationship Dossier",
                    },
                    {
                        "family_key": "relationship_profile_dossier",
                        "builder_template_key": "relationship_profile_dossier",
                        "view_name": "Relationship Dossier Again",
                    },
                ],
                "decision_rules": [],
            },
        ),
        (
            "unknown_signal_extractor_key",
            {
                "composition_mode": "unknown_signal_extractor_key",
                "workflow_key": "intellectual_genealogy",
                "target_surface": "genealogy_relationship_landscape",
                "signal_extractor_key": "unknown_key",
                "default_family": "relationship_profile_dossier",
                "families": [
                    {
                        "family_key": "relationship_profile_dossier",
                        "builder_template_key": "relationship_profile_dossier",
                        "view_name": "Relationship Dossier",
                    }
                ],
                "decision_rules": [],
            },
        ),
        (
            "unknown_builder_template_key",
            {
                "composition_mode": "unknown_builder_template_key",
                "workflow_key": "intellectual_genealogy",
                "target_surface": "genealogy_relationship_landscape",
                "signal_extractor_key": "relationship_surface_signals_v1",
                "default_family": "relationship_profile_dossier",
                "families": [
                    {
                        "family_key": "relationship_profile_dossier",
                        "builder_template_key": "unknown_builder",
                        "view_name": "Relationship Dossier",
                    }
                ],
                "decision_rules": [],
            },
        ),
        (
            "builder_template_key_mismatch",
            {
                "composition_mode": "builder_template_key_mismatch",
                "workflow_key": "intellectual_genealogy",
                "target_surface": "genealogy_relationship_landscape",
                "signal_extractor_key": "relationship_surface_signals_v1",
                "default_family": "relationship_profile_dossier",
                "families": [
                    {
                        "family_key": "relationship_profile_dossier",
                        "builder_template_key": "relationship_comparison_review",
                        "view_name": "Relationship Dossier",
                    }
                ],
                "decision_rules": [],
            },
        ),
        (
            "unknown_rule_family",
            {
                "composition_mode": "unknown_rule_family",
                "workflow_key": "intellectual_genealogy",
                "target_surface": "genealogy_relationship_landscape",
                "signal_extractor_key": "relationship_surface_signals_v1",
                "default_family": "relationship_profile_dossier",
                "families": [
                    {
                        "family_key": "relationship_profile_dossier",
                        "builder_template_key": "relationship_profile_dossier",
                        "view_name": "Relationship Dossier",
                    }
                ],
                "decision_rules": [
                    {
                        "family_key": "relationship_comparison_review",
                        "match_any": [[{"metric": "relationship_count", "operator": "eq", "value": 1}]],
                    }
                ],
            },
        ),
        (
            "unsupported_operator",
            {
                "composition_mode": "unsupported_operator",
                "workflow_key": "intellectual_genealogy",
                "target_surface": "genealogy_relationship_landscape",
                "signal_extractor_key": "relationship_surface_signals_v1",
                "default_family": "relationship_profile_dossier",
                "families": [
                    {
                        "family_key": "relationship_profile_dossier",
                        "builder_template_key": "relationship_profile_dossier",
                        "view_name": "Relationship Dossier",
                    }
                ],
                "decision_rules": [
                    {
                        "family_key": "relationship_profile_dossier",
                        "match_any": [[{"metric": "relationship_count", "operator": "lte", "value": 1}]],
                    }
                ],
            },
        ),
    ],
)
def test_invalid_repo_tracked_specs_fail_registry_validation(tmp_path, monkeypatch, composition_mode, spec_payload):
    _write_spec(tmp_path, composition_mode, spec_payload)
    monkeypatch.setattr(adaptive_registry, "_DEFINITIONS_DIR", tmp_path)

    with pytest.raises(AdaptiveSpecRegistryError):
        adaptive_registry.get_adaptive_composition_spec(composition_mode)


@pytest.mark.parametrize(
    ("composition_mode", "spec_payload", "filename_stem"),
    [
        (
            COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
            {
                "composition_mode": COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
                "workflow_key": "intellectual_genealogy",
            },
            None,
        ),
        (
            COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
            {
                **_round8_suite_payload(),
                "surfaces": [
                    _round8_suite_payload()["surfaces"][0],
                    _round8_suite_payload()["surfaces"][0],
                ],
            },
            None,
        ),
        (
            COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
            {
                **_round8_suite_payload(),
                "surfaces": [
                    {
                        **_round8_suite_payload()["surfaces"][0],
                        "signal_extractor_key": "unknown_conditions_key",
                    },
                    _round8_suite_payload()["surfaces"][1],
                ],
            },
            None,
        ),
        (
            COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
            {
                **_round8_suite_payload(),
                "surfaces": [
                    _round8_suite_payload()["surfaces"][0],
                    {
                        **_round8_suite_payload()["surfaces"][1],
                        "families": [
                            {
                                "family_key": "conditions_balance_sheet",
                                "builder_template_key": "unknown_builder",
                                "view_name": "Conditions Balance Sheet",
                            },
                            _round8_suite_payload()["surfaces"][1]["families"][1],
                        ],
                    },
                ],
            },
            None,
        ),
        (
            COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
            {
                **_round8_suite_payload(),
                "surfaces": [
                    _round8_suite_payload()["surfaces"][0],
                ],
            },
            None,
        ),
        (
            COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
            {
                **_round8_suite_payload(),
                "surfaces": [
                    _round8_suite_payload()["surfaces"][1],
                    _round8_suite_payload()["surfaces"][0],
                ],
            },
            None,
        ),
        (
            COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
            {
                **_round8_suite_payload(),
                "surfaces": [
                    _round8_suite_payload()["surfaces"][0],
                    {
                        **_round8_suite_payload()["surfaces"][1],
                        "target_surface": "genealogy_portrait",
                    },
                ],
            },
            None,
        ),
        (
            COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
            {
                **_round8_suite_payload(),
                "composition_mode": "wrong_mode",
            },
            COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
        ),
    ],
)
def test_invalid_repo_tracked_suite_specs_fail_registry_validation(
    tmp_path,
    monkeypatch,
    composition_mode,
    spec_payload,
    filename_stem,
):
    _write_spec(tmp_path, composition_mode, spec_payload, filename_stem=filename_stem)
    monkeypatch.setattr(adaptive_registry, "_SUITE_DEFINITIONS_DIR", tmp_path)

    with pytest.raises(AdaptiveSpecRegistryError):
        adaptive_registry.get_adaptive_suite_composition_spec(composition_mode)


def test_empty_decision_rules_are_legal_and_mean_default_only_spec(tmp_path, monkeypatch):
    composition_mode = "default_only_relationship_surface_v1"
    _write_spec(
        tmp_path,
        composition_mode,
        {
            "composition_mode": composition_mode,
            "workflow_key": "intellectual_genealogy",
            "target_surface": "genealogy_relationship_landscape",
            "signal_extractor_key": "relationship_surface_signals_v1",
            "default_family": "relationship_comparison_review",
            "families": [
                {
                    "family_key": "relationship_profile_dossier",
                    "builder_template_key": "relationship_profile_dossier",
                    "view_name": "Relationship Dossier",
                },
                {
                    "family_key": "relationship_comparison_review",
                    "builder_template_key": "relationship_comparison_review",
                    "view_name": "Relationship Comparison Review",
                },
            ],
            "decision_rules": [],
        },
    )
    monkeypatch.setattr(adaptive_registry, "_DEFINITIONS_DIR", tmp_path)

    spec = adaptive_registry.get_adaptive_composition_spec(composition_mode)

    assert spec.decision_rules == []
    assert spec.default_family == "relationship_comparison_review"


def test_round7_declarative_single_surface_path_remains_unchanged_after_suite_registry_expansion():
    base_payload = _relationship_surface_payload(
        [
            _relationship_item(
                "Foundational Precursor",
                relationship_type="direct_precursor",
                relationship_strength="strong",
                summary="Dominates the field.",
            ),
            _relationship_item(
                "Method Context",
                relationship_type="methodological_ancestor",
                relationship_strength="weak",
                summary="Secondary support only.",
            ),
        ]
    )
    payloads = {base_payload.view_key: base_payload.model_copy(deep=True)}

    applied = apply_bounded_dynamic_composition(
        payloads=payloads,
        workflow_key="intellectual_genealogy",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
    )

    assert applied is True
    assert payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY].view_name == "Relationship Dossier"
    assert adaptive_registry.load_all_adaptive_specs()["declarative_relationship_surface_v1"].target_surface == (
        "genealogy_relationship_landscape"
    )
    assert COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1 not in adaptive_registry.load_all_adaptive_specs()


def test_declarative_relationship_surface_matches_hardcoded_dossier_family_on_synthetic_control():
    base_payload = _relationship_surface_payload(
        [
            _relationship_item(
                "Foundational Precursor",
                relationship_type="direct_precursor",
                relationship_strength="strong",
                summary="Dominates the field.",
            ),
            _relationship_item(
                "Method Context",
                relationship_type="methodological_ancestor",
                relationship_strength="weak",
                summary="Secondary support only.",
            ),
        ]
    )
    hardcoded_payloads = {base_payload.view_key: base_payload.model_copy(deep=True)}
    declarative_payloads = {base_payload.view_key: base_payload.model_copy(deep=True)}

    hardcoded_applied = apply_bounded_dynamic_composition(
        payloads=hardcoded_payloads,
        workflow_key="intellectual_genealogy",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
    )
    declarative_applied = apply_bounded_dynamic_composition(
        payloads=declarative_payloads,
        workflow_key="intellectual_genealogy",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
    )

    assert hardcoded_applied is True
    assert declarative_applied is True

    hardcoded_payload = hardcoded_payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY]
    declarative_payload = declarative_payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY]
    assert hardcoded_payload.view_name == "Relationship Dossier"
    assert declarative_payload.view_name == "Relationship Dossier"
    assert declarative_payload.renderer_type == hardcoded_payload.renderer_type
    assert declarative_payload.renderer_config == hardcoded_payload.renderer_config
    assert declarative_payload.structured_data == hardcoded_payload.structured_data
    assert declarative_payload.derivation_kind == hardcoded_payload.derivation_kind
    assert declarative_payload.source_parent_view_key == hardcoded_payload.source_parent_view_key
    assert declarative_payload.description == hardcoded_payload.description

    hardcoded_details = inspect_runtime_composition(
        payloads={base_payload.view_key: base_payload.model_copy(deep=True)},
        workflow_key="intellectual_genealogy",
        composition_mode=COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
    )
    declarative_details = inspect_runtime_composition(
        payloads={base_payload.view_key: base_payload.model_copy(deep=True)},
        workflow_key="intellectual_genealogy",
        composition_mode=COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
    )
    assert declarative_details["selected_family"] == hardcoded_details["selected_family"]
    assert declarative_details["signal_summary"] == hardcoded_details["signal_summary"]
    assert declarative_details["rationale"] == hardcoded_details["rationale"]
    declarative_rejections = {item["family"]: item["reason"] for item in declarative_details["rejected_families"]}
    hardcoded_rejections = {item["family"]: item["reason"] for item in hardcoded_details["rejected_families"]}
    assert set(declarative_rejections).issubset(set(hardcoded_rejections))
    for family, reason in declarative_rejections.items():
        assert hardcoded_rejections[family] == reason


def test_declarative_relationship_surface_matches_hardcoded_comparison_family_on_synthetic_control():
    base_payload = _relationship_surface_payload(
        [
            _relationship_item(
                "Precursor A",
                relationship_type="direct_precursor",
                relationship_strength="strong",
                summary="Comparable precursor A.",
            ),
            _relationship_item(
                "Precursor B",
                relationship_type="methodological_ancestor",
                relationship_strength="strong",
                summary="Comparable precursor B.",
            ),
            _relationship_item(
                "Precursor C",
                relationship_type="counter_position",
                relationship_strength="moderate",
                summary="Comparable precursor C.",
            ),
        ]
    )
    hardcoded_payloads = {base_payload.view_key: base_payload.model_copy(deep=True)}
    declarative_payloads = {base_payload.view_key: base_payload.model_copy(deep=True)}

    apply_bounded_dynamic_composition(
        payloads=hardcoded_payloads,
        workflow_key="intellectual_genealogy",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
    )
    apply_bounded_dynamic_composition(
        payloads=declarative_payloads,
        workflow_key="intellectual_genealogy",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
    )

    hardcoded_payload = hardcoded_payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY]
    declarative_payload = declarative_payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY]
    assert hardcoded_payload.view_name == "Relationship Comparison Review"
    assert declarative_payload.view_name == "Relationship Comparison Review"
    assert declarative_payload.renderer_type == hardcoded_payload.renderer_type
    assert declarative_payload.renderer_config == hardcoded_payload.renderer_config
    assert declarative_payload.structured_data == hardcoded_payload.structured_data
    assert declarative_payload.derivation_kind == hardcoded_payload.derivation_kind
    assert declarative_payload.source_parent_view_key == hardcoded_payload.source_parent_view_key
    assert declarative_payload.description == hardcoded_payload.description


def test_extract_conditions_surface_signals_computes_derived_metrics():
    payload = _conditions_surface_payload(
        enabling_conditions=[{"description": "One enabling pressure"}],
        constraining_conditions=[{"description": "One constraint"}],
        path_dependencies=[
            {"description": "Dependency one"},
            {"description": "Dependency two"},
        ],
        alternative_paths=[{"branching_point": "Branch one"}],
        unacknowledged_debts=[],
        meta={
            "overall_balance": "balanced",
            "enabling_conditions_count": 1,
            "constraining_conditions_count": 1,
            "path_dependencies_count": 2,
            "unacknowledged_debts_count": 0,
            "alternative_paths_count": 1,
        },
    )

    source_payload, signal_summary = _extract_conditions_surface_signals(payload)

    assert source_payload["meta"]["path_dependencies_count"] == 2
    assert signal_summary["path_signal"] == 3
    assert signal_summary["balance_signal"] == 2
    assert signal_summary["path_signal_minus_balance_signal"] == 1


def test_hardcoded_conditions_surface_selection_is_unchanged_after_refactor():
    payloads = {
        ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY: _conditions_surface_payload(
            enabling_conditions=[{"description": "One enabling pressure"}],
            constraining_conditions=[{"description": "One constraint"}],
            path_dependencies=[
                {"description": "Dependency one"},
                {"description": "Dependency two"},
            ],
            alternative_paths=[{"branching_point": "Branch one"}],
            unacknowledged_debts=[],
            meta={
                "overall_balance": "balanced",
                "enabling_conditions_count": 1,
                "constraining_conditions_count": 1,
                "path_dependencies_count": 2,
                "unacknowledged_debts_count": 0,
                "alternative_paths_count": 1,
            },
        )
    }

    selection = _select_adaptive_conditions_surface(payloads)

    assert selection.selected_family == "conditions_path_dependency_matrix"
    assert selection.signal_summary["path_signal_minus_balance_signal"] == 1
    assert selection.rationale.startswith("Path dependencies and alternative branches dominate this conditions field")


def test_declarative_relationship_suite_matches_hardcoded_dossier_and_balance_on_synthetic_control():
    relationship_payload = _relationship_surface_payload(
        [
            _relationship_item(
                "Foundational Precursor",
                relationship_type="direct_precursor",
                relationship_strength="strong",
                summary="Dominates the field.",
            ),
            _relationship_item(
                "Method Context",
                relationship_type="methodological_ancestor",
                relationship_strength="weak",
                summary="Secondary support only.",
            ),
        ]
    )
    conditions_payload = _conditions_surface_payload(
        enabling_conditions=[
            {"description": "Made the target thinkable."},
            {"description": "Prepared the audience."},
        ],
        constraining_conditions=[{"description": "Previous commitments narrow the move-set."}],
        path_dependencies=[{"description": "A single path dependency remains visible"}],
        alternative_paths=[],
        unacknowledged_debts=[{"description": "Debt"}],
    )
    hardcoded_payloads = {
        relationship_payload.view_key: relationship_payload.model_copy(deep=True),
        conditions_payload.view_key: conditions_payload.model_copy(deep=True),
    }
    declarative_payloads = {
        relationship_payload.view_key: relationship_payload.model_copy(deep=True),
        conditions_payload.view_key: conditions_payload.model_copy(deep=True),
    }

    apply_bounded_dynamic_composition(
        payloads=hardcoded_payloads,
        workflow_key="intellectual_genealogy",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
    )
    apply_bounded_dynamic_composition(
        payloads=declarative_payloads,
        workflow_key="intellectual_genealogy",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
    )

    hardcoded_relationship = hardcoded_payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY]
    declarative_relationship = declarative_payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY]
    hardcoded_conditions = hardcoded_payloads[ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY]
    declarative_conditions = declarative_payloads[ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY]

    assert declarative_relationship.view_name == "Relationship Dossier"
    assert declarative_relationship.renderer_type == hardcoded_relationship.renderer_type
    assert declarative_relationship.renderer_config == hardcoded_relationship.renderer_config
    assert declarative_relationship.structured_data == hardcoded_relationship.structured_data
    assert declarative_relationship.derivation_kind == hardcoded_relationship.derivation_kind
    assert declarative_relationship.source_parent_view_key == hardcoded_relationship.source_parent_view_key
    assert declarative_relationship.description == hardcoded_relationship.description

    assert declarative_conditions.view_name == "Conditions Balance Sheet"
    assert declarative_conditions.renderer_type == hardcoded_conditions.renderer_type
    assert declarative_conditions.renderer_config == hardcoded_conditions.renderer_config
    assert declarative_conditions.structured_data == hardcoded_conditions.structured_data
    assert declarative_conditions.derivation_kind == hardcoded_conditions.derivation_kind
    assert declarative_conditions.source_parent_view_key == hardcoded_conditions.source_parent_view_key
    assert declarative_conditions.description == hardcoded_conditions.description

    hardcoded_details = inspect_runtime_composition(
        payloads={
            relationship_payload.view_key: relationship_payload.model_copy(deep=True),
            conditions_payload.view_key: conditions_payload.model_copy(deep=True),
        },
        workflow_key="intellectual_genealogy",
        composition_mode=COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
    )
    declarative_details = inspect_runtime_composition(
        payloads={
            relationship_payload.view_key: relationship_payload.model_copy(deep=True),
            conditions_payload.view_key: conditions_payload.model_copy(deep=True),
        },
        workflow_key="intellectual_genealogy",
        composition_mode=COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
    )

    hardcoded_relationship_decision = _decision_by_target(
        hardcoded_details,
        ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY,
    )
    declarative_relationship_decision = _decision_by_target(
        declarative_details,
        ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY,
    )
    assert declarative_relationship_decision["selected_family"] == hardcoded_relationship_decision["selected_family"]
    assert declarative_relationship_decision["signal_summary"] == hardcoded_relationship_decision["signal_summary"]
    assert declarative_relationship_decision["rationale"] == hardcoded_relationship_decision["rationale"]
    hardcoded_relationship_rejections = {
        item["family"]: item["reason"] for item in hardcoded_relationship_decision["rejected_families"]
    }
    declarative_relationship_rejections = {
        item["family"]: item["reason"] for item in declarative_relationship_decision["rejected_families"]
    }
    assert set(declarative_relationship_rejections).issubset(set(hardcoded_relationship_rejections))
    for family, reason in declarative_relationship_rejections.items():
        assert hardcoded_relationship_rejections[family] == reason

    hardcoded_conditions_decision = _decision_by_target(
        hardcoded_details,
        ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY,
    )
    declarative_conditions_decision = _decision_by_target(
        declarative_details,
        ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY,
    )
    assert declarative_conditions_decision["selected_family"] == hardcoded_conditions_decision["selected_family"]
    assert declarative_conditions_decision["signal_summary"] == hardcoded_conditions_decision["signal_summary"]
    assert declarative_conditions_decision["rationale"] == hardcoded_conditions_decision["rationale"]
    assert declarative_conditions_decision["rejected_families"] == hardcoded_conditions_decision["rejected_families"]


def test_declarative_relationship_suite_matches_hardcoded_comparison_and_matrix_on_synthetic_control():
    relationship_payload = _relationship_surface_payload(
        [
            _relationship_item(
                "Precursor A",
                relationship_type="direct_precursor",
                relationship_strength="strong",
                summary="Comparable precursor A.",
            ),
            _relationship_item(
                "Precursor B",
                relationship_type="methodological_ancestor",
                relationship_strength="strong",
                summary="Comparable precursor B.",
            ),
            _relationship_item(
                "Precursor C",
                relationship_type="counter_position",
                relationship_strength="moderate",
                summary="Comparable precursor C.",
            ),
        ]
    )
    conditions_payload = _conditions_surface_payload(
        enabling_conditions=[{"description": "One enabling premise"}],
        constraining_conditions=[{"description": "One constraint persists"}],
        path_dependencies=[
            {"description": "Dependency chain one", "chain": ["A", "B", "Target"], "is_acknowledged": False},
            {"description": "Dependency chain two", "chain": ["C", "Target"], "is_acknowledged": True},
        ],
        alternative_paths=[{"branching_point": "Method turn"}],
        unacknowledged_debts=[],
        meta={
            "overall_balance": "balanced",
            "enabling_conditions_count": 1,
            "constraining_conditions_count": 1,
            "path_dependencies_count": 2,
            "unacknowledged_debts_count": 0,
            "alternative_paths_count": 1,
        },
    )
    hardcoded_payloads = {
        relationship_payload.view_key: relationship_payload.model_copy(deep=True),
        conditions_payload.view_key: conditions_payload.model_copy(deep=True),
    }
    declarative_payloads = {
        relationship_payload.view_key: relationship_payload.model_copy(deep=True),
        conditions_payload.view_key: conditions_payload.model_copy(deep=True),
    }

    apply_bounded_dynamic_composition(
        payloads=hardcoded_payloads,
        workflow_key="intellectual_genealogy",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
    )
    apply_bounded_dynamic_composition(
        payloads=declarative_payloads,
        workflow_key="intellectual_genealogy",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
    )

    assert hardcoded_payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY].view_name == "Relationship Comparison Review"
    assert declarative_payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY].view_name == "Relationship Comparison Review"
    assert hardcoded_payloads[ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY].view_name == "Conditions Path-Dependency Matrix"
    assert declarative_payloads[ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY].view_name == "Conditions Path-Dependency Matrix"
    assert (
        declarative_payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY].structured_data
        == hardcoded_payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY].structured_data
    )
    assert (
        declarative_payloads[ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY].structured_data
        == hardcoded_payloads[ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY].structured_data
    )
    assert (
        declarative_payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY].derivation_kind
        == hardcoded_payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY].derivation_kind
    )
    assert (
        declarative_payloads[ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY].derivation_kind
        == hardcoded_payloads[ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY].derivation_kind
    )

    hardcoded_details = inspect_runtime_composition(
        payloads={
            relationship_payload.view_key: relationship_payload.model_copy(deep=True),
            conditions_payload.view_key: conditions_payload.model_copy(deep=True),
        },
        workflow_key="intellectual_genealogy",
        composition_mode=COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
    )
    declarative_details = inspect_runtime_composition(
        payloads={
            relationship_payload.view_key: relationship_payload.model_copy(deep=True),
            conditions_payload.view_key: conditions_payload.model_copy(deep=True),
        },
        workflow_key="intellectual_genealogy",
        composition_mode=COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
    )
    assert _decision_by_target(
        declarative_details,
        ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY,
    )["selected_family"] == "relationship_comparison_review"
    assert _decision_by_target(
        declarative_details,
        ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY,
    )["selected_family"] == "conditions_path_dependency_matrix"
    assert _decision_by_target(
        declarative_details,
        ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY,
    )["signal_summary"] == _decision_by_target(
        hardcoded_details,
        ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY,
    )["signal_summary"]
    assert _decision_by_target(
        declarative_details,
        ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY,
    )["signal_summary"] == _decision_by_target(
        hardcoded_details,
        ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY,
    )["signal_summary"]


def test_declarative_relationship_surface_translates_invalid_spec_to_bounded_validation_error(monkeypatch):
    payloads = {
        ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY: _relationship_surface_payload(
            [
                _relationship_item(
                    "Foundational Precursor",
                    relationship_type="direct_precursor",
                    relationship_strength="strong",
                    summary="Dominates the field.",
                )
            ]
        )
    }

    def _raise(_composition_mode: str):
        raise AdaptiveSpecRegistryError("broken declarative spec")

    monkeypatch.setattr(composition_module, "get_adaptive_composition_spec", _raise)

    with pytest.raises(BoundedCompositionValidationError) as excinfo:
        apply_bounded_dynamic_composition(
            payloads=payloads,
            workflow_key="intellectual_genealogy",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
        )

    assert excinfo.value.issues[0].reason == "adaptive_spec_validation_failed"


def test_declarative_suite_translates_invalid_spec_to_bounded_validation_error(monkeypatch):
    payloads = {
        ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY: _relationship_surface_payload(
            [
                _relationship_item(
                    "Foundational Precursor",
                    relationship_type="direct_precursor",
                    relationship_strength="strong",
                    summary="Dominates the field.",
                )
            ]
        ),
        ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY: _conditions_surface_payload(),
    }

    def _raise(_composition_mode: str):
        raise AdaptiveSpecRegistryError("broken declarative suite spec")

    monkeypatch.setattr(composition_module, "get_adaptive_suite_composition_spec", _raise)

    with pytest.raises(BoundedCompositionValidationError) as excinfo:
        apply_bounded_dynamic_composition(
            payloads=payloads,
            workflow_key="intellectual_genealogy",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
        )

    assert excinfo.value.issues[0].reason == "adaptive_spec_validation_failed"
    assert excinfo.value.issues[0].view_key == DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_ISSUE_TARGET


def test_declarative_suite_runtime_rejects_workflow_mismatch_after_mode_acceptance(tmp_path, monkeypatch):
    spec_payload = _round8_suite_payload()
    spec_payload["workflow_key"] = "wrong_workflow"
    _write_spec(
        tmp_path,
        COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
        spec_payload,
    )
    monkeypatch.setattr(adaptive_registry, "_SUITE_DEFINITIONS_DIR", tmp_path)

    payloads = {
        ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY: _relationship_surface_payload(
            [
                _relationship_item(
                    "Foundational Precursor",
                    relationship_type="direct_precursor",
                    relationship_strength="strong",
                    summary="Dominates the field.",
                )
            ]
        ),
        ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY: _conditions_surface_payload(),
    }

    with pytest.raises(BoundedCompositionValidationError) as excinfo:
        apply_bounded_dynamic_composition(
            payloads=payloads,
            workflow_key="intellectual_genealogy",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
        )

    assert excinfo.value.issues[0].reason == "adaptive_spec_workflow_mismatch"
    assert excinfo.value.issues[0].view_key == DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_ISSUE_TARGET
