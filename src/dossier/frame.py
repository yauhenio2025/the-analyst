"""The evidential frame of a hypothesis test, rendered from the engine's ledger by code (2026-09-06).

`hypothesis_evidential_frame` writes rows in the house answer shape (S1 strengthen · S2 weaken · S3 form · S4
decisive_test · S5 residual). This module turns a finished job's rows into the JSON the Stacks' hunch lane stores per
pass: {strengthen[], weaken[], form: {paragraph, conditions[]}, decisive_tests[], residual[], works[]}. Shape only:
nothing is judged or invented here; a row without a verified anchor is carried with `conjecture: true`.
"""
from __future__ import annotations

import re
from typing import Any, Optional

from src.dossier.cohort_export import fields_of

ENGINE = "hypothesis_evidential_frame"
ROW = re.compile(r"^\s*(?:[-*]\s+)?\[((?:S\d\.)?F\d+)\]")
WORK = re.compile(r"[A-Z][^;,()]{1,60}, [^;()]{2,120} \(\d{4}[a-z]?\)")


def _rows(final_output: str, failed: set[str]) -> list[dict]:
    from src.executor.ledger_walls import parse_rows

    lines = {m.group(1): line.strip() for line in final_output.splitlines() for m in [ROW.match(line)] if m}
    out = []
    for r in parse_rows(final_output):
        raw = lines.get(r.id)
        if not raw:
            continue
        f = fields_of(raw)
        head = re.sub(r"^\s*(?:[-*]\s+)?\[[^\]]+\]\s*", "", raw.split(" — ", 1)[0]).strip()
        anchor = (f.get("anchor") or "").strip().strip('"“”')
        out.append({"id": r.id, "dim": r.dim or f.get("dim", ""), "text": head, "fields": f, "anchor": anchor, "doc": r.doc or f.get("doc", ""),
                    "conjecture": (not anchor) or (r.id in failed), "confidence": f.get("confidence", "")})
    return out


def _form_paragraph(prose: str) -> str:
    """The opening paragraph of the synthesis that joins the form conditions (the brief asks for it first)."""
    body = prose.split("\n## ", 1)[0] if prose.startswith("## ") else prose
    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip() and not p.strip().startswith(("#", "|", "- [", "[S"))]
    return paras[0] if paras else ""


FROM = re.compile(r"^(?:CHECK|READ|EXTRACT|VERIFY)?\.?((?:S\d\.)?F\d+)$")


def carry_fields(rows: list[dict], passes: Optional[list[str]]) -> int:
    """The checked mode's reconciliation renumbers rows and can drop the answer shape's own fields (kind, where, held,
    rank…); a final row that says `from: CHECK.S1.F2` gets the missing fields back from the earlier pass that still
    carries `[S1.F2]`. Shape only: a field present on the final row is never overwritten."""
    if not passes:
        return 0
    earlier: dict[str, dict[str, str]] = {}
    for text in passes:
        for line in text.splitlines():
            m = ROW.match(line)
            if m and m.group(1) not in earlier:
                earlier[m.group(1)] = fields_of(line.strip())
    carried = 0
    for r in rows:
        src = r["fields"].get("from", "")
        m = FROM.match(src.strip())
        origin = earlier.get(m.group(1)) if m else None
        if not origin:
            continue
        for k, v in origin.items():
            if k not in r["fields"] and k not in ("anchor", "doc", "dim", "from"):
                r["fields"][k] = v; carried += 1
        if not r["anchor"] and origin.get("anchor"):
            r["anchor"] = origin["anchor"].strip().strip('"“”'); r["conjecture"] = False
    return carried


def passes_of(job: dict) -> list[str]:
    """The engine phase's earlier pass contents from the executor's output store (this instance)."""
    sub = job.get("analysis_job_id")
    if not sub:
        return []
    try:
        from src.executor.output_store import load_all_job_outputs
        rows = load_all_job_outputs(sub, include_content=True)
    except Exception:
        return []
    return [r.get("content") or "" for r in rows if r.get("engine_key") == ENGINE and (r.get("stance_key") or "") in ("read", "check", "extract", "verify")]


def render_frame(job: dict, passes: Optional[list[str]] = None) -> Optional[dict]:
    """The frame JSON from a job record (a dict, the store's or the API's); None when the engine did not run.
    `passes` = the phase's earlier pass contents (read, check), from which the reconciled rows' fields are carried."""
    analysis = job.get("analysis") or {}
    phase = next((ph for _, ph in sorted(analysis.items(), key=lambda kv: float(kv[0])) if ph.get("engine_key") == ENGINE), None)
    if not phase or not phase.get("final_output"):
        return None
    failed = set((phase.get("final_wall") or {}).get("failed_ids") or [])
    rows = _rows(phase["final_output"], failed)
    carried = carry_fields(rows, passes)
    prose = phase["final_output"].split("\n- [", 1)[0]
    def ev(r):
        return {"id": r["id"], "evidence": r["text"], "kind": r["fields"].get("kind", ""), "where": r["fields"].get("where", ""),
                "held": r["fields"].get("held", "unknown").split("|")[0].strip(), "anchor": r["anchor"], "doc": r["doc"],
                "conjecture": r["conjecture"], "confidence": r["confidence"]}
    tests = []
    for r in rows:
        if r["dim"] != "decisive_test":
            continue
        rank = re.search(r"\d+", r["fields"].get("rank", "") or "")
        tests.append({"id": r["id"], "test": r["text"], "question": r["fields"].get("question", ""), "evidence_needed": r["fields"].get("evidence-needed", ""),
                      "sources": [s.strip() for s in re.split(r";", r["fields"].get("sources", "")) if s.strip()],
                      "decidable_now": r["fields"].get("decidable-now", "").split("|")[0].strip(), "why": r["fields"].get("why", ""),
                      "rank": int(rank.group(0)) if rank else 99, "anchor": r["anchor"], "doc": r["doc"], "conjecture": r["conjecture"]})
    tests.sort(key=lambda t: t["rank"])
    works: list[str] = []
    for r in rows:
        for cand in [r["fields"].get("where", "")] + [s.strip() for s in re.split(r";", r["fields"].get("sources", ""))]:
            for m in WORK.finditer(cand or ""):
                w = m.group(0).strip()
                if w not in works:
                    works.append(w)
    return {"engine": ENGINE, "job_id": job.get("id"), "verdict_vocabulary": ["holds", "holds in part", "does not hold", "unclear"],
            "strengthen": [ev(r) for r in rows if r["dim"] == "strengthen"],
            "weaken": [ev(r) for r in rows if r["dim"] == "weaken"],
            "form": {"paragraph": _form_paragraph(prose),
                     "conditions": [{"id": r["id"], "condition": r["text"], "account": r["fields"].get("account", ""), "anchor": r["anchor"], "doc": r["doc"], "conjecture": r["conjecture"]}
                                    for r in rows if r["dim"] == "form"]},
            "decisive_tests": tests, "tests": tests,
            "residual": [f"{r['text']} (because: {r['fields'].get('because', '?')})" for r in rows if r["dim"] == "residual"],
            "works": works, "rows": len(rows), "conjectures": sum(1 for r in rows if r["conjecture"]), "fields_carried_from_passes": carried}
