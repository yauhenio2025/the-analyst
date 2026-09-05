"""Second-queue PLAN adapter to study_first_queue; USD12 includes generation and scores.

Use the existing P1/P2 no-retry recorder for admission and receipts. Production
process calls are unchanged. Freeze -> generate -> source-read memos -> score.
No paid replay, auto fallback or head-to-head. --export saves reviewable artifacts.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import fcntl
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import yaml
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from scripts import study_first_queue as first
from scripts import study_corpus_methods_P1_P2_2026_09_06 as budget
from src.executor.context_broker import split_ledger
from src.executor.ledger_walls import SourceIndex, parse_rows, verify_rows, check_citations
from src.engines.registry import get_engine_registry
from src.engines.schemas_v2 import CapabilityEngineDefinition
from src.operationalizations.registry import get_operationalization_registry
from src.executor.process_runner import run_process, run_oneshot_checked
from src.llm.client import parse_llm_json_response

ARCHIVE=ROOT/'communications/study/second_queue_2026_09_06'
OUT=ROOT/'data/study/second_queue_2026_09_06'
DESIGNS=json.loads((ARCHIVE/'designs.json').read_text())
PAPERS={**first.PAPERS,'chen':first.IDEAS/'chen2025_progress_without_progress_jaeggi.txt',
    'religion2001':first.IDEAS/'deutschmann2001_capitalism_as_religion.md',
    'religion2022':first.IDEAS/'deutschmann2022_interpretation_of_capitalism_as_religion.md',
    'technique':first.IDEAS/'castoriadis1984_technique.md','rationality':first.IDEAS/'castoriadis1997_rationality_of_capitalism.md'}
# Same PLAN pattern: named materials, original control where it exists, conditions per engine.
PLAN={
 'G2':(['technique','rationality'],False,['dvs','checked']),
 'G3':(['religion2001','religion2022'],False,['dvs','checked']),
 'G4':(['promise','religion2022'],False,['dvs','checked']),
 'A4':(['harris','hegel'],True,['checked','old']),
 'A5':(['elling','zambrana'],True,['checked','old']),
 'A6':(['elling','chen'],True,['checked','old']),
 'C1':(['zambrana','hegel'],True,['checked','old']),
 'C6':(['aukus','chen'],True,['checked','old']),
 'S3':(['promise','subsea'],True,['checked','old']),
 'E12':(['aukus','promise'],True,['checked','old']),
 'A3':(['harris','aukus'],True,['checked','old']),
}
JOBS={}
for ident,(papers,old,conditions) in PLAN.items():
    sets=[papers] if ident.startswith('G') else [[p] for p in papers]
    for material in sets:
        for condition in conditions:
            key=f'{ident}__{condition}__'+('_'.join(material) if len(material)>1 else material[0])
            JOBS[key]={'id':ident,'engine':DESIGNS[ident]['key'],'papers':material,'condition':condition}
MODELS=budget.MODELS
RUBRIC=budget.RUBRIC.replace('usefulness: the requested comparison/reconciliation tables can be lifted, with honest missing/incommensurable cells;',
 'usefulness: the requested reading or inventory and its tables help a reader with these texts open; inventories need accurate useful coverage, not a compulsory novel thesis;')
# Reuse frozen-price accounting, with enough room for DeepSeek reasoning and bounded reader/rater outputs.
budget.OUT=OUT; budget.CAP=12.0
budget.LIMITS={'cheap':6000,'mid':32000,'strong':14000,'sonnet':1800,'sol':1800}

def inputs():
    paths=[Path(__file__).resolve(),ARCHIVE/'designs.json',ROOT/'communications/study/PROTOCOL_second_queue_2026-09-06.md',ROOT/'scripts/study_first_queue.py',
        ROOT/'scripts/study_two_engines.py',ROOT/'scripts/study_corpus_methods_P1_P2_2026_09_06.py']
    paths += [ROOT/f'src/{folder}/{d["key"]}.yaml' for d in DESIGNS.values() for folder in ('engines/capability_definitions','operationalizations/definitions')]
    paths += list((ARCHIVE/'original_capabilities').glob('*.yaml'))
    # Include transitive production code to detect concurrent plumbing changes before any new purchase.
    paths += [p for directory in ('src/executor','src/stages','src/operationalizations','src/engines','src/dossier','src/llm','src/events') for p in (ROOT/directory).glob('*.py')]
    paths += [PAPERS[p] for j in JOBS.values() for p in j['papers']]
    return sorted(set(paths))

def freeze():
    budget.require(not (OUT/'plan.json').exists(),'Plan already exists')
    plan={'cap_usd':budget.CAP,'jobs':JOBS,'models':MODELS,'prices':budget.PRICES,'output_limits':budget.LIMITS,
        'rubric':RUBRIC,'frozen_at':time.time(),'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'inputs':{str(p.relative_to(ROOT)):budget.digest(p.read_bytes()) for p in inputs()}}
    plan['identity']=budget.digest(plan);budget.write(OUT/'plan.json',plan)
    print(json.dumps({'identity':plan['identity'],'jobs':len(JOBS),'cap_usd':budget.CAP}))

def guard(plan):
    budget.require(plan['identity']==budget.digest({k:v for k,v in plan.items() if k!='identity'}),'Plan changed')
    for key,val in [('cap_usd',budget.CAP),('jobs',JOBS),('models',MODELS),('prices',budget.PRICES),('output_limits',budget.LIMITS),('rubric',RUBRIC)]:
        budget.require(budget.digest(plan[key])==budget.digest(val),f'Frozen setting changed: {key}')
    for p,sha in plan['inputs'].items():
        budget.require(budget.digest((ROOT/p).read_bytes())==sha,f'Frozen input changed: {p}')
budget.guard=guard

def documents(job):
    return {(p if len(job['papers'])>1 else 'doc'):PAPERS[p].read_text() for p in job['papers']}

def audit_one(key,content):
    job=JOBS[key];spec=get_operationalization_registry().get(job['engine']).process
    prose,ledger=split_ledger(content);ledger=re.split(r'^#{2,4} (?:Rejected by the critic|Check receipt|Scope assessment)\b',ledger,flags=re.M)[0]
    rows=parse_rows(ledger);docs=documents(job);dims={d.key for d in spec.dimensions if d.scope=='corpus'}
    prefixes={d.id_prefix for d in spec.dimensions if d.scope=='corpus'}|{'V.CORPUS'}
    corpus_ids={rid for r in rows for rid in [r.id,*r.lineage] if any(rid.startswith(p+'.') for p in prefixes)}
    wall=verify_rows(rows,SourceIndex(docs),corpus_dimensions=dims,corpus_ids=corpus_ids)
    return {'wall':wall.as_dict(),'rows':len(rows),'raw_anchors':sum(len(r.anchors) for r in rows),
        'raw_exact':sum(a.quote in docs.get(a.doc or 'doc','') for r in rows for a in r.anchors),
        'unknown_dimensions':sorted({r.dim for r in rows if r.dim and r.dim not in {d.key for d in spec.dimensions}}),
        'missing_table_ids':check_citations('\n'.join(line for line in prose.splitlines() if line.lstrip().startswith('|')),{r.id for r in rows}),
        'missing_prose_ids':check_citations(prose,{r.id for r in rows})}

def generate(key,plan):
    job=JOBS[key];target=OUT/'results'/f'{key}.json'
    budget.require(not target.exists() and not (OUT/'calls'/key).exists(),f'Existing attempt: {key}')
    recorder=budget.Recorder(key,plan);start=time.time()
    def on_call(call):
        budget.write(OUT/'steps'/key/f'{call.step_key}-{call.dimension_key}-{call.doc_key or "corpus"}.json',call.as_receipt())
    try:
        if job['condition']=='old':
            original=ARCHIVE/'original_capabilities'/f'{DESIGNS[job["id"]]["old"]}.yaml'
            cap=CapabilityEngineDefinition.model_validate(yaml.safe_load(original.read_text()))
            source=next(iter(documents(job).values()))
            result=recorder(first.old_prompt(cap),f'SOURCE [doc]:\n\n{source}',model_hint=MODELS['strong'],label='original questions, one Sol call')
            content=result['content'];process={'calls':[{'step':'old_oneshot',**{k:v for k,v in result.items() if k!='content'}}]}
        else:
            cap=get_engine_registry().get_capability_definition(job['engine']);spec=get_operationalization_registry().get(job['engine']).process
            run=run_process if job['condition']=='dvs' else run_oneshot_checked
            args={'parallelism':3} if job['condition']=='dvs' else {}
            result=run(cap,spec,documents(job),depth='deep' if job['condition']=='dvs' else 'standard',call_fn=recorder,on_call=on_call,**args)
            content=result.final_content;process=result.receipts()
        path=OUT/'outputs'/f'{key}.md';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
        budget.write(target,{'status':'complete','job':job,'output_sha256':budget.digest(content.encode()),'seconds':time.time()-start,'process':process,'audit':audit_one(key,content)})
        print(key,'COMPLETE',json.dumps(budget.costs()),flush=True)
    except BaseException as exc:
        budget.write(target,{'status':'failed','job':job,'error':f'{type(exc).__name__}: {exc}','seconds':time.time()-start});raise

def memo_binding(key):
    output=OUT/'outputs'/f'{key}.md';result=budget.read(OUT/'results'/f'{key}.json');sha=budget.digest(output.read_bytes())
    budget.require(result['status']=='complete' and result['output_sha256']==sha,'Output changed or incomplete')
    memo=ARCHIVE/'source_memos'/f'{key}.md'
    budget.require(memo.exists() and sha in memo.read_text() and len(memo.read_text())>800,'Substantive hash-bound source-read memo required before scores')
    committed=subprocess.check_output(['git','show',f'HEAD:{memo.relative_to(ROOT)}'],cwd=ROOT)
    budget.require(committed==memo.read_bytes(),'Source memo must be committed')
    return {'output_sha256':sha,'memo_sha256':budget.digest(committed),'memo_path':str(memo.relative_to(ROOT))}

def judge(key,rater,plan):
    binding=memo_binding(key);target=OUT/'scores'/f'{key}__{rater}.json';callkey=f'judge__{key}__{rater}'
    budget.require(not target.exists() and not (OUT/'calls'/callkey).exists(),'Existing score attempt')
    content=(OUT/'outputs'/f'{key}.md').read_text()
    content=re.sub(r'^### Check receipt\n.*?(?=^## |\Z)','',content,flags=re.M|re.S)
    content=re.sub(r'^.*[Cc]ritic: (?:openrouter/)?[^\n]+\n?','',content,flags=re.M)
    user='\n\n=====\n\n'.join(f'SOURCE [{k}]:\n\n{v}' for k,v in documents(JOBS[key]).items())+'\n\nANALYSIS:\n\n'+content
    system=RUBRIC+'\nRequested artifact: '+DESIGNS[JOBS[key]['id']]['ideal']+'\nKeep each reason concise (one sentence).'
    budget.write(OUT/'judge_inputs'/f'{key}__{rater}.json',{'binding':binding,'prepared_at':time.time(),'system_sha256':budget.digest(system.encode()),'user_sha256':budget.digest(user.encode())})
    res=budget.Recorder(callkey,plan,role=rater)(system,user,model_hint=MODELS[rater],label='independent rubric score')
    score=parse_llm_json_response(res['content']);budget.require(isinstance(score,dict),'Invalid JSON score')
    for criterion in budget.RUBRIC_KEYS:
        budget.require(isinstance(score.get(criterion),(int,float)) and not isinstance(score[criterion],bool) and 1<=score[criterion]<=10,'Invalid criterion score')
    budget.write(target,{'score':score,'binding':binding,'rater':rater,'mean':sum(score[k] for k in budget.RUBRIC_KEYS)/6})
    print(key,rater,'SCORED',json.dumps(budget.costs()),flush=True)

def export():
    import shutil
    for folder in ('outputs','results','scores','judge_inputs','steps'):
        if (OUT/folder).exists():shutil.copytree(OUT/folder,ARCHIVE/folder,dirs_exist_ok=True)
    for name in ('plan.json','all_memos_before_scores.json'):
        if (OUT/name).exists():shutil.copy2(OUT/name,ARCHIVE/name)
    calls=[{'path':str(p.relative_to(OUT)),**budget.read(p)} for p in sorted((OUT/'calls').glob('*/*.json')) if '.prompt.' not in p.name]
    budget.write(ARCHIVE/'calls.json',{'costs':budget.costs(),'calls':calls})

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('action',choices=['freeze','generate','score','status','export'])
    ap.add_argument('--ids',default='');ap.add_argument('--workers',type=int,choices=[1,2,3,4],default=3)
    a=ap.parse_args()
    if a.action=='freeze':freeze();export();return
    plan=budget.read(OUT/'plan.json');guard(plan)
    if a.action in ('status','export'):
        if a.action=='export':export()
        print(json.dumps(budget.costs(),indent=2));return
    from dotenv import load_dotenv
    load_dotenv(ROOT/'.env',override=False)
    with (OUT/'campaign.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        selected={k:j for k,j in JOBS.items() if not a.ids or j['id'] in a.ids.split(',')}
        if a.action=='generate':
            jobs=[k for k in selected if not (OUT/'results'/f'{k}.json').exists() and not (OUT/'calls'/k).exists()]
            fn=lambda k:generate(k,plan)
        else:
            complete=[k for k in JOBS if (OUT/'results'/f'{k}.json').exists() and budget.read(OUT/'results'/f'{k}.json')['status']=='complete']
            bindings={k:memo_binding(k) for k in complete}
            binding_path=OUT/'all_memos_before_scores.json'
            if binding_path.exists():budget.require(budget.read(binding_path)['bindings']==bindings,'Pre-score bindings changed')
            else:budget.write(binding_path,{'bindings':bindings,'prepared_at':time.time(),'commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()})
            jobs=[(k,r) for k in selected if k in complete for r in ('sonnet','sol') if not (OUT/'scores'/f'{k}__{r}.json').exists() and not (OUT/'calls'/f'judge__{k}__{r}').exists()]
            fn=lambda kr:judge(*kr,plan)
        errors=[]
        with ThreadPoolExecutor(max_workers=a.workers) as pool:
            futures={pool.submit(fn,k):k for k in jobs}
            for future in as_completed(futures):
                try:future.result()
                except Exception as exc:errors.append({'job':futures[future],'error':str(exc)});print('FAILED',futures[future],str(exc),flush=True)
        export();print(json.dumps({'costs':budget.costs(),'errors':errors}),flush=True)
        if errors:raise SystemExit(1)

if __name__=='__main__':main()
