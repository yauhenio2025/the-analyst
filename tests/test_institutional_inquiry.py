"""Field-only path through the existing executor and central methods; no paid calls."""
import copy
import json

import pytest

from src.dossier.field_investigation import run_field_investigation
from src.dossier.engine_call import call_engine
from src.engines.methods import freeze_method
from src.sources.resolve import resolve_sources
from src.sources.schemas import SourceSpec
from tests.test_field_investigation_2026_09_09 import fixture, freeze, fake
from tests.test_shared_critical_methods import model


def institutional():
    raw, *_ = fixture(prior=False)
    raw.pop('author')
    raw['primary'] = []
    raw.update(inquiry_type='institutional', method_contract={'key': 'institutional-inquiry', 'version': 1})
    raw['field'][0]['institution'] = {'hostname': 'example.org', 'name': 'Research institute'}
    raw['field'][0]['attribution'] = {'category': 'signed_view', 'official_adoption': 'unknown'}
    return freeze(raw)


def provider(calls, **options):
    delegate = fake(calls, **options)
    def call(key, sources, **kw):
        result = delegate(key, sources, **kw)
        if key == 'institutional_inquiry_memo':
            result['rows'][0]['fields']['claim_kind'] = 'field_finding'
        return result
    return call


def test_author_independent_resolution_read_map_memo_and_method_receipts():
    raw, packet, _, bodies = institutional()
    docs = resolve_sources([SourceSpec(kind='paste', role='field_investigation', text=json.dumps(raw))])
    assert not any(d.key.startswith('primary:') for d in docs)
    calls = []
    state = run_field_investigation(packet, bodies, call=provider(calls), save=lambda _: None)
    assert state['complete'] and state['author'] is None
    assert state['coverage']['primary']['read_count'] == 0
    assert state['coverage']['field']['read_count'] == 2
    assert not any('author_' in k or k.endswith('_adjudicate') for k, *_ in calls)
    assert calls[-1][0] == 'institutional_inquiry_memo'
    assert state['evidence'][0]['source_metadata']['attribution']['official_adoption'] == 'unknown'
    assert all(e['source_role'] == 'field' and e['quote_verified'] for e in state['evidence'])
    for phase in state['analysis'].values():
        assert phase['method_receipt']['sha256']
        assert 'institutional_argument_criticism' in {d['engine_key'] for d in phase['method_receipt']['dependencies']}


def test_restart_at_memo_does_not_replay_paid_reads_or_load_new_methods(monkeypatch):
    _, packet, _, bodies = institutional()
    saves, calls = [], []
    with pytest.raises(RuntimeError, match='simulated'):
        run_field_investigation(packet, bodies, call=provider(calls, fail_stage='institutional_inquiry_memo'),
                                save=lambda s: saves.append(copy.deepcopy(s)))
    prior = saves[-1]
    from src.engines import methods
    monkeypatch.setattr(methods, 'field_methods', lambda **kw: pytest.fail('refetched methods'))
    resumed = []
    state = run_field_investigation(packet, bodies, call=provider(resumed), save=lambda _: None, state=prior)
    assert state['complete'] and [c[0] for c in resumed] == ['institutional_inquiry_memo']
    assert state['cost_usd'] == pytest.approx(.5)


def test_contract_mixing_and_unavailable_sources_reject_before_spending():
    raw, *_ = institutional()
    raw['author'] = {'id': 'fake'}
    with pytest.raises(ValueError, match='author-independent'):
        freeze(raw)
    raw.pop('author')
    raw['method_contract']['version'] = 99
    with pytest.raises(ValueError, match='Unsupported'):
        freeze(raw)
    raw['method_contract']['version'] = 1
    for r in raw['field']:
        r['body'] = ''
        r['page_spans'] = []
    _, packet, _, bodies = freeze(raw)
    with pytest.raises(ValueError, match='available field body'):
        run_field_investigation(packet, bodies, call=lambda *a, **kw: pytest.fail('paid call'), save=lambda _: None)


@pytest.mark.parametrize('key', ['institutional_inquiry_plan', 'institutional_inquiry_memo',
                                'field_investigation_field_read', 'field_investigation_field_map'])
def test_independent_caller_receives_actual_central_records(key):
    snapshot = freeze_method(key)
    captured = []
    result = call_engine(key, [SourceSpec(kind='paste', key='source', text='these are my views, not the institute policy')],
                         method_snapshot=snapshot, spend_cap_usd=1, call_fn=model(captured))
    assert snapshot['operationalization']['process']['framing'] in captured[0][0]
    for dep in snapshot['dependencies']:
        assert dep['sha256'] in captured[0][0]
    assert result['method_receipt']['sha256'] == snapshot['sha256']
