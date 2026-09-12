"""Recover a competing paid reading from an archived checkpoint, without replay."""
import copy
import hashlib
import json

from src.events.pricing import resolve_pricing


def recover_reading(state, receipt):
    """Return a reconciled state for an operator to save under job ownership.

    The current memo, evidence and selected reading remain authoritative. The
    competing reading stays separately inspectable and its charge is included
    in ordinary accounting and the durable budget ledger on future resumes.
    """
    digest = hashlib.sha256(json.dumps(receipt, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    attempt = receipt['attempt']
    ident, stage = attempt['id'], receipt['stage']
    previous = state.get('recovered_research', {}).get(ident)
    if previous:
        if previous['receipt_sha256'] != digest:
            raise ValueError('Recovered attempt identity already has different evidence')
        return state
    if receipt['packet_sha256'] != state['packet_sha256'] or not stage.startswith('read:'):
        raise ValueError('Recovery must belong to the same frozen reading packet')
    reading = receipt['reading']
    frozen = state['read_inputs'][stage]
    if reading['source_key'] != frozen['source_key'] or reading['body_sha256'] != frozen['body_sha256'] or reading['inspected_ranges'] != frozen['ranges']:
        raise ValueError('Recovered reading differs from the frozen source or inspected ranges')
    if receipt['method_receipt'] != state['call_input_manifests'][stage]['method_receipt']:
        raise ValueError('Recovered reading method differs from the frozen method')
    attempts = state['spend_reservations']['attempts']
    if any(a['id'] == ident for a in attempts):
        raise ValueError('Provider attempt is already accounted for')
    if not any(a['input_sha256'] == attempt['input_sha256'] for a in attempts):
        raise ValueError('Recovered attempt has no matching original model input')
    price = resolve_pricing(attempt['model'])
    if attempt['status'] != 'settled' or not price or not attempt.get('input_tokens') or not attempt.get('output_tokens'):
        raise ValueError('Recovery requires a settled provider-usage receipt')
    cost = round((attempt['input_tokens'] * price[0] + attempt['output_tokens'] * price[1]) / 1e6, 4)
    bound = round((attempt['input_tokens'] * price[0] * 2 + attempt['output_tokens'] * price[1]) / 1e6, 6)
    if abs(bound - attempt['cost_usd']) > .000001:
        raise ValueError('Configured prices do not reconcile the archived reservation')
    for evidence in receipt['evidence']:
        if evidence['source_key'] != reading['source_key'] or evidence['body_sha256'] != reading['body_sha256']:
            raise ValueError('Recovered evidence belongs to another source')
    record = copy.deepcopy(receipt)
    record.update(receipt_sha256=digest, cost_usd=cost, used_in_current_synthesis=False,
                  accounting_note='Competing reading recovered from a saved checkpoint; no new provider call.')
    result = {**state, 'cost_usd': round(state['cost_usd'] + cost, 4),
              'recovered_research': {**state.get('recovered_research', {}), ident: record},
              'spend_reservations': {**state['spend_reservations'], 'attempts': [*attempts, copy.deepcopy(attempt)]},
              'calls': {**state['calls'], 'recovered:' + ident: {
                  'engine_key': receipt['method_receipt']['engine_key'], 'model': attempt['model'], 'cost_usd': cost,
                  'recovered_research_id': ident, 'raw_provider_response_available': False,
                  'calls': [{'model_used': attempt['model'], 'input_tokens': attempt['input_tokens'],
                             'output_tokens': attempt['output_tokens'], 'cost_usd': cost, 'recovered': True}]}}}
    return result


def recover_saved_reading(job_id, receipt):
    from src.dossier.store import get_job, update_job
    from src.dossier.investigation import load_investigation, research_accounting, _json
    from src.dossier.blob_store import put_blob
    from src.dossier.execution_lock import investigation_owner, assert_owned
    from src.dossier.drain import is_draining
    from src.dossier import events
    terminal = {'done', 'failed', 'cancelled'}
    job = get_job(job_id)
    if job is None or job.status not in terminal:
        raise ValueError('Recover receipts only after the investigation has stopped')
    with investigation_owner(job_id, should_stop=is_draining):
        job = get_job(job_id)
        if job is None or job.status not in terminal:
            raise ValueError('Investigation resumed while receipt recovery was waiting')
        state = load_investigation(job_id)
        if not state:
            raise ValueError('No frozen investigation is available for receipt recovery')
        recovered = recover_reading(state, receipt)
        assert_owned(job_id)
        if recovered is not state:
            put_blob(f'investigation:{job_id}', 'application/json', _json(recovered).encode())
        # Rebuilding is safe even after a crash between blob and job persistence.
        receipts, accounting = research_accounting(recovered)
        update_job(job_id, analysis=recovered['analysis'], receipts=receipts,
                   totals=job.totals.model_copy(update=accounting))
        ident = receipt['attempt']['id']
        record = recovered['recovered_research'][ident]
        events.emit(job_id, 'note', phase='analysis', detail='Recovered an archived competing reading and reconciled its charge; no new research call.',
                    payload_json={'recovered_attempt_id': ident, 'receipt_sha256': record['receipt_sha256']})
        return {'job_id': job_id, 'attempt_id': ident, 'receipt_sha256': record['receipt_sha256'],
                'recovered_cost_usd': record['cost_usd'], 'total_cost_usd': recovered['cost_usd'],
                'already_recovered': recovered is state, 'current_memo_and_evidence_unchanged': True}


def redo_final_stages(job_id, from_stage="memo"):
    """Forget a stopped field investigation's memo stages and run them again under the current methods (2026-09-12): the readings
    and the adjudication stay paid; the job goes back to its analysis step and resumes. Returns what was forgotten."""
    from src.dossier.store import get_job, update_job
    from src.dossier.investigation import load_investigation, research_accounting, _json
    from src.dossier.field_investigation import forget_final_stages
    from src.dossier.blob_store import put_blob
    from src.dossier.execution_lock import investigation_owner, assert_owned
    from src.dossier.drain import is_draining
    from src.dossier import events, runner
    terminal = {'done', 'failed', 'cancelled'}
    job = get_job(job_id)
    if job is None or job.status not in terminal:
        raise ValueError('Redo the memo only after the investigation has stopped')
    with investigation_owner(job_id, should_stop=is_draining):
        job = get_job(job_id)
        if job is None or job.status not in terminal:
            raise ValueError('Investigation resumed while the redo was waiting')
        state = load_investigation(job_id)
        if not state or state.get('kind') != 'field_investigation':
            raise ValueError('No frozen field investigation is available to redo')
        state = forget_final_stages(state, from_stage)
        assert_owned(job_id)
        put_blob(f'investigation:{job_id}', 'application/json', _json(state).encode())
        receipts, accounting = research_accounting(state)
        update_job(job_id, analysis=state['analysis'], receipts=receipts, totals=job.totals.model_copy(update=accounting),
                   status=runner.STATUS_FOR_STEP['analysis'], step='analysis', error=None)
        redo = state['redo'][-1]
        events.emit(job_id, 'note', phase='analysis', detail=f"redo from {from_stage}: {len(redo['forgotten_calls'])} memo calls forgotten; the readings and the adjudication are reused",
                    payload_json={'redo': redo})
    started = runner.resume(job_id)
    return {'job_id': job_id, 'from_stage': from_stage, 'forgotten_calls': redo['forgotten_calls'], 'resumed': started}
