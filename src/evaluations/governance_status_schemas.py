"""Schemas for derived current governance-status responses."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from src.evaluations.resolution_schemas import PersistedEvaluationDispositionResolution


EffectiveGovernanceStatus = Literal["approved", "blocked", "exception_recorded"]


class EvaluationCurrentGovernanceStatusResponse(BaseModel):
    resolution_key: str
    gate_decision_id: str
    effective_governance_status: EffectiveGovernanceStatus
    scope_label: str
    resolution: PersistedEvaluationDispositionResolution
