"""Dossier routes — The Analyst meaning-making workflow (owner: dossier agent).

Contract: communications/IMPLEMENTATION_TRACKER.md §4.

POST /v1/dossier/jobs                      start a run (daemon thread); entry = use | chosen | material, use_frame, path (brief v2 lanes)
GET  /v1/dossier/catalog?audience=&corpus_chars=&n_docs=   the purpose-first engine catalog for the picker (groups, recipes, excluded)
GET  /v1/dossier/jobs                      newest first
GET  /v1/dossier/jobs/{id}                 full DossierJob
GET  /v1/dossier/jobs/{id}/brief           {version, entry, options, recommendation, defaults, notes, chosen_option, status}
POST /v1/dossier/jobs/{id}/brief           choose an option → resumes at plan; overrides.path (edited how-line) fixes the plan's path
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
from typing import Optional

from pydantic import BaseModel
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse

from src.dossier import events as dossier_events
from src.dossier.schemas import (AUDIENCES, BriefChoiceRequest, CreateDossierRequest, DEPTHS, DossierJob,
                                 DossierOptions, ENTRIES, OutputOptions, Shape, USE_KINDS)
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


@router.post("/uploads")
async def upload_bundle(files: list[UploadFile] = File(...), title: str = Form("")):
    """Several local files (PDF / MD / TXT) -> one bundle, stored like an exemplar."""
    from src.sources.uploads import build_bundle
    from src.sources.exemplar_store import upsert_exemplar
    pairs = []
    for f in files:
        data = await f.read()
        if not data:
            continue
        pairs.append((f.filename or "document", data))
    if not pairs:
        raise HTTPException(status_code=400, detail="no files received")
    try:
        name, text, meta = build_bundle(pairs, title)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    rec = upsert_exemplar(name, text, meta["title"], f"uploaded bundle · {meta['document_count']} file(s)", meta["document_count"])
    return rec | {"documents": meta["documents"], "source": "upload"}


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


OWN_PATH_KEY = "own_path"


def validate_lane(req: CreateDossierRequest) -> dict:
    """entry / use_frame / path of a create request, checked (raises ValueError with the reader's reason)."""
    entry = req.entry or ("material" if req.autopilot else "use")
    if entry not in ENTRIES:
        raise ValueError(f"entry must be one of {ENTRIES}")
    use_frame = req.use_frame
    if use_frame and use_frame.use_kind and use_frame.use_kind not in USE_KINDS:
        raise ValueError(f"use_frame.use_kind must be one of {USE_KINDS} (or null)")
    path = req.path
    if entry == "chosen":
        if path is None or (not path.steps and not path.chain_key):
            raise ValueError("entry = 'chosen' needs path.steps (1-4 executable engines) or path.chain_key (a recipe)")
        from src.dossier.catalog import resolve_path_request

        resolve_path_request(path, req.audience or "executive")  # raises ValueError on a non-executable step
    elif path is not None and (path.steps or path.chain_key):
        from src.dossier.catalog import resolve_path_request

        resolve_path_request(path, req.audience or "executive")
    return {"entry": entry, "use_frame": use_frame, "path": path}


@router.get("/catalog")
def catalog(audience: str = "executive", corpus_chars: Optional[int] = None, n_docs: Optional[int] = None,
            same_author: Optional[bool] = None):
    """The purpose-first engine catalog for the picker (DESIGN_brief_deliverables §C3/§D): groups, recipes, exclusions."""
    from src.dossier.catalog import purpose_catalog

    if audience not in AUDIENCES:
        raise HTTPException(status_code=400, detail=f"audience must be one of {AUDIENCES}")
    return purpose_catalog(audience=audience, corpus_chars=corpus_chars, n_docs=n_docs, same_author=same_author)


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
        lane = validate_lane(req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
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
        output=req.output or OutputOptions(), spend_cap_usd=req.spend_cap_usd, autopilot=(lane["entry"] == "material"),
        image_provider=req.image_provider, entry=lane["entry"], use_frame=lane["use_frame"], path=lane["path"],
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
    b = job.brief
    return {"version": b.version, "entry": b.entry, "options": [o.model_dump() for o in b.options],
            "recommendation": b.recommendation.model_dump() if b.recommendation else None,
            "defaults": b.defaults.model_dump(), "notes": b.notes,
            "chosen_option": job.chosen_option, "status": job.status}


@router.post("/jobs/{job_id}/brief")
def choose_brief(job_id: str, req: BriefChoiceRequest):
    job = _load(job_id)
    if job.brief is None:
        raise HTTPException(status_code=409, detail="brief not ready")
    keys = [o.key for o in job.brief.options]
    own_path = req.option_key == OWN_PATH_KEY and bool((req.overrides or {}).get("path"))
    if req.option_key not in keys and not own_path:
        raise HTTPException(status_code=400, detail=f"unknown option_key; choose one of {keys} (or '{OWN_PATH_KEY}' with overrides.path)")
    if job.status not in ("awaiting_brief",):
        raise HTTPException(status_code=409, detail=f"job is not awaiting a brief (status={job.status})")
    options = job.options
    brief = job.brief
    overrides = dict(req.overrides or {})
    path_override = overrides.pop("path", None)
    if overrides:
        data = options.model_dump()
        for k, v in overrides.items():
            if k == "output" and isinstance(v, dict):
                data["output"] = {**data["output"], **v}
            elif k == "figures":  # the brief step's dial: a top-level alias of output.figures
                data["output"] = {**data["output"], "figures": int(v)}
            elif k in data:
                data[k] = v
        if data.get("audience") not in AUDIENCES or data.get("depth") not in DEPTHS:
            raise HTTPException(status_code=400, detail="overrides carry an invalid audience or depth")
        options = DossierOptions.model_validate(data)
    option = brief.option(req.option_key)
    if option is None and own_path:
        # "I know the analysis I want" from the brief step: a fourth card whose deliverable the brief step did not write
        from src.dossier.schemas import BriefOption, Path as BriefPath

        option = BriefOption(key=OWN_PATH_KEY, title="Your own path", deliverable_kind="case_file", use_kind="learn",
                             deliverable="A dossier along the path you chose; the desk writes its shape from what the engines return.",
                             shape=Shape(), path=BriefPath(), best_when="Pick this when you know the analysis you want.",
                             notes=["own path: no deliverable framing was written by the brief desk"])
        brief.options.append(option)
    if path_override is not None:
        # the card's "how ▸ edit": the edited steps become the fixed path (lane 2 semantics) and are stored on the option
        from src.dossier.catalog import resolve_path_request
        from src.dossier.schemas import PathRequest

        try:
            preq = PathRequest.model_validate(path_override if isinstance(path_override, dict) else {"steps": path_override})
            resolved = resolve_path_request(preq, options.audience)
        except (ValueError, TypeError) as exc:
            raise HTTPException(status_code=400, detail=f"overrides.path rejected: {exc}")
        options.path = preq
        options.entry = "chosen"
        options.depth = resolved.depth
        if option is not None:
            option.path = resolved
            option.notes.append("path edited by the requester before planning")
            from src.dossier.catalog import estimate_path
            from src.dossier.common import engine_catalog
            by_key = {e["engine_key"]: e for e in engine_catalog()}
            corpus_chars = sum(int(d.get("char_count") or 0) for d in job.documents)
            option.est_cost_usd, option.est_minutes, option.est_llm_calls = estimate_path(resolved, corpus_chars, by_key)
    elif option is not None and option.version >= 2 and option.path.steps and "depth" not in overrides:
        options.depth = option.path.depth  # the card's own weight is the run's depth
    update_job(job_id, chosen_option=req.option_key, options=options, brief=brief, status="planning", step="plan")
    dossier_events.emit(job_id, "note", phase="brief", detail=f"brief chosen: {req.option_key}" + (" (path edited)" if path_override is not None else ""),
                        payload_json={"option_key": req.option_key, "overrides": req.overrides or {}})
    runner.start(job_id)
    return {"job_id": job_id, "status": "planning", "chosen_option": req.option_key, "console_url": f"/console/{job_id}",
            "option": option.model_dump() if option is not None else None}


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
    from src.dossier import blob_store
    from src.dossier.common import job_dir

    path = job.paths.get(kind)
    target = Path(path) if path else job_dir(job.id) / f"dossier.{kind}"
    if not target.exists():
        # The disk is wiped on deploy; the bytes live in the blob store (2026-09-04).
        if not blob_store.ensure_file(target, f"dossier:{job.id}:{kind}"):
            alt = job_dir(job.id) / f"dossier.{kind}"
            if not blob_store.ensure_file(alt, f"dossier:{job.id}:{kind}"):
                raise HTTPException(status_code=404, detail=f"dossier.{kind} not available (status={job.status})")
            target = alt
    return target


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

    name = Path(filename).name
    path = job_dir(job_id) / "figures" / name
    if not path.exists():
        # Restore through the figure store (blob-backed) using the job's figure record.
        from src.images.storage import figure_mime, figure_path

        job = get_job(job_id)
        stem = name.rsplit(".", 1)[0]
        for fig in (job.figures if job else []):
            fig_name = Path(fig.path).name if fig.path else ""
            if fig.figure_id and (fig_name == name or fig.key == stem):
                try:
                    p = figure_path(fig.figure_id)
                    return FileResponse(str(p), media_type=figure_mime(fig.figure_id))
                except (FileNotFoundError, ValueError):
                    continue
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


# ── Plates (PLATES agent, V1) — a standalone capability over a finished job ─────────────────────────
# POST /v1/dossier/jobs/{id}/plates {n?: 1-3, perspectives?: [...], provider?}   plan + render in a daemon thread; events under phase "plates"
# GET  /v1/dossier/jobs/{id}/plates                                              {job_id, running, run, plates: [Plate…]}
# GET  /v1/dossier/jobs/{id}/plates/{key}.jpg                                    the kept 4K render (jpg/png/webp by content)
# DELETE /v1/dossier/jobs/{id}/plates                                            forget the plates (files stay on disk)

class PlatesRequest(BaseModel):
    n: Optional[int] = None
    perspectives: Optional[list[str]] = None
    provider: Optional[str] = None


def _plates_thread(job_id: str, n: int, perspectives: Optional[list[str]], provider: Optional[str]) -> None:
    import threading

    from src.dossier import plate_store
    from src.dossier.plates import run_plates

    def _work() -> None:
        try:
            job = get_job(job_id)
            if job is None:
                return
            run_plates(job, n, perspectives=perspectives, provider=provider, persist=lambda p: plate_store.upsert_plate(job_id, p))
        except Exception as exc:  # the skip law: the thread never dies loudly
            logger.warning(f"plates run failed for {job_id}: {exc}", exc_info=True)
            dossier_events.emit(job_id, "call_failed", phase="plates", label="plates", detail=f"plates run failed: {exc}")
        finally:
            plate_store.mark_done(job_id)

    threading.Thread(target=_work, name=f"plates-{job_id}", daemon=True).start()


@router.post("/jobs/{job_id}/plates", status_code=202)
def start_plates(job_id: str, req: Optional[PlatesRequest] = None):
    from src.dossier import plate_store
    from src.dossier.plates import MAX_PLATES

    job = _load(job_id)
    if not job.analysis:
        raise HTTPException(status_code=409, detail=f"the job has no analysis prose yet (status={job.status}); plates need a finished analysis")
    req = req or PlatesRequest()
    perspectives = [str(p).strip() for p in (req.perspectives or []) if str(p).strip()][:MAX_PLATES] or None
    n = len(perspectives) if perspectives else int(req.n or 2)
    if not (1 <= n <= MAX_PLATES):
        raise HTTPException(status_code=400, detail=f"n must be 1..{MAX_PLATES}")
    if req.provider:
        from src.images import providers as P
        if req.provider not in P.PROVIDERS:
            raise HTTPException(status_code=400, detail=f"unknown provider {req.provider!r}; known: {sorted(P.PROVIDERS)}")
    if not plate_store.mark_running(job_id, n, perspectives):
        raise HTTPException(status_code=409, detail="a plates run is already in flight for this job")
    _plates_thread(job_id, n, perspectives, req.provider)
    return {"job_id": job_id, "status": "started", "n": n, "perspectives": perspectives or [], "phase": "plates"}


@router.get("/jobs/{job_id}/plates")
def get_plates(job_id: str):
    from src.dossier import plate_store

    _load(job_id)
    plates = plate_store.list_plates(job_id)
    state = plate_store.run_state(job_id)
    return {"job_id": job_id, "running": state is not None, "run": state,
            "plates": [p.model_dump(exclude={"prompt"}) | {"prompt_chars": len(p.prompt or "")} for p in plates]}


@router.delete("/jobs/{job_id}/plates")
def delete_plates(job_id: str):
    from src.dossier import plate_store

    _load(job_id)
    if plate_store.run_state(job_id) is not None:
        raise HTTPException(status_code=409, detail="a plates run is in flight; wait for it to finish")
    return {"job_id": job_id, "deleted": plate_store.delete_plates(job_id)}


@router.get("/jobs/{job_id}/plates/{filename}")
def get_plate_image(job_id: str, filename: str):
    from src.dossier import plate_store
    from src.dossier.common import job_dir

    name = Path(filename).name
    key = name.rsplit(".", 1)[0] if "." in name else name
    candidates = [job_dir(job_id) / "plates" / name]
    plate = plate_store.get_plate(job_id, key)
    if plate and plate.path:
        candidates.insert(0, Path(plate.path))
    for ext in ("jpg", "png", "webp", "jpeg"):
        candidates.append(job_dir(job_id) / "plates" / f"{key}.{ext}")
    if not any(c.exists() for c in candidates):
        from src.dossier import blob_store

        for c in candidates:
            if blob_store.ensure_file(c, f"plate:{job_id}:{c.name}"):
                break
    for path in candidates:
        if path.exists() and path.is_file():
            media = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(path.suffix.lower(), "image/png")
            return FileResponse(str(path), media_type=media, filename=f"{job_id}-{key}{path.suffix}",
                                headers={"Cache-Control": "public, max-age=3600"})
    if plate and plate.figure_id:
        from src.images.storage import figure_mime, figure_path
        try:
            p = figure_path(plate.figure_id)
            return FileResponse(str(p), media_type=figure_mime(plate.figure_id), filename=f"{job_id}-{key}{p.suffix}")
        except (FileNotFoundError, ValueError):
            pass
    raise HTTPException(status_code=404, detail="plate not found")


# ── Admin: re-hydrate durable bytes and job records (2026-09-04) ──────────────
import os as _os

from fastapi import Header, Request


def _admin_guard(token: str | None) -> None:
    expected = _os.environ.get("ADMIN_TOKEN")
    if not expected or token != expected:
        raise HTTPException(status_code=403, detail="admin token required")


@router.put("/admin/blobs/{blob_key:path}")
async def admin_put_blob(blob_key: str, request: Request, x_admin_token: str | None = Header(default=None)):
    """Store raw bytes under a blob key (figure:<id> · figure-meta:<id> · plate:<job>:<file> · dossier:<job>:<kind>)."""
    _admin_guard(x_admin_token)
    from src.dossier import blob_store

    data = await request.body()
    if not data:
        raise HTTPException(status_code=400, detail="empty body")
    blob_store.put_blob(blob_key, request.headers.get("content-type", "application/octet-stream"), data)
    return {"blob_key": blob_key, "size": len(data)}


@router.get("/admin/blobs")
def admin_list_blobs(prefix: str = "", x_admin_token: str | None = Header(default=None)):
    _admin_guard(x_admin_token)
    from src.dossier import blob_store

    return blob_store.list_keys(prefix)


@router.put("/admin/jobs/{job_id}")
async def admin_put_job(job_id: str, request: Request, x_admin_token: str | None = Header(default=None)):
    """Import (or replace) a dossier job record from its job.json backup."""
    _admin_guard(x_admin_token)
    from src.dossier import store as _store

    payload = await request.json()
    job = DossierJob.model_validate(payload)
    if job.id != job_id:
        raise HTTPException(status_code=400, detail="job id mismatch")
    if _store.get_job(job_id) is None:
        _store.create_job(job)
    else:
        fields = {k: v for k, v in job.model_dump().items() if k not in ("id", "created_at")}
        _store.update_job(job_id, **fields)
    return {"job_id": job_id, "status": job.status}


# ── Admin: scan and purge by term (2026-09-04, "cleanse the app of Kering / de Meo") ─────────────
def _text_has(text: str, terms: list[str]) -> list[str]:
    low = (text or "").lower()
    return [t for t in terms if t.lower() in low]


@router.get("/admin/scan")
def admin_scan(terms: str, x_admin_token: str | None = Header(default=None)):
    """Everything in the app that mentions any of the comma-separated terms: dossier jobs (record + plates), story jobs, exemplars, stored documents."""
    import json as _json

    _admin_guard(x_admin_token)
    from src.dossier import plate_store
    from src.dossier.store import list_jobs as _list
    from src.executor.document_store import get_document_text, list_documents
    from src.sources.exemplar_store import get_db_exemplar, list_db_exemplars
    from src.story.store import get_job as get_story, list_jobs as list_story

    words = [t.strip() for t in terms.split(",") if t.strip()]
    out: dict = {"terms": words, "dossier_jobs": [], "story_jobs": [], "exemplars": [], "documents": []}
    for summary in _list(limit=500):
        job = get_job(summary.id)
        if job is None:
            continue
        blob = _json.dumps(job.model_dump(), ensure_ascii=False, default=str)
        hits = _text_has(blob, words)
        plates = plate_store.list_plates(summary.id)
        phits = _text_has(_json.dumps([p.model_dump() for p in plates], ensure_ascii=False, default=str), words)
        doc_titles = [d.get("title", "") for d in job.documents]
        if hits or phits:
            out["dossier_jobs"].append({"id": summary.id, "status": job.status, "hits": sorted(set(hits + phits)), "count": sum(blob.lower().count(w.lower()) for w in words),
                                       "documents": doc_titles, "plates": [p.key for p in plates], "analysis_job_id": job.analysis_job_id})
    for s in list_story(limit=500):
        job = get_story(s.id)
        if job is None:
            continue
        blob = _json.dumps(job.model_dump(), ensure_ascii=False, default=str)
        hits = _text_has(blob, words)
        if hits:
            out["story_jobs"].append({"id": s.id, "status": job.status, "hits": hits, "count": sum(blob.lower().count(w.lower()) for w in words)})
    for ex in list_db_exemplars():
        text = get_db_exemplar(ex.get("name", "")) or ""
        hits = _text_has(text + " " + _json.dumps(ex, default=str), words)
        if hits:
            out["exemplars"].append({"name": ex.get("name"), "hits": hits, "count": sum(text.lower().count(w.lower()) for w in words)})
    for d in list_documents():
        text = get_document_text(d.get("id") or d.get("doc_id") or "") or ""
        hits = _text_has(text + " " + str(d.get("title", "")), words)
        if hits:
            out["documents"].append({"id": d.get("id") or d.get("doc_id"), "title": d.get("title"), "role": d.get("role"), "hits": hits, "count": sum(text.lower().count(w.lower()) for w in words)})
    return out


def _purge_dossier_job(job_id: str) -> dict:
    from src.dossier import blob_store, plate_store
    from src.executor.db import execute
    from src.executor.document_store import delete_document

    job = get_job(job_id)
    if job is None:
        return {"id": job_id, "deleted": False}
    removed: dict = {"id": job_id, "plates": plate_store.delete_plates(job_id), "documents": 0, "executor_job": False, "blobs": 0, "events": 0}
    for d in job.documents:
        if d.get("executor_doc_id"):
            try:
                removed["documents"] += int(bool(delete_document(d["executor_doc_id"])))
            except Exception:  # noqa: BLE001
                pass
    if job.analysis_job_id:
        try:
            from src.executor.job_manager import delete_job as delete_exec_job
            removed["executor_job"] = bool(delete_exec_job(job.analysis_job_id))
        except Exception:  # noqa: BLE001
            removed["executor_job"] = False
    for prefix in (f"dossier:{job_id}:", f"plate:{job_id}:", f"figure:{job_id}-", f"figure-meta:{job_id}-"):
        for row in blob_store.list_keys(prefix):
            blob_store.delete_blob(row["blob_key"])
            removed["blobs"] += 1
    try:
        n = execute("SELECT COUNT(*) AS n FROM run_events WHERE job_id = %s", (job_id,), fetch="one") or {}
        execute("DELETE FROM run_events WHERE job_id = %s", (job_id,))
        removed["events"] = int(n.get("n") or 0)
    except Exception:  # noqa: BLE001
        pass
    execute("DELETE FROM dossier_jobs WHERE id = %s", (job_id,))
    removed["deleted"] = True
    return removed


@router.delete("/admin/jobs/{job_id}")
def admin_purge_job(job_id: str, x_admin_token: str | None = Header(default=None)):
    """Delete a dossier job and everything it owns: plates, blobs, events, the executor sub-run, its stored source documents."""
    _admin_guard(x_admin_token)
    return _purge_dossier_job(job_id)


@router.delete("/admin/story-jobs/{job_id}")
def admin_purge_story_job(job_id: str, x_admin_token: str | None = Header(default=None)):
    _admin_guard(x_admin_token)
    from src.executor.db import execute
    from src.executor.document_store import delete_document
    from src.story.store import get_job as get_story

    job = get_story(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="story job not found")
    docs = 0
    for d in job.documents:
        if d.get("executor_doc_id"):
            try:
                docs += int(bool(delete_document(d["executor_doc_id"])))
            except Exception:  # noqa: BLE001
                pass
    execute("DELETE FROM run_events WHERE job_id = %s", (job_id,))
    execute("DELETE FROM story_jobs WHERE id = %s", (job_id,))
    return {"id": job_id, "deleted": True, "documents": docs}


@router.delete("/admin/documents/{doc_id}")
def admin_purge_document(doc_id: str, x_admin_token: str | None = Header(default=None)):
    _admin_guard(x_admin_token)
    from src.executor.document_store import delete_document

    return {"id": doc_id, "deleted": bool(delete_document(doc_id))}
