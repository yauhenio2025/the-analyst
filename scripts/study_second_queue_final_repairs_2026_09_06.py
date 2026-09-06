"""One bounded same-paper checked repair each for S3 and A3; preserve the first pass."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import study_second_queue_repair_2026_09_06 as parent
s=parent.study
parent_inputs=parent.inputs
s.OUT=parent.OUT/'final_repairs';s.ARCHIVE=parent.ARCHIVE/'final_repairs';s.budget.OUT=s.OUT
s.JOBS={k:v for k,v in s.JOBS.items() if v['id'] in ('S3','A3')}

def inputs():
    return sorted(set(parent_inputs()+[Path(__file__).resolve(),s.ARCHIVE/'manifest.json',parent.ARCHIVE/'post_score_source_adjudication.md']))
s.inputs=inputs
if __name__=='__main__':s.main()
