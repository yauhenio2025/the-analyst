"""em:U3HITB25 both ways: the Analyst's fidelity audit (per statement × source pair, six verdicts) beside the Stacks'
digest_check runs (per statement, four verdicts). Rolls our pair verdicts up per statement (the worst verdict across its
pairs, in the order accurate < fair < selective < unverifiable < stretched < misattributed) and writes the side-by-side.

  python3 -m scripts.compare_memo_fidelity data/study/memo_fidelity_2026_09_06/<stem>
"""
from __future__ import annotations
import json, re, sys
from collections import Counter
from pathlib import Path

ROW = re.compile(r"^\[([A-Z]\d)\.F(\d+)\]", re.M)
ORDER = ["accurate", "fair", "selective", "unverifiable", "stretched", "misattributed"]
STACKS_TO_OURS = {"supported": "accurate", "partly": "fair", "unsupported": "unverifiable", "misattributed": "misattributed", "unchecked": "unverifiable"}


def field(row: str, name: str) -> str:
    m = re.search(rf"— {re.escape(name)}: (.*?)(?= — [a-z-]+: |$)", row)
    return (m.group(1).strip() if m else "")


def main():
    d = Path(sys.argv[1])
    pairs = json.load(open(d / "pairs.json"))
    ours: dict[int, list] = {}
    for p in pairs:
        m = re.match(r"st(\d+)/(\S+)", p["pair"])
        if not m:
            continue
        ours.setdefault(int(m.group(1)), []).append({"pair": p["pair"], "verdict": p["verdict"], "reason": (p.get("reason") or p.get("comparison") or "")[:200], "id": p["finding"], "source": p["source"]})
    stacks = json.load(open(d.parent / "stacks_runs_verdicts.json"))
    runs = {k: v for k, v in stacks["runs"].items()}
    table, agree = [], Counter()
    for s in stacks["statements"]:
        no = s["no"]; ps = ours.get(no, [])
        worst = max((p["verdict"] for p in ps if p["verdict"] in ORDER), key=ORDER.index, default="")
        theirs = {k: v["verdict"] for k, v in s["stacks"].items()}
        row = {"no": no, "section": s["section"], "cited": s["sources"], "ours_pairs": ps, "ours_worst": worst, "stacks": theirs}
        for k, tv in theirs.items():
            if worst:
                agree[(k, "same" if STACKS_TO_OURS.get(tv) == worst else "differ")] += 1
        table.append(row)
    summary = {"statements": len(table), "statements_with_our_verdict": sum(1 for t in table if t["ours_worst"]),
               "our_pair_verdicts": Counter(p["verdict"] for ps in ours.values() for p in ps),
               "our_worst_per_statement": Counter(t["ours_worst"] for t in table if t["ours_worst"]),
               "stacks_runs": {k: {kk: v[kk] for kk in ("model", "n", "supported", "partly", "unsupported", "misattributed", "cost")} for k, v in runs.items()},
               "agreement_by_run": {f"{k[0]}:{k[1]}": n for k, n in sorted(agree.items())},
               "flagged_by_us_not_them": [t["no"] for t in table if t["ours_worst"] in ("stretched", "misattributed") and all(v == "supported" for v in t["stacks"].values())],
               "flagged_by_them_not_us": [t["no"] for t in table if t["ours_worst"] in ("accurate", "fair") and any(v in ("unsupported", "misattributed") for v in t["stacks"].values())]}
    (d / "comparison.json").write_text(json.dumps({"summary": summary, "table": table}, indent=1, ensure_ascii=False, default=str))
    lines = ["| no | section | cited | ours (worst of pairs) | pairs | Stacks Sonnet 5 (run 4) | Stacks Gemini (run 5) |", "|---|---|---|---|---|---|---|"]
    for t in table:
        pairs = ", ".join(f"{p['pair'].split('/')[1]}:{p['verdict']}" for p in t["ours_pairs"])
        s4 = next((v for k, v in t["stacks"].items() if k.startswith("run4")), ""); s5 = next((v for k, v in t["stacks"].items() if k.startswith("run5")), "")
        lines.append(f"| {t['no']} | {t['section']} | {' '.join(t['cited'])} | {t['ours_worst']} | {pairs} | {s4} | {s5} |")
    (d / "comparison.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=1, default=str))


if __name__ == "__main__":
    main()
