"""First-queue methods S1 (reading guide), E8 (quantities), T1 (events): the production default (one call on Sol + DeepSeek check)
on two papers each, with the engine's original questions in one call as a comparison where an original exists (S1, T1),
scored independently by Sonnet and Sol on the six criteria (no head-to-head), anchors verified by code. ≈ $3.50.
  python scripts/study_first_queue.py            # run + rate + report (resumable)
"""
from __future__ import annotations
import json, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from scripts.study_two_engines import old_prompt  # noqa: E402
from src.engines.registry import get_engine_registry  # noqa: E402
from src.events.pricing import estimate_cost  # noqa: E402
from src.executor.context_broker import split_ledger  # noqa: E402
from src.executor.engine_runner import run_engine_call, run_engine_call_auto  # noqa: E402
from src.executor.ledger_walls import SourceIndex, parse_rows, verify_rows  # noqa: E402
from src.executor.process_runner import run_oneshot_checked  # noqa: E402
from src.llm.client import parse_llm_json_response  # noqa: E402
from src.operationalizations.registry import get_operationalization_registry  # noqa: E402

OUT = ROOT / "data/study/v5_first_queue"; (OUT / "outputs").mkdir(parents=True, exist_ok=True)
SRC = ROOT / "data/study"; IDEAS = SRC / "sources_ideas"
PAPERS = {"aukus": SRC / "source_aukus.txt", "subsea": SRC / "source_subsea.txt", "zambrana": IDEAS / "zambrana2025_philosophy_in_the_severe_style_rose.txt", "harris": IDEAS / "harris2026_eight_arguments_against_honneth.txt"}
PLAN = {"deep_summarization": (["zambrana", "aukus"], True), "statistical_evidence": (["aukus", "subsea"], False), "event_timeline_causal": (["aukus", "subsea"], True)}
MODEL = "openrouter/openai/gpt-5.6-sol"; RATERS = {"sonnet": "claude-sonnet-4-6", "sol": "openrouter/openai/gpt-5.6-sol"}; lock = threading.Lock()
KEYS = ("specificity", "anchoring", "non_obviousness", "coherence", "usefulness", "hallucination_risk")
RUBRIC = ("Score the ANALYSIS on the SOURCE, 1-10 each. specificity: about THIS text? anchoring: claims tied to verbatim quotes that exist in the source? non_obviousness: what a careful expert finds and a casual reader misses? "
          "coherence: one reading, not a list? usefulness: would an expert reader who must rely on this text act differently? hallucination_risk (10 = none): claims the source does not support, including numbers, dates or causes the source does not give? "
          "An honest inventory with limits stated is legitimate; do not reward row count or length. Answer as JSON: " + json.dumps({k: "n" for k in KEYS} | {"one_line": "..."}))
def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)
def load(p, d): return json.loads(p.read_text()) if p.exists() else d
def save(p, o):
    with lock: p.write_text(json.dumps(o, indent=2, ensure_ascii=False))
def anchors(text, src):
    _, led = split_ledger(text); rows = parse_rows(led.split("### Rejected by the critic")[0])
    if not rows: return 0.0, 0
    rep = verify_rows(rows, SourceIndex({"doc": src})); return rep.anchor_rate, rep.rows

def generate(engine, paper, cond, results, sources):
    key = f"{engine}__{cond}__{paper}"
    if key in results and (OUT / "outputs" / f"{key}.md").exists(): return
    cap = get_engine_registry().get_capability_definition(engine); spec = get_operationalization_registry().get(engine).process; src = sources[paper]; t0 = time.time()
    try:
        if cond == "old":
            import json as _j
            legacy = _j.load(open(ROOT / "src/engines/definitions" / f"{engine}.json"))
            # the original definition's questions: for a developed engine its capability dimensions; for a legacy one its focus, steps and schema
            if engine == "deep_summarization": system = old_prompt(cap)
            else:
                ex = (legacy.get("stage_context") or {}).get("extraction") or {}
                system = "\n\n".join([f"# {legacy['engine_name']}", legacy.get("description", ""), f"**Core question**: {legacy.get('researcher_question')}",
                    "Extraction focus: " + ", ".join(legacy.get("extraction_focus", [])), "Steps: " + " | ".join(ex.get("extraction_steps", [])),
                    "Schema (fields to fill, as prose): " + _j.dumps(legacy.get("canonical_schema"), ensure_ascii=False)[:2500],
                    "You are an expert reader. Produce the analysis this engine defines for an expert who must rely on the text; anchor every substantive claim in a short verbatim quote.",
                    "## Output\nThe analysis, then:\n## Findings ledger\n- [F1] <finding> — anchor: \"<verbatim>\" — confidence: high|medium|low\n(12-30 rows)\n### Counter-evidence\n### Open questions"])
            res = run_engine_call_auto(system_prompt=system, user_message=f"SOURCE [doc]:\n\n{src}", phase_number=1.0, model_hint=MODEL, depth="standard", label=f"v5 {key}")
            content = res["content"]; calls = [{"step": "old_oneshot", "model": res.get("model_used"), "cost": estimate_cost(res.get("model_used") or MODEL, res["input_tokens"], res["output_tokens"]) or 0.0}]
        else:
            run = run_oneshot_checked(cap, spec, {"doc": src}, tier_overrides={"strong": MODEL})
            content = run.final_content; calls = [{"step": c.step_key, "model": c.model_used, "cost": c.cost_usd, "wall": c.wall} for c in run.calls]
    except Exception as exc:  # noqa: BLE001
        log(f"FAILED {key}: {exc}"); return
    (OUT / "outputs" / f"{key}.md").write_text(content, encoding="utf-8"); rate, rows = anchors(content, src)
    with lock: results[key] = {"engine": engine, "paper": paper, "condition": cond, "cost_usd": round(sum(c["cost"] for c in calls), 4), "seconds": round(time.time() - t0, 1), "chars": len(content), "anchor_rate": rate, "rows": rows, "calls": calls}
    save(OUT / "results.json", results); log(f"done {key}: {len(content):,} chars, ${results[key]['cost_usd']:.2f}, {results[key]['seconds']:.0f}s, anchors {rate:.0%} of {rows}")

def rate(results, sources, R):
    jobs = [(k, rk) for k in results for rk in RATERS if f"{rk}:{k}" not in R]
    log(f"rating {len(jobs)} outputs")
    def _do(job):
        k, rk = job; m = results[k]
        try:
            res = run_engine_call(system_prompt=RUBRIC, user_message=f"SOURCE:\n\n{sources[m['paper']]}\n\n=====\n\nANALYSIS:\n\n{(OUT / 'outputs' / f'{k}.md').read_text()}", phase_number=1.0, model_hint=RATERS[rk], depth="standard", label=f"v5 rate {rk} {k}")
            r = parse_llm_json_response(res["content"]);
            if isinstance(r, list): r = next((x for x in r if isinstance(x, dict)), {})
            with lock: R[f"{rk}:{k}"] = {**{c: r.get(c) for c in KEYS}, "one_line": r.get("one_line", ""), "cost_usd": estimate_cost(res.get("model_used") or RATERS[rk], res["input_tokens"], res["output_tokens"]) or 0.0}
            log("rated", rk, k[:60], [r.get(c) for c in KEYS])
        except Exception as exc:  # noqa: BLE001
            log(f"rate failed {rk} {k}: {exc}")
        save(OUT / "ratings.json", R)
    with ThreadPoolExecutor(max_workers=4) as pool: list(pool.map(_do, jobs))
    save(OUT / "ratings.json", R)

def report(results, R):
    import statistics as st
    def mean(k, rk):
        r = R.get(f"{rk}:{k}"); vals = [r[c] for c in KEYS if r and isinstance(r.get(c), (int, float))]; return st.mean(vals) if vals else float("nan")
    lines = ["# First-queue methods S1, E8, T1: production default vs original questions (2026-09-06)", "", "One call on Sol + DeepSeek check (`checked`) against the engine's original questions in one call on Sol (`old`, where an original exists). Independent scores by Sonnet and Sol, mean of six criteria; hallucination 10 = none; anchors verified by code.", "",
             "| engine | paper | condition | rubric sonnet / sol | halluc sonnet / sol | anchors | rows | $ | s |", "|---|---|---|---|---|---|---|---|---|"]
    for k, m in sorted(results.items(), key=lambda kv: (kv[1]["engine"], kv[1]["paper"], kv[1]["condition"])):
        h = lambda rk: (R.get(f"{rk}:{k}") or {}).get("hallucination_risk", "—")
        lines.append(f"| {m['engine']} | {m['paper']} | {m['condition']} | {mean(k,'sonnet'):.2f} / {mean(k,'sol'):.2f} | {h('sonnet')} / {h('sol')} | {m['anchor_rate']:.0%} | {m['rows']} | {m['cost_usd']:.2f} | {m['seconds']:.0f} |")
    lines += ["", f"Generation ${sum(m['cost_usd'] for m in results.values()):.2f}; rating ${sum(v.get('cost_usd', 0) for v in R.values()):.2f}.", ""]
    (OUT / "REPORT.md").write_text("\n".join(lines)); log("wrote", OUT / "REPORT.md")

if __name__ == "__main__":
    sources = {p: PAPERS[p].read_text(encoding="utf-8", errors="replace") for p in PAPERS}
    results = load(OUT / "results.json", {}); R = load(OUT / "ratings.json", {})
    specs = [(e, p, c) for e, (papers, has_old) in PLAN.items() for p in papers for c in (["checked", "old"] if has_old else ["checked"])]
    with ThreadPoolExecutor(max_workers=4) as pool: list(pool.map(lambda s: generate(*s, results, sources), specs))
    rate(results, sources, R); report(results, R); log("DONE")
