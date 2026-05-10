import asyncio

import pytest
from fastapi import HTTPException

from src.api.routes.presenter import (
    get_compose_session_endpoint,
    save_compose_session_endpoint,
)
from src.presenter.compose_session_store import load_compose_session, save_compose_session
from src.presenter.schemas import ComposeFromIntentRequest, ComposeFromIntentResponse


def _compose_request(*, consumer_key: str = "the-critic") -> ComposeFromIntentRequest:
    return ComposeFromIntentRequest.model_validate(
        {
            "workflow_key": "intellectual_genealogy",
            "consumer_key": consumer_key,
            "user_intent": "Compose a genealogy briefing.",
            "prose_sections": [
                {
                    "engine_key": "genealogy_relationship_classification",
                    "title": "Relationship Comparison Map",
                    "prose": "Comparison prose.",
                }
            ],
        }
    )


def _compose_response(*, consumer_key: str = "the-critic") -> ComposeFromIntentResponse:
    return ComposeFromIntentResponse.model_validate(
        {
            "presentation": {
                "workflow_key": "intellectual_genealogy",
                "consumer_key": consumer_key,
                "presentation_contract_version": 1,
                "presentation_hash": "hash-1",
                "presentation_content_hash": "content-hash-1",
                "resolver_version": "compose-from-intent-v2",
                "style_school": "explanatory_narrative",
                "views": [],
                "view_count": 0,
            },
            "generated_view_definitions": [],
            "trace": {
                "resolver_version": "compose-from-intent-v2",
                "entries": [],
            },
        }
    )


def test_compose_session_store_round_trips_exact_saved_response(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.presenter.compose_session_store.COMPOSE_SESSIONS_DIR",
        tmp_path,
    )

    saved = save_compose_session(
        compose_request=_compose_request(),
        compose_response=_compose_response(),
        planning_decision_id="planning-decision-123",
        source_v2_job_id="job-genealogy-001",
    )
    loaded = load_compose_session(saved.session_id)

    assert loaded is not None
    assert loaded.session_id.startswith("compose-session-")
    assert loaded.compose_request.user_intent == "Compose a genealogy briefing."
    assert loaded.compose_response.presentation.presentation_hash == "hash-1"
    assert loaded.presentation_hash == "hash-1"
    assert loaded.presentation_content_hash == "content-hash-1"
    assert loaded.resolver_version == "compose-from-intent-v2"


def test_save_compose_session_route_persists_and_returns_analyzer_generated_session_id(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.presenter.compose_session_store.COMPOSE_SESSIONS_DIR",
        tmp_path,
    )

    saved = asyncio.run(
        save_compose_session_endpoint(
            {
                "compose_request": _compose_request().model_dump(mode="python"),
                "compose_response": _compose_response().model_dump(mode="python"),
                "planning_decision_id": "planning-decision-123",
                "source_v2_job_id": "job-genealogy-001",
            }
        )
    )

    fetched = asyncio.run(
        get_compose_session_endpoint(
            saved.session_id,
            consumer_key="the-critic",
        )
    )

    assert saved.session_id.startswith("compose-session-")
    assert fetched.session_id == saved.session_id
    assert fetched.compose_response.presentation.resolver_version == "compose-from-intent-v2"


def test_save_compose_session_route_round_trips_transient_proof_harness_consumer(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.presenter.compose_session_store.COMPOSE_SESSIONS_DIR",
        tmp_path,
    )

    compose_request = _compose_request(consumer_key="transient-proof-harness")
    compose_response = _compose_response(consumer_key="transient-proof-harness")
    saved = asyncio.run(
        save_compose_session_endpoint(
            {
                "compose_request": compose_request.model_dump(mode="python"),
                "compose_response": compose_response.model_dump(mode="python"),
                "planning_decision_id": "planning-decision-5f5b0182f2f9",
            }
        )
    )

    fetched = asyncio.run(
        get_compose_session_endpoint(
            saved.session_id,
            consumer_key="transient-proof-harness",
        )
    )

    assert saved.consumer_key == "transient-proof-harness"
    assert saved.planning_decision_id == "planning-decision-5f5b0182f2f9"
    assert saved.source_v2_job_id is None
    assert fetched.session_id == saved.session_id
    assert fetched.consumer_key == "transient-proof-harness"
    assert fetched.compose_response.presentation.presentation_hash == "hash-1"


def test_save_compose_session_route_returns_409_on_request_response_mismatch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.presenter.compose_session_store.COMPOSE_SESSIONS_DIR",
        tmp_path,
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(
            save_compose_session_endpoint(
                {
                    "compose_request": _compose_request().model_dump(mode="python"),
                    "compose_response": _compose_response(consumer_key="another-consumer").model_dump(mode="python"),
                }
            )
        )

    assert excinfo.value.status_code == 409


def test_get_compose_session_route_returns_404_for_missing_session(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.presenter.compose_session_store.COMPOSE_SESSIONS_DIR",
        tmp_path,
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(
            get_compose_session_endpoint(
                "compose-session-missing",
                consumer_key="the-critic",
            )
        )

    assert excinfo.value.status_code == 404


def test_get_compose_session_route_returns_409_on_consumer_mismatch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.presenter.compose_session_store.COMPOSE_SESSIONS_DIR",
        tmp_path,
    )

    saved = save_compose_session(
        compose_request=_compose_request(),
        compose_response=_compose_response(),
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(
            get_compose_session_endpoint(
                saved.session_id,
                consumer_key="different-consumer",
            )
        )

    assert excinfo.value.status_code == 409
