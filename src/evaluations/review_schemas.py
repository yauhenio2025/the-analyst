"""Schemas for persisted evaluation review/disposition decisions."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from src.evaluations.schemas import EvaluationOverallVerdict


ReviewDisposition = Literal["accept", "reject", "waive"]


class EvaluationReviewerIdentity(BaseModel):
    reviewer_name: str
    reviewer_role: str


class PersistedEvaluationReviewDecision(BaseModel):
    review_decision_id: str
    created_at: str
    review_key: str
    review_definition_version: str
    gate_decision_id: str
    gate_key: str
    gate_definition_version: str
    evaluation_pack_key: str
    reviewer_identity: EvaluationReviewerIdentity
    disposition: ReviewDisposition
    rationale: str
    observed_gate_verdict: EvaluationOverallVerdict
    contains_live_revalidation: bool = False
    observed_gate_blocking_reasons: list[str] = Field(default_factory=list)
    waiver_reasons: list[str] = Field(default_factory=list)


class EvaluationReviewDecisionSummary(BaseModel):
    review_decision_id: str
    created_at: str
    review_key: str
    review_definition_version: str
    gate_decision_id: str
    gate_key: str
    evaluation_pack_key: str
    disposition: ReviewDisposition
    observed_gate_verdict: EvaluationOverallVerdict
    contains_live_revalidation: bool = False


class EvaluationReviewDecisionListResponse(BaseModel):
    reviews: list[EvaluationReviewDecisionSummary] = Field(default_factory=list)
    count: int = 0
