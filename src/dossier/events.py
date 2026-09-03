"""Event emission for the dossier workflow.

Codes against the events contract (`src.events.store.append_event/list_events`,
owned by the events agent). The import is lazy; when the store is absent an
in-memory ledger stands in so the run and the tests never depend on it.
Bookkeeping never kills the run: every failure here is logged and swallowed.
"""
from __future__ import annotations

import logging
import threading
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)

KINDS = (
    "job_started", "phase_started", "phase_finished", "call_started",
    "call_finished", "call_failed", "narration", "artifact", "note",
    "job_finished", "job_failed",
)

_fallback: dict[str, list[dict]] = {}
_fallback_seq: dict[str, int] = {}
_lock = threading.Lock()
_store_state: dict[str, Any] = {"checked": False, "append": None, "list": None}


def _resolve_store() -> None:
    if _store_state["checked"]:
        return
    _store_state["checked"] = True
    try:
        from src.events.store import append_event, list_events  # type: ignore

        _store_state["append"] = append_event
        _store_state["list"] = list_events
        logger.info("dossier.events: using src.events.store")
    except Exception as exc:  # module not merged yet, or broken
        logger.info(f"dossier.events: src.events.store unavailable ({exc}); using in-memory fallback")


def using_fallback() -> bool:
    _resolve_store()
    return _store_state["append"] is None


def _fallback_append(job_id: str, kind: str, fields: dict) -> int:
    with _lock:
        seq = _fallback_seq.get(job_id, 0) + 1
        _fallback_seq[job_id] = seq
        event = {"job_id": job_id, "seq": seq, "ts": datetime.utcnow().isoformat(), "kind": kind, **fields}
        _fallback.setdefault(job_id, []).append(event)
        return seq


def emit(job_id: str, kind: str, **fields: Any) -> int:
    """Append one event; returns its seq (0 when even the fallback failed)."""
    _resolve_store()
    clean = {k: v for k, v in fields.items() if v is not None}
    excerpt = clean.get("detail") or clean.get("output_excerpt") or ""
    logger.info(f"[event {job_id}] {kind} {clean.get('phase') or ''} {str(excerpt)[:140]}")
    append = _store_state["append"]
    if append is not None:
        try:
            seq = append(job_id, kind, **clean)
            return int(seq) if seq is not None else 0
        except Exception as exc:
            logger.warning(f"events store append failed ({exc}); falling back to memory")
    try:
        return _fallback_append(job_id, kind, clean)
    except Exception as exc:  # pragma: no cover
        logger.warning(f"fallback event append failed: {exc}")
        return 0


def _event_to_dict(ev: Any) -> dict:
    if isinstance(ev, dict):
        return ev
    if hasattr(ev, "model_dump"):
        return ev.model_dump()
    if hasattr(ev, "__dict__"):
        return dict(ev.__dict__)
    return {"raw": str(ev)}


def list_events(job_id: str, after_seq: int = 0) -> list[dict]:
    """Events for a job with seq > after_seq, from the real store or the fallback."""
    _resolve_store()
    lister = _store_state["list"]
    if lister is not None:
        try:
            rows = lister(job_id, after_seq)
            return [_event_to_dict(r) for r in (rows or [])]
        except TypeError:
            try:
                rows = lister(job_id, after_seq=after_seq)
                return [_event_to_dict(r) for r in (rows or [])]
            except Exception as exc:
                logger.warning(f"events store list failed ({exc})")
        except Exception as exc:
            logger.warning(f"events store list failed ({exc})")
    with _lock:
        return [e for e in _fallback.get(job_id, []) if e.get("seq", 0) > after_seq]


def excerpt(text: Optional[str], n: int = 400) -> str:
    if not text:
        return ""
    text = str(text)
    return text if len(text) <= n else text[:n] + "…"
