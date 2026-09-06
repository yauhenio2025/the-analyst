"""Citation contracts: source identity is enforced mechanically, reading by models."""
from src.engines.registry import get_engine_registry
from src.operationalizations.registry import get_operationalization_registry
from src.executor.ledger_walls import SourceIndex, parse_rows, verify_rows
from src.stages.process_composer import compose_extract_prompt
from scripts.build_citation_pilot_corpus import passage_windows, printed_pages


def test_fidelity_verdict_requires_two_distinct_sources():
    spec=get_operationalization_registry().get("citation_fidelity_audit").process
    dims={d.key for d in spec.dimensions if d.scope=="corpus"}
    assert "paired_fidelity" in dims
    docs={"A":"Riley attributes a political mechanism.","W":"Weber qualifies that political mechanism."}
    local='[F1] Fair — dim: paired_fidelity — anchor: "Riley attributes a political mechanism." — doc: A'
    rows=parse_rows(local)
    assert verify_rows(rows,SourceIndex(docs),corpus_dimensions=dims).failed_ids==["F1"]
    rows=parse_rows(local+' — anchor-b: "Weber qualifies that political mechanism." — doc-b: W')
    assert not verify_rows(rows,SourceIndex(docs),corpus_dimensions=dims).failed_ids
    rows=parse_rows(local+' — anchor-b: "Riley attributes a political mechanism." — doc-b: A')
    assert verify_rows(rows,SourceIndex(docs),corpus_dimensions=dims).failed_ids==["F1"]


def test_fidelity_corpus_prompt_preserves_pair_warrant():
    key="citation_fidelity_audit";spec=get_operationalization_registry().get(key).process
    dim=next(d for d in spec.dimensions if d.key=="paired_fidelity")
    p=compose_extract_prompt(get_engine_registry().get_capability_definition(key),spec,spec.steps[0],dim,
        {"A":"A text","W":"W window"},prior_ledgers="paired local findings")
    assert "misattributed" in p.system and "distinct" in p.system
    assert "paired local findings" in p.user


def test_name_windows_exclude_spaced_reference_heading():
    parts=["Weber distinguishes class and status. That distinction matters.\nr e fe r e n c e s\nWeber, Max. A book.",
           "Weber, Max. Another bibliographic entry."]
    found=passage_windows(parts)
    assert len(found)==1 and "bibliographic" not in found[0]["window"]
    assert found[0]["pdf_page"]==1


def test_printed_page_mapping_does_not_equate_pdf_indices():
    parts=[f"{n} Scholar\nBody has a citation to 1922.\nAnother line." for n in range(301,306)]
    assert printed_pages(parts)=={1:301,2:302,3:303,4:304,5:305}
    assert printed_pages(["Unnumbered preface", "Chapter body without page number"])=={}
