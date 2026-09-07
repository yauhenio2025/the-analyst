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

ENGINES = ("oeuvre_trajectory", "citation_shift", "retrospective_reading", "prospective_reading", "epistemic_rupture", "oeuvre_position_memo", "thinker_placement")
PERSON_INPUTS = {"thinker_name", "referee_thinker_id", "referee_thinker_ids", "person_name", "folder_id", "school_name", "candidate_names"}   # an action with one of these acts on a person
ANSWERED_BY_LEDGER = {"referee.thinker-exists"}                                            # the Stacks' ledger already resolved the Referee id (the owner, 2026-09-07 12:17)
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
    rows = rows_with_fields(got[0], got[1], engine_key=engine)   # enumerated fields pinned to their vocabularies
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


def placements_of(rows: list[dict]) -> dict[str, dict]:
    """The thinker_placement rows by person: the verdict, the schools they fit, the new school proposed around them."""
    out: dict[str, dict] = {}
    for r in rows:
        f = r["fields"]; who = (f.get("person") or "").strip()
        if not who:
            continue
        e = out.setdefault(who.lower(), {"person": who, "verdict": "", "reason": "", "fits": [], "new_school": None, "findings": [], "conjecture": False})
        e["findings"].append(f"{r['engine']}/{r['id']}"); e["conjecture"] = e["conjecture"] or r["conjecture"]
        if r["dim"] == "verdict":
            e["verdict"] = f.get("verdict", ""); e["reason"] = f.get("reason", "") or r["text"]
        elif r["dim"] == "fit":
            e["fits"].append({"school": f.get("school", ""), "school_name": f.get("school_name", ""), "evidence": f.get("evidence", "") or r["text"], "finding": f"{r['engine']}/{r['id']}", "confidence": f.get("confidence", ""),
                              "anchor": r.get("anchor", ""), "doc": r.get("doc", "")})
        elif r["dim"] == "new_school":
            e["new_school"] = {"name": f.get("name", ""), "candidates": [c.strip() for c in re.split(r"[;|]", f.get("candidates", "")) if c.strip()], "why": f.get("why", "") or r["text"], "finding": f"{r['engine']}/{r['id']}"}
    return out


def canonical_name(cited: str) -> str:
    """'North, Douglass C.' → 'Douglass C. North' (the Referee's dedup key per school is the canonical form)."""
    m = re.match(r"^\s*([^,]+),\s*(.+?)\s*$", cited or "")
    return f"{m.group(2)} {m.group(1)}".strip() if m else (cited or "").strip()


def actions_for(rows: list[dict], registry=None, placements: Optional[dict[str, dict]] = None, run_id: str = "") -> list[dict]:
    """The suggested actions, one entry per cited work or person that something can be done about (the owner, 2026-09-07 12:17:
    a held work and a known person need nothing; the Referee id is already resolved by the Stacks' ledger, so the only action on an
    unknown person is to add them, placed in a school or with a new school proposed around them). Inputs filled from the row;
    a person's placement rides along. Shape only."""
    from src.actions.registry import suggest

    placements = placements or {}
    out: list[dict] = []; seen: dict[str, dict] = {}
    for r in rows:
        kind = ACTION_ROWS.get((r["engine"], r["dim"]))
        if not kind:
            continue
        f = r["fields"]
        held = (f.get("held") or "").lower(); known = (f.get("in_referee") or "").lower()
        cited = (f.get("cited") or f.get("source") or f.get("text") or "").strip()
        if not _clean(cited):
            continue                                   # a row that names nothing licenses nothing
        kind_field = (f.get("kind") or "").lower()
        is_person = kind_field == "person" if kind_field in ("person", "work") else (known in ("yes", "no") and held not in ("yes", "no"))
        if is_person and known == "yes":
            continue                                   # known to the Referee: nothing to do from here
        if not is_person and held == "yes" and kind in ("citation_shift.first_cited", "citation_shift.unexamined"):
            continue                                   # held: nothing to fetch; the citation can be explained from the Stacks' page itself
        key = ("person:" if is_person else "work:") + _clean(cited).lower()
        if key in seen:                                # the same name from two dimensions (first cited and unexamined): one entry
            seen[key]["also"].append(f"{r['engine']}/{r['id']}")
            continue
        raw_uid = (f.get("text") or f.get("source") or "").strip()
        uid = raw_uid.split("/", 1)[0].strip() if raw_uid.startswith("em:") else ""          # "em:HZHLWZ2R/1977" → the bare uid (the Stacks' ask)
        fields: dict[str, Any] = {"finding_id": r["id"], "uid": uid, "text_ref": raw_uid, "held": f.get("held", ""), "in_referee": f.get("in_referee", "")}
        fields.update(_split_person_or_work(cited, "person" if is_person else "work"))
        pl = placements.get(_clean(cited).lower()) if is_person else None
        if pl and pl.get("verdict") == "not_a_candidate":
            continue                                   # an editor, a translator, a name in passing: not a thinker to add
        suggested = []
        licensed = suggest(kind, fields, registry)
        if pl:                                         # the placement's own finding kinds license the Referee's school actions
            if pl.get("fits"):
                licensed += [x for x in suggest("thinker_placement.fit", fields, registry) if x["action"] not in {y["action"] for y in licensed}]
            if pl.get("new_school"):
                ns = pl["new_school"]
                licensed += [x for x in suggest("thinker_placement.new_school", dict(fields, school_name=ns.get("name", ""), school_description=ns.get("why", ""), candidate_names="; ".join(ns.get("candidates") or []), evidence=ns.get("why", "")), registry)
                             if x["action"] not in {y["action"] for y in licensed}]
        for s_ in licensed:
            needs_person = bool(PERSON_INPUTS & {k.rstrip("?") for k in (s_["inputs"].keys() | set(s_["missing"]) | set(s_.get("optional") or []))})
            if s_["action"] in ANSWERED_BY_LEDGER and known in ("yes", "no"):
                continue
            if is_person != needs_person:
                continue                               # a person action on a work row, or the reverse (any organ)
            suggested.append(s_)
        if pl and pl.get("fits"):                      # one school-propose per fitting school, its evidence filled from the placement row
            expanded = []
            for s_ in suggested:
                if s_["action"] == "referee.school-propose":
                    for fit in pl["fits"]:   # the Referee's candidates route (12:55): evidence is an object; source_ref merges repeats per run; author_name canonical
                        e = dict(s_)
                        e["inputs"] = dict(s_["inputs"], folder_id=fit["school"], author_name=canonical_name(cited), source_kind="oeuvre", source_ref=f"oeuvre:{run_id}" if run_id else "oeuvre",
                                           evidence={"clause": fit["evidence"], "finding": "thinker_placement.fit", "run": run_id, "text": fit.get("doc", ""), "anchor": fit.get("anchor", "")})
                        e["missing"] = [k for k in s_["missing"] if k not in ("folder_id", "evidence")]
                        e["school_name"] = fit["school_name"]; expanded.append(e)
                else:
                    expanded.append(s_)
            suggested = expanded
        if kind in ("epistemic_rupture.test", "oeuvre_position_memo.read_next") and held == "yes":
            suggested = [s_ for s_ in suggested if s_["organ"] == "the-stacks"]   # held: a bundle or a profile, not a fetch
        ready = [s_ for s_ in suggested if not s_["missing"]]
        waiting = [s_ for s_ in suggested if s_["missing"]]
        if not ready and not waiting and not pl:
            continue                                   # nothing anyone can do from this row: not a suggestion
        entry = {"finding": f"{r['engine']}/{r['id']}", "also": [], "kind": kind, "cited": cited, "row": r["text"], "held": f.get("held", ""), "in_referee": f.get("in_referee", ""),
                 "used_for": f.get("used_for") or f.get("for") or f.get("why") or "", "conjecture": r["conjecture"], "placement": pl,
                 "actions": ready, "waiting": [{"action": s_["action"], "organ": s_["organ"], "missing": s_["missing"], "inputs": s_["inputs"]} for s_ in waiting]}
        seen[key] = entry; out.append(entry)
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
    placements = placements_of(by['thinker_placement'])
    drift = [{"finding": f"{r['engine']}/{r['id']}", **d} for r in all_rows for d in r.get("drift") or []]
    read_next = sorted(table("oeuvre_position_memo", {"read_next"}), key=lambda x: int(re.search(r"\d+", x.get("rank", "") or "9").group(0)) if re.search(r"\d+", x.get("rank", "") or "") else 9)
    return {"engine": "oeuvre_position", "job_id": job.get("id"), "phases": sorted(phases), "rows": len(all_rows), "conjectures": sum(int(r["conjecture"]) for r in all_rows),
            "verdicts": verdicts, "memo": _clean(memo_prose),
            "agendas": table("oeuvre_trajectory", {"agenda"}), "turns": table("oeuvre_trajectory", {"turn"}), "place": table("oeuvre_trajectory", {"place"}),
            "shifts": table("citation_shift", {"first_cited", "dropped", "carried", "anomaly", "unexamined"}),
            "retrospective": table("retrospective_reading", {"inheritance", "resolution", "interlocutor", "verdict"}),
            "prospective": table("prospective_reading", {"seed", "developed_into", "abandoned", "verdict"}),
            "rupture": table("epistemic_rupture", {"continuity", "break", "verdict", "test"}),
            "read_next": read_next, "open": table("oeuvre_position_memo", {"open"}), "placements": list(placements.values()), "vocabulary_drift": drift, "actions": actions_for(all_rows, registry, placements, run_id=str(job.get("id") or ""))}
