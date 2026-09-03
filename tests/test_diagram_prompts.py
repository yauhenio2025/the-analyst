"""Diagram prompt builder + enforcement catalog tests (no network)."""
from __future__ import annotations

import pytest

from src.display import enforcement as E
from src.images.compliance import diagram_verdict_ok
from src.images.figure_prompts import (
    DIAGRAM_CLOSER,
    DIAGRAM_TEXT_RULES,
    build_diagram_prompt,
    style_for_school,
)

VENN = {
    "key": "overlap", "primitive": "comparative_positioning", "visual_format": "venn_diagram",
    "title": "Where the Three Cases Overlap", "caption": "All three share vendor lock-in.",
    "data": {"sets": [{"label": "AUKUS"}, {"label": "Microsoft Greece"}, {"label": "ASN Calais"}],
             "intersections": [{"of": ["AUKUS", "Microsoft Greece"], "label": "Foreign prime contractor"},
                               {"of": ["AUKUS", "Microsoft Greece", "ASN Calais"], "label": "Vendor lock-in"}]},
}
FLOW = {
    "key": "playbook", "primitive": "flow_transformation", "visual_format": "flowchart",
    "title": "The State-Capital Playbook", "caption": "Four moves, always in this order.",
    "data": {"steps": [{"label": "Government announces"}, {"label": "Framed as national security"},
                       {"label": "Named firm captures funds"}, {"label": "Community promise deferred"}]},
}


# ── catalog ───────────────────────────────────────────────────────────────

def test_v1_entries_ported_verbatim():
    assert len(E.GLOBAL_PROHIBITIONS) == 11
    assert E.GLOBAL_PROHIBITIONS[0] == "Physical objects as containers (boxes, packages, cases, folders, vessels)"
    assert E.GLOBAL_PROHIBITIONS[2] == "Metaphorical imagery (bridges, buildings, landscapes, machinery)"
    v1 = {k for k, e in E.FORMAT_ENFORCEMENT.items() if e["source"] == "v1"}
    assert v1 == {"flowchart", "timeline", "sankey_diagram", "structured_diagram", "network_graph", "treemap", "matrix",
                  "matrix_heatmap", "conceptual_landscape", "conceptual_layers", "venn_diagram", "constellation_map",
                  "weight_mass", "radial_hierarchy", "spectrum_gradient", "containment_nesting"}
    fc = E.FORMAT_ENFORCEMENT["flowchart"]
    assert "PROFESSIONAL STYLING: Like a McKinsey/BCG consulting slide, NOT a plain technical diagram" in fc["must_have"]
    assert "Plain black lines on white background (BORING - add color!)" in fc["must_not"]
    assert E.FORMAT_ENFORCEMENT["sankey_diagram"]["pass_if"] == ["flowing ribbons", "left-to-right flow", "bands connecting", "width proportional"]


def test_every_format_has_family_aspect_and_rules():
    for key, e in E.FORMAT_ENFORCEMENT.items():
        assert e["family"] in E.DATA_SHAPES, key
        assert e["aspect"] in ("1:1", "4:3", "3:4", "16:9", "9:16", "3:2", "2:3"), key
        assert len(e["must_have"]) >= 3 and len(e["must_not"]) >= 3, key
        assert e["visual_signature"] and e["reference_style"], key
    # the v2 catalog's diagram formats are all covered
    for k in ("chord_diagram", "hierarchical_tree", "radial_tree", "force_directed", "alluvial_diagram", "process_flow",
              "value_stream_map", "gantt_chart", "parallel_timelines", "cycle_diagram", "quadrant_chart", "radar_chart",
              "bar_chart", "treemap", "sunburst", "stacked_bar", "waterfall_chart", "euler_diagram", "positioning_map",
              "bubble_chart", "ach_matrix", "confidence_thermometer", "evidence_quality_matrix", "indicator_dashboard",
              "gap_analysis", "argument_tree", "toulmin_diagram", "dialectical_map", "assumption_web", "scenario_cone"):
        assert k in E.FORMAT_ENFORCEMENT, k


def test_aliases_and_normalization():
    assert E.normalize_format_key("sankey") == "sankey_diagram"
    assert E.normalize_format_key("Venn Diagram") == "venn_diagram"
    assert E.normalize_format_key("quadrant_grid") == "quadrant_chart"
    assert E.normalize_format_key("heatmap") == "matrix_heatmap"
    assert E.normalize_format_key("bridge_diagram") == "toulmin_diagram"   # v1 metaphor → diagram
    assert E.normalize_format_key("feedback_spiral") == "causal_loop_diagram"
    assert E.normalize_format_key("oil painting") is None
    assert E.aspect_for("quadrant_chart") == "1:1" and E.aspect_for("timeline") == "16:9"
    assert E.aspect_for("nonsense", default="4:3") == "4:3"
    for v in E.FORMAT_ALIASES.values():
        assert v in E.FORMAT_ENFORCEMENT


def test_primitives_map_to_canonical_formats():
    keys = E.primitive_keys()
    assert len(keys) == 12 and "cyclical_causation" in keys
    for k in keys:
        fmts = E.primitive_formats(k)
        assert fmts, k
        assert all(f in E.FORMAT_ENFORCEMENT for f in fmts), k
    assert E.primitive_formats("cyclical_causation")[0] == "causal_loop_diagram"


def test_enforcement_block_shape():
    block = E.enforcement_block("sankey")
    assert "MANDATORY FORMAT: SANKEY FLOW DIAGRAM" in block
    assert "WRONG FORMAT = COMPLETE FAILURE" in block
    assert "  ✓ Sources on LEFT, destinations on RIGHT" in block
    assert "  ✗ Collision/explosion/crack imagery" in block
    for p in E.GLOBAL_PROHIBITIONS:
        assert f"  ⛔ {p}" in block
    assert "TEXT LEGIBILITY IS NON-NEGOTIABLE" in block
    assert "Minimum 14pt equivalent font size" in block
    fallback = E.enforcement_block("something_new")
    assert "MANDATORY VISUAL FORMAT**: something_new" in fallback


def test_catalog_text_lists_primitives_formats_and_families():
    t = E.catalog_text()
    assert "PRIMITIVES" in t and "FORMATS" in t and "DATA FAMILIES" in t
    assert "- causal_loop_diagram —" in t and "- steps (" in t
    assert len(t) < 20_000


# ── prompt ────────────────────────────────────────────────────────────────

def test_prompt_order_and_blocks():
    p = build_diagram_prompt(VENN, style_school="restrained_elegance", aspect="4:3")
    assert p.startswith("Create a CONCEPTUAL VENN/EULER DIAGRAM")
    i_enf = p.index("MANDATORY FORMAT: CONCEPTUAL VENN/EULER DIAGRAM")
    i_glob = p.index("UNIVERSAL DATA VISUALIZATION RULES")
    i_style = p.index("MANDATORY STYLE OVERRIDE")
    i_data = p.index("CONTENT TO RENDER")
    i_manifest = p.index("LABEL MANIFEST")
    i_title = p.index("TITLE (render exactly this text once")
    i_text = p.index("TEXT RULES:")
    i_frame = p.index("FRAME: compose for a 4:3 aspect ratio")
    i_close = p.index(DIAGRAM_CLOSER)
    i_style_close = p.index("FINAL STYLE OVERRIDE")
    assert i_enf < i_glob < i_style < i_data < i_manifest < i_title < i_text < i_frame < i_close < i_style_close
    for g in E.GLOBAL_PROHIBITIONS:
        assert g in p
    for r in DIAGRAM_TEXT_RULES:
        assert r in p
    assert "  Set: AUKUS" in p and "Overlap of AUKUS ∩ Microsoft Greece: Foreign prime contractor" in p
    assert "  • Vendor lock-in" in p
    assert "BACKGROUND (mandatory): #fff1e5" in p
    assert "STYLE SCHOOL: restrained_elegance" in p
    assert "no scenery, no metaphors, no photographs, no 3D objects" in p
    assert "FINAL REMINDER: LAYOUT IS MANDATORY" in p
    assert "do NOT render this" in p and "All three share vendor lock-in." in p


def test_prompt_defaults_aspect_from_format_and_accepts_models():
    from src.dossier.schemas import FigureSpec

    spec = FigureSpec.model_validate(FLOW)
    p = build_diagram_prompt(spec)
    assert "FRAME: compose for a 16:9 aspect ratio" in p
    assert "MANDATORY STYLE OVERRIDE" not in p
    assert "  Step 1: Government announces" in p and "  Step 4: Community promise deferred" in p
    assert "LABEL MANIFEST — each of these 4 strings" in p


def test_prompt_revision_notes_and_errors():
    p = build_diagram_prompt(FLOW, revision_notes=["Spell exactly “Named firm captures funds”", " "])
    assert "REVISION NOTES from the reviewer" in p and "  ! Spell exactly" in p
    assert p.count("  ! ") == 1
    with pytest.raises(ValueError):
        build_diagram_prompt({**FLOW, "visual_format": "watercolor"})
    with pytest.raises(ValueError):
        build_diagram_prompt({**FLOW, "title": ""})
    with pytest.raises(ValueError):
        build_diagram_prompt({**FLOW, "data": {"steps": [{"label": "only one"}]}})
    with pytest.raises(TypeError):
        build_diagram_prompt("not a spec")


def test_style_for_school_filters_illustration_lines():
    s = style_for_school("mobilization")
    assert s["background"] == "#1a1a1a" and s["text_color"] == "#FFFFFF"
    assert "metaphor" not in s["palette_description"].lower()
    assert "lighting" not in s["palette_description"].lower()
    assert any("pictorial metaphors" in f for f in s["forbidden"])
    m = style_for_school("minimalist_precision")
    assert m["no_shadows"] is True and m["no_gradients"] is True
    assert style_for_school(None) == {} and style_for_school("bauhaus") == {}


# ── verdict rule ──────────────────────────────────────────────────────────

def test_verdict_rule():
    ok = {"format_ok": True, "prohibited_elements": [], "labels_missing": [], "misspelled": [], "illegible": []}
    assert diagram_verdict_ok(ok, 10)
    assert diagram_verdict_ok({**ok, "labels_missing": ["a", "b"]}, 10)          # 20% tolerated
    assert not diagram_verdict_ok({**ok, "labels_missing": ["a", "b", "c"]}, 10)
    assert diagram_verdict_ok({**ok, "misspelled": [{"expected": "a", "seen": "b"}]}, 3)
    assert not diagram_verdict_ok({**ok, "format_ok": False}, 10)
    assert not diagram_verdict_ok({**ok, "prohibited_elements": ["a bridge"]}, 10)
    assert diagram_verdict_ok({**ok, "extra_text": ["corporate", "R"]}, 10)                       # legend words tolerated
    assert not diagram_verdict_ok({**ok, "extra_text": ["Insight: claims land in the safe quadrant"]}, 10)


def test_quadrant_positions_are_words_not_numbers():
    d = {"x_axis": {"label": "Power", "low": "Low", "high": "High"}, "y_axis": {"label": "Interest", "low": "Low", "high": "High"},
         "items": [{"label": "Shein", "x": 0.12, "y": 0.92}, {"label": "H&M", "x": 0.5, "y": 0.5}, {"label": "A", "x": 0.9, "y": 0.1}, {"label": "B", "x": 0.3, "y": 0.7}]}
    text = E.render_data("quadrant_chart", d)
    assert "0.12" not in text and "0.92" not in text
    assert "Shein — placed at the far left, at the very top" in text
    assert "H&M — placed at the horizontal centre, at mid-height" in text
    flows = E.render_data("sankey_diagram", {"flows": [{"source": "a", "target": "b", "weight": 5}]})
    assert "very thick band" in flows and " 5" not in flows


def test_prompt_title_has_no_quotes_and_forbids_callouts():
    p = build_diagram_prompt(FLOW, style_school="explanatory_narrative")
    assert "TITLE (render exactly this text once" in p and "“The State-Capital Playbook”" not in p
    assert "callout" in p.lower() and "insight" not in style_for_school("explanatory_narrative")["palette_description"].lower()
    assert "CATEGORICAL COLORS" in p
