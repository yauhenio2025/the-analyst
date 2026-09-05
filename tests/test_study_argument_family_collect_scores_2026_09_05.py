"""Syntax collection is not acceptance; fake calls and temporary campaigns only."""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('argument_score_collector', ROOT / 'scripts/study_argument_family_collect_scores_2026_09_05.py')
collect = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collect)
FIXTURE_SPEC = importlib.util.spec_from_file_location('score_recovery_test_fixtures', ROOT / 'tests/test_study_argument_family_score_recovery_2026_09_05.py')
fixtures = importlib.util.module_from_spec(FIXTURE_SPEC)
FIXTURE_SPEC.loader.exec_module(fixtures)
campaign = fixtures.campaign
offline = fixtures.offline
RAW = (ROOT / 'tests/fixtures/argument_family_2026_09_05/malformed_sol_score_castoriadis.json').read_bytes()
KEY = 'score__sol__dialectical_structure__original__castoriadis'


@pytest.fixture
def setup(campaign, monkeypatch):
    c = campaign
    c.first = collect.load_first()
    c.job = {'key': KEY, 'kind': 'judge', 'source': 'fixture', 'reading': 'g0', 'rater': 'sol', 'base_calls': 1}
    c.plan['judgments'].append(c.job)
    c.plan['models'] = c.h.MODELS
    c.plan['calibration'] = {}
    c.calls = []
    c.response = {'content': RAW.decode(), 'model_used': c.h.MODELS['judge_sol'], 'input_tokens': 52308,
                  'output_tokens': 499, 'retries': 0, 'partial': None, 'stop_reason': None}
    def fake(**kwargs):
        c.calls.append(kwargs)
        return dict(c.response)
    c.rt.core.run_engine_call = fake
    c.rt.core.estimate_cost = lambda *args: .109606
    monkeypatch.setattr(c.h, 'estimate', lambda *args: {'estimate_usd': .2})
    return c


def execute(c, cap=16):
    return c.h.execute_job(c.job, c.plan, c.run, c.records, {}, {}, c.run.parent, cap, c.rt)


def test_actual_second_failure_has_exact_one_brace_candidate():
    first = collect.load_first()
    h = first.load_harness()
    corrected, offset, error = collect.one_brace(h, RAW)
    assert first.sha(RAW) == 'a1333d1f5283041b17deb1b342e4eddabc8cdadba485a624346b586ae877e702'
    assert offset == 1888
    assert first.sha(corrected) == 'f3447a8f7b4c36b0c34bfb5c04bc496829a72e580f422f5fd3f878cf0b7e8fbc'
    assert corrected[:offset] == RAW[:offset] and corrected[offset + 1:] == RAW[offset:]
    assert len(h.parse_score(corrected.decode())) == 8
    assert error == "Expecting ',' delimiter: line 1 column 2082 (char 2081)"
    with pytest.raises(json.JSONDecodeError):
        h.parse_score(RAW.decode())


@pytest.mark.parametrize('raw', [b'', b'{}', b'{"specificity":9', RAW.replace(b',"one_line":', b', "one_line":'),
                                 RAW + b',"one_line":', RAW[:-1]])
def test_other_malformed_or_incomplete_shapes_are_not_eligible(raw):
    h = collect.load_first().load_harness()
    with pytest.raises((RuntimeError, json.JSONDecodeError)):
        collect.one_brace(h, raw)


def test_existing_failure_is_deferred_without_repeated_call_or_output(setup):
    c = setup
    with pytest.raises(json.JSONDecodeError):
        execute(c)
    failed = json.loads(json.dumps(c.records[KEY]))
    before = (c.run / 'results.json').read_bytes()
    original_attempt = c.run / 'receipts' / KEY / failed['attempt']
    originals = {p.name: p.read_bytes() for p in original_attempt.iterdir()}
    collect.install_collection(c.first, c.h)
    assert execute(c) is False
    assert len(c.calls) == 1 and c.records[KEY] == failed
    assert (c.run / 'results.json').read_bytes() == before
    assert {p.name: p.read_bytes() for p in original_attempt.iterdir()} == originals
    assert not (c.run / 'outputs' / (KEY + '.md')).exists()
    manifest = (c.run / collect.PENDING).read_bytes()
    entry = collect.pending_entries(c.run)[KEY]
    assert entry['state'] == 'pending_independent_review_not_adopted'
    assert entry['insert_byte'] == 1888 and entry['accepted_output_created'] is False
    assert (c.run / entry['failed_job_snapshot']).read_bytes() == originals['job.json']
    assert execute(c) is False and len(c.calls) == 1
    assert (c.run / collect.PENDING).read_bytes() == manifest


def test_fresh_failure_is_saved_before_deferral_and_next_job_executes(setup):
    c = setup
    collect.install_collection(c.first, c.h)
    assert execute(c) is False
    assert c.records[KEY]['status'] == 'failed' and c.records[KEY]['error_type'] == 'JSONDecodeError'
    assert len(c.calls) == 1 and len(collect.pending_entries(c.run)) == 1
    c.job = {**c.job, 'key': 'score__sol__next'}
    c.plan['judgments'].append(c.job)
    corrected, _, _ = collect.one_brace(c.h, RAW)
    c.response['content'] = corrected.decode()
    execute(c)
    assert len(c.calls) == 2 and c.records[c.job['key']]['status'] == 'complete'
    assert c.records[KEY]['status'] == 'failed' and len(collect.pending_entries(c.run)) == 1


@pytest.mark.parametrize('mutation', [{'partial': True}, {'stop_reason': 'length'}, {'connection_error': 'reset'},
                                    {'input_tokens': None}, {'retries': None}, {'model_used': 'wrong/model'}, {'content': ''}])
def test_incomplete_fallback_or_unknown_calls_stop_without_deferral(setup, mutation):
    c = setup
    c.response.update(mutation)
    collect.install_collection(c.first, c.h)
    with pytest.raises((RuntimeError, TypeError)):
        execute(c)
    assert len(c.calls) == 1 and c.records[KEY]['status'] == 'failed'
    assert not (c.run / collect.PENDING).exists()
    with pytest.raises(RuntimeError):
        execute(c)
    assert len(c.calls) == 1


@pytest.mark.parametrize('artifact', ['parent', 'prompt', 'response', 'receipt', 'failed_record'])
def test_changed_receipt_or_parent_binding_refuses_deferral(setup, artifact):
    c = setup
    with pytest.raises(json.JSONDecodeError):
        execute(c)
    record = c.records[KEY]
    directory = c.run / 'receipts' / KEY / record['attempt']
    if artifact == 'parent':
        path = c.run / c.records['g0']['output']
    elif artifact == 'failed_record':
        path = directory / 'job.json'
    else:
        path = directory / {'prompt': 'call-0001.prompt.json', 'response': 'call-0001.response.json', 'receipt': 'call-0001.json'}[artifact]
    if artifact == 'failed_record':
        value = json.loads(path.read_bytes())
        value['error'] = 'Changed failure'
        c.h.write_json(path, value)
    else:
        path.write_bytes(path.read_bytes() + b' ')
    collect.install_collection(c.first, c.h)
    with pytest.raises(RuntimeError):
        execute(c)
    assert len(c.calls) == 1 and not (c.run / collect.PENDING).exists()


def test_pending_manifest_is_append_only_and_changed_entry_blocks(setup):
    c = setup
    collect.install_collection(c.first, c.h)
    execute(c)
    path = c.run / collect.PENDING
    entry = json.loads(path.read_text())
    entry['insert_byte'] += 1
    path.write_text(json.dumps(entry) + '\n')
    with pytest.raises(RuntimeError, match='bindings changed'):
        execute(c)
    assert len(c.calls) == 1


def test_original_budget_guard_still_stops_before_call(setup):
    c = setup
    collect.install_collection(c.first, c.h)
    with pytest.raises(RuntimeError, match='ceiling'):
        execute(c, cap=.1)
    assert not c.calls and not (c.run / collect.PENDING).exists()


@pytest.mark.parametrize('corruption', ['unknown_key', 'extra_field', 'snapshot', 'wrong_record_kind'])
def test_all_pending_bindings_are_checked_at_gate_before_any_new_call(setup, monkeypatch, corruption):
    c = setup
    gate_calls = []
    monkeypatch.setattr(c.h, 'review_gate', lambda *args: gate_calls.append(args) or {'decision': 'proceed'})
    collect.install_collection(c.first, c.h)
    execute(c)
    path = c.run / collect.PENDING
    entry = json.loads(path.read_text())
    if corruption == 'unknown_key':
        entry['key'] = 'not_a_planned_score'
    elif corruption == 'extra_field':
        entry['unreviewed'] = True
    elif corruption == 'snapshot':
        snapshot = c.run / entry['failed_job_snapshot']
        snapshot.write_bytes(snapshot.read_bytes() + b' ')
    else:
        c.records[KEY]['kind'] = 'generation'
    path.write_text(json.dumps(entry) + '\n')
    next_job = {**c.job, 'key': 'score__sol__next'}
    c.plan['judgments'].append(next_job)
    with pytest.raises(RuntimeError):
        c.h.review_gate('/unchanged/review.json', 'judge', c.plan, c.run, c.records, {}, {}, c.rt)
        c.h.execute_job(next_job, c.plan, c.run, c.records, {}, {}, c.run.parent, 16, c.rt)
    assert len(gate_calls) == 1 and len(c.calls) == 1
    assert next_job['key'] not in c.records


def test_source_review_rejection_is_preserved(setup, monkeypatch):
    c = setup
    def reject(*args):
        raise RuntimeError('Original source gate rejected')
    monkeypatch.setattr(c.h, 'review_gate', reject)
    collect.install_collection(c.first, c.h)
    with pytest.raises(RuntimeError, match='Original source gate rejected'):
        c.h.review_gate('/bad/review.json', 'judge', c.plan, c.run, c.records, {}, {}, c.rt)
    assert not c.calls


def test_report_excludes_pending_scores_from_accepted_count(setup, monkeypatch):
    c = setup
    monkeypatch.setattr(c.h, 'report', lambda *args: {'valid_judgments': 0, 'status_counts': {'failed': 1}})
    collect.install_collection(c.first, c.h)
    execute(c)
    result = c.h.report(c.plan, c.run, c.records, {}, {}, c.rt)
    assert result['valid_judgments'] == 0
    assert result['pending_score_syntax']['count'] == 1 and result['pending_score_syntax']['accepted'] == 0


@pytest.mark.parametrize('args', [['--adopt'], ['--run'], ['--run', '--phase', 'report'], ['--phase', 'corpus']])
def test_invalid_modes_never_reach_first_wrapper(args, monkeypatch):
    monkeypatch.setattr(collect, 'load_first', lambda: pytest.fail('Invalid mode reached first wrapper'))
    with pytest.raises(RuntimeError):
        collect.main(args)


def test_collection_delegates_exact_paid_args_and_does_not_replace_guards(monkeypatch):
    first = collect.load_first()
    h = first.load_harness()
    guards = {name: getattr(h, name) for name in ('budget_guard', 'validate_saved_campaign', 'guard_inputs')}
    monkeypatch.setattr(first, 'load_harness', lambda: h)
    forwarded = []
    def no_launch(args):
        loaded = first.load_harness()
        assert all(getattr(loaded, name) is value for name, value in guards.items())
        forwarded.append(args)
        return 0
    monkeypatch.setattr(first, 'main', no_launch)
    monkeypatch.setattr(collect, 'load_first', lambda: first)
    args = ['--run', '--phase', 'judge', '--budget-usd', '16', '--review-record', '/exact/review.json']
    assert collect.main(args) == 0 and forwarded == [args]


def test_first_wrapper_pin_is_immutable(tmp_path, monkeypatch):
    path = tmp_path / 'wrapper.py'
    path.write_bytes(collect.FIRST_PATH.read_bytes() + b'\n')
    monkeypatch.setattr(collect, 'FIRST_PATH', path)
    with pytest.raises(RuntimeError, match='First recovery wrapper changed'):
        collect.load_first()
