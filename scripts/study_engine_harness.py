"""Study: does the engine harness beat a one-shot? (2026-09-04)

Runs, per engine and model, three conditions on one source document and writes
data/study/{manifest.json, outputs/*.md, source.txt}; then a blind judge scores
every output on a rubric and compares harness vs one-shot pairwise both ways.
The harness condition calls exactly what the executor calls
(compose_all_pass_prompts → compose_pass_prompt → run_engine_call_auto).
"""
from __future__ import annotations

import json
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.engines.registry import get_engine_registry  # noqa: E402
from src.engines.schemas_v2 import PassDefinition  # noqa: E402
from src.executor.context_broker import assemble_inner_pass_context  # noqa: E402
from src.executor.engine_runner import run_engine_call_auto  # noqa: E402
from src.stages.capability_composer import compose_all_pass_prompts, compose_pass_prompt  # noqa: E402

OUT = ROOT / "data" / "study"
(OUT / "outputs").mkdir(parents=True, exist_ok=True)
SOURCE = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
(OUT / "source.txt").write_text(SOURCE, encoding="utf-8")
ENGINES = ["conditions_of_possibility_analyzer", "argument_architecture"]
MODELS = {"sonnet": "claude-sonnet-4-6", "fable": "claude-fable-5-1"}
JUDGE = "claude-fable-5-1"
DEPTH = "deep"
manifest: list[dict] = []
lock = threading.Lock()


def record(engine, condition, model_key, content, cost, seconds, passes=None, model_used=None):
    name = f"{engine}__{condition}__{model_key}.md"
    (OUT / "outputs" / name).write_text(content, encoding="utf-8")
    with lock:
        manifest.append({"engine": engine, "condition": condition, "model": MODELS[model_key], "model_used": model_used, "cost_usd": cost, "seconds": round(seconds, 1), "chars": len(content), "passes": passes, "file": f"outputs/{name}"})
        (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(time.strftime("%H:%M:%S"), f"done {name} ({len(content):,} chars, ${cost:.2f}, {seconds:.0f}s)", flush=True)


def harness(engine: str, model_key: str) -> None:
    reg = get_engine_registry()
    cap = reg.get_capability_definition(engine)
    t0 = time.time(); cost = 0.0
    pass_prompts = compose_all_pass_prompts(cap, depth=DEPTH)
    prior: dict[int, str] = {}; stances: dict[int, str] = {}; parts = []; models = set()
    for pp in pass_prompts:
        inner = assemble_inner_pass_context(prior_pass_outputs=prior, consumes_from=pp.consumes_from, pass_stances=stances)
        pass_def = PassDefinition(pass_number=pp.pass_number, label=pp.pass_label, stance=pp.stance_key, description="", focus_dimensions=pp.focus_dimensions, consumes_from=pp.consumes_from)
        recomposed = compose_pass_prompt(cap_def=cap, pass_def=pass_def, depth=DEPTH, shared_context=inner or None)
        res = run_engine_call_auto(system_prompt=recomposed.prompt, user_message=SOURCE, phase_number=1.0, model_hint=MODELS[model_key], depth=DEPTH, label=f"study {engine} pass {pp.pass_number}")
        prior[pp.pass_number] = res["content"]; stances[pp.pass_number] = pp.stance_key; models.add(res.get("model_used"))
        cost += float(res.get("cost_usd") or 0)
        parts.append(f"## Pass {pp.pass_number}: {pp.pass_label} (stance: {pp.stance_key}; dimensions: {', '.join(pp.focus_dimensions or [])})\n\n{res['content']}")
        print(time.strftime("%H:%M:%S"), f"  {engine}/{model_key} pass {pp.pass_number} ({pp.stance_key}) {len(res['content']):,} chars", flush=True)
    record(engine, "harness", model_key, "\n\n---\n\n".join(parts), cost, time.time() - t0, passes=len(pass_prompts), model_used=",".join(sorted(m for m in models if m)))


def oneshot(engine: str, model_key: str, with_questions: bool) -> None:
    reg = get_engine_registry(); cap = reg.get_capability_definition(engine)
    t0 = time.time()
    if engine == "conditions_of_possibility_analyzer":
        task = ("Analyse the conditions of possibility of this text's argument: what had to be true, epistemically, institutionally, materially and discursively, for its ideas to become thinkable; "
                "which prior work and commitments enabled it and which constrain it; the path dependencies; the unacknowledged debts; the alternative paths that were available and foreclosed; "
                "the counterfactual (the argument written by someone with no prior history); and a synthetic judgment on whether the author's history is more enabling or constraining.")
    else:
        task = ("Map the architecture of this text's argument: its claims, grounds, warrants, backing, qualifiers and rebuttals; the argumentation schemes it uses and their characteristic weaknesses; "
                "how it attacks and defends; who must prove what and what is presumed; the suppressed premises; and an overall assessment of where the argument is strong and where it fails.")
    system = ("You are an expert reader in the history of ideas and argumentation. " + task +
              " Anchor every substantive claim in a short verbatim quote from the text. Write for an intelligent executive reader: specific, non-obvious, coherent, no filler.")
    if with_questions:
        qs = [q for d in cap.analytical_dimensions for q in (d.probing_questions or [])]
        system += "\n\nWork through these questions in your own order, but do not answer them mechanically one by one:\n" + "\n".join(f"- {q}" for q in qs)
    res = run_engine_call_auto(system_prompt=system, user_message=SOURCE, phase_number=1.0, model_hint=MODELS[model_key], depth="standard", label=f"study {engine} oneshot")
    record(engine, "oneshot_questions" if with_questions else "oneshot", model_key, res["content"], float(res.get("cost_usd") or 0), time.time() - t0, passes=1, model_used=res.get("model_used"))


RUBRIC = """Score the ANALYSIS on the SOURCE, 1-10 each, with one sentence of reason per criterion, as JSON:
{"specificity": n, "anchoring": n, "non_obviousness": n, "coherence": n, "usefulness": n, "hallucination_risk": n (10 = no risk), "reasons": {...}, "one_line": "..."}
specificity: is it about THIS text or could it be about any text? anchoring: are claims tied to verbatim quotes that exist in the source? non_obviousness: does it find what a careful expert would find but a casual reader would not? coherence: does it hold together as one reading rather than a list? usefulness: would an executive reader act differently after reading it? hallucination_risk: are there claims the source does not support (check quotes against the source)."""


def judge_all() -> None:
    from src.dossier.llm import call_json, call_text  # recorded calls, no job
    judgments = {"rubric": {}, "pairwise": []}
    entries = [m for m in manifest]
    for m in entries:
        content = (OUT / m["file"]).read_text(encoding="utf-8")
        user = f"SOURCE (verbatim):\n\n{SOURCE}\n\n=====\n\nANALYSIS:\n\n{content}"
        try:
            raw, _ = call_json("study-judge", "judge", label=f"rubric {m['file']}", system=RUBRIC, user=user, tool_name="score", model=JUDGE, max_tokens=2000,
                               schema={"type": "object", "properties": {"specificity": {"type": "integer"}, "anchoring": {"type": "integer"}, "non_obviousness": {"type": "integer"}, "coherence": {"type": "integer"}, "usefulness": {"type": "integer"}, "hallucination_risk": {"type": "integer"}, "reasons": {"type": "object"}, "one_line": {"type": "string"}}, "required": ["specificity", "anchoring", "non_obviousness", "coherence", "usefulness", "hallucination_risk", "one_line"]})
            judgments["rubric"][m["file"]] = raw
            print(time.strftime("%H:%M:%S"), "judged", m["file"], {k: raw.get(k) for k in ("specificity", "anchoring", "non_obviousness", "coherence", "usefulness", "hallucination_risk")}, flush=True)
        except Exception as exc:  # noqa: BLE001
            judgments["rubric"][m["file"]] = {"error": str(exc)[:300]}
        (OUT / "judgments.json").write_text(json.dumps(judgments, indent=2))
    # pairwise: harness vs oneshot and vs oneshot_questions, same engine & model, both orders
    by = {(m["engine"], m["condition"], m["model"]): m for m in entries}
    for engine in ENGINES:
        for model in MODELS.values():
            h = by.get((engine, "harness", model))
            for other_cond in ("oneshot", "oneshot_questions"):
                o = by.get((engine, other_cond, model))
                if not h or not o:
                    continue
                for order in ((h, o), (o, h)):
                    a, b = order
                    user = (f"SOURCE (verbatim):\n\n{SOURCE}\n\n=====\n\nANALYSIS A:\n\n{(OUT / a['file']).read_text(encoding='utf-8')}\n\n=====\n\nANALYSIS B:\n\n{(OUT / b['file']).read_text(encoding='utf-8')}")
                    sysm = "Two analyses of the same source. Which is the better reading for an expert who must brief an executive: more specific to this text, better anchored in real quotes, less obvious, more coherent, more useful, fewer unsupported claims? Answer as JSON {\"winner\": \"A\"|\"B\"|\"tie\", \"margin\": \"slight\"|\"clear\"|\"decisive\", \"why\": \"...\", \"what_A_has_that_B_lacks\": \"...\", \"what_B_has_that_A_lacks\": \"...\"}."
                    try:
                        raw, _ = call_json("study-judge", "judge", label=f"pair {a['file']} vs {b['file']}", system=sysm, user=user, tool_name="verdict", model=JUDGE, max_tokens=1500,
                                           schema={"type": "object", "properties": {"winner": {"type": "string"}, "margin": {"type": "string"}, "why": {"type": "string"}, "what_A_has_that_B_lacks": {"type": "string"}, "what_B_has_that_A_lacks": {"type": "string"}}, "required": ["winner", "margin", "why"]})
                        judgments["pairwise"].append({"engine": engine, "model": model, "A": a["file"], "B": b["file"], **raw})
                        print(time.strftime("%H:%M:%S"), "pair", a["condition"], "vs", b["condition"], model, "->", raw.get("winner"), raw.get("margin"), flush=True)
                    except Exception as exc:  # noqa: BLE001
                        judgments["pairwise"].append({"engine": engine, "model": model, "A": a["file"], "B": b["file"], "error": str(exc)[:300]})
                    (OUT / "judgments.json").write_text(json.dumps(judgments, indent=2))


def main() -> None:
    threads = []
    for engine in ENGINES:
        for mk in MODELS:
            threads.append(threading.Thread(target=harness, args=(engine, mk), daemon=True))
            threads.append(threading.Thread(target=oneshot, args=(engine, mk, False), daemon=True))
            if mk == "fable":
                threads.append(threading.Thread(target=oneshot, args=(engine, mk, True), daemon=True))
    for t in threads:
        t.start(); time.sleep(2)
    for t in threads:
        t.join()
    print(time.strftime("%H:%M:%S"), "all runs done; judging", flush=True)
    judge_all()
    total = sum(m["cost_usd"] for m in manifest)
    print(time.strftime("%H:%M:%S"), f"STUDY DONE: {len(manifest)} runs, ${total:.2f} in generation; judgments in data/study/judgments.json", flush=True)


if __name__ == "__main__":
    main()
