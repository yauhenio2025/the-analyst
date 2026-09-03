"""LLM calls for the dossier's own steps (reconnaissance, brief, plan, tables, figures, compose).

Every call emits call_started / call_finished / call_failed events and leaves a
receipt. JSON answers use a forced tool call (the veo2 pattern: tool schema +
shape validation + one re-ask with the errors appended verbatim). Inputs over
~180K tokens go through the 1M-context beta, mirroring src/llm/backends.py.
"""
from __future__ import annotations

import json
import logging
import os
import time
from typing import Any, Optional, Type

from pydantic import BaseModel, ValidationError

from src.dossier import events
from src.dossier.receipts import make_receipt, record
from src.llm.client import parse_llm_json_response

logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.environ.get("DOSSIER_MODEL", "claude-sonnet-4-6")
ONE_M_BETA = "context-1m-2025-08-07"
STD_CONTEXT_TOKENS = 200_000
ONE_M_THRESHOLD_TOKENS = 150_000  # per the contract: >150K tokens → 1M path
MAX_ATTEMPTS = 3
TRANSIENT_BACKOFF_S = (15, 45, 90)


class LLMError(RuntimeError):
    pass


def estimate_tokens(text: str) -> int:
    return max(1, len(text or "") // 4)


def _client():
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise LLMError("ANTHROPIC_API_KEY is not set")
    return anthropic.Anthropic(
        api_key=api_key,
        timeout=anthropic.Timeout(1200.0, connect=60.0, read=1200.0, write=120.0),
        max_retries=2,
    )


def _is_transient(exc: Exception) -> bool:
    try:
        import anthropic

        if isinstance(exc, (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.APITimeoutError)):
            return True
        if isinstance(exc, anthropic.APIStatusError) and getattr(exc, "status_code", 0) >= 500:
            return True
        if isinstance(exc, anthropic.APIStatusError) and getattr(exc, "status_code", 0) == 529:
            return True
    except Exception:
        pass
    text = str(exc).lower()
    return "overloaded" in text or "timeout" in text or "connection" in text


def _create(client, *, use_1m: bool, **kwargs):
    if use_1m:
        return client.beta.messages.create(betas=[ONE_M_BETA], **kwargs)
    return client.messages.create(**kwargs)


def _usage(resp) -> tuple[int, int]:
    usage = getattr(resp, "usage", None)
    if usage is None:
        return 0, 0
    inp = int(getattr(usage, "input_tokens", 0) or 0)
    inp += int(getattr(usage, "cache_read_input_tokens", 0) or 0)
    inp += int(getattr(usage, "cache_creation_input_tokens", 0) or 0)
    out = int(getattr(usage, "output_tokens", 0) or 0)
    return inp, out


def _run(
    job_id: str,
    step: str,
    *,
    label: str,
    system: str,
    user: str,
    model: str,
    max_tokens: int,
    effort: Optional[str],
    tool: Optional[dict],
) -> tuple[Any, dict]:
    """One recorded call. Returns (parsed_or_text, meta)."""
    client = _client()
    est = estimate_tokens(system) + estimate_tokens(user)
    use_1m = est > ONE_M_THRESHOLD_TOKENS
    if not use_1m:
        headroom = STD_CONTEXT_TOKENS - est - 2_000
        if headroom < max_tokens:
            max_tokens = max(4_000, headroom)
    kwargs: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    if tool is not None:
        kwargs["tools"] = [tool]
        kwargs["tool_choice"] = {"type": "tool", "name": tool["name"]}
    elif effort:
        kwargs["thinking"] = {"type": "adaptive"}
        kwargs["output_config"] = {"effort": effort}

    prompt_text = system + "\n\n" + user
    seq = events.emit(
        job_id, "call_started", phase=step, model=model, label=label,
        detail=f"{label}: ~{est:,} input tokens ({'1M' if use_1m else 'std'} context), max_tokens={max_tokens}",
        prompt_excerpt=events.excerpt(user, 600), input_tokens=est,
    )
    started = time.time()
    last_exc: Optional[Exception] = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            resp = _create(client, use_1m=use_1m, **kwargs)
            break
        except Exception as exc:
            last_exc = exc
            if attempt < MAX_ATTEMPTS and _is_transient(exc):
                wait = TRANSIENT_BACKOFF_S[min(attempt - 1, len(TRANSIENT_BACKOFF_S) - 1)]
                logger.warning(f"[{label}] transient LLM error (attempt {attempt}): {exc}; retry in {wait}s")
                events.emit(job_id, "note", phase=step, detail=f"{label}: transient error, retrying in {wait}s ({exc})")
                time.sleep(wait)
                continue
            duration_ms = int((time.time() - started) * 1000)
            events.emit(job_id, "call_failed", phase=step, model=model, label=label,
                        duration_ms=duration_ms, detail=f"{label} failed: {exc}")
            raise LLMError(f"{label}: {exc}") from exc
    else:  # pragma: no cover
        raise LLMError(f"{label}: {last_exc}")

    duration_ms = int((time.time() - started) * 1000)
    input_tokens, output_tokens = _usage(resp)
    stop_reason = getattr(resp, "stop_reason", "")

    text_parts, tool_input = [], None
    for block in getattr(resp, "content", []) or []:
        btype = getattr(block, "type", "")
        if btype == "text":
            text_parts.append(block.text)
        elif btype == "tool_use" and tool is not None and getattr(block, "name", "") == tool["name"]:
            tool_input = block.input
    text = "".join(text_parts)

    if tool is not None:
        if tool_input is None:
            # No tool block came back — fall back to parsing any JSON in the text.
            try:
                tool_input = parse_llm_json_response(text)
            except Exception as exc:
                raise LLMError(f"{label}: no tool result and no parseable JSON ({exc}); stop_reason={stop_reason}")
        result_obj: Any = tool_input
        result_text = json.dumps(tool_input, ensure_ascii=False)
    else:
        result_obj = text
        result_text = text

    receipt = make_receipt(
        step=step, kind="llm", model=model, label=label,
        input_tokens=input_tokens, output_tokens=output_tokens, duration_ms=duration_ms,
        prompt_text=prompt_text, result_text=result_text,
    )
    record(job_id, receipt)
    events.emit(
        job_id, "call_finished", phase=step, model=model, label=label,
        input_tokens=input_tokens, output_tokens=output_tokens, cost_usd=receipt.cost_usd,
        duration_ms=duration_ms, output_excerpt=events.excerpt(result_text, 600),
        detail=f"{label}: {input_tokens:,} in / {output_tokens:,} out, ${receipt.cost_usd:.3f}, {duration_ms/1000:.0f}s"
        + (f" (stop={stop_reason})" if stop_reason and stop_reason != "end_turn" and stop_reason != "tool_use" else ""),
        payload_json={"stop_reason": stop_reason, "attempt_seq": seq},
    )
    meta = {"model": model, "input_tokens": input_tokens, "output_tokens": output_tokens,
            "duration_ms": duration_ms, "cost_usd": receipt.cost_usd, "stop_reason": stop_reason,
            "prompt_hash": receipt.prompt_hash, "result_hash": receipt.result_hash}
    return result_obj, meta


def call_text(
    job_id: str, step: str, *, label: str, system: str, user: str,
    model: Optional[str] = None, max_tokens: int = 16000, effort: Optional[str] = None,
) -> tuple[str, dict]:
    return _run(job_id, step, label=label, system=system, user=user, model=model or DEFAULT_MODEL,
                max_tokens=max_tokens, effort=effort, tool=None)


def call_json(
    job_id: str, step: str, *, label: str, system: str, user: str,
    tool_name: str, schema: dict, model_cls: Optional[Type[BaseModel]] = None,
    tool_description: str = "Return the structured answer.",
    model: Optional[str] = None, max_tokens: int = 16000, repair_attempts: int = 1,
) -> tuple[Any, dict]:
    """Forced-tool JSON call validated against `model_cls` (if given).

    On validation failure the errors are appended verbatim to the user message
    and the call is re-asked once (the shape-retry law).
    """
    tool = {"name": tool_name, "description": tool_description, "input_schema": schema}
    user_msg = user
    last_errors = ""
    for attempt in range(repair_attempts + 1):
        raw, meta = _run(job_id, step, label=label if attempt == 0 else f"{label} (repair {attempt})",
                         system=system, user=user_msg, model=model or DEFAULT_MODEL,
                         max_tokens=max_tokens, effort=None, tool=tool)
        if model_cls is None:
            return raw, meta
        try:
            return model_cls.model_validate(raw), meta
        except ValidationError as exc:
            last_errors = str(exc)[:4000]
            logger.warning(f"[{label}] shape validation failed: {last_errors[:300]}")
            events.emit(job_id, "note", phase=step, detail=f"{label}: answer failed shape validation; re-asking with the errors")
            user_msg = (
                user + "\n\n---\nYOUR PREVIOUS ANSWER FAILED VALIDATION. Return the complete, corrected object. Errors:\n"
                + last_errors
            )
    raise LLMError(f"{label}: answer failed validation after repair: {last_errors[:500]}")


def schema_of(model_cls: Type[BaseModel]) -> dict:
    """JSON schema for a forced tool, stripped of Pydantic's $defs indirections where possible."""
    schema = model_cls.model_json_schema()
    return _inline_defs(schema)


def _inline_defs(schema: dict) -> dict:
    defs = schema.pop("$defs", {}) or {}

    def walk(node: Any) -> Any:
        if isinstance(node, dict):
            if "$ref" in node and node["$ref"].startswith("#/$defs/"):
                target = defs.get(node["$ref"].split("/")[-1], {})
                merged = dict(target)
                for k, v in node.items():
                    if k != "$ref":
                        merged[k] = v
                return walk(merged)
            return {k: walk(v) for k, v in node.items()}
        if isinstance(node, list):
            return [walk(x) for x in node]
        return node

    return walk(schema)
