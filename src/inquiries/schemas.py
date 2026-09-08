"""The small, source-bound handoff between a method and an application's worker."""
from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, StringConstraints, model_validator

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Identifier = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=180)]
Method = Literal["constructive_inquiry", "constructive_retest"]


def nonblank(value: str) -> str:
    if not value.strip():
        raise ValueError("Text must not be blank")
    return value


FrozenText = Annotated[str, AfterValidator(nonblank)]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Commitment(StrictModel):
    id: Identifier
    text: FrozenText
    part_id: int | None = None
    version_id: int | None = None
    position: int | None = None
    approved: bool | None = None
    source_ref: str | dict[str, Any] | None = None
    version: str | int | None = None


class Source(StrictModel):
    key: Identifier
    title: Text
    text: FrozenText
    uid: str | None = None
    version: str | int | None = None
    authors: list[Text] = Field(default_factory=list)


class TestProposal(StrictModel):
    id: Identifier
    question: Text
    procedure: Text
    discriminates: Text
    evidence_needed: Text
    source_keys: list[Identifier]


class Context(StrictModel):
    inquiry_id: Identifier
    revision: int = Field(ge=0)
    question: Text
    commitments: list[Commitment] = Field(min_length=1, max_length=30)
    purpose: str = ""
    stage: str = ""
    desired_next_step: str = ""
    prior_readings: list[dict[str, Any]] = Field(default_factory=list)
    previous_result: dict[str, Any] | None = None
    test: TestProposal | None = None
    author_responses: list[dict[str, Any]] = Field(default_factory=list)
    preparation: dict[str, Any] = Field(default_factory=dict)


def unique(values: list[str], label: str) -> None:
    if len(values) != len(set(values)):
        raise ValueError(f"Duplicate {label}")


class PrepareRequest(StrictModel):
    method: Method
    context: Context
    sources: list[Source] = Field(min_length=1, max_length=40)

    @model_validator(mode="after")
    def valid_input(self):
        unique([c.id for c in self.context.commitments], "commitment IDs")
        unique([s.key for s in self.sources], "source keys")
        if sum(len(s.text) for s in self.sources) > 1_500_000:
            raise ValueError("Selected sources exceed 1,500,000 characters")
        if self.method == "constructive_retest":
            if not self.context.previous_result or not self.context.test:
                raise ValueError("Retest requires previous_result and selected test")
            previous = self.context.previous_result
            # Stored results include code-owned quote flags; strip those for shape
            # validation, while retaining the original supplied context snapshot.
            if isinstance(previous.get("evidence"), list):
                previous = {**previous, "evidence": [
                    {k: v for k, v in e.items() if k not in ("verified", "anchor_status")} if isinstance(e, dict) else e
                    for e in previous["evidence"]]}
            prior = InquiryResult.model_validate(previous)
            selected = [t.model_dump() for t in prior.tests if t.id == self.context.test.id]
            if len(selected) != 1 or selected[0] != self.context.test.model_dump():
                raise ValueError("Selected test must match exactly one test in previous_result")
        elif self.context.test is not None or self.context.previous_result is not None:
            raise ValueError("Initial inquiry cannot contain a prior result or selected test")
        return self


class ProposedAccount(StrictModel):
    status: Literal["proposed"]
    text: Text
    derivation: Text
    mechanism: Text
    scope: Text
    commitment_ids: list[Identifier] = Field(min_length=1)
    evidence_ids: list[Identifier]


class Evidence(StrictModel):
    id: Identifier
    source_key: Identifier
    quote: Text
    claim: Text
    role: Literal["supports", "challenges", "mechanism", "distinction", "context"]
    locus: str = ""


class Question(StrictModel):
    id: Identifier
    question: Text
    why: Text


class Revision(StrictModel):
    id: Identifier
    level: Literal["local", "broader"]
    commitment_id: Identifier | None
    before: str = ""
    after: Text
    reason: Text
    evidence_ids: list[Identifier]


class TestOutcome(StrictModel):
    test_id: Identifier
    status: Literal["strengthened", "weakened", "revised", "inconclusive", "failed"]
    explanation: Text
    evidence_ids: list[Identifier]


class InquiryResult(StrictModel):
    summary: Text
    proposed_account: ProposedAccount
    evidence: list[Evidence] = Field(max_length=100)
    new_questions: list[Question] = Field(max_length=20)
    tests: list[TestProposal] = Field(max_length=20)
    revisions: list[Revision] = Field(max_length=30)
    self_scrutiny: Text
    test_outcome: TestOutcome | None

    @model_validator(mode="after")
    def valid_ids(self):
        for name in ("evidence", "new_questions", "tests", "revisions"):
            unique([entry.id for entry in getattr(self, name)], f"{name} IDs")
        evidence_ids = {e.id for e in self.evidence}
        if "proposed_account" in evidence_ids:
            raise ValueError("Evidence ID proposed_account is reserved for the construction row")
        for item in [self.proposed_account, *self.revisions, *([self.test_outcome] if self.test_outcome else [])]:
            if set(item.evidence_ids) - evidence_ids:
                raise ValueError("Unknown evidence ID in result")
        return self


class Execution(StrictModel):
    provider: Text
    model: str = ""
    job_id: str = ""
    cost_usd: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    seconds: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    list_price_usd: float | None = Field(default=None, ge=0, allow_inf_nan=False)


class CompleteRequest(StrictModel):
    prepared_id: Identifier
    input_fingerprint: Text
    method_fingerprint: Text
    input: PrepareRequest
    result: InquiryResult
    execution: Execution


class Feedback(StrictModel):
    feedback_id: Identifier
    text: Text
    decision: str | None = None
    revision_id: str | None = None
