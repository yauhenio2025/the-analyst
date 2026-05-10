from __future__ import annotations

import json
from pathlib import Path

from src.orchestrator.task_planning_schemas import PersistedTaskPlanningDecision
from src.presenter.schemas import (
    ComposeFromIntentRequest,
    ComposeFromIntentResponse,
    ComposeFromSelectionRequest,
    ComposeFromSourceRequest,
)


_COMMUNICATIONS_DIR = Path(__file__).resolve().parents[1] / "communications"
_AOI_WORKFLOW_KEY = "anxiety_of_influence_thematic_single_thinker"
_GENEALOGY_WORKFLOW_KEY = "intellectual_genealogy"
_THE_CRITIC = "the-critic"
_EXPECTED_FIRST_HOP_AFFORDANCE = {
    "capturable": True,
    "allowed_destinations": ["arsenal", "research_todo"],
}
_EXPECTED_AOI_SOURCE_FAMILIES = {
    "thematic_synthesis",
    "engagement_mapping",
    "sin_findings",
    "thematic_report",
}


def _load_bundle(filename: str) -> dict:
    return json.loads((_COMMUNICATIONS_DIR / filename).read_text())


def _assert_common_response_contract(
    bundle: dict,
    response: ComposeFromIntentResponse,
    *,
    expected_endpoint: str,
    expected_resolver_version: str,
) -> None:
    assert bundle["compose_call"] == {"method": "POST", "endpoint": expected_endpoint}
    assert response.presentation.workflow_key == bundle["workflow_key"]
    assert response.presentation.consumer_key == bundle["consumer_key"]
    assert response.presentation.consumer_key == _THE_CRITIC
    assert response.presentation.view_count == len(response.generated_view_definitions)
    assert response.presentation.resolver_version == expected_resolver_version


def _assert_first_hop_affordance(view, *, expected: dict | None) -> None:
    if expected is None:
        assert view.first_hop_affordance is None
        return
    assert view.first_hop_affordance is not None
    assert view.first_hop_affordance.model_dump(mode="json", exclude_none=True) == expected


def test_phase_e_matrix_aoi_source_profile_dossier_case() -> None:
    bundle = _load_bundle("PROOF_phase_e_matrix_aoi_source_profile_dossier_2026-03-30.json")

    request = ComposeFromSourceRequest.model_validate(bundle["request_json"])
    response = ComposeFromIntentResponse.model_validate(bundle["response_json"])

    assert bundle["route_family"] == "source_profile"
    assert bundle["workflow_key"] == _AOI_WORKFLOW_KEY
    assert bundle["consumer_key"] == _THE_CRITIC
    assert bundle["source_v2_job_id"] == "job-744edf255ad5"
    assert request.workflow_key == _AOI_WORKFLOW_KEY
    assert request.consumer_key == _THE_CRITIC
    assert request.source_v2_job_id == "job-744edf255ad5"
    assert request.profile == "dossier"

    _assert_common_response_contract(
        bundle,
        response,
        expected_endpoint="/v1/presenter/compose-from-source",
        expected_resolver_version="compose-from-source-v3",
    )
    parent = response.presentation.views[0]
    _assert_first_hop_affordance(parent, expected=None)
    assert len(parent.children) == 2
    for child in parent.children:
        _assert_first_hop_affordance(
            child,
            expected=_EXPECTED_FIRST_HOP_AFFORDANCE,
        )


def test_phase_e_matrix_aoi_source_selection_case() -> None:
    bundle = _load_bundle("PROOF_phase_e_matrix_aoi_source_selection_2026-03-30.json")

    request = ComposeFromSelectionRequest.model_validate(bundle["request_json"])
    response = ComposeFromIntentResponse.model_validate(bundle["response_json"])
    snapshot = PersistedTaskPlanningDecision.model_validate(bundle["planning_snapshot"])
    handoff = snapshot.planning_decision.aoi_composition_handoff_plan

    assert handoff is not None
    assert bundle["route_family"] == "source_selection"
    assert bundle["workflow_key"] == _AOI_WORKFLOW_KEY
    assert bundle["consumer_key"] == _THE_CRITIC
    assert bundle["planning_decision_id"] == snapshot.planning_decision_id
    assert bundle["source_v2_job_id"] == snapshot.source_v2_job_id
    assert bundle["source_v2_job_id"] == handoff.source_v2_job_id

    # Mechanical request equality over the actual compose-from-selection wire fields.
    assert request.workflow_key == handoff.workflow_key
    assert request.consumer_key == handoff.consumer_key
    assert request.source_v2_job_id == bundle["source_v2_job_id"]
    assert request.source_v2_job_id == handoff.source_v2_job_id
    assert request.selection == handoff.selected_sources
    assert request.user_intent == handoff.resolved_intent_seed
    assert request.selection_summary == handoff.selection_summary
    assert request.legacy_profile_equivalent == handoff.legacy_profile_equivalent

    # Separate snapshot-level assertions for the planner-only source-family law.
    assert set(handoff.expected_source_families) == _EXPECTED_AOI_SOURCE_FAMILIES
    assert set(handoff.available_source_families) == _EXPECTED_AOI_SOURCE_FAMILIES
    assert len(handoff.expected_source_families) == 4
    assert len(handoff.available_source_families) == 4

    _assert_common_response_contract(
        bundle,
        response,
        expected_endpoint="/v1/presenter/compose-from-selection",
        expected_resolver_version="compose-from-selection-v1",
    )
    parent = response.presentation.views[0]
    _assert_first_hop_affordance(parent, expected=None)
    assert len(parent.children) == 4
    for child in parent.children:
        _assert_first_hop_affordance(
            child,
            expected=_EXPECTED_FIRST_HOP_AFFORDANCE,
        )


def test_phase_e_matrix_genealogy_direct_sections_case() -> None:
    bundle = _load_bundle("PROOF_phase_e_matrix_genealogy_direct_sections_2026-03-30.json")

    request = ComposeFromIntentRequest.model_validate(bundle["request_json"])
    lowering_response = ComposeFromIntentRequest.model_validate(bundle["lowering_response_json"])
    response = ComposeFromIntentResponse.model_validate(bundle["response_json"])
    snapshot = PersistedTaskPlanningDecision.model_validate(bundle["planning_snapshot"])
    handoff = snapshot.planning_decision.direct_sections_composition_handoff_plan

    assert handoff is not None
    assert bundle["route_family"] == "direct_sections"
    assert bundle["workflow_key"] == _GENEALOGY_WORKFLOW_KEY
    assert bundle["consumer_key"] == _THE_CRITIC
    assert bundle["planning_decision_id"] == snapshot.planning_decision_id
    assert bundle["source_v2_job_id"] == snapshot.source_v2_job_id
    assert bundle["source_v2_job_id"] == handoff.source_v2_job_id
    assert bundle["lowering_call"]["method"] == "GET"
    assert (
        bundle["lowering_call"]["endpoint"]
        == "/v1/orchestrator/planning-decisions/{planning_decision_id}/compose-from-intent-request"
    )
    assert bundle["lowering_call"]["planning_decision_id"] == snapshot.planning_decision_id
    assert bundle["lowering_call"]["consumer_key"] == _THE_CRITIC

    # Mechanical proof that lowering output is the exact compose input.
    assert lowering_response.model_dump(mode="json") == request.model_dump(mode="json")

    # Mechanical proof that the compose request is directly derivable from the handoff plan.
    assert request.workflow_key == handoff.workflow_key
    assert request.consumer_key == handoff.consumer_key
    assert request.user_intent == handoff.resolved_intent_seed
    assert request.prose_sections == handoff.prose_sections

    _assert_common_response_contract(
        bundle,
        response,
        expected_endpoint="/v1/presenter/compose-from-intent",
        expected_resolver_version="compose-from-intent-v2",
    )
    assert len(response.presentation.views) == 1
    _assert_first_hop_affordance(
        response.presentation.views[0],
        expected=_EXPECTED_FIRST_HOP_AFFORDANCE,
    )
