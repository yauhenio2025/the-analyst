"""FigureSpec wall: data shapes per family, label length, grounding, style choice, records (no network)."""
from __future__ import annotations

import json

import pytest

from src.display import enforcement as E
from src.dossier.figures import (
    _attempt_score,
    _coerce_spec,
    _revision_notes,
    choose_style_school,
    label_in_material,
    validate_spec,
)
from src.dossier.schemas import DossierJob, Figure, FigureSpec
from src.dossier.walls import normalize

MATERIAL = normalize(
    "The AUKUS partnership routes contracts to Lockheed Martin and Raytheon Australia. Microsoft's €976 m investment in "
    "Greece promised 300 jobs over 10 years; the environmental assessment counts 12 FTE per data centre. "
    "Alcatel Submarine Networks (ASN) was nationalised for €350 m. Vendor lock-in follows every case. "
    "Governments frame each deal as national security and digital modernisation."
)


def spec(**over) -> FigureSpec:
    base = {
        "key": "who_wins", "primitive": "flow_transformation", "visual_format": "sankey",
        "title": "Where the Public Money Goes", "caption": "Announcements route funds to a short list of firms.",
        "why_this_format": "flows with magnitude",
        "data": {"flows": [{"source": "AUKUS", "target": "Lockheed Martin", "weight": 4},
                           {"source": "AUKUS", "target": "Raytheon Australia", "weight": 3},
                           {"source": "Greece", "target": "Microsoft", "weight": 5, "label": "€976 m"}]},
        "anchors": [{"label": "Lockheed Martin", "quote": "routes contracts to Lockheed Martin and Raytheon Australia", "source": "analysis"}],
    }
    base.update(over)
    return _coerce_spec(base, 1)


# ── shapes ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("fmt,data,ok", [
    ("flowchart", {"steps": [{"label": "A"}, {"label": "B"}, {"label": "C"}]}, True),
    ("flowchart", {"steps": [{"label": "A"}, {"label": "B"}]}, False),
    ("flowchart", {"steps": [{"label": "A"}, {"label": "B"}, {"label": "C"}], "branches": [{"from": "A", "label": "yes", "to": "Z"}]}, False),
    ("venn_diagram", {"sets": [{"label": "A"}, {"label": "B"}], "intersections": [{"of": ["A", "B"], "label": "shared"}]}, True),
    ("venn_diagram", {"sets": [{"label": "A"}, {"label": "B"}], "intersections": []}, False),
    ("venn_diagram", {"sets": [{"label": "A"}, {"label": "B"}], "intersections": [{"of": ["A", "Q"], "label": "x"}]}, False),
    ("quadrant_chart", {"x_axis": {"label": "Power", "low": "Low", "high": "High"}, "y_axis": {"label": "Interest", "low": "Low", "high": "High"},
                        "items": [{"label": f"I{i}", "x": 0.1 * i, "y": 0.5} for i in range(1, 6)]}, True),
    ("quadrant_chart", {"x_axis": {"label": "Power", "low": "Low", "high": "High"}, "y_axis": {"label": "Interest"},
                        "items": [{"label": f"I{i}", "x": 0.1 * i, "y": 0.5} for i in range(1, 6)]}, False),
    ("quadrant_chart", {"x_axis": {"label": "Power", "low": "Low", "high": "High"}, "y_axis": {"label": "Interest", "low": "Low", "high": "High"},
                        "items": [{"label": "I1", "x": 3, "y": 0.5}] * 4}, False),
    ("timeline", {"events": [{"date": "2021", "label": "AUKUS announced"}, {"date": "2023", "label": "Delay"}, {"date": "2025", "label": "Review"}]}, True),
    ("timeline", {"events": [{"label": "no date"}, {"date": "2023", "label": "b"}, {"date": "2025", "label": "c"}]}, False),
    ("sankey_diagram", {"flows": [{"source": "a", "target": "b", "weight": 9}] * 3}, False),
    ("network_graph", {"nodes": [{"label": "a"}, {"label": "b"}, {"label": "c"}, {"label": "d"}],
                       "edges": [{"source": "a", "target": "b"}, {"source": "b", "target": "c"}, {"source": "c", "target": "zz"}]}, False),
    ("cycle_diagram", {"stages": [{"label": "a"}, {"label": "b"}, {"label": "c"}, {"label": "d"}], "links": [{"from": "a", "to": "b", "polarity": "+"}]}, True),
    ("matrix", {"rows": ["r1", "r2"], "columns": ["c1", "c2", "c3"], "cells": [["1", "2", "3"], ["4", "5", "6"]]}, True),
    ("matrix", {"rows": ["r1", "r2"], "columns": ["c1", "c2", "c3"], "cells": [["1", "2"], ["4", "5", "6"]]}, False),
    ("grouped_bar_chart", {"rows": ["Greece", "AUKUS"], "columns": ["Announced", "Documented"], "cells": [["300 jobs", "12 FTE"], ["1,200", "0"]]}, True),
    ("grouped_bar_chart", {"rows": ["Greece", "AUKUS"], "columns": ["Announced", "Documented"], "cells": [["300 jobs", "12 FTE"], ["Maximise jobs", "Diffuse"]]}, False),
    ("argument_tree", {"claim": "The deals are hollow", "premises": [{"label": "Jobs overstated", "evidence": ["12 FTE per data centre"]}, {"label": "Vendor lock-in"}]}, True),
    ("argument_tree", {"claim": "x", "premises": [{"label": "one"}]}, False),
    ("hierarchical_tree", {"root": {"label": "State", "children": [{"label": "Defence", "children": [{"label": "AUKUS"}]}, {"label": "Digital"}]}}, True),
    ("hierarchical_tree", {"root": {"label": "State"}}, False),
    ("conceptual_layers", {"layers": [{"label": "Surface claim"}, {"label": "Policy frame"}, {"label": "Fiscal mechanism", "items": ["subsidy", "guarantee"]}]}, True),
    ("two_column_split", {"columns": [{"label": "Promised", "items": ["300 jobs"]}, {"label": "Documented", "items": ["12 FTE"]}]}, True),
    ("concentric_circles", {"center": "Prime contractor", "rings": [{"label": "Tier 1", "items": ["a"]}, {"label": "Periphery", "items": ["b", "c"]}]}, True),
    ("spectrum_gradient", {"axis": {"label": "Sovereignty", "low": "Dependent", "high": "Sovereign"}, "items": [{"label": "a", "position": 0.1}, {"label": "b", "position": 0.5}, {"label": "c", "position": 0.9}]}, True),
    ("bar_chart", {"measure": "Jobs", "categories": [{"label": "Announced", "value": "300"}, {"label": "Documented", "value": "12"}, {"label": "Other", "value": "0"}]}, True),
    ("bar_chart", {"measure": "Jobs", "categories": [{"label": "Announced", "value": "many"}, {"label": "Documented", "value": "12"}, {"label": "Other", "value": "0"}]}, False),
    ("force_field", {"change": "Nationalise ASN", "driving": [{"label": "Security", "strength": 4}, {"label": "Jobs", "strength": 2}],
                     "restraining": [{"label": "Cost €350 m", "strength": 3}, {"label": "EU rules", "strength": 2}]}, True),
    ("dialectical_map", {"thesis": "National interest", "antithesis": "Corporate capture", "tensions": ["who pays"], "synthesis": "Militarised neoliberalism"}, True),
    ("semiotic_square", {"s1": "Sovereign", "s2": "Dependent", "not_s1": "Not sovereign", "not_s2": "Not dependent"}, True),
    ("scenario_cone", {"present": "2026 review", "futures": [{"label": "Delivered", "likelihood": "low"}, {"label": "Delayed", "likelihood": "high"}]}, True),
    ("indicator_dashboard", {"indicators": [{"label": "Jobs", "status": "red"}, {"label": "Cost", "status": "amber"}, {"label": "Delivery", "status": "purple"}]}, False),
    ("waterfall_chart", {"start": {"label": "Announced", "value": "300"}, "changes": [{"label": "Construction only", "delta": "-200"}, {"label": "Outsourced", "delta": "-88"}], "end": {"label": "Documented", "value": "12"}}, True),
])
def test_family_validators(fmt, data, ok):
    errors = E.validate_data(fmt, data)
    assert (not errors) == ok, errors


def test_label_length_and_empty_data():
    assert E.validate_data("flowchart", {}) == ["data must be a non-empty object"]
    long = {"steps": [{"label": "This label has far too many words in it"}, {"label": "B"}, {"label": "C"}]}
    errs = E.validate_data("flowchart", long)
    assert any("label too long" in x for x in errs)
    assert E.validate_data("oil_painting", {"x": 1}) == ["unknown visual_format 'oil_painting'"]


def test_collect_and_content_labels():
    d = {"x_axis": {"label": "Power", "low": "Low", "high": "High"}, "y_axis": {"label": "Interest", "low": "Low", "high": "High"},
         "quadrants": {"top_right": "Key players"}, "items": [{"label": "Lockheed Martin", "x": 0.9, "y": 0.9, "group": "defence", "note": "not rendered"}]}
    assert E.collect_labels(d) == ["Power", "Low", "High", "Interest", "Key players", "Lockheed Martin"]
    assert E.content_labels(d) == ["Lockheed Martin"]
    assert "not rendered" not in E.render_data("quadrant_chart", d)
    assert "Item: Lockheed Martin — placed at the far right, at the very top, group: defence" in E.render_data("quadrant_chart", d)


# ── the wall ──────────────────────────────────────────────────────────────

def test_wall_accepts_grounded_spec_and_canonicalizes():
    s = spec()
    errors, g = validate_spec(s, MATERIAL)
    assert errors == []
    assert s.visual_format == "sankey_diagram" and s.key == "who_wins"
    assert g["anchors_verified"] == 1 and g["grounded"] == g["content_labels"] and g["fraction"] == 1.0
    assert s.anchors[0].verified is True


def test_wall_rejects_bad_format_primitive_title_and_caption_digits():
    s = spec(visual_format="watercolor", primitive="vibes", title="x" * 80, caption="Delivers 999 jobs.")
    errors, _ = validate_spec(s, MATERIAL)
    joined = " | ".join(errors)
    assert "not in the catalog" in joined and "primitive 'vibes'" in joined
    assert "title is 80 chars" in joined and "caption uses the number '999'" in joined


def test_wall_rejects_ungrounded_content():
    s = spec(data={"flows": [{"source": "Acme Corp", "target": "Zorblax Industries", "weight": 4},
                             {"source": "Acme Corp", "target": "Quux Holdings", "weight": 3},
                             {"source": "Foo", "target": "Bar", "weight": 2}]},
             anchors=[{"label": "Acme Corp", "quote": "not in the material", "source": "analysis"}])
    errors, g = validate_spec(s, MATERIAL)
    assert any(e.startswith("ungrounded") for e in errors)
    assert g["anchors_verified"] == 0 and g["grounded"] == 0
    assert g["anchors_failed"][0]["label"] == "Acme Corp"


def test_wall_grounding_allows_paraphrase_of_material_words_only():
    assert label_in_material("Raytheon Australia", MATERIAL)
    assert label_in_material("Vendor lock-in follows", MATERIAL)
    assert label_in_material("National security frame", MATERIAL)     # paraphrase from the material's own words
    assert not label_in_material("Security framing", MATERIAL)        # 'framing' is not a word of the material
    assert not label_in_material("Burger King activism", MATERIAL)
    assert not label_in_material("12 FTE per warehouse", MATERIAL)
    assert label_in_material("€976 m", MATERIAL)


def test_wall_structural_labels_need_no_grounding():
    s = spec(visual_format="quadrant_chart", primitive="comparative_positioning",
             data={"x_axis": {"label": "Sovereignty Gained", "low": "None", "high": "Full"},
                   "y_axis": {"label": "Public Money Spent", "low": "Little", "high": "Vast"},
                   "quadrants": {"top_left": "Hollow Wins", "bottom_right": "Cheap Gains"},
                   "items": [{"label": "AUKUS", "x": 0.2, "y": 0.9}, {"label": "Microsoft Greece", "x": 0.3, "y": 0.6},
                             {"label": "ASN nationalised", "x": 0.7, "y": 0.5}, {"label": "Lockheed Martin", "x": 0.1, "y": 0.8}]})
    errors, g = validate_spec(s, MATERIAL)
    assert errors == []
    assert g["content_labels"] == 4 and g["labels"] == 12


def test_coerce_spec_unpacks_stringified_data_and_snakes_keys():
    raw = {"key": "Who Wins?", "primitive": "network_influence", "visual_format": "network",
           "title": "t", "caption": "c", "why_this_format": "w",
           "data": json.dumps({"nodes": [{"label": "a"}], "edges": []}), "anchors": [{"label": "a", "quote": "q", "source": "TABLE"}]}
    s = _coerce_spec(raw, 3)
    assert s.key == "who_wins" and s.primitive == "network_influence" and s.data["nodes"][0]["label"] == "a"
    assert s.anchors[0].source == "table"
    assert _coerce_spec({}, 7).key == "figure_7"


# ── style, records, retry bookkeeping ─────────────────────────────────────

def _job(audience="executive", engines=("structural_pattern_detector",)) -> DossierJob:
    return DossierJob.model_validate({
        "options": {"audience": audience},
        "plan": {"phases": [{"phase_number": 4.1, "engine_key": e} for e in engines]},
    })


def test_choose_style_school_uses_affinities():
    assert choose_style_school(_job("executive", ("argument_architecture",)), "flowchart") == "explanatory_narrative"
    assert choose_style_school(_job("researcher", ("citation_network",)), "network_graph") == "emergent_systems"
    assert choose_style_school(_job("analyst", ("stakeholder_power_interest",)), "quadrant_chart") in ("restrained_elegance", "minimalist_precision")


def test_figure_record_carries_spec_fields_and_loads_old_records():
    fig = Figure(**spec().model_dump(), aspect="16:9", attempts=[{"n": 1, "kept": True}])
    d = fig.model_dump()
    for k in ("primitive", "visual_format", "title", "data", "why_this_format", "style_school", "compliance", "attempts", "grounding", "anchors"):
        assert k in d
    assert fig.status == "planned" and fig.labels() == ["AUKUS", "Lockheed Martin", "Raytheon Australia", "Greece", "Microsoft", "€976 m"]
    old = {"key": "k", "caption": "c", "scene": "a wooden table", "visual_register": "editorial", "status": "generated",
           "url": "/v1/figures/x", "compliance": {"ok": False}}
    legacy = Figure.model_validate(old)
    assert legacy.scene == "a wooden table" and legacy.visual_format == "" and legacy.attempts == []


def test_attempt_scoring_prefers_fewer_missing_labels_then_format():
    a = {"checked": True, "format_ok": True, "prohibited_elements": [], "labels_missing": ["x", "y"], "misspelled": [], "illegible": []}
    b = {"checked": True, "format_ok": True, "prohibited_elements": [], "labels_missing": ["x"], "misspelled": [], "illegible": []}
    c = {"checked": True, "format_ok": False, "prohibited_elements": [], "labels_missing": [], "misspelled": [], "illegible": []}
    assert min([a, b, c], key=_attempt_score) is b
    assert _attempt_score(None) == (1, 999, 1)


def test_revision_notes_from_verdict():
    notes = _revision_notes({"format_ok": False, "detected_format": "a painting of a bridge", "prohibited_elements": ["bridge"],
                             "labels_missing": ["Lockheed Martin"], "misspelled": [{"expected": "Raytheon", "seen": "Raytheen"}],
                             "illegible": [], "extra_text": ["Source: FT"], "title_found": False, "suggestion": "Use boxes."})
    joined = "\n".join(notes)
    assert "NOT the required format" in joined and "Remove: bridge" in joined
    assert "MISSING — render each of them: Lockheed Martin" in joined
    assert "Spell exactly “Raytheon”" in joined and "Source: FT" in joined and "title was missing" in joined and "Use boxes." in joined


# ── render_figure with stubbed provider + checker: the retry loop, files, receipts ──

def test_render_figure_retries_once_keeps_better_attempt_and_records_both(tmp_path, monkeypatch):
    import src.dossier.figures as F
    from src.images import adapter as A
    from src.images import compliance as C

    calls = {"render": [], "check": 0}
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 64

    class R:
        def __init__(self, n):
            self.image_bytes = png + bytes([n]); self.mime_type = "image/png"; self.provider = "gemini_pro"
            self.model = "gemini-3-pro-image-preview"; self.cost_usd = 0.134; self.prompt_sent = "p"

    def fake_generate(prompt, **kw):
        calls["render"].append(prompt)
        assert kw["no_text"] is False and kw["size"] == "2K" and kw["aspect"] == "16:9"
        return R(len(calls["render"]))

    def fake_check(image_bytes, spec, **kw):
        calls["check"] += 1
        base = {"checked": True, "model": "claude-sonnet-4-6", "usage": {"input_tokens": 1000, "output_tokens": 100},
                "n_labels": 6, "prohibited_elements": [], "misspelled": [], "illegible": [], "extra_text": [],
                "title_found": True, "confidence": "high", "detected_format": "sankey"}
        if calls["check"] == 1:
            return {**base, "ok": False, "format_ok": True, "labels_found": ["AUKUS"],
                    "labels_missing": ["Lockheed Martin", "Raytheon Australia", "Greece"], "suggestion": "bigger labels",
                    "issues": ["3 label(s) missing"]}
        return {**base, "ok": True, "format_ok": True, "labels_found": ["AUKUS", "Lockheed Martin"], "labels_missing": [],
                "suggestion": None, "issues": []}

    monkeypatch.setattr(A, "generate_image", fake_generate)
    monkeypatch.setattr(C, "check_diagram", fake_check)
    monkeypatch.setenv("FIGURES_DIR", str(tmp_path / "store"))
    receipts = []
    monkeypatch.setattr(F, "record", lambda job_id, r: receipts.append(r))

    job = DossierJob.model_validate({"id": "t-job", "options": {"audience": "executive"}})
    s = spec()
    s.style_school = "minimalist_precision"
    s.__dict__["_grounding"] = {"grounded": 6}
    out = tmp_path / "figs"; out.mkdir()
    fig = F.render_figure(job, s, out)

    assert len(calls["render"]) == 2 and calls["check"] == 2
    assert "REVISION NOTES" not in calls["render"][0] and "REVISION NOTES" in calls["render"][1]
    assert "These labels were MISSING — render each of them: Lockheed Martin; Raytheon Australia; Greece" in calls["render"][1]
    assert fig.status == "generated" and fig.compliance["ok"] is True and fig.aspect == "16:9"
    assert [a["n"] for a in fig.attempts] == [1, 2] and [a["kept"] for a in fig.attempts] == [False, True]
    assert fig.cost_usd == pytest.approx(0.268) and fig.grounding == {"grounded": 6}
    assert (out / "who_wins.attempt1.png").exists() and (out / "who_wins.attempt2.png").exists()
    assert (out / "who_wins.png").read_bytes() == (out / "who_wins.attempt2.png").read_bytes()
    assert fig.path == str(out / "who_wins.png") and fig.figure_id and fig.url == f"/v1/figures/{fig.figure_id}"
    kinds = [(r.kind, r.label) for r in receipts]
    assert ("image", "figure who_wins (attempt 1)") in kinds and ("image", "figure who_wins (attempt 2)") in kinds
    assert sum(1 for r in receipts if r.kind == "llm") == 2       # one vision check per attempt
    assert all("prompt" not in a for a in fig.attempts)             # prompts live on the sidecars, not the job row


def test_render_figure_keeps_first_attempt_when_second_is_worse(tmp_path, monkeypatch):
    import src.dossier.figures as F
    from src.images import adapter as A
    from src.images import compliance as C

    n = {"r": 0, "c": 0}
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 64

    class R:
        def __init__(self):
            n["r"] += 1
            self.image_bytes = png + bytes([n["r"]]); self.mime_type = "image/png"; self.provider = "gemini_pro"
            self.model = "m"; self.cost_usd = 0.1; self.prompt_sent = "p"

    monkeypatch.setattr(A, "generate_image", lambda prompt, **kw: R())

    def fake_check(image_bytes, spec, **kw):
        n["c"] += 1
        missing = ["a", "b"] if n["c"] == 1 else ["a", "b", "c", "d"]
        return {"checked": True, "ok": False, "format_ok": True, "prohibited_elements": [], "misspelled": [], "illegible": [],
                "labels_missing": missing, "labels_found": [], "extra_text": [], "issues": ["missing"], "usage": None,
                "model": "x", "n_labels": 6, "title_found": True, "suggestion": None}

    monkeypatch.setattr(C, "check_diagram", fake_check)
    monkeypatch.setenv("FIGURES_DIR", str(tmp_path / "store"))
    monkeypatch.setattr(F, "record", lambda *a: None)
    job = DossierJob.model_validate({"id": "t-job2", "options": {"audience": "analyst"}})
    out = tmp_path / "figs"; out.mkdir()
    fig = F.render_figure(job, spec(), out)
    assert [a["kept"] for a in fig.attempts] == [True, False]
    assert (out / "who_wins.png").read_bytes() == (out / "who_wins.attempt1.png").read_bytes()
    assert fig.note.startswith("compliance:") and fig.status == "generated"
