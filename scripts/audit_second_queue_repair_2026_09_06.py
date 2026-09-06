"""Read-only custody, anchor and ID audit; semantic release decisions stay in source memos."""
import json
from pathlib import Path
import re
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.study_second_queue_repair_2026_09_06 import study as s
from src.dossier.common import analysis_ledger
from src.dossier.schemas import DossierJob
from src.sources.schemas import Document
from scripts.audit_corpus_methods_P1_P2_2026_09_06 import expanded_final_citations


def audit():
    plan=s.budget.read(s.OUT/'plan.json');s.guard(plan)
    order_path=s.OUT/'all_memos_before_scores.json'
    order=s.budget.read(order_path) if order_path.exists() else None
    errors=[];jobs={}
    for key,job in s.JOBS.items():
        rp=s.OUT/'results'/f'{key}.json'
        if not rp.exists():errors.append(key+': missing result');continue
        result=s.budget.read(rp)
        if result['status']!='complete':
            jobs[key]={'status':result['status'],'error':result.get('error')};errors.append(key+': failed');continue
        p=s.OUT/'outputs'/f'{key}.md';content=p.read_text();sha=s.budget.digest(p.read_bytes())
        if sha!=result['output_sha256']:errors.append(key+': changed output')
        computed=s.audit_one(key,content)
        if computed!=result['audit']:errors.append(key+': changed mechanical audit')
        prose,ledger=s.split_ledger(content);rows=s.parse_rows(ledger)
        index=s.SourceIndex(s.documents(job))
        supplied_missing=[{'id':r.id,'suffix':a.suffix,'doc':a.doc} for r in rows for a in r.anchors if not index.find(a.quote,a.doc)]
        spec=s.get_operationalization_registry().get(job['engine']).process
        wall=s.verify_rows(rows,index,corpus_dimensions={d.key for d in spec.dimensions if d.scope=='corpus'})
        table='\n'.join(line for line in content.splitlines() if line.lstrip().startswith('|'))
        eligible={r.id for r in rows if r.anchor_verified and r.status!='rejected'}
        bad_table=s.check_citations(table,eligible)
        if wall.failed_ids or bad_table:errors.append(key+': unverified/rejected table evidence')
        view=DossierJob();view.analysis={'1.0':{'engine_key':job['engine'],'final_output':content}}
        desk=analysis_ledger(view,[Document(key=k,title=k,text=v) for k,v in s.documents(job).items()])
        desk_path=s.ARCHIVE/'desk_ledgers'/f'{key}.md';desk_path.parent.mkdir(exist_ok=True);desk_path.write_text(desk)
        desk_ids=set(re.findall(r'^- \[([^]]+)\]',desk.split('Rows whose anchors are unverified or incomplete')[0],re.M))
        bad_desk=sorted(expanded_final_citations(table)-desk_ids)
        if bad_desk:errors.append(key+': table evidence not citable at desk')
        binding=s.memo_binding(key)
        scores={}
        for rater in ('sonnet','sol'):
            sp=s.OUT/'scores'/f'{key}__{rater}.json'
            if not sp.exists():errors.append(key+'/'+rater+': missing score');continue
            score=s.budget.read(sp);scores[rater]=score['mean']
            if score['binding']!=binding or not order or order['bindings'][key]!=binding:
                errors.append(key+'/'+rater+': binding mismatch');continue
            memo=subprocess.check_output(['git','show',f"{order['commit']}:{binding['memo_path']}"],cwd=ROOT)
            if s.budget.digest(memo)!=binding['memo_sha256']:errors.append(key+': committed memo changed')
            for cp in (s.OUT/'calls'/f'judge__{key}__{rater}').glob('*.json'):
                if '.prompt.' not in cp.name and s.budget.read(cp)['started_at']<order['prepared_at']:
                    errors.append(key+': score predates memo manifest')
        original={}
        for rater in ('sonnet','sol'):
            op=ROOT/'communications/study/second_queue_2026_09_06/scores'/f'{job["id"]}__old__{job["papers"][0]}__{rater}.json'
            if op.exists():original[rater]=s.budget.read(op)['mean']
        supplement=s.OUT/'baseline_scores/A3__old__aukus__sonnet.json'
        baseline_supplement=s.budget.read(supplement) if job['id']=='A3' and supplement.exists() else None
        jobs[key]={'status':'complete','output_sha256':sha,**computed,'supplied_anchors_needing_existing_wall_trimming':supplied_missing,
                   'ineligible_table_ids':bad_table,'scores':scores,'frozen_original_scores':original,
                   'supplemental_original_sonnet_mean':baseline_supplement['mean'] if baseline_supplement else None,
                   'desk_citable_ids':sorted(desk_ids),'table_ids_not_citable_at_desk':bad_desk,
                   'inventory_exception':job['id'] in ('A6','C1','E12','S3'),
                   'source_memo':binding['memo_path'],'process_steps':[c['step'] for c in result['process']['calls']]}
    c=s.budget.costs();review=s.budget.read(s.ARCHIVE/'claude_review_receipt.json')
    report={'plan_identity':plan['identity'],'jobs':jobs,'costs':c,'direct_claude_review_usd':review['cost_usd'],
            'known_round_usd':round(c['known_usd']+review['cost_usd'],6),
            'monetary_guidance_usd':10,'guidance_is_gate':False,'terminated_cli_cost':'unknown; no usage receipt',
            'mechanics_only':True,'errors':errors}
    s.budget.write(s.ARCHIVE/'audit.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='jobs'},indent=2))
    if errors:raise SystemExit(1)

if __name__=='__main__':audit()
