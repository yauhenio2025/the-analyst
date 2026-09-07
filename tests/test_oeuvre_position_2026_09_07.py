"""A paper's place in its author's oeuvre (Evgeny, 2026-09-07): the six engines load with the registry's vocabularies, the
recipe carries scopes, the Stacks' bundle expands at the door into focal / before / after documents and the packet."""
import json

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
