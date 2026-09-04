"""Frontier study (2026-09-04): quality against cost and time for four execution shapes on seven models.

Conditions
  a  one call with the rewritten questions and method cards (the whole shape in one prompt)
  b  the fixed four-stance harness at deep depth (production control, unchanged)
  c  decompose-verify-synthesize with every step on the same model
  d  cheap read + strong write: extract on GPT-5.6 Luna, verify on DeepSeek V4 Pro, synthesize on the model
Models: Fable 5.1, Sonnet 4.6 (control), GPT-5.6 Sol, Kimi K3, DeepSeek V4 Pro, GPT-5.6 Luna, DeepSeek V4 Flash.
Papers: AUKUS (Wijaya & Hayes 2025), subsea cables (Abels 2026). Engines: conditions_of_possibility_analyzer,
argument_architecture. Judges: Sonnet 4.6 and GPT-5.6 Sol, blind, rubric + pairwise against the Fable
one-shot (condition a) both orders. Recorded per run: tokens, cost, seconds, and the code-computed anchor
verification rate of the final ledger.

  python scripts/study_engine_harness_v3.py --dry-run                 # compose everything, estimate cost, no calls
  python scripts/study_engine_harness_v3.py --preset lean             # run generation + judging (asks nothing; resumable)
  python scripts/study_engine_harness_v3.py --judge-only --report     # judge what is on disk, write FRONTIER.md
Resumable: every run and judgment is keyed and skipped when already on disk.
"""
from __future__ import annotations

import argparse, json, os, sys, threading, time, traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from src.engines.registry import get_engine_registry  # noqa: E402
from src.engines.schemas_v2 import PassDefinition  # noqa: E402
from src.events.pricing import estimate_cost  # noqa: E402
from src.executor.context_broker import assemble_inner_pass_context, split_ledger  # noqa: E402
from src.executor.engine_runner import run_engine_call, run_engine_call_auto  # noqa: E402
from src.executor.ledger_walls import SourceIndex, parse_rows, verify_rows  # noqa: E402
from src.executor.process_runner import preview_prompts, run_process  # noqa: E402
from src.llm.client import parse_llm_json_response  # noqa: E402
from src.operationalizations.registry import get_operationalization_registry  # noqa: E402
from src.stages.capability_composer import compose_all_pass_prompts, compose_pass_prompt  # noqa: E402
from src.stages.process_composer import compose_oneshot_prompt  # noqa: E402

OUT = ROOT / "data" / "study" / "v3"; (OUT / "outputs").mkdir(parents=True, exist_ok=True); (OUT / "receipts").mkdir(exist_ok=True)
PAPERS = {"aukus": ROOT / "data/study/source_aukus.txt", "subsea": ROOT / "data/study/source_subsea.txt"}
ENGINES = {"cop": "conditions_of_possibility_analyzer", "aa": "argument_architecture"}
MODELS = {
    "fable": "claude-fable-5-1", "sonnet": "claude-sonnet-4-6", "sol": "openrouter/openai/gpt-5.6-sol",
    "kimi3": "openrouter/moonshotai/kimi-k3", "dspro": "openrouter/deepseek/deepseek-v4-pro",
    "luna": "openrouter/openai/gpt-5.6-luna", "dsflash": "openrouter/deepseek/deepseek-v4-flash",
}
CHEAP, MID = MODELS["luna"], MODELS["dspro"]
STRONG_FOR_D = ("fable", "sonnet", "sol", "kimi3", "dspro")          # (d) synthesizes on these; reading is always luna + dspro
LEGACY_MODELS = {"kimi": "openrouter/moonshotai/kimi-k2.6"}         # K2.6 ran once (22:30) and was replaced by K3 at the owner's ask; kept so its run stays readable
JUDGES = {"sonnet": "claude-sonnet-4-6", "sol": "openrouter/openai/gpt-5.6-sol"}
BASELINE = ("a", "fable")                                            # pairwise opponent: the Fable one-shot with the rewritten questions
PRESETS = {
    "full": {"conditions": "a,b,c,d", "models": ",".join(MODELS), "b_models": ",".join(MODELS), "orders": "both"},
    "lean": {"conditions": "a,b,c,d", "models": ",".join(MODELS), "b_models": "fable,sonnet,sol,luna", "orders": "split"},
}
lock = threading.Lock()


def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)


def load_json(p: Path, default):
    return json.loads(p.read_text()) if p.exists() else default


def save_json(p: Path, obj):
    with lock: p.write_text(json.dumps(obj, indent=2, ensure_ascii=False))


# ── generation ────────────────────────────────────────────────────────────

def anchor_rate(content: str, source: str) -> tuple[float, int]:
    _, ledger = split_ledger(content)
    rows = parse_rows(ledger)
    if not rows: return 0.0, 0
    rep = verify_rows(rows, SourceIndex({"doc": source}))
    return rep.anchor_rate, rep.rows


def run_key(engine, cond, model, paper): return f"{engine}__{cond}__{model}__{paper}"


def cond_a(cap, spec, model_id, source, label):
    pp = compose_oneshot_prompt(cap, spec, {"doc": source})
    res = run_engine_call_auto(system_prompt=pp.system, user_message=pp.user, phase_number=1.0, model_hint=model_id, depth="standard", label=label)
    used = res.get("model_used") or model_id
    return res["content"], [{"step": "oneshot", "model_used": used, "input_tokens": res["input_tokens"], "output_tokens": res["output_tokens"], "duration_ms": res["duration_ms"], "cost_usd": estimate_cost(used, res["input_tokens"], res["output_tokens"]) or 0.0}]


def cond_b(cap, spec, model_id, source, label):
    pps = compose_all_pass_prompts(cap, depth="deep"); prior, stances, calls = {}, {}, []
    for pp in pps:
        inner = assemble_inner_pass_context(prior, pp.consumes_from, stances)
        pd = PassDefinition(pass_number=pp.pass_number, label=pp.pass_label, stance=pp.stance_key, description=pp.description, focus_dimensions=pp.focus_dimensions, consumes_from=pp.consumes_from)
        sysm = compose_pass_prompt(cap, pd, depth="deep", shared_context=inner or None, is_final=pp.is_final).prompt
        res = run_engine_call_auto(system_prompt=sysm, user_message=source, phase_number=1.0, model_hint=model_id, depth="deep", label=f"{label} pass {pp.pass_number}")
        prior[pp.pass_number] = res["content"]; stances[pp.pass_number] = pp.stance_key; used = res.get("model_used") or model_id
        calls.append({"step": f"pass{pp.pass_number}:{pp.stance_key}", "model_used": used, "input_tokens": res["input_tokens"], "output_tokens": res["output_tokens"], "duration_ms": res["duration_ms"], "cost_usd": estimate_cost(used, res["input_tokens"], res["output_tokens"]) or 0.0, "chars": len(res["content"])})
    return prior[max(prior)], calls


def cond_cd(cap, spec, model_id, source, label, uniform: bool):
    tiers = {"cheap": model_id, "mid": model_id, "strong": model_id} if uniform else {"cheap": CHEAP, "mid": MID, "strong": model_id}
    run = run_process(cap, spec, {"doc": source}, tier_overrides=tiers)
    return run.final_content, [c.as_receipt() for c in run.calls], run.receipts()


def generate(engine_key, cond, mk, paper, manifest, sources):
    key = run_key(engine_key, cond, mk, paper); fname = f"outputs/{key}.md"
    if any(m["key"] == key for m in manifest) and (OUT / fname).exists():
        return
    cap = get_engine_registry().get_capability_definition(engine_key); spec = get_operationalization_registry().get(engine_key).process
    source, model_id, label, t0 = sources[paper], MODELS[mk], f"v3 {key}", time.time()
    try:
        extra = {}
        if cond == "a": content, calls = cond_a(cap, spec, model_id, source, label)
        elif cond == "b": content, calls = cond_b(cap, spec, model_id, source, label)
        elif cond == "c": content, calls, extra = cond_cd(cap, spec, model_id, source, label, uniform=True)
        else: content, calls, extra = cond_cd(cap, spec, model_id, source, label, uniform=False)
    except Exception as exc:  # noqa: BLE001
        log(f"FAILED {key}: {exc}"); (OUT / "receipts" / f"{key}.error.txt").write_text(traceback.format_exc()); return
    rate, rows = anchor_rate(content, source)
    (OUT / fname).write_text(content, encoding="utf-8")
    (OUT / "receipts" / f"{key}.json").write_text(json.dumps({"calls": calls, **({"process": extra} if extra else {})}, indent=2, ensure_ascii=False))
    entry = {"key": key, "engine": engine_key, "condition": cond, "model": mk, "model_id": model_id, "paper": paper,
             "models_used": sorted({c["model_used"] for c in calls}), "calls": len(calls),
             "input_tokens": sum(c["input_tokens"] for c in calls), "output_tokens": sum(c["output_tokens"] for c in calls),
             "cost_usd": round(sum(c["cost_usd"] for c in calls), 4), "seconds": round(time.time() - t0, 1), "chars": len(content),
             "anchor_rate": rate, "ledger_rows": rows, "file": fname}
    with lock:
        manifest[:] = [m for m in manifest if m["key"] != key]; manifest.append(entry)
    save_json(OUT / "manifest.json", manifest)
    log(f"done {key}: {len(content):,} chars, ${entry['cost_usd']:.2f}, {entry['seconds']:.0f}s, {len(calls)} calls, anchors {rate:.0%} of {rows}")


# ── judging ───────────────────────────────────────────────────────────────

RUBRIC_KEYS = ("specificity", "anchoring", "non_obviousness", "coherence", "usefulness", "hallucination_risk")
RUBRIC = ("Score the ANALYSIS on the SOURCE, 1-10 each. specificity: about THIS text? anchoring: claims tied to verbatim quotes that exist in "
          "the source? non_obviousness: what a careful expert finds and a casual reader misses? coherence: one reading, not a list? usefulness: "
          "would an expert reader who must decide what this text establishes act differently? hallucination_risk (10 = none): claims the source "
          "does not support, including claims about the authors' minds or careers? Answer as JSON: "
          '{"specificity": n, "anchoring": n, "non_obviousness": n, "coherence": n, "usefulness": n, "hallucination_risk": n, "one_line": "..."}')
PAIR = ("Two analyses of the same source. Which is the better reading for an expert who must decide what this text establishes: more specific "
        "to this text, better anchored in real quotes, less obvious, more coherent, more useful, fewer unsupported claims (including claims about "
        "the authors rather than the text)? Judge the reading, not the length. Answer as JSON: "
        '{"winner": "A"|"B"|"tie", "margin": "slight"|"clear"|"decisive", "why": "...", "what_A_has_that_B_lacks": "...", "what_B_has_that_A_lacks": "..."}')


def judge_call(jk, system, user, label):
    model = JUDGES[jk]
    res = run_engine_call(system_prompt=system, user_message=user, phase_number=1.0, model_hint=model, depth="standard", label=label)
    used = res.get("model_used") or model
    return parse_llm_json_response(res["content"]), estimate_cost(used, res["input_tokens"], res["output_tokens"]) or 0.0


def judge(manifest, sources, judges, orders):
    J = load_json(OUT / "judgments.json", {"rubric": {}, "pairwise": []}); done_pairs = {(p["judge"], p["A"], p["B"]) for p in J["pairwise"]}
    by = {(m["engine"], m["condition"], m["model"], m["paper"]): m for m in manifest}
    jobs = []
    for m in manifest:
        for jk in judges:
            if f"{jk}:{m['key']}" not in J["rubric"]:
                jobs.append(("rubric", jk, m, None))
        base = by.get((m["engine"], BASELINE[0], BASELINE[1], m["paper"]))
        if not base or base["key"] == m["key"]: continue
        pairs = [(m, base), (base, m)]
        for i, (a, b) in enumerate(pairs):
            for jk in judges:
                if orders == "split" and (i % 2) != list(judges).index(jk) % 2: continue
                if (jk, a["key"], b["key"]) in done_pairs: continue
                jobs.append(("pair", jk, a, b))
    log(f"judging: {len(jobs)} calls")

    def _do(job):
        kind, jk, a, b = job
        src = sources[a["paper"]]
        try:
            if kind == "rubric":
                r, cost = judge_call(jk, RUBRIC, f"SOURCE:\n\n{src}\n\n=====\n\nANALYSIS:\n\n{(OUT / a['file']).read_text()}", f"v3 rubric {jk} {a['key']}")
                with lock: J["rubric"][f"{jk}:{a['key']}"] = {**{k: r.get(k) for k in RUBRIC_KEYS}, "one_line": r.get("one_line", ""), "judge": jk, "cost_usd": cost}
                log("rubric", jk, a["key"][:60], [r.get(k) for k in RUBRIC_KEYS])
            else:
                r, cost = judge_call(jk, PAIR, f"SOURCE:\n\n{src}\n\n=====\n\nANALYSIS A:\n\n{(OUT / a['file']).read_text()}\n\n=====\n\nANALYSIS B:\n\n{(OUT / b['file']).read_text()}", f"v3 pair {jk}")
                w = r.get("winner"); win = a["key"] if w == "A" else b["key"] if w == "B" else "tie"
                with lock: J["pairwise"].append({"judge": jk, "engine": a["engine"], "paper": a["paper"], "A": a["key"], "B": b["key"], "winner": win, "margin": r.get("margin"), "why": r.get("why", ""), "A_has": r.get("what_A_has_that_B_lacks", ""), "B_has": r.get("what_B_has_that_A_lacks", ""), "cost_usd": cost})
                log("pair", jk, a["condition"], a["model"], "vs", b["condition"], b["model"], a["paper"], "->", win.split("__")[1:3] if win != "tie" else "tie", r.get("margin"))
        except Exception as exc:  # noqa: BLE001
            log(f"judge failed {kind} {jk} {a['key']}: {exc}")
        save_json(OUT / "judgments.json", J)
    with ThreadPoolExecutor(max_workers=4) as pool: list(pool.map(_do, jobs))
    save_json(OUT / "judgments.json", J); return J


# ── report ────────────────────────────────────────────────────────────────

def report(manifest, J):
    lines = ["# Frontier study (2026-09-04): quality against cost and time", "", f"Runs: {len(manifest)}. Judges: {', '.join(JUDGES)}. Baseline for pairwise: Fable one-shot with the rewritten questions (condition a).", ""]
    for ek in ENGINES.values():
        lines += [f"## {ek}", "", "| condition | model | ran on | paper | rubric mean (sonnet / sol) | halluc (10=none) | wins vs baseline | cost $ | seconds | calls | anchor rate | rows | chars |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for m in sorted([m for m in manifest if m["engine"] == ek], key=lambda m: (m["condition"], m["cost_usd"])):
            means, hall = [], []
            for jk in JUDGES:
                r = J["rubric"].get(f"{jk}:{m['key']}")
                vals = [r[k] for k in RUBRIC_KEYS if r and isinstance(r.get(k), (int, float))] if r else []
                means.append(f"{sum(vals)/len(vals):.1f}" if vals else "—"); hall.append(str(r.get("hallucination_risk")) if r else "—")
            pw = [p for p in J["pairwise"] if m["key"] in (p["A"], p["B"]) and p["engine"] == ek]
            wins = sum(1 for p in pw if p["winner"] == m["key"]); ties = sum(1 for p in pw if p["winner"] == "tie")
            used = [u.split("/")[-1] for u in m.get("models_used", [])]
            ran_on = "as requested" if used == [m["model_id"].split("/")[-1]] else "**" + ", ".join(used) + "**"   # a refusal fallback shows here
            lines.append(f"| {m['condition']} | {m['model']} | {ran_on} | {m['paper']} | {' / '.join(means)} | {' / '.join(hall)} | {wins}/{len(pw)}{(' (+' + str(ties) + ' tie)') if ties else ''} | {m['cost_usd']:.2f} | {m['seconds']:.0f} | {m['calls']} | {m['anchor_rate']:.0%} | {m['ledger_rows']} | {m['chars']:,} |")
        lines.append("")
        # the frontier: per condition, the cheapest run within 0.5 rubric points of the best mean
        scored = []
        for m in [m for m in manifest if m["engine"] == ek]:
            vals = [J["rubric"][f"{jk}:{m['key']}"][k] for jk in JUDGES for k in RUBRIC_KEYS if J["rubric"].get(f"{jk}:{m['key']}") and isinstance(J["rubric"][f"{jk}:{m['key']}"].get(k), (int, float))]
            if vals: scored.append((sum(vals) / len(vals), m))
        if scored:
            best = max(s for s, _ in scored)
            near = sorted([(s, m) for s, m in scored if s >= best - 0.5], key=lambda x: x[1]["cost_usd"])
            lines += [f"Best mean rubric {best:.2f}. Within 0.5 of it, cheapest first: " + "; ".join(f"{m['condition']}/{m['model']}/{m['paper']} ({s:.2f}, ${m['cost_usd']:.2f}, {m['seconds']:.0f}s)" for s, m in near[:6]), ""]
    total = sum(m["cost_usd"] for m in manifest); jcost = sum(v.get("cost_usd", 0) for v in J["rubric"].values()) + sum(p.get("cost_usd", 0) for p in J["pairwise"])
    lines += [f"Generation ${total:.2f}; judging ${jcost:.2f}; total ${total + jcost:.2f}.", "",
              "A bold entry in `ran on` means the requested model refused and the runner fell back to the house model for that call; the row measures what ran, not what was asked. "
              "Fable refused every four-stance pass on the AUKUS paper (22:41) while accepting the one-call prompt with the rewritten questions.", ""]
    (OUT / "FRONTIER.md").write_text("\n".join(lines)); log("wrote", OUT / "FRONTIER.md")


# ── dry run: compose everything, count tokens, price it ────────────────────

OUT_TOKENS = {"extract": 2000, "verify": 3500, "synthesize": 6000, "oneshot": 5500, "pass": 7000}


def dry_run(specs, sources, judges, orders, b_models):
    rows, total = [], 0.0
    for engine_key, cond, mk, paper in specs:
        cap = get_engine_registry().get_capability_definition(engine_key); spec = get_operationalization_registry().get(engine_key).process
        src = sources[paper]; model = MODELS[mk]; cost = 0.0; calls = 0
        if cond == "a":
            pp = compose_oneshot_prompt(cap, spec, {"doc": src}); calls = 1
            cost = estimate_cost(model, (len(pp.system) + len(pp.user)) // 4, OUT_TOKENS["oneshot"]) or 0.0
        elif cond == "b":
            pps = compose_all_pass_prompts(cap, depth="deep"); calls = len(pps)
            for i, pp in enumerate(pps):
                ctx = min(i, 1) * 8000 + max(0, i - 1) * 3000  # ledgers + capped prose from prior passes, in tokens
                cost += estimate_cost(model, (len(pp.prompt) + len(src)) // 4 + ctx, OUT_TOKENS["pass"]) or 0.0
        else:
            tiers = {"cheap": model, "mid": model, "strong": model} if cond == "c" else {"cheap": CHEAP, "mid": MID, "strong": model}
            for pp in preview_prompts(cap, spec, {"doc": src}):
                m = tiers[pp.model_tier]; calls += 1
                extra = 12000 if pp.kind in ("verify", "synthesize") else 0  # ledgers carried in the user message
                cost += estimate_cost(m, (len(pp.system) + len(pp.user)) // 4 + extra, OUT_TOKENS[pp.kind]) or 0.0
                if pp.kind == "extract": cost += 0.3 * (estimate_cost(m, (len(pp.system) + len(pp.user)) // 4, 600) or 0.0)  # re-anchor rounds, some
        rows.append((engine_key, cond, mk, paper, calls, cost)); total += cost
    n_out = len(specs); src_tok = sum(len(s) for s in sources.values()) / len(sources) / 4
    jcost = 0.0
    for jk in judges:
        jm = JUDGES[jk]
        jcost += n_out * (estimate_cost(jm, int(src_tok + 4000), 400) or 0.0)                       # rubric
        pairs = (n_out - len(sources)) * (2 if orders == "both" else 1)
        jcost += pairs * (estimate_cost(jm, int(src_tok + 8000), 600) or 0.0)                        # pairwise vs baseline
    print(f"\nDRY RUN — {len(specs)} generation runs, {sum(r[4] for r in rows)} model calls (plus re-anchor rounds)\n")
    print("| engine | cond | model | paper | calls | est $ |\n|---|---|---|---|---|---|")
    for r in rows: print(f"| {r[0][:12]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]:.2f} |")
    by_cond = {}
    for r in rows: by_cond[r[1]] = by_cond.get(r[1], 0) + r[5]
    print("\nby condition: " + ", ".join(f"{k}: ${v:.2f}" for k, v in sorted(by_cond.items())))
    print(f"generation ≈ ${total:.2f}; judging ({', '.join(judges)}, orders={orders}) ≈ ${jcost:.2f}; TOTAL ≈ ${total + jcost:.2f}")
    print("Assumed output tokens per call:", OUT_TOKENS, "— real costs are recorded from usage; Fable priced $10/$50 per M.")


def rescan(manifest, sources):
    """Recompute every run's anchor rate with the current parser; drop runs whose critic output failed to parse
    (a verify call with zero rows means every extraction row was carried forward unjudged) so they rerun."""
    keep = []
    for m in manifest:
        m["anchor_rate"], m["ledger_rows"] = anchor_rate((OUT / m["file"]).read_text(), sources[m["paper"]])
        rec = OUT / "receipts" / f"{m['key']}.json"
        lost = False
        if m["condition"] in ("c", "d") and rec.exists():
            calls = json.loads(rec.read_text()).get("calls", [])
            lost = any(c.get("kind") == "verify" and (c.get("wall") or {}).get("rows", 0) == 0 for c in calls)
        if lost:
            log(f"rescan: {m['key']} lost its critic (verify parsed 0 rows) — dropped, will rerun"); rec.rename(rec.with_suffix(".lost.json"))
        else:
            keep.append(m)
    manifest[:] = keep; save_json(OUT / "manifest.json", manifest)
    log(f"rescan: {len(keep)} runs kept; anchor rates recomputed")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--preset", choices=list(PRESETS), default="lean"); ap.add_argument("--conditions"); ap.add_argument("--models"); ap.add_argument("--b-models", dest="b_models")
    ap.add_argument("--papers", default="aukus,subsea"); ap.add_argument("--engines", default="cop,aa"); ap.add_argument("--judges", default="sonnet,sol"); ap.add_argument("--orders", choices=["both", "split"])
    ap.add_argument("--skip", default="c:fable:subsea", help="comma-separated cond:model[:paper] triples to leave out (default skips the Fable-everywhere chain on paper two: ~$7.6 a run, one per engine is enough for the frontier)")
    ap.add_argument("--rescan", action="store_true", help="recompute anchor rates with the current parser and drop runs whose critic output failed to parse, then continue")
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--judge-only", action="store_true"); ap.add_argument("--no-judge", action="store_true"); ap.add_argument("--report", action="store_true"); ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args(); P = PRESETS[a.preset]
    conds = (a.conditions or P["conditions"]).split(","); models = (a.models or P["models"]).split(","); b_models = (a.b_models or P["b_models"]).split(","); orders = a.orders or P["orders"]
    papers = a.papers.split(","); engines = [ENGINES[e] for e in a.engines.split(",")]; judges = a.judges.split(",")
    sources = {p: PAPERS[p].read_text(encoding="utf-8", errors="replace") for p in papers}
    skips = [tuple(x.split(":")) for x in a.skip.split(",") if x]
    def _skipped(c, m, p): return any(sk[0] == c and sk[1] == m and (len(sk) < 3 or sk[2] == p) for sk in skips)
    specs = [(e, c, m, p) for e in engines for p in papers for c in conds for m in models
             if not (c == "b" and m not in b_models) and not (c == "d" and m not in STRONG_FOR_D) and not _skipped(c, m, p)]
    if a.dry_run: return dry_run(specs, sources, judges, orders, b_models)
    manifest = load_json(OUT / "manifest.json", [])
    if a.rescan: rescan(manifest, sources)
    if not a.judge_only:
        log(f"generating {len(specs)} runs on {a.workers} workers")
        with ThreadPoolExecutor(max_workers=a.workers) as pool:
            list(pool.map(lambda s: generate(*s, manifest, sources), specs))
        log(f"generation done: {len(manifest)} runs on disk, ${sum(m['cost_usd'] for m in manifest):.2f}")
    J = load_json(OUT / "judgments.json", {"rubric": {}, "pairwise": []})
    if not a.no_judge: J = judge(manifest, sources, judges, orders)
    if a.report or not a.no_judge: report(manifest, J)
    log("DONE")


if __name__ == "__main__":
    main()
