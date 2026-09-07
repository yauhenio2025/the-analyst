"""The encounter rendered by code (Evgeny, 2026-09-07 17:40: "encounter, then impact scan"): one thinker's system mapped for the owner
(positions across the oeuvre, concepts, opponents, turns, silences) and the draft (axes, relations, takes, questions back, the route in),
joined per axis; the questions back as `distinction` challenge payloads. Shape only; unanchored rows carry `conjecture`."""
from __future__ import annotations

import re
from typing import Any, Optional

from src.dossier.explainer import CITED_ID, rows_with_fields

ENGINES = ("encounter_map", "encounter_draft", "distinction_settle")


def _clean(text: str) -> str:
    return CITED_ID.sub("", text or "").strip()


def _phases(job: dict) -> dict[str, tuple[str, set[str]]]:
    out = {}
    for ph in (job.get("analysis") or {}).values():
        k = ph.get("engine_key")
        if k in ENGINES and ph.get("final_output"):
            out[k] = (ph["final_output"], set((ph.get("final_wall") or {}).get("failed_ids") or []))
    return out


def _rows(job: dict, engine: str) -> list[dict]:
    got = _phases(job).get(engine)
    if not got:
        return []
    rows = rows_with_fields(got[0], got[1], engine_key=engine)
    for r in rows:
        r["engine"] = engine; r["text"] = _clean(r["text"])
    return rows


def _row(r: dict, *fields: str) -> dict:
    f = r["fields"]
    out = {"id": f"{r['engine']}/{r['id']}", "text": r["text"], **{k: f.get(k, "") for k in fields if k != "text"}, "anchor": r.get("anchor", ""), "doc": r.get("doc", ""),
           "confidence": r.get("confidence", ""), "conjecture": r["conjecture"]}
    if "text" in fields:
        out["ref"] = f.get("text", "")      # a shape field named `text` (the uid or title of a text) never overwrites the row's sentence
    return out


def _ids(s: str) -> list[str]:
    return [x for x in re.split(r"[;,\s]+", s or "") if re.match(r"^[A-Z]\d\.F\d+$", x)]


def render_encounter(job: dict, thinker: str = "") -> Optional[dict]:
    phases = _phases(job)
    if not ({"encounter_map", "encounter_draft"} & set(phases)):
        return None
    by = {e: _rows(job, e) for e in ENGINES}
    m = by["encounter_map"]; d = by["encounter_draft"]
    positions = [_row(r, "question", "text", "period", "locus") for r in m if r["dim"] == "position"]
    concepts = [_row(r, "concept", "carries", "puts_to_owner") for r in m if r["dim"] == "concept"]
    opponents = [_row(r, "opponent", "question", "shared") for r in m if r["dim"] == "opponent"]
    turns = [_row(r, "question", "from", "to", "changed") for r in m if r["dim"] == "turn"]
    silences = [_row(r, "question") for r in m if r["dim"] == "silence"]
    axes = [_row(r, "gathers", "parts") for r in d if r["dim"] == "axis"]
    from src.dossier.distinctions import _to_you
    relations = [{**_row(r, "axis", "relation", "relation_raw", "ours", "theirs", "bridge", "bears_on"), "ours": _to_you(_row(r, "ours").get("ours", ""))} for r in d if r["dim"] == "relation"]
    takes = [_row(r, "element", "take", "take_raw", "into") for r in d if r["dim"] == "take"]
    asks = [_row(r, "from", "kind", "options") for r in d if r["dim"] == "question_back"]
    route = sorted([_row(r, "text", "held", "rank", "axis", "why") for r in d if r["dim"] == "read_next"], key=lambda x: int(x["rank"]) if str(x.get("rank") or "").isdigit() else 99)
    short = {x["id"].split("/", 1)[1]: x for x in positions + concepts + axes + relations + takes}
    per_axis = []
    for a in axes:
        aid = a["id"].split("/", 1)[1]
        per_axis.append({"axis": a, "relations": [x for x in relations if x.get("axis") == aid], "positions": [short[i] for i in _ids(a.get("gathers", "")) if i in short],
                         "route": [x for x in route if x.get("axis") == aid]})
    challenges = []
    for q in asks:
        src = short.get(q.get("from", ""), {})
        rel = src if src.get("relation") is not None else {}
        challenges.append({"kind": "distinction", "interlocutor": thinker, "encounter": True, "from": src.get("id"),
                           "relation": {"id": rel.get("id"), "relation": rel.get("relation", ""), "axis": short.get(rel.get("axis", ""), {}).get("text", ""), "ours": rel.get("ours", ""), "theirs": rel.get("theirs", ""), "bridge": rel.get("bridge", "")} if rel else None,
                           "take": {"id": src.get("id"), "take": src.get("take", ""), "element": src.get("element", ""), "text": src.get("text", "")} if src.get("take") is not None else None,
                           "ask": {"id": q["id"], "kind": q.get("kind", ""), "text": q["text"], "options": [o.strip() for o in (q.get("options") or "").split("|") if o.strip() and o.strip().lower() != "none"]},
                           "bears_on": sorted({int(x) for x in re.findall(r"\d+", (rel.get("bears_on") or "") if rel else "")}), "conjecture": bool(q.get("conjecture") or src.get("conjecture"))})
    drift = [{"finding": f"{r['engine']}/{r['id']}", **x} for e in ENGINES for r in by[e] for x in r.get("drift") or []]
    return {"engine": "encounter", "job_id": job.get("id"), "thinker": thinker, "phases": list(phases), "rows": sum(len(v) for v in by.values()),
            "conjectures": sum(1 for v in by.values() for r in v if r["conjecture"]), "positions": positions, "concepts": concepts, "opponents": opponents, "turns": turns,
            "silences": silences, "axes": per_axis, "takes": takes, "challenges": challenges, "read_next": route,
            "settled": [_row(r, "interlocutor", "from", "relation_kind", "axis", "because", "sayable") for r in by["distinction_settle"] if r["dim"] == "distinction"],
            "vocabulary_drift": drift}
