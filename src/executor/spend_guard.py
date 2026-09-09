"""Durable per-attempt reservations for explicitly bounded institutional research.

An interrupted request retains its ceiling. A retry is a new reservation, never
an assumption that the missing response was free. Other executor jobs are unchanged.
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


@contextmanager
def budget(state, cap, save):
    ledger = state.setdefault('spend_reservations', {'base_cost_usd': state['cost_usd'], 'attempts': []})
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
