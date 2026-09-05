"""Two more engines under the shape (2026-09-05): do the rewritten, text-facing questions beat the engine's original
questions in one call on the same model? For inferential_commitment_mapper and epistemological_method_detector on the
two study papers: (old) one call on GPT-5.6 Sol carrying the capability YAML's original probing questions with the
anchoring law and ledger format; (new) the redesigned one call + DeepSeek critic (`run_oneshot_checked`, the production
default at standard depth). Judged blind on Sonnet, both orders, reading against reading with the source in view.

  python scripts/study_two_engines.py            # run + judge + report (resumable)
"""
from __future__ import annotations
import json, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from src.engines.registry import get_engine_registry  # noqa: E402
from src.events.pricing import estimate_cost  # noqa: E402
from src.executor.context_broker import split_ledger  # noqa: E402
from src.executor.engine_runner import run_engine_call, run_engine_call_auto  # noqa: E402
from src.executor.ledger_walls import SourceIndex, parse_rows, verify_rows  # noqa: E402
from src.executor.process_runner import run_oneshot_checked  # noqa: E402
from src.llm.client import parse_llm_json_response  # noqa: E402
from src.operationalizations.registry import get_operationalization_registry  # noqa: E402
from src.stages.process_composer import ANCHORING_LAW, LEDGER_HEADING  # noqa: E402

OUT = ROOT / "data/study/v4_two_engines"
PAPERS = {"aukus": ROOT / "data/study/source_aukus.txt", "subsea": ROOT / "data/study/source_subsea.txt"}
ENGINES = ("inferential_commitment_mapper", "epistemological_method_detector")
MODEL = "openrouter/openai/gpt-5.6-sol"; JUDGE = "claude-sonnet-4-6"; lock = threading.Lock()
def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)
def load(p, d): return json.loads(p.read_text()) if p.exists() else d
def save(p, o):
    with lock: p.write_text(json.dumps(o, indent=2, ensure_ascii=False))
def anchors(text, src):
    _, led = split_ledger(text); rows = parse_rows(led.split("### Rejected by the critic")[0])
    if not rows: return 0.0, 0
    rep = verify_rows(rows, SourceIndex({"doc": src})); return rep.anchor_rate, rep.rows

def old_prompt(cap):
    qs = [q for d in cap.analytical_dimensions for q in (d.probing_questions or [])]
    return ("\n\n".join([
        f"# {cap.engine_name}", (cap.problematique or "").strip(), f"**Core question**: {cap.researcher_question}",
        "You are an expert reader. Work through these questions in your own order, but do not answer them mechanically one by one; write one coherent reading for an expert who must decide what this text establishes.",
        "\n".join(f"- {q}" for q in qs), ANCHORING_LAW,
        "## Output\nThe reading, then:\n" + LEDGER_HEADING + '\n- [F1] <finding> — anchor: "<verbatim>" — confidence: high|medium|low\n(12-30 rows)\n### Counter-evidence\n### Open questions']))

def generate(engine, paper, cond, results, sources):
    key = f"{engine}__{cond}__{paper}"
    if key in results and (OUT / "outputs" / f"{key}.md").exists(): return
    cap = get_engine_registry().get_capability_definition(engine); spec = get_operationalization_registry().get(engine).process; src = sources[paper]; t0 = time.time()
    try:
        if cond == "old":
            res = run_engine_call_auto(system_prompt=old_prompt(cap), user_message=f"SOURCE [doc]:\n\n{src}", phase_number=1.0, model_hint=MODEL, depth="standard", label=f"v4 {key}")
            content = res["content"]; calls = [{"step": "old_oneshot", "model": res.get("model_used"), "cost": estimate_cost(res.get("model_used") or MODEL, res["input_tokens"], res["output_tokens"]) or 0.0}]
        else:
            run = run_oneshot_checked(cap, spec, {"doc": src}, tier_overrides={"strong": MODEL})
            content = run.final_content; calls = [{"step": c.step_key, "model": c.model_used, "cost": c.cost_usd, "wall": c.wall} for c in run.calls]
    except Exception as exc:  # noqa: BLE001
        log(f"FAILED {key}: {exc}"); return
    (OUT / "outputs" / f"{key}.md").write_text(content, encoding="utf-8"); rate, rows = anchors(content, src)
    with lock: results[key] = {"engine": engine, "paper": paper, "condition": cond, "cost_usd": round(sum(c["cost"] for c in calls), 4), "seconds": round(time.time() - t0, 1), "chars": len(content), "anchor_rate": rate, "rows": rows, "calls": calls}
    save(OUT / "results.json", results); log(f"done {key}: {len(content):,} chars, ${results[key]['cost_usd']:.2f}, {results[key]['seconds']:.0f}s, anchors {rate:.0%} of {rows}")

PAIR = ("Two analyses of the same source by the same method. Which is the better reading for an expert who must decide what this text establishes: more specific "
        "to this text, better anchored in real quotes, less obvious, more coherent, more useful, fewer unsupported claims (including claims about the authors rather "
        "than the text)? Judge the reading, not the length. Answer as JSON: "
        '{"winner": "A"|"B"|"tie", "margin": "slight"|"clear"|"decisive", "why": "...", "what_A_has_that_B_lacks": "...", "what_B_has_that_A_lacks": "..."}')

def judge(results, sources, J):
    jobs = []
    for engine in ENGINES:
        for paper in PAPERS:
            o, n = f"{engine}__old__{paper}", f"{engine}__new__{paper}"
            if o not in results or n not in results: continue
            for a, b in ((o, n), (n, o)):
                if any(j["A"] == a and j["B"] == b for j in J): continue
                jobs.append((engine, paper, a, b))
    log(f"judging {len(jobs)} pairs on {JUDGE}")
    def _do(job):
        engine, paper, a, b = job
        user = f"SOURCE:\n\n{sources[paper]}\n\n=====\n\nANALYSIS A:\n\n{(OUT / 'outputs' / f'{a}.md').read_text()}\n\n=====\n\nANALYSIS B:\n\n{(OUT / 'outputs' / f'{b}.md').read_text()}"
        try:
            res = run_engine_call(system_prompt=PAIR, user_message=user, phase_number=1.0, model_hint=JUDGE, depth="standard", label=f"v4 judge {a} vs {b}")
            r = parse_llm_json_response(res["content"]);
            if isinstance(r, list): r = next((x for x in r if isinstance(x, dict)), {})
            w = r.get("winner"); win = a if w == "A" else b if w == "B" else "tie"
            with lock: J.append({"engine": engine, "paper": paper, "A": a, "B": b, "winner": win, "margin": r.get("margin"), "why": r.get("why", ""), "A_has": r.get("what_A_has_that_B_lacks", ""), "B_has": r.get("what_B_has_that_A_lacks", ""), "cost_usd": estimate_cost(res.get("model_used") or JUDGE, res["input_tokens"], res["output_tokens"]) or 0.0})
            log("pair", engine[:14], paper, a.split("__")[1], "vs", b.split("__")[1], "->", win.split("__")[1] if win != "tie" else "tie", r.get("margin"))
        except Exception as exc:  # noqa: BLE001
            log(f"judge failed {a} vs {b}: {exc}")
        save(OUT / "judgments.json", J)
    with ThreadPoolExecutor(max_workers=4) as pool: list(pool.map(_do, jobs))
    save(OUT / "judgments.json", J)

def report(results, J):
    lines = ["# Two more engines under the shape (2026-09-05): rewritten questions + check vs the original questions, one call on GPT-5.6 Sol", "",
             f"Judged blind on {JUDGE}, both orders, reading against reading with the source in view.", "",
             "| engine | paper | new wins (of 2) | margins | old $ / s / anchors / rows | new $ / s / anchors / rows |", "|---|---|---|---|---|---|"]
    for engine in ENGINES:
        for paper in PAPERS:
            o, n = results.get(f"{engine}__old__{paper}"), results.get(f"{engine}__new__{paper}")
            if not o or not n: continue
            js = [j for j in J if j["engine"] == engine and j["paper"] == paper]
            wins = sum(1 for j in js if j["winner"].endswith(f"new__{paper}")); margins = ", ".join(f"{('new' if j['winner'].split('__')[1:2]==['new'] else 'old' if j['winner']!='tie' else 'tie')}/{j['margin']}" for j in js)
            lines.append(f"| {engine} | {paper} | {wins}/{len(js)} | {margins} | {o['cost_usd']:.2f} / {o['seconds']:.0f} / {o['anchor_rate']:.0%} / {o['rows']} | {n['cost_usd']:.2f} / {n['seconds']:.0f} / {n['anchor_rate']:.0%} / {n['rows']} |")
    lines += ["", "## The judge's reasons", ""]
    for j in J:
        lines.append(f"- **{j['engine']} / {j['paper']}**, A = {j['A'].split('__')[1]}, B = {j['B'].split('__')[1]} → {j['winner'].split('__')[1] if j['winner'] != 'tie' else 'tie'} ({j['margin']}): {j['why'][:700]}")
    lines += ["", f"Generation ${sum(r['cost_usd'] for r in results.values()):.2f}; judging ${sum(j.get('cost_usd', 0) for j in J):.2f}."]
    (OUT / "REPORT.md").write_text("\n".join(lines)); log("wrote", OUT / "REPORT.md")

if __name__ == "__main__":
    (OUT / "outputs").mkdir(parents=True, exist_ok=True)
    sources = {p: PAPERS[p].read_text(encoding="utf-8", errors="replace") for p in PAPERS}
    results = load(OUT / "results.json", {}); J = load(OUT / "judgments.json", [])
    specs = [(e, p, c) for e in ENGINES for p in PAPERS for c in ("old", "new")]
    with ThreadPoolExecutor(max_workers=4) as pool: list(pool.map(lambda s: generate(*s, results, sources), specs))
    judge(results, sources, J); report(results, J); log("DONE")
