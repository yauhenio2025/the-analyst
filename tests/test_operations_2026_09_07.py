"""The move an engine performs has a name and a place (Evgeny, 2026-09-07 19:05): the operations vocabulary and the field on the record."""
import glob
import yaml

from src.engines.schemas_v2 import CapabilityEngineDefinition


def test_operations_are_a_vocabulary_and_tagged_engines_use_its_words():
    from src.vocabularies.registry import get_vocabulary_registry
    v = get_vocabulary_registry().get("operations")
    words = v.value_list()
    assert words[:2] == ["ascent", "descent"] and "placement" in words and "narration" in words
    tagged = {}
    for f in glob.glob("src/engines/capability_definitions/*.yaml"):
        d = yaml.safe_load(open(f)); CapabilityEngineDefinition.model_validate(d)
        if d.get("operation"):
            assert d["operation"] in words, (f, d["operation"])
            tagged[d["engine_key"]] = d["operation"]
    assert tagged["macro_actions"] == "ascent" and tagged["impact_scan"] == "descent" and tagged["thinker_placement"] == "placement" and tagged["distinction_draft"] == "distinction"
    assert sum(1 for op in tagged.values() if op == "ascent") >= 4 and len(tagged) >= 20
