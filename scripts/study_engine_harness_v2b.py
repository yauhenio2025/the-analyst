"""Did the plumbing help? Judge the fixed harness's final pass against the pre-fix integration pass, same engine and model, both orders."""
import json, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from src.dossier.llm import call_json
OUT = ROOT / "data" / "study"; SOURCE = (OUT / "source_aukus.txt").read_text(encoding="utf-8")
PAIR_SCHEMA = {"type": "object", "properties": {"winner": {"type": "string", "enum": ["A", "B", "tie"]}, "margin": {"type": "string", "enum": ["slight", "clear", "decisive"]}, "why": {"type": "string"}}, "required": ["winner", "margin", "why"]}
PAIR = "Two analyses of the same source. Which is the better reading for an expert who must brief an executive: more specific to this text, better anchored in real quotes, less obvious, more coherent, more useful, fewer unsupported claims? Judge the reading, not the length."
out = []
for engine in ("conditions_of_possibility_analyzer", "argument_architecture"):
    for mk, model in (("sonnet", "claude-sonnet-4-6"), ("fable", "claude-fable-5-1")):
        new = (OUT / "outputs" / f"{engine}__harness_v2_final__{mk}.md").read_text(encoding="utf-8")
        old = (OUT / "outputs" / f"{engine}__harness_integration_only__{mk}.md").read_text(encoding="utf-8")
        for (an, at), (bn, bt) in ((("fixed_final", new), ("prefix_final", old)), (("prefix_final", old), ("fixed_final", new))):
            try:
                r, _ = call_json("study-judge", "judge", label="pair fixed vs prefix", system=PAIR, user=f"SOURCE:\n\n{SOURCE}\n\n=====\n\nANALYSIS A:\n\n{at}\n\n=====\n\nANALYSIS B:\n\n{bt}", tool_name="verdict", schema=PAIR_SCHEMA, model="claude-sonnet-4-6", max_tokens=1000)
            except Exception as exc: r = {"error": str(exc)[:200]}
            w = r.get("winner"); out.append({"engine": engine, "model": model, "A": an, "B": bn, **r}); (OUT / "judgments_v2_fixed_vs_prefix.json").write_text(json.dumps(out, indent=2))
            print(time.strftime("%H:%M:%S"), engine[:14], mk, an, "vs", bn, "->", (an if w == "A" else bn if w == "B" else w), r.get("margin"), "|", (r.get("why") or "")[:160], flush=True)
print("DONE")
