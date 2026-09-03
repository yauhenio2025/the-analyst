"""Dossier job store — table `dossier_jobs` on the executor DB (Postgres or SQLite).

Persisted after EVERY step (incremental persistence): the row is the truth a
console reads, and `resume(job_id)` continues from the recorded step.
"""
from __future__ import annotations

import json
import logging
import threading
from datetime import datetime
from typing import Any, Optional

from src.executor.db import execute, init_db
from src.dossier.schemas import DossierJob, DossierJobSummary, Receipt

logger = logging.getLogger(__name__)

_table_ready = False
_table_lock = threading.Lock()
_receipt_lock = threading.Lock()

JSON_COLUMNS = (
    "sources_json", "options_json", "profiles_json", "brief_json", "analysis_json",
    "tables_json", "figures_json", "sections_json", "receipts_json", "totals_json",
    "paths_json", "documents_json", "plan_json", "notes_json",
)

DDL = """
CREATE TABLE IF NOT EXISTS dossier_jobs (
    id TEXT PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'queued',
    step TEXT DEFAULT '',
    created_at TEXT,
    updated_at TEXT,
    sources_json TEXT DEFAULT '[]',
    documents_json TEXT DEFAULT '[]',
    options_json TEXT DEFAULT '{}',
    profiles_json TEXT,
    brief_json TEXT,
    chosen_option TEXT,
    plan_id TEXT,
    plan_json TEXT,
    analysis_job_id TEXT,
    analysis_json TEXT DEFAULT '{}',
    tables_json TEXT DEFAULT '[]',
    figures_json TEXT DEFAULT '[]',
    sections_json TEXT,
    receipts_json TEXT DEFAULT '[]',
    totals_json TEXT DEFAULT '{}',
    error TEXT,
    paths_json TEXT DEFAULT '{}',
    notes_json TEXT DEFAULT '[]'
)
"""


def ensure_table() -> None:
    global _table_ready
    if _table_ready:
        return
    with _table_lock:
        if _table_ready:
            return
        init_db()
        execute(DDL)
        _table_ready = True
        logger.info("dossier_jobs table ready")


def _jsonable(value: Any) -> Any:
    """Pydantic models anywhere in the tree become dicts (a list of models used to be persisted as reprs)."""
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    return value


def _dumps(value: Any) -> str:
    if value is None:
        return "null"
    return json.dumps(_jsonable(value), ensure_ascii=False, default=str)


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


def _row_to_job(row: dict) -> DossierJob:
    data = {
        "id": row["id"],
        "status": row.get("status") or "queued",
        "step": row.get("step") or "",
        "created_at": str(row.get("created_at") or ""),
        "updated_at": str(row.get("updated_at") or ""),
        "sources": _loads(row.get("sources_json"), []),
        "documents": _loads(row.get("documents_json"), []),
        "options": _loads(row.get("options_json"), {}),
        "profiles": _loads(row.get("profiles_json"), None),
        "brief": _loads(row.get("brief_json"), None),
        "chosen_option": row.get("chosen_option"),
        "plan_id": row.get("plan_id"),
        "plan": _loads(row.get("plan_json"), None),
        "analysis_job_id": row.get("analysis_job_id"),
        "analysis": _loads(row.get("analysis_json"), {}),
        "tables": _loads(row.get("tables_json"), []),
        "figures": _loads(row.get("figures_json"), []),
        "sections": _loads(row.get("sections_json"), None),
        "receipts": _loads(row.get("receipts_json"), []),
        "totals": _loads(row.get("totals_json"), {}),
        "error": row.get("error"),
        "paths": _loads(row.get("paths_json"), {}),
        "notes": _loads(row.get("notes_json"), []),
    }
    return DossierJob.model_validate(data)


def create_job(job: DossierJob) -> DossierJob:
    ensure_table()
    now = datetime.utcnow().isoformat()
    job.created_at = now
    job.updated_at = now
    execute(
        """INSERT INTO dossier_jobs
           (id, status, step, created_at, updated_at, sources_json, documents_json, options_json,
            profiles_json, brief_json, chosen_option, plan_id, plan_json, analysis_job_id,
            analysis_json, tables_json, figures_json, sections_json, receipts_json, totals_json,
            error, paths_json, notes_json)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            job.id, job.status, job.step, now, now,
            _dumps(job.sources), _dumps(job.documents), _dumps(job.options),
            _dumps(job.profiles) if job.profiles else None,
            _dumps(job.brief) if job.brief else None,
            job.chosen_option, job.plan_id,
            _dumps(job.plan) if job.plan else None,
            job.analysis_job_id,
            _dumps(job.analysis), _dumps(job.tables), _dumps(job.figures),
            _dumps(job.sections) if job.sections else None,
            _dumps(job.receipts), _dumps(job.totals), job.error, _dumps(job.paths), _dumps(job.notes),
        ),
    )
    logger.info(f"Created dossier job {job.id}")
    return job


def get_job(job_id: str) -> Optional[DossierJob]:
    ensure_table()
    row = execute("SELECT * FROM dossier_jobs WHERE id = %s", (job_id,), fetch="one")
    return _row_to_job(row) if row else None


def list_jobs(limit: int = 50) -> list[DossierJobSummary]:
    ensure_table()
    rows = execute(
        "SELECT id, status, step, created_at, updated_at, options_json, documents_json, "
        "chosen_option, totals_json, error, sections_json FROM dossier_jobs "
        "ORDER BY created_at DESC LIMIT %s",
        (limit,),
        fetch="all",
    ) or []
    out = []
    for row in rows:
        options = _loads(row.get("options_json"), {})
        documents = _loads(row.get("documents_json"), [])
        totals = _loads(row.get("totals_json"), {})
        sections = _loads(row.get("sections_json"), None) or {}
        title = sections.get("title") or ""
        if not title and documents:
            title = documents[0].get("title", "")
            if len(documents) > 1:
                title += f" (+{len(documents) - 1})"
        out.append(DossierJobSummary(
            id=row["id"], status=row.get("status") or "queued", step=row.get("step") or "",
            created_at=str(row.get("created_at") or ""), updated_at=str(row.get("updated_at") or ""),
            title=title, intent=options.get("intent"), audience=options.get("audience", "executive"),
            depth=options.get("depth", "simple"), document_count=len(documents),
            chosen_option=row.get("chosen_option"), cost_usd=float(totals.get("cost_usd") or 0.0),
            error=row.get("error"),
        ))
    return out


COLUMN_FOR_FIELD = {
    "status": "status", "step": "step", "sources": "sources_json", "documents": "documents_json",
    "options": "options_json", "profiles": "profiles_json", "brief": "brief_json",
    "chosen_option": "chosen_option", "plan_id": "plan_id", "plan": "plan_json",
    "analysis_job_id": "analysis_job_id", "analysis": "analysis_json", "tables": "tables_json",
    "figures": "figures_json", "sections": "sections_json", "receipts": "receipts_json",
    "totals": "totals_json", "error": "error", "paths": "paths_json", "notes": "notes_json",
}


def update_job(job_id: str, **fields: Any) -> None:
    """Persist selected fields (Pydantic models / dicts / lists are JSON-encoded)."""
    ensure_table()
    if not fields:
        return
    sets, params = [], []
    for field, value in fields.items():
        col = COLUMN_FOR_FIELD.get(field)
        if col is None:
            raise ValueError(f"unknown dossier job field: {field}")
        if col.endswith("_json"):
            value = _dumps(value) if value is not None else None
        sets.append(f"{col} = %s")
        params.append(value)
    sets.append("updated_at = %s")
    params.append(datetime.utcnow().isoformat())
    params.append(job_id)
    execute(f"UPDATE dossier_jobs SET {', '.join(sets)} WHERE id = %s", tuple(params))


def append_receipt(job_id: str, receipt: Receipt) -> None:
    """Read-modify-write under a process lock; recomputes totals."""
    ensure_table()
    with _receipt_lock:
        row = execute("SELECT receipts_json, totals_json FROM dossier_jobs WHERE id = %s", (job_id,), fetch="one")
        if row is None:
            return
        receipts = _loads(row.get("receipts_json"), [])
        receipts.append(receipt.model_dump())
        totals = _loads(row.get("totals_json"), {}) or {}
        totals = compute_totals(receipts, totals)
        execute(
            "UPDATE dossier_jobs SET receipts_json = %s, totals_json = %s, updated_at = %s WHERE id = %s",
            (_dumps(receipts), _dumps(totals), datetime.utcnow().isoformat(), job_id),
        )


def compute_totals(receipts: list[dict], base: Optional[dict] = None) -> dict:
    totals = dict(base or {})
    totals["llm_calls"] = sum(1 for r in receipts if r.get("kind", "llm") == "llm")
    totals["image_calls"] = sum(1 for r in receipts if r.get("kind") == "image")
    totals["input_tokens"] = sum(int(r.get("input_tokens") or 0) for r in receipts)
    totals["output_tokens"] = sum(int(r.get("output_tokens") or 0) for r in receipts)
    totals["cost_usd"] = round(sum(float(r.get("cost_usd") or 0.0) for r in receipts), 4)
    step_costs: dict[str, float] = {}
    for r in receipts:
        step_costs[r.get("step", "?")] = round(step_costs.get(r.get("step", "?"), 0.0) + float(r.get("cost_usd") or 0.0), 4)
    totals["step_costs_usd"] = step_costs
    totals.setdefault("step_durations_ms", {})
    totals.setdefault("duration_ms", 0)
    return totals


def add_note(job_id: str, kind: str, detail: str, **extra: Any) -> None:
    ensure_table()
    row = execute("SELECT notes_json FROM dossier_jobs WHERE id = %s", (job_id,), fetch="one")
    if row is None:
        return
    notes = _loads(row.get("notes_json"), [])
    notes.append({"ts": datetime.utcnow().isoformat(), "kind": kind, "detail": detail, **extra})
    execute("UPDATE dossier_jobs SET notes_json = %s WHERE id = %s", (_dumps(notes), job_id))


def record_step_duration(job_id: str, step: str, duration_ms: int) -> None:
    ensure_table()
    row = execute("SELECT totals_json FROM dossier_jobs WHERE id = %s", (job_id,), fetch="one")
    if row is None:
        return
    totals = _loads(row.get("totals_json"), {}) or {}
    durations = totals.get("step_durations_ms") or {}
    durations[step] = int(duration_ms)
    totals["step_durations_ms"] = durations
    totals["duration_ms"] = int(sum(durations.values()))
    execute("UPDATE dossier_jobs SET totals_json = %s WHERE id = %s", (_dumps(totals), job_id))
