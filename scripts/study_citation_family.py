"""Citation family: independent methods and the index-only fidelity condition.

Frozen sources/prompts, ordinary process runner, receipts for every call; source
reads committed before Sonnet/Sol scoring. USD20 is guidance including dossier.
"""
from pathlib import Path
import json
import re
import sys
import time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import study_second_queue as s
from src.sources.citation_evidence import prepare_citation_sources
from src.executor.process_runner import run_process,run_oneshot_checked
from src.executor.context_broker import split_ledger
from src.executor.ledger_walls import SourceIndex,parse_rows,verify_rows,check_citations,normalize
from src.engines.registry import get_engine_registry
from src.operationalizations.registry import get_operationalization_registry
from src.llm.client import parse_llm_json_response
ARCHIVE=ROOT/'communications/study/citation_family_2026_09_06'
OUT=ROOT/'data/study/citation_family_2026_09_06'
SOURCES=ROOT/'data/study/sources_citation'
s.ARCHIVE=ARCHIVE;s.OUT=OUT;s.budget.OUT=OUT;s.budget.CAP=20.0
s.DESIGNS=json.loads((ARCHIVE/'designs.json').read_text())
s.JOBS={ident+'__'+mode:{'id':ident,'engine':s.DESIGNS[ident]['key'],'condition':mode}
        for ident,mode in [('ENG','dvs'),('G6','checked'),('G8','dvs')]}
s.JOBS['G6__index_only']={'id':'G6','engine':s.DESIGNS['G6']['key'],'condition':'checked','index_only':True}
s.budget.LIMITS={'cheap':6000,'mid':42000,'strong':28000,'sonnet':2400,'sol':2400}
_require=s.budget.require

def require(ok,message):
    if not ok and message=='USD8 admission cap: no new invocation':
        print('Conservative reservation crosses USD20 guidance; completion authorized; all receipts retained.',flush=True);return
    _require(ok,message)
s.budget.require=require

def documents(job):
    if job.get('index_only'):
        return {'citation_index':(SOURCES/'evidence_index.json').read_text()}
    return json.loads((SOURCES/'documents.json').read_text())
s.documents=documents

def inputs():
    files=[Path(__file__),ROOT/'scripts/study_second_queue.py',ROOT/'scripts/study_corpus_methods_P1_P2_2026_09_06.py',
      ROOT/'scripts/build_citation_pilot_corpus.py',ARCHIVE/'designs.json',SOURCES/'documents.json',SOURCES/'evidence_index.json',SOURCES/'pilot_plan.json']
    files += [ROOT/f'src/{folder}/{d["key"]}.yaml' for d in s.DESIGNS.values() for folder in ('engines/capability_definitions','operationalizations/definitions')]
    files += [ROOT/p for p in ('src/executor/process_runner.py','src/executor/ledger_walls.py','src/executor/scoped_outcomes.py',
      'src/executor/ruling_coverage.py','src/executor/context_broker.py','src/stages/process_composer.py','src/sources/citation_evidence.py')]
    return sorted(set(files))
s.inputs=inputs

def retained(content):
    prose,ledger=split_ledger(content)
    ledger=re.split(r'^#{2,4} (?:Rejected by the critic|Check receipt|Scope assessment)\b',ledger,flags=re.M)[0]
    return prose,parse_rows(ledger)

def audit_one(key,content):
    job=s.JOBS[key];docs,context=prepare_citation_sources(job['engine'],documents(job))
    spec=get_operationalization_registry().get(job['engine']).process
    prose,rows=retained(content);dims={d.key for d in spec.dimensions if d.scope=='corpus'}
    wall=verify_rows(rows,SourceIndex(docs),corpus_dimensions=dims)
    refs=set(re.findall(r'\bRW\d{4}\b',prose))
    return {'rows':len(rows),'wall':wall.as_dict(),'source_keys':list(docs),
      'anchors':sum(len(r.anchors) for r in rows),'raw_exact':sum(a.quote in docs.get(a.doc,'') for r in rows for a in r.anchors),
      'table_rows':sum(l.startswith('|') and not re.match(r'^\|[ :|-]+\|$',l) for l in prose.splitlines()),
      'passage_ids_in_prose_or_tables':sorted(refs),
      'missing_table_ids':check_citations('\n'.join(l for l in prose.splitlines() if l.startswith('|')),{r.id for r in rows}),
      'missing_prose_ids':check_citations(prose,{r.id for r in rows})}
s.audit_one=audit_one

def generate(key,plan):
    job=s.JOBS[key];target=OUT/'results'/f'{key}.json'
    require(not target.exists() and not (OUT/'calls'/key).exists(),'Existing attempt '+key)
    start=time.time();recorder=s.budget.Recorder(key,plan)
    def on_call(call):
        s.budget.write(OUT/'steps'/key/f'{call.step_key}-{call.dimension_key}-{call.doc_key or "corpus"}.json',call.as_receipt())
    try:
        cap=get_engine_registry().get_capability_definition(job['engine']);spec=get_operationalization_registry().get(job['engine']).process
        run=run_process if job['condition']=='dvs' else run_oneshot_checked
        args={'parallelism':5} if job['condition']=='dvs' else {}
        result=run(cap,spec,documents(job),depth='deep' if job['condition']=='dvs' else 'standard',call_fn=recorder,on_call=on_call,**args)
        content=result.final_content;p=OUT/'outputs'/f'{key}.md';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
        s.budget.write(target,{'status':'complete','job':job,'output_sha256':s.budget.digest(content.encode()),
          'seconds':time.time()-start,'process':result.receipts(),'audit':audit_one(key,content)})
        print(key,'COMPLETE',json.dumps(s.budget.costs()),flush=True)
    except BaseException as exc:
        s.budget.write(target,{'status':'failed','job':job,'error':f'{type(exc).__name__}: {exc}','seconds':time.time()-start});raise
s.generate=generate

def source_packet(key,content):
    """Full local material remains available; Sonnet sees reproducible source contexts.

    Include every candidate citation witness, every held primary window, and each
    output anchor plus ±1200 normalized characters. This is explicitly a packet,
    not a full-text independent coverage/absence judgment.
    """
    job=s.JOBS[key];docs,context=prepare_citation_sources(job['engine'],documents(job))
    index=json.loads((SOURCES/'evidence_index.json').read_text());_,rows=retained(content)
    out={}
    for key,text in docs.items():
        norm=normalize(text); intervals=[]
        if 'SOURCE ROLE: primary_window' in text or len(text)<14000:
            out[key]=text;continue
        for row in rows:
            for a in row.anchors:
                if a.doc!=key:continue
                q=normalize(a.quote);at=norm.find(q)
                if at>=0:intervals.append((max(0,at-1200),min(len(norm),at+len(q)+1200)))
        for t in index['texts']:
            if t['uid']==key:
                for p in t['passages']:
                    q=normalize(p['window']);at=norm.find(q)
                    if at>=0:intervals.append((max(0,at-400),min(len(norm),at+len(q)+400)))
        merged=[]
        for lo,hi in sorted(intervals):
            if merged and lo<=merged[-1][1]:merged[-1][1]=max(hi,merged[-1][1])
            else:merged.append([lo,hi])
        out[key]=text[:700]+'\n\nNORMALIZED SOURCE CONTEXTS (separate ranges, not continuous text):\n'+'\n\n'.join(f'[normalized chars {lo}:{hi}]\n{norm[lo:hi]}' for lo,hi in merged)
    return out,context

def judge(key,rater,plan):
    binding=s.memo_binding(key);target=OUT/'scores'/f'{key}__{rater}.json';callkey=f'judge__{key}__{rater}'
    require(not target.exists() and not (OUT/'calls'/callkey).exists(),'Existing score attempt')
    content=(OUT/'outputs'/f'{key}.md').read_text();packet,context=source_packet(key,content)
    system=s.RUBRIC+'\nRequested artifact: '+s.DESIGNS[s.JOBS[key]['id']]['ideal']+'''\nThe sources are an explicitly bounded source-context packet: all indexed citation-name windows,
all retrieved primary windows, and output anchors with neighboring context. Do not certify full-corpus
coverage or global absence from this packet. Judge the readings and table predicates against what is supplied.
A location match is not fidelity. Reception must preserve plan themes AND labelled reader additions.
Keep reasons concise. Do not infer model/mode quality from the analysis format.'''
    user=context+'\n\n'+'\n\n=====\n\n'.join(f'SOURCE [{k}]:\n{v}' for k,v in packet.items())+'\n\nANALYSIS:\n'+content
    s.budget.write(OUT/'judge_inputs'/f'{key}__{rater}.json',{'binding':binding,'source_packet':True,
      'packet_chars':sum(map(len,packet.values())),'source_keys':list(packet),'system_sha256':s.budget.digest(system.encode()),'user_sha256':s.budget.digest(user.encode())})
    res=s.budget.Recorder(callkey,plan,role=rater)(system,user,model_hint=s.MODELS[rater],label='independent bibliographic inventory rating')
    score=parse_llm_json_response(res['content'])
    for c in s.budget.RUBRIC_KEYS:require(isinstance(score.get(c),(int,float)) and 1<=score[c]<=10,'Invalid score '+c)
    s.budget.write(target,{'score':score,'binding':binding,'rater':rater,'mean':sum(score[c] for c in s.budget.RUBRIC_KEYS)/6})
    print(key,rater,'SCORED',flush=True)
s.judge=judge

if __name__=='__main__':s.main()
