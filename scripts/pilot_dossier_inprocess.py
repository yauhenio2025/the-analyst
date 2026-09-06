"""The Riley → Weber pilot memo written by the Mastermind: one dossier over the pilot corpus through the three
citation engines, run in-process (no server), with the evidence index and the Stacks' plan as context documents.

  TMPDIR=data/tmp python3 -u -m scripts.pilot_dossier_inprocess [--depth-eng deep] [--cap 15]

Writes data/study/citation_family_2026_09_06/pilot/<job_id>/ (job.json, dossier.md, tables.json, events.json).
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
SOURCES = ROOT / "data/study/sources_citation"; OUT = ROOT / "data/study/citation_family_2026_09_06/pilot"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cap", type=float, default=15.0); ap.add_argument("--depth-eng", default="deep")
    ap.add_argument("--depth-g6", default="standard"); ap.add_argument("--depth-g8", default="deep")
    ap.add_argument("--reuse-profiles-from", default="", help="a cancelled pilot job whose reconnaissance profiles are carried over, re-keyed by document order")
    a = ap.parse_args()
    from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=False)
    from src.api.routes.dossier import validate_lane
    from src.dossier.schemas import CreateDossierRequest
    from src.dossier.schemas import DossierJob, DossierOptions, OutputOptions
    from src.dossier.store import create_job, get_job, update_job
    from src.dossier import runner
    from src.executor.document_store import store_document
    from src.sources.resolve import resolve_sources
    from src.sources.schemas import SourceSpec

    docs = json.loads((SOURCES / "documents.json").read_text())
    index = json.loads((SOURCES / "evidence_index.json").read_text())
    import ast, re
    def creators(raw):
        try:
            people = ast.literal_eval(raw) if isinstance(raw, str) and raw.startswith("[") else raw
            if isinstance(people, list):
                return "; ".join(f"{p.get('lastName','')}, {p.get('firstName','')}".strip(", ") for p in people if isinstance(p, dict)) or str(raw)
        except Exception:
            pass
        return str(raw or "")
    titles = {t["uid"]: f"{creators(t.get('creators'))} ({t.get('year') or 'n.d.'}) — {t['title']}" for t in index["texts"]}
    def header_title(k, v):
        m = re.search(r"^AUTHOR: (.+)$", v[:400], re.M); t = re.search(r"^TITLE: (.+)$", v[:600], re.M)
        return f"{m.group(1)} — {t.group(1)}" if m and t else (f"{m.group(1)} on Weber ({k})" if m else k)
    # keys ARE the Stacks uids, so the evidence index's texts and checks meet the supplied full texts (2026-09-06: the
    # first launch keyed them by a slug of a broken title and every citing text was double-witnessed)
    sources = [SourceSpec(kind="paste", key=k, title=titles.get(k) or header_title(k, v), text=v) for k, v in docs.items()]
    sources.append(SourceSpec(kind="paste", role="evidence_index", title="Riley → Weber: evidence index", text=(SOURCES / "evidence_index.json").read_text()))
    sources.append(SourceSpec(kind="paste", role="plan", title="Riley → Weber: the Stacks' plan (reconstructed)", text=(SOURCES / "pilot_plan.json").read_text()))
    req = CreateDossierRequest(
        sources=sources, audience="researcher", depth="medium", spend_cap_usd=a.cap, output=OutputOptions(tables=True, figures=0, plates=0),
        intent=("How does Dylan Riley engage Max Weber across his work; is that engagement justified by the Weber texts he cites; "
                "and where does his reading sit among Weber's readers we hold?"),
        entry="chosen", path={"steps": [{"engine_key": "citation_engagement_map", "depth": a.depth_eng},
                                        {"engine_key": "citation_fidelity_audit", "depth": a.depth_g6},
                                        {"engine_key": "citation_reception_map", "depth": a.depth_g8}]},
    )
    lane = validate_lane(req)
    resolved = resolve_sources(req.sources)
    options = DossierOptions(intent=req.intent, audience=req.audience, depth=req.depth, output=req.output, spend_cap_usd=req.spend_cap_usd,
                             autopilot=False, entry=lane["entry"], use_frame=lane["use_frame"], path=lane["path"])
    job = DossierJob(options=options, sources=[s.model_dump() for s in req.sources])
    job.documents = [{**d.meta(), "executor_doc_id": store_document(title=d.title, text=d.text, author=d.creators or None, role="dossier_source")} for d in resolved]
    create_job(job)
    if a.reuse_profiles_from:
        from src.dossier.schemas import Reconnaissance
        old = get_job(a.reuse_profiles_from)
        prior = old.profiles.profiles if old and old.profiles else []
        old_keys = [d.get("key") for d in old.documents if d.get("role", "source") == "source"] if old else []
        new_keys = [d["key"] for d in job.documents if d.get("role", "source") == "source"]
        remap = dict(zip(old_keys, new_keys)) if len(old_keys) == len(new_keys) else {}
        carried = []
        for p in prior:
            nk = remap.get(p.doc_key)
            if not nk:
                continue
            claims = [c.model_copy(update={"anchor": c.anchor.model_copy(update={"doc_key": nk})}) for c in p.key_claims]
            carried.append(p.model_copy(update={"doc_key": nk, "key_claims": claims}))
        if carried:
            update_job(job.id, profiles=Reconnaissance(profiles=carried, partial=True))
            print(time.strftime("%H:%M:%S"), f"carried {len(carried)} profiles from {a.reuse_profiles_from} (re-keyed by document order)", flush=True)
    runner.start(job.id)
    out = OUT / job.id; out.mkdir(parents=True, exist_ok=True)
    print(time.strftime("%H:%M:%S"), "started", job.id, "| documents", len(job.documents), "| context", sum(1 for d in job.documents if d.get("role") != "source"), flush=True)
    seen = None
    while True:
        j = get_job(job.id)
        if (j.status, j.step) != seen:
            seen = (j.status, j.step); print(time.strftime("%H:%M:%S"), "status", j.status, "step", j.step, flush=True)
        if j.status in ("done", "failed", "cancelled"):
            break
        time.sleep(20)
    (out / "job.json").write_text(json.dumps(j.model_dump(), indent=1, ensure_ascii=False, default=str))
    try:
        from src.dossier.compose import render_markdown  # if present
        (out / "dossier.md").write_text(render_markdown(j))
    except Exception as exc:  # noqa: BLE001
        md = j.paths.get("md") if getattr(j, "paths", None) else None
        if md and Path(md).exists(): (out / "dossier.md").write_text(Path(md).read_text())
        else: print("dossier.md not rendered:", str(exc)[:120], flush=True)
    print(time.strftime("%H:%M:%S"), "DONE", job.id, j.status, "| error:", j.error, "| totals:", json.dumps(getattr(j, "totals", None), default=str)[:300], flush=True)


if __name__ == "__main__":
    main()
