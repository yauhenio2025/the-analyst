"""Execute and validate the central experimental reading-to-search decision."""
from __future__ import annotations

import re

from src.dossier.investigation import _field, quote_span, recover_answer_rows

ENGINE = 'research_evidence_feedback'


def decision(result, sources, packet):
    bodies = {s.key: s.text for s in sources if s.role == 'source' and s.kind == 'paste' and s.text}
    rows = recover_answer_rows(result)
    observations, seen, ambiguous = [], {}, set()
    for row in rows:
        if row.get('dim') != 'observation':
            continue
        key, quote = row.get('doc'), row.get('anchor') or ''
        body = bodies.get(key, '')
        span = quote_span(quote, body, [(0, len(body))]) if body else None
        observation = {**row, 'quote_verified': bool(span), 'source_key': key,
                       'quote_start': span[0] if span else None, 'quote_end': span[1] if span else None}
        rid = row.get('id')
        if rid in seen and seen[rid] != observation:
            ambiguous.add(rid)
        seen[rid] = observation
    observations = [{**o, 'quote_verified': o['quote_verified'] and rid not in ambiguous} for rid, o in seen.items()]
    valid = {o['id'] for o in observations if o['quote_verified']}
    valid.update(g['id'] for g in packet.get('gaps', []) if isinstance(g, dict) and g.get('id'))
    actions = [r for r in rows if r.get('dim') == 'next_action']
    errors = []
    if len(actions) != 1:
        errors.append('Expected one unambiguous next action')
        action = {}
    else:
        action = actions[0]
    kind, query = _field(action, 'action'), str(_field(action, 'query')).strip()
    basis = [i.strip('[]') for i in re.split(r'[\s,;]+', str(_field(action, 'basis'))) if i]
    if kind not in ('search', 'stop'):
        errors.append('Unknown next action')
    if kind == 'search' and (not 3 <= len(query) <= 500 or not basis or set(basis) - valid
                             or not _field(action, 'gap') or not _field(action, 'expected_value')):
        errors.append('Search requires a focused query, verified observation or recorded gap, and expected value')
    if kind == 'search' and query.casefold() in {str(q).casefold() for q in packet.get('previous_queries', [])}:
        errors.append('The proposed search repeats an executed focus')
    return {'action': 'stop' if errors else kind, 'query': query if not errors and kind == 'search' else '',
            'reason': '; '.join(errors) if errors else action.get('finding', ''),
            'basis': basis, 'gap': _field(action, 'gap'), 'expected_value': _field(action, 'expected_value'),
            'observations': observations, 'validation_errors': errors,
            'status': 'experimental', 'quality_improvement_established': False}


def run(sources, *, packet, spend_cap_usd, method_sha256=None, call_fn=None):
    from src.dossier.engine_call import call_engine
    from src.executor.spend_guard import budget
    if not packet or not packet.get('question'):
        raise ValueError('Research feedback requires the original question and source context')
    state = {'cost_usd': 0.0}
    # The caller durably reserves this whole ceiling before the request. If the
    # connection is lost it must not assume the invocation was free or retry it.
    with budget(state, spend_cap_usd, lambda _: None):
        result = call_engine(ENGINE, sources, packet=packet, spend_cap_usd=spend_cap_usd,
                             expected_method_sha256=method_sha256, call_fn=call_fn)
    result['feedback_decision'] = decision(result, sources, packet)
    result['spend_reservations'] = state['spend_reservations']
    result['charged_or_reserved_usd'] = max(float(result.get('cost_usd') or 0), sum(
        r.get('cost_usd', r['ceiling_usd']) for r in state['spend_reservations']['attempts']))
    return result
