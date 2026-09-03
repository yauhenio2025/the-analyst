"""Pass S — THE SPINE: what the dossier argues, before a word of it is written.

One call (Sonnet, forced tool). The answer opens with de-llm's composition read
(plain summary, buried crux, readers and their mode, strands, what should be a
table / a picture / prose) and then declares the spine: a thesis; sections with
ONE claim each; per section the table spec and/or figure spec that claim needs;
the anchors it will lean on; the jobs of the summary and the conclusion (which
must differ). Every later desk consumes it: tables and figures build exactly
what it commissioned, the writer proves exactly its claims in its order, the
cross-check judges the finished dossier against its words.

Walls (shape only): 3-7 sections, unique snake_case keys, one-sentence claims,
exhibits within budget, no digits in captions, anchors verbatim (a trimmed
fragment does not count), feeds name real keys, summary job != conclusion job.
Retry: FIELD patches — only the failing sections are re-asked, merged, the whole
re-validated (Wirecut's `_spine_patch_trio`). What still fails after the patch
is repaired by code where the repair is shape trivia (a second sentence cut, an
over-budget exhibit dropped) and recorded in `spine.notes`.

Skip law: a spine that cannot be built records `spine_unavailable`; the run
continues on the legacy paths (tables/figures planned from the prose, one-call
compose) with the fact on the record.
"""
from __future__ import annotations

import logging
import re
from typing import Any, Optional

from src.dossier import events
from src.dossier.common import AUDIENCE_REGISTER, analysis_prose, compact_profiles
from src.dossier.llm import call_json
from src.dossier.schemas import (
    EVIDENCE_KINDS, Anchor, CompositionRead, DossierJob, DossierSpine, ExhibitsBudget,
    SpineFigureSpec, SpineSection, SpineTableSpec,
)
from src.dossier.walls import NormalizedCorpus, has_digit_run, is_one_sentence, normalize, sentence_count, verify_anchor
from src.sources.schemas import Document

logger = logging.getLogger(__name__)

STEP = "spine"
MIN_SECTIONS, MAX_SECTIONS = 3, 7
MIN_ANCHORS, MAX_ANCHORS = 1, 4
MAX_TABLES_DEFAULT = 3
ANALYSIS_CHARS_PER_PHASE = 60_000

# ── Tool schema ───────────────────────────────────────────────────────────

ANCHOR_SCHEMA = {"type": "object", "required": ["doc_key", "quote"], "additionalProperties": False,
                 "properties": {"doc_key": {"type": "string"}, "quote": {"type": "string", "description": "verbatim, 40-200 chars, copied from a PROFILE anchor or exactly from the document"}}}
TABLE_SPEC_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["intent", "row_unit", "columns", "carries_claims"],
    "properties": {
        "intent": {"type": "string", "description": "what rows × columns would PROVE the claim"},
        "row_unit": {"type": "string", "description": "one row = one case / one term / one actor / one practice"},
        "columns": {"type": "array", "minItems": 2, "maxItems": 6, "items": {"type": "string"}},
        "carries_claims": {"type": "array", "minItems": 1, "maxItems": 5, "items": {"type": "string"},
                           "description": "the claims the rows must carry, in the reader's words"},
    },
}
FIGURE_SPEC_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["primitive", "visual_format", "picture_shows", "caption_says", "why_a_picture"],
    "properties": {
        "primitive": {"type": "string", "description": "the analytical primitive the section exhibits (from PRIMITIVES)"},
        "visual_format": {"type": "string", "description": "a format key the primitive prefers (from PRIMITIVES)"},
        "picture_shows": {"type": "string", "description": "the STRUCTURE the diagram makes visible — which named things, in what relation, <= 300 chars"},
        "caption_says": {"type": "string", "description": "<= 2 sentences: what the reader takes from the picture. NO digits — numbers live in prose and tables"},
        "why_a_picture": {"type": "string", "description": "why prose and a table cannot do this job"},
    },
}
SECTION_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["key", "heading", "claim", "reader_needs_next", "evidence_kind", "table", "figure", "anchors_planned", "feeds"],
    "properties": {
        "key": {"type": "string", "description": "snake_case, unique"},
        "heading": {"type": "string", "description": "<= 70 chars, in the audience's register"},
        "claim": {"type": "string", "description": "ONE sentence this section proves — the sentence a reader would repeat"},
        "reader_needs_next": {"type": "string", "description": "what the reader needs right after this claim (the throw-forward)"},
        "evidence_kind": {"type": "string", "enum": list(EVIDENCE_KINDS)},
        "table": {"anyOf": [TABLE_SPEC_SCHEMA, {"type": "null"}], "description": "null unless a row set PROVES the claim"},
        "figure": {"anyOf": [FIGURE_SPEC_SCHEMA, {"type": "null"}], "description": "null unless a picture does a job prose and tables cannot"},
        "anchors_planned": {"type": "array", "minItems": 1, "maxItems": 4, "items": ANCHOR_SCHEMA},
        "feeds": {"type": "array", "items": {"type": "string"}, "description": "keys of LATER sections that build on this one"},
    },
}
READ_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["plain_summary", "buried_crux", "readers", "strands", "prose_to_table", "table_to_prose",
                 "figures_earned", "figures_dropped", "cumulative_direction", "form_capacity"],
    "properties": {
        "plain_summary": {"type": "string", "description": "at most four sentences: subject, finding, what the reader should do"},
        "buried_crux": {"type": "string", "description": "what the analysis carries but never states plainly — the decision the reader needs, the disagreement between documents, the caveat that changes the finding — and where it hides"},
        "readers": {"type": "array", "minItems": 1, "maxItems": 3, "items": {"type": "object", "additionalProperties": False, "required": ["type", "mode", "wants"],
                    "properties": {"type": {"type": "string"}, "mode": {"type": "string", "description": "reads straight through | consults the summary and one table | scans for the decision"}, "wants": {"type": "string"}}}},
        "strands": {"type": "array", "maxItems": 6, "items": {"type": "object", "additionalProperties": False, "required": ["name", "carried_by", "accidental", "note"],
                    "properties": {"name": {"type": "string"}, "carried_by": {"type": "array", "items": {"type": "string"}}, "accidental": {"type": "boolean"}, "note": {"type": "string"}}}},
        "prose_to_table": {"type": "array", "items": {"type": "string"}, "description": "enumerations the analysis makes in prose that a table shows better (name rows and columns)"},
        "table_to_prose": {"type": "array", "items": {"type": "string"}, "description": "table ideas that are really one claim and should be a sentence"},
        "figures_earned": {"type": "array", "items": {"type": "string"}, "description": "picture ideas that do a job prose cannot"},
        "figures_dropped": {"type": "array", "items": {"type": "string"}, "description": "picture ideas that are decoration, and why"},
        "cumulative_direction": {"type": "string", "description": "which way the evidence pushes the reader; does that match the finding the brief promised; where is the counter-evidence"},
        "form_capacity": {"type": "string", "description": "does this material fill a 3-7 section dossier, or is it two sections and a table"},
    },
}
SPINE_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["read", "thesis", "reader_question", "handle", "through_line", "summary_job", "conclusion_job", "sections"],
    "properties": {
        "read": READ_SCHEMA,
        "thesis": {"type": "string", "description": "ONE sentence — the dossier's claim"},
        "reader_question": {"type": "string", "description": "what this audience needs answered"},
        "handle": {"type": "string", "description": "the dossier in one line a reader can repeat"},
        "through_line": {"type": "string", "description": "the object, case or example that returns across sections"},
        "summary_job": {"type": "string", "description": "one line: what the executive summary does (e.g. the finding and the stakes)"},
        "conclusion_job": {"type": "string", "description": "one line: what the close does — a DIFFERENT job (e.g. the decision rule and the question to ask)"},
        "sections": {"type": "array", "minItems": MIN_SECTIONS, "maxItems": MAX_SECTIONS, "items": SECTION_SCHEMA},
    },
}
PATCH_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["sections"],
                "properties": {"sections": {"type": "array", "minItems": 1, "maxItems": MAX_SECTIONS, "items": SECTION_SCHEMA}}}

SYSTEM = """You are the structure editor of The Analyst. The analysis is done and nothing of the dossier is written. Before a
word is written you decide what the dossier ARGUES and what each part of it needs on the desk to prove its point. Your
answer — the SPINE — is the one artifact every later desk consumes: the tables desk builds exactly the tables you
specify, the figures desk draws exactly the diagrams you specify, the writer proves exactly the claims you name, in
your order, and the cross-check judges the finished dossier against your words. Plan the argument, not the paragraphs.

First, the READ — declared before you plan anything: in plain words, what this dossier says (four sentences at most);
what the analysis carries but never states plainly (the decision the reader actually needs, the disagreement between
the documents, the caveat that changes the finding — and where it hides); who reads it and how (straight through, or
consulting the summary and one table); the strands that run across phases and documents (mark the accidental ones —
the same example used twice by chance); every enumeration the analysis makes in prose that a table would show better,
and every table idea that is really one sentence; which picture ideas earn their place and which are decoration; which
way the evidence pushes the reader, and whether that matches what the brief promised; whether the material fills a
dossier at all.

Then the SPINE:
- One claim per section. A section that proves two things is two sections; a section that proves none is cut. Write
  the claim as the one sentence a reader would repeat. Order sections by the reader's route, never by the order the
  analysis engines happened to run.
- An exhibit is commissioned by a claim, never by a dial. Ask for a table only where a row set PROVES the claim (say
  what one row is, and which claims the rows must carry); ask for a diagram only where a picture does a job prose and
  tables cannot (a structure the reader must SEE: a flow, a grid of positions, a sequence, a hierarchy, a tension) —
  choose the analytical PRIMITIVE the section exhibits and a format that primitive prefers, and say in `picture_shows`
  which named things appear in what relation. The caption is not the argument: `caption_says` tells the reader what to
  take from the picture in at most two sentences and never carries a number — numbers live in the prose and tables.
- The exhibits budget is a ceiling, not a target: fewer, load-bearing exhibits beat the budget filled. At most one
  table and one figure per section.
- Ground everything: every section names 1-4 verified quotes it will lean on, copied character-for-character from the
  PROFILES' anchors (preferred) or from the documents — a mechanical check refuses anything that is not verbatim. A
  claim the documents cannot carry is not planned.
- Write headings and claims in the audience's register. For an executive the last section is the one they act on —
  give it the strongest exhibit, not none.
- The summary and the conclusion do DIFFERENT jobs; declare each in one line (e.g. summary = the finding and the
  stakes; conclusion = the decision rule and the question to ask on Monday). A close that restates the summary is a
  defect.
- The brief's suggested shape is advisory: honor its promises, not its headings."""


# ── Inputs ────────────────────────────────────────────────────────────────

def primitives_text() -> str:
    """The compact primitive → preferred-format list (the spine picks the shape; the figures desk fills it)."""
    try:
        from src.display.enforcement import primitive_formats, primitives

        lines = []
        for p in primitives():
            fmts = ", ".join(primitive_formats(p["key"])[:6]) or "(any)"
            lines.append(f"- {p['key']}: {str(p.get('description', '')).split('.')[0]}. Formats: {fmts}")
        return "\n".join(lines)
    except Exception as exc:  # the catalog is optional input; the wall normalizes later
        logger.info(f"primitives catalog unavailable ({exc})")
        return "(catalog unavailable — name the primitive and a format in plain words)"


def budget_for(job: DossierJob) -> ExhibitsBudget:
    return ExhibitsBudget(tables=MAX_TABLES_DEFAULT if job.options.output.tables else 0,
                         figures=max(0, int(job.options.output.figures or 0)))


def _option_text(job: DossierJob) -> str:
    from src.dossier.plan import chosen_option

    opt = chosen_option(job)
    if opt is None:
        return f"INTENT: {job.options.intent or '(none)'}"
    lines = [f"ANGLE (the chosen deliverable): {opt.title}", opt.telling]
    if opt.deliverable:
        lines.append(f"Deliverable: {opt.deliverable} ({opt.deliverable_kind or 'dossier'}; used to {opt.use_kind or '?'})")
    if opt.you_will_understand:
        lines.append("Promised understanding: " + " | ".join(p.text for p in opt.you_will_understand if p.text))
    if opt.you_will_be_able_to:
        lines.append("Promised abilities: " + " | ".join(p.text for p in opt.you_will_be_able_to if p.text))
    if opt.questions_answered:
        lines.append("Questions answered: " + " | ".join(opt.questions_answered))
    if opt.output_shape.sections:
        lines.append("Brief's suggested sections (advisory): " + " / ".join(opt.output_shape.sections))
    if opt.output_shape.tables:
        lines.append("Brief's table ideas (advisory): " + " | ".join(opt.output_shape.tables))
    if opt.output_shape.figures:
        lines.append("Brief's figure ideas (advisory): " + " | ".join(opt.output_shape.figures))
    if job.options.intent:
        lines.append(f"Requester's intent: {job.options.intent}")
    return "\n".join(lines)


def _user(job: DossierJob) -> str:
    budget = budget_for(job)
    audience = job.options.audience
    return (
        f"{_option_text(job)}\n\nAUDIENCE: {audience} — {AUDIENCE_REGISTER.get(audience, '')}\n"
        f"EXHIBITS BUDGET (ceiling): {budget.tables} tables, {budget.figures} diagrams. "
        f"Sections: {MIN_SECTIONS}-{MAX_SECTIONS}.\n\n"
        f"PRIMITIVES (for figure specs — the analytical relation a diagram makes visible, and the formats it prefers):\n{primitives_text()}\n\n"
        f"ANALYSIS PROSE (every phase):\n{analysis_prose(job, max_chars_per_phase=ANALYSIS_CHARS_PER_PHASE)}\n\n"
        f"RECONNAISSANCE PROFILES (their anchors are verified verbatim quotes — copy from here):\n{compact_profiles(job.profiles)}"
    )


# ── Coercion + the wall ───────────────────────────────────────────────────

def _snake(value: str, fallback: str) -> str:
    key = re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().lower()).strip("_")
    return key or fallback


def coerce_spine(raw: dict[str, Any], budget: ExhibitsBudget) -> DossierSpine:
    """Shape-only coercion of the tool answer into the model (no judgment)."""
    raw = raw or {}
    read_raw = raw.get("read") or {}
    try:
        read = CompositionRead.model_validate(read_raw) if isinstance(read_raw, dict) else CompositionRead()
    except Exception:
        read = CompositionRead(plain_summary=str(read_raw.get("plain_summary", "")) if isinstance(read_raw, dict) else "")
    sections: list[SpineSection] = []
    for i, s in enumerate(raw.get("sections") or [], start=1):
        if not isinstance(s, dict):
            continue
        table = None
        t = s.get("table")
        if isinstance(t, dict) and (t.get("row_unit") or t.get("columns") or t.get("intent")):
            table = SpineTableSpec(intent=str(t.get("intent", "")).strip(), row_unit=str(t.get("row_unit", "")).strip(),
                                   columns=[str(c).strip() for c in (t.get("columns") or []) if str(c).strip()],
                                   carries_claims=[str(c).strip() for c in (t.get("carries_claims") or []) if str(c).strip()])
        figure = None
        f = s.get("figure")
        if isinstance(f, dict) and (f.get("picture_shows") or f.get("caption_says")):
            figure = SpineFigureSpec(primitive=_snake(str(f.get("primitive", "")), ""), visual_format=str(f.get("visual_format", "")).strip(),
                                     picture_shows=str(f.get("picture_shows", "")).strip(), caption_says=str(f.get("caption_says", "")).strip(),
                                     why_a_picture=str(f.get("why_a_picture", "")).strip())
        anchors = []
        for a in s.get("anchors_planned") or []:
            if isinstance(a, dict) and str(a.get("quote", "")).strip():
                anchors.append(Anchor(doc_key=str(a.get("doc_key", "")).strip(), quote=str(a.get("quote", "")).strip()))
        sections.append(SpineSection(
            key=_snake(str(s.get("key", "")), f"section_{i}"), heading=str(s.get("heading", "")).strip(),
            claim=str(s.get("claim", "")).strip(), reader_needs_next=str(s.get("reader_needs_next", "")).strip(),
            evidence_kind=str(s.get("evidence_kind", "mechanism")).strip() or "mechanism",
            table=table, figure=figure, anchors_planned=anchors,
            feeds=[_snake(str(k), "") for k in (s.get("feeds") or []) if str(k).strip()],
        ))
    return DossierSpine(
        read=read, thesis=str(raw.get("thesis", "")).strip(), reader_question=str(raw.get("reader_question", "")).strip(),
        handle=str(raw.get("handle", "")).strip(), through_line=str(raw.get("through_line", "")).strip(),
        summary_job=str(raw.get("summary_job", "")).strip(), conclusion_job=str(raw.get("conclusion_job", "")).strip(),
        sections=sections, exhibits_budget=budget,
    )


def _job_key(text: str) -> str:
    return normalize(text).strip(" .!?;:,")


def validate_spine(spine: DossierSpine, corpus: Optional[NormalizedCorpus]) -> tuple[dict[str, list[str]], list[str]]:
    """The wall. Returns (errors per section key, global errors). Verifies anchors in place
    (a verified, untrimmed anchor is kept; a trimmed fragment or a miss is an error — refused, not trimmed)."""
    per: dict[str, list[str]] = {}
    glob: list[str] = []
    try:
        from src.display.enforcement import normalize_format_key, primitive_keys
        prims = set(primitive_keys())
    except Exception:
        normalize_format_key, prims = (lambda v: v or None), set()  # type: ignore[assignment]

    if not spine.thesis or not is_one_sentence(spine.thesis):
        glob.append("thesis must be exactly one sentence")
    if not spine.summary_job or not spine.conclusion_job:
        glob.append("summary_job and conclusion_job are both required")
    elif _job_key(spine.summary_job) == _job_key(spine.conclusion_job):
        glob.append("summary_job and conclusion_job must be DIFFERENT jobs")
    n = len(spine.sections)
    if n < MIN_SECTIONS or n > MAX_SECTIONS:
        glob.append(f"{n} sections; the spine needs {MIN_SECTIONS}-{MAX_SECTIONS}")
    keys = [s.key for s in spine.sections]
    dupes = {k for k in keys if keys.count(k) > 1}
    if dupes:
        glob.append("duplicate section keys: " + ", ".join(sorted(dupes)))
    keyset = set(keys)

    for s in spine.sections:
        errs = per.setdefault(s.key, [])
        if not s.heading:
            errs.append("heading is required")
        if not s.claim:
            errs.append("claim is required — the one sentence this section proves")
        elif not is_one_sentence(s.claim):
            errs.append(f"claim must be ONE sentence (it has {sentence_count(s.claim)}): split the section or cut the claim")
        if s.evidence_kind not in EVIDENCE_KINDS:
            errs.append(f"evidence_kind must be one of {', '.join(EVIDENCE_KINDS)}")
        if s.table is not None:
            if not s.table.row_unit:
                errs.append("table.row_unit is required (one row = one …)")
            if not (2 <= len(s.table.columns) <= 6):
                errs.append(f"table.columns must have 2-6 entries (has {len(s.table.columns)})")
            if not s.table.carries_claims:
                errs.append("table.carries_claims must name at least one claim the rows carry")
        if s.figure is not None:
            if not s.figure.picture_shows:
                errs.append("figure.picture_shows is required")
            if not s.figure.caption_says:
                errs.append("figure.caption_says is required")
            elif has_digit_run(s.figure.caption_says):
                errs.append("figure.caption_says carries a number — captions never carry numbers; move it to the prose or the table")
            if prims and s.figure.primitive not in prims:
                errs.append(f"figure.primitive {s.figure.primitive!r} is not a known primitive ({', '.join(sorted(prims))})")
            canon = normalize_format_key(s.figure.visual_format) if s.figure.visual_format else None
            if canon is None:
                errs.append(f"figure.visual_format {s.figure.visual_format!r} is not a catalog format; pick one the primitive prefers")
            else:
                s.figure.visual_format = canon
        if corpus is not None:
            kept: list[Anchor] = []
            failed: list[str] = []
            for a in s.anchors_planned[:MAX_ANCHORS + 2]:
                v = verify_anchor(a, corpus)
                if v is not None and not v.trimmed:
                    kept.append(v)
                else:
                    failed.append(a.quote[:100])
            s.anchors_planned = kept[:MAX_ANCHORS]
            if len(kept) < MIN_ANCHORS:
                errs.append("no planned anchor is verbatim in the documents (copy character-for-character from the profiles' anchors); refused: "
                            + " | ".join(f"“{q}”" for q in failed[:3]))
        elif not s.anchors_planned:
            errs.append("anchors_planned needs at least one quote")
        s.feeds = [k for k in s.feeds if k in keyset and k != s.key]
    return {k: v for k, v in per.items() if v}, glob


def _repair_by_code(spine: DossierSpine, per: dict[str, list[str]], budget: ExhibitsBudget) -> DossierSpine:
    """Shape trivia the model still got wrong after the patch is repaired by code and recorded (never merit)."""
    notes = list(spine.notes)
    for s in spine.sections:
        errs = per.get(s.key) or []
        if s.claim and not is_one_sentence(s.claim):
            first = re.split(r"(?<=[.!?])\s+", s.claim.strip())[0]
            notes.append(f"section {s.key}: claim cut to its first sentence by code ({s.claim[:60]}…)")
            s.claim = first
        if s.figure is not None and any("caption_says carries a number" in e for e in errs):
            stripped = re.sub(r"\s*\d[\d,.:/%-]*\s*", " ", s.figure.caption_says).strip()
            if stripped and not has_digit_run(stripped):
                notes.append(f"section {s.key}: digits removed from caption_says by code")
                s.figure.caption_says = stripped
            else:
                notes.append(f"section {s.key}: figure spec dropped (caption carried numbers the patch did not remove)")
                s.figure = None
        if s.figure is not None and any("figure.visual_format" in e or "figure.primitive" in e or "picture_shows" in e for e in errs):
            notes.append(f"section {s.key}: figure spec dropped (unknown primitive/format or empty picture_shows after the patch)")
            s.figure = None
        if s.table is not None and any(e.startswith("table.") for e in errs):
            notes.append(f"section {s.key}: table spec dropped (shape errors after the patch: {' | '.join(e for e in errs if e.startswith('table.'))[:160]})")
            s.table = None
        if any(e.startswith("no planned anchor") for e in errs):
            notes.append(f"section {s.key}: no verbatim anchor survived the wall; the section is kept without planned anchors")
    # budget ceiling: earliest sections lose their exhibit first (the last section is the one an executive acts on)
    t_over = len(spine.table_sections()) - budget.tables
    for s in spine.sections:
        if t_over <= 0:
            break
        if s.table is not None:
            s.table = None
            t_over -= 1
            notes.append(f"section {s.key}: table spec dropped by code (over the budget of {budget.tables})")
    f_over = len(spine.figure_sections()) - budget.figures
    for s in spine.sections:
        if f_over <= 0:
            break
        if s.figure is not None:
            s.figure = None
            f_over -= 1
            notes.append(f"section {s.key}: figure spec dropped by code (over the budget of {budget.figures})")
    spine.notes = notes
    return spine


def _merge_patch(spine: DossierSpine, patch: DossierSpine, wanted: set[str]) -> tuple[DossierSpine, list[str]]:
    """Replace the failing sections (by key) with the patched ones; keep every other section verbatim."""
    by_key = {s.key: s for s in patch.sections if s.key in wanted}
    unknown = [s.key for s in patch.sections if s.key not in wanted]
    merged = [by_key.get(s.key, s) for s in spine.sections]
    spine.sections = merged
    return spine, unknown


# ── The step ──────────────────────────────────────────────────────────────

def _patch_tail(per: dict[str, list[str]], glob: list[str]) -> str:
    lines = ["---", "YOUR SPINE WAS JUDGED WHOLE; ONLY THESE SECTIONS FAILED THE WALL. Return ONLY replacement entries for the "
             "sections listed (same `key`, everything corrected); every other section is kept as you wrote it. A mistake you "
             "fix once must stay fixed."]
    for k, errs in per.items():
        lines.append(f"- section `{k}`: " + " | ".join(errs))
    if glob:
        lines.append("Whole-spine notes (fix where a section causes them): " + " | ".join(glob))
    return "\n".join(lines)


def build_spine(job: DossierJob, docs: list[Document]) -> DossierSpine:
    """The call, the wall, one field-patch round, the code repairs. Raises when no spine can be built."""
    budget = budget_for(job)
    corpus = NormalizedCorpus({d.key: d.text for d in docs}) if docs else None
    user = _user(job)
    raw, _ = call_json(job.id, STEP, label="composition read + spine", system=SYSTEM, user=user,
                       tool_name="record_spine", schema=SPINE_SCHEMA, model_cls=None, max_tokens=14000, cache=True)
    spine = coerce_spine(raw, budget)
    per, glob = validate_spine(spine, corpus)
    events.emit(job.id, "note", phase=STEP, detail=f"spine wall: {len(spine.sections)} sections, {len(per)} with errors"
                + (f"; whole: {' | '.join(glob)}" if glob else ""), payload_json={"kind": "spine_wall", "errors": per, "global": glob})
    if per or glob:
        wanted = set(per.keys()) or {s.key for s in spine.sections}
        raw2, _ = call_json(job.id, STEP, label=f"spine patch ({len(wanted)} sections)", system=SYSTEM, user=user,
                            user_tail=_patch_tail(per, glob), tool_name="record_spine_patch", schema=PATCH_SCHEMA,
                            model_cls=None, max_tokens=8000, cache=True)
        patch = coerce_spine({"sections": (raw2 or {}).get("sections", []), "thesis": spine.thesis,
                              "summary_job": spine.summary_job, "conclusion_job": spine.conclusion_job}, budget)
        spine, unknown = _merge_patch(spine, patch, wanted)
        if unknown:
            spine.notes.append("patch returned sections that were not asked for (ignored): " + ", ".join(unknown))
        per, glob = validate_spine(spine, corpus)
        events.emit(job.id, "note", phase=STEP, detail=f"spine wall after patch: {len(per)} sections still failing"
                    + (f"; whole: {' | '.join(glob)}" if glob else ""), payload_json={"kind": "spine_wall", "errors": per, "global": glob, "after_patch": True})
    spine = _repair_by_code(spine, per, budget)
    if glob and _job_key(spine.summary_job) == _job_key(spine.conclusion_job):
        spine.notes.append("summary_job and conclusion_job were identical; the conclusion's job was set by code to 'the decision rule and the question to ask'")
        spine.conclusion_job = "the decision rule and the question to ask next"
    if len(spine.sections) < MIN_SECTIONS:
        raise RuntimeError(f"spine has {len(spine.sections)} sections after repair; needs {MIN_SECTIONS}")
    spine.sections = spine.sections[:MAX_SECTIONS]
    spine.round = 1
    return spine


def narration_for(spine: DossierSpine) -> str:
    t, f = len(spine.table_sections()), len(spine.figure_sections())
    return (f"Deciding what the dossier argues — {len(spine.sections)} sections, each with one claim; "
            f"{t} table{'s' if t != 1 else ''} and {f} diagram{'s' if f != 1 else ''} commissioned by the argument, not by a dial.")


def run_spine(job: DossierJob, docs: list[Document]) -> Optional[DossierSpine]:
    """Pass S with the skip law: None (recorded `spine_unavailable`) lets the legacy paths run."""
    try:
        spine = build_spine(job, docs)
    except Exception as exc:
        logger.warning(f"spine unavailable: {exc}", exc_info=True)
        events.emit(job.id, "note", phase=STEP, detail=f"spine_unavailable: {exc.__class__.__name__}: {str(exc)[:300]} — tables, figures and the draft fall back to prose-planned paths",
                    payload_json={"kind": "spine_unavailable", "reason": str(exc)[:300]})
        return None
    events.emit(job.id, "narration", phase=STEP, narrator=narration_for(spine), detail=narration_for(spine))
    events.emit(job.id, "artifact", phase=STEP, detail=f"spine: {spine.thesis}",
                payload_json={"kind": "spine", "thesis": spine.thesis, "handle": spine.handle,
                              "sections": [{"key": s.key, "heading": s.heading, "claim": s.claim,
                                            "table": bool(s.table), "figure": bool(s.figure), "anchors": len(s.anchors_planned)} for s in spine.sections],
                              "summary_job": spine.summary_job, "conclusion_job": spine.conclusion_job, "notes": spine.notes})
    for n in spine.notes:
        events.emit(job.id, "note", phase=STEP, detail=f"spine repair: {n}", payload_json={"kind": "spine_repair"})
    return spine
