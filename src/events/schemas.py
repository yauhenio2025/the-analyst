"""Pydantic v2 schemas for the per-call run-event ledger.

A `RunEvent` is one row of the `run_events` table (see `src/events/store.py`).
Events are appended by the executor hooks (job → phase → chain → engine →
pass → LLM call) and by the narrator; consumers (web console, mgmt console,
dossier runner) read them via `GET /v1/events/{job_id}` or the SSE stream.

Representation note: the storage column is `payload_json TEXT`; the JSON
representation exposes it parsed as `payload` (object).
"""

from typing import Any, Optional

from pydantic import BaseModel, Field

EVENT_KINDS: tuple[str, ...] = (
    "job_started",
    "job_finished",
    "job_failed",
    "phase_started",
    "phase_finished",
    "chain_started",
    "chain_finished",
    "call_started",
    "call_finished",
    "call_failed",
    "call_refused",
    "narration",
    "artifact",
    "note",
)

TERMINAL_KINDS: tuple[str, ...] = ("job_finished", "job_failed")


class RunEvent(BaseModel):
    """One ledger row. All fields except identity/kind are optional."""

    id: Optional[int] = Field(default=None, description="Row id (db primary key)")
    job_id: str
    seq: int = Field(description="Monotonic per-job sequence number (1-based)")
    ts: str = Field(description="ISO-8601 UTC timestamp")
    kind: str = Field(description="One of EVENT_KINDS")

    # Where in the job tree this event sits
    phase: Optional[str] = Field(default=None, description="Phase key, e.g. '1.0', '1.5'")
    chain: Optional[str] = None
    engine: Optional[str] = None
    pass_name: Optional[str] = Field(default=None, description="e.g. 'Pass 2: Conflict Mapping'")
    stance: Optional[str] = None
    work_key: Optional[str] = None

    # LLM call facts
    model: Optional[str] = Field(default=None, description="Model id actually sent to the provider")
    input_chars: Optional[int] = None
    output_chars: Optional[int] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    cost_usd: Optional[float] = None
    duration_ms: Optional[int] = None
    prompt_hash: Optional[str] = Field(default=None, description="sha256(system + user)")
    prompt_excerpt: Optional[str] = Field(
        default=None,
        description="First 2000 chars of system prompt + '\\n---\\n' + first 1000 of user message",
    )
    output_excerpt: Optional[str] = Field(default=None, description="First 2000 chars of output")

    # Human layer
    detail: Optional[str] = Field(default=None, description="One human sentence")
    narrator: Optional[str] = Field(default=None, description="LLM one-liner (narration events)")

    payload: dict[str, Any] = Field(default_factory=dict, description="Parsed payload_json")


class PhaseSummary(BaseModel):
    phase: str
    name: Optional[str] = None
    status: str = "running"
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    duration_ms: int = 0
    narrator: Optional[str] = None
    engines: list[str] = Field(default_factory=list)
    started_at: Optional[str] = None
    finished_at: Optional[str] = None


class JobSummary(BaseModel):
    job_id: str
    status: str = Field(default="running", description="running | completed | failed | cancelled | unknown")
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    duration_ms: int = 0
    phases: list[PhaseSummary] = Field(default_factory=list)
    events: int = 0
    last_seq: int = 0
    started_at: Optional[str] = None
    last_event_at: Optional[str] = None
    failed_calls: int = 0
