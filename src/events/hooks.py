"""Executor-facing hooks for the run-event ledger.

Thin, exception-proof helpers called from `workflow_runner`, `chain_runner`,
`engine_runner` and the orchestrator pipeline. Every function swallows
errors — the ledger must never break execution.

Fields written per kind:
- job_started      payload: workflow_key, workflow_name, plan_id, thinker_name, target_title,
                            phases[{phase, phase_name, engines, depends_on, depth, model_hint, skip}],
                            estimated_llm_calls, prior_works
- job_finished     payload: status ("completed" | "cancelled"), summary snapshot
- job_failed       payload: status ("failed" | "cancelled"), error
- phase_started    phase; payload: phase_name, description, engines, chain, depends_on, depth,
                            model_hint, iteration_mode, context_emphasis, rationale
- phase_finished   phase, duration_ms, input/output tokens, cost_usd; payload: phase_name, status, error,
                            total_tokens, calls
- chain_started    phase, chain, work_key; payload: engines
- chain_finished   phase, chain, work_key, duration_ms; payload: engines_run, total_tokens
- note             detail; payload: anything
"""

import logging
import time
from typing import Any, Optional

from src.events import context as events_context
from src.events.narrator import narrate_phase_async
from src.events.store import append_event, job_summary

logger = logging.getLogger(__name__)


def _safe(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:  # noqa: BLE001
            logger.warning("events hook %s failed: %s", getattr(fn, "__name__", "?"), e)
            return None
    wrapper.__name__ = getattr(fn, "__name__", "hook")
    return wrapper


def _fmt_seconds(ms: Optional[int]) -> str:
    if not ms:
        return "0s"
    s = ms / 1000.0
    if s < 60:
        return f"{s:.1f}s"
    return f"{int(s // 60)}m{int(s % 60):02d}s"


def _fmt_cost(cost: Optional[float]) -> str:
    return "n/a" if cost is None else f"${cost:.4f}"


def _phase_engines(wf_phase: Any, plan_phase: Any) -> tuple[list[str], Optional[str]]:
    """Resolve the engine list and chain key a phase will run."""
    chain_key = getattr(plan_phase, "chain_key", None) or getattr(wf_phase, "chain_key", None)
    engine_key = getattr(plan_phase, "engine_key", None) or getattr(wf_phase, "engine_key", None)
    if getattr(plan_phase, "engine_key", None):
        chain_key = None  # explicit engine override suppresses the template chain
    engines: list[str] = []
    if chain_key:
        try:
            from src.chains.registry import get_chain_registry
            chain = get_chain_registry().get(chain_key)
            if chain is not None:
                engines = list(getattr(chain, "engine_keys", []) or [])
        except Exception:  # noqa: BLE001
            pass
    if not engines and engine_key:
        engines = [engine_key]
    return engines, chain_key


def _engine_descriptions(engine_keys: list[str]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    try:
        from src.engines.registry import get_engine_registry
        reg = get_engine_registry()
    except Exception:  # noqa: BLE001
        return [{"key": k} for k in engine_keys]
    for key in engine_keys:
        entry: dict[str, Any] = {"key": key}
        try:
            cap = reg.get_capability_definition(key)
            if cap is not None:
                entry["name"] = getattr(cap, "engine_name", None) or key
                entry["problematique"] = getattr(cap, "problematique", None)
            else:
                legacy = reg.get(key)
                if legacy is not None:
                    entry["name"] = getattr(legacy, "name", None) or getattr(legacy, "engine_name", None) or key
                    entry["problematique"] = getattr(legacy, "description", None)
        except Exception:  # noqa: BLE001
            pass
        out.append(entry)
    return out


def _plan_context(plan: Any, workflow: Any = None) -> dict[str, Any]:
    ctx: dict[str, Any] = {}
    try:
        ctx["workflow_key"] = getattr(plan, "workflow_key", None)
        if workflow is not None:
            ctx["workflow_name"] = getattr(workflow, "workflow_name", None)
            ctx["workflow_description"] = getattr(workflow, "description", None)
        target = getattr(plan, "target_work", None)
        thinker = getattr(plan, "thinker_name", None)
        title = getattr(target, "title", None) if target is not None else None
        if thinker or title:
            ctx["subject"] = " — ".join([p for p in (thinker, title) if p])
        ctx["strategy_summary"] = getattr(plan, "strategy_summary", None)
        trace = getattr(plan, "decision_trace", None)
        rationale = getattr(trace, "overall_strategy_rationale", None) if trace is not None else None
        ctx["strategy_rationale"] = rationale or getattr(plan, "strategy_rationale", None)
        rq = getattr(plan, "research_question", None)
        if rq:
            ctx["research_question"] = rq
    except Exception:  # noqa: BLE001
        pass
    return ctx


# ---------------------------------------------------------------------------
# Job
# ---------------------------------------------------------------------------

@_safe
def job_started(job_id: str, plan: Any, workflow: Any = None) -> int:
    phases: list[dict[str, Any]] = []
    wf_phases = {}
    if workflow is not None:
        wf_phases = {p.phase_number: p for p in getattr(workflow, "phases", []) or []}
    for pp in getattr(plan, "phases", []) or []:
        wf_phase = wf_phases.get(pp.phase_number)
        engines, chain_key = _phase_engines(wf_phase, pp)
        phases.append({
            "phase": events_context.phase_key(pp.phase_number),
            "phase_name": getattr(pp, "phase_name", None),
            "engines": engines,
            "chain": chain_key,
            "depends_on": [events_context.phase_key(d) for d in (
                getattr(pp, "depends_on", None) or getattr(wf_phase, "depends_on_phases", None) or []
            )],
            "depth": getattr(pp, "depth", None),
            "model_hint": getattr(pp, "model_hint", None),
            "skip": bool(getattr(pp, "skip", False)),
            "iteration_mode": getattr(pp, "iteration_mode", None) or getattr(wf_phase, "iteration_mode", None),
        })
    target = getattr(plan, "target_work", None)
    workflow_name = getattr(workflow, "workflow_name", None) or getattr(plan, "workflow_key", None)
    n_active = sum(1 for p in phases if not p["skip"])
    detail = (
        f"Started job {job_id}: workflow '{workflow_name}' on "
        f"'{getattr(target, 'title', None) or '?'}' ({getattr(plan, 'thinker_name', None) or 'unknown author'}) — "
        f"{n_active} phase(s), ~{getattr(plan, 'estimated_llm_calls', 0) or '?'} LLM calls planned."
    )
    return append_event(
        job_id,
        "job_started",
        detail=detail,
        payload={
            "workflow_key": getattr(plan, "workflow_key", None),
            "workflow_name": workflow_name,
            "plan_id": getattr(plan, "plan_id", None),
            "thinker_name": getattr(plan, "thinker_name", None),
            "target_title": getattr(target, "title", None),
            "prior_works": [getattr(pw, "title", None) for pw in getattr(plan, "prior_works", []) or []],
            "phases": phases,
            "estimated_llm_calls": getattr(plan, "estimated_llm_calls", None),
            "execution_model": getattr(plan, "execution_model", None),
            "strategy_summary": (getattr(plan, "strategy_summary", None) or "")[:2000],
        },
    )


@_safe
def job_finished(job_id: str, status: str, error: Optional[str] = None) -> int:
    """Terminal event. status: completed | failed | cancelled."""
    status = (status or "completed").lower()
    kind = "job_finished" if status == "completed" else "job_failed"
    summary = job_summary(job_id)
    if kind == "job_finished":
        detail = (
            f"Job {job_id} completed in {_fmt_seconds(summary.get('duration_ms'))}: "
            f"{summary.get('calls', 0)} LLM calls, "
            f"{summary.get('input_tokens', 0):,}→{summary.get('output_tokens', 0):,} tokens, "
            f"{_fmt_cost(summary.get('cost_usd'))}."
        )
    else:
        detail = f"Job {job_id} {status}" + (f": {str(error)[:300]}" if error else ".")
    return append_event(
        job_id,
        kind,
        duration_ms=summary.get("duration_ms"),
        input_tokens=summary.get("input_tokens"),
        output_tokens=summary.get("output_tokens"),
        cost_usd=summary.get("cost_usd"),
        detail=detail,
        payload={
            "status": status,
            "error": error,
            "calls": summary.get("calls"),
            "failed_calls": summary.get("failed_calls"),
            "phases": [
                {k: p.get(k) for k in ("phase", "name", "status", "calls", "cost_usd", "duration_ms")}
                for p in summary.get("phases", [])
            ],
        },
    )


@_safe
def note(job_id: str, detail: str, **payload: Any) -> int:
    ctx = events_context.current()
    return append_event(
        job_id,
        "note",
        phase=payload.pop("phase", ctx.get("phase")),
        engine=payload.pop("engine", ctx.get("engine")),
        detail=detail,
        payload=payload,
    )


# ---------------------------------------------------------------------------
# Phase
# ---------------------------------------------------------------------------

@_safe
def phase_started(job_id: str, plan: Any, wf_phase: Any, plan_phase: Any, workflow: Any = None) -> int:
    key = events_context.phase_key(plan_phase.phase_number)
    engines, chain_key = _phase_engines(wf_phase, plan_phase)
    depends_on = [
        events_context.phase_key(d)
        for d in (getattr(plan_phase, "depends_on", None) or getattr(wf_phase, "depends_on_phases", None) or [])
    ]
    # Names of upstream phases (for narration)
    upstream: list[dict[str, Any]] = []
    for d in depends_on:
        name = None
        for pp in getattr(plan, "phases", []) or []:
            if events_context.phase_key(pp.phase_number) == d:
                name = getattr(pp, "phase_name", None)
                break
        upstream.append({"phase": d, "phase_name": name})

    description = getattr(wf_phase, "phase_description", None) or getattr(wf_phase, "base_phase_description", None)
    depth = getattr(plan_phase, "depth", None)
    skip = bool(getattr(plan_phase, "skip", False))
    engine_descs = _engine_descriptions(engines)

    if skip:
        detail = f"Phase {key} '{plan_phase.phase_name}' skipped: {getattr(plan_phase, 'skip_reason', None) or 'per plan'}."
    else:
        engines_txt = ", ".join(engines) if engines else (chain_key or "function phase")
        deps_txt = f"; builds on phase(s) {', '.join(depends_on)}" if depends_on else "; works on the source documents directly"
        detail = f"Phase {key} '{plan_phase.phase_name}' started with {engines_txt} at depth {depth}{deps_txt}."

    seq = append_event(
        job_id,
        "phase_started",
        phase=key,
        chain=chain_key,
        detail=detail,
        payload={
            "phase_name": plan_phase.phase_name,
            "description": description,
            "engines": engines,
            "engine_details": engine_descs,
            "chain": chain_key,
            "depends_on": depends_on,
            "depth": depth,
            "model_hint": getattr(plan_phase, "model_hint", None),
            "iteration_mode": getattr(plan_phase, "iteration_mode", None) or getattr(wf_phase, "iteration_mode", None),
            "context_emphasis": getattr(plan_phase, "context_emphasis", None),
            "rationale": getattr(plan_phase, "rationale", None),
            "context_parameters": getattr(wf_phase, "context_parameters", None),
            "skip": skip,
            "skip_reason": getattr(plan_phase, "skip_reason", None),
            "requires_full_documents": getattr(plan_phase, "requires_full_documents", None),
        },
    )

    if not skip:
        narrate_phase_async(
            job_id=job_id,
            workflow_key=getattr(plan, "workflow_key", "") or "",
            phase_key=key,
            phase_spec={
                "phase": key,
                "phase_name": plan_phase.phase_name,
                "description": description,
                "engines": engine_descs,
                "chain": chain_key,
                "depth": depth,
                "iteration_mode": getattr(plan_phase, "iteration_mode", None) or getattr(wf_phase, "iteration_mode", None),
                "context_parameters": getattr(wf_phase, "context_parameters", None),
                "depends_on": upstream,
                "context_emphasis": getattr(plan_phase, "context_emphasis", None),
                "rationale": getattr(plan_phase, "rationale", None),
            },
            plan_context=_plan_context(plan, workflow),
        )
    return seq


@_safe
def phase_finished(job_id: str, plan_phase: Any, result: Any) -> int:
    key = events_context.phase_key(plan_phase.phase_number)
    status = getattr(getattr(result, "status", None), "value", None) or str(getattr(result, "status", "completed"))
    error = getattr(result, "error", None)
    duration_ms = int(getattr(result, "duration_ms", 0) or 0)

    # Per-phase call/cost aggregates from the ledger itself
    calls = in_tok = out_tok = 0
    cost = 0.0
    try:
        for p in job_summary(job_id).get("phases", []):
            if p.get("phase") == key:
                calls = p.get("calls", 0)
                in_tok = p.get("input_tokens", 0)
                out_tok = p.get("output_tokens", 0)
                cost = p.get("cost_usd", 0.0)
                break
    except Exception:  # noqa: BLE001
        pass

    if status == "completed":
        detail = (
            f"Phase {key} '{plan_phase.phase_name}' completed in {_fmt_seconds(duration_ms)}: "
            f"{calls} LLM call(s), {in_tok:,}→{out_tok:,} tokens, {_fmt_cost(cost)}."
        )
    elif status == "skipped":
        detail = f"Phase {key} '{plan_phase.phase_name}' skipped."
    else:
        detail = f"Phase {key} '{plan_phase.phase_name}' {status} after {_fmt_seconds(duration_ms)}" + (
            f": {str(error)[:300]}" if error else "."
        )
    final_output = getattr(result, "final_output", "") or ""
    return append_event(
        job_id,
        "phase_finished",
        phase=key,
        duration_ms=duration_ms,
        input_tokens=in_tok,
        output_tokens=out_tok,
        cost_usd=cost,
        output_chars=len(final_output),
        output_excerpt=final_output[:2000] if final_output else None,
        detail=detail,
        payload={
            "phase_name": plan_phase.phase_name,
            "status": status,
            "error": error,
            "total_tokens": getattr(result, "total_tokens", None),
            "calls": calls,
            "engines": list((getattr(result, "engine_results", None) or {}).keys()),
            "works": list((getattr(result, "work_results", None) or {}).keys()) or None,
        },
    )


# ---------------------------------------------------------------------------
# Chain
# ---------------------------------------------------------------------------

@_safe
def chain_started(job_id: str, phase_number: Any, chain_key: str, engine_keys: list[str],
                  work_key: Optional[str] = None, depth: Optional[str] = None) -> int:
    key = events_context.phase_key(phase_number)
    work_txt = f" for work '{work_key}'" if work_key else ""
    return append_event(
        job_id,
        "chain_started",
        phase=key,
        chain=chain_key,
        work_key=work_key or None,
        detail=(
            f"Chain '{chain_key}' started in phase {key}{work_txt}: "
            f"{len(engine_keys)} engine(s) in sequence ({', '.join(engine_keys)}), depth {depth}."
        ),
        payload={"engines": list(engine_keys), "depth": depth},
    )


@_safe
def chain_finished(job_id: str, phase_number: Any, chain_key: str, engines_run: list[str],
                   total_tokens: int, duration_ms: int, work_key: Optional[str] = None) -> int:
    key = events_context.phase_key(phase_number)
    work_txt = f" for work '{work_key}'" if work_key else ""
    return append_event(
        job_id,
        "chain_finished",
        phase=key,
        chain=chain_key,
        work_key=work_key or None,
        duration_ms=int(duration_ms or 0),
        detail=(
            f"Chain '{chain_key}' finished in phase {key}{work_txt} after {_fmt_seconds(duration_ms)}: "
            f"{len(engines_run)} engine(s) run, {int(total_tokens or 0):,} tokens."
        ),
        payload={"engines_run": list(engines_run), "total_tokens": int(total_tokens or 0)},
    )


# ---------------------------------------------------------------------------
# LLM call (used by engine_runner)
# ---------------------------------------------------------------------------

def _call_where(ctx: dict[str, Any]) -> str:
    parts = []
    if ctx.get("engine"):
        parts.append(ctx["engine"])
    if ctx.get("pass_name"):
        parts.append(ctx["pass_name"])
    if ctx.get("stance"):
        parts.append(f"{ctx['stance']} stance")
    if ctx.get("work_key"):
        parts.append(f"work '{ctx['work_key']}'")
    return " · ".join(parts) if parts else "engine call"


@_safe
def call_started(job_id: str, ctx: dict[str, Any], *, model: str, system_prompt: str, user_message: str,
                 attempt: int, max_attempts: int, label: str = "", effort: Optional[str] = None,
                 mode: str = "sync", use_1m: bool = False, max_tokens: Optional[int] = None) -> int:
    from src.events.store import prompt_excerpt, prompt_hash
    in_chars = len(system_prompt or "") + len(user_message or "")
    attempt_txt = f" (attempt {attempt}/{max_attempts})" if attempt > 1 else ""
    detail = (
        f"Phase {ctx.get('phase')}: calling {model} for {_call_where(ctx)} with "
        f"{in_chars:,} chars of prompt (~{in_chars // 4:,} tokens){attempt_txt}."
    )
    return append_event(
        job_id,
        "call_started",
        phase=ctx.get("phase"),
        chain=ctx.get("chain"),
        engine=ctx.get("engine"),
        pass_name=ctx.get("pass_name"),
        stance=ctx.get("stance"),
        work_key=ctx.get("work_key"),
        model=model,
        input_chars=in_chars,
        prompt_hash=prompt_hash(system_prompt, user_message),
        prompt_excerpt=prompt_excerpt(system_prompt, user_message),
        detail=detail,
        payload={
            "attempt": attempt,
            "max_attempts": max_attempts,
            "label": label,
            "effort": effort,
            "mode": mode,
            "use_1m_context": bool(use_1m),
            "max_tokens": max_tokens,
            "system_chars": len(system_prompt or ""),
            "user_chars": len(user_message or ""),
        },
    )


@_safe
def call_finished(job_id: str, ctx: dict[str, Any], *, model: str, system_prompt: str, user_message: str,
                  content: str, input_tokens: int, output_tokens: int, thinking_tokens: int,
                  duration_ms: int, attempt: int, label: str = "", partial: bool = False,
                  effort: Optional[str] = None) -> int:
    from src.events.pricing import estimate_cost
    from src.events.store import output_excerpt, prompt_excerpt, prompt_hash
    in_chars = len(system_prompt or "") + len(user_message or "")
    out_chars = len(content or "")
    cost = estimate_cost(model, input_tokens, output_tokens)
    detail = (
        f"Phase {ctx.get('phase')}: {model} returned {out_chars:,} chars for {_call_where(ctx)} in "
        f"{_fmt_seconds(duration_ms)} — {int(input_tokens or 0):,}→{int(output_tokens or 0):,} tokens, "
        f"{_fmt_cost(cost)}" + (" (partial output salvaged)" if partial else "") + "."
    )
    return append_event(
        job_id,
        "call_finished",
        phase=ctx.get("phase"),
        chain=ctx.get("chain"),
        engine=ctx.get("engine"),
        pass_name=ctx.get("pass_name"),
        stance=ctx.get("stance"),
        work_key=ctx.get("work_key"),
        model=model,
        input_chars=in_chars,
        output_chars=out_chars,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost_usd=cost,
        duration_ms=duration_ms,
        prompt_hash=prompt_hash(system_prompt, user_message),
        prompt_excerpt=prompt_excerpt(system_prompt, user_message),
        output_excerpt=output_excerpt(content),
        detail=detail,
        payload={
            "attempt": attempt,
            "thinking_tokens": thinking_tokens,
            "partial": bool(partial),
            "label": label,
            "effort": effort,
        },
    )


@_safe
def call_failed(job_id: str, ctx: dict[str, Any], *, model: str, system_prompt: str, user_message: str,
                error: str, duration_ms: int, attempt: int, max_attempts: int, will_retry: bool,
                retry_delay_s: Optional[int] = None, label: str = "") -> int:
    from src.events.store import prompt_excerpt, prompt_hash
    in_chars = len(system_prompt or "") + len(user_message or "")
    tail = f" — retrying in {retry_delay_s}s." if will_retry else " — giving up."
    detail = (
        f"Phase {ctx.get('phase')}: attempt {attempt}/{max_attempts} on {model} for {_call_where(ctx)} "
        f"failed after {_fmt_seconds(duration_ms)}: {str(error)[:240]}{tail}"
    )
    return append_event(
        job_id,
        "call_failed",
        phase=ctx.get("phase"),
        chain=ctx.get("chain"),
        engine=ctx.get("engine"),
        pass_name=ctx.get("pass_name"),
        stance=ctx.get("stance"),
        work_key=ctx.get("work_key"),
        model=model,
        input_chars=in_chars,
        duration_ms=duration_ms,
        prompt_hash=prompt_hash(system_prompt, user_message),
        prompt_excerpt=prompt_excerpt(system_prompt, user_message),
        detail=detail,
        payload={
            "attempt": attempt,
            "max_attempts": max_attempts,
            "will_retry": bool(will_retry),
            "retry_delay_s": retry_delay_s,
            "error": str(error)[:2000],
            "label": label,
        },
    )


def timer() -> float:
    return time.time()
