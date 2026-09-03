"""Dossier schemas — the meaning-making workflow's data (see communications/IMPLEMENTATION_TRACKER.md §2).

Every artifact the eight steps produce is a Pydantic model here, so the store,
the API and the composer speak one vocabulary. Anchors are verbatim quotes tied
to a document key; the walls (walls.py) refuse anchors that do not appear in
the source text.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from src.sources.schemas import SourceSpec

STATUSES = (
    "queued", "reconnaissance", "awaiting_brief", "planning", "analysis",
    "tables", "figures", "composing", "done", "failed", "cancelled",
)
STEPS = (
    "reconnaissance", "brief", "plan", "analysis", "tables", "figures",
    "compose", "receipts",
)
AUDIENCES = ("executive", "researcher", "analyst")
DEPTHS = ("simple", "medium", "advanced")


def _now() -> str:
    return datetime.utcnow().isoformat()


# ── Anchors ─────────────────────────────────────────────────────────────

class Anchor(BaseModel):
    doc_key: str
    quote: str = Field(..., description="Verbatim quote from the document, <= 200 chars")
    verified: bool = False
    trimmed: bool = False


# ── Step 1: reconnaissance ──────────────────────────────────────────────

class KeyClaim(BaseModel):
    claim: str
    anchor: Anchor


class DocumentProfile(BaseModel):
    doc_key: str
    title: str = ""
    genre: str = ""
    one_line: str = ""
    thesis: str = ""
    method: str = ""
    key_claims: list[KeyClaim] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    tensions: list[str] = Field(default_factory=list)
    claims_dropped: int = 0


class CorpusMap(BaseModel):
    shared_questions: list[str] = Field(default_factory=list)
    disagreements: list[str] = Field(default_factory=list)
    throughlines: list[str] = Field(default_factory=list)
    candidate_angles: list[str] = Field(default_factory=list)


class Reconnaissance(BaseModel):
    profiles: list[DocumentProfile] = Field(default_factory=list)
    corpus_map: CorpusMap = Field(default_factory=CorpusMap)


# ── Step 2: brief ───────────────────────────────────────────────────────

class EngineChoice(BaseModel):
    engine_key: str
    why: str = ""


class OutputShape(BaseModel):
    sections: list[str] = Field(default_factory=list)
    tables: list[str] = Field(default_factory=list)
    figures: list[str] = Field(default_factory=list)


class BriefOption(BaseModel):
    key: str
    title: str
    telling: str = Field(..., description="One paragraph: the angle, what the reader learns")
    engines: list[EngineChoice] = Field(default_factory=list)
    est_cost_usd: float = 0.0
    est_minutes: float = 0.0
    est_llm_calls: int = 0
    output_shape: OutputShape = Field(default_factory=OutputShape)


class BriefDefaults(BaseModel):
    audience: str = "executive"
    depth: str = "simple"
    figures: int = 2


class Brief(BaseModel):
    options: list[BriefOption] = Field(default_factory=list)
    defaults: BriefDefaults = Field(default_factory=BriefDefaults)


# ── Step 3: plan ────────────────────────────────────────────────────────

class DossierPlanPhase(BaseModel):
    phase_number: float
    engine_key: str
    engine_name: str = ""
    depth: str = "surface"
    passes: int = 1
    why: str = ""
    context_emphasis: str = ""


class DossierPlan(BaseModel):
    plan_id: Optional[str] = None
    phases: list[DossierPlanPhase] = Field(default_factory=list)
    strategy_rationale: str = ""
    alternatives_considered: list[dict[str, str]] = Field(default_factory=list)
    estimated_llm_calls: int = 0
    estimated_cost_usd: float = 0.0


# ── Step 5: tables ──────────────────────────────────────────────────────

class Cell(BaseModel):
    value: str = ""
    anchor: Optional[Anchor] = None


class Row(BaseModel):
    cells: list[Cell] = Field(default_factory=list)


class Table(BaseModel):
    key: str
    caption: str
    columns: list[str] = Field(default_factory=list)
    rows: list[Row] = Field(default_factory=list)
    note: str = ""
    rows_dropped: int = 0


# ── Step 6: figures ─────────────────────────────────────────────────────

class FigureBrief(BaseModel):
    key: str
    caption: str
    scene: str = Field(..., description="A depictable scene, no text in the image")
    visual_register: str = "editorial"


class Figure(FigureBrief):
    figure_id: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None
    provider: Optional[str] = None
    prompt: Optional[str] = None
    cost_usd: float = 0.0
    status: Literal["planned", "generated", "skipped", "failed"] = "planned"
    note: str = ""
    compliance: Optional[dict[str, Any]] = None


# ── Step 7: compose ─────────────────────────────────────────────────────

class Claim(BaseModel):
    text: str
    anchor: Optional[Anchor] = None


class Section(BaseModel):
    number: int = 0
    heading: str
    paragraphs: list[str] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    table_keys: list[str] = Field(default_factory=list)
    figure_keys: list[str] = Field(default_factory=list)


class Sections(BaseModel):
    title: str = ""
    subtitle: str = ""
    executive_summary: list[str] = Field(default_factory=list)
    sections: list[Section] = Field(default_factory=list)
    conclusion: list[str] = Field(default_factory=list)
    claims_unanchored: int = 0


# ── Step 8: receipts ────────────────────────────────────────────────────

class Receipt(BaseModel):
    step: str
    kind: Literal["llm", "image"] = "llm"
    model: str = ""
    label: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    duration_ms: int = 0
    prompt_hash: str = ""
    result_hash: str = ""
    ts: str = Field(default_factory=_now)
    source_job_id: Optional[str] = None


class Totals(BaseModel):
    llm_calls: int = 0
    image_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    duration_ms: int = 0
    step_durations_ms: dict[str, int] = Field(default_factory=dict)
    step_costs_usd: dict[str, float] = Field(default_factory=dict)


# ── Job ─────────────────────────────────────────────────────────────────

class OutputOptions(BaseModel):
    text: bool = True
    tables: bool = True
    figures: int = 2
    video: bool = False


class DossierOptions(BaseModel):
    intent: Optional[str] = None
    audience: str = "executive"
    depth: str = "simple"
    output: OutputOptions = Field(default_factory=OutputOptions)
    spend_cap_usd: Optional[float] = None
    autopilot: bool = False
    image_provider: Optional[str] = None


class CreateDossierRequest(BaseModel):
    sources: list[SourceSpec]
    intent: Optional[str] = None
    audience: Optional[str] = None
    depth: Optional[str] = None
    output: Optional[OutputOptions] = None
    spend_cap_usd: Optional[float] = None
    autopilot: bool = False
    image_provider: Optional[str] = None


class BriefChoiceRequest(BaseModel):
    option_key: str
    overrides: Optional[dict[str, Any]] = None


class DossierJob(BaseModel):
    id: str = Field(default_factory=lambda: f"dossier-{uuid.uuid4().hex[:12]}")
    status: str = "queued"
    step: str = ""
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)
    sources: list[dict[str, Any]] = Field(default_factory=list)
    documents: list[dict[str, Any]] = Field(default_factory=list, description="Resolved documents (metadata only)")
    options: DossierOptions = Field(default_factory=DossierOptions)
    profiles: Optional[Reconnaissance] = None
    brief: Optional[Brief] = None
    chosen_option: Optional[str] = None
    plan_id: Optional[str] = None
    plan: Optional[DossierPlan] = None
    analysis_job_id: Optional[str] = None
    analysis: dict[str, Any] = Field(default_factory=dict, description="phase -> prose + pass metadata")
    tables: list[Table] = Field(default_factory=list)
    figures: list[Figure] = Field(default_factory=list)
    sections: Optional[Sections] = None
    receipts: list[Receipt] = Field(default_factory=list)
    totals: Totals = Field(default_factory=Totals)
    error: Optional[str] = None
    paths: dict[str, str] = Field(default_factory=dict)
    notes: list[dict[str, Any]] = Field(default_factory=list)


class DossierJobSummary(BaseModel):
    id: str
    status: str
    step: str
    created_at: str
    updated_at: str
    title: str = ""
    intent: Optional[str] = None
    audience: str = "executive"
    depth: str = "simple"
    document_count: int = 0
    chosen_option: Optional[str] = None
    cost_usd: float = 0.0
    error: Optional[str] = None
