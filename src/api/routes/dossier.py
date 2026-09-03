"""Dossier routes — The Analyst meaning-making workflow (owner: dossier agent).

Contract: communications/IMPLEMENTATION_TRACKER.md §4.

POST /v1/dossier/jobs                      start a run (daemon thread)
GET  /v1/dossier/jobs                      newest first
GET  /v1/dossier/jobs/{id}                 full DossierJob
GET  /v1/dossier/jobs/{id}/brief           {options, defaults}
POST /v1/dossier/jobs/{id}/brief           choose an option → resumes at plan
GET  /v1/dossier/jobs/{id}/events?after=   JSON poll of the event ledger (SSE lives with the events agent)
GET  /v1/dossier/jobs/{id}/receipts
GET  /v1/dossier/jobs/{id}/dossier.html|pdf|md
GET  /v1/dossier/jobs/{id}/figures/{filename}
POST /v1/dossier/jobs/{id}/cancel
POST /v1/dossier/jobs/{id}/resume
GET  /v1/dossier/exemplars
"""
from __future__ import annotations

import logging
from pathlib import Path

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse

from src.dossier import events as dossier_events
from src.dossier.schemas import (AUDIENCES, BriefChoiceRequest, CreateDossierRequest, DEPTHS, DossierJob,
                                 DossierOptions, OutputOptions)
from src.dossier import runner
from src.dossier.store import create_job, get_job, list_jobs, update_job

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/dossier", tags=["dossier"])


@router.get("/health")
def dossier_health():
    return {"ok": True, "component": "dossier", "status": "ready",
            "events_store": "fallback" if dossier_events.using_fallback() else "src.events.store"}


class ExemplarUpload(BaseModel):
    name: str
    text: str
    title: str = ""
    description: str = ""
    document_count: int = 1


@router.post("/exemplars")
def upload_exemplar(body: ExemplarUpload):
    """Store an exemplar input in the executor DB (texts are not in git)."""
    from src.sources.exemplar_store import upsert_exemplar
    from src.sources.stacks import looks_like_stacks_export, split_stacks_export
    if len(body.text.strip()) < 200:
        raise HTTPException(status_code=400, detail="exemplar text too short")
    n_docs = len(split_stacks_export(body.text)) if looks_like_stacks_export(body.text) else body.document_count
    return upsert_exemplar(body.name, body.text, body.title, body.description, n_docs or 1)


@router.delete("/exemplars/{name}")
def remove_exemplar(name: str):
    from src.sources.exemplar_store import delete_exemplar
    if not delete_exemplar(name):
        raise HTTPException(status_code=404, detail="exemplar not found")
    return {"deleted": name}


@router.get("/exemplars")
def exemplars():
    from src.sources.resolve import list_exemplars

    return {"exemplars": list_exemplars()}


def _load(job_id: str) -> DossierJob:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"dossier job not found: {job_id}")
    return job


@router.post("/jobs")
def create(req: CreateDossierRequest):
    from src.executor.document_store import store_document
    from src.sources.resolve import resolve_sources
    from src.sources.stacks import StacksUnavailable

    if req.audience and req.audience not in AUDIENCES:
        raise HTTPException(status_code=400, detail=f"audience must be one of {AUDIENCES}")
    if req.depth and req.depth not in DEPTHS:
        raise HTTPException(status_code=400, detail=f"depth must be one of {DEPTHS}")
    try:
        docs = resolve_sources(req.sources)
    except StacksUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if not docs:
        raise HTTPException(status_code=400, detail="no documents resolved from sources")

    options = DossierOptions(
        intent=req.intent, audience=req.audience or "executive", depth=req.depth or "simple",
        output=req.output or OutputOptions(), spend_cap_usd=req.spend_cap_usd, autopilot=req.autopilot,
        image_provider=req.image_provider,
    )
    job = DossierJob(options=options, sources=[s.model_dump() for s in req.sources])
    documents = []
    for d in docs:
        doc_id = store_document(title=d.title, text=d.text, author=d.creators or None, role="dossier_source")
        documents.append({**d.meta(), "executor_doc_id": doc_id})
    job.documents = documents
    create_job(job)
    runner.start(job.id)
    return {"job_id": job.id, "status": "queued", "console_url": f"/console/{job.id}",
            "documents": [{"key": d["key"], "title": d["title"], "char_count": d["char_count"]} for d in documents]}


@router.get("/jobs")
def list_all(limit: int = 50):
    return {"jobs": [j.model_dump() for j in list_jobs(limit=limit)]}


@router.get("/jobs/{job_id}")
def get_one(job_id: str):
    return _load(job_id).model_dump()


@router.get("/jobs/{job_id}/brief")
def get_brief(job_id: str):
    job = _load(job_id)
    if job.brief is None:
        raise HTTPException(status_code=409, detail=f"brief not ready (status={job.status}, step={job.step})")
    return {"options": [o.model_dump() for o in job.brief.options], "defaults": job.brief.defaults.model_dump(),
            "chosen_option": job.chosen_option, "status": job.status}


@router.post("/jobs/{job_id}/brief")
def choose_brief(job_id: str, req: BriefChoiceRequest):
    job = _load(job_id)
    if job.brief is None:
        raise HTTPException(status_code=409, detail="brief not ready")
    keys = [o.key for o in job.brief.options]
    if req.option_key not in keys:
        raise HTTPException(status_code=400, detail=f"unknown option_key; choose one of {keys}")
    if job.status not in ("awaiting_brief",):
        raise HTTPException(status_code=409, detail=f"job is not awaiting a brief (status={job.status})")
    options = job.options
    if req.overrides:
        data = options.model_dump()
        for k, v in req.overrides.items():
            if k == "output" and isinstance(v, dict):
                data["output"] = {**data["output"], **v}
            elif k in data:
                data[k] = v
        if data.get("audience") not in AUDIENCES or data.get("depth") not in DEPTHS:
            raise HTTPException(status_code=400, detail="overrides carry an invalid audience or depth")
        options = DossierOptions.model_validate(data)
    update_job(job_id, chosen_option=req.option_key, options=options, status="planning", step="plan")
    dossier_events.emit(job_id, "note", phase="brief", detail=f"brief chosen: {req.option_key}",
                        payload_json={"option_key": req.option_key, "overrides": req.overrides or {}})
    runner.start(job_id)
    return {"job_id": job_id, "status": "planning", "chosen_option": req.option_key, "console_url": f"/console/{job_id}"}


@router.get("/jobs/{job_id}/events")
def get_events(job_id: str, after: int = 0, limit: int = 500):
    _load(job_id)
    evs = dossier_events.list_events(job_id, after)[:limit]
    last = max((int(e.get("seq", 0) or 0) for e in evs), default=after)
    return {"job_id": job_id, "events": evs, "last_seq": last, "store": "fallback" if dossier_events.using_fallback() else "src.events.store"}


@router.get("/jobs/{job_id}/receipts")
def get_receipts(job_id: str):
    job = _load(job_id)
    return {"job_id": job_id, "receipts": [r.model_dump() for r in job.receipts], "totals": job.totals.model_dump()}


def _file(job: DossierJob, kind: str) -> Path:
    path = job.paths.get(kind)
    if not path or not Path(path).exists():
        raise HTTPException(status_code=404, detail=f"dossier.{kind} not available (status={job.status})")
    return Path(path)


@router.get("/jobs/{job_id}/dossier.html", response_class=HTMLResponse)
def get_html(job_id: str):
    job = _load(job_id)
    text = _file(job, "html").read_text(encoding="utf-8")
    text = text.replace('src="figures/', f'src="/v1/dossier/jobs/{job_id}/figures/')
    return HTMLResponse(text)


@router.get("/jobs/{job_id}/dossier.pdf")
def get_pdf(job_id: str):
    job = _load(job_id)
    return FileResponse(str(_file(job, "pdf")), media_type="application/pdf", filename=f"{job_id}.pdf")


@router.get("/jobs/{job_id}/dossier.md", response_class=PlainTextResponse)
def get_md(job_id: str):
    job = _load(job_id)
    return PlainTextResponse(_file(job, "md").read_text(encoding="utf-8"), media_type="text/markdown")


@router.get("/jobs/{job_id}/figures/{filename}")
def get_figure(job_id: str, filename: str):
    from src.dossier.common import job_dir

    path = job_dir(job_id) / "figures" / Path(filename).name
    if not path.exists():
        raise HTTPException(status_code=404, detail="figure not found")
    media = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(path.suffix.lower(), "image/png")
    return FileResponse(str(path), media_type=media)


@router.post("/jobs/{job_id}/cancel")
def cancel(job_id: str):
    _load(job_id)
    runner.cancel(job_id)
    return {"job_id": job_id, "status": "cancelled"}


@router.post("/jobs/{job_id}/resume")
def resume(job_id: str):
    job = _load(job_id)
    if job.status == "done":
        return {"job_id": job_id, "status": "done", "resumed": False}
    if job.status == "awaiting_brief":
        raise HTTPException(status_code=409, detail="awaiting a brief choice; POST /brief first")
    if job.status in ("failed", "cancelled"):
        update_job(job_id, status=runner.STATUS_FOR_STEP.get(job.step, "queued"), error=None)
    started = runner.resume(job_id)
    return {"job_id": job_id, "status": job.status, "resumed": started, "from_step": job.step}
