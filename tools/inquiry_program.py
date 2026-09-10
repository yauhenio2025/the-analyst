"""Write the research program for an inquiry from a saved packet: free preflight, one approved call.

Stage S1 of the redesign (the-reporter: communications/DESIGN_2026-09-10_inquiry_as_program_of_explanations.md).
The program runs before discovery, so by default the field inventory is withheld even when the
archive has one; `--with-field-inventory` supplies it for a revised program after discovery.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from src.dossier.engine_call import call_engine
from src.dossier.investigation import _context, _json, _spec
from src.dossier.research_state import research_state_from_program, scan_inventory
from src.engines.methods import freeze_method, method_receipt
from src.executor.spend_guard import SpendLimit, budget
from src.sources.field_investigation import expand_field_investigation

KEY = 'inquiry_program'
MODEL = 'openrouter/openai/gpt-5.6-sol'
OUTPUT_TOKENS = 9000
DEPTH = 'surface'
MID = 'openrouter/deepseek/deepseek-v4-pro'   # the critic's tier at standard depth


def write(path, value):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temp.replace(path)


class Captured(Exception):
    def __init__(self, system, user):
        self.system, self.user = system, user


def load_packet(archive: Path):
    job = json.loads((archive / 'analyst-job.json').read_text())
    docs = expand_field_investigation(job['sources'][0]['text'])
    packet = json.loads(next(d.text for d in docs if d.role == 'plan' and d.key == 'investigation'))
    bodies = {d.key: d.text for d in docs if d.role == 'source'}
    return packet, bodies


def summarize(rows):
    return [{**{k: row.get(k) for k in ('uid', 'title', 'year', 'authors', 'date_scope', 'body_state')},
             'profile_summary': _json(row.get('profile') or {})[:1200],
             'profile_summary_truncated': len(_json(row.get('profile') or {})) > 1200} for row in rows]


def build_inputs(packet, bodies, *, hunch, leads, good_answer, with_field):
    scope = {**(packet.get('scope') or {}), 'hunch': hunch, 'leads': leads, 'good_answer': good_answer}
    common = {'author': packet.get('author'), 'inquiry_type': packet.get('inquiry_type', 'bilateral'), 'question': packet['question'],
              'scope': scope, 'stage': 'program_before_discovery' if not with_field else 'program_revised_after_discovery'}
    sources = [_spec('inquiry-question', _json(common)), _spec('thinker-inventory', _json(summarize(packet.get('primary') or [])))]
    if with_field:
        sources.append(_spec('field-inventory', _json(summarize(packet.get('field') or []))))
    context = [c for c in _context(packet, bodies, cap=40000) if c['key'] != 'prior_investigations' and c.get('selected_for_context', True)]
    if context:
        sources.append(_spec('prior-context', _json(context)))
    try:
        from src.readings.registry import prior_block
        prior = prior_block(persons=[(packet.get('author') or {}).get('name', '')], texts=[])
    except Exception:
        prior = None
    if prior:
        sources.append(_spec('readings-ledger', _json(prior)))
    return sources, common


def compose(sources, packet, method):
    def capture(system, user, **kwargs):
        raise Captured(system, user)
    try:
        call_engine(KEY, sources, packet=packet, depth=DEPTH, model=MODEL, spend_cap_usd=100.0, call_fn=capture, max_chars=650000, method_snapshot=method)
    except Captured as c:
        return c.system, c.user
    raise RuntimeError('the engine returned without invoking the provider')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive', required=True, type=Path, help='directory holding analyst-job.json (the frozen packet)')
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--hunch', default='')
    ap.add_argument('--lead', action='append', default=[], help='a remembered lead, repeatable; withheld by --blind')
    ap.add_argument('--good-answer', default='')
    ap.add_argument('--with-field-inventory', action='store_true')
    ap.add_argument('--blind', action='store_true', help='withhold the leads so the program must locate voices and venues itself')
    ap.add_argument('--execute-approved-usd', type=float, default=None)
    ap.add_argument('--depth', default='surface', choices=['surface', 'standard'], help='standard adds the mid-tier critic over the rows')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True, mode=0o700)
    args.out.chmod(0o700)
    global DEPTH
    DEPTH = args.depth
    packet, bodies = load_packet(args.archive)
    leads = [] if args.blind else args.lead
    sources, common = build_inputs(packet, bodies, hunch=args.hunch, leads=leads, good_answer=args.good_answer, with_field=args.with_field_inventory)
    method = freeze_method(KEY)
    system, user = compose(sources, common, method)
    (args.out / 'prompt-system.private.md').write_text(system)
    (args.out / 'prompt-user.private.json').write_text(user)
    from src.events.pricing import resolve_pricing, estimate_cost
    price = resolve_pricing(MODEL)
    guard_ceiling = round(((len(system.encode()) + len(user.encode()) + 4096) * price[0] * 2 + OUTPUT_TOKENS * price[1]) / 1e6, 6)
    approx_tokens = (len(system) + len(user)) // 4
    preflight = {'model': MODEL, 'output_token_limit': OUTPUT_TOKENS, 'method_receipt': method_receipt(method),
                 'sources': [{'key': s.key, 'chars': len(s.text)} for s in sources], 'system_chars': len(system), 'user_chars': len(user),
                 'approx_input_tokens': approx_tokens, 'expected_cost_usd_at_full_output': estimate_cost(MODEL, approx_tokens, OUTPUT_TOKENS),
                 'guard_ceiling_usd': guard_ceiling, 'blind': args.blind, 'with_field_inventory': args.with_field_inventory,
                 'inputs_sha256': hashlib.sha256((system + '\0' + user).encode()).hexdigest()}
    write(args.out / 'preflight.json', preflight)
    print(json.dumps({k: preflight[k] for k in ('user_chars', 'approx_input_tokens', 'expected_cost_usd_at_full_output', 'guard_ceiling_usd', 'blind')}), flush=True)
    if args.execute_approved_usd is None:
        return
    from src.executor import engine_runner
    from src.executor.output_budget import limit
    from src.executor.process_runner import _default_call
    from dotenv import load_dotenv
    load_dotenv('/home/evgeny/projects/the-analyst/.env', override=False)
    engine_runner.MAX_RETRIES = 1
    engine_runner.FALLBACK_MODEL = MODEL
    if preflight['expected_cost_usd_at_full_output'] > args.execute_approved_usd:
        raise SystemExit('expected cost at full output exceeds the approved amount; nothing spent')
    state = {'version': 1, 'status': 'invoking', 'cost_usd': 0, 'approved_cap_usd': args.execute_approved_usd, 'model': MODEL,
             'method': method_receipt(method), 'code_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
             'preflight': preflight}
    state_path = args.out / 'state.json'

    def save(_=None):
        write(state_path, state)

    def provider(system_, user_, **kwargs):
        if kwargs.get('model_hint') not in (MODEL, MID):
            raise ValueError('only the pinned models are authorized')
        n = len(state.setdefault('provider_requests', [])) + 1
        state['provider_requests'].append({'label': kwargs.get('label'), 'model': kwargs.get('model_hint')})
        write(args.out / f'provider-{n:02d}-request.json', {'system': system_, 'user': user_, 'max_output_tokens': OUTPUT_TOKENS,
                                                             'options': {k: v for k, v in kwargs.items() if k != 'cancellation_check'}})
        result = _default_call(system_, user_, **kwargs)
        write(args.out / f'provider-{n:02d}-response.json', result)
        return result

    save()
    try:
        with budget(state, max(guard_ceiling + 0.01, args.execute_approved_usd), save), limit(OUTPUT_TOKENS):
            result = call_engine(KEY, sources, packet=common, depth=args.depth, model=MODEL, call_fn=provider,
                                 spend_cap_usd=max(guard_ceiling + 0.01, args.execute_approved_usd), max_chars=650000, method_snapshot=method)
    except SpendLimit as exc:
        state.update(status='refused_by_guard', error=str(exc)); save(); raise SystemExit(str(exc))
    except Exception as exc:
        state.update(status='error', error=type(exc).__name__ + ': ' + str(exc)); save(); raise
    state['cost_usd'] = float(result.get('cost_usd') or 0)
    inventory_uids = {r['uid'] for r in packet.get('primary') or []}
    rs = research_state_from_program(result, question=packet['question'], hunch=args.hunch, leads=leads, good_answer=args.good_answer,
                                     thinker=(packet.get('author') or {}).get('name', ''), inventory_uids=inventory_uids)
    scan_inventory(rs, packet.get('primary') or [], bodies)
    write(args.out / 'research-state.json', rs.model_dump(mode='json'))
    (args.out / 'program.md').write_text((result.get('prose') or '') + '\n')
    write(args.out / 'program-response.json', result)
    state.update(status='complete', calls=result.get('calls'), wall=result.get('wall'),
                 summary={'explanations': [(e.id, e.priority, e.voices) for e in rs.explanations], 'lanes': len(rs.lanes),
                          'readings': [(r.order, r.uid, r.in_inventory) for r in rs.readings], 'gaps': len(rs.gaps), 'problems': rs.problems,
                          'scan_candidates': [(c.uid, c.total, c.already_ordered) for c in rs.candidates],
                          'research_state_sha256': rs.sha256()})
    save()
    print(json.dumps({'cost_usd': state['cost_usd'], **state['summary']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
