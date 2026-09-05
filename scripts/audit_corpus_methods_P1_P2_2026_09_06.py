"""Offline mechanical audit of frozen P1/P2 outputs; never judges semantic relations."""
from collections import Counter
import json
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import study_corpus_methods_P1_P2_2026_09_06 as study
from src.executor.context_broker import split_ledger
from src.executor.ledger_walls import SourceIndex,parse_rows,verify_rows,check_citations
from src.operationalizations.registry import get_operationalization_registry


def audit():
    plan=study.read(study.OUT/'plan.json');study.guard(plan)
    results={}
    for key,job in study.JOBS.items():
        path=study.OUT/'outputs'/f'{key}.md'
        if not path.exists(): continue
        record=study.read(study.OUT/'results'/f'{key}.json')
        content=path.read_text();assert study.digest(content.encode())==record['output_sha256']
        prose,ledger=split_ledger(content)
        ledger=re.split(r'^#{2,4} (?:Rejected by the critic|Check receipt|Scope assessment)\b',ledger,flags=re.M)[0]
        rows=parse_rows(ledger);docs=study.documents(job)
        dims={d.key for d in get_operationalization_registry().get(job['engine']).process.dimensions if d.scope=='corpus'}
        raw_anchors=[{'id':r.id,'doc':a.doc,'quote':a.quote,'exact':a.quote in docs.get(a.doc,'')} for r in rows for a in r.anchors]
        wall=verify_rows(rows,SourceIndex(docs),corpus_dimensions=dims)
        tables=[line for line in prose.splitlines() if line.lstrip().startswith('|')]
        scopes=record['process']['final_wall'].get('scope_outcomes',[])
        calls=[study.read(p) for p in (study.OUT/'calls').glob(key+'*/*.json') if '.prompt.' not in p.name]
        results[key]={'output_sha256':record['output_sha256'],'source_sha256':{k:study.digest(v.encode()) for k,v in docs.items()},
          'wall':wall.as_dict(),'exact_raw_anchors':sum(a['exact'] for a in raw_anchors),'raw_anchor_count':len(raw_anchors),
          'raw_nonexact':[{k:v for k,v in a.items() if k!='quote'} for a in raw_anchors if not a['exact']],
          'verified_source_coverage':dict(Counter(a.verified_doc for r in rows for a in r.anchors if a.verified_doc)),
          'missing_prose_ids':check_citations(prose,{r.id for r in rows}),
          'missing_table_ids':check_citations('\n'.join(tables),{r.id for r in rows}),
          'table_lines':len(tables),'scope_outcomes':dict(Counter(r['outcome'] for r in scopes)),
          'scope_blocking_issues':[{'docs':r['document_keys'],'dimension':r['dimension_key'],'issues':r.get('evidence_state',{}).get('blocking_issues',[])} for r in scopes if r.get('evidence_state',{}).get('blocking_issues')],
          'ruling_coverage':record['process']['final_wall'].get('check_ruling_coverage'),
          'calls':len(calls),'cost_usd':round(sum(c.get('cost_usd') or 0 for c in calls),6),'seconds':record['seconds']}
    study.write(study.OUT/'audit.json',results)
    print(json.dumps(results,indent=2))

if __name__=='__main__': audit()
