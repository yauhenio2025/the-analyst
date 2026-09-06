"""Third queue: the second-queue study pattern, one checked and one legacy control per method.

Freeze -> generate -> commit source-read memos -> independent Sonnet and Sol -> release audit.
USD15 is guidance, not an admission ceiling. Production runner and anchor rules are unchanged.
"""
from pathlib import Path
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import study_second_queue as study
ARCHIVE=ROOT/'communications/study/third_queue_2026_09_06'
OUT=ROOT/'data/study/third_queue_2026_09_06'
DESIGNS=json.loads((ARCHIVE/'designs.json').read_text())
study.ARCHIVE=ARCHIVE;study.OUT=OUT;study.DESIGNS=DESIGNS
study.budget.OUT=OUT;study.budget.CAP=15.0
study.JOBS={f'{ident}__{condition}__'+ '_'.join(d['papers']):
    {'id':ident,'engine':d['key'],'papers':d['papers'],'condition':condition}
    for ident,d in DESIGNS.items() for condition in ('checked','old')}
_require=study.budget.require

def require(ok,message):
    if not ok and message=='USD8 admission cap: no new invocation':
        print('USD15 guidance crossed by conservative reservations; owner authorized completion.',flush=True)
        return
    _require(ok,message)
study.budget.require=require

def inputs():
    files=[Path(__file__).resolve(),ROOT/'scripts/study_second_queue.py',ROOT/'scripts/study_first_queue.py',
        ROOT/'scripts/study_two_engines.py',ROOT/'scripts/study_corpus_methods_P1_P2_2026_09_06.py',
        ROOT/'communications/study/PROTOCOL_third_queue_2026-09-06.md',ARCHIVE/'designs.json']
    files += [ROOT/f'src/{folder}/{d["key"]}.yaml' for d in DESIGNS.values()
        for folder in ('engines/capability_definitions','operationalizations/definitions')]
    files += [ROOT/p for p in ('src/executor/process_runner.py','src/executor/ledger_walls.py',
        'src/executor/scoped_outcomes.py','src/executor/ruling_coverage.py','src/executor/context_broker.py',
        'src/stages/process_composer.py','src/operationalizations/schemas.py','src/engines/schemas_v2.py','src/events/pricing.py')]
    files += list((ARCHIVE/'original_definitions').glob('*.json'))+list((ARCHIVE/'original_prompts').glob('*.txt'))
    files += [study.PAPERS[p] for d in DESIGNS.values() for p in d['papers']]
    return sorted(set(files))
study.inputs=inputs
_generate=study.generate

def generate(key,plan):
    job=study.JOBS[key]
    if job['condition']!='old':return _generate(key,plan)
    target=OUT/'results'/f'{key}.json'
    require(not target.exists() and not (OUT/'calls'/key).exists(),f'Existing attempt: {key}')
    start=time.time()
    try:
        prompt=(ARCHIVE/'original_prompts'/f'{job["id"]}.txt').read_text()
        source=next(iter(study.documents(job).values()))
        res=study.budget.Recorder(key,plan)(prompt,'SOURCE [doc]:\n\n'+source,
            model_hint=study.MODELS['strong'],label='original legacy questions, one Sol call')
        content=res['content'];p=OUT/'outputs'/f'{key}.md';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
        study.budget.write(target,{'status':'complete','job':job,'output_sha256':study.budget.digest(content.encode()),
            'seconds':time.time()-start,'process':{'calls':[{'step':'old_oneshot',**{k:v for k,v in res.items() if k!='content'}}]},
            'audit':study.audit_one(key,content)})
        print(key,'COMPLETE',json.dumps(study.budget.costs()),flush=True)
    except BaseException as exc:
        study.budget.write(target,{'status':'failed','job':job,'error':f'{type(exc).__name__}: {exc}','seconds':time.time()-start});raise
study.generate=generate

if __name__=='__main__':study.main()
