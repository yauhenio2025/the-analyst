"""Trial isolation, routing contrast and restart safety; no providers or archive required."""
import copy

import pytest

from tools import tether_routing_trial as trial
from src.dossier.investigation import _spec


def evidence():
    return [{'citation_id': uid, 'source_role': role, 'quote_verified': True}
            for uid, role in [('field/F1', 'field'), ('field/F2', 'field'), ('author/F1', 'primary')]]


def result(stage):
    kind = 'field_finding' if stage.endswith('_field_map') else 'comparison'
    ids = 'field/F1' if kind == 'field_finding' else 'field/F1;author/F1'
    rows = [{'id': 'F1', 'dim': 'debate' if kind == 'field_finding' else 'answer',
             'fields': {'claim_kind': kind, 'evidence_ids': ids}}]
    if stage.endswith('_memo'):
        rows.append({'id': 'R1', 'dim': 'revision', 'fields': {'baseline': 'standalone', 'disposition': 'new', 'evidence_ids': ids}})
    return {'rows': rows, 'cost_usd': .1, 'prose': 'Qualified comparison [field/F1; author/F1].',
            'final_output': 'Qualified comparison [field/F1; author/F1].'}


def state():
    return {'cost_usd': 0, 'order': ['one', 'two'], 'methods': {k: {} for k in trial.KEYS.values()},
            'arms': {label: {'routing': route, 'reverse': False, 'stages': {}}
                     for label, route in [('one', 'baseline'), ('two', 'union')]}}


def prepared(case, arm, stage, previous):
    return [_spec('supplied', 'A supplied reading.')], {'evidence': evidence()}, {'stage': stage}


def test_contrast_restores_prose_support_and_only_union_inherits_it():
    outputs = [{'rows': [{'fields': {'evidence_ids': 'field/F1'}}], 'prose': 'A contrary finding [field/F2].'}]
    assert trial.routes(outputs, evidence(), 'baseline') == ['field/F1']
    assert trial.routes(outputs, evidence(), 'union') == ['field/F1', 'field/F2']
    assert trial.routes([{'rows': []}], evidence(), 'baseline', ['field/F2']) == []
    assert trial.routes([{'rows': []}], evidence(), 'union', ['field/F2']) == ['field/F2']


def test_completed_trial_reuses_all_outputs_and_keeps_method_model_and_budget_fixed(tmp_path, monkeypatch):
    monkeypatch.setattr(trial, 'prepare', prepared)
    current, calls = state(), []
    def call(key, sources, **kw):
        calls.append(kw)
        assert kw['model'] == trial.MODEL and kw['depth'] == 'surface'
        return result(key)
    trial.run({'original': {'mode': 'standalone'}}, current, tmp_path, call)
    assert current['status'] == 'complete' and current['cost_usd'] == pytest.approx(.6)
    assert len(calls) == 6 and calls[-1]['spend_cap_usd'] == pytest.approx(7.5)
    saved = copy.deepcopy(current)
    trial.run({'original': {'mode': 'standalone'}}, current, tmp_path,
              lambda *a, **k: pytest.fail('completed output must never repeat'))
    assert current == saved


def test_uncertain_invocation_stops_without_automatic_retry(tmp_path, monkeypatch):
    monkeypatch.setattr(trial, 'prepare', prepared)
    current = state()
    def call(*args, **kw):
        raise RuntimeError('response lost')
    with pytest.raises(RuntimeError, match='response lost'):
        trial.run({}, current, tmp_path, call)
    assert current['status'] == 'stopped'
    with pytest.raises(ValueError, match='prior invocation is incomplete'):
        trial.run({}, current, tmp_path, lambda *a, **k: pytest.fail('cannot repeat an uncertain request'))


def test_failed_support_does_not_trigger_an_unplanned_paid_repair(tmp_path, monkeypatch):
    monkeypatch.setattr(trial, 'prepare', prepared)
    current = state()
    with pytest.raises(ValueError, match='support check failed'):
        trial.run({}, current, tmp_path, lambda *a, **kw: {'rows': [], 'cost_usd': .1, 'final_output': 'Draft'})
    assert current['cost_usd'] == .1
    assert current['arms']['one']['stages']['field_map']['status'] == 'unsupported_draft'
