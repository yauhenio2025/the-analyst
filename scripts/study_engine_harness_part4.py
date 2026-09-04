"""Study part 4 (fairness check): judge the harness's FINAL integration pass alone against the one-shots."""
import json, os, re, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from src.dossier.llm import call_json
OUT = ROOT / "data" / "study"; SOURCE = (OUT / "source_aukus.txt").read_text(encoding="utf-8")
ms = json.loads((OUT / "manifest.json").read_text()); by = {(m["engine"], m["condition"], m["model"]): m for m in ms}
PAIR_SCHEMA = {"type": "object", "properties": {"winner": {"type": "string", "enum": ["A", "B", "tie"]}, "margin": {"type": "string", "enum": ["slight", "clear", "decisive"]}, "why": {"type": "string"}}, "required": ["winner", "margin", "why"]}
PAIR = "Two analyses of the same source. Which is the better reading for an expert who must brief an executive: more specific to this text, better anchored in real quotes, less obvious, more coherent, more useful, fewer unsupported claims? Judge the reading, not the length."
def last_pass(text):
    parts = re.split(r"\n\n---\n\n(?=## Pass )", text); return parts[-1]
out = []
for engine in ("conditions_of_possibility_analyzer", "argument_architecture"):
    for model in ("claude-sonnet-4-6", "claude-fable-5-1"):
        h = by.get((engine, "harness", model)); o = by.get((engine, "oneshot", model))
        if not h or not o: continue
        hp = last_pass((OUT / h["file"]).read_text(encoding="utf-8")); op = (OUT / o["file"]).read_text(encoding="utf-8")
        (OUT / "outputs" / f"{engine}__harness_integration_only__{'sonnet' if 'sonnet' in model else 'fable'}.md").write_text(hp, encoding="utf-8")
        for (a, at), (b, bt) in (((h, hp), (o, op)), ((o, op), (h, hp))):
            user = f"SOURCE (verbatim):\n\n{SOURCE}\n\n=====\n\nANALYSIS A:\n\n{at}\n\n=====\n\nANALYSIS B:\n\n{bt}"
            try:
                r, _ = call_json("study-judge", "judge", label="pair integration", system=PAIR, user=user, tool_name="verdict", schema=PAIR_SCHEMA, model="claude-sonnet-4-6", max_tokens=1200)
            except Exception as exc:
                r = {"error": str(exc)[:200]}
            rec = {"engine": engine, "model": model, "A": a["condition"] + ("(integration pass only)" if a is h else ""), "B": b["condition"] + ("(integration pass only)" if b is h else ""), **r}
            out.append(rec); (OUT / "judgments_integration_only.json").write_text(json.dumps(out, indent=2))
            print(time.strftime("%H:%M:%S"), engine[:14], model[-10:], rec["A"], "vs", rec["B"], "->", r.get("winner"), r.get("margin"), flush=True)
print("PART 4 DONE")
