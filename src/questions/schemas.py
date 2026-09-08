"""Question development can begin with a problem and no settled commitments."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, model_validator

from src.inquiries.planning_schemas import PlanningBudget, PriorReadingCandidate, SelectedSource, SourceCandidate
from src.inquiries.schemas import Commitment, Evidence, Execution, Identifier, Source, StrictModel, Text, unique


class Assumption(StrictModel):
    text: Text
    status: Literal["author_stated", "inferred", "proposed"]
    commitment_ids: list[Identifier] = Field(default_factory=list)

    @model_validator(mode="after")
    def valid_assumption(self):
        unique(self.commitment_ids, "assumption commitment IDs")
        if self.status == "author_stated" and not self.commitment_ids:
            raise ValueError("An author-stated assumption requires a supplied commitment reference")
        return self


class Proposal(StrictModel):
    status: Literal["proposed"]
    question: Text
    motivation: Text
    change: Text
    assumptions: list[Assumption] = Field(max_length=20)
    enables: Text
    preserves: list[Text] = Field(max_length=20)
    retires: list[Text] = Field(max_length=20)


class QuestionOption(StrictModel):
    id: Identifier
    question: Text
    reason: Text


class NextActivity(StrictModel):
    kind: Literal["constructive_inquiry", "author_investigation", "exploration", "author_clarification", "pause"]
    question: Text
    reason: Text
    commitment_ids: list[Identifier] = Field(default_factory=list)

    @model_validator(mode="after")
    def valid_activity(self):
        unique(self.commitment_ids, "next-activity commitment IDs")
        if self.kind == "constructive_inquiry" and not self.commitment_ids:
            raise ValueError("Constructive inquiry requires supplied approved or explicit commitments")
        return self


class QuestionResult(StrictModel):
    summary: Text
    proposal: Proposal
    alternatives: list[QuestionOption] = Field(max_length=10)
    prerequisites: list[QuestionOption] = Field(max_length=10)
    evidence: list[Evidence] = Field(max_length=100)
    next_activity: NextActivity

    @model_validator(mode="after")
    def valid_ids(self):
        ids = ["proposal"]
        for name in ("alternatives", "prerequisites", "evidence"):
            ids.extend(r.id for r in getattr(self, name))
        unique(ids, "result IDs (proposal is reserved)")
        return self


class QuestionContext(StrictModel):
    question_id: Identifier
    revision: int = Field(ge=0)
    problem: Text
    current_question: Text | None = None
    motivation: str = ""
    commitments: list[Commitment] = Field(default_factory=list, max_length=30)
    prior_readings: list[dict[str, Any]] = Field(default_factory=list)
    previous_result: dict[str, Any] | None = None
    author_responses: list[dict[str, Any]] = Field(default_factory=list)
    origin_inquiry: dict[str, Any] | None = None
    preparation: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def valid_context(self):
        unique([c.id for c in self.commitments], "commitment IDs")
        if self.previous_result is not None:
            previous = self.previous_result
            if isinstance(previous.get("evidence"), list):
                previous = {**previous, "evidence": [
                    {k: v for k, v in row.items() if k not in ("verified", "anchor_status")}
                    if isinstance(row, dict) else row for row in previous["evidence"]]}
            QuestionResult.model_validate(previous)
        return self


class QuestionPlan(StrictModel):
    phase: Literal["discovery", "selection"]
    status: Literal["ready", "blocked"]
    needs_sources: bool
    research_brief: Text
    rationale: Text
    evidence_requirements: list[Text] = Field(max_length=20)
    selected_sources: list[SelectedSource] = Field(max_length=40)
    selected_prior_reading_ids: list[Identifier] = Field(max_length=20)
    coverage: Text
    gaps: list[Text] = Field(max_length=30)

    @model_validator(mode="after")
    def valid_plan(self):
        unique([s.source_key for s in self.selected_sources], "selected source keys")
        unique(self.selected_prior_reading_ids, "selected prior-reading IDs")
        if self.status == "blocked" and not self.gaps:
            raise ValueError("A blocked preparation must state its gap")
        if self.phase == "discovery" and (self.selected_sources or self.selected_prior_reading_ids):
            raise ValueError("Discovery states evidence needs before selecting evidence")
        if not self.needs_sources and self.selected_sources:
            raise ValueError("Conceptual-only preparation cannot select primary sources")
        if self.phase == "selection" and self.status == "ready" and self.needs_sources and not self.selected_sources:
            raise ValueError("Ready source selection requires readable evidence")
        return self


class PrepareRequest(StrictModel):
    method: Literal["question_preparation", "question_development"]
    phase: Literal["discovery", "selection", "development"]
    context: QuestionContext
    sources: list[Source] = Field(default_factory=list, max_length=40)
    candidates: list[SourceCandidate] = Field(default_factory=list, max_length=200)
    prior_readings: list[PriorReadingCandidate] = Field(default_factory=list, max_length=100)
    discovery_plan: QuestionPlan | None = None
    availability: dict[str, Any] = Field(default_factory=dict)
    budget: PlanningBudget = Field(default_factory=PlanningBudget)

    @model_validator(mode="after")
    def valid_phase(self):
        unique([s.key for s in self.sources], "primary source keys")
        unique([s.key for s in self.candidates], "candidate keys")
        unique([r.id for r in self.prior_readings], "prior-reading IDs")
        if self.phase == "development":
            if self.method != "question_development":
                raise ValueError("Development requires the question_development method")
            if self.candidates or self.prior_readings:
                raise ValueError("Development receives primary sources and hydrated context, not selection candidates")
            if len(self.sources) > self.budget.max_sources or sum(len(s.text) for s in self.sources) > self.budget.max_chars:
                raise ValueError("Primary sources exceed the declared development budget")
        else:
            if self.method != "question_preparation":
                raise ValueError("Discovery and selection require question_preparation")
            if self.sources:
                raise ValueError("Preparation receives metadata; primary source reading belongs to development")
        if self.discovery_plan is not None and (self.discovery_plan.phase != "discovery" or self.discovery_plan.status != "ready"):
            raise ValueError("A supplied discovery plan must be a ready discovery result")
        if self.phase == "discovery" and self.discovery_plan is not None:
            raise ValueError("Discovery cannot include a prior discovery plan")
        if self.phase == "selection" and (self.discovery_plan is None or not self.discovery_plan.needs_sources):
            raise ValueError("Selection requires a discovery plan that needs primary sources")
        if self.phase == "development" and self.discovery_plan is not None:
            if self.discovery_plan.needs_sources != bool(self.sources):
                raise ValueError("Development evidence must respect the discovery plan's source requirement")
        return self


class CompleteRequest(StrictModel):
    prepared_id: Identifier
    input_fingerprint: Text
    method_fingerprint: Text
    input: PrepareRequest
    result: QuestionPlan | QuestionResult
    execution: Execution

    @model_validator(mode="after")
    def valid_result_phase(self):
        if isinstance(self.result, QuestionResult) != (self.input.phase == "development"):
            raise ValueError("The result must match the prepared phase")
        return self
