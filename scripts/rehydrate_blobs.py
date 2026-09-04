"""Re-hydrate a live The Analyst service from local backups (2026-09-04).

Usage: ADMIN_TOKEN=... python scripts/rehydrate_blobs.py [--api URL] [--jobs id,id] [--import-missing]

For each data/dossiers/live-<job_id>/ backup: uploads dossier.{html,md,pdf},
plates (matched by key against the live plates listing; plate-1.jpg is the
first plate), and figures (figure-N.jpg in job.json order) to the admin blob
endpoint; with --import-missing, jobs absent from the live service are
re-created from job.json first.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
BACKUPS = ROOT / "data" / "dossiers"


def put(api: str, token: str, key: str, mime: str, data: bytes) -> None:
    r = requests.put(f"{api}/v1/dossier/admin/blobs/{key}", data=data, headers={"content-type": mime, "x-admin-token": token}, timeout=300)
    r.raise_for_status()
    print(f"  put {key} ({len(data):,} bytes)")


def meta_blob(figure_id: str, job_id: str, name: str, data: bytes) -> bytes:
    return json.dumps({
        "figure_id": figure_id, "job_id": job_id, "name": name, "mime_type": "image/jpeg", "ext": "jpg",
        "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "width": None, "height": None,
        "created_at": datetime.now(timezone.utc).isoformat(), "url": f"/v1/figures/{figure_id}", "restored": True,
    }).encode("utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default="https://the-analyst-kcuc.onrender.com")
    ap.add_argument("--jobs", default="")
    ap.add_argument("--import-missing", action="store_true")
    args = ap.parse_args()
    token = os.environ.get("ADMIN_TOKEN")
    if not token:
        sys.exit("ADMIN_TOKEN required")
    wanted = {j.strip() for j in args.jobs.split(",") if j.strip()}
    for d in sorted(BACKUPS.glob("live-dossier-*")):
        job_id = d.name.replace("live-", "")
        if wanted and job_id not in wanted:
            continue
        job_json = d / "job.json"
        if not job_json.exists():
            print(f"{job_id}: no job.json, skipping")
            continue
        job = json.loads(job_json.read_text())
        live = requests.get(f"{args.api}/v1/dossier/jobs/{job_id}", timeout=60)
        exists = live.ok and isinstance(live.json(), dict) and live.json().get("id") == job_id
        print(f"== {job_id} live={exists} status={job.get('status')}")
        if not exists:
            if not args.import_missing:
                print("  absent on live; pass --import-missing to restore the record")
                continue
            r = requests.put(f"{args.api}/v1/dossier/admin/jobs/{job_id}", json=job, headers={"x-admin-token": token}, timeout=120)
            r.raise_for_status()
            print(f"  imported job record: {r.json()}")
        # dossier files
        for kind, mime in (("html", "text/html"), ("md", "text/markdown"), ("pdf", "application/pdf")):
            f = d / f"dossier.{kind}"
            if f.exists():
                put(args.api, token, f"dossier:{job_id}:{kind}", mime, f.read_bytes())
        # figures: job.json order ↔ figure-N.jpg
        for i, fig in enumerate(job.get("figures") or [], start=1):
            f = d / f"figure-{i}.jpg"
            fid = fig.get("figure_id")
            if f.exists() and fid:
                data = f.read_bytes()
                put(args.api, token, f"figure:{fid}", "image/jpeg", data)
                put(args.api, token, f"figure-meta:{fid}", "application/json", meta_blob(fid, job_id, fig.get("key", ""), data))
        # plates: live listing keys ↔ plate-<key>.jpg (plate-1.jpg = first plate)
        pl = requests.get(f"{args.api}/v1/dossier/jobs/{job_id}/plates", timeout=60)
        plates = pl.json() if pl.ok else []
        plates = plates if isinstance(plates, list) else plates.get("plates", [])
        for i, p in enumerate(plates, start=1):
            key = p.get("key")
            f = d / f"plate-{key}.jpg"
            if not f.exists() and i == 1:
                f = d / "plate-1.jpg"
            if not f.exists():
                print(f"  plate {key}: no local file")
                continue
            data = f.read_bytes()
            put(args.api, token, f"plate:{job_id}:{key}.jpg", "image/jpeg", data)
            if p.get("figure_id"):
                put(args.api, token, f"figure:{p['figure_id']}", "image/jpeg", data)
                put(args.api, token, f"figure-meta:{p['figure_id']}", "application/json", meta_blob(p["figure_id"], job_id, f"plate-{key}", data))


if __name__ == "__main__":
    main()
