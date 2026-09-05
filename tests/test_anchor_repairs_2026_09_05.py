"""Offline regressions for the first Harris reading; fixtures reproduce text-shape failures."""
import json
import re

import pytest

from src.dossier.common import analysis_ledger
from src.dossier.schemas import DossierJob
from src.dossier.walls import normalize
from src.executor.ledger_walls import SourceIndex, parse_rows, render_rows, verify_rows
from src.executor.process_runner import apply_rulings, assemble_checked_content
from src.sources.schemas import Document


@pytest.mark.parametrize("source,quote", [
    ("Our experi\u00ad\nences of misrecognition are a product of power structures.",
     "Our experiences of misrecognition are a product of power structures."),
    ("The most esteemed voca\u00ad\r\n tions are widely accepted as being underpaid.",
     "The most esteemed vocations are widely accepted as being underpaid."),
    ("The plurality of irresolvable and fatal weak\u00ad\nnesses makes repair futile.",
     "The plurality of irresolvable and fatal weaknesses makes repair futile."),
    ("deco\u00ad\nlonial theory", "decolonial theory"),
    ("discre\u00adtionary", "discretionary"),
])
def test_explicit_discretionary_breaks_verify_the_whole_quote(source, quote):
    row = parse_rows(f'- [F1] Finding — anchor: "{quote}"')[0]
    report = verify_rows([row], SourceIndex({"doc": source}))
    assert report.verified == 1 and report.trimmed == 0
    assert row.anchor == quote


def test_soft_hyphen_fix_does_not_join_unmarked_words_or_remove_real_hyphens():
    assert normalize("separate\nwords") == "separate words"
    assert normalize("re-form") == "re-form"
    assert normalize("co\u00ad\noperate") == "cooperate"
    index = SourceIndex({"doc": "A market-\ndriven account of social life."})
    assert index.find("market-driven account") == "doc"  # existing alternate index retained
    assert SourceIndex({"doc": "The committee chose to re-form the institution."}).find("reform") is None


@pytest.mark.parametrize("label", ["counter-anchor", "anchor-counter", "anchor-b"])
def test_a_fabricated_secondary_quote_cannot_pass_as_a_verified_row(label):
    primary = "The text presents an observed structural relation."
    absent = "This purported counterevidence appears in no source."
    row = parse_rows(f'- [D4.F1] Finding — anchor: "{primary}" — {label}: "{absent}"')[0]
    report = verify_rows([row], SourceIndex({"doc": primary}))
    assert report.anchors == 2 and report.verified_anchors == 1
    assert not row.anchor_verified and report.failed_ids == ["D4.F1"]
    assert not verify_rows(parse_rows(row.render()), SourceIndex({"doc": primary})).verified


def test_counter_anchor_inherits_single_document_and_roundtrips_for_desks():
    first, second = "The text presents a structural premise.", "The counterexample limits its universal scope."
    row = parse_rows(f'- [D4.F1] Finding — anchor: "{first}" — doc: paper — counter-anchor: "{second}"')[0]
    index = SourceIndex({"paper": first + " " + second})
    assert verify_rows([row], index).verified_anchors == 2
    assert row.extra_anchors[0].doc == "paper"
    reparsed = parse_rows(row.render())[0]
    assert verify_rows([reparsed], index).verified_anchors == 2
    job = DossierJob()
    job.analysis = {"1.0": {"final_output": render_rows([row])}}
    desk = analysis_ledger(job, [Document(key="paper", title="Paper", text=first + " " + second)])
    assert first in desk and second in desk


def test_counter_anchor_respects_its_declared_document():
    first, second = "A premise is introduced in the early account.", "The later account expressly limits that premise."
    text = f'- [P6.F1] Finding — anchor: "{first}" — doc: early — counter-anchor: "{second}" — counter-doc: late'
    index = SourceIndex({"early": first, "late": second})
    assert verify_rows(parse_rows(text), index, require_cross_document=True).verified == 1
    assert verify_rows(parse_rows(text.replace("counter-doc: late", "counter-doc: early")), index).verified == 0


def test_prefix_match_history_survives_rendering_and_reverification():
    primary = "The committee found that the proposed reform was ineffective."
    second = "The later report expressly rejected the proposed alternative."
    row = parse_rows(f'- [F1] Finding — anchor: "{primary} invented ending" — anchor-b: "{second} invented ending"')[0]
    index = SourceIndex({"doc": primary + " " + second})
    assert verify_rows([row], index).trimmed == 1
    rendered = row.render()
    assert "trimmed-anchor: yes" in rendered and "trimmed-anchor-b: yes" in rendered
    reparsed = parse_rows(rendered)[0]
    assert verify_rows([reparsed], index).trimmed == 1
    assert reparsed.anchor_trimmed and reparsed.extra_anchors[0].trimmed


@pytest.mark.parametrize("field", ["revised-finding", "finding rewritten to"])
def test_explicit_weakening_reaches_desks_and_preserves_original_finding(field):
    original, revised = "Recognition explains every injustice.", "Recognition explains some injustices."
    rows = parse_rows(f'- [F1] {original} — anchor: "{revised}" — confidence: high')
    rulings = parse_rows(f'- [F1] {original} — anchor: "{revised}" — status: weakened — reason: overreach '
                        f'— confidence: medium — {field}: {json.dumps(revised)}')
    index = SourceIndex({"paper": revised})
    verify_rows(rows, index)
    kept, rejected, unverified, report = apply_rulings(rows, rulings, index)
    assert kept[0].finding == revised
    final = assemble_checked_content("Reading stays as written.", "", kept, rejected, unverified, report, "critic")
    assert f'original-finding: {json.dumps(original)}' in final
    assert parse_rows(final)[0].finding == revised
    job = DossierJob()
    job.analysis = {"1.0": {"final_output": final}}
    desk = analysis_ledger(job, [Document(key="paper", title="Paper", text=revised)])
    assert revised in desk and original not in desk


def test_existing_rewritten_head_is_used_without_inventing_replacement_from_reason():
    rows = parse_rows('- [F1] A universal claim. — anchor: "Only a narrower claim is supported."')
    rulings = parse_rows('- [F1] A narrower claim. — anchor: "Only a narrower claim is supported." '
                        '— status: weakened — reason: could perhaps use some other wording')
    index = SourceIndex({"doc": "Only a narrower claim is supported."})
    verify_rows(rows, index)
    kept, _, _, _ = apply_rulings(rows, rulings, index)
    assert kept[0].finding == "A narrower claim."
    assert 'original-finding: "A universal claim."' in kept[0].render()


def test_quoted_replacement_can_contain_quotes_and_field_like_prose():
    revised = 'The text says "recognition" — reason: its scope is limited.'
    row = parse_rows('- [F1] Original — anchor: "A quote" — status: weakened '
                     f'— revised-finding: {json.dumps(revised)} — confidence: medium')[0]
    assert row.revised_finding == revised


@pytest.mark.parametrize("field", ['revised-finding: unquoted text', 'revised-finding: ""',
                                 'revised-finding: "one" — finding rewritten to: "two"'])
def test_ambiguous_or_malformed_explicit_weakening_is_rejected(field):
    with pytest.raises(ValueError, match="revised-finding"):
        parse_rows(f'- [F1] Finding — anchor: "A quote" — status: weakened — {field}')


def test_unverified_receipt_does_not_assert_the_quote_is_a_paraphrase():
    row = parse_rows('- [F1] Finding — anchor: "A quotation absent from the extracted text."')[0]
    rep = {"in": 1, "confirmed": 1, "carried": 0, "weakened": 0, "rejected": 0,
           "added": 0, "added_dropped": 0, "unverified": 1}
    content = assemble_checked_content("Reading", "", [row], [], [row], rep, "critic")
    assert "unverified or incomplete anchor" in content
    assert "paraphrased quote" not in content


@pytest.mark.parametrize("revised", [
    'The text says "recognition" — reason: its scope is limited.',
    'The label is — revised-finding: "quoted language", used as an example.',
    'The text uses anchor: "a rhetorical label" as an example.',
    'The text uses counter-anchor: "a rhetorical label" as an example.',
    'The quotation says — status: rejected — doc: missing — dim: wrong — from: F99 — confidence: low.',
])
def test_explicit_revision_roundtrip_preserves_field_like_prose_and_actual_metadata(revised):
    source = "Recognition has a limited scope in the text."
    original = 'The original quotes "prefix — revised-finding: suggested text — anchor: fake — status: rejected".'
    rows = parse_rows(f'- [F1] {original} — anchor: "{source}" — dim: givens — confidence: high')
    rulings = parse_rows(f'- [F1] An old finding — anchor: "{source}" — status: weakened — dim: givens '
                        f'— revised-finding: {json.dumps(revised, ensure_ascii=False)} — confidence: medium')
    index = SourceIndex({"paper": source})
    verify_rows(rows, index)
    kept, rejected, unverified, report = apply_rulings(rows, rulings, index)
    final = assemble_checked_content("Reading unchanged.", "", kept, rejected, unverified, report, "critic")
    reparsed = parse_rows(final)[0]
    assert reparsed.finding == revised and reparsed.revised_finding == revised
    assert reparsed.status == "weakened" and reparsed.confidence == "medium" and reparsed.dim == "givens"
    assert reparsed.doc == "paper" and reparsed.lineage == [] and len(reparsed.anchors) == 1
    assert reparsed.anchor == source and verify_rows([reparsed], index).verified == 1
    assert "original-finding: " + json.dumps(original, ensure_ascii=False) in final
    assert parse_rows(reparsed.render())[0].finding == revised
    job = DossierJob(); job.analysis = {"1.0": {"final_output": final}}
    desk = analysis_ledger(job, [Document(key="paper", title="Paper", text=source)])
    assert revised in desk and original not in desk


@pytest.mark.parametrize("prose", [
    'The example is "prefix — revised-finding: not a metadata field".',
    'The example is “prefix — revised-finding: also not metadata”.',
    'The example is \'prefix — revised-finding: still not metadata\'.',
])
def test_historical_quoted_prose_does_not_trigger_explicit_revision_shape_errors(prose):
    text = f'- [F1] {prose} — anchor: "A source quotation supports the finding." — status: confirmed'
    row = parse_rows(text)[0]
    assert row.finding == prose and row.revised_finding == "" and row.status == "confirmed"
    assert parse_rows(row.render())[0].finding == prose


@pytest.mark.parametrize("head", [
    "Omission: the historical continuity remains unsupported",
    "Strongest form: the account is conditional",
    "Attack on Marx: the interpretation is disputed",
    "Warrant: the passage supplies a reason",
])
def test_legacy_colon_heads_remain_findings_instead_of_metadata(head):
    row = parse_rows(f'- [F1] {head} — anchor: "A source quotation supports the finding."')[0]
    assert row.finding == head and parse_rows(row.render())[0].finding == head


def test_runner_fingerprint_includes_normalization_code():
    from scripts.study_ideas_material import CODE_FILES
    assert "src/dossier/walls.py" in CODE_FILES


@pytest.mark.parametrize("spelling", ["promised-at", "promised‑at"])
def test_legacy_omission_quote_slots_still_supply_an_anchor(spelling):
    quote = "The text promises an explicit account of historical continuity."
    row = parse_rows(f'- [F1] Omission: no traced institution — dim: omissions — {spelling}: “{quote}” '
                     '— nearest-delivery: no supporting example — confidence: medium')[0]
    assert row.finding == "Omission: no traced institution" and row.dim == "omissions" and row.anchor == quote
    assert verify_rows([row], SourceIndex({"paper": quote})).verified == 1


@pytest.mark.parametrize("fields", [
    'anchor: "The first quotation is present here." — anchor: "A different quotation is absent here."',
    'anchor-counter: "The first quotation is present here." — counter-anchor: "A different quotation is absent here."',
])
def test_repeated_actual_anchor_fields_are_ambiguous_instead_of_last_wins(fields):
    with pytest.raises(ValueError, match="repeated anchor fields"):
        parse_rows(f'- [F1] Finding — {fields}')


def test_legacy_scalar_fields_keep_prefix_recognition_without_scanning_quoted_prose():
    row = parse_rows('- [F1] Finding — anchor: "A source quotation is present." — status: weakened (narrower) '
                     '— confidence: high (qualified) — dim: givens (scope) — doc: [paper] — supplied') [0]
    assert (row.status, row.confidence, row.dim, row.doc) == ("weakened", "high", "givens", "paper")



def test_revision_and_original_provenance_do_not_become_fallback_evidence_after_render():
    revised = "Recognition has a limited scope in the text."
    original = "The original finding has a much wider scope."
    index = SourceIndex({"paper": revised + " " + original})
    rows = parse_rows(f'- [F1] {original} — confidence: high')
    rulings = parse_rows(f'- [F1] Old finding — status: weakened — revised-finding: {json.dumps(revised)}')
    assert rulings[0].anchor == ""
    kept, _, unverified, _ = apply_rulings(rows, rulings, index)
    assert unverified == kept
    reparsed = parse_rows(kept[0].render())[0]
    assert reparsed.finding == revised and reparsed.anchor == ""
    assert verify_rows([reparsed], index).verified == 0


def test_explicit_absent_anchor_does_not_use_a_quotation_in_the_finding_as_evidence():
    quote = "is the source (Searle) an expert?"
    row = parse_rows(f'- [V.F9] Authority question “{quote}”: unaddressed — anchor: none — status: added')[0]
    assert row.anchor == ""
    assert verify_rows([row], SourceIndex({"paper": quote})).verified == 0
    assert parse_rows(row.render())[0].anchor == ""


@pytest.mark.parametrize("ruling", ["confirmed", "weakened", "rejected", "added"])
def test_checked_receipt_discloses_ledger_changes_while_preserving_original_prose(ruling):
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.executor.process_runner import run_oneshot_checked
    quote = "Recognition explains some injustices in this account."
    prose = "Recognition explains every injustice [F1]."
    reading = (f'{prose}\n\n## Findings ledger\n- [F1] Recognition explains every injustice. — anchor: "{quote}"\n'
               f'- [F2] A second finding. — anchor: "{quote}"')
    changed = (f'- [F1] Recognition explains every injustice. — anchor: "{quote}" '
               f'— status: {"confirmed" if ruling == "added" else ruling}')
    if ruling == "weakened":
        changed += f' — revised-finding: {json.dumps(quote)}'
    critic = f'## Findings ledger\n{changed}\n- [F2] A second finding. — anchor: "{quote}" — status: confirmed'
    if ruling == "added":
        critic += f'\n- [V.F1] A new finding. — anchor: "{quote}" — status: added'
    cap = get_engine_registry().get_capability_definition("conditions_of_possibility_analyzer")
    spec = get_operationalization_registry().get(cap.engine_key).process
    def fake(*args, model_hint, **kwargs):
        return {"content": critic, "model_used": model_hint}
    result = run_oneshot_checked(cap, spec, {"paper": quote}, reading=reading, call_fn=fake)
    assert result.final_content.split("## Findings ledger", 1)[0].strip() == prose
    disclosure = "The ledger incorporates the critic's changes; the preceding prose is unchanged from the original reading."
    assert (disclosure in result.final_content.split("### Check receipt", 1)[1]) == (ruling != "confirmed")
    assert result.calls[-1].content == critic



def test_auxiliary_references_are_not_duplicate_rulings_and_raw_tail_is_preserved():
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.executor.process_runner import run_oneshot_checked
    quote = "The reading is supported by this source sentence."
    reading = f'Reading [F1].\n\n## Findings ledger\n- [F1] Original — anchor: "{quote}"\n### Open questions\n- Original question stays.'
    critic = f'## Findings ledger\n- [F1] Original — anchor: "{quote}" — status: confirmed\n'
    critic += '### Must keep\n- [F1] This is an important reference.\n### Counter-evidence\n- [F1] A reference, not a ruling.\n### Open questions\n- [F1] Another reference.'
    cap = get_engine_registry().get_capability_definition("argument_architecture")
    spec = get_operationalization_registry().get("argument_architecture").process
    def fake(*args, model_hint, **kwargs):
        return {"content": critic, "model_used": model_hint}
    result = run_oneshot_checked(cap, spec, {"paper": quote}, reading=reading, call_fn=fake)
    assert [r.id for r in parse_rows(critic)] == ["F1"]
    assert result.calls[-1].content == critic and '### Must keep' in result.calls[-1].content
    assert 'Original question stays.' in result.final_content
    assert result.final_wall['duplicate_ids'] == [] and result.final_wall['check_confirmed'] == 1
    duplicate = critic.split('### Must keep')[0] + f'- [F1] Conflicting ruling — anchor: "{quote}" — status: rejected'
    with pytest.raises(RuntimeError, match="duplicate ledger ids"):
        apply_rulings(parse_rows(reading), parse_rows(duplicate), SourceIndex({"paper": quote}))


def test_a_new_explicit_ledger_resumes_after_an_auxiliary_section():
    rows = parse_rows('## Findings ledger\n- [F1] First — anchor: "one"\n### Must keep\n- [F1] Reference\n'
                      '## Findings ledger\n- [F2] Second — anchor: "two"')
    assert [r.id for r in rows] == ["F1", "F2"]


@pytest.mark.parametrize("document_count", [1, 2])
def test_deep_critic_replacement_is_the_rendered_synthesis_head(document_count):
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.executor.process_runner import run_process

    cap = get_engine_registry().get_capability_definition("conditions_of_possibility_analyzer")
    spec = get_operationalization_registry().get(cap.engine_key).process.model_copy(deep=True)
    spec.dimensions = [next(d for d in spec.dimensions if d.scope == scope)
                       for scope in ("document", "corpus")]
    docs = dict(list({"early": "The early account limits the scope of recognition.",
                      "late": "The later account explicitly qualifies the inherited premise."}.items())[:document_count])
    original = "Recognition necessarily explains every injustice."
    revised = 'Recognition explains some injustices — reason: the text uses "recognition" — anchor: "as an example".'
    critic_receipts, synthesis_ledgers = [], []

    def fake(system, user, *, model_hint, label, **_):
        if "| extract |" in label:
            prefix = re.search(r"^- \[([^]]+)\.F1\]", system, re.M).group(1)
            corpus_row = f"| {spec.dimensions[1].key}" in label
            doc = "early" if corpus_row else re.search(r"SOURCE \[([^]]+)\]", user).group(1)
            content = (f'## Findings ledger\n- [{prefix}.F1] {original} '
                       f'— dim: {spec.dimensions[int(corpus_row)].key} — anchor: "{docs[doc]}" — doc: {doc}')
            if corpus_row:
                content += f' — anchor-b: "{docs["late"]}" — doc-b: late'
        elif "| verify" in label:
            rows = parse_rows(user.split("EXTRACTION LEDGERS:", 1)[1])
            content = "## Findings ledger\n" + "\n".join(
                r.render() + f' — status: weakened — revised-finding: {json.dumps(revised)}'
                for r in rows)
            content += "\n### Must keep\n" + "\n".join(
                f'- [{r.id}] Auxiliary reference explaining why the finding matters.' for r in rows)
            critic_receipts.append(content)
        else:
            # A positive reference must not leak into the rejected-rulings section.
            assert "Auxiliary reference explaining" not in user
            ledger = user.split("VERIFIED FINDINGS LEDGER:", 1)[1]
            synthesis_ledgers.append(ledger)
            rows = parse_rows(ledger)
            assert len(rows) == (1 if document_count == 1 else 3)
            for i, row in enumerate(rows, 1):
                # Inspect the actual prompt head, not just the parser's replacement property.
                assert row.text.startswith(json.dumps(revised, ensure_ascii=False) + " — ")
                assert original not in row.text
                assert row.finding == revised and row.status == "weakened"
                assert row.anchor in docs.values() and row.lineage == []
                before = (row.raw, row.text)
                assert parse_rows(row.render())[0].finding == revised
                assert (row.raw, row.text) == before  # Rendering preserves the raw receipt.
                row.text += f" — from: {row.id}"
                row.id = f"F{i}"
            content = "# Reading\nThe account has a limited scope [F1].\n\n" + render_rows(rows)
        return {"content": content, "model_used": model_hint, "input_tokens": 1, "output_tokens": 1}

    result = run_process(cap, spec, docs, depth="deep", call_fn=fake, parallelism=1)
    assert synthesis_ledgers and result.final_wall["failed_ids"] == []
    assert result.final_wall["missing_lineage"] == []
    assert result.final_wall["verified_anchors"] == (1 if document_count == 1 else 4)
    actual_critics = [c.content for c in result.calls if c.step_key == "verify"]
    assert actual_critics == critic_receipts
    assert all(original in raw for raw in actual_critics)
    job = DossierJob(); job.analysis = {"1.0": {"final_output": result.final_content}}
    desk = analysis_ledger(job, [Document(key=k, title=k, text=v) for k, v in docs.items()])
    assert revised in desk and original not in desk


@pytest.mark.parametrize("quote", [
    'they remained, in Karl Polanyi\'s famous formulation (1978 [1944]: 88 f.), "socially embedded."',
    'Every society institutes at once its institution and the "legitimation" thereof.',
    'Markets are no longer "embedded" in society (Polanyi 1978 [1944]: 88 f.); conversely, society has rather transformed into an "appendage" of markets and of money as their medium.',
])
@pytest.mark.parametrize("label", ["anchor", "anchor-b", "counter-anchor"])
def test_real_corpus_json_escaped_anchors_verify_the_complete_literal_and_roundtrip(quote, label):
    primary = "The earlier source sets out the premise for this comparison."
    fields = f'{label}: {json.dumps(quote, ensure_ascii=False)} (p. 110)'
    if label != "anchor":
        fields = f'anchor: "{primary}" — {fields}'
    raw = f'- [P6.F1] A source-grounded comparison. — {fields} — confidence: high'
    row = parse_rows(raw)[0]
    assert row.anchors[-1].quote == quote and not row.anchors[-1].parse_error
    index = SourceIndex({"paper": primary + " " + quote})
    rep = verify_rows([row], index)
    assert rep.verified == 1 and rep.trimmed == 0 and rep.invalid_anchor_ids == []
    rendered = row.render()
    assert json.dumps(quote, ensure_ascii=False) in rendered and '(p. 110)' in rendered
    assert row.raw == raw
    reparsed = parse_rows(rendered)[0]
    assert reparsed.anchors[-1].quote == quote and verify_rows([reparsed], index).verified == 1
    job = DossierJob(); job.analysis = {"1.0": {"final_output": "## Findings ledger\n" + rendered}}
    desk = analysis_ledger(job, [Document(key="paper", title="Paper", text=primary + " " + quote)])
    assert quote in desk


@pytest.mark.parametrize("literal", [
    '"Simmel\'s paradoxical characterization of money as an "absolute means" is more appropriate"',
    '“Simmel\'s paradoxical characterization of money as an “absolute means” is more appropriate”',
    "'Simmel describes the 'absolute means' of economic exchange in the text.'",
])
def test_ambiguous_inner_quotes_are_unverified_without_rewriting_the_displayed_literal(literal):
    raw = f'- [P6.F2] Finding — anchor: {literal} — doc: paper'
    row = parse_rows(raw)[0]
    index = SourceIndex({"paper": literal})
    rep = verify_rows([row], index)
    assert row.anchor == "" and row.anchor_parse_error
    assert rep.invalid_anchor_ids == ['P6.F2'] and rep.verified == 0 and rep.trimmed == 0
    assert row.raw == raw
    rendered = row.render()
    assert f'anchor: {literal}' in rendered and 'quote-error:' in rendered
    reparsed = parse_rows(rendered)[0]
    assert reparsed.anchor_parse_error and verify_rows([reparsed], index).verified == 0
    assert reparsed.render().count('quote-error:') == 1


def test_quote_parsing_does_not_remove_the_deliberate_source_prefix_trimming_policy():
    source = 'The text describes money as an "absolute means" in the economy.'
    raw = f'- [F1] Finding — anchor: {json.dumps(source + " fabricated ending absent from the source")}'
    row = parse_rows(raw)[0]
    assert row.anchor.endswith('fabricated ending absent from the source') and not row.anchor_parse_error
    rep = verify_rows([row], SourceIndex({"paper": source}))
    assert rep.verified == 1 and rep.trimmed == 1 and rep.invalid_anchor_ids == []
    assert row.anchor == source
    rendered = row.render()
    assert json.dumps(source) in rendered and 'trimmed-anchor: yes' in rendered
    assert 'fabricated ending' not in rendered and 'quote-error:' not in rendered


@pytest.mark.parametrize("ambiguous_slot", ["anchor", "anchor-b"])
@pytest.mark.parametrize("exposed_field", [False, True])
def test_corpus_reanchor_can_replace_an_ambiguous_literal_and_make_the_pair_citable(ambiguous_slot, exposed_field):
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.executor.process_runner import run_process
    docs = {"early": 'The earlier paper calls money an "absolute means" of exchange.',
            "late": 'The later paper examines the "legitimation" of this institution.'}
    cap = get_engine_registry().get_capability_definition("conditions_of_possibility_analyzer")
    spec = get_operationalization_registry().get(cap.engine_key).process.model_copy(deep=True)
    spec.dimensions = [next(d for d in spec.dimensions if d.scope == scope) for scope in ("document", "corpus")]
    corpus_dim = spec.dimensions[1]
    repaired = []
    malformed = {doc: ('"' + text.split('"')[0] + '"quoted — doc: invented" after the quotation"'
                       if exposed_field else '"' + text + '"') for doc, text in docs.items()}
    def fake(system, user, *, model_hint, label, **_):
        if '| extract |' in label:
            prefix = re.search(r'^- \[([^]]+)\.F1\]', system, re.M).group(1)
            if f'| {corpus_dim.key}' in label:
                fields = []
                for slot, doc in [('anchor', 'early'), ('anchor-b', 'late')]:
                    literal = json.dumps(docs[doc])
                    if slot == ambiguous_slot and '(re-anchor)' not in label:
                        literal = malformed[doc]
                    fields.append(f'{slot}: {literal} — {"doc" if slot == "anchor" else "doc-b"}: {doc}')
                if '(re-anchor)' in label:
                    assert malformed['early' if ambiguous_slot == 'anchor' else 'late'] in user
                    assert ('quote-error:' if ambiguous_slot == 'anchor' else 'quote-error-b:') in user
                    repaired.append(label)
                content = f'- [{prefix}.F1] Across the texts — dim: {corpus_dim.key} — ' + ' — '.join(fields)
                if '(re-anchor)' in label:
                    suffix = '' if ambiguous_slot == 'anchor' else '-b'
                    content += f' — quote-error{suffix}: stale diagnostic copied from the repair request'
            else:
                doc = re.search(r'SOURCE \[([^]]+)\]', user).group(1)
                content = f'- [{prefix}.F1] A premise — anchor: {json.dumps(docs[doc])} — doc: {doc}'
        elif '| verify' in label:
            content = user.split('EXTRACTION LEDGERS:', 1)[1]
        else:
            rows = parse_rows(user.split('VERIFIED FINDINGS LEDGER:', 1)[1])
            corpus = next(r for r in rows if r.dim == corpus_dim.key)
            assert not any(a.parse_error for a in corpus.anchors)
            assert 'quote-error' not in corpus.render()
            content = '# Reading\nThe later text revises the earlier premise [F1].\n\n## Findings ledger\n'
            content += (f'- [F1] Across the texts — dim: {corpus_dim.key} — anchor: {json.dumps(docs["early"])} — doc: early '
                        f'— anchor-b: {json.dumps(docs["late"])} — doc-b: late — from: {corpus.id}')
        return {'content': content, 'model_used': model_hint}
    result = run_process(cap, spec, docs, depth='deep', call_fn=fake, parallelism=1)
    assert len(repaired) == 1 and result.final_wall['verified_anchors'] == 2
    extraction = next(c for c in result.calls if c.dimension_key == corpus_dim.key)
    assert extraction.wall['invalid_anchor_ids'] == [f'{corpus_dim.id_prefix}.F1']
    assert extraction.reanchored == 1 and extraction.wall['after_reanchor']['invalid_anchor_ids'] == []
    final = parse_rows(result.final_content)[0]
    assert verify_rows([final], SourceIndex(docs), require_cross_document=True).verified == 1
    assert final.anchors[0].quote == docs['early'] and final.anchors[1].quote == docs['late']


@pytest.mark.parametrize('engine,predecessor,row_id,dimension', [
    ('conditions_of_possibility_analyzer', 'P6.F3', 'F8', 'visibility'),
    ('inferential_commitment_mapper', 'X6.F11', 'F14', 'consequences'),
    ('inferential_commitment_mapper', 'V.CORPUS.F1', 'F15', 'consequences'),
    ('conditions_of_possibility_analyzer', '', 'P6.F8', 'visibility'),
])
@pytest.mark.parametrize('paired', [False, True])
def test_desks_preserve_encoded_corpus_provenance_for_final_descendants(engine, predecessor, row_id, dimension, paired):
    early = 'The first source states the premise for this comparison.'
    late = 'The later source changes that premise explicitly.'
    row = f'- [{row_id}] A later conclusion — dim: {dimension} — anchor: "{late}" — doc: late'
    if paired:
        row += f' — anchor-b: "{early}" — doc-b: early'
    if predecessor:
        row += f' — from: {predecessor}'
    job = DossierJob(); job.analysis = {'1': {'engine_key': engine, 'final_output': '## Findings ledger\n' + row}}
    out = analysis_ledger(job, [Document(key=k, title=k, text=v) for k, v in {'early': early, 'late': late}.items()])
    citable, _, unverified = out.partition('Rows whose anchors are unverified or incomplete')
    assert (f'[{row_id}]' in citable) is paired
    assert (f'[{row_id}]' in unverified) is not paired
    if paired:
        assert 'anchor [late]' in citable and 'anchor [early]' in citable


@pytest.mark.parametrize('predecessor', ['P60.F3', 'XP6.F3', 'V.CORPUSX.F1', 'V.DOC1.F1'])
def test_corpus_namespace_matching_does_not_capture_similar_or_document_prefixes(predecessor):
    quote = 'The original source supports this document-level conclusion.'
    job = DossierJob(); job.analysis = {'1': {'engine_key': 'conditions_of_possibility_analyzer',
        'final_output': f'## Findings ledger\n- [F1] Ordinary finding — dim: visibility — anchor: "{quote}" — doc: document — from: {predecessor}'}}
    docs = [Document(key='actual', title='Actual', text=quote), Document(key='other', title='Other', text='No matching quote.')]
    out = analysis_ledger(job, docs)
    assert '- [F1]' in out.split('Rows whose anchors are unverified or incomplete')[0]
    assert f'anchor [actual]: "{quote}"' in out  # Ordinary foreign executor keys retain the existing fallback.


def test_desks_use_the_composers_uppercase_key_fallback_for_a_corpus_namespace(monkeypatch):
    from types import SimpleNamespace
    import src.operationalizations.registry as registry
    from src.stages.process_composer import dim_prefix
    dim = SimpleNamespace(scope='corpus', id_prefix='', key='links')
    assert dim_prefix(dim) == 'LINKS'
    monkeypatch.setattr(registry, 'get_operationalization_registry', lambda: SimpleNamespace(
        get=lambda _: SimpleNamespace(process=SimpleNamespace(dimensions=[dim]))))
    quote = 'The later source supplies only half of the required comparison.'
    job = DossierJob(); job.analysis = {'1': {'engine_key': 'fixture', 'final_output':
        f'## Findings ledger\n- [F1] Comparison — dim: conclusion — anchor: "{quote}" — doc: late — from: LINKS.F1'}}
    out = analysis_ledger(job, [Document(key='late', title='Late', text=quote), Document(key='early', title='Early', text='Earlier source.')])
    citable, _, unverified = out.partition('Rows whose anchors are unverified or incomplete')
    assert '[F1]' not in citable and '[F1]' in unverified


@pytest.mark.parametrize('secondary', [False, True])
@pytest.mark.parametrize('with_documents', [False, True])
def test_desks_keep_malformed_primary_and_secondary_quotes_visible_as_unverified(secondary, with_documents):
    quote = 'The term "capitalism" names a social system in the later text.'
    literal = '"' + quote + '"'
    row = '- [F11] The later text defines capitalism as a social system — '
    if secondary:
        row += 'anchor: "The earlier text supplies a valid premise." — doc: early — '
    row += f'{"anchor-b" if secondary else "anchor"}: {literal} — {"doc-b" if secondary else "doc"}: late'
    job = DossierJob(); job.analysis = {'1': {'final_output': '## Findings ledger\n' + row}}
    docs = [Document(key='early', title='Early', text='The earlier text supplies a valid premise.'),
            Document(key='late', title='Late', text=quote)] if with_documents else None
    out = analysis_ledger(job, docs)
    citable, _, unverified = out.partition('Rows whose anchors are unverified or incomplete')
    assert '[F11]' not in citable and '[F11]' in unverified
    assert 'near [late]: (unverified quotation: ambiguous inner quotation marks; use JSON-escaped double quotes)' in unverified
    assert 'The later text defines capitalism as a social system' in unverified
    assert job.analysis['1']['final_output'].endswith(row) and literal in row


@pytest.mark.parametrize('secondary', [False, True])
def test_exposed_field_like_prose_after_an_inner_quote_cannot_verify_a_prefix(secondary):
    source = 'The source makes a claim supported by evidence.'
    row = '- [F1] Claim — '
    if secondary:
        row += 'anchor: "The other source supports the comparison." — doc: other — '
    slot = 'anchor-b' if secondary else 'anchor'
    doc = 'doc-b' if secondary else 'doc'
    row += f'{slot}: "The source makes a claim "quoted — {doc}: invented" after the quotation" — {doc}: actual'
    parsed = parse_rows(row)[0]
    index = SourceIndex({'actual': source, 'other': 'The other source supports the comparison.'})
    report = verify_rows([parsed], index)
    assert report.verified == 0 and report.invalid_anchor_ids == ['F1'] and report.trimmed == 0
    assert parsed.anchors[-1].quote == '' and 'unexpected text' in parsed.anchors[-1].parse_error
    rendered = parsed.render()
    assert '"The source makes a claim "quoted' in rendered
    reparsed = parse_rows(rendered)[0]
    assert verify_rows([reparsed], index).verified == 0 and reparsed.anchors[-1].parse_error


@pytest.mark.parametrize('trailer', ['', '.', '(p. 110)', '(Rose, 1981: 214).', '[p. 7]', 'pp. 12–14', 'p. 110.'])
def test_quote_trailer_grammar_preserves_citations_pages_and_punctuation(trailer):
    quote = 'The source supplies the complete quotation for this finding.'
    row = parse_rows(f'- [F1] Finding — anchor: "{quote}" {trailer} — doc: actual')[0]
    assert verify_rows([row], SourceIndex({'actual': quote})).verified == 1
    assert row.anchor == quote and not row.anchor_parse_error
    assert trailer in row.render()


def test_unquoted_attribution_trailer_is_unverified_without_erasing_the_displayed_value():
    raw = '- [F34] Finding — anchor: “Essence must appear,” Hegel says (Hegel, 2010: 418).'
    row = parse_rows(raw)[0]
    assert row.anchor_parse_error and row.anchor == ''
    assert verify_rows([row], SourceIndex({'paper': 'Essence must appear,'})).verified == 0
    assert '“Essence must appear,” Hegel says (Hegel, 2010: 418).' in row.render()


@pytest.mark.parametrize('declarations', [
    'doc: invented — doc: actual',
    'doc-b: invented — doc-b: actual',
    'counter-doc: invented — doc-counter: actual',
    'counter-doc: invented — doc‑counter: actual',
])
def test_duplicate_document_declarations_are_nonfatal_and_do_not_bind_one_key(declarations):
    quote = 'The source makes a claim supported by evidence.'
    fields = f'anchor: "{quote}"'
    if declarations.startswith('doc-b:'):
        fields += f' — anchor-b: "{quote}"'
    elif declarations.startswith('counter-doc:'):
        fields += f' — counter-anchor: "{quote}"'
    row = parse_rows(f'- [F1] Finding — {fields} — {declarations}')[0]
    target = row.anchors[-1]
    assert target.doc == '' and 'ambiguous document declarations' in target.parse_error
    report = verify_rows([row], SourceIndex({'actual': quote}))
    assert report.verified == 0 and report.invalid_anchor_ids == ['F1']
    reparsed = parse_rows(row.render())[0]
    assert verify_rows([reparsed], SourceIndex({'actual': quote})).verified == 0


@pytest.mark.parametrize('value', ['invented" after the quotation"', 'actual unexplained prose', '[actual] (supplied)', '[actual', 'actual]'])
def test_document_key_segments_do_not_accept_only_a_valid_prefix(value):
    quote = 'The source makes a claim supported by evidence.'
    row = parse_rows(f'- [F1] Finding — anchor: "{quote}" — doc: {value}')[0]
    assert row.doc == '' and 'invalid document declaration' in row.anchor_parse_error
    assert verify_rows([row], SourceIndex({'actual': quote})).verified == 0


@pytest.mark.parametrize('suffix', ['', ' — drawn', ' — presupposed in the later text', ' — stopped'])
@pytest.mark.parametrize('key', ['document', '[document]'])
def test_complete_foreign_executor_keys_keep_fallback_and_separate_unlabeled_slots(key, suffix):
    quote = 'The source makes a claim supported by evidence.'
    row = parse_rows(f'- [F1] Finding — anchor: "{quote}" — doc: {key}{suffix} — confidence: high')[0]
    assert row.doc == 'document' and not row.anchor_parse_error
    assert verify_rows([row], SourceIndex({'actual': quote})).verified == 1
    assert suffix in row.render()


@pytest.mark.parametrize('duplicate', [False, True])
def test_inner_field_with_no_bare_anchor_tail_still_fails_document_shape(duplicate):
    row = '- [F1] Claim — anchor: "The source makes a claim " — doc: invented" after the quotation"'
    if duplicate:
        row += ' — doc: actual'
    parsed = parse_rows(row)[0]
    assert parsed.anchor == 'The source makes a claim' and parsed.anchor_parse_error
    assert verify_rows([parsed], SourceIndex({'actual': 'The source makes a claim supported by evidence.'})).verified == 0


@pytest.mark.parametrize('secondary', [False, True])
@pytest.mark.parametrize('duplicate', [False, True])
def test_document_shape_failure_can_be_reanchored_with_a_complete_verified_corpus_pair(secondary, duplicate):
    from src.executor.process_runner import StepCall, _wall_extraction
    from src.stages.process_composer import ProcessPrompt
    docs = {'early': 'The earlier source supplies a premise for the comparison.',
            'late': 'The later source changes that premise explicitly.'}
    fields = []
    for slot, doc in [('anchor', 'early'), ('anchor-b', 'late')]:
        doc_name = 'doc-b' if slot == 'anchor-b' else 'doc'
        declaration = f'{doc_name}: {doc}'
        if (slot == 'anchor-b') == secondary:
            declaration = (f'{doc_name}: invented — {doc_name}: {doc}' if duplicate else
                           f'{doc_name}: {doc}" unexplained quotation tail"')
        fields.append(f'{slot}: "{docs[doc]}" — {declaration}')
    raw = '- [P6.F1] Corpus finding — ' + ' — '.join(fields)
    prompt = ProcessPrompt(engine_key='fixture', step_key='extract', kind='extract',
        system='Extract', user='Sources', label='fixture | extract', id_prefix='P6')
    receipt = StepCall(step_key='extract', kind='extract', content=raw)
    error_name = 'quote-error-b' if secondary else 'quote-error'
    def fake(system, user, **_):
        assert error_name in user and ('document declarations' in user or 'document declaration' in user)
        return {'content': f'- [P6.F1] Corpus finding — anchor: "{docs["early"]}" — doc: early '
                f'— anchor-b: "{docs["late"]}" — doc-b: late — {error_name}: stale diagnostic copied by repair',
                'model_used': 'offline-fixture'}
    kept = _wall_extraction(receipt, prompt, SourceIndex(docs), fake, 'offline-fixture',
        depth='deep', big=False, cancellation_check=None, require_cross_document=True)
    assert len(kept) == 1 and receipt.reanchored == 1 and receipt.content == raw
    assert receipt.wall['invalid_anchor_ids'] == ['P6.F1']
    assert receipt.wall['after_reanchor']['invalid_anchor_ids'] == []
    rendered = render_rows(kept)
    assert 'quote-error' not in rendered
    reparsed = parse_rows(rendered)
    assert verify_rows(reparsed, SourceIndex(docs), require_cross_document=True).verified == 1
    job = DossierJob(); job.analysis = {'1': {'engine_key': 'conditions_of_possibility_analyzer', 'final_output': rendered}}
    desk = analysis_ledger(job, [Document(key=k, title=k, text=v) for k,v in docs.items()])
    assert '[P6.F1]' in desk.split('Rows whose anchors are unverified or incomplete')[0]
    assert 'anchor [early]' in desk and 'anchor [late]' in desk
