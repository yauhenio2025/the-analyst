"""The process runner (study 2026-09-04): extract → verify → synthesize with per-step model routing.

Runs an engine's ProcessSpec over one document or a corpus:

  extract     one call per dimension (and per document), in parallel, on the cheap tier; ledger only;
              wall: anchors verbatim, one re-anchor round, then failed rows dropped
  verify      one call per document on the mid tier (plus one across the corpus when corpus dimensions
              exist); every row ruled confirmed / weakened / rejected, misses added; wall on the anchors
  synthesize  one call on the strong tier from the verified ledger; wall: cited ids exist, anchors verified

Routing per step: explicit overrides (the study) > env PROCESS_ROUTING_<TIER> > the step's own `model`
> the plan's model_hint (strong tier only) > the spec's routing table > the house model. Every call goes
through `run_engine_call_auto`, so refusals fall back and events are recorded as for any engine call.
Judgment stays with the models; this file holds shape, sequence, arithmetic and persistence hooks.
"""
from __future__ import annotations

import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from src.events.pricing import estimate_cost
from src.executor.context_broker import split_ledger
from src.executor.engine_runner import FALLBACK_MODEL, run_engine_call_auto
from src.executor.ledger_walls import (
    LedgerRow, SourceIndex, WallReport, check_citations, parse_rows, reanchor_request, render_rows, verify_rows,
)
from src.operationalizations.schemas import ProcessDimension, ProcessSpec, ProcessStep
from src.stages.process_composer import (
    LEDGER_HEADING, ProcessPrompt, compose_extract_prompt, compose_synthesize_prompt, compose_verify_prompt,
)

logger = logging.getLogger(__name__)

TIERS = ("cheap", "mid", "strong")
DEFAULT_ROUTING = {"cheap": "openrouter/openai/gpt-5.6-luna", "mid": "openrouter/deepseek/deepseek-v4-pro", "strong": FALLBACK_MODEL}
EXTRACT_PARALLELISM = int(os.environ.get("PROCESS_EXTRACT_PARALLELISM", "5"))

CallFn = Callable[..., dict]  # (system_prompt, user_message, model_hint, label, ...) -> run_engine_call_auto result


def resolve_step_model(
    step: ProcessStep, spec: ProcessSpec, *, tier_overrides: Optional[dict[str, str]] = None, model_hint: Optional[str] = None,
) -> str:
    """The model a step runs on. See the module docstring for the precedence."""
    tier = step.model_tier
    if tier_overrides and tier_overrides.get(tier):
        return tier_overrides[tier]
    env = os.environ.get(f"PROCESS_ROUTING_{tier.upper()}")
    if env:
        return env
    if step.model:
        return step.model
    if model_hint and tier == "strong" and (model_hint.startswith(("claude-", "gemini-", "openrouter/"))):
        return model_hint
    if spec.routing.get(tier):
        return spec.routing[tier]
    return DEFAULT_ROUTING[tier]


@dataclass
class StepCall:
    """One model call inside a step, with its receipt."""

    step_key: str
    kind: str
    dimension_key: str = ""
    doc_key: str = ""
    model_requested: str = ""
    model_used: str = ""
    content: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    duration_ms: int = 0
    cost_usd: float = 0.0
    retries: int = 0
    wall: dict = field(default_factory=dict)
    reanchored: int = 0
    dropped_ids: list[str] = field(default_factory=list)
    label: str = ""
    system_prompt: str = ""

    def as_receipt(self) -> dict:
        return {
            "step": self.step_key, "kind": self.kind, "dimension": self.dimension_key, "doc": self.doc_key,
            "model_requested": self.model_requested, "model_used": self.model_used,
            "input_tokens": self.input_tokens, "output_tokens": self.output_tokens, "duration_ms": self.duration_ms,
            "cost_usd": round(self.cost_usd, 4), "retries": self.retries, "wall": self.wall,
            "reanchored": self.reanchored, "dropped_ids": self.dropped_ids, "chars": len(self.content),
        }


@dataclass
class ProcessRunResult:
    engine_key: str
    process_key: str
    calls: list[StepCall] = field(default_factory=list)
    final_content: str = ""
    final_model: str = ""
    final_wall: dict = field(default_factory=dict)
    seconds: float = 0.0

    @property
    def cost_usd(self) -> float:
        return round(sum(c.cost_usd for c in self.calls), 4)

    @property
    def input_tokens(self) -> int:
        return sum(c.input_tokens for c in self.calls)

    @property
    def output_tokens(self) -> int:
        return sum(c.output_tokens for c in self.calls)

    def calls_for(self, step_key: str) -> list[StepCall]:
        return [c for c in self.calls if c.step_key == step_key]

    def receipts(self) -> dict:
        return {
            "engine": self.engine_key, "process": self.process_key, "cost_usd": self.cost_usd,
            "input_tokens": self.input_tokens, "output_tokens": self.output_tokens, "seconds": round(self.seconds, 1),
            "final_model": self.final_model, "final_wall": self.final_wall, "calls": [c.as_receipt() for c in self.calls],
        }


def _default_call(system_prompt: str, user_message: str, *, model_hint: str, label: str, depth: str = "standard",
                  requires_full_documents: bool = False, cancellation_check=None) -> dict:
    return run_engine_call_auto(
        system_prompt=system_prompt, user_message=user_message, phase_number=1.0, model_hint=model_hint,
        depth=depth, requires_full_documents=requires_full_documents, cancellation_check=cancellation_check, label=label,
    )


def _invoke(call_fn: CallFn, prompt: ProcessPrompt, model: str, *, depth: str, big: bool, cancellation_check) -> StepCall:
    t0 = time.time()
    res = call_fn(prompt.system, prompt.user, model_hint=model, label=prompt.label, depth=depth,
                  requires_full_documents=big, cancellation_check=cancellation_check)
    used = res.get("model_used") or model
    sc = StepCall(
        step_key=prompt.step_key, kind=prompt.kind, dimension_key=prompt.dimension_key, doc_key=prompt.doc_key,
        model_requested=model, model_used=used, content=res.get("content") or "",
        input_tokens=int(res.get("input_tokens") or 0), output_tokens=int(res.get("output_tokens") or 0),
        duration_ms=int(res.get("duration_ms") or (time.time() - t0) * 1000), retries=int(res.get("retries") or 0),
        label=prompt.label, system_prompt=prompt.system,
    )
    sc.cost_usd = estimate_cost(used, sc.input_tokens, sc.output_tokens) or 0.0
    return sc


def _ledger_text(content: str) -> str:
    _, ledger = split_ledger(content)
    return ledger or content


def _wall_extraction(sc: StepCall, prompt: ProcessPrompt, index: SourceIndex, call_fn: CallFn, model: str, *,
                     depth: str, big: bool, cancellation_check, reanchor: bool = True) -> list[LedgerRow]:
    """Verify an extraction's anchors; one re-anchor round for the failures; drop what still fails."""
    rows = parse_rows(_ledger_text(sc.content))
    rep = verify_rows(rows, index)
    failed = [r for r in rows if not r.anchor_verified]
    if failed and reanchor:
        req = ProcessPrompt(
            engine_key=prompt.engine_key, step_key=prompt.step_key, kind=prompt.kind, dimension_key=prompt.dimension_key,
            doc_key=prompt.doc_key, system=prompt.system,
            user=prompt.user + "\n\n=====\n\n" + reanchor_request(failed), model_tier=prompt.model_tier,
            label=prompt.label + " (re-anchor)", id_prefix=prompt.id_prefix,
        )
        try:
            again = _invoke(call_fn, req, model, depth=depth, big=big, cancellation_check=cancellation_check)
            sc.input_tokens += again.input_tokens; sc.output_tokens += again.output_tokens
            sc.duration_ms += again.duration_ms; sc.cost_usd += again.cost_usd
            fixed = {r.id: r for r in parse_rows(_ledger_text(again.content))}
            verify_rows(fixed.values(), index)
            for r in failed:
                f = fixed.get(r.id)
                if f and f.anchor_verified:
                    r.anchor, r.anchor_verified, r.anchor_trimmed, r.anchor_doc = f.anchor, True, f.anchor_trimmed, f.anchor_doc
                    r.text = f.text
                    sc.reanchored += 1
        except Exception as exc:  # noqa: BLE001 — the re-anchor round never blocks the run
            logger.warning(f"[{prompt.label}] re-anchor round failed: {exc}")
    kept = [r for r in rows if r.anchor_verified]
    sc.dropped_ids = [r.id for r in rows if not r.anchor_verified]
    rep2 = verify_rows(kept, index)
    sc.wall = {**rep.as_dict(), "after_reanchor": rep2.as_dict()}
    return kept


def run_process(
    cap_def: Any,
    spec: ProcessSpec,
    documents: dict[str, str],
    *,
    depth: str = "standard",
    tier_overrides: Optional[dict[str, str]] = None,
    model_hint: Optional[str] = None,
    call_fn: Optional[CallFn] = None,
    cancellation_check: Optional[Callable[[], bool]] = None,
    on_call: Optional[Callable[[StepCall], None]] = None,
    parallelism: int = EXTRACT_PARALLELISM,
    reanchor: bool = True,
    surface_only_load_bearing: bool = False,
    upstream_context: str = "",
) -> ProcessRunResult:
    """Run the process over `documents` ({doc_key: text}). Returns every call's receipt and the final reading."""
    call_fn = call_fn or _default_call
    t0 = time.time()
    result = ProcessRunResult(engine_key=cap_def.engine_key, process_key=spec.key)
    index = SourceIndex(documents)
    total_chars = sum(len(v) for v in documents.values())
    big = total_chars > 600_000
    corpus = len(documents) > 1
    doc_dims = [d for d in spec.dimensions if d.scope == "document" and (d.load_bearing or not surface_only_load_bearing)]
    corpus_dims = [d for d in spec.dimensions if d.scope == "corpus"] if corpus else []

    def _cancelled():
        return bool(cancellation_check and cancellation_check())

    # Ledgers by step key: {step_key: {doc_key: [rows]}}; "" is the corpus-level doc key
    ledgers: dict[str, dict[str, list[LedgerRow]]] = {}
    rejected_by_doc: dict[str, list[LedgerRow]] = {}

    def _record(sc: StepCall) -> None:
        result.calls.append(sc)
        if on_call:
            try:
                on_call(sc)
            except Exception as exc:  # noqa: BLE001
                logger.warning(f"on_call hook failed: {exc}")

    for step in spec.steps:
        if _cancelled():
            raise InterruptedError(f"process {spec.key} cancelled before step {step.key}")
        model = resolve_step_model(step, spec, tier_overrides=tier_overrides, model_hint=model_hint)

        if step.kind == "extract":
            jobs: list[tuple[ProcessPrompt, str]] = []
            doc_keys = list(documents.keys())
            for dim in doc_dims:
                if step.parallel_over in ("dimension_x_document", "document") or corpus:
                    for dk in doc_keys:
                        jobs.append((compose_extract_prompt(cap_def, spec, step, dim, documents, doc_key=dk), dk))
                else:
                    jobs.append((compose_extract_prompt(cap_def, spec, step, dim, documents), doc_keys[0] if len(doc_keys) == 1 else ""))

            def _do(job):
                prompt, dk = job
                sc = _invoke(call_fn, prompt, model, depth=depth, big=big, cancellation_check=cancellation_check)
                kept = _wall_extraction(sc, prompt, index, call_fn, model, depth=depth, big=big,
                                        cancellation_check=cancellation_check, reanchor=reanchor)
                for r in kept:
                    r.doc = r.doc or dk
                return sc, dk, kept

            step_ledgers: dict[str, list[LedgerRow]] = {}
            workers = max(1, min(parallelism, len(jobs))) if step.parallel_over != "none" else 1
            with ThreadPoolExecutor(max_workers=workers) as pool:
                for sc, dk, kept in pool.map(_do, jobs):
                    _record(sc)
                    step_ledgers.setdefault(dk, []).extend(kept)
            # corpus dimensions read the per-document ledgers, not the sources
            if corpus_dims:
                merged = "\n\n".join(
                    f"## Document [{dk}]\n" + render_rows(rows) for dk, rows in step_ledgers.items()
                )
                cjobs = [compose_extract_prompt(cap_def, spec, step, dim, documents, prior_ledgers=merged) for dim in corpus_dims]
                with ThreadPoolExecutor(max_workers=max(1, min(parallelism, len(cjobs)))) as pool:
                    for sc in pool.map(lambda p: _invoke(call_fn, p, model, depth=depth, big=big, cancellation_check=cancellation_check), cjobs):
                        rows = parse_rows(_ledger_text(sc.content))
                        rep = verify_rows(rows, index)
                        kept = [r for r in rows if r.anchor_verified]
                        sc.dropped_ids = [r.id for r in rows if not r.anchor_verified]
                        sc.wall = rep.as_dict()
                        _record(sc)
                        step_ledgers.setdefault("", []).extend(kept)
            ledgers[step.key] = step_ledgers

        elif step.kind == "verify":
            consumed = step.consumes or [s.key for s in spec.steps if s.kind == "extract"]
            per_doc: dict[str, list[LedgerRow]] = {}
            for ck in consumed:
                for dk, rows in ledgers.get(ck, {}).items():
                    per_doc.setdefault(dk, []).extend(rows)
            step_ledgers = {}
            targets = [dk for dk in per_doc.keys() if dk != ""] or [""]
            for dk in targets:
                if _cancelled():
                    raise InterruptedError(f"process {spec.key} cancelled during {step.key}")
                rows = per_doc.get(dk, [])
                if not rows:
                    continue
                text = render_rows(rows)
                prompt = compose_verify_prompt(cap_def, spec, step, documents, text, doc_key=dk if corpus else "")
                sc = _invoke(call_fn, prompt, model, depth=depth, big=big, cancellation_check=cancellation_check)
                vrows = parse_rows(_ledger_text(sc.content))
                rep = verify_rows(vrows, index)
                known = {r.id for r in rows}
                # a row the critic did not mention is carried forward as confirmed (the critic's omission is not a rejection)
                mentioned = {r.id for r in vrows}
                carried = [r for r in rows if r.id not in mentioned]
                for r in carried:
                    r.status = r.status or "confirmed"
                kept = [r for r in vrows if r.anchor_verified and r.status in ("confirmed", "weakened", "added", "")] + carried
                rejected = [r for r in vrows if r.status == "rejected" or (not r.anchor_verified and r.id in known)]
                sc.dropped_ids = [r.id for r in vrows if not r.anchor_verified]
                sc.wall = {**rep.as_dict(), "carried_forward": len(carried), "rejected": len(rejected), "added": sum(1 for r in vrows if r.status == "added")}
                _record(sc)
                step_ledgers[dk] = kept
                rejected_by_doc[dk] = rejected
            if corpus and per_doc.get(""):
                # cross-document rows: one verify with all sources in context
                text = render_rows(per_doc[""])
                prompt = compose_verify_prompt(cap_def, spec, step, documents, text)
                sc = _invoke(call_fn, prompt, model, depth=depth, big=big, cancellation_check=cancellation_check)
                vrows = parse_rows(_ledger_text(sc.content))
                rep = verify_rows(vrows, index)
                sc.wall = rep.as_dict(); _record(sc)
                step_ledgers[""] = [r for r in vrows if r.anchor_verified and r.status != "rejected"]
                rejected_by_doc[""] = [r for r in vrows if r.status == "rejected"]
            ledgers[step.key] = step_ledgers

        elif step.kind == "synthesize":
            consumed = step.consumes or [s.key for s in spec.steps if s.kind in ("verify", "extract")][-1:]
            all_rows: list[LedgerRow] = []
            for ck in consumed:
                for dk, rows in ledgers.get(ck, {}).items():
                    all_rows.extend(rows)
            if not all_rows:
                raise RuntimeError(f"process {spec.key}: nothing survived the walls before {step.key}; no rows to synthesize from")
            verified_text = render_rows(all_rows)
            rejected_rows = [r for rows in rejected_by_doc.values() for r in rows]
            rejected_text = "\n".join(r.render() for r in rejected_rows) if rejected_rows else ""
            prompt = compose_synthesize_prompt(cap_def, spec, step, documents, verified_text, rejected_text=rejected_text)
            if upstream_context:
                prompt.user = f"{upstream_context}\n\n=====\n\n{prompt.user}"
            sc = _invoke(call_fn, prompt, model, depth=depth, big=big, cancellation_check=cancellation_check)
            prose, ledger = split_ledger(sc.content)
            frows = parse_rows(ledger)
            rep = verify_rows(frows, index)
            earlier = {r.id for r in all_rows} | {r.id for r in rejected_rows}
            missing = check_citations(prose, {r.id for r in frows}, also_ok=earlier)
            rep.missing_cited = missing
            sc.wall = {**rep.as_dict(), "has_ledger": bool(ledger), "prose_chars": len(prose)}
            _record(sc)
            result.final_content = sc.content
            result.final_model = sc.model_used
            result.final_wall = sc.wall
            ledgers[step.key] = {"": frows}

    result.seconds = time.time() - t0
    if not result.final_content and result.calls:
        result.final_content = result.calls[-1].content
        result.final_model = result.calls[-1].model_used
    return result


def preview_prompts(cap_def: Any, spec: ProcessSpec, documents: dict[str, str]) -> list[ProcessPrompt]:
    """Every extraction prompt plus the verify and synthesize prompts with placeholder ledgers (no calls)."""
    out: list[ProcessPrompt] = []
    for step in spec.steps:
        if step.kind == "extract":
            for dim in spec.dimensions:
                if dim.scope == "document":
                    out.append(compose_extract_prompt(cap_def, spec, step, dim, documents, doc_key=next(iter(documents)) if len(documents) > 1 else ""))
                elif len(documents) > 1:
                    out.append(compose_extract_prompt(cap_def, spec, step, dim, documents, prior_ledgers="(per-document ledgers)"))
        elif step.kind == "verify":
            out.append(compose_verify_prompt(cap_def, spec, step, documents, f"{LEDGER_HEADING}\n- [D1.F1] (extraction rows)"))
        elif step.kind == "synthesize":
            out.append(compose_synthesize_prompt(cap_def, spec, step, documents, f"{LEDGER_HEADING}\n- [D1.F1] (verified rows)"))
    return out
