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
    assert [s["engine_key"] for s in recipe["steps"]] == ["oeuvre_trajectory", "citation_shift", "retrospective_reading", "prospective_reading", "epistemic_rupture", "oeuvre_position_memo"]
    path = resolve_path_request(PathRequest(chain_key="oeuvre_position"), "researcher")
    assert [s.scope for s in path.steps] == [[], [], ["focal:", "before:"], ["focal:", "after:"], [], []]
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
    assert all(not a["missing"] for a in guizot_work["actions"]) and any(w["action"] == "referee.citations-harvest" and "referee_thinker_id" in w["missing"] for w in guizot_work["waiting"])   # ready ones as buttons, the rest named with what they lack
    fetch = next(w for w in guizot_work["waiting"] if w["action"] == "referee.pdf-fetch")     # a fetch needs a query or a corpus row the finding cannot supply
    assert "query_id" in fetch["missing"] or "corpus_result_id" in fetch["missing"]
    from src.actions.registry import suggest
    filled = next(s for s in suggest("citation_shift.unexamined", {"work_title": "Histoire de la civilisation en Europe", "work_author": "Guizot, François", "work_year": "1830"}, ActionRegistry(DEFINITIONS, durable=False)) if s["action"] == "referee.pdf-fetch")
    assert filled["inputs"]["work_title"] == "Histoire de la civilisation en Europe" and filled["inputs"]["work_author"] == "Guizot, François" and filled["inputs"]["work_year"] == "1830"
    guizot_person = acts["citation_shift/C5.F2"]
    exists = next(a for a in guizot_person["actions"] if a["action"] == "referee.thinker-exists")
    assert exists["inputs"] == {"thinker_name": "Guizot, François"} and exists["cost"] == "none"
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
    assert job.plan.plan_id == "plan-fast" and [p.engine_key for p in job.plan.phases] == ["oeuvre_trajectory", "citation_shift", "retrospective_reading", "prospective_reading", "epistemic_rupture", "oeuvre_position_memo"]
    assert [p.scope for p in job.plan.phases][2:4] == [["focal:", "before:"], ["focal:", "after:"]] and job.plan.estimated_llm_calls == 6


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
