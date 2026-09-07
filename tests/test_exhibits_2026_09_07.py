"""The exhibits registry (Evgeny, 2026-09-07 09:31: presentation elements as visible categories in the Mastermind, seeds an LLM
extrapolates): the nine seeds load, a finding kind lists the exhibits that serve it, an organ registers its own, a reviewer's
verdict writes back in the registry's vocabulary."""
import pytest

from src.exhibits.registry import Exhibit, ExhibitRegistry, ExhibitUse, get_exhibit_registry, planner_block


def test_the_seeds_load_and_serve_by_kind_and_medium():
    reg = get_exhibit_registry()
    assert {e.key for e in reg.list()} >= {"oeuvre-timeline", "idea-map", "two-halves", "verdict-chips", "persists-breaks-sidebar", "reading-route-cards", "shift-table", "pull-quote", "glossary-box"}
    assert {e.key for e in reg.for_kind("epistemic_rupture.verdict")} >= {"two-halves", "pull-quote"} and "oeuvre-timeline" not in {e.key for e in reg.for_kind("epistemic_rupture.verdict")}
    assert {e.key for e in reg.for_kind("citation_shift.dropped")} >= {"shift-table"}      # citation_shift.* serves every shift dimension
    assert [e.key for e in reg.for_medium("image")] == ["idea-map"] and reg.get("idea-map").cost == "cents" and reg.get("two-halves").renderer == "dialectical_pair"
    block = planner_block(reg.for_kind("oeuvre_position_memo.read_next"))
    assert block and set(block[0]) == {"exhibit", "name", "when", "inputs", "medium", "renderer", "shape", "didactic", "cost", "uses"}
    assert all(e.shape and e.didactic for e in reg.list())


def test_an_organ_registers_an_exhibit_and_a_review_writes_back(tmp_path):
    reg = ExhibitRegistry(tmp_path, durable=False)
    e = reg.upsert(Exhibit(key="members-by-circle", name="A cohort's members by circle", when=["citation_cohort_synthesis.*"], medium="html", renderer="card_grid_grouped",
                           shape="one card per member grouped by circle", didactic="who is in, and how close", owner="the-stacks"))
    assert e.version and ExhibitRegistry(tmp_path, durable=False).get("members-by-circle").owner == "the-stacks"
    reg.add_use("members-by-circle", ExhibitUse(page="cohort 1", organ="the-stacks", verdict="simplify", note="too many circles"))
    again = reg.upsert(Exhibit(key="members-by-circle", name="A cohort's members by circle", when=["citation_cohort_synthesis.*", "cohort.*"], medium="html", shape="s", didactic="d", owner="the-stacks"))
    assert again.evidence[0].verdict == "simplify" and len(again.when) == 2
    with pytest.raises(PermissionError):
        reg.upsert(Exhibit(key="members-by-circle", name="x", when=["a.b"], shape="s", didactic="d", owner="the-referee"))
    with pytest.raises(ValueError):
        reg.upsert(Exhibit(key="Bad Key", name="x", when=["a.b"], shape="s", didactic="d"))
    with pytest.raises(ValueError):
        reg.upsert(Exhibit(key="odd", name="x", when=["a.b"], shape="s", didactic="d", medium="hologram"))


def test_the_routes_and_the_review_vocabulary():
    from src.api.routes.exhibits import get_exhibit, kinds, list_exhibits
    from src.vocabularies.registry import values
    assert any(r["exhibit"] == "oeuvre-timeline" for r in list_exhibits(kind="oeuvre_trajectory.agenda")) and get_exhibit("verdict-chips")["medium"] == "html"
    assert "epistemic_rupture.break" in kinds() and values("page_review_verdicts") == ["keep", "simplify", "replace", "drop", "move"]
    assert values("exhibit_media") == ["html", "svg", "image", "table", "box", "prose"]
