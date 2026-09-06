"""The vocabulary registry (2026-09-06): every enumerated field an engine answers in is a vocabulary the Mastermind
serves; the engine's answer shape and the vocabulary can never disagree (the drift the owner flagged)."""
import re

import pytest

from src.operationalizations.registry import get_operationalization_registry
from src.vocabularies.registry import get_vocabulary_registry


def _shape_values(engine_key: str, dimension: str, field: str) -> set[str]:
    op = get_operationalization_registry().get(engine_key)
    dims = [d for d in op.process.dimensions if dimension == "*" or d.key == dimension]
    out: set[str] = set()
    for d in dims:
        m = re.search(rf"— {re.escape(field)}: ([^—]+?)(?= —|$)", d.answer_shape)
        if m:
            vals = re.sub(r"\s*\([^)]*\)\s*$", "", m.group(1).strip())     # a trailing qualifier: "search (only when retrieved)"
            if "|" in vals and "<" not in vals:
                out |= {v.strip() for v in vals.split("|")}
    return out


def test_registry_loads_and_serves_the_citation_and_hypothesis_families():
    reg = get_vocabulary_registry()
    keys = {v.key for v in reg.list()}
    assert {"citation_moves", "citation_stances", "citation_attribution_kinds", "fidelity_verdicts", "retrieval_how", "reader_relations", "reader_stances", "evidence_kinds", "cohort_circles", "hypothesis_verdicts"} <= keys
    assert reg.get("citation_moves").value_list() == ["authority", "evidence", "foil", "dialogue", "genealogy", "illustration", "courtesy", "self-positioning"]
    assert reg.values_for("citation_engagement_map", "stance") == ["adopts", "builds_on", "qualifies", "disputes", "mentions"]
    assert {v.key for v in reg.for_engine("citation_fidelity_audit")} >= {"citation_attribution_kinds", "fidelity_verdicts", "retrieval_how", "confidence"}


@pytest.mark.parametrize("key", [v.key for v in get_vocabulary_registry().list() if v.used_by])
def test_every_answer_shape_agrees_with_its_vocabulary(key):
    voc = get_vocabulary_registry().get(key)
    for use in voc.used_by:
        shape = _shape_values(use.engine_key, use.dimension, use.field)
        assert shape, f"{use.engine_key}.{use.dimension}.{use.field}: no enumerated values in the answer shape"
        assert shape == set(voc.value_list()), f"{key} vs {use.engine_key}.{use.field}: shape {sorted(shape)} != vocabulary {voc.value_list()}"


def test_the_api_route_serves_them():
    from src.api.routes.vocabularies import get_vocabulary, list_vocabularies, vocabularies_for_engine
    assert any(v["key"] == "citation_moves" for v in list_vocabularies())
    assert get_vocabulary("fidelity_verdicts")["values"][5]["value"] == "unverifiable"
    assert "reader_relations" in [v["key"] for v in vocabularies_for_engine("citation_reception_map")]
