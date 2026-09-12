"""Run the research program engine and return the research state and the Reporter's program with the engine result.

Stage S1 of the redesign, exposed on the light-call route so the Stacks can write the program before it commissions
discovery. The Stacks holds the thinker's bodies, so it performs the body scan for the program's phrases itself; this
wrapper returns the phrases and everything else the state carries."""
from __future__ import annotations

import json

from src.dossier.research_state import program_for_reporter, research_state_from_program

ENGINE = 'inquiry_program'


def _inventory_uids(sources) -> set[str] | None:
    for s in sources:
        if s.key == 'thinker-inventory' and s.text:
            try:
                rows = json.loads(s.text)
                return {r.get('uid') for r in rows if isinstance(r, dict) and r.get('uid')}
            except (ValueError, AttributeError):
                return None
    return None


def run(sources, *, packet, spend_cap_usd, method_sha256=None, call_fn=None, depth='surface', model=None):
    from src.dossier.engine_call import call_engine
    from src.executor.spend_guard import budget
    if not packet or not packet.get('question'):
        raise ValueError('The research program requires the question in the packet')
    scope = packet.get('scope') or {}
    state = {'cost_usd': 0.0}
    with budget(state, spend_cap_usd, lambda _: None):
        result = call_engine(ENGINE, sources, packet=packet, depth=depth, model=model, spend_cap_usd=spend_cap_usd,
                             expected_method_sha256=method_sha256, call_fn=call_fn)
    rs = research_state_from_program(result, question=packet['question'], hunch=scope.get('hunch') or '',
                                     leads=list(scope.get('leads') or []), good_answer=scope.get('good_answer') or '',
                                     thinker=((packet.get('author') or {}).get('name') or ''), inventory_uids=_inventory_uids(sources))
    result['research_state'] = rs.model_dump(mode='json')
    result['research_state_sha256'] = rs.sha256()
    result['program'] = program_for_reporter(rs)
    result['spend_reservations'] = state['spend_reservations']
    result['charged_or_reserved_usd'] = max(float(result.get('cost_usd') or 0), sum(
        r.get('cost_usd', r['ceiling_usd']) for r in state['spend_reservations']['attempts']))
    return result
