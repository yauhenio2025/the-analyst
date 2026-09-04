"""The story desk's steps. Each is one or more recorded LLM calls plus code that holds shape only."""
from __future__ import annotations

import hashlib
import logging
from typing import Any

from src.dossier import events
from src.dossier.llm import call_json, schema_of
from src.dossier.walls import NormalizedCorpus, verify_anchor
from src.sources.schemas import Document

from . import prompts
from .doctrine import doctrine
from .schemas import (APPROACHES, ApproachRank, ApproachSlate, HandoffSource, StoryBrief, StoryElement, StoryHandoff,
                      StoryJob, StoryMap, StoryProfile, StorySpine, ThroughLine)

logger = logging.getLogger(__name__)
PER_DOC_MAX_CHARS = 700_000
STEP = {"recon": "reconnaissance", "map": "map", "approaches": "approaches", "brief": "brief", "spine": "spine", "handoff": "handoff"}


def _doc_header(d: Document) -> str:
    return f"doc_key: {d.key}\ntitle: {d.title}\ncreators: {d.creators}\nyear: {d.year}\npublication: {d.publication}\nchars: {d.char_count}"


# ── 1. story reconnaissance, one call per document ───────────────────────────
def run_reconnaissance(job: StoryJob, docs: list[Document]) -> list[StoryProfile]:
    system = prompts.reconnaissance_system()
    schema = schema_of(StoryProfile)
    profiles: list[StoryProfile] = []
    intent = job.options.intent or ""
    for i, doc in enumerate(docs, start=1):
        text = doc.text[:PER_DOC_MAX_CHARS]
        user = (f"INTENT (what the operator wants the film to do, if stated): {intent or 'not stated'}\n\n"
                f"SOURCE {i} of {len(docs)}\n{_doc_header(doc)}\n\n===== BEGIN SOURCE =====\n{text}\n===== END SOURCE =====")
        events.emit(job.id, "note", phase=STEP["recon"], detail=f"reading {doc.key}: {doc.title[:80]} ({doc.char_count:,} chars) against the registry's demands")
        profile, _ = call_json(job.id, STEP["recon"], label=f"story read {doc.key}", system=system, user=user,
                               tool_name="record_story_profile", schema=schema, model_cls=StoryProfile, max_tokens=16000)
        profile.doc_key = doc.key
        profile.title = profile.title or doc.title
        # the anchor wall: every element must quote its source
        corpus = NormalizedCorpus({doc.key: doc.text})
        kept: list[StoryElement] = []
        counters: dict[str, int] = {}
        for el in profile.elements:
            el.anchor.doc_key = doc.key
            a = verify_anchor(el.anchor, corpus)
            if a is None:
                continue
            n = counters.get(el.kind, 0) + 1
            counters[el.kind] = n
            kept.append(el.model_copy(update={"anchor": a, "id": f"{doc.key}:{el.kind}:{n}"}))
        dropped = len(profile.elements) - len(kept)
        profile.elements = kept
        profile.elements_dropped = dropped
        profiles.append(profile)
        by_kind = ", ".join(f"{k} {v}" for k, v in sorted(counters.items()))
        events.emit(job.id, "artifact", phase=STEP["recon"], detail=f"{doc.key}: {len(kept)} anchored elements ({by_kind}); wall dropped {dropped}",
                    payload_json={"kind": "story_profile", "doc_key": doc.key, "elements": len(kept), "dropped": dropped, "gaps": profile.gaps})
    return profiles


def compact_profiles(profiles: list[StoryProfile], max_elements_per_doc: int = 80) -> str:
    out = []
    for p in profiles:
        out.append(f"### {p.doc_key} — {p.title}\ngenre: {p.genre}\none line: {p.one_line}\nquestion: {p.question}\nstance: {p.stance}\ngaps: {'; '.join(p.gaps) or 'none stated'}\nelements:")
        for el in p.elements[:max_elements_per_doc]:
            det = "; ".join(f"{k}={v}" for k, v in el.detail.items() if v)
            out.append(f"- [{el.id}] ({el.kind}, i{el.intensity}) {el.text}" + (f" — {det}" if det else "") + f' — "{el.anchor.quote[:120]}"')
    return "\n".join(out)


# ── 2. story map across profiles ─────────────────────────────────────────────
def run_map(job: StoryJob) -> StoryMap:
    user = (f"INTENT: {job.options.intent or 'not stated'}\nAUDIENCE: {job.options.audience}\n\nSTORY PROFILES OF {len(job.profiles)} SOURCES\n\n"
            + compact_profiles(job.profiles))
    smap, _ = call_json(job.id, STEP["map"], label="story map", system=prompts.map_system(), user=user,
                        tool_name="record_story_map", schema=schema_of(StoryMap), model_cls=StoryMap, max_tokens=16000)
    valid_ids = {el.id for p in job.profiles for el in p.elements}
    doc_keys = [p.doc_key for p in job.profiles]
    for tl in smap.through_lines:
        tl.element_ids = [e for e in tl.element_ids if e in valid_ids]
        tl.carried_by = [d for d in tl.carried_by if d in doc_keys]
        tl.not_carried_by = [d for d in doc_keys if d not in tl.carried_by]
        tl.single_source = len(tl.carried_by) < 2
    # coverage matrix: arithmetic over the model's judgment
    smap.coverage = {tl.key: {d: (d in tl.carried_by) for d in doc_keys} for tl in smap.through_lines}
    events.emit(job.id, "artifact", phase=STEP["map"], detail=f"{len(smap.through_lines)} through-lines, {len(smap.recurrences)} recurrences, {len(smap.contradictions)} contradictions",
                payload_json={"kind": "story_map", "through_lines": [{"key": t.key, "title": t.title, "carried_by": t.carried_by, "single_source": t.single_source} for t in smap.through_lines]})
    return smap


def _map_text(smap: StoryMap) -> str:
    lines = ["THROUGH-LINES:"]
    for t in smap.through_lines:
        lines.append(f"- {t.key}: {t.title}\n  question: {t.question}\n  face: {t.face_on_the_stake}\n  value turn: {t.value_turn.value}: {t.value_turn.before} → {t.value_turn.after} (by {t.value_turn.turned_by})\n  antagonism: {t.antagonism}\n  open loop: {t.open_loop}\n  verdict possible: {t.verdict_possible}\n  carried by: {', '.join(t.carried_by)}; not: {', '.join(t.not_carried_by)}\n  why: {t.why}")
    lines.append("\nRECURRENCES:")
    lines += [f"- {r.what} ({r.kind}) in {', '.join(r.doc_keys)}" for r in smap.recurrences]
    lines.append("\nCONTRADICTIONS:")
    lines += [f"- {c.about} [{c.usable_as}]: " + " | ".join(f"{p.doc_key}: {p.says}" for p in c.positions) for c in smap.contradictions]
    if smap.timeline:
        lines.append("\nTIMELINE:")
        lines += [f"- {t.when}: {t.what} ({', '.join(t.doc_keys)})" for t in smap.timeline]
    return "\n".join(lines)


# ── 3. approach slate ────────────────────────────────────────────────────────
def run_approaches(job: StoryJob) -> ApproachSlate:
    user = f"INTENT: {job.options.intent or 'not stated'}\nAUDIENCE: {job.options.audience}\n\nSTORY MAP\n{_map_text(job.map)}"
    slate, _ = call_json(job.id, STEP["approaches"], label="approach slate", system=prompts.approaches_system(), user=user,
                         tool_name="record_approach_slate", schema=schema_of(ApproachSlate), model_cls=ApproachSlate, max_tokens=8000)
    slate.ranked = [r for r in slate.ranked if r.key in APPROACHES]
    slate.ranked.sort(key=lambda r: r.rank or 99)
    for i, r in enumerate(slate.ranked, start=1):
        r.rank = i
    events.emit(job.id, "artifact", phase=STEP["approaches"], detail="approaches ranked: " + ", ".join(f"{r.rank}. {r.key}" for r in slate.ranked[:4]),
                payload_json={"kind": "approach_slate", "top": [r.model_dump() for r in slate.ranked[:3]]})
    return slate


# ── 4. deliverable-first brief ───────────────────────────────────────────────
def run_brief(job: StoryJob) -> StoryBrief:
    top = "\n".join(f"- {r.rank}. {r.key}: {r.why} (carried by {', '.join(r.carried_by)}; must cut: {r.must_cut})" for r in (job.approaches.ranked if job.approaches else [])[:6])
    length = f"requested length: {job.options.length_seconds}s" if job.options.length_seconds else "length: choose per option (45-240s)"
    user = (f"INTENT: {job.options.intent or 'not stated'}\nAUDIENCE: {job.options.audience}\n{length}\n\nSTORY MAP\n{_map_text(job.map)}\n\nAPPROACHES RANKED\n{top}\n\n"
            "Indicative cost rule for est_cost_usd: 3 + 0.6 per 10 seconds of film; est_minutes: 4 + length_seconds / 20.")
    brief, _ = call_json(job.id, STEP["brief"], label="story brief", system=prompts.brief_system(), user=user,
                         tool_name="record_story_brief", schema=schema_of(StoryBrief), model_cls=StoryBrief, max_tokens=8000)
    keys = {t.key for t in job.map.through_lines} if job.map else set()
    doc_keys = [p.doc_key for p in job.profiles]
    for o in brief.options:
        if o.through_line_key not in keys and keys:
            o.through_line_key = next(iter(keys))
        if o.approach_key not in APPROACHES and job.approaches and job.approaches.ranked:
            o.approach_key = job.approaches.ranked[0].key
        o.sources_used = [d for d in o.sources_used if d in doc_keys]
        o.sources_left_out = [d for d in doc_keys if d not in o.sources_used]
    if brief.recommendation not in {o.key for o in brief.options} and brief.options:
        brief.recommendation = brief.options[0].key
    events.emit(job.id, "artifact", phase=STEP["brief"], detail=f"{len(brief.options)} options; recommended {brief.recommendation}",
                payload_json={"kind": "story_brief", "options": [{"key": o.key, "title": o.title, "length_seconds": o.length_seconds, "through_line_key": o.through_line_key, "approach_key": o.approach_key} for o in brief.options]})
    return brief


# ── 5. spine with tributaries ────────────────────────────────────────────────
def run_spine(job: StoryJob) -> StorySpine:
    option = next((o for o in job.brief.options if o.key == job.chosen_option), None) if job.brief else None
    tl = next((t for t in job.map.through_lines if option and t.key == option.through_line_key), None) if job.map else None
    if option is None or tl is None:
        raise RuntimeError("spine needs a chosen option and its through-line")
    used = set(option.sources_used) or set(tl.carried_by)
    ledger = [p for p in job.profiles if p.doc_key in used]
    user = (f"INTENT: {job.options.intent or 'not stated'}\nAUDIENCE: {job.options.audience}\n\nCHOSEN OPTION\n{option.model_dump_json(indent=1)}\n\n"
            f"THROUGH-LINE\n{tl.model_dump_json(indent=1)}\n\nLEDGER (only these sources; cite element ids)\n{compact_profiles(ledger)}")
    spine, _ = call_json(job.id, STEP["spine"], label="story spine", system=prompts.spine_system(), user=user,
                         tool_name="record_story_spine", schema=schema_of(StorySpine), model_cls=StorySpine, max_tokens=12000)
    valid_ids = {el.id for p in ledger for el in p.elements}
    for m in spine.movements:
        m.element_ids = [e for e in m.element_ids if e in valid_ids]
        m.sources = [d for d in m.sources if d in used]
        m.entry_of = [d for d in m.entry_of if d in used]
    spine.motif.element_ids = [e for e in spine.motif.element_ids if e in valid_ids]
    if spine.hook.element_id not in valid_ids:
        strongest = max((el for p in ledger for el in p.elements), key=lambda e: e.intensity, default=None)
        spine.hook.element_id = strongest.id if strongest else ""
    spine.through_line_key = tl.key
    spine.approach_key = spine.approach_key or option.approach_key
    spine.length_seconds = spine.length_seconds or option.length_seconds
    events.emit(job.id, "artifact", phase=STEP["spine"], detail=f"spine: {len(spine.movements)} movements over {len(used)} sources; motif '{spine.motif.what[:60]}'",
                payload_json={"kind": "story_spine", "movements": [{"n": m.n, "title": m.title, "sources": m.sources} for m in spine.movements]})
    return spine


# ── 6. handoff document ──────────────────────────────────────────────────────
def build_handoff(job: StoryJob, docs: list[Document]) -> StoryHandoff:
    option = next((o for o in job.brief.options if o.key == job.chosen_option), None) if job.brief else None
    tl = next((t for t in job.map.through_lines if t.key == job.spine.through_line_key), None) if (job.map and job.spine) else None
    if option is None or tl is None or job.spine is None:
        raise RuntimeError("handoff needs the brief choice, the through-line and the spine")
    used = set(option.sources_used) or set(tl.carried_by)
    ledger = [el for p in job.profiles if p.doc_key in used for el in p.elements]
    sources = []
    for d in docs:
        if d.key not in used:
            continue
        sources.append(HandoffSource(doc_key=d.key, title=d.title, creators=d.creators, year=d.year, publication=d.publication,
                                     chars=d.char_count, sha256=hashlib.sha256(d.text.encode("utf-8")).hexdigest(),
                                     text_url=f"/v1/story/jobs/{job.id}/sources/{d.key}"))
    approach = next((r for r in job.approaches.ranked if r.key == job.spine.approach_key), None) if job.approaches else None
    doctrines: dict[str, str] = {}
    for key, name in (("wirecut_spine", "spine_doctrine.md"), ("wirecut_telling_desk", "telling_desk.md"),
                      ("wirecut_narrative_approaches", "narrative_doctrine.md"), ("wirecut_narrative_approaches", "approach_suggest.md")):
        _, sha = doctrine(key, name)
        if sha:
            doctrines[f"{key}/{name}"] = sha
    handoff = StoryHandoff(story_job_id=job.id, intent=job.options.intent or "", audience=job.options.audience, through_line=tl,
                           approach=approach, spine=job.spine, ledger=ledger, sources=sources,
                           coverage={d.key: (d.key in tl.carried_by) for d in docs}, doctrines=doctrines,
                           totals=job.totals.model_dump())
    events.emit(job.id, "artifact", phase=STEP["handoff"], detail=f"handoff ready: {len(sources)} sources, {len(ledger)} anchored elements, {len(job.spine.movements)} movements",
                payload_json={"kind": "story_handoff", "url": f"/v1/story/jobs/{job.id}/handoff"})
    return handoff
