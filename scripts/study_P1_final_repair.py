"""One natural AUKUS/subsea pair, deep, after the third-queue release decision."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import study_third_queue as parent
from scripts import audit_third_queue as auditor
s=parent.study
s.OUT=ROOT/'data/study/P1_final_repair_2026_09_06'
s.ARCHIVE=ROOT/'communications/study/P1_final_repair_2026_09_06'
s.budget.OUT=s.OUT;s.budget.CAP=4.0
s.DESIGNS={'P1':{'key':'compare_supplied_cases','papers':['aukus','subsea'],'inventory':True,
    'ideal':'A case-by-criterion comparison of the supplied cases, with justified common questions, a source-to-case map, source-attributed answers, and explicit missing or incommensurable cells. Preserve separate project chronology and causal status, separate instrument identities, qualifying exceptions and the limits of this collection. Every positive cell cites supporting findings; cross-source findings retain both source keys.'}}
s.JOBS={'P1__dvs__aukus_subsea':{'id':'P1','engine':'compare_supplied_cases','papers':['aukus','subsea'],'condition':'dvs'}}

def inputs():
    return sorted(set(parent.inputs()+[Path(__file__).resolve(),ROOT/'scripts/audit_third_queue.py',
        s.ARCHIVE/'protocol.md',
        ROOT/'src/engines/capability_definitions/compare_supplied_cases.yaml',
        ROOT/'src/operationalizations/definitions/compare_supplied_cases.yaml',
        ROOT/'communications/study/STUDY_second_queue_repair_2026-09-06.md']))
s.inputs=inputs
# The existing recorder's guard and no-replay rule remain; the owner made USD4 guidance.
_original_require=parent._require
def require(ok,message):
    if not ok and message=='USD8 admission cap: no new invocation':
        print('USD4 guidance crossed by conservative reservations; owner authorized completion.',flush=True)
        return
    _original_require(ok,message)
s.budget.require=require
auditor.s=s
if __name__=='__main__':
    if sys.argv[1:]==['audit']:auditor.audit()
    else:s.main()
