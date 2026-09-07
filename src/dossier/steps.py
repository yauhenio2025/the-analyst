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

READ_ROLES = {"source", "statements", "evidence_index", "profile"}   # what an added step reads; the light call unpacks the index roles itself
import os
STEP_MAX_CHARS = int(os.environ.get("STEP_MAX_CHARS", "1500000"))   # a step over a job's own documents reads what the job read (the light route's 400K cap is for pasted sources; a 680K statements file was silently skipped, 2026-09-07 15:15)


def sources_for(engine_key: str, documents: list[dict], packet: dict, get_text: Callable[[str], str], max_chars: int) -> list[SourceSpec]:
    """The documents an added step reads, as sources: narrowed for engines that know what they need, else the sources in order
    until the cap."""
    docs = [d for d in documents if (d.get("role") or "source") in READ_ROLES and d.get("executor_doc_id")]
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
        out.append(SourceSpec(kind="paste", role=d.get("role") or "source", key=d.get("key"), title=d.get("title") or d.get("key"), text=text))
        total += len(text)
    return out


def packet_for(engine_key: str, packet: dict) -> Optional[dict]:
    """What of the plan document the added step's packet carries: the placement step needs the persons and the schools, not
    the citation tables."""
    if not packet:
        return None
    if engine_key == "thinker_placement":   # the schools trimmed to what a fit needs: 401 at 300 chars each had outrun the light call's cap
        schools = [{"id": x.get("id"), "name": x.get("name"), "description": (x.get("description") or "")[:100], "sample": (x.get("sample") or [])[:3]} for x in packet.get("schools") or []]
        return {k: packet[k] for k in ("focal", "author", "persons_unknown", "notes") if k in packet} | {"persons": (packet.get("persons") or [])[:60], "schools": schools}
    return packet


def upstream_findings(job: dict, engine_key: str, cap: int = 60_000) -> dict[str, str]:
    """The final outputs of the phases a recipe lists before `engine_key`, keyed by engine (the light call has no context broker)."""
    from src.dossier.catalog import load_recipes
    before: list[str] = []
    for r in load_recipes():
        keys = [st["engine_key"] for st in r.get("steps") or []]
        if engine_key in keys:
            before += keys[:keys.index(engine_key)] + list(r.get("context") or [])   # `context`: the engines whose rows a sole step reads (distinction_settle reads the round)
    out = {}
    for ph in (job.get("analysis") or {}).values():
        k = ph.get("engine_key")
        if k in before and ph.get("final_output") and k not in out:
            out[k] = ph["final_output"][:cap]
    return out


def add_step(job: dict, engine_key: str, *, get_text: Callable[[str], str], call: Callable[..., dict], depth: str = "surface",
             model: Optional[str] = None, spend_cap_usd: float = 2.0, max_chars: int = STEP_MAX_CHARS, packet_override: Optional[dict] = None,
             extra_sources: Optional[list[dict]] = None) -> dict:
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
    if packet_override:   # a caller's blocks over the stored packet (run 3's plan document predates persons_unknown and schools)
        packet = {**packet, **packet_override}
    small = packet_for(engine_key, packet)
    upstream = upstream_findings(job, engine_key)
    if upstream:
        small = {**(small or {}), "upstream_findings": upstream}   # the rows of the recipe's earlier steps, with their ids (the engines' framings expect them)
    room = max_chars - len(json.dumps(small, ensure_ascii=False)) - 8_000 if small else max_chars   # the packet counts against the light call's cap
    extras = [SourceSpec(kind="paste", role=x.get("role") or "source", key=x.get("key"), title=x.get("title") or x.get("key"), text=x["text"]) for x in extra_sources or [] if x.get("text")]
    room -= sum(len(x.text) for x in extras)
    sources = sources_for(engine_key, documents, packet, get_text, room) + extras   # a caller's own documents (the argument's parts) ride beside the job's
    if not sources:
        raise ValueError("the job has no source documents this step can read")
    skipped = [d.get("key") for d in documents if (d.get("role") or "source") in READ_ROLES and d.get("executor_doc_id") and d.get("key") not in {x.key for x in sources}]
    out = call(engine_key, sources, packet=small, depth=depth, model=model, spend_cap_usd=spend_cap_usd, max_chars=max_chars)
    analysis = job.setdefault("analysis", {}) or {}
    numbers = [float(k) for k in analysis.keys() if str(k).replace(".", "", 1).isdigit()]
    base = int(max(numbers)) if numbers else 4
    n = max([x for x in numbers if int(x) == base] + [float(base)])
    key = f"{base}.{int(round((n - base) * 10)) + 1}"
    phase = {"phase_number": float(key), "engine_key": engine_key, "engine_name": out.get("engine_name") or engine_key, "depth": depth, "passes": [],
             "final_output": out.get("final_output") or "", "final_wall": {"failed_ids": (out.get("wall") or {}).get("failed_ids") or [], "verified": (out.get("wall") or {}).get("verified"),
                                                                            "anchors": (out.get("wall") or {}).get("anchors")},
             "added": True, "cost_usd": out.get("cost_usd"), "model": out.get("model"), "seconds": out.get("seconds"), "sources": [s.key for s in sources],
             "extra_sources": [x.key for x in extras], "skipped": skipped}   # a document the cap left out is named, never silent
    analysis[key] = phase
    job["analysis"] = analysis
    totals = job.get("totals") or {}
    totals["cost_usd"] = round(float(totals.get("cost_usd") or 0) + float(out.get("cost_usd") or 0), 4)
    totals["llm_calls"] = int(totals.get("llm_calls") or 0) + len(out.get("calls") or [])
    job["totals"] = totals
    return phase
