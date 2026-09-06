"""The fidelity audit's second input: a memo's numbered statements against the sources they cite (the Stacks'
digest_check inputs), translated into the citation evidence index without judgment."""
import json

import pytest

from src.sources.citation_evidence import evidence_indexes, prepare_citation_sources
from src.sources.memo_statements import is_statements_file, statements_documents, statements_to_evidence_index

FILE = {
    "memo": {"uid": "em:U3HITB25", "title": "Weber's basic concepts", "date": "2026-09-05", "markdown": "# Memo\n\nWeber's concepts arose in comparative economic history."},
    "statements": [
        {"no": 1, "section": "core finding", "statement": "Weber's concepts arose within comparative economic history.", "sources": ["S1", "S4"]},
        {"no": 2, "section": "theme 1", "statement": "Modern capitalism is a distinctive configuration.", "sources": ["S2"]},
        {"no": 3, "section": "open", "statement": "A statement citing nothing.", "sources": []},
        {"no": 4, "section": "reading", "statement": "A statement citing an unknown label.", "sources": ["S9"]},
    ],
    "sources": [
        {"label": "S1", "uid": "em:RJRLLVLQ", "title": "Max Weber's Analysis of Capitalism", "year": "2019", "creators": "Bruhns", "text": "Weber's basic concepts arose within a continuous programme of comparative economic history."},
        {"label": "S2", "uid": "em:YASGM27U", "title": "Weber's Historical Studies", "year": "2024", "creators": "Bruhns", "text": "Modern capitalism is the distinctive configuration of rational enterprise."},
        {"label": "S4", "uid": "em:NQZYBP6Y", "title": "Basic Concepts", "year": "2006", "creators": "Bruhns", "text": "   "},
    ],
    "verdicts": "supported | partly | unsupported | misattributed | unchecked",
    "stacks_check_runs": [{"id": 7, "model": "sonnet", "cost": 0.4, "n": 4, "supported": 2, "partly": 1, "unsupported": 1, "misattributed": 0, "check": {"big": "blob"}}],
}


def test_the_translation_makes_the_memo_the_citing_text_and_each_source_a_held_witness():
    idx = statements_to_evidence_index(FILE)
    assert idx["role"] == "evidence_index" and idx["mode"] == "memo_against_sources"
    memo, = idx["texts"]
    assert memo["uid"] == "em:U3HITB25" and memo["text"].startswith("# Memo") and len(memo["passages"]) == 4
    assert memo["passages"][0]["cites"] == ["em:RJRLLVLQ", "em:NQZYBP6Y"] and memo["passages"][0]["locus"] == "statement 1"
    assert [c["copy"]["uid"] for c in idx["checks"]] == ["em:RJRLLVLQ", "em:YASGM27U"]          # the empty text is no witness
    assert idx["checks"][0]["cited_by"] == [1] and idx["checks"][0]["windows"][0]["how"] == "section"
    assert idx["unchecked"] == [{"no": 4, "label": "S9"}]
    assert idx["plan"]["themes"] == ["core finding", "open", "reading", "theme 1"]
    assert idx["plan"]["stacks_check_runs"] == [{"id": 7, "model": "sonnet", "cost": 0.4, "n": 4, "supported": 2, "partly": 1, "unsupported": 1, "misattributed": 0}]


def test_the_index_goes_through_the_fidelity_audits_existing_unpacking():
    docs = statements_documents({"stmts": json.dumps(FILE), "other": "plain text"})
    assert docs["other"] == "plain text" and json.loads(docs["stmts"])["mode"] == "memo_against_sources"
    assert [k for k, _ in evidence_indexes(docs)] == ["stmts"]
    sources, context = prepare_citation_sources("citation_fidelity_audit", docs)
    assert set(sources) == {"em:U3HITB25", "em:RJRLLVLQ", "em:YASGM27U", "other"}         # a plain document stays a source
    assert sources["em:U3HITB25"].startswith("SOURCE ROLE: citing_author") and sources["em:RJRLLVLQ"].startswith("SOURCE ROLE: primary_window")
    assert "UPSTREAM CITATION PLAN" in context and "never treat the memo as a witness for itself" in context
    assert "big" not in context                                                                  # the Stacks' raw check blobs never travel
    # the engagement map sees only the memo, the reception map nothing primary
    eng, _ = prepare_citation_sources("citation_engagement_map", docs)
    assert set(eng) == {"em:U3HITB25", "other"}


def test_it_refuses_what_is_not_a_statements_file():
    assert not is_statements_file({"statements": [], "sources": []}) and not is_statements_file({"author": "x"})
    with pytest.raises(ValueError):
        statements_to_evidence_index({"statements": [{"statement": "s"}], "sources": [{"uid": "u", "text": ""}]})
