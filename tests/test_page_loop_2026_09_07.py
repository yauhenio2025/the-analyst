"""The page loop (Evgeny, 2026-09-07 09:45): the planner's rows become a plan walled by code (registry kinds, existing sections and
rows), the makers build every exhibit from the rows, the prose is matched to the plan's sections, the page composes, the reviewer's
verdicts parse in the registry's vocabulary and write back on the exhibits; a fake model runs the whole loop in a test."""
import json

from src.dossier.page_loop import compose_page, memo_document, parse_plan, parse_prose, parse_review, run_page_loop

OEUVRE = {"verdicts": {"position": "reorientation", "retrospective": "culmination", "prospective": "way_station", "rupture": "deepening", "place": "middle", "halves": "1972–1984 formation vs 1985–2025 codification", "warrant": "w"},
          "memo": "## Read backwards\n\nIt completes the critique (retrospective_reading/F19).",
          "agendas": [{"id": "F1", "dim": "agenda", "text": "The transition agenda", "span": "em:A/1976 … em:B/2007; 11 texts", "concepts": "social-property relations; market dependence", "anchor": "x", "doc": "before:em:A", "conjecture": False}],
          "turns": [{"id": "F7", "dim": "turn", "text": "From controversy to reconstruction", "at": "em:A/1977 → em:F/1985", "changed": "method", "anchor": "x", "doc": "before:em:A", "conjecture": False}],
          "place": [{"id": "F12", "dim": "place", "text": "the hinge", "position": "middle", "anchor": "x", "doc": "focal:em:F", "conjecture": False}],
          "shifts": [{"id": "F4", "dim": "unexamined", "text": "Meek is cited and not a Referee thinker", "cited": "Meek, Ronald", "kind": "person", "held": "unknown", "in_referee": "no", "used_for": "the four-stages theory", "anchor": "x", "doc": "focal:em:F", "conjecture": False}],
          "retrospective": [{"id": "F19", "dim": "verdict", "text": "a qualified culmination", "verdict": "culmination", "anchor": "x", "doc": "focal:em:F", "conjecture": False}],
          "prospective": [{"id": "F1", "dim": "seed", "text": "the two-model architecture", "what": "the two-model architecture", "developed_in": "em:B/2007", "anchor": "x", "doc": "focal:em:F", "conjecture": False}],
          "rupture": [{"id": "F1", "dim": "verdict", "text": "a deepening", "verdict": "deepening", "halves": "1972–1984 formation vs 1985–2025 codification", "anchor": "x", "doc": "focal:em:F", "conjecture": False},
                      {"id": "F2", "dim": "continuity", "text": "the object persists", "what": "object", "before": "em:A/1977", "after": "em:B/2007", "anchor": "x", "doc": "before:em:A", "conjecture": False},
                      {"id": "F7", "dim": "break", "text": "the method changes", "what": "method", "before": "comparison", "after": "reconstruction", "at_focal": "partly", "anchor": "x", "doc": "before:em:A", "conjecture": False}],
          "read_next": [{"id": "F2", "dim": "read_next", "text": "em:A/1977", "rank": "1", "why": "the road here", "held": "yes", "anchor": "x", "doc": "before:em:A", "conjecture": False}],
          "open": [{"id": "F9", "dim": "open", "text": "what Part II supplied", "decided_by": "finding it", "anchor": "x", "doc": "focal:em:F", "conjecture": False}]}
PACKET = {"author": {"id": "brenner-robert", "name": "Brenner, Robert"}, "focal": {"uid": "em:F", "year": "1985", "title": "Marx's First Model"}, "texts": [{"uid": "em:A", "year": "1976", "title": "Agrarian"}, {"uid": "em:F", "year": "1985", "title": "Marx's First Model"}, {"uid": "em:B", "year": "2007", "title": "Property and Progress"}]}

PLAN = """## The line

The reader gets the verdict first, then the shape of the oeuvre, then the break.

## Findings ledger
- [L1.F1] The answer in five words — dim: section — order: 1 — words: 120 — grasp: the joined verdict — from: oeuvre_position_memo/F9 — anchor: "It completes the critique" — doc: memo — confidence: high
- [L1.F2] The oeuvre on one line — dim: section — order: 2 — words: 260 — grasp: where 1985 sits among six agendas — from: oeuvre_trajectory/F1, oeuvre_trajectory/F7 — anchor: "The transition agenda" — doc: memo — confidence: high
- [L2.F1] The five verdict chips — dim: exhibit — kind: verdict-chips — section: L1.F1 — rows: epistemic_rupture/F1 — placement: before — aim: the answer before any paragraph — anchor: "It completes the critique" — doc: memo — confidence: high
- [L2.F2] The timeline — dim: exhibit — kind: oeuvre-timeline — section: L1.F2 — rows: oeuvre_trajectory/F1, oeuvre_trajectory/F7, oeuvre_trajectory/F99 — placement: before — aim: the agendas and the focal text at a glance — anchor: "The transition agenda" — doc: memo — confidence: high
- [L2.F3] A hologram — dim: exhibit — kind: hologram — section: L1.F2 — rows: oeuvre_trajectory/F1 — placement: after — aim: x — anchor: "The transition agenda" — doc: memo — confidence: low
- [L2.F4] A second timeline — dim: exhibit — kind: oeuvre-timeline — section: L1.F2 — rows: oeuvre_trajectory/F1 — placement: after — aim: x — anchor: "The transition agenda" — doc: memo — confidence: low
- [L3.F1] The full row tables — dim: cut — why: the ledger view carries them — kept_in: ledger — anchor: "It completes the critique" — doc: memo — confidence: medium
"""
PROSE = """## The answer in five words

Read whole, 1985 is a reorientation [oeuvre_position_memo/F9].

## The oeuvre on one line

The timeline shows six agendas; the focal text sits in the transition agenda's middle [oeuvre_trajectory/F1].

## Findings ledger
- [W1.F1] The answer in five words — dim: prose — words: 9 — cites: oeuvre_position_memo/F9 — grasp: the joined verdict — anchor: "It completes the critique" — doc: memo — confidence: high
- [W1.F2] The oeuvre on one line — dim: prose — words: 16 — cites: oeuvre_trajectory/F1 — grasp: where 1985 sits — anchor: "The transition agenda" — doc: memo — confidence: high
"""
REVIEW = """The page reads on the first pass; the timeline could carry the turn labels more plainly.

## Findings ledger
- [V1.F1] The chips — dim: verdict — element: L2.F1 — verdict: keep — reason: the answer is there first — fix: none — anchor: "SECTION: The answer in five words" — doc: page — confidence: high
- [V1.F2] The timeline — dim: verdict — element: L2.F2 — verdict: simplify — reason: the turn labels crowd — fix: keep three turns — anchor: "EXHIBIT oeuvre-timeline" — doc: page — confidence: medium
- [V2.F1] The answer in five words — dim: clarity — section: L1.F1 — first_pass: yes — why: one sentence — anchor: "SECTION: The answer in five words" — doc: page — confidence: high
"""


def test_the_plan_is_walled_by_code():
    from src.exhibits.registry import ExhibitRegistry, DEFINITIONS
    reg = ExhibitRegistry(DEFINITIONS, durable=False)
    memo = memo_document(OEUVRE)
    assert "[oeuvre_trajectory/F1]" in memo and "THE VERDICTS" in memo and "position: reorientation" in memo
    import re
    ids = set(re.findall(r"\b([a-z_]+/(?:[A-Z]\d\.)?F\d+)\b", memo))
    plan = parse_plan(PLAN, {e.key for e in reg.list()}, ids)
    assert [s["heading"] for s in plan["sections"]] == ["The answer in five words", "The oeuvre on one line"] and plan["sections"][1]["words"] == 260
    assert [e["kind"] for e in plan["exhibits"]] == ["verdict-chips", "oeuvre-timeline"]           # the hologram and the duplicate timeline are rejected
    assert {r["id"] for r in plan["rejected"]} == {"L2.F3", "L2.F4"}
    assert plan["exhibits"][1]["rows"] == ["oeuvre_trajectory/F1", "oeuvre_trajectory/F7"] and plan["exhibits"][1]["missing_rows"] == ["oeuvre_trajectory/F99"]
    assert plan["cuts"][0]["kept_in"] == "ledger"


def test_prose_review_and_the_composed_page():
    from src.exhibits.registry import ExhibitRegistry, DEFINITIONS
    reg = ExhibitRegistry(DEFINITIONS, durable=False)
    plan = parse_plan(PLAN, {e.key for e in reg.list()}, {"oeuvre_trajectory/F1", "oeuvre_trajectory/F7", "oeuvre_position_memo/F9", "epistemic_rupture/F1"})
    prose = parse_prose(PROSE, plan["sections"])
    assert set(prose) == {"L1.F1", "L1.F2"} and prose["L1.F2"].startswith("The timeline shows")
    review = parse_review(REVIEW)
    assert [(v["element"], v["verdict"]) for v in review["verdicts"]] == [("L2.F1", "keep"), ("L2.F2", "simplify")] and review["clarity"][0]["first_pass"] == "yes"
    from src.exhibits.makers import make
    made = {e["id"]: make(e["kind"], OEUVRE, rows=e["rows"], packet=PACKET) for e in plan["exhibits"]}
    html, desc = compose_page("T", "S", plan, prose, made, review, 1)
    assert "<h2>The answer in five words</h2>" in html and "class=\"chips\"" in html and "<svg" in html and "[oeuvre_position_memo/F9]" in html
    assert html.index("chips") < html.index("<p>Read whole") and "The reviewer's verdicts" in html and "Left out of the page" in html
    assert "[L1.F1] SECTION" in desc and "[L2.F2] EXHIBIT oeuvre-timeline (before)" in desc and "PROSE (15 words)" in desc


def test_the_loop_runs_with_a_fake_model_and_writes_verdicts_back(tmp_path):
    from src.exhibits.registry import ExhibitRegistry, DEFINITIONS
    import shutil
    for f in DEFINITIONS.glob("*.json"):
        shutil.copy(f, tmp_path / f.name)
    reg = ExhibitRegistry(tmp_path, durable=False)
    calls = []

    def fake(system, user, *, model_hint, label, **kw):
        calls.append(label)
        if "page_planner" in label:
            return {"content": PLAN, "model_used": model_hint, "input_tokens": 3000, "output_tokens": 500}
        if "page_prose" in label:
            return {"content": PROSE, "model_used": model_hint, "input_tokens": 3000, "output_tokens": 300}
        return {"content": REVIEW, "model_used": model_hint, "input_tokens": 2000, "output_tokens": 200}

    rec = run_page_loop("d-page", OEUVRE, PACKET, audience="researcher", rounds=2, call_fn=fake, exhibit_registry=reg)
    assert len(rec["rounds"]) == 2 and len(calls) == 6 and rec["cost_usd"] > 0
    r1 = rec["rounds"][0]
    assert [e["kind"] for e in r1["plan"]["exhibits"]] == ["verdict-chips", "oeuvre-timeline"] and r1["review"]["verdicts"][1]["verdict"] == "simplify"
    assert rec["final_html"].startswith("<!doctype html>") and "The oeuvre on one line" in rec["final_html"]
    assert [u.verdict for u in reg.get("oeuvre-timeline").evidence] == ["simplify", "simplify"] and reg.get("verdict-chips").evidence[0].page == "d-page/round1"
