"""Answer-repair law: stringified array/object tool fields are unpacked against the schema."""
import json

from src.dossier.llm import _inline_defs, unstringify
from src.dossier.reconnaissance import RECON_SCHEMA
from src.dossier.schemas import Reconnaissance


def test_stringified_profiles_are_unpacked_and_validate():
    profiles = [{"doc_key": "A", "title": "T", "genre": "g", "one_line": "o", "thesis": "t", "method": "m",
                 "key_claims": [{"claim": "c", "anchor": {"doc_key": "A", "quote": "verbatim words here"}}],
                 "entities": ["x"], "tensions": []}]
    raw = {"profiles": json.dumps(profiles), "corpus_map": json.dumps({"shared_questions": ["q"], "disagreements": [], "throughlines": [], "candidate_angles": ["a"]})}
    fixed = unstringify(raw, RECON_SCHEMA)
    assert isinstance(fixed["profiles"], list) and isinstance(fixed["corpus_map"], dict)
    recon = Reconnaissance.model_validate(fixed)
    assert recon.profiles[0].key_claims[0].anchor.quote == "verbatim words here"


def test_plain_strings_are_left_alone_and_nested_strings_unpacked():
    schema = {"type": "object", "properties": {"note": {"type": "string"}, "rows": {"type": "array", "items": {"type": "object", "properties": {"cells": {"type": "array"}}}}}}
    raw = {"note": "[not json, just brackets", "rows": [{"cells": '[{"value": "v"}]'}]}
    fixed = unstringify(raw, schema)
    assert fixed["note"] == "[not json, just brackets"
    assert fixed["rows"][0]["cells"] == [{"value": "v"}]


def test_inline_defs_resolves_refs():
    schema = _inline_defs({"type": "object", "properties": {"a": {"$ref": "#/$defs/X"}}, "$defs": {"X": {"type": "string"}}})
    assert schema["properties"]["a"] == {"type": "string"}
