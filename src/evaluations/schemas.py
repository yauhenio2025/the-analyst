"""Schemas for persisted governance/evaluation reports."""

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


EvaluationCheckStatus = Literal["pass", "fail", "error", "not_applicable"]
EvaluationOverallVerdict = Literal["pass", "fail", "error"]
EvaluationEvidenceMode = Literal[
    "inspection_route",
    "stored_object",
    "executor_read_contract",
    "frozen_artifact",
]


class EvaluationEvidenceRef(BaseModel):
    ref_key: str
    source_kind: str
    locator: str
    expected_sha256: Optional[str] = None
    observed_sha256: Optional[str] = None
    note: Optional[str] = None


class EvaluationCheck(BaseModel):
    check_key: str
    label: str
    status: EvaluationCheckStatus
    required: bool = True
    summary: str = ""
    evidence_mode: EvaluationEvidenceMode
    evidence_observed_at: str = ""
    live_revalidation_performed: bool = False
    evidence_refs: list[EvaluationEvidenceRef] = Field(default_factory=list)
    observed_values: dict[str, Any] = Field(default_factory=dict)


class EvaluationDimensionSummary(BaseModel):
    dimension_key: str
    status: EvaluationCheckStatus
    summary: str = ""
    supporting_checks: list[str] = Field(default_factory=list)


class PersistedEvaluationReport(BaseModel):
    evaluation_report_id: str
    created_at: str
    evaluation_pack_key: str
    case_key: str
    subject_kind: str
    subject_identity: str
    workflow_key: str
    consumer_key: Optional[str] = None
    supporting_subjects: dict[str, str] = Field(default_factory=dict)
    input_evidence_refs: list[EvaluationEvidenceRef] = Field(default_factory=list)
    checks: list[EvaluationCheck] = Field(default_factory=list)
    dimension_summaries: list[EvaluationDimensionSummary] = Field(default_factory=list)
    overall_verdict: EvaluationOverallVerdict


class EvaluationReportSummary(BaseModel):
    evaluation_report_id: str
    created_at: str
    evaluation_pack_key: str
    case_key: str
    subject_kind: str
    subject_identity: str
    workflow_key: str
    consumer_key: Optional[str] = None
    overall_verdict: EvaluationOverallVerdict


class EvaluationReportListResponse(BaseModel):
    reports: list[EvaluationReportSummary] = Field(default_factory=list)
    count: int = 0
