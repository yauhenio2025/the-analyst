"""Story desk runner: steps in order, the brief gate, receipts, cancellation."""
from __future__ import annotations

import logging
import threading
import traceback
from typing import Optional

from src.dossier import events
from src.sources.schemas import Document

from . import steps
from .schemas import STATUS_FOR_STEP, STEPS, StoryJob
from .store import get_job, update_job

logger = logging.getLogger(__name__)
_running: set[str] = set()
_cancel: set[str] = set()
_lock = threading.Lock()

STEP_WHY = {
    "reconnaissance": "reading every source against the demands the downstream passes declared in the registry; every element anchored",
    "map": "finding what runs through the sources: recurrences, contradictions, candidate through-lines with tributaries",
    "approaches": "ranking Wirecut's twelve structures against the map",
    "brief": "three deliverable-first options; nothing is rendered before you choose",
    "spine": "the plan before the script: movements assigned to sources, motif, hook, open loop",
    "handoff": "assembling the contract Wirecut reads: through-line, spine, anchored ledger, sources",
}


def is_cancelled(job_id: str) -> bool:
    with _lock:
        return job_id in _cancel


def cancel(job_id: str) -> bool:
    with _lock:
        if job_id not in _running:
            return False
        _cancel.add(job_id)
    update_job(job_id, status="cancelled")
    events.emit(job_id, "job_cancelled", detail="cancelled by the requester")
    return True


def start(job_id: str) -> bool:
    with _lock:
        if job_id in _running:
            return False
        _running.add(job_id)
        _cancel.discard(job_id)
    threading.Thread(target=_run, args=(job_id,), name=f"story-{job_id}", daemon=True).start()
    return True


def _next_step(job: StoryJob) -> Optional[str]:
    if job.status == "done":
        return None
    if not job.profiles:
        return "reconnaissance"
    if job.map is None:
        return "map"
    if job.approaches is None:
        return "approaches"
    if job.brief is None:
        return "brief"
    if job.spine is None:
        return "spine"
    if job.handoff is None:
        return "handoff"
    return None


def load_documents(job: StoryJob) -> list[Document]:
    from src.executor.document_store import get_document_text

    docs = []
    for meta in job.documents:
        text = get_document_text(meta.get("executor_doc_id")) or "" if meta.get("executor_doc_id") else ""
        docs.append(Document(key=meta.get("key", "doc"), title=meta.get("title", ""), creators=meta.get("creators", ""),
                             year=meta.get("year", ""), publication=meta.get("publication", ""), library=meta.get("library", ""),
                             stacks_key=meta.get("stacks_key", ""), text=text, char_count=len(text)))
    return docs


def _run(job_id: str) -> None:
    try:
        job = get_job(job_id)
        if job is None:
            return
        step = _next_step(job)
        if step is None:
            return
        if job.status == "queued":
            events.emit(job_id, "job_started", detail=f"story desk over {len(job.documents)} sources, audience {job.options.audience}",
                        payload_json={"options": job.options.model_dump(), "documents": job.documents})
        docs = load_documents(job)
        for step_name in STEPS[STEPS.index(step):]:
            if is_cancelled(job_id):
                return
            job = get_job(job_id) or job
            if step_name == "brief" and job.brief is not None and not job.chosen_option:
                update_job(job_id, status="awaiting_brief", step="brief")
                return
            if step_name in ("spine", "handoff") and not job.chosen_option:
                update_job(job_id, status="awaiting_brief", step="brief")
                return
            update_job(job_id, status=STATUS_FOR_STEP[step_name], step=step_name)
            events.emit(job_id, "phase_started", phase=step_name, detail=STEP_WHY[step_name])
            if step_name == "reconnaissance":
                update_job(job_id, profiles=[p.model_dump() for p in steps.run_reconnaissance(job, docs)])
            elif step_name == "map":
                update_job(job_id, map=steps.run_map(job))
            elif step_name == "approaches":
                update_job(job_id, approaches=steps.run_approaches(job))
            elif step_name == "brief":
                job = update_job(job_id, brief=steps.run_brief(job))
                if not job.options.autopilot:
                    update_job(job_id, status="awaiting_brief", step="brief")
                    events.emit(job_id, "note", phase="brief", detail="awaiting_brief: choose one of the three options to continue", payload_json={"kind": "awaiting_brief"})
                    return
                update_job(job_id, chosen_option=job.brief.recommendation)
            elif step_name == "spine":
                update_job(job_id, spine=steps.run_spine(job))
            elif step_name == "handoff":
                update_job(job_id, handoff=steps.build_handoff(job, docs))
            events.emit(job_id, "phase_finished", phase=step_name, detail=f"{step_name} done")
        job = update_job(job_id, status="done", step="handoff")
        events.emit(job_id, "job_finished", detail=f"story desk done: ${job.totals.cost_usd:.2f}, {job.totals.llm_calls} calls", cost_usd=job.totals.cost_usd,
                    payload_json={"handoff_url": f"/v1/story/jobs/{job_id}/handoff", "totals": job.totals.model_dump()})
    except Exception as exc:  # noqa: BLE001
        logger.error(f"story {job_id} failed: {exc}\n{traceback.format_exc()}")
        try:
            update_job(job_id, status="failed", error=f"{exc.__class__.__name__}: {exc}")
        except Exception:  # noqa: BLE001
            pass
        events.emit(job_id, "job_failed", detail=f"{exc.__class__.__name__}: {exc}")
    finally:
        with _lock:
            _running.discard(job_id)
