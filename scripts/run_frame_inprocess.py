"""The evidential frame of a hypothesis test, run in-process on a Stacks speculation memo (the Stacks' run 26 fixture).

  TMPDIR=data/tmp python3 -u -m scripts.run_frame_inprocess ~/projects/zotero-stacks/data/runs/26 [--depth standard]

Builds the job the Stacks will post (memo as the document, a plan block with hypothesis / verdict / coverage, engines
only), runs it through the runner in this process, then renders the frame JSON. Writes
data/study/frame_2026_09_06/<job_id>/{job.json, frame.json, final_output.md}.
"""
from __future__ import annotations
import argparse, json, re, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
OUT = ROOT / "data/study/frame_2026_09_06"


def plan_block(report: str, prompt: str) -> dict:
    hyp = ""
    m = re.search(r"^## The hypothesis.*?\n\n(.+?)\n\n", prompt, re.S | re.M)
    if m:
        hyp = " ".join(m.group(1).split())
    verdict = ""
    vm = re.search(r"^## Verdict\s*\n\n(holds in part|does not hold|holds|unclear)\s*\n\n(.+?)(?:\n\n|\Z)", report, re.S | re.M)
    verdict, note = (vm.group(1), " ".join(vm.group(2).split())) if vm else ("", "")
    def works(section):
        sm = re.search(rf"^## {section}\s*\n(.+?)(?=\n## |\Z)", report, re.S | re.M)
        return [w.strip("- ").strip() for w in (sm.group(1).splitlines() if sm else []) if w.strip().startswith("- ")]
    held = []
    cm = re.search(r"^## Coverage\s*\n(.+?)(?=\n## |\Z)", report, re.S | re.M)
    if cm:
        held = [l.strip("- ").strip() for l in cm.group(1).splitlines() if l.strip().startswith("- ")]
    return {"role": "plan", "kind": "hypothesis_test", "hypothesis": hyp, "verdict": verdict, "verdict_note": note,
            "verdict_vocabulary": ["holds", "holds in part", "does not hold", "unclear"],
            "coverage": {"held": held, "not_held": works("Not held"), "partial": []},
            "questions": ["What evidence would strengthen or weaken this hypothesis, in which named works?",
                          "What form must the argument take for the hypothesis to hold?", "Which tests would settle it, and which are decidable now?"],
            "warnings": ["Never restate the verdict.", "Name works as citable strings, never wishes.", "Separate what the corpus lacks from what the argument lacks."]}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("run_dir"); ap.add_argument("--depth", default="standard"); a = ap.parse_args()
    from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=False)
    from src.api.routes.dossier import validate_lane
    from src.dossier.schemas import CreateDossierRequest, DossierJob, DossierOptions, OutputOptions
    from src.dossier.store import create_job, get_job
    from src.dossier import runner
    from src.dossier.frame import passes_of, render_frame
    from src.executor.document_store import store_document
    from src.sources.resolve import resolve_sources
    from src.sources.schemas import SourceSpec
    rd = Path(a.run_dir).expanduser(); report = (rd / "REPORT.md").read_text(); prompt = (rd / "PROMPT.md").read_text()
    plan = plan_block(report, prompt)
    print("hypothesis:", plan["hypothesis"][:160], "| verdict:", plan["verdict"], "| not held:", len(plan["coverage"]["not_held"]), flush=True)
    sources = [SourceSpec(kind="paste", key="memo", title=f"Speculation memo, run {rd.name}: {report.splitlines()[0].lstrip('# ')[:80]}", text=report),
               SourceSpec(kind="paste", role="plan", key="plan", title="The hypothesis, the verdict and the coverage", text=json.dumps(plan, ensure_ascii=False, indent=1))]
    req = CreateDossierRequest(sources=sources, audience="researcher", depth="medium", spend_cap_usd=3.0,
                               output=OutputOptions(text=False, tables=False, figures=0, plates=0), intent=plan["hypothesis"] or "the hypothesis of the memo",
                               entry="chosen", path={"steps": [{"engine_key": "hypothesis_evidential_frame", "depth": a.depth}]})
    lane = validate_lane(req); resolved = resolve_sources(req.sources)
    options = DossierOptions(intent=req.intent, audience=req.audience, depth=req.depth, output=req.output, spend_cap_usd=req.spend_cap_usd,
                             autopilot=False, entry=lane["entry"], use_frame=lane["use_frame"], path=lane["path"])
    job = DossierJob(options=options, sources=[s.model_dump() for s in req.sources])
    job.documents = [{**d.meta(), "executor_doc_id": store_document(title=d.title, text=d.text, author=d.creators or None, role="dossier_source")} for d in resolved]
    create_job(job); runner.start(job.id)
    out = OUT / job.id; out.mkdir(parents=True, exist_ok=True)
    print(time.strftime("%H:%M:%S"), "started", job.id, flush=True)
    seen = None
    while True:
        j = get_job(job.id)
        if (j.status, j.step) != seen:
            seen = (j.status, j.step); print(time.strftime("%H:%M:%S"), "status", j.status, "step", j.step, flush=True)
        if j.status in ("done", "failed", "cancelled"):
            break
        time.sleep(15)
    record = j.model_dump(mode="json"); (out / "job.json").write_text(json.dumps(record, indent=1, ensure_ascii=False, default=str))
    frame = render_frame(record, passes_of(record))
    (out / "frame.json").write_text(json.dumps(frame, indent=1, ensure_ascii=False))
    for ph in (record.get("analysis") or {}).values():
        if ph.get("engine_key") == "hypothesis_evidential_frame":
            (out / "final_output.md").write_text(ph.get("final_output") or "")
    print(time.strftime("%H:%M:%S"), "DONE", job.id, j.status, "| error:", j.error, "| cost:", round(j.totals.cost_usd, 3),
          "| frame:", {k: (len(v) if isinstance(v, list) else v) for k, v in (frame or {}).items() if k in ("strengthen", "weaken", "decisive_tests", "residual", "works", "rows", "conjectures")}, flush=True)


if __name__ == "__main__":
    main()
