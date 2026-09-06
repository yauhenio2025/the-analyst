"""Third-queue output custody and actual-desk anchor/ID audit; no semantic decisions."""
from pathlib import Path
import json,re,shutil,sys,subprocess
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.study_third_queue import study as s
from src.dossier.common import analysis_ledger
from src.dossier.schemas import DossierJob
from src.sources.schemas import Document
from scripts.audit_corpus_methods_P1_P2_2026_09_06 import expanded_final_citations

def audit():
    plan=s.budget.read(s.OUT/'plan.json');s.guard(plan);records={};custody=[]
    orderp=s.OUT/'all_memos_before_scores.json';order=s.budget.read(orderp) if orderp.exists() else None
    for key,job in s.JOBS.items():
        rp=s.OUT/'results'/f'{key}.json'
        if not rp.exists():continue
        res=s.budget.read(rp)
        if res['status']!='complete':records[key]=res;continue
        p=s.OUT/'outputs'/f'{key}.md';content=p.read_text();sha=s.budget.digest(p.read_bytes())
        s.budget.require(sha==res['output_sha256'],'Changed output: '+key)
        computed=s.audit_one(key,content)
        s.budget.require(computed==res['audit'],'Changed mechanical result: '+key)
        prose,ledger=s.split_ledger(content)
        ledger=re.split(r'^#{2,4} (?:Rejected by the critic|Check receipt|Scope assessment)\b',ledger,flags=re.M)[0]
        rows=s.parse_rows(ledger);index=s.SourceIndex(s.documents(job))
        missing=[{'id':r.id,'suffix':a.suffix,'doc':a.doc} for r in rows for a in r.anchors if not index.find(a.quote,a.doc)]
        spec=s.get_operationalization_registry().get(job['engine']).process
        wall=s.verify_rows(rows,index,corpus_dimensions={d.key for d in spec.dimensions if d.scope=='corpus'})
        table='\n'.join(line for line in prose.splitlines() if line.lstrip().startswith('|'))
        eligible={r.id for r in rows if r.anchor_verified and r.status!='rejected'}
        bad_table=s.check_citations(table,eligible)
        view=DossierJob();view.analysis={'1.0':{'engine_key':job['engine'],'final_output':content}}
        desk=analysis_ledger(view,[Document(key=k,title=k,text=v) for k,v in s.documents(job).items()])
        dp=s.ARCHIVE/'desk_ledgers'/f'{key}.md';dp.parent.mkdir(exist_ok=True);dp.write_text(desk)
        desk_ids=set(re.findall(r'^- \[([^]]+)\]',desk.split('Rows whose anchors are unverified or incomplete')[0],re.M))
        bad_desk=sorted(expanded_final_citations(table)-desk_ids)
        scores={};binding=None
        for rater in ('sonnet','sol'):
            sp=s.OUT/'scores'/f'{key}__{rater}.json'
            if not sp.exists():continue
            binding=s.memo_binding(key);score=s.budget.read(sp)
            s.budget.require(score['binding']==binding and order['bindings'][key]==binding,'Score binding changed')
            committed=subprocess.check_output(['git','show',f"{order['commit']}:{binding['memo_path']}"],cwd=ROOT)
            s.budget.require(s.budget.digest(committed)==binding['memo_sha256'],'Pre-score memo changed')
            for cp in (s.OUT/'calls'/f'judge__{key}__{rater}').glob('*.json'):
                if '.prompt.' not in cp.name:s.budget.require(s.budget.read(cp)['started_at']>=order['prepared_at'],'Score predates source memo')
            scores[rater]=score['mean']
        records[key]={'status':'complete','output_sha256':sha,**computed,'supplied_spans_needing_existing_trimming':missing,
            'ineligible_table_ids':bad_table,'table_ids_not_citable_at_desk':bad_desk,'scores':scores,
            'inventory':s.DESIGNS[job['id']]['inventory'],'binding':binding,
            'process_steps':[c['step'] for c in res['process']['calls']],
            'mechanical_release_pass':not(wall.failed_ids or bad_table or bad_desk or computed['unknown_dimensions'])}
    for cp in sorted((s.OUT/'calls').glob('*/*.json')):
        if '.prompt.' in cp.name:continue
        call=s.budget.read(cp)
        if call['status']=='running':continue
        raw=cp.with_suffix('.md');prompt=cp.with_name(cp.stem+'.prompt.json')
        s.budget.require(s.budget.digest(raw.read_bytes())==call['output_sha256'],'Raw response changed')
        s.budget.require(s.budget.digest(s.budget.read(prompt))==call['prompt_sha256'],'Raw prompt changed')
        dest=s.ARCHIVE/'model_outputs'/cp.parent.name/raw.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(raw,dest)
        custody.append({'receipt':str(cp.relative_to(s.OUT)),'output':str(dest.relative_to(s.ARCHIVE)),
            'output_sha256':call['output_sha256'],'status':call['status']})
    report={'plan_identity':plan['identity'],'mechanics_only':True,'jobs':records,'costs':s.budget.costs(),'response_custody':custody}
    s.budget.write(s.ARCHIVE/'audit.json',report)
    s.export()
    print(json.dumps({'costs':report['costs'],'jobs':{k:{'status':v['status'],'rows':v.get('rows'),
        'mechanical_pass':v.get('mechanical_release_pass'),'bad_table':v.get('ineligible_table_ids'),
        'scores':v.get('scores')} for k,v in records.items()}},indent=2))
if __name__=='__main__':audit()
