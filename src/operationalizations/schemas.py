"""Operationalization schemas — the bridge between stances and engines.

Stances are abstract cognitive postures (discovery, confrontation, etc.).
Engines define analytical dimensions and capabilities.
Operationalizations specify HOW each stance applies to each engine:
what label it gets, what prose description guides the LLM, and which
dimensions/capabilities it focuses on.

This is the third layer in the three-layer architecture:
  Stances (HOW to think) × Engines (WHAT to think about) → Operationalizations (the bridge)
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class StanceOperationalization(BaseModel):
    """How a specific analytical stance applies to a specific engine.

    This is the core unit of the operationalization layer. It captures
    the engine-specific meaning of an abstract stance — the prose that
    tells the LLM exactly what 'discovery' or 'confrontation' means
    when applied to THIS engine's dimensions and capabilities.
    """

    stance_key: str = Field(
        ...,
        description="Key of the analytical stance (references stances.yaml)",
        examples=["discovery", "confrontation", "dialectical"],
    )
    label: str = Field(
        ...,
        description="Engine-specific label for this stance application "
        "(e.g., 'Commitment Discovery' for discovery + inferential_commitment_mapper)",
    )
    description: str = Field(
        ...,
        description="Engine-specific prose describing what this stance does for this engine. "
        "This is the operationalization — injected into the prompt alongside the stance.",
    )
    focus_dimensions: list[str] = Field(
        default_factory=list,
        description="Dimension keys this stance focuses on (subset of engine's dimensions)",
    )
    focus_capabilities: list[str] = Field(
        default_factory=list,
        description="Capability keys this stance exercises (subset of engine's capabilities)",
    )


class DepthPassEntry(BaseModel):
    """A single pass in a depth-level sequence.

    References a stance operationalization by key and defines data flow
    between passes via consumes_from.
    """

    pass_number: int = Field(
        ...,
        description="1-indexed pass number within this depth level",
    )
    stance_key: str = Field(
        ...,
        description="Key of the analytical stance for this pass "
        "(must have a matching StanceOperationalization)",
    )
    consumes_from: list[int] = Field(
        default_factory=list,
        description="Pass numbers whose prose output feeds into this pass as context",
    )


class DepthSequence(BaseModel):
    """The pass ordering for a specific depth level of an engine.

    Defines which stances appear in what order at surface/standard/deep.
    """

    depth_key: str = Field(
        ...,
        description="Depth level key",
        examples=["surface", "standard", "deep"],
    )
    passes: list[DepthPassEntry] = Field(
        default_factory=list,
        description="Ordered list of passes for this depth level",
    )
    process: Optional[str] = Field(
        default=None,
        description="Key of the engine's process (see ProcessSpec) that runs at this depth instead of "
        "stance passes. When set, `passes` is ignored. Study 2026-09-04: extract → verify → synthesize.",
    )


# ── The process shape (study 2026-09-04): extract → verify → synthesize ──────────────
#
# A process is the engine's method expressed as three kinds of work with the findings
# ledger as the only hand-off: cheap models read the text per dimension and return
# anchored rows; a critic checks every row against the source and hunts for misses;
# one strong model writes the reading from the verified ledger. Each step routes to a
# model tier. Nothing here replaces stance passes: an operationalization may carry
# both, and a depth sequence chooses which runs.


class ProcessDimension(BaseModel):
    """One text-facing question set the extraction step answers with anchored rows."""

    key: str = Field(..., description="snake_case key, used as the id prefix of its rows (D1.F3 → prefix 'D1')")
    name: str = Field(..., description="Human name of the dimension")
    id_prefix: str = Field("", description="Short prefix for row ids (defaults to the key upper-cased)")
    scope: Literal["document", "corpus"] = Field(
        "document", description="corpus dimensions run only when two or more documents are present, over the per-document ledgers"
    )
    questions: list[str] = Field(default_factory=list, description="Questions about the TEXT (never about the authors)")
    answer_shape: str = Field("", description="The row shape an anchored answer takes")
    method_card: str = Field("", description="What the lineage makes the model DO here: imperatives, not names")
    indicators: list[str] = Field(default_factory=list, description="Textual signals to hunt for")
    load_bearing: bool = Field(False, description="Runs at surface depth (the three or four dimensions a short reading needs)")


class ProcessStep(BaseModel):
    """One step of the process, routed to a model tier."""

    key: str
    kind: Literal["extract", "verify", "synthesize"]
    parallel_over: Literal["dimension", "document", "dimension_x_document", "none"] = "none"
    model_tier: Literal["cheap", "mid", "strong"] = "strong"
    model: Optional[str] = Field(None, description="Explicit model id for this step; beats the routing table")
    consumes: list[str] = Field(default_factory=list, description="Keys of earlier steps whose ledgers this step reads")
    output: Literal["ledger", "prose_ledger"] = "ledger"
    duties: list[str] = Field(
        default_factory=list,
        description="Verify-step duties in order, e.g. check_anchors_in_context, reject_biography, reconcile_ids, "
        "merge_duplicates, rerun_critical_questions, hunt_misses, name_must_keep",
    )
    brief: str = Field("", description="Synthesize step: the reading a reader needs, in order")
    reader: str = Field("", description="Synthesize step: who the reading is for")
    tables: list[str] = Field(default_factory=list, description="Synthesize step: the tables the desks can lift, named")
    is_final: bool = False
    max_rows: int = Field(20, description="Extraction: rows per dimension call")


class ProcessSpec(BaseModel):
    """The engine's method as a routed process the registry holds."""

    key: str = Field("dvs", description="Process key referenced by DepthSequence.process")
    description: str = ""
    dimensions: list[ProcessDimension] = Field(default_factory=list)
    steps: list[ProcessStep] = Field(default_factory=list)
    routing: dict[str, str] = Field(
        default_factory=dict,
        description="model tier → model id (cheap / mid / strong). Overridable per call, by env PROCESS_ROUTING_<TIER>, and by the plan's model_hint (strong tier).",
    )

    def get_step(self, key: str) -> Optional["ProcessStep"]:
        for st in self.steps:
            if st.key == key:
                return st
        return None

    @property
    def final_step(self) -> Optional["ProcessStep"]:
        finals = [st for st in self.steps if st.is_final]
        if finals:
            return finals[-1]
        return self.steps[-1] if self.steps else None


class EngineOperationalization(BaseModel):
    """Complete operationalization for one engine.

    One file per engine in src/operationalizations/definitions/.
    Contains all stance operationalizations and depth sequences.
    """

    engine_key: str = Field(
        ...,
        description="Engine key (must match a capability engine definition)",
    )
    engine_name: str = Field(
        ...,
        description="Human-readable engine name",
    )
    stance_operationalizations: list[StanceOperationalization] = Field(
        default_factory=list,
        description="How each stance applies to this engine",
    )
    depth_sequences: list[DepthSequence] = Field(
        default_factory=list,
        description="Pass orderings for each depth level",
    )
    process: Optional[ProcessSpec] = Field(
        default=None,
        description="The engine's extract → verify → synthesize process (study 2026-09-04); run by a depth sequence whose `process` names it",
    )

    def process_for_depth(self, depth_key: str) -> Optional[ProcessSpec]:
        """The process a depth key runs, or None when the depth runs stance passes."""
        seq = self.get_depth_sequence(depth_key)
        if seq is None or not seq.process or self.process is None:
            return None
        return self.process if self.process.key == seq.process else None

    def get_stance_op(self, stance_key: str) -> StanceOperationalization | None:
        """Look up a stance operationalization by key."""
        for op in self.stance_operationalizations:
            if op.stance_key == stance_key:
                return op
        return None

    def get_depth_sequence(self, depth_key: str) -> DepthSequence | None:
        """Look up a depth sequence by key."""
        for seq in self.depth_sequences:
            if seq.depth_key == depth_key:
                return seq
        return None

    @property
    def stance_keys(self) -> list[str]:
        """All stance keys that have operationalizations."""
        return [op.stance_key for op in self.stance_operationalizations]

    @property
    def depth_keys(self) -> list[str]:
        """All depth levels that have sequences."""
        return [seq.depth_key for seq in self.depth_sequences]


class OperationalizationSummary(BaseModel):
    """Lightweight summary for listing endpoints."""

    engine_key: str
    engine_name: str
    stance_count: int
    depth_count: int
    stance_keys: list[str]
    depth_keys: list[str]


class CoverageEntry(BaseModel):
    """One cell in the coverage matrix."""

    engine_key: str
    engine_name: str
    has_operationalization: bool
    stance_keys: list[str]


class CoverageMatrix(BaseModel):
    """Engine x Stance coverage grid."""

    all_stance_keys: list[str] = Field(
        description="All known stance keys (columns)",
    )
    engines: list[CoverageEntry] = Field(
        description="One entry per engine with operationalization status",
    )
