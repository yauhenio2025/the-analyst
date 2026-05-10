import asyncio
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from src.analysis_products.schemas import AnalysisResultManifest
from src.analysis_products.source_backed_readiness import (
    SourceBackedReadinessNotFoundError,
    SourceBackedReadinessRequestError,
    build_source_backed_readiness,
)
from src.aoi.constants import AOI_WORKFLOW_KEY
from src.api.routes.results import get_source_backed_readiness_route
from src.presenter.bounded_dynamic_composition import (
    COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1,
    inspect_runtime_composition_on_payload_copy,
    list_supported_composition_modes_for_workflow,
)
from src.presenter.composition_source_bridge import (
    CompositionSourceCandidate,
    CompositionSourceCatalog,
)
from src.presenter.presentation_api import _load_per_item_data
from src.presenter.schemas import ViewPayload


def _manifest(
    *,
    workflow_key: str = "intellectual_genealogy",
    result_state: str = "ready",
    presentation_status: str = "completed",
    restore_available: bool = True,
    restore_reason: str = "presentation_ready",
) -> AnalysisResultManifest:
    return AnalysisResultManifest(
        job_id="job-1",
        plan_id="plan-1",
        workflow_key=workflow_key,
        consumer_key="the-critic",
        result_id="result-1",
        result_state=result_state,
        corpus_ref="corp-1",
        status="completed",
        presentation_contract_version=1,
        presentation_hash="hash-1",
        presentation_content_hash="content-1",
        prepared_at="2026-03-23T12:00:00+00:00",
        artifacts_ready=True,
        presentation_status=presentation_status,
        preparation_detail="",
        presentation_active=False,
        restore_available=restore_available,
        restore_reason=restore_reason,
        staleness_reasons=[],
        product_warnings=[],
        links={
            "page_url": "",
            "presentation_url": "",
            "manifest_url": "",
            "trace_url": "",
            "refresh_presentation_url": "",
        },
        artifact_families=[],
    )


def _aoi_catalog(*, sin_state: str = "unavailable") -> CompositionSourceCatalog:
    return CompositionSourceCatalog(
        source_v2_job_id="job-aoi",
        workflow_key=AOI_WORKFLOW_KEY,
        objective_key="influence_thematic",
        objective_source="job_plan_data",
        plan_context_found=True,
        plan_context_source="job_plan_data",
        selected_source_thinker_id="otto_neurath",
        selected_source_thinker_name="Otto Neurath",
        candidates=[
            CompositionSourceCandidate(
                source_family_key="thematic_synthesis",
                engine_key="aoi_thematic_synthesis",
                title="Thematic Synthesis",
                source_backend_kind="artifact",
                candidate_state="available",
            ),
            CompositionSourceCandidate(
                source_family_key="engagement_mapping",
                engine_key="aoi_engagement_mapping",
                title="Engagement Mapping",
                source_backend_kind="artifact",
                candidate_state="available",
            ),
            CompositionSourceCandidate(
                source_family_key="sin_findings",
                engine_key="aoi_sin_findings",
                title="Sin Findings",
                source_backend_kind="artifact",
                candidate_state=sin_state,
            ),
            CompositionSourceCandidate(
                source_family_key="thematic_report",
                engine_key="aoi_thematic_report",
                title="AOI Report",
                source_backend_kind="phase_output_metadata",
                candidate_state="available",
            ),
        ],
    )


def _groupable_payload(view_key: str, position: float) -> ViewPayload:
    return ViewPayload(
        view_key=view_key,
        view_name=view_key.replace("_", " ").title(),
        description="",
        renderer_type="accordion",
        renderer_config={"sections": [{"key": "summary", "title": "Summary"}]},
        presentation_stance="diagnostic",
        priority="primary",
        rationale="",
        data_quality="standard",
        source_parent_view_key=None,
        phase_number=1.0,
        engine_key="test_engine",
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
        position=position,
        children=[],
    )


class _FakeTransformRegistry:
    def for_engine(self, _engine_key):
        return [SimpleNamespace(template_key="tp_concept_evolution_extraction")]


def test_source_backed_readiness_requires_one_selector_kind():
    with pytest.raises(SourceBackedReadinessRequestError, match="Provide either profile or composition_mode"):
        build_source_backed_readiness(
            "job-1",
            profile="dossier",
            composition_mode=COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1,
        )


def test_source_backed_readiness_route_maps_request_error_to_400(monkeypatch):
    monkeypatch.setattr(
        "src.api.routes.results.build_source_backed_readiness",
        lambda *args, **kwargs: (_ for _ in ()).throw(SourceBackedReadinessRequestError("bad request")),
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(get_source_backed_readiness_route("job-1", consumer_key="the-critic"))

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "bad request"


def test_source_backed_readiness_route_maps_missing_job_to_404(monkeypatch):
    monkeypatch.setattr(
        "src.api.routes.results.build_source_backed_readiness",
        lambda *args, **kwargs: (_ for _ in ()).throw(SourceBackedReadinessNotFoundError("Job not found: job-1")),
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(get_source_backed_readiness_route("job-1", consumer_key="the-critic"))

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Job not found: job-1"


def test_aoi_readiness_is_partially_ready_when_profiles_are_feasible_but_consumer_is_not_supported(monkeypatch):
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": AOI_WORKFLOW_KEY},
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.resolve_source_catalog",
        lambda source_v2_job_id: _aoi_catalog(),
    )

    decision = build_source_backed_readiness(
        "job-aoi",
        consumer_key="another-consumer",
    )

    assert decision.requested_selector is None
    assert decision.requested_selector_status == "not_requested"
    assert decision.allowed_selectors == []
    assert decision.blocked_selectors["dossier"] == [
        "compose-from-source only supports registered consumer adapters; got 'another-consumer'"
    ]
    assert decision.blocked_selectors["comparison"] == ["sin_findings (unavailable)"]
    assert decision.followup_readiness_status == "blocked"
    assert decision.readiness_status == "blocked"
    assert "compose-from-source only supports registered consumer adapters; got 'another-consumer'" in (
        decision.downstream_followup_contract["blocking_reasons"]
    )


def test_aoi_readiness_accepts_aoi_canary_for_dossier_profile_and_keeps_selector_lifecycle_stable(monkeypatch):
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": AOI_WORKFLOW_KEY},
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.resolve_source_catalog",
        lambda source_v2_job_id: _aoi_catalog(),
    )

    decision = build_source_backed_readiness(
        "job-744edf255ad5",
        consumer_key="aoi-canary",
        profile="dossier",
    )

    assert decision.selector_lifecycle_phase == "source_selection"
    assert decision.requested_selector == "dossier"
    assert decision.requested_selector_status == "ready"
    assert decision.followup_readiness_status == "ready"
    assert decision.readiness_status == "ready"
    assert decision.downstream_followup_contract["endpoint"] == "/v1/presenter/compose-from-source"
    assert decision.downstream_followup_contract["request_fields"] == {
        "workflow_key": AOI_WORKFLOW_KEY,
        "consumer_key": "aoi-canary",
        "source_v2_job_id": "job-744edf255ad5",
        "profile": "dossier",
    }
    assert "blocking_reasons" not in decision.downstream_followup_contract


def test_aoi_readiness_reports_requested_blocked_profile_but_available_alternative(monkeypatch):
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": AOI_WORKFLOW_KEY},
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.resolve_source_catalog",
        lambda source_v2_job_id: _aoi_catalog(),
    )

    decision = build_source_backed_readiness(
        "job-aoi",
        consumer_key="the-critic",
        profile="comparison",
    )

    assert decision.requested_selector == "comparison"
    assert decision.requested_selector_status == "blocked"
    assert decision.allowed_selectors == ["dossier"]
    assert decision.followup_readiness_status == "ready"
    assert decision.readiness_status == "partially_ready"


def test_aoi_canary_readiness_accepts_comparison_profile_when_catalog_supports_it(monkeypatch):
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": AOI_WORKFLOW_KEY},
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.resolve_source_catalog",
        lambda source_v2_job_id: _aoi_catalog(sin_state="available"),
    )

    decision = build_source_backed_readiness(
        "job-744edf255ad5",
        consumer_key="aoi-canary",
        profile="comparison",
    )

    assert decision.selector_lifecycle_phase == "source_selection"
    assert decision.requested_selector == "comparison"
    assert decision.requested_selector_status == "ready"
    assert decision.allowed_selectors == ["dossier", "comparison"]
    assert decision.blocked_selectors == {}
    assert decision.followup_readiness_status == "ready"
    assert decision.readiness_status == "ready"
    assert decision.downstream_followup_contract["request_fields"] == {
        "workflow_key": AOI_WORKFLOW_KEY,
        "consumer_key": "aoi-canary",
        "source_v2_job_id": "job-744edf255ad5",
        "profile": "comparison",
    }


def test_transient_proof_harness_readiness_keeps_source_profile_blocked(monkeypatch):
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": AOI_WORKFLOW_KEY},
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.resolve_source_catalog",
        lambda source_v2_job_id: _aoi_catalog(sin_state="available"),
    )

    decision = build_source_backed_readiness(
        "job-744edf255ad5",
        consumer_key="transient-proof-harness",
        profile="dossier",
    )

    assert decision.selector_lifecycle_phase == "source_selection"
    assert decision.requested_selector == "dossier"
    assert decision.requested_selector_status == "blocked"
    assert decision.allowed_selectors == []
    assert decision.blocked_selectors["dossier"] == [
        "compose-from-source does not support consumer_key='transient-proof-harness' for handoff_kind='source_profile'"
    ]
    assert decision.followup_readiness_status == "blocked"
    assert decision.readiness_status == "blocked"


def test_transient_proof_probe_readiness_keeps_source_profile_blocked(monkeypatch):
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": AOI_WORKFLOW_KEY},
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.resolve_source_catalog",
        lambda source_v2_job_id: _aoi_catalog(sin_state="available"),
    )

    decision = build_source_backed_readiness(
        "job-744edf255ad5",
        consumer_key="transient-proof-probe",
        profile="dossier",
    )

    assert decision.selector_lifecycle_phase == "source_selection"
    assert decision.requested_selector == "dossier"
    assert decision.requested_selector_status == "blocked"
    assert decision.allowed_selectors == []
    assert decision.blocked_selectors["dossier"] == [
        "compose-from-source does not support consumer_key='transient-proof-probe' for handoff_kind='source_profile'"
    ]
    assert decision.followup_readiness_status == "blocked"
    assert decision.readiness_status == "blocked"


def test_aoi_readiness_rejects_composition_mode_selector(monkeypatch):
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": AOI_WORKFLOW_KEY},
    )

    with pytest.raises(SourceBackedReadinessRequestError, match="composition_mode readiness is out of scope for AOI Stage 10"):
        build_source_backed_readiness(
            "job-aoi",
            consumer_key="the-critic",
            composition_mode=COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1,
        )


def test_genealogy_readiness_rejects_profile_selector(monkeypatch):
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": "intellectual_genealogy"},
    )

    with pytest.raises(SourceBackedReadinessRequestError, match="profile readiness is only supported for AOI workflows"):
        build_source_backed_readiness("job-1", profile="dossier")


def test_genealogy_readiness_blocks_all_modes_before_runtime_when_presentation_not_prepared(monkeypatch):
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": "intellectual_genealogy"},
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.build_result_manifest",
        lambda job_id, consumer_key="the-critic": _manifest(
            presentation_status="running",
            restore_available=False,
            restore_reason="preparing",
            result_state="preparing",
        ),
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness._prepare_page_payloads",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("runtime inspection should not run")),
    )

    decision = build_source_backed_readiness("job-1", consumer_key="the-critic")
    supported_modes = list_supported_composition_modes_for_workflow("intellectual_genealogy")

    assert decision.requested_selector is None
    assert decision.requested_selector_status == "not_requested"
    assert decision.allowed_selectors == []
    assert sorted(decision.blocked_selectors.keys()) == sorted(supported_modes)
    assert decision.followup_readiness_status == "blocked"
    assert decision.readiness_status == "blocked"
    assert decision.genealogy_readiness_detail.presentation_status == "running"
    assert decision.genealogy_readiness_detail.restore_reason == "preparing"


def test_genealogy_readiness_reports_requested_blocked_mode_with_alternative(monkeypatch):
    supported_modes = list_supported_composition_modes_for_workflow("intellectual_genealogy")
    requested_mode = supported_modes[0]
    allowed_alternative = supported_modes[1]

    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": "intellectual_genealogy"},
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.build_result_manifest",
        lambda job_id, consumer_key="the-critic": _manifest(),
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness._prepare_page_payloads",
        lambda *args, **kwargs: {"payloads": {}, "workflow_key": "intellectual_genealogy"},
    )

    def _inspect_mode(*, composition_mode, **_kwargs):
        if composition_mode == requested_mode:
            issue = SimpleNamespace(
                reason="missing_group_child",
                view_key="dynamic_genealogy_briefing",
                field="children",
                message="missing child",
            )
            return False, None, [issue]
        return True, {"selected": composition_mode}, []

    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.inspect_runtime_composition_on_payload_copy",
        _inspect_mode,
    )

    decision = build_source_backed_readiness(
        "job-1",
        consumer_key="the-critic",
        composition_mode=requested_mode,
    )

    assert decision.requested_selector == requested_mode
    assert decision.requested_selector_status == "blocked"
    assert allowed_alternative in decision.allowed_selectors
    assert decision.followup_readiness_status == "ready"
    assert decision.readiness_status == "partially_ready"


def test_genealogy_readiness_without_requested_selector_inspects_all_modes(monkeypatch):
    supported_modes = list_supported_composition_modes_for_workflow("intellectual_genealogy")

    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": "intellectual_genealogy"},
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.build_result_manifest",
        lambda job_id, consumer_key="the-critic": _manifest(),
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness._prepare_page_payloads",
        lambda *args, **kwargs: {"payloads": {}, "workflow_key": "intellectual_genealogy"},
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.inspect_runtime_composition_on_payload_copy",
        lambda **kwargs: (True, {"selected": kwargs["composition_mode"]}, []),
    )

    decision = build_source_backed_readiness("job-1", consumer_key="the-critic")

    assert decision.requested_selector is None
    assert decision.requested_selector_status == "not_requested"
    assert decision.allowed_selectors == supported_modes
    assert decision.readiness_status == "ready"


def test_genealogy_readiness_uses_read_only_payload_prep_and_does_not_create_relationship_artifacts(monkeypatch):
    outputs = [
        {
            "id": "po-winning",
            "work_key": "work_a",
            "pass_number": 2,
            "phase_number": 1.5,
            "content": "Winning prose",
            "metadata": {},
        },
    ]
    captured: dict[str, object] = {}

    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.get_job",
        lambda job_id: {"job_id": job_id, "workflow_key": "intellectual_genealogy"},
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.build_result_manifest",
        lambda job_id, consumer_key="the-critic": _manifest(),
    )
    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness.inspect_runtime_composition_on_payload_copy",
        lambda **kwargs: (True, {"selected": kwargs["composition_mode"]}, []),
    )

    def _prepare_payloads(job_id, *, consumer_key, slim=False, read_only=False):
        captured["read_only"] = read_only
        items = _load_per_item_data(
            job_id=job_id,
            phase_number=1.5,
            engine_key="genealogy_relationship_classification",
            slim=False,
            read_only=read_only,
        )
        payload = ViewPayload(
            view_key="genealogy_relationship_landscape",
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
        return {"payloads": {payload.view_key: payload}, "workflow_key": "intellectual_genealogy"}

    monkeypatch.setattr(
        "src.analysis_products.source_backed_readiness._prepare_page_payloads",
        _prepare_payloads,
    )

    with patch(
        "src.presenter.presentation_api.load_phase_outputs",
        return_value=outputs,
    ), patch(
        "src.transformations.registry.get_transformation_registry",
        return_value=_FakeTransformRegistry(),
    ), patch(
        "src.presenter.presentation_api.load_presentation_cache",
        return_value={
            "relationship_type": "methodological_ancestor",
            "confidence": "high",
        },
    ), patch(
        "src.presenter.presentation_api._resolve_work_metadata",
        return_value={"display_title": "Work A", "year": 1984},
    ), patch(
        "src.analysis_products.store.store_relationship_classification_artifact",
    ) as persist_artifact:
        decision = build_source_backed_readiness("job-1", consumer_key="the-critic")

    assert captured["read_only"] is True
    persist_artifact.assert_not_called()
    assert decision.readiness_status == "ready"


def test_runtime_inspection_helper_does_not_mutate_original_payloads():
    payloads = {
        "genealogy_target_profile": _groupable_payload("genealogy_target_profile", 1.0),
        "genealogy_relationship_landscape": _groupable_payload("genealogy_relationship_landscape", 1.1),
        "genealogy_text_profiling": _groupable_payload("genealogy_text_profiling", 2.0),
        "genealogy_idea_evolution": _groupable_payload("genealogy_idea_evolution", 2.1),
        "genealogy_tactics": _groupable_payload("genealogy_tactics", 2.2),
        "genealogy_conditions": _groupable_payload("genealogy_conditions", 3.0),
        "genealogy_portrait": _groupable_payload("genealogy_portrait", 3.1),
    }

    applied, details, issues = inspect_runtime_composition_on_payload_copy(
        payloads=payloads,
        workflow_key="intellectual_genealogy",
        consumer_key="the-critic",
        composition_mode=COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1,
    )

    assert applied is True
    assert details is None
    assert issues == []
    assert payloads["genealogy_target_profile"].source_parent_view_key is None
    assert "dynamic_genealogy_briefing" not in payloads
