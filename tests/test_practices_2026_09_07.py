"""Search craft as practices (Evgeny, 2026-09-07 00:10: 'such tricks have to start living in the Mastermind, in parallel
with the engines'): the registry loads the first twelve, serves them by task kind as records a planner's packet carries,
and a run's yield writes back onto the practice it deployed."""
import json
from pathlib import Path

import pytest

from src.practices.registry import Practice, PracticeEvidence, PracticeRegistry, get_practice_registry, packet_block


def test_the_first_twelve_load_with_the_record_shape():
    reg = get_practice_registry()
    keys = {p.key for p in reg.list()}
    assert {"byline-anchor", "wildcard-name", "venue-first", "author-page-as-index", "transcript-site", "title-quote", "compress-to-names",
            "proper-noun-anchor", "filetype-pdf", "news-vertical-for-recency", "no-date-on-thin-indexes", "open-web-with-known-hosts-excluded"} <= keys
    b = reg.get("byline-anchor")
    assert b.task_kinds == ["person-harvest"] and '"<first> * <last>" "<anchor>"' in b.shape and b.ingredients and b.yields and b.misses and b.origin
    assert all(p.when and p.shape and p.yields for p in reg.list())


def test_practices_are_served_by_task_kind_as_records():
    reg = get_practice_registry()
    person = reg.for_task("person-harvest")
    assert {p.key for p in person} >= {"byline-anchor", "wildcard-name", "venue-first", "proper-noun-anchor"}   # proper-noun-anchor applies to every task
    assert "filetype-pdf" not in {p.key for p in person} and "filetype-pdf" in {p.key for p in reg.for_task("pdf-fetch")}
    assert "proper-noun-anchor" in {p.key for p in reg.for_task("anything-at-all")}
    block = packet_block(person)
    assert all(set(b) == {"practice", "when", "shape", "ingredients", "yields", "misses", "evidence"} for b in block)
    assert reg.task_kinds() == ["institution-harvest", "paper-discovery", "pdf-fetch", "person-harvest", "work-identity"]


def test_a_yield_writes_back_onto_the_practice(tmp_path):
    src = get_practice_registry().file_for("byline-anchor")
    (tmp_path / "byline-anchor.json").write_text(src.read_text())
    reg = PracticeRegistry(tmp_path)
    p = reg.add_evidence("byline-anchor", PracticeEvidence(run="reporter-run-77", organ="the-reporter", queries=10, new_relevant=3, note="alameda.institute reached"))
    assert p.yield_totals() == {"runs": 1, "queries": 10, "new_relevant": 3} and p.evidence[0].recorded
    again = PracticeRegistry(tmp_path).get("byline-anchor")
    assert again.evidence[0].run == "reporter-run-77" and packet_block([again])[0]["evidence"]["new_relevant"] == 3
    with pytest.raises(KeyError):
        reg.add_evidence("no-such-practice", PracticeEvidence(run="x"))


def test_the_routes_serve_the_registry():
    from src.api.routes.practices import get_practice, list_practices, task_kinds
    rows = list_practices(task="person-harvest")
    assert rows and all("practice" in r and "shape" in r for r in rows)
    assert get_practice("wildcard-name")["key"] == "wildcard-name" and "person-harvest" in task_kinds()


def test_an_organ_registers_a_practice_and_only_its_owner_may_overwrite_it(tmp_path):
    from src.practices.registry import Practice
    reg = PracticeRegistry(tmp_path)
    p = reg.upsert(Practice(key="fetch-ladder", name="The fetch ladder", task_kinds=["pdf-fetch"], when="a paper has a DOI", shape="doi → unpaywall → publisher → scholar",
                            yields="the PDF", owner="the-referee"))
    assert p.version and PracticeRegistry(tmp_path).get("fetch-ladder").owner == "the-referee" and "pdf-fetch" in PracticeRegistry(tmp_path).task_kinds()
    reg.add_evidence("fetch-ladder", PracticeEvidence(run="referee-9", organ="the-referee", queries=4, new_relevant=2))
    p2 = reg.upsert(Practice(key="fetch-ladder", name="The fetch ladder", task_kinds=["pdf-fetch", "work-identity"], when="a paper has a DOI or a title", shape="…", yields="the PDF", owner="the-referee"))
    assert p2.evidence[0].run == "referee-9" and p2.task_kinds == ["pdf-fetch", "work-identity"]      # an update keeps the runs' evidence
    with pytest.raises(PermissionError):
        reg.upsert(Practice(key="fetch-ladder", name="x", task_kinds=["pdf-fetch"], when="w", shape="s", yields="y", owner="gs-revamp"))
    with pytest.raises(ValueError):
        reg.upsert(Practice(key="Not A Slug", name="x", task_kinds=["pdf-fetch"], when="w", shape="s", yields="y"))
    with pytest.raises(ValueError):
        reg.upsert(Practice(key="thin", name="x", task_kinds=[], when="", shape="s", yields="y"))
