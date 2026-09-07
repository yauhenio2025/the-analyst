"""One citation explained in its place, rendered from the engine's ledger by code (2026-09-06).

`citation_explainer` writes rows in the house answer shape (E1 how · E2 why_here · E3 in_argument · X4 across_texts)
and a reading in headed parts. This module turns a finished call's output into the JSON the Stacks' cites page stores
per citation: {how, why, fit, intent, quote, move, stance, place, section_role, quote_verified, …}, one per citation
id (`ref`), plus the across-texts rows when several texts were supplied. Shape only: nothing is judged or invented
here; a row whose anchor the wall could not find is carried with `conjecture: true`.
"""
from __future__ import annotations

import re
from typing import Any, Iterable, Optional

from src.dossier.cohort_export import fields_of

ENGINE = "citation_explainer"
ROW = re.compile(r"^\s*(?:[-*]\s+)?\[((?:[A-Z]\d\.)?F\d+)\]")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)
BOLD_LEAD = re.compile(r"^\*\*([^*]{2,40}?)[.:]?\*\*[.:]?\s*", re.M)
CITED_ID = re.compile(r"\s*[\(\[]\s*(?:[A-Z]\d\.)?F\d+(?:\s*[,;]\s*(?:[A-Z]\d\.)?F\d+)*\s*[\)\]]")
PARTS = {"how": ("how",), "why": ("why here", "why_here"), "fit": ("in the argument", "in_argument"),
         "across": ("across the texts", "across_texts")}


def _pinned(engine_key: Optional[str]) -> dict[str, list[str]]:
    """The fields a vocabulary pins for this engine → its values (shape: an enumerated value outside its vocabulary is drift)."""
    if not engine_key:
        return {}
    from src.vocabularies.registry import get_vocabulary_registry
    out: dict[str, list[str]] = {}
    for v in get_vocabulary_registry().for_engine(engine_key):
        for u in v.used_by:
            if u.engine_key == engine_key and u.field:
                out[u.field] = v.value_list()
    return out


def pin_fields(fields: dict, pinned: dict[str, list[str]]) -> list[dict]:
    """Normalise enumerated fields in place: a value outside its vocabulary that contains exactly one vocabulary word ("qualified
    culmination" → culmination) is replaced, the raw value kept under `<field>_raw`; anything else is left and reported. Returns the
    drift rows (2026-09-07: run 3's retrospective verdict came back qualified; no wall had read the vocabularies)."""
    drift = []
    for field, allowed in pinned.items():
        raw = (fields.get(field) or "").strip()
        if not raw:
            continue
        val = raw.lower().replace(" ", "_")
        if val in allowed:
            if val != raw:
                fields[field] = val
            continue
        hits = [a for a in allowed if re.search(r"(?<![a-z])" + re.escape(a).replace("_", "[ _]") + r"(?![a-z])", raw.lower())]
        fixed = hits[0] if len(hits) == 1 else None
        if fixed:
            fields[field + "_raw"] = raw; fields[field] = fixed
        drift.append({"field": field, "value": raw, "fixed": fixed})
    return drift


def rows_with_fields(final_output: str, failed: Iterable[str] = (), engine_key: Optional[str] = None) -> list[dict]:
    """Every ledger row with its answer-shape fields, the wall's verdict folded in as `conjecture`; with `engine_key`, the fields a
    vocabulary pins are checked against it (`drift` on the row when a value was outside it)."""
    from src.executor.ledger_walls import parse_rows

    pinned = _pinned(engine_key)
    failed = set(failed)
    lines = {m.group(1): line.strip() for line in final_output.splitlines() for m in [ROW.match(line)] if m}
    out = []
    for r in parse_rows(final_output):
        raw = lines.get(r.id)
        if not raw:
            continue
        f = fields_of(raw)
        head = re.sub(r"^\s*(?:[-*]\s+)?\[[^\]]+\]\s*", "", raw.split(" — ", 1)[0]).strip()
        anchor = (f.get("anchor") or "").strip().strip('"“”')
        anchored = bool(anchor) or bool((f.get("anchor-b") or "").strip().strip('"“”'))
        row = {"id": r.id, "dim": r.dim or f.get("dim", ""), "text": head, "fields": f, "anchor": anchor,
               "doc": r.doc or f.get("doc", ""), "conjecture": (not anchored) or (r.id in failed),
               "confidence": f.get("confidence", "")}
        if pinned:
            drift = pin_fields(f, pinned)
            if drift:
                row["drift"] = drift
        out.append(row)
    return out


def _part_key(title: str) -> Optional[str]:
    t = title.strip().strip(":.").lower()
    for key, names in PARTS.items():
        if any(t == n or t.startswith(n) for n in names):
            return key
    return None


def _parts(prose: str) -> dict[str, str]:
    """The reading's parts (How · Why here · In the argument · Across the texts) as the model laid them out: headed
    sections, or bold-lead paragraphs (**How.** …) under one heading; row citations stripped."""
    found: dict[str, str] = {}
    heads = list(HEADING.finditer(prose))
    for i, m in enumerate(heads):
        key = _part_key(m.group(1))
        body = prose[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(prose)].strip()
        if key and key not in found:
            found[key] = CITED_ID.sub("", body).strip()
    if found:
        return found
    for para in re.split(r"\n\s*\n", prose):
        m = BOLD_LEAD.match(para.strip())
        key = _part_key(m.group(1)) if m else None
        if key and key not in found:
            found[key] = CITED_ID.sub("", para.strip()[m.end():]).strip()
    return found


def _clean(text: str) -> str:
    return CITED_ID.sub("", text or "").strip()


def render_explanation(final_output: str, failed: Iterable[str] = (), *, refs: Optional[dict[str, Any]] = None) -> Optional[dict]:
    """A finished call's output → the explanations by citation id, the across-texts rows, the reading's parts."""
    from src.executor.context_broker import split_ledger

    if not final_output:
        return None
    prose, _ = split_ledger(final_output)
    rows = rows_with_fields(final_output, failed)
    parts = _parts(prose or "")
    by_ref: dict[str, dict] = {}
    order: list[str] = []
    for r in rows:
        if r["dim"] == "across_texts":
            continue
        ref = (r["fields"].get("ref") or r["doc"] or "").strip() or "1"
        e = by_ref.get(ref)
        if e is None:
            e = by_ref[ref] = {"ref": ref, "doc": r["doc"], "how": "", "why": "", "fit": "", "intent": "", "move": "", "stance": "",
                               "object": "", "supports": "", "qualification": "", "section_role": "", "place": "", "quote": "",
                               "quote_verified": False, "confidence": "", "rows": [], "conjectures": 0, "more": [], "seen": set()}
            order.append(ref)
        e["rows"].append(r["id"])
        e["conjectures"] += int(r["conjecture"])
        f = r["fields"]
        if r["dim"] in e["seen"]:   # the first row of a dimension is the headline; later rows are further readings
            e["more"].append({"id": r["id"], "dim": r["dim"], "text": _clean(r["text"]), "quote": r["anchor"], "quote_verified": not r["conjecture"],
                              **{k: v for k, v in f.items() if k in ("move", "stance", "object", "supports", "qualification", "section-role", "place", "confidence")}})
            continue
        e["seen"].add(r["dim"])
        if r["dim"] == "how":
            e.update({"how": _clean(r["text"]), "move": f.get("move", ""), "stance": f.get("stance", ""), "object": f.get("object", ""),
                      "quote": r["anchor"], "quote_verified": not r["conjecture"], "intent": f.get("move", ""), "confidence": r["confidence"]})
        elif r["dim"] == "why_here":
            e.update({"why": _clean(r["text"]), "supports": f.get("supports", ""), "qualification": f.get("qualification", "")})
        elif r["dim"] == "in_argument":
            e.update({"fit": _clean(r["text"]), "section_role": f.get("section-role", ""), "place": f.get("place", "")})
        if not e["doc"] and r["doc"]:
            e["doc"] = r["doc"]
    explanations = [by_ref[k] for k in order]
    for e in explanations:
        seen = e.pop("seen", set())
        e["missing_fields"] = [k for k, dim in (("move", "how"), ("stance", "how"), ("place", "in_argument")) if dim in seen and not e.get(k)] + \
                              [f"row:{d}" for d in ("how", "why_here", "in_argument") if d not in seen]
    if len(explanations) == 1:   # one citation: the reading's own parts are the fuller prose, the rows their labels
        e = explanations[0]
        for key, name in (("how", "how"), ("why", "why"), ("fit", "fit")):
            if parts.get(name):
                e[key] = parts[name]
    across = [{"id": r["id"], "text": _clean(r["text"]), "texts_years": r["fields"].get("texts-years", ""), "relation": r["fields"].get("relation", ""),
               "anchor": r["anchor"], "doc": r["doc"], "anchor_b": (r["fields"].get("anchor-b") or "").strip().strip('"“”'),
               "doc_b": r["fields"].get("doc-b", ""), "conjecture": r["conjecture"], "confidence": r["confidence"]}
              for r in rows if r["dim"] == "across_texts"]
    if refs:
        for e in explanations:
            e["citation"] = refs.get(e["ref"])
    return {"engine": ENGINE, "rows": len(rows), "conjectures": sum(int(r["conjecture"]) for r in rows), "parts": parts,
            "explanations": explanations, "across": across, "explanation": explanations[0] if len(explanations) == 1 else None,
            "summary": parts.get("across") or (prose.split("\n\n", 1)[0].strip() if prose and len(explanations) != 1 else "")}
