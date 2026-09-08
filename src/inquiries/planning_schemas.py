"""Portable planning inputs; metadata is a selection aid, never primary evidence."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, model_validator

from src.inquiries.schemas import (
    Commitment, Execution, Identifier, InquiryResult, StrictModel, Text, unique,
)


class PlanningContext(StrictModel):
    inquiry_id: Identifier
    revision: int = Field(ge=0)
    question: Text
    commitments: list[Commitment] = Field(default_factory=list, max_length=30)
    purpose: str = ""
    stage: str = ""
    author_responses: list[dict[str, Any]] = Field(default_factory=list)
    previous_result: dict[str, Any] | None = None
    requested_test_id: Identifier | None = None

    @model_validator(mode="after")
    def valid_context(self):
        unique([c.id for c in self.commitments], "commitment IDs")
        if self.previous_result is not None:
            previous = self.previous_result
            if isinstance(previous.get("evidence"), list):
                previous = {**previous, "evidence": [
                    {k: v for k, v in e.items() if k not in ("verified", "anchor_status")}
                    if isinstance(e, dict) else e for e in previous["evidence"]]}
            prior = InquiryResult.model_validate(previous)
            if self.requested_test_id and self.requested_test_id not in {t.id for t in prior.tests}:
                raise ValueError("Requested test must exist in previous_result")
        elif self.requested_test_id:
            raise ValueError("Requested test requires previous_result")
        return self


class TextWindow(StrictModel):
    id: Identifier
    chars: int = Field(ge=1)
    preview: str = Field(default="", max_length=12_000)
    locus: str = ""


class SourceCandidate(StrictModel):
    key: Identifier
    title: Text
    uid: str | None = None
    version: str | int | None = None
    authors: list[Text] = Field(default_factory=list)
    chars: int = Field(ge=0)
    readable: bool
    preview: str = Field(default="", max_length=12_000)
    coverage: str = ""
    windows: list[TextWindow] = Field(default_factory=list, max_length=100)

    @model_validator(mode="after")
    def valid_windows(self):
        unique([w.id for w in self.windows], "window IDs within source")
        if any(w.chars > self.chars for w in self.windows):
            raise ValueError("A window cannot exceed its source length")
        return self


class PriorReadingCandidate(StrictModel):
    id: Identifier
    job_id: Identifier
    phase: Identifier
    summary: str = ""
    source_keys: list[Identifier] = Field(default_factory=list)
    input_fingerprint: str | None = None
    rows: list[dict[str, Any]] = Field(default_factory=list)


class PlanningBudget(StrictModel):
    max_sources: int = Field(default=20, ge=1, le=40)
    max_chars: int = Field(default=400_000, ge=1, le=1_500_000)
    max_prior_readings: int = Field(default=8, ge=0, le=20)


class SelectedSource(StrictModel):
    source_key: Identifier
    window_ids: list[Identifier] = Field(default_factory=list, max_length=1)

    @model_validator(mode="after")
    def valid_ids(self):
        unique(self.window_ids, "selected window IDs")
        return self


class PlanningResult(StrictModel):
    phase: Literal["discovery", "selection"]
    status: Literal["ready", "blocked"]
    selected_commitment_ids: list[Identifier]
    selected_test_id: Identifier | None
    research_brief: Text
    rationale: Text
    evidence_requirements: list[Text] = Field(max_length=20)
    selected_sources: list[SelectedSource] = Field(max_length=40)
    selected_prior_reading_ids: list[Identifier] = Field(max_length=20)
    coverage: Text
    gaps: list[Text] = Field(max_length=30)

    @model_validator(mode="after")
    def valid_result(self):
        unique(self.selected_commitment_ids, "selected commitment IDs")
        unique([s.source_key for s in self.selected_sources], "selected source keys")
        unique(self.selected_prior_reading_ids, "selected prior-reading IDs")
        if self.status == "blocked" and not self.gaps:
            raise ValueError("Blocked preparation must state its gaps")
        if self.status == "ready" and not self.selected_commitment_ids:
            raise ValueError("Ready preparation requires a supplied commitment")
        if self.phase == "discovery" and (self.selected_sources or self.selected_prior_reading_ids):
            raise ValueError("Discovery selects the question and test before selecting evidence")
        if self.phase == "selection" and self.status == "ready" and not self.selected_sources:
            raise ValueError("Ready selection requires held evidence")
        return self


class PlanningPrepareRequest(StrictModel):
    method: Literal["inquiry_preparation"] = "inquiry_preparation"
    phase: Literal["discovery", "selection"]
    context: PlanningContext
    sources: list[SourceCandidate] = Field(default_factory=list, max_length=200)
    prior_readings: list[PriorReadingCandidate] = Field(default_factory=list, max_length=100)
    availability: dict[str, Any] = Field(default_factory=dict)
    budget: PlanningBudget = Field(default_factory=PlanningBudget)
    discovery_plan: PlanningResult | None = None

    @model_validator(mode="after")
    def valid_request(self):
        unique([s.key for s in self.sources], "source keys")
        unique([r.id for r in self.prior_readings], "prior-reading IDs")
        if self.phase == "selection":
            if self.discovery_plan is None or self.discovery_plan.phase != "discovery" or self.discovery_plan.status != "ready":
                raise ValueError("Selection requires a ready discovery plan")
            _validate_selection_context(self.context, self.discovery_plan)
        elif self.discovery_plan is not None:
            raise ValueError("Discovery cannot contain another discovery plan")
        return self


def _validate_selection_context(context: PlanningContext, result: PlanningResult) -> None:
    commitments = {c.id: c for c in context.commitments}
    if set(result.selected_commitment_ids) - commitments.keys():
        raise ValueError("Unknown commitment ID in planning result")
    if any(commitments[cid].approved is False for cid in result.selected_commitment_ids):
        raise ValueError("Planning cannot promote an unapproved commitment")
    if context.previous_result is not None:
        tests = {t["id"] for t in context.previous_result["tests"]}
        if result.selected_test_id is not None and result.selected_test_id not in tests:
            raise ValueError("Selected test must exist in previous_result")
        if result.status == "ready" and result.selected_test_id is None:
            raise ValueError("Ready retest preparation requires a selected prior test")
        if context.requested_test_id and result.selected_test_id not in (None, context.requested_test_id):
            raise ValueError("Planning must preserve the requested test")
    elif result.selected_test_id is not None:
        raise ValueError("Initial preparation cannot select a prior test")


class PlanningCompleteRequest(StrictModel):
    prepared_id: Identifier
    input_fingerprint: Text
    method_fingerprint: Text
    input: PlanningPrepareRequest
    result: PlanningResult
    execution: Execution
