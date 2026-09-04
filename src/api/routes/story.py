"""The story desk: many sources → story profiles → map → brief → spine → handoff to Wirecut.

POST /v1/story/jobs                     start (sources like a dossier, or from_job to reuse a dossier's documents)
GET  /v1/story/jobs                     list
GET  /v1/story/jobs/{id}                full job
GET  /v1/story/jobs/{id}/brief          the three options
POST /v1/story/jobs/{id}/brief          choose {option_key}
POST /v1/story/jobs/{id}/cancel | /resume
GET  /v1/story/jobs/{id}/handoff        the Wirecut contract (StoryHandoff)
GET  /v1/story/jobs/{id}/sources/{doc_key}   source text
GET  /v1/story/jobs/{id}/events         event ledger (also /v1/events/{id}/stream for SSE)
GET  /v1/story/handoff-schema           JSON schema of the contract
GET  /v1/story/demands                  what the downstream passes ask of the sources (from the registry)
"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from src.sources.schemas import SourceSpec
from src.story import runner
from src.story.demands import registry_demands
from src.story.schemas import StoryHandoff, StoryJob, StoryOptions
from src.story.store import create_job, get_job, list_jobs, update_job

router = APIRouter(prefix="/v1/story", tags=["story"])


class CreateStoryRequest(BaseModel):
    sources: list[SourceSpec] = Field(default_factory=list)
    from_job: Optional[str] = Field(default=None, description="reuse the documents of an existing dossier job")
    intent: Optional[str] = None
    audience: str = "executive"
    preset: Optional[str] = None
    length_seconds: Optional[int] = None
    autopilot: bool = False


class StoryChoiceRequest(BaseModel):
    option_key: str


def _load(job_id: str) -> StoryJob:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"story job {job_id} not found")
    return job


@router.post("/jobs")
def create(req: CreateStoryRequest):
    from src.executor.document_store import store_document
    from src.sources.resolve import resolve_sources

    documents: list[dict] = []
    if req.from_job:
        from src.dossier.store import get_job as get_dossier
        src = get_dossier(req.from_job)
        if src is None:
            raise HTTPException(status_code=404, detail=f"dossier job {req.from_job} not found")
        documents = list(src.documents)
    else:
        try:
            docs = resolve_sources(req.sources)
        except (ValueError, FileNotFoundError) as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        for d in docs:
            doc_id = store_document(title=d.title, text=d.text, author=d.creators or None, role="story_source")
            documents.append({**d.meta(), "executor_doc_id": doc_id})
    if not documents:
        raise HTTPException(status_code=400, detail="no documents")
    job = StoryJob(options=StoryOptions(intent=req.intent, audience=req.audience, preset=req.preset, length_seconds=req.length_seconds,
                                        autopilot=req.autopilot, from_job=req.from_job),
                   sources=[s.model_dump() for s in req.sources], documents=documents)
    create_job(job)
    runner.start(job.id)
    return {"job_id": job.id, "status": "queued", "documents": [{"key": d.get("key"), "title": d.get("title"), "char_count": d.get("char_count")} for d in documents]}


@router.get("/jobs")
def list_all(limit: int = 50):
    return {"jobs": [j.model_dump() for j in list_jobs(limit)]}


@router.get("/jobs/{job_id}")
def get_one(job_id: str):
    return _load(job_id).model_dump()


@router.get("/jobs/{job_id}/brief")
def get_brief(job_id: str):
    job = _load(job_id)
    if job.brief is None:
        raise HTTPException(status_code=409, detail=f"brief not ready (status={job.status}, step={job.step})")
    return {"options": [o.model_dump() for o in job.brief.options], "recommendation": job.brief.recommendation, "why": job.brief.why,
            "chosen_option": job.chosen_option, "status": job.status,
            "coverage": job.map.coverage if job.map else {}, "through_lines": [t.model_dump() for t in job.map.through_lines] if job.map else []}


@router.post("/jobs/{job_id}/brief")
def choose(job_id: str, req: StoryChoiceRequest):
    job = _load(job_id)
    if job.brief is None:
        raise HTTPException(status_code=409, detail="brief not ready")
    if req.option_key not in {o.key for o in job.brief.options}:
        raise HTTPException(status_code=400, detail=f"unknown option_key; choose one of {[o.key for o in job.brief.options]}")
    if job.status != "awaiting_brief":
        raise HTTPException(status_code=409, detail=f"job is not awaiting a brief (status={job.status})")
    update_job(job_id, chosen_option=req.option_key, status="spining", step="spine")
    from src.dossier import events
    events.emit(job_id, "note", phase="brief", detail=f"brief chosen: {req.option_key}", payload_json={"option_key": req.option_key})
    runner.start(job_id)
    return {"job_id": job_id, "status": "spining", "chosen_option": req.option_key}


@router.post("/jobs/{job_id}/cancel")
def cancel(job_id: str):
    _load(job_id)
    return {"job_id": job_id, "cancelled": runner.cancel(job_id)}


@router.post("/jobs/{job_id}/resume")
def resume(job_id: str):
    job = _load(job_id)
    if job.status in ("failed", "cancelled"):
        update_job(job_id, status="queued", error=None)
    return {"job_id": job_id, "started": runner.start(job_id)}


@router.get("/jobs/{job_id}/handoff", response_model=StoryHandoff)
def handoff(job_id: str):
    job = _load(job_id)
    if job.handoff is None:
        raise HTTPException(status_code=409, detail=f"handoff not ready (status={job.status}, step={job.step})")
    return job.handoff


@router.post("/jobs/{job_id}/rebuild-handoff", response_model=StoryHandoff)
def rebuild_handoff(job_id: str):
    """Re-verify every anchor byte-verbatim against the raw sources and rebuild the handoff (all sources listed, used flags, current doctrine hashes)."""
    from src.story import steps

    job = _load(job_id)
    if job.spine is None:
        raise HTTPException(status_code=409, detail="no spine yet")
    docs = runner.load_documents(job)
    profiles, dropped = steps.reverify_profiles(job, docs)
    job = update_job(job_id, profiles=[p.model_dump() for p in profiles])
    handoff = steps.build_handoff(job, docs)
    update_job(job_id, handoff=handoff)
    from src.dossier import events
    events.emit(job_id, "note", phase="handoff", detail=f"handoff rebuilt: anchors re-cut byte-verbatim, {dropped} dropped")
    return handoff


@router.get("/jobs/{job_id}/sources/{doc_key}", response_class=PlainTextResponse)
def source_text(job_id: str, doc_key: str):
    job = _load(job_id)
    for d in runner.load_documents(job):
        if d.key == doc_key:
            return d.text
    raise HTTPException(status_code=404, detail=f"source {doc_key} not in job")


@router.get("/jobs/{job_id}/events")
def job_events(job_id: str, after: int = 0):
    from src.events.store import list_events

    _load(job_id)
    return [e.model_dump() if hasattr(e, "model_dump") else e for e in list_events(job_id, after_seq=after)]


@router.get("/handoff-schema")
def handoff_schema():
    return StoryHandoff.model_json_schema()


@router.get("/demands")
def demands():
    return [{"engine_key": k, "engine_name": n, "demands": d} for k, n, d in registry_demands()]
