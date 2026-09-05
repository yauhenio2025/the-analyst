"""Offline guards for the fixed held-out comparison; fake models only."""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/study_ideas_hegel_heldout_2026_09_05.py'
_spec = importlib.util.spec_from_file_location('heldout_study', SCRIPT)
study = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(study)


@pytest.fixture(scope='module')
def runtime():
    # CLI imports are isolated in a fresh process. Mirror that boundary when a
    # broad pytest collection has already imported the mutable main runtime.
    names = lambda: [key for key in sys.modules if key in ('src', 'scripts') or key.startswith(('src.', 'scripts.'))]
    previous = {key: sys.modules.pop(key) for key in names()}
    original_path, original_bytecode = sys.path[:], sys.dont_write_bytecode
    try:
        with study.frozen_runtime() as rt:
            yield rt
    finally:
        for key in names():
            sys.modules.pop(key, None)
        sys.modules.update(previous)
        sys.path[:] = original_path
        sys.dont_write_bytecode = original_bytecode


@pytest.fixture(scope='module')
def prepared(runtime):
    root = study.project_root()
    source = root / 'data/study/sources_ideas'
    calibration = root / 'data/study/ideas_2026_09_05/374325c24e6b10a1'
    if not all((source / name).is_file() for name in study.SOURCES.values()) or not (calibration / 'results.json').is_file():
        pytest.skip('Local ignored held-out sources and prior calibration receipts are not available')
    return (*study.build_plan(runtime, source, calibration), source)


def fake_backend(prepared):
    _, _, docs, _ = prepared
    quote = next(line for line in docs['ganzinger'][next(iter(docs['ganzinger']))].splitlines() if len(line) > 50)
    def call(**kwargs):
        critic = kwargs['model_hint'] == study.MODELS['critic']
        content = ('## Findings ledger\n' if critic else 'A source-grounded reading [F1].\n\n## Findings ledger\n')
        content += '- [F1] A bounded finding — anchor: ' + json.dumps(quote, ensure_ascii=False) + (' — status: confirmed' if critic else '') + ' — confidence: high'
        return {'content': content, 'model_used': kwargs['model_hint'], 'input_tokens': 100, 'output_tokens': 40, 'duration_ms': 1234, 'retries': 0, 'partial': False, 'stop_reason': 'stop'}
    return call


def generate(runtime, prepared, tmp_path, monkeypatch, condition='previous', override=None):
    plan, contexts, docs, sources = prepared
    job = next(j for j in plan['generations'] if j['condition'] == condition and j['source'] == 'ganzinger')
    monkeypatch.setattr(runtime.core, 'run_engine_call_auto', override or fake_backend(prepared))
    folder = tmp_path / 'output' / plan['identity'][:16]
    records = study.read_json(folder / 'results.json', {})
    study.execute_job(job, plan, folder, records, contexts, docs, sources, tmp_path / 'output', 6, runtime)
    return job, folder, records


def test_matrix_without_private_inputs():
    generations, judges = study.matrix()
    assert len(generations) == len(judges) == 16
    assert len({j['key'] for j in generations + judges}) == 32
    for engine in study.ENGINES:
        for paper in study.SOURCES:
            pair = [j for j in judges if j['engine'] == engine and j['source'] == paper]
            assert pair[0]['A'] == pair[1]['B'] and pair[0]['B'] == pair[1]['A']


def test_pinned_matrix_and_estimate(prepared):
    plan, contexts, docs, _ = prepared
    assert len(plan['generations']) == len(plan['judgments']) == 16
    assert plan['planned_invocations'] == {'read': 16, 'critic': 16, 'judge': 16}
    assert plan['runtime_commit'] == study.RUNTIME
    assert plan == json.loads(json.dumps(plan))
    assert sum(plan['estimated_cost_by_role'].values()) < 6
    for engine in study.ENGINES:
        assert set(plan['definitions'][engine]['conditions']) == {'previous', 'revised'}
        previous = contexts[f'{engine}__previous__ganzinger']
        revised = contexts[f'{engine}__revised__ganzinger']
        assert previous['cap'] == revised['cap'] and previous['documents'] == revised['documents']
        assert previous['spec'] != revised['spec']
    assert len(docs) == 2


def test_preview_never_invokes_or_writes(runtime, prepared, monkeypatch, tmp_path, capsys):
    from contextlib import nullcontext
    monkeypatch.setattr(study, 'frozen_runtime', lambda: nullcontext(runtime))
    monkeypatch.setattr(runtime.core, 'run_engine_call_auto', lambda **kw: pytest.fail('Paid call in preview'))
    monkeypatch.setattr(runtime.core, 'run_engine_call', lambda **kw: pytest.fail('Paid judge in preview'))
    out = tmp_path / 'absent'
    assert study.main(['--output-root', str(out)]) == 0
    preview = json.loads(capsys.readouterr().out)
    assert preview['mode'] == 'NO-CALL PREVIEW' and len(preview['matrix']) == 32
    assert not out.exists()


def test_budget_blocks_unknown_negative_and_overrun_across_identities(tmp_path):
    path = tmp_path / 'identity1/receipts/job/attempt/call-0001.json'
    for cost in (None, -1, float('nan')):
        study.write_json(path, {'cost_usd': cost})
        with pytest.raises(RuntimeError, match='Unknown'):
            study.budget_guard(tmp_path, 6, .1)
    study.write_json(path, {'cost_usd': 5.95})
    with pytest.raises(RuntimeError, match='ceiling'):
        study.budget_guard(tmp_path, 6, .1)
    assert study.budget_guard(tmp_path, 6, .04) == 5.95


def test_raw_quote_compliance_separate_from_membership(runtime):
    source = 'A sufficiently long exact source quotation for verification.'
    content = '## Findings ledger\n- [F1] Canonical — anchor: ' + json.dumps(source) + '\n- [F2] Legacy — anchor: “' + source + '”\n- [F3] Wrong quotation — anchor: "A made up sufficiently long quotation."'
    diag = study.quote_diagnostics(content, runtime, {'doc': source})
    assert diag['canonical_json'] == 2 and diag['legacy_quoted'] == 1
    assert diag['raw_membership_wall']['parseable_rows'] == 3
    assert diag['raw_membership_wall']['verified_anchors'] == 2
    malformed = study.quote_diagnostics('## Findings ledger\n- [F4] Broken — anchor: "A quote with "inner" words"', runtime, {'doc': source})
    assert malformed['malformed'] == 1 and malformed['raw_membership_wall']['invalid_anchor_ids'] == ['F4']


@pytest.mark.parametrize('condition', ['previous', 'revised'])
def test_complete_replays_exactly_without_backend(runtime, prepared, tmp_path, monkeypatch, condition):
    job, folder, records = generate(runtime, prepared, tmp_path, monkeypatch, condition)
    plan, contexts, docs, source = prepared
    monkeypatch.setattr(runtime.core, 'run_engine_call_auto', lambda **kw: pytest.fail('Resume called backend'))
    assert study.validate_completed(job, records[job['key']], plan, folder, records, contexts, docs, runtime)
    study.execute_job(job, plan, folder, records, contexts, docs, source, tmp_path / 'output', 6, runtime)
    calls = study.saved_calls(folder, records[job['key']])
    assert len(calls) == 2 and {c[0]['role'] for c in calls} == {'read', 'critic'}
    assert all(c[0]['backend_duration_ms'] == 1234 for c in calls)
    assert all(c[0]['raw_quote_diagnostics']['canonical_json'] == 1 for c in calls)


@pytest.mark.parametrize('artifact', ['prompt', 'response', 'receipt', 'output'])
def test_tampered_artifact_refuses_resume(runtime, prepared, tmp_path, monkeypatch, artifact):
    job, folder, records = generate(runtime, prepared, tmp_path, monkeypatch)
    plan, contexts, docs, _ = prepared
    attempt = folder / 'receipts' / job['key'] / records[job['key']]['attempt']
    path = {'prompt': attempt/'call-0001.prompt.json', 'response': attempt/'call-0001.md', 'receipt': attempt/'call-0001.json', 'output': folder/records[job['key']]['output']}[artifact]
    path.write_bytes(path.read_bytes() + b' ')
    with pytest.raises(RuntimeError, match='changed|differs'):
        study.validate_completed(job, records[job['key']], plan, folder, records, contexts, docs, runtime)


@pytest.mark.parametrize('change', [{'partial': True}, {'stop_reason': 'error'}, {'model_used': 'wrong-model'}, {'input_tokens': None}])
def test_failed_call_receipt_preserved_and_no_retry(runtime, prepared, tmp_path, monkeypatch, change):
    backend = fake_backend(prepared)
    def bad(**kwargs):
        return {**backend(**kwargs), **change}
    with pytest.raises((RuntimeError, ValueError)):
        generate(runtime, prepared, tmp_path, monkeypatch, override=bad)
    plan, contexts, docs, sources = prepared
    folder = tmp_path / 'output' / plan['identity'][:16]
    records = study.read_json(folder/'results.json')
    record = next(iter(records.values()))
    assert record['status'] == 'failed'
    receipt_path = next(folder.glob('receipts/*/*/call-0001.json'))
    assert study.read_json(receipt_path)['status'] == 'failed' and receipt_path.with_suffix('.md').exists()
    monkeypatch.setattr(runtime.core, 'run_engine_call_auto', lambda **kw: pytest.fail('Automatic paid retry'))
    job = next(j for j in plan['generations'] if j['key'] == record['key'])
    with pytest.raises(RuntimeError, match='no automatic paid retry'):
        study.execute_job(job, plan, folder, records, contexts, docs, sources, tmp_path/'output', 6, runtime)


def test_opposite_orders_and_parent_bindings(runtime, prepared, tmp_path, monkeypatch):
    _, folder, _ = generate(runtime, prepared, tmp_path, monkeypatch, 'previous')
    _, folder, records = generate(runtime, prepared, tmp_path, monkeypatch, 'revised')
    plan, contexts, docs, sources = prepared
    jobs = [j for j in plan['judgments'] if j['engine'] == study.ENGINES[0] and j['source'] == 'ganzinger']
    def judge(**kwargs):
        return {'content': '{"winner":"A","margin":"clear","why":"Source reasons."}', 'model_used': study.MODELS['judge'], 'input_tokens': 100, 'output_tokens': 40, 'retries': 0, 'duration_ms': 500, 'partial': False}
    monkeypatch.setattr(runtime.core, 'run_engine_call', judge)
    for job in jobs:
        study.execute_job(job, plan, folder, records, contexts, docs, sources, tmp_path/'output', 6, runtime)
    outcome = study.report(plan, folder, contexts, docs, runtime)['pairs'][0]
    assert outcome['outcome'] == 'split'
    records[jobs[0]['A']]['status'] = 'failed'
    with pytest.raises(RuntimeError, match='identity'):
        study.validate_completed(jobs[0], records[jobs[0]['key']], plan, folder, records, contexts, docs, runtime)
    for raw in ('{}', '{"winner":"A"}', 'not JSON'):
        with pytest.raises(ValueError):
            runtime.core.parse_judgment(raw, jobs[0])
