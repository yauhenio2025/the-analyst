"""The readings ledger's routes (2026-09-07): what has been read about a person or a text, by whom and when; the reading itself; a backfill."""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException

from src.readings.registry import index_job, reading, readings_for

router = APIRouter(prefix="/readings", tags=["readings"])


@router.get("")
def list_readings(person: Optional[str] = None, text: Optional[str] = None, job: Optional[str] = None, limit: int = 50):
    if not (person or text or job):
        raise HTTPException(status_code=400, detail="give person=, text= (a uid) or job=")
    return readings_for(person=person, text=text, job=job, limit=limit)


@router.get("/{job_id}/{phase}")
def one_reading(job_id: str, phase: str):
    r = reading(job_id, phase)
    if r is None:
        raise HTTPException(status_code=404, detail="no such reading")
    return r


@router.post("/index/{job_id}")
def index(job_id: str):
    """Index a finished job's phases (a backfill for runs made before the ledger; idempotent)."""
    from src.dossier.store import get_job
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="no such job")
    return {"job_id": job_id, "indexed": index_job(job.model_dump())}
