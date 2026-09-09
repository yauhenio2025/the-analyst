import copy

import pytest

from src.dossier.research_feedback import ENGINE, decision, run
from src.engines.methods import compose_method, freeze_method
from src.sources.schemas import SourceSpec
from src.stages.process_composer import compose_oneshot_prompt

SOURCE = 'The participant claimed the policy would expand demand. That outcome remains unmeasured.'
SOURCES = [SourceSpec(kind='paste', role='source', key='original.w0', text=SOURCE)]
FINAL = '''A participant's advocacy does not demonstrate the outcome. Seek contrary measurement.

## Findings ledger
- [E1.F1] A participant predicts an effect — dim: observation — speaker: participant — affects: demand mechanism remains uncertain — anchor: "The participant claimed the policy would expand demand." — doc: original.w0 — confidence: high
- [E2.F1] Demand and substitution remain competing explanations — dim: hypothesis — change: retained — discriminating_observation: measured portfolio substitution — confidence: medium
- [E3.F1] Seek a discriminating measurement — dim: next_action — action: search — query: stablecoin treasury portfolio substitution evidence — basis: E1.F1 — gap: measurement of substitution — expected_value: distinguish new demand from shifted holdings — confidence: medium
'''


def fake(seen):
    def call(system, user, **kw):
        seen.append((system, user, kw))
        from src.executor.spend_guard import active
        assert active()
        return {'content': FINAL, 'input_tokens': 100, 'output_tokens': 100}
    return call


def test_independent_caller_executes_frozen_experimental_method():
    snap = freeze_method(ENGINE)
    seen = []
    result = run(SOURCES, packet={'question': 'What explains this change?', 'gaps': []}, spend_cap_usd=3,
                 method_sha256=snap['sha256'], call_fn=fake(seen))
    assert len(seen) == 1 and result['feedback_decision']['action'] == 'search'
    assert result['feedback_decision']['observations'][0]['quote_verified']
    assert result['method_snapshot'] == snap
    assert snap['operationalization']['method_metadata']['status'] == 'experimental'
    assert result['charged_or_reserved_usd'] >= result['cost_usd']
    assert SOURCE in seen[0][1] and 'RESEARCH CONTEXT' in seen[0][1] and 'CITATION PACKET' not in seen[0][1]
    assert all(d['sha256'] in seen[0][0] for d in snap['dependencies'])


def test_decision_composer_does_not_force_document_order_or_position_map():
    cap, spec = compose_method(freeze_method(ENGINE))
    text = compose_oneshot_prompt(cap, spec, {'a': SOURCE, 'b': SOURCE}).system
    assert 'Begin with a compact position map' not in text
    assert 'document order does not determine' in text
    assert 'next_action' in text and 'exact' in text


@pytest.mark.parametrize('alter', ['invented_quote', 'wrong_doc', 'bad_basis', 'repeated_query', 'two_actions'])
def test_unverified_or_ambiguous_feedback_never_executes_search(alter):
    output, packet = FINAL, {'question': 'Question'}
    if alter == 'invented_quote':
        output = output.replace('The participant claimed the policy would expand demand.', 'The policy demonstrably caused expansion.')
    if alter == 'wrong_doc': output = output.replace('doc: original.w0', 'doc: different.w0')
    if alter == 'bad_basis': output = output.replace('basis: E1.F1', 'basis: invented')
    if alter == 'repeated_query': packet['previous_queries'] = ['stablecoin treasury portfolio substitution evidence']
    if alter == 'two_actions': output += '\n- [E3.F2] Stop — dim: next_action — action: stop'
    result = decision({'final_output': output}, SOURCES, packet)
    assert result['action'] == 'stop' and result['validation_errors']


def test_gap_based_search_and_justified_stop_need_no_fabricated_quote():
    output = FINAL.replace('basis: E1.F1', 'basis: gap:0')
    result = decision({'final_output': output}, SOURCES, {'gaps': [{'id': 'gap:0', 'message': 'Publisher transcript missing'}]})
    assert result['action'] == 'search'
    output = '- [E3.F1] Further searches do not discriminate the remaining explanations — dim: next_action — action: stop — confidence: medium'
    assert decision({'final_output': output}, SOURCES, {})['action'] == 'stop'


def test_version_change_refuses_before_model_invocation():
    seen = []
    with pytest.raises(ValueError, match='nothing was spent'):
        run(SOURCES, packet={'question': 'Question'}, spend_cap_usd=3, method_sha256='a'*64, call_fn=fake(seen))
    assert not seen


def test_api_uses_bounded_feedback_entrypoint(monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from src.api.routes.engines import router
    from src.dossier import research_feedback
    seen = []
    monkeypatch.setattr(research_feedback, 'run', lambda *a, **k: seen.append(copy.deepcopy(k)) or {'feedback_decision': {'action': 'stop'}})
    app = FastAPI(); app.include_router(router, prefix='/v1'); client = TestClient(app)
    req = {'sources': [s.model_dump(mode='json') for s in SOURCES], 'packet': {'question': 'Question'}, 'spend_cap_usd': 1}
    assert client.post(f'/v1/engines/{ENGINE}/call', json=req).status_code == 200
    assert seen[0]['spend_cap_usd'] == 1
    assert client.post(f'/v1/engines/{ENGINE}/call', json={**req, 'depth': 'standard'}).status_code == 400


def test_frozen_output_limit_reaches_real_backend_boundary_without_network(monkeypatch):
    from types import SimpleNamespace
    from src.executor import engine_runner
    from src.executor.output_budget import current
    from src.llm.backends import LLMCallResult
    observed = []
    def backend(**kw):
        observed.append(kw)
        return LLMCallResult(FINAL, 'openrouter/openai/gpt-5.6-sol', 1000, 1000, 0, 1)
    monkeypatch.setattr(engine_runner, 'get_backend', lambda _: SimpleNamespace(execute_sync=backend, execute_streaming=backend))
    sources = [SourceSpec(kind='paste', key='original.w0', text=SOURCE + ' context' * 3500)]
    result = run(sources, packet={'question': 'What explains the change?'}, spend_cap_usd=2)
    assert len(observed) == 1 and observed[0]['max_tokens'] == 6000
    assert result['spend_reservations']['attempts'][0]['status'] == 'settled'
    assert result['spend_reservations']['attempts'][0]['ceiling_usd'] < 2
    assert current() is None
