"""Figure routes — generation, storage and serving of analytical figures
(owner: images agent). Prefix /v1/figures.

    GET  /v1/figures/health
    GET  /v1/figures/providers            available providers with cost/rpm
    POST /v1/figures/generate             generate → (check) → save → {figure_id, url, ...}
    GET  /v1/figures/by-job/{job_id}      sidecars for a job
    GET  /v1/figures/{figure_id}          the image (FileResponse, correct media type)
    GET  /v1/figures/{figure_id}/meta     sidecar JSON
"""

from __future__ import annotations

import logging
import time
from typing import Any

from fastapi import APIRouter, HTTPException, Response
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

from src.images import providers as P
from src.images.adapter import (
    ImageProviderError,
    PolicyRejection,
    Throttled,
    generate_image,
    generate_with_fallback,
)
from src.images.compliance import check_figure
from src.images.figure_prompts import REGISTERS, build_figure_prompt, declutter_scene
from src.images.storage import (
    figure_meta,
    figure_mime,
    figure_path,
    figure_url,
    list_figures,
    save_figure,
)

logger = logging.getLogger("images.routes")

router = APIRouter(prefix="/v1/figures", tags=["figures"])


class GenerateFigureRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    prompt: str = Field(..., min_length=1, description="Prompt, or scene text when register is set")
    provider: str = Field(P.DEFAULT_PROVIDER, description="gemini_pro | gemini_flash | seedream_5_pro | qwen_image_2_pro")
    size: str = Field("2K", description="1K | 2K | 4K (coerced to what the provider supports)")
    aspect: str = "16:9"
    job_id: str = "adhoc"
    name: str | None = Field(None, description="slug for the figure id; defaults to 'figure'")
    register_: str | None = Field(None, alias="register", description="editorial | diagrammatic | photographic | archival — wraps prompt via build_figure_prompt")
    caption: str | None = None
    palette: str | None = None
    no_text: bool = True
    check: bool = Field(False, description="run the Claude-vision compliance check")
    declutter: bool = Field(False, description="Sonnet pass: compress scene to one depictable picture")
    fallback: list[str] | None = Field(None, description="provider chain; when set, overrides provider")
    style: dict[str, Any] | None = None
    extra_prohibitions: list[str] | None = None
    meta: dict[str, Any] = Field(default_factory=dict)


@router.get("/health")
def figures_health():
    return {"ok": True, "component": "figures", "providers": P.available_providers()}


@router.get("/providers")
def figures_providers(all: bool = False):
    """Key-gated provider table (cost per image, rpm, sizes, aspects)."""
    return {"providers": P.describe_providers(only_available=not all),
            "default": P.DEFAULT_PROVIDER,
            "registers": sorted(REGISTERS)}


@router.post("/generate")
async def figures_generate(req: GenerateFigureRequest):
    if req.register_ and req.register_ not in REGISTERS:
        raise HTTPException(400, f"unknown register {req.register_!r}; known: {sorted(REGISTERS)}")
    chain = req.fallback or [req.provider]
    for key in chain:
        if key not in P.PROVIDERS:
            raise HTTPException(400, f"unknown provider {key!r}; known: {sorted(P.PROVIDERS)}")
    if not any(P.is_available(k) for k in chain):
        raise HTTPException(503, f"no configured provider among {chain}; available: {P.available_providers()}")

    scene = req.prompt
    if req.declutter:
        scene = await run_in_threadpool(declutter_scene, scene)
    prompt = scene
    if req.register_:
        prompt = build_figure_prompt(scene, register=req.register_, palette=req.palette,
                                     caption=req.caption, no_text=req.no_text,
                                     extra_prohibitions=req.extra_prohibitions, aspect=req.aspect,
                                     style=req.style)
        style = None                     # already folded into the prompt
    else:
        style = req.style

    t0 = time.monotonic()
    try:
        if req.fallback:
            result = await run_in_threadpool(
                generate_with_fallback, prompt, req.fallback, size=req.size, aspect=req.aspect,
                style=style, no_text=req.no_text)
        else:
            result = await run_in_threadpool(
                generate_image, prompt, provider=req.provider, size=req.size, aspect=req.aspect,
                style=style, no_text=req.no_text)
    except PolicyRejection as exc:
        raise HTTPException(422, f"content policy rejection: {exc}")
    except Throttled as exc:
        raise HTTPException(429, f"provider throttled: {exc}",
                            headers={"Retry-After": str(int(exc.retry_after))})
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    except ImageProviderError as exc:
        raise HTTPException(502, f"image provider error: {exc}")
    latency_ms = int((time.monotonic() - t0) * 1000)

    compliance: dict[str, Any] | None = None
    if req.check:
        expectation = req.caption or scene
        compliance = await run_in_threadpool(check_figure, result.image_bytes, expectation,
                                             no_text=req.no_text)

    meta = {
        **result.to_meta(),
        "scene": scene,
        "register": req.register_,
        "caption": req.caption,
        "palette": req.palette,
        "no_text": req.no_text,
        "latency_ms": latency_ms,
        "compliance": compliance,
        **(req.meta or {}),
    }
    figure_id = await run_in_threadpool(
        save_figure, result.image_bytes, result.mime_type,
        job_id=req.job_id, name=req.name or "figure", meta=meta)
    logger.info("figure_generated", extra={"figure_id": figure_id, "provider": result.provider,
                                           "cost_usd": result.cost_usd, "latency_ms": latency_ms})
    return {
        "figure_id": figure_id,
        "url": figure_url(figure_id),
        "cost_usd": result.cost_usd,
        "provider": result.provider,
        "model": result.model,
        "mime_type": result.mime_type,
        "width": result.width,
        "height": result.height,
        "latency_ms": latency_ms,
        "compliance": compliance,
        "prompt_chars": len(result.prompt_sent),
    }


@router.get("/by-job/{job_id}")
def figures_by_job(job_id: str):
    figs = list_figures(job_id)
    return {"job_id": job_id, "count": len(figs), "figures": figs}


@router.get("/{figure_id}/meta")
def figures_meta(figure_id: str):
    try:
        return figure_meta(figure_id)
    except (FileNotFoundError, ValueError):
        raise HTTPException(404, f"figure {figure_id!r} not found")


@router.get("/{figure_id}")
def figures_get(figure_id: str):
    try:
        path = figure_path(figure_id)
    except (FileNotFoundError, ValueError):
        raise HTTPException(404, f"figure {figure_id!r} not found")
    return FileResponse(path, media_type=figure_mime(figure_id), filename=path.name,
                        headers={"Cache-Control": "public, max-age=31536000, immutable"})
