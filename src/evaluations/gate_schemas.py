"""Schemas for persisted evaluation gate decisions."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from src.evaluations.schemas import EvaluationOverallVerdict


GateDimensionVerdict = Literal["pass", "fail", "error", "not_applicable", "missing"]


class GateVerdictPolicy(BaseModel):
    required_report_verdict: EvaluationOverallVerdict = "pass"
    missing_required_report_outcome: EvaluationOverallVerdict = "error"
    unexpected_input_case_outcome: EvaluationOverallVerdict = "error"
    report_error_outcome: EvaluationOverallVerdict = "error"
    report_fail_outcome: EvaluationOverallVerdict = "fail"
    missing_required_dimension_outcome: EvaluationOverallVerdict = "error"
    dimension_error_outcome: EvaluationOverallVerdict = "error"
    dimension_fail_outcome: EvaluationOverallVerdict = "fail"
    dimension_not_applicable_outcome: EvaluationOverallVerdict = "fail"


class EvaluationGateRequiredCase(BaseModel):
    case_key: str
    required_verdict: EvaluationOverallVerdict = "pass"
    required_dimensions: list[str] = Field(default_factory=list)


class EvaluationGateRuleTable(BaseModel):
    scope_label: str = "retrospective_frozen_pack_gate"
    required_cases: list[EvaluationGateRequiredCase] = Field(default_factory=list)
    verdict_policy: GateVerdictPolicy = Field(default_factory=GateVerdictPolicy)


class EvaluationGateCaseSummary(BaseModel):
    case_key: str
    evaluation_report_id: Optional[str] = None
    report_overall_verdict: Optional[EvaluationOverallVerdict] = None
    dimension_verdicts: dict[str, GateDimensionVerdict] = Field(default_factory=dict)
    case_verdict: EvaluationOverallVerdict = "error"
    contains_live_revalidation: bool = False
    subject_kind: Optional[str] = None
    subject_identity: Optional[str] = None
    workflow_key: Optional[str] = None
    consumer_key: Optional[str] = None
    blocking_reasons: list[str] = Field(default_factory=list)


class PersistedEvaluationGateDecision(BaseModel):
    gate_decision_id: str
    created_at: str
    gate_key: str
    gate_definition_version: str
    evaluation_pack_key: str
    input_report_ids_by_case_key: dict[str, str] = Field(default_factory=dict)
    contains_live_revalidation: bool = False
    rule_table: EvaluationGateRuleTable
    case_summaries: list[EvaluationGateCaseSummary] = Field(default_factory=list)
    overall_verdict: EvaluationOverallVerdict
    blocking_reasons: list[str] = Field(default_factory=list)


class EvaluationGateDecisionSummary(BaseModel):
    gate_decision_id: str
    created_at: str
    gate_key: str
    gate_definition_version: str
    evaluation_pack_key: str
    overall_verdict: EvaluationOverallVerdict
    contains_live_revalidation: bool = False


class EvaluationGateDecisionListResponse(BaseModel):
    gates: list[EvaluationGateDecisionSummary] = Field(default_factory=list)
    count: int = 0
