"""Step 3 — plan: a WorkflowExecutionPlan for the executor, restricted to executable engines.

Sonnet picks the phases (from the executable catalog, guided by the chosen
angle); code enforces the depth policy (engine count, pass budget), validates
keys, and writes the executor plan file. `strategy_rationale` and
`alternatives_considered` are recorded on the dossier job.
"""
from __future__ import annotations

import logging
from typing import Optional

from src.dossier import events
from src.dossier.common import (DEPTH_POLICY, SYNTHESIS_ENGINES, catalog_text, compact_profiles, corpus_title,
                                engine_catalog, estimate_engine_run, passes_for)
from src.dossier.llm import call_json
from src.dossier.schemas import BriefOption, DossierJob, DossierPlan, DossierPlanPhase, Path
from src.sources.schemas import Document

logger = logging.getLogger(__name__)

STEP = "plan"
ANALYSIS_PHASE_BASE = 4  # analysis phases are numbered 4.1, 4.2, … under dossier_standard phase 4

PLAN_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["phases", "strategy_rationale", "alternatives_considered"],
    "properties": {
        "phases": {"type": "array", "minItems": 1, "maxItems": 4,
                   "items": {"type": "object", "additionalProperties": False,
                             "required": ["engine_key", "depth", "why", "context_emphasis"],
                             "properties": {"engine_key": {"type": "string"},
                                            "depth": {"type": "string", "enum": ["surface", "standard", "deep"]},
                                            "why": {"type": "string"},
                                            "context_emphasis": {"type": "string", "description": "one or two sentences telling this engine what the angle needs from it and what the previous phase established"}}}},
        "strategy_rationale": {"type": "string", "description": "2-4 sentences: why this sequence, what each phase feeds the next"},
        "alternatives_considered": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                                                               "required": ["engine_key", "why_not"],
                                                               "properties": {"engine_key": {"type": "string"}, "why_not": {"type": "string"}}}},
    },
}

SYSTEM = """You are the methodologist of The Analyst. You turn a chosen angle into an ordered sequence of analysis engines
for the executor. Each phase runs one engine over the full corpus; every later phase receives the earlier phases' prose as
'Prior Analysis Context', so order matters: earlier phases should establish what later phases build on. Use only engines
from the catalog. Respect the depth policy exactly. Say why each engine, and what you considered and rejected."""


def chosen_option(job: DossierJob) -> Optional[BriefOption]:
    if not job.brief:
        return None
    for o in job.brief.options:
        if o.key == job.chosen_option:
            return o
    return job.brief.options[0] if job.brief.options else None


def _enforce_policy(phases: list[DossierPlanPhase], depth: str, by_key: dict, fallback_engines: list[str]) -> list[DossierPlanPhase]:
    policy = DEPTH_POLICY.get(depth, DEPTH_POLICY["simple"])
    valid = [p for p in phases if p.engine_key in by_key]
    seen, uniq = set(), []
    for p in valid:
        if p.engine_key not in seen:
            uniq.append(p)
            seen.add(p.engine_key)
    for key in fallback_engines:  # top up from the brief's own engine choice when the planner fell short
        if len(uniq) >= policy["min_engines"]:
            break
        if key in by_key and key not in seen:
            uniq.append(DossierPlanPhase(phase_number=0, engine_key=key, why="from the chosen brief option", context_emphasis=""))
            seen.add(key)
    if not uniq:
        uniq = [DossierPlanPhase(phase_number=0, engine_key="deep_summarization", why="fallback: no valid engine chosen", context_emphasis="")]
    uniq = uniq[: policy["max_engines"]]
    if policy["synthesis"] and uniq[-1].engine_key not in SYNTHESIS_ENGINES and len(uniq) < policy["max_engines"]:
        uniq.append(DossierPlanPhase(phase_number=0, engine_key="deep_summarization", depth="standard",
                                     why="synthesis pass across the prior phases (advanced depth policy)",
                                     context_emphasis="Synthesize the prior phases into one argument; do not repeat them."))
    # pass budget: cap depths so the total pass count stays within policy
    for p in uniq:
        if depth != "advanced":
            p.depth = policy["engine_depth"]
        elif p.depth == "deep":
            p.depth = "standard"
    budget = policy["max_passes"]
    while sum(passes_for(by_key.get(p.engine_key, {}), p.depth) for p in uniq) > budget:
        downgraded = False
        for p in reversed(uniq):
            if p.depth != "surface":
                p.depth = "surface"
                downgraded = True
                break
        if not downgraded:
            uniq = uniq[:-1]
    for i, p in enumerate(uniq, start=1):
        p.phase_number = round(ANALYSIS_PHASE_BASE + i / 10, 1)
        p.passes = passes_for(by_key.get(p.engine_key, {}), p.depth)
        p.engine_name = by_key.get(p.engine_key, {}).get("engine_name", p.engine_key)
    return uniq


def fixed_path(job: DossierJob, option: Optional[BriefOption], by_key: dict) -> Optional[Path]:
    """The path the plan must honour exactly, or None for the legacy planner.

    Lane 2 (`entry == "chosen"`): the requester's own path on the job options. Otherwise a v2 brief
    option carries its own priced path (DESIGN_brief_deliverables §B2) — the card promised those steps
    at that price, so the planner keeps them and writes only context_emphasis + rationale.
    """
    from src.dossier.catalog import resolve_path_request

    if job.options.entry == "chosen" and job.options.path:
        try:
            return resolve_path_request(job.options.path, job.options.audience, by_key)
        except ValueError as exc:
            logger.warning(f"fixed path rejected ({exc}); falling back to the option's path")
    if option is not None and option.version >= 2 and option.path.steps:
        return option.path
    return None


def fixed_phases(path: Path, proposed: list[DossierPlanPhase], by_key: dict) -> list[DossierPlanPhase]:
    """Exactly the fixed steps, in order, at their depths; context_emphasis/why taken from the model's matching phase."""
    out = []
    for i, s in enumerate(path.steps, start=1):
        if s.engine_key not in by_key:
            continue
        match = next((p for p in proposed if p.engine_key == s.engine_key and p not in out), None)
        ph = DossierPlanPhase(
            phase_number=round(ANALYSIS_PHASE_BASE + len(out) / 10 + 0.1, 1), engine_key=s.engine_key,
            engine_name=by_key[s.engine_key].get("engine_name", s.engine_key),
            depth=s.depth if s.depth in ("surface", "standard", "deep") else "surface",
            why=(match.why if match and match.why else (s.contributes or "from the chosen deliverable's path")),
            context_emphasis=(match.context_emphasis if match else ""),
        )
        ph.passes = passes_for(by_key[s.engine_key], ph.depth)
        out.append(ph)
    if not out:
        out = [DossierPlanPhase(phase_number=round(ANALYSIS_PHASE_BASE + 0.1, 1), engine_key="deep_summarization",
                                engine_name=by_key.get("deep_summarization", {}).get("engine_name", "deep_summarization"),
                                why="fallback: the fixed path named no executable engine", context_emphasis="", passes=1)]
    return out


def build_executor_plan(job: DossierJob, docs: list[Document], plan: DossierPlan, option: Optional[BriefOption]):
    from src.orchestrator.planner import _save_plan
    from src.orchestrator.schemas import PhaseExecutionSpec, TargetWork, WorkflowExecutionPlan

    title = corpus_title(docs, job.options.intent)
    description = (option.telling if option else "Dossier over the supplied documents")[:900]
    phases = []
    prev: Optional[float] = None
    for p in plan.phases:
        phases.append(PhaseExecutionSpec(
            phase_number=p.phase_number, phase_name=p.engine_name or p.engine_key,
            depth=p.depth, engine_key=p.engine_key, iteration_mode="single",
            depends_on=[prev] if prev is not None else [],
            context_emphasis=p.context_emphasis or None, rationale=p.why,
            model_hint="sonnet", requires_full_documents=sum(d.char_count for d in docs) > 600_000,
            estimated_cost_usd=estimate_engine_run(sum(d.char_count for d in docs), p.passes)[0],
        ))
        prev = p.phase_number
    exec_plan = WorkflowExecutionPlan(
        workflow_key="dossier_standard",
        thinker_name=title[:80],
        target_work=TargetWork(title=title, description=description),
        prior_works=[],
        research_question=(option.title if option else job.options.intent) or None,
        strategy_summary=plan.strategy_rationale,
        phases=phases,
        estimated_llm_calls=sum(p.passes for p in plan.phases),
        estimated_depth_profile=", ".join(f"{p.engine_key}@{p.depth}" for p in plan.phases),
        estimated_total_cost_usd=plan.estimated_cost_usd,
        status="approved",
        model_used="dossier.plan (claude-sonnet-4-6 selection, code-enforced depth policy)",
        objective_key="dossier",
    )
    exec_plan.__dict__["_skip_plan_revision"] = True
    _save_plan(exec_plan)
    return exec_plan


def run_plan(job: DossierJob, docs: list[Document]) -> DossierPlan:
    catalog = engine_catalog()
    by_key = {e["engine_key"]: e for e in catalog}
    option = chosen_option(job)
    depth = job.options.depth
    policy = DEPTH_POLICY.get(depth, DEPTH_POLICY["simple"])
    corpus_chars = sum(d.char_count for d in docs)

    option_text = "(no brief option — plan from the intent)"
    if option:
        option_text = (f"{option.title}\n{option.telling}\nEngines the brief suggested: "
                       + ", ".join(f"{e.engine_key} ({e.why})" for e in option.engines))
    fixed = fixed_path(job, option, by_key)
    if fixed is not None:
        depth = fixed.depth
        fixed_text = " → ".join(f"{s.engine_key}@{s.depth}" for s in fixed.steps)
        depth_rule = (f"THE PATH IS FIXED: {fixed_text}. Return exactly these phases in this order with these depths — "
                      "do not add, drop, reorder or re-depth any of them. Your job is the context_emphasis of each phase, "
                      "the strategy rationale, and the alternatives you would have considered.")
    else:
        depth_rule = {
            "simple": "exactly ONE engine at depth 'surface' (one pass).",
            "medium": "TWO or THREE engines, each at depth 'surface', chained so each builds on the previous.",
            "advanced": "THREE or FOUR engines at depth 'standard'; the LAST phase must be a synthesis engine "
                        f"(one of {', '.join(SYNTHESIS_ENGINES)}) that integrates the prior phases.",
        }[depth]
    user = (
        f"CHOSEN ANGLE:\n{option_text}\n\nDEPTH POLICY ({depth}): {depth_rule}\n"
        f"AUDIENCE: {job.options.audience}\nCORPUS: {len(docs)} documents, {corpus_chars:,} chars.\n\n"
        f"RECONNAISSANCE (abridged):\n{compact_profiles(job.profiles)[:12000]}\n\n"
        f"EXECUTABLE ENGINES:\n{catalog_text(catalog, with_problematique=True)}\n\n"
        "Return the phases in run order with a context_emphasis for each, the strategy rationale, and 2-5 alternatives you rejected."
    )
    raw, _ = call_json(job.id, STEP, label=f"plan: {'fixed path' if fixed else depth + ' depth'} over the executable catalog", system=SYSTEM, user=user,
                       tool_name="record_plan", schema=PLAN_SCHEMA, model_cls=None, max_tokens=6000)
    raw = raw or {}
    phases = []
    for ph in raw.get("phases", []):
        try:
            phases.append(DossierPlanPhase(phase_number=0, engine_key=str(ph.get("engine_key", "")).strip(),
                                           depth=str(ph.get("depth", policy["engine_depth"])), why=str(ph.get("why", "")),
                                           context_emphasis=str(ph.get("context_emphasis", ""))))
        except Exception as exc:
            logger.warning(f"plan phase rejected: {exc}")
    rejected_unknown = [p.engine_key for p in phases if p.engine_key not in by_key]
    if fixed is not None:
        phases = fixed_phases(fixed, phases, by_key)
    else:
        fallback = [e.engine_key for e in option.engines] if option else []
        phases = _enforce_policy(phases, depth, by_key, fallback)
    total_passes = sum(p.passes for p in phases)
    cost, minutes = estimate_engine_run(corpus_chars, total_passes)
    plan = DossierPlan(
        phases=phases,
        strategy_rationale=str(raw.get("strategy_rationale", "")),
        alternatives_considered=[{"engine_key": str(a.get("engine_key", "")), "why_not": str(a.get("why_not", ""))}
                                 for a in raw.get("alternatives_considered", []) if isinstance(a, dict)],
        estimated_llm_calls=total_passes, estimated_cost_usd=cost,
    )
    if rejected_unknown:
        events.emit(job.id, "note", phase=STEP, detail=f"planner named non-executable engines, dropped: {rejected_unknown}")
    exec_plan = build_executor_plan(job, docs, plan, option)
    plan.plan_id = exec_plan.plan_id
    events.emit(job.id, "artifact", phase=STEP,
                detail="plan: " + " → ".join(f"{p.engine_key}@{p.depth}" for p in phases) + f" ({total_passes} passes, est ${cost:.2f}, ~{minutes} min)",
                payload_json={"kind": "plan", "plan_id": exec_plan.plan_id,
                              "phases": [p.model_dump() for p in phases],
                              "strategy_rationale": plan.strategy_rationale,
                              "alternatives_considered": plan.alternatives_considered})
    return plan
