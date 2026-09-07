"""Add one engine step to a finished dossier job (2026-09-07 13:20): the engine runs as a light call over the job's own documents
and its phase is appended to the job's analysis, where the renderers read it like any other phase. Built for the placement step
over a run made before the recipe had it (run 3 of Brenner 1985); general for any engine that reads the job's documents.

The sources: every document of role `source` within the light call's size cap; an engine may narrow them — thinker_placement reads
the focal text and the texts that cite the persons to place. The packet: the job's plan document (the oeuvre packet) when it has one.
"""
from __future__ import annotations

import json
from typing import Any, Callable, Optional

from src.sources.schemas import SourceSpec


def sources_for(engine_key: str, documents: list[dict], packet: dict, get_text: Callable[[str], str], max_chars: int) -> list[SourceSpec]:
    """The documents an added step reads, as sources: narrowed for engines that know what they need, else the sources in order
    until the cap."""
    docs = [d for d in documents if d.get("role") == "source" and d.get("executor_doc_id")]
    keep = docs
    if engine_key == "thinker_placement":
        uids = {u for e in packet.get("persons_unknown") or [] for side in (e.get("cited_in") or {}).values() for u in side}
        keep = [d for d in docs if str(d.get("key", "")).startswith("focal:") or any(str(d.get("key", "")).endswith(":" + u) for u in uids)]
    out, total = [], 0
    for d in keep:
        text = get_text(d["executor_doc_id"]) or ""
        if not text.strip():
            continue
        if total + len(text) > max_chars:
            if any(s.key.startswith("focal:") for s in out) or not str(d.get("key", "")).startswith("focal:"):
                continue
        out.append(SourceSpec(kind="paste", role="source", key=d.get("key"), title=d.get("title") or d.get("key"), text=text))
        total += len(text)
    return out


def packet_for(engine_key: str, packet: dict) -> Optional[dict]:
    """What of the plan document the added step's packet carries: the placement step needs the persons and the schools, not
    the citation tables."""
    if not packet:
        return None
    if engine_key == "thinker_placement":
        return {k: packet[k] for k in ("focal", "author", "persons_unknown", "schools", "notes") if k in packet} | {"persons": (packet.get("persons") or [])[:60]}
    return packet


def add_step(job: dict, engine_key: str, *, get_text: Callable[[str], str], call: Callable[..., dict], depth: str = "surface",
             model: Optional[str] = None, spend_cap_usd: float = 2.0, max_chars: int = 400_000) -> dict:
    """Run `engine_key` over the job's documents and append its phase to `job['analysis']` (mutated and returned as the new
    phase). `call` is call_engine or a stand-in with its signature."""
    documents = job.get("documents") or []
    packet: dict = {}
    for d in documents:
        if d.get("role") == "plan" and d.get("executor_doc_id"):
            try:
                packet = json.loads(get_text(d["executor_doc_id"]) or "{}")
            except ValueError:
                packet = {}
            break
    sources = sources_for(engine_key, documents, packet, get_text, max_chars)
    if not sources:
        raise ValueError("the job has no source documents this step can read")
    out = call(engine_key, sources, packet=packet_for(engine_key, packet), depth=depth, model=model, spend_cap_usd=spend_cap_usd)
    analysis = job.setdefault("analysis", {}) or {}
    numbers = [float(k) for k in analysis.keys() if str(k).replace(".", "", 1).isdigit()]
    base = int(max(numbers)) if numbers else 4
    n = max([x for x in numbers if int(x) == base] + [float(base)])
    key = f"{base}.{int(round((n - base) * 10)) + 1}"
    phase = {"phase_number": float(key), "engine_key": engine_key, "engine_name": out.get("engine_name") or engine_key, "depth": depth, "passes": [],
             "final_output": out.get("final_output") or "", "final_wall": {"failed_ids": (out.get("wall") or {}).get("failed_ids") or [], "verified": (out.get("wall") or {}).get("verified"),
                                                                            "anchors": (out.get("wall") or {}).get("anchors")},
             "added": True, "cost_usd": out.get("cost_usd"), "model": out.get("model"), "seconds": out.get("seconds"), "sources": [s.key for s in sources]}
    analysis[key] = phase
    job["analysis"] = analysis
    totals = job.get("totals") or {}
    totals["cost_usd"] = round(float(totals.get("cost_usd") or 0) + float(out.get("cost_usd") or 0), 4)
    totals["llm_calls"] = int(totals.get("llm_calls") or 0) + len(out.get("calls") or [])
    job["totals"] = totals
    return phase
