"""Manual syntax queue: pinned dependencies, fake backends, no repair/adoption."""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('manual_score_collector', ROOT / 'scripts/study_argument_family_collect_manual_scores_2026_09_05.py')
manual = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(manual)
BASE_SPEC = importlib.util.spec_from_file_location('one_brace_collector_fixtures', ROOT / 'tests/test_study_argument_family_collect_scores_2026_09_05.py')
base = importlib.util.module_from_spec(BASE_SPEC)
BASE_SPEC.loader.exec_module(base)
campaign = base.campaign
offline = base.offline
setup = base.setup
RAW = (ROOT / 'tests/fixtures/argument_family_2026_09_05/malformed_sonnet_score_ganzinger.json').read_bytes()
KEY = 'score__sonnet__counterfactual_analyzer__candidate__ganzinger'


def switch_to_manual_case(c):
    c.job = {**c.job, 'key': KEY, 'rater': 'sonnet'}
    c.plan['judgments'].append(c.job)
    c.response.update(content=RAW.decode(), model_used=c.h.MODELS['judge_sonnet'], input_tokens=27829, output_tokens=883)
    c.rt.core.estimate_cost = lambda *args: .096732


@pytest.fixture
def configured(setup):
    c = setup
    c.collector = manual.load_collector()
    manual.install_manual(c.collector)
    switch_to_manual_case(c)
    c.collector.install_collection(c.first, c.h)
    return c


def test_actual_sonnet_failure_is_queued_without_any_proposed_correction(configured):
    c = configured
    assert c.first.sha(RAW) == '4ebea8c863132426d401b0969f31c34065fa97ad1f54fe68ad4356afbf883ac0'
    assert base.execute(c) is False
    assert len(c.calls) == 1 and c.records[KEY]['status'] == 'failed'
    entry = c.collector.pending_entries(c.run)[KEY]
    assert entry['rule'] == manual.MANUAL_RULE
    assert entry['corrected_sha256'] is None and entry['insert_byte'] is None
    assert entry['collector_sha256'] == manual.COLLECTOR_SHA
    assert entry['manual_adapter_sha256'] == c.first.sha(Path(manual.__file__).read_bytes())
    assert entry['accepted_output_created'] is False and entry['new_paid_calls_for_deferral'] == 0
    assert not (c.run / 'outputs' / (KEY + '.md')).exists()
    raw_path = c.run / 'receipts' / KEY / c.records[KEY]['attempt'] / 'call-0001.md'
    assert raw_path.read_bytes() == RAW
    with pytest.raises(json.JSONDecodeError):
        c.h.parse_score(RAW.decode())


def test_existing_one_brace_pending_entry_and_snapshot_stay_exact(setup):
    c = setup
    collector = manual.load_collector()
    collector.install_collection(c.first, c.h)
    base.execute(c)
    original = (c.run / collector.PENDING).read_bytes()
    entry = collector.pending_entries(c.run)[base.KEY]
    snapshot = (c.run / entry['failed_job_snapshot']).read_bytes()
    manual.install_manual(collector)
    assert base.execute(c) is False and len(c.calls) == 1
    assert (c.run / collector.PENDING).read_bytes() == original
    assert (c.run / entry['failed_job_snapshot']).read_bytes() == snapshot
    assert 'manual_adapter_sha256' not in entry and entry['insert_byte'] == 1888
    switch_to_manual_case(c)
    base.execute(c)
    entries = collector.pending_entries(c.run)
    assert entries[base.KEY] == entry and entries[KEY]['corrected_sha256'] is None
    assert (c.run / collector.PENDING).read_bytes().startswith(original)


def test_manual_failure_continuation_never_repeats_call_or_accepts_score(configured):
    c = configured
    base.execute(c)
    before_results = (c.run / 'results.json').read_bytes()
    before_pending = (c.run / c.collector.PENDING).read_bytes()
    assert base.execute(c) is False
    assert len(c.calls) == 1
    assert (c.run / 'results.json').read_bytes() == before_results
    assert (c.run / c.collector.PENDING).read_bytes() == before_pending
    c.job = {**c.job, 'key': 'score__sonnet__next'}
    c.plan['judgments'].append(c.job)
    corrected, _, _ = c.collector.one_brace(c.h, base.RAW)
    c.response['content'] = corrected.decode()
    base.execute(c)
    assert len(c.calls) == 2 and c.records[c.job['key']]['status'] == 'complete'
    assert c.records[KEY]['status'] == 'failed'


@pytest.mark.parametrize('raw', ['{"other": ', 'A non-JSON response with no complete score.', '{"reasons": {'])
def test_other_native_json_decode_failures_are_manual_only(configured, raw):
    c = configured
    c.response['content'] = raw
    assert base.execute(c) is False
    entry = c.collector.pending_entries(c.run)[KEY]
    assert entry['rule'] == manual.MANUAL_RULE and entry['corrected_sha256'] is None
    assert entry['insert_byte'] is None and c.records[KEY]['status'] == 'failed'


@pytest.mark.parametrize('raw', ['{}', '{"specificity": true}', '{"specificity": 1, "specificity": 2}'])
def test_non_jsondecode_schema_errors_remain_fatal(configured, raw):
    c = configured
    c.response['content'] = raw
    with pytest.raises(RuntimeError):
        base.execute(c)
    assert len(c.calls) == 1 and c.records[KEY]['error_type'] == 'RuntimeError'
    assert not (c.run / c.collector.PENDING).exists()


@pytest.mark.parametrize('change', [{'partial': True}, {'stop_reason': 'length'}, {'connection_error': 'reset'},
                                  {'input_tokens': None}, {'retries': None}, {'model_used': 'wrong/model'}, {'content': ''}])
def test_incomplete_backend_usage_or_fallback_still_stops(configured, change):
    c = configured
    c.response.update(change)
    with pytest.raises((RuntimeError, TypeError)):
        base.execute(c)
    assert len(c.calls) == 1 and not (c.run / c.collector.PENDING).exists()
    with pytest.raises(RuntimeError):
        base.execute(c)
    assert len(c.calls) == 1


def test_changed_call_binding_does_not_reach_manual_fallback(setup):
    c = setup
    switch_to_manual_case(c)
    with pytest.raises(json.JSONDecodeError):
        base.execute(c)
    directory = c.run / 'receipts' / KEY / c.records[KEY]['attempt']
    path = directory / 'call-0001.prompt.json'
    path.write_bytes(path.read_bytes() + b' ')
    collector = manual.load_collector()
    manual.install_manual(collector)
    collector.install_collection(c.first, c.h)
    with pytest.raises(RuntimeError, match='inventory/hash'):
        base.execute(c)
    assert len(c.calls) == 1 and not (c.run / collector.PENDING).exists()


def test_adapter_hash_tampering_blocks_gate_before_another_call(configured, monkeypatch):
    c = configured
    base.execute(c)
    path = c.run / c.collector.PENDING
    entry = json.loads(path.read_text())
    entry['manual_adapter_sha256'] = '0' * 64
    path.write_text(json.dumps(entry) + '\n')
    with pytest.raises(RuntimeError, match='manifest no longer matches'):
        c.collector.validate_pending(c.first, c.h, c.plan, c.run, c.records, {}, {}, c.rt)
    assert len(c.calls) == 1


def test_manual_adapter_preserves_budget_guard(configured):
    c = configured
    with pytest.raises(RuntimeError, match='ceiling'):
        base.execute(c, cap=.1)
    assert not c.calls and not (c.run / c.collector.PENDING).exists()


def test_scoped_hook_is_restored_after_binding_refusal(setup):
    c = setup
    collector = manual.load_collector()
    original = collector.one_brace
    manual.install_manual(collector)
    with pytest.raises(RuntimeError):
        collector.candidate(c.first, c.h, c.job, {}, c.plan, c.run, c.records, {}, {}, c.rt)
    assert collector.one_brace is original


def test_main_preserves_exact_original_arguments(monkeypatch):
    collector = manual.load_collector()
    original_candidate = collector.candidate
    forwarded = []
    def no_launch(args):
        assert collector.candidate is not original_candidate
        forwarded.append(args)
        return 0
    monkeypatch.setattr(collector, 'main', no_launch)
    monkeypatch.setattr(manual, 'load_collector', lambda: collector)
    args = ['--run', '--phase', 'judge', '--budget-usd', '16', '--review-record', '/exact/review.json']
    assert manual.main(args) == 0 and forwarded == [args]


def test_old_collector_pin_cannot_change(tmp_path, monkeypatch):
    path = tmp_path / 'collector.py'
    path.write_bytes(manual.COLLECTOR_PATH.read_bytes() + b'\n')
    monkeypatch.setattr(manual, 'COLLECTOR_PATH', path)
    with pytest.raises(RuntimeError, match='One-brace collector changed'):
        manual.load_collector()
