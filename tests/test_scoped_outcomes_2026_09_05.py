"""Offline behavior at empty-output boundaries; opted-out prompts stay byte-identical."""
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.engines.registry import get_engine_registry
from src.operationalizations.registry import get_operationalization_registry
from src.operationalizations.schemas import ProcessDimension, ProcessSpec, ProcessStep
from src.executor.process_runner import run_oneshot_checked, run_process
from src.executor.scoped_outcomes import render_scope_json
from src.stages.process_composer import (
    LEDGER_HEADING, compose_extract_prompt, compose_oneshot_prompt,
    compose_synthesize_prompt, compose_verify_prompt,
)

CAP = SimpleNamespace(engine_key="candidate", engine_name="Candidate", problematique="ASSERT THAT EVERY TEXT HAS THE PHENOMENON.")
SOURCE = "The text presents two compatible positions supported by separate reasons."
OTHER = "The text considers a possibility without claiming that it must occur."


@pytest.fixture(autouse=True)
def no_provider_calls(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("offline test attempted a provider call")
    monkeypatch.setattr("src.executor.engine_runner.get_backend", forbidden)
    monkeypatch.setattr("src.executor.process_runner._default_call", forbidden)


def spec(*, corpus=False, opted=True):
    dims = [ProcessDimension(key="opposition", name="Opposition", id_prefix="D1", scope="document",
                             questions=["What, if any, qualifying opposition occurs?"],
                             method_card="Identify incompatible commitments; compatible positions do not qualify.",
                             answer_shape="finding — dim: opposition — anchor: quote")]
    if corpus:
        dims.append(ProcessDimension(key="relations", name="Relations", id_prefix="DX6", scope="corpus",
                                     questions=["What, if any, supported cross-document relation occurs?"],
                                     method_card="Compare qualified claims with two document-keyed anchors."))
    return ProcessSpec(key="candidate", description="Conditional eligibility inquiry.",
                       framing="Do not presuppose a qualifying instance. Apply the explicit eligibility criterion.",
                       scoped_outcomes=opted, dimensions=dims,
                       steps=[ProcessStep(key="extract", kind="extract", model_tier="cheap", max_rows=12),
                              ProcessStep(key="verify", kind="verify", model_tier="mid", consumes=["extract"]),
                              ProcessStep(key="synthesize", kind="synthesize", model_tier="strong", consumes=["verify"], is_final=True)],
                       routing={"cheap": "fake/cheap", "mid": "fake/mid", "strong": "fake/strong"})


def record(doc="a", *, dim="opposition", outcome="no_relevant_instance", ids=(), review=False, **changes):
    out = dict(document_keys=[doc] if isinstance(doc, str) else list(doc), dimension_key=dim,
               outcome=outcome, sections_inspected=["Opening argument"], coverage="partial",
               criterion="Incompatible commitments asserted under the same conditions.",
               basis="The inspected passage presents compatible positions.", limitations=["Other sections not assessed."],
               finding_ids=list(ids), review_state="supported_within_stated_scope" if review else "unchecked",
               review_basis="I checked the stated opening against the eligibility criterion." if review else "")
    out.update(changes)
    return out


def output(*records, rows=(), prose="A scoped reading."):
    return prose + "\n\n" + LEDGER_HEADING + "\n" + "\n".join(rows) + "\n\n" + render_scope_json(list(records))


def row(rid="F1", doc="a", quote=SOURCE, status="", dim="opposition", lineage=""):
    return (f'- [{rid}] A positive structural finding — dim: {dim} — anchor: {json.dumps(quote)} — doc: {doc}'
            + (f" — status: {status}" if status else "") + (f" — from: {lineage}" if lineage else ""))


def sequence(*responses):
    pending = iter(responses)
    calls = []
    def fake(system, user, **kwargs):
        calls.append((system, user, kwargs))
        response = next(pending)
        return {"model_used": kwargs["model_hint"], **(response if isinstance(response, dict) else {"content": response})}
    return fake, calls


def scopes(result):
    return result.final_wall["scope_outcomes"]


def test_68_production_prompts_are_unchanged():
    baseline = json.loads((Path(__file__).parent / "fixtures/scoped_outcomes/production_prompt_hashes_3426419.json").read_text())
    actual = {}
    for engine in ("conditions_of_possibility_analyzer", "argument_architecture", "inferential_commitment_mapper", "epistemological_method_detector"):
        cap = get_engine_registry().get_capability_definition(engine)
        process = get_operationalization_registry().get(engine).process
        assert process.framing is None and not process.scoped_outcomes
        for docs in ({"doc-a": "Alpha source."}, {"doc-a": "Alpha source.", "doc-b": "Beta source."}):
            prompts = [compose_oneshot_prompt(cap, process, docs),
                       compose_verify_prompt(cap, process, process.steps[1], docs, "BASE LEDGER"),
                       compose_synthesize_prompt(cap, process, process.final_step, docs, "BASE LEDGER")]
            for dim in process.dimensions:
                if dim.scope == "document":
                    prompts.append(compose_extract_prompt(cap, process, process.steps[0], dim, docs, doc_key="doc-a" if len(docs) > 1 else ""))
                elif len(docs) > 1:
                    prompts.append(compose_extract_prompt(cap, process, process.steps[0], dim, docs, prior_ledgers="BASE LEDGER"))
            for i, prompt in enumerate(prompts):
                actual[f"{engine}:{len(docs)}:{i}"] = hashlib.sha256(json.dumps(prompt.model_dump(), sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    assert actual == baseline


def test_framing_overrides_all_composed_prompts_and_removes_positive_minimum():
    process, docs = spec(corpus=True), {"a": SOURCE, "b": OTHER}
    prompts = [compose_oneshot_prompt(CAP, process, docs),
               compose_verify_prompt(CAP, process, process.steps[1], docs, ""),
               compose_synthesize_prompt(CAP, process, process.final_step, docs, "")]
    prompts += [compose_extract_prompt(CAP, process, process.steps[0], dim, docs) for dim in process.dimensions]
    for prompt in prompts:
        assert process.framing in prompt.system
        assert CAP.problematique not in prompt.system
        assert "12-30 rows" not in prompt.system and "8 to 12 rows" not in prompt.system
        assert "three to five row ids" not in prompt.system
        assert "Give each assessed document anchored representation" not in prompt.system
    legacy = spec(opted=False)
    legacy.framing = None
    assert CAP.problematique in compose_oneshot_prompt(CAP, legacy, {"a": SOURCE}).system
    assert "12-30 rows" in compose_oneshot_prompt(CAP, legacy, {"a": SOURCE}).system


def test_zero_row_oneshot_is_actually_reviewed_and_raw_receipts_survive():
    read = output(record(review=True))  # reader cannot certify itself
    critic = output(record(review=True))
    call, calls = sequence(read, critic)
    saved = []
    result = run_oneshot_checked(CAP, spec(), {"a": SOURCE}, call_fn=call, on_call=saved.append)
    assert len(calls) == 2
    assert saved[0].content == read and saved[1].content == critic
    assert saved[0].wall["scope_outcomes"][0]["review_state"] == "unchecked"
    assert '"review_state": "unchecked"' in calls[1][1]
    assert scopes(result)[0]["outcome"] == "no_relevant_instance"
    assert scopes(result)[0]["review_state"] == "supported_within_stated_scope"
    assert "no relevant instance reported" in result.final_content
    assert "Opening argument" in result.final_content and "Reported coverage: partial" in result.final_content
    assert "## Scope outcomes" not in result.final_content
    assert result.final_wall["rows"] == 0


@pytest.mark.parametrize("coverage", ["partial", "unknown"])
def test_unchecked_negative_is_scoped_and_never_self_certified(coverage):
    call, calls = sequence(output(record(review=True, coverage=coverage)))
    result = run_oneshot_checked(CAP, spec(), {"a": SOURCE}, call_fn=call, check=False)
    assert len(calls) == 1
    assert scopes(result)[0]["outcome"] == "no_relevant_instance"
    assert scopes(result)[0]["review_state"] == "unchecked"
    assert scopes(result)[0]["evidence_state"]["invocation_partial"] is None
    assert "not proofs of absence" in result.final_content


@pytest.mark.parametrize("bad", [
    "A response with no ledger or scope records.",
    LEDGER_HEADING + '\n\n## Scope outcomes\n{broken json',
    output(record(document_keys=["foreign"])),
    output(record(), record()),
    output(record(sections_inspected=[])),
    output(record(), rows=["- malformed extraction with no row identity"]),
])
def test_malformed_or_missing_extraction_never_becomes_supported_absence(bad):
    call, calls = sequence(bad, output(record(review=True)))
    result = run_oneshot_checked(CAP, spec(), {"a": SOURCE}, call_fn=call)
    assert len(calls) == 2
    assert scopes(result)[0]["outcome"] == "inconclusive"
    assert scopes(result)[0]["review_state"] == "unchecked"
    assert scopes(result)[0]["evidence_state"]["blocking_issues"]
    assert result.calls[0].content == bad


@pytest.mark.parametrize("meta", [{"partial": True}, {"stop_reason": "length"},
                                 {"connection_error": "stream interrupted"}, {"error": "source read failed"}])
def test_known_invocation_trouble_cannot_be_upgraded_by_critic(meta):
    call, _ = sequence({"content": output(record()), **meta}, output(record(review=True)))
    result = run_oneshot_checked(CAP, spec(), {"a": SOURCE}, call_fn=call)
    assert scopes(result)[0]["outcome"] == "inconclusive"
    assert "Invocation is known partial or failed" in scopes(result)[0]["evidence_state"]["blocking_issues"]
    original = result.calls[0].wall["scope_outcomes"][0]["evidence_state"]
    assert original["invocation_partial"] == meta.get("partial")
    assert original["invocation_error"] == (meta.get("error") or meta.get("connection_error"))


@pytest.mark.parametrize("critic", [LEDGER_HEADING, output(record(review=True, review_basis=""))])
def test_missing_scope_review_or_reason_cannot_support_negative(critic):
    call, _ = sequence(output(record()), critic)
    result = run_oneshot_checked(CAP, spec(), {"a": SOURCE}, call_fn=call)
    assert scopes(result)[0]["review_state"] == "unchecked"
    assert scopes(result)[0]["outcome"] == "inconclusive"


def test_reviewer_can_dispute_a_negative_without_inventing_positive_rows():
    call, _ = sequence(output(record()), output(record(review=True, review_state="disputed", review_basis="The stated criterion was applied too narrowly.")))
    result = run_oneshot_checked(CAP, spec(), {"a": SOURCE}, call_fn=call)
    assert scopes(result)[0]["review_state"] == "disputed"
    assert "disputed by the reviewer" in result.final_content
    assert result.final_wall["rows"] == 0


def test_all_anchors_lost_in_oneshot_does_not_become_absence():
    positive = record(outcome="findings_present", ids=["F1"])
    call, _ = sequence(output(positive, rows=[row(quote="This quotation does not occur in the supplied source.")]),
                       output(record(review=True), rows=[row(status="rejected")]))
    result = run_oneshot_checked(CAP, spec(), {"a": SOURCE}, call_fn=call)
    assert scopes(result)[0]["outcome"] == "inconclusive"
    assert "lost anchor evidence" in " ".join(scopes(result)[0]["evidence_state"]["blocking_issues"])


@pytest.mark.parametrize("runner", [run_process, run_oneshot_checked])
@pytest.mark.parametrize("docs", [{}, {"a": ""}, {"a": SOURCE, "b": " "}])
def test_missing_selected_source_refuses_before_call(runner, docs):
    call, calls = sequence()
    with pytest.raises(ValueError, match="missing source is not absence"):
        runner(CAP, spec(), docs, call_fn=call)
    assert not calls


def test_deep_all_negative_scopes_are_reviewed_and_synthesized_without_rows():
    final = "The opening gives no qualifying instance within the inspected scope.\n\n" + LEDGER_HEADING
    call, calls = sequence(output(record()), output(record(review=True)), final)
    result = run_process(CAP, spec(), {"a": SOURCE}, call_fn=call, reanchor=False, parallelism=1)
    assert [c.step_key for c in result.calls] == ["extract", "verify", "synthesize"]
    assert len(calls) == 3 and '"no_relevant_instance"' in calls[2][1]
    assert scopes(result)[0]["review_state"] == "supported_within_stated_scope"
    assert "no relevant instance reported" in result.final_content
    assert result.calls[-1].content == final


@pytest.mark.parametrize("extraction", [
    "Broken extraction", output(record(outcome="findings_present", ids=["D1.F1"]), rows=[row("D1.F1", quote="An invented absent quote that the wall cannot find.")]),
])
def test_deep_empty_from_malformed_or_lost_evidence_remains_inconclusive(extraction):
    call, calls = sequence(extraction, output(record(review=True)), LEDGER_HEADING)
    result = run_process(CAP, spec(), {"a": SOURCE}, call_fn=call, reanchor=False, parallelism=1)
    assert len(calls) == 3
    assert scopes(result)[0]["outcome"] == "inconclusive"
    assert "inconclusive" in result.final_content


def test_legacy_empty_boundaries_keep_existing_call_counts_and_failure_guard():
    process = spec(opted=False)
    call, calls = sequence(LEDGER_HEADING)
    one = run_oneshot_checked(CAP, process, {"a": SOURCE}, call_fn=call)
    assert len(calls) == 1 and "scope_outcomes" not in one.final_wall
    call, calls = sequence(LEDGER_HEADING)
    with pytest.raises(RuntimeError, match="nothing survived the walls"):
        run_process(CAP, process, {"a": SOURCE}, call_fn=call, reanchor=False)
    assert len(calls) == 1


def test_mixed_deep_corpus_preserves_all_scopes_and_checks_empty_documents():
    docs = {"a": SOURCE, "b": OTHER, "c": SOURCE}
    positive = record("a", outcome="findings_present", ids=["D1.DOC1.F1"], basis="The reader reports a qualifying structural relation.")
    negative = record("b")
    uncertain = record("c", outcome="inconclusive", basis="The relevant attribution remains unsettled.")
    corpus = record(list(docs), dim="relations", outcome="inconclusive", basis="The reports cannot settle a relation across all three documents.")
    final = "Only the positive document is mentioned by this deliberately incomplete synthesis.\n\n" + LEDGER_HEADING + "\n" + row(lineage="D1.DOC1.F1")
    call, calls = sequence(output(positive, rows=[row("D1.DOC1.F1")]), output(negative), output(uncertain), output(corpus),
                           output({**positive, "review_state": "supported_within_stated_scope", "review_basis": "The positive finding is supported."}, rows=[row("D1.DOC1.F1", status="confirmed")]),
                           output({**negative, "review_state": "supported_within_stated_scope", "review_basis": "Checked the limited opening."}),
                           output(uncertain), output(corpus), final)
    result = run_process(CAP, spec(corpus=True), docs, call_fn=call, reanchor=False, parallelism=1)
    assert len(calls) == 9
    assert len(result.calls_for("verify")) == 4  # includes two zero-row documents and empty corpus scope
    got = {(tuple(r["document_keys"]), r["dimension_key"]): r for r in scopes(result)}
    assert len(got) == 4
    assert got[(("a",), "opposition")]["outcome"] == "findings_present"
    assert got[(("b",), "opposition")]["outcome"] == "no_relevant_instance"
    assert got[(("c",), "opposition")]["outcome"] == "inconclusive"
    assert got[(("a", "b", "c"), "relations")]["outcome"] == "inconclusive"
    assert "b / opposition: no relevant instance reported" in result.final_content
    assert "c / opposition: inconclusive" in result.final_content
    assert "a, b, c / relations: inconclusive" in result.final_content
    assert all(f'"{key}"' in calls[-1][1] for key in docs)
    assert '"dimension_key": "relations"' in calls[-1][1]
    assert "## Scope outcomes" not in result.final_content
    assert "no direct source inspection" in result.calls[3].wall["scope_outcomes"][0]["evidence_state"]["basis_material"]


def test_failed_quote_in_a_does_not_contaminate_same_dimension_in_b():
    docs = {"a": SOURCE, "b": OTHER}
    first = output(record("a", outcome="findings_present", ids=["F1"]), record("b"),
                   rows=[row(quote="The missing quote has no match in either source.")])
    review = output(record("a", review=True), record("b", review=True), rows=[row(status="rejected")])
    call, _ = sequence(first, review)
    result = run_oneshot_checked(CAP, spec(), docs, call_fn=call)
    a, b = scopes(result)
    assert a["outcome"] == "inconclusive"
    assert b["outcome"] == "no_relevant_instance" and b["review_state"] == "supported_within_stated_scope"
    assert not b["evidence_state"]["blocking_issues"]


def test_scope_finding_id_cannot_bind_to_other_document():
    call, _ = sequence(output(record("a", outcome="findings_present", ids=["F1"]),
                              record("b", outcome="findings_present", ids=["F1"]), rows=[row()]))
    result = run_oneshot_checked(CAP, spec(), {"a": SOURCE, "b": OTHER}, call_fn=call, check=False)
    assert scopes(result)[0]["outcome"] == "findings_present"
    assert scopes(result)[1]["outcome"] == "inconclusive"
    assert "does not belong" in " ".join(scopes(result)[1]["evidence_state"]["blocking_issues"])


@pytest.mark.parametrize("second_quote,expected", [(OTHER, "findings_present"), ("An invented second-document quotation that is absent.", "inconclusive")])
def test_corpus_scope_requires_both_real_anchors_without_contaminating_document_scopes(second_quote, expected):
    paired = row(dim="relations") + f' — anchor-b: {json.dumps(second_quote)} — doc-b: b'
    declared = [record("a"), record("b"), record(["a", "b"], dim="relations", outcome="findings_present", ids=["F1"])]
    call, _ = sequence(output(*declared, rows=[paired]))
    result = run_oneshot_checked(CAP, spec(corpus=True), {"a": SOURCE, "b": OTHER}, call_fn=call, check=False)
    assert [r["outcome"] for r in scopes(result)] == ["no_relevant_instance", "no_relevant_instance", expected]
    assert result.final_wall["anchors"] == 2
    assert result.final_wall["verified_anchors"] == (2 if expected == "findings_present" else 1)


@pytest.mark.parametrize("dimension_field", ["", " — dim: oppositon"])
def test_unassigned_positive_row_does_not_silently_validate_a_negative(dimension_field):
    missing_dimension = row().replace(" — dim: opposition", dimension_field)
    call, _ = sequence(output(record(), rows=[missing_dimension]))
    result = run_oneshot_checked(CAP, spec(), {"a": SOURCE}, call_fn=call, check=False)
    assert scopes(result)[0]["outcome"] == "inconclusive"
    assert "dimension identity" in result.final_content


def test_explicit_critic_addition_references_survive_existing_id_renumbering():
    call, _ = sequence(output(record()), output(record(outcome="findings_present", ids=["V.F1"], review=True),
                                                rows=[row("V.F1", status="added")]))
    result = run_oneshot_checked(CAP, spec(), {"a": SOURCE}, call_fn=call)
    assert scopes(result)[0]["outcome"] == "findings_present"
    assert scopes(result)[0]["finding_ids"] == ["F1"]
    assert "from: V.F1" in result.final_content


@pytest.mark.parametrize("heading", ["## Scope outcomes", "### SCOPE OUTCOMES:", "**Scope outcomes**", "## Scope outcome"])
def test_recognizable_malformed_scope_json_stays_in_raw_receipt_only(heading):
    bad = LEDGER_HEADING + "\n\n" + heading + '\n```json\n[{"secret_internal_field": "malformed"}\n'
    call, _ = sequence(bad)
    result = run_oneshot_checked(CAP, spec(), {"a": SOURCE}, call_fn=call, check=False)
    assert result.calls[0].content == bad
    assert "secret_internal_field" not in result.final_content
    assert scopes(result)[0]["outcome"] == "inconclusive"


def test_reanchoring_restores_positive_evidence_and_keeps_its_raw_receipt():
    extraction = output(record(outcome="findings_present", ids=["D1.F1"]), rows=[row("D1.F1", quote="An invented absent quotation with no valid match.")])
    replacement = LEDGER_HEADING + "\n" + row("D1.F1")
    review = output(record(outcome="findings_present", ids=["D1.F1"], review=True), rows=[row("D1.F1", status="confirmed")])
    call, calls = sequence(extraction, replacement, review, LEDGER_HEADING + "\n" + row(lineage="D1.F1"))
    result = run_process(CAP, spec(), {"a": SOURCE}, call_fn=call, parallelism=1)
    assert len(calls) == 4 and result.calls[0].reanchored == 1
    assert result.calls[0].content == extraction
    assert result.calls[0].wall["reanchor_receipts"][0]["content"] == replacement
    assert scopes(result)[0]["outcome"] == "findings_present"


@pytest.mark.parametrize("mode", ["oneshot", "oneshot_checked", "dvs"])
def test_opted_final_product_is_persisted_after_raw_calls_without_extra_model_call(monkeypatch, mode):
    from src.executor import chain_runner as cr, process_runner as pr
    process = spec()
    if mode == "oneshot":
        call, calls = sequence(output(record()))
    elif mode == "oneshot_checked":
        call, calls = sequence(output(record()), output(record(review=True)))
    else:
        call, calls = sequence(output(record()), output(record(review=True)), LEDGER_HEADING)
    saved, token_updates = [], []
    monkeypatch.setattr(pr, "_default_call", call)
    monkeypatch.setattr(cr, "save_output", lambda **kwargs: saved.append(kwargs))
    monkeypatch.setattr(cr, "update_job_tokens", lambda *args, **kwargs: token_updates.append(kwargs))
    result = cr._run_engine_process(CAP, process, SOURCE, "deep", None, "", None, None, "offline", 1.0, "a", None, False, None,
                                    mode=mode, documents={"a": SOURCE})
    expected_calls = {"oneshot": 1, "oneshot_checked": 2, "dvs": 3}[mode]
    assert len(calls) == len(token_updates) == expected_calls
    assert len(saved) == len(result) == expected_calls + 1
    assert "## Scope outcomes" in saved[0]["content"]
    assert "## Scope outcomes" not in saved[-1]["content"]
    assert "## Scope assessment" in saved[-1]["content"]
    assert saved[-1]["metadata"]["wall"]["scope_outcomes"]
    assert result[-1].content == saved[-1]["content"]


def test_scope_prose_with_row_like_lines_cannot_create_ledger_findings_on_reparse():
    from src.executor.ledger_walls import parse_rows
    basis = "The opening has no instance.\n" + row("INJECTED1")
    call, _ = sequence(output(record(basis=basis)))
    result = run_oneshot_checked(CAP, spec(), {"a": SOURCE}, call_fn=call, check=False)
    assert scopes(result)[0]["basis"] == basis  # assessment and receipt text preserved
    assert not parse_rows(result.final_content)
    assert "INJECTED1" in result.final_content  # rendered as ordinary prose, not hidden


def test_zero_rows_discloses_separate_scope_review_without_zero_of_zero_warning():
    call, _ = sequence(output(record()), output(record(review=True)))
    result = run_oneshot_checked(CAP, spec(), {"a": SOURCE}, call_fn=call)
    assert "Check incomplete: 0 of 0" not in result.final_content
    assert "No original finding rows; see the scope review below" in result.final_content
    assert not result.final_wall["check_ruling_coverage"]["coverage_complete"]
    assert scopes(result)[0]["review_state"] == "supported_within_stated_scope"


@pytest.mark.parametrize("stage", ["extract", "verify"])
def test_deep_partial_empty_calls_remain_visible_through_synthesis(stage):
    responses = [output(record()), output(record(review=True)), LEDGER_HEADING]
    ix = 0 if stage == "extract" else 1
    responses[ix] = {"content": responses[ix], "partial": True, "connection_error": "interrupted response"}
    call, _ = sequence(*responses)
    result = run_process(CAP, spec(), {"a": SOURCE}, call_fn=call, reanchor=False, parallelism=1)
    assert scopes(result)[0]["outcome"] == "inconclusive"
    assert "Invocation is known partial or failed" in result.final_content
    assert result.calls[ix].wall["scope_outcomes"][0]["evidence_state"]["invocation_partial"] is True


def test_scoped_synthesis_describes_retained_findings_without_claiming_all_confirmed():
    process = spec()
    prompt = compose_synthesize_prompt(CAP, process, process.final_step, {"a": SOURCE}, "")
    assert "rows a critic confirmed against the source" not in prompt.system
    assert "recorded review and evidence limits" in prompt.system


def test_failed_row_with_unknown_dimension_is_not_silently_discarded_as_absence():
    call, _ = sequence(output(record(), rows=[row(dim="oppositon", quote="An invented absent quotation with no match.")]))
    result = run_oneshot_checked(CAP, spec(), {"a": SOURCE}, call_fn=call, check=False)
    assert scopes(result)[0]["outcome"] == "inconclusive"
    assert "lost anchor evidence" in result.final_content
