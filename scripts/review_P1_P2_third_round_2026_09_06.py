"""Review the P1 quarantined candidate and P2 accepted output without changing either.

Use the existing frozen rubric and USD6 recorder. Source memos and the review
manifest must be committed before four independent ratings. Quarantine is retained
in provenance, never promoted to a completed production run.
"""
import argparse,fcntl,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import study_corpus_methods_P1_P2_third_round_2026_09_06 as t
from src.llm.client import parse_llm_json_response
s=t.study;ARCHIVE=t.ARCHIVE;MANIFEST=ARCHIVE/'review_manifest.json'
PRODUCTS={
 'P1__quarantined__pair':{'path':ARCHIVE/'quarantined/P1__repair.md','memo':ARCHIVE/'P1__quarantined_source_memo.md','status':'rejected after bounded production repair','job':'P1__deep__pair'},
 'P2__deep__pair':{'path':s.OUT/'outputs/P2__deep__pair.md','memo':ARCHIVE/'P2__deep__pair.md','status':'accepted after bounded empty-response continuation','job':'P2__deep__pair'},
}


def binding(p):
    sha=s.digest(p['path'].read_bytes());memo=p['memo'].read_bytes()
    s.require(sha in memo.decode() and len(memo)>800,'Substantive exact-output source memo required')
    return {'output_sha256':sha,'memo_sha256':s.digest(memo),'memo_path':str(p['memo'].relative_to(ROOT))}


def prepare():
    plan=s.read(s.OUT/'plan.json');s.guard(plan);s.require(not MANIFEST.exists(),'Review already frozen')
    s.require(s.read(s.OUT/'results/P1__deep__pair.json')['status']=='failed','P1 must remain failed')
    s.require(s.read(s.OUT/'results/P2__deep__pair.json')['status']=='complete','No completed P2 output')
    s.write(MANIFEST,{'original_plan_identity':plan['identity'],'driver_sha256':s.digest(Path(__file__).read_bytes()),
      'prepared_at':s.time.time(),'products':{k:{'path':str(p['path'].relative_to(ROOT)),'status':p['status'],'binding':binding(p)} for k,p in PRODUCTS.items()},
      'note':'P1 ratings describe a quarantined rejected candidate, not a successful production output. Same whole sources, tasks, rubric, model routes and USD6 accounting. No output edited.'})
    print(json.dumps({'products':list(PRODUCTS),'cap_usd':s.CAP}))


def guard():
    plan=s.read(s.OUT/'plan.json');s.guard(plan);m=s.read(MANIFEST)
    s.require(m['original_plan_identity']==plan['identity'] and m['driver_sha256']==s.digest(Path(__file__).read_bytes()),'Review driver/plan changed')
    for k,p in PRODUCTS.items():s.require(binding(p)==m['products'][k]['binding'],'Review bytes changed: '+k)
    return plan,m


def score():
    plan,m=guard();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    for p in [MANIFEST,*[p['memo'] for p in PRODUCTS.values()]]:
        s.require(subprocess.check_output(['git','show',f'{head}:{p.relative_to(ROOT)}'],cwd=ROOT)==p.read_bytes(),'Source review/manifest must be committed')
    order=s.OUT/'all_memos_before_scores.json'
    bindings={k:v['binding'] for k,v in m['products'].items()}
    if not order.exists():s.write(order,{'bindings':bindings,'commit':head,'prepared_at':s.time.time(),'review_manifest_sha256':s.digest(MANIFEST.read_bytes())})
    else:s.require(s.read(order)['bindings']==bindings,'Ordering manifest changed')
    for key,p in PRODUCTS.items():
        for rater in ('sonnet','sol'):
            target=s.OUT/'scores'/f'{key}__{rater}.json';callkey=f'judge__{key}__{rater}'
            if target.exists():continue
            s.require(not (s.OUT/'calls'/callkey).exists(),'No paid score replay')
            content=p['path'].read_text();content=re.sub(r'^### Check receipt\n.*?(?=^## |\Z)','',content,flags=re.M|re.S)
            content=re.sub(r'^.*[Cc]ritic: (?:openrouter/)?[^\n]+\n?','',content,flags=re.M)
            system=s.RUBRIC+'\n\nRequested task: '+s.TASKS[key[:2]]
            user='\n\n=====\n\n'.join(f'SOURCE [{k}]:\n\n{v}' for k,v in s.documents(s.JOBS[p['job']]).items())+'\n\n=====\n\nANALYSIS:\n\n'+content
            b=bindings[key];s.write(s.OUT/'judge_inputs'/f'{key}__{rater}.json',{'binding':b,'prepared_at':s.time.time(),'system_sha256':s.digest(system.encode()),'user_sha256':s.digest(user.encode()),'product_status':p['status']})
            res=s.Recorder(callkey,plan,role=rater)(system,user,model_hint=s.MODELS[rater],label='independent rubric score')
            rating=parse_llm_json_response(res['content']);s.require(isinstance(rating,dict),'Score JSON missing')
            for c in s.RUBRIC_KEYS:
                s.require(isinstance(rating.get(c),(int,float)) and not isinstance(rating[c],bool) and 1<=rating[c]<=10,'Bad score')
                s.require(isinstance(rating.get('reasons',{}).get(c),str) and rating['reasons'][c].strip(),'Missing reason')
            s.write(target,{'score':rating,'binding':b,'rater':rater,'mean':sum(rating[c] for c in s.RUBRIC_KEYS)/6,'product_status':p['status']})
            print(key,rater,'SCORED',json.dumps(s.costs()),flush=True)
    t.export()


def audit():
    plan,m=guard();order=s.read(s.OUT/'all_memos_before_scores.json');errors=[];scores=0
    for key,p in PRODUCTS.items():
        b=binding(p);committed=subprocess.check_output(['git','show',f"{order['commit']}:{b['memo_path']}"],cwd=ROOT)
        if s.digest(committed)!=b['memo_sha256'] or b['output_sha256'] not in committed.decode():errors.append(key+': bad memo custody')
        for rater in ('sonnet','sol'):
            path=s.OUT/'scores'/f'{key}__{rater}.json'
            if not path.exists():errors.append(key+' / '+rater+': missing score');continue
            scores+=1
            if s.read(path)['binding']!=b:errors.append(key+': score binding changed')
            for f in (s.OUT/'calls'/f'judge__{key}__{rater}').glob('*.json'):
                if '.prompt.' in f.name:continue
                if s.read(f)['started_at']<order['prepared_at']:errors.append(key+': judge predates committed memos')
    costs=s.costs()
    if costs['known_usd']+costs['reserved_usd']>6:errors.append('USD6 exceeded')
    # This existing auditor inspects only accepted outputs; P1's separate
    # quarantined_audit.json keeps its rejected candidate distinct.
    t._previous_audit()
    s.write(ARCHIVE/'review_validation.json',{'plan_identity':plan['identity'],'scores':scores,'products':{k:p['status'] for k,p in PRODUCTS.items()},'costs':costs,'errors':errors,'meaning_checked_by':'source-read memos; this validator checks bytes, anchors, keys and ordering only'})
    t.export();print(json.dumps({'scores':scores,'costs':costs,'errors':errors},indent=2))
    if errors:raise RuntimeError('; '.join(errors))


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('action',choices=['prepare','score','audit']);a=ap.parse_args()
    if a.action=='prepare':prepare();return
    if a.action=='audit':audit();return
    from dotenv import load_dotenv
    load_dotenv(ROOT/'.env',override=False)
    with (s.OUT/'campaign.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);score()
if __name__=='__main__':main()
