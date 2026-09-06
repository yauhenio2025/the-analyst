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


@pytest.mark.parametrize("key", [v.key for v in get_vocabulary_registry().list() if any(u.kind == "engine" for u in v.used_by)])
def test_every_answer_shape_agrees_with_its_vocabulary(key):
    voc = get_vocabulary_registry().get(key)
    for use in voc.used_by:
        if use.kind != "engine":
            continue
        shape = _shape_values(use.engine_key, use.dimension, use.field)
        assert shape, f"{use.engine_key}.{use.dimension}.{use.field}: no enumerated values in the answer shape"
        assert shape == set(voc.value_list()), f"{key} vs {use.engine_key}.{use.field}: shape {sorted(shape)} != vocabulary {voc.value_list()}"


def test_the_api_route_serves_them():
    from src.api.routes.vocabularies import get_vocabulary, list_vocabularies, vocabularies_for_engine
    assert any(v["key"] == "citation_moves" for v in list_vocabularies())
    assert get_vocabulary("fidelity_verdicts")["values"][5]["value"] == "unverifiable"
    assert "reader_relations" in [v["key"] for v in vocabularies_for_engine("citation_reception_map")]


def test_the_desks_read_their_enumerations_from_the_registry():
    from src.dossier import schemas as S
    from src.vocabularies.registry import values
    assert list(S.EVIDENCE_KINDS) == values("spine_evidence_kinds") and list(S.DELIVERABLE_KINDS) == values("deliverable_kinds")
    assert list(S.USE_KINDS) == values("use_kinds") and list(S.ENTRIES) == values("entry_lanes") and list(S.STEP_DEPTHS) == values("step_depths")
    assert list(S.FINDING_KINDS) == values("finding_kinds") and list(S.AFFORDANCES) == values("finding_affordances") and list(S.FATES) == values("finding_fates")
    assert list(S.FIGURE_FORMATS) == values("figure_formats") and list(S.AUDIENCES) == values("audiences") and list(S.DEPTHS) == values("dossier_depths")


def test_the_packet_validator_and_the_source_roles_agree_with_the_registry():
    from scripts.validate_citation_cohort_2026_09_06 import VERDICTS
    from src.sources.schemas import SourceRole
    from src.vocabularies.registry import values
    import typing
    assert set(VERDICTS) == set(values("fidelity_verdicts"))
    assert list(typing.get_args(SourceRole)) == values("source_roles")
    src = open("scripts/validate_citation_cohort_2026_09_06.py").read()
    for k in values("packet_row_status"):
        assert f"'{k}'" in src
    for k in values("packet_anchor_status"):
        assert f"'{k}'" in src


def test_mirrored_vocabularies_name_their_owner():
    reg = get_vocabulary_registry()
    assert reg.get("referee_centrality").owner == "the-referee" and reg.get("referee_centrality").value_list() == ["core", "major", "peripheral"]
    assert reg.get("citation_event_kinds").owner == "the-stacks" and reg.get("profile_person_roles").owner == "the-stacks"
    assert all(u.kind in ("engine", "desk", "schema", "external") for v in reg.list() for u in v.used_by)
