"""Live end-to-end check (2026-09-06): a two-paper dossier on the deployed desk with a chosen path of the new methods,
to see the spine cite findings by id and the tables lift ledger rows. Polls to completion, then prints what the desks did.
  python scripts/live_dossier_check.py            # creates the job and waits (≈ 20–40 min); resumable with --job <id>
"""
from __future__ import annotations
import argparse, json, sys, time, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; BASE = "https://the-analyst-kcuc.onrender.com"; OUT = ROOT / "data/study/live_dossier"; OUT.mkdir(parents=True, exist_ok=True)
def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)
def http(method, path, body=None, timeout=120):
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body is not None else None, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read(); ct = r.headers.get("Content-Type", "")
        return json.loads(raw) if "json" in ct else raw.decode("utf-8", "replace")

def create():
    aukus = (ROOT / "data/study/source_aukus.txt").read_text(); subsea = (ROOT / "data/study/source_subsea.txt").read_text()
    body = {"sources": [{"kind": "paste", "title": "Wijaya and Hayes 2025 — AUKUS behind the scenes", "text": aukus},
                        {"kind": "paste", "title": "Abels 2026 — Private network realignment (subsea cables)", "text": subsea}],
            "intent": "What do these two papers establish about how states steer private networks and markets — with the numbers and the sequence of events as the sources give them, and where each paper's argument is weakest?",
            "audience": "executive", "depth": "medium", "output": {"tables": True, "figures": 0, "plates": 0}, "spend_cap_usd": 8.0,
            "entry": "chosen", "path": {"steps": [{"engine_key": "statistical_evidence", "depth": "standard"}, {"engine_key": "event_timeline_causal", "depth": "standard"}, {"engine_key": "argument_architecture", "depth": "standard"}], "depth": "medium"}}
    r = http("POST", "/v1/dossier/jobs", body); log("created", r); return r["job_id"]

def wait(job_id):
    seen = set(); t0 = time.time()
    while time.time() - t0 < 60 * 60:
        j = http("GET", f"/v1/dossier/jobs/{job_id}")
        st, step = j.get("status"), j.get("step")
        if (st, step) not in seen: seen.add((st, step)); log("status", st, "step", step)
        if st == "awaiting_brief":
            b = http("GET", f"/v1/dossier/jobs/{job_id}/brief"); opts = b.get("options") or (b.get("brief") or {}).get("options") or []
            key = (b.get("recommendation") or {}).get("option_key") or (opts[0]["key"] if opts else "own_path")
            log("brief ready; choosing", key, "of", [o.get("key") for o in opts]); http("POST", f"/v1/dossier/jobs/{job_id}/brief", {"option_key": key})
        if st in ("completed", "failed", "cancelled", "error"): return j
        time.sleep(30)
    return http("GET", f"/v1/dossier/jobs/{job_id}")

def report(job_id, j):
    (OUT / f"{job_id}.job.json").write_text(json.dumps(j, indent=2, ensure_ascii=False))
    try:
        ev = http("GET", f"/v1/dossier/jobs/{job_id}/events"); (OUT / f"{job_id}.events.json").write_text(json.dumps(ev, indent=2, ensure_ascii=False))
    except Exception as exc: ev = []; log("events unavailable:", exc)
    try:
        md = http("GET", f"/v1/dossier/jobs/{job_id}/dossier.md"); (OUT / f"{job_id}.dossier.md").write_text(md if isinstance(md, str) else json.dumps(md)); log("dossier.md", len(md) if isinstance(md, str) else "?", "chars")
    except Exception as exc: log("dossier.md unavailable:", exc)
    events = ev if isinstance(ev, list) else (ev.get("events") or ev.get("items") or [])
    spine = [e for e in events if (e.get("payload_json") or e.get("payload") or {}).get("kind") == "spine"]
    for e in spine:
        p = e.get("payload_json") or e.get("payload") or {}
        log("SPINE thesis:", p.get("thesis")); [log("  section", s.get("key"), "| findings:", s.get("findings"), "| table:", s.get("table")) for s in p.get("sections", [])]
    walls = [e for e in events if "anchor wall" in str(e.get("detail", ""))]
    for e in walls[:8]: log("TABLE WALL:", e.get("detail")[:200])
    procs = [e for e in events if "process" in str(e.get("detail", "")).lower() and "call" in str(e.get("detail", "")).lower()]
    for e in procs[:6]: log("PROCESS:", str(e.get("detail"))[:200])
    log("job:", j.get("status"), "| cost:", j.get("cost_usd") or j.get("spend_usd") or (j.get("options") or {}).get("spend_cap_usd"))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--job", default=""); a = ap.parse_args()
    job_id = a.job or create(); j = wait(job_id); report(job_id, j); log("DONE", job_id)
