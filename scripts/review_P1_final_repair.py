"""Two independent ratings of the unchanged failed P1 candidate; never promote it."""
from pathlib import Path
import json,sys,subprocess,time,fcntl
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.study_P1_final_repair import s
from src.llm.client import parse_llm_json_response
b=s.budget;A=s.ARCHIVE;M=A/'review_manifest.json';KEY='P1__quarantined__aukus_subsea';JOB='P1__dvs__aukus_subsea'
PRODUCT=A/'quarantined/final.md';MEMO=A/'P1_quarantined_source_memo.md'

def binding():
    sha=b.digest(PRODUCT.read_bytes());memo=MEMO.read_bytes()
    b.require(sha in memo.decode() and len(memo)>800,'Substantive output-bound source memo required')
    return {'output_sha256':sha,'memo_sha256':b.digest(memo),'memo_path':str(MEMO.relative_to(ROOT))}

def guard():
    plan=b.read(s.OUT/'plan.json');s.guard(plan)
    b.require(b.read(s.OUT/'results'/f'{JOB}.json')['status']=='failed','Failed production status must be preserved')
    m=b.read(M)
    b.require(m['binding']==binding() and m['driver_sha256']==b.digest(Path(__file__).read_bytes()) and m['plan_identity']==plan['identity'],'Review changed')
    return plan,m

def prepare():
    plan=b.read(s.OUT/'plan.json');s.guard(plan);b.require(not M.exists(),'Review already frozen')
    b.write(M,{'plan_identity':plan['identity'],'prepared_at':time.time(),'driver_sha256':b.digest(Path(__file__).read_bytes()),'binding':binding(),
        'product_status':'quarantined; rejected after bounded repair','output_path':str(PRODUCT.relative_to(ROOT)),
        'note':'Same whole pair, frozen rubric and USD4 guidance ledger. Two independent ratings only; no additional generation and no accepted output created.'})

def score():
    plan,m=guard();head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    for p in (MEMO,M,Path(__file__).resolve()):
        b.require(subprocess.check_output(['git','show',f'{head}:{p.relative_to(ROOT)}'])==p.read_bytes(),'Review and source memo must be committed before scores')
    op=s.OUT/'all_memos_before_scores.json'
    if not op.exists():b.write(op,{'bindings':{KEY:binding()},'commit':head,'prepared_at':time.time(),'review_manifest_sha256':b.digest(M.read_bytes())})
    else:b.require(b.read(op)['bindings']=={KEY:binding()},'Score order binding changed')
    for rater in ('sonnet','sol'):
        target=s.OUT/'scores'/f'{KEY}__{rater}.json';callkey=f'judge__{KEY}__{rater}'
        b.require(not target.exists() and not (s.OUT/'calls'/callkey).exists(),'No paid score replay')
        guard()
        system=s.RUBRIC+'\nRequested artifact: '+s.DESIGNS['P1']['ideal']+'\nKeep each reason concise (one sentence).'
        user='\n\n=====\n\n'.join(f'SOURCE [{k}]:\n\n{v}' for k,v in s.documents(s.JOBS[JOB]).items())+'\n\nANALYSIS:\n\n'+PRODUCT.read_text()
        b.write(s.OUT/'judge_inputs'/f'{KEY}__{rater}.json',{'binding':binding(),'prepared_at':time.time(),'system_sha256':b.digest(system.encode()),'user_sha256':b.digest(user.encode()),'product_status':m['product_status']})
        res=b.Recorder(callkey,plan,role=rater)(system,user,model_hint=s.MODELS[rater],label='independent quarantined-candidate score')
        rating=parse_llm_json_response(res['content']);b.require(isinstance(rating,dict),'Missing score JSON')
        for c in b.RUBRIC_KEYS:b.require(isinstance(rating.get(c),(int,float)) and not isinstance(rating[c],bool) and 1<=rating[c]<=10,'Invalid criterion')
        b.write(target,{'score':rating,'binding':binding(),'rater':rater,'mean':sum(rating[c] for c in b.RUBRIC_KEYS)/6,'product_status':m['product_status']})
        print(rater,'SCORED',json.dumps(b.costs()),flush=True)
    s.export()

def audit():
    plan,m=guard();order=b.read(s.OUT/'all_memos_before_scores.json');bd=binding()
    b.require(order['bindings']=={KEY:bd},'Ordering binding changed')
    historical=subprocess.check_output(['git','show',f"{order['commit']}:{bd['memo_path']}"])
    b.require(b.digest(historical)==bd['memo_sha256'],'Historical memo changed')
    for rater in ('sonnet','sol'):
        score=b.read(s.OUT/'scores'/f'{KEY}__{rater}.json');b.require(score['binding']==bd and score['product_status']==m['product_status'],'Score binding/status changed')
        for p in (s.OUT/'calls'/f'judge__{KEY}__{rater}').glob('*.json'):
            if '.prompt.' not in p.name:b.require(b.read(p)['started_at']>=order['prepared_at'],'Score predates committed source read')
    from scripts import audit_third_queue as raw_audit
    raw_audit.s=s;raw_audit.audit()
    b.write(A/'review_validation.json',{'scores':2,'production_status':'failed','product_status':m['product_status'],'binding':bd,'costs':b.costs(),'errors':[]})

if __name__=='__main__':
    action=sys.argv[1]
    if action=='prepare':prepare()
    elif action=='audit':audit()
    elif action=='score':
        from dotenv import load_dotenv
        load_dotenv(ROOT/'.env',override=False)
        with (s.OUT/'campaign.lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);score()
    else:raise SystemExit('prepare | score | audit')
