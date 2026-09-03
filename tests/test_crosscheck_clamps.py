"""Pass X (no network): code clamps outrank the judge (caption digit, unplaced exhibit, failed picture check,
redundant frames); the verdict walls (kinds, where-exists, quote-on-page, realization required, repeats merged);
fate completeness (silence → persists by code); the safe automatic realizations and the zero-change gate."""
from __future__ import annotations

from src.dossier import crosscheck as X
from src.dossier import findings as ledger
from src.dossier.schemas import (
    Anchor, Cell, Claim, DossierJob, DossierOptions, DossierSpine, Figure, Row, Section, Sections, SpineFigureSpec, SpineSection, SpineTableSpec, Table,
)
from src.sources.schemas import Document

DOCS = [Document(key="A", title="Doc A", text="the document text", char_count=17)]


def make_job(depth="medium") -> DossierJob:
    j = DossierJob(options=DossierOptions(depth=depth))
    j.spine = DossierSpine(thesis="T.", summary_job="the finding", conclusion_job="the decision rule", sections=[
        SpineSection(key="one", heading="One", claim="C1.", table=SpineTableSpec(row_unit="r", columns=["a", "b"], carries_claims=["c"])),
        SpineSection(key="two", heading="Two", claim="C2.", figure=SpineFigureSpec(primitive="flow_transformation", visual_format="sankey_diagram", picture_shows="p", caption_says="Money goes to firms.")),
    ])
    j.tables = [Table(key="cases", caption="Cases in 2024", columns=["a", "b"], section_key="one", rows=[Row(cells=[Cell(value="x"), Cell(value="y")])])]
    j.figures = [Figure(key="flows", caption="About 300 firms.", title="Flows", visual_format="sankey_diagram", primitive="flow_transformation", status="generated",
                        path="/nonexistent/flows.png", section_key="two", caption_says="Money goes to firms.", detected="a bar chart", checked_ok=False,
                        compliance={"checked": True, "ok": False, "issues": ["wrong format"], "suggestion": "draw the sankey"})]
    j.sections = Sections(title="T", executive_summary=["The finding is that money goes to a short list of firms and nobody checks the paperwork afterwards."],
                          conclusion=["Ask on Monday for the paperwork."],
                          sections=[Section(number=1, heading="One", section_key="one", paragraphs=["Table 1 lists the cases. [[table:cases]] So it holds."],
                                            claims=[Claim(text="A claim.", anchor=Anchor(doc_key="A", quote="the document text", verified=True))]),
                                    Section(number=2, heading="Two", section_key="two", paragraphs=["No pointer here, the picture is orphaned."])])
    return j


def test_clamps_mint_from_recorded_facts():
    j = make_job()
    out = X.clamp_findings(j, 1)
    kinds = sorted(f.kind for f in out)
    assert kinds == ["caption_carries_number", "caption_carries_number", "exhibit_unplaced", "figure_depicts_other"]
    fig_caption = next(f for f in out if f.kind == "caption_carries_number" and f.where.figure_key == "flows")
    assert fig_caption.realization == "Money goes to firms." and fig_caption.affordance == "rewrite_caption"
    tbl_caption = next(f for f in out if f.kind == "caption_carries_number" and f.where.table_key == "cases")
    assert tbl_caption.realization == "Cases in"
    unplaced = next(f for f in out if f.kind == "exhibit_unplaced")
    assert unplaced.where.figure_key == "flows" and unplaced.affordance == "drop_figure"
    depicts = next(f for f in out if f.kind == "figure_depicts_other")
    assert depicts.source == "clamp" and depicts.realization == "draw the sankey" and "wrong format" in depicts.note


def test_clamps_never_duplicate_an_open_finding():
    j = make_job()
    j.findings = [ledger.mint("figure_depicts_other", where={"figure_key": "flows", "section_key": "two"}, note="from the desk", affordance="rerender_figure")]
    out = X.clamp_findings(j, 1)
    assert "figure_depicts_other" not in [f.kind for f in out]


def test_redundant_frames_clamp():
    j = make_job()
    j.sections.conclusion = [j.sections.executive_summary[0] + " That is the rule."]
    out = X.clamp_findings(j, 1)
    r = next(f for f in out if f.kind == "redundant_summary_conclusion")
    assert "shares" in r.note and r.affordance == "rewrite_section"


def test_verdict_walls_drop_unknown_offpage_and_unlocated_findings():
    j = make_job()
    raw = {"hangs_together": False, "summary": "s", "what_changed": None, "prior_fates": [], "findings": [
        {"kind": "not_a_kind", "where": {}, "quote": "x", "note": "n", "affordance": "none", "realization": None, "recommended": True, "target_id": None},
        {"kind": "claim_unbacked", "where": {"section_key": "ghost"}, "quote": "So it holds.", "note": "n", "affordance": "none", "realization": None, "recommended": True, "target_id": None},
        {"kind": "claim_unbacked", "where": {"section_key": "one"}, "quote": "these words are nowhere on the page", "note": "n", "affordance": "none", "realization": None, "recommended": True, "target_id": None},
        {"kind": "claim_unbacked", "where": {"section_key": "one"}, "quote": "So it holds.", "note": "asserted bare", "affordance": "rewrite_paragraph", "realization": None, "recommended": True, "target_id": None},
        {"kind": "caption_restates_text", "where": {"section_key": "one", "table_key": "cases"}, "quote": "Table 1 lists the cases.", "note": "echo", "affordance": "rewrite_paragraph", "realization": "Table 1 shows why.", "recommended": True, "target_id": None},
    ]}
    kept, fates, notes = X.validate_verdict(raw, j, [], 1)
    assert [f.kind for f in kept] == ["claim_unbacked", "caption_restates_text"]
    assert kept[0].affordance == "none"   # rewrite without a realization → advisory
    assert kept[1].realization == "Table 1 shows why." and kept[1].source == "judge"
    joined = " | ".join(notes)
    assert "unknown kind" in joined and "names nothing" in joined and "not on the page" in joined and "without a drafted realization" in joined


def test_repeat_of_a_standing_finding_is_merged_not_duplicated():
    j = make_job()
    standing = [ledger.mint("figure_depicts_other", where={"figure_key": "flows", "section_key": "two"}, note="desk note", affordance="rerender_figure")]
    raw = {"findings": [{"kind": "figure_depicts_other", "where": {"figure_key": "flows", "section_key": "two"}, "quote": "About 300 firms.", "note": "judge note",
                         "affordance": "revise_figure_spec", "realization": "a sankey of money to firms", "recommended": True, "target_id": standing[0].id}],
           "prior_fates": [{"target_id": standing[0].id, "fate": "persists", "rationale": "still wrong"}]}
    kept, fates, notes = X.validate_verdict(raw, j, standing, 1)
    assert kept == [] and "judge note" in standing[0].note and standing[0].realization == "a sankey of money to firms"
    assert fates == [{"target_id": standing[0].id, "fate": "persists", "rationale": "still wrong"}]


def test_fate_completeness_silence_persists_by_code():
    a = ledger.mint("anchor_fragment", note="a", affordance="reanchor_claim")
    b = ledger.mint("table_rows_dropped", note="b", affordance="revise_table_rows")
    notes = X.apply_fates([a, b], [{"target_id": a.id, "fate": "resolved", "rationale": "fixed"}], 1)
    assert a.status == "resolved" and a.fates[-1].by == "judge"
    assert b.status == "open" and b.fates[-1].fate == "persists" and b.fates[-1].by == "code" and len(notes) == 1


def test_judge_finding_on_a_clamped_fact_joins_the_clamp():
    clamp = ledger.mint("caption_carries_number", where={"figure_key": "flows"}, note="clamp", affordance="rewrite_caption", source="clamp")
    judge = ledger.mint("caption_carries_number", where={"figure_key": "flows", "section_key": "two"}, note="judge says", affordance="rewrite_caption", realization="Money goes to firms.")
    out, notes = X._merge_clamps([clamp], [judge])
    assert out == [] and "judge says" in clamp.note and clamp.realization == "Money goes to firms."


def test_realize_rewrites_captions_drops_unplaced_and_redraws_once(monkeypatch):
    j = make_job()
    j.findings = X.clamp_findings(j, 1)
    rendered = {}
    monkeypatch.setattr("src.dossier.compose.render_all", lambda job, docs: rendered.setdefault("paths", {"html": "x"}))

    def fake_render(job, spec, out_dir, provider=None, revision_notes=None):
        assert revision_notes and revision_notes[0].startswith("THE CROSS-CHECK'S VERDICT")
        return Figure(**spec.model_dump(), status="generated", path="/tmp/new.png", compliance={"checked": True, "ok": True, "detected_format": "sankey", "labels_found": ["a"], "n_labels": 1})

    monkeypatch.setattr("src.dossier.figures.render_figure", fake_render)
    # the unplaced-figure drop would remove the figure before the redraw; make the figure placed so the redraw is exercised
    j.sections.sections[1].paragraphs = ["Figure 1 shows it. [[figure:flows]] So."]
    j.findings = [f for f in j.findings if f.kind != "exhibit_unplaced"]
    acted, notes = X.realize(j, DOCS, 1)
    assert j.tables[0].caption == "Cases in" and j.figures[0].caption == "Money goes to firms."
    assert j.figures[0].checked_ok is True and j.figures[0].attempts[0].get("before_crosscheck") is True
    fates = {f.kind: f.fates[-1].fate for f in j.findings}
    assert fates["caption_carries_number"] == "executed" and fates["figure_depicts_other"] == "resolved"
    assert len(acted) == 3 and "document re-rendered" in notes and rendered["paths"] == {"html": "x"}


def test_realize_drops_an_unplaced_exhibit_and_zero_change_gate(monkeypatch):
    j = make_job()
    j.figures[0].checked_ok = True
    j.figures[0].caption = "Money goes to firms."
    j.tables[0].caption = "Cases"
    j.findings = X.clamp_findings(j, 1)
    assert [f.kind for f in j.findings] == ["exhibit_unplaced"]
    monkeypatch.setattr("src.dossier.compose.render_all", lambda job, docs: {"html": "x"})
    acted, notes = X.realize(j, DOCS, 1)
    assert j.figures == [] and len(acted) == 1 and j.findings[0].status == "resolved"
    # nothing recommended → the gate
    j2 = make_job()
    j2.findings = [ledger.mint("register_break", note="n", affordance="rewrite_section", realization="x", recommended=False)]
    acted2, notes2 = X.realize(j2, DOCS, 1)
    assert acted2 == [] and any("zero-change gate" in n for n in notes2)


def test_run_crosscheck_simple_depth_is_report_only(monkeypatch):
    j = make_job(depth="simple")
    j.sections.sections[1].paragraphs = ["Figure 1 shows it. [[figure:flows]] So."]

    def fake_call_json(job_id, step, *, label, system, user, tool_name, schema, images=None, **kw):
        assert images is None and "STANDING FINDINGS" in user and "ACTUALLY SHOWS (checked): a bar chart" in user
        return {"hangs_together": False, "summary": "Two problems.", "what_changed": None, "prior_fates": [],
                "findings": [{"kind": "jargon_unglossed", "where": {"section_key": "one"}, "quote": "So it holds.", "note": "unglossed", "affordance": "none",
                              "realization": None, "recommended": True, "target_id": None}]}, {}

    monkeypatch.setattr(X, "call_json", fake_call_json)
    persisted = {}
    v = X.run_crosscheck(j, DOCS, persist=lambda **f: persisted.update(f))
    assert v.judged and v.hangs_together is False and v.findings_minted == 4 and v.clamps == 3 and v.realized == []
    assert sorted(f.kind for f in j.findings) == ["caption_carries_number", "caption_carries_number", "figure_depicts_other", "jargon_unglossed"]
    assert j.figures[0].caption == "About 300 firms."   # report only: nothing executed
    assert "crosscheck" in persisted and "findings" in persisted


def test_run_crosscheck_judge_failure_keeps_the_clamps(monkeypatch):
    j = make_job(depth="simple")

    def boom(*a, **k):
        raise RuntimeError("model down")

    monkeypatch.setattr(X, "call_json", boom)
    v = X.run_crosscheck(j, DOCS)
    assert v.judged is False and v.hangs_together is None and v.clamps == 4 and len(j.findings) == 4
