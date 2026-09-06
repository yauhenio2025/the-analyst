"""Explicit recovery after /tmp log writes failed; reuse complete paid responses.

Exact prompt hashes only. A complete provider response whose subsequent log
write failed is recoverable; a provider stop_reason=error is not. Original
receipts and failed results remain unchanged. A new request is a named repair.
"""
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import argparse
import json
import shutil
import time
from scripts import study_citation_family as study
from src.executor.process_runner import run_process,run_oneshot_checked
from src.engines.registry import get_engine_registry
from src.operationalizations.registry import get_operationalization_registry
s=study.s;OUT=study.OUT;ARCHIVE=study.ARCHIVE

class Recover:
    def __init__(self,key,plan):
        self.key=key;self.paid=s.budget.Recorder('resume__'+key,plan);self.cached={};self.used=[]
        for folder in (key,'resume__'+key):
            for p in (OUT/'calls'/folder).glob('*.json'):
                if '.prompt.' in p.name:continue
                r=s.budget.read(p)
                if r.get('stop_reason') not in ('stop','end_turn') or not p.with_suffix('.md').exists():continue
                content=p.with_suffix('.md').read_text()
                if content.strip() and s.budget.digest(content.encode())==r.get('output_sha256'):
                    self.cached[r['prompt_sha256']]=(p,r,content)
        # Append new invocations after earlier recovery calls; never overwrite.
        self.paid.counter=max([int(p.stem) for p in (OUT/'calls'/('resume__'+key)).glob('*.json') if '.prompt.' not in p.name] or [0])
    def __call__(self,system,user,**kwargs):
        sha=s.budget.digest({'system':system,'user':user})
        if sha not in self.cached:return self.paid(system,user,**kwargs)
        p,r,content=self.cached[sha];self.used.append(str(p.relative_to(OUT)))
        return {'content':content,'model_used':r['model_requested'],'input_tokens':r['input_tokens'],
          'output_tokens':r['output_tokens'],'stop_reason':r['stop_reason'],'partial':False,'duration_ms':r['duration_ms'],'retries':0}

def resume(key,plan):
    target=OUT/'results'/f'{key}.json';previous=s.budget.read(target) if target.exists() else {}
    if previous.get('status')=='complete':return
    if target.exists():
        dest=OUT/'failed_results'/f'{key}__{int(time.time())}.json';dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,dest)
    job=s.JOBS[key];cap=get_engine_registry().get_capability_definition(job['engine']);spec=get_operationalization_registry().get(job['engine']).process
    recorder=Recover(key,plan);start=time.time()
    def on_call(c):s.budget.write(OUT/'steps'/key/f'{c.step_key}-{c.dimension_key}-{c.doc_key or "corpus"}.json',c.as_receipt())
    try:
        run=run_process if job['condition']=='dvs' else run_oneshot_checked
        args={'parallelism':5} if job['condition']=='dvs' else {}
        result=run(cap,spec,study.documents(job),depth='deep' if job['condition']=='dvs' else 'standard',call_fn=recorder,on_call=on_call,**args)
        content=result.final_content;p=OUT/'outputs'/f'{key}.md';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
        s.budget.write(target,{'status':'complete','job':job,'output_sha256':s.budget.digest(content.encode()),'seconds':time.time()-start,
           'recovered_responses':recorder.used,'process':result.receipts(),'audit':study.audit_one(key,content)})
        print(key,'RECOVERED',flush=True)
    except BaseException as exc:
        s.budget.write(target,{'status':'failed','job':job,'error':f'{type(exc).__name__}: {exc}','recovered_responses':recorder.used,'seconds':time.time()-start})
        raise
    finally:
        s.budget.write(OUT/'recovery'/f'{key}.json',{'script_sha256':s.budget.digest(Path(__file__).read_bytes()),
          'original_result':previous,'reused_complete_responses':recorder.used,'new_call_directory':'calls/resume__'+key})

if __name__=='__main__':
    from dotenv import load_dotenv
    load_dotenv(study.ROOT/'.env',override=False)
    ap=argparse.ArgumentParser();ap.add_argument('--keys',default='');a=ap.parse_args()
    plan=s.budget.read(OUT/'plan.json');s.guard(plan)
    keys=a.keys.split(',') if a.keys else [k for k in s.JOBS if (OUT/'results'/f'{k}.json').exists() and s.budget.read(OUT/'results'/f'{k}.json')['status']=='failed']
    errors=[]
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures={pool.submit(resume,k,plan):k for k in keys}
        for f in as_completed(futures):
            try:f.result()
            except Exception as exc:errors.append({'job':futures[f],'error':str(exc)});print('FAILED',futures[f],str(exc),flush=True)
    s.export()
    for folder in ('failed_results','recovery'):
        if (OUT/folder).exists():shutil.copytree(OUT/folder,ARCHIVE/folder,dirs_exist_ok=True)
    print(json.dumps({'errors':errors,'costs':s.budget.costs()}),flush=True)
