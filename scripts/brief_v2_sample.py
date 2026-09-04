"""One real brief-v2 call per saved exemplar profile (≈ $0.05–0.12 each) — the §E2 comparison.

Reads the saved job.json (reconnaissance profiles + document metadata; the document text is not
needed: the brief prices from char counts), runs `run_brief` in a scratch job id so nothing in
data/ is touched, and writes the brief + the checks' notes + the call cost to
communications/changes/brief-v2-samples/<name>.json.

    set -a; source .env; set +a
    python scripts/brief_v2_sample.py [fashion|house|state_capitalism ...] [--data-dir DIR] [--entry use|material|chosen]
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SAMPLES = {
    "fashion": "live-dossier-be00c33e5180",
    "house": "live-dossier-5cdf8f1a470f",
    "state_capitalism": "live-dossier-dce25aeed631",
}


def load_job(path: Path, entry: str, use_frame: dict | None, chosen_path: dict | None):
    from src.dossier.schemas import DossierJob, PathRequest, UseFrame
    from src.sources.schemas import Document

    raw = json.loads(path.read_text(encoding="utf-8"))
    job = DossierJob.model_validate({k: v for k, v in raw.items() if k not in ("brief", "chosen_option", "plan", "plan_id", "analysis", "tables", "figures", "sections", "receipts", "totals", "paths", "notes")})
    job.id = f"sample-brief-v2-{path.parent.name[-12:]}-{int(time.time())}"
    job.status, job.step = "reconnaissance", "brief"
    job.options.entry = entry
    job.options.autopilot = entry == "material"
    if use_frame:
        job.options.use_frame = UseFrame.model_validate(use_frame)
    if chosen_path:
        job.options.path = PathRequest.model_validate(chosen_path)
    docs = [Document(key=d.get("key", "doc"), title=d.get("title", ""), creators=d.get("creators", "") or "", year=str(d.get("year", "") or ""),
                     publication=d.get("publication", "") or "", text="", char_count=int(d.get("char_count") or 0)) for d in job.documents]
    return job, docs, raw


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*", default=list(SAMPLES))
    ap.add_argument("--data-dir", default="/home/evgeny/projects/the-analyst/data/dossiers")
    ap.add_argument("--out-dir", default=str(ROOT / "communications" / "changes" / "brief-v2-samples"))
    ap.add_argument("--entry", default="use", choices=["use", "material", "chosen"])
    ap.add_argument("--use-kind", default=None)
    ap.add_argument("--chain-key", default=None, help="entry=chosen: a recipe key")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from src.dossier import events
    from src.dossier.brief import run_brief

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in args.names:
        job_id = SAMPLES[name]
        job, docs, raw = load_job(Path(args.data_dir) / job_id / "job.json", args.entry,
                                  {"use_kind": args.use_kind} if args.use_kind else None,
                                  {"chain_key": args.chain_key} if args.chain_key else None)
        print(f"\n===== {name} ({job_id}) — {len(docs)} docs, {sum(d.char_count for d in docs):,} chars, intent={job.options.intent!r}, entry={args.entry}")
        started = time.time()
        brief = run_brief(job, docs)
        elapsed = time.time() - started
        evs = events.list_events(job.id)
        calls = [e for e in evs if e.get("kind") == "call_finished"]
        cost = sum(float(e.get("cost_usd") or 0) for e in calls)
        for o in brief.options:
            print(f"\n[{o.key}] {o.title}  · {o.use_kind} · {o.deliverable_kind} · ${o.est_cost_usd} · ~{o.est_minutes} min · {o.path.depth}")
            print(f"  deliverable: {o.deliverable}")
            for p in o.you_will_understand:
                print(f"  understand: {p.text}  [{', '.join(r.label() for r in p.supported_by)}]")
            for p in o.you_will_be_able_to:
                print(f"  able to: {p.text}  [{', '.join(r.label() for r in p.supported_by)}]{' (unsupported)' if p.unsupported else ''}")
            print(f"  not for: {' | '.join(o.not_for)}")
            print(f"  shape: {len(o.shape.sections)} sections · " + " · ".join(f"T{i} {t.row_unit} ({t.rows_expected})" for i, t in enumerate(o.shape.tables, 1))
                  + (" · " + " · ".join(f"F{i} {f.format}" for i, f in enumerate(o.shape.figures, 1)) if o.shape.figures else ""))
            print(f"  how: {' → '.join(s.plain_name for s in o.path.steps)} · {o.path.depth}")
            print(f"  best when: {o.best_when}")
            if o.notes:
                print(f"  notes: {o.notes}")
        if brief.recommendation:
            print(f"\nRECOMMENDED: {brief.recommendation.option_key} — because {brief.recommendation.because}")
            print(f"runner-up: {brief.recommendation.runner_up} — {brief.recommendation.runner_up_because}")
        print(f"brief notes: {brief.notes}")
        print(f"calls: {len(calls)}, cost ${cost:.3f}, {elapsed:.0f}s")
        record = {
            "sample": name, "source_job": job_id, "entry": args.entry, "intent": job.options.intent, "audience": job.options.audience,
            "depth_preference": job.options.depth, "documents": [{"key": d.key, "title": d.title, "char_count": d.char_count} for d in docs],
            "brief": brief.model_dump(), "calls": [{k: e.get(k) for k in ("label", "input_tokens", "output_tokens", "cost_usd", "duration_ms")} for e in calls],
            "cost_usd": round(cost, 4), "elapsed_s": round(elapsed, 1),
            "events": [{k: e.get(k) for k in ("kind", "detail")} for e in evs if e.get("kind") in ("note", "artifact")],
            "live_brief_v1_titles": [o.get("title") for o in (raw.get("brief") or {}).get("options", [])],
        }
        out = out_dir / f"{name}.json"
        out.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"saved {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
