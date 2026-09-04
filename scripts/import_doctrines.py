"""Import doctrine files for mirrored engines from the organs' repos (Phase B, step 1).

For every engine definition whose lineage_refs name a Markdown file that exists
under ~/projects/<repo>/<path>, copy it to src/engines/doctrines/<engine_key>/
and record it in the definition's `doctrine_files` with a sha256. The Master
then serves the text at GET /v1/engines/{key}/doctrine, hash-pinned, so an organ
can read its prompt from the registry and keep the hash in its receipts.

Idempotent. Never touches analytical engines (they have no lineage_refs).
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFS = ROOT / "src" / "engines" / "definitions"
DOCTRINES = ROOT / "src" / "engines" / "doctrines"
PROJECTS = Path(os.environ.get("PROJECTS_DIR", str(Path.home() / "projects")))

# Named third parties never travel into served doctrine text (owner, 2026-09-04). Applied to every imported file.
SCRUB = [("de Meo's", "the CEO's"), ("De Meo's", "The CEO's"), ("de Meo", "the CEO"), ("De Meo", "The CEO"),
         ("Kering's", "the house's"), ("Kering-type", "client-type"), ("Kering", "the house"), ("kering", "house")]


def scrub(text: str) -> str:
    for a, b in SCRUB:
        text = text.replace(a, b)
    return text


def resolve(ref: str) -> Path | None:
    if ":" not in ref:
        return None
    repo, rest = ref.split(":", 1)
    path = rest.split(":", 1)[0]  # drop :line
    if not path.endswith(".md"):
        return None
    candidate = PROJECTS / repo / path
    return candidate if candidate.is_file() else None


def main() -> None:
    imported = 0
    for f in sorted(DEFS.glob("*.json")):
        data = json.loads(f.read_text())
        refs = data.get("lineage_refs") or []
        if not refs:
            continue
        files = []
        for ref in refs:
            src = resolve(ref)
            if src is None:
                continue
            dest_dir = DOCTRINES / data["engine_key"]
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / src.name
            dest.write_text(scrub(src.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
            text = dest.read_bytes()
            files.append({
                "name": src.name,
                "source_ref": ref,
                "sha256": hashlib.sha256(text).hexdigest(),
                "chars": len(text.decode("utf-8", "replace")),
            })
            imported += 1
        if files:
            # preserve entries this importer does not produce (e.g. data files such as approach_windows.json)
            names = {x["name"] for x in files}
            keep = [x for x in data.get("doctrine_files", []) if x.get("name") not in names and not str(x.get("name", "")).endswith(".md")]
            data["doctrine_files"] = files + keep
            f.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"imported {imported} doctrine files")


if __name__ == "__main__":
    main()
