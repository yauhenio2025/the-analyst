"""Operationalization API routes.

Serves the bridge layer between stances (HOW) and engines (WHAT).
Each engine can have an operationalization file specifying how each
stance applies and what depth sequences are available.
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from src.engines.discovery import resolve_capability_definition
from src.operationalizations.registry import get_operationalization_registry
from src.operationalizations.schemas import (
    CoverageMatrix,
    DepthSequence,
    EngineOperationalization,
    OperationalizationSummary,
    ProcessSpec,
    StanceOperationalization,
)
from src.stages.capability_composer import (
    compose_pass_prompt,
    PassPrompt,
)
from src.engines.registry import get_engine_registry
from src.engines.schemas_v2 import PassDefinition

router = APIRouter(prefix="/operationalizations", tags=["operationalizations"])


# ── Registry accessor ───────────────────────────────────────────────────

def _get_registry():
    return get_operationalization_registry()


def _canonicalize_engine_key(engine_key: str) -> str:
    cap_def = resolve_capability_definition(get_engine_registry(), engine_key)
    return cap_def.engine_key if cap_def is not None else engine_key


def _get_operationalization_or_404(engine_key: str) -> tuple[str, EngineOperationalization]:
    reg = _get_registry()
    canonical_key = _canonicalize_engine_key(engine_key)
    op = reg.get(canonical_key)
    if op is None:
        raise HTTPException(
            status_code=404,
            detail=f"No operationalization for engine '{engine_key}'",
        )
    return canonical_key, op


# ── List / Coverage ─────────────────────────────────────────────────────

@router.get("/", response_model=list[OperationalizationSummary])
async def list_operationalizations():
    """List all engine operationalizations (summaries)."""
    reg = _get_registry()
    return reg.list_summaries()


@router.get("/coverage", response_model=CoverageMatrix)
async def get_coverage():
    """Get the engine x stance coverage matrix."""
    reg = _get_registry()
    return reg.coverage_matrix()


# ── Single engine ───────────────────────────────────────────────────────

@router.get("/{engine_key}", response_model=EngineOperationalization)
async def get_operationalization(engine_key: str):
    """Get the full operationalization for an engine."""
    _, op = _get_operationalization_or_404(engine_key)
    return op


@router.put("/{engine_key}", response_model=EngineOperationalization)
async def update_operationalization(engine_key: str, body: EngineOperationalization):
    """Update the full operationalization for an engine."""
    canonical_key = _canonicalize_engine_key(engine_key)
    if body.engine_key != canonical_key:
        raise HTTPException(
            status_code=400,
            detail="engine_key in body must match canonical engine key",
        )
    reg = _get_registry()
    success = reg.save(canonical_key, body)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save operationalization")
    return body


# ── Stance operationalizations ──────────────────────────────────────────

@router.get("/{engine_key}/stances", response_model=list[StanceOperationalization])
async def list_stance_ops(engine_key: str):
    """List all stance operationalizations for an engine."""
    _, op = _get_operationalization_or_404(engine_key)
    return op.stance_operationalizations


@router.get("/{engine_key}/stances/{stance_key}", response_model=StanceOperationalization)
async def get_stance_op(engine_key: str, stance_key: str):
    """Get a specific stance operationalization for an engine."""
    canonical_key, _ = _get_operationalization_or_404(engine_key)
    reg = _get_registry()
    stance_op = reg.get_stance_for_engine(canonical_key, stance_key)
    if stance_op is None:
        raise HTTPException(
            status_code=404,
            detail=f"No operationalization for stance '{stance_key}' on engine '{engine_key}'",
        )
    return stance_op


@router.put("/{engine_key}/stances/{stance_key}", response_model=StanceOperationalization)
async def update_stance_op(
    engine_key: str,
    stance_key: str,
    body: StanceOperationalization,
):
    """Update a specific stance operationalization for an engine."""
    canonical_key, op = _get_operationalization_or_404(engine_key)
    reg = _get_registry()

    if body.stance_key != stance_key:
        raise HTTPException(status_code=400, detail="stance_key in body must match URL")

    # Replace or append
    found = False
    for i, existing in enumerate(op.stance_operationalizations):
        if existing.stance_key == stance_key:
            op.stance_operationalizations[i] = body
            found = True
            break

    if not found:
        op.stance_operationalizations.append(body)

    reg.save(canonical_key, op)
    return body


# ── Depth sequences ─────────────────────────────────────────────────────

@router.get("/{engine_key}/depths/{depth_key}", response_model=DepthSequence)
async def get_depth_sequence(engine_key: str, depth_key: str):
    """Get the depth sequence for a specific depth level."""
    canonical_key, _ = _get_operationalization_or_404(engine_key)
    reg = _get_registry()
    seq = reg.get_depth_sequence(canonical_key, depth_key)
    if seq is None:
        raise HTTPException(
            status_code=404,
            detail=f"No depth sequence for '{depth_key}' on engine '{engine_key}'",
        )
    return seq


@router.put("/{engine_key}/depths/{depth_key}", response_model=DepthSequence)
async def update_depth_sequence(
    engine_key: str,
    depth_key: str,
    body: DepthSequence,
):
    """Update the depth sequence for a specific depth level."""
    canonical_key, op = _get_operationalization_or_404(engine_key)
    reg = _get_registry()

    if body.depth_key != depth_key:
        raise HTTPException(status_code=400, detail="depth_key in body must match URL")

    # Replace or append
    found = False
    for i, existing in enumerate(op.depth_sequences):
        if existing.depth_key == depth_key:
            op.depth_sequences[i] = body
            found = True
            break

    if not found:
        op.depth_sequences.append(body)

    reg.save(canonical_key, op)
    return body


# ── Compose preview ─────────────────────────────────────────────────────

class ComposePreviewRequest(BaseModel):
    """Request body for compose preview."""
    depth_key: str = Field(default="standard", description="Depth level to compose for")
    pass_number: int = Field(default=1, description="Pass number to preview")


@router.post("/{engine_key}/compose-preview", response_model=PassPrompt)
async def compose_preview(engine_key: str, body: ComposePreviewRequest):
    """Preview the composed prompt for a specific pass using operationalization data.

    This builds a PassDefinition from the operationalization layer and
    composes the prompt as it would be at runtime.
    """
    canonical_key, op = _get_operationalization_or_404(engine_key)
    op_reg = _get_registry()

    # Get the depth sequence
    depth_seq = op.get_depth_sequence(body.depth_key)
    if depth_seq is None:
        raise HTTPException(
            status_code=404,
            detail=f"No depth sequence for '{body.depth_key}' on engine '{engine_key}'",
        )

    # Find the pass entry
    pass_entry = None
    for pe in depth_seq.passes:
        if pe.pass_number == body.pass_number:
            pass_entry = pe
            break

    if pass_entry is None:
        raise HTTPException(
            status_code=404,
            detail=f"No pass {body.pass_number} in depth '{body.depth_key}' for engine '{engine_key}'",
        )

    # Get the stance operationalization
    stance_op = op.get_stance_op(pass_entry.stance_key)
    if stance_op is None:
        raise HTTPException(
            status_code=404,
            detail=f"No operationalization for stance '{pass_entry.stance_key}' on engine '{engine_key}'",
        )

    # Get engine capability definition
    engine_reg = get_engine_registry()
    cap_def = resolve_capability_definition(engine_reg, engine_key)
    if cap_def is None:
        raise HTTPException(status_code=404, detail=f"No capability definition for engine '{engine_key}'")

    # Build a PassDefinition from operationalization data
    pass_def = PassDefinition(
        pass_number=pass_entry.pass_number,
        label=stance_op.label,
        stance=pass_entry.stance_key,
        description=stance_op.description,
        focus_dimensions=stance_op.focus_dimensions,
        focus_capabilities=stance_op.focus_capabilities,
        consumes_from=pass_entry.consumes_from,
    )

    return compose_pass_prompt(
        cap_def=cap_def,
        pass_def=pass_def,
        depth=body.depth_key,
    )


# ── The process shape (study 2026-09-04) ─────────────────────────────────

@router.get("/{engine_key}/process", response_model=ProcessSpec)
async def get_process(engine_key: str):
    """The engine's extract → verify → synthesize process, if it has one."""
    _, op = _get_operationalization_or_404(engine_key)
    if op.process is None:
        raise HTTPException(status_code=404, detail=f"No process for engine '{engine_key}'")
    return op.process


class ProcessPreviewRequest(BaseModel):
    document_text: str = Field("(document text)", description="Text to compose against (only its length matters for a preview)")
    doc_key: str = "document"


class ProcessPreviewPrompt(BaseModel):
    step_key: str
    kind: str
    dimension_key: str = ""
    model_tier: str
    model: str
    system: str
    user_chars: int


@router.post("/{engine_key}/process-preview", response_model=list[ProcessPreviewPrompt])
async def preview_process(engine_key: str, req: ProcessPreviewRequest):
    """Every prompt the process would send (no calls): extraction per dimension, verify, synthesize, with the routed model."""
    from src.executor.process_runner import preview_prompts, resolve_step_model

    canonical, op = _get_operationalization_or_404(engine_key)
    if op.process is None:
        raise HTTPException(status_code=404, detail=f"No process for engine '{engine_key}'")
    cap_def = resolve_capability_definition(get_engine_registry(), canonical)
    if cap_def is None:
        raise HTTPException(status_code=404, detail=f"No capability definition for '{engine_key}'")
    out = []
    for pp in preview_prompts(cap_def, op.process, {req.doc_key: req.document_text}):
        step = op.process.get_step(pp.step_key)
        model = resolve_step_model(step, op.process) if step else ""
        out.append(ProcessPreviewPrompt(step_key=pp.step_key, kind=pp.kind, dimension_key=pp.dimension_key,
                                        model_tier=pp.model_tier, model=model, system=pp.system, user_chars=len(pp.user)))
    return out
