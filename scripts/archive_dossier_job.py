"""Archive a finished dossier job from this instance's store into a study folder (job.json, dossier.md/html/pdf,
tables.json, findings.json, receipts.json, events.json, analysis/<phase>.md).

  TMPDIR=data/tmp python3 -m scripts.archive_dossier_job <job_id> <out_dir>
"""
from __future__ import annotations
import json, shutil, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))


def main():
    job_id, out = sys.argv[1], Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    from src.dossier.store import get_job
    from src.dossier import events
    job = get_job(job_id)
    if job is None:
        raise SystemExit(f"no job {job_id}")
    record = job.model_dump(mode="json")
    (out / "job.json").write_text(json.dumps(record, indent=1, ensure_ascii=False, default=str))
    for kind in ("md", "html", "pdf"):
        p = (job.paths or {}).get(kind) if getattr(job, "paths", None) else None
        if p and Path(p).exists():
            shutil.copy(p, out / f"dossier.{kind}")
    (out / "tables.json").write_text(json.dumps(record.get("tables") or [], indent=1, ensure_ascii=False))
    (out / "findings.json").write_text(json.dumps(record.get("findings") or [], indent=1, ensure_ascii=False))
    (out / "receipts.json").write_text(json.dumps(record.get("receipts") or [], indent=1, ensure_ascii=False, default=str))
    (out / "events.json").write_text(json.dumps(events.list_events(job_id), indent=1, ensure_ascii=False, default=str))
    (out / "analysis").mkdir(exist_ok=True)
    for pn, ph in (record.get("analysis") or {}).items():
        (out / "analysis" / f"{pn}_{ph.get('engine_key')}.md").write_text(ph.get("final_output") or "")
    print("archived", job_id, "->", out, "| status", job.status, "| cost", round(job.totals.cost_usd, 2), "| tables", len(record.get("tables") or []),
          "| phases", list((record.get("analysis") or {}).keys()), "| files", sorted(p.name for p in out.iterdir()))


if __name__ == "__main__":
    main()
