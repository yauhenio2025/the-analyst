"""One explicit continuation of P2's empty provider response, within its original USD6.

Completed calls are replayed from exact prompt-bound bytes without purchase.
Only the failed corpus verifier and the existing synthesis/one-repair path may
make new calls. Original failed receipts/results remain archived. No P1 retry.
"""
from pathlib import Path
import argparse,fcntl,json,shutil,subprocess,sys,threading
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import study_corpus_methods_P1_P2_third_round_2026_09_06 as t
s=t.study;KEY='P2__deep__pair';ARCHIVE=t.ARCHIVE
AMEND=ARCHIVE/'continuation.json'


def cache():
    out={};failed=[]
    for p in sorted((s.OUT/'calls'/KEY).glob('*.json')):
        if '.prompt.' in p.name:continue
        c=s.read(p);raw=p.with_suffix('.md').read_bytes()
        s.require(s.digest(raw)==c['output_sha256'],'Archived response changed')
        prompt=s.read(p.with_name(p.stem+'.prompt.json'))
        s.require(s.digest(prompt)==c['prompt_sha256'],'Archived prompt changed')
        c={**c,'path':str(p.relative_to(s.OUT)),'content':raw.decode()}
        if c['status']=='complete':out[c['prompt_sha256']]=c
        else:failed.append(c)
    s.require(len(failed)==1 and failed[0]['label']=='reconcile_sources | verify' and not failed[0]['content'],'Unexpected failed-step boundary')
    return out,failed[0]


def prepare():
    s.guard(s.read(s.OUT/'plan.json'));s.require(not AMEND.exists(),'Already prepared')
    completed,failed=cache();result=s.read(s.OUT/'results'/f'{KEY}.json')
    s.require(result['status']=='failed','Expected original failed result')
    dest=ARCHIVE/'failed_attempts';dest.mkdir(exist_ok=True)
    for key in s.JOBS:shutil.copy2(s.OUT/'results'/f'{key}.json',dest/f'{key}.json')
    s.write(AMEND,{'reason':'One bounded continuation after a billed provider stream returned only reasoning tokens, no answer and no finish status. Supersedes no-replay wording only for this failed empty step; no completed invocation is purchased again. P1 is not retried after its bounded synthesis repair failed.',
      'original_plan_identity':s.read(s.OUT/'plan.json')['identity'],'cap_usd':6,'completed_cache_entries':len(completed),
      'failed_prompt_sha256':failed['prompt_sha256'],'failed_receipt':failed['path'],'failed_receipt_sha256':s.digest((s.OUT/failed['path']).read_bytes()),
      'driver_sha256':s.digest(Path(__file__).read_bytes()),'max_failed_step_continuations':1,
      'subsequent_calls':'existing final synthesis and at most its existing bounded structural repair; same prompts/routes/limits',
      'prepared_at':s.time.time(),'preparation_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()})
    print(json.dumps(s.read(AMEND),indent=2))


class Boundary(Exception):pass


def run(probe=False):
    plan=s.read(s.OUT/'plan.json');s.guard(plan);amend=s.read(AMEND)
    s.require(amend['driver_sha256']==s.digest(Path(__file__).read_bytes()),'Continuation driver changed')
    s.require(amend['original_plan_identity']==plan['identity'] and amend['cap_usd']==s.CAP==6,'Plan/cap mismatch')
    if not probe:
        committed=subprocess.check_output(['git','show',f'HEAD:{AMEND.relative_to(ROOT)}'],cwd=ROOT)
        s.require(committed==AMEND.read_bytes(),'Continuation decision must be committed before calls')
    cached,failed=cache();prefix=KEY+'__continuation'
    s.require(not (s.OUT/'calls'/prefix).exists(),'Continuation already attempted; no replay')
    paid=s.Recorder(prefix,plan);mutex=threading.Lock();trace=[];boundary_used=False;new_labels=[]
    def caller(system,user,*,model_hint,label,**kwargs):
        nonlocal boundary_used
        sha=s.digest({'system':system,'user':user})
        with mutex:
            if sha in cached:
                c=cached[sha];s.require(c['model_requested']==model_hint and c['label']==label,'Cache metadata mismatch')
                trace.append({'label':label,'replayed_from':c['path'],'prompt_sha256':sha})
                return {'content':c['content'],'model_used':model_hint,'input_tokens':c['input_tokens'],'output_tokens':c['output_tokens'],'stop_reason':c['stop_reason'],'partial':False,'duration_ms':0,'retries':0}
            if sha==failed['prompt_sha256']:
                s.require(not boundary_used,'Failed step may be continued once only')
                if probe:raise Boundary('Reached the exact empty-response step after '+str(len(trace))+' cached calls; no provider invoked')
                boundary_used=True
            else:
                s.require(boundary_used and label in ('reconcile_sources | synthesize','reconcile_sources | synthesize (repair corpus synthesis)'),'Unplanned new invocation: '+label)
            s.require(label not in new_labels,'No repeated new call');new_labels.append(label)
        return paid(system,user,model_hint=model_hint,label=label,**kwargs)
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.executor.process_runner import run_process
    def on_call(call):
        if not probe:s.write(s.OUT/'steps'/prefix/f'{call.step_key}-{call.dimension_key}-{call.doc_key or "corpus"}.json',call.as_receipt())
    start=s.time.time()
    try:
        result=run_process(get_engine_registry().get_capability_definition(s.JOBS[KEY]['engine']),get_operationalization_registry().get(s.JOBS[KEY]['engine']).process,
          s.documents(s.JOBS[KEY]),depth='deep',parallelism=3,call_fn=caller,on_call=on_call)
        s.require(not probe,'Probe unexpectedly reached a final result')
        content=result.final_content;out=s.OUT/'outputs'/f'{KEY}.md';out.parent.mkdir(exist_ok=True);out.write_text(content)
        s.write(s.OUT/'results'/f'{KEY}.json',{'status':'complete','job':s.JOBS[KEY],'output_sha256':s.digest(content.encode()),'seconds':s.time.time()-start,'process':result.receipts(),
          'continuation':{'decision':str(AMEND.relative_to(ROOT)),'original_failed_result':str((ARCHIVE/'failed_attempts'/f'{KEY}.json').relative_to(ROOT)),'replayed_calls':trace,'new_labels':new_labels,'note':'Process receipt tokens include replayed cached calls; budget calls.json counts purchases once.'}})
    except Boundary as e:
        print(str(e));return
    finally:
        if not probe:
            s.write(ARCHIVE/'continuation_execution.json',{'replayed_calls':trace,'new_labels':new_labels,'costs':s.costs()});t.export()
    print(json.dumps(s.costs(),indent=2))


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('action',choices=['prepare','probe','resume']);a=ap.parse_args()
    if a.action=='prepare':prepare();return
    from dotenv import load_dotenv
    if a.action=='resume':load_dotenv(ROOT/'.env',override=False)
    with (s.OUT/'campaign.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);run(probe=a.action=='probe')
if __name__=='__main__':main()
