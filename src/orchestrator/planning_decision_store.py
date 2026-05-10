"""File-backed persistence for immutable task-planning decisions."""

from __future__ import annotations

from datetime import datetime, timezone
import logging
from pathlib import Path
from typing import Optional
from uuid import uuid4

from src.orchestrator.task_planning_schemas import (
    PersistedTaskPlanningDecision,
    TaskPlanningDecision,
)
from src.orchestrator.task_routing_schemas import CompositionTaskRequest, CompositionTaskRoutingDecision

logger = logging.getLogger(__name__)

PLANNING_DECISIONS_DIR = Path(__file__).parent / "planning_decisions"


def _build_planning_decision_id() -> str:
    return f"planning-decision-{uuid4().hex[:12]}"


def save_task_planning_decision(
    *,
    task_request: CompositionTaskRequest,
    routing_decision: CompositionTaskRoutingDecision,
    planning_decision: TaskPlanningDecision,
) -> PersistedTaskPlanningDecision:
    """Persist one immutable planning snapshot and return its stored record."""

    planning_decision_id = _build_planning_decision_id()
    workflow_key, consumer_key, thinker_id, thinker_name, source_v2_job_id = _extract_snapshot_summary(
        task_request=task_request,
        routing_decision=routing_decision,
        planning_decision=planning_decision,
    )
    snapshot = PersistedTaskPlanningDecision(
        planning_decision_id=planning_decision_id,
        created_at=datetime.now(timezone.utc).isoformat(),
        workflow_key=workflow_key,
        consumer_key=consumer_key,
        selected_source_thinker_id=thinker_id,
        selected_source_thinker_name=thinker_name,
        source_v2_job_id=source_v2_job_id,
        task_request=task_request,
        routing_decision=routing_decision,
        planning_decision=planning_decision.model_copy(
            update={"planning_decision_id": planning_decision_id}
        ),
    )
    PLANNING_DECISIONS_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_path = PLANNING_DECISIONS_DIR / f"{planning_decision_id}.json"
    snapshot_path.write_text(snapshot.model_dump_json(indent=2), encoding="utf-8")
    logger.info("Planning decision saved to %s", snapshot_path)
    return snapshot


def _extract_snapshot_summary(
    *,
    task_request: CompositionTaskRequest,
    routing_decision: CompositionTaskRoutingDecision,
    planning_decision: TaskPlanningDecision,
) -> tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]:
    aoi_handoff = planning_decision.aoi_composition_handoff_plan
    if aoi_handoff is not None:
        return (
            aoi_handoff.workflow_key,
            aoi_handoff.consumer_key or task_request.consumer_key,
            aoi_handoff.selected_source_thinker_id,
            aoi_handoff.selected_source_thinker_name,
            aoi_handoff.source_v2_job_id,
        )

    direct_sections_handoff = planning_decision.direct_sections_composition_handoff_plan
    if direct_sections_handoff is not None:
        thinker_id, thinker_name, hinted_job_id = _extract_saved_result_source_identity(task_request)
        return (
            direct_sections_handoff.workflow_key,
            direct_sections_handoff.consumer_key or task_request.consumer_key,
            thinker_id,
            thinker_name,
            direct_sections_handoff.source_v2_job_id or hinted_job_id,
        )

    thinker_id, thinker_name, hinted_job_id = _extract_saved_result_source_identity(task_request)
    return (
        routing_decision.selected_workflow_key,
        task_request.consumer_key,
        thinker_id,
        thinker_name,
        hinted_job_id,
    )


def _extract_saved_result_source_identity(
    task_request: CompositionTaskRequest,
) -> tuple[Optional[str], Optional[str], Optional[str]]:
    source_constraints = task_request.source_constraints
    if source_constraints is None or source_constraints.source_mode != "saved_result":
        return None, None, None
    return (
        source_constraints.selected_source_thinker_id,
        source_constraints.selected_source_thinker_name,
        source_constraints.source_v2_job_id,
    )


def load_task_planning_decision(
    planning_decision_id: str,
) -> Optional[PersistedTaskPlanningDecision]:
    """Load one persisted planning snapshot by id."""

    snapshot_path = PLANNING_DECISIONS_DIR / f"{planning_decision_id}.json"
    if not snapshot_path.exists():
        return None
    return PersistedTaskPlanningDecision.model_validate_json(
        snapshot_path.read_text(encoding="utf-8")
    )
