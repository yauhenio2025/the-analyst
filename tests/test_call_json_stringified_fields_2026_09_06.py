"""A tool answer whose array field arrived as a string (2026-09-06: Sonnet returned a spine's sections as a 10K-char
JSON string with a broken quote near its end; the spine coerced it to no sections and compose crashed on it).
The call path salvages what parses, re-asks when a schema field is still a string, and never hands a desk a string."""
import json
from pathlib import Path

import pytest

from src.dossier import llm
from src.dossier.llm import _parse_embedded_json, _salvage_array, stringified_fields, unstringify

FIX = json.loads((Path(__file__).parent / "fixtures/stringified_sections_2026_09_06.json").read_text())["sections"]
SCHEMA = {"type": "object", "properties": {"thesis": {"type": "string"},
                                           "sections": {"type": "array", "items": {"type": "object", "properties": {"key": {"type": "string"}}}}}}


def test_the_real_broken_string_is_salvaged_to_its_complete_elements():
    with pytest.raises(json.JSONDecodeError):
        json.loads(FIX)                                                          # the tail is malformed
    parsed = _parse_embedded_json(FIX)
    assert isinstance(parsed, list) and len(parsed) >= 3 and all(isinstance(s, dict) and s.get("key") for s in parsed)
    assert parsed[0]["key"] == "corpus_orientation"


def test_salvage_cuts_at_the_last_complete_element_and_invents_nothing():
    broken = '[{"key": "a", "claim": "one"}, {"key": "b", "claim": "two"}, {"key": "c", "claim": "thr'
    assert _salvage_array(broken) == [{"key": "a", "claim": "one"}, {"key": "b", "claim": "two"}]
    assert _salvage_array("not an array") is None and _salvage_array("[{") is None


def test_unstringify_and_stringified_fields_agree():
    raw = {"thesis": "t", "sections": '[{"key": "x"}]'}
    assert unstringify(raw, SCHEMA) == {"thesis": "t", "sections": [{"key": "x"}]}
    assert stringified_fields({"thesis": "t", "sections": "garbage"}, SCHEMA) == ["sections"]
    assert stringified_fields({"thesis": "t", "sections": [{"key": "x"}]}, SCHEMA) == []


def test_call_json_re_asks_when_a_field_is_still_a_string_and_returns_the_repaired_answer(monkeypatch):
    answers = iter([({"thesis": "t", "sections": "garbage that is not json"}, {}), ({"thesis": "t", "sections": [{"key": "x"}]}, {})])
    seen_tails = []
    def fake(_attempt, chosen_model):
        return next(answers)
    monkeypatch.setattr(llm, "_with_refusal_fallback", fake)
    monkeypatch.setattr(llm.events, "emit", lambda *a, **k: seen_tails.append(k.get("detail", "")))
    monkeypatch.setattr(llm, "_pick_model", lambda *a, **k: "claude-sonnet-4-6", raising=False)
    raw, _ = llm.call_json("j", "spine", label="spine", system="s", user="u", tool_name="t", schema=SCHEMA, model_cls=None, repair_attempts=1)
    assert raw == {"thesis": "t", "sections": [{"key": "x"}]}
    assert any("must be JSON arrays/objects" in d for d in seen_tails)


def test_call_json_raises_rather_than_hand_a_desk_a_string(monkeypatch):
    monkeypatch.setattr(llm, "_with_refusal_fallback", lambda _a, m: ({"thesis": "t", "sections": "still garbage"}, {}))
    monkeypatch.setattr(llm.events, "emit", lambda *a, **k: None)
    monkeypatch.setattr(llm, "_pick_model", lambda *a, **k: "claude-sonnet-4-6", raising=False)
    with pytest.raises(llm.LLMError):
        llm.call_json("j", "spine", label="spine", system="s", user="u", tool_name="t", schema=SCHEMA, model_cls=None, repair_attempts=0)


def test_compose_tolerates_string_sections():
    from src.dossier import compose
    from src.dossier.schemas import DossierJob
    from src.sources.schemas import Document
    job = DossierJob(id="d1")
    raw = {"title": "T", "subtitle": "s", "executive_summary": ["e"], "sections": ["A whole section as prose.", {"heading": "H", "paragraphs": ["p"], "claims": ["not a dict"]}], "conclusion": ["c"]}
    import src.dossier.compose as c
    orig = c.call_json
    c.call_json = lambda *a, **k: (raw, {})
    c.events.emit = lambda *a, **k: None
    try:
        out = c.write_sections(job, [Document(key="k", title="t", text="p", char_count=1)])
    finally:
        c.call_json = orig
    assert [s.heading for s in out.sections] == ["Section 1", "H"] and out.sections[0].paragraphs == ["A whole section as prose."]
