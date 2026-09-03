"""Pass E (no network): tables keyed by section with the per-exhibit skip law; figure specs walled
against the spine's laws; records enriched with what the picture actually shows; findings minted."""
from __future__ import annotations

from src.dossier import tables as T
from src.dossier.figures import _coerce_spec, enrich_from_spine, finding_for_figure, validate_spine_spec
from src.dossier.schemas import DossierJob, DossierSpine, Figure, SpineFigureSpec, SpineSection, SpineTableSpec
from src.dossier.walls import NormalizedCorpus, normalize

DOC_A = ("Sustainability and neoliberalism are major contemporary idea systems that permeate a lot of the discourse in "
         "media, corporate board rooms, policy forums, research settings, and classrooms.")
DOC_B = "Digital platforms reconfigure apparel production networks through a spatial-digital fix that relocates risk to producers."
CORPUS = NormalizedCorpus({"A": DOC_A, "B": DOC_B})
GOOD = {"doc_key": "A", "quote": "permeate a lot of the discourse in media, corporate board rooms"}
BAD = {"doc_key": "A", "quote": "this sentence is in no document at all, honestly"}


def spine():
    return DossierSpine(thesis="T.", sections=[
        SpineSection(key="one", heading="One", claim="C1.", table=SpineTableSpec(intent="i", row_unit="one row = one case", columns=["Case", "What"], carries_claims=["c"])),
        SpineSection(key="two", heading="Two", claim="C2.", table=SpineTableSpec(intent="i", row_unit="one row = one term", columns=["Term", "Signal"], carries_claims=["c"])),
        SpineSection(key="three", heading="Three", claim="C3."),
    ])


def job():
    j = DossierJob()
    j.spine = spine()
    return j


def table(sk, key, rows):
    return {"section_key": sk, "key": key, "caption": "cap", "columns": ["A", "B"], "note": "n", "proves": "p",
            "rows": [{"cells": [{"value": "x", "anchor": None}, {"value": "y", "anchor": a}]} for a in rows]}


def test_admit_keys_tables_by_section_and_drops_unanchored_rows():
    j = job()
    raw = {"tables": [table("one", "cases", [GOOD, GOOD, BAD]), table("two", "terms", [GOOD, GOOD])]}
    accepted, failures, minted, rejects = T._admit(j, raw, {"one", "two"}, CORPUS, set())
    assert set(accepted) == {"one", "two"}
    assert accepted["one"].section_key == "one" and accepted["one"].proves == "p" and len(accepted["one"].rows) == 2
    assert [f.kind for f in minted] == ["table_rows_dropped"] and minted[0].where.table_key == "cases"
    assert len(failures) == 1 and rejects == []


def test_admit_refuses_uncommissioned_and_duplicate_sections_and_short_tables():
    j = job()
    raw = {"tables": [table("ghost", "g", [GOOD, GOOD]), table("one", "a", [GOOD, GOOD]), table("one", "b", [GOOD, GOOD]), table("two", "c", [GOOD, BAD])]}
    accepted, _, minted, rejects = T._admit(j, raw, {"one", "two"}, CORPUS, set())
    assert set(accepted) == {"one"}
    assert any("not commissioned" in r for r in rejects) and any("already has a table" in r for r in rejects)
    assert any("only 1 row(s) survived" in r for r in rejects)


def test_run_spine_tables_reasks_once_then_records_table_unavailable(monkeypatch):
    j = job()
    calls = []

    def fake_call_json(job_id, step, *, label, system, user, tool_name, schema, user_tail="", **kw):
        calls.append((label, user_tail))
        if len(calls) == 1:
            return {"tables": [table("one", "cases", [GOOD, GOOD])]}, {}
        return {"tables": [table("two", "terms", [BAD])]}, {}   # still short after the re-ask

    monkeypatch.setattr(T, "call_json", fake_call_json)
    docs = [type("D", (), {"key": "A", "text": DOC_A, "char_count": len(DOC_A)})(), type("D", (), {"key": "B", "text": DOC_B, "char_count": len(DOC_B)})()]
    monkeypatch.setattr(T, "corpus_text", lambda d: "corpus")
    monkeypatch.setattr(T, "analysis_prose", lambda j: "prose")
    monkeypatch.setattr(T, "compact_profiles", lambda p: "profiles")
    out = T.run_spine_tables(j, docs)
    assert [t.section_key for t in out] == ["one"]
    assert len(calls) == 2 and "two" in calls[1][1] and "RE-ASK" in calls[1][1]
    kinds = [f.kind for f in j.findings]
    assert "table_unavailable" in kinds
    f = next(x for x in j.findings if x.kind == "table_unavailable")
    assert f.where.section_key == "two" and f.affordance == "add_table" and "one row = one term" in f.realization


def test_schema_enumerates_sections():
    sch = T.spine_tables_schema(["one", "two"], 2)
    props = sch["properties"]["tables"]["items"]["properties"]
    assert props["section_key"]["enum"] == ["one", "two"] and "proves" in props


# ── figures ──────────────────────────────────────────────────────────────

MATERIAL = normalize("AUKUS routes contracts to Lockheed Martin. Greece hosts Microsoft.")
SEC = SpineSection(key="s1", heading="Where the money goes", claim="C.",
                   figure=SpineFigureSpec(primitive="flow_transformation", visual_format="sankey_diagram", picture_shows="money to firms", caption_says="Money goes to a short list of firms."))


def spec(**over):
    base = {"key": "flows", "primitive": "flow_transformation", "visual_format": "sankey_diagram", "title": "Where the Money Goes",
            "caption": "Money goes to a short list of firms.", "why_this_format": "flows",
            "data": {"flows": [{"source": "AUKUS", "target": "Lockheed Martin", "weight": 4}, {"source": "Greece", "target": "Microsoft", "weight": 3}, {"source": "AUKUS", "target": "Microsoft", "weight": 1}]},
            "anchors": [{"label": "Lockheed Martin", "quote": "routes contracts to Lockheed Martin", "source": "analysis"}]}
    base.update(over)
    return _coerce_spec(base, 1)


def test_spine_spec_wall_accepts_a_clean_spec():
    errors, grounding = validate_spine_spec(spec(), SEC, MATERIAL)
    assert errors == [] and grounding["anchors_verified"] == 1


def test_spine_spec_wall_refuses_changed_primitive_digit_caption_and_long_caption():
    errors, _ = validate_spine_spec(spec(primitive="network_relation", caption="About 300 jobs. Then 12. Then none."), SEC, MATERIAL)
    joined = " | ".join(errors)
    assert "primitive must stay" in joined and "carries a number" in joined and "at most two sentences" in joined


def test_enrich_and_findings_from_the_check():
    ok = Figure(**spec().model_dump(), status="generated", compliance={"checked": True, "ok": True, "format_ok": True, "detected_format": "sankey", "labels_found": ["AUKUS", "Microsoft"], "n_labels": 2})
    ok = enrich_from_spine(ok, SEC)
    assert ok.section_key == "s1" and ok.checked_ok is True and ok.picture_shows == "money to firms" and "2/2 labels" in ok.detected
    assert finding_for_figure(ok, SEC) is None
    bad = Figure(**spec().model_dump(), status="generated", compliance={"checked": True, "ok": False, "format_ok": False, "detected_format": "bar chart", "labels_found": [], "n_labels": 2, "labels_missing": ["AUKUS", "Microsoft"], "issues": ["wrong format"], "suggestion": "draw the sankey"})
    bad = enrich_from_spine(bad, SEC)
    assert bad.checked_ok is False and "not the sankey_diagram" in bad.detected
    f = finding_for_figure(bad, SEC)
    assert f.kind == "figure_depicts_other" and f.affordance == "rerender_figure" and f.realization == "draw the sankey" and f.where.figure_key == "flows"
    unchecked = enrich_from_spine(Figure(**spec().model_dump(), status="generated", compliance={"checked": False}), SEC)
    assert unchecked.checked_ok is None and unchecked.detected.startswith("unchecked")
    failed = enrich_from_spine(Figure(**spec().model_dump(), status="failed", note="provider down"), SEC)
    assert finding_for_figure(failed, SEC).kind == "figure_unavailable"
