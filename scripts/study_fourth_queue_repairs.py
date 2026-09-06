"""Separately frozen fourth-queue repairs and replacement of the truncated I13 control."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import study_fourth_queue as parent
from scripts import audit_fourth_queue as auditor

s = parent.study
BASE = parent.ARCHIVE
s.OUT = parent.OUT / "repairs"
s.ARCHIVE = BASE / "repairs"
# The legacy adapter uses its module's OUT while reading the original frozen prompt from BASE.
parent.OUT = s.OUT
s.budget.OUT = s.OUT
amendment = json.loads((s.ARCHIVE / "amendment.json").read_text())
s.JOBS = {k: v for k, v in s.JOBS.items()
          if (v["id"] in amendment["checked_ids"] and v["condition"] == "checked")
          or (v["id"] == "I13" and v["condition"] == "old")}


def inputs():
    return sorted(set(parent.inputs() + [Path(__file__).resolve(),
        ROOT / "scripts/audit_fourth_queue.py", s.ARCHIVE / "protocol.md",
        s.ARCHIVE / "amendment.json", BASE / "first_pass_audit.json",
        BASE / "post_score_adjudication.md"] + list((BASE / "scores").glob("*.json"))))


s.inputs = inputs
auditor.s = s

if __name__ == "__main__":
    if sys.argv[1:] == ["audit"]:
        auditor.audit()
    else:
        s.main()
