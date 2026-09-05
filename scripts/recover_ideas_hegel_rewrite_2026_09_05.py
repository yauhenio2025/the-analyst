"""Separate offline proposal for one exact invalid terminal rewrite directive.

No semantic rewriting: remove the pinned bare directive only when F16's original
and critic finding heads are byte-identical, its status is weakened, and the critic
supplies the explicit corrected secondary anchor. Never adopts or launches models.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location('hegel_first_recovery', ROOT / 'scripts/recover_ideas_hegel_heldout_2026_09_05.py')
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)
require, sha, load_harness = base.require, base.sha, base.load_harness
IDENTITY, HARNESS_SHA256 = base.IDENTITY, base.HARNESS_SHA256
TARGET = 'inferential_commitment_mapper__previous__ganzinger'
ATTEMPT = '1064cbe77bbf'
EXPECTED_ERROR = 'revised-finding must be a quoted string'
READ_SHA256 = 'b150dd3d458d109573035cce6dca489997a483cd80d9faf7a2147b0cafd5c9d9'
CRITIC_SHA256 = '9eaeaa20a0878ba022d48f4652dbd612fe727c7c08449d18bbf7c571ab13d379'
TERMINAL_FIELD = ' — revised-finding: same finding, anchor‑b corrected'
CORRECTED_ANCHOR = 'the development from the empty, abstract universal to the synthetic, concrete singular'
COMPARISONS = (*base.COMPARISONS, 'argument_architecture__previous__elling', 'argument_architecture__revised__elling')


def strip_exact_terminal_field(original_ledger, critic_ledger, lw):
    originals = lw.parse_rows(original_ledger)
    require(originals and len({r.id for r in originals}) == len(originals), 'Original ledger has missing/duplicate IDs')
    original = [r for r in originals if r.id == 'F16']
    require(len(original) == 1, 'Expected exactly one original F16')
    lines = critic_ledger.splitlines(keepends=True)
    matches = [(i, lw._ROW_RE.match(line.rstrip('\r\n'))) for i, line in enumerate(lines)]
    matches = [(i, m) for i, m in matches if m and m[1] == 'F16']
    require(len(matches) == 1, 'Expected exactly one critic F16 row')
    index, match = matches[0]; line = lines[index]; bare = line.rstrip('\r\n')
    values = lw._field_values(match[2])
    revisions = [(name, value, field) for name, value, field in values if name in ('revised-finding', 'finding rewritten to')]
    require(len(revisions) == 1 and values[-1][0] == 'revised-finding' and bare.endswith(TERMINAL_FIELD),
            'The exact invalid terminal field is absent or ambiguous')
    require([value for name, value, _ in values if name == 'status'] == ['weakened'], 'F16 must be explicitly weakened')
    original_match = lw._ROW_RE.match(original[0].raw)
    original_values = lw._field_values(original_match[2])
    original_head = original_match[2][:original_values[0][2].start()]
    critic_head = match[2][:values[0][2].start()]
    require(original_head.encode() == critic_head.encode(), 'Critic finding head differs from original; no semantic repair is permitted')
    anchors = [value for name, value, _ in values if name == 'anchor-b']
    require(len(anchors) == 1 and lw._anchor_literal(anchors[0]) == (CORRECTED_ANCHOR, len(anchors[0]), ''),
            'Expected exact explicit corrected anchor-b')
    require(any(a.suffix == 'b' and a.quote != CORRECTED_ANCHOR for a in original[0].extra_anchors), 'Original secondary anchor was not different')
    start = match.start(2) + values[-1][2].start()
    require(bare[start:] == TERMINAL_FIELD, 'Terminal field byte boundaries differ')
    lines[index] = line[:start] + line[len(bare):]
    filtered = ''.join(lines)
    parsed = lw.parse_rows(filtered)
    updated = [r for r in parsed if r.id == 'F16']
    require(len(updated) == 1 and updated[0].finding == original[0].finding and not updated[0].revised_finding,
            'Removing the directive changed the finding or left another rewrite')
    evidence = {'id': 'F16', 'field': 'revised-finding', 'raw_field': TERMINAL_FIELD,
        'field_sha256': sha(TERMINAL_FIELD.encode()), 'original_row_sha256': sha(line.encode()),
        'filtered_row_sha256': sha(lines[index].encode()), 'unchanged_finding_head_sha256': sha(original_head.encode()),
        'reason': 'Exact terminal bare directive removed; unchanged finding head and explicit corrected anchor-b remain'}
    return filtered, evidence


@contextmanager
def repaired_view(rt, original_response, critic_response):
    old = rt.pr._ledger_text
    evidence = {'applications': 0, 'critic_response_sha256': sha(critic_response.encode()), 'ignored_rows': [], 'removed_fields': []}
    def view(content):
        ledger = old(content)
        if content != critic_response:
            return ledger
        evidence['applications'] += 1
        filtered = ledger
        if sha(critic_response.encode()) == CRITIC_SHA256:
            require(sha(original_response.encode()) == READ_SHA256, 'Pinned original read response differs')
            filtered, removal = strip_exact_terminal_field(old(original_response), ledger, rt.lw)
            evidence['removed_fields'] = [removal]
        evidence.update(original_ledger_sha256=sha(ledger.encode()), filtered_ledger_sha256=sha(filtered.encode()))
        return filtered
    rt.pr._ledger_text = view
    try:
        yield evidence
    finally:
        rt.pr._ledger_text = old


def replay(h, rt, context, calls, original_record, filtered=False):
    if not filtered:
        return base.replay(h, rt, context, calls, original_record, filtered=False)
    with repaired_view(rt, calls[0][2], calls[1][2]) as evidence:
        result, error, _, cpu = base.replay(h, rt, context, calls, original_record, filtered=False)
    require(evidence['applications'] == 1, 'Expected exactly one saved critic ledger view')
    return result, error, evidence, cpu


def prepare(h, rt, run):
    plan_raw, results_raw = (run/'plan.json').read_bytes(), (run/'results.json').read_bytes()
    plan, records = json.loads(plan_raw), json.loads(results_raw)
    fresh, contexts, docs = h.build_plan(rt, ROOT/'data/study/sources_ideas', ROOT/'data/study/ideas_2026_09_05/374325c24e6b10a1')
    require(plan['identity'] == IDENTITY and fresh == plan, 'Exact frozen study plan differs')
    selected = {key: records[key] for key in (*COMPARISONS, TARGET)}
    require(selected[TARGET]['status'] == 'failed' and selected[TARGET]['attempt'] == ATTEMPT and selected[TARGET]['error'] == EXPECTED_ERROR,
            'Original target failure differs')
    paths = {run/'plan.json'}
    for key, record in selected.items():
        job = next(j for j in plan['generations'] if j['key'] == key)
        require(record['identity'] == IDENTITY and record['job_sha256'] == h.digest(job), 'Job identity differs')
        attempt = run/'receipts'/key/record['attempt']
        require(h.read_json(attempt/'job.json') == record, 'Original job/record differs')
        paths.update(attempt.glob('call-*')); paths.add(attempt/'job.json')
        if key != TARGET:
            require(record['status'] == 'complete', 'Comparison final is incomplete')
            h.validate_completed(job, record, plan, run, records, contexts, docs, rt)
            paths.add(run/record['output'])
    before = {str(p.relative_to(run)): sha(p.read_bytes()) for p in sorted(paths) if p.is_file()}
    jobs, recovered = {}, None
    for key, record in selected.items():
        calls = h.saved_calls(run, record)
        if key == TARGET:
            require(sha(calls[0][2].encode()) == READ_SHA256 and sha(calls[1][2].encode()) == CRITIC_SHA256, 'Pinned target raw responses differ')
        unchanged, original_error, _, cpu1 = replay(h, rt, contexts[key], calls, record)
        if key == TARGET:
            require(original_error == {'error_type':'ValueError','error':EXPECTED_ERROR}, 'Exact original failure did not reproduce')
        else:
            require(original_error is None and unchanged.final_content.encode() == (run/record['output']).read_bytes(), 'Original comparison does not reproduce')
        result, error, transformation, cpu2 = replay(h, rt, contexts[key], calls, record, filtered=True)
        require(error is None and result is not None, f'Filtered replay failed: {key}: {error}')
        if key != TARGET:
            require(result.final_content == unchanged.final_content and result.receipts() == unchanged.receipts(), 'A completed final or process receipt changed')
        jobs[key] = {'original_record':record, 'original_record_sha256':h.digest(record), 'original_error_reproduced':original_error,
            'comparison_byte_identical':key != TARGET, 'output_sha256':sha(result.final_content.encode()), 'process':result.receipts(),
            'transformation':transformation, 'offline_cpu_seconds':round(cpu1+cpu2,6), 'original_attempt_seconds':record.get('seconds'),
            'process_duration_basis':'saved process duration' if 'process' in record else 'sum of saved backend call durations',
            'calls':[{k:c[0].get(k) for k in ('prompt_sha256','output_sha256','model_requested','model_used','label','input_tokens','output_tokens','retries','partial','stop_reason','cost_usd','duration_ms','backend_duration_ms')} for c in calls]}
        if key == TARGET: recovered = result.final_content.encode()
    require(all(sha((run/name).read_bytes()) == expected for name,expected in before.items()), 'Selected artifacts changed during replay')
    current = h.read_json(run/'results.json')
    require(all(current.get(k)==r for k,r in selected.items()), 'Selected records changed during replay')
    manifest = {'kind':'offline_exact_terminal_directive_recovery_proposal','version':1,'plan_identity':IDENTITY,
        'runtime_commit':h.RUNTIME,'harness_sha256':HARNESS_SHA256,'transformation_code_sha256':sha(Path(__file__).read_bytes()),
        'replay_dependency_sha256':sha(Path(base.__file__).read_bytes()),'plan_file_sha256':sha(plan_raw),'results_snapshot_sha256':sha(results_raw),
        'comparison_keys':list(COMPARISONS),'completed_finals_compared':len(COMPARISONS),'all_completed_comparisons_byte_identical':True,
        'target':TARGET,'target_attempt':ATTEMPT,'target_output_sha256':sha(recovered),'input_files_sha256':before,'jobs':jobs,
        'new_paid_calls':0,'state':'proposal_only_not_adopted',
        'resume_contract':'Separate target-specific transformation; preserve original failed job and raw responses. Reviewed external adapter validates this manifest and exact field removal only while replaying this adopted parent. No quoted replacement is invented.'}
    snapshots = {'plan.snapshot.json':plan_raw,'results.snapshot.json':results_raw,'failed_job.snapshot.json':(run/'receipts'/TARGET/ATTEMPT/'job.json').read_bytes(),'recovered.md':recovered}
    for p in (run/'receipts'/TARGET/ATTEMPT).glob('call-*'): snapshots['original_attempt/'+p.name]=p.read_bytes()
    return manifest,snapshots


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir',type=Path,default=ROOT/'data/study/ideas_hegel_heldout_2026_09_05'/IDENTITY[:16])
    parser.add_argument('--write-bundle',action='store_true');args=parser.parse_args(argv)
    from dotenv import load_dotenv
    load_dotenv(ROOT/'.env',override=False)
    def offline(event,arguments):
        if event in ('socket.connect','socket.getaddrinfo'):raise RuntimeError('Network is forbidden during offline recovery')
    sys.addaudithook(offline)
    h=load_harness()
    with h.frozen_runtime() as rt: manifest,snapshots=prepare(h,rt,args.run_dir)
    bundle=None
    if args.write_bundle:
        bundle=args.run_dir/'reader_notes/rewrite_recovery'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');bundle.mkdir(parents=True,exist_ok=False)
        for name,raw in snapshots.items():
            p=bundle/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        (bundle/'recovery_script.snapshot.py').write_bytes(Path(__file__).read_bytes())
        (bundle/'replay_dependency.snapshot.py').write_bytes(Path(base.__file__).read_bytes())
        h.write_json(bundle/'manifest.json',manifest)
    print(json.dumps({'state':manifest['state'],'bundle':str(bundle) if bundle else None,'target':TARGET,'target_output_sha256':manifest['target_output_sha256'],
        'all_byte_identical':True,'compared_completed_finals':len(COMPARISONS),'new_paid_calls':0,'recovered_final_wall':manifest['jobs'][TARGET]['process']['final_wall']},indent=2))
    return 0


if __name__=='__main__':raise SystemExit(main())
