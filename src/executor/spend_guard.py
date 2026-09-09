"""Durable per-attempt reservations for explicitly bounded institutional research.

An interrupted request retains an unresolved ceiling. Only an identical verified
request can refine its input bound; the full output allowance stays reserved.
A retry is a new reservation, never an assumption that a missing response was free.
"""
from contextlib import contextmanager
from contextvars import ContextVar
import hashlib
import uuid

from src.events.pricing import resolve_pricing

_CURRENT = ContextVar('institutional_spend_guard', default=None)


class SpendLimit(ValueError):
    pass


def active():
    return _CURRENT.get() is not None


def refine_repeated_input_bounds(ledger):
    """Tighten only input bounds witnessed by an identical completed request.

    A missing response is still an uncertain charge. Its entire configured
    output allowance remains reserved, and its original ceiling is retained.
    The witness must have provider-verified usage (a settled record), the same
    model and exact system/user hash, and matching configured accounting rates.
    An extra 4096 input tokens retain the existing framing safety allowance.
    """
    changed = False
    attempts = ledger.get('attempts', [])
    for record in attempts:
        if record.get('status') not in ('reserved', 'uncertain') or 'cost_usd' in record:
            continue
        price = resolve_pricing(record.get('model', ''))
        if not price or not record.get('input_sha256') or not record.get('max_output_tokens'):
            continue
        witnesses = [r for r in attempts if r.get('status') == 'settled'
                     and r.get('model') == record['model']
                     and r.get('input_sha256') == record['input_sha256']
                     and r.get('input_tokens', 0) > 0 and r.get('output_tokens', 0) > 0
                     and r.get('cost_usd') == round(
                         (r['input_tokens'] * price[0] * 2 + r['output_tokens'] * price[1]) / 1e6, 6)]
        if not witnesses:
            continue
        witness = max(witnesses, key=lambda r: r['input_tokens'])
        input_bound = witness['input_tokens'] + 4096
        original = record.get('original_ceiling_usd', record['ceiling_usd'])
        ceiling = min(original, round((input_bound * price[0] * 2 + record['max_output_tokens'] * price[1]) / 1e6, 6))
        if ceiling == record['ceiling_usd']:
            continue
        record.setdefault('original_ceiling_usd', record['ceiling_usd'])
        record.update(ceiling_usd=ceiling, input_bound_receipt={
            'policy': 'identical_request_usage_with_framing_allowance_v1',
            'witness_attempt_id': witness['id'], 'input_sha256': record['input_sha256'],
            'witness_input_tokens': witness['input_tokens'], 'framing_allowance_tokens': 4096,
            'input_token_ceiling': input_bound, 'max_output_tokens': record['max_output_tokens'],
            'input_usd_per_million': price[0] * 2, 'output_usd_per_million': price[1],
            'charge_remains_unresolved': True})
        changed = True
    return changed


@contextmanager
def budget(state, cap, save):
    ledger = state.setdefault('spend_reservations', {'base_cost_usd': state['cost_usd'], 'attempts': []})
    if refine_repeated_input_bounds(ledger):
        save(state)
    token = _CURRENT.set((ledger, cap, lambda: save(state)))
    try:
        yield
    finally:
        _CURRENT.reset(token)


def reserve(model, system, user, max_tokens, label):
    context = _CURRENT.get()
    if context is None:
        return None
    ledger, cap, save = context
    price = resolve_pricing(model)
    # These adapters expose SDK retry controls and token usage. A new provider
    # needs an explicit receipt contract before it can spend from this ledger.
    if not price or not model.startswith(('openrouter/', 'claude-')):
        raise SpendLimit(f'No bounded provider receipt contract for {model}; nothing was spent')
    tokens = len(system.encode()) + len(user.encode()) + 4096
    # UTF-8 bytes bound ordinary text tokens; double input list price covers
    # cache writes and the extended-context premium without assuming cache hits.
    ceiling = round((tokens * price[0] * 2 + max_tokens * price[1]) / 1e6, 6)
    used = ledger['base_cost_usd'] + sum(r.get('cost_usd', r['ceiling_usd']) for r in ledger['attempts'])
    if used + ceiling > cap:
        raise SpendLimit(f'Analysis cap ${cap:.2f}: ${used:.2f} spent/reserved; next call ceiling ${ceiling:.2f}. Research retained')
    record = {'id': uuid.uuid4().hex, 'model': model, 'label': label, 'ceiling_usd': ceiling,
              'status': 'reserved', 'input_sha256': hashlib.sha256((system+'\0'+user).encode()).hexdigest(),
              'max_output_tokens': max_tokens}
    ledger['attempts'].append(record)
    save()
    return record


def settle(record, result):
    if record is None:
        return
    context = _CURRENT.get()
    # Partial adapters can estimate usage after a broken stream. Keep their
    # ceiling until a real provider receipt reconciles the uncertain charge.
    if result.partial or not result.usage_verified or not result.input_tokens or not result.output_tokens:
        record['status'] = 'uncertain'
    else:
        price = resolve_pricing(result.model_id)
        if price:
            record.update(status='settled', input_tokens=result.input_tokens, output_tokens=result.output_tokens,
                          cost_usd=round((result.input_tokens * price[0] * 2 + result.output_tokens * price[1]) / 1e6, 6))
    context[2]()
