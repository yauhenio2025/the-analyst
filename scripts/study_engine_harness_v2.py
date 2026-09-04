"""Retest after the plumbing fixes (2026-09-04): the fixed harness at deep depth, judged on what the dossier
consumes (the final pass), against the one-shots already on disk. Records tokens and estimated cost."""
from __future__ import annotations

import json, sys, threading, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from src.engines.registry import get_engine_registry  # noqa: E402
from src.engines.schemas_v2 import PassDefinition  # noqa: E402
from src.executor.context_broker import assemble_inner_pass_context, split_ledger  # noqa: E402
from src.executor.engine_runner import run_engine_call_auto  # noqa: E402
from src.stages.capability_composer import compose_all_pass_prompts, compose_pass_prompt  # noqa: E402
from src.dossier.llm import call_json  # noqa: E402

OUT = ROOT / "data" / "study"; SOURCE = (OUT / "source_aukus.txt").read_text(encoding="utf-8")
ENGINES = ["conditions_of_possibility_analyzer", "argument_architecture"]
MODELS = {"sonnet": "claude-sonnet-4-6", "fable": "claude-fable-5-1"}
PRICE = {"claude-sonnet-4-6": (3.0, 15.0), "claude-fable-5-1": (15.0, 75.0)}  # $/M tokens in, out (estimate; fable assumed opus-class)
JUDGE = "claude-sonnet-4-6"; DEPTH = "deep"
manifest = json.loads((OUT / "manifest.json").read_text()); lock = threading.Lock()


def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)


def cost(model, tin, tout):
    pi, po = PRICE.get(model, (3.0, 15.0)); return round(tin / 1e6 * pi + tout / 1e6 * po, 3)


def harness_v2(engine, mk):
    cap = get_engine_registry().get_capability_definition(engine); model = MODELS[mk]; t0 = time.time()
    pps = compose_all_pass_prompts(cap, depth=DEPTH); prior, stances, parts, total_cost, models_used, ledgers = {}, {}, [], 0.0, set(), 0
    for pp in pps:
        inner = assemble_inner_pass_context(prior, pp.consumes_from, stances)
        pd = PassDefinition(pass_number=pp.pass_number, label=pp.pass_label, stance=pp.stance_key, description=pp.description, focus_dimensions=pp.focus_dimensions, consumes_from=pp.consumes_from)
        sysm = compose_pass_prompt(cap, pd, depth=DEPTH, shared_context=inner or None, is_final=pp.is_final).prompt
        res = run_engine_call_auto(system_prompt=sysm, user_message=SOURCE, phase_number=1.0, model_hint=model, depth=DEPTH, label=f"v2 {engine} {mk} pass {pp.pass_number}")
        prior[pp.pass_number] = res["content"]; stances[pp.pass_number] = pp.stance_key; models_used.add(res.get("model_used") or "")
        total_cost += cost(res.get("model_used") or model, res.get("input_tokens", 0), res.get("output_tokens", 0))
        _, ledger = split_ledger(res["content"]); ledgers += int(bool(ledger))
        parts.append(f"## Pass {pp.pass_number}: {pp.pass_label} (stance: {pp.stance_key}; final={pp.is_final})\n\n{res['content']}")
        log(f"  {engine}/{mk} pass {pp.pass_number} ({pp.stance_key}) {len(res['content']):,} chars, ledger={'yes' if ledger else 'NO'}, ctx in {len(inner):,}")
    final = prior[max(prior)]
    name_all = f"{engine}__harness_v2_all__{mk}.md"; name_final = f"{engine}__harness_v2_final__{mk}.md"
    (OUT / "outputs" / name_all).write_text("\n\n---\n\n".join(parts), encoding="utf-8"); (OUT / "outputs" / name_final).write_text(final, encoding="utf-8")
    with lock:
        manifest[:] = [m for m in manifest if m["file"] not in (f"outputs/{name_all}", f"outputs/{name_final}")]
        manifest.append({"engine": engine, "condition": "harness_v2_final", "model": model, "model_used": ",".join(sorted(m for m in models_used if m)), "cost_usd": total_cost, "seconds": round(time.time() - t0, 1), "chars": len(final), "passes": len(pps), "file": f"outputs/{name_final}", "notes": f"{ledgers}/{len(pps)} passes produced a findings ledger; all passes in {name_all}"})
        (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    log(f"done {name_final} ({len(final):,} chars final; ${total_cost:.2f}; {time.time()-t0:.0f}s; ledgers {ledgers}/{len(pps)})")


RUBRIC_SCHEMA = {"type": "object", "properties": {k: {"type": "integer"} for k in ("specificity", "anchoring", "non_obviousness", "coherence", "usefulness", "hallucination_risk")} | {"one_line": {"type": "string"}}, "required": ["specificity", "anchoring", "non_obviousness", "coherence", "usefulness", "hallucination_risk", "one_line"]}
RUBRIC = "Score the ANALYSIS on the SOURCE, 1-10 each. specificity: about THIS text? anchoring: claims tied to verbatim quotes that exist in the source? non_obviousness: what a careful expert finds and a casual reader misses? coherence: one reading, not a list? usefulness: would an executive act differently? hallucination_risk (10 = none): claims the source does not support?"
PAIR_SCHEMA = {"type": "object", "properties": {"winner": {"type": "string", "enum": ["A", "B", "tie"]}, "margin": {"type": "string", "enum": ["slight", "clear", "decisive"]}, "why": {"type": "string"}}, "required": ["winner", "margin", "why"]}
PAIR = "Two analyses of the same source. Which is the better reading for an expert who must brief an executive: more specific to this text, better anchored in real quotes, less obvious, more coherent, more useful, fewer unsupported claims? Judge the reading, not the length."


def judge():
    j = {"judge": JUDGE, "rubric": {}, "pairwise": []}
    by = {(m["engine"], m["condition"], m["model"]): m for m in manifest}
    for engine in ENGINES:
        for model in MODELS.values():
            h = by.get((engine, "harness_v2_final", model))
            if not h: continue
            content = (OUT / h["file"]).read_text(encoding="utf-8")
            try:
                r, _ = call_json("study-judge", "judge", label=f"rubric {h['file']}", system=RUBRIC, user=f"SOURCE:\n\n{SOURCE}\n\n=====\n\nANALYSIS:\n\n{content}", tool_name="score", schema=RUBRIC_SCHEMA, model=JUDGE, max_tokens=1200)
            except Exception as exc: r = {"error": str(exc)[:200]}
            j["rubric"][h["file"]] = r; log("rubric", h["file"][8:60], {k: r.get(k) for k in ("specificity", "anchoring", "non_obviousness", "coherence", "usefulness", "hallucination_risk")} if "error" not in r else r["error"])
            for oc in ("oneshot", "oneshot_questions"):
                o = by.get((engine, oc, model))
                if not o: continue
                for a, b in ((h, o), (o, h)):
                    user = f"SOURCE:\n\n{SOURCE}\n\n=====\n\nANALYSIS A:\n\n{(OUT / a['file']).read_text(encoding='utf-8')}\n\n=====\n\nANALYSIS B:\n\n{(OUT / b['file']).read_text(encoding='utf-8')}"
                    try:
                        r, _ = call_json("study-judge", "judge", label="pair v2", system=PAIR, user=user, tool_name="verdict", schema=PAIR_SCHEMA, model=JUDGE, max_tokens=1000)
                    except Exception as exc: r = {"error": str(exc)[:200]}
                    j["pairwise"].append({"engine": engine, "model": model, "A": a["condition"], "B": b["condition"], **r}); (OUT / "judgments_v2.json").write_text(json.dumps(j, indent=2))
                    w = r.get("winner"); log("pair", engine[:14], model[-10:], a["condition"], "vs", b["condition"], "->", (a["condition"] if w == "A" else b["condition"] if w == "B" else w), r.get("margin"))
    (OUT / "judgments_v2.json").write_text(json.dumps(j, indent=2))


if __name__ == "__main__":
    ts = [threading.Thread(target=harness_v2, args=(e, mk), daemon=True) for e in ENGINES for mk in MODELS]
    for t in ts: t.start(); time.sleep(2)
    for t in ts: t.join()
    log("v2 harness runs done; judging"); judge(); log("RETEST DONE")
