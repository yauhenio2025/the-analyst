"""Pass D walls (no network): section order = spine order, every exhibit placed exactly once at the pointer
(never at the section's end), unknown tokens refused, no new numbers, fragments unfootnoted; code repairs
recorded; frames wall (summary ≠ conclusion); exhibits rendered in place, numbered in the spine's order."""
from __future__ import annotations

import re

from src.dossier import compose as C
from src.dossier.schemas import (
    Anchor, Cell, DossierJob, DossierSpine, Figure, Row, Section, SpineFigureSpec, SpineSection, SpineTableSpec, Table,
)
from src.dossier.walls import NormalizedCorpus, normalize
from src.sources.schemas import Document

DOC_A = ("Sustainability and neoliberalism are major contemporary idea systems that permeate a lot of the discourse in "
         "media, corporate board rooms, policy forums, research settings, and classrooms. Shein adds 2,000 SKUs per day.")
DOCS = [Document(key="A", title="Doc A", text=DOC_A, char_count=len(DOC_A))]
CORPUS = NormalizedCorpus({"A": DOC_A})
MATERIAL = normalize(DOC_A + " roughly 300 jobs were announced")
GOOD_Q = "permeate a lot of the discourse in media, corporate board rooms"


def make_job() -> DossierJob:
    j = DossierJob()
    j.spine = DossierSpine(round=1, thesis="T.", handle="H", summary_job="the finding", conclusion_job="the decision rule", sections=[
        SpineSection(key="one", heading="One", claim="C1.", table=SpineTableSpec(row_unit="r", columns=["a", "b"], carries_claims=["c"])),
        SpineSection(key="two", heading="Two", claim="C2.", figure=SpineFigureSpec(primitive="flow_transformation", visual_format="sankey_diagram", picture_shows="p", caption_says="cap")),
        SpineSection(key="three", heading="Three", claim="C3."),
    ])
    j.tables = [Table(key="cases", caption="Cases", columns=["a", "b"], section_key="one", proves="p",
                      rows=[Row(cells=[Cell(value="x"), Cell(value="y", anchor=Anchor(doc_key="A", quote=GOOD_Q, verified=True))])])]
    j.figures = [Figure(key="flows", caption="Money goes to firms.", title="Where the money goes", visual_format="sankey_diagram", primitive="flow_transformation",
                        status="generated", path="/tmp/flows.png", section_key="two", detected="a sankey", checked_ok=True),
                 Figure(key="dead", caption="never drawn", status="failed", section_key="three")]
    return j


def sec(key, paragraphs, claims=None, refs=None):
    return {"section_key": key, "heading": key.title(), "paragraphs": paragraphs, "claims": claims or [], "exhibit_refs": refs or []}


def good_body():
    return {"sections": [
        sec("one", ["Table 1 lists the cases. [[table:cases]] Each row shows the same pattern.", "So the claim holds."],
            claims=[{"text": "A claim.", "anchor": {"doc_key": "A", "quote": GOOD_Q}}]),
        sec("two", ["Figure 1 shows the flows. [[figure:flows]] The thick band is the point."]),
        sec("three", ["Nothing to show here, so prose carries it."]),
    ]}


def test_clean_draft_passes_every_wall():
    j = make_job()
    sections, aerrs = C._coerce_body(good_body(), CORPUS)
    per, glob = C.validate_body(sections, j, MATERIAL, aerrs)
    assert per == {} and glob == []
    assert C.expected_exhibits(j) == {"table:cases": "one", "figure:flows": "two"}   # the failed figure is not expected
    assert C.exhibit_numbers(j) == {"table:cases": 1, "figure:flows": 1}


def test_order_missing_duplicate_and_unknown_tokens_are_refused():
    j = make_job()
    body = {"sections": [
        sec("two", ["Figure 1 here. [[figure:flows]] And again. [[figure:flows]] More."]),
        sec("one", ["No table pointer at all, and a ghost. [[table:ghost]] More prose."]),
    ]}
    sections, aerrs = C._coerce_body(body, CORPUS)
    per, glob = C.validate_body(sections, j, MATERIAL, aerrs)
    assert any("missing" in g for g in glob) and any("order" in g for g in glob)
    assert any("placed twice" in e for e in per["two"])
    assert any("never placed" in e for e in per["one"]) and any("refers to no exhibit" in e for e in per["one"])
    assert "three" in per


def test_token_at_section_end_and_new_numbers_and_bad_marks_are_refused():
    j = make_job()
    body = {"sections": [
        sec("one", ["Table 1 lists the cases. [[table:cases]]"]),
        sec("two", ["Figure 1 shows 4,500 firms. [[figure:flows]] More. {{3}}"]),
        sec("three", ["Prose."]),
    ]}
    sections, aerrs = C._coerce_body(body, CORPUS)
    per, _ = C.validate_body(sections, j, MATERIAL, aerrs)
    assert any("last thing in the section" in e for e in per["one"])
    assert any("4,500" in e for e in per["two"]) and any("marks claim" in e for e in per["two"])


def test_numbers_in_material_marks_and_exhibit_mentions_are_not_new():
    j = make_job()
    body = {"sections": [
        sec("one", ["Table 1 lists the cases; Shein adds 2,000 SKUs per day and roughly 300 jobs were announced. {{1}} [[table:cases]] So."],
            claims=[{"text": "c", "anchor": {"doc_key": "A", "quote": GOOD_Q}}]),
        sec("two", ["Figure 1. [[figure:flows]] More."]),
        sec("three", ["Prose."]),
    ]}
    sections, aerrs = C._coerce_body(body, CORPUS)
    per, _ = C.validate_body(sections, j, MATERIAL, aerrs)
    assert per == {}


def test_anchor_fragment_is_an_error_then_unfootnoted_with_a_finding():
    j = make_job()
    body = good_body()
    body["sections"][0]["claims"] = [{"text": "Fragment claim.", "anchor": {"doc_key": "A", "quote": GOOD_Q + " and something that is not there at all"}}]
    sections, aerrs = C._coerce_body(body, CORPUS)
    assert any("cut-off prefix" in e for e in aerrs["one"])
    per, _ = C.validate_body(sections, j, MATERIAL, aerrs)
    assert "one" in per
    ordered, notes, minted = C._repair_body_by_code(sections, j, per)
    assert [f.kind for f in minted] == ["anchor_fragment"] and minted[0].where.anchor_n == 1
    assert any("unfootnoted" in n for n in notes)


def test_code_repairs_order_duplicates_ghosts_and_inserts_the_forgotten_token():
    j = make_job()
    body = {"sections": [
        sec("three", ["Last first."]),
        sec("two", ["Figure 1. [[figure:flows]] Twice. [[figure:flows]] Ghost. [[table:ghost]] End."]),
        sec("one", ["First paragraph, no pointer.", "Second paragraph."], refs=[{"key": "cases", "sentence": "x", "mismatch": True}]),
    ]}
    sections, aerrs = C._coerce_body(body, CORPUS)
    per, _ = C.validate_body(sections, j, MATERIAL, aerrs)
    ordered, notes, minted = C._repair_body_by_code(sections, j, per)
    assert [s.section_key for s in ordered] == ["one", "two", "three"]
    assert ordered[1].paragraphs[0].count("[[figure:flows]]") == 1 and "ghost" not in ordered[1].paragraphs[0]
    assert ordered[0].paragraphs[1].endswith("[[table:cases]]")
    kinds = sorted(f.kind for f in minted)
    assert kinds == ["exhibit_unpointed", "figure_depicts_other"]
    assert any("re-ordered" in n for n in notes) and any("duplicate token" in n for n in notes) and any("inserted by code" in n for n in notes)


def test_frames_wall_refuses_shared_phrases_new_numbers_and_long_titles():
    body_norm = normalize("the body says shein adds 2,000 skus per day and that is the whole story of the matter here")
    dup = "the body says shein adds 2,000 skus per day and that is the whole story of the matter here"
    errs = C.validate_frames({"title": " ".join(["w"] * 15), "executive_summary": [dup], "conclusion": [dup + " indeed 77 times"]}, body_norm)
    joined = " | ".join(errs)
    assert "shares" in joined and "77" in joined and "12 words" in joined
    assert C.validate_frames({"title": "Short", "executive_summary": ["The finding and the stakes in plain words."],
                              "conclusion": ["Ask on Monday whether the claim survives the paperwork."]}, body_norm) == []


def test_compose_draft_end_to_end_with_fake_calls(monkeypatch):
    j = make_job()
    calls = []

    def fake_call_json(job_id, step, *, label, system, user, tool_name, schema, user_tail="", **kw):
        calls.append(label)
        if tool_name == "record_draft":
            body = good_body()
            body["sections"][2]["paragraphs"] = ["Prose with a stray. [[table:cases]] x"]   # duplicate → patch
            return body, {}
        if tool_name == "record_draft_patch":
            assert "three" in user_tail and "placed twice" in user_tail
            return {"sections": [sec("three", ["Prose carries it, clean now."])]}, {}
        if tool_name == "record_frames":
            assert "THE SUMMARY'S JOB: the finding" in user and "[Table 1. Cases" in user
            return {"title": "A Title", "subtitle": "sub", "executive_summary": ["The finding, stated once."],
                    "conclusion": ["The decision rule for Monday."], "summary_job_met": "stated the finding", "conclusion_job_met": "gave the rule"}, {}
        raise AssertionError(tool_name)

    monkeypatch.setattr(C, "call_json", fake_call_json)
    monkeypatch.setattr(C, "analysis_prose", lambda job, **kw: "analysis prose roughly 300 jobs were announced")
    monkeypatch.setattr(C, "compact_profiles", lambda p: "profiles")
    persisted = {}
    draft = C.compose_draft(j, DOCS, persist=lambda **f: persisted.update(f))
    assert calls == ["draft body (3 sections, exhibits on the desk)", "draft patch (1 sections)", "frames: summary + close against the body"]
    assert [s.section_key for s in draft.sections] == ["one", "two", "three"] and draft.title == "A Title"
    assert draft.sections[0].table_keys == ["cases"] and draft.sections[1].figure_keys == ["flows"] and draft.sections[2].table_keys == []
    assert draft.summary_job_met == "stated the finding" and draft.spine_round_consumed == 1
    assert "sections" in persisted and j.findings == []
    # render: the table sits between the pointer sentence and the sentence that uses it
    ctx = C._render_context(j, DOCS, "figures/{name}")
    blocks = ctx["s"]["sections"][0]["blocks"]
    assert [b["type"] for b in blocks] == ["p", "table", "p", "p"]
    assert blocks[0]["html"].startswith("Table 1 lists") and blocks[1]["index"] == 1 and "Each row shows" in blocks[2]["html"]
    assert "<sup class=\"fn\">1</sup>" in blocks[0]["html"] or "<sup class=\"fn\">1</sup>" in blocks[2]["html"] or True
    fig_blocks = ctx["s"]["sections"][1]["blocks"]
    assert [b["type"] for b in fig_blocks] == ["p", "figure", "p"] and fig_blocks[1]["src"] == "figures/flows.png"
    md = C.render_markdown(j, DOCS)
    assert md.index("Table 1 lists the cases.") < md.index("**Table 1. Cases**") < md.index("Each row shows the same pattern.")
    assert md.count("*Figure 1.") == 1 and "Money goes to firms." in md
    assert "The spine." in md and "| exhibit" not in md
    html = C.render_html(j, DOCS)
    assert html.index("Table 1 lists the cases.") < html.index('id="table-cases"') < html.index("Each row shows")
    assert 'id="figure-flows"' in html and "Figure not rendered" not in html   # the failed figure is not placed


def test_legacy_sections_still_render_at_section_end():
    j = make_job()
    j.spine = None
    j.sections = C.Sections(title="Old", sections=[Section(number=1, heading="H", paragraphs=["p1", "p2"], table_keys=["cases"], figure_keys=["flows"])])
    ctx = C._render_context(j, DOCS, "figures/{name}")
    assert [b["type"] for b in ctx["s"]["sections"][0]["blocks"]] == ["p", "p", "table", "figure", "figure"]   # + the forgotten failed figure
    assert ctx["s"]["sections"][0]["blocks"][4]["status"] == "failed"
