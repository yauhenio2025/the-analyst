"""Offline recovery lifecycle; any artifact-backed adoption runs only in a temp copy."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/adopt_ideas_hegel_recovery_2026_09_05.py'
spec = importlib.util.spec_from_file_location('recovery_adopter', SCRIPT)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)
BUNDLES = ('ruling_recovery/20260905T082845.591540Z', 'rewrite_recovery/20260905T084347.772343Z')
HASHES = ('ad296c943f5a46e5edcd3e62c8983447bfed826fb8e585859ffa9ce83509c64e',
          '6b7f5e0e02a338d1b006ec8d17e62507ab28800b148ebefc850fb7186dcfed26')


def test_sensitivity_does_not_infer_unfinished_winners():
    pairs = [dict(engine=e, paper=p, outcome='incomplete') for e in adapter.proposal.load_harness().ENGINES for p in ('ganzinger', 'elling')]
    result = adapter.recovery_sensitivity(pairs)
    assert result['all_planned_pairs']['incomplete'] == 8
    assert result['excluding_recovered_generation_pairs']['incomplete'] == 6
    pairs[2]['outcome'] = 'revised'  # Recovered Argument/Ganzinger pair.
    pairs[0]['outcome'] = 'split'
    pairs[1]['outcome'] = 'previous'
    result = adapter.recovery_sensitivity(pairs)
    assert result['all_planned_pairs']['revised'] == 1
    assert result['excluding_recovered_generation_pairs']['revised'] == 0
    assert result['excluding_recovered_generation_pairs']['split'] == 1
    assert result['excluding_recovered_generation_pairs']['previous'] == 1
    assert result['frozen_processing_incomplete_pairs'] == 2


def test_campaign_lock_prevents_adoption_while_generation_runs(tmp_path):
    run = tmp_path / adapter.proposal.IDENTITY[:16]
    with adapter.campaign_lock(run):
        with pytest.raises(RuntimeError, match='Campaign is active'):
            with adapter.campaign_lock(run):
                pytest.fail('Concurrent adoption entered')


def test_running_record_blocks_adoption(tmp_path):
    h = adapter.proposal.load_harness()
    h.write_json(tmp_path / 'results.json', {'job': {'status': 'running'}})
    with pytest.raises(RuntimeError, match='record is running'):
        adapter.require_idle(h, tmp_path)


def test_original_execute_job_refuses_paid_retry(tmp_path):
    h = adapter.proposal.load_harness()
    target = adapter.proposal.TARGET
    run = tmp_path / adapter.proposal.IDENTITY[:16]
    receipt = run / 'receipts' / target / adapter.proposal.ATTEMPT / 'call-0001.json'
    receipt.parent.mkdir(parents=True); receipt.write_text('{}')
    # Refusal precedes backend access, source checks, new attempts or any write.
    with pytest.raises(RuntimeError, match='no automatic paid retry'):
        h.execute_job({'key': target}, {}, run, {target: {'status': 'failed'}}, {}, {}, tmp_path, tmp_path, 6, None)
    assert list(run.rglob('call-*.json')) == [receipt]


def test_two_report_wrappers_merge_history_and_leave_execution_unchanged(monkeypatch, tmp_path):
    h = adapter.proposal.load_harness()
    execute = h.execute_job
    pairs = [dict(engine=e, paper=p, outcome='incomplete') for e in h.ENGINES for p in h.SOURCES]
    records = {target: {'recovery': {'test': target}} for target in adapter.RECIPES}
    monkeypatch.setattr(adapter, 'load_bundle', lambda bundle, digest, run: {'target': str(bundle)})
    monkeypatch.setattr(h, 'read_json', lambda *a: records)
    monkeypatch.setattr(h, 'report', lambda *a: {'pairs': copy.deepcopy(pairs), 'limitations': []})
    for target in adapter.RECIPES:
        adapter.install_adapter(h, target, 'test', tmp_path)
    report = h.report({}, tmp_path, {}, {}, None)
    assert h.execute_job is execute
    assert set(report['recovery_provenance']) == set(adapter.RECIPES)
    assert len(report['historical_postprocess_failures']) == 2
    assert len(report['limitations']) == 1
    assert report['recovery_sensitivity']['all_planned_pairs']['incomplete'] == 8


@pytest.fixture(scope='module')
def isolated(tmp_path_factory):
    source = ROOT / 'data/study/ideas_hegel_heldout_2026_09_05' / adapter.proposal.IDENTITY[:16]
    if not all((source / 'reader_notes' / rel / 'manifest.json').is_file() for rel in BUNDLES):
        pytest.skip('Ignored reviewed recovery bundles are not available in this checkout')
    h = adapter.proposal.load_harness()
    if not all((ROOT / 'data/study/sources_ideas' / name).is_file() for name in h.SOURCES.values()) or not (ROOT / 'data/study/ideas_2026_09_05/374325c24e6b10a1/results.json').is_file():
        pytest.skip('Ignored sources/calibration receipts are not available')
    run = tmp_path_factory.mktemp('isolated-recovery') / adapter.proposal.IDENTITY[:16]
    run.mkdir()
    records = {}
    bundles = []
    for rel, digest in zip(BUNDLES, HASHES):
        bundle = run / 'reader_notes' / rel
        shutil.copytree(source / 'reader_notes' / rel, bundle, ignore=shutil.ignore_patterns('adoptions'))
        manifest = json.loads((bundle / 'manifest.json').read_bytes())
        assert adapter.sha((bundle / 'manifest.json').read_bytes()) == digest
        for name in manifest['input_files_sha256']:
            path = run / name; path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / name, path)
        records.update({key: entry['original_record'] for key, entry in manifest['jobs'].items()})
        bundles.append(bundle)
    h.write_json(run / 'results.json', records)
    return run, bundles


def cli(isolated, *extra, success=True):
    run, bundles = isolated
    argv = [sys.executable, str(SCRIPT), '--run-dir', str(run)]
    for bundle, digest in zip(bundles, HASHES):
        argv += ['--bundle', str(bundle), '--manifest-sha256', digest]
    # The CLI installs a process-wide network denial hook for every command here.
    result = subprocess.run(argv + list(extra), cwd=ROOT, env=os.environ.copy(), capture_output=True, text=True)
    if success:
        assert result.returncode == 0, result.stderr + result.stdout
        return json.loads(result.stdout)
    assert result.returncode != 0
    return result.stderr + result.stdout


def test_actual_two_target_lifecycle_is_network_free_and_preserves_billing(isolated):
    run, bundles = isolated
    original_results = (run / 'results.json').read_bytes()
    originals = {str(p.relative_to(run)): p.read_bytes() for p in run.glob('receipts/*/*/*') if p.is_file()}
    preview = cli(isolated)
    assert len(preview['recoveries']) == 2 and all(r['state'] == 'OFFLINE_ADOPTION_PREVIEW' for r in preview['recoveries'])
    assert (run / 'results.json').read_bytes() == original_results
    assert not any((run / 'outputs' / (key + '.md')).exists() for key in adapter.RECIPES)
    before_report = cli(isolated, '--phase', 'report')
    adopted = cli(isolated, '--adopt')
    assert len(adopted['recoveries']) == 2 and all(r['new_paid_calls'] == 0 for r in adopted['recoveries'])
    final_results = (run / 'results.json').read_bytes()
    report = cli(isolated, '--phase', 'report')
    assert report['valid_generations'] == 9 and report['valid_judgments'] == 0
    assert report['validation_errors'] == {}
    assert report['usage_total'] == before_report['usage_total']
    assert set(report['recovery_provenance']) == set(adapter.RECIPES)
    assert len(report['historical_postprocess_failures']) == 2
    assert report['recovery_sensitivity']['all_planned_pairs']['incomplete'] == 8
    assert report['recovery_sensitivity']['excluding_recovered_generation_pairs']['incomplete'] == 6
    assert {str(p.relative_to(run)): p.read_bytes() for p in run.glob('receipts/*/*/*') if p.is_file()} == originals
    again = cli(isolated, '--adopt')
    assert all(r['state'] == 'already_adopted' for r in again['recoveries'])
    assert (run / 'results.json').read_bytes() == final_results
    assert 'Study is not complete' in cli(isolated, '--phase', 'report', '--require-complete', success=False)


@pytest.mark.parametrize('part', ['manifest', 'output', 'prompt', 'failed_job'])
def test_tampered_reviewed_input_is_refused(isolated, part):
    run, bundles = isolated
    manifest = json.loads((bundles[0] / 'manifest.json').read_bytes())
    path = {'manifest': bundles[0] / 'manifest.json', 'output': bundles[0] / 'recovered.md',
        'prompt': next(run / name for name in manifest['input_files_sha256'] if name.endswith('.prompt.json')),
        'failed_job': run / f'receipts/{adapter.proposal.TARGET}/{adapter.proposal.ATTEMPT}/job.json'}[part]
    original = path.read_bytes()
    try:
        path.write_bytes(original + b' ')
        with pytest.raises(RuntimeError, match='changed'):
            adapter.load_bundle(bundles[0], HASHES[0], run)
    finally:
        path.write_bytes(original)


def test_record_metadata_tamper_invalidates_adopted_parent(isolated):
    run, _ = isolated
    cli(isolated, '--adopt')  # Also makes this test valid when selected alone.
    path = run / 'results.json'; original = path.read_bytes(); records = json.loads(original)
    assert records[adapter.proposal.TARGET]['status'] == 'complete'
    records[adapter.proposal.TARGET]['recovery']['adapter_sha256'] = 'forged'
    try:
        path.write_text(json.dumps(records))
        report = cli(isolated, '--phase', 'report')
        assert report['valid_generations'] == 8
        assert adapter.proposal.TARGET in report['validation_errors']
        assert report['valid_judgments'] == 0
    finally:
        path.write_bytes(original)
