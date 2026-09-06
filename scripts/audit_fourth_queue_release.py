"""Audit explicit fourth-queue release decisions, source custody and ordinary desk offers.

The source judgments are recorded by the reader in release_decisions.json. This script
checks their artifact identities, anchors, IDs, scores and catalog wiring, not meaning.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.study_fourth_queue import study as s
from src.dossier.catalog import purpose_catalog, resolve_path_request
from src.dossier.schemas import PathRequest, PathStepRequest


def audit():
    base = s.ARCHIVE
    decisions = json.loads((base / "release_decisions.json").read_text())
    offers = purpose_catalog(n_docs=1)
    placed = {e["engine_key"]: g["key"] for g in offers["groups"] for e in g["engines"]}
    records = {}
    totals = {"known_actual_usd": 0.0, "conservative_known_usd": 0.0,
              "unknown_use_reserve_usd": 0.0, "calls": 0, "failed_calls": 0}
    for folder in (base, base / "repairs"):
        for call in json.loads((folder / "calls.json").read_text())["calls"]:
            assert call["status"] != "running", call["path"]
            totals["calls"] += 1
            totals["failed_calls"] += call["status"] != "complete"
            if call.get("cost_usd") is None:
                totals["unknown_use_reserve_usd"] += call["reservation_usd"]
            else:
                totals["conservative_known_usd"] += call["cost_usd"]
                charge = call.get("provider_cost_usd")
                totals["known_actual_usd"] += call["cost_usd"] if charge is None else charge
    for ident, decision in decisions.items():
        design = s.DESIGNS[ident]
        key = design["key"]
        if not decision["released"]:
            assert decision["defect"] and key not in placed, ident
            try:
                resolve_path_request(PathRequest(steps=[PathStepRequest(engine_key=key)]))
            except ValueError:
                pass
            else:
                raise AssertionError(f"Withheld method resolves on the desk: {ident}")
            records[ident] = decision
            continue
        folder = base if decision["stage"] == "first" else base / "repairs"
        frozen = json.loads((folder / "plan.json").read_text())["inputs"]
        for definitions in ("engines/capability_definitions", "operationalizations/definitions"):
            relative = f"src/{definitions}/{key}.yaml"
            assert s.budget.digest((ROOT / relative).read_bytes()) == frozen[relative], ident
        job = f'{ident}__checked__' + "_".join(design["papers"])
        result = json.loads((folder / "results" / f"{job}.json").read_text())
        content = (folder / "outputs" / f"{job}.md").read_text()
        sha = s.budget.digest(content.encode())
        assert result["status"] == "complete" and sha == result["output_sha256"], ident
        assert result["audit"] == s.audit_one(job, content), ident
        audit_file = "first_pass_audit.json" if folder == base else "audit.json"
        record = json.loads((folder / audit_file).read_text())["jobs"][job]
        assert record["mechanical_release_pass"] and record["output_sha256"] == sha, ident
        scores = {}
        for rater in ("sonnet", "sol"):
            score = json.loads((folder / "scores" / f"{job}__{rater}.json").read_text())
            assert score["binding"]["output_sha256"] == sha, ident
            memo = ROOT / score["binding"]["memo_path"]
            assert s.budget.digest(memo.read_bytes()) == score["binding"]["memo_sha256"], ident
            scores[rater] = score["mean"]
        control_folder = base / "repairs" if ident == "I13" else base
        old = f'{ident}__old__' + "_".join(design["papers"])
        original = json.loads((control_folder / "scores" / f"{old}__sonnet.json").read_text())["mean"]
        assert design["inventory"] or scores["sonnet"] >= original, ident
        assert placed[key] == decision["purpose"], ident
        for depth in ("surface", "standard", "deep"):
            path = resolve_path_request(PathRequest(steps=[PathStepRequest(engine_key=key, depth=depth)]))
            assert path.steps[0].engine_key == key and path.steps[0].depth == depth, ident
        records[ident] = {**decision, "output_sha256": sha, "rows": record["rows"],
                          "anchors": record["wall"]["anchors"], "scores": scores,
                          "original_sonnet": original, "catalog_and_paths_pass": True}
    assert set(records) == set(s.DESIGNS)
    totals = {k: round(v, 6) if isinstance(v, float) else v for k, v in totals.items()}
    report = {"mechanics_only": True, "methods": records, "costs": totals}
    s.budget.write(base / "release_audit.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    audit()
