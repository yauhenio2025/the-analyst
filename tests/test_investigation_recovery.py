import copy
import json
from contextlib import contextmanager
import pytest

from src.dossier.investigation_recovery import recover_reading


def fixture():
    stage = 'read:field:reporter:one'
    method = {'engine_key': 'field_investigation_field_read', 'version': 3, 'sha256': 'method'}
    reading = {'source_key': 'field:reporter:one', 'body_sha256': 'body', 'inspected_ranges': [[0, 50]], 'reading': 'Earlier paid reading.'}
    state = {'packet_sha256': 'packet', 'cost_usd': 2.0, 'memo': 'Current memo.', 'evidence': ['Current evidence.'],
             'readings': ['Current reading.'], 'analysis': {'1': 'Current phase.'},
             'read_inputs': {stage: {'source_key': reading['source_key'], 'body_sha256': 'body', 'ranges': [[0, 50]]}},
             'call_input_manifests': {stage: {'method_receipt': method}},
             'spend_reservations': {'attempts': [{'id': 'current', 'input_sha256': 'same-input'}]}, 'calls': {stage: {'cost_usd': 2}}}
    receipt = {'stage': stage, 'packet_sha256': 'packet', 'reading': reading, 'method_receipt': method,
               'evidence': [{'source_key': reading['source_key'], 'body_sha256': 'body', 'quote_verified': False}],
               'archive': {'content_sha256': 'archive', 'stacks_artifact_id': 493},
               'attempt': {'id': 'earlier', 'input_sha256': 'same-input', 'status': 'settled',
                           'model': 'openrouter/openai/gpt-5.6-sol', 'input_tokens': 1000, 'output_tokens': 100,
                           'cost_usd': .005, 'ceiling_usd': .02}}
    return state, receipt


def test_recovered_charge_and_research_survive_without_replacing_current_results():
    state, receipt = fixture()
    before = copy.deepcopy(state)
    result = recover_reading(state, receipt)
    assert state == before and result['cost_usd'] == 2.003
    for key in ('memo', 'evidence', 'readings', 'analysis'):
        assert result[key] == state[key]
    recovered = result['recovered_research']['earlier']
    assert not recovered['used_in_current_synthesis'] and recovered['evidence'][0]['quote_verified'] is False
    assert result['spend_reservations']['attempts'][-1] == receipt['attempt']
    assert result['calls']['recovered:earlier']['cost_usd'] == .003
    assert recover_reading(result, receipt) is result
    changed = copy.deepcopy(receipt); changed['reading']['reading'] = 'Different content'
    with pytest.raises(ValueError, match='different evidence'):
        recover_reading(result, changed)


@pytest.mark.parametrize('mutation', ['packet', 'body', 'method', 'input', 'price'])
def test_recovery_rejects_unrelated_or_unreconciled_receipts(mutation):
    state, receipt = fixture()
    if mutation == 'packet': receipt['packet_sha256'] = 'other'
    elif mutation == 'body': receipt['reading']['body_sha256'] = 'other'
    elif mutation == 'method': receipt['method_receipt'] = {'version': 99}
    elif mutation == 'input': receipt['attempt']['input_sha256'] = 'other'
    else: receipt['attempt']['cost_usd'] = 99
    with pytest.raises(ValueError):
        recover_reading(state, receipt)
    assert state['cost_usd'] == 2 and len(state['spend_reservations']['attempts']) == 1


def test_persisted_recovery_repairs_interrupted_accounting_without_another_charge(monkeypatch):
    from src.dossier import store, investigation, blob_store, execution_lock, events
    from src.dossier.schemas import DossierJob
    from src.dossier.investigation_recovery import recover_saved_reading
    state, receipt = fixture()
    saved, updates = [state], []
    job = DossierJob(id='job', status='done')
    monkeypatch.setattr(store, 'get_job', lambda _: job)
    monkeypatch.setattr(investigation, 'load_investigation', lambda _: saved[0])
    monkeypatch.setattr(blob_store, 'put_blob', lambda key, mime, data: saved.__setitem__(0, json.loads(data)))
    monkeypatch.setattr(events, 'emit', lambda *args, **kwargs: None)
    @contextmanager
    def own(*args, **kwargs):
        yield
    monkeypatch.setattr(execution_lock, 'investigation_owner', own)
    def update(*args, **kwargs):
        updates.append(kwargs)
        if len(updates) == 1:
            raise OSError('Simulated interruption after checkpoint persistence')
    monkeypatch.setattr(store, 'update_job', update)
    with pytest.raises(OSError):
        recover_saved_reading('job', receipt)
    result = recover_saved_reading('job', receipt)
    assert result['already_recovered'] and result['total_cost_usd'] == 2.003
    assert updates[-1]['totals'].cost_usd == 2.003 and updates[-1]['totals'].llm_calls == 2
    assert saved[0]['memo'] == 'Current memo.' and len(saved[0]['recovered_research']) == 1
    job.status = 'analysis'
    with pytest.raises(ValueError, match='stopped'):
        recover_saved_reading('job', receipt)
