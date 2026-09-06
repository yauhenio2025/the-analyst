import sys,json,fcntl,time
sys.path.insert(0,'/home/evgeny/projects/the-analyst')
from scripts import study_second_queue as s
from dotenv import load_dotenv
load_dotenv(s.ROOT/'.env',override=False)
plan=s.budget.read(s.OUT/'plan.json');s.guard(plan)
remaining=[(k,r) for k in s.JOBS for r in ('sonnet','sol') if not (s.OUT/'scores'/f'{k}__{r}.json').exists() and not (s.OUT/'calls'/f'judge__{k}__{r}').exists()]
# No purchased invocation is retried. Reconsider only admissions that failed
# while other reservations were outstanding. Prioritize unscored new products.
remaining.sort(key=lambda kr:(s.JOBS[kr[0]]['condition']=='old',s.JOBS[kr[0]]['id']!='A3',kr[0],kr[1]!='sonnet'))
with (s.OUT/'campaign.lock').open('a') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 records=[]
 for key,rater in remaining:
  try:s.judge(key,rater,plan);records.append({'key':key,'rater':rater,'outcome':'scored'})
  except Exception as e:records.append({'key':key,'rater':rater,'outcome':'not_scored','reason':str(e)});print(key,rater,str(e),flush=True)
 s.budget.write(s.ARCHIVE/'serial_admissions.json',{'reason':'Reconsider unpurchased admissions after outstanding reservations settled; unchanged prompts/routes/limits, new products first. Error string USD8 is inherited; frozen enforced CAP is USD12.','records':records,'costs':s.budget.costs()})
 s.export()
 print(json.dumps(s.budget.costs()),flush=True)
