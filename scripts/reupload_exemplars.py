"""Re-upload exemplar inputs to the live service (they live in the executor DB, which is
ephemeral on Render until EXECUTOR_DATABASE_URL is set).

    EXEMPLARS_SRC=~/projects/the-analyst-wt/dossier/data/exemplars python3 scripts/reupload_exemplars.py
"""
import json, os, sys, urllib.request

B = os.environ.get("THE_ANALYST_URL", "https://the-analyst-kcuc.onrender.com")
SRC = os.path.expanduser(os.environ.get("EXEMPLARS_SRC", "data/exemplars"))
ITEMS = [
    ("fashion_bundle.txt", "Fashion under sustainability and platform pressure — 5 papers",
     "Dholakia & Ziliberberg 2024; Kuang et al. 2024; Özdil & Konuralp 2025; Nassar et al. 2021; Hewitt et al. 2024 (stacks export)"),
    ("kering_study.md", "Kering on the public record (study, 2026-07-19)", "Owner's verified study of Kering/de Meo statements"),
]
for name, title, desc in ITEMS:
    path = os.path.join(SRC, name)
    if not os.path.exists(path):
        print("missing", path); continue
    body = {"name": name, "title": title, "description": desc, "text": open(path, encoding="utf-8").read()}
    req = urllib.request.Request(B + "/v1/dossier/exemplars", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=300) as resp:
        d = json.loads(resp.read()); print("uploaded", d["name"], d["char_count"], "chars,", d["document_count"], "docs")
