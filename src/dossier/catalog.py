"""The purpose-first engine catalog, recipes, audience vocabulary and path arithmetic for the brief.

Design: communications/DESIGN_brief_deliverables.md §C3 (GET /v1/dossier/catalog), §D (content),
§B5 (the code-side checks' vocabulary and estimate rules).

Everything here is code, not judgment: catalog membership comes from the runtime capability registry
joined with `catalog_purpose.json` (a missing YAML drops an engine, never a stale entry); prices are
arithmetic over pass counts; the vocabulary ban-list is a fixed list of theory terms.
"""
from __future__ import annotations

import json
import logging
import re
from functools import lru_cache
from pathlib import Path as FsPath
from typing import Any, Optional

from src.dossier.common import EXCLUDED_PREFIXES, SYNTHESIS_ENGINES, engine_catalog, estimate_engine_run, passes_for
from src.dossier.schemas import DEPTHS, STEP_DEPTHS, Path, PathRequest, PathStep

logger = logging.getLogger(__name__)

HERE = FsPath(__file__).resolve().parent
PURPOSE_PATH = HERE / "catalog_purpose.json"
RECIPES_PATH = HERE / "recipes.json"

FIT_ORDER = ("ok", "conditional", "off", "not_for_dossier")

# Theory vocabulary an executive card must not carry (rule 5). Quoted spans are exempt — a verbatim
# phrase from a document is evidence, not jargon. Kept short and unambiguous on purpose: the raw
# 1,599-term translation table contains "claim", "evidence", "pattern" — words no card can avoid.
EXECUTIVE_BAN_TERMS = (
    "inferential commitment", "inferential commitments", "inferential", "dialectical", "dialectic", "dialectics",
    "counterfactual", "counterfactuals", "hegemony", "hegemonic", "discourse", "discourses", "discursive",
    "epistemology", "epistemological", "epistemic", "genealogy", "genealogical", "appropriation", "legitimation",
    "neoliberal", "neoliberalism", "ontology", "ontological", "problematique", "teleological", "praxis", "semiotic",
    "semantic field", "semantic constellation", "conditions of possibility", "constitutive", "modal reasoning",
    "taxonomy", "theoretical framework", "conceptual framework", "conceptual frameworks", "centrality", "antithesis",
    "paradigm", "paradigmatic", "ideology", "ideological", "reification", "commodification", "governmentality",
    "biopolitics", "subaltern", "intersubjective", "phenomenological", "hermeneutic", "positivist", "structuralist",
    "post-structuralist", "poststructuralist", "critical theory", "argumentative function", "entitlement relation",
    "incompatibility relation", "material inference",
)
# Terms the executive vocabulary file does not translate; the prompt supplies these plain equivalents.
FALLBACK_TRANSLATIONS = {
    "legitimation": "earning acceptance (how a claim comes to be accepted as fair or right)",
    "appropriation": "capture (taking a term or an idea for one's own purposes)",
    "neoliberal": "market-first (policy that favours markets over the state)",
    "ontology": "the map of what a house treats as real",
    "problematique": "the underlying problem",
    "praxis": "practice",
    "semiotic": "sign-and-meaning",
    "ideology": "belief system (the assumptions behind a position)",
    "paradigm": "model (the standard way of thinking)",
    "reification": "treating an idea as a thing",
    "commodification": "turning something into a product for sale",
    "discursive": "narrative-based (carried by how things are talked about)",
    "epistemic": "about what counts as knowing",
    "inferential": "what-follows-from-what",
    "hermeneutic": "interpretive",
    "normative": "value-based (what ought to be)",
}
# Vocabulary lines the prompt shows for the executive register (~40): the ban terms that the file
# translates, plus the theory words the catalog text itself uses.
EXECUTIVE_VOCAB_TERMS = EXECUTIVE_BAN_TERMS + (
    "concept appropriation", "dialectical structure", "contingency", "methodological", "core concept",
    "peripheral concept", "knowledge claims", "causal claim", "backing", "synthesis", "bridge",
)


# ── files ─────────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def load_purpose() -> dict:
    with open(PURPOSE_PATH, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_recipes() -> list[dict]:
    with open(RECIPES_PATH, encoding="utf-8") as f:
        return json.load(f).get("recipes", [])


@lru_cache(maxsize=1)
def purpose_index() -> dict[str, dict]:
    """engine_key -> purpose entry (+ group key/title)."""
    out = {}
    for g in load_purpose().get("groups", []):
        for e in g.get("engines", []):
            out[e["engine_key"]] = {**e, "group": g["key"], "group_title": g["title"]}
    return out


def excluded_reasons() -> dict[str, str]:
    return {e["engine_key"]: e["why"] for e in load_purpose().get("excluded", [])}


# ── names and vocabulary ──────────────────────────────────────────────────

def plain_name_for(engine_key: str, audience: str, by_key: Optional[dict] = None) -> str:
    """Executive: the purpose catalog's plain name. Analyst/researcher: the engine's own name."""
    entry = purpose_index().get(engine_key)
    if audience == "executive" and entry and entry.get("plain_name"):
        return entry["plain_name"]
    if by_key and engine_key in by_key:
        return by_key[engine_key].get("engine_name") or engine_key.replace("_", " ")
    if entry and entry.get("plain_name"):
        return entry["plain_name"]
    return engine_key.replace("_", " ")


def _translations(audience: str) -> dict[str, str]:
    try:
        from src.audiences.registry import get_audience_registry

        a = get_audience_registry().get(audience)
        return dict(a.vocabulary.translations) if a else {}
    except Exception as exc:  # the vocabulary is guidance; its absence never blocks the brief
        logger.warning(f"audience vocabulary unavailable for {audience}: {exc}")
        return {}


def vocabulary_lines(audience: str) -> list[tuple[str, str]]:
    """(theory term, plain equivalent) pairs for the prompt — executive only; other registers keep the terms."""
    if audience != "executive":
        return []
    tr = _translations(audience)
    out, seen = [], set()
    for term in EXECUTIVE_VOCAB_TERMS:
        if term in seen:
            continue
        plain = tr.get(term) or FALLBACK_TRANSLATIONS.get(term)
        if plain and plain.strip().lower() != term.lower():
            out.append((term, plain))
            seen.add(term)
    return out


def ban_terms(audience: str) -> tuple[str, ...]:
    return EXECUTIVE_BAN_TERMS if audience == "executive" else ()


_QUOTED = re.compile(r"[“\"]([^”\"]{3,}?)[”\"]")


def jargon_hits(text: str, terms: tuple[str, ...] | list[str]) -> list[str]:
    """Banned terms present in `text` (case-insensitive, word-bounded; quoted spans exempt)."""
    if not text or not terms:
        return []
    scrubbed = _QUOTED.sub(" ", text)
    hits = []
    for term in terms:
        body = r"[\s-]+".join(re.escape(w) for w in re.split(r"[\s-]+", term.strip()) if w)
        pat = r"(?<![\w-])" + body + r"(?![\w-])"
        if re.search(pat, scrubbed, flags=re.IGNORECASE):
            hits.append(term)
    return hits


# ── fit for this corpus ───────────────────────────────────────────────────

def fit_for_corpus(entry: dict, n_docs: Optional[int], same_author: Optional[bool]) -> tuple[str, str]:
    fit = entry.get("fit", "ok")
    note = entry.get("fit_note", "") or ""
    when = entry.get("applies_when")
    if fit != "conditional" or not when:
        return fit, note
    if when == "single_document" and n_docs and n_docs > 1:
        return "off", f"single long work only — this corpus has {n_docs} documents"
    if when == "same_author" and same_author is False:
        return "off", "presumes one author across time — this bundle has several authors"
    if when == "prior_phases":
        return "conditional", "only as the last step, after a concept engine has run"
    if when == "surface_only":
        return "conditional", "usable at surface depth on a corpus; " + note
    return fit, note


# ── the catalog ───────────────────────────────────────────────────────────

def _depth_estimates(reg_entry: dict, corpus_chars: Optional[int]) -> dict[str, dict]:
    out = {}
    for dk, dv in (reg_entry.get("depths") or {}).items():
        passes = int(dv.get("passes", 1) or 1)
        row: dict[str, Any] = {"passes": passes}
        if corpus_chars:
            cost, minutes = estimate_engine_run(corpus_chars, passes)
            row["est_cost_usd"] = cost
            row["est_minutes"] = minutes
        out[dk] = row
    return out


def purpose_catalog(audience: str = "executive", corpus_chars: Optional[int] = None, n_docs: Optional[int] = None,
                    same_author: Optional[bool] = None) -> dict:
    """The picker's source of truth: purpose groups joined with the runtime registry, recipes, exclusions."""
    registry = {e["engine_key"]: e for e in engine_catalog(for_dossier=False)}
    reasons = excluded_reasons()
    executable = {k for k in registry if not k.startswith(EXCLUDED_PREFIXES) and k not in reasons}
    idx = purpose_index()
    groups = []
    placed = set()
    for g in load_purpose().get("groups", []):
        engines = []
        for e in g.get("engines", []):
            key = e["engine_key"]
            if key not in executable:
                logger.info(f"catalog: {key} is in catalog_purpose.json but has no capability YAML — dropped")
                continue
            reg = registry[key]
            fit, fit_note = fit_for_corpus(e, n_docs, same_author)
            engines.append({
                "engine_key": key,
                "engine_name": reg.get("engine_name", key),
                "plain_name": plain_name_for(key, audience, registry),
                "executive_name": e.get("plain_name", ""),
                "use_when": e.get("use_when", ""),
                "yields": e.get("yields", ""),
                "row_unit": e.get("row_unit", ""),
                "deliverable_kinds": e.get("deliverable_kinds", []),
                "pairs_with": [p for p in e.get("pairs_with", []) if p in executable],
                "depths": _depth_estimates(reg, corpus_chars),
                "fit": fit, "fit_note": fit_note,
                "category": reg.get("category", ""),
            })
            placed.add(key)
        groups.append({"key": g["key"], "title": g["title"], "purpose": g.get("purpose", ""), "engines": engines})
    # Eligible engines without a purpose entry appear in More; explicit exclusions stay excluded.
    more = []
    for key in sorted(executable - placed):
        reg = registry[key]
        more.append({
            "engine_key": key, "engine_name": reg.get("engine_name", key), "plain_name": plain_name_for(key, audience, registry),
            "executive_name": "", "use_when": reg.get("researcher_question", ""), "yields": "", "row_unit": "",
            "deliverable_kinds": [], "pairs_with": [], "depths": _depth_estimates(reg, corpus_chars),
            "fit": "ok", "fit_note": "not yet described by purpose", "category": reg.get("category", ""),
        })
    if more:
        groups.append({"key": "more", "title": "More", "purpose": "executable engines not yet described by purpose", "engines": more})
    excluded = [{"engine_key": k, "why": reasons.get(k, "not for a document dossier")}
                for k in sorted(registry) if k not in executable]
    recipes = []
    for r in load_recipes():
        if any(s["engine_key"] not in executable for s in r.get("steps", [])):
            logger.info(f"catalog: recipe {r['key']} references a non-executable engine — dropped")
            continue
        steps = [PathStep(engine_key=s["engine_key"], depth=s.get("depth", "surface"),
                          plain_name=plain_name_for(s["engine_key"], audience, registry)) for s in r["steps"]]
        path = Path(steps=steps, depth=r.get("depth") or path_depth_from_steps(steps, registry), chain_key=r["key"])
        cost, minutes, calls = estimate_path(path, corpus_chars or 0, registry) if corpus_chars else (0.0, 0.0, 0)
        recipes.append({
            "key": r["key"], "title": r["title"], "use_when": r.get("use_when", ""), "yields": r.get("yields", ""),
            "depth": path.depth, "steps": [s.model_dump() for s in steps],
            "est_cost_usd": cost, "est_minutes": minutes, "est_llm_calls": calls,
        })
    own_cost, own_min = estimate_engine_run(corpus_chars, 3) if corpus_chars else (0.0, 0.0)
    return {
        "audience": audience, "corpus_chars": corpus_chars, "n_docs": n_docs,
        "groups": groups, "recipes": recipes, "excluded": excluded,
        "own_overhead": {"est_cost_usd": round(own_cost, 3), "est_minutes": round(own_min + 2, 1), "calls": 4,
                         "why": "the dossier's own calls: plan, tables, figure plan, compose"},
        "use_kinds": list(USE_REGISTER.keys()),
    }


USE_REGISTER = {
    "decide": "choose between courses of action; retire/advance something",
    "brief": "bring a board, a CEO, a committee up to speed for a meeting",
    "prepare": "get ready for a negotiation, a pitch, a challenge, a hearing",
    "stress_test": "test our own position or claims before they are attacked",
    "compare": "set two or more cases/options side by side to choose",
    "watch": "set up what to monitor and the early signs to look for",
    "learn": "get up to speed on a field or a set of papers fast",
    "argue": "build or defend a case with the strongest evidence",
}


def catalog_purpose_text(catalog: dict, audience: str) -> str:
    """The EXECUTABLE ENGINES block of the brief prompt: purpose one-liners + depths/passes + fit for this corpus."""
    lines = []
    for g in catalog["groups"]:
        lines.append(f"## {g['title']} — {g['purpose']}")
        for e in g["engines"]:
            passes = ", ".join(f"{k}={v['passes']}p" for k, v in e["depths"].items())
            name = f'{e["engine_key"]} — plain_name "{e["plain_name"]}"' if audience == "executive" else f'{e["engine_key"]} — {e["engine_name"]}'
            lines.append(f"- {name} ({passes})")
            lines.append(f"  use when you need to: {e['use_when']}")
            lines.append(f"  yields: {e['yields']}" + (f"; row unit: {e['row_unit']}" if e.get("row_unit") else ""))
            if e["fit"] == "off":
                lines.append(f"  NOT FOR THIS CORPUS: {e['fit_note']}")
            elif e["fit"] == "conditional":
                lines.append(f"  conditional: {e['fit_note']}")
            elif e.get("fit_note"):
                lines.append(f"  note: {e['fit_note']}")
    if catalog.get("recipes"):
        lines.append("## Recipes (paths that work well together; you may use or vary them)")
        for r in catalog["recipes"]:
            lines.append(f"- {r['title']}: " + " → ".join(f"{s['engine_key']}@{s['depth']}" for s in r["steps"]) + f" — {r['use_when']}; yields {r['yields']}")
    return "\n".join(lines)


def plain_name_lines(catalog: dict) -> str:
    out = []
    for g in catalog["groups"]:
        for e in g["engines"]:
            out.append(f'  {e["engine_key"]} = "{e["plain_name"]}"')
    return "\n".join(out)


# ── path arithmetic ───────────────────────────────────────────────────────

def path_depth_from_steps(steps: list[PathStep], by_key: dict) -> str:
    """The option's weight label from its own steps (code decides labels, not the model)."""
    passes = sum(passes_for(by_key.get(s.engine_key, {}), s.depth) for s in steps)
    n = len(steps)
    if n <= 1 and passes <= 1:
        return "simple"
    if n <= 3 and passes <= 4:
        return "medium"
    return "advanced"


def estimate_path(path: Path, corpus_chars: int, by_key: dict) -> tuple[float, float, int]:
    """(cost_usd, minutes, llm_calls) for an option from ITS OWN steps — so three options price differently."""
    passes = sum(passes_for(by_key.get(s.engine_key, {}), s.depth) for s in path.steps)
    passes = max(1, min(passes, 10))
    engine_cost, engine_min = estimate_engine_run(corpus_chars, passes)
    own_cost, own_min = estimate_engine_run(corpus_chars, 3)  # plan, tables, compose + figure plan
    return round(engine_cost + own_cost, 2), round(engine_min + own_min + 2, 1), passes + 4


def validate_steps(steps: list[PathStep], by_key: dict) -> list[PathStep]:
    """Executable keys only, unique (a trailing synthesis engine may repeat), 1-4 steps, known depths."""
    out: list[PathStep] = []
    seen: set[str] = set()
    for s in steps:
        if s.engine_key not in by_key:
            continue
        if s.engine_key in seen:
            is_trailing_synthesis = (s is steps[-1]) and s.engine_key in SYNTHESIS_ENGINES
            if not is_trailing_synthesis:
                continue
        if s.depth not in STEP_DEPTHS:
            s.depth = "surface"
        out.append(s)
        seen.add(s.engine_key)
    return out[:4]


def resolve_path_request(req: PathRequest, audience: str = "executive", by_key: Optional[dict] = None) -> Path:
    """A lane-2 request -> a Path (recipe steps filled in). Raises ValueError with the reader's reason."""
    by_key = by_key or {e["engine_key"]: e for e in engine_catalog()}
    steps: list[PathStep] = []
    chain_key = req.chain_key
    if chain_key:
        recipe = next((r for r in load_recipes() if r["key"] == chain_key), None)
        if recipe is None:
            raise ValueError(f"unknown recipe: {chain_key}; choose one of {[r['key'] for r in load_recipes()]}")
        for s in recipe["steps"]:
            steps.append(PathStep(engine_key=s["engine_key"], depth=s.get("depth", "surface")))
    for s in req.steps or []:
        steps.append(PathStep(engine_key=s.engine_key, depth=s.depth or "surface"))
    if not steps:
        raise ValueError("path.steps is empty and no recipe was named")
    unknown = [s.engine_key for s in steps if s.engine_key not in by_key]
    if unknown:
        raise ValueError(f"path names non-executable engines: {unknown}")
    if len(steps) > 4:
        raise ValueError("a path has at most 4 steps")
    steps = validate_steps(steps, by_key)
    for s in steps:
        s.plain_name = plain_name_for(s.engine_key, audience, by_key)
    depth = req.depth if req.depth in DEPTHS else path_depth_from_steps(steps, by_key)
    return Path(steps=steps, depth=depth, chain_key=chain_key)
