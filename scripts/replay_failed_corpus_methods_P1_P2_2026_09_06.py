"""Manually recover one failed invocation using exact saved calls, under the original USD8 cap.

No substantive prompt changes. A failed source invocation is not accepted as a product.
Unknown charges remain fully reserved. This entry point is deliberately separate from
normal generation and refuses reuse of its continuation directory.
"""
import argparse
import fcntl
import json
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import study_corpus_methods_P1_P2_2026_09_06 as study


def recover(key,plan):
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.executor.process_runner import run_process,run_oneshot_checked
    newkey=key+'__replay1';job=study.JOBS[key]
    study.require(not (study.OUT/'calls'/newkey).exists(),'Recovery already attempted; inspect without automatic retries')
    old=study.read(study.OUT/'results'/f'{key}.json');study.require(old['status']=='failed','Job did not fail')
    saved={};failures=[];replayed=[]
    for p in (study.OUT/'calls'/key).glob('*.json'):
        if '.prompt.' in p.name:continue
        r=study.read(p);prompt=study.read(p.with_name(p.stem+'.prompt.json'));content=p.with_suffix('.md').read_text()
        study.require(study.digest(prompt)==r['prompt_sha256'] and study.digest(content.encode())==r['output_sha256'],'Saved artifact hash mismatch')
        identity=(r['label'],r['model_requested'],r['prompt_sha256'])
        if r['status']=='complete':saved[identity]=(r,content,str(p.relative_to(study.OUT)))
        else:failures.append(identity)
    study.require(len(failures)==1,'Recovery expects one failed invocation')
    amendment=study.read(study.OUT/'transport_amendment.json')
    study.require(amendment['original_identity']==plan['identity'],'Wrong transport amendment')
    study.LIMITS.update(amendment['limits'])
    proof={'original_result':old,'failed_invocation':list(failures[0]),'script_sha256':study.digest(Path(__file__).read_bytes()),
           'original_identity':plan['identity'],'limits':study.LIMITS,'method':'Exact prompt/model/label replay; only the failed invocation and subsequent work are paid.',
           'costs_before':study.costs(),'prepared_at':time.time()}
    study.write(study.OUT/'failed_results'/f'{key}.json',old)
    study.write(study.OUT/'recoveries'/f'{key}.json',proof)
    invoke=study.Recorder(newkey,plan);new_started=False
    def call(system,user,**kwargs):
        nonlocal new_started
        identity=(kwargs['label'],kwargs['model_hint'],study.digest({'system':system,'user':user}))
        if identity in saved:
            r,content,path=saved.pop(identity);replayed.append(path)
            return {'content':content,'model_used':kwargs['model_hint'],'input_tokens':r['input_tokens'],'output_tokens':r['output_tokens'],
                    'duration_ms':r['duration_ms'],'partial':False,'stop_reason':r['stop_reason'],'retries':0}
        if not new_started:
            study.require(identity==failures[0] and not saved,'Replay diverged before the recorded failure')
            new_started=True
        return invoke(system,user,**kwargs)
    cap=get_engine_registry().get_capability_definition(job['engine']);spec=get_operationalization_registry().get(job['engine']).process
    run=run_process if job['mode']=='deep' else run_oneshot_checked
    def on_call(c):study.write(study.OUT/'steps'/newkey/f'{c.step_key}-{c.dimension_key}-{c.doc_key or "corpus"}.json',c.as_receipt())
    start=time.time()
    result=run(cap,spec,study.documents(job),depth=job['mode'],tier_overrides={k:study.MODELS[k] for k in ('cheap','mid','strong')},call_fn=call,on_call=on_call,
               **({'parallelism':1} if job['mode']=='deep' else {}))
    path=study.OUT/'outputs'/f'{key}.md';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(result.final_content)
    study.write(study.OUT/'results'/f'{key}.json',{'status':'complete','job':job,'output_sha256':study.digest(result.final_content.encode()),
       'seconds':old['seconds']+time.time()-start,'recovery_seconds':time.time()-start,'process':result.receipts(),
       'replayed_calls':replayed,'failed_attempt':'failed_results/'+key+'.json','new_calls':newkey})
    print(key,'RECOVERED',json.dumps(study.costs()),flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('job',choices=study.JOBS);args=parser.parse_args()
    plan=study.read(study.OUT/'plan.json');study.guard(plan)
    from dotenv import load_dotenv
    load_dotenv(ROOT/'.env',override=False)
    with (study.OUT/'campaign.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        recover(args.job,plan)

if __name__=='__main__':main()
