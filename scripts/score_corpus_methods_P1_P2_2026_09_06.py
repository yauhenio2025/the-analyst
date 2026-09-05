"""Independent single-output scores, with prior memos and one shared USD8 admission lock."""
import fcntl
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import study_corpus_methods_P1_P2_2026_09_06 as study


def main():
    from dotenv import load_dotenv
    load_dotenv(ROOT/'.env',override=False)
    plan=study.read(study.OUT/'plan.json');study.guard(plan)
    with (study.OUT/'campaign.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        bindings={key:study.memo_binding(key,plan) for key in study.JOBS}
        study.write(study.OUT/'all_memos_before_scores.json',bindings)
        errors=[]
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures={pool.submit(study.judge,key,rater,plan):(key,rater) for key in study.JOBS for rater in ('sonnet','sol')}
            for future in as_completed(futures):
                key,rater=futures[future]
                try:future.result()
                except Exception as exc:
                    errors.append({'job':key,'rater':rater,'error':str(exc)})
                    print(key,rater,'FAILED',str(exc),flush=True)
        print(json.dumps({'costs':study.costs(),'errors':errors}),flush=True)
        if errors:raise SystemExit(1)


if __name__=='__main__':main()
