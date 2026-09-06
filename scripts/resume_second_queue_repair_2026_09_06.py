"""Bounded continuation of an empty provider response; successful calls replay locally only."""
from pathlib import Path
import argparse,fcntl,json,shutil,subprocess,sys,threading,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.study_second_queue_repair_2026_09_06 import study as s


def cache(key):
    good={};failed=[]
    for p in sorted((s.OUT/'calls'/key).glob('*.json')):
        if '.prompt.' in p.name:continue
        c=s.budget.read(p);raw=p.with_suffix('.md').read_bytes()
        s.budget.require(s.budget.digest(raw)==c['output_sha256'],'Changed archived response')
        prompt=s.budget.read(p.with_name(p.stem+'.prompt.json'))
        s.budget.require(s.budget.digest(prompt)==c['prompt_sha256'],'Changed archived prompt')
        c={**c,'path':str(p.relative_to(s.OUT)),'content':raw.decode()}
        if c['status']=='complete':good[c['prompt_sha256']]=c
        else:failed.append(c)
    s.budget.require(len(failed)==1 and not failed[0]['content'],'Expected one empty provider failure')
    return good,failed[0]


def prepare(key):
    plan=s.budget.read(s.OUT/'plan.json');s.guard(plan);good,bad=cache(key)
    path=s.ARCHIVE/'continuations'/f'{key}.json';s.budget.require(not path.exists(),'Already prepared')
    result=s.OUT/'results'/f'{key}.json';s.budget.require(s.budget.read(result)['status']=='failed','Expected failed result')
    dest=s.ARCHIVE/'failed_attempts';dest.mkdir(exist_ok=True);shutil.copy2(result,dest/result.name)
    s.budget.write(path,{'original_plan_identity':plan['identity'],'key':key,'prepared_at':time.time(),
        'reason':'Complete the authorized production validation after an empty reasoning-only provider response. No completed invocation is repurchased. Same prompts, routes, source and limits; one failed-step continuation.',
        'failed_prompt_sha256':bad['prompt_sha256'],'failed_receipt':bad['path'],
        'failed_receipt_sha256':s.budget.digest((s.OUT/bad['path']).read_bytes()),
        'completed_cache_entries':len(good),'max_failed_step_continuations':1,
        'driver_sha256':s.budget.digest(Path(__file__).read_bytes())})


class Boundary(Exception):pass


def run(key,probe=False):
    plan=s.budget.read(s.OUT/'plan.json');s.guard(plan)
    path=s.ARCHIVE/'continuations'/f'{key}.json';amend=s.budget.read(path)
    s.budget.require(amend['driver_sha256']==s.budget.digest(Path(__file__).read_bytes()),'Driver changed')
    s.budget.require(amend['original_plan_identity']==plan['identity'],'Plan mismatch')
    if not probe:s.budget.require(subprocess.check_output(['git','show',f'HEAD:{path.relative_to(ROOT)}'],cwd=ROOT)==path.read_bytes(),'Commit continuation first')
    good,bad=cache(key);prefix=key+'__continuation'
    s.budget.require(not (s.OUT/'calls'/prefix).exists(),'Continuation already attempted')
    paid=s.budget.Recorder(prefix,plan);mutex=threading.Lock();trace=[];boundary_used=False;new_labels=[]
    def caller(system,user,*,model_hint,label,**kwargs):
        nonlocal boundary_used
        sha=s.budget.digest({'system':system,'user':user})
        with mutex:
            if sha in good:
                c=good[sha];s.budget.require(c['model_requested']==model_hint and c['label']==label,'Cache metadata mismatch')
                trace.append({'label':label,'replayed_from':c['path'],'prompt_sha256':sha})
                return {'content':c['content'],'model_used':model_hint,'input_tokens':c['input_tokens'],'output_tokens':c['output_tokens'],'stop_reason':c['stop_reason'],'partial':False,'duration_ms':0,'retries':0}
            if sha==bad['prompt_sha256']:
                s.budget.require(not boundary_used,'Only one failed-step continuation')
                if probe:raise Boundary('Reached exact empty-response boundary after '+str(len(trace))+' cached calls; no provider invoked')
                boundary_used=True
            else:
                s.budget.require(boundary_used and ('| verify' in label or '| synthesize' in label or '| reconcile checked tables' in label),'Unplanned purchase: '+label)
            s.budget.require(label not in new_labels,'No repeated new call');new_labels.append(label)
        return paid(system,user,model_hint=model_hint,label=label,**kwargs)
    job=s.JOBS[key];cap=s.get_engine_registry().get_capability_definition(job['engine']);spec=s.get_operationalization_registry().get(job['engine']).process
    def on_call(c):
        if not probe:s.budget.write(s.OUT/'steps'/prefix/f'{c.step_key}-{c.dimension_key}-{c.doc_key or "corpus"}.json',c.as_receipt())
    start=time.time()
    try:
        fn=s.run_process if job['condition']=='dvs' else s.run_oneshot_checked
        args={'parallelism':3} if job['condition']=='dvs' else {}
        result=fn(cap,spec,s.documents(job),depth='deep' if job['condition']=='dvs' else 'standard',call_fn=caller,on_call=on_call,**args)
        s.budget.require(not probe,'Probe unexpectedly completed')
        content=result.final_content;p=s.OUT/'outputs'/f'{key}.md';p.parent.mkdir(exist_ok=True);p.write_text(content)
        s.budget.write(s.OUT/'results'/f'{key}.json',{'status':'complete','job':job,'output_sha256':s.budget.digest(content.encode()),'seconds':time.time()-start,'process':result.receipts(),'audit':s.audit_one(key,content),'continuation':{'decision':str(path.relative_to(ROOT)),'replayed_calls':trace,'new_labels':new_labels}})
    except Boundary as exc:print(str(exc));return
    finally:
        if not probe:
            s.budget.write(s.ARCHIVE/'continuations'/f'{key}_execution.json',{'replayed_calls':trace,'new_labels':new_labels,'costs':s.budget.costs()});s.export()


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('action',choices=['prepare','probe','resume']);ap.add_argument('key');a=ap.parse_args()
    if a.action=='prepare':prepare(a.key);return
    if a.action=='probe':run(a.key,True);return
    from dotenv import load_dotenv
    load_dotenv(ROOT/'.env',override=False)
    with (s.OUT/'campaign.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);run(a.key)
if __name__=='__main__':main()
