import copy
from types import SimpleNamespace

import pytest

from src.executor import engine_runner, spend_guard as guard
from src.llm.backends import LLMCallResult


MODEL = 'openrouter/openai/gpt-5.6-sol'


def test_engine_boundary_refuses_before_backend_when_ceiling_exceeds_cap(monkeypatch):
    backend = SimpleNamespace(execute_sync=lambda **kw: pytest.fail('unreserved paid request'),
                              execute_streaming=lambda **kw: pytest.fail('unreserved paid request'))
    monkeypatch.setattr(engine_runner, 'get_backend', lambda _: backend)
    with guard.budget({'cost_usd': 0}, .01, lambda _: None):
        with pytest.raises(guard.SpendLimit, match='next call ceiling'):
            engine_runner.run_engine_call('Instructions', 'Source text', model_hint=MODEL, depth='surface')
    assert not guard.active()


def test_restart_preserves_uncertain_attempt_and_success_releases_only_with_usage():
    state = {'cost_usd': 0}; saves = []
    with guard.budget(state, 1, lambda s: saves.append(copy.deepcopy(s))):
        first = guard.reserve(MODEL, 'Instructions', 'Source', 65000, 'memo')
        assert first['status'] == 'reserved'
    restarted = saves[-1]
    with guard.budget(restarted, 1, lambda _: None):
        with pytest.raises(guard.SpendLimit):
            guard.reserve(MODEL, 'Instructions', 'Source', 65000, 'memo retry')
        guard.settle(restarted['spend_reservations']['attempts'][0],
                     LLMCallResult('A memo', MODEL, 1000, 2000, 0, 120))
        retry = guard.reserve(MODEL, 'Instructions', 'Source', 65000, 'next stage')
        assert retry['input_sha256'] == first['input_sha256']


def test_unknown_and_partial_receipts_never_release_budget():
    state = {'cost_usd': 0}
    with guard.budget(state, 1, lambda _: None):
        with pytest.raises(guard.SpendLimit, match='receipt contract'):
            guard.reserve('unknown', '', '', 10, 'read')
        attempt = guard.reserve(MODEL, '', '', 1000, 'read')
        guard.settle(attempt, LLMCallResult('Partial text', MODEL, 100, 100, 0, 120, partial=True))
        assert attempt['status'] == 'uncertain' and 'cost_usd' not in attempt


def test_bounded_openrouter_client_disables_hidden_sdk_retries(monkeypatch):
    import sys
    from src.llm.backends import OpenRouterBackend
    captured = []
    monkeypatch.setenv('OPENROUTER_API_KEY', 'isolated-test-key')
    monkeypatch.setitem(sys.modules, 'openai', SimpleNamespace(OpenAI=lambda **kw: captured.append(kw)))
    with guard.budget({'cost_usd': 0}, 1, lambda _: None):
        OpenRouterBackend(MODEL)._get_client()
    OpenRouterBackend(MODEL)._get_client()
    assert captured[0]['max_retries'] == 0 and 'max_retries' not in captured[1]


def repeated_request_ledger():
    state = {'cost_usd': 0}
    with guard.budget(state, 10, lambda _: None):
        lost = guard.reserve(MODEL, 'Instructions', 'Source ' * 10000, 65536, 'read')
        retry = guard.reserve(MODEL, 'Instructions', 'Source ' * 10000, 65536, 'read retry')
        guard.settle(retry, LLMCallResult('Complete', MODEL, 15000, 4000, 0, 120))
    return state, lost, retry


def test_identical_verified_retry_bounds_input_without_settling_lost_output():
    state, lost, retry = repeated_request_ledger()
    original = lost['ceiling_usd']
    saves = []
    with guard.budget(state, 10, lambda s: saves.append(copy.deepcopy(s))):
        assert lost['status'] == 'reserved' and 'cost_usd' not in lost
        assert lost['original_ceiling_usd'] == original > lost['ceiling_usd']
        receipt = lost['input_bound_receipt']
        assert receipt['witness_attempt_id'] == retry['id']
        assert receipt['input_token_ceiling'] == 15000 + 4096
        assert receipt['max_output_tokens'] == 65536
        assert receipt['charge_remains_unresolved']
        assert lost['ceiling_usd'] == round(((15000 + 4096) * 4 + 65536 * 10) / 1e6, 6)
    assert len(saves) == 1
    restarted = saves[0]
    with guard.budget(restarted, 10, lambda _: pytest.fail('unchanged refinement resaved')):
        assert restarted['spend_reservations'] == state['spend_reservations']


@pytest.mark.parametrize('change', [
    {'input_sha256': 'another-input'}, {'model': 'claude-sonnet-4-6'},
    {'status': 'uncertain'}, {'input_tokens': 0}, {'output_tokens': 0}, {'cost_usd': 100},
])
def test_mismatched_or_unverified_usage_cannot_release_a_reservation(change):
    state, lost, retry = repeated_request_ledger()
    original = copy.deepcopy(lost)
    retry.update(change)
    assert not guard.refine_repeated_input_bounds(state['spend_reservations'])
    assert lost == original


def test_largest_matching_input_witness_is_used_and_later_larger_usage_restores_headroom():
    state, lost, retry = repeated_request_ledger()
    larger = {**retry, 'id': 'larger-verified', 'input_tokens': 18000, 'cost_usd': .112}
    state['spend_reservations']['attempts'].append(larger)
    assert guard.refine_repeated_input_bounds(state['spend_reservations'])
    assert lost['input_bound_receipt']['witness_attempt_id'] == larger['id']
    before = lost['ceiling_usd']
    larger.update(input_tokens=22000, cost_usd=.128)
    assert guard.refine_repeated_input_bounds(state['spend_reservations'])
    assert before < lost['ceiling_usd'] < lost['original_ceiling_usd']
    assert lost['input_bound_receipt']['input_token_ceiling'] == 22000 + 4096
