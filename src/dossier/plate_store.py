"""Plate store — table `dossier_plates` on the executor DB (Postgres or SQLite), one row per (job, plate).

Created lazily with CREATE TABLE IF NOT EXISTS through `src.executor.db.execute`; the dossier_jobs
table is untouched. Rows are upserted after every attempt-level milestone (planned → generated /
failed), so a console reads the truth mid-run. An in-process registry says which jobs have a plates
run in flight (the run itself is a daemon thread started by the route).
"""
from __future__ import annotations

import json
import logging
import threading
from datetime import datetime
from typing import Any, Optional

from src.dossier.plates import Plate

logger = logging.getLogger(__name__)

_table_ready = False
_table_lock = threading.Lock()
_runs_lock = threading.Lock()
_runs: dict[str, dict[str, Any]] = {}

DDL = """
CREATE TABLE IF NOT EXISTS dossier_plates (
    job_id TEXT NOT NULL,
    key TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'planned',
    spec_json TEXT NOT NULL DEFAULT '{}',
    figure_id TEXT,
    url TEXT,
    path TEXT,
    narrative TEXT DEFAULT '',
    compliance_json TEXT,
    receipts_json TEXT DEFAULT '[]',
    attempts_json TEXT DEFAULT '[]',
    cost_usd REAL DEFAULT 0,
    created_at TEXT,
    updated_at TEXT,
    PRIMARY KEY (job_id, key)
)
"""

_SPEC_FIELDS = ("key", "family", "visual_format", "perspective", "title", "canonical", "narrative", "size_guides", "style_school",
                "why_this_perspective", "claimed_territory", "excludes", "abstraction_level", "aspect", "anchors", "provider", "model",
                "prompt", "width", "height", "note", "grounding", "declutter", "created_at")


def ensure_table() -> None:
    global _table_ready
    if _table_ready:
        return
    with _table_lock:
        if _table_ready:
            return
        from src.executor.db import execute, init_db

        init_db()
        execute(DDL)
        _table_ready = True
        logger.info("dossier_plates table ready")


def reset_for_tests() -> None:
    global _table_ready
    with _table_lock:
        _table_ready = False
    with _runs_lock:
        _runs.clear()


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, default=str) if value is not None else "null"


def _loads(text: Any, default: Any) -> Any:
    if text is None:
        return default
    if isinstance(text, (dict, list)):
        return text
    try:
        parsed = json.loads(text)
        return default if parsed is None else parsed
    except Exception:
        return default


def upsert_plate(job_id: str, plate: Plate) -> None:
    """Insert or replace the plate's row (SQLite ≥ 3.24 and Postgres share the ON CONFLICT syntax)."""
    from src.executor.db import execute

    ensure_table()
    now = datetime.utcnow().isoformat()
    d = plate.model_dump()
    spec = {k: d.get(k) for k in _SPEC_FIELDS}
    params = (job_id, plate.key, plate.status, _dumps(spec), plate.figure_id, plate.url, plate.path, plate.narrative or "",
              _dumps(plate.compliance) if plate.compliance is not None else None, _dumps(plate.receipts), _dumps(plate.attempts),
              float(plate.cost_usd or 0.0), plate.created_at or now, now)
    execute(
        """INSERT INTO dossier_plates (job_id, key, status, spec_json, figure_id, url, path, narrative, compliance_json,
                                       receipts_json, attempts_json, cost_usd, created_at, updated_at)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           ON CONFLICT (job_id, key) DO UPDATE SET
               status = excluded.status, spec_json = excluded.spec_json, figure_id = excluded.figure_id, url = excluded.url,
               path = excluded.path, narrative = excluded.narrative, compliance_json = excluded.compliance_json,
               receipts_json = excluded.receipts_json, attempts_json = excluded.attempts_json, cost_usd = excluded.cost_usd,
               updated_at = excluded.updated_at""",
        params,
    )


def _row_to_plate(row: dict) -> Plate:
    spec = _loads(row.get("spec_json"), {}) or {}
    data = {**{k: v for k, v in spec.items() if v is not None},
            "key": row["key"], "status": row.get("status") or "planned", "figure_id": row.get("figure_id"), "url": row.get("url"),
            "path": row.get("path"), "narrative": row.get("narrative") or spec.get("narrative") or "",
            "compliance": _loads(row.get("compliance_json"), None), "receipts": _loads(row.get("receipts_json"), []),
            "attempts": _loads(row.get("attempts_json"), []), "cost_usd": float(row.get("cost_usd") or 0.0),
            "created_at": str(row.get("created_at") or "")}
    return Plate.model_validate(data)


def list_plates(job_id: str) -> list[Plate]:
    from src.executor.db import execute

    ensure_table()
    rows = execute("SELECT * FROM dossier_plates WHERE job_id = %s ORDER BY created_at ASC, key ASC", (job_id,), fetch="all") or []
    out = []
    for r in rows:
        try:
            out.append(_row_to_plate(r))
        except Exception as exc:
            logger.warning(f"plate row unreadable ({job_id}/{r.get('key')}): {exc}")
    return out


def get_plate(job_id: str, key: str) -> Optional[Plate]:
    from src.executor.db import execute

    ensure_table()
    row = execute("SELECT * FROM dossier_plates WHERE job_id = %s AND key = %s", (job_id, key), fetch="one")
    return _row_to_plate(row) if row else None


def delete_plates(job_id: str) -> int:
    from src.executor.db import execute

    ensure_table()
    rows = execute("SELECT COUNT(*) AS n FROM dossier_plates WHERE job_id = %s", (job_id,), fetch="one") or {}
    execute("DELETE FROM dossier_plates WHERE job_id = %s", (job_id,))
    return int(rows.get("n") or 0)


# ── the in-process run registry ─────────────────────────────────────────

def mark_running(job_id: str, n: int, perspectives: Optional[list[str]] = None) -> bool:
    """Claim a plates run for the job; False when one is already in flight."""
    with _runs_lock:
        if job_id in _runs:
            return False
        _runs[job_id] = {"started_at": datetime.utcnow().isoformat(), "n": n, "perspectives": perspectives or []}
        return True


def mark_done(job_id: str) -> None:
    with _runs_lock:
        _runs.pop(job_id, None)


def run_state(job_id: str) -> Optional[dict[str, Any]]:
    with _runs_lock:
        state = _runs.get(job_id)
        return dict(state) if state else None
