"""P1/P2 frozen corpus study. --freeze is offline; --generate and --judge spend under USD8.

One provider attempt per invocation; interrupted/unknown charges remain reserved. No
fallback or automatic job retry. Each independent score requires a hash-bound prior
reader memo. Ordinary process/composer/walls are used unchanged via call_fn.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / 'data/study/corpus_methods_P1_P2_2026_09_06'
CAP = 8.0
ENGINES = ('compare_supplied_cases', 'reconcile_sources')
MODELS = {'cheap': 'openrouter/openai/gpt-5.6-luna', 'mid': 'openrouter/deepseek/deepseek-v4-pro',
          'strong': 'openrouter/openai/gpt-5.6-sol', 'sonnet': 'claude-sonnet-4-6', 'sol': 'openrouter/openai/gpt-5.6-sol'}
# Repository list prices are a conservative local accounting convention, not an invoice.
PRICES = {'cheap': (.20, 1.20), 'mid': (1.042, 2.085), 'strong': (2, 10), 'sonnet': (3, 15), 'sol': (2, 10)}
LIMITS = {'cheap': 9000, 'mid': 18000, 'strong': 22000, 'sonnet': 3000, 'sol': 4000}
CORPORA = {
 'pair': {'aukus': 'data/study/source_aukus.txt', 'subsea': 'data/study/source_subsea.txt'},
 'castoriadis': {n: f'data/study/sources_ideas/{n}.md' for n in ('castoriadis1984_technique', 'castoriadis1990_what_democracy', 'castoriadis1997_rationality_of_capitalism')},
 'deutschmann': {n: f'data/study/sources_ideas/{n}.md' for n in ('deutschmann2001_capitalism_as_religion', 'deutschmann2001_promise_of_absolute_wealth', 'deutschmann2022_interpretation_of_capitalism_as_religion')},
}
JOBS = {f'{p}__{mode}__{corpus}': {'engine': engine, 'mode': mode, 'corpus': corpus}
        for p, engine, cases in [('P1', ENGINES[0], [('deep','pair'), ('deep','castoriadis'), ('standard','pair')]),
                                  ('P2', ENGINES[1], [('deep','deutschmann'), ('deep','castoriadis'), ('standard','pair')])]
        for mode, corpus in cases}
TASKS = {
 'P1': 'Compare the supplied cases or approaches on justified common questions. Preserve case/source identity, criteria, each attributed matrix cell, scope, missing/incommensurable cells and exceptions. For AUKUS/subsea compare state strategies toward private networks and markets without pooling distinct actors. For conceptual sources compare the supplied approaches as approaches.',
 'P2': 'Reconcile how these sources answer shared questions. Preserve every source\'s answer and object/time/scope; distinguish agreement, qualification, contradiction, different scope, inspected silence and insufficient evidence. Discover themes and coverage without inferring consensus from recurrence.',
}
RUBRIC_KEYS = ('specificity','anchoring','non_obviousness','coherence','usefulness','hallucination_risk')
RUBRIC = '''Score this single ANALYSIS against the supplied SOURCES, independently. No comparison or winner.
Six integer scores from 1 to 10, higher always better:
specificity: captures these sources and their distinct roles rather than generic themes;
anchoring: quotes occur in the named sources AND support the actual interpretation and scope;
non_obviousness: useful expert distinctions a casual reader misses;
coherence: consistent source attribution, scope and claims across prose, tables and findings;
usefulness: the requested comparison/reconciliation tables can be lifted, with honest missing/incommensurable cells;
hallucination_risk: 10 means no unsupported claims, invented consensus, false contradiction, or invented absence.
Read all sources and all substantive output. A verbatim quote verifies occurrence, not meaning. Judge table cells,
relation labels, definitions, quantifiers, dates, attribution, warrants and silence against the actual passages.
Different scope is not contradiction; recurring vocabulary is not agreement. An honest inconclusive or bounded
negative cell can be useful. Do not reward length, row count, special fields or asserted verification/check status.
Identify any decisive error with the analysis claim and counter-passage. Give a concise source-specific reason
for each criterion. Return only JSON with all six scores and nonempty reasons:
{"specificity":n,"anchoring":n,"non_obviousness":n,"coherence":n,"usefulness":n,"hallucination_risk":n,
"reasons":{"specificity":"...","anchoring":"...","non_obviousness":"...","coherence":"...",
"usefulness":"...","hallucination_risk":"..."},"decisive_errors":[],"one_line":"..."}'''


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    tmp.replace(path)


def read(path):
    return json.loads(path.read_bytes())


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def input_paths():
    paths = [Path(__file__).relative_to(ROOT)]
    paths += [Path(f'src/{folder}/{key}.yaml') for folder in ('engines/capability_definitions','operationalizations/definitions') for key in ENGINES]
    paths += [Path(f'communications/study/REDESIGN_{key}_2026-09-06.md') for key in ENGINES]
    paths += [Path(p) for p in ('src/executor/process_runner.py','src/stages/process_composer.py','src/executor/ledger_walls.py',
      'src/executor/scoped_outcomes.py','src/executor/ruling_coverage.py','src/executor/context_broker.py','src/operationalizations/schemas.py',
      'src/engines/schemas_v2.py','src/events/pricing.py')]
    paths += [Path(p) for corpus in CORPORA.values() for p in corpus.values()]
    return sorted(set(paths))


def freeze():
    require(not (OUT/'plan.json').exists(), 'Plan already frozen; do not create a second campaign to hide spend')
    plan = {'cap_usd':CAP,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'frozen_at':time.time(),'jobs':JOBS,'models':MODELS,'prices':PRICES,'output_limits':LIMITS,
            'rubric':RUBRIC,'tasks':TASKS,'input_hashes':{str(p):digest((ROOT/p).read_bytes()) for p in input_paths()},
            'control':'Offline mixed-scope archive fixture only; no additional paid control.'}
    plan['identity'] = digest(plan)
    write(OUT/'plan.json',plan)
    print(json.dumps({'identity':plan['identity'],'jobs':list(JOBS),'cap_usd':CAP,'source_chars':{k:sum(len((ROOT/p).read_text()) for p in v.values()) for k,v in CORPORA.items()}},indent=2))


def guard(plan):
    require(plan['cap_usd'] == CAP and plan['jobs'] == JOBS, 'Campaign definition changed')
    require(plan['identity'] == digest({k:v for k,v in plan.items() if k!='identity'}), 'Plan identity mismatch')
    for p, sha in plan['input_hashes'].items():
        require(digest((ROOT/p).read_bytes()) == sha, f'Frozen input changed: {p}')


def costs():
    rs=[read(p) for p in (OUT/'calls').glob('*/*.json') if '.prompt.' not in p.name]
    return {'calls':len(rs), 'known_usd':round(sum(r.get('cost_usd') or 0 for r in rs),6),
            'reserved_usd':round(sum(r['reservation_usd'] for r in rs if r.get('cost_usd') is None),6),
            'incomplete_calls':sum(r['status']!='complete' for r in rs),
            'provider_reported_usd':round(sum(r.get('provider_cost_usd') or 0 for r in rs),6)}


def admission(role, system, user):
    # UTF-8 bytes bound the byte-token vocabulary conservatively; output is provider-capped.
    # Include 2048 tokens for message framing, plus 10% monetary reserve.
    input_bound = len((system+user).encode()) + 2048
    a,b = PRICES[role]
    return 1.1*(input_bound*a + LIMITS[role]*b)/1e6


LOCK=threading.Lock()


class Recorder:
    def __init__(self,job,plan,role=None):
        self.job,self.plan,self.role=job,plan,role
        self.counter=0

    def __call__(self,system,user,*,model_hint,label,**kwargs):
        role=self.role or next(k for k in ('cheap','mid','strong') if MODELS[k]==model_hint)
        require(MODELS[role]==model_hint,'Unexpected model')
        with LOCK:
            guard(self.plan)
            reservation=admission(role,system,user)
            c=costs()
            require(c['known_usd']+c['reserved_usd']+reservation<=CAP,'USD8 admission cap: no new invocation')
            self.counter+=1
            path=OUT/'calls'/self.job/f'{self.counter:04d}.json'
            require(not path.exists(),'Refuse automatic replay of a paid invocation')
            prompt={'system':system,'user':user}
            receipt={'status':'running','model_requested':model_hint,'role':role,'label':label,'started_at':time.time(),
                     'reservation_usd':reservation,'cost_usd':None,'prompt_sha256':digest(prompt),'max_output_tokens':LIMITS[role]}
            write(path.with_name(path.stem+'.prompt.json'),prompt)
            write(path,receipt)
        content=''
        try:
            # Direct SDK transport has no retry/fallback; the model work uses unchanged process prompts.
            if model_hint.startswith('openrouter/'):
                from openai import OpenAI
                client=OpenAI(api_key=os.environ['OPENROUTER_API_KEY'],base_url='https://openrouter.ai/api/v1',max_retries=0,timeout=600)
                stream=client.chat.completions.create(model=model_hint.removeprefix('openrouter/'),messages=[{'role':'system','content':system},{'role':'user','content':user}],
                  max_tokens=LIMITS[role],stream=True,stream_options={'include_usage':True},extra_body={'reasoning':{'effort':'low'}})
                usage=None; stop=None; used=None
                for chunk in stream:
                    used=chunk.model or used
                    if chunk.usage: usage=chunk.usage.model_dump()
                    if chunk.choices:
                        content+=chunk.choices[0].delta.content or ''
                        stop=chunk.choices[0].finish_reason or stop
                require(usage is not None,'Missing provider usage; reservation retained')
                inp,out=usage['prompt_tokens'],usage['completion_tokens']
                receipt['provider_cost_usd']=usage.get('cost')
                receipt['provider_usage']=usage
            else:
                from anthropic import Anthropic
                client=Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'],max_retries=0,timeout=600)
                res=client.messages.create(model=model_hint,max_tokens=LIMITS[role],system=system,messages=[{'role':'user','content':user}])
                content=''.join(b.text for b in res.content if b.type=='text')
                usage=res.usage.model_dump(); inp=usage['input_tokens']; out=usage['output_tokens']
                stop=res.stop_reason; used=res.model
                receipt['provider_usage']=usage
            cost=(inp*PRICES[role][0]+out*PRICES[role][1])/1e6
            # Use the larger of list-price token accounting and any provider-reported cost.
            cost=max(cost,receipt.get('provider_cost_usd') or 0)
            receipt.update(cost_usd=round(cost,6),input_tokens=inp,output_tokens=out,model_used=used,stop_reason=stop,
                           output_sha256=digest(content.encode()),duration_ms=round((time.time()-receipt['started_at'])*1000))
            require(cost<=reservation,'Provider cost exceeded the reserved bound; stop campaign')
            require(used in (model_hint,model_hint.removeprefix('openrouter/')),f'Unexpected provider model: {used}')
            require(content.strip() and stop in ('stop','end_turn'),'Empty, partial or refused output; preserved without retry')
            receipt['status']='complete'
            print(f"{self.job} {label}: ${cost:.4f}, {receipt['duration_ms']/1000:.1f}s",flush=True)
            return {'content':content,'model_used':model_hint,'input_tokens':inp,'output_tokens':out,'stop_reason':stop,'partial':False,'duration_ms':receipt['duration_ms'],'retries':0}
        except BaseException as exc:
            receipt.update(status='failed',error=f'{type(exc).__name__}: {exc}')
            raise
        finally:
            path.with_suffix('.md').write_text(content)
            receipt['output_sha256']=digest(content.encode())
            with LOCK: write(path,receipt)


def documents(job):
    return {k:(ROOT/p).read_text() for k,p in CORPORA[job['corpus']].items()}


def generate(key,plan):
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.executor.process_runner import run_process,run_oneshot_checked
    job=JOBS[key]; target=OUT/'results'/f'{key}.json'
    require(not target.exists() and not (OUT/'calls'/key).exists(),f'Existing attempt: {key}')
    cap=get_engine_registry().get_capability_definition(job['engine'])
    spec=get_operationalization_registry().get(job['engine']).process
    recorder=Recorder(key,plan)
    def on_call(call):
        write(OUT/'steps'/key/f'{call.step_key}-{call.dimension_key}-{call.doc_key or "corpus"}.json',call.as_receipt())
    start=time.time()
    try:
        run=run_process if job['mode']=='deep' else run_oneshot_checked
        args={'parallelism':3} if job['mode']=='deep' else {}
        result=run(cap,spec,documents(job),depth=job['mode'],tier_overrides={k:MODELS[k] for k in ('cheap','mid','strong')},call_fn=recorder,on_call=on_call,**args)
        content=result.final_content
        output=OUT/'outputs'/f'{key}.md';output.parent.mkdir(parents=True,exist_ok=True);output.write_text(content)
        write(target,{'status':'complete','job':job,'output_sha256':digest(content.encode()),'seconds':time.time()-start,'process':result.receipts()})
        print(key, 'COMPLETE',json.dumps(costs()),flush=True)
    except BaseException as exc:
        write(target,{'status':'failed','job':job,'seconds':time.time()-start,'error':f'{type(exc).__name__}: {exc}'})
        raise


def memo_binding(key,plan):
    output=OUT/'outputs'/f'{key}.md'; result=read(OUT/'results'/f'{key}.json')
    require(result['status']=='complete','No completed output')
    sha=digest(output.read_bytes());require(sha==result['output_sha256'],'Output changed')
    memo=ROOT/'communications/study/corpus_methods_P1_P2_2026_09_06'/f'{key}.md'
    require(memo.exists() and sha in memo.read_text() and len(memo.read_text())>800,'Source-read memo must name exact output SHA-256 and substantive findings before scoring')
    return {'output_sha256':sha,'memo_sha256':digest(memo.read_bytes()),'memo_path':str(memo.relative_to(ROOT))}


def judge(key,rater,plan):
    from src.llm.client import parse_llm_json_response
    binding=memo_binding(key,plan)
    for previous in (OUT/'scores').glob(f'{key}__*.json'):
        require(read(previous)['binding']==binding,'Memo or output changed after scores')
    target=OUT/'scores'/f'{key}__{rater}.json'
    callkey=f'judge__{key}__{rater}'
    require(not target.exists() and not (OUT/'calls'/callkey).exists(),'Existing judge attempt; no automatic retry')
    # Hide transport/wall receipts and model identity; retain actual prose, tables and scope reports.
    content=(OUT/'outputs'/f'{key}.md').read_text()
    import re
    content=re.sub(r'^### Check receipt\n.*?(?=^## |\Z)', '', content, flags=re.M|re.S)
    content=re.sub(r'^.*[Cc]ritic: (?:openrouter/)?[^\n]+\n?', '',content,flags=re.M)
    src='\n\n=====\n\n'.join(f'SOURCE [{k}]:\n\n{v}' for k,v in documents(JOBS[key]).items())
    user=src+'\n\n=====\n\nANALYSIS:\n\n'+content
    system=RUBRIC+'\n\nRequested task: '+TASKS[key[:2]]
    # Persist memo binding before invoking either judge.
    write(OUT/'judge_inputs'/f'{key}__{rater}.json',{'binding':binding,'prepared_at':time.time(),'analysis_sha256':digest(content.encode())})
    res=Recorder(callkey,plan,role=rater)(system,user,model_hint=MODELS[rater],label='independent rubric score')
    score=parse_llm_json_response(res['content'])
    require(isinstance(score,dict),'Invalid score JSON')
    for criterion in RUBRIC_KEYS:
        require(isinstance(score.get(criterion),(int,float)) and not isinstance(score.get(criterion),bool) and 1<=score[criterion]<=10,'Invalid score')
        require(isinstance(score.get('reasons',{}).get(criterion),str) and score['reasons'][criterion].strip(),'Missing criterion reason')
    write(target,{'score':score,'binding':binding,'rater':rater,'mean':sum(score[k] for k in RUBRIC_KEYS)/6})
    print(key,rater,'SCORED',json.dumps(costs()),flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    action=parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--freeze',action='store_true');action.add_argument('--generate',nargs='+',choices=JOBS)
    action.add_argument('--judge',nargs='+',choices=JOBS);action.add_argument('--status',action='store_true')
    parser.add_argument('--rater',choices=('sonnet','sol'),default='sonnet')
    args=parser.parse_args()
    if args.freeze: freeze();return
    plan=read(OUT/'plan.json');guard(plan)
    if args.status: print(json.dumps(costs(),indent=2));return
    from dotenv import load_dotenv
    load_dotenv(ROOT/'.env',override=False)
    OUT.mkdir(parents=True,exist_ok=True)
    with (OUT/'campaign.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if args.generate:
            for key in args.generate: generate(key,plan)
        else:
            for key in args.judge: judge(key,args.rater,plan)


if __name__=='__main__':
    main()
