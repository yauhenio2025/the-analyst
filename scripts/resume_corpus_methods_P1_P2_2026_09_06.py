"""Explicit transport recovery for P1/P2; frozen prompts unchanged, original charges retained.

The first DeepSeek verification reached 18,000 output tokens, including 12,952
reasoning tokens, while emitting scope JSON. Raise only its provider output cap to
32,000. Replay completed extraction invocations by exact prompt/model/label hashes.
All new calls share the original USD8 accounting root. No automatic retries.
"""
import argparse
import json
from pathlib import Path
import sys
import time
import fcntl

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import study_corpus_methods_P1_P2_2026_09_06 as study


def prepare(plan):
    manifest={'original_identity':plan['identity'],'script_sha256':study.digest(Path(__file__).read_bytes()),
              'change':'mid max_output_tokens 18000 -> 32000; unchanged source, method, prompt, routing, rubric and budget',
              'limits':{**study.LIMITS,'mid':32000},'failure_sha256':study.digest((study.OUT/'calls/P1__deep__pair/0010.json').read_bytes()),
              'original_spend_root':str(study.OUT),'cap_usd':8.0}
    path=study.OUT/'transport_amendment.json'
    if path.exists(): study.require(study.read(path)==manifest,'Transport amendment changed')
    else: study.write(path,manifest)
    study.LIMITS['mid']=32000


def recover_pair(plan):
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.executor.process_runner import run_process
    key='P1__deep__pair';newkey=key+'__continuation1';job=study.JOBS[key]
    study.require(not (study.OUT/'calls'/newkey).exists(),'Existing recovery attempt; inspect before any further paid action')
    original=study.read(study.OUT/'results'/f'{key}.json')
    study.require(original['status']=='failed','Recovery requires the recorded failed job')
    study.write(study.OUT/'failed_results'/f'{key}.json',original)
    saved={}
    for p in (study.OUT/'calls'/key).glob('*.json'):
        if '.prompt.' in p.name:continue
        r=study.read(p)
        if r['status']!='complete':continue
        prompt=study.read(p.with_name(p.stem+'.prompt.json'));content=p.with_suffix('.md').read_text()
        study.require(study.digest(prompt)==r['prompt_sha256'] and study.digest(content.encode())==r['output_sha256'],'Replay artifact mismatch')
        saved[(r['label'],r['model_requested'],r['prompt_sha256'])]=(r,content,str(p.relative_to(study.OUT)))
    replayed=[];invoke=study.Recorder(newkey,plan)
    def call(system,user,**kwargs):
        identity=(kwargs['label'],kwargs['model_hint'],study.digest({'system':system,'user':user}))
        if identity in saved:
            r,content,path=saved.pop(identity);replayed.append(path)
            return {'content':content,'model_used':kwargs['model_hint'],'input_tokens':r['input_tokens'],'output_tokens':r['output_tokens'],
                    'duration_ms':r['duration_ms'],'partial':False,'stop_reason':r['stop_reason'],'retries':0}
        study.require('| extract |' not in kwargs['label'],'Extraction replay mismatch; do not generate new extraction evidence')
        return invoke(system,user,**kwargs)
    cap=get_engine_registry().get_capability_definition(job['engine']);spec=get_operationalization_registry().get(job['engine']).process
    start=time.time()
    def on_call(c):study.write(study.OUT/'steps'/newkey/f'{c.step_key}-{c.dimension_key}-{c.doc_key or "corpus"}.json',c.as_receipt())
    result=run_process(cap,spec,study.documents(job),depth='deep',tier_overrides={k:study.MODELS[k] for k in ('cheap','mid','strong')},call_fn=call,on_call=on_call,parallelism=1)
    study.require(not saved,'Not all extraction evidence was replayed')
    path=study.OUT/'outputs'/f'{key}.md';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(result.final_content)
    study.write(study.OUT/'results'/f'{key}.json',{'status':'complete','job':job,'output_sha256':study.digest(result.final_content.encode()),
      'seconds':original['seconds']+time.time()-start,'recovery_seconds':time.time()-start,'process':result.receipts(),
      'replayed_calls':replayed,'failed_attempt':'failed_results/'+key+'.json','new_calls':newkey})
    print(key,'RECOVERED',json.dumps(study.costs()),flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recover-pair',action='store_true')
    parser.add_argument('--generate',nargs='*',choices=study.JOBS,default=[])
    args=parser.parse_args();plan=study.read(study.OUT/'plan.json');study.guard(plan)
    from dotenv import load_dotenv
    load_dotenv(ROOT/'.env',override=False)
    with (study.OUT/'campaign.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        prepare(plan)
        if args.recover_pair:recover_pair(plan)
        for key in args.generate:study.generate(key,plan)

if __name__=='__main__':main()
