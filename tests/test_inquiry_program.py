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
    assert [d.key for d in spec.dimensions] == ["stake", "explanation", "lane", "reading", "gap"]
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
             actors="Ardoino", queries="Ardoino Treasury dollar; Tether CEO interview dollar dominance", contrary="Tether critics dollar", coverage="one participant statement"),
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
    assert state.lanes[0].queries == ["Ardoino Treasury dollar", "Tether CEO interview dollar dominance"]
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
