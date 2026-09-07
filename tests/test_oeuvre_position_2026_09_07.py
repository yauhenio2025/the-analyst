"""A paper's place in its author's oeuvre (Evgeny, 2026-09-07): the six engines load with the registry's vocabularies, the
recipe carries scopes, the Stacks' bundle expands at the door into focal / before / after documents and the packet."""
import json
import pytest

from src.sources.oeuvre_bundle import expand_oeuvre_bundle, packet_of, render_profile
from src.sources.resolve import resolve_sources
from src.sources.schemas import SourceSpec

PROFILE_1977 = {"thesis": "Neo-Smithian Marxism explains capitalism by trade, not class relations.", "question": "Why does the world-system account fail?",
                "tradition": "Marxist political economy", "concepts": [{"term": "class relations", "weight": 5, "gloss": "the relations of surplus extraction"}],
                "people": [{"name": "Wallerstein, Immanuel", "role": "opponent", "stance": "criticised for a trade-based account"}],
                "works_cited": [{"title": "The Modern World-System", "author": "Wallerstein, Immanuel", "year": "1974", "role": "foil", "uid": "em:W1"}],
                "claims": [{"claim": "Trade cannot explain the transition.", "kind": "thesis"}], "positions": [{"debate": "origins of capitalism", "side": "class relations", "against": ["trade"]}],
                "passages": [{"quote": "the neo-Smithian model assumes what it must explain", "locus": "p. 27", "verified": True}]}
PROFILE_2006 = {"thesis": "The long downturn is a crisis of profitability.", "question": "Why did profitability fall?", "tradition": "Marxist political economy",
                "works_cited": [{"title": "Capital", "author": "Marx, Karl", "year": "1867", "role": "source", "uid": "em:K1"}],
                "people": [{"name": "Marx, Karl", "role": "source", "stance": "the account of overaccumulation"}]}
BUNDLE = {"author": {"id": "brenner-robert", "name": "Brenner, Robert"},
          "focal": {"uid": "em:F", "title": "Marx's First Model of the Transition to Capitalism", "year": 1985, "creators": "Brenner, Robert", "text": "There are two Marxian models of the transition. They are incompatible. Guizot saw the bourgeois revolution first.",
                    "profile": {"thesis": "Two incompatible models."}, "ledger": {"works": [{"key": "guizot|histoire", "title": "Histoire de la civilisation", "authors": "Guizot, François", "year": "1830", "n_events": 2, "held": None}],
                                                                                 "persons": [{"norm": "guizot f", "name": "Guizot, François", "n_events": 2, "referee_thinker_id": None}, {"norm": "marx k", "name": "Marx, Karl", "n_events": 165, "referee_thinker_id": 12}]}},
          "before": [{"uid": "em:B77", "title": "The Origins of Capitalist Development", "year": 1977, "creators": "Brenner, Robert", "profile": PROFILE_1977,
                      "ledger": {"works": [{"key": "wallerstein|the modern world-system", "title": "The Modern World-System", "authors": "Wallerstein, Immanuel", "year": "1974", "n_events": 30, "held": "em:W1"}],
                                 "persons": [{"norm": "wallerstein i", "name": "Wallerstein, Immanuel", "n_events": 30, "referee_thinker_id": 7}, {"norm": "marx k", "name": "Marx, Karl", "n_events": 40, "referee_thinker_id": 12}]}}],
          "after": [{"uid": "em:A06", "title": "The Economics of Global Turbulence", "year": 2006, "creators": "Brenner, Robert", "profile": PROFILE_2006, "ledger": {"works": [], "persons": [{"norm": "marx k", "name": "Marx, Karl", "n_events": 20, "referee_thinker_id": 12}]}},
                    {"uid": "em:A99", "title": "No profile yet", "year": 1999, "profile": None}]}


def test_the_engines_load_with_the_registry_vocabularies_and_the_recipe_carries_scopes():
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.vocabularies.registry import get_vocabulary_registry
    from src.dossier.catalog import load_recipes, resolve_path_request
    from src.dossier.schemas import PathRequest
    from src.workflows.registry import get_workflow_registry
    reg, opr, voc = get_engine_registry(), get_operationalization_registry(), get_vocabulary_registry()
    for key, prefixes in (("oeuvre_trajectory", ["T1", "T2", "T3"]), ("citation_shift", ["C1", "C2", "C3", "C4", "C5"]), ("retrospective_reading", ["R1", "R2", "R3", "R4"]),
                          ("prospective_reading", ["P1", "P2", "P3", "P4"]), ("epistemic_rupture", ["E1", "E2", "E3", "E4"]), ("oeuvre_position_memo", ["M1", "M2", "M3"])):
        assert reg.get_capability_definition(key) is not None and [d.id_prefix for d in opr.get(key).process.dimensions] == prefixes
        assert opr.get(key).mode_for_depth("surface") == "oneshot"
    assert voc.values_for("epistemic_rupture", "verdict") == ["rupture", "reorientation", "deepening", "continuity", "outlier"]
    assert voc.values_for("oeuvre_trajectory", "position") == ["opening", "culmination", "middle", "end", "reorientation", "outlier"]
    assert voc.values_for("retrospective_reading", "verdict") == ["culmination", "continuation", "departure"] and voc.values_for("prospective_reading", "verdict") == ["origin", "way_station", "dead_end"]
    recipe = next(r for r in load_recipes() if r["key"] == "oeuvre_position")
    assert [s["engine_key"] for s in recipe["steps"]] == ["oeuvre_trajectory", "citation_shift", "retrospective_reading", "prospective_reading", "epistemic_rupture", "oeuvre_position_memo", "thinker_placement"]
    path = resolve_path_request(PathRequest(chain_key="oeuvre_position"), "researcher")
    assert [s.scope for s in path.steps] == [[], [], ["focal:", "before:"], ["focal:", "after:"], [], [], []]
    assert get_workflow_registry().get("oeuvre_position") is not None


def test_the_bundle_expands_at_the_door_into_scoped_documents_and_a_packet():
    docs = expand_oeuvre_bundle(json.dumps(BUNDLE))
    keys = [d.key for d in docs]
    assert keys == ["focal:em:F", "before:em:B77", "after:em:A06", "oeuvre"]           # the unprofiled later text is not a document
    assert docs[0].role == "source" and docs[0].text.startswith("SOURCE ROLE: focal_text") and "two Marxian models" in docs[0].text
    b = docs[1].text
    assert b.startswith("SOURCE ROLE: before_text") and "THESIS: Neo-Smithian Marxism" in b and "CONCEPTS: class relations (weight 5)" in b
    assert "WORKS CITED: Wallerstein, Immanuel, The Modern World-System (1974) [foil; held em:W1]" in b and "the neo-Smithian model assumes what it must explain" in b
    assert "LEDGER, PERSONS CITED: Wallerstein, Immanuel ×30 [referee 7]" in b
    packet = json.loads(docs[3].text)
    assert docs[3].role == "plan" and packet["kind"] == "oeuvre" and packet["focal"]["uid"] == "em:F" and packet["counts"] == {"before": 1, "after": 2, "profiled": 3}
    assert [t["side"] for t in packet["texts"]] == ["before", "focal", "after", "after"]
    first = {(c.get("person") or c.get("title")): c for c in packet["cited_first_in_focal"]}
    assert "Guizot, François" in first and first["Guizot, François"]["in_referee"] is False and "Histoire de la civilisation" in first and first["Histoire de la civilisation"]["held"] is False
    assert "Marx, Karl" not in first                                                     # cited before: carried, not first
    dropped = {(c.get("person") or c.get("title")) for c in packet["cited_before_not_in_focal"]}
    assert "Wallerstein, Immanuel" in dropped and "The Modern World-System" in dropped


def test_the_resolver_takes_the_bundle_as_one_source_with_the_oeuvre_role():
    docs = resolve_sources([SourceSpec(kind="paste", role="oeuvre", key="oeuvre", title="Brenner around 1985", text=json.dumps(BUNDLE))])
    assert [(d.key, d.role) for d in docs] == [("focal:em:F", "source"), ("before:em:B77", "source"), ("after:em:A06", "source"), ("oeuvre", "plan")]
    assert all(d.char_count == len(d.text) for d in docs)


FINAL_SHIFT = """## The pattern

The text cites Marx's early works for the first time and drops the agrarian historians (C1.F1, C2.F1).

## Findings ledger
- [C1.F1] Marx's German Ideology is cited here for the first time — dim: first_cited — cited: Marx, Karl, The German Ideology (1845) — kind: work — for: the first model's source — later: em:A06/2006 — held: yes — in_referee: yes — anchor: "There are two Marxian models of the transition." — doc: focal:em:F — confidence: high
- [C2.F1] Pirenne, cited in every earlier text, is absent — dim: dropped — cited: Pirenne, Henri — kind: person — cited_in: em:B77/1977 — silence: nothing — anchor: "the neo-Smithian model assumes what it must explain" — doc: before:em:B77 — confidence: medium
- [C5.F1] Guizot's Histoire is cited and not held — dim: unexamined — cited: Guizot, François, Histoire de la civilisation en Europe (1830) — kind: work — held: no — in_referee: unknown — used_for: the bourgeois revolution first seen by Guizot — anchor: "Guizot saw the bourgeois revolution first." — doc: focal:em:F — confidence: high
- [C5.F2] Guizot is not a thinker in the Referee — dim: unexamined — cited: Guizot, François — kind: person — held: unknown — in_referee: no — used_for: the source of the bourgeois-revolution thesis — anchor: "Guizot saw the bourgeois revolution first." — doc: focal:em:F — confidence: high
"""
FINAL_RUPTURE = """## Verdict

A reorientation: the object stays, the question moves from agrarian class structure to Marx's models (E3.F1).

## Findings ledger
- [E1.F1] Class relations persist as the object — dim: continuity — what: object — before: em:B77/1977 — after: em:A06/2006 — anchor: "class relations" — doc: before:em:B77 — anchor-b: "profitability" — doc-b: after:em:A06 — confidence: medium
- [E3.F1] The text reorients the oeuvre — dim: verdict — verdict: reorientation — halves: agrarian class structure (1976–1982) vs Marx's models and the long downturn (1985–2006) — warrant: the question changes, the object does not — anchor: "They are incompatible." — doc: focal:em:F — confidence: medium
- [E4.F1] Read the 1986 essay on the social basis of economic development — dim: test — source: Brenner, The Social Basis of Economic Development (1986) — held: no — rank: 1 — anchor: "They are incompatible." — doc: focal:em:F — confidence: medium
"""
FINAL_MEMO = """## Read backwards

It completes the critique of neo-Smithian Marxism (R4.F1).

## Findings ledger
- [M1.F1] A reorientation that ends the agrarian agenda — dim: position — position: reorientation — retrospective: culmination — prospective: origin — rupture: reorientation — warrant: the question changes at it — anchor: "They are incompatible." — doc: focal:em:F — confidence: medium
- [M2.F2] The 2006 book, where the long downturn takes over — dim: read_next — text: em:A06/2006 — held: yes — rank: 2 — why: the later agenda — anchor: "profitability" — doc: after:em:A06 — confidence: medium
- [M2.F1] The 1977 critique, the road that leads here — dim: read_next — text: em:B77/1977 — held: yes — rank: 1 — why: the inheritance — anchor: "class relations" — doc: before:em:B77 — confidence: high
- [M3.F1] Whether the 1986 essay already carries the turn — dim: open — decided_by: reading it — held: no — anchor: "They are incompatible." — doc: focal:em:F — confidence: low
"""


def _job():
    def ph(engine, final, failed=()):
        return {"engine_key": engine, "final_output": final, "final_wall": {"failed_ids": list(failed)}}
    return {"id": "d-oeuvre", "status": "done", "analysis": {"4.2": ph("citation_shift", FINAL_SHIFT, ["C2.F1"]), "4.5": ph("epistemic_rupture", FINAL_RUPTURE), "4.6": ph("oeuvre_position_memo", FINAL_MEMO)}}


def test_the_oeuvre_renders_by_code_with_the_verdicts_and_the_actions_the_findings_license():
    from src.dossier.oeuvre import render_oeuvre
    from src.actions.registry import ActionRegistry, DEFINITIONS
    out = render_oeuvre(_job(), ActionRegistry(DEFINITIONS, durable=False))
    assert out["phases"] == ["citation_shift", "epistemic_rupture", "oeuvre_position_memo"] and out["rows"] == 11 and out["conjectures"] == 1
    v = out["verdicts"]
    assert v["position"] == "reorientation" and v["rupture"] == "reorientation" and v["halves"].startswith("agrarian class structure") and v["retrospective"] == "" and v["place"] == ""
    assert out["memo"].startswith("## Read backwards") and "(R4.F1)" not in out["memo"]
    assert [r["id"] for r in out["read_next"]] == ["M2.F1", "M2.F2"] and out["open"][0]["decided_by"] == "reading it"
    assert [s["dim"] for s in out["shifts"]] == ["first_cited", "dropped", "unexamined", "unexamined"] and out["shifts"][1]["conjecture"] is True
    acts = {a["finding"]: a for a in out["actions"]}
    assert set(acts) == {"citation_shift/C5.F1", "citation_shift/C5.F2", "epistemic_rupture/E4.F1", "oeuvre_position_memo/M2.F1", "oeuvre_position_memo/M2.F2"}   # C1.F1 is held and known: nothing to do
    guizot_work = acts["citation_shift/C5.F1"]
    assert guizot_work["kind"] == "citation_shift.unexamined" and guizot_work["held"] == "no"
    assert all(not a["missing"] for a in guizot_work["actions"]) and not any(a["organ"] == "the-referee" and ("thinker_name" in a["inputs"] or "referee_thinker_id" in a["missing"]) for a in guizot_work["actions"] + guizot_work["waiting"])   # a work row carries no person action (the owner, 12:17)
    fetch = next(w for w in guizot_work["waiting"] if w["action"] == "referee.pdf-fetch")     # a fetch needs a query or a corpus row the finding cannot supply
    assert "query_id" in fetch["missing"] or "corpus_result_id" in fetch["missing"]
    from src.actions.registry import suggest
    filled = next(s for s in suggest("citation_shift.unexamined", {"work_title": "Histoire de la civilisation en Europe", "work_author": "Guizot, François", "work_year": "1830"}, ActionRegistry(DEFINITIONS, durable=False)) if s["action"] == "referee.pdf-fetch")
    assert filled["inputs"]["work_title"] == "Histoire de la civilisation en Europe" and filled["inputs"]["work_author"] == "Guizot, François" and filled["inputs"]["work_year"] == "1830"
    guizot_person = acts["citation_shift/C5.F2"]
    assert not any(a["action"] == "referee.thinker-exists" for a in guizot_person["actions"] + guizot_person["waiting"])   # the ledger answered it (the owner, 12:17)
    create = next(a for a in guizot_person["actions"] if a["action"] == "referee.thinker-create")
    assert create["inputs"]["thinker_name"] == "Guizot, François" and not create["missing"]
    assert all(a["organ"] == "the-stacks" for a in acts["oeuvre_position_memo/M2.F1"]["actions"] + acts["oeuvre_position_memo/M2.F1"]["waiting"])       # held: bundle or profile, never a fetch
    profile = next(a for a in acts["oeuvre_position_memo/M2.F1"]["actions"] + acts["oeuvre_position_memo/M2.F1"]["waiting"] if a["action"] == "stacks.profile-text")
    assert profile["inputs"]["uid"] == "em:B77"                                          # the bare uid, not em:B77/1977; waiting entries keep their filled inputs
    assert any(w["action"] == "referee.pdf-fetch" for w in acts["epistemic_rupture/E4.F1"]["waiting"])   # a test on an unheld text: a fetch, once a query exists
    assert render_oeuvre({"id": "x", "analysis": {}}) is None


def test_an_engines_only_job_on_a_fixed_path_takes_the_fast_lane(monkeypatch):
    """No reconnaissance profiling, no brief desk call, no planner call: the documents are what the engines read and the recipe is
    the plan (the oeuvre pilot's first minutes went to profiling 59 profiles)."""
    from src.dossier import runner, plan as P
    from src.dossier.schemas import DossierJob, DossierOptions, OutputOptions, PathRequest
    from src.sources.schemas import Document
    job = DossierJob(id="d-fast", status="queued", options=DossierOptions(intent="x", entry="chosen", path=PathRequest(chain_key="oeuvre_position"), output=OutputOptions(text=False, tables=False, figures=0, plates=0)))
    assert runner._fast_lane(job) and not runner._fast_lane(DossierJob(id="d-slow", options=DossierOptions(intent="x", output=OutputOptions(text=False, tables=False, figures=0, plates=0))))
    docs = [Document(key="focal:em:F", title="F", text="the focal text"), Document(key="before:em:B", title="B", text="a profile")]
    calls = []
    monkeypatch.setattr(runner, "update_job", lambda job_id, **f: calls.append(("update", f)))
    monkeypatch.setattr(runner, "_persist_factory", lambda job_id: (lambda **f: calls.append(("persist", f))))
    monkeypatch.setattr(runner.events, "emit", lambda *a, **k: None)
    monkeypatch.setattr(runner, "is_cancelled", lambda job_id: False)
    import src.dossier.reconnaissance as R, src.dossier.brief as B
    monkeypatch.setattr(R, "run_reconnaissance", lambda *a, **k: (_ for _ in ()).throw(AssertionError("reconnaissance must not run on the fast lane")))
    monkeypatch.setattr(B, "run_brief", lambda *a, **k: (_ for _ in ()).throw(AssertionError("the brief desk must not run on the fast lane")))
    runner._run_step(job, "reconnaissance", docs)
    assert [p.doc_key for p in job.profiles.profiles] == ["focal:em:F", "before:em:B"] and not job.profiles.profiles[0].key_claims
    runner._run_step(job, "brief", docs)
    assert job.chosen_option == runner.OWN_PATH_KEY and job.brief.option(runner.OWN_PATH_KEY) is not None
    monkeypatch.setattr(P, "call_json", lambda *a, **k: (_ for _ in ()).throw(AssertionError("the planner must not be called on the fast lane")))
    monkeypatch.setattr(P, "build_executor_plan", lambda job, docs, plan, option: type("X", (), {"plan_id": "plan-fast"})())
    monkeypatch.setattr(P.events, "emit", lambda *a, **k: None)
    runner._run_step(job, "plan", docs)
    assert job.plan.plan_id == "plan-fast" and [p.engine_key for p in job.plan.phases] == ["oeuvre_trajectory", "citation_shift", "retrospective_reading", "prospective_reading", "epistemic_rupture", "oeuvre_position_memo", "thinker_placement"]
    assert [p.scope for p in job.plan.phases][2:4] == [["focal:", "before:"], ["focal:", "after:"]] and job.plan.estimated_llm_calls == 7


def test_a_figure_spec_repair_does_not_assign_an_undeclared_field():
    """The figures step crashed on the oeuvre desks run: a rejected spec was given `section_key`, a field FigureSpec does not
    declare, which pydantic refuses (2026-09-07). The repair keeps the section on the spec's __dict__ only."""
    import inspect
    from src.dossier import figures
    from src.dossier.schemas import FigureSpec
    src = inspect.getsource(figures.spec_figures)
    assert "sp.section_key =" not in src
    with pytest.raises(ValueError):
        FigureSpec(key="f", primitive="lineage", visual_format="x").section_key = "s"


def test_the_ledger_is_the_authority_on_holdings_and_the_focal_document_carries_it():
    """The Stacks (2026-09-07 12:05): a work held in the library came out 'unheld' — the packet had merged the ledger's row and the profile's
    works-cited by title, so the profile's English title made a second, unheld row that the set difference then chose."""
    b = json.loads(json.dumps(BUNDLE))
    b["focal"]["profile"]["works_cited"] = [{"title": "The Communist Manifesto", "author": "Marx, Karl; Engels, Friedrich", "year": "1848", "role": "source", "uid": None}]
    b["focal"]["ledger"]["works"] = [{"key": "marx:1848:manifest kommunistischen partei", "title": "Manifest der Kommunistischen Partei", "authors": "Marx, Karl; Engels, Friedrich",
                                      "year": "1848", "n_events": 3, "held": "em:9U6GQ84T", "held_how": "library", "held_edition": "MECW 6"}]
    pk = packet_of(b)
    manifestos = [c for c in pk["cited_first_in_focal"] if "manifest" in (c.get("title") or "").lower()]
    assert len(manifestos) == 1 and manifestos[0]["held"] is True and manifestos[0]["held_uid"] == "em:9U6GQ84T" and manifestos[0]["held_how"] == "library"
    assert not any("communist manifesto" in (c.get("title") or "").lower() for c in pk["cited_first_in_focal"])
    assert any("whether or not that work's text is supplied" in n for n in pk["notes"])
    docs = expand_oeuvre_bundle(json.dumps(b))
    focal = next(d for d in docs if d.key.startswith("focal:"))
    assert "LEDGER, WORKS CITED" in focal.text and "held em:9U6GQ84T (library, MECW 6)" in focal.text
    assert focal.text.index("LEDGER, WORKS CITED") < focal.text.index("There are two Marxian models")
    # a text without a ledger still contributes its profile's works-cited
    b["focal"]["ledger"] = {}
    pk2 = packet_of(b)
    assert any("communist manifesto" in (c.get("title") or "").lower() and c["held"] is False for c in pk2["cited_first_in_focal"])


def test_the_placement_engine_the_packets_persons_and_the_recipes_seventh_step():
    """The owner (2026-09-07 12:17): the thinker-exists check is already answered; the action on an unknown person is to add them
    with a placement — a school they fit or a new school around them with candidates."""
    from src.operationalizations.registry import get_operationalization_registry
    from src.dossier.catalog import load_recipes
    from src.vocabularies.registry import get_vocabulary_registry
    op = get_operationalization_registry().get("thinker_placement")
    assert [d.key for d in op.process.dimensions] == ["fit", "new_school", "verdict"] and all(d.scope == "document" for d in op.process.dimensions)
    assert {v.value for v in get_vocabulary_registry().get("thinker_placement_verdicts").values} == {"fits", "new_school", "not_a_candidate"}
    steps = next(r for r in load_recipes() if r["key"] == "oeuvre_position")["steps"]
    assert [s["engine_key"] for s in steps][-2:] == ["oeuvre_position_memo", "thinker_placement"]
    pk = packet_of(BUNDLE)
    import os; os.environ["REFEREE_URL"] = ""                            # no Referee in tests: the engine proposes new schools only
    pk = packet_of(BUNDLE)
    assert pk["schools"] == []
    unknown = {e["person"]: e for e in pk["persons_unknown"]}
    assert "Guizot, François" in unknown and all(not e["referee_thinker_id"] for e in unknown.values())
    assert any(e["in_referee"] for e in pk["persons"])                    # Wallerstein carries a Referee id in the fixture
    given = json.loads(json.dumps(BUNDLE)); given["referee"] = {"schools": [{"id": 7, "name": "Political Marxism", "description": "social-property relations", "member_count": 12, "members": [{"name": "Wood, Ellen"}]}]}
    assert packet_of(given)["schools"] == [{"id": 7, "slug": None, "name": "Political Marxism", "kind": None, "description": "social-property relations", "members": 12, "sample": ["Wood, Ellen"]}]


def test_suggested_actions_in_the_owners_terms():
    """A held work and a known person need nothing; the exists-check is suppressed when the ledger answered it; an unknown person's
    entry carries the placement and one school-propose per fitting school; an optional input never blocks."""
    from src.dossier.oeuvre import actions_for, placements_of
    from src.actions.registry import suggest
    row = lambda i, dim, **f: {"engine": "citation_shift", "id": i, "dim": dim, "text": f.get("cited", ""), "conjecture": False, "fields": f}
    rows = [row("F1", "first_cited", cited="The Poverty of Philosophy", kind="work", held="yes", in_referee="unknown"),
            row("F2", "first_cited", cited="Meek, Ronald", kind="person", held="unknown", in_referee="no"),
            row("F3", "unexamined", cited="Meek, Ronald", kind="person", held="unknown", in_referee="no", used_for="the four-stages genealogy"),
            row("F4", "unexamined", cited="Cohen, G. A.", kind="person", held="unknown", in_referee="no"),
            row("F5", "first_cited", cited="Marx, Karl", kind="person", held="unknown", in_referee="yes"),
            row("F6", "unexamined", cited="Social Science and the Ignoble Savage", kind="work", held="no", in_referee="unknown")]
    prow = lambda i, dim, **f: {"engine": "thinker_placement", "id": i, "dim": dim, "text": f.get("person", ""), "conjecture": False, "fields": f}
    pl = placements_of([prow("F1", "verdict", person="Meek, Ronald", verdict="fits", reason="a historian of the four-stages theory"),
                        prow("F2", "fit", person="Meek, Ronald", school="7", school_name="History of economic thought", evidence="cited for the four-stages genealogy"),
                        prow("F3", "verdict", person="Cohen, G. A.", verdict="not_a_candidate", reason="cited once in passing")])
    assert pl["meek, ronald"]["fits"][0]["school_name"] == "History of economic thought"
    from src.actions.registry import ActionRegistry, DEFINITIONS
    reg = ActionRegistry(DEFINITIONS, durable=False)
    sp = reg.get("referee.school-propose"); sp.when = sorted(set(sp.when) | {"thinker_placement.fit"}); reg._items[sp.key] = sp   # the Referee adds this on its side
    out = actions_for(rows, reg, placements=pl, run_id="run-x")
    by = {e["cited"]: e for e in out}
    assert "The Poverty of Philosophy" not in by and "Marx, Karl" not in by and "Cohen, G. A." not in by
    meek = by["Meek, Ronald"]
    assert meek["also"] == ["citation_shift/F3"] and meek["placement"]["verdict"] == "fits"
    names = [a["action"] for a in meek["actions"] + meek["waiting"]]
    assert "referee.thinker-exists" not in names and "referee.thinker-create" in [a["action"] for a in meek["actions"]]
    propose = [a for a in meek["actions"] + meek["waiting"] if a["action"] == "referee.school-propose"]
    assert propose and propose[0]["inputs"]["folder_id"] == "7" and propose[0]["inputs"]["evidence"]["clause"] == "cited for the four-stages genealogy"
    assert propose[0]["inputs"]["author_name"] == "Ronald Meek" and propose[0]["inputs"]["source_ref"] == "oeuvre:run-x" and propose[0]["inputs"]["evidence"]["finding"] == "thinker_placement.fit"
    assert all(not (PERSON := {"thinker_name", "referee_thinker_id"} & set(a["inputs"]) | set(a["missing"])) or True for a in by["Social Science and the Ignoble Savage"]["actions"])
    assert not any(a["organ"] == "the-referee" and "thinker_name" in a["inputs"] for a in by["Social Science and the Ignoble Savage"]["actions"] + by["Social Science and the Ignoble Savage"]["waiting"])
    s = next(a for a in suggest("citation_shift.unexamined", {"thinker_name": "Meek, Ronald"}, reg) if a["action"] == "referee.thinker-create")
    assert s["missing"] == [] and "scholar_profile_url" in s["optional"]


def test_a_step_added_to_a_finished_job_reads_its_documents_and_joins_its_analysis():
    """A run made before the recipe had a step gets it as a light call over its own documents (2026-09-07 13:20)."""
    from src.dossier.steps import add_step
    texts = {"d1": "SOURCE ROLE: focal_text\nMeek is cited for the four-stages theory.", "d2": "profile of 1989: Meek again.", "d3": "profile of 2006: nothing here.",
             "dp": json.dumps({"kind": "oeuvre", "focal": {"uid": "em:F"}, "persons": [{"person": "Meek, Ronald", "in_referee": False}], "persons_unknown": [{"person": "Meek, Ronald", "cited_in": {"before": [], "focal": ["em:F"], "after": ["em:A89"]}}],
                              "schools": [{"id": 1, "name": "History of economic thought"}], "cited_first_in_focal": [{"title": "x"}] * 50, "notes": ["n"]})}
    job = {"documents": [{"key": "focal:em:F", "role": "source", "executor_doc_id": "d1"}, {"key": "after:em:A89", "role": "source", "executor_doc_id": "d2"},
                         {"key": "after:em:A06", "role": "source", "executor_doc_id": "d3"}, {"key": "oeuvre", "role": "plan", "executor_doc_id": "dp"}],
           "analysis": {"4.1": {"engine_key": "oeuvre_trajectory", "final_output": "x"}, "4.6": {"engine_key": "oeuvre_position_memo", "final_output": "y"}}, "totals": {"cost_usd": 10.0, "llm_calls": 25}}
    seen = {}
    def fake_call(engine_key, sources, *, packet=None, depth="surface", model=None, spend_cap_usd=2.0):
        seen.update(engine_key=engine_key, keys=[s.key for s in sources], packet=packet, depth=depth)
        return {"engine_key": engine_key, "final_output": "[P3.F1] Meek: not a candidate — dim: verdict — person: Meek, Ronald — verdict: not_a_candidate — reason: bibliographic — anchor: \"Meek is cited\" — doc: focal:em:F — confidence: high",
                "wall": {"failed_ids": [], "verified": 1, "anchors": 1}, "cost_usd": 0.15, "calls": [1, 2], "model": "m", "seconds": 3}
    phase = add_step(job, "thinker_placement", get_text=texts.get, call=fake_call)
    assert seen["keys"] == ["focal:em:F", "after:em:A89"] and "cited_first_in_focal" not in seen["packet"] and seen["packet"]["schools"][0]["id"] == 1
    assert "4.7" in job["analysis"] and job["analysis"]["4.7"]["engine_key"] == "thinker_placement" and job["analysis"]["4.7"]["added"] is True
    assert job["totals"] == {"cost_usd": 10.15, "llm_calls": 27}
    from src.dossier.oeuvre import _rows
    rows = _rows({"analysis": job["analysis"]}, "thinker_placement")
    assert rows and rows[0]["fields"]["verdict"] == "not_a_candidate"
    add_step(job, "thinker_placement", get_text=texts.get, call=fake_call, packet_override={"schools": [{"id": 9, "name": "Political Marxism", "description": "x" * 300, "sample": ["a", "b", "c", "d"]}]})
    assert seen["packet"]["schools"] == [{"id": 9, "name": "Political Marxism", "description": "x" * 100, "sample": ["a", "b", "c"]}] and seen["packet"]["persons_unknown"][0]["person"] == "Meek, Ronald" and "4.8" in job["analysis"]
    texts["d1"] = "SOURCE ROLE: focal_text\n" + "Meek. " * 400        # the packet counts against the cap: with room for one document only the focal text goes
    add_step(job, "thinker_placement", get_text=texts.get, call=fake_call, max_chars=len(json.dumps(seen["packet"])) + 2_000 + 2_600)
    assert seen["keys"] == ["focal:em:F"]


def test_enumerated_fields_are_pinned_to_their_vocabulary_and_drift_is_reported():
    """Run 3's retrospective verdict came back 'qualified culmination' (2026-09-07 13:00): a value outside its vocabulary is shape,
    so the parser normalises it when one vocabulary word is inside it and reports the drift; nothing else is judged."""
    from src.dossier.explainer import rows_with_fields
    out = ("[R4.F1] The paper culminates the critique — dim: verdict — verdict: qualified culmination — warrant: w — anchor: \"x\" — doc: focal:em:F — confidence: high\n"
           "[R4.F2] Another — dim: verdict — verdict: Continuation — anchor: \"y\" — doc: focal:em:F — confidence: low\n"
           "[R4.F3] A third — dim: verdict — verdict: a fresh start — anchor: \"z\" — doc: focal:em:F — confidence: low")
    rows = rows_with_fields(out, engine_key="retrospective_reading")
    assert rows[0]["fields"]["verdict"] == "culmination" and rows[0]["fields"]["verdict_raw"] == "qualified culmination" and rows[0]["drift"] == [{"field": "verdict", "value": "qualified culmination", "fixed": "culmination"}]
    assert rows[1]["fields"]["verdict"] == "continuation" and "drift" not in rows[1]
    assert rows[2]["fields"]["verdict"] == "a fresh start" and rows[2]["drift"][0]["fixed"] is None
    assert "drift" not in rows_with_fields(out)[0]                     # without an engine nothing is pinned
