"""Schemas for the advisory task-routing endpoint.

Stage 8 is intentionally advisory: the router chooses a downstream family
and returns the contract the host would need to satisfy, but it never
dispatches into execution or transient composition itself.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictBaseModel(BaseModel):
    """Base model that forbids undeclared fields for routing contracts."""

    model_config = ConfigDict(extra="forbid")


class SavedResultSourceHint(StrictBaseModel):
    """Metadata-only hint describing a saved-result launch context."""

    source_mode: Literal["saved_result"] = "saved_result"
    selected_source_thinker_id: Optional[str] = None
    selected_source_thinker_name: Optional[str] = None
    source_analysis_id: Optional[str] = None
    source_v2_job_id: Optional[str] = None


class RegisteredCorpusSourceHint(StrictBaseModel):
    """Metadata-only hint for a registered-corpus launch context."""

    source_mode: Literal["registered_corpus"] = "registered_corpus"
    consumer_key: str
    external_project_id: str
    target_external_doc_key: str
    prior_work_external_doc_keys_count: int = Field(ge=0)
    has_target_chapter_external_doc_keys: bool
    selected_source_thinker_id: Optional[str] = None
    selected_source_thinker_name: Optional[str] = None


class InlineDocumentsSourceHint(StrictBaseModel):
    """Metadata-only hint for an inline-documents launch context."""

    source_mode: Literal["inline_documents"] = "inline_documents"
    has_target_work_text: bool
    prior_work_count: int = Field(ge=0)
    has_target_work_chapters: bool
    selected_source_thinker_id: Optional[str] = None
    selected_source_thinker_name: Optional[str] = None


CompositionTaskSourceConstraints = Annotated[
    SavedResultSourceHint | RegisteredCorpusSourceHint | InlineDocumentsSourceHint,
    Field(discriminator="source_mode"),
]


RoutingOutcome = Literal[
    "aoi_transient_source_backed",
    "genealogy_transient_source_backed",
    "genealogy_job_backed",
    "unsupported",
]
RoutingConfidence = Literal["high", "medium", "low"]
LaunchContractKind = Literal[
    "planner.aoi_compose_handoff",
    "planner.direct_sections_compose_handoff",
    "presenter.compose_from_source",
    "orchestrator.analyze",
    "orchestrator.analyze_by_ref",
    "unsupported",
]
SourceSufficiencyStatus = Literal["sufficient", "insufficient", "ambiguous"]


class RoutingTraceEntry(StrictBaseModel):
    """One coarse trace entry for advisory routing."""

    stage: str
    details: dict[str, Any] = Field(default_factory=dict)


class RejectedRoutingCandidate(StrictBaseModel):
    """A bounded record explaining why a candidate objective was rejected."""

    objective_key: str
    rejection_reason: str
    details: list[str] = Field(default_factory=list)


class CompositionTaskRoutingDecision(StrictBaseModel):
    """Advisory routing outcome returned by POST /v1/orchestrator/route-task."""

    normalized_task_summary: str
    selected_objective_key: Optional[str] = None
    selected_workflow_key: Optional[str] = None
    routing_outcome: RoutingOutcome
    routing_confidence: RoutingConfidence
    launch_contract_kind: LaunchContractKind
    source_sufficiency_status: SourceSufficiencyStatus
    required_fields: list[str] = Field(default_factory=list)
    required_host_preparation: list[str] = Field(default_factory=list)
    downstream_launch_contract: dict[str, Any] = Field(default_factory=dict)
    rejected_candidates: list[RejectedRoutingCandidate] = Field(default_factory=list)
    trace: list[RoutingTraceEntry] = Field(default_factory=list)


class CompositionTaskRequest(StrictBaseModel):
    """Input for the advisory routing endpoint."""

    task: str
    objective_hint: Optional[str] = None
    audience: Optional[str] = None
    desired_depth: Optional[str] = None
    style_expectations: Optional[str] = None
    workflow_hint: Optional[str] = None
    consumer_key: Optional[str] = None
    source_constraints: Optional[CompositionTaskSourceConstraints] = None

    @field_validator("task")
    @classmethod
    def _validate_task(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if not normalized:
            raise ValueError("task must not be empty")
        return normalized
