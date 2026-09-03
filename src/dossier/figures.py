"""Step 6 — figures: a FigurePlan of N briefs, then the images contract (src.images.*).

The images modules are written concurrently on feat/images; they are imported
lazily and called through a signature-tolerant shim. If they are absent or any
figure fails, a `figures_skipped` / per-figure note is recorded and the run
continues (the skip law: optional passes never kill the run).
"""
from __future__ import annotations

import inspect
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
    user = (
        f"Plan exactly {n} figure(s).\nANGLE: {opt.title if opt else job.options.intent}\n"
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


def _call_flex(fn, *positional, **kwargs):
    """Call fn with only the kwargs it accepts (the images API is being written concurrently)."""
    try:
        sig = inspect.signature(fn)
        accepts_var = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
        if not accepts_var:
            kwargs = {k: v for k, v in kwargs.items() if k in sig.parameters}
    except (TypeError, ValueError):
        pass
    return fn(*positional, **kwargs)


def _get(obj: Any, *names: str, default=None):
    for name in names:
        if isinstance(obj, dict) and name in obj and obj[name] is not None:
            return obj[name]
        if hasattr(obj, name) and getattr(obj, name) is not None:
            return getattr(obj, name)
    return default


def _generate_one(job: DossierJob, brief: FigureBrief, out_dir: Path, provider: Optional[str]) -> Figure:
    fig = Figure(**brief.model_dump())
    started = time.time()
    try:
        from src.images.adapter import generate_image  # type: ignore
        try:
            from src.images.adapter import generate_with_fallback  # type: ignore
        except Exception:
            generate_with_fallback = None  # type: ignore
        try:
            from src.images.figure_prompts import build_figure_prompt  # type: ignore
        except Exception:
            build_figure_prompt = None  # type: ignore
        try:
            from src.images.storage import save_figure  # type: ignore
        except Exception:
            save_figure = None  # type: ignore
        try:
            from src.images.compliance import check_figure  # type: ignore
        except Exception:
            check_figure = None  # type: ignore
    except Exception as exc:
        fig.status = "skipped"
        fig.note = f"images modules unavailable: {exc}"
        return fig

    prompt = brief.scene
    if build_figure_prompt is not None:
        try:
            built = _call_flex(build_figure_prompt, brief.scene, scene=brief.scene, caption=brief.caption,
                               register=brief.visual_register, style=brief.visual_register, no_text=True)
            prompt = str(_get(built, "prompt", "text", default=built) or brief.scene)
        except Exception as exc:
            events.emit(job.id, "note", phase=STEP, detail=f"{brief.key}: build_figure_prompt failed ({exc}); using the scene as prompt")
    fig.prompt = prompt

    events.emit(job.id, "call_started", phase=STEP, model=provider or "images.default", label=f"figure {brief.key}",
                detail=f"rendering figure {brief.key} ({brief.visual_register})", prompt_excerpt=events.excerpt(prompt, 400))
    gen = generate_with_fallback if generate_with_fallback is not None else generate_image
    result = _call_flex(gen, prompt, prompt=prompt, provider=provider, size="2K", aspect="16:9", no_text=True)
    duration_ms = int((time.time() - started) * 1000)

    provider_used = str(_get(result, "provider", "provider_key", default=provider or "") or provider or "")
    cost = float(_get(result, "cost_usd", "cost", default=0.0) or 0.0)
    fig.provider = provider_used or None
    fig.cost_usd = cost
    fig.figure_id = _get(result, "figure_id", "id")
    fig.url = _get(result, "url")
    fig.path = _get(result, "path")

    image_bytes = _get(result, "bytes", "image_bytes", "data")
    if isinstance(result, (bytes, bytearray)):
        image_bytes = bytes(result)
    if save_figure is not None and image_bytes:
        try:
            saved = _call_flex(save_figure, image_bytes, image_bytes=image_bytes, data=image_bytes, job_id=job.id,
                               key=brief.key, figure_key=brief.key, caption=brief.caption, provider=provider_used, prompt=prompt)
            fig.figure_id = _get(saved, "figure_id", "id", default=fig.figure_id)
            fig.url = _get(saved, "url", default=fig.url)
            fig.path = _get(saved, "path", default=fig.path)
        except Exception as exc:
            events.emit(job.id, "note", phase=STEP, detail=f"{brief.key}: save_figure failed ({exc}); saving locally")
    local = out_dir / f"{brief.key}.png"
    if image_bytes:
        local.write_bytes(image_bytes)
        fig.path = fig.path or str(local)
    elif fig.path and Path(fig.path).exists():
        local.write_bytes(Path(fig.path).read_bytes())
    if not local.exists():
        raise RuntimeError("image generation returned no bytes and no readable path")
    fig.path = str(local)
    if not fig.url:
        fig.url = f"/v1/dossier/jobs/{job.id}/figures/{brief.key}.png"

    if check_figure is not None:
        try:
            verdict = _call_flex(check_figure, str(local), path=str(local), image_path=str(local), image_bytes=local.read_bytes(),
                                 prompt=prompt, caption=brief.caption, no_text=True)
            fig.compliance = verdict if isinstance(verdict, dict) else {"verdict": str(_get(verdict, "verdict", "ok", default=verdict))}
        except Exception as exc:
            fig.compliance = {"error": str(exc)}
    fig.status = "generated"
    record(job.id, make_receipt(step=STEP, kind="image", model=provider_used or "image", label=f"figure {brief.key}",
                                duration_ms=duration_ms, prompt_text=prompt, cost_usd=cost))
    events.emit(job.id, "call_finished", phase=STEP, model=provider_used or "image", label=f"figure {brief.key}",
                cost_usd=cost, duration_ms=duration_ms, detail=f"figure {brief.key} rendered by {provider_used or 'image provider'} (${cost:.3f})")
    events.emit(job.id, "artifact", phase=STEP, detail=f"figure {brief.key}: {brief.caption[:120]}",
                payload_json={"kind": "figure", "key": brief.key, "url": fig.url, "path": fig.path, "figure_id": fig.figure_id, "provider": provider_used})
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
