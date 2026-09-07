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


def narrate_later(min_new_events: int = 3) -> bool:
    """Run the trajectory narrative in a daemon thread when the register has grown since the last narrative (a light call, cents).
    Never blocks the caller; failures are logged, not raised."""
    import logging, threading
    log = logging.getLogger(__name__)
    try:
        rows = events(limit=400)
        since_last = 0
        for e in rows:
            if e.get("kind") == "narrative":
                break
            since_last += 1
        if since_last < min_new_events:
            return False
    except Exception as exc:
        log.warning(f"narrate_later could not read the register: {exc}"); return False

    def _go():
        try:
            from src.api.routes.trajectory import narrate, NarrateIn
            narrate(NarrateIn())
        except Exception as exc:
            log.warning(f"the narrative did not run: {exc}")
    threading.Thread(target=_go, name="trajectory-narrative", daemon=True).start()
    return True


def job_substance(job_id: str) -> dict:
    """What a job read and found, from the readings ledger: the engines, the persons most named, the rows, where it renders."""
    try:
        from src.readings.registry import readings_for, reading
    except Exception:
        return {}
    entries = readings_for(job=job_id, limit=40).get("readings") or []
    if not entries:
        return {}
    persons: dict[str, int] = {}; texts: set[str] = set(); rows = 0; renders: list[str] = []
    for e in entries:
        r = reading(job_id, e["phase"]) or {}
        for i, p in enumerate(r.get("persons") or []):
            persons[p] = persons.get(p, 0) + max(1, 6 - i)
        texts.update(r.get("texts") or []); rows += r.get("n_rows") or 0
        for x in r.get("renders") or []:
            if x not in renders:
                renders.append(x)
    return {"engine_keys": sorted({e["engine"] for e in entries}), "persons": sorted(persons, key=lambda p: -persons[p])[:8], "texts": len(texts), "rows": rows, "renders": renders[:3]}


def backfill_jobs(jobs: list[dict], refresh: bool = False) -> int:
    """Record job_done events for finished jobs (idempotent by job id; `refresh` re-records every finished job with its substance from
    the readings ledger — the first narrative saw job ids and nothing else)."""
    global _events
    if refresh:
        with _lock:
            _load()
            _events = [e for e in _events if not (e.get("kind") == "job_done" and e.get("backfilled"))]
            _save()
    have = {e.get("job_id") for e in events(kind="job_done", limit=5000)}
    n = 0
    for j in jobs:
        if j.get("status") != "done" or j.get("id") in have:
            continue
        sub = job_substance(j.get("id"))
        record_event("job_done", job_id=j.get("id"), when=j.get("updated_at") or j.get("created_at"),
                     engine_keys=sub.get("engine_keys") or [ph.get("engine_key") for ph in (j.get("analysis") or {}).values() if isinstance(ph, dict) and ph.get("engine_key")],
                     persons=sub.get("persons"), rows=sub.get("rows"), renders=sub.get("renders"),
                     intent=((j.get("options") or {}).get("intent") or "")[:200], cost_usd=(j.get("totals") or {}).get("cost_usd"), backfilled=True)
        n += 1
    return n
