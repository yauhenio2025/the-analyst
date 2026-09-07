"""Intents, the action register, the narrative and the macro actions (Evgeny, 2026-09-07 18:30: 'a self-constructing narrative that
always narrates what we do so that macro actions become possible… we approve once and that enables ten, fifteen, twenty actions')."""
import json

import pytest
import yaml

from src.actions.registry import Action, ActionRegistry, DEFINITIONS, allowed_intents, suggest
from src.engines.schemas_v2 import CapabilityEngineDefinition
from src.operationalizations.registry import get_operationalization_registry


def test_the_intents_vocabulary_pins_the_narrative_and_every_action_carries_its_intents():
    from src.vocabularies.registry import get_vocabulary_registry
    vr = get_vocabulary_registry()
    assert allowed_intents() == ["expand_network", "expand_library", "expand_horizons", "sharpen_position", "verify_holdings", "keep_current"]
    assert vr.values_for("trajectory_narrative", "intent") == allowed_intents() and vr.values_for("macro_actions", "intent") is None   # the macro's intent may be leave_for_now: the parser, not the pin, checks it
    reg = ActionRegistry(DEFINITIONS, durable=False)
    assert all(a.intents for a in reg.list()) and "expand_network" in reg.get("referee.thinker-create").intents and reg.get("referee.pdf-fetch").intents == ["expand_library"]
    s = next(x for x in suggest("citation_shift.unexamined", {"thinker_name": "Meek, Ronald"}, reg) if x["action"] == "referee.thinker-create")
    assert s["intents"] == ["expand_network"]


def test_an_actions_intents_are_validated_on_upsert(tmp_path):
    reg = ActionRegistry(tmp_path, durable=False)
    a = reg.upsert(Action(key="stacks.shelve-texts", organ="the-stacks", name="Shelve", when=["a.b"], owner="the-stacks", intents=["expand_library"]))
    assert a.intents == ["expand_library"]
    with pytest.raises(ValueError, match="intents"):
        reg.upsert(Action(key="stacks.shelve-more", organ="the-stacks", name="Shelve", when=["a.b"], owner="the-stacks", intents=["grow_everything"]))


def test_the_register_appends_reads_back_and_survives_a_reload(monkeypatch):
    import src.actions.register as reg
    store = {}
    monkeypatch.setattr(reg, "_put", lambda key, ct, data: store.__setitem__(key, data) or True)
    monkeypatch.setattr(reg, "_get", lambda key: store.get(key))
    reg.reset_for_tests()
    e1 = reg.record_event("job_done", job_id="dossier-1", engine_keys=["oeuvre_trajectory"], cost_usd=11.3, intent="sharpen_position")
    e2 = reg.record_event("outcome", action="referee.thinker-create", organ="the-referee", status="done", finding="citation_shift.unexamined", batch="M1.F1", intent="expand_network")
    assert e1["kind"] == "job_done" and e2["batch"] == "M1.F1" and "when" in e1
    assert [e["kind"] for e in reg.events()] == ["outcome", "job_done"]                       # newest first
    assert [e["kind"] for e in reg.events(kind="outcome")] == ["outcome"] and reg.events(since="2999-01-01T00:00:00Z") == []
    with pytest.raises(ValueError):
        reg.record_event("mystery")
    text = reg.render_register(reg.events())
    assert text.startswith("SOURCE ROLE: register") and "job_done — job_id: dossier-1" in text and text.index("job_done") < text.index("outcome — action")   # oldest first in the document
    reg.reset_for_tests()                                                                     # a restart: the blob is the record
    assert len(reg.events()) == 2 and store["register:events"].count(b"\n") == 1


def test_the_governance_engines_load():
    for k, dims in (("trajectory_narrative", ["project", "intent_served", "next"]), ("macro_actions", ["macro", "enables"])):
        raw = yaml.safe_load(open(f"src/engines/capability_definitions/{k}.yaml")); CapabilityEngineDefinition.model_validate(raw)
        assert raw["family"] == "governance"
        op = get_operationalization_registry().get(k)
        assert [d.key for d in op.process.dimensions] == dims and all(d.scope == "document" and d.id_prefix and f"— dim: {d.key} —" in d.answer_shape and "anchor:" in d.answer_shape for d in op.process.dimensions)


ACTIONS = [{"finding": "citation_shift/F11", "kind": "citation_shift.unexamined", "cited": "Meek, Ronald", "held": "unknown", "in_referee": "no", "used_for": "the four-stages genealogy",
            "placement": {"verdict": "fits", "fits": [{"school": "78", "school_name": "Intellectual History of Marxism and Socialism"}], "new_school": None},
            "actions": [{"action": "referee.thinker-create", "organ": "the-referee", "cost": "cents", "intents": ["expand_network"], "inputs": {"thinker_name": "Meek, Ronald"}},
                        {"action": "referee.school-propose", "organ": "the-referee", "cost": "none", "intents": ["expand_network"], "inputs": {"folder_id": "78", "author_name": "Ronald Meek"}}],
            "waiting": [{"action": "referee.citations-harvest", "organ": "the-referee", "missing": ["referee_thinker_id"]}]},
           {"finding": "citation_shift/F9", "kind": "citation_shift.unexamined", "cited": "The Wealth of Nations", "held": "no", "in_referee": "unknown",
            "actions": [{"action": "referee.seed-title-resolve", "organ": "the-referee", "cost": "cents", "intents": ["verify_holdings", "expand_library"], "inputs": {"work_title": "The Wealth of Nations"}}],
            "waiting": [{"action": "referee.pdf-fetch", "organ": "the-referee", "missing": ["query_id"]}]}]


def test_the_macro_engine_runs_as_a_light_call_and_the_parser_makes_macros():
    from src.actions.macro import parse_macros, render_actions_document
    from src.dossier.engine_call import call_engine
    from src.sources.schemas import SourceSpec
    doc = render_actions_document(ACTIONS, {"author": "Brenner, Robert", "focal": "em:CBT7B8CL"})
    assert "[citation_shift/F11] citation_shift.unexamined: Meek, Ronald (held unknown; in the Referee no)" in doc and "ready: referee.thinker-create on the-referee (cost cents; intents expand_network)" in doc
    assert "placement: fits (Intellectual History of Marxism and Socialism)" in doc and "waiting: referee.pdf-fetch on the-referee needs query_id" in doc
    ledger = ("# Reading\n\nThe page's possibilities amount to two things.\n\n## Findings ledger\n\n"
              "[M1.F1] Expand Brenner's network: add Meek to the Referee, placed — dim: macro — intent: expand_network — says: whom Brenner draws on for the four-stages story — cost_class: cents — estimate: two calls, cents — anchor: \"Meek, Ronald (held unknown; in the Referee no)\" — doc: actions — confidence: high\n"
              "[M1.F2] Leave for now — dim: macro — intent: leave_for_now — says: a fetch needs a query first — cost_class: none — estimate: nothing — anchor: \"referee.pdf-fetch on the-referee needs query_id\" — doc: actions — confidence: medium\n"
              "[M2.F1] Create Meek in the Referee — dim: enables — macro: M1.F1 — action: referee.thinker-create — organ: the-referee — inputs: thinker_name=Meek, Ronald — finding: citation_shift/F11 — anchor: \"referee.thinker-create on the-referee\" — doc: actions — confidence: high\n"
              "[M2.F2] Propose Meek to school 78 — dim: enables — macro: M1.F1 — action: referee.school-propose — organ: the-referee — inputs: folder_id=78; author_name=Ronald Meek — finding: citation_shift/F11 — anchor: \"referee.school-propose on the-referee\" — doc: actions — confidence: high\n"
              "[M2.F3] The fetch waits on a query — dim: enables — macro: M1.F2 — action: referee.pdf-fetch — organ: the-referee — inputs: none — finding: citation_shift/F9 — anchor: \"needs query_id\" — doc: actions — confidence: medium\n"
              "[M2.F4] An orphan — dim: enables — macro: M1.F9 — action: x.y — organ: z — inputs: none — finding: f — anchor: \"Wealth of Nations\" — doc: actions — confidence: low")
    calls = []
    def fake(system, user, *, model_hint, label, **kw):
        calls.append(label)
        return {"content": ledger, "model_used": model_hint, "input_tokens": 2000, "output_tokens": 400}
    out = call_engine("macro_actions", [SourceSpec(kind="paste", role="source", key="actions", title="t", text=doc)], packet={"intents": []}, depth="surface", spend_cap_usd=1.0, call_fn=fake)
    assert calls and out["wall"]["verified"] == 6 and out["wall"]["failed_ids"] == []
    parsed = parse_macros(out["rows"], allowed_intents())
    assert [m["intent"] for m in parsed["macros"]] == ["expand_network", "leave_for_now"] and parsed["macros"][0]["title"].startswith("Expand Brenner's network")
    assert [e["action"] for e in parsed["macros"][0]["enables"]] == ["referee.thinker-create", "referee.school-propose"] and parsed["macros"][0]["enables"][1]["inputs"] == {"folder_id": "78", "author_name": "Ronald Meek"}
    assert parsed["macros"][1]["enables"][0]["action"] == "referee.pdf-fetch" and [u["action"] for u in parsed["unplaced"]] == ["x.y"]
    weird = parse_macros([{"id": "M1.F1", "dim": "macro", "finding": "Grow everything", "fields": {"intent": "grow_everything"}, "anchor_verified": True}], allowed_intents())
    assert weird["macros"][0]["intent"] == "leave_for_now" and weird["macros"][0]["intent_raw"] == "grow_everything"


def test_the_trajectory_block_is_compact_and_reads_the_next_directions():
    from src.api.routes.trajectory import trajectory_block
    assert trajectory_block(None).startswith("TRAJECTORY: no narrative yet")
    t = {"when": "2026-09-07T18:40:00Z", "prose": "We are reading Brenner's 1985 paper in his oeuvre and meeting Hintze on the state's logic. " * 3,
         "rows": [{"dim": "next", "finding": "Add the four unknown thinkers to the Referee, placed"}, {"dim": "project", "finding": "x"}]}
    block = trajectory_block(t)
    assert block.startswith("TRAJECTORY (what we are doing, narrated 2026-09-07T18:40:00Z)") and "NEXT: Add the four unknown thinkers" in block and len(block) <= 2000
    assert len(trajectory_block({**t, "prose": "w" * 5000}, limit=500)) == 500
