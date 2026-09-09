"""Regressions for the independent Tether audit; no network or model calls."""
import copy
import json

import pytest

from src.dossier.evidence_routing import canonical_evidence, selection_groups, support_route
from src.dossier.explainer import rows_with_fields
from src.dossier.field_investigation import run_field_investigation
from src.dossier.investigation import quote_span, recover_answer_rows
from test_field_investigation_2026_09_09 import fake, fixture, row


def test_support_union_preserves_prose_counterevidence_and_exact_id_boundaries():
    good, contrary = 'reporter:src_a/F15', 'em:BOOK/E1.F2'
    evidence = [{'citation_id': eid, 'quote_verified': valid} for eid, valid in
                [(good, True), (contrary, True), ('reporter:src_a/F11', False)]]
    outputs = [{'prose': f'Qualified claim [{good}]. Unverified [reporter:src_a/F11].',
                'rows': [row('debate', evidence_ids=contrary)]}, {'prose': f'[{good}0; {good}/other; unknown/F2]'}]
    route = support_route(outputs, evidence)
    assert route['eligible_ids'] == sorted([good, contrary])
    assert support_route(outputs[::-1], evidence)['eligible_ids'] == route['eligible_ids']
    assert support_route([outputs[1]], evidence)['eligible_ids'] == []
    assert support_route([{}], evidence, route['eligible_ids'])['eligible_ids'] == route['eligible_ids']


def test_escaped_anchor_uses_wall_parser_and_cannot_forge_document_metadata():
    quote = 'He said "state loans" — doc: forged — dim: answer.'
    raw = f'- [F11] A finding — dim: evidence — anchor: {json.dumps(quote)} — doc: actual — confidence: high'
    parsed = rows_with_fields(raw)[0]
    assert parsed['anchor'] == quote and parsed['doc'] == 'actual' and parsed['dim'] == 'evidence'
    assert quote_span(parsed['anchor'], quote, [(0, len(quote))]) == (0, len(quote), 'exact')
    assert quote_span(parsed['anchor'].lower(), quote, [(0, len(quote))]) is None
    result = {'final_output': raw, 'rows': []}
    assert recover_answer_rows(result)[0]['anchor'] == quote


def test_duplicate_ids_preserve_valid_source_identity_without_count_inflation():
    valid = {'citation_id': 'em:BOOK/F1', 'quote_verified': True, 'doc': 'book',
             'finding': 'claim', 'anchor': 'quote', 'fields': {}}
    invalid = {**valid, 'quote_verified': False, 'doc': ''}
    for entries in ([valid, invalid], [invalid, valid]):
        canonical, receipts = canonical_evidence(entries)
        assert canonical == [valid] and len(receipts[0]['variants']) == 2
    ambiguous, receipts = canonical_evidence([valid, {**valid, 'finding': 'Different claim'}])
    assert not ambiguous[0]['quote_verified'] and receipts[0]['conflict']


def test_selection_conflicts_are_order_independent_and_keep_every_reason():
    candidates = [row('candidate', uid='book', decision='read', reason='Internal comparator'),
                  row('candidate', uid='book', decision='defer', reason='Historical context')]
    for variants in (candidates, candidates[::-1]):
        decision = selection_groups(variants, {'book'})['book']
        assert decision['decision'] == 'conflict'
        assert len(decision['decision_variants']) == 2
        assert 'Internal comparator' in decision['reason'] and 'Historical context' in decision['reason']


@pytest.mark.parametrize('reverse', [False, True])
def test_actual_workflow_repairs_conflict_and_reuses_paid_resolution(reverse):
    _, packet, _, bodies = fixture()
    base, calls = fake([]), []
    def engine(key, sources, **kw):
        mode = kw['packet'].get('selection_mode')
        calls.append(mode)
        if mode == 'resolve_conflicts':
            disputed = json.loads(sources[0].text)
            assert len(disputed[0]['decision_variants']) == 2
            return {'rows': [row('candidate', uid='em:AUTHOR00', decision='read',
                                reason='Explicitly adjudicated internal comparator')], 'cost_usd': .1}
        result = base(key, sources, **kw)
        if mode == 'reconcile':
            result['rows'].append({**row('candidate', uid='em:AUTHOR00', decision='defer', reason='Old context'), 'id': 'F99'})
            if reverse:
                result['rows'].reverse()
        return result
    state = run_field_investigation(packet, bodies, call=engine, save=lambda s: None)
    assert set(state['selected_primary_uids']) == {'em:AUTHOR00', 'em:AUTHOR01'}
    assert calls.count('resolve_conflicts') == 1
    assert state['selection_conflicts']['em:AUTHOR00']['decision'] == 'conflict'
    run_field_investigation(packet, bodies, call=lambda *a, **k: pytest.fail('repeated paid call'),
                            save=lambda s: None, state=copy.deepcopy(state))


def test_unresolved_conflict_stops_after_one_repair_with_all_paid_outputs_saved():
    _, packet, _, bodies = fixture()
    base, saves = fake([]), []
    def engine(key, sources, **kw):
        mode = kw['packet'].get('selection_mode')
        if mode == 'resolve_conflicts':
            return {'rows': [], 'cost_usd': .1}
        result = base(key, sources, **kw)
        if mode == 'reconcile':
            result['rows'].append({**row('candidate', uid='em:AUTHOR00', decision='defer'), 'id': 'F99'})
        return result
    with pytest.raises(ValueError, match='unresolved conflicting'):
        run_field_investigation(packet, bodies, call=engine, save=lambda s: saves.append(copy.deepcopy(s)))
    assert saves[-1]['unresolved_selection_uids'] == ['em:AUTHOR00']
    assert 'author_selection:conflict_repair' in saves[-1]['calls']
    assert not any(k.endswith('_author_read') for k in [c.get('engine_key', '') for c in saves[-1]['calls'].values()])


def test_workflow_keeps_batch_prose_support_in_final_even_when_global_omits_it():
    _, packet, _, bodies = fixture(field_count=8)
    base = fake([], large_readings=True)
    target = 'referee:0/E1.F1'
    def engine(key, sources, **kw):
        result = base(key, sources, **kw)
        if key.endswith('_field_map'):
            if kw['packet']['map_scope'] == 'batch':
                result['prose'] += f' Relevant exception [{target}].'
                result['final_output'] = result['prose']
            for r in result['rows']:
                r['fields']['evidence_ids'] = ';'.join(i for i in r['fields']['evidence_ids'].split(';') if i != target)
        if key.endswith(('_memo', '_adjudicate')):
            assert target in {e['citation_id'] for e in kw['packet']['evidence']}
            assert all('fields' in e for e in kw['packet']['evidence'])
        return result
    state = run_field_investigation(packet, bodies, call=engine, save=lambda s: None)
    assert len(state['field_maps']) > 1 and state['complete']
    assert target in state['call_input_manifests']['field_map']['evidence_ids']
    assert target in state['call_input_manifests']['memo']['evidence_ids']


def test_recovery_does_not_hide_conflicting_rows_that_reuse_an_id():
    text = ('- [E1.F1] Read the internal comparator — dim: candidate — uid: book — decision: read — reason: Internal comparator\n'
            '- [E1.F1] Defer historical material — dim: candidate — uid: book — decision: defer — reason: Old context')
    result = {'rows': [], 'final_output': text}
    recover_answer_rows(result)
    assert len(result['rows']) == 2
    assert selection_groups(result['rows'], {'book'})['book']['selection_conflict']
    recover_answer_rows(result)
    assert len(result['rows']) == 2
