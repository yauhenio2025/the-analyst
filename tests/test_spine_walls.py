"""Pass S walls (no network): section bounds, keys, one-sentence claims, the caption-number law,
anchors verbatim (fragments refused), feeds membership, budget ceilings, patch merge, code repairs."""
from __future__ import annotations

from src.dossier.schemas import ExhibitsBudget
from src.dossier.spine import _merge_patch, _repair_by_code, coerce_spine, narration_for, validate_spine
from src.dossier.walls import NormalizedCorpus

DOC_A = ("Sustainability and neoliberalism are major contemporary idea systems that permeate a lot of the discourse in "
         "media, corporate board rooms, policy forums, research settings, and classrooms. While sustainability is invoked "
         "freely, neoliberalism operates in a somewhat stealth fashion.")
DOC_B = ("Digital platforms reconfigure apparel production networks through a spatial-digital fix that relocates risk to "
         "producers, who bear the cost of demand volatility.")
CORPUS = NormalizedCorpus({"A": DOC_A, "B": DOC_B})
BUDGET = ExhibitsBudget(tables=2, figures=1)


def section(key, **over):
    base = {
        "key": key, "heading": f"Heading {key}", "claim": f"Section {key} proves one thing.",
        "reader_needs_next": "the next thing", "evidence_kind": "mechanism", "table": None, "figure": None,
        "anchors_planned": [{"doc_key": "A", "quote": "permeate a lot of the discourse in media, corporate board rooms"}],
        "feeds": [],
    }
    base.update(over)
    return base


def raw(sections, **over):
    base = {"read": {"plain_summary": "It says a thing."}, "thesis": "Every claim rests on two pillars.",
            "reader_question": "q", "handle": "h", "through_line": "t",
            "summary_job": "the finding and the stakes", "conclusion_job": "the decision rule and the question to ask",
            "sections": sections}
    base.update(over)
    return base


def test_clean_spine_passes():
    sp = coerce_spine(raw([section("one"), section("two"), section("three")]), BUDGET)
    per, glob = validate_spine(sp, CORPUS)
    assert per == {} and glob == []
    assert sp.sections[0].anchors_planned[0].verified and not sp.sections[0].anchors_planned[0].trimmed


def test_section_bounds_and_duplicate_keys():
    sp = coerce_spine(raw([section("one"), section("one")]), BUDGET)
    _, glob = validate_spine(sp, CORPUS)
    assert any("2 sections" in g for g in glob) and any("duplicate" in g for g in glob)


def test_claim_must_be_one_sentence_and_thesis_too():
    sp = coerce_spine(raw([section("one", claim="First thing. Second thing."), section("two"), section("three")],
                          thesis="Two sentences. Here."), BUDGET)
    per, glob = validate_spine(sp, CORPUS)
    assert any("ONE sentence" in e for e in per["one"])
    assert any("thesis" in g for g in glob)


def test_abbreviations_do_not_split_a_claim():
    sp = coerce_spine(raw([section("one", claim="Officials use e.g. security language vs. the record, i.e. the paperwork."), section("two"), section("three")]), BUDGET)
    per, _ = validate_spine(sp, CORPUS)
    assert "one" not in per


def test_caption_number_law_and_unknown_format():
    fig = {"primitive": "flow_transformation", "visual_format": "sankey", "picture_shows": "money flows to firms",
           "caption_says": "Roughly 300 jobs were promised.", "why_a_picture": "flows"}
    sp = coerce_spine(raw([section("one", figure=fig), section("two"), section("three")]), BUDGET)
    per, _ = validate_spine(sp, CORPUS)
    assert any("carries a number" in e for e in per["one"])
    assert sp.sections[0].figure.visual_format == "sankey_diagram"  # alias normalized in place
    bad = dict(fig, caption_says="Money goes to a short list of firms.", visual_format="pie_of_doom", primitive="not_a_primitive")
    sp = coerce_spine(raw([section("one", figure=bad), section("two"), section("three")]), BUDGET)
    per, _ = validate_spine(sp, CORPUS)
    assert any("visual_format" in e for e in per["one"]) and any("primitive" in e for e in per["one"])


def test_table_spec_shape():
    sp = coerce_spine(raw([section("one", table={"intent": "x", "row_unit": "", "columns": ["only"], "carries_claims": []}),
                           section("two"), section("three")]), BUDGET)
    per, _ = validate_spine(sp, CORPUS)
    errs = " | ".join(per["one"])
    assert "row_unit" in errs and "2-6" in errs and "carries_claims" in errs


def test_anchor_fragment_is_refused_not_trimmed():
    trimmed = [{"doc_key": "A", "quote": "neoliberalism operates in a somewhat stealth fashion and hides its engines from view"}]
    sp = coerce_spine(raw([section("one", anchors_planned=trimmed), section("two"), section("three")]), BUDGET)
    per, _ = validate_spine(sp, CORPUS)
    assert any("no planned anchor is verbatim" in e for e in per["one"])
    assert sp.sections[0].anchors_planned == []


def test_anchor_rekeyed_and_kept():
    sp = coerce_spine(raw([section("one", anchors_planned=[{"doc_key": "A", "quote": "relocates risk to producers, who bear the cost of demand volatility"}]),
                           section("two"), section("three")]), BUDGET)
    per, _ = validate_spine(sp, CORPUS)
    assert "one" not in per and sp.sections[0].anchors_planned[0].doc_key == "B"


def test_feeds_pruned_to_real_later_keys():
    sp = coerce_spine(raw([section("one", feeds=["two", "ghost", "one"]), section("two"), section("three")]), BUDGET)
    validate_spine(sp, CORPUS)
    assert sp.sections[0].feeds == ["two"]


def test_summary_and_conclusion_jobs_must_differ():
    sp = coerce_spine(raw([section("one"), section("two"), section("three")], conclusion_job="The finding and the stakes."), BUDGET)
    _, glob = validate_spine(sp, CORPUS)
    assert any("DIFFERENT" in g for g in glob)


def test_budget_ceiling_drops_earliest_exhibits_by_code():
    tbl = {"intent": "i", "row_unit": "one row = one case", "columns": ["a", "b"], "carries_claims": ["c"]}
    fig = {"primitive": "flow_transformation", "visual_format": "sankey_diagram", "picture_shows": "p", "caption_says": "c", "why_a_picture": "w"}
    sp = coerce_spine(raw([section("one", table=tbl, figure=fig), section("two", table=tbl, figure=fig), section("three", table=tbl)]), BUDGET)
    per, _ = validate_spine(sp, CORPUS)
    sp = _repair_by_code(sp, per, BUDGET)
    assert [bool(s.table) for s in sp.sections] == [False, True, True]
    assert [bool(s.figure) for s in sp.sections] == [False, True, False]
    assert any("over the budget" in n for n in sp.notes)


def test_code_repairs_two_sentence_claim_and_digit_caption():
    fig = {"primitive": "flow_transformation", "visual_format": "sankey_diagram", "picture_shows": "p", "caption_says": "About 300 jobs became 12.", "why_a_picture": "w"}
    sp = coerce_spine(raw([section("one", claim="First. Second.", figure=fig), section("two"), section("three")]), BUDGET)
    per, _ = validate_spine(sp, CORPUS)
    sp = _repair_by_code(sp, per, BUDGET)
    assert sp.sections[0].claim == "First."
    assert sp.sections[0].figure is not None and "300" not in sp.sections[0].figure.caption_says
    assert len(sp.notes) == 2


def test_patch_merge_replaces_only_the_failing_sections():
    sp = coerce_spine(raw([section("one", claim="Bad. Claim."), section("two"), section("three")]), BUDGET)
    patch = coerce_spine({"sections": [section("one", claim="Good claim."), section("two", claim="Not asked for.")]}, BUDGET)
    merged, unknown = _merge_patch(sp, patch, {"one"})
    assert [s.claim for s in merged.sections] == ["Good claim.", "Section two proves one thing.", "Section three proves one thing."]
    assert unknown == ["two"]


def test_narration_counts_exhibits():
    tbl = {"intent": "i", "row_unit": "r", "columns": ["a", "b"], "carries_claims": ["c"]}
    sp = coerce_spine(raw([section("one", table=tbl), section("two"), section("three")]), BUDGET)
    assert "3 sections" in narration_for(sp) and "1 table " in narration_for(sp) and "0 diagrams" in narration_for(sp)
