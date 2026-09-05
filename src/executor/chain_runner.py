"""Sequential chain execution for the executor.

A chain is a sequence of engines that run one after another, each receiving
the previous engine's output as context. The chain runner:

1. Loads the chain definition (engine_keys, blend_mode)
2. For each engine in the chain:
   a. Loads the CapabilityEngineDefinition
   b. Composes prompts using the capability_composer
   c. Runs multi-pass execution (via operationalizations)
   d. Threads output as context to the next engine
3. Returns the final engine's output as the chain result

Plan overrides (depth, focus_dimensions) are applied per-engine.

Ported from The Critic's execute_chain() with plan-driven override support.
"""

import logging
import time
from typing import Any, Callable, Optional

from src.aoi.contract import build_aoi_output_metadata
from src.chains.registry import get_chain_registry
from src.engines.registry import get_engine_registry
from src.executor.context_broker import (
    assemble_chain_context,
    assemble_inner_pass_context,
)
from src.executor.engine_runner import run_engine_call, run_engine_call_auto
from src.executor.job_manager import update_job_tokens
from src.events import context as _events_context
from src.events import hooks as _events_hooks
from src.executor.output_store import (
    get_completed_passes,
    load_engine_last_pass_content,
    load_pass_content,
    save_output,
)
from src.executor.schemas import EngineCallResult
from src.operationalizations.registry import get_operationalization_registry
from src.stages.capability_composer import (
    compose_all_pass_prompts,
    compose_pass_prompt,
)

logger = logging.getLogger(__name__)


def run_chain(
    chain_key: str,
    document_text: str,
    *,
    job_id: str,
    phase_number: float,
    work_key: str = "",
    depth: str = "standard",
    engine_overrides: Optional[dict[str, dict]] = None,
    context_emphasis: Optional[str] = None,
    upstream_context: str = "",
    model_hint: Optional[str] = None,
    requires_full_documents: bool = False,
    cancellation_check: Optional[Callable[[], bool]] = None,
    progress_callback: Optional[Callable[[str], None]] = None,
    documents: Optional[dict[str, str]] = None,
    document_context: str = "",
) -> dict:
    """Execute a chain of engines sequentially.

    Args:
        chain_key: Chain definition key
        document_text: The document text to analyze
        documents: Selected raw sources keyed by stable source identity, for process modes.
            Omit for the legacy single-document input. Never put generated context here.
        document_context: Source labels/scope or generated summaries for process context only.
        job_id: Job ID for output persistence
        phase_number: Current phase number
        work_key: Work identifier (for per-work phases)
        depth: Default depth for all engines in the chain
        engine_overrides: Per-engine depth/focus overrides from the plan
        context_emphasis: Emphasis text to prepend to context
        upstream_context: Context from upstream phases
        model_hint: Default model hint for all engines
        requires_full_documents: Whether to use 1M context
        cancellation_check: Callable that returns True to cancel
        progress_callback: Callable for progress updates

    Returns:
        dict with keys: engine_results, final_output, total_tokens, duration_ms
    """
    start_time = time.time()
    chain_reg = get_chain_registry()
    engine_reg = get_engine_registry()

    chain = chain_reg.get(chain_key)
    if chain is None:
        # Safety net: if chain_key is actually an engine key, run as single engine
        engine_def = engine_reg.get(chain_key) or engine_reg.get_capability_definition(chain_key)
        if engine_def:
            logger.warning(
                f"Chain '{chain_key}' not found, but it's a valid engine — "
                f"falling back to run_single_engine()"
            )
            return run_single_engine(
                engine_key=chain_key,
                document_text=document_text,
                documents=documents,
                document_context=document_context,
                job_id=job_id,
                phase_number=phase_number,
                work_key=work_key,
                depth=depth,
                upstream_context=upstream_context,
                context_emphasis=context_emphasis,
                model_hint=model_hint,
                requires_full_documents=requires_full_documents,
                cancellation_check=cancellation_check,
                progress_callback=progress_callback,
            )
        raise ValueError(f"Chain not found: {chain_key}")

    logger.info(
        f"Starting chain '{chain_key}': {len(chain.engine_keys)} engines, "
        f"depth={depth}, work_key={work_key or 'N/A'}"
    )
    _events_hooks.chain_started(
        job_id, phase_number, chain_key, list(chain.engine_keys), work_key=work_key or None, depth=depth,
    )

    engine_results: dict[str, list[EngineCallResult]] = {}
    previous_engine_output: Optional[str] = None
    total_tokens = 0

    # Check for already-completed passes (resume support)
    completed_passes = get_completed_passes(job_id)
    if completed_passes:
        logger.info(
            f"RESUME: Found {len(completed_passes)} completed passes for job {job_id} "
            f"in phase {phase_number}"
        )

    for engine_idx, engine_key in enumerate(chain.engine_keys):
        if cancellation_check and cancellation_check():
            raise InterruptedError(f"Chain '{chain_key}' cancelled before engine {engine_key}")

        if progress_callback:
            progress_callback(
                f"Engine {engine_idx + 1}/{len(chain.engine_keys)}: {engine_key}"
            )

        # RESUME: Check if this engine's work is already complete
        engine_completed = any(
            p[1] == engine_key and p[0] == phase_number and p[3] == (work_key or "")
            for p in completed_passes
        )
        if engine_completed:
            # Load the last pass output for chain context threading
            saved_output = load_engine_last_pass_content(
                job_id, phase_number, engine_key, work_key=work_key,
            )
            if saved_output:
                previous_engine_output = saved_output
                logger.info(
                    f"RESUME: Skipping engine {engine_key} (already complete), "
                    f"loaded {len(saved_output):,} chars for context"
                )
                continue
            # If we can't load the saved output, fall through and re-run

        # Resolve per-engine overrides from the plan
        engine_depth = depth
        engine_focus_dims = None
        if engine_overrides and engine_key in engine_overrides:
            override = engine_overrides[engine_key]
            if isinstance(override, dict):
                engine_depth = override.get("depth", depth)
                engine_focus_dims = override.get("focus_dimensions")
            else:
                # It's an EngineExecutionSpec object
                engine_depth = getattr(override, "depth", depth)
                engine_focus_dims = getattr(override, "focus_dimensions", None)

        # Load capability engine definition
        cap_def = engine_reg.get_capability_definition(engine_key)
        if cap_def is None:
            logger.error(f"Engine not found: {engine_key}, skipping")
            continue

        # Run multi-pass execution for this engine
        with _events_context.scope(
            job_id=job_id, phase=_events_context.phase_key(phase_number),
            chain=chain_key, work_key=work_key or None,
        ):
            pass_results = _run_engine_passes(
                cap_def=cap_def,
                document_text=document_text,
                documents=documents,
                document_context=document_context,
                depth=engine_depth,
                focus_dimensions=engine_focus_dims,
                previous_engine_output=previous_engine_output,
                upstream_context=upstream_context,
                context_emphasis=context_emphasis,
                engine_label=chain.engine_keys[engine_idx - 1] if engine_idx > 0 else None,
                job_id=job_id,
                phase_number=phase_number,
                work_key=work_key,
                model_hint=model_hint,
                requires_full_documents=requires_full_documents,
                cancellation_check=cancellation_check,
            )

        engine_results[engine_key] = pass_results

        # The last pass output becomes context for the next engine
        if pass_results:
            previous_engine_output = pass_results[-1].content
            total_tokens += sum(r.input_tokens + r.output_tokens for r in pass_results)

    duration_ms = int((time.time() - start_time) * 1000)
    final_output = previous_engine_output or ""

    logger.info(
        f"Chain '{chain_key}' completed: {len(engine_results)} engines, "
        f"{total_tokens:,} tokens, {duration_ms:,}ms"
    )
    _events_hooks.chain_finished(
        job_id, phase_number, chain_key, list(engine_results.keys()),
        total_tokens=total_tokens, duration_ms=duration_ms, work_key=work_key or None,
    )

    return {
        "engine_results": engine_results,
        "final_output": final_output,
        "total_tokens": total_tokens,
        "duration_ms": duration_ms,
    }


def _run_engine_passes(
    cap_def: Any,
    document_text: str,
    depth: str,
    focus_dimensions: Optional[list[str]],
    previous_engine_output: Optional[str],
    upstream_context: str,
    context_emphasis: Optional[str],
    engine_label: Optional[str],
    job_id: str,
    phase_number: float,
    work_key: str,
    model_hint: Optional[str],
    requires_full_documents: bool,
    cancellation_check: Optional[Callable[[], bool]],
    documents: Optional[dict[str, str]] = None,
    document_context: str = "",
) -> list[EngineCallResult]:
    """Run all passes for a single engine using operationalization-driven prompts.

    Handles:
    - Multi-pass execution (discovery → architecture → integration etc.)
    - Inner-pass context threading (via consumes_from)
    - Incremental output persistence
    """
    # Process shape (study 2026-09-04): a depth key that names the engine's process runs
    # extract → verify → synthesize with per-step model routing instead of stance passes.
    _op = get_operationalization_registry().get(cap_def.engine_key)
    _mode = _op.mode_for_depth(depth) if _op is not None else None
    if _mode in ("oneshot", "oneshot_checked") and _op.process is not None:
        return _run_engine_process(
            cap_def=cap_def, spec=_op.process, document_text=document_text, depth=depth,
            documents=documents, document_context=document_context,
            previous_engine_output=previous_engine_output, upstream_context=upstream_context,
            context_emphasis=context_emphasis, engine_label=engine_label, job_id=job_id,
            phase_number=phase_number, work_key=work_key, model_hint=model_hint,
            requires_full_documents=requires_full_documents, cancellation_check=cancellation_check,
            mode=_mode,
        )
    _spec = _op.process_for_depth(depth) if _op is not None else None
    if _spec is not None:
        return _run_engine_process(
            cap_def=cap_def, spec=_spec, document_text=document_text, depth=depth,
            documents=documents, document_context=document_context,
            previous_engine_output=previous_engine_output, upstream_context=upstream_context,
            context_emphasis=context_emphasis, engine_label=engine_label, job_id=job_id,
            phase_number=phase_number, work_key=work_key, model_hint=model_hint,
            requires_full_documents=requires_full_documents, cancellation_check=cancellation_check,
        )

    # Get pass prompts from the capability composer
    # This checks the operationalization registry first, then falls back to inline passes
    pass_prompts = compose_all_pass_prompts(
        cap_def=cap_def,
        depth=depth,
        use_operationalizations=True,
    )

    if not pass_prompts:
        # No multi-pass definition — run a single whole-engine prompt
        logger.info(
            f"No pass definitions for {cap_def.engine_key} at depth={depth}, "
            f"running single whole-engine call"
        )
        return _run_single_engine_call(
            cap_def=cap_def,
            document_text=document_text,
            depth=depth,
            focus_dimensions=focus_dimensions,
            previous_engine_output=previous_engine_output,
            upstream_context=upstream_context,
            context_emphasis=context_emphasis,
            engine_label=engine_label,
            job_id=job_id,
            phase_number=phase_number,
            work_key=work_key,
            model_hint=model_hint,
            requires_full_documents=requires_full_documents,
            cancellation_check=cancellation_check,
        )

    # Multi-pass execution
    results: list[EngineCallResult] = []
    prior_pass_outputs: dict[int, str] = {}
    pass_stances: dict[int, str] = {}

    # Check for already-completed passes (resume support)
    completed_passes = get_completed_passes(job_id)

    for pass_prompt in pass_prompts:
        if cancellation_check and cancellation_check():
            raise InterruptedError(
                f"Cancelled during {cap_def.engine_key} pass {pass_prompt.pass_number}"
            )

        # RESUME: Check if this specific pass is already complete
        pass_key = (phase_number, cap_def.engine_key, pass_prompt.pass_number, work_key or "")
        if pass_key in completed_passes:
            saved_content = load_pass_content(
                job_id, phase_number, cap_def.engine_key,
                pass_prompt.pass_number, work_key=work_key,
            )
            if saved_content:
                prior_pass_outputs[pass_prompt.pass_number] = saved_content
                pass_stances[pass_prompt.pass_number] = pass_prompt.stance_key
                results.append(EngineCallResult(
                    engine_key=cap_def.engine_key,
                    pass_number=pass_prompt.pass_number,
                    stance_key=pass_prompt.stance_key,
                    content=saved_content,
                    model_used="(resumed)",
                    input_tokens=0,
                    output_tokens=0,
                    thinking_tokens=0,
                    duration_ms=0,
                    retries=0,
                ))
                logger.info(
                    f"  RESUME: Pass {pass_prompt.pass_number}/{len(pass_prompts)} "
                    f"({pass_prompt.pass_label}): loaded {len(saved_content):,} chars from DB"
                )
                continue

        # Build inner-pass context from consumed passes
        inner_context = assemble_inner_pass_context(
            prior_pass_outputs=prior_pass_outputs,
            consumes_from=pass_prompt.consumes_from,
            pass_stances=pass_stances,
        )

        # Build chain context from previous engine
        chain_context = ""
        if previous_engine_output:
            chain_context = assemble_chain_context(
                previous_engine_output=previous_engine_output,
                engine_label=engine_label or "prior engine",
            )

        # Compose the full prompt with actual shared context
        # Re-compose with the real shared context now available
        shared_context_parts = []
        if upstream_context:
            shared_context_parts.append(upstream_context)
        if context_emphasis:
            shared_context_parts.append(
                f"## Analytical Emphasis\n\n**{context_emphasis}**"
            )
        if chain_context:
            shared_context_parts.append(chain_context)
        if inner_context:
            shared_context_parts.append(inner_context)

        full_shared_context = "\n\n---\n\n".join(shared_context_parts) if shared_context_parts else None

        # Get the PassDefinition to re-compose with shared context
        from src.engines.schemas_v2 import PassDefinition
        pass_def = PassDefinition(
            pass_number=pass_prompt.pass_number,
            label=pass_prompt.pass_label,
            stance=pass_prompt.stance_key,
            description=getattr(pass_prompt, "description", "") or "",  # the operationalization's own words, once lost here (study 2026-09-04)
            focus_dimensions=pass_prompt.focus_dimensions,
            consumes_from=pass_prompt.consumes_from,
        )

        recomposed = compose_pass_prompt(
            cap_def=cap_def,
            pass_def=pass_def,
            depth=depth,
            shared_context=full_shared_context,
            is_final=(pass_prompt.pass_number == max(pp.pass_number for pp in pass_prompts)),
        )

        system_prompt = recomposed.prompt

        # Build user message with document text
        user_message = document_text

        label = (
            f"Phase {phase_number} | {cap_def.engine_key} | "
            f"Pass {pass_prompt.pass_number} ({pass_prompt.pass_label})"
        )
        if work_key:
            label += f" | {work_key}"

        # Execute the LLM call (auto-chunks if user_message exceeds threshold)
        with _events_context.scope(
            job_id=job_id, phase=_events_context.phase_key(phase_number),
            engine=cap_def.engine_key,
            pass_name=f"Pass {pass_prompt.pass_number}: {pass_prompt.pass_label}",
            stance=pass_prompt.stance_key or None, work_key=work_key or None,
        ):
            result = run_engine_call_auto(
                system_prompt=system_prompt,
                user_message=user_message,
                phase_number=phase_number,
                model_hint=model_hint,
                depth=depth,
                requires_full_documents=requires_full_documents,
                cancellation_check=cancellation_check,
                label=label,
            )

        # Build EngineCallResult
        engine_result = EngineCallResult(
            engine_key=cap_def.engine_key,
            pass_number=pass_prompt.pass_number,
            stance_key=pass_prompt.stance_key,
            content=result["content"],
            model_used=result["model_used"],
            input_tokens=result["input_tokens"],
            output_tokens=result["output_tokens"],
            thinking_tokens=result["thinking_tokens"],
            duration_ms=result["duration_ms"],
            retries=result["retries"],
        )
        results.append(engine_result)

        # Track for inner-pass context threading
        prior_pass_outputs[pass_prompt.pass_number] = result["content"]
        pass_stances[pass_prompt.pass_number] = pass_prompt.stance_key

        # Persist incrementally
        output_metadata = build_aoi_output_metadata(
            job_id=job_id,
            phase_number=phase_number,
            engine_key=cap_def.engine_key,
            content=result["content"],
        )
        output_id = save_output(
            job_id=job_id,
            phase_number=phase_number,
            engine_key=cap_def.engine_key,
            pass_number=pass_prompt.pass_number,
            content=result["content"],
            work_key=work_key,
            stance_key=pass_prompt.stance_key,
            role="extraction",
            model_used=result["model_used"],
            input_tokens=result["input_tokens"],
            output_tokens=result["output_tokens"],
            parent_id=None,  # TODO: lineage tracking
            metadata=output_metadata,
        )
        try:
            from src.analysis_products.store import record_aoi_artifact_from_metadata

            record_aoi_artifact_from_metadata(
                job_id=job_id,
                phase_number=phase_number,
                engine_key=cap_def.engine_key,
                source_output_id=output_id,
                output_metadata=output_metadata,
            )
        except Exception as artifact_error:
            logger.warning(
                "AOI artifact dual-write failed for job %s phase %s engine %s: %s",
                job_id,
                phase_number,
                cap_def.engine_key,
                artifact_error,
            )

        # Update job-level token counters INCREMENTALLY after each LLM call.
        # Previously only updated after full phase completion — counter stayed
        # at 0 for 30+ min during multi-engine phases.
        update_job_tokens(
            job_id,
            llm_calls=1,
            input_tokens=result["input_tokens"],
            output_tokens=result["output_tokens"],
        )

        logger.info(
            f"  Pass {pass_prompt.pass_number}/{len(pass_prompts)} "
            f"({pass_prompt.pass_label}): "
            f"{result['input_tokens']}+{result['output_tokens']} tokens, "
            f"{result['duration_ms']}ms"
        )

    return results


def _run_engine_process(
    cap_def: Any,
    spec: Any,
    document_text: str,
    depth: str,
    previous_engine_output: Optional[str],
    upstream_context: str,
    context_emphasis: Optional[str],
    engine_label: Optional[str],
    job_id: str,
    phase_number: float,
    work_key: str,
    model_hint: Optional[str],
    requires_full_documents: bool,
    cancellation_check: Optional[Callable[[], bool]],
    mode: str = "dvs",
    documents: Optional[dict[str, str]] = None,
    document_context: str = "",
) -> list[EngineCallResult]:
    """Run the engine's process and persist every call as a pass output. `mode` is `dvs` (the chain),
    `oneshot` (one call) or `oneshot_checked` (one call, then the critic, rulings applied by code).

    The final synthesis is the last pass (what the desks read); the extraction and verification calls are
    saved before it as receipts, roles `extraction` and `verification`.
    """
    from src.executor.process_runner import run_oneshot_checked, run_process

    # Preserve source boundaries before the process decides whether to run corpus dimensions.
    # The text form remains available to legacy stance engines and their auto-chunking path.
    sources = dict(documents) if documents is not None else {work_key or "document": document_text}
    empty_keys = [key for key, text in sources.items() if not text.strip()]
    if not sources or empty_keys:
        detail = ", ".join(empty_keys) if empty_keys else "no sources selected"
        raise ValueError(f"Process execution requires non-empty selected source documents: {detail}")
    shared_parts = []
    if document_context:
        shared_parts.append(document_context)
    if upstream_context:
        shared_parts.append(upstream_context)
    if context_emphasis:
        shared_parts.append(f"## Analytical Emphasis\n\n**{context_emphasis}**")
    if previous_engine_output:
        shared_parts.append(assemble_chain_context(previous_engine_output=previous_engine_output, engine_label=engine_label or "prior engine"))
    upstream = "\n\n---\n\n".join(shared_parts)

    results: list[EngineCallResult] = []
    counter = {"n": 0}

    def _persist(sc):
        counter["n"] += 1
        role = {"extract": "extraction", "verify": "verification", "synthesize": "synthesis"}.get(sc.kind, sc.kind)
        if sc.step_key == "check": role = "verification"
        save_output(
            job_id=job_id, phase_number=phase_number, engine_key=cap_def.engine_key, pass_number=counter["n"],
            content=sc.content, work_key=work_key, stance_key=f"{sc.step_key}:{sc.dimension_key}" if sc.dimension_key else sc.step_key,
            role=role, model_used=sc.model_used, input_tokens=sc.input_tokens, output_tokens=sc.output_tokens,
            metadata={"process": spec.key, "step": sc.step_key, "kind": sc.kind, "dimension": sc.dimension_key,
                      "doc": sc.doc_key, "wall": sc.wall, "cost_usd": sc.cost_usd, "model_requested": sc.model_requested},
        )
        update_job_tokens(job_id, llm_calls=1, input_tokens=sc.input_tokens, output_tokens=sc.output_tokens)
        results.append(EngineCallResult(
            engine_key=cap_def.engine_key, pass_number=counter["n"], stance_key=sc.step_key, content=sc.content,
            model_used=sc.model_used, input_tokens=sc.input_tokens, output_tokens=sc.output_tokens,
            thinking_tokens=0, duration_ms=sc.duration_ms, retries=sc.retries,
        ))
        logger.info(f"  {cap_def.engine_key} {sc.step_key}{(' ' + sc.dimension_key) if sc.dimension_key else ''}: "
                    f"{sc.model_used} {sc.input_tokens}+{sc.output_tokens} tokens, {sc.duration_ms}ms, wall={sc.wall.get('anchor_rate')}")

    with _events_context.scope(job_id=job_id, phase=_events_context.phase_key(phase_number), engine=cap_def.engine_key,
                               pass_name=f"process {spec.key}", stance=None, work_key=work_key or None):
        if mode in ("oneshot", "oneshot_checked"):
            run = run_oneshot_checked(
                cap_def, spec, sources, depth=depth, check=(mode == "oneshot_checked"),
                model_hint=model_hint, cancellation_check=cancellation_check, on_call=_persist, upstream_context=upstream,
            )
        else:
            run = run_process(
                cap_def, spec, sources, depth=depth, model_hint=model_hint,
                cancellation_check=cancellation_check, on_call=_persist, upstream_context=upstream,
            )
        # The applied ledger is the engine's product: persisted as the last pass so the desks read it
        if (mode == "oneshot_checked" or spec.scoped_outcomes) and results and run.final_content != results[-1].content:
            stance = "checked" if mode == "oneshot_checked" else "scope_assessed"
            counter["n"] += 1
            save_output(job_id=job_id, phase_number=phase_number, engine_key=cap_def.engine_key, pass_number=counter["n"],
                        content=run.final_content, work_key=work_key, stance_key=stance, role="synthesis",
                        model_used=run.final_model, metadata={"process": spec.key, "mode": mode, "wall": run.final_wall})
            results.append(EngineCallResult(engine_key=cap_def.engine_key, pass_number=counter["n"], stance_key=stance,
                                            content=run.final_content, model_used=run.final_model))
    logger.info(f"{cap_def.engine_key} {mode} ({spec.key}): {len(run.calls)} calls, ${run.cost_usd}, {run.seconds:.0f}s, final anchor rate {run.final_wall.get('anchor_rate')}")
    return results


def _run_single_engine_call(
    cap_def: Any,
    document_text: str,
    depth: str,
    focus_dimensions: Optional[list[str]],
    previous_engine_output: Optional[str],
    upstream_context: str,
    context_emphasis: Optional[str],
    engine_label: Optional[str],
    job_id: str,
    phase_number: float,
    work_key: str,
    model_hint: Optional[str],
    requires_full_documents: bool,
    cancellation_check: Optional[Callable[[], bool]],
) -> list[EngineCallResult]:
    """Fallback: run a single whole-engine call (no multi-pass)."""
    from src.stages.capability_composer import compose_capability_prompt

    # Build shared context
    shared_context_parts = []
    if upstream_context:
        shared_context_parts.append(upstream_context)
    if context_emphasis:
        shared_context_parts.append(
            f"## Analytical Emphasis\n\n**{context_emphasis}**"
        )
    if previous_engine_output:
        chain_ctx = assemble_chain_context(
            previous_engine_output=previous_engine_output,
            engine_label=engine_label or "prior engine",
        )
        shared_context_parts.append(chain_ctx)

    full_shared = "\n\n---\n\n".join(shared_context_parts) if shared_context_parts else None

    cap_prompt = compose_capability_prompt(
        cap_def=cap_def,
        depth=depth,
        shared_context=full_shared,
        focus_dimensions=focus_dimensions,
    )

    label = f"Phase {phase_number} | {cap_def.engine_key}"
    if work_key:
        label += f" | {work_key}"

    with _events_context.scope(
        job_id=job_id, phase=_events_context.phase_key(phase_number),
        engine=cap_def.engine_key, pass_name="Pass 1: whole-engine", stance=None,
        work_key=work_key or None,
    ):
        result = run_engine_call_auto(
            system_prompt=cap_prompt.prompt,
            user_message=document_text,
            phase_number=phase_number,
            model_hint=model_hint,
            depth=depth,
            requires_full_documents=requires_full_documents,
            cancellation_check=cancellation_check,
            label=label,
        )

    engine_result = EngineCallResult(
        engine_key=cap_def.engine_key,
        pass_number=1,
        stance_key="",
        content=result["content"],
        model_used=result["model_used"],
        input_tokens=result["input_tokens"],
        output_tokens=result["output_tokens"],
        thinking_tokens=result["thinking_tokens"],
        duration_ms=result["duration_ms"],
        retries=result["retries"],
    )

    # Persist
    output_metadata = build_aoi_output_metadata(
        job_id=job_id,
        phase_number=phase_number,
        engine_key=cap_def.engine_key,
        content=result["content"],
    )
    output_id = save_output(
        job_id=job_id,
        phase_number=phase_number,
        engine_key=cap_def.engine_key,
        pass_number=1,
        content=result["content"],
        work_key=work_key,
        role="extraction",
        model_used=result["model_used"],
        input_tokens=result["input_tokens"],
        output_tokens=result["output_tokens"],
        metadata=output_metadata,
    )
    try:
        from src.analysis_products.store import record_aoi_artifact_from_metadata

        record_aoi_artifact_from_metadata(
            job_id=job_id,
            phase_number=phase_number,
            engine_key=cap_def.engine_key,
            source_output_id=output_id,
            output_metadata=output_metadata,
        )
    except Exception as artifact_error:
        logger.warning(
            "AOI artifact dual-write failed for job %s phase %s engine %s: %s",
            job_id,
            phase_number,
            cap_def.engine_key,
            artifact_error,
        )

    # Incremental token counter update
    update_job_tokens(
        job_id,
        llm_calls=1,
        input_tokens=result["input_tokens"],
        output_tokens=result["output_tokens"],
    )

    return [engine_result]


def run_single_engine(
    engine_key: str,
    document_text: str,
    *,
    job_id: str,
    phase_number: float,
    work_key: str = "",
    depth: str = "standard",
    focus_dimensions: Optional[list[str]] = None,
    upstream_context: str = "",
    context_emphasis: Optional[str] = None,
    model_hint: Optional[str] = None,
    requires_full_documents: bool = False,
    cancellation_check: Optional[Callable[[], bool]] = None,
    progress_callback: Optional[Callable[[str], None]] = None,
    documents: Optional[dict[str, str]] = None,
    document_context: str = "",
) -> dict:
    """Execute a single engine (not part of a chain).

    Used for phases backed by a single engine_key instead of a chain_key.
    Handles multi-pass via operationalizations just like chain_runner does.
    `documents` and `document_context` have the same source/context contract as run_chain.

    Returns:
        dict with keys: engine_results, final_output, total_tokens, duration_ms
    """
    start_time = time.time()
    engine_reg = get_engine_registry()

    cap_def = engine_reg.get_capability_definition(engine_key)
    if cap_def is None:
        raise ValueError(f"Engine not found: {engine_key}")

    if progress_callback:
        progress_callback(f"Engine: {engine_key}")

    with _events_context.scope(
        job_id=job_id, phase=_events_context.phase_key(phase_number),
        chain=None, work_key=work_key or None,
    ):
        pass_results = _run_engine_passes(
            cap_def=cap_def,
            document_text=document_text,
            documents=documents,
            document_context=document_context,
            depth=depth,
            focus_dimensions=focus_dimensions,
            previous_engine_output=None,
            upstream_context=upstream_context,
            context_emphasis=context_emphasis,
            engine_label=None,
            job_id=job_id,
            phase_number=phase_number,
            work_key=work_key,
            model_hint=model_hint,
            requires_full_documents=requires_full_documents,
            cancellation_check=cancellation_check,
        )

    total_tokens = sum(r.input_tokens + r.output_tokens for r in pass_results)
    final_output = pass_results[-1].content if pass_results else ""
    duration_ms = int((time.time() - start_time) * 1000)

    return {
        "engine_results": {engine_key: pass_results},
        "final_output": final_output,
        "total_tokens": total_tokens,
        "duration_ms": duration_ms,
    }
