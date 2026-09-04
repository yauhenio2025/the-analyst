"""Study part 3: Fable harness through the dossier caller (call_text), and judging with Sonnet via forced tool use."""
from __future__ import annotations

import json, sys, threading, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from src.engines.registry import get_engine_registry  # noqa: E402
from src.engines.schemas_v2 import PassDefinition  # noqa: E402
from src.executor.context_broker import assemble_inner_pass_context  # noqa: E402
from src.stages.capability_composer import compose_all_pass_prompts, compose_pass_prompt  # noqa: E402
from src.dossier.llm import call_json, call_text  # noqa: E402

OUT = ROOT / "data" / "study"; SOURCE = (OUT / "source_aukus.txt").read_text(encoding="utf-8")
ENGINES = ["conditions_of_possibility_analyzer", "argument_architecture"]
FABLE = "claude-fable-5-1"; SONNET = "claude-sonnet-4-6"; JUDGE = SONNET; DEPTH = "deep"
manifest = json.loads((OUT / "manifest.json").read_text()); lock = threading.Lock()


def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)


def record(engine, condition, model_key, model_id, content, seconds, passes, cost, notes=""):
    name = f"{engine}__{condition}__{model_key}.md"; (OUT / "outputs" / name).write_text(content, encoding="utf-8")
    with lock:
        manifest[:] = [m for m in manifest if m["file"] != f"outputs/{name}"]
        manifest.append({"engine": engine, "condition": condition, "model": model_id, "model_used": model_id, "cost_usd": cost, "seconds": round(seconds, 1), "chars": len(content), "passes": passes, "file": f"outputs/{name}", "notes": notes})
        (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    log(f"done {name} ({len(content):,} chars, {seconds:.0f}s, ${cost:.2f}) {notes}")


def harness_fable(engine):
    cap = get_engine_registry().get_capability_definition(engine); t0 = time.time(); cost = 0.0
    prior, stances, parts = {}, {}, []
    for pp in compose_all_pass_prompts(cap, depth=DEPTH):
        inner = assemble_inner_pass_context(prior_pass_outputs=prior, consumes_from=pp.consumes_from, pass_stances=stances)
        pd = PassDefinition(pass_number=pp.pass_number, label=pp.pass_label, stance=pp.stance_key, description="", focus_dimensions=pp.focus_dimensions, consumes_from=pp.consumes_from)
        system = compose_pass_prompt(cap_def=cap, pass_def=pd, depth=DEPTH, shared_context=inner or None).prompt
        text, meta = call_text("study-fable", "harness", label=f"study3 {engine} pass {pp.pass_number}", system=system, user=SOURCE, model=FABLE, max_tokens=16000)
        cost += float(meta.get("cost_usd") or 0)
        prior[pp.pass_number] = text; stances[pp.pass_number] = pp.stance_key
        parts.append(f"## Pass {pp.pass_number}: {pp.pass_label} (stance: {pp.stance_key}; dimensions: {', '.join(pp.focus_dimensions or [])})\n\n{text}")
        log(f"  {engine}/fable pass {pp.pass_number} ({pp.stance_key}) {len(text):,} chars")
    record(engine, "harness", "fable", FABLE, "\n\n---\n\n".join(parts), time.time() - t0, 4, cost, "via dossier call_text (executor path returned empty on Fable)")


RUBRIC_SCHEMA = {"type": "object", "properties": {k: {"type": "integer"} for k in ("specificity", "anchoring", "non_obviousness", "coherence", "usefulness", "hallucination_risk")} | {"reasons": {"type": "object", "properties": {k: {"type": "string"} for k in ("specificity", "anchoring", "non_obviousness", "coherence", "usefulness", "hallucination_risk")}}, "one_line": {"type": "string"}}, "required": ["specificity", "anchoring", "non_obviousness", "coherence", "usefulness", "hallucination_risk", "one_line"]}
RUBRIC = """Score the ANALYSIS on the SOURCE, 1-10 each, with one sentence of reason per criterion.
specificity: is it about THIS text or could it be about any text? anchoring: are claims tied to verbatim quotes that exist in the source? non_obviousness: does it find what a careful expert would find but a casual reader would not? coherence: does it hold together as one reading rather than a list? usefulness: would an executive reader act differently after reading it? hallucination_risk (10 = no risk): are there claims the source does not support (check quotes against the source)."""
PAIR_SCHEMA = {"type": "object", "properties": {"winner": {"type": "string", "enum": ["A", "B", "tie"]}, "margin": {"type": "string", "enum": ["slight", "clear", "decisive"]}, "why": {"type": "string"}, "what_A_has_that_B_lacks": {"type": "string"}, "what_B_has_that_A_lacks": {"type": "string"}}, "required": ["winner", "margin", "why"]}
PAIR = "Two analyses of the same source. Which is the better reading for an expert who must brief an executive: more specific to this text, better anchored in real quotes, less obvious, more coherent, more useful, fewer unsupported claims? Judge the reading, not the length."


def judge_all():
    j = {"rubric": {}, "pairwise": [], "judge": JUDGE}
    for m in manifest:
        content = (OUT / m["file"]).read_text(encoding="utf-8")
        try:
            r, _ = call_json("study-judge", "judge", label=f"rubric {m['file']}", system=RUBRIC, user=f"SOURCE (verbatim):\n\n{SOURCE}\n\n=====\n\nANALYSIS:\n\n{content}", tool_name="score", schema=RUBRIC_SCHEMA, model=JUDGE, max_tokens=2500)
        except Exception as exc:  # noqa: BLE001
            r = {"error": str(exc)[:300]}
        j["rubric"][m["file"]] = r; (OUT / "judgments.json").write_text(json.dumps(j, indent=2))
        log("rubric", m["file"][8:62], {k: r.get(k) for k in ("specificity", "anchoring", "non_obviousness", "coherence", "usefulness", "hallucination_risk")} if "error" not in r else r["error"][:80])
    by = {(m["engine"], m["condition"], m["model"]): m for m in manifest}
    for engine in ENGINES:
        for model in (SONNET, FABLE):
            h = by.get((engine, "harness", model))
            for oc in ("oneshot", "oneshot_questions"):
                o = by.get((engine, oc, model))
                if not h or not o: continue
                for a, b in ((h, o), (o, h)):
                    user = f"SOURCE (verbatim):\n\n{SOURCE}\n\n=====\n\nANALYSIS A:\n\n{(OUT / a['file']).read_text(encoding='utf-8')}\n\n=====\n\nANALYSIS B:\n\n{(OUT / b['file']).read_text(encoding='utf-8')}"
                    try:
                        r, _ = call_json("study-judge", "judge", label=f"pair {a['file']} vs {b['file']}", system=PAIR, user=user, tool_name="verdict", schema=PAIR_SCHEMA, model=JUDGE, max_tokens=1500)
                    except Exception as exc:  # noqa: BLE001
                        r = {"error": str(exc)[:300]}
                    j["pairwise"].append({"engine": engine, "model": model, "A": a["file"], "B": b["file"], **r}); (OUT / "judgments.json").write_text(json.dumps(j, indent=2))
                    log("pair", engine[:14], model[-10:], a["condition"], "vs", b["condition"], "->", r.get("winner"), r.get("margin"))


if __name__ == "__main__":
    ts = [threading.Thread(target=harness_fable, args=(e,), daemon=True) for e in ENGINES]
    for t in ts: t.start(); time.sleep(2)
    for t in ts: t.join()
    log("fable harness done; judging", len(manifest), "outputs with", JUDGE)
    judge_all()
    log("STUDY PART 3 DONE")
