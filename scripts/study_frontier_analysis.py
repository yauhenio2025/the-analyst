"""Aggregate the frontier study (data/study/v3): per-condition means by judge, paired deltas against the
one-call condition on the same model and paper, pairwise records against the Fable one-shot with the
candidate identified, per-model one-call results, judge agreement and position effects. Prints markdown."""
import json, statistics as st, sys
from collections import defaultdict
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "data/study/v3")
man = json.load(open(OUT / "manifest.json")); J = json.load(open(OUT / "judgments.json"))
KEYS = ("specificity", "anchoring", "non_obviousness", "coherence", "usefulness", "hallucination_risk")
JUDGES = ("sonnet", "sol"); by = {m["key"]: m for m in man}
def rub(key, jk):
    r = J["rubric"].get(f"{jk}:{key}"); return None if not r or not all(isinstance(r.get(k), (int, float)) for k in KEYS) else st.mean(r[k] for k in KEYS)
def hal(key, jk):
    r = J["rubric"].get(f"{jk}:{key}"); return None if not r else r.get("hallucination_risk")
def mean(xs): xs = [x for x in xs if x is not None]; return st.mean(xs) if xs else float("nan")
def is_base(k): m = by.get(k); return bool(m) and m["condition"] == "a" and m["model"] == "fable"
def cand(p): return p["B"] if is_base(p["A"]) else p["A"]

for ek in ("conditions_of_possibility_analyzer", "argument_architecture"):
    print(f"\n## {ek}\n")
    print("| condition | rubric mean sonnet / sol | hallucination sonnet / sol (10 = none) | pairwise wins vs Fable one-call, sonnet / sol | mean cost $ | mean seconds | anchors verified | n |\n|---|---|---|---|---|---|---|---|")
    for cond in "abcd":
        ms = [m for m in man if m["engine"] == ek and m["condition"] == cond and m["ledger_rows"] > 0 and not is_base(m["key"])]
        keys = {m["key"] for m in ms}
        pw = {jk: [p for p in J["pairwise"] if p["judge"] == jk and cand(p) in keys] for jk in JUDGES}
        wins = {jk: sum(1 for p in pw[jk] if p["winner"] == cand(p)) for jk in JUDGES}
        ties = {jk: sum(1 for p in pw[jk] if p["winner"] == "tie") for jk in JUDGES}
        label = cond + (" (excluding the Fable baseline itself)" if cond == "a" else "")
        print(f"| {label} | {mean(rub(m['key'],'sonnet') for m in ms):.2f} / {mean(rub(m['key'],'sol') for m in ms):.2f} | {mean(hal(m['key'],'sonnet') for m in ms):.1f} / {mean(hal(m['key'],'sol') for m in ms):.1f} | {wins['sonnet']}/{len(pw['sonnet'])} / {wins['sol']}/{len(pw['sol'])}{' (+' + str(ties['sonnet']+ties['sol']) + ' ties)' if ties['sonnet']+ties['sol'] else ''} | {mean(m['cost_usd'] for m in ms):.2f} | {mean(m['seconds'] for m in ms):.0f} | {mean(m['anchor_rate'] for m in ms):.0%} | {len(ms)} |")
    print("\nPaired deltas on the same model and paper (condition minus the one call), mean and count up / down / same:\n")
    print("| condition | by sonnet | by sol | n |\n|---|---|---|---|")
    for cond in "bcd":
        row = []
        n = 0
        for jk in JUDGES:
            ds = []
            for m in man:
                if m["engine"] != ek or m["condition"] != cond or m["ledger_rows"] == 0: continue
                a = by.get(f"{ek}__a__{m['model']}__{m['paper']}")
                if not a or a["ledger_rows"] == 0: continue
                x, y = rub(m["key"], jk), rub(a["key"], jk)
                if x is not None and y is not None: ds.append(x - y)
            n = len(ds)
            row.append(f"{st.mean(ds):+.2f} ({sum(d > 0 for d in ds)} up / {sum(d < 0 for d in ds)} down / {sum(d == 0 for d in ds)} same)" if ds else "—")
        print(f"| {cond} − a | {row[0]} | {row[1]} | {n} |")
    print("\nThe one call per model (mean of the two papers):\n")
    print("| model | rubric sonnet / sol | hallucination sonnet / sol | wins vs Fable one-call sonnet / sol | cost $ | seconds | anchors | n |\n|---|---|---|---|---|---|---|---|")
    for mk in ("fable", "sol", "kimi3", "sonnet", "dspro", "luna", "dsflash", "kimi"):
        ms = [m for m in man if m["engine"] == ek and m["condition"] == "a" and m["model"] == mk and m["ledger_rows"] > 0]
        if not ms: continue
        keys = {m["key"] for m in ms}
        pw = {jk: [p for p in J["pairwise"] if p["judge"] == jk and cand(p) in keys] for jk in JUDGES}
        wins = {jk: sum(1 for p in pw[jk] if p["winner"] == cand(p)) for jk in JUDGES}
        w = "baseline" if mk == "fable" else f"{wins['sonnet']}/{len(pw['sonnet'])} / {wins['sol']}/{len(pw['sol'])}"
        print(f"| {mk} | {mean(rub(m['key'],'sonnet') for m in ms):.2f} / {mean(rub(m['key'],'sol') for m in ms):.2f} | {mean(hal(m['key'],'sonnet') for m in ms):.1f} / {mean(hal(m['key'],'sol') for m in ms):.1f} | {w} | {mean(m['cost_usd'] for m in ms):.2f} | {mean(m['seconds'] for m in ms):.0f} | {mean(m['anchor_rate'] for m in ms):.0%} | {len(ms)} |")
pairs = defaultdict(dict)
for p in J["pairwise"]: pairs[frozenset((p["A"], p["B"]))][p["judge"]] = p["winner"]
both = [v for v in pairs.values() if len(v) == 2]
print(f"\nJudge agreement on the winner of the same pair (seen in opposite orders): {sum(1 for v in both if v['sonnet'] == v['sol'])}/{len(both)}.")
for jk in JUDGES:
    ps = [p for p in J["pairwise"] if p["judge"] == jk]
    print(f"{jk} as judge: {sum(1 for p in ps if p['winner'] == p['A'])} A-wins, {sum(1 for p in ps if p['winner'] == p['B'])} B-wins, {sum(1 for p in ps if p['winner'] == 'tie')} ties of {len(ps)}; the Fable one-call won {sum(1 for p in ps if is_base(p['winner']))}.")
print(f"\nGeneration ${sum(m['cost_usd'] for m in man):.2f} over {len(man)} runs; judging ${sum(v.get('cost_usd', 0) for v in J['rubric'].values()) + sum(p.get('cost_usd', 0) for p in J['pairwise']):.2f}.")
