"""Narrator: one plain-language sentence per phase for an executive reader.

At `phase_started` the executor calls `narrate_phase_async()`. It builds a
compact description of the phase (name, description, engines, context
parameters, dependencies) plus the plan's strategy/emphasis, asks
claude-haiku-4-5-20251001 for ONE sentence — what this step does with the
previous step's output and why — and appends a `narration` event.

- Runs in a daemon thread; never blocks the executor.
- Cached in memory by (workflow_key, phase_key); a cache hit emits immediately.
- Skips silently when ANTHROPIC_API_KEY is unset or EVENTS_NARRATOR=off.
"""

import json
import logging
import os
import threading
import time
from typing import Any, Optional

from src.events.store import append_event

logger = logging.getLogger(__name__)

NARRATOR_MODEL = "claude-haiku-4-5-20251001"
NARRATOR_MAX_TOKENS = 160
NARRATOR_TIMEOUT_S = 30.0

SYSTEM_PROMPT = (
    "You narrate an automated document-analysis pipeline for an executive reader "
    "who has no background in the underlying analytical theory. Write exactly ONE "
    "plain-language sentence (at most 40 words) saying what this step does — using "
    "the output of the previous step(s) when there are any — and why it matters to "
    "the final result. No jargon, no engine or technique names, no quotation marks, "
    "no preamble, no bullet points. Output only the sentence."
)

_cache: dict[tuple[str, str], str] = {}
_inflight: set[tuple[str, str]] = set()
_lock = threading.Lock()


def _enabled() -> bool:
    if os.environ.get("EVENTS_NARRATOR", "").strip().lower() in ("0", "off", "false", "no"):
        return False
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def _truncate(text: Any, limit: int) -> str:
    s = "" if text is None else str(text)
    return s if len(s) <= limit else s[:limit] + " …"


def build_narration_prompt(phase_spec: dict[str, Any], plan_context: Optional[dict[str, Any]] = None) -> str:
    """Render the user message for Haiku from a phase spec + plan context."""
    plan_context = plan_context or {}
    lines: list[str] = []
    wf_name = plan_context.get("workflow_name") or plan_context.get("workflow_key")
    if wf_name:
        lines.append(f"Workflow: {wf_name}")
    if plan_context.get("workflow_description"):
        lines.append(f"Workflow purpose: {_truncate(plan_context['workflow_description'], 600)}")
    if plan_context.get("subject"):
        lines.append(f"Subject under analysis: {_truncate(plan_context['subject'], 300)}")
    if plan_context.get("strategy_summary"):
        lines.append(f"Planner strategy: {_truncate(plan_context['strategy_summary'], 1500)}")
    if plan_context.get("strategy_rationale"):
        lines.append(f"Planner rationale: {_truncate(plan_context['strategy_rationale'], 1000)}")

    lines.append("")
    lines.append(f"THIS STEP — phase {phase_spec.get('phase')}: {phase_spec.get('phase_name')}")
    if phase_spec.get("description"):
        lines.append(f"Description: {_truncate(phase_spec['description'], 1200)}")
    engines = phase_spec.get("engines") or []
    if engines:
        pretty = []
        for e in engines:
            if isinstance(e, dict):
                label = e.get("name") or e.get("key")
                if e.get("problematique"):
                    label = f"{label} — {_truncate(e['problematique'], 240)}"
                pretty.append(str(label))
            else:
                pretty.append(str(e))
        lines.append("Analytical engines used: " + "; ".join(pretty))
    if phase_spec.get("chain"):
        lines.append(f"Engine chain: {phase_spec['chain']}")
    if phase_spec.get("depth"):
        lines.append(f"Depth: {phase_spec['depth']}")
    if phase_spec.get("iteration_mode"):
        lines.append(f"Iteration mode: {phase_spec['iteration_mode']}")
    if phase_spec.get("context_parameters"):
        lines.append("Context parameters: " + _truncate(json.dumps(phase_spec["context_parameters"], ensure_ascii=False, default=str), 800))
    deps = phase_spec.get("depends_on") or []
    if deps:
        dep_desc = []
        for d in deps:
            if isinstance(d, dict):
                dep_desc.append(f"phase {d.get('phase')} ({d.get('phase_name')})" if d.get("phase_name") else f"phase {d.get('phase')}")
            else:
                dep_desc.append(f"phase {d}")
        lines.append("Receives the output of: " + ", ".join(dep_desc))
    else:
        lines.append("This is a first step: it works directly on the source documents.")
    if phase_spec.get("context_emphasis"):
        lines.append(f"Planner's emphasis for this step: {_truncate(phase_spec['context_emphasis'], 800)}")
    if phase_spec.get("rationale"):
        lines.append(f"Why the planner chose this step: {_truncate(phase_spec['rationale'], 800)}")

    lines.append("")
    lines.append("Write the one sentence now.")
    return "\n".join(lines)


def call_narrator(prompt: str, *, model: str = NARRATOR_MODEL) -> str:
    """Synchronous Haiku call. Raises on API failure."""
    import anthropic

    client = anthropic.Anthropic(timeout=NARRATOR_TIMEOUT_S, max_retries=1)
    response = client.messages.create(
        model=model,
        max_tokens=NARRATOR_MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(block.text for block in response.content if getattr(block, "type", "") == "text")
    sentence = " ".join(text.strip().split())
    if sentence.startswith(("\"", "'")) and sentence.endswith(("\"", "'")):
        sentence = sentence[1:-1].strip()
    return sentence


def _emit(job_id: str, phase_key: str, sentence: str, *, cached: bool, latency_ms: Optional[int] = None,
          usage: Optional[dict[str, Any]] = None) -> None:
    payload: dict[str, Any] = {"cached": cached, "model": NARRATOR_MODEL}
    if latency_ms is not None:
        payload["latency_ms"] = latency_ms
    if usage:
        payload["usage"] = usage
    append_event(
        job_id,
        "narration",
        phase=phase_key,
        narrator=sentence,
        detail=sentence,
        model=NARRATOR_MODEL,
        payload=payload,
    )


def narrate_phase_async(
    job_id: str,
    workflow_key: str,
    phase_key: str,
    phase_spec: dict[str, Any],
    plan_context: Optional[dict[str, Any]] = None,
) -> Optional[threading.Thread]:
    """Emit a `narration` event for this phase, from cache or via a daemon thread.

    Returns the thread when one was started (for tests), else None.
    Never raises.
    """
    try:
        if not _enabled():
            return None
        cache_key = (str(workflow_key or ""), str(phase_key))
        with _lock:
            cached = _cache.get(cache_key)
        if cached:
            _emit(job_id, phase_key, cached, cached=True)
            return None
        with _lock:
            if cache_key in _inflight:
                # Another job is already narrating this phase; poll-and-emit in a thread.
                pass
            _inflight.add(cache_key)

        prompt = build_narration_prompt(phase_spec, plan_context)

        def _worker() -> None:
            started = time.time()
            try:
                # If a sibling thread filled the cache meanwhile, reuse it.
                with _lock:
                    existing = _cache.get(cache_key)
                if existing:
                    _emit(job_id, phase_key, existing, cached=True)
                    return
                sentence = call_narrator(prompt)
                if not sentence:
                    return
                with _lock:
                    _cache[cache_key] = sentence
                _emit(job_id, phase_key, sentence, cached=False, latency_ms=int((time.time() - started) * 1000))
            except Exception as e:  # noqa: BLE001
                logger.warning("narrator failed for job %s phase %s: %s", job_id, phase_key, e)
            finally:
                with _lock:
                    _inflight.discard(cache_key)

        thread = threading.Thread(target=_worker, name=f"narrator-{job_id}-{phase_key}", daemon=True)
        thread.start()
        return thread
    except Exception as e:  # noqa: BLE001
        logger.warning("narrate_phase_async failed for job %s phase %s: %s", job_id, phase_key, e)
        return None


def clear_cache() -> None:
    with _lock:
        _cache.clear()
        _inflight.clear()
