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


# ---------------------------------------------------------------------------
# Diagram check — format + every required label (v1 validate_format_compliance,
# extended with a label manifest). Never raises.
# ---------------------------------------------------------------------------

DIAGRAM_CHECK_PROMPT = """You are reviewing a generated figure for an analytical dossier. It was supposed to be a
{format_name} ({format_key}) titled “{title}”.

FORMAT CHECK — the image SHOULD show: {pass_if}.
It should NOT show: {fail_if}.
It must be a FLAT LABELLED DIAGRAM (shapes, lines, arrows, text), not an illustration: no scenery, no
physical objects, no people, no metaphors, no photographs, no 3D objects. If it is a picture of something
instead of a diagram of the content, format_ok is false.

REQUIRED LABELS — each must appear in the image, legible without zooming, spelled as written:
{labels}

Inspect the image carefully. Read every piece of text in it. Then answer in this exact JSON and nothing else:
{{
  "format_ok": true/false,
  "detected_format": "what the image actually is, in a few words",
  "title_found": true/false,
  "labels_found": ["required labels that appear, spelled correctly and legible"],
  "labels_missing": ["required labels that do not appear at all"],
  "misspelled": [{{"expected": "required label", "seen": "what is printed instead"}}],
  "illegible": ["required labels present but too small, cut off, overlapped or low-contrast"],
  "prohibited_elements": ["scenery, objects, metaphors, photos, 3D, dramatic effects, logos, bylines — if any"],
  "extra_text": ["words in the image that are NOT in the required labels or the title and are not legend entries, axis ticks, +/- marks or quadrant/step numbering (i.e. invented content)"],
  "confidence": "high"/"medium"/"low",
  "suggestion": "one concrete change to the prompt that would fix the worst problem, or null"
}}"""


def _norm_label(s: str) -> str:
    return " ".join(str(s or "").lower().replace("’", "'").split())


def invented_sentences(verdict: dict[str, Any]) -> list[str]:
    """Extra text that reads as a sentence (>= 4 words): invented analytic content, not a legend entry."""
    return [str(t) for t in (verdict.get("extra_text") or []) if len(str(t).split()) >= 4]


def diagram_verdict_ok(verdict: dict[str, Any], n_labels: int) -> bool:
    """The acceptance rule: right format, no prohibited elements, no invented sentences, and at
    most max(1, 20%) of the labels missing/misspelled/illegible."""
    if not verdict.get("format_ok"):
        return False
    if verdict.get("prohibited_elements"):
        return False
    if invented_sentences(verdict):
        return False
    bad = len(verdict.get("labels_missing") or []) + len(verdict.get("misspelled") or []) \
        + len(verdict.get("illegible") or [])
    return bad <= max(1, n_labels // 5)


def check_diagram(
    image_bytes: bytes,
    spec: Any,
    *,
    model: str = DEFAULT_MODEL,
    api_key: str | None = None,
    max_tokens: int = 1500,
) -> dict[str, Any]:
    """Claude-vision verdict on a rendered diagram against its FigureSpec.

    Returns {ok, format_ok, detected_format, title_found, labels_found, labels_missing,
    misspelled, illegible, prohibited_elements, extra_text, suggestion, confidence,
    checked, model, usage, n_labels}. Never raises; without a key → ok=None, checked=False.
    """
    from src.display.enforcement import check_criteria, collect_labels, format_entry, normalize_format_key

    d = spec.model_dump() if hasattr(spec, "model_dump") else dict(spec or {})
    fmt = normalize_format_key(str(d.get("visual_format") or "")) or ""
    labels = collect_labels(d.get("data") or {})
    base: dict[str, Any] = {
        "ok": None, "format_ok": None, "detected_format": None, "title_found": None,
        "labels_found": [], "labels_missing": [], "misspelled": [], "illegible": [],
        "prohibited_elements": [], "extra_text": [], "suggestion": None, "confidence": "low",
        "checked": False, "model": model, "usage": None, "n_labels": len(labels), "issues": [],
    }
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        base["issues"] = ["check skipped: no ANTHROPIC_API_KEY"]
        return base
    if not image_bytes:
        base.update({"ok": False, "issues": ["empty image"]})
        return base
    try:
        import anthropic

        entry = format_entry(fmt) if fmt else {"name": d.get("visual_format") or "diagram"}
        pass_if, fail_if = check_criteria(fmt) if fmt else ([], [])
        data, media_type = _prepare(image_bytes)
        prompt = DIAGRAM_CHECK_PROMPT.format(
            format_name=entry["name"], format_key=fmt or "?", title=str(d.get("title") or ""),
            pass_if="; ".join(pass_if) or "the named format", fail_if="; ".join(fail_if) or "anything pictorial",
            labels="\n".join(f"  {i}. {lab}" for i, lab in enumerate(labels, 1)) or "  (none)",
        )
        client = anthropic.Anthropic(api_key=key)
        resp = client.messages.create(
            model=model, max_tokens=max_tokens,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type,
                                             "data": base64.b64encode(data).decode("ascii")}},
                {"type": "text", "text": prompt},
            ]}],
        )
        raw = "".join(getattr(b, "text", "") for b in resp.content)
        usage = {"input_tokens": getattr(resp.usage, "input_tokens", None),
                 "output_tokens": getattr(resp.usage, "output_tokens", None)}
        try:
            v = _extract_json(raw)
        except Exception:
            logger.warning("diagram_check_parse_error", extra={"preview": raw[:200]})
            base.update({"issues": ["could not parse diagram verdict"], "checked": True, "raw": raw[:500], "usage": usage})
            return base

        def _strs(k: str) -> list[str]:
            return [str(x) for x in (v.get(k) or []) if str(x).strip()]

        # Reconcile the model's lists against the manifest so counts are honest.
        found_norm = {_norm_label(x) for x in _strs("labels_found")}
        missing = [lab for lab in labels if _norm_label(lab) not in found_norm
                   and _norm_label(lab) in {_norm_label(x) for x in _strs("labels_missing")}]
        unaccounted = [lab for lab in labels if _norm_label(lab) not in found_norm and lab not in missing]
        misspelled = [m for m in (v.get("misspelled") or []) if isinstance(m, dict) and m.get("expected")]
        misspelled_norm = {_norm_label(m["expected"]) for m in misspelled}
        illegible = [x for x in _strs("illegible")]
        illegible_norm = {_norm_label(x) for x in illegible}
        # a label the model neither found nor listed anywhere counts as missing
        for lab in unaccounted:
            n = _norm_label(lab)
            if n not in misspelled_norm and n not in illegible_norm:
                missing.append(lab)
        result: dict[str, Any] = {
            "ok": None,
            "format_ok": bool(v.get("format_ok")),
            "detected_format": v.get("detected_format"),
            "title_found": bool(v.get("title_found")),
            "labels_found": [lab for lab in labels if _norm_label(lab) in found_norm],
            "labels_missing": missing,
            "misspelled": misspelled,
            "illegible": illegible,
            "prohibited_elements": _strs("prohibited_elements"),
            "extra_text": _strs("extra_text"),
            "suggestion": v.get("suggestion") or None,
            "confidence": v.get("confidence") or "low",
            "checked": True, "model": model, "usage": usage, "n_labels": len(labels),
        }
        result["ok"] = diagram_verdict_ok(result, len(labels))
        issues = []
        if not result["format_ok"]:
            issues.append(f"wrong format: looks like {result['detected_format']}")
        if result["prohibited_elements"]:
            issues.append("prohibited: " + "; ".join(result["prohibited_elements"][:3]))
        if result["labels_missing"]:
            issues.append(f"{len(result['labels_missing'])} label(s) missing: " + "; ".join(result["labels_missing"][:4]))
        if result["misspelled"]:
            issues.append(f"{len(result['misspelled'])} misspelled: " + "; ".join(
                f"{m['expected']}→{m.get('seen', '?')}" for m in result["misspelled"][:3]))
        if result["illegible"]:
            issues.append(f"{len(result['illegible'])} illegible: " + "; ".join(result["illegible"][:3]))
        inv = invented_sentences(result)
        if inv:
            issues.append(f"{len(inv)} invented sentence(s): " + "; ".join(t[:60] for t in inv[:2]))
        result["issues"] = issues
        logger.info("diagram_check_complete", extra={"ok": result["ok"], "format_ok": result["format_ok"],
                                                     "missing": len(result["labels_missing"])})
        return result
    except Exception as exc:  # noqa: BLE001 — never block rendering on the checker
        logger.error("diagram_check_failed", extra={"error": str(exc)[:300]})
        base["issues"] = [f"check error: {str(exc)[:200]}"]
        return base
