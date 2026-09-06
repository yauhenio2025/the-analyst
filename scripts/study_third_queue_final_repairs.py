"""One separately frozen checked repair for four third-queue source defects."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import study_third_queue as parent
from scripts import audit_third_queue as auditor

s = parent.study
s.OUT = parent.OUT / 'final_repairs'
s.ARCHIVE = parent.ARCHIVE / 'final_repairs'
s.budget.OUT = s.OUT
s.JOBS = {k: v for k, v in s.JOBS.items()
          if v['id'] in ('I15', 'T2', 'E2', 'P3') and v['condition'] == 'checked'}

def inputs():
    return sorted(set(parent.inputs() + [Path(__file__).resolve(),
        ROOT / 'scripts/audit_third_queue.py', s.ARCHIVE / 'protocol.md',
        parent.ARCHIVE / 'first_pass_audit.json',
        parent.ARCHIVE / 'post_score_adjudication.md'] +
        list((parent.ARCHIVE / 'scores').glob('*__old__*.json'))))

s.inputs = inputs
auditor.s = s

if __name__ == '__main__':
    if sys.argv[1:] == ['audit']:
        auditor.audit()
    else:
        s.main()
