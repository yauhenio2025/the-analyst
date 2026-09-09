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
