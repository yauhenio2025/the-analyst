"""One reviewed score syntax recovery; default is an offline adoption preview.

--adopt snapshots the failed state before publishing one derived score. All call
files remain unchanged. --phase report is offline; --run --phase judge delegates
the original arguments, budget, lock and review gate to the exact frozen harness.
An interrupted adoption requires explicit review, never an automatic paid retry.
"""
from __future__ import annotations

import argparse
import copy
from contextlib import contextmanager
import fcntl
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / 'scripts/study_argument_family_2026_09_05.py'
HARNESS_SHA = 'f7f13874ca09356fdd6a71a18af8a4e89a8dc7e2dbc4eb41df559855393a6d88'
IDENTITY = '530df62823ec1915b1a4a48472d4b59782e6017f92f9d5496a8c645c5836ad16'
TARGET = 'score__sol__dialectical_structure__candidate__zambrana'
ATTEMPT = '725009567849'
RAW_SHA = 'ac18ed1c0137b0ee6e55599c8175a8e32bee650aae85ebec5f105e0055f8fb4e'
REPAIRED_SHA = '29a32930e0af258f16fa4a7129e8862d9142c10488a273094eac4f080cbb4d2e'
INSERT_BYTE = 2049
SCORES = (9, 8, 8, 7, 9, 8)
PLAN_SHA = '3a92d1c6f816ceb6b2f9f45d964941dbc1450d534960b71088c6024095d331e6'
RESULTS_SHA = '3d52ccef94117126858a8e023794c114ad246cfaa4f38536bed4bc3823139eb5'
FAILED_JOB_SHA = '90094ea0112806ffbc8b0e4621f7d31aad017d41ccad0e34586c58e92f5c1de6'
LOG_SHA = '1aa749a70dda2fc1a703670d4fca4d52abe4dd59c718086e1f6dcfcdf151382d'
CALL_HASHES = {
    'call-0001.json': 'cd61149cb93abc8a7cc5ae880e36c35a1ab7223ccc2cddca91ff04e92c50ce37',
    'call-0001.md': RAW_SHA,
    'call-0001.prompt.json': '5b4f95d36ba624087854679e78fd76bfcfcded08d4fba1e6022260825523a85b',
    'call-0001.response.json': 'ca4e65f1aa5255c93ee1b6136b93ddf17989f43142f08e7bf6b6613adefec46b',
}
RUN = ROOT / 'data/study/argument_family_2026_09_05' / IDENTITY[:16]
LOG = ROOT / 'data/study/argument_family_preparation_2026_09_05/judge.log'
BUNDLE = Path('reader_notes/score_recovery/adoption')
OUTPUT = Path('outputs') / f'{TARGET}.md'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pinned(path, expected):
    raw = path.read_bytes()
    require(sha(raw) == expected, f'Pinned bytes changed: {path}')
    return raw


def load_harness():
    pinned(HARNESS, HARNESS_SHA)
    spec = importlib.util.spec_from_file_location('argument_family_frozen_score_recovery', HARNESS)
    harness = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(harness)
    return harness


def repair(raw):
    require(sha(raw) == RAW_SHA, 'Not the reviewed malformed score')
    require(raw[INSERT_BYTE:INSERT_BYTE + 11] == b',"one_line"', 'Insertion boundary changed')
    fixed = raw[:INSERT_BYTE] + b'}' + raw[INSERT_BYTE:]
    require(sha(fixed) == REPAIRED_SHA, 'Repaired score hash changed')
    return fixed


def recover_known(h, raw, *, strict=None):
    """Explicit offline operation; this does not replace the fresh-call parser."""
    value = (strict or h.parse_score)(repair(raw.encode('utf-8')).decode('utf-8'))
    require(tuple(value[k] for k in h.RUBRIC_KEYS) == SCORES, 'Reviewed numeric scores changed')
    return value


def attempt(run):
    return run / 'receipts' / TARGET / ATTEMPT


def validate_calls(h, run, record):
    paths = {p.name for p in attempt(run).glob('call-*') if p.is_file()}
    require(paths == set(CALL_HASHES), 'Known invocation file inventory differs')
    for name, expected in CALL_HASHES.items():
        pinned(attempt(run) / name, expected)
    return h.saved_calls(run, record)


def validate_adopted(h, run, record):
    """Provenance supplement; the original harness still performs full replay."""
    bundle = run / BUNDLE
    metadata = record.get('recovery', {})
    manifest_raw = pinned(bundle / 'manifest.json', metadata.get('manifest_sha256'))
    manifest = json.loads(manifest_raw)
    fixed = {'identity': IDENTITY, 'target': TARGET, 'attempt': ATTEMPT, 'harness_sha256': HARNESS_SHA,
             'wrapper_sha256': sha(Path(__file__).read_bytes()), 'raw_sha256': RAW_SHA,
             'repaired_raw_sha256': REPAIRED_SHA, 'insert_byte': INSERT_BYTE,
             'validated_generations': 24, 'validated_native_scores': 11, 'new_paid_calls': 0}
    require(set(manifest) == set(fixed) | {'files_sha256'} and all(manifest[k] == v for k, v in fixed.items()),
            'Recovery manifest facts differ')
    expected_files = {'results.failed.json', 'job.failed.json', 'judge.failed.log', 'plan.json',
                      'wrapper.py', 'repaired.raw.json', 'score.json'} | {f'original_attempt/{name}' for name in CALL_HASHES}
    require(set(manifest['files_sha256']) == expected_files, 'Recovery snapshot inventory differs')
    for name, expected in manifest['files_sha256'].items():
        pinned(bundle / name, expected)
    original = json.loads(pinned(bundle / 'job.failed.json', FAILED_JOB_SHA))
    before = json.loads(pinned(bundle / 'results.failed.json', RESULTS_SHA))
    require(before[TARGET] == original, 'Original failed records differ')
    pinned(bundle / 'judge.failed.log', LOG_SHA)
    pinned(bundle / 'plan.json', PLAN_SHA)
    pinned(bundle / 'repaired.raw.json', REPAIRED_SHA)
    require((bundle / 'wrapper.py').read_bytes() == Path(__file__).read_bytes(), 'Wrapper snapshot changed')
    for name, expected in CALL_HASHES.items():
        pinned(bundle / 'original_attempt' / name, expected)
    validate_calls(h, run, record)
    judgment = recover_known(h, (attempt(run) / 'call-0001.md').read_text())
    expected = candidate_record(h, original, judgment, sha(manifest_raw))
    require(record == expected, 'Adopted record differs from exact derived record')
    require(h.read_json(attempt(run) / 'job.json') == record, 'Adopted job/results records differ')
    require((run / OUTPUT).read_bytes() == (bundle / 'score.json').read_bytes()
            == score_bytes(judgment), 'Derived score bytes changed')
    return True


def install_reporting(h):
    validate = h.validate_completed
    report = h.report
    strict = h.parse_score

    def validate_with_provenance(job, record, plan, run, records, contexts, documents, rt):
        previous = h.parse_score
        h.parse_score = strict
        try:
            if job['key'] == TARGET and record.get('status') == 'complete':
                validate_adopted(h, run, record)
                # Sequential harness only: permit the repair during this pinned
                # completed target's replay. Nested/non-target validations reset
                # to strict; fresh execute_job calls never enter this context.
                h.parse_score = lambda raw: recover_known(h, raw, strict=strict) if sha(raw.encode()) == RAW_SHA else strict(raw)
            return validate(job, record, plan, run, records, contexts, documents, rt)
        finally:
            h.parse_score = previous

    def report_with_recovery(plan, run, records, contexts, documents, rt):
        result = report(plan, run, records, contexts, documents, rt)
        recovered = int(records.get(TARGET, {}).get('status') == 'complete'
                        and TARGET not in result['validation_errors'])
        result['score_recovery'] = {
            'valid_recovered_scores': recovered,
            'valid_native_scores': result['valid_judgments'] - recovered,
            'recovered_keys': [TARGET] if recovered else [],
            'method': 'One pinned response receives one closing brace; no score or reason text changes.',
            'new_paid_calls_for_recovery': 0,
            'original_failure_preserved': str(BUNDLE / 'job.failed.json') if recovered else None,
        }
        return result

    h.validate_completed = validate_with_provenance
    h.report = report_with_recovery


def score_bytes(judgment):
    return json.dumps(judgment, ensure_ascii=False, indent=2).encode('utf-8')


def candidate_record(h, original, judgment, manifest_sha):
    record = copy.deepcopy(original)
    record.pop('error', None)
    record.pop('error_type', None)
    record.update(status='complete', judgment=judgment, output=str(OUTPUT),
                  output_sha256=sha(score_bytes(judgment)), recovery={
                      'method': 'exact_sha256_single_closing_brace',
                      'manifest': str(BUNDLE / 'manifest.json'), 'manifest_sha256': manifest_sha,
                      'original_failed_job_sha256': FAILED_JOB_SHA,
                      'original_raw_sha256': RAW_SHA, 'repaired_raw_sha256': REPAIRED_SHA,
                      'insert_byte': INSERT_BYTE, 'new_paid_calls': 0})
    return record


def prepare(h, rt, run, log):
    require(run.name == IDENTITY[:16], 'Unexpected campaign directory')
    pinned(run / 'plan.json', PLAN_SHA)
    plan, contexts, documents = h.build_plan(
        rt, ROOT / 'data/study/sources_ideas', ROOT / 'data/study/ideas_2026_09_05/374325c24e6b10a1',
        ROOT / h.CONTROL_PATH, ROOT / h.CANDIDATE_PATH)
    require(plan['identity'] == IDENTITY and h.read_json(run / 'plan.json') == plan, 'Frozen plan replay differs')
    h.guard_inputs(plan)
    h.validate_saved_campaign(run.parent, plan)
    records_raw = (run / 'results.json').read_bytes()
    records = json.loads(records_raw)
    require(all(r.get('status') != 'running' for r in records.values()), 'A logical job is running')
    for path in h.receipt_paths(run.parent):
        require(h.read_json(path).get('status') == 'complete', 'An invocation is not complete')
    original = records[TARGET]
    already = original.get('status') == 'complete'
    if already:
        validate_adopted(h, run, original)
    else:
        require(sha(records_raw) == RESULTS_SHA, 'Original campaign results changed')
        require(h.read_json(attempt(run) / 'job.json') == original, 'Failed job/results records differ')
        pinned(attempt(run) / 'job.json', FAILED_JOB_SHA)
        pinned(log, LOG_SHA)
        require(original['status'] == 'failed' and original['error_type'] == 'JSONDecodeError'
                and original['attempt'] == ATTEMPT and original['identity'] == IDENTITY,
                'Unexpected failed job')
        require(not (run / OUTPUT).exists() and not (run / BUNDLE).exists(), 'Adoption artifacts already exist; review interrupted adoption')
        require(sum(r['kind'] == 'generation' and r['status'] == 'complete' for r in records.values()) == 24
                and sum(r['kind'] == 'judge' and r['status'] == 'complete' for r in records.values()) == 11
                and len(records) == 36, 'Expected exactly24 generations,11 native scores and the known failure')
    for job in h.all_jobs(plan):
        if records.get(job['key'], {}).get('status') == 'complete':
            h.validate_completed(job, records[job['key']], plan, run, records, contexts, documents, rt)
    job = next(j for j in plan['judgments'] if j['key'] == TARGET)
    require(original['job_sha256'] == h.digest(job), 'Known scoring job changed')
    require(original['inputs_sha256'] == {job['reading']: records[job['reading']]['output_sha256']}, 'Scored analysis binding changed')
    calls = validate_calls(h, run, original)
    require(len(calls) == 1, 'Known score must have exactly one invocation')
    receipt, prompt, response = calls[0]
    rt.h.validate_call((receipt, prompt, response['content']), h.judge_prompt(job, run, records, documents),
                       h.MODELS['judge_sol'], 'argument-family ' + TARGET)
    require(receipt['response_sha256'] == h.digest(response), 'Response object hash changed')
    require(receipt['input_tokens'] == response['input_tokens'] == 17274
            and receipt['output_tokens'] == response['output_tokens'] == 566
            and receipt['retries'] == response['retries'] == 0
            and receipt['cost_usd'] == rt.core.estimate_cost(h.MODELS['judge_sol'], 17274, 566) == 0.040208,
            'Known usage/cost changed')
    judgment = recover_known(h, response['content'])
    require((run / 'results.json').read_bytes() == records_raw, 'Results changed during replay')
    return records_raw, records, judgment, already


@contextmanager
def campaign_lock(run):
    # This is the exact lock used by the frozen harness, not a recovery-only lock.
    with (run.parent / 'campaign.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError('Campaign is active; recovery must wait') from exc
        yield


def adopt(h, rt, run, log):
    with campaign_lock(run):
        before, records, judgment, already = prepare(h, rt, run, log)
        if already:
            return {'state': 'already_adopted', 'target': TARGET, 'new_paid_calls': 0}
        bundle = run / BUNDLE
        bundle.mkdir(parents=True, exist_ok=False)
        snapshots = {'results.failed.json': before, 'job.failed.json': pinned(attempt(run) / 'job.json', FAILED_JOB_SHA),
                     'judge.failed.log': pinned(log, LOG_SHA), 'plan.json': pinned(run / 'plan.json', PLAN_SHA),
                     'wrapper.py': Path(__file__).read_bytes(), 'repaired.raw.json': repair((attempt(run) / 'call-0001.md').read_bytes()),
                     'score.json': score_bytes(judgment)}
        snapshots.update({f'original_attempt/{name}': pinned(attempt(run) / name, expected) for name, expected in CALL_HASHES.items()})
        for name, raw in snapshots.items():
            path = bundle / name
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as handle:
                handle.write(raw)
        manifest = {'identity': IDENTITY, 'target': TARGET, 'attempt': ATTEMPT, 'harness_sha256': HARNESS_SHA,
                    'wrapper_sha256': sha(snapshots['wrapper.py']), 'raw_sha256': RAW_SHA,
                    'repaired_raw_sha256': REPAIRED_SHA, 'insert_byte': INSERT_BYTE,
                    'validated_generations': 24, 'validated_native_scores': 11, 'new_paid_calls': 0,
                    'files_sha256': {name: sha(raw) for name, raw in snapshots.items()}}
        h.write_json(bundle / 'manifest.json', manifest)
        record = candidate_record(h, records[TARGET], judgment, sha((bundle / 'manifest.json').read_bytes()))
        require((run / 'results.json').read_bytes() == before, 'Concurrent results update; adoption refused')
        with (run / OUTPUT).open('xb') as handle:
            handle.write(score_bytes(judgment))
        # Both original records are preserved above before either active record changes.
        records[TARGET] = record
        h.write_json(attempt(run) / 'job.json', record)
        h.write_json(run / 'results.json', records)
        validate_adopted(h, run, record)
        return {'state': 'adopted', 'target': TARGET, 'manifest_sha256': record['recovery']['manifest_sha256'],
                'valid_native_scores': 11, 'valid_recovered_scores': 1, 'new_paid_calls': 0}


def offline(event, arguments):
    if event in ('socket.connect', 'socket.getaddrinfo'):
        raise RuntimeError('Network is forbidden in score recovery preview/adoption/report')


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser.add_argument('--adopt', action='store_true')
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--phase', default='adopt')
    parser.add_argument('--output-root', type=Path, default=RUN.parent)
    args, remaining = parser.parse_known_args(argv)
    require(args.phase in ('adopt', 'judge', 'report'), 'Recovery wrapper supports only adopt/judge/report')
    require(not args.adopt or args.phase == 'adopt', '--adopt is only valid in the adoption phase')
    require(not args.run or args.phase == 'judge', 'Only explicit --run --phase judge may invoke providers')
    require(args.output_root.resolve() == RUN.parent.resolve(), 'Recovery is bound to the original campaign root')
    if not args.run:
        sys.addaudithook(offline)
    h = load_harness()
    install_reporting(h)
    if args.phase == 'adopt':
        require(not remaining, 'Adoption takes no campaign/source overrides')
        from dotenv import load_dotenv
        load_dotenv(ROOT / '.env', override=False)
        with h.frozen_runtime() as rt:
            if args.adopt:
                result = adopt(h, rt, RUN, LOG)
            else:
                _, _, judgment, already = prepare(h, rt, RUN, LOG)
                result = {'state': 'already_adopted' if already else 'OFFLINE_ADOPTION_PREVIEW',
                          'target': TARGET, 'output_sha256': sha(score_bytes(judgment)), 'new_paid_calls': 0}
        print(json.dumps(result, indent=2))
        return 0
    # Require adoption before any resumed scoring; no incomplete logical job is retried.
    record = h.read_json(RUN / 'results.json')[TARGET]
    require(record.get('status') == 'complete', 'Reviewed offline adoption must precede report/resume')
    validate_adopted(h, RUN, record)
    return h.main(argv)


if __name__ == '__main__':
    raise SystemExit(main())
