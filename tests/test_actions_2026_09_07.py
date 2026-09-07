"""The actions registry (Evgeny, 2026-09-07: findings tied to the operations an organ can perform): the seeded records load,
a finding kind lists what can be done about it with inputs filled from the row, an organ registers its own and only it may
overwrite them, and an outcome writes back."""
import pytest

from src.actions.registry import Action, ActionOutcome, ActionRegistry, get_action_registry, suggest


def test_the_seeded_actions_load_and_a_finding_lists_what_can_be_done():
    reg = get_action_registry()
    assert {a.organ for a in reg.list()} >= {"the-referee", "the-stacks", "the-reporter", "the-mastermind"}
    assert reg.get("referee.citations-harvest").cost == "metered" and reg.get("referee.thinker-exists").cost == "none"
    keys = {a.key for a in reg.for_finding("citation_shift.unexamined")}
    assert {"referee.thinker-exists", "referee.thinker-create", "referee.citations-harvest", "referee.pdf-fetch", "referee.seed-title-resolve"} <= keys
    assert "stacks.oeuvre-bundle" not in keys and "stacks.citation-ledger" in keys      # citation_shift.* licenses the ledger
    assert "mastermind.run-engine" in {a.key for a in reg.for_finding("anything.at-all")}   # `*` applies to every finding
    s = suggest("citation_shift.unexamined", {"thinker_name": "Guizot, François", "work_title": "Histoire de la civilisation en Europe", "referee_thinker_id": None}, reg)
    exists = next(x for x in s if x["action"] == "referee.thinker-exists")
    assert exists["inputs"] == {"thinker_name": "Guizot, François"} and exists["missing"] == [] and exists["cost"] == "none"
    harvest = next(x for x in s if x["action"] == "referee.citations-harvest")
    assert harvest["inputs"] == {} and harvest["missing"] == ["referee_thinker_id"] and "harvest pause" in harvest["gated_by"]


def test_an_organ_registers_its_action_and_an_outcome_writes_back(tmp_path):
    reg = ActionRegistry(tmp_path, durable=False)
    a = reg.upsert(Action(key="stacks.digest-texts", organ="the-stacks", name="Digest a bundle", when=["oeuvre_position_memo.read_next"], inputs=["uids"], route="POST /api/digests", cost="cents", owner="the-stacks"))
    assert a.version and ActionRegistry(tmp_path, durable=False).get("stacks.digest-texts").organ == "the-stacks"
    reg.add_outcome("stacks.digest-texts", ActionOutcome(run="digest-7", organ="the-stacks", finding="oeuvre_position_memo.read_next", status="done", cost_usd=0.4, result="a digest of five texts"))
    again = reg.upsert(Action(key="stacks.digest-texts", organ="the-stacks", name="Digest a bundle", when=["oeuvre_position_memo.read_next", "text.chosen-as-focal"], route="POST /api/digests", cost="cents", owner="the-stacks"))
    assert again.evidence[0].run == "digest-7" and again.totals() == {"runs": 1, "done": 1, "cost_usd": 0.4}
    with pytest.raises(PermissionError):
        reg.upsert(Action(key="stacks.digest-texts", organ="the-stacks", name="x", when=["a.b"], owner="the-referee"))
    with pytest.raises(ValueError):
        reg.upsert(Action(key="Bad Key", organ="the-stacks", name="x", when=["a.b"]))
    with pytest.raises(ValueError):
        reg.upsert(Action(key="stacks.x", organ="the-stacks", name="x", when=["a.b"], cost="free"))
    with pytest.raises(KeyError):
        reg.add_outcome("no.such", ActionOutcome(run="r"))


def test_the_routes_serve_the_registry():
    from src.api.routes.actions import SuggestIn, finding_kinds, get_action, list_actions, suggest_actions
    assert any(r["key"] == "referee.pdf-fetch" for r in list_actions(finding="citation_shift.unexamined", organ="the-referee"))
    assert get_action("referee.thinker-exists")["route"].startswith("GET /api/thinkers/search") and "citation_shift.unexamined" in finding_kinds()
    assert suggest_actions(SuggestIn(finding="citation_shift.unexamined", fields={"thinker_name": "Meek, Ronald"}))[0]["finding"] == "citation_shift.unexamined"
