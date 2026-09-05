"""Collect independent scores while preserving narrowly eligible syntax failures.

This wrapper never adopts a score or retries a failed logical invocation. Only a
complete, fully bound independent score whose sole defect fits the reviewed
one-brace rule may be deferred in an append-only pending manifest. The original
campaign budget, lock, source gate and fixed harness still execute every call.
Default is an offline report; paid collection requires --run --phase judge.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FIRST_PATH = ROOT / 'scripts/study_argument_family_score_recovery_2026_09_05.py'
FIRST_SHA = '442553a7a57ba1c466a14ddfcb9968a4ff0f2698ebda3a50e3f3877a203c14ea'
PENDING = Path('reader_notes/score_syntax_pending/pending.jsonl')


def load_first():
    import hashlib
    if hashlib.sha256(FIRST_PATH.read_bytes()).hexdigest() != FIRST_SHA:
        raise RuntimeError('First recovery wrapper changed')
    spec = importlib.util.spec_from_file_location('argument_score_first_recovery', FIRST_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pending_entries(run):
    path = run / PENDING
    if not path.exists():
        return {}
    entries = {}
    for line in path.read_text().splitlines():
        entry = json.loads(line)
        if entry['key'] in entries:
            raise RuntimeError('Duplicate pending syntax key')
        entries[entry['key']] = entry
    return entries


def one_brace(h, raw):
    """One exact delimiter, outside strings; strict schema after one insertion."""
    try:
        h.parse_score(raw.decode('utf-8'))
    except json.JSONDecodeError as exc:
        original_error = str(exc)
    else:
        raise RuntimeError('Only native JSONDecodeError is eligible for deferral')
    marker = b',"one_line":'
    h.require(raw.count(marker) == 1, 'One-brace rule requires one exact one_line delimiter')
    offset = raw.index(marker)
    quoted = escaped = False
    for byte in raw[:offset]:
        if escaped:
            escaped = False
        elif quoted and byte == ord('\\'):
            escaped = True
        elif byte == ord('"'):
            quoted = not quoted
    h.require(not quoted, 'Brace insertion would change quoted text')
    corrected = raw[:offset] + b'}' + raw[offset:]
    h.parse_score(corrected.decode('utf-8'))  # Exact eight fields, six numbers/reasons; no defaults.
    return corrected, offset, original_error


def candidate(first, h, job, record, plan, run, records, contexts, documents, rt):
    """Validate a pending candidate; no job/output writes or score acceptance."""
    h.require(plan['identity'] == first.IDENTITY and job in plan['judgments'] and job['kind'] == 'judge'
              and job.get('rater') in h.RATERS and 'reading' in job and not {'A', 'B'} & set(job),
              'Only a frozen independent score may be deferred')
    h.require(job['key'] != first.TARGET, 'First adopted recovery cannot be deferred or replaced')
    h.guard_inputs(plan)
    h.require(record.get('key') == job['key'] and record.get('kind') == 'judge' and record.get('identity') == plan['identity']
              and record.get('job_sha256') == h.digest(job) and record.get('status') == 'failed'
              and record.get('error_type') == 'JSONDecodeError' and record.get('invocations') == 1,
              'Only one saved failed JSON score invocation may be deferred')
    h.require('judgment' not in record and 'output' not in record and 'output_sha256' not in record
              and 'recovery' not in record, 'A pending syntax score cannot already contain accepted output')
    h.require(not (run / 'outputs' / (job['key'] + '.md')).exists(), 'Unexpected output for failed score')
    directory = run / 'receipts' / job['key'] / record['attempt']
    failed_raw = (directory / 'job.json').read_bytes()
    h.require(json.loads(failed_raw) == record, 'Failed job/results records differ')
    h.require(h.read_json(run / 'results.json').get(job['key']) == record, 'Failed live result differs')
    calls = h.saved_calls(run, record)
    h.require(len(calls) == 1, 'Exactly one saved score invocation is required')
    receipt, prompt, response = calls[0]
    parent = next(j for j in plan['generations'] if j['key'] == job['reading'])
    h.validate_completed(parent, records.get(parent['key'], {}), plan, run, records, contexts, documents, rt)
    h.require(record['inputs_sha256'] == {parent['key']: records[parent['key']]['output_sha256']}, 'Score parent binding differs')
    role = 'judge_' + job['rater']
    model = plan['models'][role]
    h.require(model == h.MODELS[role] and receipt.get('role') == role, 'Frozen scoring route differs')
    rt.h.validate_call((receipt, prompt, response['content']), h.judge_prompt(job, run, records, documents),
                       model, 'argument-family ' + job['key'])
    h.require(receipt['response_sha256'] == h.digest(response) and response.get('model_used') == model,
              'Response object/model differs')
    for field in ('input_tokens', 'output_tokens', 'retries'):
        h.require(type(response.get(field)) is int and response[field] >= 0 and response[field] == receipt.get(field),
                  'Unknown or inconsistent response usage/retries')
    for item in (receipt, response):
        h.require(not item.get('partial') and item.get('stop_reason') not in ('length', 'max_tokens', 'error')
                  and not item.get('error') and not item.get('connection_error'), 'Partial/error score is not deferrable')
    cost = receipt.get('cost_usd')
    h.require(type(cost) in (int, float) and math.isfinite(cost) and cost >= 0
              and cost == rt.core.estimate_cost(model, response['input_tokens'], response['output_tokens']),
              'Unknown or inconsistent invocation cost')
    raw = response['content'].encode('utf-8')
    corrected, offset, error = one_brace(h, raw)
    h.require(error == record['error'], 'Saved failure differs from native parser failure')
    return {'key': job['key'], 'attempt': record['attempt'], 'identity': plan['identity'],
            'state': 'pending_independent_review_not_adopted', 'harness_sha256': first.HARNESS_SHA,
            'first_wrapper_sha256': FIRST_SHA, 'collector_sha256': first.sha(Path(__file__).read_bytes()),
            'failed_job_sha256': first.sha(failed_raw), 'failed_record': record,
            'failed_job_snapshot': str(PENDING.parent / job['key'] / record['attempt'] / 'job.failed.json'),
            'raw_sha256': first.sha(raw), 'corrected_sha256': first.sha(corrected), 'insert_byte': offset,
            'rule': 'Insert exactly one closing brace before the unique unquoted comma-one_line delimiter; strict complete score schema must then pass.',
            'prompt_sha256': receipt['prompt_sha256'], 'inputs_sha256': record['inputs_sha256'],
            'model': model, 'input_tokens': response['input_tokens'], 'output_tokens': response['output_tokens'],
            'cost_usd': cost, 'backend_retries': response['retries'], 'new_paid_calls_for_deferral': 0,
            'accepted_output_created': False, 'invocation_files_sha256': record['invocation_files_sha256']}


def defer(first, h, job, record, plan, run, records, contexts, documents, rt):
    entry = candidate(first, h, job, record, plan, run, records, contexts, documents, rt)
    previous = pending_entries(run).get(job['key'])
    snapshot = run / entry['failed_job_snapshot']
    if previous is not None:
        h.require(previous == entry, 'Previously deferred score bindings changed')
        first.pinned(snapshot, entry['failed_job_sha256'])
        return False
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    raw = (run / 'receipts' / job['key'] / record['attempt'] / 'job.json').read_bytes()
    if snapshot.exists():
        first.pinned(snapshot, entry['failed_job_sha256'])
    else:
        with snapshot.open('xb') as handle:
            handle.write(raw)
    # The unchanged harness holds campaign.lock throughout execute_job. Append
    # one durable line; a truncated/invalid manifest fails closed on continuation.
    with (run / PENDING).open('a') as handle:
        handle.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + '\n')
        handle.flush()
        os.fsync(handle.fileno())
    return False  # The score remains failed, never validated/complete.


def install_collection(first, h):
    execute = h.execute_job
    report = h.report
    review_gate = h.review_gate

    def execute_collect(job, plan, run, records, contexts, documents, output_root, cap, rt):
        if job['kind'] == 'judge' and records.get(job['key'], {}).get('status') == 'failed':
            return defer(first, h, job, records[job['key']], plan, run, records, contexts, documents, rt)
        try:
            return execute(job, plan, run, records, contexts, documents, output_root, cap, rt)
        except json.JSONDecodeError:
            if job['kind'] != 'judge':
                raise
            return defer(first, h, job, records.get(job['key'], {}), plan, run, records, contexts, documents, rt)

    def report_collect(plan, run, records, contexts, documents, rt):
        result = report(plan, run, records, contexts, documents, rt)
        entries = validate_pending(first, h, plan, run, records, contexts, documents, rt)
        result['pending_score_syntax'] = {'count': len(entries), 'keys': list(entries),
            'accepted': 0, 'new_paid_calls_for_deferral': 0,
            'limit': 'Pending entries remain failed and excluded from score comparisons; separate reviewed adoption is required.'}
        return result

    def review_collect(path, phase, plan, run, records, contexts, documents, rt):
        # Called once under the original campaign lock before its job loop.
        # Preserve the original source-review gate, then audit every pending
        # entry before any remaining independent job can invoke a model.
        result = review_gate(path, phase, plan, run, records, contexts, documents, rt)
        validate_pending(first, h, plan, run, records, contexts, documents, rt)
        return result

    h.execute_job = execute_collect
    h.report = report_collect
    h.review_gate = review_collect


def validate_pending(first, h, plan, run, records, contexts, documents, rt):
    entries = pending_entries(run)
    jobs = {j['key']: j for j in plan['judgments']}
    h.require(set(entries) <= set(jobs) and set(entries) <= set(records), 'Unknown pending syntax key')
    for key, entry in entries.items():
        h.require(candidate(first, h, jobs[key], records[key], plan, run, records, contexts, documents, rt) == entry,
                  'Pending manifest no longer matches the failed score')
        first.pinned(run / entry['failed_job_snapshot'], entry['failed_job_sha256'])
    return entries


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--adopt', action='store_true')
    parser.add_argument('--phase', default='report')
    args, _ = parser.parse_known_args(argv)
    if args.adopt or args.phase not in ('judge', 'report') or args.run and args.phase != 'judge':
        raise RuntimeError('Collection supports offline report or explicit --run --phase judge; it cannot adopt')
    first = load_first()
    load = first.load_harness
    def load_collect():
        h = load()
        install_collection(first, h)
        return h
    first.load_harness = load_collect
    if '--phase' not in argv and not any(arg.startswith('--phase=') for arg in argv):
        argv += ['--phase', args.phase]
    return first.main(argv)


if __name__ == '__main__':
    raise SystemExit(main())
