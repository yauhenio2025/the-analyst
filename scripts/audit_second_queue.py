"""Read-only audit of the second queue: bytes, anchors, IDs, receipts and ordering.

This does not assess interpretation, completeness of a quotation's meaning, or
whether a table cell is supported. Those judgments belong in the source memos.
"""
from collections import Counter
import json
import re
from pathlib import Path
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import study_second_queue as s


def audit():
    plan=s.budget.read(s.OUT/'plan.json'); s.guard(plan)
    costs=s.budget.costs()
    errors=[]; jobs={}
    if costs['known_usd']+costs['reserved_usd']>12: errors.append('Budget exceeded')
    before=s.OUT/'all_memos_before_scores.json'
    binding=s.budget.read(before) if before.exists() else None
    for key,job in s.JOBS.items():
        path=s.OUT/'results'/f'{key}.json'
        if not path.exists(): jobs[key]={'status':'pending'};continue
        result=s.budget.read(path)
        if result['status']!='complete': jobs[key]={'status':'failed','error':result['error']};continue
        content=(s.OUT/'outputs'/f'{key}.md').read_text()
        sha=s.budget.digest(content.encode())
        if sha!=result['output_sha256']:errors.append(f'{key}: output hash changed')
        computed=s.audit_one(key,content)
        if computed!=result['audit']:errors.append(f'{key}: mechanical audit changed')
        prose,ledger=s.split_ledger(content)
        rows=s.parse_rows(ledger.split('### Rejected by the critic')[0].split('## Scope assessment')[0])
        final=result.get('process',{}).get('final_wall',{})
        calls=result.get('process',{}).get('calls',[])
        memo=s.ARCHIVE/'source_memos'/f'{key}.md'
        entry={'status':'complete','output_sha256':sha,'characters':len(content),'words':len(content.split()),
            **computed,'rows_without_dimension':sum(not r.dim for r in rows),
            'source_anchor_counts':dict(Counter(a.doc or 'doc' for r in rows for a in r.anchors)),
            'final_missing_lineage':final.get('missing_lineage'),
            'production_missing_cited':final.get('missing_cited'),
            'inline_rejected_ids':sorted(set(re.findall(r'\[([^\]\s,]+), rejected by the check\]',prose))),
            'production_citation_check':final.get('citation_check'),
            'ruling_coverage':final.get('check_ruling_coverage'),
            'scope_outcomes':dict(Counter(r.get('outcome') for r in final.get('scope_outcomes',[]))),
            'process_steps':len(calls),'memo_present_and_bound':memo.exists() and sha in memo.read_text(),
            'scores':{}}
        for rater in ('sonnet','sol'):
            sp=s.OUT/'scores'/f'{key}__{rater}.json'
            if not sp.exists():continue
            score=s.budget.read(sp);entry['scores'][rater]=score['mean']
            if not binding:errors.append(f'{key}: scored without pre-score manifest');continue
            frozen=binding['bindings'][key]
            if score['binding']!=frozen:errors.append(f'{key}: score binding differs')
            committed=subprocess.check_output(['git','show',f"{binding['commit']}:{frozen['memo_path']}"],cwd=s.ROOT)
            if s.budget.digest(committed)!=frozen['memo_sha256'] or sha not in committed.decode():
                errors.append(f'{key}: committed memo/output binding differs')
            for cp in (s.OUT/'calls'/f'judge__{key}__{rater}').glob('*.json'):
                if '.prompt.' in cp.name:continue
                call=s.budget.read(cp)
                if call['started_at']<binding['prepared_at']:errors.append(f'{key}: judge predates source memo manifest')
        jobs[key]=entry
    report={'plan_identity':plan['identity'],'costs':costs,'mechanics_only':True,
        'counts':dict(Counter(j['status'] for j in jobs.values())),
        'source_memos':sum(j.get('memo_present_and_bound',False) for j in jobs.values()),
        'scores':sum(len(j.get('scores',{})) for j in jobs.values()),'errors':errors,'jobs':jobs}
    s.budget.write(s.ARCHIVE/'audit.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='jobs'},indent=2))
    if errors:raise SystemExit(1)

if __name__=='__main__':audit()
