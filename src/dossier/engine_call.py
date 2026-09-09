"""A light engine call (2026-09-06): one engine over a few supplied sources, in the request, without a dossier job.

For the one-cent methods a consumer's page runs on a click — the Stacks' "explain this citation" is the first —
a dossier job (desks, plan, brief, receipts on disk) is the wrong weight. This runs the engine's one-call mode
(`surface`: the reading on the strong tier; `standard`: the reading and the critic on the mid tier, rulings applied
by code) through the same process runner and the same walls as a job, returns the rows with the wall's verdicts and
the engine's shaped JSON when a renderer exists, and refuses before spending when the estimate passes the caller's
cap. Nothing is stored here: the caller keeps what it needs; the receipts travel in the answer.
"""
from __future__ import annotations

import json
import logging
import os
import time
from typing import Any, Callable, Optional

from src.events.pricing import estimate_cost
from src.sources.resolve import resolve_sources
from src.vocabularies.pins import vocabulary_drift
from src.sources.schemas import SourceSpec

logger = logging.getLogger(__name__)

DEPTHS = ("surface", "standard")
MAX_CHARS = int(os.environ.get("ENGINE_CALL_MAX_CHARS", "400000"))
OUTPUT_TOKENS = 4000
SYSTEM_TOKENS = 7000   # the composed prompt: framing, four method cards, the anchoring law
CONTEXT_ROLES = {"plan": "PLAN", "profile": "WORK PROFILE", "evidence_index": "EVIDENCE INDEX", "statements": "STATEMENTS", "cohort": "COHORT"}

# engine_key -> (final_output, failed_ids, refs) -> shaped JSON
RENDERERS: dict[str, Callable[..., Optional[dict]]] = {}


def _renderers() -> dict[str, Callable[..., Optional[dict]]]:
    if not RENDERERS:
        from src.dossier.explainer import render_explanation
        from src.dossier.reread import render_reread
        RENDERERS["citation_explainer"] = render_explanation
        RENDERERS["reference_reread"] = render_reread
    return RENDERERS


def normalize_model(model: Optional[str]) -> Optional[str]:
    """A caller's model id in this house's namespace: `claude-…` and `gemini-…` go direct, `openrouter/<vendor>/<id>`
    through OpenRouter; an OpenRouter-style `anthropic/<id>` becomes the direct id, any other `<vendor>/<id>` goes
    through OpenRouter."""
    if not model:
        return None
    m = model.strip()
    if m.startswith(("claude-", "gemini-", "openrouter/")):
        return m
    if m.startswith("anthropic/"):
        return m.split("/", 1)[1]
    if "/" in m:
        return "openrouter/" + m
    raise ValueError(f"unknown model id {m!r}: give claude-…, gemini-…, or <vendor>/<model> for OpenRouter")


def estimate_usd(model: str, chars: int, *, depth: str, mid_model: str = "") -> float:
    """What the call will cost before it runs: the reading on `model`, plus the critic on `mid_model` at standard depth."""
    tokens_in = int(chars / 3.5) + SYSTEM_TOKENS
    tokens_out = max(OUTPUT_TOKENS, int(tokens_in * 0.4))   # a one-call reading writes about 0.4 tokens per input token (explainer 7K→2.8K; reread 116K→46K, 2026-09-07)
    cost = estimate_cost(model, tokens_in, tokens_out) or 0.0
    if depth == "standard":
        cost += estimate_cost(mid_model or model, tokens_in + tokens_out, tokens_out) or 0.0
    return round(cost, 4)


def _context_block(packet: Optional[dict], docs: list) -> str:
    parts = []
    if packet:
        parts.append("CITATION PACKET (context, not an anchor source; its citation ids are the `ref` field of the rows; "
                     "the passage sentence is the one to find in the section):\n" + json.dumps(packet, ensure_ascii=False))
    for d in docs:
        role = getattr(d, "role", "source") or "source"
        if role == "source":
            continue
        parts.append(f"{CONTEXT_ROLES.get(role, role.upper())} [{d.key}] (context, not an anchor source):\n{d.text}")
    return "\n\n".join(parts)


def call_engine(engine_key: str, sources: list[SourceSpec], *, packet: Optional[dict] = None, depth: str = "surface",
                model: Optional[str] = None, spend_cap_usd: float = 0.5, call_fn: Optional[Callable] = None,
                refs: Optional[dict[str, Any]] = None, max_chars: Optional[int] = None,
                method_snapshot: Optional[dict] = None, expected_method_sha256: Optional[str] = None) -> dict:
    """Run one engine over the supplied sources in this request. Raises KeyError for an unknown engine, ValueError
    for a bad request (depth, model, size, the cap)."""
    from src.engines.registry import get_engine_registry
    from src.executor.ledger_walls import SourceIndex, parse_rows, verify_rows
    from src.executor.context_broker import split_ledger
    from src.executor.process_runner import ProcessStep, resolve_step_model, run_oneshot_checked
    from src.operationalizations.registry import get_operationalization_registry
    from src.dossier.cohort_export import fields_of

    if depth not in DEPTHS:
        raise ValueError(f"depth must be one of {DEPTHS}; the deep process runs as a dossier job")
    from src.engines.methods import freeze_method, compose_method, method_receipt, validate_snapshot
    if method_snapshot is None:
        cap_def = get_engine_registry().get_capability_definition(engine_key)
        op = get_operationalization_registry().get(engine_key)
        if cap_def is None or op is None or op.process is None:
            raise KeyError(f"no engine with a process named {engine_key!r}")
    method_snapshot = method_snapshot or freeze_method(engine_key)
    validate_snapshot(method_snapshot, engine_key)
    if expected_method_sha256 is not None and method_snapshot['sha256'] != expected_method_sha256:
        raise ValueError('The requested central method version changed; nothing was spent')
    cap_def, spec = compose_method(method_snapshot)
    from src.sources.citation_evidence import FAMILY, prepare_citation_sources

    docs = resolve_sources(sources)
    unpacked_roles = {"statements", "evidence_index"} if engine_key in FAMILY else set()   # the family unpacks these into witnesses
    documents = {d.key: d.text for d in docs if (getattr(d, "role", "source") or "source") in unpacked_roles | {"source"} and d.text}
    if not documents:
        raise ValueError("no source with text was supplied (a source needs kind=paste and text)")
    upstream = _context_block(packet, [d for d in docs if (getattr(d, "role", "source") or "source") not in unpacked_roles])
    chars = sum(len(v) for v in documents.values()) + len(upstream)
    cap = max_chars or MAX_CHARS
    if chars > cap:
        raise ValueError(f"{chars:,} chars supplied; this route takes at most {cap:,} (a dossier job takes more)")
    strong = normalize_model(model) or resolve_step_model(ProcessStep(key="read", kind="synthesize", model_tier="strong"), spec)
    mid = resolve_step_model(spec.get_step("verify") or ProcessStep(key="verify", kind="verify", model_tier="mid"), spec)
    est = estimate_usd(strong, chars, depth=depth, mid_model=mid)
    if est > spend_cap_usd:
        raise ValueError(f"estimated ${est:.2f} for {chars:,} chars on {strong} at {depth} depth passes the cap ${spend_cap_usd:.2f}; nothing was spent")
    t0 = time.time()
    result = run_oneshot_checked(cap_def, spec, documents, depth=depth, check=(depth == "standard"),
                                 tier_overrides={"strong": strong} if model else None, call_fn=call_fn, upstream_context=upstream)
    prose, ledger = split_ledger(result.final_content or "")
    rows = parse_rows(ledger or result.final_content or "")
    witnesses = prepare_citation_sources(engine_key, documents)[0] if engine_key in FAMILY else documents   # the wall reads what the engine read
    rep = verify_rows(rows, SourceIndex(witnesses))
    failed = set(rep.failed_ids)
    row_dicts = []
    for r in rows:
        f = fields_of(r.render())
        row_dicts.append({"id": r.id, "dim": r.dim or f.get("dim", ""), "doc": r.doc or f.get("doc", ""), "finding": r.finding or r.text.split(" — ", 1)[0],
                          "fields": {k: v for k, v in f.items() if k not in ("anchor", "doc", "dim")}, "anchor": r.anchor,
                          "anchor_verified": bool(r.anchor_verified), "status": r.status, "confidence": r.confidence})
    renderer = _renderers().get(engine_key)
    shaped = renderer(result.final_content or "", failed, refs=refs) if renderer else None
    out = {"engine_key": engine_key, "depth": depth, "model": result.final_model or strong, "model_requested": model or "", "seconds": round(time.time() - t0, 1),
           "cost_usd": result.cost_usd, "estimated_usd": est, "chars": chars, "calls": [c.as_receipt() for c in result.calls],
           "wall": {"anchors": len(rows), "verified": sum(1 for r in rows if r.anchor_verified), "failed_ids": sorted(failed), "vocabulary_drift": vocabulary_drift(rows, engine_key)[:40]},
           "prose": prose, "final_output": result.final_content, "rows": row_dicts, "shaped": shaped,
           "method_receipt": method_receipt(method_snapshot), "method_snapshot": method_snapshot}
    logger.info("engine call %s · %s · %s · %d chars · %d rows (%d verified) · $%.4f · %.1fs", engine_key, depth, out["model"], chars,
                len(rows), out["wall"]["verified"], result.cost_usd, out["seconds"])
    return out
