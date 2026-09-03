"""Plates: the wall (families, density, lengths, leaks, grounding), the prompt assembly, the verdict rule,
the appendix partial and the store — no network."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.dossier import plates as PL  # noqa: E402
from src.dossier.plates import (  # noqa: E402
    Plate, PlateSpec, _attempt_score, _coerce_spec, build_plate_prompt, collect_plate_labels, content_labels, declutter_plate,
    extract_size_guides, leak_scan, plate_verdict_ok, prompt_content_section, render_appendix_html, revision_notes, validate_canonical,
    validate_plate_spec,
)
from src.dossier.walls import normalize  # noqa: E402

MATERIAL = normalize(
    "The AUKUS partnership routes contracts to Lockheed Martin and Raytheon Australia; Hanwha, Lynas and Fortescue follow. "
    "Microsoft's €976 m investment in Greece promised 300 jobs over 10 years; official proceedings count 12 FTE per data centre. "
    "Alcatel Submarine Networks (ASN) was nationalised for €350 m to save the Calais plant. HMN Tech lost SeaMeWe-6 to SubCom at $600M. "
    "BDC state venture capital in Canada. Vendor lock-in follows every case; sanctions exposure; reversal constraint; national security "
    "framing; modernisation; bipartisan consensus; fast-track regulation; sovereign capability; community promise; ITAR exemptions; "
    "procurement pipeline; Team Telecom; Greece 2.0 recovery plan; Strategic Investments framework; militarised neoliberalism; "
    "state capitalism; platform capitalism; infrastructural power; investment screening; empire; climate crisis."
)


def scorecard_canonical() -> dict:
    return {
        "quadrants": [
            {"label": "GAINS: What the State Announced", "tone": "gain", "items": [
                {"label": "Sovereign capability through AUKUS", "size": 0.9}, {"label": "300 jobs over 10 years in Greece", "size": 0.8},
                {"label": "Calais plant saved by ASN nationalisation", "size": 0.7}, {"label": "Modernisation via Greece 2.0", "size": 0.6}]},
            {"label": "LOSSES: What the Documents Show", "tone": "loss", "items": [
                {"label": "12 FTE per data centre", "size": 0.9}, {"label": "Vendor lock-in in every case", "size": 0.8},
                {"label": "HMN Tech excluded, SubCom at $600M", "size": 0.7}, {"label": "Reversal constraint on partners", "size": 0.6}]},
            {"label": "GAINS: Who Captured the Benefit", "tone": "gain", "items": [
                {"label": "Lockheed Martin and Raytheon Australia", "size": 0.9}, {"label": "Microsoft proprietary ecosystem", "size": 0.8},
                {"label": "Hanwha, Lynas and Fortescue", "size": 0.6}, {"label": "BDC state venture capital", "size": 0.5}]},
            {"label": "LOSSES: What Was Foreclosed", "tone": "loss", "items": [
                {"label": "Bipartisan consensus forecloses scrutiny", "size": 0.8}, {"label": "Fast-track regulation", "size": 0.7},
                {"label": "Sanctions exposure via ITAR exemptions", "size": 0.7}, {"label": "Community promise deferred", "size": 0.6}]},
        ],
        "marks": [{"quadrant": "GAINS: What the State Announced", "kind": "cross", "label": "Contradicted by the paperwork"}],
        "links": [{"from": "LOSSES: What the Documents Show", "to": "LOSSES: What Was Foreclosed", "label": "Compounding lock-in"}],
    }


def framework_canonical() -> dict:
    return {
        "regions": [
            {"label": "Militarised Neoliberalism", "note": "Wijaya and Hayes on AUKUS", "nodes": [
                {"label": "National Security Framing", "definition": "Corporate procurement presented as sovereign capability", "size": 0.9},
                {"label": "Procurement Pipeline", "definition": "Guaranteed contracts for Lockheed Martin and Raytheon Australia", "size": 0.8},
                {"label": "Bipartisan Consensus", "definition": "Cross-party agreement that forecloses scrutiny", "size": 0.7}]},
            {"label": "Platform Capitalism", "note": "Papaevangelou and Siapera on Greece", "nodes": [
                {"label": "Modernisation Promise", "definition": "Greece 2.0 recovery plan frames Microsoft as public upgrade", "size": 0.9},
                {"label": "Vendor Lock-in", "definition": "Proprietary ecosystem the state cannot leave", "size": 0.8},
                {"label": "Community Promise", "definition": "300 jobs announced, 12 FTE per data centre documented", "size": 0.7}]},
        ],
        "relations": [
            {"from": "National Security Framing", "to": "Procurement Pipeline", "label": "LICENSES"},
            {"from": "Bipartisan Consensus", "to": "Procurement Pipeline", "label": "PROTECTS"},
            {"from": "Modernisation Promise", "to": "Vendor Lock-in", "label": "CONCEALS"},
            {"from": "Vendor Lock-in", "to": "Community Promise", "label": "CONTRASTS WITH"},
        ],
        "bridges": [{"from": "Militarised Neoliberalism", "to": "Platform Capitalism", "label": "SAME PLAYBOOK, DIFFERENT SECTOR"}],
        "side_boxes": [{"label": "APPLICATIONS", "items": ["Investment screening", "Fast-track regulation", "Sanctions exposure"], "region": "Platform Capitalism"}],
    }


def spec(**over) -> PlateSpec:
    base = {
        "key": "who_wins", "family": "scorecard", "perspective": "Scorecard of announced versus documented",
        "title": "When Governments Say Strategic: The Scorecard", "abstraction_level": 3,
        "claimed_territory": "announced versus documented benefits", "excludes": ["the framework of concepts"],
        "why_this_perspective": "The material repeats one pattern; a scorecard shows it whole.",
        "narrative": "Read the panels left to right. The green panels list what was announced and who captured it. The red panels list what the documents show and what was foreclosed. The cross marks the announcements the paperwork contradicts.",
        "canonical": scorecard_canonical(),
    }
    base.update(over)
    return _coerce_spec(base, 1)


# ── families / shapes ────────────────────────────────────────────────────

def test_scorecard_shape_holds():
    assert validate_canonical("scorecard", scorecard_canonical()) == []


def test_framework_shape_holds():
    assert validate_canonical("framework_map", framework_canonical()) == []


@pytest.mark.parametrize("family,canonical,needle", [
    ("scorecard", {"quadrants": [{"label": "A", "tone": "gain", "items": [{"label": "x"}, {"label": "y"}]}]}, "at least 2"),
    ("scorecard", {"quadrants": [{"label": "A", "tone": "up", "items": [{"label": "x"}, {"label": "y"}]}, {"label": "B", "tone": "loss", "items": [{"label": "z"}, {"label": "w"}]}]}, "tone must be"),
    ("scorecard", {"quadrants": [{"label": "A", "tone": "gain", "items": [{"label": "x", "size": 3}, {"label": "y"}]}, {"label": "B", "tone": "loss", "items": [{"label": "z"}, {"label": "w"}]}]}, "size must be a NUMBER"),
    ("scorecard", {"quadrants": [{"label": "A", "tone": "gain", "items": [{"label": "x"}, {"label": "y"}]}, {"label": "B", "tone": "loss", "items": [{"label": "z"}, {"label": "w"}]}],
                   "links": [{"from": "A", "to": "Q", "label": "l"}]}, "links[0]"),
    ("framework_map", {"regions": [{"label": "R", "nodes": [{"label": "a"}, {"label": "b", "definition": "d"}]}], "relations": [{"from": "a", "to": "b", "label": "x"}, {"from": "b", "to": "a", "label": "y"}]}, "definition is required"),
    ("framework_map", {"regions": [{"label": "R", "nodes": [{"label": "a", "definition": "d"}, {"label": "b", "definition": "d"}]}], "relations": [{"from": "a", "to": "zz", "label": "x"}, {"from": "b", "to": "a", "label": "y"}]}, "relations[0]"),
    ("flow_map", {"current": {"label": "c", "stations": [{"label": "s1"}, {"label": "s2"}]}}, "at least 3"),
    ("flow_map", {"current": {"label": "c", "stations": [{"label": "s1"}, {"label": "s2"}, {"label": "s3"}]}, "branches": [{"label": "b", "from": "nope", "steps": ["x"], "terminal": "t"}]}, "branches[0]"),
    ("power_map", {"x_axis": {"label": "P", "low": "l", "high": "h"}, "y_axis": {"label": "I", "low": "l", "high": "h"}, "actors": [{"label": "a", "x": 2, "y": 0.5}] * 5}, "x and y NUMBERS"),
    ("timeline_of_shifts", {"events": [{"label": "no date"}, {"date": "1", "label": "b"}, {"date": "2", "label": "c"}, {"date": "3", "label": "d"}, {"date": "4", "label": "e"}]}, "date is required"),
    ("register", {"columns": [{"label": "ID", "kind": "text"}, {"label": "Certainty", "kind": "badge"}, {"label": "S", "kind": "glyph"}],
                  "rows": [{"label": "r", "cells": ["HIGH LIKELY VERY MUCH", "serial"]}, {"label": "r2", "cells": ["PROB", "serial"]}, {"label": "r3", "cells": ["POSS", "serial"]}]}, "badge: at most 3 words"),
    ("register", {"columns": [{"label": "ID", "kind": "text"}, {"label": "C", "kind": "badge"}, {"label": "S", "kind": "glyph"}],
                  "rows": [{"label": "r", "cells": ["HIGH", "sideways"]}, {"label": "r2", "cells": ["PROB", "serial"]}, {"label": "r3", "cells": ["POSS", "serial"]}]}, "glyph: one of"),
    ("register", {"columns": [{"label": "ID", "kind": "text"}, {"label": "C", "kind": "badge"}, {"label": "S", "kind": "glyph"}],
                  "rows": [{"label": "r", "cells": ["a", "HIGH", "serial"]}, {"label": "r2", "cells": ["PROB", "serial"]}, {"label": "r3", "cells": ["POSS", "serial"]}]}, "exactly 2 strings"),
    ("layer_stack", {"layers": [{"label": "a", "items": [{"label": "x"}]}, {"label": "b", "items": []}, {"label": "c", "items": [{"label": "y"}]}]}, "items must list 1-6"),
    ("argument_tree", {"claim": {"label": "c"}, "premises": [{"label": "p", "strength": 7}, {"label": "q"}]}, "strength must be a NUMBER"),
    ("nope", {"x": 1}, "not one of"),
])
def test_shape_rejections(family, canonical, needle):
    errors = validate_canonical(family, canonical)
    assert errors, f"{family} should have been rejected"
    assert any(needle in e for e in errors), errors


def test_family_aliases_normalize():
    assert PL.normalize_family("Risk Register") == "register"
    assert PL.normalize_family("flow of commitments") == "flow_map"
    assert PL.normalize_family("stakeholder power map") == "power_map"
    assert PL.normalize_family("SCORECARD") == "scorecard"
    assert PL.normalize_family("bridge") is None


def test_every_family_maps_to_an_enforcement_format_and_grammar():
    from src.display.enforcement import FORMAT_ENFORCEMENT

    for key, f in PL.PLATE_FAMILIES.items():
        assert f["format"] in FORMAT_ENFORCEMENT, key
        assert f["aspect"] in PL.ASPECTS, key
        assert len(f["grammar"]) >= 3, key
        assert "template" in f and "rule" in f and callable(f["validate"]) and callable(f["render"]), key
    assert "scorecard" in PL.families_text() and "register" in PL.families_text()


# ── density, lengths, leaks ──────────────────────────────────────────────

def test_density_floor_rejects_a_thin_plate():
    thin = {"quadrants": [{"label": "A", "tone": "gain", "items": [{"label": "x"}, {"label": "y"}]},
                          {"label": "B", "tone": "loss", "items": [{"label": "z"}, {"label": "w"}]}]}
    errors = validate_canonical("scorecard", thin)
    assert any("too thin for a plate" in e for e in errors)


def test_leaked_tokens_in_a_label_are_rejected():
    c = scorecard_canonical()
    c["quadrants"][0]["items"][0]["label"] = "Sovereign capability [SIZE_GUIDE: 0.9]"
    errors = validate_canonical("scorecard", c)
    assert any("leaked rendering tokens" in e for e in errors)
    c = scorecard_canonical()
    c["quadrants"][1]["items"][0]["note"] = "colour #1e40af badge"
    assert any("leaked" in e for e in validate_canonical("scorecard", c))
    c = scorecard_canonical()
    c["quadrants"][1]["items"][0]["label"] = "truncass to 100 chars"
    assert any("leaked" in e for e in validate_canonical("scorecard", c))


def test_ellipsis_and_over_long_strings_are_rejected():
    c = scorecard_canonical()
    c["quadrants"][0]["items"][0]["label"] = "Sovereign capability through…"
    assert any("ellipsis" in e for e in validate_canonical("scorecard", c))
    c = scorecard_canonical()
    c["quadrants"][0]["items"][0]["label"] = " ".join(["word"] * 25)
    assert any("label too long" in e for e in validate_canonical("scorecard", c))
    c = scorecard_canonical()
    c["quadrants"][0]["items"][0]["note"] = " ".join(["word"] * 25)
    assert any("note too long" in e for e in validate_canonical("scorecard", c))


def test_leak_scan_catches_the_three_client_bugs_and_spares_prose():
    assert leak_scan("Abolishing distinction [SIZE_GUIDE: 1.0]") == ["[SIZE_GUIDE: 1.0]"]
    assert leak_scan("closed... truncass to 100 chars")
    assert leak_scan("badge #1e40af") == ["#1e40af"]
    assert leak_scan("weight: 3") and leak_scan("0.85 confidence")
    assert leak_scan("300 jobs over 10 years; €976 m; 12 FTE per centre; SeaMeWe-6 at $600M; 78% strong; €1.5 billion; 2.36 MP") == []
    assert leak_scan("importance 0.75") == ["0.75"]


def test_size_guides_are_numbers_extracted_and_never_rendered():
    s = spec()
    errors, _ = validate_plate_spec(s, MATERIAL)
    assert errors == []
    assert s.size_guides["Sovereign capability through AUKUS"] == 0.9
    assert extract_size_guides({"items": [{"label": "a", "size": 2}]}) == {"a": 1.0}
    prompt = build_plate_prompt(s)
    content = prompt_content_section(prompt)
    assert leak_scan(content) == []
    assert "0.9" not in content and "SIZE_GUIDE" not in prompt
    assert "draw in very large type" in content and "draw in large type" in content


# ── the wall as a whole ──────────────────────────────────────────────────

def test_wall_accepts_a_grounded_spec_and_fills_defaults():
    s = spec()
    s.canonical["quadrants"][0]["items"][0]["note"] = " ".join(["over"] * 30)   # a marginal overrun is trimmed, not re-asked
    errors, grounding = validate_plate_spec(s, MATERIAL)
    assert errors == []
    assert len(s.canonical["quadrants"][0]["items"][0]["note"].split()) == PL.MAX_NOTE_WORDS and s.__dict__["_declutter"]["trimmed"] == 1
    assert s.visual_format == "structured_diagram" and s.aspect == "16:9"
    assert grounding["labels"] >= 16 and grounding["grounded"] >= grounding["content_labels"] * 0.4


def test_wall_rejects_ungrounded_and_bad_meta():
    s = spec()
    for qi, q in enumerate(s.canonical["quadrants"]):
        for j, it in enumerate(q["items"]):
            it["label"] = f"Quantum bagel harvest on Neptune {chr(65 + qi)}{chr(65 + j)}"
    errors, grounding = validate_plate_spec(s, MATERIAL)
    assert any("ungrounded" in e for e in errors) and grounding["fraction"] < 0.4
    s = spec(title="x" * 121)
    assert any("max 120" in e for e in validate_plate_spec(s, MATERIAL)[0])
    s = spec(narrative="One sentence only")
    assert any("narrative must be 3-5" in e for e in validate_plate_spec(s, MATERIAL)[0])
    s = spec(abstraction_level=9)
    assert any("abstraction_level" in e for e in validate_plate_spec(s, MATERIAL)[0])
    s = spec(family="bridge_diagram")
    assert any("family" in e for e in validate_plate_spec(s, MATERIAL)[0])


def test_coerce_spec_tolerates_string_canonical_and_excludes():
    raw = {"key": "A Plate!", "family": "Risk register", "canonical": json.dumps({"columns": []}), "excludes": "the rest", "abstraction_level": "4"}
    s = _coerce_spec(raw, 3)
    assert s.key == "a_plate" and s.canonical == {"columns": []} and s.excludes == ["the rest"] and s.abstraction_level == 4


def test_labels_walk_notes_cells_and_skip_controls():
    c = framework_canonical()
    labels = collect_plate_labels(c)
    assert "National Security Framing" in labels and "Corporate procurement presented as sovereign capability" in labels
    assert "LICENSES" in labels and "SAME PLAYBOOK, DIFFERENT SECTOR" in labels and "Investment screening" in labels
    assert "0.9" not in labels and "gain" not in labels
    assert "Corporate procurement presented as sovereign capability" not in content_labels(c)
    reg = {"columns": [{"label": "ID", "kind": "text"}, {"label": "C", "kind": "badge"}], "rows": [{"label": "r", "starred": True, "cells": ["HIGH"]}]}
    assert collect_plate_labels(reg) == ["ID", "C", "r", "HIGH"]


# ── declutter ────────────────────────────────────────────────────────────

def test_declutter_dedupes_trims_and_drops_lowest_size_beyond_cap():
    c = scorecard_canonical()
    c["quadrants"][0]["items"].append({"label": "Sovereign capability through AUKUS", "size": 0.1})   # exact repeat
    c["quadrants"][0]["items"][1]["note"] = " ".join(["long"] * 40)
    out, report = declutter_plate(c, "scorecard")
    assert report["deduped"] == 1 and report["trimmed"] == 1
    assert len(out["quadrants"][0]["items"]) == 4
    fw = framework_canonical()
    fw["relations"].append({"from": "National Security Framing", "to": "Nowhere Node", "label": "DANGLES"})
    out, report = declutter_plate(fw, "framework_map")
    assert len(out["relations"]) == 4 and report["dropped"][0]["why"] == "dangling endpoint"
    big = {"quadrants": [{"label": f"Q{i}", "tone": "gain", "items": [{"label": f"item {i} {j}", "size": j / 40} for j in range(40)]} for i in range(4)]}
    out, report = declutter_plate(big, "scorecard")
    assert len(collect_plate_labels(out)) <= PL.MAX_TEXT_ELEMENTS
    assert report["dropped"] and report["dropped"][0]["label"].endswith(" 0")


# ── prompt assembly (v1's order) ─────────────────────────────────────────

def test_prompt_order_and_blocks():
    s = spec()
    validate_plate_spec(s, MATERIAL)
    s.style_school = "explanatory_narrative"
    p = build_plate_prompt(s)
    i = {k: p.find(k) for k in ("READ FIRST", "MANDATORY FORMAT", "PLATE LAYOUT GRAMMAR", "MANDATORY STYLE OVERRIDE", "CONTENT TO RENDER",
                                "LABEL MANIFEST", "TITLE (render exactly", "TEXT RULES", "FRAME:", "DENSITY:", "FINAL REMINDER", "FINAL STYLE OVERRIDE")}
    assert all(v >= 0 for v in i.values()), i
    order = ["READ FIRST", "MANDATORY FORMAT", "PLATE LAYOUT GRAMMAR", "MANDATORY STYLE OVERRIDE", "CONTENT TO RENDER", "LABEL MANIFEST",
             "TITLE (render exactly", "TEXT RULES", "FRAME:", "DENSITY:", "FINAL REMINDER", "FINAL STYLE OVERRIDE"]
    assert [i[k] for k in order] == sorted(i[k] for k in order)
    assert "STRUCTURED ORGANIZATIONAL DIAGRAM" in p and "green band" in p
    for lab in collect_plate_labels(s.canonical):
        assert f"• {lab}" in p
    assert "compose for a 16:9 aspect ratio at 4K" in p
    assert "Physical objects as containers" in p          # GLOBAL_PROHIBITIONS
    assert "NEVER show any bracketed annotations" in p     # v1 preamble
    assert "When Governments Say Strategic: The Scorecard" in p


def test_prompt_revision_notes_and_register_grammar():
    s = spec()
    validate_plate_spec(s, MATERIAL)
    p = build_plate_prompt(s, revision_notes=["Spell exactly “Raytheon Australia”", ""])
    assert "REVISION NOTES" in p and "! Spell exactly “Raytheon Australia”" in p
    reg = PlateSpec(key="reg", family="register", title="Argument Architecture: 7 Arguments → 1 Master Conclusion",
                    narrative="Read down the rows. Each row is one argument. Badges grade certainty and type.",
                    canonical={"columns": [{"label": "ID", "kind": "text"}, {"label": "Certainty", "kind": "badge"}, {"label": "Structure", "kind": "glyph"},
                                           {"label": "Premises", "kind": "number"}, {"label": "Strength", "kind": "bar"}],
                               "rows": [{"label": f"Argument {i}", "starred": i == 1, "cells": ["HIGH", "serial", "3", f"{70 + i}%"]} for i in range(1, 5)],
                               "legend": [{"badge": "HIGH", "meaning": "Highly likely"}]})
    errors, _ = validate_plate_spec(reg, "")
    assert errors == [], errors
    p = build_plate_prompt(reg)
    assert "dark navy header band" in p and "glyph icon →→ (serial)" in p and "strength bar 71%" in p and "★" in p
    assert "MATRIX" in p and reg.aspect == "3:4"


def test_prompt_refuses_a_broken_spec():
    s = spec()
    s.canonical = {"quadrants": []}
    with pytest.raises(ValueError):
        build_plate_prompt(s)
    with pytest.raises(ValueError):
        build_plate_prompt(PlateSpec(key="x", family="nope", title="t", canonical=scorecard_canonical()))


# ── verdict rule + revision notes ────────────────────────────────────────

def test_plate_verdict_rules():
    base = {"format_ok": True, "prohibited_elements": [], "leaked_tokens": [], "extra_text": [], "density": "dense",
            "labels_missing": [], "misspelled": [], "illegible": []}
    assert plate_verdict_ok(base, 40)
    assert not plate_verdict_ok({**base, "format_ok": False}, 40)
    assert not plate_verdict_ok({**base, "leaked_tokens": ["[SIZE_GUIDE: 0.9]"]}, 40)
    assert not plate_verdict_ok({**base, "density": "sparse — half the canvas empty"}, 40)
    assert not plate_verdict_ok({**base, "extra_text": ["this sentence was invented by the model"]}, 40)
    assert plate_verdict_ok({**base, "labels_missing": ["a"] * 8}, 40)
    assert not plate_verdict_ok({**base, "labels_missing": ["a"] * 9}, 40)
    assert plate_verdict_ok({**base, "illegible": ["a", "b"]}, 5)
    assert not plate_verdict_ok({**base, "illegible": ["a", "b", "c"]}, 5)


def test_revision_notes_name_leaks_and_sparseness():
    notes = revision_notes({"format_ok": True, "leaked_tokens": ["#1e40af"], "density": "sparse", "labels_missing": ["Raytheon Australia"],
                            "misspelled": [{"expected": "Lynas", "seen": "Lynus"}], "title_found": True, "legible_at_4k": False, "suggestion": "bigger"})
    text = "\n".join(notes)
    assert "REMOVE the leaked token “#1e40af”" in text and "SPARSE" in text and "Raytheon Australia" in text and "Lynus" in text
    assert "Increase every text size" in text and notes[-1] == "bigger"
    assert _attempt_score({"checked": True, "format_ok": True, "leaked_tokens": [], "prohibited_elements": [], "density": "dense", "labels_missing": []}) < \
           _attempt_score({"checked": True, "format_ok": True, "leaked_tokens": ["x"], "prohibited_elements": [], "density": "dense", "labels_missing": []})
    assert _attempt_score(None) == (1, 1, 999, 1)


# ── appendix partial + store ─────────────────────────────────────────────

def _plate(status="generated", ok=True) -> Plate:
    s = spec()
    validate_plate_spec(s, MATERIAL)
    return Plate(**s.model_dump(), status=status, path="/tmp/x/who_wins.jpg", url="/v1/dossier/jobs/j/plates/who_wins.jpg", width=5504, height=3072,
                 compliance={"checked": True, "ok": ok, "labels_found": ["a"] * 18, "n_labels": 19, "issues": [] if ok else ["2 string(s) missing: x"]},
                 attempts=[{"n": 1}], cost_usd=0.24)


def test_appendix_partial_renders_generated_plates_only():
    html = render_appendix_html([_plate(), _plate(status="failed")], src_for=lambda p: f"/img/{p.key}.jpg")
    assert html.count("<figure class=\"plate\"") == 1
    assert "Plate 1" in html and "When Governments Say Strategic: The Scorecard" in html and "/img/who_wins.jpg" in html
    assert "Read the panels left to right" in html and "passed — 18/19 strings found" in html and "scorecard (structured diagram)" in html
    assert render_appendix_html([]) .strip() == ""
    assert "flagged — 2 string(s) missing" in render_appendix_html([_plate(ok=False)])


@pytest.fixture
def sqlite_db(tmp_path, monkeypatch):
    from src.dossier import plate_store
    from src.executor import db as executor_db

    monkeypatch.setattr(executor_db, "DATABASE_URL", "")
    monkeypatch.setattr(executor_db, "SQLITE_PATH", tmp_path / "plates-test.db")
    monkeypatch.setattr(executor_db, "_initialized", False)
    plate_store.reset_for_tests()
    yield plate_store
    plate_store.reset_for_tests()


def test_store_upsert_list_get_delete_and_run_registry(sqlite_db):
    st = sqlite_db
    p = _plate()
    st.upsert_plate("job-1", Plate(**p.model_dump(exclude={"status", "path", "url", "compliance", "attempts", "cost_usd"}), status="planned"))
    assert [x.status for x in st.list_plates("job-1")] == ["planned"]
    st.upsert_plate("job-1", p)
    rows = st.list_plates("job-1")
    assert len(rows) == 1 and rows[0].status == "generated" and rows[0].width == 5504 and rows[0].compliance["ok"] is True
    assert rows[0].canonical == p.canonical and rows[0].size_guides == p.size_guides and rows[0].narrative == p.narrative
    assert st.get_plate("job-1", "who_wins").title == p.title and st.get_plate("job-1", "nope") is None
    assert st.list_plates("job-2") == []
    assert st.mark_running("job-1", 2) and not st.mark_running("job-1", 1)
    assert st.run_state("job-1")["n"] == 2
    st.mark_done("job-1")
    assert st.run_state("job-1") is None
    assert st.delete_plates("job-1") == 1 and st.list_plates("job-1") == []
