"""Claude-vision compliance check for generated figures.

Lifted from analyzer src/renderers/gemini_image.py `validate_format_compliance`
(JSON verdict, fail-open on parse/transport errors) and re-aimed at
editorial figures: does the image match the expectation, is there rendered
text, are there garbled artefacts or identifiable real people.

`check_figure` NEVER raises. Without ANTHROPIC_API_KEY it returns ok=True
with issue "check skipped".
"""

from __future__ import annotations

import base64
import json
import logging
import os
import re
from io import BytesIO
from typing import Any

logger = logging.getLogger("images.compliance")

DEFAULT_MODEL = "claude-sonnet-4-6"
_MAX_EDGE = 1568           # Anthropic resizes above this anyway; keeps payload < 5 MB
_MAX_BYTES = 4_500_000

CHECK_PROMPT = """You are reviewing a generated figure for an analytical dossier.

EXPECTATION (what the figure was supposed to show and how):
{expectation}

Inspect the image carefully and answer:
1. Does it depict the expectation (subject, structure, relationships, register)?
2. Is there ANY rendered text, lettering, numbers, labels, captions, watermarks or
   logos in the image? {text_rule}
3. Are there garbled artefacts (melted shapes, extra limbs, duplicated figures, broken
   geometry, gibberish glyphs)?
4. Does it show a recognizable real person, real brand, or real logo?
5. Is it cluttered (many focal points, > ~8 distinct elements) or melodramatic
   (explosions, lightning, storms) rather than composed and calm?

Respond in this exact JSON format and nothing else:
{{
  "compliant": true/false,
  "confidence": "high"/"medium"/"low",
  "detected": "one sentence: what the image actually shows",
  "has_text": true/false,
  "issues": ["specific", "problems", "found"],
  "recommendation": "one concrete prompt change that would fix the worst issue, or null"
}}"""


def _prepare(image_bytes: bytes) -> tuple[bytes, str]:
    """Downscale/re-encode to JPEG ≤1568px for the vision call when Pillow is
    available; otherwise pass through with a sniffed media type."""
    try:
        from PIL import Image  # type: ignore

        with Image.open(BytesIO(image_bytes)) as im:
            im = im.convert("RGB")
            w, h = im.size
            scale = min(1.0, _MAX_EDGE / max(w, h))
            if scale < 1.0:
                im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))))
            buf = BytesIO()
            im.save(buf, format="JPEG", quality=88)
            data = buf.getvalue()
            if len(data) > _MAX_BYTES:
                buf = BytesIO()
                im.save(buf, format="JPEG", quality=70)
                data = buf.getvalue()
            return data, "image/jpeg"
    except Exception:
        from src.images.storage import sniff_mime

        return image_bytes, sniff_mime(image_bytes)


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if "```" in text:
        m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
        if m:
            text = m.group(1)
    if not text.startswith("{"):
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            text = m.group(0)
    return json.loads(text)


def check_figure(
    image_bytes: bytes,
    expectation: str,
    *,
    model: str = DEFAULT_MODEL,
    no_text: bool = True,
    api_key: str | None = None,
    max_tokens: int = 600,
) -> dict[str, Any]:
    """Return {ok, issues, suggestion, confidence, detected, has_text, checked, model}."""
    base: dict[str, Any] = {
        "ok": True, "issues": [], "suggestion": None, "confidence": "low",
        "detected": None, "has_text": None, "checked": False, "model": model,
    }
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        base["issues"] = ["check skipped: no ANTHROPIC_API_KEY"]
        return base
    if not image_bytes:
        base["ok"] = False
        base["issues"] = ["empty image"]
        return base
    try:
        import anthropic

        data, media_type = _prepare(image_bytes)
        text_rule = (
            "Rendered text of ANY kind is a violation for this figure."
            if no_text else
            "Text is permitted only if legible, correctly spelled and part of the expectation."
        )
        prompt = CHECK_PROMPT.format(expectation=(expectation or "").strip() or "(none given)",
                                     text_rule=text_rule)
        client = anthropic.Anthropic(api_key=key)
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image",
                     "source": {"type": "base64", "media_type": media_type,
                                "data": base64.b64encode(data).decode("ascii")}},
                    {"type": "text", "text": prompt},
                ],
            }],
        )
        raw = "".join(getattr(b, "text", "") for b in resp.content)
        try:
            verdict = _extract_json(raw)
        except Exception:
            logger.warning("compliance_parse_error", extra={"preview": raw[:200]})
            base.update({"issues": ["could not parse compliance verdict"],
                         "checked": True, "raw": raw[:500]})
            return base
        issues = [str(i) for i in (verdict.get("issues") or [])]
        has_text = bool(verdict.get("has_text"))
        ok = bool(verdict.get("compliant", True))
        if no_text and has_text:
            ok = False
            if not any("text" in i.lower() for i in issues):
                issues.append("rendered text present in a no-text figure")
        result = {
            "ok": ok,
            "issues": issues,
            "suggestion": verdict.get("recommendation") or None,
            "confidence": verdict.get("confidence") or "low",
            "detected": verdict.get("detected"),
            "has_text": has_text,
            "checked": True,
            "model": model,
            "usage": {
                "input_tokens": getattr(resp.usage, "input_tokens", None),
                "output_tokens": getattr(resp.usage, "output_tokens", None),
            },
        }
        logger.info("compliance_complete", extra={k: result[k] for k in ("ok", "confidence", "has_text")})
        return result
    except Exception as exc:  # noqa: BLE001 — never block rendering on the checker
        logger.error("compliance_failed", extra={"error": str(exc)[:300]})
        base["issues"] = [f"check error: {str(exc)[:200]}"]
        return base
