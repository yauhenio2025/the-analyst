"""Schemas for persisted evaluation disposition resolutions."""

from __future__ import annotations

from pydantic import BaseModel, Field

from src.evaluations.review_schemas import ReviewDisposition
from src.evaluations.schemas import EvaluationOverallVerdict


class EvaluationResolverIdentity(BaseModel):
    resolver_name: str
    resolver_role: str


class PersistedEvaluationDispositionResolution(BaseModel):
    resolution_id: str
    resolution_key: str
    created_at: str
    resolution_definition_version: str
    review_decision_id: str
    review_key: str
    review_definition_version: str
    gate_decision_id: str
    gate_key: str
    gate_definition_version: str
    evaluation_pack_key: str
    resolver_identity: EvaluationResolverIdentity
    resolution_note: str
    adopted_review_disposition: ReviewDisposition
    observed_gate_verdict: EvaluationOverallVerdict
    contains_live_revalidation: bool = False


class EvaluationDispositionResolutionSummary(BaseModel):
    resolution_id: str
    resolution_key: str
    created_at: str
    resolution_definition_version: str
    review_decision_id: str
    review_key: str
    gate_decision_id: str
    gate_key: str
    evaluation_pack_key: str
    adopted_review_disposition: ReviewDisposition
    observed_gate_verdict: EvaluationOverallVerdict
    contains_live_revalidation: bool = False


class EvaluationDispositionResolutionListResponse(BaseModel):
    resolutions: list[EvaluationDispositionResolutionSummary] = Field(default_factory=list)
    count: int = 0


class EvaluationCurrentDispositionResolutionResponse(BaseModel):
    resolution_key: str
    gate_decision_id: str
    resolution: PersistedEvaluationDispositionResolution
