"""Campaign-specific score repair; all adoption writes target temporary fixtures."""
import fcntl
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('argument_score_recovery', ROOT / 'scripts/study_argument_family_score_recovery_2026_09_05.py')
recovery = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recovery)
RAW = (ROOT / 'tests/fixtures/argument_family_2026_09_05/malformed_sol_score.json').read_bytes()


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    import socket
    def forbidden(*args, **kwargs):
        pytest.fail('Network is forbidden in score recovery tests')
    monkeypatch.setattr(socket.socket, 'connect', forbidden)
    monkeypatch.setattr(socket, 'getaddrinfo', forbidden)


def test_exact_known_repair_changes_only_one_byte_and_preserves_scores_reasons():
    h = recovery.load_harness()
    strict = h.parse_score
    with pytest.raises(json.JSONDecodeError):
        strict(RAW.decode())
    fixed = recovery.repair(RAW)
    assert fixed[:2049] == RAW[:2049] and fixed[2050:] == RAW[2049:] and fixed[2049:2050] == b'}'
    assert recovery.sha(fixed) == recovery.REPAIRED_SHA
    value = recovery.recover_known(h, RAW.decode())
    assert tuple(value[k] for k in h.RUBRIC_KEYS) == (9, 8, 8, 7, 9, 8)
    assert set(value) == set(h.RUBRIC_KEYS) | {'reasons', 'one_line'}
    assert set(value['reasons']) == set(h.RUBRIC_KEYS)
    assert value == strict(fixed.decode())


@pytest.mark.parametrize('mutation', [lambda raw: raw + b' ', lambda raw: raw.replace(b'9', b'8', 1),
                                      lambda raw: raw.replace(b'one_line', b'summary')])
def test_nearby_malformed_responses_are_not_salvaged(mutation):
    h = recovery.load_harness()
    with pytest.raises((RuntimeError, json.JSONDecodeError)):
        h.parse_score(mutation(RAW).decode())


@pytest.mark.parametrize('case', ['extra_key', 'missing_reason', 'duplicate', 'bool', 'nan'])
def test_normal_parser_schema_stays_strict(case):
    h = recovery.load_harness()
    value = recovery.recover_known(h, RAW.decode())
    if case == 'extra_key':
        value['extra'] = 'No'
    elif case == 'missing_reason':
        value['reasons'].pop(h.RUBRIC_KEYS[0])
    elif case == 'bool':
        value[h.RUBRIC_KEYS[0]] = True
    elif case == 'nan':
        value[h.RUBRIC_KEYS[0]] = float('nan')
    raw = json.dumps(value)
    if case == 'duplicate':
        raw = raw[:-1] + ', "one_line": "Again"}'
    with pytest.raises(RuntimeError):
        h.parse_score(raw)


def test_changed_harness_and_repair_pin_fail_closed(tmp_path, monkeypatch):
    path = tmp_path / 'harness.py'
    path.write_bytes(recovery.HARNESS.read_bytes() + b'\n')
    monkeypatch.setattr(recovery, 'HARNESS', path)
    with pytest.raises(RuntimeError, match='Pinned bytes'):
        recovery.load_harness()
    monkeypatch.setattr(recovery, 'REPAIRED_SHA', '0' * 64)
    with pytest.raises(RuntimeError, match='Repaired score hash'):
        recovery.repair(RAW)


@pytest.fixture
def campaign(tmp_path, monkeypatch):
    """Tiny fake completed jobs, real pinned malformed response and harness utilities."""
    h = recovery.load_harness()
    run = tmp_path / 'campaign' / recovery.IDENTITY[:16]
    run.mkdir(parents=True)
    (run / 'outputs').mkdir()
    log = tmp_path / 'judge.log'
    log.write_bytes(b'Original failed parser log\n')
    jobs = [{'key': f'g{i}', 'kind': 'generation'} for i in range(24)]
    judges = [{'key': f's{i}', 'kind': 'judge'} for i in range(11)]
    target = {'key': recovery.TARGET, 'kind': 'judge', 'reading': 'g0', 'source': 'fixture', 'rater': 'sol'}
    plan = {'identity': recovery.IDENTITY, 'generations': jobs, 'judgments': judges + [target], 'corroborations': []}
    records = {}
    for job in jobs + judges:
        content = ('Completed ' + job['key']).encode()
        output = 'outputs/' + job['key'] + '.md'
        (run / output).write_bytes(content)
        records[job['key']] = {**job, 'status': 'complete', 'output': output, 'output_sha256': recovery.sha(content)}
    prompt = {'system': 'Frozen scoring rubric', 'user': 'Exact source and analysis'}
    response = {'content': RAW.decode(), 'model_used': h.MODELS['judge_sol'], 'input_tokens': 17274,
                'output_tokens': 566, 'retries': 0, 'partial': None, 'stop_reason': None}
    receipt = {'status': 'complete', 'model_requested': h.MODELS['judge_sol'], 'model_used': h.MODELS['judge_sol'],
               'label': 'argument-family ' + recovery.TARGET, 'prompt_sha256': h.digest(prompt),
               'response_sha256': h.digest(response), 'output_sha256': recovery.RAW_SHA,
               'input_tokens': 17274, 'output_tokens': 566, 'retries': 0, 'cost_usd': .040208}
    directory = recovery.attempt(run)
    h.write_json(directory / 'call-0001.json', receipt)
    h.write_json(directory / 'call-0001.prompt.json', prompt)
    h.write_json(directory / 'call-0001.response.json', response)
    (directory / 'call-0001.md').write_bytes(RAW)
    calls = {p.name: recovery.sha(p.read_bytes()) for p in directory.glob('call-*')}
    failed = {'key': recovery.TARGET, 'kind': 'judge', 'status': 'failed', 'identity': recovery.IDENTITY,
              'attempt': recovery.ATTEMPT, 'job_sha256': h.digest(target), 'error_type': 'JSONDecodeError',
              'error': 'Known malformed syntax', 'invocations': 1, 'seconds': 10.249,
              'inputs_sha256': {'g0': records['g0']['output_sha256']},
              'invocation_files_sha256': {str((directory / name).relative_to(run)): value for name, value in calls.items()}}
    records[recovery.TARGET] = failed
    h.write_json(directory / 'job.json', failed)
    h.write_json(run / 'results.json', records)
    h.write_json(run / 'plan.json', plan)
    h.write_json(run.parent / 'campaign.json', {'identity': recovery.IDENTITY, 'cap_usd': 16})
    for name, value in {'CALL_HASHES': calls, 'FAILED_JOB_SHA': recovery.sha((directory / 'job.json').read_bytes()),
                        'RESULTS_SHA': recovery.sha((run / 'results.json').read_bytes()),
                        'PLAN_SHA': recovery.sha((run / 'plan.json').read_bytes()), 'LOG_SHA': recovery.sha(log.read_bytes())}.items():
        monkeypatch.setattr(recovery, name, value)
    monkeypatch.setattr(h, 'build_plan', lambda *args: (plan, {}, {'fixture': {'doc': 'Exact source'}}))
    monkeypatch.setattr(h, 'guard_inputs', lambda p: h.require(p == plan, 'Plan changed'))
    monkeypatch.setattr(h, 'judge_prompt', lambda *args: prompt)
    checked = []
    real_validate = h.validate_completed
    def validate_completed(job, record, p, folder, all_records, contexts, docs, rt):
        checked.append(job['key'])
        if job['key'] == recovery.TARGET:
            return real_validate(job, record, p, folder, all_records, contexts, docs, rt)
        assert record['status'] == 'complete'
        h.require(recovery.sha((folder / record['output']).read_bytes()) == record['output_sha256'], 'Completed output changed')
        return True
    monkeypatch.setattr(h, 'validate_completed', validate_completed)
    def validate_call(saved, actual, model, label):
        r, p, text = saved
        h.require(r['status'] == 'complete' and r['model_requested'] == r['model_used'] == model, 'Model/status mismatch')
        h.require(p == actual and h.digest(p) == r['prompt_sha256'] and r['label'] == label, 'Prompt/label mismatch')
        h.require(h.digest(text.encode()) == r['output_sha256'], 'Raw hash mismatch')
    rt = SimpleNamespace(h=SimpleNamespace(validate_call=validate_call), core=SimpleNamespace(estimate_cost=lambda *args: .040208))
    recovery.install_reporting(h)
    return SimpleNamespace(h=h, rt=rt, run=run, log=log, records=records, plan=plan, checked=checked)


def test_preview_replays_all_completed_jobs_and_writes_nothing(campaign):
    c = campaign
    before = {str(p.relative_to(c.run)): p.read_bytes() for p in c.run.rglob('*') if p.is_file()}
    _, _, judgment, already = recovery.prepare(c.h, c.rt, c.run, c.log)
    assert len(c.checked) == 35 and len(set(c.checked)) == 35 and not already
    assert tuple(judgment[k] for k in c.h.RUBRIC_KEYS) == recovery.SCORES
    assert before == {str(p.relative_to(c.run)): p.read_bytes() for p in c.run.rglob('*') if p.is_file()}


@pytest.mark.parametrize('artifact', ['completed_output', 'raw', 'invocation', 'response', 'failed_job', 'results', 'plan', 'log'])
def test_any_changed_bound_input_prevents_publication(campaign, artifact):
    c = campaign
    paths = {'completed_output': c.run / c.records['g1']['output'], 'raw': recovery.attempt(c.run) / 'call-0001.md',
             'invocation': recovery.attempt(c.run) / 'call-0001.json', 'response': recovery.attempt(c.run) / 'call-0001.response.json',
             'failed_job': recovery.attempt(c.run) / 'job.json', 'results': c.run / 'results.json',
             'plan': c.run / 'plan.json', 'log': c.log}
    path = paths[artifact]
    path.write_bytes(path.read_bytes() + b' ')
    with pytest.raises(RuntimeError):
        recovery.adopt(c.h, c.rt, c.run, c.log)
    assert not (c.run / recovery.OUTPUT).exists()
    assert not (c.run / recovery.BUNDLE).exists()


def test_adoption_preserves_failure_and_raw_bytes_and_is_idempotent(campaign):
    c = campaign
    before = (c.run / 'results.json').read_bytes()
    failed = (recovery.attempt(c.run) / 'job.json').read_bytes()
    raw_files = {p.name: p.read_bytes() for p in recovery.attempt(c.run).glob('call-*')}
    result = recovery.adopt(c.h, c.rt, c.run, c.log)
    assert result['valid_native_scores'] == 11 and result['valid_recovered_scores'] == 1
    bundle = c.run / recovery.BUNDLE
    assert (bundle / 'results.failed.json').read_bytes() == before
    assert (bundle / 'job.failed.json').read_bytes() == failed
    assert (bundle / 'judge.failed.log').read_bytes() == c.log.read_bytes()
    for name, raw in raw_files.items():
        assert (recovery.attempt(c.run) / name).read_bytes() == raw == (bundle / 'original_attempt' / name).read_bytes()
    records = c.h.read_json(c.run / 'results.json')
    assert all(records[key] == value for key, value in c.records.items() if key != recovery.TARGET)
    assert records[recovery.TARGET]['invocation_files_sha256'] == c.records[recovery.TARGET]['invocation_files_sha256']
    assert c.h.budget_guard(c.run.parent, 16, 0) == .040208
    assert recovery.adopt(c.h, c.rt, c.run, c.log)['state'] == 'already_adopted'
    assert recovery.validate_adopted(c.h, c.run, records[recovery.TARGET])


@pytest.mark.parametrize('artifact', ['score', 'snapshot', 'manifest', 'record'])
def test_adopted_provenance_cannot_be_rewritten(campaign, artifact):
    c = campaign
    recovery.adopt(c.h, c.rt, c.run, c.log)
    record = c.h.read_json(c.run / 'results.json')[recovery.TARGET]
    if artifact == 'record':
        record['judgment']['specificity'] = 1
    else:
        path = {'score': c.run / recovery.OUTPUT, 'snapshot': c.run / recovery.BUNDLE / 'job.failed.json',
                'manifest': c.run / recovery.BUNDLE / 'manifest.json'}[artifact]
        path.write_bytes(path.read_bytes() + b' ')
    with pytest.raises(RuntimeError):
        recovery.validate_adopted(c.h, c.run, record)


@pytest.mark.parametrize('field', ['attempt', 'raw_sha256', 'repaired_raw_sha256', 'insert_byte',
                                   'validated_generations', 'validated_native_scores', 'files_sha256'])
def test_manifest_fixed_facts_cannot_change_even_with_new_record_hash(campaign, field):
    c = campaign
    recovery.adopt(c.h, c.rt, c.run, c.log)
    record = c.h.read_json(c.run / 'results.json')[recovery.TARGET]
    path = c.run / recovery.BUNDLE / 'manifest.json'
    manifest = c.h.read_json(path)
    if field == 'files_sha256':
        manifest[field].pop('score.json')
    elif isinstance(manifest[field], int):
        manifest[field] += 1
    else:
        manifest[field] = 'Changed'
    c.h.write_json(path, manifest)
    record['recovery']['manifest_sha256'] = recovery.sha(path.read_bytes())
    with pytest.raises(RuntimeError, match='manifest facts|snapshot inventory'):
        recovery.validate_adopted(c.h, c.run, record)


def test_same_raw_for_fresh_other_score_still_fails_strict_parser(campaign, monkeypatch):
    c = campaign
    job = {'key': 'score__sol__different', 'kind': 'judge', 'source': 'fixture', 'reading': 'g0',
           'rater': 'sol', 'base_calls': 1}
    c.plan['calibration'] = {}
    monkeypatch.setattr(c.h, 'estimate', lambda *args: {'estimate_usd': .1})
    calls = []
    def fake(**kwargs):
        calls.append(kwargs)
        return {'content': RAW.decode(), 'model_used': c.h.MODELS['judge_sol'], 'input_tokens': 17274,
                'output_tokens': 566, 'retries': 0, 'partial': None, 'stop_reason': None}
    c.rt.core.run_engine_call = fake
    # A fresh different logical job is allowed to call its fake backend once,
    # but its byte-identical malformed response has no reviewed recovery scope.
    with pytest.raises(json.JSONDecodeError):
        c.h.execute_job(job, c.plan, c.run, c.records, {}, {}, c.run.parent, 16, c.rt)
    assert len(calls) == 1 and c.records[job['key']]['status'] == 'failed'
    assert c.records[job['key']]['error_type'] == 'JSONDecodeError'
    with pytest.raises(json.JSONDecodeError):
        c.h.parse_score(RAW.decode())


def test_only_adopted_target_replay_can_use_repair_and_restores_parser(campaign):
    c = campaign
    recovery.adopt(c.h, c.rt, c.run, c.log)
    records = c.h.read_json(c.run / 'results.json')
    target = c.plan['judgments'][-1]
    assert c.h.validate_completed(target, records[recovery.TARGET], c.plan, c.run, records, {}, {}, c.rt)
    with pytest.raises(json.JSONDecodeError):
        c.h.parse_score(RAW.decode())


def test_campaign_lock_prevents_adoption(campaign):
    c = campaign
    with (c.run.parent / 'campaign.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with pytest.raises(RuntimeError, match='Campaign is active'):
            recovery.adopt(c.h, c.rt, c.run, c.log)
    assert not (c.run / recovery.BUNDLE).exists()


def test_reporting_keeps_native_and_recovered_counts_separate(campaign, monkeypatch):
    c = campaign
    recovery.adopt(c.h, c.rt, c.run, c.log)
    records = c.h.read_json(c.run / 'results.json')
    monkeypatch.setattr(c.h, 'report', lambda *args: {'valid_judgments': 12, 'validation_errors': {}})
    recovery.install_reporting(c.h)
    report = c.h.report(c.plan, c.run, records, {}, {}, c.rt)
    assert report['valid_judgments'] == 12
    assert report['score_recovery']['valid_native_scores'] == 11
    assert report['score_recovery']['valid_recovered_scores'] == 1
    assert report['score_recovery']['recovered_keys'] == [recovery.TARGET]


@pytest.mark.parametrize('args', [['--run'], ['--run', '--phase', 'initial'], ['--adopt', '--phase', 'judge']])
def test_invalid_entry_modes_stop_before_harness(args, monkeypatch):
    monkeypatch.setattr(recovery, 'load_harness', lambda: pytest.fail('Invalid mode reached harness'))
    with pytest.raises(RuntimeError):
        recovery.main(args)


def test_judge_resume_forwards_original_args_after_provenance_check(campaign, monkeypatch):
    c = campaign
    recovery.adopt(c.h, c.rt, c.run, c.log)
    monkeypatch.setattr(recovery, 'RUN', c.run)
    monkeypatch.setattr(recovery, 'load_harness', lambda: c.h)
    forwarded = []
    monkeypatch.setattr(c.h, 'main', lambda args: forwarded.append(args) or 0)
    args = ['--run', '--phase', 'judge', '--budget-usd', '16', '--review-record', '/review.json']
    assert recovery.main(args) == 0
    assert forwarded == [args]


def test_no_adoption_means_no_paid_resume(campaign, monkeypatch):
    c = campaign
    monkeypatch.setattr(recovery, 'RUN', c.run)
    monkeypatch.setattr(recovery, 'load_harness', lambda: c.h)
    monkeypatch.setattr(c.h, 'main', lambda args: pytest.fail('Unadopted failure reached paid harness'))
    with pytest.raises(RuntimeError, match='adoption must precede'):
        recovery.main(['--run', '--phase', 'judge', '--budget-usd', '16'])
