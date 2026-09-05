"""Offline final adoption/report for an exact, independently reviewed score list.

Default previews --approval JSON; --adopt publishes only that list after all 48
score calls. --phase report validates native, first-recovered and batch-recovered
scores separately. No paid entry point or retry exists. Interrupted adoption
fails closed: preserve the bundle and review partial publication manually; never
rerun a model or discard the preserved failed records to recover a crash.

Approval schema is enforced below. Paths in repairs are relative to the campaign;
review_files paths are absolute. Offsets address original UTF-8 bytes. Allowed
insertions are only } before the unique comma/JSON-whitespace/"one_line"/colon
boundary (preserving its whitespace), or a backslash
before an existing ASCII quote. Every corrected artifact needs human review.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COLLECTOR_PATH = ROOT / 'scripts/study_argument_family_collect_manual_scores_2026_09_05.py'
COLLECTOR_SHA = 'b6ae90a9bb203e7980ecd55ad49c1eefbfd5e3a1d55bcb709b545c46c2ea3078'
BUNDLE = Path('reader_notes/score_syntax_batch/adoption')
APPROVAL_FIELDS = {'identity', 'decision', 'results_sha256', 'pending_sha256', 'adapter_sha256',
                   'collector_sha256', 'first_wrapper_sha256', 'review_files', 'repairs'}
REPAIR_FIELDS = {'key', 'attempt', 'failed_job_sha256', 'raw_sha256', 'corrected_sha256', 'corrected_path', 'edits'}


def load_dependencies():
    import hashlib
    if hashlib.sha256(COLLECTOR_PATH.read_bytes()).hexdigest() != COLLECTOR_SHA:
        raise RuntimeError('Manual collection adapter changed')
    spec = importlib.util.spec_from_file_location('argument_score_manual_collection', COLLECTOR_PATH)
    manual = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(manual)
    collector = manual.load_collector()
    manual.install_manual(collector)
    first = collector.load_first()
    return collector, first


def local(run, name):
    path = Path(name)
    if path.is_absolute() or '..' in path.parts or path.as_posix() != name:
        raise RuntimeError('Expected a canonical campaign-relative artifact path')
    target = run / path
    if not target.resolve().is_relative_to(run.resolve()):
        raise RuntimeError('Artifact escapes campaign')
    return target


def reviewed_repair(first, h, raw, item):
    first.require(first.sha(raw) == item['raw_sha256'], 'Reviewed raw score changed')
    try:
        h.parse_score(raw.decode())
    except json.JSONDecodeError:
        pass
    else:
        raise RuntimeError('Only a native JSON syntax failure may be repaired')
    edits = item['edits']
    first.require(isinstance(edits, list) and 0 < len(edits) <= 20, 'Expected a bounded explicit insertion list')
    previous = -1
    pieces = []
    cursor = 0
    for edit in edits:
        first.require(set(edit) == {'offset', 'insert'} and type(edit['offset']) is int,
                      'Only explicit byte-offset insertions are allowed')
        offset, insertion = edit['offset'], edit['insert']
        first.require(previous < offset <= len(raw) and insertion in ('}', '\\'), 'Insertion order/type differs')
        if insertion == '}':
            boundaries = list(re.finditer(rb',[ \t\r\n]*"one_line"[ \t\r\n]*:', raw))
            first.require(len(boundaries) == 1 and boundaries[0].start() == offset,
                          'Closing brace is limited to the unique one_line delimiter')
            quoted = escaped = False
            for byte in raw[:offset]:
                if escaped:
                    escaped = False
                elif quoted and byte == ord('\\'):
                    escaped = True
                elif byte == ord('"'):
                    quoted = not quoted
            first.require(not quoted, 'Closing brace cannot be inserted inside quoted text')
        else:
            first.require(raw[offset:offset + 1] == b'"', 'Backslash must precede an existing ASCII quote')
        pieces.extend((raw[cursor:offset], insertion.encode()))
        cursor = previous = offset
    fixed = b''.join(pieces) + raw[cursor:]
    first.require(first.sha(fixed) == item['corrected_sha256'], 'Reviewed corrected score changed')
    return fixed, h.parse_score(fixed.decode())


def validate_approval(first, approval):
    first.require(set(approval) == APPROVAL_FIELDS and approval['identity'] == first.IDENTITY
                  and approval['decision'] == 'adopt_reviewed_exact_scores'
                  and approval['adapter_sha256'] == first.sha(Path(__file__).read_bytes())
                  and approval['collector_sha256'] == COLLECTOR_SHA
                  and approval['first_wrapper_sha256'] == first.sha(Path(first.__file__).read_bytes()),
                  'Approval identity, code pins or decision differs')
    items = approval['repairs']
    first.require(isinstance(items, list) and items and all(set(i) == REPAIR_FIELDS for i in items)
                  and len({i['key'] for i in items}) == len(items)
                  and first.TARGET not in {i['key'] for i in items}, 'Review list differs or replaces first recovery')
    files = approval['review_files']
    first.require(isinstance(files, dict) and files and all(Path(p).is_absolute() for p in files)
                  and any(p.endswith('.log') for p in files) and any(p.endswith('.md') for p in files),
                  'Approval must pin the human review memo and original logs')
    return {i['key']: i for i in items}


def candidate_record(first, original, judgment, item, manifest_sha):
    result = copy.deepcopy(original)
    result.pop('error', None)
    result.pop('error_type', None)
    result.update(status='complete', judgment=judgment, output='outputs/' + item['key'] + '.md',
                  output_sha256=first.sha(first.score_bytes(judgment)), recovery={
                      'method': 'reviewed_exact_score_syntax_insertions', 'manifest': str(BUNDLE / 'manifest.json'),
                      'manifest_sha256': manifest_sha, 'original_failed_job_sha256': item['failed_job_sha256'],
                      'original_raw_sha256': item['raw_sha256'], 'corrected_raw_sha256': item['corrected_sha256'],
                      'edits': item['edits'], 'new_paid_calls': 0})
    return result


def expected_files(first, collector, approval, entries):
    names = {'approval.json', 'pending.jsonl', 'results.failed.json', 'plan.json', 'adapter.py',
             'collector.py', 'one_brace_collector.py', 'first_wrapper.py'}
    names.update('review/' + str(i) for i, _ in enumerate(sorted(approval['review_files'])))
    for key, entry in entries.items():
        names.update({key + '/job.failed.json', key + '/corrected.raw.json', key + '/score.json'})
        names.update(key + '/calls/' + Path(p).name for p in entry['invocation_files_sha256'])
    return names


def validate_bundle(first, collector, h, run, record):
    """Validate immutable original evidence and exact derived record before replay."""
    bundle = run / BUNDLE
    raw = first.pinned(bundle / 'manifest.json', record.get('recovery', {}).get('manifest_sha256'))
    manifest = json.loads(raw)
    approval = json.loads((bundle / 'approval.json').read_bytes())
    items = validate_approval(first, approval)
    pending_raw = first.pinned(bundle / 'pending.jsonl', approval['pending_sha256'])
    entries = {e['key']: e for e in map(json.loads, pending_raw.decode().splitlines())}
    first.require(len(entries) == len(pending_raw.decode().splitlines()) and set(entries) == set(items), 'Pending snapshot/list differs')
    facts = {'identity': first.IDENTITY, 'adapter_sha256': approval['adapter_sha256'],
             'approval_sha256': first.sha((bundle / 'approval.json').read_bytes()), 'new_paid_calls': 0,
             'validated_generations': 24, 'validated_first_recovered_scores': 1,
             'validated_native_scores': 47 - len(items), 'batch_keys': sorted(items)}
    first.require(set(manifest) == set(facts) | {'files_sha256'}
                  and all(manifest[k] == v for k, v in facts.items())
                  and set(manifest['files_sha256']) == expected_files(first, collector, approval, entries),
                  'Batch manifest facts or inventory differs')
    for name, expected in manifest['files_sha256'].items():
        first.pinned(local(bundle, name), expected)
    first.pinned(bundle / 'plan.json', first.PLAN_SHA)
    first.require((bundle / 'adapter.py').read_bytes() == Path(__file__).read_bytes()
                  and (bundle / 'collector.py').read_bytes() == COLLECTOR_PATH.read_bytes()
                  and (bundle / 'one_brace_collector.py').read_bytes() == Path(collector.__file__).read_bytes()
                  and (bundle / 'first_wrapper.py').read_bytes() == Path(first.__file__).read_bytes(), 'Code snapshot differs')
    for i, (path, expected) in enumerate(sorted(approval['review_files'].items())):
        first.pinned(bundle / 'review' / str(i), expected)
    before = json.loads(first.pinned(bundle / 'results.failed.json', approval['results_sha256']))
    key = record['key']
    first.require(key in items, 'Unknown batch recovery key')
    item, entry = items[key], entries[key]
    original = json.loads(first.pinned(bundle / key / 'job.failed.json', item['failed_job_sha256']))
    first.require(original == before[key] == entry['failed_record'] and original['attempt'] == item['attempt']
                  and original['status'] == 'failed' and original['error_type'] == 'JSONDecodeError'
                  and entry['raw_sha256'] == item['raw_sha256']
                  and entry['failed_job_sha256'] == item['failed_job_sha256'], 'Original failed bindings differ')
    for path, expected in entry['invocation_files_sha256'].items():
        first.pinned(local(run, path), expected)
        first.pinned(bundle / key / 'calls' / Path(path).name, expected)
    raw_score = (run / 'receipts' / key / item['attempt'] / 'call-0001.md').read_bytes()
    fixed, judgment = reviewed_repair(first, h, raw_score, item)
    first.require((bundle / key / 'corrected.raw.json').read_bytes() == fixed
                  and (bundle / key / 'score.json').read_bytes() == first.score_bytes(judgment), 'Derived snapshot differs')
    first.require(record == candidate_record(first, original, judgment, item, first.sha(raw)), 'Derived record differs')
    return item, fixed


def install_reporting(first, collector, h):
    native_validate, strict = h.validate_completed, h.parse_score
    first.install_reporting(h)
    ordinary_validate, ordinary_report = h.validate_completed, h.report

    def validate(job, record, plan, run, records, contexts, documents, rt):
        previous = h.parse_score
        h.parse_score = strict
        try:
            if record.get('recovery', {}).get('method') == 'reviewed_exact_score_syntax_insertions':
                first.require(job['kind'] == 'judge' and job['key'] == record['key'], 'Recovery cannot change job kind/key')
                item, fixed = validate_bundle(first, collector, h, run, record)
                h.parse_score = lambda raw: strict(fixed.decode()) if first.sha(raw.encode()) == item['raw_sha256'] else strict(raw)
                return native_validate(job, record, plan, run, records, contexts, documents, rt)
            return ordinary_validate(job, record, plan, run, records, contexts, documents, rt)
        finally:
            h.parse_score = previous

    def report(plan, run, records, contexts, documents, rt):
        planned = {j['key'] for j in plan['generations'] + plan['judgments']}
        first.require(set(records) <= planned, 'Unexpected record outside the fixed generation/score matrix')
        result = ordinary_report(plan, run, records, contexts, documents, rt)
        batch_keys = [j['key'] for j in plan['judgments']
                      if records.get(j['key'], {}).get('recovery', {}).get('method') == 'reviewed_exact_score_syntax_insertions']
        recovered = [k for k in batch_keys if records[k].get('status') == 'complete' and k not in result['validation_errors']]
        first_count = result['score_recovery']['valid_recovered_scores']
        result['score_recovery'].update(valid_native_scores=result['valid_judgments'] - first_count - len(recovered),
            valid_first_recovered_scores=first_count, valid_batch_recovered_scores=len(recovered),
            valid_recovered_scores=first_count + len(recovered),
            recovered_keys=result['score_recovery']['recovered_keys'] + sorted(recovered),
            batch_manifest=str(BUNDLE / 'manifest.json'),
            method='First pinned brace recovery plus separately reviewed exact batch syntax insertions.',
            historical_parser_failures_preserved=1 + len(batch_keys),
            limit='Syntax-derived scores preserve reviewed wording; original parser failures remain historical failures. No new calls or inferred scores.')
        return result

    h.validate_completed, h.report = validate, report


def prepare(first, collector, h, rt, run, approval_path):
    first.require(not (run / BUNDLE).exists(), 'Batch bundle already exists; use report or review interrupted adoption')
    approval_raw = approval_path.read_bytes()
    approval = json.loads(approval_raw)
    items = validate_approval(first, approval)
    first.pinned(run / 'plan.json', first.PLAN_SHA)
    plan, contexts, documents = h.build_plan(rt, ROOT / 'data/study/sources_ideas',
        ROOT / 'data/study/ideas_2026_09_05/374325c24e6b10a1', ROOT / h.CONTROL_PATH, ROOT / h.CANDIDATE_PATH)
    first.require(plan['identity'] == first.IDENTITY and h.read_json(run / 'plan.json') == plan, 'Frozen plan changed')
    h.guard_inputs(plan)
    h.validate_saved_campaign(run.parent, plan)
    h.budget_guard(run.parent, h.CAP_USD, 0)  # Known costs only; no admission or invocation.
    before = first.pinned(run / 'results.json', approval['results_sha256'])
    records = json.loads(before)
    jobs = plan['generations'] + plan['judgments']
    first.require(len(plan['generations']) == 24 and len(plan['judgments']) == 48
                  and set(records) == {j['key'] for j in jobs}, 'All 24 generations and 48 independent scores must be collected')
    first.require(all(records[j['key']]['status'] == 'complete' for j in plan['generations'])
                  and records[first.TARGET]['status'] == 'complete'
                  and {k for k, r in records.items() if r['status'] != 'complete'} == set(items), 'Only the reviewed scores may remain failed')
    for job in jobs:
        if records[job['key']]['status'] == 'complete':
            h.validate_completed(job, records[job['key']], plan, run, records, contexts, documents, rt)
        if job['kind'] == 'judge':
            first.require(records[job['key']]['invocations'] == 1, 'Scores must retain exactly one logical call')
            first.require(len(list((run / 'receipts' / job['key']).glob('*/call-[0-9][0-9][0-9][0-9].json'))) == 1,
                          'Additional score attempt found')
    pending = first.pinned(run / collector.PENDING, approval['pending_sha256'])
    entries = collector.validate_pending(first, h, plan, run, records, contexts, documents, rt)
    first.require(set(entries) == set(items), 'Review list must exactly equal pending failures')
    snapshots = {'approval.json': approval_raw, 'pending.jsonl': pending, 'results.failed.json': before,
                 'plan.json': (run / 'plan.json').read_bytes(), 'adapter.py': Path(__file__).read_bytes(),
                 'collector.py': COLLECTOR_PATH.read_bytes(), 'one_brace_collector.py': Path(collector.__file__).read_bytes(),
                 'first_wrapper.py': Path(first.__file__).read_bytes()}
    for i, (path, expected) in enumerate(sorted(approval['review_files'].items())):
        snapshots['review/' + str(i)] = first.pinned(Path(path), expected)
    judgments = {}
    for key, item in items.items():
        entry = entries[key]
        first.require(all(item[k] == entry[k] for k in ('key', 'attempt', 'failed_job_sha256', 'raw_sha256')), 'Review/pending binding differs')
        raw = (run / 'receipts' / key / item['attempt'] / 'call-0001.md').read_bytes()
        fixed, judgments[key] = reviewed_repair(first, h, raw, item)
        first.require(first.pinned(local(run, item['corrected_path']), item['corrected_sha256']) == fixed, 'Corrected review artifact differs')
        snapshots[key + '/job.failed.json'] = first.pinned(run / entry['failed_job_snapshot'], item['failed_job_sha256'])
        snapshots[key + '/corrected.raw.json'] = fixed
        snapshots[key + '/score.json'] = first.score_bytes(judgments[key])
        for path, expected in entry['invocation_files_sha256'].items():
            snapshots[key + '/calls/' + Path(path).name] = first.pinned(local(run, path), expected)
    first.require(set(snapshots) == expected_files(first, collector, approval, entries), 'Snapshot inventory differs')
    first.require((run / 'results.json').read_bytes() == before, 'Results changed during replay')
    return approval, records, judgments, snapshots


def adopt(first, collector, h, rt, run, approval_path):
    with first.campaign_lock(run):
        return _adopt_locked(first, collector, h, rt, run, approval_path)


def _adopt_locked(first, collector, h, rt, run, approval_path):
    approval, records, judgments, snapshots = prepare(first, collector, h, rt, run, approval_path)
    bundle = run / BUNDLE
    bundle.mkdir(parents=True, exist_ok=False)
    for name, raw in snapshots.items():
        path = local(bundle, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as handle:
            handle.write(raw)
    manifest = {'identity': first.IDENTITY, 'adapter_sha256': approval['adapter_sha256'],
                'approval_sha256': first.sha(snapshots['approval.json']), 'new_paid_calls': 0,
                'validated_generations': 24, 'validated_first_recovered_scores': 1,
                'validated_native_scores': 47 - len(judgments), 'batch_keys': sorted(judgments),
                'files_sha256': {name: first.sha(raw) for name, raw in snapshots.items()}}
    h.write_json(bundle / 'manifest.json', manifest)
    manifest_sha = first.sha((bundle / 'manifest.json').read_bytes())
    first.require((run / 'results.json').read_bytes() == snapshots['results.failed.json'], 'Concurrent results update; adoption refused')
    for item in approval['repairs']:
        key = item['key']
        record = candidate_record(first, records[key], judgments[key], item, manifest_sha)
        with local(run, record['output']).open('xb') as handle:
            handle.write(first.score_bytes(judgments[key]))
        h.write_json(run / 'receipts' / key / item['attempt'] / 'job.json', record)
        records[key] = record
    h.write_json(run / 'results.json', records)
    return {'state': 'adopted', 'batch_keys': sorted(judgments), 'manifest_sha256': manifest_sha, 'new_paid_calls': 0}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--approval', type=Path)
    parser.add_argument('--adopt', action='store_true')
    parser.add_argument('--phase', choices=('adopt', 'report'), default='adopt')
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args(argv)
    if args.phase != 'adopt' and args.adopt or args.phase == 'adopt' and not args.approval:
        parser.error('Adoption preview/publish requires --approval; report cannot adopt')
    collector, first = load_dependencies()
    sys.addaudithook(first.offline)
    from dotenv import load_dotenv
    load_dotenv(ROOT / '.env', override=False)
    h = first.load_harness()
    install_reporting(first, collector, h)
    with first.campaign_lock(first.RUN), h.frozen_runtime() as rt:
        if args.phase == 'adopt':
            if args.adopt:
                result = _adopt_locked(first, collector, h, rt, first.RUN, args.approval.resolve())
            else:
                approval, _, _, _ = prepare(first, collector, h, rt, first.RUN, args.approval.resolve())
                result = {'state': 'OFFLINE_ADOPTION_PREVIEW', 'batch_keys': [i['key'] for i in approval['repairs']], 'new_paid_calls': 0}
        else:
            plan, contexts, documents = h.build_plan(rt, ROOT / 'data/study/sources_ideas',
                ROOT / 'data/study/ideas_2026_09_05/374325c24e6b10a1', ROOT / h.CONTROL_PATH, ROOT / h.CANDIDATE_PATH)
            first.require(plan['identity'] == first.IDENTITY, 'Frozen identity changed')
            h.guard_inputs(plan)
            h.validate_saved_campaign(first.RUN.parent, plan)
            result = h.report(plan, first.RUN, h.read_json(first.RUN / 'results.json'), contexts, documents, rt)
            if args.require_complete:
                first.require(result['valid_generations'] == 24 and result['valid_judgments'] == 48
                              and not result['validation_errors'], 'Incomplete validated study')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
