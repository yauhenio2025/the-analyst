"""Four same-evidence continuations; dry by default, one shared approved $8 cap.

Original readings/selection stay fixed. Only support eligibility and batch order
vary. Private inputs, responses, frozen methods and spend reservations are saved.
No discovery, added originals, automatic retries, model fallback or model judging.
"""
from __future__ import annotations

import argparse
import copy
import fcntl
import hashlib
import json
import random
import subprocess
from pathlib import Path

from src.dossier.context_packing import input_chars, input_hash, pack_final_context
from src.dossier.evidence_routing import canonical_evidence, support_route
from src.dossier.field_investigation import _baseline_context, _ids, _memo_validation, validate_claims
from src.dossier.investigation import _context, _excerpt, _spec, recover_answer_rows
from src.dossier.reporter_context import pack_reporter_context
from src.engines.methods import freeze_method, method_receipt
from src.executor.spend_guard import budget
from src.sources.field_investigation import expand_field_investigation

MODEL = 'openrouter/openai/gpt-5.6-sol'
CAP = 8.0
OUTPUT_TOKENS = 16000
KEYS = {'field_map': 'field_investigation_field_map', 'adjudication': 'field_investigation_adjudicate',
        'memo': 'field_investigation_memo'}


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(encoded(value).encode()).hexdigest()


def write(path, value):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temp.replace(path)


def charged(state):
    ledger = state.get('spend_reservations', {})
    return max(state['cost_usd'], ledger.get('base_cost_usd', 0) +
               sum(r.get('cost_usd', r['ceiling_usd']) for r in ledger.get('attempts', [])))


def routes(outputs, evidence, treatment, inherited=()):
    if treatment == 'union':
        return support_route(outputs, evidence, inherited)['eligible_ids']
    known = {e['citation_id'] for e in evidence if e['quote_verified']}
    return sorted({i for output in outputs for row in output.get('rows', [])
                   for i in _ids((row.get('fields') or {}).get('evidence_ids'))} & known)


def load_case(archive):
    raw = {name: (archive / name).read_bytes() for name in ('analyst-investigation.json', 'analyst-job.json')}
    original, job = [json.loads(v) for v in raw.values()]
    docs = expand_field_investigation(job['sources'][0]['text'])
    packet = json.loads(next(d.text for d in docs if d.role == 'plan' and d.key == 'investigation'))
    bodies = {d.key: d.text for d in docs if d.role == 'source'}
    # Use the current executor's prior-context policy, identically in all arms,
    # with the saved plan's queries. Whole prior records remain in the archive.
    context = [c for c in _context(packet, bodies, cap=40000, queries=original['queries'])
               if c['key'] != 'prior_investigations' and c['selected_for_context']]
    baseline = _baseline_context(packet)
    ranges = [(0, len(baseline))] if len(baseline) <= 200000 else [(0, 100000), (len(baseline)-100000, len(baseline))]
    context.append({'key': 'prior_investigations', 'kind': 'prior_investigations', 'title': 'Prior investigation baseline',
                    'inspected_ranges': ranges, 'truncated': len(baseline) > 200000,
                    'text': _excerpt(baseline, ranges), 'selected_for_context': True})
    evidence_fields = {'citation_id', 'uid', 'source_key', 'source_role', 'finding', 'source_quote', 'quote_verified',
                       'conjecture', 'quote_start', 'quote_end', 'quote_match', 'quote_layout', 'pages', 'page_urls',
                       'title', 'year', 'fields'}
    canonical, identity_receipts = canonical_evidence(original['evidence'])
    evidence = [{k: v for k, v in e.items() if k in evidence_fields} for e in canonical]
    readings = [{k: r[k] for k in ('uid', 'title', 'source_role', 'year', 'reading', 'source_metadata',
                                  'inspected_ranges', 'reading_mode') if k in r}
                for r in original['readings'] if r['source_role'] == 'primary']
    common = {k: original[k] for k in ('author', 'question', 'scope', 'field_collections', 'field_gaps', 'mode', 'as_of')}
    common['inquiry_type'] = 'bilateral'
    return {'original': original, 'packet': packet, 'context': context, 'evidence': evidence,
            'primary_readings': readings, 'common': common, 'identity_receipts': identity_receipts,
            'archive_sha256': {k: hashlib.sha256(v).hexdigest() for k, v in raw.items()}}


def prepare(case, arm, stage, previous):
    original, evidence = case['original'], case['evidence']
    field = [e for e in evidence if e['source_role'] == 'field']
    maps = original['field_maps'][::-1] if arm['reverse'] else original['field_maps']
    batch_ids = routes(maps, field, arm['routing'])
    common = copy.deepcopy(case['common'])
    if stage == 'field_map':
        ids = batch_ids
        sources = [_spec('field-map-batches', encoded([m['final_output'] for m in maps]))]
        upstream = {**common, 'plan': original['plan']['final_output'], 'map_scope': 'global_reconciliation',
                    'evidence': [e for e in field if e['citation_id'] in ids],
                    'evidence_selection': 'verified field supports retained for this stage',
                    'field_evidence_total': len(field), 'full_readings_retained': True,
                    'source_catalog': [{'uid': r['uid'], 'title': r.get('title')} for r in case['packet']['field']]}
    else:
        field_map = previous['field_map']
        ids = routes([field_map], field, arm['routing'], batch_ids)
        sources = [_spec('field-argument-map', field_map['final_output']),
                   _spec('primary-readings', encoded(case['primary_readings']))]
        upstream = {**common, 'coverage': original['coverage'], 'field_map': field_map['final_output'],
                    'evidence': [e for e in evidence if e['source_role'] == 'primary' or e['citation_id'] in ids],
                    'evidence_selection': 'all primary evidence plus verified field supports retained for this stage',
                    'field_evidence_total': len(field), 'full_field_evidence_retained': True,
                    'prior_context': case['context']}
        if stage == 'memo':
            upstream['adjudication'] = previous['adjudication']['final_output']
    upstream = copy.deepcopy(upstream)
    sources, upstream, reporter = pack_reporter_context(stage, sources, upstream, packet_sha256=original['packet_sha256'])
    sources, upstream, packing = pack_final_context(stage, sources, upstream, packet_sha256=original['packet_sha256'])
    representation = 'quotations'
    if stage == 'field_map' and input_chars(sources, upstream) > 520000:
        upstream['evidence'] = [{k: e[k] for k in ('citation_id', 'source_role', 'quote_verified')} for e in upstream['evidence']]
        upstream['field_evidence_representation'] = 'reference_index_to_supplied_argument_maps'
        representation = 'reference_index'
    if input_chars(sources, upstream) > 640000:
        raise ValueError(f'Prepared input ({input_chars(sources, upstream):,} chars) exceeds the production guard')
    manifest = {'stage': stage, 'input_sha256': input_hash(sources, upstream), 'chars': input_chars(sources, upstream),
                'eligible_ids': ids, 'representation': representation, 'reporter_packing': reporter, 'packing': packing}
    return sources, upstream, manifest


def run(case, state, out, call):
    def save(_=None):
        write(out / 'state.json', state)
    for label in state['order']:
        arm = state['arms'][label]
        for stage, key in KEYS.items():
            record = arm.setdefault('stages', {}).get(stage)
            if record:
                if record['status'] != 'complete':
                    raise ValueError('A prior invocation is incomplete; inspect and reconcile it before any continuation')
                continue
            previous = {k: v['response'] for k, v in arm['stages'].items()}
            sources, upstream, manifest = prepare(case, arm, stage, previous)
            record = arm['stages'][stage] = {'status': 'prepared', 'input_manifest': manifest}
            write(out / f'{label}-{stage}-input.json', {'sources': [s.model_dump(mode='json') for s in sources],
                                                      'packet': upstream, 'method': state['methods'][key]})
            save()
            remaining = CAP - charged(state)
            if remaining <= 0:
                raise ValueError('The shared trial cap is exhausted')
            record['status'] = 'invoking'
            save()
            try:
                with budget(state, CAP, save):
                    response = call(key, sources, packet=upstream, depth='surface', model=MODEL,
                                    spend_cap_usd=remaining, max_chars=650000, method_snapshot=state['methods'][key])
                recover_answer_rows(response)
                record['response'] = response
                state['cost_usd'] += float(response.get('cost_usd') or 0)
                # Production validates against the frozen, actually read originals.
                # A map may legitimately retain support cited in a supplied batch
                # even when the old structured filter omitted its quotation.
                supplied = case.get('evidence', upstream['evidence'])
                if stage == 'memo':
                    prose, _, validation = _memo_validation(response, supplied, case['original']['mode'])
                    (out / f'{label}-memo.md').write_text(prose + '\n')
                else:
                    validation = validate_claims(response['rows'], supplied, required=True, field_map=stage == 'field_map')
                record.update(status='complete', validation=validation)
                if not validation['supported']:
                    record['status'] = 'unsupported_draft'
                    save()
                    raise ValueError('A support check failed; draft retained without an unplanned repair')
                save()
                print(encoded({'arm': label, 'stage': stage, 'cost_usd': state['cost_usd'],
                               'charged_or_reserved_usd': charged(state)}), flush=True)
            except Exception as exc:
                record['error'] = type(exc).__name__ + ': ' + str(exc)
                state['status'] = 'stopped'
                save()
                raise
    state['status'] = 'complete'
    save()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--execute-approved-8-usd', action='store_true')
    args = ap.parse_args()
    if args.out.resolve().is_relative_to(args.archive.resolve()):
        ap.error('Output must be outside the immutable archive')
    args.out.mkdir(parents=True, exist_ok=True, mode=0o700)
    args.out.chmod(0o700)
    with (args.out / '.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        case = load_case(args.archive)
        state_path = args.out / 'state.json'
        state = json.loads(state_path.read_text()) if state_path.exists() else None
        if state is None:
            randomizer = random.Random(20260910)
            arms, order = {}, []
            for reverse in (False, True):
                choices = ['baseline', 'union']; randomizer.shuffle(choices)
                for routing in choices:
                    label = f'Answer-{len(arms)+1}'
                    arms[label] = {'routing': routing, 'reverse': reverse, 'stages': {}}
                    order.append(label)
            state = {'version': 1, 'status': 'prepared', 'cost_usd': 0, 'cap_usd': CAP, 'model': MODEL,
                     'output_token_limit': OUTPUT_TOKENS, 'archive_sha256': case['archive_sha256'],
                     'methods': {key: freeze_method(key) for key in KEYS.values()}, 'arms': arms, 'order': order,
                     'selection_fixed': case['original']['selected_primary_uids'],
                     'code_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                     'context_policy': 'saved_plan_queries_using_current_executor_policy',
                     'evidence_policy': 'canonical original identities, same in all arms; no additional quote verification',
                     'method_note': 'Current central methods/composer fixed for every arm; historical reads and source selection unchanged.'}
        if state['archive_sha256'] != case['archive_sha256']:
            raise ValueError('The original archive changed')
        write(state_path, state)
        previews = {label: prepare(case, arm, 'field_map', {})[2] for label, arm in state['arms'].items()}
        write(args.out / 'preflight.json', {'model': MODEL, 'cap_usd': CAP, 'arms': previews,
                                          'method_receipts': [method_receipt(m) for m in state['methods'].values()]})
        print(encoded({'preflight': 'ready', 'arms': {k: {'chars': v['chars'], 'supports': len(v['eligible_ids'])}
                                                     for k,v in previews.items()}}), flush=True)
        if not args.execute_approved_8_usd:
            return
        from src.dossier.engine_call import call_engine
        from src.executor import engine_runner
        from src.executor.output_budget import limit
        from src.executor.process_runner import _default_call
        from dotenv import load_dotenv
        load_dotenv('/home/evgeny/projects/the-analyst/.env', override=False)
        engine_runner.MAX_RETRIES = 1  # Isolated trial process; never changes a deployed service.
        engine_runner.FALLBACK_MODEL = MODEL
        def provider(system_prompt, user_message, **kwargs):
            if kwargs.get('model_hint') != MODEL:
                raise ValueError('This trial authorizes only the pinned model')
            requests = state.setdefault('provider_requests', [])
            number = len(requests) + 1
            name = f'provider-{number:02d}'
            requests.append({'file': name, 'status': 'invoking'})
            write(args.out / (name + '-request.json'), {'system': system_prompt, 'user': user_message,
                  'options': {k:v for k,v in kwargs.items() if k != 'cancellation_check'}, 'max_output_tokens': OUTPUT_TOKENS})
            write(state_path, state)
            result = _default_call(system_prompt, user_message, **kwargs)
            write(args.out / (name + '-response.json'), result)
            requests[-1]['status'] = 'returned'
            write(state_path, state)
            return result
        def invoke(key, sources, **kwargs):
            return call_engine(key, sources, call_fn=provider, **kwargs)
        with limit(OUTPUT_TOKENS):
            run(case, state, args.out, invoke)
        assert case['archive_sha256'] == load_case(args.archive)['archive_sha256']


if __name__ == '__main__':
    main()
