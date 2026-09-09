"""Lossless support identity transport; relevance and selection remain method judgments."""
from __future__ import annotations

import json
import re


def support_route(outputs, evidence, inherited=()):
    """Union structured support with exact, verified citations in the supplied prose.

    A global summary cannot silently erase support used by a batch. This only
    makes original findings eligible for synthesis; it does not endorse a claim.
    """
    known = {e['citation_id'] for e in evidence if e.get('quote_verified')}
    origins = {eid: ['upstream_support'] for eid in inherited if eid in known}
    rejected = set()
    for index, result in enumerate(outputs):
        structured = set()
        for row in result.get('rows', []):
            value = (row.get('fields') or {}).get('evidence_ids') or []
            structured.update(str(i).strip('[]') for i in
                              (value if isinstance(value, list) else re.split(r'[\s,;]+', value)) if i)
        rejected.update(structured - known)
        prose = '\n'.join(str(result.get(k) or '') for k in ('prose', 'final_output'))
        for eid in sorted(known):
            reasons = []
            if eid in structured:
                reasons.append(f'{index + 1}:ledger')
            if re.search(r'(?<![\w:./-])' + re.escape(eid) + r'(?![\w./-])', prose):
                reasons.append(f'{index + 1}:prose')
            if reasons:
                origins.setdefault(eid, []).extend(reasons)
    return {'version': 1, 'eligible_ids': sorted(origins), 'origins': origins,
            'rejected_structured_ids': sorted(rejected),
            'unreferenced_verified_ids': sorted(known - origins.keys()),
            'policy': 'verified ledger and exact prose citations, retaining upstream support'}


def selection_groups(rows, allowed):
    """Retain all rationales; conflicting dispositions require explicit reconciliation."""
    groups = {}
    for row in rows:
        fields = row.get('fields') or {}
        uid, decision = str(fields.get('uid', '')), fields.get('decision')
        if uid not in allowed or decision not in ('read', 'context', 'defer', 'unavailable'):
            continue
        group = groups.setdefault(uid, [])
        if row not in group:
            group.append(row)
    out = {}
    for uid, variants in groups.items():
        dispositions = {r['fields']['decision'] for r in variants}
        conflict = len(dispositions) != 1
        # Preserve the model's order for ranking, but never use that order to
        # settle contradictory dispositions for the same work.
        out[uid] = {**variants[0], 'uid': uid,
                    'decision': 'conflict' if conflict else next(iter(dispositions)),
                    'reason': ' | '.join(dict.fromkeys(str(r['fields'].get('reason', '')) for r in variants)),
                    'decision_variants': variants, 'selection_conflict': conflict}
    return out


def canonical_evidence(entries):
    """One support identity per finding; duplicate/ambiguous rows remain in receipts."""
    groups = {}
    for entry in entries:
        groups.setdefault(entry['citation_id'], []).append(entry)
    canonical, receipts = [], []
    for eid, variants in groups.items():
        verified = [e for e in variants if e.get('quote_verified')]
        signatures = {json.dumps({k: e.get(k) for k in ('doc', 'finding', 'anchor', 'fields')},
                                 sort_keys=True, ensure_ascii=False) for e in verified}
        conflict = len(signatures) > 1
        chosen = dict((verified or variants)[0])
        if conflict:
            chosen.update(quote_verified=False, anchor_verified=False, conjecture=True,
                          evidence_identity_conflict=True)
        canonical.append(chosen)
        if len(variants) > 1:
            receipts.append({'citation_id': eid, 'variants': variants, 'conflict': conflict,
                             'resolution': 'unresolved' if conflict else 'verified rendition' if verified else 'unverified'})
    return canonical, receipts
