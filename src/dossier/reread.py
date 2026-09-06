"""The owner's references re-read against the texts, rendered from the engine's ledger by code (2026-09-06).

`reference_reread` writes rows in the house answer shape (R1 recollection · R2 source_says · X3 reread · X4 follow_up)
over a statements file (the comment as numbered statements, the named works as sources). This module turns a finished
call's or job's rows into the JSON the Stacks' references lane stores per turn: {references: [{pair, says, clue, part,
source_says, where, voice, verdict, reason, implication, quote, quote_b, …}], follow_ups: [{rank, question, licensed_by,
part, quote, doc, quote_b, doc_b}], summary}. Shape only: nothing is judged or invented here; a row whose anchor the
wall could not find is carried with `conjecture: true`.
"""
from __future__ import annotations

import re
from typing import Any, Iterable, Optional

from src.dossier.explainer import CITED_ID, rows_with_fields

ENGINE = "reference_reread"


def _q(v: Optional[str]) -> str:
    return (v or "").strip().strip('"“”')


def _clean(text: str) -> str:
    return CITED_ID.sub("", text or "").strip()


def render_reread(final_output: str, failed: Iterable[str] = (), *, refs: Optional[dict[str, Any]] = None) -> Optional[dict]:
    """A finished output → the references (one per statement × work pair) and the follow-ups, by code."""
    from src.executor.context_broker import split_ledger

    if not final_output:
        return None
    prose, _ = split_ledger(final_output)
    rows = rows_with_fields(final_output, failed)
    by_pair: dict[str, dict] = {}
    order: list[str] = []
    follow_ups: list[dict] = []
    for r in rows:
        f = r["fields"]
        if r["dim"] == "follow_up":
            rank = re.search(r"\d+", f.get("rank", "") or "")
            follow_ups.append({"id": r["id"], "rank": int(rank.group(0)) if rank else 99, "question": _clean(r["text"]), "licensed_by": f.get("licensed-by", ""),
                               "part": f.get("part", ""), "quote": r["anchor"], "doc": r["doc"], "quote_b": _q(f.get("anchor-b")), "doc_b": f.get("doc-b", ""),
                               "conjecture": r["conjecture"], "confidence": r["confidence"]})
            continue
        pair = re.sub(r"\s*\([^)]*\)\s*$", "", (f.get("pair-ref") or "").strip()) or r["doc"] or "?"   # "st3/WRIGHT (unheld)" → "st3/WRIGHT"
        e = by_pair.get(pair)
        if e is None:
            e = by_pair[pair] = {"pair": pair, "statement": pair.split("/", 1)[0], "work": pair.split("/", 1)[1] if "/" in pair else "", "says": "", "clue": "", "part": "",
                                 "source_says": "", "where": "", "voice": "", "verdict": "", "reason": "", "implication": "", "quote": "", "quote_verified": False,
                                 "quote_b": "", "doc_b": "", "quote_b_verified": False, "rows": [], "conjectures": 0}
            order.append(pair)
        e["rows"].append(r["id"]); e["conjectures"] += int(r["conjecture"])
        if r["dim"] == "recollection" and not e["says"]:
            e.update({"says": f.get("says") or _clean(r["text"]), "clue": f.get("clue", ""), "part": f.get("part", ""), "quote": e["quote"] or r["anchor"],
                      "quote_verified": e["quote_verified"] or not r["conjecture"]})
        elif r["dim"] == "source_says" and not e["source_says"]:
            e.update({"source_says": f.get("p-says") or _clean(r["text"]), "where": f.get("where", ""), "voice": f.get("voice", ""),
                      "quote_b": e["quote_b"] or r["anchor"], "doc_b": e["doc_b"] or r["doc"], "quote_b_verified": e["quote_b_verified"] or not r["conjecture"]})
        elif r["dim"] == "reread" and not e["verdict"]:
            e.update({"verdict": f.get("verdict", ""), "reason": f.get("reason", ""), "implication": f.get("implication", ""), "verdict_text": _clean(r["text"]),
                      "quote": e["quote"] or r["anchor"], "quote_verified": e["quote_verified"] or not r["conjecture"]})
            if f.get("anchor-b") and not e["quote_b"]:
                e.update({"quote_b": _q(f.get("anchor-b")), "doc_b": f.get("doc-b", ""), "quote_b_verified": not r["conjecture"]})
    references = [by_pair[k] for k in order]
    for e in references:   # a pair the model left without its reread row (an unheld work, usually) says so, by code
        e["missing_rows"] = [d for d, key in (("recollection", "says"), ("source_says", "source_says"), ("reread", "verdict")) if not e.get(key)]
    if refs:
        for e in references:
            e["statement_ref"] = refs.get(e["statement"]) or refs.get(e["pair"])
    follow_ups.sort(key=lambda x: (x["rank"], x["id"]))
    summary = ""
    if prose:
        paras = [p.strip() for p in re.split(r"\n\s*\n", prose) if p.strip() and not p.strip().startswith(("#", "|", "- ["))]
        summary = _clean(paras[0]) if paras else ""
    verdicts = {}
    for e in references:
        verdicts[e["verdict"] or "none"] = verdicts.get(e["verdict"] or "none", 0) + 1
    return {"engine": ENGINE, "rows": len(rows), "conjectures": sum(int(r["conjecture"]) for r in rows), "references": references, "follow_ups": follow_ups[:3],
            "verdicts": verdicts, "summary": summary}


def rows_from_job(job: dict) -> Optional[tuple[str, set[str]]]:
    """The reread phase's final output and the wall's failed ids from a finished dossier job record."""
    for ph in (job.get("analysis") or {}).values():
        if ph.get("engine_key") == ENGINE and ph.get("final_output"):
            return ph["final_output"], set((ph.get("final_wall") or {}).get("failed_ids") or [])
    return None
