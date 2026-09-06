"""Citation contracts: source identity is enforced mechanically, reading by models."""
from src.engines.registry import get_engine_registry
from src.operationalizations.registry import get_operationalization_registry
from src.executor.ledger_walls import SourceIndex, parse_rows, verify_rows
from src.stages.process_composer import compose_extract_prompt
from scripts.build_citation_pilot_corpus import passage_windows, printed_pages
import json
import pytest
from src.sources.citation_evidence import prepare_citation_sources, plan_context, with_citation_context


def index_fixture():
    return {"author": "A", "person": "P", "plan": {"questions": ["Check the qualification"],
            "warnings": ["Edition differs"], "themes": ["Closure"]},
            "texts": [{"uid": "em:A", "passages": [{"ref_id": "R1", "window": "A attributes a qualified claim."}]}],
            "checks": [{"copy": {"uid": "em:W", "edition": "held"}, "ref_ids": ["R1"],
                        "windows": [{"how": "section", "section_title": "Politik als Beruf", "text": "P qualifies this claim."}]}]}


def test_index_alone_unpacks_literal_witnesses_and_keeps_plan_outside_evidence():
    raw = {"index": json.dumps(index_fixture())}
    docs, context = prepare_citation_sources("citation_fidelity_audit", raw)
    assert set(docs) == {"em:A", "em:W"}
    assert "A attributes a qualified claim." in docs["em:A"]
    assert "P qualifies this claim." in docs["em:W"]
    assert "Closure" in context and "Politik als Beruf" in context
    assert all("Closure" not in text for text in docs.values())
    row = parse_rows('[F1] fair — dim: paired_fidelity — anchor: "A attributes a qualified claim." — doc: em:A'
                     ' — anchor-b: "P qualifies this claim." — doc-b: em:W')
    assert not verify_rows(row, SourceIndex(docs), corpus_dimensions={"paired_fidelity"}).failed_ids
    assert raw == {"index": json.dumps(index_fixture())}


def test_bad_index_cannot_turn_one_source_into_two_or_invent_retrieval_kind():
    for mutate in (lambda obj: obj["checks"][0]["copy"].update(uid="em:A"),
                   lambda obj: obj["checks"][0]["windows"][0].update(how="unheld")):
        obj = index_fixture(); mutate(obj)
        with pytest.raises(ValueError):
            prepare_citation_sources("citation_fidelity_audit", {"index": json.dumps(obj)})


def test_plan_reaches_every_call_including_checked_reconciliation():
    from src.executor.process_runner import run_oneshot_checked
    key = "citation_fidelity_audit"
    spec = get_operationalization_registry().get(key).process.model_copy(update={"scoped_outcomes": False})
    prompts = []
    line = '[F1] fair — dim: paired_fidelity — anchor: "A attributes a qualified claim." — doc: em:A — anchor-b: "P qualifies this claim." — doc-b: em:W'
    def call(system, user, **kwargs):
        prompts.append(user)
        content = "## Findings ledger\n" + line
        if "verify" in kwargs["label"].lower() or "check" in kwargs["label"].lower():
            content += " — status: confirmed"
        return {"content": content, "model_used": kwargs["model_hint"], "stop_reason": "stop", "partial": False}
    result = run_oneshot_checked(get_engine_registry().get_capability_definition(key), spec,
                                {"index": json.dumps(index_fixture())}, call_fn=call)
    assert any(c.step_key == "reconcile_checked" for c in result.calls)
    assert len(prompts) >= 3 and all("Check the qualification" in p and "Edition differs" in p and "Closure" in p for p in prompts)


def test_reception_contract_exposes_spine_and_addition_origin():
    spec = get_operationalization_registry().get("citation_reception_map").process
    dim = next(d for d in spec.dimensions if d.key == "theme_position")
    assert "theme-origin: plan_spine|reader_addition" in dim.answer_shape


def test_source_resolution_preserves_explicit_index_and_witness_keys():
    from src.sources.resolve import resolve_sources
    from src.sources.schemas import SourceSpec
    docs = resolve_sources([SourceSpec(kind="paste", key="em:A", text="SOURCE ROLE: citing_author\nAn actual source."),
                            SourceSpec(kind="paste", key="index", role="evidence_index", text=json.dumps(index_fixture()))])
    assert [d.key for d in docs] == ["em:A", "index"]
    assert "Closure" in plan_context({d.key: d.text for d in docs})
    with pytest.raises(ValueError):
        resolve_sources([SourceSpec(key="em:A", text="one"), SourceSpec(key="em:A", text="two")])


def test_dossier_context_bridge_keeps_index_witnesses_available_to_fidelity():
    from src.executor.chain_runner import _citation_context_envelopes
    raw = json.dumps(index_fixture())
    upstream = 'PRIOR ENGINE OUTPUT\n\nCONTEXT SUPPLIED WITH THE JOB [evidence]:\n' + raw
    docs, remaining = _citation_context_envelopes("citation_fidelity_audit", {"em:A": "Full A text"}, upstream)
    assert "PRIOR ENGINE OUTPUT" in remaining and raw not in remaining
    witnesses, context = prepare_citation_sources("citation_fidelity_audit", docs)
    assert witnesses["em:A"] == "Full A text" and "P qualifies" in witnesses["em:W"]
    assert "Closure" in context
    assert _citation_context_envelopes("deep_summarization", {"em:A": "Full A text"}, upstream) == ({"em:A": "Full A text"}, upstream)


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
