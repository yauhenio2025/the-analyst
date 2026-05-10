import json
from pathlib import Path

from src.presenter.schemas import (
    ComposeFromIntentRequest,
    ComposeFromIntentResponse,
    ComposeFromSelectionRequest,
)


ROOT = Path(__file__).resolve().parents[1]
COMMUNICATIONS = ROOT / "communications"
CONSUMER_KEY = "transient-proof-probe"
AOI_BUNDLE_PATH = (
    COMMUNICATIONS / "PROOF_phase_e_transient_proof_probe_source_selection_2026-04-01.json"
)
GENEALOGY_BUNDLE_PATH = (
    COMMUNICATIONS
    / "PROOF_phase_e_transient_proof_probe_genealogy_direct_sections_2026-04-01.json"
)


def _load_bundle(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_transient_proof_probe_source_selection_bundle_matches_fresh_contract_truth() -> None:
    bundle = _load_bundle(AOI_BUNDLE_PATH)
    request = ComposeFromSelectionRequest.model_validate(bundle["request_json"])
    response = ComposeFromIntentResponse.model_validate(bundle["response_json"])
    adaptation = bundle["consumer_adaptation_truth"]
    root_view = response.presentation.views[0]
    raw_json_leaf_keys = [
        view.view_key
        for view in root_view.children
        if not view.children and view.renderer_type == "raw_json"
    ]

    assert bundle["consumer_key"] == CONSUMER_KEY
    assert bundle["route_family"] == "source_selection"
    assert request.consumer_key == CONSUMER_KEY
    assert response.presentation.consumer_key == CONSUMER_KEY
    assert bundle["compose_call"] == {
        "method": "POST",
        "endpoint": "/v1/presenter/compose-from-selection",
    }
    assert response.presentation.resolver_version == "compose-from-selection-v1"
    assert root_view.renderer_type == adaptation["expected_root_renderer"]
    assert raw_json_leaf_keys == adaptation["expected_raw_json_view_keys"]
    assert adaptation["observed_raw_json_view_keys"] == raw_json_leaf_keys
    assert adaptation["root_renderer_matches"] is True
    assert adaptation["raw_json_set_matches"] is True


def test_transient_proof_probe_genealogy_direct_sections_bundle_matches_fresh_contract_truth() -> None:
    bundle = _load_bundle(GENEALOGY_BUNDLE_PATH)
    request = ComposeFromIntentRequest.model_validate(bundle["request_json"])
    response = ComposeFromIntentResponse.model_validate(bundle["response_json"])
    adaptation = bundle["consumer_adaptation_truth"]
    root_view = response.presentation.views[0]

    assert bundle["consumer_key"] == CONSUMER_KEY
    assert bundle["route_family"] == "direct_sections"
    assert request.consumer_key == CONSUMER_KEY
    assert response.presentation.consumer_key == CONSUMER_KEY
    assert bundle["compose_call"] == {
        "method": "POST",
        "endpoint": "/v1/presenter/compose-from-intent",
    }
    assert response.presentation.resolver_version == "compose-from-intent-v2"
    assert root_view.renderer_type == "card_grid"
    assert root_view.renderer_type == adaptation["expected_root_renderer"]
    assert adaptation["expected_raw_json_view_keys"] == []
    assert adaptation["observed_raw_json_view_keys"] == []
    assert adaptation["root_renderer_matches"] is True
    assert adaptation["raw_json_set_matches"] is True
