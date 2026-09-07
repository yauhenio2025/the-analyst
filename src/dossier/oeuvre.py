"""A paper's place in its author's oeuvre, rendered from the workflow's ledgers by code (Evgeny, 2026-09-07).

The recipe `oeuvre_position` runs six engines; this module turns a finished job's rows into the JSON the Stacks' page shows:
the verdicts (place · retrospective · prospective · rupture · the joined position), the agendas and turns, the citation shifts,
the readings' rows, the reading route, the open questions — and the ACTIONS the findings license, one per row of a kind an
action declares (a cited work not held, a person not in the Referee, a test that needs a text), with the row's fields as the
action's inputs. Shape only: nothing is judged here; a row whose anchor the wall could not find is carried with `conjecture`.
"""
from __future__ import annotations

import re
from typing import Any, Iterable, Optional

from src.dossier.explainer import CITED_ID, rows_with_fields

ENGINES = ("oeuvre_trajectory", "citation_shift", "retrospective_reading", "prospective_reading", "epistemic_rupture", "oeuvre_position_memo")
ACTION_ROWS = {   # dimension → (finding kind, the row fields → action inputs)
    ("citation_shift", "unexamined"): "citation_shift.unexamined",
    ("citation_shift", "first_cited"): "citation_shift.first_cited",
    ("citation_shift", "anomaly"): "citation_shift.anomaly",
    ("epistemic_rupture", "test"): "epistemic_rupture.test",
    ("oeuvre_position_memo", "read_next"): "oeuvre_position_memo.read_next",
}


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
    rows = rows_with_fields(got[0], got[1])
    for r in rows:
        r["engine"] = engine
        r["text"] = _clean(r["text"])
    return rows


def _first(rows: list[dict], dim: str) -> Optional[dict]:
    return next((r for r in rows if r["dim"] == dim), None)


def _split_person_or_work(cited: str, kind: str) -> dict:
    """A cited string → the inputs an action expects (thinker_name for a person; work_title / work_author / work_year for a work)."""
    cited = (cited or "").strip()
    if kind == "person":
        return {"thinker_name": cited, "person_name": cited}
    m = re.match(r"^(?P<author>[^,]+,\s*[^,]+?),\s*(?P<title>.+?)(?:\s*\((?P<year>\d{4}[a-z]?)\))?$", cited)
    if m:
        return {"work_author": m.group("author").strip(), "work_title": m.group("title").strip(), "work_year": m.group("year") or ""}
    return {"work_title": cited}


def actions_for(rows: list[dict], registry=None) -> list[dict]:
    """The suggested actions: one entry per licensed row, the actions the registry lists for its kind, inputs filled."""
    from src.actions.registry import suggest

    out = []
    for r in rows:
        kind = ACTION_ROWS.get((r["engine"], r["dim"]))
        if not kind:
            continue
        f = r["fields"]
        if kind == "citation_shift.first_cited" and f.get("held", "").lower() == "yes" and f.get("in_referee", "").lower() == "yes":
            continue   # held and known: nothing to do
        fields: dict[str, Any] = {"finding_id": r["id"], "uid": f.get("text") or f.get("source") or "", "held": f.get("held", ""), "in_referee": f.get("in_referee", "")}
        fields.update(_split_person_or_work(f.get("cited") or f.get("source") or f.get("text") or "", f.get("kind") or ("person" if f.get("in_referee") else "work")))
        if f.get("in_referee", "").lower() == "yes":
            fields["referee_known"] = True
        suggested = suggest(kind, fields, registry)
        if kind in ("epistemic_rupture.test", "oeuvre_position_memo.read_next") and f.get("held", "").lower() == "yes":
            suggested = [s for s in suggested if s["organ"] == "the-stacks"]   # held: a bundle or a profile, not a fetch
        ready = [s for s in suggested if not s["missing"]]          # the actions this row can feed as it stands
        waiting = [s for s in suggested if s["missing"]]
        out.append({"finding": f"{r['engine']}/{r['id']}", "kind": kind, "cited": f.get("cited") or f.get("source") or f.get("text") or "", "row": r["text"], "held": f.get("held", ""),
                    "in_referee": f.get("in_referee", ""), "used_for": f.get("used_for") or f.get("for") or f.get("why") or "", "conjecture": r["conjecture"],
                    "actions": ready, "waiting": [{"action": s["action"], "organ": s["organ"], "missing": s["missing"]} for s in waiting]})
    return out


def render_oeuvre(job: dict, registry=None) -> Optional[dict]:
    """A finished job → the verdicts, the tables, the memo's parts and the actions."""
    from src.executor.context_broker import split_ledger

    phases = _phases(job)
    if not phases:
        return None
    by = {e: _rows(job, e) for e in ENGINES}
    t3 = _first(by["oeuvre_trajectory"], "place"); r4 = _first(by["retrospective_reading"], "verdict")
    p4 = _first(by["prospective_reading"], "verdict"); e3 = _first(by["epistemic_rupture"], "verdict"); m1 = _first(by["oeuvre_position_memo"], "position")
    verdicts = {"place": (t3 or {}).get("fields", {}).get("position", ""), "retrospective": (r4 or {}).get("fields", {}).get("verdict", ""),
                "prospective": (p4 or {}).get("fields", {}).get("verdict", ""), "rupture": (e3 or {}).get("fields", {}).get("verdict", ""),
                "halves": (e3 or {}).get("fields", {}).get("halves", ""), "position": (m1 or {}).get("fields", {}).get("position", ""),
                "warrant": (m1 or {}).get("fields", {}).get("warrant", "") or (t3 or {}).get("fields", {}).get("warrant", "")}
    memo_prose = ""
    if "oeuvre_position_memo" in phases:
        memo_prose, _ = split_ledger(phases["oeuvre_position_memo"][0])
    def table(engine, dims):
        return [{"id": r["id"], "dim": r["dim"], "text": r["text"], **{k: v for k, v in r["fields"].items() if k not in ("anchor", "anchor-b", "doc", "doc-b", "dim")},
                 "anchor": r["anchor"], "doc": r["doc"], "conjecture": r["conjecture"]} for r in by[engine] if r["dim"] in dims]
    all_rows = [r for e in ENGINES for r in by[e]]
    read_next = sorted(table("oeuvre_position_memo", {"read_next"}), key=lambda x: int(re.search(r"\d+", x.get("rank", "") or "9").group(0)) if re.search(r"\d+", x.get("rank", "") or "") else 9)
    return {"engine": "oeuvre_position", "job_id": job.get("id"), "phases": sorted(phases), "rows": len(all_rows), "conjectures": sum(int(r["conjecture"]) for r in all_rows),
            "verdicts": verdicts, "memo": _clean(memo_prose),
            "agendas": table("oeuvre_trajectory", {"agenda"}), "turns": table("oeuvre_trajectory", {"turn"}), "place": table("oeuvre_trajectory", {"place"}),
            "shifts": table("citation_shift", {"first_cited", "dropped", "carried", "anomaly", "unexamined"}),
            "retrospective": table("retrospective_reading", {"inheritance", "resolution", "interlocutor", "verdict"}),
            "prospective": table("prospective_reading", {"seed", "developed_into", "abandoned", "verdict"}),
            "rupture": table("epistemic_rupture", {"continuity", "break", "verdict", "test"}),
            "read_next": read_next, "open": table("oeuvre_position_memo", {"open"}), "actions": actions_for(all_rows, registry)}
