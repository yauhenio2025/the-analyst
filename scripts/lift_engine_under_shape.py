"""Lift a developed engine under the shape with its existing questions (2026-09-06; the consolidation recipe's first step).

From the engine's capability YAML: each analytical dimension becomes a process dimension (its probing questions kept
verbatim; the method card written from the intellectual groundings of the capabilities that produce the dimension, as
imperatives; indicators from those capabilities; a generic anchored answer shape), plus one generic corpus dimension
(the same finding across documents, two anchors) that runs only with two or more documents. Steps, routing and modes
are the standard ones (surface = one call, standard = one call + critic, deep = the chain; Sol / DeepSeek V4 Pro / Luna).
If an operationalization file exists its stance passes are kept for reference and gain `mode:`; otherwise one is created.
The result is a starting point to be read, not a finished definition: rewrite questions only on demonstrated defects.

  python scripts/lift_engine_under_shape.py comparative_reasoning_analyzer concept_centrality_mapper chapter_role_analyzer
  python scripts/lift_engine_under_shape.py --dry-run <key>      # print the block without writing
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
CAPS = ROOT / "src/engines/capability_definitions"; OPS = ROOT / "src/operationalizations/definitions"
ROUTING = {"cheap": "openrouter/openai/gpt-5.6-luna", "mid": "openrouter/deepseek/deepseek-v4-pro", "strong": "openrouter/openai/gpt-5.6-sol"}
MODES = [{"depth_key": "surface", "mode": "oneshot"}, {"depth_key": "standard", "mode": "oneshot_checked"}, {"depth_key": "deep", "mode": "dvs"}, {"depth_key": "dvs", "process": "dvs"}]


def _name(key: str) -> str: return key.replace("_", " ").capitalize()


def _card(dim_key: str, caps: list[dict], questions: list[str] | None = None) -> tuple[str, list[str]]:
    producers = [c for c in caps if dim_key in (c.get("produces_dimensions") or [])]
    parts, indicators = [], []
    for c in producers:
        g = c.get("intellectual_grounding") or {}
        thinker = (g.get("thinker") or "").replace("_", " ").title(); method = (g.get("method") or "").strip().rstrip(".")
        if method:
            parts.append(f"{thinker}: {method[0].lower() + method[1:]}" if thinker else method)
        indicators += [i for i in (c.get("indicators") or []) if i not in indicators]
    body = "; ".join(parts) if parts else "read the dimension's questions against the text and answer only what its sentences show"
    if not indicators:   # no capability produces this dimension: hunt for the sentences that answer its questions
        indicators = [f"a sentence that answers: {q.rstrip('?')[:90].lower()}" for q in (questions or [])[:3]] or ["a sentence that names the dimension's object"]
    return (f"Do: {body}. Anchor every finding in the sentence that shows it; a claim about the authors' minds or careers is not a finding.", indicators[:6])


def lift(key: str) -> dict:
    cap = yaml.safe_load(open(CAPS / f"{key}.yaml")); dims = cap.get("analytical_dimensions") or []; caps = cap.get("capabilities") or []
    if not dims: raise SystemExit(f"{key}: no analytical dimensions to lift")
    pd = []
    for i, d in enumerate(dims, 1):
        prefix = f"D{i}"; card, ind = _card(d["key"], caps, d.get("probing_questions") or [])
        pd.append({"key": d["key"], "id_prefix": prefix, "name": _name(d["key"]), **({"load_bearing": True} if i <= min(3, len(dims)) else {}),
                   "questions": list(d.get("probing_questions") or []),
                   "answer_shape": f'[{prefix}.F<n>] <the finding in one sentence, naming the passage\'s object> — dim: {d["key"]} — anchor: "<verbatim>" — confidence: high|medium|low',
                   "method_card": card, "indicators": ind})
    pd.append({"key": "shared_across_corpus", "id_prefix": "X" + str(len(dims) + 1), "name": "The same finding across the corpus", "scope": "corpus",
               "questions": ["Which findings recur across documents, in the same or different words? Anchor each in each document.", "On which question do documents diverge? Both anchors, with the object and scope of each."],
               "answer_shape": f'[X{len(dims) + 1}.F<n>] <shared finding | divergence> — dim: shared_across_corpus — anchor: "<verbatim>" — doc: <A> — anchor-b: "<verbatim>" — doc-b: <B> — confidence: …',
               "method_card": "Do: match findings across documents by their object, not their wording; state recurrence and divergence with two anchors; do not settle a divergence here.", "indicators": ["the same claim in two documents", "a term used differently in two documents"]})
    order = "\n".join(f"{i}. {_name(d['key'])}: {(d.get('description') or '').strip().split('.')[0][:160]}." for i, d in enumerate(dims, 1))
    brief = (f"{order}\n{len(dims) + 1}. The judgment: what the text establishes on this method's question, what it leaves open, and the one finding a reader should test first.\n"
             "Carry one line of argument through the parts; cite findings by id; no claim without a row.")
    steps = [{"key": "extract", "kind": "extract", "parallel_over": "dimension", "model_tier": "cheap", "output": "ledger", "max_rows": 16},
             {"key": "verify", "kind": "verify", "consumes": ["extract"], "model_tier": "mid", "output": "ledger", "duties": ["check_anchors_in_context", "reject_biography", "merge_duplicates", "hunt_misses", "name_must_keep"]},
             {"key": "synthesize", "kind": "synthesize", "consumes": ["verify"], "model_tier": "strong", "output": "prose_ledger", "is_final": True,
              "reader": f"a reader who must know what this text establishes on the question: {cap.get('researcher_question') or cap['engine_name']}",
              "tables": [d["key"] for d in dims[:3]], "brief": brief}]
    return {"key": "dvs", "description": f"{cap['engine_name']} under the shape with its existing questions (lifted {__import__('datetime').date.today().isoformat()}): {(cap.get('researcher_question') or '').strip()} Every finding anchored; nothing about the authors.", "routing": ROUTING, "dimensions": pd, "steps": steps}


def write(key: str, process: dict) -> Path:
    path = OPS / f"{key}.yaml"; dump = lambda o: yaml.safe_dump(o, sort_keys=False, allow_unicode=True, width=110)
    if path.exists():
        op = yaml.safe_load(path.read_text()) or {}
        if op.get("process") and "lifted" not in str((op.get("process") or {}).get("description", "")):
            raise SystemExit(f"{key}: has a hand-written process block; refusing to overwrite")
        seqs = {s["depth_key"]: s for s in op.get("depth_sequences") or []}
        for m in MODES:
            if m["depth_key"] in seqs: seqs[m["depth_key"]].update({k: v for k, v in m.items() if k != "depth_key"})
            else: seqs[m["depth_key"]] = m
        op["depth_sequences"] = list(seqs.values()); op["process"] = process
        path.write_text(f"# Lifted under the shape (existing questions) by scripts/lift_engine_under_shape.py; stance passes kept for reference.\n" + dump(op))
    else:
        cap = yaml.safe_load(open(CAPS / f"{key}.yaml"))
        path.write_text(f"engine_key: {key}\nengine_name: {cap['engine_name']}\n# Lifted under the shape (existing questions) by scripts/lift_engine_under_shape.py.\nstance_operationalizations: []\n" + dump({"depth_sequences": MODES, "process": process}))
    return path


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("keys", nargs="+"); ap.add_argument("--dry-run", action="store_true"); a = ap.parse_args()
    for key in a.keys:
        proc = lift(key)
        if a.dry_run: print(yaml.safe_dump({"process": proc}, sort_keys=False, allow_unicode=True, width=110)); continue
        p = write(key, proc); print(f"{key}: written {p.relative_to(ROOT)} ({len(proc['dimensions'])} dimensions)")
