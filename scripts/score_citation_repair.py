"""Independent Sonnet + Sol ratings for the fidelity audit's repaired condition, with the study's rubric and recorder.

  TMPDIR=data/tmp python3 -u -m scripts.score_citation_repair [--key G6__index_only_repair]

Requires a committed, hash-bound source memo at communications/study/citation_family_2026_09_06/source_memos/<key>.md.
"""
from pathlib import Path
import argparse, json, re, subprocess, sys, time
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from scripts import study_citation_family as study
from src.llm.client import parse_llm_json_response
s = study.s; OUT = study.OUT / "repairs"; ARCHIVE = study.ARCHIVE / "repairs"
s.budget.OUT = OUT


def _guard(plan):
    # the repair's plan freezes its inputs by hash (no identity field): verify those, as the repair script does
    for path, sha in plan['inputs'].items():
        s.budget.require(s.budget.digest((ROOT / path).read_bytes()) == sha, 'Repair input changed ' + path)
s.budget.guard = _guard


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--key", default="G6__index_only_repair"); a = ap.parse_args()
    from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=False)
    key = a.key; plan = s.budget.read(OUT / "plan.json")
    output = OUT / "outputs" / f"{key}.md"; result = s.budget.read(OUT / "results" / f"{key}.json"); sha = s.budget.digest(output.read_bytes())
    s.budget.require(result["status"] == "complete" and result["output_sha256"] == sha, "Output changed or incomplete")
    memo = study.ARCHIVE / "source_memos" / f"{key}.md"
    s.budget.require(memo.exists() and sha in memo.read_text() and len(memo.read_text()) > 800, "Hash-bound source memo required before scores")
    committed = subprocess.check_output(["git", "show", f"HEAD:{memo.relative_to(ROOT)}"], cwd=ROOT)
    s.budget.require(committed == memo.read_bytes(), "Source memo must be committed")
    binding = {"output_sha256": sha, "memo_sha256": s.budget.digest(committed), "memo_path": str(memo.relative_to(ROOT))}
    job = {"id": "G6", "engine": "citation_fidelity_audit", "condition": "checked", "index_only": True}
    content = output.read_text()
    content = re.sub(r"^### Check receipt\n.*?(?=^## |\Z)", "", content, flags=re.M | re.S)
    content = re.sub(r"^.*[Cc]ritic: (?:openrouter/)?[^\n]+\n?", "", content, flags=re.M)
    user = "\n\n=====\n\n".join(f"SOURCE [{k}]:\n\n{v}" for k, v in study.documents(job).items()) + "\n\nANALYSIS:\n\n" + content
    system = s.RUBRIC + "\nRequested artifact: " + s.DESIGNS["G6"]["ideal"] + "\nKeep each reason concise (one sentence)."
    for rater in ("sonnet", "sol"):
        target = OUT / "scores" / f"{key}__{rater}.json"; callkey = f"judge__{key}__{rater}"
        if target.exists():
            print(key, rater, "already scored"); continue
        s.budget.write(OUT / "judge_inputs" / f"{key}__{rater}.json", {"binding": binding, "prepared_at": time.time(), "system_sha256": s.budget.digest(system.encode()), "user_sha256": s.budget.digest(user.encode())})
        res = s.budget.Recorder(callkey, plan, role=rater)(system, user, model_hint=s.MODELS[rater], label="independent rubric score (repair)")
        score = parse_llm_json_response(res["content"]); s.budget.require(isinstance(score, dict), "Invalid JSON score")
        for criterion in s.budget.RUBRIC_KEYS:
            s.budget.require(isinstance(score.get(criterion), (int, float)) and not isinstance(score[criterion], bool) and 1 <= score[criterion] <= 10, "Invalid criterion score")
        s.budget.write(target, {"score": score, "binding": binding, "rater": rater, "mean": sum(score[k] for k in s.budget.RUBRIC_KEYS) / 6})
        print(key, rater, "SCORED", json.dumps(score), flush=True)
    import shutil
    for folder in ("scores", "judge_inputs", "outputs", "results", "calls"):
        if (OUT / folder).exists(): shutil.copytree(OUT / folder, ARCHIVE / folder, dirs_exist_ok=True)


if __name__ == "__main__":
    main()
