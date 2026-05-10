from __future__ import annotations

from types import SimpleNamespace

import pytest

from src.aoi.constants import AOI_WORKFLOW_KEY
from src.engines.discovery import (
    CapabilityMetadataResolutionError,
    resolve_capability_definition,
    resolve_composition_role as _resolve_composition_role,
)
from src.engines.registry import get_engine_registry
from src.presenter.composition_source_bridge import (
    ComposeFromSourceResolutionError,
    SOURCE_FAMILY_ENGAGEMENT_MAPPING,
    SOURCE_FAMILY_SIN_FINDINGS,
    SOURCE_FAMILY_THEMATIC_REPORT,
    SOURCE_FAMILY_THEMATIC_SYNTHESIS,
    build_selection_composition_bridge,
    build_source_composition_bridge,
    resolve_source_catalog,
)
from src.presenter.schemas import AoiSelectedSourceInput


def test_resolve_source_catalog_records_candidate_states_without_throwing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": AOI_WORKFLOW_KEY},
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_effective_plan_context",
        lambda job_id, plan_id=None: SimpleNamespace(plan=None, source="missing"),
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_aoi_normalized_artifact",
        lambda job_id, engine_key: {
            "aoi_engagement_mapping": {"engagements": []},
            "aoi_sin_findings": "bad-payload",
        }.get(engine_key),
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_phase_outputs",
        lambda job_id, engine_key=None: [],
    )

    catalog = resolve_source_catalog(source_v2_job_id="job-1")

    state_by_family = {
        candidate.source_family_key: candidate.candidate_state
        for candidate in catalog.candidates
    }
    assert state_by_family == {
        SOURCE_FAMILY_THEMATIC_SYNTHESIS: "unavailable",
        SOURCE_FAMILY_ENGAGEMENT_MAPPING: "available",
        SOURCE_FAMILY_SIN_FINDINGS: "invalid",
        SOURCE_FAMILY_THEMATIC_REPORT: "unavailable",
    }


def test_resolve_source_catalog_uses_merged_plan_data_objective_when_effective_plan_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.get_job",
        lambda job_id: {
            "job_id": job_id,
            "workflow_key": AOI_WORKFLOW_KEY,
            "plan_data": {
                "_type": "request_snapshot",
                "plan_request": {
                    "workflow_key": AOI_WORKFLOW_KEY,
                    "objective_key": "logical",
                    "selected_source_thinker_id": "otto_neurath",
                    "selected_source_thinker_name": "Otto Neurath",
                },
                "request_options": {},
            },
        },
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_effective_plan_context",
        lambda job_id, plan_id=None: SimpleNamespace(plan=None, source="missing"),
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_aoi_normalized_artifact",
        lambda job_id, engine_key: None,
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_phase_outputs",
        lambda job_id, engine_key=None: [],
    )

    catalog = resolve_source_catalog(source_v2_job_id="job-merged-objective")

    assert catalog.objective_key == "logical"
    assert catalog.objective_source == "merged_plan_data"
    assert catalog.selected_source_thinker_id == "otto_neurath"
    assert catalog.selected_source_thinker_name == "Otto Neurath"


def test_build_source_composition_bridge_uses_live_sources_even_if_plan_marks_phase_skipped(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan = SimpleNamespace(
        objective_key="influence_thematic",
        workflow_key=AOI_WORKFLOW_KEY,
        selected_source_thinker_id="otto_neurath",
        selected_source_thinker_name="Otto Neurath",
        phases=[
            SimpleNamespace(
                phase_number=1.0,
                phase_name="Synthesis",
                engine_key="aoi_thematic_synthesis",
                engine_overrides=None,
                skip=True,
                skip_reason="Planner skipped this phase.",
            ),
            SimpleNamespace(
                phase_number=4.0,
                phase_name="Report",
                engine_key="aoi_thematic_report",
                engine_overrides=None,
                skip=False,
                skip_reason=None,
            ),
        ],
    )

    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": AOI_WORKFLOW_KEY},
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_effective_plan_context",
        lambda job_id, plan_id=None: SimpleNamespace(plan=plan, source="job_plan_data"),
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_aoi_normalized_artifact",
        lambda job_id, engine_key: {"themes": [{"theme_name": "Planning"}]}
        if engine_key == "aoi_thematic_synthesis"
        else None,
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_phase_outputs",
        lambda job_id, engine_key=None: [
            {
                "id": "po-report-1",
                "phase_number": 4.0,
                "pass_number": 1,
                "created_at": "2026-03-23T10:00:00",
                "metadata": {
                    "normalized": {
                        "report_sections": {
                            "summary": "Summary",
                            "engagement_pattern": "Pattern",
                        }
                    }
                },
            }
        ],
    )

    bridge = build_source_composition_bridge(
        source_v2_job_id="job-1",
        profile="dossier",
    )

    assert [section.engine_key for section in bridge.materialized_sections] == [
        "aoi_thematic_synthesis",
        "aoi_thematic_report",
    ]
    assert bridge.catalog.plan_source_mismatches == [
        {
            "source_family_key": "thematic_synthesis",
            "plan_mismatch": "plan_declared_skipped_but_live_source_available",
        }
    ]
    report_candidate = next(
        candidate for candidate in bridge.catalog.candidates if candidate.source_family_key == "thematic_report"
    )
    assert report_candidate.source_backend_kind == "normalized_report_payload"
    assert [item.candidate.source_family_key for item in bridge.selection.rejected] == [
        "engagement_mapping",
        "sin_findings",
    ]


def test_source_catalog_candidates_emit_role_hints_from_capability_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": AOI_WORKFLOW_KEY},
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_effective_plan_context",
        lambda job_id, plan_id=None: SimpleNamespace(plan=None, source="missing"),
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_aoi_normalized_artifact",
        lambda job_id, engine_key: {
            "aoi_thematic_synthesis": {"themes": [{"theme_name": "Planning"}]},
            "aoi_engagement_mapping": {"engagements": [{"theme": "Planning"}]},
            "aoi_sin_findings": {"findings": [{"theme": "Planning"}]},
        }.get(engine_key),
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_phase_outputs",
        lambda job_id, engine_key=None: [
            {
                "id": "po-report-1",
                "phase_number": 4.0,
                "pass_number": 1,
                "created_at": "2026-03-23T10:00:00",
                "metadata": {
                    "normalized": {
                        "report_sections": {
                            "summary": "Summary",
                            "engagement_pattern": "Pattern",
                        }
                    }
                },
            }
        ],
    )

    catalog = resolve_source_catalog(source_v2_job_id="job-role-hints")
    registry = get_engine_registry()

    for candidate in catalog.candidates:
        capability = resolve_capability_definition(registry, candidate.engine_key)
        assert capability is not None
        assert candidate.composition_role_hint == capability.composition_role


def test_build_source_composition_bridge_profile_fails_when_required_family_loses_role_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": AOI_WORKFLOW_KEY},
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_effective_plan_context",
        lambda job_id, plan_id=None: SimpleNamespace(plan=None, source="missing"),
    )

    def _fail_if_thematic_read(job_id, engine_key):
        if engine_key == "aoi_thematic_synthesis":
            raise AssertionError("role metadata failure should happen before thematic artifact lookup")
        return None

    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_aoi_normalized_artifact",
        _fail_if_thematic_read,
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_phase_outputs",
        lambda job_id, engine_key=None: [
            {
                "id": "po-report-1",
                "phase_number": 4.0,
                "pass_number": 1,
                "created_at": "2026-03-23T10:00:00",
                "metadata": {"normalized": {"report_sections": {"summary": "Summary"}}},
            }
        ],
    )

    def _resolve_with_missing_thematic_role(engine_registry, engine_key):
        if engine_key == "aoi_thematic_synthesis":
            raise CapabilityMetadataResolutionError("missing composition_role for thematic synthesis")
        return _resolve_composition_role(engine_registry, engine_key)

    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.resolve_composition_role",
        _resolve_with_missing_thematic_role,
    )

    with pytest.raises(ComposeFromSourceResolutionError) as excinfo:
        build_source_composition_bridge(
            source_v2_job_id="job-profile-metadata-fail",
            profile="dossier",
        )

    assert "thematic_synthesis (invalid:" in str(excinfo.value)
    assert "Composition role metadata resolution failed" in str(excinfo.value)


def test_build_selection_composition_bridge_explicit_selection_fails_when_required_family_loses_role_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": AOI_WORKFLOW_KEY},
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_effective_plan_context",
        lambda job_id, plan_id=None: SimpleNamespace(plan=None, source="missing"),
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_aoi_normalized_artifact",
        lambda job_id, engine_key: None,
    )

    def _fail_if_report_lookup(job_id, engine_key=None):
        if engine_key == "aoi_thematic_report":
            raise AssertionError("role metadata failure should happen before report output lookup")
        return []

    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_phase_outputs",
        _fail_if_report_lookup,
    )

    def _resolve_with_missing_report_role(engine_registry, engine_key):
        if engine_key == "aoi_thematic_report":
            raise CapabilityMetadataResolutionError("missing composition_role for thematic report")
        return _resolve_composition_role(engine_registry, engine_key)

    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.resolve_composition_role",
        _resolve_with_missing_report_role,
    )

    with pytest.raises(ComposeFromSourceResolutionError) as excinfo:
        build_selection_composition_bridge(
            source_v2_job_id="job-explicit-metadata-fail",
            selection=[
                AoiSelectedSourceInput(
                    source_family_key=SOURCE_FAMILY_THEMATIC_REPORT,
                    selection_rank=1,
                    rationale="Need the report closeout.",
                )
            ],
            selection_summary="Explicitly select report only.",
        )

    assert "thematic_report (invalid:" in str(excinfo.value)
    assert "Composition role metadata resolution failed" in str(excinfo.value)


def test_build_selection_composition_bridge_materializes_non_profile_family_combination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan = SimpleNamespace(
        objective_key="influence_thematic",
        workflow_key=AOI_WORKFLOW_KEY,
        selected_source_thinker_id="otto_neurath",
        selected_source_thinker_name="Otto Neurath",
        phases=[],
    )

    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": AOI_WORKFLOW_KEY},
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_effective_plan_context",
        lambda job_id, plan_id=None: SimpleNamespace(plan=plan, source="job_plan_data"),
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_aoi_normalized_artifact",
        lambda job_id, engine_key: {
            "aoi_thematic_synthesis": {"themes": [{"theme_name": "Planning"}]},
            "aoi_engagement_mapping": {"engagements": [{"theme": "Planning"}]},
            "aoi_sin_findings": {"findings": [{"theme": "Planning"}]},
        }.get(engine_key),
    )
    monkeypatch.setattr(
        "src.presenter.composition_source_bridge.load_phase_outputs",
        lambda job_id, engine_key=None: [
            {
                "id": "po-report-1",
                "phase_number": 4.0,
                "pass_number": 1,
                "created_at": "2026-03-23T10:00:00",
                "metadata": {
                    "normalized": {
                        "report_sections": {
                            "summary": "Summary",
                            "engagement_pattern": "Pattern",
                        }
                    }
                },
            }
        ],
    )

    bridge = build_selection_composition_bridge(
        source_v2_job_id="job-1",
        selection=[
            AoiSelectedSourceInput(
                source_family_key=SOURCE_FAMILY_THEMATIC_SYNTHESIS,
                selection_rank=1,
                rationale="Lead with thematic synthesis.",
            ),
            AoiSelectedSourceInput(
                source_family_key=SOURCE_FAMILY_ENGAGEMENT_MAPPING,
                selection_rank=2,
                rationale="Include the engagement map for contrast.",
            ),
            AoiSelectedSourceInput(
                source_family_key=SOURCE_FAMILY_THEMATIC_REPORT,
                selection_rank=3,
                rationale="Close with the structured report.",
            ),
        ],
        selection_summary="Use synthesis, engagement, and report without the findings bank.",
    )

    assert bridge.selection.selection_kind == "explicit"
    assert bridge.selection.profile is None
    assert bridge.selection.legacy_profile_equivalent is None
    assert [section.source_family_key for section in bridge.materialized_sections] == [
        SOURCE_FAMILY_THEMATIC_SYNTHESIS,
        SOURCE_FAMILY_ENGAGEMENT_MAPPING,
        SOURCE_FAMILY_THEMATIC_REPORT,
    ]
