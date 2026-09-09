"""Replay production helpers on an immutable investigation archive, without providers.

python3 -m tools.replay_research_reliability --archive PATH --out RECEIPT.json
Only the body-free receipt is written. The archive is read-only.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from src.dossier.evidence_routing import canonical_evidence, selection_groups, support_route
from src.dossier.explainer import rows_with_fields
from src.dossier.investigation import quote_span


def replay(archive):
    names = ('analyst-investigation.json', 'analyst-job.json')
    hashes = {name: hashlib.sha256((archive / name).read_bytes()).hexdigest() for name in names}
    state, job = [json.loads((archive / name).read_text()) for name in names]
    packet = json.loads(job['sources'][0]['text'])
    bodies = {r['uid']: r['body'] for role in ('field', 'primary') for r in packet[role]}
    phases = {p['stage']: p for p in job['analysis'].values()}
    field = [e for e in state['evidence'] if e['source_role'] == 'field']
    first = support_route(state['field_maps'], field)
    last = support_route([state['field_map']], field, first['eligible_ids'])
    baseline = set(state['call_input_manifests']['field_map']['evidence_ids'])
    groups = selection_groups(state['selection']['rows'], {r['uid'] for r in state['inventory']})
    recovered, counts = [], Counter()
    for e in state['evidence']:
        parsed = [r for r in rows_with_fields(phases['read:' + e['source_key']]['final_output'])
                  if r['id'] == e['id'] and r['doc'] == e['doc'] and r['dim'] == 'evidence']
        candidate = dict(e)
        if len(parsed) == 1:
            quote = parsed[0]['anchor']
            span = quote_span(quote, bodies[e['uid']], state['read_inputs']['read:' + e['source_key']]['ranges'])
            valid = bool(span) and e['doc'] == e['source_key'] and parsed[0]['fields'].get('uid', '') in ('', e['uid'])
            if valid and not e['quote_verified']:
                counts['literal_spans_recovered'] += 1
                candidate.update(quote_verified=True, anchor=quote, quote=quote)
        recovered.append(candidate)
    canonical, duplicates = canonical_evidence(recovered)
    for name, digest in hashes.items():
        assert hashlib.sha256((archive / name).read_bytes()).hexdigest() == digest
    return {'paid_calls': 0, 'archive_sha256': hashes,
            'historical_batch_support_count': len(baseline),
            'corrected_batch_support_count': len(first['eligible_ids']),
            'batch_order_invariant': first['eligible_ids'] == support_route(state['field_maps'][::-1], field)['eligible_ids'],
            'restored_support_ids': sorted(set(first['eligible_ids']) - baseline),
            'final_support_ids': last['eligible_ids'],
            'selection_conflicts': {uid: sorted({r['fields']['decision'] for r in g['decision_variants']})
                                    for uid, g in groups.items() if g['selection_conflict']},
            **counts, 'historical_evidence_rows': len(recovered), 'canonical_evidence_rows': len(canonical),
            'duplicate_identities': len(duplicates),
            'unresolved_identity_conflicts': [r['citation_id'] for r in duplicates if r['conflict']],
            'quality_comparison': 'Not run; no regenerated answer or quality score is implied.'}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    if args.out.resolve().is_relative_to(args.archive.resolve()):
        ap.error('write the receipt outside the immutable archive')
    receipt = replay(args.archive)
    args.out.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: v for k, v in receipt.items() if not k.endswith('_ids')}, indent=2))
