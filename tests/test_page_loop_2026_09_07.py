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
    assert "<h2 title='L1.F1'>The answer in five words</h2>" in html and "class=\"chips\"" in html and "<svg" in html and "[oeuvre_position_memo/F9]" in html
    assert html.index("chips") < html.index("<p>Read whole") and "The reviewer's verdicts" in html and "Left out of the page" in html
    assert "[L1.F1] SECTION" in desc and "[L2.F2] EXHIBIT oeuvre-timeline (folded, shown as a titled line the reader opens)" in desc and "PROSE (15 words)" in desc


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

    before = {k: len(reg.get(k).evidence) for k in ("oeuvre-timeline", "verdict-chips")}     # the seeds may carry real runs' verdicts already
    rec = run_page_loop("d-page", OEUVRE, PACKET, audience="researcher", rounds=2, call_fn=fake, exhibit_registry=reg)
    assert len(rec["rounds"]) == 2 and len(calls) == 6 and rec["cost_usd"] > 0
    r1 = rec["rounds"][0]
    assert [e["kind"] for e in r1["plan"]["exhibits"]] == ["verdict-chips", "oeuvre-timeline"] and r1["review"]["verdicts"][1]["verdict"] == "simplify"
    assert rec["final_html"].startswith("<!doctype html>") and "The oeuvre on one line" in rec["final_html"]
    assert [x.verdict for x in reg.get("oeuvre-timeline").evidence][before["oeuvre-timeline"]:] == ["simplify", "simplify"] and reg.get("verdict-chips").evidence[before["verdict-chips"]].page == "d-page/round1"
    assert rec["rounds"][0]["plan"]["exhibits"][1]["placement"] == "folded"        # the timeline was planned 'before'; a wide exhibit never leads: it folds


def test_the_text_is_the_main_dish_wide_exhibits_fold_and_nothing_but_chips_stands_before_the_first_section():
    """The owner (2026-09-07 11:45): the timeline 'cannot be the main dish'; exhibits at the top 'hide the rest of the essay'."""
    plan = {"line": "", "sections": [{"id": "L1.F1", "heading": "The place", "grasp": "g", "words": 200}, {"id": "L1.F2", "heading": "What changes", "grasp": "g", "words": 200}],
            "exhibits": [{"id": "L2.F1", "kind": "oeuvre-timeline", "section": "L1.F1", "rows": [], "placement": "before", "aim": "the span"},
                         {"id": "L2.F2", "kind": "verdict-chips", "section": "L1.F1", "rows": [], "placement": "before", "aim": "the verdicts"},
                         {"id": "L2.F3", "kind": "pull-quote", "section": "L1.F2", "rows": [], "placement": "before", "aim": "the sentence"},
                         {"id": "L2.F4", "kind": "shift-table", "section": "L1.F2", "rows": [], "placement": "beside", "aim": "the shifts"}], "cuts": []}
    made = {"L2.F1": {"title": "Brenner’s texts 1972–2025 on one line", "html": "<svg/>", "description": "timeline"}, "L2.F2": {"html": "<div class='chips'>c</div>", "description": "chips"},
            "L2.F3": {"html": "<blockquote class='pull'>q</blockquote>", "description": "quote"}, "L2.F4": {"html": "<table class='shift'></table>", "description": "table"}}
    html, desc = compose_page("T", "S", plan, {"L1.F1": "First paragraph.", "L1.F2": "Second."}, made, None, 1)
    by_id = {e["id"]: e["placement"] for e in plan["exhibits"]}
    assert by_id == {"L2.F1": "folded", "L2.F2": "before", "L2.F3": "after", "L2.F4": "folded"}
    assert html.index("<div class='chips'>") < html.index("First paragraph.") < html.index("<details class='exhibit folded' id='L2.F1'")
    assert "<summary>Brenner’s texts 1972–2025 on one line<span class='hint'>open</span></summary>" in html
    assert html.index("Second.") < html.index("<blockquote class='pull'>")
    assert "shown as a titled line the reader opens" in desc


def test_a_page_loop_survives_a_restart_and_resumes_from_its_last_round(tmp_path, monkeypatch):
    """The Reporter's deploy gate restarted the API mid-loop and the loop vanished (2026-09-07 13:03): the status and every finished
    round now live in the blob store; a stored 'running' with no thread here reads as interrupted; resume continues from the next round."""
    import time as _t
    from src.exhibits.registry import ExhibitRegistry, DEFINITIONS
    import shutil
    import src.dossier.page_loop as pl
    for f in DEFINITIONS.glob("*.json"):
        shutil.copy(f, tmp_path / f.name)
    reg = ExhibitRegistry(tmp_path, durable=False)
    store: dict[str, bytes] = {}
    monkeypatch.setattr(pl, "_put", lambda key, ct, data: store.__setitem__(key, data))
    monkeypatch.setattr(pl, "_get", lambda key: store.get(key))
    calls = []
    def fake(system, user, *, model_hint, label, **kw):
        calls.append(label)
        if "page_planner" in label:
            return {"content": PLAN, "model_used": model_hint, "input_tokens": 3000, "output_tokens": 500}
        if "page_prose" in label:
            return {"content": PROSE, "model_used": model_hint, "input_tokens": 3000, "output_tokens": 300}
        return {"content": REVIEW, "model_used": model_hint, "input_tokens": 2000, "output_tokens": 200}
    # round one runs and is saved; then "the API restarts": the thread is gone, the stored status still says running
    pl._running.clear()
    st = pl.start_page_loop("d-durable", OEUVRE, PACKET, audience="researcher", rounds=1, call_fn=fake, exhibit_registry=reg)
    for _ in range(200):
        if st["status"] != "running":
            break
        _t.sleep(0.05)
    assert st["status"] == "done" and st["rounds_done"] == 1 and len(calls) == 3
    assert json.loads(store["page:d-durable:status"])["status"] == "done" and "page:d-durable:round1.html" in store and "page:d-durable:record" in store
    store["page:d-durable:status"] = json.dumps({**st, "status": "running"}).encode()      # what a killed loop leaves behind
    pl._running.clear()
    assert pl.page_status("d-durable")["status"] == "interrupted" and pl.active_page_loops() == []
    # resume: the prior round is kept, only round two runs
    calls.clear()
    st2 = pl.start_page_loop("d-durable", OEUVRE, PACKET, resume=True, audience="researcher", rounds=2, call_fn=fake, exhibit_registry=reg)
    assert st2["resumed"] is True and st2["rounds_done"] == 1
    for _ in range(200):
        if st2["status"] != "running":
            break
        _t.sleep(0.05)
    assert st2["status"] == "done" and st2["rounds_done"] == 2 and len(calls) == 3
    rec = json.loads(store["page:d-durable:record"])
    assert [r["round"] for r in rec["rounds"]] == [1, 2] and rec["final_html"] if "final_html" in rec else True
    assert store["page:d-durable:html"].startswith(b"<!doctype html>")
    # while a loop runs it is active work for the jobs listing
    pl._running["d-x"] = {"status": "running", "rounds_done": 0, "started": 1.0}
    assert pl.active_page_loops() == [{"id": "page:d-x", "kind": "page_loop", "job_id": "d-x", "status": "composing", "step": "page", "rounds_done": 0, "started": 1.0}]
    pl._running.clear()


def test_the_readers_page_carries_no_ids_and_the_last_rounds_drop_is_applied():
    """The owner (2026-09-07 16:39) on run 3's page: route cards showed bare uids, the loop's notes sat on the page, captions carried ids,
    and a 'drop' verdict from the last round was printed rather than applied."""
    from src.exhibits.makers import make
    plan = {"line": "", "sections": [{"id": "L1.F1", "heading": "What to read next", "grasp": "g", "words": 100}],
            "exhibits": [{"id": "L2.F5", "kind": "reading-route-cards", "section": "L1.F1", "rows": [], "placement": "after", "aim": "the four next texts, ranked"},
                         {"id": "L2.F6", "kind": "shift-table", "section": "L1.F1", "rows": [], "placement": "after", "aim": "the shifts"},
                         {"id": "L2.F7", "kind": "verdict-chips", "section": "L1.F1", "rows": [], "placement": "before", "aim": "the verdicts"}], "cuts": [{"what": "the idea map", "why": "no figure"}]}
    made = {e["id"]: make(e["kind"], OEUVRE, rows=e["rows"], packet=PACKET) for e in plan["exhibits"]}
    cards = made["L2.F5"]["html"]
    assert "em:" not in cards and "in the library" in cards and "title=\"[oeuvre_position_memo/" in cards     # named by year and title; the id on hover only
    review = {"verdicts": [{"element": "L2.F6", "verdict": "drop", "reason": "repeats the prose"}, {"element": "L2.F5", "verdict": "move", "reason": "hides the text"}], "clarity": []}
    html, desc = compose_page("T", "S", plan, {"L1.F1": "Read these."}, made, review, 2)
    assert [e["id"] for e in plan["exhibits"]] == ["L2.F5", "L2.F7"] and plan["exhibits"][0]["placement"] == "folded"      # drop applied, move folds
    assert "<figcaption class='cap'>" not in html.split("<details class='about'>")[0] or "[L2." not in html.split("<details class='about'>")[0]   # no plan id on the face
    assert "<details class='about'><summary>How this page was made</summary>" in html and "Left out of the page" in html.split("<details class='about'>")[1]


def test_recompose_rebuilds_the_stored_page_without_a_model(monkeypatch):
    import src.dossier.page_loop as pl
    store = {}
    monkeypatch.setattr(pl, "_put", lambda key, ct, data: store.__setitem__(key, data)); monkeypatch.setattr(pl, "_get", lambda key: store.get(key))
    plan = {"line": "", "sections": [{"id": "L1.F1", "heading": "Next", "grasp": "g", "words": 100}], "exhibits": [{"id": "L2.F5", "kind": "reading-route-cards", "section": "L1.F1", "rows": [], "placement": "after", "aim": "the next texts"}], "cuts": []}
    store["page:d-rc:record"] = json.dumps({"job_id": "d-rc", "title": "T", "audience": "researcher", "rounds": [{"round": 1, "plan": plan, "prose": {"L1.F1": "Read these."}, "review": None}]}).encode()
    out = pl.recompose_page("d-rc", OEUVRE, PACKET)
    assert out["round"] == 1 and out["exhibits"] == [("reading-route-cards", "after")] and store["page:d-rc:html"].startswith(b"<!doctype html>") and b"em:" not in store["page:d-rc:html"].split(b"<details class='about'>")[0]
    assert pl.recompose_page("d-none", OEUVRE, PACKET) is None


def test_the_reading_alone_can_be_dropped_into_a_host_column():
    """The owner (2026-09-07 22:36) on the oeuvre page's centre: 'too much text, not properly thought through… format better'.
    The composed page's reading — headings, grasp lines, prose, folded exhibits — without the page's own furniture."""
    from src.dossier.page_loop import page_body
    plan = {"line": "", "sections": [{"id": "L1.F1", "heading": "The verdict", "grasp": "a way station.", "words": 100}], "exhibits": [
        {"id": "L2.F1", "kind": "verdict-chips", "section": "L1.F1", "rows": [], "placement": "before", "aim": "the verdicts"},
        {"id": "L2.F2", "kind": "shift-table", "section": "L1.F1", "rows": [], "placement": "folded", "aim": "the shifts"}], "cuts": [{"what": "x", "why": "y"}]}
    made = {"L2.F1": {"html": "<div class=\"chips\">c</div>", "description": "chips"}, "L2.F2": {"title": "The citation shifts", "html": "<table class='shift'></table>", "description": "table"}}
    html, _ = compose_page("T", "S", plan, {"L1.F1": "The essay [oeuvre_trajectory/F1]."}, made, {"verdicts": [], "clarity": []}, 2)
    b = page_body(html)
    assert "<h1>" not in b and "class='sub'" not in b and "How this page was made" not in b and 'class="chips"' not in b
    assert "<h2 title='L1.F1'>The verdict</h2>" in b and "a way station</p>" in b and "The essay" in b
    assert "<details class='exhibit folded'" in b and "The citation shifts" in b        # the folded exhibits travel
    assert "[oeuvre_trajectory/F1]" not in b and b.startswith("<style>") and "<div class='reading'>" in b


def test_the_reading_as_records_for_a_host_page(monkeypatch):
    """The Stacks (2026-09-07 23:00): 'JSON, please — with JSON the page owns the type, the spacing and the folds'."""
    import src.dossier.page_loop as pl
    plan = {"sections": [{"id": "L1.F1", "heading": "The verdict", "grasp": "a way station.", "words": 120},
                          {"id": "L1.F2", "heading": "What it inherits", "grasp": "an old conclusion by a new route", "words": 250}],
            "exhibits": [{"id": "L2.F1", "kind": "verdict-chips", "section": "L1.F1", "placement": "after", "aim": "the five words"},
                          {"id": "L2.F2", "kind": "two-halves", "section": "L1.F2", "placement": "after", "aim": "what persists"},
                          {"id": "L2.F3", "kind": "shift-table", "section": "L1.F2", "placement": "folded", "aim": "the shifts"}],
            "cuts": [{"what": "the idea map", "why": "no figure exists"}]}
    rec = {"job_id": "d-j", "title": "T", "audience": "researcher", "rounds": [{"round": 2, "plan": plan,
            "prose": {"L1.F1": "It is a way station [oeuvre_trajectory/F12].\n\nThe verdict holds [epistemic_rupture/F1].", "L1.F2": "It rereads 1977."},
            "exhibits": {"L2.F1": {"description": "five chips"}, "L2.F2": {"title": "Before and after the paper", "description": "two columns"}, "L2.F3": {"title": "The citation shifts", "description": "30 rows"}},
            "review": {"verdicts": [{"element": "L2.F3", "verdict": "drop", "reason": "repeats the prose"}], "clarity": []}}]}
    monkeypatch.setattr(pl, "_get", lambda key: json.dumps(rec).encode() if key == "page:d-j:record" else None)
    d = pl.page_sections("d-j")
    assert d["round"] == 2 and [s["heading"] for s in d["sections"]] == ["The verdict", "What it inherits"]
    first = d["sections"][0]
    assert first["grasp"] == "a way station" and first["paragraphs"] == ["It is a way station.", "The verdict holds."] and first["cites"] == ["epistemic_rupture/F1", "oeuvre_trajectory/F12"]
    assert first["exhibits"][0]["kind"] == "verdict-chips" and first["exhibits"][0]["svg_url"] is None
    second = d["sections"][1]
    assert [e["kind"] for e in second["exhibits"]] == ["two-halves"]                 # the dropped exhibit is gone
    assert second["exhibits"][0]["title"] == "Before and after the paper" and second["exhibits"][0]["svg_url"].endswith("/exhibits/two-halves.svg")
    assert d["cuts"][0]["what"] == "the idea map" and pl.page_sections("nothing") is None


def test_the_json_reading_route_is_wired(monkeypatch):
    """It served 500 on the live desk: JSONResponse was used in the route module without being imported (the Stacks, 2026-09-08)."""
    import src.api.routes.dossier as d
    assert d.JSONResponse is not None
    import src.dossier.page_loop as pl
    rec = {"job_id": "d-w", "title": "T", "audience": "researcher", "rounds": [{"round": 1, "plan": {"sections": [{"id": "L1.F1", "heading": "H", "grasp": "g", "words": 10}], "exhibits": [], "cuts": []}, "prose": {"L1.F1": "P."}, "exhibits": {}, "review": None}]}
    monkeypatch.setattr(pl, "_get", lambda key: json.dumps(rec).encode() if key == "page:d-w:record" else None)
    from fastapi.testclient import TestClient
    import src.api.main as m
    c = TestClient(m.app)
    r = c.get("/v1/dossier/jobs/d-w/page?body=json")
    assert r.status_code == 200 and r.json()["sections"][0]["heading"] == "H"
    assert c.get("/v1/dossier/jobs/d-none/page?body=json").status_code == 404
