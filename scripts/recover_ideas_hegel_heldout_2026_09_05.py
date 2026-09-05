"""Offline proposal for one saved held-out critic parsing failure; never adopts or launches.

Default previews the replay/equivalence evidence. --write-bundle writes an immutable
proposal under reader_notes, without touching study results, jobs, receipts or outputs.
Unrelated, previously unattempted study jobs may continue while this reads six pinned
records. A future adopter/resume adapter must be reviewed separately.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = '43f051bdd4d890762145163d0e1d41c9be46aa19234f61456962ded883530d7e'
HARNESS_SHA256 = 'bf781c7202f3e6e22de624bfe9929cfd8402ce0bb2a5a55b8756754ed0190ac1'
TARGET = 'argument_architecture__revised__ganzinger'
ATTEMPT = 'c5620c0d97c1'
EXPECTED_ERROR = 'Ledger row I4 has repeated anchor fields; use distinct anchor/doc suffixes'
COMPARISONS = (
    'conditions_of_possibility_analyzer__previous__ganzinger',
    'conditions_of_possibility_analyzer__revised__ganzinger',
    'conditions_of_possibility_analyzer__previous__elling',
    'conditions_of_possibility_analyzer__revised__elling',
    'argument_architecture__previous__ganzinger',
)
HEADING = re.compile(r'^\s{0,3}#{1,6}\s')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_harness():
    path = ROOT / 'scripts/study_ideas_hegel_heldout_2026_09_05.py'
    require(sha(path.read_bytes()) == HARNESS_SHA256, 'Frozen harness bytes changed')
    spec = importlib.util.spec_from_file_location('pinned_hegel_harness', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prune_unapplied_rows(ledger, original_ids, lw):
    """Remove only unknown, non-added row blocks that apply_rulings cannot use.

    Known auxiliary references and duplicate IDs stay byte-identical. An ambiguous repeated status
    is retained, as is any addition. Unknown IDs are never mapped onto originals.
    No anchor is decoded or repaired here, so retained malformed rows still fail
    under the strict frozen parser. The exact removed bytes travel in the manifest.
    """
    originals = set(original_ids)
    lines = ledger.splitlines(keepends=True)
    counts, auxiliary = Counter(), False
    for line in lines:
        if lw._LEDGER_SECTION_RE.match(line):
            auxiliary = False
        elif lw._AUX_SECTION_RE.match(line):
            auxiliary = True
        match = None if auxiliary else lw._ROW_RE.match(line.rstrip('\r\n'))
        if match:
            counts[match[1]] += 1
    kept, removed = [], []
    auxiliary, index = False, 0
    while index < len(lines):
        line = lines[index]
        if lw._LEDGER_SECTION_RE.match(line):
            auxiliary = False
        elif lw._AUX_SECTION_RE.match(line):
            auxiliary = True
        match = None if auxiliary else lw._ROW_RE.match(line.rstrip('\r\n'))
        if match and match[1] not in originals and counts[match[1]] == 1:
            statuses = [value for name, value, _ in lw._field_values(match[2]) if name == 'status']
            sm = lw._STATUS_RE.match('status: ' + (statuses[0] if len(statuses) == 1 else ''))
            status = sm[1].lower() if sm else ''
            if len(statuses) <= 1 and status != 'added':
                end = index + 1
                while end < len(lines) and not (HEADING.match(lines[end]) or lw._ROW_RE.match(lines[end])):
                    end += 1
                block = ''.join(lines[index:end])
                removed.append({'id': match[1], 'status': status, 'raw_status': statuses,
                                'reason': 'ID absent from original rows and status is not added; frozen apply_rulings cannot apply this row',
                                'start_line': index + 1, 'end_line': end,
                                'block_sha256': sha(block.encode()), 'raw_block': block})
                index = end
                continue
        kept.append(line)
        index += 1
    return ''.join(kept), removed


@contextmanager
def filtered_critic_view(rt, critic_response, original_ids):
    """Override one exact saved critic ledger view, never the read or prompt."""
    original = rt.pr._ledger_text
    evidence = {'applications': 0, 'critic_response_sha256': sha(critic_response.encode())}
    def view(content):
        ledger = original(content)
        if content == critic_response:
            filtered, removed = prune_unapplied_rows(ledger, original_ids, rt.lw)
            evidence.update(applications=evidence['applications'] + 1,
                            original_ledger_sha256=sha(ledger.encode()), filtered_ledger_sha256=sha(filtered.encode()), ignored_rows=removed)
            return filtered
        return ledger
    rt.pr._ledger_text = view
    try:
        yield evidence
    finally:
        rt.pr._ledger_text = original


def replay(h, rt, context, calls, original_record, filtered=False):
    position, error, result = 0, None, None
    evidence = None
    started = time.perf_counter()
    def saved(system_prompt, user_message, **kwargs):
        nonlocal position
        require(position < len(calls), 'Offline replay requested an unsaved call')
        response = h.validate_call(calls[position], {'system': system_prompt, 'user': user_message}, kwargs['model_hint'], kwargs['label'])
        position += 1
        return response
    def run():
        return rt.pr.run_oneshot_checked(context['cap'], context['spec'], context['documents'], depth='standard',
             tier_overrides={'strong': h.MODELS['read'], 'mid': h.MODELS['critic']}, call_fn=saved)
    originals = rt.lw.parse_rows(rt.pr._ledger_text(calls[0][2]))
    require(originals and len({r.id for r in originals}) == len(originals), 'Missing or ambiguous original IDs')
    try:
        if filtered:
            with filtered_critic_view(rt, calls[1][2], {r.id for r in originals}) as evidence:
                result = run()
            require(evidence['applications'] == 1, 'Recovery did not target exactly one critic ledger view')
        else:
            result = run()
    except Exception as exc:
        error = {'error_type': type(exc).__name__, 'error': str(exc)}
    require(position == 2, 'Replay failed before validating both exact saved prompts/models/responses')
    cpu_seconds = time.perf_counter() - started
    if result is not None:
        # Step calls already use original backend durations, tokens and models.
        # A failed process has no recorded process total; do not relabel CPU time as API time.
        result.seconds = original_record.get('process', {}).get('seconds',
            sum(c[0].get('backend_duration_ms') or c[0]['duration_ms'] for c in calls) / 1000)
    return result, error, evidence, cpu_seconds


def prepare(h, rt, run):
    plan_bytes, results_bytes = (run / 'plan.json').read_bytes(), (run / 'results.json').read_bytes()
    plan, records = json.loads(plan_bytes), json.loads(results_bytes)
    require(plan['identity'] == IDENTITY and h.digest({k: v for k, v in plan.items() if k != 'identity'}) == IDENTITY, 'Unexpected study identity')
    fresh, contexts, docs = h.build_plan(rt, ROOT / 'data/study/sources_ideas', ROOT / 'data/study/ideas_2026_09_05/374325c24e6b10a1')
    require(fresh == plan, 'Exact frozen plan reconstruction differs')
    target = records.get(TARGET, {})
    require(target.get('status') == 'failed' and target.get('attempt') == ATTEMPT and target.get('error') == EXPECTED_ERROR, 'Expected original failed target changed')
    selected = {key: records[key] for key in (*COMPARISONS, TARGET)}
    paths = {run / 'plan.json'}
    for key, record in selected.items():
        job = next(j for j in plan['generations'] if j['key'] == key)
        require(record['identity'] == IDENTITY and record['job_sha256'] == h.digest(job), 'Selected record identity differs')
        attempt = run / 'receipts' / key / record['attempt']
        require(h.read_json(attempt / 'job.json') == record, 'Selected job/record differs')
        paths.update(attempt.glob('call-*')); paths.add(attempt / 'job.json')
        if key != TARGET:
            require(record['status'] == 'complete', 'An original comparison is not complete')
            h.validate_completed(job, record, plan, run, records, contexts, docs, rt)
            paths.add(run / record['output'])
    before = {str(p.relative_to(run)): sha(p.read_bytes()) for p in sorted(paths) if p.is_file()}
    jobs, recovered = {}, None
    for key, record in selected.items():
        calls = h.saved_calls(run, record)
        context = contexts[key]
        unchanged, original_error, _, cpu1 = replay(h, rt, context, calls, record)
        if key == TARGET:
            require(original_error == {'error_type': 'ValueError', 'error': EXPECTED_ERROR}, 'Frozen replay did not reproduce exact original failure')
        else:
            require(original_error is None and unchanged.final_content.encode() == (run / record['output']).read_bytes(), 'Original completed output does not reproduce')
        result, error, transformation, cpu2 = replay(h, rt, context, calls, record, filtered=True)
        require(error is None and result is not None, f'Filtered replay failed for {key}: {error}')
        if key != TARGET:
            require(result.final_content == unchanged.final_content and result.final_wall == unchanged.final_wall
                    and result.receipts() == unchanged.receipts(), 'Existing final/wall/process receipt changed under filtering')
        entry = {'original_record': record, 'original_record_sha256': h.digest(record),
                 'original_error_reproduced': original_error, 'comparison_byte_identical': key != TARGET,
                 'output_sha256': sha(result.final_content.encode()), 'process': result.receipts(),
                 'transformation': transformation, 'offline_cpu_seconds': round(cpu1 + cpu2, 6),
                 'original_attempt_seconds': record.get('seconds'),
                 'process_duration_basis': 'saved process duration' if 'process' in record else 'sum of saved backend call durations',
                 'calls': [{k: c[0].get(k) for k in ('prompt_sha256', 'output_sha256', 'model_requested', 'model_used', 'label', 'input_tokens', 'output_tokens', 'retries', 'partial', 'stop_reason', 'cost_usd', 'duration_ms', 'backend_duration_ms')} for c in calls]}
        jobs[key] = entry
        if key == TARGET:
            recovered = result.final_content.encode()
    require(all(sha((run / name).read_bytes()) == expected for name, expected in before.items()), 'A selected immutable artifact changed during replay')
    current = h.read_json(run / 'results.json')
    require(all(current.get(key) == record for key, record in selected.items()), 'A selected record changed during replay')
    manifest = {'kind': 'offline_ignored_critic_rows_recovery_proposal', 'version': 1, 'plan_identity': IDENTITY,
        'runtime_commit': h.RUNTIME, 'harness_sha256': HARNESS_SHA256, 'transformation_code_sha256': sha(Path(__file__).read_bytes()),
        'plan_file_sha256': sha(plan_bytes), 'results_snapshot_sha256': sha(results_bytes),
        'comparison_keys': list(COMPARISONS), 'completed_finals_compared': len(COMPARISONS), 'all_completed_comparisons_byte_identical': True,
        'target': TARGET, 'target_attempt': ATTEMPT, 'target_output_sha256': sha(recovered),
        'input_files_sha256': before, 'jobs': jobs, 'new_paid_calls': 0,
        'state': 'proposal_only_not_adopted',
        'resume_contract': 'Ordinary unchanged-harness replay will still reproduce the original parse failure. A reviewed external adapter must validate the recovery manifest and apply this exact target-bound transformation only during validation of the adopted recovered parent. Fresh job execution stays unchanged. Adoption must preserve the failed record/job and raw call files, retain the same attempt and costs, gate on idle state and use an atomic guarded results update.'}
    snapshots = {'plan.snapshot.json': plan_bytes, 'results.snapshot.json': results_bytes,
        'failed_job.snapshot.json': (run / 'receipts' / TARGET / ATTEMPT / 'job.json').read_bytes(),
        'recovered.md': recovered}
    for p in (run / 'receipts' / TARGET / ATTEMPT).glob('call-*'):
        snapshots['original_attempt/' + p.name] = p.read_bytes()
    return manifest, snapshots


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, default=ROOT / 'data/study/ideas_hegel_heldout_2026_09_05' / IDENTITY[:16])
    parser.add_argument('--write-bundle', action='store_true')
    args = parser.parse_args(argv)
    from dotenv import load_dotenv
    load_dotenv(ROOT / '.env', override=False)
    def offline(event, arguments):
        if event in ('socket.connect', 'socket.getaddrinfo'):
            raise RuntimeError('Network is forbidden during offline recovery')
    sys.addaudithook(offline)
    h = load_harness()
    with h.frozen_runtime() as rt:
        manifest, snapshots = prepare(h, rt, args.run_dir)
    bundle = None
    if args.write_bundle:
        bundle = args.run_dir / 'reader_notes/ruling_recovery' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
        bundle.mkdir(parents=True, exist_ok=False)
        for name, raw in snapshots.items():
            path = bundle / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
        (bundle / 'recovery_script.snapshot.py').write_bytes(Path(__file__).read_bytes())
        h.write_json(bundle / 'manifest.json', manifest)
    print(json.dumps({'state': manifest['state'], 'identity': IDENTITY, 'bundle': str(bundle) if bundle else None,
        'target': TARGET, 'target_output_sha256': manifest['target_output_sha256'],
        'compared_completed_finals': manifest['completed_finals_compared'], 'all_byte_identical': True,
        'ignored_target_ids': [r['id'] for r in manifest['jobs'][TARGET]['transformation']['ignored_rows']],
        'recovered_final_wall': manifest['jobs'][TARGET]['process']['final_wall'], 'new_paid_calls': 0}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
