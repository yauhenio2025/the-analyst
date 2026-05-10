import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.api.routes.evaluations import router as evaluations_router
from src.evaluations.resolution_schemas import (
    EvaluationResolverIdentity,
    PersistedEvaluationDispositionResolution,
)
from src.evaluations.resolution_store import save_evaluation_disposition_resolution


def _resolution(
    resolution_id: str,
    *,
    created_at: str,
    resolution_key: str = "bounded_platform_readiness_resolution_v1",
    review_decision_id: str = "review-decision-21edf9b955ee",
    gate_decision_id: str = "gate-decision-745c2cb7e090",
    evaluation_pack_key: str = "phase4_frozen_governance_v1",
) -> PersistedEvaluationDispositionResolution:
    return PersistedEvaluationDispositionResolution(
        resolution_id=resolution_id,
        resolution_key=resolution_key,
        created_at=created_at,
        resolution_definition_version="v1",
        review_decision_id=review_decision_id,
        review_key="bounded_platform_readiness_review_v1",
        review_definition_version="v1",
        gate_decision_id=gate_decision_id,
        gate_key="bounded_platform_readiness_v1",
        gate_definition_version="v1",
        evaluation_pack_key=evaluation_pack_key,
        resolver_identity=EvaluationResolverIdentity(
            resolver_name="Codex",
            resolver_role="operator",
        ),
        resolution_note="Adopting this exact review as the current stance.",
        adopted_review_disposition="accept",
        observed_gate_verdict="pass",
        contains_live_revalidation=True,
    )


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(evaluations_router, prefix="/v1")
    return TestClient(app)


def test_resolution_routes_fetch_and_list_with_filters(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.resolution_store.EVALUATION_RESOLUTIONS_DIR", tmp_path)
    resolution = save_evaluation_disposition_resolution(
        _resolution("resolution-route", created_at="2026-03-29T01:00:00+00:00")
    )
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-other",
            created_at="2026-03-29T02:00:00+00:00",
            resolution_key="other-resolution",
            review_decision_id="review-decision-other",
            gate_decision_id="gate-decision-other",
            evaluation_pack_key="other-pack",
        )
    )

    with _client() as client:
        get_response = client.get(f"/v1/evaluations/resolutions/{resolution.resolution_id}")
        list_response = client.get(
            "/v1/evaluations/resolutions",
            params={
                "resolution_key": "bounded_platform_readiness_resolution_v1",
                "review_decision_id": "review-decision-21edf9b955ee",
                "gate_decision_id": "gate-decision-745c2cb7e090",
                "evaluation_pack_key": "phase4_frozen_governance_v1",
                "limit": 10,
            },
        )

    assert get_response.status_code == 200
    assert get_response.json()["resolution_id"] == resolution.resolution_id
    assert list_response.status_code == 200
    body = list_response.json()
    assert body["count"] == 1
    assert body["resolutions"][0]["resolution_id"] == resolution.resolution_id
    assert body["resolutions"][0]["review_key"] == "bounded_platform_readiness_review_v1"
    assert body["resolutions"][0]["gate_key"] == "bounded_platform_readiness_v1"


def test_current_resolution_route_uses_canonical_store_lookup_and_is_not_swallowed(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.resolution_store.EVALUATION_RESOLUTIONS_DIR", tmp_path)
    save_evaluation_disposition_resolution(
        _resolution("resolution-older", created_at="2026-03-29T00:00:00+00:00")
    )
    newer = save_evaluation_disposition_resolution(
        _resolution("resolution-newer", created_at="2026-03-29T01:00:00+00:00")
    )

    with _client() as client:
        response = client.get(
            "/v1/evaluations/resolutions/current",
            params={
                "resolution_key": "bounded_platform_readiness_resolution_v1",
                "gate_decision_id": "gate-decision-745c2cb7e090",
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["resolution_key"] == "bounded_platform_readiness_resolution_v1"
    assert body["gate_decision_id"] == "gate-decision-745c2cb7e090"
    assert body["resolution"]["resolution_id"] == newer.resolution_id


def test_current_resolution_route_returns_404_when_other_scopes_exist_only(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.resolution_store.EVALUATION_RESOLUTIONS_DIR", tmp_path)
    save_evaluation_disposition_resolution(
        _resolution(
            "resolution-other",
            created_at="2026-03-29T01:00:00+00:00",
            resolution_key="other-resolution",
            gate_decision_id="gate-decision-other",
        )
    )

    with _client() as client:
        response = client.get(
            "/v1/evaluations/resolutions/current",
            params={
                "resolution_key": "bounded_platform_readiness_resolution_v1",
                "gate_decision_id": "gate-decision-745c2cb7e090",
            },
        )

    assert response.status_code == 404


def test_resolution_route_returns_404_for_missing_resolution_id(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.resolution_store.EVALUATION_RESOLUTIONS_DIR", tmp_path)

    with _client() as client:
        response = client.get("/v1/evaluations/resolutions/resolution-missing")

    assert response.status_code == 404
