"""Regenerate only the memo stage of saved Tether arms under the argument-first framing.

Same saved inputs, model, depth, output limit and spend guard as the routing trial;
the only treatment is the current frozen `field_investigation_memo` method (the
`argument` composition role and its brief). Preflight is free: it composes the
prompt, proves the user message is byte-identical to the saved provider request,
records the system-prompt diff, and prices each call by the guard's own ceiling.
`--execute-approved-usd` spends, one arm at a time, until the cap refuses.
"""
from __future__ import annotations

import argparse
import difflib
import fcntl
import hashlib
import json
import subprocess
from pathlib import Path

from src.dossier.engine_call import call_engine
from src.dossier.field_investigation import _memo_validation
from src.dossier.investigation import recover_answer_rows
from src.engines.methods import freeze_method, method_receipt
from src.events.pricing import resolve_pricing
from src.executor.spend_guard import SpendLimit, budget
from src.sources.schemas import SourceSpec

MODEL = 'openrouter/openai/gpt-5.6-sol'
OUTPUT_TOKENS = 16000
KEY = 'field_investigation_memo'
SAVED_REQUEST = {'Answer-1': 'provider-03', 'Answer-2': 'provider-06', 'Answer-3': 'provider-09'}


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def write(path, value):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temp.replace(path)


class Captured(Exception):
    def __init__(self, system, user):
        self.system, self.user = system, user


def load_arm(inputs, label):
    saved = json.loads((inputs / f'{label}-memo-input.json').read_text())
    sources = [SourceSpec.model_validate(s) for s in saved['sources']]
    request = json.loads((inputs / f'{SAVED_REQUEST[label]}-request.json').read_text())
    return sources, saved['packet'], saved['method'], request


def compose(sources, packet, method):
    def capture(system, user, **kwargs):
        raise Captured(system, user)
    try:
        call_engine(KEY, sources, packet=packet, depth='surface', model=MODEL, spend_cap_usd=100.0,
                    call_fn=capture, max_chars=650000, method_snapshot=method)
    except Captured as c:
        return c.system, c.user
    raise RuntimeError('the engine returned without invoking the provider')


def ceiling(system, user):
    price = resolve_pricing(MODEL)
    tokens = len(system.encode()) + len(user.encode()) + 4096
    return round((tokens * price[0] * 2 + OUTPUT_TOKENS * price[1]) / 1e6, 6)


def preflight(inputs, out, labels, method):
    report = {'model': MODEL, 'output_token_limit': OUTPUT_TOKENS, 'method_receipt': method_receipt(method), 'arms': {}}
    for label in labels:
        sources, packet, old_method, request = load_arm(inputs, label)
        system, user = compose(sources, packet, method)
        old_system, old_user = request['system'], request['user']
        diff = list(difflib.unified_diff(old_system.splitlines(), system.splitlines(), 'saved-system', 'new-system', lineterm='', n=0))
        (out / f'{label}-system-diff.txt').write_text('\n'.join(diff) + '\n')
        report['arms'][label] = {
            'saved_method_sha256': old_method['sha256'], 'new_method_sha256': method['sha256'],
            'user_identical_to_saved_request': sha(user) == sha(old_user), 'user_chars': len(user), 'saved_user_chars': len(old_user),
            'system_chars': len(system), 'saved_system_chars': len(old_system), 'system_changed_lines': sum(1 for l in diff if l[:1] in '+-' and not l.startswith(('+++', '---'))),
            'guard_ceiling_usd': ceiling(system, user)}
    write(out / 'preflight.json', report)
    return report


def worst_case(inputs, label):
    """The approved cap is enforced on actual charges plus a witnessed worst case for the next call: the saved
    provider response for the byte-identical user message gives its input tokens; add 2,000 for the longer
    system prompt and assume the full output allowance. The production guard's byte-counted ceiling (about six
    times the actual charge) stays on the reservation ledger under its own, wider cap."""
    from src.executor.process_runner import estimate_cost
    witness = json.loads((inputs / f'{SAVED_REQUEST[label]}-response.json').read_text())
    return round(estimate_cost(MODEL, int(witness['input_tokens']) + 2000, OUTPUT_TOKENS), 6), int(witness['input_tokens'])


def execute(inputs, out, labels, method, cap, guard_cap, state_path):
    from src.executor import engine_runner
    from src.executor.output_budget import limit
    from src.executor.process_runner import _default_call
    from dotenv import load_dotenv
    load_dotenv('/home/evgeny/projects/the-analyst/.env', override=False)
    engine_runner.MAX_RETRIES = 1
    engine_runner.FALLBACK_MODEL = MODEL
    state = json.loads(state_path.read_text()) if state_path.exists() else {
        'version': 1, 'status': 'prepared', 'cost_usd': 0, 'approved_cap_usd': cap, 'guard_cap_usd': guard_cap,
        'cap_policy': 'approved cap on actual charges plus witnessed worst case per call; guard cap admits the byte-counted reservations',
        'model': MODEL, 'output_token_limit': OUTPUT_TOKENS,
        'method': method_receipt(method), 'code_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'arms': {}}
    if state['method']['sha256'] != method['sha256']:
        raise ValueError('The frozen method changed since this trial state was written; nothing was spent')

    def save(_=None):
        write(state_path, state)

    def provider(system, user, **kwargs):
        if kwargs.get('model_hint') != MODEL:
            raise ValueError('This trial authorizes only the pinned model')
        requests = state.setdefault('provider_requests', [])
        name = f'provider-{len(requests) + 1:02d}'
        requests.append({'file': name, 'status': 'invoking'})
        write(out / (name + '-request.json'), {'system': system, 'user': user, 'max_output_tokens': OUTPUT_TOKENS,
                                               'options': {k: v for k, v in kwargs.items() if k != 'cancellation_check'}})
        save()
        result = _default_call(system, user, **kwargs)
        write(out / (name + '-response.json'), result)
        requests[-1]['status'] = 'returned'
        save()
        return result

    for label in labels:
        record = state['arms'].get(label)
        if record:
            if record['status'] != 'complete':
                raise ValueError(f'{label} has an incomplete prior invocation; inspect it before any continuation')
            continue
        sources, packet, _, _ = load_arm(inputs, label)
        worst, witness_tokens = worst_case(inputs, label)
        if state['cost_usd'] + worst > cap:
            state['arms'][label] = {'status': 'refused_by_approved_cap', 'worst_case_usd': worst, 'witness_input_tokens': witness_tokens,
                                    'error': f"approved cap ${cap:.2f}: ${state['cost_usd']:.4f} charged; worst case for this call ${worst:.4f}"}
            state['status'] = 'stopped_by_approved_cap'
            save()
            print(json.dumps({'arm': label, 'refused_by_approved_cap': worst}), flush=True)
            return state
        record = state['arms'][label] = {'status': 'invoking', 'worst_case_usd': worst, 'witness_input_tokens': witness_tokens}
        save()
        try:
            with budget(state, guard_cap, save), limit(OUTPUT_TOKENS):
                response = call_engine(KEY, sources, packet=packet, depth='surface', model=MODEL, call_fn=provider,
                                       spend_cap_usd=guard_cap, max_chars=650000, method_snapshot=method)
        except SpendLimit as exc:
            record.update(status='refused_by_guard', error=str(exc))
            state['status'] = 'stopped_by_guard'
            save()
            print(json.dumps({'arm': label, 'refused': str(exc)}), flush=True)
            return state
        except Exception as exc:
            record.update(status='error', error=type(exc).__name__ + ': ' + str(exc))
            state['status'] = 'stopped'
            save()
            raise
        recover_answer_rows(response)
        state['cost_usd'] += float(response.get('cost_usd') or 0)
        prose, _, validation = _memo_validation(response, packet['evidence'], packet.get('mode'))
        (out / f'{label}-memo.md').write_text(prose + '\n')
        write(out / f'{label}-memo-response.json', response)
        record.update(status='complete', cost_usd=response.get('cost_usd'), validation=validation,
                      calls=response.get('calls'), wall=response.get('wall'), prose_chars=len(prose))
        save()
        print(json.dumps({'arm': label, 'cost_usd': state['cost_usd'], 'supported': validation['supported'],
                          'prose_chars': len(prose)}), flush=True)
    state['status'] = 'complete'
    save()
    return state


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--inputs', required=True, type=Path, help='the routing trial output directory (saved memo inputs and provider requests)')
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--arms', default='Answer-2,Answer-1')
    ap.add_argument('--execute-approved-usd', type=float, default=None)
    args = ap.parse_args()
    if args.out.resolve() == args.inputs.resolve() or args.out.resolve().is_relative_to(args.inputs.resolve()):
        ap.error('Output must be outside the routing trial directory')
    args.out.mkdir(parents=True, exist_ok=True, mode=0o700)
    args.out.chmod(0o700)
    labels = [a.strip() for a in args.arms.split(',') if a.strip()]
    with (args.out / '.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        method = freeze_method(KEY)
        report = preflight(args.inputs, args.out, labels, method)
        print(json.dumps({'preflight': {k: {'user_identical': v['user_identical_to_saved_request'],
                                            'system_changed_lines': v['system_changed_lines'], 'ceiling_usd': v['guard_ceiling_usd']}
                                        for k, v in report['arms'].items()}}), flush=True)
        if args.execute_approved_usd is None:
            return
        if not all(v['user_identical_to_saved_request'] for v in report['arms'].values()):
            raise SystemExit('A user message differs from the saved request; the treatment would not be framing alone. Nothing spent.')
        guard_cap = round(sum(v['guard_ceiling_usd'] for v in report['arms'].values()) + 0.01, 2)
        execute(args.inputs, args.out, labels, method, args.execute_approved_usd, guard_cap, args.out / 'state.json')


if __name__ == '__main__':
    main()
