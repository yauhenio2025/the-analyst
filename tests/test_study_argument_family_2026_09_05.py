"""Frozen argument-family harness: offline replay and launch barriers, fake models only."""
import importlib.util
import json
import math
from pathlib import Path
import re
import sys

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/study_argument_family_2026_09_05.py'
spec = importlib.util.spec_from_file_location('argument_family_study', SCRIPT)
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


@pytest.fixture(scope='module')
def runtime():
    names = lambda: [k for k in sys.modules if k in ('src', 'scripts') or k.startswith(('src.', 'scripts.'))]
    previous = {key: sys.modules.pop(key) for key in names()}
    original_path, original_bytecode = sys.path[:], sys.dont_write_bytecode
    try:
        with study.frozen_runtime() as rt:
            yield rt
    finally:
        for key in names():
            sys.modules.pop(key, None)
        sys.modules.update(previous)
        sys.path[:], sys.dont_write_bytecode = original_path, original_bytecode


@pytest.fixture(scope='module')
def prepared(runtime):
    root = study.project_root()
    sources = root / 'data/study/sources_ideas'
    calibration = root / 'data/study/ideas_2026_09_05/374325c24e6b10a1'
    if not (calibration / 'results.json').is_file():
        pytest.skip('Private local prior receipts unavailable')
    return study.build_plan(runtime, sources, calibration, root / study.CONTROL_PATH, root / study.CANDIDATE_PATH)


@pytest.fixture(autouse=True)
def offline(runtime, monkeypatch):
    def no_call(*args, **kwargs):
        pytest.fail('Unexpected provider call in offline test')
    monkeypatch.setattr(runtime.core, 'run_engine_call_auto', no_call)
    monkeypatch.setattr(runtime.core, 'run_engine_call', no_call)


def fake_backend(log, *, override=None):
    def fake(**kwargs):
        log.append(kwargs)
        label, system = kwargs['label'], kwargs['system_prompt']
        if kwargs['model_hint'] == study.MODELS['judge']:
            text = json.dumps({'winner': 'A', 'margin': 'slight', 'why': 'A grounded comparison.',
                               'what_A_has_that_B_lacks': 'One distinction.', 'what_B_has_that_A_lacks': 'One qualification.'})
        elif label.startswith('argument-family ') or ' | synthesize' in label:
            text = 'Fake limited reading.\n\n## Findings ledger\n'
        else:
            identities = json.loads(re.search(r'Required identities: ([^\n]+)', system).group(1))
            checked = ' | verify' in label
            outcomes = [{**identity, 'outcome': 'no_relevant_instance', 'sections_inspected': ['Supplied test passage'],
                         'coverage': 'partial', 'criterion': 'Fixture criterion.', 'basis': 'This is a fake scoped assessment.',
                         'limitations': ['Fake model does not evaluate philosophical content.'], 'finding_ids': [],
                         'review_state': 'supported_within_stated_scope' if checked else 'unchecked',
                         'review_basis': 'Fixture review basis.' if checked else ''} for identity in identities]
            text = 'Fake limited reading.\n\n## Findings ledger\n\n## Scope outcomes\n```json\n' + json.dumps(outcomes) + '\n```'
        result = {'content': text, 'model_used': kwargs['model_hint'], 'input_tokens': 100, 'output_tokens': 50,
                  'duration_ms': 1234, 'retries': 0, 'partial': False, 'stop_reason': 'stop'}
        return override(result, kwargs) if override else result
    return fake


def generate(runtime, prepared, tmp_path, monkeypatch, *, condition='candidate', source='absence', override=None):
    plan, contexts, docs = prepared
    job = next(j for j in plan['generations'] if j['engine'] == study.ENGINES[0] and j['condition'] == condition and j['source'] == source)
    log = []
    monkeypatch.setattr(runtime.core, 'run_engine_call_auto', fake_backend(log, override=override))
    root = tmp_path / 'campaign'; folder = root / plan['identity'][:16]
    records = study.read_json(folder / 'results.json', {})
    study.execute_job(job, plan, folder, records, contexts, docs, root, 16, runtime)
    return job, folder, records, log


def test_exact_matrix():
    gen, judge = study.matrix()
    assert len(gen) == len(judge) == 24
    assert len({j['key'] for j in gen + judge}) == 48
    assert sum(j['stage'] == 'initial' for j in gen) == 16
    assert sum(j['stage'] == 'corpus' for j in gen) == 8
    for engine, source in {(j['engine'], j['source']) for j in judge}:
        pair = [j for j in judge if (j['engine'], j['source']) == (engine, source)]
        assert pair[0]['A'] == pair[1]['B'] and pair[0]['B'] == pair[1]['A']


def test_plan_pins_actual_runtime_candidates_controls_and_overheads(prepared):
    plan, contexts, documents = prepared
    assert plan['runtime_commit'] == study.RUNTIME
    assert plan['planned_base_calls'] == 136
    assert plan['estimated_total_usd'] > 0
    assert plan['calibration']['roles']['critic']['calls'] == 28
    assert plan['calibration']['scope_chars_per_record'] == 1600
    assert len(plan['sources']) == 13
    for engine in study.ENGINES:
        definition = plan['definitions'][engine]
        assert definition['process']['scoped_outcomes'] and 'Eligibility:' in definition['process']['framing']
        assert definition['candidate_commit'].startswith('005cee5')
        assert definition['baseline_capability_file_sha256']
    corpus = next(j for j in plan['generations'] if j['condition'] == 'candidate' and j['source'] == 'castoriadis')
    assert corpus['base_calls'] == 21
    assert sum(c['role'] == 'extract' for c in corpus['call_envelopes']) == 16
    assert sum(c['role'] == 'critic' for c in corpus['call_envelopes']) == 4
    assert corpus['call_envelopes'][-1]['scope_output_records'] == 16
    assert len(corpus['static_prompt_hashes']) == 15


def test_default_preview_never_calls_or_creates_campaign(runtime, prepared, monkeypatch, tmp_path, capsys):
    from contextlib import nullcontext
    monkeypatch.setattr(study, 'frozen_runtime', lambda: nullcontext(runtime))
    out = tmp_path / 'absent'
    assert study.main(['--output-root', str(out)]) == 0
    preview = json.loads(capsys.readouterr().out)
    assert preview['mode'] == 'NO-CALL PREVIEW' and preview['base_calls'] == 136
    assert not out.exists()


@pytest.mark.parametrize('args', [['--run'], ['--run', '--budget-usd', '17'], ['--run', '--budget-usd', 'nan'],
                                 ['--run', '--budget-usd', '16', '--phase', 'report']])
def test_invalid_launch_fails_before_runtime(args, monkeypatch):
    monkeypatch.setattr(study, 'frozen_runtime', lambda: pytest.fail('Runtime entered for invalid launch'))
    with pytest.raises(RuntimeError):
        study.main(args)


@pytest.mark.parametrize('cost', [None, -1, float('nan'), float('inf'), True])
def test_unknown_or_invalid_cost_blocks_whole_campaign(tmp_path, cost):
    study.write_json(tmp_path / 'identity/receipts/job/attempt/call-0001.json', {'cost_usd': cost, 'status': 'complete'})
    with pytest.raises(RuntimeError, match='Unknown'):
        study.budget_guard(tmp_path, 16, .1)


def test_budget_aggregates_identities_and_blocks_failed_known_call(tmp_path):
    a = tmp_path / 'one/receipts/a/attempt/call-0001.json'
    b = tmp_path / 'two/receipts/b/attempt/call-0001.json'
    study.write_json(a, {'cost_usd': 8, 'status': 'complete'}); study.write_json(b, {'cost_usd': 7.9, 'status': 'complete'})
    with pytest.raises(RuntimeError, match='ceiling'):
        study.budget_guard(tmp_path, 16, .2)
    assert study.budget_guard(tmp_path, 16, .05) == 15.9
    study.write_json(b, {'cost_usd': 0, 'status': 'failed'})
    with pytest.raises(RuntimeError, match='failed/running'):
        study.budget_guard(tmp_path, 16, .01)


@pytest.mark.parametrize('condition,source,expected', [('original', 'absence', 1), ('candidate', 'absence', 2),
                                                      ('original', 'mixed', 1), ('candidate', 'mixed', 21)])
def test_original_checked_and_deep_replay_exactly_without_provider(runtime, prepared, tmp_path, monkeypatch, condition, source, expected):
    job, folder, records, log = generate(runtime, prepared, tmp_path, monkeypatch, condition=condition, source=source)
    assert len(log) == expected
    monkeypatch.setattr(runtime.core, 'run_engine_call_auto', lambda **kw: pytest.fail('Paid call during replay'))
    plan, contexts, docs = prepared
    assert study.validate_completed(job, records[job['key']], plan, folder, records, contexts, docs, runtime)
    study.execute_job(job, plan, folder, records, contexts, docs, folder.parent, 16, runtime)
    if condition == 'candidate':
        scopes = records[job['key']]['process']['final_wall']['scope_outcomes']
        assert len(scopes) == (16 if source == 'mixed' else 5)
        assert '## Scope assessment' in (folder / records[job['key']]['output']).read_text()
        assert '## Scope outcomes' in next((folder / 'receipts'/job['key']).glob('*/call-0001.md')).read_text()
    else:
        assert study.JUDGE_RUBRIC not in log[0]['system_prompt']
        assert 'Scoped outcomes contract' not in log[0]['system_prompt']


@pytest.mark.parametrize('mutation', [{'partial': True}, {'stop_reason': 'length'}, {'connection_error': 'interrupted'},
                                    {'error': 'provider failed'}, {'model_used': 'wrong/model'}, {'input_tokens': None}])
def test_partial_error_fallback_unknown_usage_retained_and_never_paid_retried(runtime, prepared, tmp_path, monkeypatch, mutation):
    plan, contexts, docs = prepared
    job = next(j for j in plan['generations'] if j['condition'] == 'candidate' and j['source'] == 'absence')
    root = tmp_path / 'campaign'; folder = root / plan['identity'][:16]; records = {}; log = []
    monkeypatch.setattr(runtime.core, 'run_engine_call_auto', fake_backend(log, override=lambda result, kw: {**result, **mutation}))
    with pytest.raises(RuntimeError):
        study.execute_job(job, plan, folder, records, contexts, docs, root, 16, runtime)
    assert len(log) == 1 and records[job['key']]['status'] == 'failed'
    raw = next((folder / 'receipts').glob('*/*/call-0001.response.json'))
    assert all(study.read_json(raw).get(k) == v for k, v in mutation.items())
    monkeypatch.setattr(runtime.core, 'run_engine_call_auto', lambda **kw: pytest.fail('Retried paid call'))
    with pytest.raises(RuntimeError, match='no automatic retry'):
        study.execute_job(job, plan, folder, records, contexts, docs, root, 16, runtime)


def test_stray_logical_calls_in_another_identity_cannot_be_restarted(runtime, prepared, tmp_path):
    plan, contexts, docs = prepared; job = plan['generations'][0]
    path = tmp_path / f"other/receipts/{job['key']}/attempt/call-0001.prompt.json"
    study.write_json(path, {'system': 'unfinished'})
    with pytest.raises(RuntimeError, match='already has logical-job calls'):
        study.execute_job(job, plan, tmp_path / plan['identity'][:16], {}, contexts, docs, tmp_path, 16, runtime)


@pytest.mark.parametrize('artifact', ['output', 'response', 'process'])
def test_resume_replays_against_tampering_not_only_updated_hashes(runtime, prepared, tmp_path, monkeypatch, artifact):
    job, folder, records, _ = generate(runtime, prepared, tmp_path, monkeypatch)
    record = records[job['key']]; attempt = folder/'receipts'/job['key']/record['attempt']
    if artifact == 'output':
        path = folder / record['output']; path.write_text(path.read_text() + '\nChanged product')
        record['output_sha256'] = study.digest(path.read_bytes())
    elif artifact == 'response':
        path = attempt/'call-0001.response.json'; response = study.read_json(path); response['output_tokens'] += 1; study.write_json(path,response)
        record['invocation_files_sha256'][str(path.relative_to(folder))] = study.digest(path.read_bytes())
    else:
        record['process']['final_wall']['scope_outcomes'][0]['outcome'] = 'inconclusive'
    study.write_json(attempt/'job.json',record)
    plan,contexts,docs=prepared
    with pytest.raises(RuntimeError):
        study.validate_completed(job,record,plan,folder,records,contexts,docs,runtime)


def test_opposite_judge_orders_map_to_condition_and_split_remains_split(runtime, prepared, tmp_path, monkeypatch):
    _, folder, records, _ = generate(runtime, prepared, tmp_path, monkeypatch, condition='original')
    _, folder, records, _ = generate(runtime, prepared, tmp_path, monkeypatch, condition='candidate')
    plan, contexts, docs = prepared; log=[]
    monkeypatch.setattr(runtime.core,'run_engine_call',fake_backend(log))
    jobs=[j for j in plan['judgments'] if j['engine']==study.ENGINES[0] and j['source']=='absence']
    for job in jobs:
        study.execute_job(job,plan,folder,records,contexts,docs,folder.parent,16,runtime)
    assert records[jobs[0]['key']]['judgment']['winner']==jobs[0]['A']
    assert records[jobs[1]['key']]['judgment']['winner']==jobs[1]['A']
    result=study.report(plan,folder,records,contexts,docs,runtime)
    pair=next(p for p in result['pairs'] if p['engine']==study.ENGINES[0] and p['source']=='absence')
    assert pair['outcome']=='split'
    assert len(log)==2


def test_review_gate_requires_all_exact_outputs_and_unchanged_memo(runtime, prepared, tmp_path, monkeypatch):
    plan, contexts, docs = prepared
    small_plan={**plan,'generations':[j for j in plan['generations'] if j['engine']==study.ENGINES[0] and j['source']=='absence']}
    _,folder,records,_=generate(runtime,prepared,tmp_path,monkeypatch,condition='original')
    _,folder,records,_=generate(runtime,prepared,tmp_path,monkeypatch,condition='candidate')
    with pytest.raises(RuntimeError,match='separate reviewed'):
        study.review_gate(None,'corpus',small_plan,folder,records,contexts,docs,runtime)
    memo=tmp_path/'memo.md';memo.write_text('Reviewed these exact two products with the source.')
    review=tmp_path/'review.json'
    data={'identity':plan['identity'],'phase':'corpus','decision':'proceed',
          'outputs_sha256':{j['key']:records[j['key']]['output_sha256'] for j in small_plan['generations']},
          'memo_path':str(memo),'memo_sha256':study.digest(memo.read_bytes())}
    study.write_json(review,data)
    assert study.review_gate(review,'corpus',small_plan,folder,records,contexts,docs,runtime)
    memo.write_text('Changed memo')
    with pytest.raises(RuntimeError,match='memo'):
        study.review_gate(review,'corpus',small_plan,folder,records,contexts,docs,runtime)


def test_full_preview_over_cap_refuses_before_campaign_creation(runtime, prepared, monkeypatch):
    from contextlib import nullcontext
    plan, contexts, docs = prepared
    oversized = {**plan, 'estimated_total_usd': 16.01}
    monkeypatch.setattr(study, 'frozen_runtime', lambda: nullcontext(runtime))
    monkeypatch.setattr(study, 'build_plan', lambda *a: (oversized, contexts, docs))
    with pytest.raises(RuntimeError, match='Full-matrix preview exceeds'):
        study.main(['--run', '--budget-usd', '16'])


def test_mutated_bound_control_or_harness_refuses_before_call(prepared, tmp_path):
    plan, _, _ = prepared
    source = tmp_path / 'control.txt'; source.write_text('Frozen fixture')
    local = {**plan, 'input_files_sha256': {str(source): study.digest(source.read_bytes())}}
    study.guard_inputs(local)
    source.write_text('Changed fixture')
    with pytest.raises(RuntimeError, match='Frozen input changed'):
        study.guard_inputs(local)
    with pytest.raises(RuntimeError, match='Harness changed'):
        study.guard_inputs({**local, 'harness_sha256': 'incorrect'})


def test_valid_reanchor_is_counted_pinned_and_replayed_without_extra_paid_calls(runtime, prepared, tmp_path, monkeypatch):
    plan, contexts, docs = prepared
    job = next(j for j in plan['generations'] if j['engine'] == study.ENGINES[0] and j['condition'] == 'candidate' and j['source'] == 'mixed')
    altered = False
    quote = docs['mixed']['archive_policy'].split('. ')[0] + '. '
    quote = 'Original records should remain unchanged so that an audit can reconstruct the decisions recorded in them.'
    def change(result, kwargs):
        nonlocal altered
        if kwargs['label'].endswith('(re-anchor)'):
            result['content'] = '## Findings ledger\n- [DS1.DOC1.F1] A fixture finding — dim: positions_and_attribution — anchor: ' + json.dumps(quote) + ' — doc: archive_policy'
        elif not altered and ' | extract | ' in kwargs['label']:
            altered = True
            identities = json.loads(re.search(r'Required identities: ([^\n]+)', kwargs['system_prompt']).group(1))
            record = {**identities[0], 'outcome': 'findings_present', 'sections_inspected': ['Policy note'], 'coverage': 'partial',
                      'criterion': 'Fixture criterion', 'basis': 'Fixture finding', 'limitations': [], 'finding_ids': ['DS1.DOC1.F1'],
                      'review_state': 'unchecked', 'review_basis': ''}
            result['content'] = '## Findings ledger\n- [DS1.DOC1.F1] A fixture finding — dim: positions_and_attribution — anchor: "This invented quotation cannot match the supplied policy." — doc: archive_policy\n\n## Scope outcomes\n' + json.dumps([record])
        return result
    _,folder,records,log=generate(runtime,prepared,tmp_path,monkeypatch,source='mixed',override=change)
    assert len(log)==22 and records[job['key']]['invocations']==22
    assert records[job['key']]['process']['calls'][0]['reanchored']==1
    monkeypatch.setattr(runtime.core,'run_engine_call_auto',lambda **kw: pytest.fail('Paid replay'))
    assert study.validate_completed(job,records[job['key']],plan,folder,records,contexts,docs,runtime)


def test_canonical_campaign_lock_excludes_concurrent_launcher(tmp_path):
    import fcntl
    path = tmp_path / 'campaign.lock'
    with path.open('a') as a, path.open('a') as b:
        fcntl.flock(a, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with pytest.raises(BlockingIOError):
            fcntl.flock(b, fcntl.LOCK_EX | fcntl.LOCK_NB)


@pytest.mark.parametrize('changed', ['campaign', 'plan'])
def test_report_refuses_changed_campaign_or_saved_plan_before_empty_report(tmp_path, monkeypatch, changed):
    from contextlib import nullcontext
    plan = {'identity': 'a' * 64, 'frozen': 'input'}
    folder = tmp_path / plan['identity'][:16]
    study.write_json(tmp_path / 'campaign.json', {'identity': 'different' if changed == 'campaign' else plan['identity']})
    study.write_json(folder / 'plan.json', {**plan, 'frozen': 'changed'} if changed == 'plan' else plan)
    before = {p: p.read_bytes() for p in tmp_path.rglob('*.json')}
    monkeypatch.setattr(study, 'frozen_runtime', lambda: nullcontext(None))
    monkeypatch.setattr(study, 'build_plan', lambda *args: (plan, {}, {}))
    monkeypatch.setattr(study, 'report', lambda *args: pytest.fail('An identity mismatch became an empty successful report'))
    with pytest.raises(RuntimeError, match='Campaign identity changed|Saved plan differs'):
        study.main(['--phase', 'report', '--output-root', str(tmp_path)])
    assert {p: p.read_bytes() for p in tmp_path.rglob('*.json')} == before


def test_report_accepts_matching_campaign_and_plan_without_writing(tmp_path, monkeypatch, capsys):
    from contextlib import nullcontext
    plan = {'identity': 'a' * 64, 'frozen': 'input'}
    study.write_json(tmp_path / 'campaign.json', {'identity': plan['identity']})
    study.write_json(tmp_path / plan['identity'][:16] / 'plan.json', plan)
    before = {p: p.read_bytes() for p in tmp_path.rglob('*.json')}
    monkeypatch.setattr(study, 'frozen_runtime', lambda: nullcontext(None))
    monkeypatch.setattr(study, 'build_plan', lambda *args: (plan, {}, {}))
    monkeypatch.setattr(study, 'report', lambda *args: {'identity': plan['identity'], 'valid_generations': 0})
    assert study.main(['--phase', 'report', '--output-root', str(tmp_path)]) == 0
    assert json.loads(capsys.readouterr().out)['identity'] == plan['identity']
    assert {p: p.read_bytes() for p in tmp_path.rglob('*.json')} == before


def test_post_call_parser_failure_keeps_raw_receipts_and_cannot_retry(runtime, prepared, tmp_path, monkeypatch):
    plan, contexts, docs = prepared
    job = next(j for j in plan['generations'] if j['condition'] == 'original' and j['source'] == 'absence')
    root = tmp_path/'campaign'; folder = root/plan['identity'][:16]; records = {}; log = []
    malformed = '## Findings ledger\n- [F1] Ambiguous row — anchor: "First quotation" — anchor: "Different quotation"'
    monkeypatch.setattr(runtime.core,'run_engine_call_auto',fake_backend(log,override=lambda result,kw:{**result,'content':malformed}))
    with pytest.raises(ValueError,match='repeated anchor'):
        study.execute_job(job,plan,folder,records,contexts,docs,root,16,runtime)
    assert len(log)==1 and records[job['key']]['status']=='failed'
    path=next((folder/'receipts').glob('*/*/call-0001.json'))
    assert study.read_json(path)['status']=='complete'  # provider completed; deterministic application failed
    assert path.with_suffix('.md').read_text()==malformed
    monkeypatch.setattr(runtime.core,'run_engine_call_auto',lambda **kw:pytest.fail('Paid parser retry'))
    with pytest.raises(RuntimeError,match='no automatic retry'):
        study.execute_job(job,plan,folder,records,contexts,docs,root,16,runtime)
