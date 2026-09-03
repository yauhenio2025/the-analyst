"""DossierRunner — the eight steps in a daemon thread, persisted after every step, resumable.

Lifted from veo2/engine/ops.py: params stored verbatim on the job so a restart
can resume from the recorded step; every step emits phase_started /
phase_finished; failures classify the run `failed` with the error recorded.
"""
from __future__ import annotations

import logging
import threading
import time
import traceback
from typing import Callable, Optional

from src.dossier import events
from src.dossier.common import load_documents
from src.dossier.schemas import DossierJob, STEPS
from src.dossier.store import add_note, get_job, record_step_duration, update_job

logger = logging.getLogger(__name__)

STATUS_FOR_STEP = {
    "reconnaissance": "reconnaissance", "brief": "reconnaissance", "plan": "planning", "analysis": "analysis",
    "tables": "tables", "figures": "figures", "compose": "composing", "receipts": "composing",
}
STEP_WHY = {
    "reconnaissance": "Reading every document closely so the later steps work from what the material actually says, not from a summary.",
    "brief": "Proposing three genuinely different angles, each with its engines and cost, so the choice of dossier is explicit and cheap to change.",
    "plan": "Turning the chosen angle into an ordered sequence of executable engines, so each phase feeds the next with context.",
    "analysis": "Running the engines through the executor: multi-pass analysis where every phase reads the previous phases' prose.",
    "tables": "Condensing the analysis into evidence tables whose every row is pinned to a verbatim passage.",
    "figures": "Planning figures as labelled analytical diagrams — primitive, format, exact labels from the analysis — then rendering and checking them.",
    "compose": "Writing the dossier for the audience with footnoted anchors, then rendering HTML, PDF and Markdown.",
    "receipts": "Totalling every call so the cost and the method are on the record.",
}

_running: set[str] = set()
_cancel: set[str] = set()
_lock = threading.Lock()


def is_cancelled(job_id: str) -> bool:
    with _lock:
        return job_id in _cancel


def cancel(job_id: str) -> bool:
    job = get_job(job_id)
    if job is None:
        return False
    with _lock:
        _cancel.add(job_id)
    if job.analysis_job_id:
        try:
            from src.executor.job_manager import request_cancellation

            request_cancellation(job.analysis_job_id, force=True)
        except Exception as exc:
            logger.warning(f"could not cancel executor job {job.analysis_job_id}: {exc}")
    if job.status not in ("done", "failed"):
        update_job(job_id, status="cancelled", error="cancelled by request")
        events.emit(job_id, "job_failed", detail="cancelled by request")
    return True


def _next_step(job: DossierJob) -> Optional[str]:
    """Where to (re)start: the recorded step, or the step after the last completed one."""
    if job.status in ("done",):
        return None
    if job.status == "awaiting_brief":
        return "plan" if job.chosen_option else None
    if job.step in STEPS:
        return job.step
    return "reconnaissance"


def start(job_id: str) -> bool:
    with _lock:
        if job_id in _running:
            return False
        _running.add(job_id)
        _cancel.discard(job_id)
    threading.Thread(target=_run, args=(job_id,), name=f"dossier-{job_id}", daemon=True).start()
    return True


def resume(job_id: str) -> bool:
    return start(job_id)


def _run(job_id: str) -> None:
    try:
        job = get_job(job_id)
        if job is None:
            return
        step = _next_step(job)
        if step is None:
            return
        if job.status == "queued":
            events.emit(job_id, "job_started", detail=f"dossier run over {len(job.documents)} documents, depth {job.options.depth}, audience {job.options.audience}",
                        payload_json={"options": job.options.model_dump(), "documents": job.documents})
        docs = load_documents(job)
        idx = STEPS.index(step)
        for step_name in STEPS[idx:]:
            if is_cancelled(job_id):
                return
            job = get_job(job_id) or job
            _run_step(job, step_name, docs)
            if step_name == "brief" and not job.options.autopilot:
                job = get_job(job_id) or job
                if not job.chosen_option:
                    update_job(job_id, status="awaiting_brief", step="brief")
                    events.emit(job_id, "note", phase="brief", detail="awaiting_brief: choose one of the three options to continue",
                                payload_json={"kind": "awaiting_brief"})
                    return
        update_job(job_id, status="done", step="receipts")
        job = get_job(job_id) or job
        events.emit(job_id, "job_finished", detail=f"dossier done: ${job.totals.cost_usd:.2f}, {job.totals.llm_calls} calls, "
                    f"{round(job.totals.duration_ms/60000, 1)} min", cost_usd=job.totals.cost_usd,
                    payload_json={"paths": job.paths, "totals": job.totals.model_dump()})
    except Exception as exc:
        logger.error(f"dossier {job_id} failed: {exc}\n{traceback.format_exc()}")
        try:
            update_job(job_id, status="failed", error=f"{exc.__class__.__name__}: {exc}")
        except Exception:
            pass
        events.emit(job_id, "job_failed", detail=f"{exc.__class__.__name__}: {exc}")
    finally:
        with _lock:
            _running.discard(job_id)


def _persist_factory(job_id: str) -> Callable[..., None]:
    def persist(**fields) -> None:
        update_job(job_id, **fields)
    return persist


def _run_step(job: DossierJob, step: str, docs) -> None:
    job_id = job.id
    update_job(job_id, status=STATUS_FOR_STEP[step], step=step)
    events.emit(job_id, "phase_started", phase=step, detail=STEP_WHY[step])
    started = time.time()
    persist = _persist_factory(job_id)
    summary = ""
    if step == "reconnaissance":
        from src.dossier.reconnaissance import run_reconnaissance

        recon = run_reconnaissance(job, docs)
        job.profiles = recon
        persist(profiles=recon)
        summary = f"{len(recon.profiles)} profiles, {sum(len(p.key_claims) for p in recon.profiles)} anchored claims"
    elif step == "brief":
        from src.dossier.brief import run_brief

        brief = run_brief(job, docs)
        job.brief = brief
        fields = {"brief": brief}
        if job.options.autopilot and not job.chosen_option:
            job.chosen_option = brief.autopilot_key()  # the recommendation (brief v2), else option 1
            fields["chosen_option"] = job.chosen_option
            events.emit(job_id, "note", phase=step, detail=brief.autopilot_reason(), payload_json={"kind": "material_decided", "option_key": job.chosen_option})
        persist(**fields)
        summary = " / ".join(o.title for o in brief.options)
    elif step == "plan":
        from src.dossier.plan import run_plan

        plan = run_plan(job, docs)
        job.plan = plan
        job.plan_id = plan.plan_id
        persist(plan=plan, plan_id=plan.plan_id)
        summary = " → ".join(f"{p.engine_key}@{p.depth}" for p in plan.phases)
    elif step == "analysis":
        from src.dossier.analysis import run_analysis

        sub_id, analysis = run_analysis(job, docs, cancel_check=lambda: is_cancelled(job_id), persist=persist)
        job.analysis_job_id = sub_id
        job.analysis = analysis
        persist(analysis_job_id=sub_id, analysis=analysis)
        summary = f"executor job {sub_id}: {len(analysis)} phases"
    elif step == "tables":
        from src.dossier.tables import run_tables

        tables = run_tables(job, docs)
        job.tables = tables
        persist(tables=tables)
        summary = f"{len(tables)} tables, {sum(len(t.rows) for t in tables)} verified rows"
    elif step == "figures":
        from src.dossier.figures import run_figures

        figures = run_figures(job, docs)
        job.figures = figures
        persist(figures=figures)
        summary = ", ".join(f"{f.key}:{f.status}" for f in figures) or "none"
    elif step == "compose":
        from src.dossier.compose import run_compose

        job = get_job(job_id) or job  # fresh receipts/totals for the appendix
        sections, paths = run_compose(job, docs, persist)
        job.paths = paths
        persist(paths=paths)
        summary = f"{len(sections.sections)} sections; files: {', '.join(paths.keys())}"
    elif step == "receipts":
        from src.dossier.store import compute_totals

        fresh = get_job(job_id) or job
        totals = compute_totals([r.model_dump() for r in fresh.receipts], fresh.totals.model_dump())
        persist(totals=totals)
        summary = f"{totals['llm_calls']} llm calls, {totals['image_calls']} image calls, ${totals['cost_usd']:.2f}"
        # re-render so the appendix carries the final totals (cheap, no model call)
        try:
            from src.dossier.compose import render_all

            fresh = get_job(job_id) or fresh
            render_all(fresh, docs)
        except Exception as exc:
            add_note(job_id, "rerender_failed", str(exc))
    duration_ms = int((time.time() - started) * 1000)
    record_step_duration(job_id, step, duration_ms)
    events.emit(job_id, "phase_finished", phase=step, duration_ms=duration_ms, detail=f"{step} done in {duration_ms/1000:.0f}s — {summary}")
