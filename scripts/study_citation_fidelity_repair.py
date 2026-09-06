"""Bounded G6 repair: the evidence-index-only condition, same questions and walls."""
from pathlib import Path
import json,sys,time,yaml,shutil
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import study_citation_family as parent
from src.operationalizations.schemas import ProcessSpec
from src.executor.process_runner import run_oneshot_checked
from src.engines.registry import get_engine_registry
s=parent.s;OUT=parent.OUT/'repairs';ARCHIVE=parent.ARCHIVE/'repairs'
s.budget.OUT=OUT
op=yaml.safe_load((ARCHIVE/'citation_fidelity_audit.yaml').read_text());spec=ProcessSpec.model_validate(op['process'])
key='G6__index_only_repair';job={'id':'G6','engine':'citation_fidelity_audit','condition':'checked','index_only':True}
inputs=[Path(__file__),ARCHIVE/'citation_fidelity_audit.yaml',ROOT/'src/executor/process_runner.py',ROOT/'src/sources/citation_evidence.py',parent.SOURCES/'evidence_index.json']

def guard(plan):
    for path,sha in plan['inputs'].items():s.budget.require(s.budget.digest((ROOT/path).read_bytes())==sha,'Repair input changed '+path)
s.budget.guard=guard

def main():
    from dotenv import load_dotenv
    load_dotenv(ROOT/'.env',override=False);OUT.mkdir(parents=True,exist_ok=True)
    target=OUT/'results'/f'{key}.json';s.budget.require(not target.exists() and not (OUT/'calls'/key).exists(),'Existing repair attempt')
    plan={'reason':'Original reader refused due optional per-document scope JSON and all-or-nothing interpretation; use pair/coverage inventories and preserve independent unverifiable pairs.',
      'inputs':{str(p.relative_to(ROOT)):s.budget.digest(p.read_bytes()) for p in inputs},'models':s.MODELS,'limits':s.budget.LIMITS,'created_at':time.time()}
    s.budget.write(OUT/'plan.json',plan);s.budget.write(ARCHIVE/'plan.json',plan)
    def on_call(c):s.budget.write(OUT/'steps'/f'{c.step_key}.json',c.as_receipt())
    try:
        result=run_oneshot_checked(get_engine_registry().get_capability_definition(job['engine']),spec,parent.documents(job),
                                  call_fn=s.budget.Recorder(key,plan),on_call=on_call)
        content=result.final_content;p=OUT/'outputs'/f'{key}.md';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
        # Same dimensions, source index, pair wall and table-citation audit as initial condition.
        audit=parent.audit_one('G6__index_only',content)
        s.budget.write(target,{'status':'complete','job':job,'output_sha256':s.budget.digest(content.encode()),'process':result.receipts(),'audit':audit})
    except BaseException as exc:s.budget.write(target,{'status':'failed','job':job,'error':str(exc)});raise
    finally:
        for folder in ('results','outputs','steps'):
            if (OUT/folder).exists():shutil.copytree(OUT/folder,ARCHIVE/folder,dirs_exist_ok=True)
        s.budget.write(ARCHIVE/'calls.json',{'costs':s.budget.costs(),'calls':[{'path':str(p.relative_to(OUT)),**s.budget.read(p)} for p in (OUT/'calls').glob('*/*.json') if '.prompt.' not in p.name]})

if __name__=='__main__':main()
