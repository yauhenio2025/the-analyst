"""The research program engine and the research-state record, offline."""
import json

from src.dossier.research_state import research_state_from_program
from src.engines.methods import compose_method, freeze_method


def _row(rid, dim, finding, **fields):
    return {"id": rid, "dim": dim, "doc": "", "anchor": "", "fields": fields, "finding": finding, "confidence": "medium", "anchor_verified": False}


def test_program_method_freezes_with_the_decision_role_and_no_position_map():
    method = freeze_method("inquiry_program")
    cap, spec = compose_method(method)
    assert spec.composition_role == "decision"
    assert [d.key for d in spec.dimensions] == ["stake", "explanation", "lane", "reading", "scan", "gap"]
    from src.stages.process_composer import _corpus_reading
    assert "position map" not in _corpus_reading(spec)
    assert {d["capability"]["engine_key"] for d in method["dependencies"]} == {"causal_mechanism_audit", "multimedia_source_criticism"}


def test_program_prompt_carries_the_hunch_and_withholds_nothing_it_was_given():
    from src.dossier.engine_call import call_engine
    from src.dossier.investigation import _json, _spec
    captured = {}

    def capture(system, user, **kwargs):
        captured.update(system=system, user=user)
        raise RuntimeError("captured")

    common = {"author": {"id": "riley-dylan", "name": "Riley, Dylan"}, "question": "Does the case complicate the thinker?",
              "scope": {"hunch": "The case reveals a monetary-infrastructural dimension.", "leads": ["a co-founder on dollar dominance"], "good_answer": "Tests the hunch against the strongest rival."}}
    sources = [_spec("inquiry-question", _json(common)), _spec("thinker-inventory", _json([{"uid": "em:A1", "title": "Thesis", "profile_summary": "asset circuit"}]))]
    try:
        call_engine("inquiry_program", sources, packet=common, depth="surface", spend_cap_usd=100.0, call_fn=capture, max_chars=650000)
    except RuntimeError:
        pass
    assert "monetary-infrastructural dimension" in captured["user"]
    assert "co-founder on dollar dominance" in captured["user"]
    assert "Competing explanations of the case" in captured["system"]
    assert "Begin with a compact position map" not in captured["system"]


def test_research_state_is_built_from_rows_and_names_its_defects():
    result = {"prose": "The stake is the asset circuit.", "method_receipt": {"engine_key": "inquiry_program"}, "rows": [
        _row("P1.F1", "stake", "Returns come from politically inflated asset prices", thinker="Riley", formulation="em:A1", bears_on="E1; E3"),
        _row("P2.F1", "explanation", "Favoritism raised the firm's returns", id="E1", origin="field", supports_if="incidence differs from rivals",
             undercuts_if="the rule bound all issuers alike", voices="critic; record", venues="court filings; investigative press", actors="Warren; ICIJ",
             discriminating="Tether versus Circle under the same rule", priority="2"),
        _row("P2.F2", "explanation", "Private reserve income serves state dollar strategy", id="E3", origin="hunch", supports_if="executives and Treasury say so in their own words",
             undercuts_if="stablecoin demand only displaces other Treasury demand", voices="participant; official; economist", venues="podcasts; treasury.gov; central bank research",
             actors="Ardoino; Bessent; Kansas City Fed", discriminating="net Treasury demand", priority="1"),
        _row("P2.F3", "explanation", "Ordinary intermediation, politics marginal", id="E4", origin="inquiry", supports_if="growth predates access",
             undercuts_if="", voices="comparator", venues="issuer reports", actors="Circle", discriminating="", priority="3"),
        _row("P3.F1", "lane", "Participants in their own voice", explanations="E3", voice="participant", venues="podcasts.apple.com; omny.fm",
             actors="Ardoino", queries='"Ardoino Treasury dollar"; Tether CEO interview dollar dominance', contrary='"Tether critics dollar"', coverage="one participant statement"),
        _row("P3.F2", "lane", "Official policy", explanations="E3; E1", voice="official", venues="treasury.gov", actors="Bessent",
             queries="stablecoin Treasury statement", contrary="Fed stablecoin demand displacement", coverage="one official document"),
        _row("P3.F3", "lane", "Broken lane", explanations="E9", voice="pundit", venues="", actors="", queries="", contrary="", coverage=""),
        _row("P4.F1", "reading", "Settles the stake", uid="em:A1", explanations="E1; E3", look_for="asset circuit passage", order="1"),
        _row("P4.F2", "reading", "Internal comparator", uid="em:ZZ", explanations="E3", look_for="state loans", order="2"),
        _row("P5.F1", "gap", "The co-founder remark is unlocated", kind="lead_to_verify", lead="a co-founder on dollar dominance", resolve_by="Reporter locates speaker, date, venue"),
    ]}
    state = research_state_from_program(result, question="Q", hunch="H", leads=["a co-founder on dollar dominance"], thinker="Riley", inventory_uids={"em:A1"})
    assert [e.id for e in state.explanations] == ["E3", "E1", "E4"]          # by priority
    assert state.explanations[0].voices == ["participant", "official", "economist"]
    assert state.lanes[0].queries == ["Ardoino Treasury dollar", "Tether CEO interview dollar dominance"] and state.lanes[0].contrary == "Tether critics dollar"
    assert [r.uid for r in state.readings] == ["em:A1", "em:ZZ"] and state.readings[1].in_inventory is False
    assert state.gaps[0].kind == "lead_to_verify"
    problems = "\n".join(state.problems)
    assert "E4 has no discriminating observation" in problems
    assert "E4 says nothing that would undercut it" in problems
    assert "unknown explanation E9" in problems and "'pundit'" in problems and "without literal queries" in problems
    assert "explanation E4 has no lane" in problems
    assert "not in the inventory: em:ZZ" in problems
    assert state.sha256() == research_state_from_program(result, question="Q", hunch="H", leads=["a co-founder on dollar dominance"], thinker="Riley", inventory_uids={"em:A1"}).sha256()
    json.dumps(state.model_dump(mode="json"))


def test_research_state_flags_a_hunch_that_no_explanation_carries():
    result = {"prose": "", "rows": [_row("P2.F1", "explanation", "Only one", id="E1", origin="field", supports_if="x", undercuts_if="y",
                                          voices="critic", venues="press", discriminating="z", priority="1")]}
    state = research_state_from_program(result, question="Q", hunch="a hunch")
    assert "no explanation is marked as originating from it" in "\n".join(state.problems)
    assert "fewer than two competing explanations" in "\n".join(state.problems)


def test_scan_rows_parse_and_the_body_scan_surfaces_texts_the_profiles_hide():
    from src.dossier.research_state import scan_inventory
    result = {"prose": "", "rows": [
        _row("P2.F1", "explanation", "A", id="E1", origin="hunch", supports_if="x", undercuts_if="y", voices="official", venues="v", discriminating="d", priority="1"),
        _row("P2.F2", "explanation", "B", id="E2", origin="field", supports_if="x", undercuts_if="y", voices="critic", venues="v", discriminating="d", priority="2"),
        _row("P3.F1", "lane", "L", explanations="E1; E2", voice="official", venues="treasury.gov", queries="a; b", contrary="c", coverage="one"),
        _row("P4.F1", "reading", "first", uid="em:TITLED", explanations="E1", look_for="definition", order="1"),
        _row("P6.F1", "scan", "deficit finance is the mechanism", phrases='"deficit"; state loans; seigniorage', explanations="E1"),
    ]}
    state = research_state_from_program(result, question="Q", hunch="H", inventory_uids={"em:TITLED", "em:REPLY", "em:REVIEW", "em:OTHER"})
    assert state.scans[0].phrases == ["deficit", "state loans", "seigniorage"]
    rows = [{"uid": "em:TITLED", "title": "Thesis", "source_key": "primary:em:TITLED"},
            {"uid": "em:REPLY", "title": "A reply to critics", "source_key": "primary:em:REPLY", "year": 2025},
            {"uid": "em:REVIEW", "title": "Routes or rivals", "source_key": "primary:em:REVIEW", "year": 2013},
            {"uid": "em:OTHER", "title": "Elsewhere", "source_key": "primary:em:OTHER"}]
    bodies = {"primary:em:TITLED": "Political capitalism defined. Deficit once.",
              "primary:em:REPLY": "Financing permanent deficits became a major source of profits; the deficit again; deficit spending.",
              "primary:em:REVIEW": "Weber linked state loans, arms and interstate competition.",
              "primary:em:OTHER": "Nothing about money here."}
    scan_inventory(state, rows, bodies)
    ranked = [(c.uid, c.total, c.already_ordered) for c in state.candidates]
    assert ranked[0] == ("em:REPLY", 3, False) and ("em:REVIEW", 1, False) in ranked and ("em:TITLED", 1, True) in ranked
    assert all(c.uid != "em:OTHER" for c in state.candidates)
    assert state.candidates[0].explanations == ["E1"] and "major source of profits" in state.candidates[0].windows[0]


def test_program_route_wrapper_returns_state_and_the_reporter_program():
    from src.dossier.inquiry_program import run
    from src.dossier.investigation import _json, _spec
    ledger = "\n".join([
        "[P1.F1] Political power determines the rate of return — dim: stake — thinker: Riley — formulation: em:A1 — bears_on: E1 — anchor: \"asset circuit\" — doc: thinker-inventory — confidence: high",
        "[P2.F1] Private reserve income serves state dollar strategy — dim: explanation — id: E1 — origin: hunch — supports_if: executives and Treasury say so — undercuts_if: demand only displaces — voices: participant; official — venues: podcasts; treasury.gov — actors: Ardoino — discriminating: net Treasury demand — priority: 1 — confidence: medium",
        "[P2.F2] Ordinary intermediation — dim: explanation — id: E2 — origin: field — supports_if: growth predates access — undercuts_if: returns jump after intervention — voices: comparator — venues: filings — actors: Circle — discriminating: fundamentals model — priority: 2 — confidence: medium",
        "[P3.F1] Participants in their own voice — dim: lane — explanations: E1 — voice: participant — venues: podcasts; omny.fm — actors: Ardoino — queries: \"Tether CEO interview dollar\"; Tether Treasury reserves podcast — contrary: Tether critics dollar — coverage: one statement — confidence: medium",
        "[P3.F2] Broken — dim: lane — explanations: E1 — voice: pundit — venues: x — actors: — queries: a — contrary: b — coverage: c — confidence: low",
        "[P4.F1] Settles the stake — dim: reading — uid: em:A1 — explanations: E1 — look_for: asset circuit — order: 1 — confidence: high",
        "[P6.F1] Mechanisms — dim: scan — phrases: state loans; deficit — explanations: E1 — confidence: medium",
        "[P5.F1] Verify the lead — dim: gap — kind: lead_to_verify — lead: a co-founder on dollar dominance — resolve_by: Reporter — confidence: medium",
    ])
    def fake(system, user, **kwargs):
        return {"content": "The stake is the asset circuit.\n\n## Findings ledger\n" + ledger, "model_used": "openrouter/openai/gpt-5.6-sol",
                "input_tokens": 1000, "output_tokens": 400}
    packet = {"question": "Does Tether complicate Riley?", "author": {"id": "riley-dylan", "name": "Riley, Dylan"},
              "scope": {"hunch": "monetary-infrastructural", "leads": ["a co-founder on dollar dominance"], "good_answer": "tests the bridge"}}
    sources = [_spec("inquiry-question", _json(packet)), _spec("thinker-inventory", _json([{"uid": "em:A1", "title": "Thesis", "profile_summary": "asset circuit"}]))]
    result = run(sources, packet=packet, spend_cap_usd=1.0, call_fn=fake, model="openrouter/openai/gpt-5.6-sol")
    state = result["research_state"]
    assert state["hunch"] == "monetary-infrastructural" and state["leads"] == ["a co-founder on dollar dominance"] and state["thinker"] == "Riley, Dylan"
    assert [e["id"] for e in state["explanations"]] == ["E1", "E2"] and state["readings"][0]["in_inventory"] is True
    assert state["scans"][0]["phrases"] == ["state loans", "deficit"]
    assert any("'pundit'" in p for p in state["problems"])
    program = result["program"]
    assert [e["id"] for e in program["explanations"]] == ["E1", "E2"] and program["explanations"][0]["voices"] == ["participant", "official"]
    assert [l["id"] for l in program["lanes"]] == ["P3.F1"]                         # the pundit lane is left out; the state names it
    assert program["lanes"][0]["queries"] == ["Tether CEO interview dollar", "Tether Treasury reserves podcast"]
    assert program["stake"].startswith("Political power") and len(program["source"]) == 64 and program["queries_per_lane"] == 3
    assert result["research_state_sha256"] == program["source"] and result["charged_or_reserved_usd"] >= result["cost_usd"]
