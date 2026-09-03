"""Export The Analyst's own desk prompts as doctrine files (Phase B for native engines).

The dossier desks keep their system prompts as Python constants. This writes each
one to src/engines/doctrines/<engine_key>/<CONSTANT>.md and records it in the
engine definition's doctrine_files (source_ref = the-analyst:src/...py:CONSTANT),
so GET /v1/engines/{key}/doctrine serves the very text the desk runs on.

Idempotent: entries whose source_ref starts with "the-analyst:" are replaced.
"""
from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT))
DEFS = ROOT / "src" / "engines" / "definitions"
DOCTRINES = ROOT / "src" / "engines" / "doctrines"

MAP = {
    "analyst_reconnaissance": ("src.dossier.reconnaissance", ["SYSTEM"]),
    "analyst_brief": ("src.dossier.brief", ["SYSTEM_HEAD"]),
    "analyst_plan": ("src.dossier.plan", ["SYSTEM"]),
    "analyst_spine": ("src.dossier.spine", ["SYSTEM"]),
    "analyst_tables": ("src.dossier.tables", ["SYSTEM", "SPINE_SYSTEM"]),
    "analyst_figure_planner": ("src.dossier.figures", ["SPINE_SYSTEM"]),
    "analyst_plate_planner": ("src.dossier.plates", ["SYSTEM", "PLATE_CHECK_PROMPT"]),
    "analyst_compose": ("src.dossier.compose", ["SYSTEM", "DRAFT_SYSTEM", "FRAMES_SYSTEM"]),
    "analyst_crosscheck": ("src.dossier.crosscheck", ["SYSTEM"]),
    "analyst_receipts": ("src.events.narrator", ["SYSTEM_PROMPT"]),
}


def main() -> None:
    n = 0
    for key, (module_name, consts) in MAP.items():
        mod = importlib.import_module(module_name)
        path = DEFS / f"{key}.json"
        data = json.loads(path.read_text())
        files = [f for f in data.get("doctrine_files", []) if not str(f.get("source_ref", "")).startswith("the-analyst:")]
        for const in consts:
            value = getattr(mod, const, None)
            if not isinstance(value, str) or not value.strip():
                continue
            src_path = module_name.replace(".", "/") + ".py"
            text = f"<!-- {src_path}:{const} — served by The Master; the desk runs on this text -->\n\n" + value.strip() + "\n"
            dest_dir = DOCTRINES / key
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / f"{const}.md"
            dest.write_text(text)
            files.append({
                "name": dest.name,
                "source_ref": f"the-analyst:{src_path}:{const}",
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "chars": len(text),
            })
            n += 1
        data["doctrine_files"] = files
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"exported {n} native doctrine files")


if __name__ == "__main__":
    main()
