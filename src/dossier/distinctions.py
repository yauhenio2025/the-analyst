"""The distinction round rendered by code (Evgeny, 2026-09-07 13:34: "on the questions you are arguing, they argue this; your position
seems to be this; is it correct? restate? elaborate?"): the rows of interlocutor_position, distinction_draft and distinction_settle
joined per interlocutor and question, and the questions back as the payloads the Stacks file as challenges of kind `distinction`.
Shape only; a row the wall could not anchor is carried with `conjecture`."""
from __future__ import annotations

import re
from typing import Any, Optional

from src.dossier.explainer import CITED_ID, rows_with_fields

ENGINES = ("interlocutor_position", "distinction_draft", "distinction_settle", "impact_scan")


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
    return {"id": f"{r['engine']}/{r['id']}", "text": r["text"], **{k: f.get(k, "") for k in fields}, "anchor": r.get("anchor", ""), "doc": r.get("doc", ""),
            "confidence": r.get("confidence", ""), "conjecture": r["conjecture"]}


def render_distinctions(job: dict) -> Optional[dict]:
    """A finished round → the questions, each interlocutor's claims and silences, the owner's inferred positions, the relations, the
    questions back as challenge payloads, and (after the settle round) the settled distinctions with their effects."""
    phases = _phases(job)
    if not phases:
        return None
    by = {e: _rows(job, e) for e in ENGINES}
    questions = [_row(r, "interlocutors") for r in by["interlocutor_position"] if r["dim"] == "question"]
    claims = [_row(r, "interlocutor", "question", "role", "locus", "turn_says") for r in by["interlocutor_position"] if r["dim"] == "their_claim"]
    silences = [_row(r, "interlocutor", "question") for r in by["interlocutor_position"] if r["dim"] == "their_silence"]
    positions = [_row(r, "question", "part") for r in by["distinction_draft"] if r["dim"] == "your_position"]
    relations = [_row(r, "interlocutor", "question", "position", "claim", "relation", "relation_raw", "axis", "ours", "theirs", "bridge", "bears_on") for r in by["distinction_draft"] if r["dim"] == "relation"]
    asks = [_row(r, "from", "interlocutor", "kind", "options") for r in by["distinction_draft"] if r["dim"] == "question_back"]
    settled = [_row(r, "interlocutor", "from", "relation_kind", "axis", "because", "sayable") for r in by["distinction_settle"] if r["dim"] == "distinction"]
    effects = [_row(r, "distinction", "part", "relation") for r in by["distinction_settle"] if r["dim"] == "effect"]
    open_ = [_row(r, "decided_by", "held") for r in by["distinction_settle"] if r["dim"] == "open"]
    q_by = {q["id"].split("/", 1)[1]: q for q in questions}
    c_by = {c["id"].split("/", 1)[1]: c for c in claims}
    p_by = {p["id"].split("/", 1)[1]: p for p in positions}
    r_by = {x["id"].split("/", 1)[1]: x for x in relations}
    # the challenges: one per question back, with everything the Stacks render (their claim anchored, your position, the relation, the question)
    challenges = []
    for a in asks:
        rel = r_by.get(a.get("from", ""), {})
        claim = c_by.get(rel.get("claim", ""), {}); pos = p_by.get(rel.get("position", ""), {}); q = q_by.get(rel.get("question", ""), {})
        challenges.append({"kind": "distinction", "interlocutor": a.get("interlocutor") or rel.get("interlocutor", ""), "question": {"id": q.get("id"), "text": q.get("text", "")},
                           "their_claim": {"id": claim.get("id"), "text": claim.get("text", ""), "doc": claim.get("doc", ""), "locus": claim.get("locus", ""), "anchor": claim.get("anchor", ""), "role": claim.get("role", "")},
                           "your_position": {"id": pos.get("id"), "text": pos.get("text", ""), "part": pos.get("part", ""), "anchor": pos.get("anchor", "")},
                           "relation": {"id": rel.get("id"), "relation": rel.get("relation", ""), "axis": rel.get("axis", ""), "ours": rel.get("ours", ""), "theirs": rel.get("theirs", ""), "bridge": rel.get("bridge", "")},
                           "ask": {"id": a["id"], "kind": a.get("kind", ""), "text": a["text"], "options": [o.strip() for o in (a.get("options") or "").split("|") if o.strip() and o.strip().lower() != "none"]},
                           "bears_on": sorted({int(x) for x in re.findall(r"\d+", rel.get("bears_on") or "")} | ({int(pos["part"])} if str(pos.get("part") or "").isdigit() else set())),   # the parts the claim touches: the reach of the distinction is the reading's to say (the Stacks' ledger, 15:55)
                           "conjecture": any(x.get("conjecture") for x in (a, rel, claim, pos) if x)})
    # per interlocutor: the view a reader scans
    names = sorted({c["interlocutor"] for c in claims} | {r["interlocutor"] for r in relations} | {s["interlocutor"] for s in silences})
    interlocutors = [{"name": n, "claims": [c for c in claims if c["interlocutor"] == n], "silences": [s for s in silences if s["interlocutor"] == n],
                      "relations": [r for r in relations if r["interlocutor"] == n], "settled": [s for s in settled if s["interlocutor"] == n]} for n in names]
    impact = {"touched": [_row(r, "part", "relation", "from") for r in by["impact_scan"] if r["dim"] == "impact"],
              "dependencies": [_row(r, "part", "on", "how", "relation") for r in by["impact_scan"] if r["dim"] == "dependency"],
              "retests": [_row(r, "test", "run", "because") for r in by["impact_scan"] if r["dim"] == "retest"]}   # what the settled distinction changes elsewhere (the impact scan, 2026-09-07)
    drift = [{"finding": f"{r['engine']}/{r['id']}", **d} for e in ENGINES for r in by[e] for d in r.get("drift") or []]
    return {"engine": "distinction", "impact": impact, "job_id": job.get("id"), "phases": list(phases), "rows": sum(len(v) for v in by.values()),
            "conjectures": sum(1 for v in by.values() for r in v if r["conjecture"]), "questions": questions, "interlocutors": interlocutors,
            "positions": positions, "challenges": challenges, "settled": settled, "effects": effects, "open": open_, "vocabulary_drift": drift}
