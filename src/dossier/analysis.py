"""Step 4 — analysis: run the plan THROUGH THE EXISTING EXECUTOR.

The legacy text prompt is stored as one target document, alongside explicit
original-source bindings for process engines; an executor job is created from
the saved plan exactly the way POST /v1/executor/jobs does (create_job +
start_execution_thread, in-process). The sub-job's events are mirrored into
the dossier job's stream every 2 s (payload_json.source_job_id set); when the
events store is absent, phase_outputs rows and progress-detail changes stand
in. On completion every pass becomes a receipt and the prose per phase is
recorded on the dossier job.
"""
from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timezone
from typing import Callable, Optional

from src.dossier import events
from src.dossier.common import corpus_text, corpus_title
from src.dossier.receipts import make_receipt, record
from src.dossier.schemas import DossierJob
from src.sources.schemas import Document

logger = logging.getLogger(__name__)

STEP = "analysis"
POLL_S = 2.0
TIMEOUT_S = int(os.environ.get("DOSSIER_ANALYSIS_TIMEOUT_S", "5400"))
MIRROR_STRIP = {"job_id", "seq", "ts", "id", "created_at"}


class AnalysisFailed(RuntimeError):
    pass


def _store_corpus(job: DossierJob, docs: list[Document]) -> tuple[str, str]:
    from src.executor.document_store import store_document

    title = corpus_title(docs, job.options.intent)
    text = corpus_text(docs)
    doc_id = store_document(title=title, text=text, author=f"dossier {job.id}", role="target")
    return doc_id, title


def _store_source_bindings(job: DossierJob, docs: list[Document]) -> dict[str, str]:
    """Keep desk source keys through the executor and its persisted resume inputs."""
    from src.executor.document_ids import CORPUS_DOCUMENT_PREFIX
    from src.executor.document_store import store_document

    if len({doc.key for doc in docs}) != len(docs):
        raise AnalysisFailed("duplicate source keys in dossier corpus")
    stored = {meta.get("key"): meta.get("executor_doc_id") for meta in job.documents}
    bindings = {}
    for doc in docs:
        doc_id = stored.get(doc.key)
        if not doc_id:
            doc_id = store_document(title=doc.title, text=doc.text, author=doc.creators, role="target")
        bindings[CORPUS_DOCUMENT_PREFIX + doc.key] = doc_id
    return bindings


def _start_sub_job(job: DossierJob, plan_id: str, document_ids: dict[str, str]) -> str:
    from src.executor.job_manager import create_job
    from src.executor.schemas import ExecutorJob
    from src.executor.workflow_runner import start_execution_thread
    from src.orchestrator.planner import load_plan

    plan = load_plan(plan_id)
    if plan is None:
        raise AnalysisFailed(f"executor plan not found: {plan_id}")
    sub = ExecutorJob(plan_id=plan_id)
    create_job(sub.job_id, plan_id, plan_data=plan.model_dump(), document_ids=document_ids,
               workflow_key=plan.workflow_key)
    start_execution_thread(job_id=sub.job_id, plan_id=plan_id, document_ids=document_ids)
    return sub.job_id


def _is_live(sub_job_id: str) -> bool:
    """Is the executor job actually executing in THIS process (not just recorded 'running')?"""
    try:
        from src.executor.workflow_runner import _active_jobs, _active_jobs_lock

        with _active_jobs_lock:
            return sub_job_id in _active_jobs
    except Exception:
        return True  # cannot tell; assume live rather than double-start


def _resume_sub_job(sub: dict) -> None:
    """Resume an orphaned executor job via the executor's own resume path (completed passes are skipped)."""
    from src.executor.db import _json_loads
    from src.executor.workflow_runner import start_resume_thread

    plan_data = sub.get("plan_data")
    if isinstance(plan_data, str):
        plan_data = _json_loads(plan_data)
    document_ids = sub.get("document_ids")
    if isinstance(document_ids, str):
        document_ids = _json_loads(document_ids)
    if not plan_data:
        raise AnalysisFailed(f"executor job {sub.get('job_id')} has no plan_data to resume from")
    start_resume_thread(sub["job_id"], plan_data, document_ids or None)


def _mirror_events(job_id: str, sub_job_id: str, after_seq: int) -> int:
    for ev in events.list_events(sub_job_id, after_seq):
        seq = int(ev.get("seq", after_seq) or after_seq)
        after_seq = max(after_seq, seq)
        kind = ev.get("kind") or "note"
        fields = {k: v for k, v in ev.items() if k not in MIRROR_STRIP and k != "kind"}
        payload = fields.pop("payload_json", None)
        if isinstance(payload, dict):
            payload = {**payload, "source_job_id": sub_job_id, "source_seq": seq}
        else:
            payload = {"source_job_id": sub_job_id, "source_seq": seq, "source_payload": payload}
        fields["phase"] = fields.get("phase") or STEP
        events.emit(job_id, kind, payload_json=payload, **fields)
    return after_seq


def _fallback_mirror_outputs(job_id: str, sub_job_id: str, seen: set[str]) -> None:
    """Without an events store: each new phase_outputs row is one finished engine pass."""
    from src.executor.output_store import load_all_job_outputs

    for row in load_all_job_outputs(sub_job_id, include_content=False):
        rid = row.get("id")
        if rid in seen:
            continue
        seen.add(rid)
        events.emit(
            job_id, "call_finished", phase=f"{STEP} {row.get('phase_number')}", engine=row.get("engine_key"),
            model=row.get("model_used"), input_tokens=row.get("input_tokens"), output_tokens=row.get("output_tokens"),
            detail=f"{row.get('engine_key')} pass {row.get('pass_number')} ({row.get('stance_key') or 'whole'}) finished",
            payload_json={"source_job_id": sub_job_id, "output_id": rid, "pass_number": row.get("pass_number"),
                          "stance_key": row.get("stance_key"), "phase_number": row.get("phase_number")},
        )


def _collect(job: DossierJob, sub_job_id: str, plan_phases: list[dict]) -> dict:
    from src.executor.output_store import load_all_job_outputs

    names = {float(p["phase_number"]): p for p in plan_phases}
    rows = load_all_job_outputs(sub_job_id, include_content=True)
    # Pass numbers restart at each engine. Sorting only by pass number can
    # otherwise make an earlier, longer engine look like the chain's product.
    by_phase: dict[float, list[dict]] = {}
    for row in rows:
        by_phase.setdefault(float(row["phase_number"]), []).append(row)
    rows = []
    for phase_rows in by_phase.values():
        try:
            dated = []
            for row in phase_rows:
                stamp = row.get("created_at")
                when = stamp if isinstance(stamp, datetime) else datetime.fromisoformat(stamp)
                when = when.replace(tzinfo=timezone.utc) if when.tzinfo is None else when
                dated.append((when.timestamp(), row))
            phase_rows = [row for _, row in sorted(dated, key=lambda item: item[0])]
        except (TypeError, ValueError):
            # Historical rows without complete timestamps keep their legacy
            # order; do not invent a mixed chronology from pass numbers.
            pass
        rows.extend(phase_rows)
    analysis: dict[str, dict] = {}
    for row in rows:
        pn = float(row["phase_number"])
        key = str(pn)
        entry = analysis.setdefault(key, {
            "phase_number": pn, "engine_key": row.get("engine_key"),
            "engine_name": names.get(pn, {}).get("engine_name") or row.get("engine_key"),
            "depth": names.get(pn, {}).get("depth", ""), "passes": [], "final_output": "",
        })
        content = row.get("content") or ""
        entry["passes"].append({
            "pass_number": row.get("pass_number"), "stance_key": row.get("stance_key") or "",
            "model": row.get("model_used") or "", "input_tokens": int(row.get("input_tokens") or 0),
            "output_tokens": int(row.get("output_tokens") or 0), "chars": len(content), "output_id": row.get("id"),
        })
        # The final engine owns the final output, including the corpus namespace
        # used by desk re-verification (e.g. P6 versus X6 in a mixed chain).
        entry["engine_key"] = row.get("engine_key")
        planned = names.get(pn, {})
        entry["engine_name"] = (planned.get("engine_name") if planned.get("engine_key") == row.get("engine_key")
                                else None) or row.get("engine_key")
        entry["final_output"] = content  # latest call in this phase (legacy order when timestamps are incomplete)
        metadata = row.get("metadata") or {}
        if isinstance(metadata, str):
            from src.executor.db import _json_loads
            metadata = _json_loads(metadata) or {}
        entry["final_wall"] = metadata.get("wall")
        receipt = make_receipt(
            step=STEP, kind="llm", model=row.get("model_used") or "",
            label=f"{row.get('engine_key')} pass {row.get('pass_number')}" + (f" ({row.get('stance_key')})" if row.get("stance_key") else ""),
            input_tokens=int(row.get("input_tokens") or 0), output_tokens=int(row.get("output_tokens") or 0),
            result_text=content, source_job_id=sub_job_id,
        )
        record(job.id, receipt)
    return analysis


def run_analysis(job: DossierJob, docs: list[Document], *, cancel_check: Optional[Callable[[], bool]] = None,
                 persist: Optional[Callable[..., None]] = None) -> tuple[str, dict]:
    """Returns (sub_job_id, analysis dict). Raises AnalysisFailed."""
    from src.executor.job_manager import get_job, request_cancellation

    if not job.plan or not job.plan.plan_id:
        raise AnalysisFailed("no executor plan on the job (run the plan step first)")
    plan_phases = [p.model_dump() for p in job.plan.phases]

    sub_job_id = job.analysis_job_id
    sub = get_job(sub_job_id) if sub_job_id else None
    if sub and sub.get("status") == "completed":
        events.emit(job.id, "note", phase=STEP, detail=f"reusing completed executor job {sub_job_id}")
    elif sub and sub.get("status") in ("pending", "running"):
        if _is_live(sub_job_id):
            events.emit(job.id, "note", phase=STEP, detail=f"re-attaching to running executor job {sub_job_id}")
        else:
            events.emit(job.id, "note", phase=STEP,
                        detail=f"executor job {sub_job_id} is recorded running but not live in this process; resuming it through the executor (completed passes are kept)",
                        payload_json={"source_job_id": sub_job_id, "kind": "sub_job_resumed"})
            _resume_sub_job(sub)
    else:
        doc_id, title = _store_corpus(job, docs)
        document_ids = {"target": doc_id, title: doc_id}
        document_ids.update(_store_source_bindings(job, docs))
        sub_job_id = _start_sub_job(job, job.plan.plan_id, document_ids)
        events.emit(job.id, "note", phase=STEP,
                    detail=f"executor job {sub_job_id} started from plan {job.plan.plan_id}: "
                           + " → ".join(f"{p['engine_key']}@{p['depth']}" for p in plan_phases),
                    payload_json={"source_job_id": sub_job_id, "plan_id": job.plan.plan_id, "corpus_doc_id": doc_id})
        if persist:
            persist(analysis_job_id=sub_job_id)

    after_seq = 0
    seen_outputs: set[str] = set()
    last_detail = ""
    fallback = events.using_fallback()
    started = time.time()
    while True:
        if cancel_check and cancel_check():
            request_cancellation(sub_job_id, force=True)
            raise AnalysisFailed("cancelled")
        sub = get_job(sub_job_id) or {}
        status = sub.get("status")
        try:
            after_seq = _mirror_events(job.id, sub_job_id, after_seq)
        except Exception as exc:
            logger.debug(f"event mirroring failed: {exc}")
        if fallback:
            try:
                _fallback_mirror_outputs(job.id, sub_job_id, seen_outputs)
                progress = sub.get("progress") or {}
                detail = f"phase {progress.get('current_phase')} {progress.get('phase_name') or ''}: {progress.get('detail') or ''}".strip()
                if detail and detail != last_detail:
                    last_detail = detail
                    events.emit(job.id, "narration", phase=STEP, detail=detail,
                                payload_json={"source_job_id": sub_job_id, "progress": progress})
            except Exception as exc:
                logger.debug(f"fallback mirroring failed: {exc}")
        if status == "completed":
            break
        if status in ("failed", "cancelled"):
            raise AnalysisFailed(f"executor job {sub_job_id} {status}: {sub.get('error') or ''}")
        if time.time() - started > TIMEOUT_S:
            request_cancellation(sub_job_id, force=True)
            raise AnalysisFailed(f"executor job {sub_job_id} exceeded {TIMEOUT_S}s")
        time.sleep(POLL_S)

    analysis = _collect(job, sub_job_id, plan_phases)
    if not analysis:
        raise AnalysisFailed(f"executor job {sub_job_id} completed but produced no phase outputs")
    total_chars = sum(len(v.get("final_output") or "") for v in analysis.values())
    events.emit(job.id, "artifact", phase=STEP,
                detail=f"analysis: {len(analysis)} phases, {sum(len(v['passes']) for v in analysis.values())} passes, {total_chars:,} chars of prose",
                payload_json={"kind": "analysis", "source_job_id": sub_job_id,
                              "phases": [{"phase_number": v["phase_number"], "engine_key": v["engine_key"],
                                          "passes": len(v["passes"]), "chars": len(v.get("final_output") or "")} for v in analysis.values()]})
    return sub_job_id, analysis
