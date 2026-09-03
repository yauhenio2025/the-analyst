"""Thread/context-local execution context for the run-event ledger.

The executor's call stack is workflow_runner → phase_runner → chain_runner →
engine_runner. Rather than threading job/phase/chain/engine/pass through every
signature, callers push the fields they know into a `contextvars.ContextVar`
and `engine_runner` reads the merged context when it emits call events.

Usage:
    with scope(job_id=job_id, phase="1.0", chain="concept_analysis"):
        ...  # anything called here sees these fields via current()

    token = push(engine="x")      # manual form
    ...
    pop(token)

ContextVars are per-thread: a fresh thread (ThreadPoolExecutor worker) starts
empty, which is why chain_runner sets job_id/phase/work_key itself from its
own arguments instead of relying on the parent thread.
"""

import contextvars
from contextlib import contextmanager
from typing import Any, Iterator, Optional

_CTX: contextvars.ContextVar[Optional[dict[str, Any]]] = contextvars.ContextVar(
    "run_events_context", default=None
)

CONTEXT_FIELDS = ("job_id", "phase", "chain", "engine", "pass_name", "stance", "work_key")


def current() -> dict[str, Any]:
    """Return a copy of the current context (empty dict if none)."""
    value = _CTX.get()
    return dict(value) if value else {}


def push(**fields: Any) -> contextvars.Token:
    """Merge `fields` into the current context; returns a token for pop()."""
    merged = current()
    for key, value in fields.items():
        merged[key] = value
    return _CTX.set(merged)


def pop(token: contextvars.Token) -> None:
    """Restore the context that was active before the matching push()."""
    try:
        _CTX.reset(token)
    except Exception:
        # Token from another context (thread) — fall back to clearing.
        _CTX.set(None)


@contextmanager
def scope(**fields: Any) -> Iterator[dict[str, Any]]:
    """Context manager form of push()/pop()."""
    token = push(**fields)
    try:
        yield current()
    finally:
        pop(token)


def phase_key(phase_number: Any) -> Optional[str]:
    """Canonical phase key: '1.0', '1.5', '2.0' (matches executor phase_statuses keys)."""
    if phase_number is None:
        return None
    try:
        return str(float(phase_number))
    except (TypeError, ValueError):
        return str(phase_number)
