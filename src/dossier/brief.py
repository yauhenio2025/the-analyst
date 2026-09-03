"""Step 2 — the brief: exactly three angles (tellings) the dossier could take, with engines, cost and shape.

Sonnet proposes; code re-computes the cost/time estimates from pass counts and
the corpus size (arithmetic, not judgment) and validates engine keys against
the executable catalog.
"""
from __future__ import annotations

import logging

from src.dossier import events
from src.dossier.common import (AUDIENCE_REGISTER, DEPTH_POLICY, catalog_text, compact_profiles,
                                engine_catalog, estimate_engine_run, passes_for)
from src.dossier.llm import call_json
from src.dossier.schemas import Brief, BriefDefaults, BriefOption, DossierJob, EngineChoice
from src.sources.schemas import Document

logger = logging.getLogger(__name__)

STEP = "brief"

OPTION_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["key", "title", "telling", "engines", "output_shape"],
    "properties": {
        "key": {"type": "string", "description": "short snake_case key, e.g. legitimation_narratives"},
        "title": {"type": "string", "description": "the angle as a title, <= 10 words"},
        "telling": {"type": "string", "description": "one paragraph: what this dossier would say, and what the reader learns that they could act on"},
        "engines": {"type": "array", "minItems": 1, "maxItems": 4,
                    "items": {"type": "object", "additionalProperties": False, "required": ["engine_key", "why"],
                              "properties": {"engine_key": {"type": "string"}, "why": {"type": "string"}}},
                    "description": "executable engines in the order they would run, first = most important"},
        "output_shape": {"type": "object", "additionalProperties": False, "required": ["sections", "tables", "figures"],
                         "properties": {"sections": {"type": "array", "items": {"type": "string"}, "description": "3-6 section headings"},
                                        "tables": {"type": "array", "items": {"type": "string"}, "description": "2-3 table captions"},
                                        "figures": {"type": "array", "items": {"type": "string"}, "description": "1-3 figure ideas (depictable scenes)"}}},
    },
}
BRIEF_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["options", "defaults"],
    "properties": {
        "options": {"type": "array", "minItems": 3, "maxItems": 3, "items": OPTION_SCHEMA},
        "defaults": {"type": "object", "additionalProperties": False, "required": ["audience", "depth", "figures"],
                     "properties": {"audience": {"type": "string", "enum": ["executive", "researcher", "analyst"]},
                                    "depth": {"type": "string", "enum": ["simple", "medium", "advanced"]},
                                    "figures": {"type": "integer", "minimum": 0, "maximum": 4}}},
    },
}

SYSTEM = """You are the brief desk of The Analyst. Given reconnaissance over a corpus, you propose exactly THREE distinct angles
(tellings) a dossier could take — three genuinely different readings, not three phrasings of one. Each angle names the
executable analysis engines that would produce it (from the catalog only, in run order) and says why each engine earns
its place. Each angle also declares its output shape: section headings, 2-3 tables, 1-3 figures (depictable scenes, no text).
Write for the stated audience. Be concrete: name the documents and the tensions the angle exploits."""


def _validate_engines(engines: list[EngineChoice], valid: set[str]) -> list[EngineChoice]:
    out, seen = [], set()
    for e in engines:
        if e.engine_key in valid and e.engine_key not in seen:
            out.append(e)
            seen.add(e.engine_key)
    return out


def estimate_option(option: BriefOption, depth: str, corpus_chars: int, catalog_by_key: dict) -> BriefOption:
    policy = DEPTH_POLICY.get(depth, DEPTH_POLICY["simple"])
    engines = option.engines[: policy["max_engines"]]
    passes = 0
    for e in engines:
        passes += passes_for(catalog_by_key.get(e.engine_key, {}), policy["engine_depth"])
    passes = max(1, min(passes, policy["max_passes"]))
    engine_cost, engine_min = estimate_engine_run(corpus_chars, passes)
    # the dossier's own calls: reconnaissance (done), brief (done), plan, tables, sections, figure plan
    own_cost, own_min = estimate_engine_run(corpus_chars, 3)
    option.est_llm_calls = passes + 4
    option.est_cost_usd = round(engine_cost + own_cost, 2)
    option.est_minutes = round(engine_min + own_min + 2, 1)
    return option


def run_brief(job: DossierJob, docs: list[Document]) -> Brief:
    catalog = engine_catalog()
    valid = {e["engine_key"] for e in catalog}
    by_key = {e["engine_key"]: e for e in catalog}
    corpus_chars = sum(d.char_count for d in docs)
    audience = job.options.audience
    depth = job.options.depth

    user = (
        f"AUDIENCE: {audience} — {AUDIENCE_REGISTER.get(audience, '')}\n"
        f"REQUESTED DEPTH: {depth} ({DEPTH_POLICY[depth]['min_engines']}-{DEPTH_POLICY[depth]['max_engines']} engines)\n"
        + (f"REQUESTER'S INTENT: {job.options.intent}\n" if job.options.intent else "")
        + f"CORPUS: {len(docs)} documents, {corpus_chars:,} characters.\n\n"
        f"RECONNAISSANCE:\n{compact_profiles(job.profiles)}\n\n"
        f"EXECUTABLE ENGINES (choose only from these keys):\n{catalog_text(catalog)}\n\n"
        "Propose exactly three options. For `defaults`, recommend the audience, depth and number of figures that fit this corpus and intent."
    )
    brief, _ = call_json(
        job.id, STEP, label="brief: three angles", system=SYSTEM, user=user,
        tool_name="propose_brief", schema=BRIEF_SCHEMA, model_cls=Brief, max_tokens=8000,
    )

    options = []
    for i, opt in enumerate(brief.options[:3], start=1):
        opt.engines = _validate_engines(opt.engines, valid)
        if not opt.engines:
            opt.engines = [EngineChoice(engine_key="deep_summarization", why="fallback: no valid engine was named")]
        opt.key = (opt.key or f"option_{i}").strip().lower().replace(" ", "_")[:40]
        options.append(estimate_option(opt, depth, corpus_chars, by_key))
    while len(options) < 3:  # the schema asked for three; keep the contract even if the model fell short
        options.append(estimate_option(BriefOption(
            key=f"option_{len(options)+1}", title="Straight synthesis", telling="A plain synthesis of what the documents argue.",
            engines=[EngineChoice(engine_key="deep_summarization", why="reads every argument closely")]), depth, corpus_chars, by_key))
    defaults = brief.defaults or BriefDefaults()
    # the requester's explicit choices win over the model's recommendation
    defaults.audience = job.options.audience or defaults.audience
    defaults.depth = job.options.depth or defaults.depth
    defaults.figures = job.options.output.figures if job.options.output else defaults.figures
    out = Brief(options=options, defaults=defaults)
    events.emit(job.id, "artifact", phase=STEP, detail="brief: " + " / ".join(o.title for o in options),
                payload_json={"kind": "brief", "options": [{"key": o.key, "title": o.title, "engines": [e.engine_key for e in o.engines],
                                                            "est_cost_usd": o.est_cost_usd, "est_minutes": o.est_minutes} for o in options]})
    return out
