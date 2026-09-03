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
CACHE_MIN_CHARS = 8_000        # below this the prefix is not worth a cache write
CACHE_READ_FACTOR = 0.1        # Anthropic prompt caching: reads at 10 % of the input price
CACHE_WRITE_FACTOR = 1.25      # writes at 125 %


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
    inp, out, _, _ = _usage_full(resp)
    return inp, out


def _usage_full(resp) -> tuple[int, int, int, int]:
    """(input_total, output, cache_read, cache_write) — the total includes the cached parts."""
    usage = getattr(resp, "usage", None)
    if usage is None:
        return 0, 0, 0, 0
    fresh = int(getattr(usage, "input_tokens", 0) or 0)
    read = int(getattr(usage, "cache_read_input_tokens", 0) or 0)
    write = int(getattr(usage, "cache_creation_input_tokens", 0) or 0)
    out = int(getattr(usage, "output_tokens", 0) or 0)
    return fresh + read + write, out, read, write


def _cached_cost(model: str, input_total: int, output_tokens: int, cache_read: int, cache_write: int) -> Optional[float]:
    """Cost with the caching discounts applied (None when the model is unpriced)."""
    from src.dossier.receipts import llm_cost

    full = llm_cost(model, input_total, output_tokens)
    if full is None or not (cache_read or cache_write):
        return full
    per_in = (llm_cost(model, input_total, 0) or 0.0) / max(1, input_total)
    fresh = input_total - cache_read - cache_write
    return round(per_in * (fresh + cache_read * CACHE_READ_FACTOR + cache_write * CACHE_WRITE_FACTOR)
                 + (llm_cost(model, 0, output_tokens) or 0.0), 6)


def _user_content(user: str, user_tail: str, images: Optional[list[tuple[bytes, str]]]) -> Any:
    """The user turn as content blocks: the big prefix (cached when large), then images, then the
    uncached tail (patch errors, re-ask feedback) so a retry hits the cache on the prefix."""
    if not user_tail and not images and len(user) < CACHE_MIN_CHARS:
        return user
    blocks: list[dict[str, Any]] = []
    head: dict[str, Any] = {"type": "text", "text": user}
    if len(user) >= CACHE_MIN_CHARS:
        head["cache_control"] = {"type": "ephemeral"}
    blocks.append(head)
    import base64

    for data, mime in images or []:
        blocks.append({"type": "image", "source": {"type": "base64", "media_type": mime or "image/jpeg",
                                                   "data": base64.b64encode(data).decode("ascii")}})
    if user_tail:
        blocks.append({"type": "text", "text": user_tail})
    return blocks


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
    user_tail: str = "",
    images: Optional[list[tuple[bytes, str]]] = None,
) -> tuple[Any, dict]:
    """One recorded call. Returns (parsed_or_text, meta).

    `user` is the (cacheable) prefix; `user_tail` rides after it uncached so a patch/re-ask
    re-uses the prefix; `images` are (bytes, mime) blocks between the two (vision judges).
    """
    client = _client()
    est = estimate_tokens(system) + estimate_tokens(user) + estimate_tokens(user_tail) + 1_600 * len(images or [])
    use_1m = est > ONE_M_THRESHOLD_TOKENS
    if not use_1m:
        headroom = STD_CONTEXT_TOKENS - est - 2_000
        if headroom < max_tokens:
            max_tokens = max(4_000, headroom)
    kwargs: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": _user_content(user, user_tail, images)}],
    }
    if tool is not None:
        kwargs["tools"] = [tool]
        kwargs["tool_choice"] = {"type": "tool", "name": tool["name"]}
    elif effort:
        kwargs["thinking"] = {"type": "adaptive"}
        kwargs["output_config"] = {"effort": effort}

    prompt_text = system + "\n\n" + user + ("\n\n" + user_tail if user_tail else "")
    seq = events.emit(
        job_id, "call_started", phase=step, model=model, label=label,
        detail=f"{label}: ~{est:,} input tokens ({'1M' if use_1m else 'std'} context), max_tokens={max_tokens}"
               + (f", {len(images)} image(s)" if images else ""),
        prompt_excerpt=events.excerpt((user_tail + "\n\n" if user_tail else "") + user, 600), input_tokens=est,
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
    input_tokens, output_tokens, cache_read, cache_write = _usage_full(resp)
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
        cost_usd=_cached_cost(model, input_tokens, output_tokens, cache_read, cache_write),
    )
    record(job_id, receipt)
    cache_note = f" (cache: {cache_read:,} read, {cache_write:,} written)" if (cache_read or cache_write) else ""
    events.emit(
        job_id, "call_finished", phase=step, model=model, label=label,
        input_tokens=input_tokens, output_tokens=output_tokens, cost_usd=receipt.cost_usd,
        duration_ms=duration_ms, output_excerpt=events.excerpt(result_text, 600),
        detail=f"{label}: {input_tokens:,} in / {output_tokens:,} out, ${receipt.cost_usd:.3f}, {duration_ms/1000:.0f}s{cache_note}"
        + (f" (stop={stop_reason})" if stop_reason and stop_reason != "end_turn" and stop_reason != "tool_use" else ""),
        payload_json={"stop_reason": stop_reason, "attempt_seq": seq, "cache_read": cache_read, "cache_write": cache_write},
    )
    meta = {"model": model, "input_tokens": input_tokens, "output_tokens": output_tokens,
            "duration_ms": duration_ms, "cost_usd": receipt.cost_usd, "stop_reason": stop_reason,
            "prompt_hash": receipt.prompt_hash, "result_hash": receipt.result_hash,
            "cache_read": cache_read, "cache_write": cache_write}
    return result_obj, meta


def call_text(
    job_id: str, step: str, *, label: str, system: str, user: str,
    model: Optional[str] = None, max_tokens: int = 16000, effort: Optional[str] = None,
) -> tuple[str, dict]:
    return _run(job_id, step, label=label, system=system, user=user, model=model or DEFAULT_MODEL,
                max_tokens=max_tokens, effort=effort, tool=None)


def unstringify(value: Any, schema: Optional[dict]) -> Any:
    """Answer-repair law: a tool input whose array/object field arrived as a JSON string is unpacked in code.

    Walks the value alongside the schema; a string where the schema expects an
    array/object (or that merely looks like JSON) is parsed. Shape only — the
    content is never altered.
    """
    schema = schema or {}
    stype = schema.get("type")
    if isinstance(value, str):
        looks_json = value.lstrip()[:1] in ("[", "{")
        if stype in ("array", "object") or (looks_json and stype in (None, "string") and "anyOf" in schema) or (looks_json and stype is None):
            try:
                value = parse_llm_json_response(value)
            except Exception:
                return value
        else:
            return value
    if isinstance(value, dict):
        props = schema.get("properties") or {}
        return {k: unstringify(v, props.get(k)) for k, v in value.items()}
    if isinstance(value, list):
        items = schema.get("items") if isinstance(schema.get("items"), dict) else None
        return [unstringify(v, items) for v in value]
    return value


def call_json(
    job_id: str, step: str, *, label: str, system: str, user: str,
    tool_name: str, schema: dict, model_cls: Optional[Type[BaseModel]] = None,
    tool_description: str = "Return the structured answer.",
    model: Optional[str] = None, max_tokens: int = 16000, repair_attempts: int = 1,
    user_tail: str = "", images: Optional[list[tuple[bytes, str]]] = None,
) -> tuple[Any, dict]:
    """Forced-tool JSON call validated against `model_cls` (if given).

    On validation failure the errors are appended verbatim to the user message
    and the call is re-asked once (the shape-retry law). `user_tail` is the
    uncached part of the request (feedback, patch instructions); `images` are
    (bytes, mime) pairs shown to the model between prefix and tail.
    """
    tool = {"name": tool_name, "description": tool_description, "input_schema": schema}
    tail = user_tail
    last_errors = ""
    for attempt in range(repair_attempts + 1):
        raw, meta = _run(job_id, step, label=label if attempt == 0 else f"{label} (repair {attempt})",
                         system=system, user=user, model=model or DEFAULT_MODEL,
                         max_tokens=max_tokens, effort=None, tool=tool, user_tail=tail, images=images)
        try:
            repaired = unstringify(raw, schema)
            if repaired != raw:
                events.emit(job_id, "note", phase=step, detail=f"{label}: unpacked JSON-encoded string fields in the tool answer (shape repair, content untouched)")
                raw = repaired
        except Exception as exc:  # repair never blocks
            logger.debug(f"unstringify failed: {exc}")
        if model_cls is None:
            return raw, meta
        try:
            return model_cls.model_validate(raw), meta
        except ValidationError as exc:
            last_errors = str(exc)[:4000]
            logger.warning(f"[{label}] shape validation failed: {last_errors[:300]}")
            events.emit(job_id, "note", phase=step, detail=f"{label}: answer failed shape validation; re-asking with the errors")
            tail = (
                (user_tail + "\n\n" if user_tail else "")
                + "---\nYOUR PREVIOUS ANSWER FAILED VALIDATION. Return the complete, corrected object. Errors:\n"
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
