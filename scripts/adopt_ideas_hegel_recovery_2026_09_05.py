"""Reviewed external adoption/report/judge adapter; frozen harness remains byte-identical.

Default previews adoption. --adopt requires an idle campaign and preserves the original
failed job.json and all call files in place. --phase report is offline. Only explicit
--phase judge --run --budget-usd 6 may invoke models, via the unchanged harness.
A crash leaving an output but no completed record requires explicit review; no automatic
paid retry or orphan-output replacement is implemented.
"""
from __future__ import annotations

import argparse
import copy
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location('hegel_recovery_proposal', ROOT / 'scripts/recover_ideas_hegel_heldout_2026_09_05.py')
proposal = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(proposal)
require, sha = proposal.require, proposal.sha
_spec2 = importlib.util.spec_from_file_location('hegel_rewrite_recovery_proposal', ROOT / 'scripts/recover_ideas_hegel_rewrite_2026_09_05.py')
rewrite_proposal = importlib.util.module_from_spec(_spec2)
_spec2.loader.exec_module(rewrite_proposal)
RECIPES = {proposal.TARGET: proposal, rewrite_proposal.TARGET: rewrite_proposal}
RECOVERED_PAIRS = {(target.split('__')[0], target.split('__')[2]) for target in RECIPES}


def recovery_sensitivity(pairs):
    """Pre-judge policy: count valid agreements, and expose recovery dependence."""
    def counts(selected):
        outcomes = {name: 0 for name in ('previous', 'revised', 'tie', 'split', 'incomplete')}
        for pair in selected:
            require(pair['outcome'] in outcomes, 'Unexpected pair outcome')
            outcomes[pair['outcome']] += 1
        return {'pair_count': len(selected), **outcomes}
    unaffected = [p for p in pairs if (p['engine'], p['paper']) not in RECOVERED_PAIRS]
    return {'all_planned_pairs': counts(pairs), 'excluding_recovered_generation_pairs': counts(unaffected),
        'excluded_pairs': [{'engine': e, 'paper': p} for e, p in sorted(RECOVERED_PAIRS)],
        'frozen_processing_incomplete_pairs': 2,
        'policy': 'Set before judging: retain both accepted recoveries in the eight-pair analysis; also report the six pairs that needed no offline generation recovery. Incomplete pairs never imply a winner.'}


def load_bundle(bundle, accepted_sha, run):
    raw = (bundle / 'manifest.json').read_bytes()
    require(sha(raw) == accepted_sha, 'Reviewed recovery manifest changed')
    manifest = json.loads(raw)
    recipe = RECIPES.get(manifest.get('target'))
    require(recipe is not None, 'Unreviewed recovery target')
    require(manifest['plan_identity'] == proposal.IDENTITY and manifest['harness_sha256'] == proposal.HARNESS_SHA256,
            'Recovery identity/harness differs')
    require(manifest['target'] == recipe.TARGET and manifest['target_attempt'] == recipe.ATTEMPT,
            'Recovery target differs')
    require(manifest['comparison_keys'] == list(recipe.COMPARISONS) and manifest['completed_finals_compared'] == len(recipe.COMPARISONS)
            and manifest['all_completed_comparisons_byte_identical'] is True and manifest['new_paid_calls'] == 0,
            'Recovery equivalence evidence is incomplete')
    require(manifest['transformation_code_sha256'] == sha(Path(recipe.__file__).read_bytes()) == sha((bundle / 'recovery_script.snapshot.py').read_bytes()),
            'Reviewed transformation code changed')
    require(sha((bundle / 'recovered.md').read_bytes()) == manifest['target_output_sha256'], 'Recovered artifact changed')
    for name, field in [('plan.snapshot.json', 'plan_file_sha256'), ('results.snapshot.json', 'results_snapshot_sha256')]:
        require(sha((bundle / name).read_bytes()) == manifest[field], f'Original snapshot changed: {name}')
    if 'replay_dependency_sha256' in manifest:
        require(manifest['replay_dependency_sha256'] == sha(Path(proposal.__file__).read_bytes()) == sha((bundle / 'replay_dependency.snapshot.py').read_bytes()), 'Replay dependency changed')
    target_entry = manifest['jobs'][recipe.TARGET]
    failed_raw = (bundle / 'failed_job.snapshot.json').read_bytes()
    require(sha(failed_raw) == manifest['input_files_sha256'][f'receipts/{recipe.TARGET}/{recipe.ATTEMPT}/job.json'], 'Original failed job snapshot bytes changed')
    failed = json.loads(failed_raw)
    require(failed == target_entry['original_record'] and failed['status'] == 'failed' and failed['error'] == recipe.EXPECTED_ERROR,
            'Original failed job snapshot differs')
    for name, expected in manifest['input_files_sha256'].items():
        require(sha((run / name).read_bytes()) == expected, f'Original artifact changed: {name}')
    prefix = f'receipts/{recipe.TARGET}/{recipe.ATTEMPT}/call-'
    expected_copies = {Path(name).name for name in manifest['input_files_sha256'] if name.startswith(prefix)}
    require({p.name for p in (bundle / 'original_attempt').glob('call-*')} == expected_copies, 'Original call snapshot inventory differs')
    for path in (bundle / 'original_attempt').glob('call-*'):
        live = run / 'receipts' / recipe.TARGET / recipe.ATTEMPT / path.name
        require(path.read_bytes() == live.read_bytes(), f'Original call snapshot changed: {path.name}')
    return manifest


def annotation(bundle, accepted_sha, manifest, run):
    recipe = RECIPES[manifest['target']]
    entry = manifest['jobs'][recipe.TARGET]
    original_job = f'receipts/{recipe.TARGET}/{recipe.ATTEMPT}/job.json'
    return {'method': manifest['kind'],
        'manifest': str((bundle / 'manifest.json').relative_to(run)), 'manifest_sha256': accepted_sha,
        'transformation_code_sha256': manifest['transformation_code_sha256'],
        'adapter_sha256': sha(Path(__file__).read_bytes()),
        'original_job': original_job, 'original_job_sha256': manifest['input_files_sha256'][original_job],
        'original_error': entry['original_record']['error'], 'original_attempt_seconds': entry['original_attempt_seconds'],
        'ignored_ids': [row['id'] for row in entry['transformation'].get('ignored_rows', [])],
        'removed_fields': [{'id': item['id'], 'field': item['field'], 'field_sha256': item['field_sha256']} for item in entry['transformation'].get('removed_fields', [])], 'new_paid_calls': 0}


def candidate_record(bundle, accepted_sha, manifest, run):
    target = manifest['target']
    record = copy.deepcopy(manifest['jobs'][target]['original_record'])
    record.pop('error', None); record.pop('error_type', None)
    record.update(status='complete', output=f'outputs/{target}.md',
        output_sha256=manifest['target_output_sha256'], process=manifest['jobs'][target]['process'],
        recovery=annotation(bundle, accepted_sha, manifest, run))
    return record


def validate_recovered(h, job, record, plan, run, contexts, rt, bundle, accepted_sha):
    manifest = load_bundle(bundle, accepted_sha, run)
    recipe = RECIPES[manifest['target']]
    require(job['key'] == recipe.TARGET and record == candidate_record(bundle, accepted_sha, manifest, run),
            'Recovered completed record differs from reviewed proposal')
    require(plan['identity'] == proposal.IDENTITY and record['identity'] == plan['identity'] and record['job_sha256'] == h.digest(job),
            'Recovered job/plan identity differs')
    output = (run / record['output']).read_bytes()
    require(sha(output) == record['output_sha256'] == manifest['target_output_sha256'], 'Adopted output changed')
    calls = h.saved_calls(run, record)
    original = manifest['jobs'][recipe.TARGET]['original_record']
    result, error, transformation, _ = recipe.replay(h, rt, contexts[job['key']], calls, original, filtered=True)
    require(error is None and result.final_content.encode() == output and result.receipts() == record['process'],
            'Exact recovered replay differs')
    require(transformation == manifest['jobs'][recipe.TARGET]['transformation'], 'Applied row filter differs from reviewed transformation')
    return True


def install_adapter(h, bundle, accepted_sha, run):
    """Patch validation/report only; execute_job and all model calls remain original."""
    manifest = load_bundle(bundle, accepted_sha, run)
    recipe = RECIPES[manifest['target']]
    original_validate, original_report = h.validate_completed, h.report
    def validate(job, record, plan, folder, records, contexts, docs, rt):
        if job['key'] == recipe.TARGET and record.get('recovery'):
            require(folder.resolve() == run.resolve(), 'Recovery used in another run')
            return validate_recovered(h, job, record, plan, folder, contexts, rt, bundle, accepted_sha)
        return original_validate(job, record, plan, folder, records, contexts, docs, rt)
    def report(plan, folder, contexts, docs, rt):
        result = original_report(plan, folder, contexts, docs, rt)
        records = h.read_json(folder / 'results.json', {})
        recovered = records.get(recipe.TARGET, {}).get('recovery')
        result.setdefault('recovery_provenance', {}).update({recipe.TARGET: recovered} if recovered else {})
        historical = result.setdefault('historical_postprocess_failures', [])
        if not any(item['job'] == recipe.TARGET and item['attempt'] == recipe.ATTEMPT for item in historical):
            historical.append({'job': recipe.TARGET, 'attempt': recipe.ATTEMPT, 'error': recipe.EXPECTED_ERROR, 'new_paid_calls_for_recovery': 0})
        result['recovery_sensitivity'] = recovery_sensitivity(result['pairs'])
        caveat = 'Two generation pairs failed under frozen processing and depend on separately reviewed offline recoveries; the six-pair sensitivity analysis excludes both. Raw format failures remain part of the reliability result.'
        if caveat not in result['limitations']:
            result['limitations'].append(caveat)
        return result
    h.validate_completed, h.report = validate, report


@contextmanager
def campaign_lock(run):
    with (run.parent / 'heldout.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError('Campaign is active; adoption must wait for its lock') from exc
        yield


def require_idle(h, run):
    require(not any(r.get('status') == 'running' for r in h.read_json(run / 'results.json').values()), 'A generation/judge record is running')
    for path in run.glob('receipts/*/*/call-[0-9][0-9][0-9][0-9].json'):
        require(h.read_json(path).get('status') != 'running', 'An invocation is running')


def prepare_adoption(h, rt, run, bundle, accepted_sha):
    manifest = load_bundle(bundle, accepted_sha, run)
    recipe = RECIPES[manifest['target']]
    fresh, contexts, docs = h.build_plan(rt, ROOT / 'data/study/sources_ideas', ROOT / 'data/study/ideas_2026_09_05/374325c24e6b10a1')
    require(fresh == h.read_json(run / 'plan.json'), 'Exact frozen plan reconstruction differs')
    records_raw = (run / 'results.json').read_bytes(); records = json.loads(records_raw)
    expected = candidate_record(bundle, accepted_sha, manifest, run)
    current = records.get(recipe.TARGET, {})
    if current == expected:
        job = next(j for j in fresh['generations'] if j['key'] == recipe.TARGET)
        validate_recovered(h, job, current, fresh, run, contexts, rt, bundle, accepted_sha)
        return records_raw, records, expected, True
    require(current == manifest['jobs'][recipe.TARGET]['original_record'], 'Original failed result changed')
    require(not (run / expected['output']).exists(), 'Output exists while result is failed; explicit orphan-output review is required')
    for key in recipe.COMPARISONS:
        job = next(j for j in fresh['generations'] if j['key'] == key)
        require(records.get(key) == manifest['jobs'][key]['original_record'], 'Original completed comparison record changed')
        h.validate_completed(job, records[key], fresh, run, records, contexts, docs, rt)
    calls = h.saved_calls(run, current)
    result, error, evidence, _ = recipe.replay(h, rt, contexts[recipe.TARGET], calls, current, filtered=True)
    require(error is None and sha(result.final_content.encode()) == expected['output_sha256']
            and result.receipts() == expected['process'] and evidence == manifest['jobs'][recipe.TARGET]['transformation'],
            'Reviewed recovered artifact no longer reproduces')
    require((run / 'results.json').read_bytes() == records_raw, 'Results changed during adoption preparation; preview again')
    return records_raw, records, expected, False


def adopt(h, rt, run, bundle, accepted_sha):
    with campaign_lock(run):
        require_idle(h, run)
        before, records, expected, already = prepare_adoption(h, rt, run, bundle, accepted_sha)
        if already:
            return {'state': 'already_adopted', 'target': expected['key']}
        audit = bundle / 'adoptions' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
        audit.mkdir(parents=True, exist_ok=False)
        (audit / 'results.before.json').write_bytes(before)
        h.write_json(audit / 'candidate_record.json', expected)
        output = run / expected['output']; output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('xb') as handle:
            handle.write((bundle / 'recovered.md').read_bytes())
        require((run / 'results.json').read_bytes() == before, 'Concurrent results update; original failed result remains intact')
        records[expected['key']] = expected
        h.write_json(run / 'results.json', records)
        # Original failed job.json and numeric invocation receipts are never replaced or duplicated.
        receipt = {'state': 'adopted', 'target': expected['key'], 'manifest_sha256': accepted_sha,
            'results_before_sha256': sha(before), 'results_after_sha256': sha((run / 'results.json').read_bytes()),
            'output_sha256': expected['output_sha256'], 'original_failed_job_sha256': expected['recovery']['original_job_sha256'],
            'new_paid_calls': 0, 'invocation_receipts_changed': False}
        h.write_json(audit / 'adoption.json', receipt)
        return receipt


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True, action='append')
    parser.add_argument('--manifest-sha256', required=True, action='append')
    parser.add_argument('--run-dir', type=Path, default=ROOT / 'data/study/ideas_hegel_heldout_2026_09_05' / proposal.IDENTITY[:16])
    parser.add_argument('--phase', choices=('adopt', 'report', 'judge'), default='adopt')
    parser.add_argument('--adopt', action='store_true')
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--budget-usd', type=float)
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args(argv)
    require(not args.run or args.phase == 'judge', 'Only the explicit judge phase can run paid calls')
    require(not args.adopt or args.phase == 'adopt', '--adopt belongs only to adoption')
    require(args.run_dir.name == proposal.IDENTITY[:16], 'Unexpected run directory identity')
    from dotenv import load_dotenv
    load_dotenv(ROOT / '.env', override=False)
    if not (args.phase == 'judge' and args.run):
        def offline(event, arguments):
            if event in ('socket.connect', 'socket.getaddrinfo'):
                raise RuntimeError('Network is forbidden in adoption/report/preview')
        sys.addaudithook(offline)
    require(len(args.bundle) == len(args.manifest_sha256), 'Supply one approved hash per bundle, in matching order')
    pairs = list(zip(args.bundle, args.manifest_sha256))
    h = proposal.load_harness()
    manifests = [load_bundle(bundle, digest, args.run_dir) for bundle, digest in pairs]
    require(len({m['target'] for m in manifests}) == len(manifests), 'Duplicate recovery targets')
    if args.phase == 'adopt':
        results = []
        with h.frozen_runtime() as rt:
            for bundle, digest in pairs:
                if args.adopt:
                    result = adopt(h, rt, args.run_dir, bundle, digest)
                else:
                    _, _, record, already = prepare_adoption(h, rt, args.run_dir, bundle, digest)
                    result = {'state': 'already_adopted' if already else 'OFFLINE_ADOPTION_PREVIEW', 'target': record['key'],
                        'output_sha256': record['output_sha256'], 'original_failed_job_preserved': True,
                        'new_paid_calls': 0, 'must_wait_for_campaign_lock_before_adoption': True}
                results.append(result)
        print(json.dumps({'recoveries': results}, indent=2)); return 0
    for bundle, digest in pairs:
        install_adapter(h, bundle, digest, args.run_dir)
    forwarded = ['--phase', args.phase, '--output-root', str(args.run_dir.parent)]
    if args.run:
        require(args.budget_usd is not None, 'Explicit paid judge launch requires --budget-usd')
        forwarded += ['--run', '--budget-usd', str(args.budget_usd)]
    if args.require_complete:
        forwarded.append('--require-complete')
    return h.main(forwarded)


if __name__ == '__main__':
    raise SystemExit(main())
