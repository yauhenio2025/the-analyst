"""Does a cheap critic over a strong model's one-call reading make its ledger more reliable? (2026-09-05, owner's ask)

For every one-call reading in the frontier study (data/study/v3, condition a: 7 models × 2 papers × 2 engines), run
the critic (DeepSeek V4 Pro) over its findings against the source, apply the rulings by code (run_oneshot_checked with
the reading already on disk), and judge the BEFORE and AFTER ledgers blind on Sonnet, both orders: which is the more
reliable evidence base (every finding supported by its quote in context, no over-reading, no claims about the authors,
fewer misses). Hard measures alongside: anchor rate before / after, rows rejected / weakened / added per model.

  python scripts/study_oneshot_check.py            # run + judge + report (resumable)
  python scripts/study_oneshot_check.py --report   # report only
"""
from __future__ import annotations
import argparse, json, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from src.engines.registry import get_engine_registry  # noqa: E402
from src.events.pricing import estimate_cost  # noqa: E402
from src.executor.context_broker import split_ledger  # noqa: E402
from src.executor.engine_runner import run_engine_call  # noqa: E402
from src.executor.ledger_walls import SourceIndex, parse_rows, verify_rows  # noqa: E402
from src.executor.process_runner import run_oneshot_checked  # noqa: E402
from src.llm.client import parse_llm_json_response  # noqa: E402
from src.operationalizations.registry import get_operationalization_registry  # noqa: E402

V3 = ROOT / "data/study/v3"; OUT = ROOT / "data/study/v3_check"; (OUT / "outputs").mkdir(parents=True, exist_ok=True)
PAPERS = {"aukus": ROOT / "data/study/source_aukus.txt", "subsea": ROOT / "data/study/source_subsea.txt"}
CRITIC = "openrouter/deepseek/deepseek-v4-pro"; JUDGE = "claude-sonnet-4-6"; lock = threading.Lock()
def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)
def load(p, d): return json.loads(p.read_text()) if p.exists() else d
def save(p, o):
    with lock: p.write_text(json.dumps(o, indent=2, ensure_ascii=False))

def ledger_of(text): return split_ledger(text)[1]

def check_one(m, sources, results):
    key = m["key"]
    if key in results and (OUT / "outputs" / f"{key}__checked.md").exists(): return
    cap = get_engine_registry().get_capability_definition(m["engine"]); spec = get_operationalization_registry().get(m["engine"]).process
    reading = (V3 / m["file"]).read_text(); src = sources[m["paper"]]; t0 = time.time()
    try:
        run = run_oneshot_checked(cap, spec, {"doc": src}, reading=reading, tier_overrides={"mid": CRITIC})
    except Exception as exc:  # noqa: BLE001
        log(f"FAILED {key}: {exc}"); return
    (OUT / "outputs" / f"{key}__checked.md").write_text(run.final_content, encoding="utf-8")
    vc = run.calls[-1]; w = vc.wall
    before = verify_rows(parse_rows(ledger_of(reading)), SourceIndex({"doc": src}))
    with lock:
        results[key] = {"engine": m["engine"], "model": m["model"], "paper": m["paper"], "critic": vc.model_used, "cost_usd": round(vc.cost_usd, 4), "seconds": round(time.time() - t0, 1),
                        "rows_before": before.rows, "anchor_before": before.anchor_rate, "rows_after": w["rows"], "anchor_after": w["anchor_rate"],
                        **{k: w[k] for k in w if k.startswith("check_")}}
    save(OUT / "results.json", results)
    r = results[key]; log(f"checked {key}: {r['rows_before']}→{r['rows_after']} rows, anchors {r['anchor_before']:.0%}→{r['anchor_after']:.0%}, rejected {r['check_rejected']} weakened {r['check_weakened']} added {r['check_added']}, ${r['cost_usd']:.2f}, {r['seconds']:.0f}s")

PAIR = ("Two findings ledgers about the same SOURCE, produced by two analysts. Each row is a finding with a verbatim anchor. Which ledger is the "
        "more reliable evidence base for a reader who will cite rows as facts about the text? Check rows against the source: is each finding "
        "supported by its anchor read in context; is anything over-read or asserted about the authors rather than the text; does either ledger "
        "miss something important the text supports? Prefer support and completeness over length; extra rows only count if they are right. "
        'Answer as JSON: {"winner": "A"|"B"|"tie", "margin": "slight"|"clear"|"decisive", "why": "...", "unsupported_in_A": n, "unsupported_in_B": n, "misses_in_A": n, "misses_in_B": n}')

def judge(results, sources, J):
    jobs = []
    for key in results:
        m = results[key]; before = ledger_of((V3 / "outputs" / f"{key}.md").read_text()); after_full = (OUT / "outputs" / f"{key}__checked.md").read_text()
        after = split_ledger(after_full)[1].split("### Check receipt")[0].split("### Unverified anchors")[0]
        # the critic's rejected rows are a receipt, not part of the AFTER ledger the desks read
        after = after.split("### Rejected by the critic")[0]
        for order, (a, b, an, bn) in enumerate(((before, after, "before", "after"), (after, before, "after", "before"))):
            if any(j["key"] == key and j["A"] == an for j in J): continue
            jobs.append((key, m, a, b, an, bn))
    log(f"judging {len(jobs)} pairs on {JUDGE}")
    def _do(job):
        key, m, a, b, an, bn = job
        user = f"SOURCE:\n\n{sources[m['paper']]}\n\n=====\n\nLEDGER A:\n\n{a}\n\n=====\n\nLEDGER B:\n\n{b}"
        try:
            res = run_engine_call(system_prompt=PAIR, user_message=user, phase_number=1.0, model_hint=JUDGE, depth="standard", label=f"check-judge {key} {an}/{bn}")
            r = parse_llm_json_response(res["content"]); w = r.get("winner"); win = an if w == "A" else bn if w == "B" else "tie"
            with lock: J.append({"key": key, "engine": m["engine"], "model": m["model"], "paper": m["paper"], "A": an, "B": bn, "winner": win, "margin": r.get("margin"), "why": r.get("why", ""),
                                 "unsupported": {an: r.get("unsupported_in_A"), bn: r.get("unsupported_in_B")}, "misses": {an: r.get("misses_in_A"), bn: r.get("misses_in_B")},
                                 "cost_usd": estimate_cost(res.get("model_used") or JUDGE, res["input_tokens"], res["output_tokens"]) or 0.0})
            log("pair", key[:50], an, "vs", bn, "->", win, r.get("margin"))
        except Exception as exc:  # noqa: BLE001
            log(f"judge failed {key} {an}/{bn}: {exc}")
        save(OUT / "judgments.json", J)
    with ThreadPoolExecutor(max_workers=4) as pool: list(pool.map(_do, jobs))
    save(OUT / "judgments.json", J)

def report(results, J):
    import statistics as st
    lines = ["# One call, then the critic: does the check make the ledger more reliable? (2026-09-05)", "",
             f"{len(results)} readings checked by {CRITIC.split('/')[-1]}; judged blind on {JUDGE}, both orders, ledger against ledger with the source in view.", ""]
    wins = {"after": 0, "before": 0, "tie": 0}
    for j in J: wins[j["winner"]] = wins.get(j["winner"], 0) + 1
    lines += [f"**Head-to-head, after-check ledger vs before:** after wins {wins['after']}, before wins {wins['before']}, ties {wins['tie']} of {len(J)}.", ""]
    both = {}
    for j in J: both.setdefault(j["key"], {})[j["A"]] = j["winner"]
    agree_after = sum(1 for v in both.values() if len(v) == 2 and set(v.values()) == {"after"}); agree_before = sum(1 for v in both.values() if len(v) == 2 and set(v.values()) == {"before"})
    lines += [f"Both orders agree: after better in {agree_after}, before better in {agree_before}, split or tie in {len(both) - agree_after - agree_before} of {len(both)} readings.", ""]
    ua = [j["unsupported"]["after"] for j in J if isinstance(j["unsupported"].get("after"), (int, float))]; ub = [j["unsupported"]["before"] for j in J if isinstance(j["unsupported"].get("before"), (int, float))]
    ma = [j["misses"]["after"] for j in J if isinstance(j["misses"].get("after"), (int, float))]; mb = [j["misses"]["before"] for j in J if isinstance(j["misses"].get("before"), (int, float))]
    if ua and ub: lines += [f"Judge's counts per ledger (mean): unsupported rows before {st.mean(ub):.1f} → after {st.mean(ua):.1f}; misses before {st.mean(mb):.1f} → after {st.mean(ma):.1f}.", ""]
    lines += ["| engine | model | paper | rows before → after | anchors before → after | rejected | weakened | added | after wins (of 2) | critic $ | s |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for key, r in sorted(results.items(), key=lambda kv: (kv[1]["engine"], kv[1]["model"], kv[1]["paper"])):
        w = sum(1 for j in J if j["key"] == key and j["winner"] == "after")
        lines.append(f"| {r['engine'][:12]} | {r['model']} | {r['paper']} | {r['rows_before']} → {r['rows_after']} | {r['anchor_before']:.0%} → {r['anchor_after']:.0%} | {r['check_rejected']} | {r['check_weakened']} | {r['check_added']} | {w} | {r['cost_usd']:.2f} | {r['seconds']:.0f} |")
    lines += ["", "Per model (mean over engines and papers):", "", "| model | rejected | weakened | added | anchors before → after | after wins of pairs |", "|---|---|---|---|---|---|"]
    for mk in sorted({r["model"] for r in results.values()}):
        rs = [r for r in results.values() if r["model"] == mk]; keys = {k for k, r in results.items() if r["model"] == mk}
        js = [j for j in J if j["key"] in keys]
        lines.append(f"| {mk} | {st.mean(r['check_rejected'] for r in rs):.1f} | {st.mean(r['check_weakened'] for r in rs):.1f} | {st.mean(r['check_added'] for r in rs):.1f} | {st.mean(r['anchor_before'] for r in rs):.0%} → {st.mean(r['anchor_after'] for r in rs):.0%} | {sum(1 for j in js if j['winner']=='after')}/{len(js)} |")
    lines += ["", f"Critic cost ${sum(r['cost_usd'] for r in results.values()):.2f}; judging ${sum(j.get('cost_usd', 0) for j in J):.2f}.", ""]
    (OUT / "REPORT.md").write_text("\n".join(lines)); log("wrote", OUT / "REPORT.md")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--report", action="store_true"); ap.add_argument("--no-judge", action="store_true"); a = ap.parse_args()
    man = [m for m in json.loads((V3 / "manifest.json").read_text()) if m["condition"] == "a" and m["ledger_rows"] > 0]
    sources = {p: PAPERS[p].read_text(encoding="utf-8", errors="replace") for p in PAPERS}
    results = load(OUT / "results.json", {}); J = load(OUT / "judgments.json", [])
    if not a.report:
        with ThreadPoolExecutor(max_workers=4) as pool: list(pool.map(lambda m: check_one(m, sources, results), man))
        if not a.no_judge: judge(results, sources, J)
    report(results, J); log("DONE")
