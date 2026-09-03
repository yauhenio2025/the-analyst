"""Step 6 — figures: a FigurePlan of N briefs, then the images contract (src.images.*).

The images modules are written concurrently on feat/images; they are imported
lazily and called through a signature-tolerant shim. If they are absent or any
figure fails, a `figures_skipped` / per-figure note is recorded and the run
continues (the skip law: optional passes never kill the run).
"""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any, Optional

from src.dossier import events
from src.dossier.common import AUDIENCE_REGISTER, analysis_prose, compact_profiles, job_dir
from src.dossier.llm import call_json
from src.dossier.receipts import make_receipt, record
from src.dossier.schemas import DossierJob, Figure, FigureBrief
from src.sources.schemas import Document

logger = logging.getLogger(__name__)

STEP = "figures"

FIGURES_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["figures"],
    "properties": {"figures": {"type": "array", "minItems": 1, "maxItems": 4,
                               "items": {"type": "object", "additionalProperties": False,
                                         "required": ["key", "caption", "scene", "register"],
                                         "properties": {"key": {"type": "string", "description": "snake_case"},
                                                        "caption": {"type": "string", "description": "what the reader should see in it and why it matters, one or two sentences"},
                                                        "scene": {"type": "string", "description": "a concrete, depictable scene for an image model: subjects, setting, materials, light, composition. NO words, letters, logos, charts or labels in the image."},
                                                        "register": {"type": "string", "description": "visual register, e.g. editorial photograph, architectural drawing, still life, documentary"}}}}},
}

SYSTEM = """You are the figures desk of The Analyst. You plan the few images a dossier needs: each figure makes one idea from the
analysis visible as a concrete scene an image model can render — objects, places, people at work, materials, contrasts —
never diagrams, never text, never logos, never charts. Captions carry the meaning; the picture carries the feeling of it."""


def plan_figures(job: DossierJob, n: int) -> list[FigureBrief]:
    from src.dossier.plan import chosen_option

    opt = chosen_option(job)
    ideas = " | ".join(opt.output_shape.figures) if opt and opt.output_shape.figures else "(none)"
    regs = known_registers()
    reg_line = f"Allowed registers: {', '.join(regs)}\n" if regs else ""
    user = (
        f"Plan exactly {n} figure(s).\n{reg_line}ANGLE: {opt.title if opt else job.options.intent}\n"
        f"AUDIENCE: {job.options.audience} — {AUDIENCE_REGISTER.get(job.options.audience, '')}\n"
        f"Figure ideas from the brief: {ideas}\n\nANALYSIS PROSE (abridged):\n{analysis_prose(job, 25_000)[:60_000]}\n\n"
        f"PROFILES (abridged):\n{compact_profiles(job.profiles)[:8000]}"
    )
    raw, _ = call_json(job.id, STEP, label=f"figure plan ({n})", system=SYSTEM, user=user,
                       tool_name="record_figure_plan", schema=FIGURES_SCHEMA, model_cls=None, max_tokens=3000)
    briefs = []
    for f in (raw or {}).get("figures", [])[:n]:
        try:
            briefs.append(FigureBrief(key=str(f.get("key", f"figure_{len(briefs)+1}")).strip().lower().replace(" ", "_"),
                                      caption=str(f.get("caption", "")), scene=str(f.get("scene", "")),
                                      visual_register=str(f.get("register", "editorial"))))
        except Exception as exc:
            logger.warning(f"figure brief rejected: {exc}")
    return briefs


def _get(obj: Any, *names: str, default=None):
    for name in names:
        if isinstance(obj, dict) and name in obj and obj[name] is not None:
            return obj[name]
        if hasattr(obj, name) and getattr(obj, name) is not None:
            return getattr(obj, name)
    return default


def known_registers() -> list[str]:
    try:
        from src.images.figure_prompts import REGISTERS  # type: ignore

        return sorted(REGISTERS)
    except Exception:
        return []


def _coerce_register(value: str) -> str:
    regs = known_registers()
    if not regs:
        return value
    v = (value or "").strip().lower().replace(" ", "_")
    if v in regs:
        return v
    for r in regs:
        if r in v or v in r:
            return r
    try:
        from src.images.figure_prompts import DEFAULT_REGISTER  # type: ignore

        return DEFAULT_REGISTER
    except Exception:
        return regs[0]


def _generate_one(job: DossierJob, brief: FigureBrief, out_dir: Path, provider: Optional[str]) -> Figure:
    """One figure through the images contract: build prompt → generate (with fallback) → save → compliance."""
    from src.images.adapter import generate_image, generate_with_fallback
    from src.images.compliance import check_figure
    from src.images.figure_prompts import build_figure_prompt
    from src.images.storage import figure_url, save_figure

    fig = Figure(**brief.model_dump())
    register = _coerce_register(brief.visual_register)
    fig.visual_register = register
    try:
        prompt = build_figure_prompt(brief.scene, register=register, caption=brief.caption, no_text=True, aspect="16:9")
    except Exception as exc:
        events.emit(job.id, "note", phase=STEP, detail=f"{brief.key}: build_figure_prompt failed ({exc}); using the scene as prompt")
        prompt = brief.scene
    fig.prompt = prompt

    label = f"figure {brief.key}"
    events.emit(job.id, "call_started", phase=STEP, model=provider or "images.fallback_chain", label=label,
                detail=f"rendering {brief.key} as {register} (2K, 16:9, no text)", prompt_excerpt=events.excerpt(prompt, 500))
    started = time.time()
    if provider:
        result = generate_image(prompt, provider=provider, size="2K", aspect="16:9", no_text=True)
    else:
        result = generate_with_fallback(prompt, size="2K", aspect="16:9", no_text=True)
    duration_ms = int((time.time() - started) * 1000)

    image_bytes: bytes = _get(result, "image_bytes", default=b"") or b""
    mime = str(_get(result, "mime_type", default="image/png") or "image/png")
    provider_used = str(_get(result, "provider", default=provider or "") or "")
    model_used = str(_get(result, "model", default="") or "")
    cost = float(_get(result, "cost_usd", default=0.0) or 0.0)
    if not image_bytes:
        raise RuntimeError("image provider returned no bytes")

    compliance = None
    try:
        compliance = check_figure(image_bytes, f"{brief.caption}\nScene: {brief.scene}", no_text=True)
    except Exception as exc:
        compliance = {"ok": None, "checked": False, "issues": [f"check failed: {exc}"]}

    meta = {"prompt": brief.scene, "prompt_sent": prompt, "provider": provider_used, "model": model_used,
            "cost_usd": cost, "size": "2K", "aspect": "16:9", "caption": brief.caption, "register": register,
            "scene": brief.scene, "compliance": compliance, "latency_ms": duration_ms, "dossier_job_id": job.id}
    figure_id = None
    try:
        figure_id = save_figure(image_bytes, mime, job_id=job.id, name=brief.key, meta=meta)
        fig.url = figure_url(figure_id)
    except Exception as exc:
        events.emit(job.id, "note", phase=STEP, detail=f"{brief.key}: save_figure failed ({exc}); keeping the local copy only")
    ext = {"image/jpeg": "jpg", "image/webp": "webp"}.get(mime, "png")
    local = out_dir / f"{brief.key}.{ext}"
    local.write_bytes(image_bytes)
    fig.figure_id = figure_id
    fig.path = str(local)
    fig.url = fig.url or f"/v1/dossier/jobs/{job.id}/figures/{local.name}"
    fig.provider = provider_used or None
    fig.cost_usd = cost
    fig.compliance = compliance
    fig.status = "generated"
    if isinstance(compliance, dict) and compliance.get("checked") and compliance.get("ok") is False:
        fig.note = "compliance: " + "; ".join(str(i) for i in compliance.get("issues", [])[:3])

    record(job.id, make_receipt(step=STEP, kind="image", model=model_used or provider_used or "image", label=label,
                                duration_ms=duration_ms, prompt_text=prompt, cost_usd=cost))
    events.emit(job.id, "call_finished", phase=STEP, model=model_used or provider_used, label=label, cost_usd=cost,
                duration_ms=duration_ms, detail=f"{brief.key} rendered by {provider_used} in {duration_ms/1000:.0f}s (${cost:.3f})"
                + (f" — compliance issues: {fig.note}" if fig.note else ""),
                payload_json={"figure_id": figure_id, "compliance": compliance})
    events.emit(job.id, "artifact", phase=STEP, detail=f"figure {brief.key}: {brief.caption[:120]}",
                payload_json={"kind": "figure", "key": brief.key, "url": fig.url, "path": fig.path,
                              "figure_id": figure_id, "provider": provider_used, "cost_usd": cost})
    return fig


def run_figures(job: DossierJob, docs: list[Document]) -> list[Figure]:
    n = int(job.options.output.figures or 0)
    if n <= 0:
        events.emit(job.id, "note", phase=STEP, detail="figures_skipped: none requested")
        return []
    briefs = plan_figures(job, n)
    events.emit(job.id, "artifact", phase=STEP, detail=f"figure plan: {len(briefs)} briefs",
                payload_json={"kind": "figure_plan", "figures": [b.model_dump() for b in briefs]})
    out_dir = job_dir(job.id) / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        import src.images.adapter  # noqa: F401  (lazy — the images agent's module)
        images_available = True
    except Exception as exc:
        images_available = False
        events.emit(job.id, "note", phase=STEP, detail=f"figures_skipped: images modules not available ({exc.__class__.__name__}: {exc})",
                    payload_json={"kind": "figures_skipped", "reason": str(exc)})
    figures: list[Figure] = []
    for brief in briefs:
        if not images_available:
            figures.append(Figure(**brief.model_dump(), status="skipped", note="images modules not merged"))
            continue
        try:
            figures.append(_generate_one(job, brief, out_dir, job.options.image_provider))
        except Exception as exc:
            logger.warning(f"figure {brief.key} failed: {exc}", exc_info=True)
            events.emit(job.id, "call_failed", phase=STEP, label=f"figure {brief.key}", detail=f"figure {brief.key} failed: {exc}")
            figures.append(Figure(**brief.model_dump(), status="failed", note=str(exc)[:300]))
    return figures
