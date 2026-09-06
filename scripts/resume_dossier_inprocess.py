"""Resume a dossier job in-process (no server): a chosen-path job that sat at awaiting_brief before the runner learned
to choose its own path (2026-09-06), or any paused job.

  TMPDIR=data/tmp python3 -u -m scripts.resume_dossier_inprocess <job_id>

Stays alive until the job reaches a terminal status; the runner's steps run in this process.
"""
from __future__ import annotations
import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))


def main():
    job_id = sys.argv[1]
    from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=False)
    from src.dossier import runner
    from src.dossier.store import get_job, update_job
    job = get_job(job_id)
    if job is None:
        raise SystemExit(f"no job {job_id}")
    if job.status == "awaiting_brief" and job.options.entry == "chosen" and job.options.path and not job.chosen_option:
        from src.dossier.schemas import BriefOption, Path as BriefPath, Shape
        brief = job.brief
        if brief is not None and brief.option(runner.OWN_PATH_KEY) is None:
            brief.options.append(BriefOption(
                key=runner.OWN_PATH_KEY, title="Your own path", deliverable_kind="case_file", use_kind="learn",
                deliverable="A dossier along the path you chose; the desk writes its shape from what the engines return.",
                shape=Shape(), path=BriefPath(), best_when="Pick this when you know the analysis you want.",
                notes=["own path: chosen on the request; no deliverable framing was written by the brief desk"]))
        update_job(job_id, chosen_option=runner.OWN_PATH_KEY, brief=brief, status="planning", step="plan")
        print(time.strftime("%H:%M:%S"), "chose own_path for", job_id, "(entry chosen with a fixed path)", flush=True)
    runner.start(job_id)
    seen = None
    while True:
        j = get_job(job_id)
        if (j.status, j.step) != seen:
            seen = (j.status, j.step); print(time.strftime("%H:%M:%S"), "status", j.status, "step", j.step, flush=True)
        if j.status in ("done", "failed", "cancelled"):
            break
        time.sleep(20)
    print(time.strftime("%H:%M:%S"), "TERMINAL", j.status, "| error:", j.error, "| cost:", j.totals.cost_usd, flush=True)


if __name__ == "__main__":
    main()
