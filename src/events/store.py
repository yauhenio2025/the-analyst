"""Run-event ledger storage (table `run_events`).

Reuses the executor's dual-backend connection helpers (`src/executor/db.py`:
Postgres via EXECUTOR_DATABASE_URL, else SQLite at src/executor/executor.db).
The table is created lazily with CREATE TABLE IF NOT EXISTS on first use.

Guarantees:
- `append_event()` NEVER raises — the ledger must not break the executor.
  On failure it logs and returns 0 (real seq numbers start at 1).
- `seq` is monotonic per job: computed as MAX(seq)+1 inside a process-level
  lock and protected by a UNIQUE index on (job_id, seq) with a short retry,
  so concurrent writers (parallel phases, per-work thread pools, or another
  process sharing the DB) cannot collide.
"""

import hashlib
import json
import logging
import threading
from datetime import datetime, timezone
from typing import Any, Optional

from src.executor import db as _db
from src.events.pricing import estimate_cost
from src.events.schemas import EVENT_KINDS, TERMINAL_KINDS

logger = logging.getLogger(__name__)

PROMPT_EXCERPT_SYSTEM_CHARS = 2000
PROMPT_EXCERPT_USER_CHARS = 1000
OUTPUT_EXCERPT_CHARS = 2000
DETAIL_MAX_CHARS = 1000
PAYLOAD_MAX_CHARS = 64_000

_COLUMNS = (
    "job_id", "seq", "ts", "kind", "phase", "chain", "engine", "pass_name", "stance",
    "work_key", "model", "input_chars", "output_chars", "input_tokens", "output_tokens",
    "cost_usd", "duration_ms", "prompt_hash", "prompt_excerpt", "output_excerpt",
    "detail", "narrator", "payload_json",
)
_INT_FIELDS = ("input_chars", "output_chars", "input_tokens", "output_tokens", "duration_ms")

_table_lock = threading.Lock()
_seq_lock = threading.Lock()
_table_ready = False


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

def _create_sql() -> list[str]:
    pk = "SERIAL PRIMARY KEY" if _db._is_postgres() else "INTEGER PRIMARY KEY AUTOINCREMENT"
    return [
        f"""CREATE TABLE IF NOT EXISTS run_events (
            id {pk},
            job_id TEXT NOT NULL,
            seq INTEGER NOT NULL,
            ts TEXT NOT NULL,
            kind TEXT NOT NULL,
            phase TEXT,
            chain TEXT,
            engine TEXT,
            pass_name TEXT,
            stance TEXT,
            work_key TEXT,
            model TEXT,
            input_chars INTEGER,
            output_chars INTEGER,
            input_tokens INTEGER,
            output_tokens INTEGER,
            cost_usd REAL,
            duration_ms INTEGER,
            prompt_hash TEXT,
            prompt_excerpt TEXT,
            output_excerpt TEXT,
            detail TEXT,
            narrator TEXT,
            payload_json TEXT
        )""",
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_run_events_job_seq ON run_events(job_id, seq)",
        "CREATE INDEX IF NOT EXISTS idx_run_events_job_kind ON run_events(job_id, kind)",
    ]


def ensure_table() -> None:
    """Create `run_events` (+ indexes) if missing. Idempotent, thread-safe."""
    global _table_ready
    if _table_ready:
        return
    with _table_lock:
        if _table_ready:
            return
        with _db.get_connection() as conn:
            cursor = conn.cursor()
            for sql in _create_sql():
                cursor.execute(sql)
            conn.commit()
        _table_ready = True
        backend = "PostgreSQL" if _db._is_postgres() else f"SQLite ({_db.SQLITE_PATH})"
        logger.info("run_events table ready on %s", backend)


def reset_for_tests() -> None:
    """Forget the lazy-init flag (tests swap the SQLite path between cases)."""
    global _table_ready
    with _table_lock:
        _table_ready = False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def prompt_hash(system_prompt: str, user_message: str) -> str:
    """sha256 over system + user text (the exact strings sent to the model)."""
    h = hashlib.sha256()
    h.update((system_prompt or "").encode("utf-8", errors="replace"))
    h.update((user_message or "").encode("utf-8", errors="replace"))
    return h.hexdigest()


def prompt_excerpt(system_prompt: str, user_message: str) -> str:
    """First 2000 chars of the system prompt + '\\n---\\n' + first 1000 of the user message."""
    return (
        (system_prompt or "")[:PROMPT_EXCERPT_SYSTEM_CHARS]
        + "\n---\n"
        + (user_message or "")[:PROMPT_EXCERPT_USER_CHARS]
    )


def output_excerpt(text: str) -> str:
    return (text or "")[:OUTPUT_EXCERPT_CHARS]


def _sql(sql: str) -> str:
    return sql if _db._is_postgres() else sql.replace("%s", "?")


def _coerce_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _json_default(obj: Any) -> Any:
    if hasattr(obj, "model_dump"):
        try:
            return obj.model_dump()
        except Exception:
            pass
    return str(obj)


# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------

def append_event(job_id: str, kind: str, **fields: Any) -> int:
    """Append one event; returns its per-job `seq` (0 on failure). Never raises.

    Recognised keyword fields are the RunEvent columns (phase, chain, engine,
    pass_name, stance, work_key, model, input_chars, output_chars,
    input_tokens, output_tokens, cost_usd, duration_ms, prompt_hash,
    prompt_excerpt, output_excerpt, detail, narrator, ts) plus `payload`
    (dict). Any other keyword is folded into the payload.

    If `cost_usd` is omitted but model + tokens are present, it is estimated.
    """
    try:
        return _append_event(job_id, kind, fields)
    except Exception as e:  # noqa: BLE001 — the ledger must never break execution
        logger.warning("run_events append failed for job %s kind %s: %s", job_id, kind, e)
        return 0


def _append_event(job_id: str, kind: str, fields: dict[str, Any]) -> int:
    if not job_id:
        raise ValueError("job_id required")
    if kind not in EVENT_KINDS:
        logger.warning("run_events: non-standard kind %r for job %s", kind, job_id)

    ensure_table()

    payload: dict[str, Any] = {}
    supplied_payload = fields.pop("payload", None)
    if isinstance(supplied_payload, dict):
        payload.update(supplied_payload)
    elif supplied_payload is not None:
        payload["value"] = supplied_payload

    row: dict[str, Any] = {col: None for col in _COLUMNS}
    row["job_id"] = str(job_id)
    row["kind"] = kind
    row["ts"] = fields.pop("ts", None) or utc_now_iso()

    for key, value in list(fields.items()):
        if key in _COLUMNS and key not in ("job_id", "seq", "kind", "payload_json"):
            row[key] = value
        else:
            payload[key] = value

    for key in _INT_FIELDS:
        row[key] = _coerce_int(row.get(key))
    for key in ("phase", "chain", "engine", "pass_name", "stance", "work_key", "model", "prompt_hash"):
        if row.get(key) is not None:
            row[key] = str(row[key])[:500]
    if row.get("prompt_excerpt") is not None:
        row["prompt_excerpt"] = str(row["prompt_excerpt"])[: PROMPT_EXCERPT_SYSTEM_CHARS + PROMPT_EXCERPT_USER_CHARS + 16]
    if row.get("output_excerpt") is not None:
        row["output_excerpt"] = str(row["output_excerpt"])[:OUTPUT_EXCERPT_CHARS]
    if row.get("detail") is not None:
        row["detail"] = str(row["detail"])[:DETAIL_MAX_CHARS]
    if row.get("narrator") is not None:
        row["narrator"] = str(row["narrator"])[:DETAIL_MAX_CHARS]

    if row.get("cost_usd") is None and row.get("model") and (
        row.get("input_tokens") is not None or row.get("output_tokens") is not None
    ):
        row["cost_usd"] = estimate_cost(row["model"], row.get("input_tokens"), row.get("output_tokens"))
    elif row.get("cost_usd") is not None:
        try:
            row["cost_usd"] = float(row["cost_usd"])
        except (TypeError, ValueError):
            row["cost_usd"] = None

    payload_json = json.dumps(payload, ensure_ascii=False, default=_json_default)
    if len(payload_json) > PAYLOAD_MAX_CHARS:
        payload_json = json.dumps(
            {"truncated": True, "original_chars": len(payload_json), "head": payload_json[:PAYLOAD_MAX_CHARS]},
            ensure_ascii=False,
        )
    row["payload_json"] = payload_json

    insert_cols = [c for c in _COLUMNS if c != "seq"]
    placeholders = ", ".join(["%s"] * len(insert_cols))
    col_list = ", ".join(insert_cols)
    values = tuple(row[c] for c in insert_cols)

    last_error: Optional[Exception] = None
    for _attempt in range(4):
        with _seq_lock:
            with _db.get_connection() as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        _sql("SELECT COALESCE(MAX(seq), 0) FROM run_events WHERE job_id = %s"),
                        (row["job_id"],),
                    )
                    fetched = cursor.fetchone()
                    max_seq = int((fetched[0] if fetched else 0) or 0)
                    seq = max_seq + 1
                    cursor.execute(
                        _sql(f"INSERT INTO run_events ({col_list}, seq) VALUES ({placeholders}, %s)"),
                        values + (seq,),
                    )
                    conn.commit()
                    return seq
                except Exception as e:  # unique-index collision (another writer) → retry
                    last_error = e
                    try:
                        conn.rollback()
                    except Exception:
                        pass
    raise RuntimeError(f"run_events insert failed after retries: {last_error}")


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------

def _row_to_event(row: dict[str, Any]) -> dict[str, Any]:
    event = dict(row)
    raw = event.pop("payload_json", None)
    try:
        event["payload"] = json.loads(raw) if raw else {}
        if not isinstance(event["payload"], dict):
            event["payload"] = {"value": event["payload"]}
    except Exception:
        event["payload"] = {"raw": raw}
    for key in ("id", "seq") + _INT_FIELDS:
        if event.get(key) is not None:
            event[key] = _coerce_int(event[key])
    if event.get("cost_usd") is not None:
        try:
            event["cost_usd"] = float(event["cost_usd"])
        except (TypeError, ValueError):
            event["cost_usd"] = None
    return event


def list_events(job_id: str, after_seq: int = 0, limit: int = 1000) -> list[dict[str, Any]]:
    """Events for a job with seq > after_seq, ordered by seq, capped at `limit`."""
    try:
        ensure_table()
        limit = max(1, min(int(limit or 1000), 10_000))
        rows = _db.execute(
            "SELECT * FROM run_events WHERE job_id = %s AND seq > %s ORDER BY seq ASC LIMIT %s",
            (str(job_id), int(after_seq or 0), limit),
            fetch="all",
        ) or []
        return [_row_to_event(r) for r in rows]
    except Exception as e:  # noqa: BLE001
        logger.warning("run_events list failed for job %s: %s", job_id, e)
        return []


def last_seq(job_id: str) -> int:
    try:
        ensure_table()
        row = _db.execute(
            "SELECT COALESCE(MAX(seq), 0) AS m FROM run_events WHERE job_id = %s",
            (str(job_id),),
            fetch="one",
        )
        return int((row or {}).get("m") or 0)
    except Exception as e:  # noqa: BLE001
        logger.warning("run_events last_seq failed for job %s: %s", job_id, e)
        return 0


def _parse_ts(ts: Optional[str]) -> Optional[datetime]:
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def _ms_between(start: Optional[str], end: Optional[str]) -> int:
    a, b = _parse_ts(start), _parse_ts(end)
    if a is None or b is None:
        return 0
    return max(0, int((b - a).total_seconds() * 1000))


def job_summary(job_id: str) -> dict[str, Any]:
    """Aggregate the ledger: {calls, input_tokens, output_tokens, cost_usd, duration_ms, phases, ...}.

    `calls` counts call_finished events; tokens/cost are summed over them.
    `duration_ms` is wall-clock from the first event to the last (or to
    job_finished/job_failed). `phases` is an ordered list of per-phase
    aggregates including the narrator line where one was produced.
    """
    summary: dict[str, Any] = {
        "job_id": str(job_id),
        "status": "unknown",
        "calls": 0,
        "failed_calls": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "cost_usd": 0.0,
        "duration_ms": 0,
        "phases": [],
        "events": 0,
        "last_seq": 0,
        "started_at": None,
        "last_event_at": None,
    }
    events: list[dict[str, Any]] = []
    cursor_seq = 0
    while True:
        batch = list_events(job_id, after_seq=cursor_seq, limit=5000)
        if not batch:
            break
        events.extend(batch)
        cursor_seq = batch[-1]["seq"]
        if len(batch) < 5000:
            break
    if not events:
        return summary

    phases: dict[str, dict[str, Any]] = {}
    order: list[str] = []

    def phase_bucket(key: Optional[str]) -> Optional[dict[str, Any]]:
        if not key:
            return None
        if key not in phases:
            phases[key] = {
                "phase": key, "name": None, "status": "running", "calls": 0,
                "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "duration_ms": 0,
                "narrator": None, "engines": [], "started_at": None, "finished_at": None,
            }
            order.append(key)
        return phases[key]

    status = "running"
    finished_ts: Optional[str] = None
    for ev in events:
        kind = ev.get("kind")
        bucket = phase_bucket(ev.get("phase"))
        if kind == "call_finished":
            summary["calls"] += 1
            summary["input_tokens"] += int(ev.get("input_tokens") or 0)
            summary["output_tokens"] += int(ev.get("output_tokens") or 0)
            summary["cost_usd"] += float(ev.get("cost_usd") or 0.0)
            if bucket is not None:
                bucket["calls"] += 1
                bucket["input_tokens"] += int(ev.get("input_tokens") or 0)
                bucket["output_tokens"] += int(ev.get("output_tokens") or 0)
                bucket["cost_usd"] += float(ev.get("cost_usd") or 0.0)
                eng = ev.get("engine")
                if eng and eng not in bucket["engines"]:
                    bucket["engines"].append(eng)
        elif kind == "call_failed":
            summary["failed_calls"] += 1
        elif kind == "phase_started" and bucket is not None:
            bucket["started_at"] = ev.get("ts")
            bucket["status"] = "running"
            bucket["name"] = (ev.get("payload") or {}).get("phase_name") or bucket["name"]
            for eng in (ev.get("payload") or {}).get("engines") or []:
                if eng not in bucket["engines"]:
                    bucket["engines"].append(eng)
        elif kind == "phase_finished" and bucket is not None:
            bucket["finished_at"] = ev.get("ts")
            bucket["status"] = (ev.get("payload") or {}).get("status") or "completed"
            bucket["name"] = (ev.get("payload") or {}).get("phase_name") or bucket["name"]
            if ev.get("duration_ms"):
                bucket["duration_ms"] = int(ev["duration_ms"])
            elif bucket["started_at"]:
                bucket["duration_ms"] = _ms_between(bucket["started_at"], bucket["finished_at"])
        elif kind == "narration" and bucket is not None:
            bucket["narrator"] = ev.get("narrator") or bucket["narrator"]
        elif kind == "job_started":
            summary["started_at"] = summary["started_at"] or ev.get("ts")
        elif kind in TERMINAL_KINDS:
            status = (ev.get("payload") or {}).get("status") or ("completed" if kind == "job_finished" else "failed")
            finished_ts = ev.get("ts")

    summary["status"] = status
    summary["events"] = len(events)
    summary["last_seq"] = int(events[-1].get("seq") or 0)
    summary["started_at"] = summary["started_at"] or events[0].get("ts")
    summary["last_event_at"] = events[-1].get("ts")
    summary["duration_ms"] = _ms_between(summary["started_at"], finished_ts or summary["last_event_at"])
    summary["cost_usd"] = round(summary["cost_usd"], 6)
    for key in order:
        b = phases[key]
        if b["status"] == "running" and b["started_at"] and not b["finished_at"]:
            b["duration_ms"] = _ms_between(b["started_at"], summary["last_event_at"])
        b["cost_usd"] = round(b["cost_usd"], 6)
        summary["phases"].append(b)
    return summary


def has_terminal_event(job_id: str) -> bool:
    try:
        ensure_table()
        row = _db.execute(
            "SELECT COUNT(*) AS n FROM run_events WHERE job_id = %s AND kind IN ('job_finished', 'job_failed')",
            (str(job_id),),
            fetch="one",
        )
        return bool(int((row or {}).get("n") or 0))
    except Exception:  # noqa: BLE001
        return False
