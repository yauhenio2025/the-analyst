"""Story desk schemas: profiles, map, approaches, brief, spine, handoff, job."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, Field

from src.dossier.schemas import Anchor, Receipt, Totals

ELEMENT_KINDS = ("question", "face", "turn", "antagonism", "reveal", "motif", "filmable", "quotable", "number")
APPROACHES = ("helicopter_view", "one_scene_first", "the_case", "the_portrait", "the_timeline", "the_verdict",
              "open_question", "the_numbers", "the_correction", "the_object", "the_hindsight", "the_choice")
STEPS = ("reconnaissance", "map", "approaches", "brief", "spine", "handoff")
STATUS_FOR_STEP = {"reconnaissance": "reading", "map": "mapping", "approaches": "ranking", "brief": "briefing",
                   "spine": "spining", "handoff": "handing_off"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class StoryElement(BaseModel):
    """One anchored story element read from one source, typed by what the downstream passes asked for."""
    id: str = ""
    kind: str = Field(..., description="one of " + ", ".join(ELEMENT_KINDS))
    text: str = Field(..., description="the element in one or two sentences, <= 240 chars")
    detail: dict[str, str] = Field(default_factory=dict, description="kind-specific fields: face {name, stake, choice, public}; turn {value, before, after, turned_by}; reveal {assumed, true}; filmable {what, visual_form}; number {value, unit, of_what}; motif {object, could_pay_off_as}")
    anchor: Anchor
    intensity: int = Field(default=3, ge=1, le=5, description="1 background … 5 the strongest fact in the source")
    consumers: list[str] = Field(default_factory=list, description="engine keys whose demand this element answers")


class StoryProfile(BaseModel):
    doc_key: str
    title: str = ""
    genre: str = ""
    one_line: str = ""
    question: str = Field(default="", description="the question this source raises or answers")
    stance: str = Field(default="", description="what the source argues, and in what register")
    elements: list[StoryElement] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list, description="what this source cannot support")
    elements_dropped: int = 0


class Recurrence(BaseModel):
    what: str
    kind: str = ""
    doc_keys: list[str] = Field(default_factory=list)
    element_ids: list[str] = Field(default_factory=list)


class Position(BaseModel):
    doc_key: str
    says: str


class Contradiction(BaseModel):
    about: str
    positions: list[Position] = Field(default_factory=list)
    usable_as: str = Field(default="complication", description="antagonism | complication | none")


class TimelineEntry(BaseModel):
    when: str
    what: str
    doc_keys: list[str] = Field(default_factory=list)


class ValueTurn(BaseModel):
    value: str = ""
    before: str = ""
    after: str = ""
    turned_by: str = ""


class ThroughLine(BaseModel):
    key: str
    title: str
    question: str = Field(..., description="the one question the film holds open")
    face_on_the_stake: str = ""
    value_turn: ValueTurn = Field(default_factory=ValueTurn)
    antagonism: str = ""
    open_loop: str = ""
    verdict_possible: str = Field(default="", description="the verdict the material can actually support, or why none")
    carried_by: list[str] = Field(default_factory=list, description="doc_keys that carry this line")
    not_carried_by: list[str] = Field(default_factory=list)
    element_ids: list[str] = Field(default_factory=list)
    why: str = ""
    single_source: bool = False


class StoryMap(BaseModel):
    recurrences: list[Recurrence] = Field(default_factory=list)
    contradictions: list[Contradiction] = Field(default_factory=list)
    timeline: list[TimelineEntry] = Field(default_factory=list)
    through_lines: list[ThroughLine] = Field(default_factory=list)
    coverage: dict[str, dict[str, bool]] = Field(default_factory=dict, description="through_line key → doc_key → carried (computed)")


class ApproachRank(BaseModel):
    key: str
    rank: int = 0
    why: str = ""
    carried_by: list[str] = Field(default_factory=list)
    must_cut: str = ""


class ApproachSlate(BaseModel):
    ranked: list[ApproachRank] = Field(default_factory=list)
    note: str = ""


class StoryOption(BaseModel):
    key: str
    title: str
    viewer_will_understand: str = ""
    viewer_will_feel: str = ""
    viewer_will_be_able_to: str = ""
    length_seconds: int = 90
    through_line_key: str = ""
    approach_key: str = ""
    sources_used: list[str] = Field(default_factory=list)
    sources_left_out: list[str] = Field(default_factory=list)
    est_cost_usd: float = 0.0
    est_minutes: int = 0
    why: str = ""
    risks: list[str] = Field(default_factory=list)


class StoryBrief(BaseModel):
    options: list[StoryOption] = Field(default_factory=list)
    recommendation: str = ""
    why: str = ""


class Movement(BaseModel):
    n: int
    title: str
    job: str = Field(default="", description="what this movement does for the film")
    value_turn: ValueTurn = Field(default_factory=ValueTurn)
    sources: list[str] = Field(default_factory=list, description="doc_keys this movement draws on")
    element_ids: list[str] = Field(default_factory=list)
    entry_of: list[str] = Field(default_factory=list, description="doc_keys that enter the film here")
    narration_hint: str = ""


class Motif(BaseModel):
    what: str = ""
    plant_movement: int = 1
    payoff_movement: int = 1
    element_ids: list[str] = Field(default_factory=list)


class Hook(BaseModel):
    element_id: str = ""
    why: str = ""


class StorySpine(BaseModel):
    through_line_key: str
    approach_key: str = ""
    movements: list[Movement] = Field(default_factory=list)
    motif: Motif = Field(default_factory=Motif)
    hook: Hook = Field(default_factory=Hook)
    open_loop: str = ""
    colour_script: str = ""
    musical_arc: str = ""
    verdict: str = ""
    length_seconds: int = 90


class HandoffSource(BaseModel):
    doc_key: str
    title: str = ""
    creators: str = ""
    year: str = ""
    publication: str = ""
    chars: int = 0
    sha256: str = ""
    text_url: str = Field(default="", description="GET this on The Analyst API for the full text")


class StoryHandoff(BaseModel):
    """The contract between the story desk (The Analyst) and Wirecut."""
    version: str = "1.0"
    story_job_id: str
    created_at: str = Field(default_factory=_now)
    intent: str = ""
    audience: str = ""
    through_line: ThroughLine
    approach: Optional[ApproachRank] = None
    spine: StorySpine
    ledger: list[StoryElement] = Field(default_factory=list, description="every verified element of the sources the spine uses")
    sources: list[HandoffSource] = Field(default_factory=list)
    coverage: dict[str, bool] = Field(default_factory=dict, description="doc_key → carried by the chosen through-line")
    doctrines: dict[str, str] = Field(default_factory=dict, description="registry doctrine files used → sha256")
    totals: dict[str, Any] = Field(default_factory=dict)


class StoryOptions(BaseModel):
    intent: Optional[str] = None
    audience: str = "executive"
    preset: Optional[str] = None
    length_seconds: Optional[int] = None
    autopilot: bool = False
    from_job: Optional[str] = Field(default=None, description="reuse the documents of an existing dossier job")


class StoryJob(BaseModel):
    id: str = Field(default_factory=lambda: f"story-{uuid.uuid4().hex[:12]}")
    status: str = "queued"
    step: str = ""
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)
    sources: list[dict[str, Any]] = Field(default_factory=list)
    documents: list[dict[str, Any]] = Field(default_factory=list)
    options: StoryOptions = Field(default_factory=StoryOptions)
    profiles: list[StoryProfile] = Field(default_factory=list)
    map: Optional[StoryMap] = None
    approaches: Optional[ApproachSlate] = None
    brief: Optional[StoryBrief] = None
    chosen_option: Optional[str] = None
    spine: Optional[StorySpine] = None
    handoff: Optional[StoryHandoff] = None
    receipts: list[Receipt] = Field(default_factory=list)
    totals: Totals = Field(default_factory=Totals)
    error: Optional[str] = None
    notes: list[dict[str, Any]] = Field(default_factory=list)


class StoryJobSummary(BaseModel):
    id: str
    status: str
    step: str
    created_at: str
    updated_at: str
    n_documents: int = 0
    n_elements: int = 0
    intent: Optional[str] = None
    chosen_option: Optional[str] = None
    cost_usd: float = 0.0
