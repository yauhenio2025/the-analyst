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

from pydantic import BaseModel, Field, model_validator

from src.sources.schemas import SourceSpec

STATUSES = (
    "queued", "reconnaissance", "awaiting_brief", "planning", "analysis", "spine",
    "tables", "figures", "composing", "crosscheck", "done", "failed", "cancelled",
)
# The concretization passes (communications/DESIGN_concretization_passes.md §C):
# spine (S) decides what the dossier argues before any exhibit exists; tables +
# figures (E) build exactly what the spine commissioned; compose (D) writes with
# the exhibits in hand and places them at the pointer; crosscheck (X) reads the
# finished parts as one dossier and mints findings.
STEPS = (
    "reconnaissance", "brief", "plan", "analysis", "spine", "tables", "figures",
    "compose", "crosscheck", "receipts",
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


# ── Brief v2: deliverable-first (communications/DESIGN_brief_deliverables.md §B) ──

DELIVERABLE_KINDS = ("stress_test", "decision_memo", "briefing", "playbook", "comparison",
                     "watchlist", "reading_guide", "decoder", "risk_register", "case_file")
USE_KINDS = ("decide", "brief", "prepare", "stress_test", "compare", "watch", "learn", "argue")
ENTRIES = ("use", "chosen", "material")
FIGURE_FORMATS = ("two_axis_grid", "timeline", "flow", "before_after", "map", "spectrum",
                  "stack", "network", "scene")
STEP_DEPTHS = ("surface", "standard", "deep")


class ShapeRef(BaseModel):
    """Pointer from a promise to the shape element that keeps it: S3 / T1 / F2 (1-based)."""
    kind: Literal["section", "table", "figure"]
    index: int = 1

    def label(self) -> str:
        return {"section": "§", "table": "T", "figure": "F"}[self.kind] + str(self.index)


class SectionSpec(BaseModel):
    heading: str = ""                 # <= 70
    answers: str = ""                 # the question this section answers, <= 120


class TableSpec(BaseModel):
    title: str = ""                   # <= 90
    row_unit: str = ""                # "one row per …", <= 60
    columns: list[str] = Field(default_factory=list)   # 3-5, each <= 30
    rows_expected: str = ""           # "8-10"
    carried_by: list[str] = Field(default_factory=list)  # doc_keys whose text fills the cells


class FigureSpec(BaseModel):
    title: str = ""                   # <= 90
    format: str = "scene"             # one of FIGURE_FORMATS
    scene: str = ""                   # depictable, no text in the image, <= 220


class Shape(BaseModel):
    sections: list[SectionSpec] = Field(default_factory=list)   # 3-6
    tables: list[TableSpec] = Field(default_factory=list)       # 1-3
    figures: list[FigureSpec] = Field(default_factory=list)     # 0-3


class Promise(BaseModel):
    text: str = ""                    # <= 140 (understand) / <= 120 (able_to, verb-first)
    supported_by: list[ShapeRef] = Field(default_factory=list)
    unsupported: bool = False         # set by the checks when no ref survived


class CarryingDoc(BaseModel):
    doc_key: str
    carries: str = ""


class EvidenceBase(BaseModel):
    carrying_docs: list[CarryingDoc] = Field(default_factory=list)
    thin_or_missing: list[str] = Field(default_factory=list)   # <= 140 each


class PathStep(BaseModel):
    engine_key: str
    plain_name: str = ""              # audience-register name, e.g. "hidden-obligations map"
    contributes: str = ""             # one line, reader terms, <= 120
    depth: str = "surface"            # one of STEP_DEPTHS


class Path(BaseModel):
    steps: list[PathStep] = Field(default_factory=list)   # 1-4, run order
    depth: str = "simple"             # one of DEPTHS (light / standard / full)
    primitives: list[str] = Field(default_factory=lambda: ["prose", "anchored_tables", "figures"])
    chain_key: Optional[str] = None   # when a recipe was chosen (lane 2)


class BriefOption(BaseModel):
    """A deliverable the requester could commission.

    v2 fields lead (deliverable, promises, shape, evidence, path). `telling`,
    `engines` and `output_shape` are DERIVED from them after validation so
    plan/tables/figures/compose keep reading what they always read; a stored
    v1 option (no `shape`) keeps its own values and version 1.
    """
    version: int = 1
    key: str
    title: str
    deliverable_kind: str = ""        # one of DELIVERABLE_KINDS
    deliverable: str = ""             # "a 5-section stress test with a claim-type scorecard", <= 110
    use_kind: str = ""                # one of USE_KINDS — the option's job-to-be-done
    you_will_understand: list[Promise] = Field(default_factory=list)   # exactly 3
    you_will_be_able_to: list[Promise] = Field(default_factory=list)   # 2-3
    questions_answered: list[str] = Field(default_factory=list)        # 3-4
    not_for: list[str] = Field(default_factory=list)                   # 1-3
    shape: Optional[Shape] = None
    evidence_base: EvidenceBase = Field(default_factory=EvidenceBase)
    path: Path = Field(default_factory=Path)
    best_when: str = ""               # <= 140, "Pick this when …"
    alternative: bool = False         # lane 2: the desk's alternative to the fixed path
    notes: list[str] = Field(default_factory=list)   # what the checks changed, for the record
    est_cost_usd: float = 0.0
    est_minutes: float = 0.0
    est_llm_calls: int = 0
    # ── derived back-compat views (v2) / stored values (v1)
    telling: str = ""
    engines: list[EngineChoice] = Field(default_factory=list)
    output_shape: OutputShape = Field(default_factory=OutputShape)

    @model_validator(mode="before")
    @classmethod
    def _coerce_shapes(cls, data: Any) -> Any:
        """Shape-only repair (the answer-repair law): a promise given as a bare string becomes {text, supported_by: []}
        (the refs check then sends it to the repair round instead of a whole re-ask); a doc key given as a bare string
        becomes {doc_key}; a section/table/figure given as a string becomes its heading/title."""
        if not isinstance(data, dict):
            return data
        for key in ("you_will_understand", "you_will_be_able_to"):
            v = data.get(key)
            if isinstance(v, list):
                data[key] = [{"text": p, "supported_by": []} if isinstance(p, str) else p for p in v]
        ev = data.get("evidence_base")
        if isinstance(ev, dict) and isinstance(ev.get("carrying_docs"), list):
            ev["carrying_docs"] = [{"doc_key": d, "carries": ""} if isinstance(d, str) else d for d in ev["carrying_docs"]]
        shape = data.get("shape")
        if isinstance(shape, dict):
            if isinstance(shape.get("sections"), list):
                shape["sections"] = [{"heading": s, "answers": ""} if isinstance(s, str) else s for s in shape["sections"]]
            if isinstance(shape.get("tables"), list):
                shape["tables"] = [{"title": t, "row_unit": ""} if isinstance(t, str) else t for t in shape["tables"]]
            if isinstance(shape.get("figures"), list):
                shape["figures"] = [{"title": f, "scene": f} if isinstance(f, str) else f for f in shape["figures"]]
        path = data.get("path")
        if isinstance(path, dict) and isinstance(path.get("steps"), list):
            path["steps"] = [{"engine_key": s} if isinstance(s, str) else s for s in path["steps"]]
        return data

    @model_validator(mode="after")
    def _derive_legacy_views(self) -> "BriefOption":
        if self.shape is None:
            return self
        self.version = 2
        understand = " ".join(p.text for p in self.you_will_understand if p.text)
        self.telling = (f"{self.deliverable.rstrip('.')}. {understand}".strip() if self.deliverable else understand) or self.title
        self.engines = [EngineChoice(engine_key=s.engine_key, why=s.contributes) for s in self.path.steps]
        self.output_shape = OutputShape(
            sections=[s.heading for s in self.shape.sections],
            tables=[f"{t.title} — {t.row_unit}" if t.row_unit else t.title for t in self.shape.tables],
            figures=[f"{f.title} ({f.format}): {f.scene}" for f in self.shape.figures],
        )
        return self

    def refs(self) -> list[str]:
        """Every promise reference as a label (T1, §5, F1) — for events and the desk."""
        out = []
        for p in self.you_will_understand + self.you_will_be_able_to:
            out.extend(r.label() for r in p.supported_by)
        return out


class Recommendation(BaseModel):
    option_key: str
    because: str = ""                 # reader-register, <= 220; names the corpus reason
    runner_up: Optional[str] = None
    runner_up_because: Optional[str] = None


class BriefDefaults(BaseModel):
    audience: str = "executive"
    depth: str = "simple"
    figures: int = 2


class Brief(BaseModel):
    version: int = 1
    entry: str = "use"                # one of ENTRIES
    options: list[BriefOption] = Field(default_factory=list)
    recommendation: Optional[Recommendation] = None
    defaults: BriefDefaults = Field(default_factory=BriefDefaults)
    notes: list[str] = Field(default_factory=list)

    def option(self, key: Optional[str]) -> Optional[BriefOption]:
        for o in self.options:
            if o.key == key:
                return o
        return None

    def autopilot_key(self) -> str:
        """What 'let the material decide' executes: the recommendation, else the first option."""
        if self.recommendation and self.option(self.recommendation.option_key):
            return self.recommendation.option_key
        return self.options[0].key if self.options else ""

    def autopilot_reason(self) -> str:
        key = self.autopilot_key()
        opt = self.option(key)
        title = opt.title if opt else key
        if self.recommendation and self.recommendation.option_key == key and self.recommendation.because:
            return f"the material decided: {title} — because {self.recommendation.because}"
        return f"autopilot: chose option 1 — {title} (no recommendation recorded)"


class UseFrame(BaseModel):
    """Lane 1: what the requester will use the dossier for."""
    use_kind: Optional[str] = None    # one of USE_KINDS or None
    occasion: Optional[str] = None
    who_reads: Optional[str] = None
    decision: Optional[str] = None


class PathStepRequest(BaseModel):
    engine_key: str
    depth: str = "surface"            # one of STEP_DEPTHS


class PathRequest(BaseModel):
    """Lane 2: the requester's own path (steps filled from `chain_key` when a recipe is named)."""
    steps: list[PathStepRequest] = Field(default_factory=list)
    chain_key: Optional[str] = None
    depth: Optional[str] = None       # one of DEPTHS; derived from the steps when absent


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
    # spine-driven exhibits (pass E): which section commissioned the table and what its rows prove
    section_key: str = ""
    proves: str = ""


# ── Step 6: figures ─────────────────────────────────────────────────────

class FigureAnchor(BaseModel):
    """What grounds a rendered label: a verbatim phrase from the analysis, a table or a profile."""
    label: str
    quote: str = Field("", description="Verbatim phrase (<= 200 chars) from the analysis prose, a table cell or a profile")
    source: str = Field("", description="analysis | table | profile | brief")
    verified: bool = False


class FigureSpec(BaseModel):
    """A labelled analytical diagram, fully specified before rendering.

    The spec is the boundary: whoever derives it (the figure planner today, the
    section spine tomorrow) hands it to the same prompt → render → check pipeline.
    """
    key: str
    primitive: str = Field("", description="one of the 12 analytical primitives (src/primitives)")
    visual_format: str = Field("", description="canonical format key from src/display/enforcement.py")
    title: str = Field("", description="<= 70 chars; rendered at the top of the diagram")
    data: dict[str, Any] = Field(default_factory=dict, description="labelled content in the format family's shape")
    caption: str = Field("", description="the analytic point, one sentence")
    why_this_format: str = ""
    style_school: str = ""
    anchors: list[FigureAnchor] = Field(default_factory=list)
    # legacy (pre-diagram) fields, kept so old job records still load
    scene: str = ""
    visual_register: str = "diagram"

    def labels(self) -> list[str]:
        from src.display.enforcement import collect_labels

        return collect_labels(self.data)


FigureBrief = FigureSpec  # old name, kept for callers of the pre-diagram contract


class Figure(FigureSpec):
    figure_id: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    prompt: Optional[str] = None
    aspect: Optional[str] = None
    cost_usd: float = 0.0
    status: Literal["planned", "generated", "skipped", "failed"] = "planned"
    note: str = ""
    compliance: Optional[dict[str, Any]] = None
    attempts: list[dict[str, Any]] = Field(default_factory=list)
    grounding: Optional[dict[str, Any]] = None
    # spine-driven exhibits (pass E): the commissioning section, the spec it was drawn from,
    # what the picture ACTUALLY shows (from the check) and whether the check passed
    section_key: str = ""
    picture_shows: str = ""
    caption_says: str = ""
    detected: str = ""
    checked_ok: Optional[bool] = None


# ── Step 7: compose ─────────────────────────────────────────────────────

class Claim(BaseModel):
    text: str
    anchor: Optional[Anchor] = None


class ExhibitRef(BaseModel):
    """The sentence that points the reader at an exhibit (\"As Table 2 shows …\"); `mismatch` when the
    writer says the picture does not show what the section argues (the cross-check acts on it)."""
    key: str
    sentence: str = ""
    mismatch: bool = False


class Section(BaseModel):
    number: int = 0
    heading: str
    paragraphs: list[str] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    table_keys: list[str] = Field(default_factory=list)
    figure_keys: list[str] = Field(default_factory=list)
    # pass D: the spine section this proves; paragraphs carry [[table:key]] / [[figure:key]] tokens
    section_key: str = ""
    exhibit_refs: list[ExhibitRef] = Field(default_factory=list)


class Sections(BaseModel):
    title: str = ""
    subtitle: str = ""
    executive_summary: list[str] = Field(default_factory=list)
    sections: list[Section] = Field(default_factory=list)
    conclusion: list[str] = Field(default_factory=list)
    claims_unanchored: int = 0
    # frames written LAST against the assembled body, each to the job the spine declared
    summary_job_met: str = ""
    conclusion_job_met: str = ""
    spine_round_consumed: int = 0



# ── Pass S: the spine (what the dossier argues; one claim per section; the exhibits each claim needs) ──

EVIDENCE_KINDS = ("case_comparison", "mechanism", "vocabulary", "cost_ledger", "chronology", "implication")


class ReaderProfile(BaseModel):
    type: str = ""                    # who reads it (from the audience register)
    mode: str = ""                    # reads straight through | consults the summary | scans one table …
    wants: str = ""                   # what they leave with


class Strand(BaseModel):
    name: str = ""
    carried_by: list[str] = Field(default_factory=list)   # analysis phases / documents / cases that carry it
    accidental: bool = False          # the same example used by two phases by chance
    note: str = ""


class CompositionRead(BaseModel):
    """de-llm's composition read (STUDY_de-llm_longform §D.1 pass 1), declared before the spine is planned."""
    plain_summary: str = ""           # what this dossier says, in at most four sentences
    buried_crux: str = ""             # what the analysis carries but never states plainly, and where it hides
    readers: list[ReaderProfile] = Field(default_factory=list)
    strands: list[Strand] = Field(default_factory=list)
    prose_to_table: list[str] = Field(default_factory=list)   # enumerations in the prose that a table shows better
    table_to_prose: list[str] = Field(default_factory=list)   # table ideas that are really one sentence
    figures_earned: list[str] = Field(default_factory=list)   # picture ideas that do a job prose cannot
    figures_dropped: list[str] = Field(default_factory=list)  # picture ideas that are decoration, and why
    cumulative_direction: str = ""    # which way the evidence pushes the reader, and whether that matches the brief
    form_capacity: str = ""           # does the material fill a dossier, or is it two sections and a table


class SpineTableSpec(BaseModel):
    intent: str = ""                  # what rows × columns would PROVE the claim
    row_unit: str = ""                # "one row = one case / one term / one actor"
    columns: list[str] = Field(default_factory=list)      # 2-6
    carries_claims: list[str] = Field(default_factory=list)  # the claims the rows must carry, in the reader's words


class SpineFigureSpec(BaseModel):
    primitive: str = ""               # one of the 12 analytical primitives (src/primitives)
    visual_format: str = ""           # canonical format key (src/display/enforcement)
    picture_shows: str = ""           # the structure a labelled diagram shows, in words
    caption_says: str = ""            # <= 2 sentences; what the reader takes from it; NO digits
    why_a_picture: str = ""           # why prose and tables cannot do this job


class SpineSection(BaseModel):
    key: str
    heading: str = ""
    claim: str = ""                   # ONE sentence this section proves
    reader_needs_next: str = ""       # what the reader needs after this claim (the throw-forward)
    evidence_kind: str = "mechanism"  # one of EVIDENCE_KINDS
    table: Optional[SpineTableSpec] = None
    figure: Optional[SpineFigureSpec] = None
    anchors_planned: list[Anchor] = Field(default_factory=list)   # verified quotes this section leans on
    feeds: list[str] = Field(default_factory=list)                # later section keys that build on this one


class ExhibitsBudget(BaseModel):
    tables: int = 0
    figures: int = 0


class DossierSpine(BaseModel):
    round: int = 1                    # +1 on every redirect (arithmetic)
    read: CompositionRead = Field(default_factory=CompositionRead)
    thesis: str = ""                  # ONE sentence — the dossier's claim
    reader_question: str = ""         # what this audience needs answered
    handle: str = ""                  # the dossier in one line a reader can repeat
    through_line: str = ""            # the object/example that returns
    summary_job: str = ""             # what the summary does
    conclusion_job: str = ""          # what the close does — a DIFFERENT job
    sections: list[SpineSection] = Field(default_factory=list)
    exhibits_budget: ExhibitsBudget = Field(default_factory=ExhibitsBudget)
    notes: list[str] = Field(default_factory=list)   # what the walls changed, for the record

    def section(self, key: str) -> Optional[SpineSection]:
        for s in self.sections:
            if s.key == key:
                return s
        return None

    def table_sections(self) -> list[SpineSection]:
        return [s for s in self.sections if s.table is not None]

    def figure_sections(self) -> list[SpineSection]:
        return [s for s in self.sections if s.figure is not None]


# ── Pass X: findings (the target ledger) ───────────────────────────────

FINDING_KINDS = (
    "figure_depicts_other", "caption_restates_text", "caption_carries_number",
    "table_rows_off_claim", "table_unreferenced", "exhibit_pointer_wrong",
    "claim_unbacked", "anchor_fragment", "anchor_off_claim", "number_drift",
    "section_off_spine", "redundant_summary_conclusion", "register_break",
    "jargon_unglossed", "exhibit_missing_where_claim_needs_one",
    # minted by code from the exhibit desks (pass E) — recorded facts, not impressions
    "table_unavailable", "table_rows_dropped", "figure_unavailable", "exhibit_unpointed",
)
AFFORDANCES = (
    "revise_figure_spec", "rerender_figure", "drop_figure",
    "rewrite_section", "rewrite_paragraph", "revise_table_rows", "add_table", "drop_table",
    "reanchor_claim", "drop_anchor", "rewrite_caption", "merge_summary_conclusion", "none",
)
FATES = ("resolved", "persists", "regressed", "superseded", "executed", "skipped", "failed")


class FindingWhere(BaseModel):
    section_key: Optional[str] = None
    table_key: Optional[str] = None
    figure_key: Optional[str] = None
    paragraph_index: Optional[int] = None
    anchor_n: Optional[int] = None


class Fate(BaseModel):
    round: int = 1
    fate: str = "persists"            # one of FATES
    rationale: str = ""
    by: str = "judge"                 # judge | code | operator
    ts: str = Field(default_factory=_now)


class Finding(BaseModel):
    id: str
    kind: str                         # one of FINDING_KINDS
    where: FindingWhere = Field(default_factory=FindingWhere)
    quote: str = ""                   # the offending words, verbatim from the page
    note: str = ""                    # effect on the reader, then the cure — plain language
    affordance: str = "none"          # one of AFFORDANCES
    realization: Optional[str] = None # the drafted change
    recommended: bool = True
    source: str = "judge"             # judge | clamp | wall  (clamps and walls outrank the judge)
    round: int = 1                    # cross-check round that minted it
    status: str = "open"              # open | resolved | superseded
    fates: list[Fate] = Field(default_factory=list)


class CrossCheckVerdict(BaseModel):
    round: int = 1
    hangs_together: Optional[bool] = None
    summary: str = ""
    findings_minted: int = 0
    clamps: int = 0
    judged: bool = False              # False when the judge was unavailable (clamps still ran)
    what_changed: Optional[str] = None
    realized: list[str] = Field(default_factory=list)   # finding ids the automatic round acted on
    ts: str = Field(default_factory=_now)

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
    autopilot: bool = False           # == (entry == "material"); kept so the runner's gate is untouched
    image_provider: Optional[str] = None
    # brief v2 lanes (DESIGN_brief_deliverables §C3)
    entry: str = "use"                # one of ENTRIES: use | chosen | material
    use_frame: Optional[UseFrame] = None
    path: Optional[PathRequest] = None  # lane 2 (or an edited "how" line): the fixed path the plan honours


class CreateDossierRequest(BaseModel):
    sources: list[SourceSpec]
    intent: Optional[str] = None
    audience: Optional[str] = None
    depth: Optional[str] = None
    output: Optional[OutputOptions] = None
    spend_cap_usd: Optional[float] = None
    autopilot: bool = False           # alias of entry = "material"
    image_provider: Optional[str] = None
    entry: Optional[str] = None       # use (default) | chosen | material
    use_frame: Optional[UseFrame] = None
    path: Optional[PathRequest] = None  # required when entry = "chosen"


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
    spine: Optional[DossierSpine] = None
    tables: list[Table] = Field(default_factory=list)
    figures: list[Figure] = Field(default_factory=list)
    sections: Optional[Sections] = None
    findings: list[Finding] = Field(default_factory=list)
    crosscheck: Optional[CrossCheckVerdict] = None
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
