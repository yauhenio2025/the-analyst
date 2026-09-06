"""Fill the missing Sonnet rating of the unchanged first-round A3 original; no generation."""
from pathlib import Path
import json,re,subprocess,sys,time,fcntl
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.study_second_queue_repair_2026_09_06 import study as s
from src.llm.client import parse_llm_json_response


def prepare():
    old=ROOT/'communications/study/second_queue_2026_09_06'
    output=old/'outputs/A3__old__aukus.md';memo=old/'source_memos/A3__old__aukus.md'
    sha=s.budget.digest(output.read_bytes());s.budget.require(sha in memo.read_text(),'Unbound original memo')
    manifest={'output_path':str(output.relative_to(ROOT)), 'output_sha256':sha,
              'memo_path':str(memo.relative_to(ROOT)),'memo_sha256':s.budget.digest(memo.read_bytes()),
              'driver_sha256':s.budget.digest(Path(__file__).read_bytes()),'prepared_at':time.time(),
              'purpose':'Required same-paper original comparison: the first round never purchased this Sonnet rating. No new original output.'}
    s.budget.write(s.ARCHIVE/'A3_original_rating_manifest.json',manifest)


def score():
    from dotenv import load_dotenv
    load_dotenv(ROOT/'.env',override=False)
    plan=s.budget.read(s.OUT/'plan.json');s.guard(plan)
    manifest_path=s.ARCHIVE/'A3_original_rating_manifest.json';m=s.budget.read(manifest_path)
    s.budget.require(s.budget.digest(Path(__file__).read_bytes())==m['driver_sha256'],'Driver changed')
    for path in [manifest_path,ROOT/m['output_path'],ROOT/m['memo_path']]:
        s.budget.require(subprocess.check_output(['git','show',f'HEAD:{path.relative_to(ROOT)}'],cwd=ROOT)==path.read_bytes(),'Baseline source memo and manifest must be committed')
    output=(ROOT/m['output_path']).read_text();s.budget.require(s.budget.digest(output.encode())==m['output_sha256'],'Original changed')
    target=s.OUT/'baseline_scores/A3__old__aukus__sonnet.json';callkey='baseline__A3__old__aukus__sonnet'
    s.budget.require(not target.exists() and not (s.OUT/'calls'/callkey).exists(),'No paid replay')
    user='SOURCE [doc]:\n\n'+s.PAPERS['aukus'].read_text()+'\n\nANALYSIS:\n\n'+output
    system=s.RUBRIC+'\nRequested artifact: '+s.DESIGNS['A3']['ideal']+'\nKeep each reason concise (one sentence).'
    with (s.OUT/'campaign.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        res=s.budget.Recorder(callkey,plan,role='sonnet')(system,user,model_hint=s.MODELS['sonnet'],label='missing original-question baseline score')
    rating=parse_llm_json_response(res['content'])
    for k in s.budget.RUBRIC_KEYS:s.budget.require(isinstance(rating.get(k),int) and 1<=rating[k]<=10,'Bad rating')
    record={'score':rating,'mean':sum(rating[k] for k in s.budget.RUBRIC_KEYS)/6,'rater':'sonnet','manifest':m,
            'scored_at':time.time(),'supplemental_not_first_round':True}
    s.budget.write(target,record);s.budget.write(s.ARCHIVE/'baseline_scores'/target.name,record);s.export()
    print(json.dumps({'mean':record['mean'],'costs':s.budget.costs()}))

if __name__=='__main__':
    {'prepare':prepare,'score':score}[sys.argv[1]]()
