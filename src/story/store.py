"""Story job store: one JSON document per job in `story_jobs` (Postgres or SQLite)."""
from __future__ import annotations

import json
import logging
import threading
from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel

from src.dossier.store import compute_totals
from src.executor.db import execute, init_db

from .schemas import Receipt, StoryJob, StoryJobSummary

logger = logging.getLogger(__name__)
_ready = False
_lock = threading.Lock()


def ensure_table() -> None:
    global _ready
    if _ready:
        return
    with _lock:
        if _ready:
            return
        init_db()
        execute("CREATE TABLE IF NOT EXISTS story_jobs (id TEXT PRIMARY KEY, status TEXT, step TEXT, created_at TEXT, updated_at TEXT, job_json TEXT)")
        _ready = True


def _dumps(job: StoryJob) -> str:
    return json.dumps(job.model_dump(), ensure_ascii=False, default=str)


def create_job(job: StoryJob) -> StoryJob:
    ensure_table()
    now = datetime.now(timezone.utc).isoformat()
    job.created_at = now
    job.updated_at = now
    execute("INSERT INTO story_jobs (id, status, step, created_at, updated_at, job_json) VALUES (%s, %s, %s, %s, %s, %s)",
            (job.id, job.status, job.step, now, now, _dumps(job)))
    return job


def get_job(job_id: str) -> Optional[StoryJob]:
    ensure_table()
    row = execute("SELECT job_json FROM story_jobs WHERE id = %s", (job_id,), fetch="one")
    if not row:
        return None
    return StoryJob.model_validate(json.loads(row["job_json"]))


def save_job(job: StoryJob) -> None:
    ensure_table()
    job.updated_at = datetime.now(timezone.utc).isoformat()
    execute("UPDATE story_jobs SET status = %s, step = %s, updated_at = %s, job_json = %s WHERE id = %s",
            (job.status, job.step, job.updated_at, _dumps(job), job.id))


def update_job(job_id: str, **fields: Any) -> StoryJob:
    """Read-modify-write under a process lock (the runner is single-writer per job; receipts share the lock)."""
    with _lock:
        job = get_job(job_id)
        if job is None:
            raise KeyError(job_id)
        data = job.model_dump()
        for k, v in fields.items():
            data[k] = v.model_dump() if isinstance(v, BaseModel) else v
        job = StoryJob.model_validate(data)
        save_job(job)
        return job


def append_receipt(job_id: str, receipt: Receipt) -> None:
    with _lock:
        job = get_job(job_id)
        if job is None:
            return
        receipts = [r.model_dump() for r in job.receipts] + [receipt.model_dump()]
        totals = compute_totals(receipts, job.totals.model_dump())
        data = job.model_dump()
        data["receipts"] = receipts
        data["totals"] = totals
        save_job(StoryJob.model_validate(data))


def list_jobs(limit: int = 50) -> list[StoryJobSummary]:
    ensure_table()
    rows = execute("SELECT job_json FROM story_jobs ORDER BY created_at DESC LIMIT %s", (limit,), fetch="all") or []
    out = []
    for r in rows:
        try:
            j = StoryJob.model_validate(json.loads(r["job_json"]))
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"bad story job row: {exc}")
            continue
        out.append(StoryJobSummary(id=j.id, status=j.status, step=j.step, created_at=j.created_at, updated_at=j.updated_at,
                                   n_documents=len(j.documents), n_elements=sum(len(p.elements) for p in j.profiles),
                                   intent=j.options.intent, chosen_option=j.chosen_option, cost_usd=j.totals.cost_usd))
    return out
