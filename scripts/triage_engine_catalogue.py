"""Triage the engine catalogue by reading definitions, not running papers (2026-09-05).

Pass A: every registered analytical engine's definition card (description, researcher question, extraction focus,
schema keys, extraction steps; for the 28 developed engines also the problematique and the probing questions)
goes to GPT-5.6 Sol in small batches from the same category; the model returns per engine: the reader's question
it answers, its family, what its questions ask about (text / author biography / school checklist / off-genre
demand / not analytical), overlaps, distinctive value, and a verdict (keep / merge / rewrite / retire).
Pass B: one call per family with all its cards and judgments returns the consolidated set of methods the family
needs and the reading skills that belong in the critic rather than in any engine.
Code checks shape only (JSON, keys exist, family names). Rubric: communications/study/TRIAGE_rubric_2026-09-05.md.

  python scripts/triage_engine_catalogue.py --dry-run     # cards, batches, cost estimate; no calls
  python scripts/triage_engine_catalogue.py --run         # pass A + pass B + report (resumable)
Note (2026-09-05 22:50): the first run (Sol) is superseded by Codex's independent redo on gpt-6-astra (judgments_codex.json,
families_codex.json, TRIAGE_engine_catalogue_CODEX_2026-09-05.md); this script carries Codex's rubric-review fixes for any rerun.
  python scripts/triage_engine_catalogue.py --report
"""
from __future__ import annotations
import argparse, glob, json, sys, time, collections
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from src.events.pricing import estimate_cost  # noqa: E402
from src.executor.engine_runner import run_engine_call  # noqa: E402
from src.llm.client import parse_llm_json_response  # noqa: E402

OUT = ROOT / "data/study/triage"; OUT.mkdir(parents=True, exist_ok=True)
MODEL = "openrouter/openai/gpt-5.6-sol"; BATCH = 5
FAMILIES = ["genealogy_and_conditions", "argument_and_logic", "concept_mapping", "structure_and_narrative", "rhetoric_and_style",
            "evidence_and_method", "institutions_and_power", "temporal_and_change", "corpus_reports", "other"]
TEXT_FACING = ["text", "author_biography", "school_checklist", "off_genre_demand", "not_analytical", "mixed"]
VERDICTS = ["keep", "merge", "rewrite", "retire"]
UNDER_THE_SHAPE = {"conditions_of_possibility_analyzer", "argument_architecture", "inferential_commitment_mapper", "epistemological_method_detector"}
RUBRIC = (ROOT / "communications/study/TRIAGE_rubric_2026-09-05.md").read_text()
def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)


def build_cards() -> list[dict]:
    caps = {Path(f).stem: yaml.safe_load(open(f)) for f in glob.glob(str(ROOT / "src/engines/capability_definitions/*.yaml"))}
    cat = json.load(open(ROOT / "src/dossier/catalog_purpose.json"))
    offered = {e["engine_key"]: g["key"] for g in cat.get("groups", []) for e in g.get("engines", [])}
    excluded = {e.get("engine_key"): e.get("why") or e.get("reason", "") for e in cat.get("excluded", []) if isinstance(e, dict)}
    cards = []
    for f in sorted(glob.glob(str(ROOT / "src/engines/definitions/*.json"))):
        d = json.load(open(f))
        if d.get("family") not in (None, "", "analytical"):
            continue   # other organs' engines (storytelling, quality, rendering …) are not this triage's object
        key = d["engine_key"]; sc = d.get("stage_context") or {}; ex = sc.get("extraction") or {}
        schema = d.get("canonical_schema") or {}
        card = {
            "key": key, "name": d.get("engine_name"), "category": d.get("category"), "kind": d.get("kind"), "status": d.get("status"),
            "description": (d.get("description") or "")[:700], "researcher_question": d.get("researcher_question"),
            "extraction_focus": d.get("extraction_focus") or [], "extraction_steps": (ex.get("extraction_steps") or [])[:8],
            "schema_keys": [k if not isinstance(v, dict) else f"{k}{{{', '.join(list(v)[:6])}}}" for k, v in list(schema.items())[:10]] if isinstance(schema, dict) else [],
            "paradigm_keys": d.get("paradigm_keys") or [], "apps": d.get("apps") or [],
            "offered_in_group": offered.get(key, ""), "excluded_reason": excluded.get(key, ""),
            "developed": key in caps, "under_the_shape": key in UNDER_THE_SHAPE,
        }
        op_path = ROOT / "src/operationalizations/definitions" / f"{key}.yaml"
        if op_path.exists():
            op = yaml.safe_load(open(op_path)) or {}
            proc = op.get("process") or {}
            if proc.get("dimensions"):
                card["active_process_questions"] = [{"key": d["key"], "questions": d.get("questions", []), "answer_shape": d.get("answer_shape", ""), "method_card": (d.get("method_card") or "")[:400]} for d in proc["dimensions"]]
                card["active_process_source"] = str(op_path.relative_to(ROOT))
        if key in caps:
            c = caps[key]
            card["problematique"] = (c.get("problematique") or "").strip()[:900]
            card["lineage"] = ((c.get("intellectual_lineage") or {}).get("primary") or {}).get("name") if isinstance((c.get("intellectual_lineage") or {}).get("primary"), dict) else None
            card["dimensions"] = [{"key": dm["key"], "description": (dm.get("description") or "").strip()[:220], "questions": dm.get("probing_questions", [])[:6]} for dm in c.get("analytical_dimensions", [])]
        cards.append(card)
    return cards


def card_text(c: dict) -> str:
    lines = [f"### {c['key']} — {c['name']}", f"category: {c['category']} | kind: {c['kind']} | status: {c['status']} | developed definition: {c['developed']} | offered to users in group: {c['offered_in_group'] or 'no'}" + (f" | excluded from the catalogue: {c['excluded_reason']}" if c['excluded_reason'] else ""),
             f"description: {c['description']}", f"researcher question: {c['researcher_question']}",
             f"extraction focus: {', '.join(c['extraction_focus'])}", f"schema: {', '.join(c['schema_keys'])}"]
    if c.get("extraction_steps"): lines.append("extraction steps: " + " | ".join(str(s)[:120] for s in c["extraction_steps"]))
    if c.get("problematique"): lines.append(f"problematique: {c['problematique']}")
    if c.get("lineage"): lines.append(f"lineage: {c['lineage']}")
    for dm in c.get("dimensions", []) or []:
        lines.append(f"- dimension {dm['key']}: {dm['description']}"); lines += [f"    ? {q}" for q in dm["questions"]]
    if c.get("active_process_questions"):
        lines.append(f"ACTIVE QUESTIONS (the ones that run today, from {c['active_process_source']}; the capability dimensions above are the earlier definition):")
        for d in c["active_process_questions"]:
            lines.append(f"- {d['key']}: method card: {d['method_card']}"); lines += [f"    ? {q}" for q in d["questions"]]
    return "\n".join(lines)


def batches(cards: list[dict]) -> list[list[dict]]:
    by_cat = collections.defaultdict(list)
    for c in cards: by_cat[c["category"] or "none"].append(c)
    out = []
    for cat_key in sorted(by_cat):
        cs = by_cat[cat_key]
        for i in range(0, len(cs), BATCH): out.append(cs[i:i + BATCH])
    return out


A_SYSTEM = ("You are triaging an analysis-engine catalogue by reading engine DEFINITIONS. Answer only what the definition lets you answer. "
            "Follow the rubric's per-engine judgment exactly. Return ONE JSON object: {\"judgments\": [{\"key\": …, \"use\": …, \"family\": …, \"text_facing\": …, "
            "\"text_facing_note\": …, \"overlaps_with\": [...], \"distinctive_value\": …, \"verdict\": …, \"merge_into\": …, \"reason\": …}, …]} with one entry per card, "
            f"family ∈ {FAMILIES}, text_facing ∈ {TEXT_FACING}, verdict ∈ {VERDICTS}. No prose outside the JSON.\n\n" + RUBRIC)


def call_json(system: str, user: str, label: str, max_retry: int = 1) -> tuple[dict, float]:
    last = None
    for attempt in range(max_retry + 1):
        res = run_engine_call(system_prompt=system, user_message=user, phase_number=1.0, model_hint=MODEL, depth="standard", label=label)
        cost = estimate_cost(res.get("model_used") or MODEL, res["input_tokens"], res["output_tokens"]) or 0.0
        try:
            r = parse_llm_json_response(res["content"])
            if isinstance(r, list): r = next((x for x in r if isinstance(x, dict)), {})
            return r, cost
        except Exception as exc:  # noqa: BLE001
            last = exc; log(f"  parse failed ({label}), attempt {attempt + 1}: {exc}")
    raise RuntimeError(f"{label}: {last}")


def pass_a(cards, J, all_keys):
    done = {j["key"] for j in J}
    todo = [b for b in batches(cards) if any(c["key"] not in done for c in b)]
    log(f"pass A: {len(todo)} batches to judge ({len(cards) - len(done)} engines)")
    def _do(b):
        keys = [c["key"] for c in b]
        user = "CATALOGUE (all engine keys, for overlaps): " + ", ".join(sorted(all_keys)) + "\n\nCARDS:\n\n" + "\n\n".join(card_text(c) for c in b)
        try:
            r, cost = call_json(A_SYSTEM, user, f"triage A {b[0]['category']} {keys[0]}")
        except Exception as exc:  # noqa: BLE001
            log(f"FAILED batch {keys}: {exc}"); return []
        out = []
        for j in r.get("judgments", []):
            if not isinstance(j, dict) or j.get("key") not in keys: continue
            j["family"] = j.get("family") if j.get("family") in FAMILIES else "other"
            j["text_facing"] = j.get("text_facing") if j.get("text_facing") in TEXT_FACING else "mixed"
            j["verdict"] = j.get("verdict") if j.get("verdict") in VERDICTS else "rewrite"
            j["overlaps_with"] = [k for k in (j.get("overlaps_with") or []) if k in all_keys and k != j["key"]]
            j["merge_into"] = j.get("merge_into") if j.get("merge_into") in all_keys else ""
            if j["verdict"] == "merge" and not j["merge_into"]: j["shape_note"] = "merge without a known target (kept as the model returned it; consolidation must name the target)"
            j["cost_share"] = round(cost / max(1, len(keys)), 4); out.append(j)
        log(f"  judged {len(out)}/{len(keys)}: " + ", ".join(f"{j['key']}={j['verdict']}" for j in out))
        return out
    with ThreadPoolExecutor(max_workers=4) as pool:
        for res in pool.map(_do, todo):
            J.extend(res); (OUT / "judgments.json").write_text(json.dumps(J, indent=2, ensure_ascii=False))


B_SYSTEM = ("You are consolidating one family of analysis engines from their definition cards and the per-engine triage judgments. Follow the rubric's "
            "family consolidation. Choose the number of methods warranted by the reader questions and the cards; there is no target count or compression ratio. "
            "For each proposed combination, say what is shared, what distinct questions remain as dimensions, and what would be lost; for each proposed separation, "
            "state the distinct reader question. Account for every engine once as a disposition (folds into a method, retired, or unresolved for lack of evidence). "
            "Revise a pass-A placement or verdict when the fuller comparison warrants it, naming the evidence. Critic skills are reading disciplines that recur across "
            "the family and belong in the critic's duties, each one imperative sentence. Return ONE JSON object: {\"family\": …, \"methods\": [{\"name\": …, \"reader_question\": …, \"folds_in\": [engine keys], "
            "\"questions_source\": \"<engine key whose questions can serve>\" | \"new\", \"why\": …}], \"critic_skills\": [\"<a reading skill that recurs and belongs in the critic or a shared method card>\", …], "
            "\"retire\": [{\"key\": …, \"reason\": …}], \"unresolved\": [{\"key\": …, \"reason\": …}], \"revisions\": [{\"key\": …, \"field\": …, \"from\": …, \"to\": …, \"evidence\": …}], \"note\": …}. No prose outside the JSON.\n\n" + RUBRIC)


def pass_b(cards, J, F):
    by_key = {c["key"]: c for c in cards}; fams = collections.defaultdict(list)
    for j in J: fams[j["family"]].append(j)
    done = {f["family"] for f in F}
    for fam, js in sorted(fams.items()):
        if fam in done or fam == "other" and len(js) == 0: continue
        user = f"FAMILY: {fam} ({len(js)} engines)\n\n" + "\n\n".join(card_text(by_key[j["key"]]) + "\n  triage: " + json.dumps({k: j[k] for k in ("use", "text_facing", "overlaps_with", "distinctive_value", "verdict", "merge_into", "reason")}, ensure_ascii=False) for j in js)
        try:
            r, cost = call_json(B_SYSTEM, user, f"triage B {fam}")
        except Exception as exc:  # noqa: BLE001
            log(f"FAILED family {fam}: {exc}"); continue
        r["family"] = fam; r["cost_usd"] = round(cost, 4); F.append(r); (OUT / "families.json").write_text(json.dumps(F, indent=2, ensure_ascii=False))
        log(f"  family {fam}: {len(r.get('methods', []))} methods, {len(r.get('retire', []))} retire, {len(r.get('critic_skills', []))} critic skills, ${cost:.2f}")


def report(cards, J, F):
    by = {j["key"]: j for j in J}; byc = {c["key"]: c for c in cards}
    lines = ["# Engine catalogue triage (2026-09-05)", "", f"{len(cards)} registered analytical engines read as definitions by GPT-5.6 Sol; {len(J)} judged; {len(F)} families consolidated. "
             f"Cost ${sum(j.get('cost_share', 0) for j in J) + sum(f.get('cost_usd', 0) for f in F):.2f}. Rubric: `TRIAGE_rubric_2026-09-05.md`. Judgments: `data/study/triage/`.", ""]
    vc = collections.Counter(j["verdict"] for j in J); tf = collections.Counter(j["text_facing"] for j in J); fc = collections.Counter(j["family"] for j in J)
    lines += ["## Counts", "", "| verdict | n |", "|---|---|"] + [f"| {k} | {n} |" for k, n in vc.most_common()] + ["", "| what the questions ask about | n |", "|---|---|"] + [f"| {k} | {n} |" for k, n in tf.most_common()] + ["", "| family | n |", "|---|---|"] + [f"| {k} | {n} |" for k, n in fc.most_common()]
    off = [j for j in J if byc[j["key"]]["offered_in_group"]]
    lines += ["", "## The engines users are offered today", "", "| engine | group | verdict | asks about | use | reason |", "|---|---|---|---|---|---|"]
    for j in sorted(off, key=lambda j: (byc[j["key"]]["offered_in_group"], j["key"])):
        lines.append(f"| {j['key']} | {byc[j['key']]['offered_in_group']} | **{j['verdict']}**{(' → ' + j['merge_into']) if j['merge_into'] else ''} | {j['text_facing']} | {j['use'][:140]} | {j['reason'][:160]} |")
    lines += ["", "## Consolidated families", ""]
    for f in sorted(F, key=lambda f: f["family"]):
        lines += [f"### {f['family']}", ""]
        for m in f.get("methods", []):
            lines.append(f"- **{m.get('name')}** — {m.get('reader_question')} — folds in: {', '.join(m.get('folds_in', []))} — questions: {m.get('questions_source')} — {m.get('why', '')[:200]}")
        if f.get("critic_skills"): lines += ["", "Reading skills for the critic or a shared method card: " + "; ".join(f["critic_skills"])]
        if f.get("retire"): lines += ["", "Retire: " + "; ".join(f"{r.get('key')} ({r.get('reason', '')[:90]})" for r in f["retire"])]
        if f.get("note"): lines += ["", f"Note: {f['note']}"]
        lines.append("")
    lines += ["## Every engine", "", "| engine | family | asks about | verdict | use | overlaps | reason |", "|---|---|---|---|---|---|---|"]
    for j in sorted(J, key=lambda j: (j["family"], j["verdict"], j["key"])):
        lines.append(f"| {j['key']}{' *' if byc[j['key']]['developed'] else ''} | {j['family']} | {j['text_facing']} | {j['verdict']}{(' → ' + j['merge_into']) if j['merge_into'] else ''} | {j['use'][:120]} | {', '.join(j['overlaps_with'][:4])} | {j['reason'][:150]} |")
    lines += ["", "`*` = has a developed capability definition (28). Missing from the table = the model returned no judgment for it (see the log)."]
    (ROOT / "communications/study/TRIAGE_engine_catalogue_2026-09-05.md").write_text("\n".join(lines)); log("wrote communications/study/TRIAGE_engine_catalogue_2026-09-05.md")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--run", action="store_true"); ap.add_argument("--report", action="store_true"); a = ap.parse_args()
    cards = build_cards(); (OUT / "cards.json").write_text(json.dumps(cards, indent=2, ensure_ascii=False)); all_keys = {c["key"] for c in cards}
    bs = batches(cards)
    if a.dry_run or not (a.run or a.report):
        toks = sum(len(A_SYSTEM + "\n\n".join(card_text(c) for c in b)) // 4 + 2500 for b in bs)
        est_a = sum(estimate_cost(MODEL, len(A_SYSTEM + "\n\n".join(card_text(c) for c in b)) // 4 + 1500, 1800) or 0 for b in bs)
        est_b = 10 * (estimate_cost(MODEL, 25000, 3000) or 0)
        print(f"{len(cards)} analytical engines ({sum(c['developed'] for c in cards)} developed, {sum(1 for c in cards if c['offered_in_group'])} offered); {len(bs)} batches of ≤{BATCH} by category; pass A ≈ ${est_a:.2f}, pass B ≈ ${est_b:.2f}; total ≈ ${est_a + est_b:.2f}")
        print("categories:", dict(collections.Counter(c["category"] for c in cards))); sys.exit(0)
    J = json.loads((OUT / "judgments.json").read_text()) if (OUT / "judgments.json").exists() else []
    F = json.loads((OUT / "families.json").read_text()) if (OUT / "families.json").exists() else []
    if a.run:
        pass_a(cards, J, all_keys); pass_b(cards, J, F)
    report(cards, J, F); log("DONE")
