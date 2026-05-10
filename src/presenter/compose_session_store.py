"""File-backed persistence for saved transient compose sessions."""

from __future__ import annotations

from datetime import datetime, timezone
import logging
from pathlib import Path
from typing import Optional
from uuid import uuid4

from src.presenter.schemas import (
    ComposeFromIntentRequest,
    ComposeFromIntentResponse,
    PersistedComposeSession,
)

logger = logging.getLogger(__name__)

COMPOSE_SESSIONS_DIR = Path(__file__).parent / "compose_sessions"


class ComposeSessionValidationError(ValueError):
    """Raised when a compose session payload is not self-consistent."""


def _build_session_id() -> str:
    return f"compose-session-{uuid4().hex[:12]}"


def save_compose_session(
    *,
    compose_request: ComposeFromIntentRequest,
    compose_response: ComposeFromIntentResponse,
    planning_decision_id: Optional[str] = None,
    source_v2_job_id: Optional[str] = None,
) -> PersistedComposeSession:
    """Persist one saved compose session and return its stored record."""

    _validate_compose_session_payload(
        compose_request=compose_request,
        compose_response=compose_response,
    )

    presentation = compose_response.presentation
    session = PersistedComposeSession(
        session_id=_build_session_id(),
        saved_at=datetime.now(timezone.utc).isoformat(),
        workflow_key=compose_request.workflow_key,
        consumer_key=compose_request.consumer_key,
        planning_decision_id=_normalize_optional_text(planning_decision_id),
        source_v2_job_id=_normalize_optional_text(source_v2_job_id),
        presentation_hash=presentation.presentation_hash.strip(),
        presentation_content_hash=presentation.presentation_content_hash.strip(),
        resolver_version=presentation.resolver_version.strip(),
        compose_request=compose_request,
        compose_response=compose_response,
    )
    COMPOSE_SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    session_path = COMPOSE_SESSIONS_DIR / f"{session.session_id}.json"
    session_path.write_text(session.model_dump_json(indent=2), encoding="utf-8")
    logger.info("Compose session saved to %s", session_path)
    return session


def load_compose_session(session_id: str) -> Optional[PersistedComposeSession]:
    """Load one persisted compose session by id."""

    normalized_id = session_id.strip()
    if not normalized_id:
        return None
    session_path = COMPOSE_SESSIONS_DIR / f"{normalized_id}.json"
    if not session_path.exists():
        return None
    return PersistedComposeSession.model_validate_json(
        session_path.read_text(encoding="utf-8")
    )


def _validate_compose_session_payload(
    *,
    compose_request: ComposeFromIntentRequest,
    compose_response: ComposeFromIntentResponse,
) -> None:
    presentation = compose_response.presentation
    if compose_request.workflow_key != presentation.workflow_key:
        raise ComposeSessionValidationError(
            "compose session save requires matching workflow_key between request and response"
        )
    if compose_request.consumer_key != presentation.consumer_key:
        raise ComposeSessionValidationError(
            "compose session save requires matching consumer_key between request and response"
        )
    if not presentation.presentation_hash.strip():
        raise ComposeSessionValidationError(
            "compose session save requires response.presentation.presentation_hash"
        )
    if not presentation.presentation_content_hash.strip():
        raise ComposeSessionValidationError(
            "compose session save requires response.presentation.presentation_content_hash"
        )
    if not presentation.resolver_version.strip():
        raise ComposeSessionValidationError(
            "compose session save requires response.presentation.resolver_version"
        )


def _normalize_optional_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None
