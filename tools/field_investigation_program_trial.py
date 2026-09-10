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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive', required=True, type=Path)
    ap.add_argument('--research-state', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--execute-approved-usd', type=float, default=None)
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
    (args.out / 'field-map-tables.md').write_text((state.get('field_map') or {}).get('final_output', '') + '\n')
    receipt = {'status': 'complete' if state.get('complete') else 'incomplete', 'cost_usd': state.get('cost_usd'), 'code_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
               'selected_primary_uids': state.get('selected_primary_uids'), 'plan_source': state.get('plan_source'), 'memo_source': state.get('memo_source'),
               'field_map_source': (state.get('field_map') or {}).get('source'), 'support_policy': (state.get('support_routes') or {}).get('global_to_synthesis', {}).get('policy'),
               'stages': state.get('stages'), 'analysis': {k: {'stage': v['stage'], 'cost_usd': v.get('cost_usd')} for k, v in (state.get('analysis') or {}).items()},
               'evidence': {'total': len(state.get('evidence') or []), 'verified': sum(1 for e in state.get('evidence') or [] if e.get('quote_verified')),
                            'with_voice': sum(1 for e in state.get('evidence') or [] if e.get('voice')), 'with_bearing': sum(1 for e in state.get('evidence') or [] if e.get('bearing')),
                            'speaker_not_in_context': sum(1 for e in state.get('evidence') or [] if e.get('speaker_in_context') is False)},
               'memo_words': len((state.get('memo') or '').split()), 'draft_words': len((state.get('memo_draft') or '').split())}
    write(args.out / 'receipt.json', receipt)
    print(json.dumps({k: receipt[k] for k in ('status', 'cost_usd', 'selected_primary_uids', 'memo_source', 'evidence', 'memo_words', 'draft_words')}), flush=True)


if __name__ == '__main__':
    main()
