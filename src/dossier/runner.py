"""DossierRunner — the ten steps in a daemon thread, persisted after every step, resumable.

Lifted from veo2/engine/ops.py: params stored verbatim on the job so a restart
can resume from the recorded step; every step emits phase_started /
phase_finished; failures classify the run `failed` with the error recorded.
"""
from __future__ import annotations

import logging
import os
import threading
import time
import traceback
from datetime import datetime, timezone
from typing import Callable, Optional

from src.dossier import events
from src.dossier.common import DossierCancelled, load_documents
from src.dossier.schemas import DossierJob, STEPS
from src.dossier.store import add_note, get_job, list_jobs, record_step_duration, update_job

logger = logging.getLogger(__name__)

STATUS_FOR_STEP = {
    "reconnaissance": "reconnaissance", "brief": "reconnaissance", "plan": "planning", "analysis": "analysis",
    "spine": "spine", "tables": "tables", "figures": "figures", "plates": "plates", "compose": "composing", "crosscheck": "crosscheck",
    "receipts": "crosscheck",
}
# Statuses that mean "a thread is (supposed to be) running this job". Threads die with the process — Render replaces the
# instance on every deploy (12 times on 2026-09-05) — so on startup every job in one of these is an orphan.
ACTIVE_STATUSES = frozenset({"queued"} | set(STATUS_FOR_STEP.values()))
RECOVER_MAX_AGE_HOURS = float(os.environ.get("DOSSIER_RECOVER_MAX_AGE_HOURS", "24"))

STEP_WHY = {
    "reconnaissance": "Reading every document closely so the later steps work from what the material actually says, not from a summary.",
    "brief": "Proposing three genuinely different angles, each with its engines and cost, so the choice of dossier is explicit and cheap to change.",
    "plan": "Turning the chosen angle into an ordered sequence of executable engines, so each phase feeds the next with context.",
    "analysis": "Running the engines through the executor: multi-pass analysis where every phase reads the previous phases' prose.",
    "spine": "Deciding what the dossier argues before a word is written: one claim per section, and the table or diagram each claim needs — so exhibits are commissioned by the argument, not by a dial.",
    "tables": "Building exactly the tables the spine commissioned, keyed to their sections, every row pinned to a verbatim passage.",
    "figures": "Drawing exactly the diagrams the spine commissioned — primitive, format, labels from the analysis — then rendering and checking each against its own spec.",
    "plates": "Drawing the plates — one or two whole-page 4K diagrams, each a perspective that deserves to be read instead of the memo — planned from the spine and the analysis, rendered, and checked label by label.",
    "compose": "Writing the dossier with the finished exhibits on the desk, pointing at each table and diagram where the reader should look; the summary and the close written last against the assembled body.",
    "crosscheck": "Reading the dossier as one thing — do the pictures show what the text argues, do the rows match the claims, is anything asserted that nothing backs — and recording every finding with its cure.",
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


def _hours_since(ts: str, now: Optional[datetime] = None) -> float:
    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except ValueError:
        return float("inf")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return ((now or datetime.now(timezone.utc)) - dt).total_seconds() / 3600


def recover_orphaned_dossiers(now: Optional[datetime] = None, max_age_hours: Optional[float] = None) -> dict[str, list[str]]:
    """Startup: restart every dossier job whose status says a thread is running — there is none, this is a fresh
    process. Each restarts at its recorded step (reconnaissance from its per-document checkpoint; analysis re-attaches
    to its executor job). Jobs idle longer than `max_age_hours` are marked failed instead of silently re-billed;
    POST /resume still runs them on request. Mirrors the executor's recover_orphaned_jobs, which never covered dossiers
    (2026-09-05: two dossier jobs sat in 'reconnaissance' / 'analysis' for hours after deploys)."""
    limit_h = RECOVER_MAX_AGE_HOURS if max_age_hours is None else max_age_hours
    out: dict[str, list[str]] = {"resumed": [], "failed": [], "skipped": []}
    for s in list_jobs(limit=200):
        if s.status not in ACTIVE_STATUSES:
            continue
        age_h = _hours_since(s.updated_at, now)
        if age_h > limit_h:
            msg = (f"interrupted by an instance restart and not resumed automatically: last activity {age_h:.0f} h ago "
                   f"(older than {limit_h:.0f} h). POST /v1/dossier/jobs/{s.id}/resume runs it anyway.")
            update_job(s.id, status="failed", error=msg)
            events.emit(s.id, "job_failed", detail=msg, payload_json={"kind": "instance_restart_not_resumed", "age_hours": round(age_h, 1)})
            out["failed"].append(s.id)
            continue
        events.emit(s.id, "note", phase=s.step or "start",
                    detail=f"resumed after an instance restart at step {s.step or 'start'} — the step continues from its last checkpoint",
                    payload_json={"kind": "instance_restart_resume", "step": s.step, "idle_minutes": round(age_h * 60, 1)})
        (out["resumed"] if start(s.id) else out["skipped"]).append(s.id)
    if any(out.values()):
        logger.warning(f"Dossier startup recovery: resumed {out['resumed']}, failed (too old) {out['failed']}, skipped {out['skipped']}")
    return out


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
    except DossierCancelled as exc:
        logger.info(f"dossier {job_id} cancelled: {exc}")
        events.emit(job_id, "note", detail=f"stopped: {exc}", payload_json={"kind": "cancelled_mid_step"})
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


def ledger_line(job_id: str) -> str:
    from src.dossier.findings import summary_line

    fresh = get_job(job_id)
    return summary_line(fresh.findings) if fresh else "?"


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

        recon = run_reconnaissance(job, docs, persist=persist, cancel_check=lambda: is_cancelled(job_id))
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
    elif step == "spine":
        from src.dossier.spine import run_spine

        spine = run_spine(job, docs)
        job.spine = spine
        persist(spine=spine)
        summary = (f"{len(spine.sections)} sections, {len(spine.table_sections())} tables + {len(spine.figure_sections())} diagrams commissioned"
                   if spine else "spine unavailable — legacy planning")
    elif step == "tables":
        from src.dossier.tables import run_tables

        tables = run_tables(job, docs, persist)
        job.tables = tables
        persist(tables=tables)
        summary = f"{len(tables)} tables, {sum(len(t.rows) for t in tables)} verified rows" + (f"; findings: {ledger_line(job_id)}" if job.spine else "")
    elif step == "figures":
        from src.dossier.figures import run_figures

        figures = run_figures(job, docs, persist)
        job.figures = figures
        persist(figures=figures)
        summary = ", ".join(f"{f.key}:{f.status}" + ("" if f.checked_ok is None else ("/ok" if f.checked_ok else "/flagged")) for f in figures) or "none"
    elif step == "plates":
        n_plates = int(getattr(getattr(job.options, "output", None), "plates", 0) or 0)
        if n_plates <= 0:
            summary = "no plates requested"
        else:
            try:
                from src.dossier.plates import run_plates
                from src.dossier.plate_store import upsert_plate
            except ImportError as exc:
                add_note(job_id, "plates_unavailable", str(exc))
                summary = "plates not installed"
            else:
                job = get_job(job_id) or job
                plates = run_plates(job, n_plates, persist=lambda p: upsert_plate(job_id, p))
                summary = ", ".join(f"{p.key}:{p.status}" for p in plates) or "none"
    elif step == "compose":
        from src.dossier.compose import run_compose

        job = get_job(job_id) or job  # fresh receipts/totals for the appendix
        sections, paths = run_compose(job, docs, persist)
        job.paths = paths
        persist(paths=paths)
        summary = f"{len(sections.sections)} sections; files: {', '.join(paths.keys())}"
    elif step == "crosscheck":
        try:
            from src.dossier.crosscheck import run_crosscheck
        except ImportError as exc:  # the pass ships in a later milestone; the run never waits on it
            add_note(job_id, "crosscheck_unavailable", str(exc))
            summary = "cross-check not installed"
        else:
            job = get_job(job_id) or job
            verdict = run_crosscheck(job, docs, persist)
            summary = (f"{'hangs together' if verdict.hangs_together else 'findings recorded'}: {verdict.findings_minted} minted "
                       f"({verdict.clamps} by code), {len(verdict.realized)} acted on") if verdict else "cross-check unavailable"
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
