"""Run the field investigation through the program path on a saved packet: thinker first, code evidence tables, critic and revision.

Steps 3 and 4 of the redesign on the saved Tether packet (the same sixteen field sources as the original run; no new discovery).
Preflight is free: it reports the selection the program makes and the cost ceiling. Execution needs an approved amount; every
call is the production runner's, recorded in the state; the original archive is never written.
"""
from __future__ import annotations

import argparse
import copy
import json
import subprocess
from pathlib import Path

from src.dossier.field_investigation import program_selection, run_field_investigation
from src.sources.field_investigation import expand_field_investigation

MODEL = 'openrouter/openai/gpt-5.6-sol'


def write(path, value):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + '\n')
    temp.replace(path)


def load(archive: Path, state_path: Path):
    job = json.loads((archive / 'analyst-job.json').read_text())
    docs = expand_field_investigation(job['sources'][0]['text'])
    packet = json.loads(next(d.text for d in docs if d.role == 'plan' and d.key == 'investigation'))
    bodies = {d.key: d.text for d in docs if d.role == 'source'}
    rs = json.loads(state_path.read_text())
    packet = copy.deepcopy(packet)
    packet['research_state'] = rs
    return packet, bodies


def extend_state(old, packet):
    """A new run's state from an old one: the reading calls, their frozen inputs and manifests and the frozen methods carry over;
    everything derived (evidence, readings, selection, plan, coverage, final stages) is computed again under the new packet. The
    reading contracts do not carry: the readings' upstream names the snapshot, which changed; the cached result is reused as the
    reading of the same text (same source key, same body hash, checked by read_population)."""
    from datetime import datetime, timezone
    from src.dossier.field_investigation import packet_fingerprint
    reads = {k: v for k, v in old.get('calls', {}).items() if k.startswith('read:')}
    carried_cost = sum(float(a.get('cost_usd') or 0) for a in old.get('analysis', {}).values() if str(a.get('stage', '')).startswith('read:'))
    return {'packet_sha256': packet_fingerprint(packet), 'mode': old.get('mode', 'standalone'), 'stages': [], 'calls': reads, 'analysis': {},
            'cost_usd': 0.0, 'evidence': [], 'readings': [], 'complete': False,
            'read_inputs': {k: v for k, v in old.get('read_inputs', {}).items() if k in reads},
            'call_input_manifests': {k: v for k, v in old.get('call_input_manifests', {}).items() if k in reads},
            'method_snapshots': dict(old.get('method_snapshots') or {}),
            'extended_from': {'packet_sha256': old.get('packet_sha256'), 'at': datetime.now(timezone.utc).isoformat(), 'readings_carried': len(reads),
                              'carried_cost_usd': round(carried_cost, 4), 'previous_cost_usd': old.get('cost_usd')}}


def redo_from_memo(state):
    """Forget the final memo stages of a saved state so they run again under the current methods: the paid readings, the
    adjudication and every cost stay; the memo, critic and revision calls, their contracts, manifests and frozen methods go."""
    from datetime import datetime, timezone
    redo = {'from': 'memo', 'at': datetime.now(timezone.utc).isoformat(), 'cost_before_usd': state.get('cost_usd'),
            'forgotten_calls': sorted(k for k in state.get('calls', {}) if k.startswith('memo')),
            'previous_memo_source': state.get('memo_source')}
    for table in ('calls', 'call_contracts', 'call_input_manifests', 'stage_status'):
        for k in list(state.get(table) or {}):
            if k.startswith('memo'):
                del state[table][k]
    for k in ('memo_critic', 'field_investigation_memo'):
        (state.get('method_snapshots') or {}).pop(k, None)
    for k in [k for k in state if k.startswith('memo') or k in ('changes', 'paused_reason', 'running_stage')]:
        state.pop(k, None)
    state['stages'] = [s for s in state.get('stages', []) if not s.startswith('memo') and s != 'done']
    state['complete'] = False
    state.setdefault('redo', []).append(redo)
    return state


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive', required=True, type=Path)
    ap.add_argument('--research-state', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--execute-approved-usd', type=float, default=None)
    ap.add_argument('--extend-from', type=Path, default=None,
                    help='a previous run directory: its paid readings of unchanged source texts are reused under this new packet; new sources are '
                         'read and the final stages run again (the state records what was carried)')
    ap.add_argument('--redo-from', choices=['memo'], default=None,
                    help='on an existing state: forget the memo, critic and revision calls and their frozen methods so they run again under the '
                         'current methods; every reading and the adjudication stay paid and reused')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True, mode=0o700)
    args.out.chmod(0o700)
    packet, bodies = load(args.archive, args.research_state)
    available = sum(1 for r in packet['primary'] if bodies.get(r['source_key']))
    selected, decisions = program_selection(packet['research_state'], packet, bodies, int((packet.get('limits') or {}).get('max_read_texts', 12)))
    field_available = [r['uid'] for r in packet['field'] if bodies.get(r['source_key'])]
    preflight = {'model': MODEL, 'thinker_available': available, 'thinker_selected': selected,
                 'selection_reasons': {u: decisions[u]['reason'][:120] for u in selected}, 'field_to_read': field_available,
                 'expected_calls': {'author_read': len(selected), 'field_read': len(field_available), 'adjudication': 1, 'memo': 1, 'critic': 1, 'revision': 1},
                 'expected_cost_usd': round(0.17 * (len(selected) + len(field_available)) + 0.40 + 0.45 + 0.20 + 0.45, 2)}
    write(args.out / 'preflight.json', preflight)
    print(json.dumps({k: preflight[k] for k in ('thinker_selected', 'expected_calls', 'expected_cost_usd')}), flush=True)
    if args.execute_approved_usd is None:
        return
    from dotenv import load_dotenv
    load_dotenv('/home/evgeny/projects/the-analyst/.env', override=False)
    from src.dossier.engine_call import call_engine
    from src.executor import engine_runner
    engine_runner.MAX_RETRIES = 1
    engine_runner.FALLBACK_MODEL = MODEL
    state_path = args.out / 'state.json'
    state = json.loads(state_path.read_text()) if state_path.exists() else None
    if state is None and args.extend_from:
        state = extend_state(json.loads((args.extend_from / 'state.json').read_text()), packet)
        write(state_path, state)
    if state and args.redo_from == 'memo':
        state = redo_from_memo(state)
        save_redo = dict(state)
        write(state_path, save_redo)

    def save(s):
        write(state_path, s)

    def call(key, sources, **kwargs):
        kwargs.setdefault('model', MODEL)
        n = len(list(args.out.glob('provider-*-request.json'))) + 1
        write(args.out / f'provider-{n:02d}-request.json', {'engine': key, 'sources': [s.key for s in sources], 'packet_keys': sorted((kwargs.get('packet') or {}).keys())})
        result = call_engine(key, sources, **kwargs)
        write(args.out / f'provider-{n:02d}-response.json', {k: result.get(k) for k in ('engine_key', 'model', 'cost_usd', 'calls', 'wall')})
        return result

    try:
        state = run_field_investigation(packet, bodies, call=call, save=save, state=state, spend_cap_usd=args.execute_approved_usd)
    except Exception as exc:
        import traceback
        traceback.print_exc()
        print(json.dumps({'stopped': f'{type(exc).__name__}: {str(exc)[:300]}'}), flush=True)
        raise SystemExit(1)
    (args.out / 'memo.md').write_text((state.get('memo') or '') + '\n')
    (args.out / 'memo-draft.md').write_text((state.get('memo_draft') or '') + '\n')
    (args.out / 'memo-critic.md').write_text((state.get('memo_critic') or '') + '\n')
    (args.out / 'memo-critic-of-revision.md').write_text((state.get('memo_critic_revision') or '') + '\n')
    (args.out / 'memo-revision-1.md').write_text((state.get('memo_revision') or '') + '\n')
    (args.out / 'field-map-tables.md').write_text((state.get('field_map') or {}).get('final_output', '') + '\n')
    receipt = {'status': 'complete' if state.get('complete') else 'incomplete', 'cost_usd': state.get('cost_usd'), 'code_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
               'selected_primary_uids': state.get('selected_primary_uids'), 'plan_source': state.get('plan_source'), 'memo_source': state.get('memo_source'),
               'field_map_source': (state.get('field_map') or {}).get('source'), 'support_policy': (state.get('support_routes') or {}).get('global_to_synthesis', {}).get('policy'),
               'stages': state.get('stages'), 'analysis': {k: {'stage': v['stage'], 'cost_usd': v.get('cost_usd')} for k, v in (state.get('analysis') or {}).items()},
               'evidence': {'total': len(state.get('evidence') or []), 'verified': sum(1 for e in state.get('evidence') or [] if e.get('quote_verified')),
                            'with_voice': sum(1 for e in state.get('evidence') or [] if e.get('voice')), 'with_bearing': sum(1 for e in state.get('evidence') or [] if e.get('bearing')),
                            'speaker_not_in_context': sum(1 for e in state.get('evidence') or [] if e.get('speaker_in_context') is False)},
               'memo_words': len((state.get('memo') or '').split()), 'draft_words': len((state.get('memo_draft') or '').split()),
               'unused_findings_after_draft': (state.get('memo_unused_findings') or {}).get('count'),
               'unused_findings_after_revision': (state.get('memo_unused_after_revision') or {}).get('count'),
               'dropped_citations': (state.get('memo_dropped_citations') or {}).get('count'), 'must_use': state.get('memo_must_use'),
               'dropped_by_second_revision': (state.get('memo_dropped_by_second_revision') or {}).get('by_source'), 'redo': state.get('redo'),
               'extended_from': state.get('extended_from'), 'second_revision_repaired': state.get('memo_revision2_repaired')}
    write(args.out / 'receipt.json', receipt)
    print(json.dumps({k: receipt[k] for k in ('status', 'cost_usd', 'selected_primary_uids', 'memo_source', 'evidence', 'memo_words', 'draft_words')}), flush=True)


if __name__ == '__main__':
    main()
