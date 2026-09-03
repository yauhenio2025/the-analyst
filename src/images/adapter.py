"""Provider-agnostic image generation for The Analyst.

    from src.images.adapter import generate_image, edit_image, generate_with_fallback
    r = generate_image(prompt, provider="gemini_pro", size="2K", aspect="16:9")
    r.image_bytes, r.mime_type, r.cost_usd, r.prompt_sent ...

Transports (ported carefully):
  gemini      google-genai SDK generate_content + ImageConfig (analyzer v1
              src/llm/gemini.py:223-390, retry on "text instead of image");
              falls back to the REST /interactions path (veo2 engine/images.py
              _gemini_image) with the un-suffixed GA model id if the SDK path
              fails for a non-policy reason.
  ark         Seedream via Ark images/generations (veo2 _ark_image) — refs as
              an ARRAY of data URIs (the bench-validated shape), ≤1568 px.
  dashscope   Qwen-Image via DashScope multimodal generation (veo2
              _dashscope_mm_image) — 65 s backoff on throttle (2 rpm).

Errors: ImageProviderError (transient flag), PolicyRejection (never
retried), Throttled (retry_after). Retry: 2 attempts on transient / no-image;
throttles sleep retry_after (up to 3 times). A failed call produces no bytes
and no cost — callers record cost only on success.

CLI:
    python -m src.images.adapter --provider gemini_pro --size 2K --aspect 16:9 \
        --out /tmp/x.png "prompt"
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import logging
import os
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from io import BytesIO
from pathlib import Path
from typing import Any, Callable

import httpx

from src.images import providers as P
from src.images.figure_prompts import (
    build_figure_prompt,
    build_style_closing,
    build_style_override,
    ensure_no_text,
)
from src.images.storage import image_dimensions, sniff_mime

logger = logging.getLogger("images.adapter")

GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta"
ARK_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
DASHSCOPE_URL = ("https://dashscope.aliyuncs.com/api/v1/services/aigc"
                 "/multimodal-generation/generation")

MAX_ATTEMPTS = 2            # transient / text-instead-of-image
MAX_THROTTLE_RETRIES = 3
TRANSIENT_BACKOFF_S = 4.0
DASHSCOPE_THROTTLE_S = 65.0


# ---------------------------------------------------------------------------
# Result + errors
# ---------------------------------------------------------------------------

@dataclass
class ImageResult:
    image_bytes: bytes
    mime_type: str
    provider: str
    model: str
    cost_usd: float
    prompt_sent: str
    width: int | None
    height: int | None
    raw: dict = field(default_factory=dict)

    def to_meta(self) -> dict[str, Any]:
        """Sidecar-ready dict (no bytes)."""
        d = asdict(self)
        d.pop("image_bytes", None)
        d["bytes"] = len(self.image_bytes)
        d["sha256"] = hashlib.sha256(self.image_bytes).hexdigest()
        return d


class ImageProviderError(Exception):
    def __init__(self, message: str, *, provider: str | None = None,
                 transient: bool = False, raw: Any = None):
        super().__init__(message)
        self.provider = provider
        self.transient = transient
        self.raw = raw


class PolicyRejection(ImageProviderError):
    """Input or output blocked by the provider's content filter. Never retried."""


class Throttled(ImageProviderError):
    def __init__(self, message: str, *, retry_after: float = 30.0, **kw):
        super().__init__(message, transient=True, **kw)
        self.retry_after = float(retry_after)


class NoImageReturned(ImageProviderError):
    """Provider answered with text/JSON instead of an image (retried once)."""

    def __init__(self, message: str, *, text: str | None = None, **kw):
        kw.setdefault("transient", True)
        super().__init__(message, **kw)
        self.text = text


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _prep_refs(refs: list[bytes] | None, max_refs: int) -> list[tuple[bytes, str]]:
    """Bound reference images to ≤REF_MAX_EDGE px JPEG (a 4K ref timed out
    against cn-beijing; Anthropic/Gemini resize above 1568 anyway)."""
    out: list[tuple[bytes, str]] = []
    for ref in (refs or [])[:max_refs]:
        if not ref:
            continue
        try:
            from PIL import Image  # type: ignore

            with Image.open(BytesIO(ref)) as im:
                w, h = im.size
                scale = min(1.0, P.REF_MAX_EDGE / max(w, h))
                if scale < 1.0 or im.mode not in ("RGB",) or sniff_mime(ref) != "image/jpeg":
                    im = im.convert("RGB")
                    if scale < 1.0:
                        im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))))
                    buf = BytesIO()
                    im.save(buf, format="JPEG", quality=90)
                    out.append((buf.getvalue(), "image/jpeg"))
                else:
                    out.append((ref, "image/jpeg"))
        except Exception:
            out.append((ref, sniff_mime(ref)))
    if refs and len(refs) > max_refs:
        logger.warning("refs_truncated", extra={"given": len(refs), "kept": max_refs})
    return out


def _data_uri(data: bytes, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"


def _is_throttle(code: str, msg: str) -> bool:
    t = f"{code} {msg}".lower()
    return ("throttl" in t or "requests rate" in t or "too many" in t
            or "rate limit" in t or "ratelimit" in t or code.strip() == "429")


def _is_policy(code: str, msg: str) -> bool:
    t = f"{code} {msg}".lower()
    return ("sensitive" in t or "datainspection" in t or "content_filter" in t
            or "prohibited" in t or "safety" in t or "policy" in t or "blocked" in t)


def _prompt_sha(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:12]


# ---------------------------------------------------------------------------
# Gemini — SDK path (analyzer v1) with REST fallback (veo2)
# ---------------------------------------------------------------------------

_POLICY_FINISH = {"SAFETY", "PROHIBITED_CONTENT", "IMAGE_SAFETY", "IMAGE_PROHIBITED_CONTENT",
                  "BLOCKLIST", "SPII", "RECITATION", "IMAGE_RECITATION", "IMAGE_OTHER"}


def _gemini_sdk(model: str, parts: list[tuple[str, Any]], *, size: str | None, aspect: str | None,
                timeout_s: int, api_key: str) -> tuple[bytes, str, dict]:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key,
                          http_options=types.HttpOptions(timeout=int(timeout_s * 1000)))
    contents = []
    for kind, payload in parts:
        if kind == "image":
            data, mime = payload
            contents.append(types.Part.from_bytes(data=data, mime_type=mime))
        else:
            contents.append(types.Part.from_text(text=payload))
    cfg_kwargs: dict[str, Any] = {"response_modalities": ["TEXT", "IMAGE"]}
    if size or aspect:
        ic: dict[str, Any] = {}
        if aspect:
            ic["aspect_ratio"] = aspect
        if size:
            ic["image_size"] = size          # "1K" | "2K" | "4K" (uppercase K required)
        cfg_kwargs["image_config"] = types.ImageConfig(**ic)
    config = types.GenerateContentConfig(**cfg_kwargs)

    try:
        response = client.models.generate_content(model=model, contents=contents, config=config)
    except genai.errors.APIError as e:  # type: ignore[attr-defined]
        code = str(getattr(e, "code", "") or "")
        msg = str(getattr(e, "message", "") or e)
        if code == "429":
            m = re.search(r"retry(?:Delay|.after)[^\d]*(\d+)", msg, re.I)
            raise Throttled(f"gemini {model}: 429 {msg[:200]}", provider="gemini",
                            retry_after=float(m.group(1)) if m else 30.0)
        if _is_policy(code, msg):
            raise PolicyRejection(f"gemini {model}: {code} {msg[:200]}", provider="gemini")
        raise ImageProviderError(f"gemini {model}: {code} {msg[:300]}", provider="gemini",
                                 transient=code.startswith("5") or code in ("", "408"))

    pf = getattr(response, "prompt_feedback", None)
    if pf is not None and getattr(pf, "block_reason", None):
        raise PolicyRejection(f"gemini {model}: prompt blocked ({pf.block_reason})", provider="gemini")
    cands = getattr(response, "candidates", None) or []
    if not cands:
        raise NoImageReturned(f"gemini {model}: no candidates", provider="gemini")
    cand = cands[0]
    finish = str(getattr(cand, "finish_reason", "") or "")
    finish_name = finish.split(".")[-1].upper()
    text_parts: list[str] = []
    content = getattr(cand, "content", None)
    for part in (getattr(content, "parts", None) or []):
        inline = getattr(part, "inline_data", None)
        if inline is not None and getattr(inline, "data", None):
            data = inline.data
            if isinstance(data, str):
                data = base64.b64decode(data)
            mime = getattr(inline, "mime_type", None) or sniff_mime(data)
            usage = getattr(response, "usage_metadata", None)
            raw = {
                "path": "sdk", "finish_reason": finish_name,
                "usage": {
                    "prompt_tokens": getattr(usage, "prompt_token_count", None),
                    "candidates_tokens": getattr(usage, "candidates_token_count", None),
                    "total_tokens": getattr(usage, "total_token_count", None),
                } if usage else None,
                "text": "".join(text_parts)[:500] or None,
            }
            return data, mime, raw
        if getattr(part, "text", None):
            text_parts.append(part.text)
    if finish_name in _POLICY_FINISH:
        raise PolicyRejection(f"gemini {model}: finish_reason={finish_name}", provider="gemini")
    text = "".join(text_parts)
    raise NoImageReturned(f"gemini {model}: text instead of image: {text[:160]!r}",
                          provider="gemini", text=text)


def _gemini_rest(model: str, parts: list[tuple[str, Any]], *, size: str | None, aspect: str | None,
                 timeout_s: int, api_key: str) -> tuple[bytes, str, dict]:
    """veo2's interactions-endpoint transport (live-verified 2026-08-13)."""
    inputs: list[dict[str, Any]] = []
    for kind, payload in parts:
        if kind == "image":
            data, mime = payload
            inputs.append({"type": "image", "mime_type": mime,
                           "data": base64.b64encode(data).decode("ascii")})
        else:
            inputs.append({"type": "text", "text": payload})
    rf: dict[str, Any] = {"type": "image", "mime_type": "image/jpeg"}
    if aspect:
        rf["aspect_ratio"] = aspect
    if size:
        rf["image_size"] = size
    body = {"model": model, "input": inputs, "response_format": rf}
    r = httpx.post(f"{GEMINI_BASE}/interactions",
                   headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
                   json=body, timeout=timeout_s)
    if r.status_code == 429:
        raise Throttled(f"gemini-rest {model}: 429 {r.text[:200]}", provider="gemini", retry_after=30)
    if r.status_code != 200:
        if _is_policy(str(r.status_code), r.text):
            raise PolicyRejection(f"gemini-rest {model}: {r.status_code} {r.text[:200]}", provider="gemini")
        raise ImageProviderError(f"gemini-rest {model}: {r.status_code} {r.text[:300]}",
                                 provider="gemini", transient=r.status_code >= 500)
    j = r.json()
    for step in j.get("steps", []):
        for part in step.get("content", []):
            if part.get("type") == "image" and part.get("data"):
                data = base64.b64decode(part["data"])
                return data, part.get("mime_type") or sniff_mime(data), {"path": "rest"}
    out = j.get("output_image") or {}
    if out.get("data"):
        data = base64.b64decode(out["data"])
        return data, out.get("mime_type") or sniff_mime(data), {"path": "rest"}
    raise NoImageReturned(f"gemini-rest {model}: no image in response (keys: {sorted(j)})",
                          provider="gemini")


def _gemini(info: dict[str, Any], prompt: str, size: str, aspect: str,
            refs: list[tuple[bytes, str]], timeout_s: int, api_key: str) -> tuple[bytes, str, dict]:
    parts: list[tuple[str, Any]] = [("image", r) for r in refs] + [("text", prompt)]
    try:
        return _gemini_sdk(info["model"], parts, size=size, aspect=aspect,
                           timeout_s=timeout_s, api_key=api_key)
    except (PolicyRejection, Throttled, NoImageReturned):
        raise
    except Exception as sdk_exc:  # noqa: BLE001 — anything else: try the REST path
        rest_model = info.get("rest_model") or info["model"]
        logger.warning("gemini_sdk_failed_trying_rest",
                       extra={"model": info["model"], "rest_model": rest_model,
                              "error": str(sdk_exc)[:300]})
        try:
            data, mime, raw = _gemini_rest(rest_model, parts, size=size if size != "4K" else "2K",
                                           aspect=aspect, timeout_s=timeout_s, api_key=api_key)
        except ImageProviderError as rest_exc:
            rest_exc.raw = {"sdk_error": str(sdk_exc)[:300]}
            raise
        raw["sdk_error"] = str(sdk_exc)[:300]
        raw["model_used"] = rest_model
        return data, mime, raw


# ---------------------------------------------------------------------------
# Ark — Seedream
# ---------------------------------------------------------------------------

def _ark(info: dict[str, Any], prompt: str, size: str, aspect: str,
         refs: list[tuple[bytes, str]], timeout_s: int, api_key: str) -> tuple[bytes, str, dict]:
    model = info["model"]
    body: dict[str, Any] = {"model": model, "prompt": prompt,
                            "size": P.ARK_SIZES[size][aspect], "watermark": False}
    if refs:
        body["image"] = [_data_uri(d, m) for d, m in refs]      # ARRAY (bench-validated, up to 7)
    with httpx.Client(timeout=timeout_s) as client:
        r = client.post(ARK_URL, headers={"Authorization": f"Bearer {api_key}"}, json=body)
        try:
            j = r.json()
        except Exception:
            j = {"error": {"message": r.text[:300]}}
        if r.status_code == 200 and j.get("data"):
            d0 = j["data"][0]
            raw = {"usage": j.get("usage"), "size": body["size"]}
            if d0.get("b64_json"):
                data = base64.b64decode(d0["b64_json"])
                return data, sniff_mime(data), raw
            if d0.get("url"):
                img = client.get(d0["url"])
                img.raise_for_status()
                return img.content, sniff_mime(img.content), raw
        err = j.get("error") or {}
        code = str(err.get("code") or r.status_code)
        msg = str(err.get("message") or j)[:300]
        if r.status_code == 429 or _is_throttle(code, msg):
            raise Throttled(f"ark {model}: {code} {msg}", provider="seedream", retry_after=10)
        if _is_policy(code, msg):
            raise PolicyRejection(f"ark {model}: {code} {msg}", provider="seedream", raw=j)
        raise ImageProviderError(f"ark {model}: {r.status_code} {code} {msg}",
                                 provider="seedream", transient=r.status_code >= 500, raw=j)


# ---------------------------------------------------------------------------
# DashScope — Qwen-Image
# ---------------------------------------------------------------------------

def _dashscope(info: dict[str, Any], prompt: str, size: str, aspect: str,
               refs: list[tuple[bytes, str]], timeout_s: int, api_key: str) -> tuple[bytes, str, dict]:
    model = info["model"]
    content: list[dict[str, str]] = [{"image": _data_uri(d, m)} for d, m in refs]
    content.append({"text": prompt})
    body = {
        "model": model,
        "input": {"messages": [{"role": "user", "content": content}]},
        "parameters": {"watermark": False, "size": P.DASHSCOPE_SIZES[size][aspect],
                       "prompt_extend": False},
    }
    with httpx.Client(timeout=timeout_s) as client:
        r = client.post(DASHSCOPE_URL, headers={"Authorization": f"Bearer {api_key}"}, json=body)
        try:
            j = r.json()
        except Exception:
            j = {"code": str(r.status_code), "message": r.text[:300]}
        if r.status_code == 200:
            try:
                parts = j["output"]["choices"][0]["message"]["content"]
                url = next(c["image"] for c in parts if "image" in c)
            except (KeyError, IndexError, StopIteration, TypeError):
                raise NoImageReturned(f"dashscope {model}: 200 but no image: {str(j)[:200]}",
                                      provider="qwen")
            img = client.get(url)
            img.raise_for_status()
            return img.content, sniff_mime(img.content), {"usage": j.get("usage"),
                                                          "request_id": j.get("request_id"),
                                                          "size": body["parameters"]["size"]}
        code = str(j.get("code", r.status_code))
        msg = str(j.get("message", ""))[:300]
        if r.status_code == 429 or _is_throttle(code, msg):
            raise Throttled(f"dashscope {model}: {code} {msg}", provider="qwen",
                            retry_after=DASHSCOPE_THROTTLE_S)
        if _is_policy(code, msg):
            raise PolicyRejection(f"dashscope {model}: {code} {msg}", provider="qwen", raw=j)
        raise ImageProviderError(f"dashscope {model}: {r.status_code} {code} {msg}",
                                 provider="qwen", transient=r.status_code >= 500, raw=j)


_ADAPTERS: dict[str, Callable[..., tuple[bytes, str, dict]]] = {
    "gemini": _gemini,
    "ark": _ark,
    "dashscope-mm": _dashscope,
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _compose_prompt(prompt: str, style: dict | None, no_text: bool) -> str:
    prompt = (prompt or "").strip()
    if not prompt:
        raise ValueError("prompt must be non-empty")
    if style:
        prompt = build_style_override(style) + prompt + build_style_closing(style)
    if no_text:
        prompt = ensure_no_text(prompt)
    return prompt


def generate_image(
    prompt: str,
    *,
    provider: str = P.DEFAULT_PROVIDER,
    size: str = "2K",
    aspect: str = "16:9",
    refs: list[bytes] | None = None,
    style: dict | None = None,
    no_text: bool = True,
    timeout_s: int = 600,
) -> ImageResult:
    """Generate one image. Raises ImageProviderError / PolicyRejection / Throttled."""
    info = P.provider_info(provider)
    api_key = P.provider_api_key(provider)
    if not api_key:
        raise ImageProviderError(
            f"provider {provider!r} not configured (set one of {list(info['keys_any'])})",
            provider=provider)
    size_used = P.coerce_size(provider, size)
    aspect = P.check_aspect(provider, aspect)
    prompt_sent = _compose_prompt(prompt, style, no_text)
    prepared = _prep_refs(refs, info["max_refs"])
    cost = P.estimate_cost(provider, size_used, len(prepared))
    adapter = _ADAPTERS[info["api"]]
    timeout_s = int(timeout_s or info.get("timeout_s") or 600)

    base_log = {"provider": provider, "model": info["model"], "size": size_used,
                "size_requested": size, "aspect": aspect, "refs": len(prepared),
                "prompt_chars": len(prompt_sent), "prompt_sha": _prompt_sha(prompt_sent)}
    attempt = 0
    throttles = 0
    started = time.monotonic()
    while True:
        attempt += 1
        t0 = time.monotonic()
        logger.info("image_generate_start", extra={**base_log, "attempt": attempt})
        try:
            data, mime, raw = adapter(info, prompt_sent, size_used, aspect, prepared, timeout_s, api_key)
        except Throttled as exc:
            throttles += 1
            if throttles > MAX_THROTTLE_RETRIES:
                logger.error("image_generate_throttled_giveup", extra={**base_log, "error": str(exc)})
                raise
            logger.warning("image_generate_throttled",
                           extra={**base_log, "retry_after_s": exc.retry_after, "throttle_n": throttles})
            time.sleep(exc.retry_after)
            continue
        except PolicyRejection as exc:
            logger.error("image_generate_policy_rejected", extra={**base_log, "error": str(exc)})
            raise
        except ImageProviderError as exc:
            if exc.transient and attempt < MAX_ATTEMPTS:
                logger.warning("image_generate_retry",
                               extra={**base_log, "attempt": attempt, "error": str(exc)[:300]})
                time.sleep(TRANSIENT_BACKOFF_S * attempt)
                continue
            logger.error("image_generate_failed",
                         extra={**base_log, "attempt": attempt, "error": str(exc)[:300]})
            raise
        except (httpx.HTTPError, TimeoutError, OSError) as exc:
            if attempt < MAX_ATTEMPTS:
                logger.warning("image_generate_retry_transport",
                               extra={**base_log, "attempt": attempt, "error": str(exc)[:300]})
                time.sleep(TRANSIENT_BACKOFF_S * attempt)
                continue
            raise ImageProviderError(f"{provider}: transport error: {exc}", provider=provider,
                                     transient=True) from exc
        latency_ms = int((time.monotonic() - t0) * 1000)
        width, height = image_dimensions(data)
        raw = dict(raw or {})
        raw.update({"attempts": attempt, "throttles": throttles, "latency_ms": latency_ms,
                    "total_ms": int((time.monotonic() - started) * 1000),
                    "size_requested": size, "size_used": size_used, "aspect": aspect,
                    "refs": len(prepared), "prompt_sha": base_log["prompt_sha"],
                    "model_used": raw.get("model_used", info["model"])})
        logger.info("image_generate_done", extra={**base_log, "latency_ms": latency_ms,
                                                  "bytes": len(data), "mime": mime,
                                                  "width": width, "height": height,
                                                  "cost_usd": cost})
        return ImageResult(image_bytes=data, mime_type=mime, provider=provider,
                           model=raw.get("model_used", info["model"]), cost_usd=cost,
                           prompt_sent=prompt_sent, width=width, height=height, raw=raw)


def edit_image(
    source: bytes,
    instruction: str,
    *,
    provider: str = P.DEFAULT_PROVIDER,
    size: str | None = None,
    aspect: str | None = None,
    no_text: bool = True,
    timeout_s: int = 600,
) -> ImageResult:
    """Gemini edit mode: source image + instruction → edited image.

    Other providers raise NotImplementedError (Seedream/Qwen have no edit
    endpoint activated on these accounts)."""
    info = P.provider_info(provider)
    if info["api"] != "gemini" or not info.get("supports_edit"):
        raise NotImplementedError(f"edit_image is Gemini-only; {provider!r} does not support edit")
    api_key = P.provider_api_key(provider)
    if not api_key:
        raise ImageProviderError(f"provider {provider!r} not configured", provider=provider)
    if not source:
        raise ValueError("source image is empty")
    instruction = (instruction or "").strip()
    if not instruction:
        raise ValueError("instruction must be non-empty")
    prompt = (
        "You are an image editor. Modify the provided image according to the "
        f"instruction below and return the edited image. Keep everything not mentioned "
        f"unchanged: same composition, medium, palette, framing and subject.\n\n"
        f"INSTRUCTION: {instruction}"
    )
    if no_text:
        prompt = ensure_no_text(prompt)
    src = _prep_refs([source], 1)
    parts: list[tuple[str, Any]] = [("image", src[0]), ("text", prompt)]
    size_used = P.coerce_size(provider, size) if size else None
    if aspect:
        P.check_aspect(provider, aspect)
    cost = P.estimate_cost(provider, size_used or "2K", 1)
    t0 = time.monotonic()
    logger.info("image_edit_start", extra={"provider": provider, "model": info["model"],
                                           "instruction_chars": len(instruction)})
    attempt = 0
    while True:
        attempt += 1
        try:
            data, mime, raw = _gemini_sdk(info["model"], parts, size=size_used, aspect=aspect,
                                          timeout_s=timeout_s, api_key=api_key)
            break
        except NoImageReturned as exc:
            if attempt < MAX_ATTEMPTS:
                logger.warning("image_edit_retry", extra={"error": str(exc)[:200]})
                time.sleep(TRANSIENT_BACKOFF_S)
                continue
            raise
    width, height = image_dimensions(data)
    raw = dict(raw or {})
    raw.update({"mode": "edit", "attempts": attempt,
                "latency_ms": int((time.monotonic() - t0) * 1000)})
    logger.info("image_edit_done", extra={"provider": provider, "latency_ms": raw["latency_ms"],
                                          "bytes": len(data)})
    return ImageResult(image_bytes=data, mime_type=mime, provider=provider, model=info["model"],
                       cost_usd=cost, prompt_sent=prompt, width=width, height=height, raw=raw)


def generate_with_fallback(
    prompt: str,
    providers: list[str] | None = None,
    **kwargs: Any,
) -> ImageResult:
    """Try providers in order; the first success wins. Unconfigured providers
    are skipped; PolicyRejection on one provider still tries the next (their
    filters differ). Raises ImageProviderError with the full trace if all fail."""
    chain = list(providers or ["gemini_pro", "seedream_5_pro"])
    trace: list[dict[str, Any]] = []
    for key in chain:
        if key not in P.PROVIDERS:
            trace.append({"provider": key, "skipped": "unknown provider"})
            continue
        if not P.is_available(key):
            trace.append({"provider": key, "skipped": "not configured"})
            continue
        t0 = time.monotonic()
        try:
            result = generate_image(prompt, provider=key, **kwargs)
        except (ImageProviderError, ValueError) as exc:
            trace.append({"provider": key, "error": str(exc)[:300], "type": type(exc).__name__,
                          "ms": int((time.monotonic() - t0) * 1000)})
            logger.warning("fallback_provider_failed", extra={"provider": key, "error": str(exc)[:200]})
            continue
        trace.append({"provider": key, "ok": True, "ms": int((time.monotonic() - t0) * 1000)})
        result.raw["fallback_trace"] = trace
        return result
    raise ImageProviderError(f"all providers failed: {json.dumps(trace)[:800]}", raw=trace)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m src.images.adapter",
                                 description="Generate one image via the provider fleet.")
    ap.add_argument("prompt", help="prompt text (or scene text when --register is given)")
    ap.add_argument("--provider", default=P.DEFAULT_PROVIDER, choices=sorted(P.PROVIDERS))
    ap.add_argument("--size", default="2K", choices=["1K", "2K", "4K"])
    ap.add_argument("--aspect", default="16:9")
    ap.add_argument("--out", default=None, help="output path (extension follows mime if omitted)")
    ap.add_argument("--ref", action="append", default=[], help="reference image path (repeatable)")
    ap.add_argument("--register", default=None, choices=sorted(__import__("src.images.figure_prompts",
                    fromlist=["REGISTERS"]).REGISTERS),
                    help="wrap the prompt as a figure scene in this register")
    ap.add_argument("--palette", default=None)
    ap.add_argument("--caption", default=None)
    ap.add_argument("--allow-text", action="store_true", help="do not append the NO-TEXT closer")
    ap.add_argument("--fallback", default=None, help="comma-separated provider chain")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--json", action="store_true", help="print result metadata as JSON")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)

    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(asctime)s %(name)s %(levelname)s %(message)s")
    no_text = not args.allow_text
    prompt = args.prompt
    if args.register:
        prompt = build_figure_prompt(prompt, register=args.register, palette=args.palette,
                                     caption=args.caption, no_text=no_text, aspect=args.aspect)
    refs = [Path(p).read_bytes() for p in args.ref]
    t0 = time.monotonic()
    try:
        if args.fallback:
            result = generate_with_fallback(prompt, providers=args.fallback.split(","),
                                            size=args.size, aspect=args.aspect, refs=refs,
                                            no_text=no_text, timeout_s=args.timeout)
        else:
            result = generate_image(prompt, provider=args.provider, size=args.size,
                                    aspect=args.aspect, refs=refs, no_text=no_text,
                                    timeout_s=args.timeout)
    except ImageProviderError as exc:
        print(f"ERROR ({type(exc).__name__}): {exc}", file=sys.stderr)
        return 2
    elapsed = time.monotonic() - t0
    ext = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp"}.get(result.mime_type, "png")
    out = Path(args.out) if args.out else Path(f"figure-{result.provider}-{int(time.time())}.{ext}")
    if out.suffix.lower().lstrip(".") not in (ext, "jpeg" if ext == "jpg" else ext):
        fixed = out.with_suffix(f".{ext}")
        print(f"note: provider returned {result.mime_type}; writing {fixed} instead of {out}",
              file=sys.stderr)
        out = fixed
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(result.image_bytes)
    meta = result.to_meta()
    meta["out"] = str(out)
    meta["elapsed_s"] = round(elapsed, 1)
    if args.json:
        meta.pop("prompt_sent", None)
        print(json.dumps(meta, indent=2, default=str))
    else:
        print(f"{out}  {result.width}x{result.height} {result.mime_type} "
              f"{len(result.image_bytes) // 1024} KB  provider={result.provider} model={result.model} "
              f"cost=${result.cost_usd:.3f} elapsed={elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
