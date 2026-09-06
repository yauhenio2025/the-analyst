"""The Stacks' two contract questions (2026-09-06): an index text or check meets a supplied full text by uid OR key,
with or without the em: prefix (no second passage-only witness of the same text), and the index's roles map labels
supplied documents that carry no SOURCE ROLE line before the scope filter."""
import json

from src.sources.citation_evidence import prepare_citation_sources

INDEX = {"role": "evidence_index", "author": {"id": "riley-dylan"}, "person": {"norm": "weber m"}, "plan": {"questions": ["q"]},
         "texts": [{"uid": "em:BEFGGK6M", "key": "BEFGGK6M", "title": "Privilege and Property", "year": 2003,
                    "passages": [{"ref_id": 5505, "hit": "Weber is cited here.", "before": "", "after": ""}]}],
         "checks": [{"work_key": "w1", "title": "Economy and Society", "copy": {"uid": "em:Q4WEBER1", "key": "Q4WEBER1"},
                     "windows": [{"how": "page", "printed": [1], "text": "Weber's own words at the cited place."}]}],
         "roles": {"BEFGGK6M": "citing_author", "Q4WEBER1": "primary_window", "Z7READER": "secondary_reader"}}


def _docs(**extra):
    return {"index": json.dumps(INDEX), **extra}


def test_a_supplied_full_text_keyed_by_zotero_key_meets_its_index_entry_without_a_second_witness():
    docs = _docs(BEFGGK6M="The full citing text. Weber is cited here. And much more.")
    sources, context = prepare_citation_sources("citation_engagement_map", docs)
    assert set(sources) == {"BEFGGK6M"}                                   # no passage-only em:BEFGGK6M beside it
    assert sources["BEFGGK6M"].startswith("SOURCE ROLE: citing_author\n")  # labelled by the roles map
    assert '"supplied_as": "BEFGGK6M"' in context


def test_a_zotero_uid_header_line_also_meets_the_index():
    docs = _docs(privilege_and_property="SOURCE ROLE: citing_author\nAUTHOR: Dylan Riley\nZOTERO UID: em:BEFGGK6M\n\nThe full citing text.")
    sources, _ = prepare_citation_sources("citation_engagement_map", docs)
    assert set(sources) == {"privilege_and_property"}


def test_a_supplied_cited_work_meets_its_check_and_a_reader_is_kept_out_of_the_engagement_map():
    docs = _docs(BEFGGK6M="The full citing text.", Q4WEBER1="The whole held copy of Economy and Society.", Z7READER="A reader on Weber.")
    eng, _ = prepare_citation_sources("citation_engagement_map", docs)
    assert set(eng) == {"BEFGGK6M"}                                        # the reader and the primary are out of scope here
    fid, _ = prepare_citation_sources("citation_fidelity_audit", docs)
    assert set(fid) == {"BEFGGK6M", "Q4WEBER1"} and "whole held copy" in fid["Q4WEBER1"]   # the supplied copy, not a window witness
    rec, _ = prepare_citation_sources("citation_reception_map", docs)
    assert set(rec) == {"BEFGGK6M", "Z7READER"} and rec["Z7READER"].startswith("SOURCE ROLE: secondary_reader")


def test_without_a_supplied_text_the_index_still_builds_its_witnesses():
    sources, _ = prepare_citation_sources("citation_fidelity_audit", _docs())
    assert set(sources) == {"em:BEFGGK6M", "em:Q4WEBER1"}
    assert sources["em:Q4WEBER1"].startswith("SOURCE ROLE: primary_window")
