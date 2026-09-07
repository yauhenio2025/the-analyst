"""The action register (Evgeny, 2026-09-07 18:30): one time-ordered record of what we did — every action outcome an organ posted, every
dossier job created or finished, every step added, every answer of his on the Brief — so that the narrative engine can say what we are
doing and the macro-actions engine can read a page's possibilities against our trajectory. Append-only; the executor database keeps the
last 5,000 events under one blob key; the process keeps a copy in memory. Shape only: nothing here judges an event."""
from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from typing import Any, Optional

BLOB_KEY = "register:events"
CAP = 5_000
KINDS = ("outcome", "job_created", "job_done", "job_failed", "step_added", "answer", "narrative", "macro_approved", "note")

_events: list[dict] = []
_loaded = False
_lock = threading.Lock()


def _put(key: str, content_type: str, data: bytes) -> bool:
    from src.dossier.blob_store import put_blob_safe
    return put_blob_safe(key, content_type, data)


def _get(key: str) -> Optional[bytes]:
    from src.dossier.blob_store import get_blob
    got = get_blob(key)
    return got[1] if isinstance(got, tuple) else got


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load() -> None:
    global _loaded
    if _loaded:
        return
    try:
        raw = _get(BLOB_KEY)
        if raw:
            for line in raw.decode("utf-8").splitlines():
                line = line.strip()
                if line:
                    try:
                        _events.append(json.loads(line))
                    except ValueError:
                        continue
    except Exception:
        pass
    _loaded = True


def _save() -> bool:
    try:
        return _put(BLOB_KEY, "application/x-ndjson", "\n".join(json.dumps(e, ensure_ascii=False) for e in _events[-CAP:]).encode("utf-8"))
    except Exception:
        return False


def record_event(kind: str, **fields: Any) -> dict:
    """Append one event: kind (outcome · job_created · job_done · job_failed · step_added · answer · narrative · macro_approved · note)
    and its fields (action, organ, status, batch, intent, finding, job_id, engine_key, cost_usd, summary …). Returns the event."""
    if kind not in KINDS:
        raise ValueError(f"event kind must be one of {KINDS}, not {kind!r}")
    ev = {"when": _now(), "kind": kind, **{k: v for k, v in fields.items() if v not in (None, "", [], {})}}
    with _lock:
        _load()
        _events.append(ev)
        del _events[:-CAP]
        _save()
    return ev


def events(since: Optional[str] = None, kind: Optional[str] = None, limit: int = 200) -> list[dict]:
    """The events, newest first; `since` an ISO instant; `kind` one kind."""
    with _lock:
        _load()
        rows = list(reversed(_events))                     # newest first by position; the stable sort below keeps that order within one second
    if since:
        rows = [e for e in rows if e.get("when", "") >= since]
    if kind:
        rows = [e for e in rows if e.get("kind") == kind]
    rows.sort(key=lambda e: e.get("when", ""), reverse=True)
    return rows[:max(1, limit)]


def render_register(rows: list[dict], limit: int = 400) -> str:
    """The register as the document the narrative engine reads: one line per event, oldest first, the fields in words."""
    lines = ["SOURCE ROLE: register", "THE ACTION REGISTER (what we did, oldest first; one line per event)", ""]
    for e in sorted(reversed(rows), key=lambda e: e.get("when", ""))[-limit:]:   # rows arrive newest first (events()); oldest first here, order kept within one second
        rest = "; ".join(f"{k}: {v if not isinstance(v, (dict, list)) else json.dumps(v, ensure_ascii=False)[:160]}" for k, v in e.items() if k not in ("when", "kind"))
        lines.append(f"[{e.get('when', '')}] {e.get('kind', '')} — {rest}")
    if len(lines) == 3:
        lines.append("(no events yet)")
    return "\n".join(lines)


def reset_for_tests() -> None:
    global _loaded
    with _lock:
        _events.clear()
        _loaded = False
