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


def test_the_timeline_and_the_two_halves_draw_from_the_rows_by_code():
    from src.exhibits.svg import exhibit_svg, timeline_svg, two_halves_svg
    oeuvre = {"verdicts": {"rupture": "deepening"},
              "agendas": [{"id": "F1", "text": "The transition agenda", "span": "em:A/1976 … em:B/2007; 11 texts"}, {"id": "F2", "text": "The downturn agenda", "span": "em:C/1986 … em:D/2025; 24 texts"}],
              "turns": [{"id": "F7", "text": "From controversy to reconstruction", "at": "em:A/1977 → em:F/1985", "changed": "method, concepts"}],
              "rupture": [{"id": "E3", "dim": "verdict", "text": "a deepening", "verdict": "deepening", "halves": "1972–1984 formation vs 1985–2025 codification"},
                          {"id": "E1", "dim": "continuity", "text": "the object persists", "what": "object", "before": "em:A/1977", "after": "em:D/2001"},
                          {"id": "E2", "dim": "break", "text": "the method changes", "what": "method", "before": "comparison", "after": "reconstruction", "at_focal": "partly"}]}
    packet = {"author": {"id": "brenner-robert", "name": "Brenner, Robert"}, "focal": {"uid": "em:F", "year": "1985", "title": "Marx's First Model"},
              "texts": [{"uid": "em:A", "year": "1976", "title": "Agrarian"}, {"uid": "em:F", "year": "1985", "title": "Marx's First Model"}, {"uid": "em:D", "year": "2007", "title": "Property and Progress"}, {"uid": "em:X", "year": "n.d.", "title": "undated"}]}
    svg = timeline_svg(oeuvre, packet)
    assert svg.startswith("<svg") and "Brenner, Robert" in svg and "F1" in svg and "F2" in svg and "F7 1977→1985" in svg and "1985 · Marx" in svg
    assert svg.count("<title>") >= 6 and "prefers-color-scheme: dark" in svg          # hover rows; light and dark selected
    halves = two_halves_svg(oeuvre)
    assert "verdict: deepening" in halves and "1972–1984 formation" in halves and "1985–2025 codification" in halves
    assert "persists · object" in halves and "breaks · method · partly at the focal text" in halves and 'class="seam"' in halves
    assert exhibit_svg("no-such", oeuvre, packet) is None and exhibit_svg("two-halves", oeuvre, None).startswith("<svg")
