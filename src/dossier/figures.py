"""Step 6 — figures: labelled analytical DIAGRAMS, the way analyzer v1 / visualizer did them.

    plan (Sonnet, strict JSON)  →  FigureSpec[]      (src/dossier/figures.plan_figures)
    spec → prompt               →  str               (src/images/figure_prompts.build_diagram_prompt)
    prompt → image              →  bytes             (src/images/adapter.generate_image, gemini_pro 2K)
    image × spec → verdict      →  dict              (src/images/compliance.check_diagram)
    not ok → re-render ONCE with the reviewer's notes; keep the better attempt (v1's retry)

Every figure is a flowchart, a Venn, a quadrant, a timeline, a Sankey, a network, a
cycle, a matrix, an argument tree … chosen through the analytical primitive the
analysis exhibits (src/primitives) and rendered under src/display/enforcement.py's
per-format must_have/must_not rules. Nothing pictorial, nothing metaphorical.

The spec → prompt → render → check pipeline (`render_figure`) is independent of
where the spec came from: a later pass may derive specs from the section spine and
call `render_figure` unchanged. `validate_spec` is the wall specs must pass.

Skip law: a failure records `figure_skipped` / `figure_failed` with its reason and
the run continues; the figures step never kills a dossier.
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import time
from pathlib import Path
from typing import Any, Optional

from src.display.enforcement import (
    MAX_LABEL_CHARS,
    MAX_LABEL_WORDS,
    all_format_keys,
    aspect_for,
    catalog_text,
    collect_labels,
    content_labels,
    normalize_format_key,
    primitive_keys,
    validate_data,
)
from src.dossier import events, findings as ledger
from src.dossier.common import AUDIENCE_REGISTER, analysis_prose, compact_profiles, job_dir
from src.dossier.llm import call_json
from src.dossier.receipts import make_receipt, record
from src.dossier.schemas import DossierJob, Figure, FigureAnchor, FigureSpec, Finding, SpineSection
from src.dossier.walls import has_digit_run, normalize
from src.sources.schemas import Document

logger = logging.getLogger(__name__)

STEP = "figures"
DEFAULT_PROVIDER = "gemini_pro"          # Nano Banana Pro: the renderer for text-bearing diagrams
FALLBACK_PROVIDERS = ("gemini_flash",)   # same family, also renders text; Seedream/Qwen do not
RENDER_SIZE = "2K"
MAX_RENDER_ATTEMPTS = 2                  # first render + one revision (v1's retry)
MIN_GROUNDED_FRACTION = 0.5              # labels grounded in the material / all labels
MIN_VERIFIED_ANCHORS = 1
MAX_LABELS = 30
MIN_ANCHOR_CHARS = 6
MAX_TITLE_CHARS = 70
MATERIAL_MAX_CHARS = 90_000

# ── Planner schema (forced tool) ─────────────────────────────────────────

FIGURE_ITEM_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["key", "primitive", "visual_format", "title", "data", "caption", "why_this_format", "anchors"],
    "properties": {
        "key": {"type": "string", "description": "snake_case identifier"},
        "primitive": {"type": "string", "description": "one of the 12 analytical primitives"},
        "visual_format": {"type": "string", "description": "one of the catalog format keys"},
        "title": {"type": "string", "description": "<= 70 characters; rendered at the top of the diagram"},
        "data": {"type": "object", "additionalProperties": True,
                 "description": "the diagram's entire labelled content in the format family's JSON shape; every label <= 6 words"},
        "caption": {"type": "string", "description": "the analytic point in one sentence; use no number that is not in the data"},
        "why_this_format": {"type": "string", "description": "one sentence: why this primitive and this format for this content"},
        "anchors": {"type": "array", "minItems": 1, "maxItems": 24,
                    "items": {"type": "object", "additionalProperties": False, "required": ["label", "quote", "source"],
                              "properties": {"label": {"type": "string", "description": "a label from data"},
                                             "quote": {"type": "string", "description": "verbatim phrase (20-200 chars) from the ANALYSIS PROSE, a TABLE cell or a PROFILE that grounds the label"},
                                             "source": {"type": "string", "description": "analysis | table | profile"}}}},
    },
}
FIGURES_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["figures"],
                  "properties": {"figures": {"type": "array", "minItems": 1, "maxItems": 6, "items": FIGURE_ITEM_SCHEMA}}}

SYSTEM = """You are the figures desk of The Analyst. Every figure you plan is a LABELLED ANALYTICAL DIAGRAM — a flowchart,
a Venn diagram, a quadrant chart, a timeline, a Sankey, a network, a cycle, a matrix, an argument tree, a force-field —
never an illustration, never a scene, never a metaphor, never a photograph. A reader must be able to read the figure's
labels and see the analytic point in the structure itself.

For each figure you choose the analytical PRIMITIVE the analysis actually exhibits (cyclical causation, hierarchical
support, dialectical tension, branching, bundling, strategic interaction, layering, temporal evolution, comparative
positioning, flow, rhetorical architecture, network) and the FORMAT that shows that primitive, from the catalog. Then
you write the diagram's COMPLETE content in the format family's JSON shape: short labels (at most 6 words), names,
dates and figures exactly as the material gives them, nothing invented, nothing vague. Prefer content that the tables
and the analysis state concretely (named actors, cases, terms, stages, dates) over abstractions. Each figure shows a
DIFFERENT structure — do not plan two figures of the same format or the same content. A figure that cannot be filled
from the material is not proposed. Every label is grounded: for the important labels you copy a verbatim phrase from
the material that supports it."""


# ── Material (what figures may draw on) ──────────────────────────────────

def tables_text(job: DossierJob) -> str:
    parts = []
    for t in job.tables:
        parts.append(f"### Table `{t.key}` — {t.caption}\n| " + " | ".join(t.columns) + " |")
        for r in t.rows:
            parts.append("| " + " | ".join((c.value or "").replace("|", "/") for c in r.cells) + " |")
        if t.note:
            parts.append(f"note: {t.note}")
    return "\n".join(parts) if parts else "(no tables)"


def material_text(job: DossierJob, max_chars: int = MATERIAL_MAX_CHARS) -> str:
    """Analysis prose + tables + profiles + the chosen telling: the only ground figures may stand on."""
    from src.dossier.plan import chosen_option

    opt = chosen_option(job)
    telling = f"{opt.title}\n{opt.telling}" if opt else (job.options.intent or "")
    tables = tables_text(job)
    profiles = compact_profiles(job.profiles)
    budget = max(20_000, max_chars - len(tables) - min(len(profiles), 12_000) - len(telling))
    analysis = analysis_prose(job, max_chars_per_phase=budget // max(1, len(job.analysis) or 1))[:budget]
    return (f"ANGLE (the chosen telling):\n{telling}\n\nTABLES (verified rows):\n{tables}\n\n"
            f"ANALYSIS PROSE:\n{analysis}\n\nPROFILES:\n{profiles[:12_000]}")


# ── The wall: shape + grounding ──────────────────────────────────────────

def _snake(value: str, fallback: str) -> str:
    key = re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().lower()).strip("_")
    return key or fallback


def _coerce_spec(raw: dict[str, Any], index: int) -> FigureSpec:
    anchors = []
    for a in raw.get("anchors", []) or []:
        if isinstance(a, dict) and str(a.get("label", "")).strip():
            anchors.append(FigureAnchor(label=str(a.get("label", "")).strip(), quote=str(a.get("quote", "")).strip(),
                                        source=str(a.get("source", "")).strip().lower()))
    data = raw.get("data")
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            data = {}
    return FigureSpec(
        key=_snake(str(raw.get("key", "")), f"figure_{index}"),
        primitive=_snake(str(raw.get("primitive", "")), ""),
        visual_format=str(raw.get("visual_format", "")).strip(),
        title=str(raw.get("title", "")).strip(),
        data=data if isinstance(data, dict) else {},
        caption=str(raw.get("caption", "")).strip(),
        why_this_format=str(raw.get("why_this_format", "")).strip(),
        anchors=anchors,
    )


def validate_spec(spec: FigureSpec, material_norm: str) -> tuple[list[str], dict[str, Any]]:
    """Shape (format, data family, label length, title, caption digits) and grounding (anchors
    verbatim in the material, or the label itself in the material). Returns (errors, grounding)."""
    errors: list[str] = []
    canon = normalize_format_key(spec.visual_format)
    if canon is None:
        errors.append(f"visual_format {spec.visual_format!r} is not in the catalog; choose one of: {', '.join(all_format_keys())}")
    else:
        spec.visual_format = canon
    if spec.primitive not in primitive_keys():
        errors.append(f"primitive {spec.primitive!r} must be one of: {', '.join(primitive_keys())}")
    if not spec.title:
        errors.append("title is required")
    elif len(spec.title) > MAX_TITLE_CHARS:
        errors.append(f"title is {len(spec.title)} chars; max {MAX_TITLE_CHARS}")
    if canon:
        errors.extend(validate_data(canon, spec.data))
    labels = collect_labels(spec.data) if isinstance(spec.data, dict) else []
    if len(labels) > MAX_LABELS:
        errors.append(f"{len(labels)} labels is too many for one diagram (max {MAX_LABELS}); condense")
    # caption digits must exist somewhere in the data
    data_text = json.dumps(spec.data, ensure_ascii=False) if spec.data else ""
    for num in set(re.findall(r"\d[\d,.]*", spec.caption or "")):
        if num not in data_text:
            errors.append(f"caption uses the number '{num}' which is not in the data")
    # grounding — over CONTENT labels (axis names, quadrant names etc. are the planner's own scaffolding)
    content = content_labels(spec.data) if isinstance(spec.data, dict) else []
    grounding = {"checked": bool(material_norm), "labels": len(labels), "content_labels": len(content), "grounded": 0,
                 "ungrounded": [], "anchors": len(spec.anchors), "anchors_verified": 0, "anchors_failed": []}
    if material_norm:
        verified_labels: set[str] = set()
        for a in spec.anchors:
            q = normalize(a.quote)
            a.verified = bool(q) and len(q) >= MIN_ANCHOR_CHARS and q in material_norm
            if a.verified:
                grounding["anchors_verified"] += 1
                verified_labels.add(normalize(a.label))
            elif len(grounding["anchors_failed"]) < 12:
                grounding["anchors_failed"].append({"label": a.label, "quote": a.quote[:120]})
        for lab in content:
            if normalize(lab) in verified_labels or label_in_material(lab, material_norm):
                grounding["grounded"] += 1
            else:
                grounding["ungrounded"].append(lab)
        frac = grounding["grounded"] / len(content) if content else 1.0
        grounding["fraction"] = round(frac, 2)
        if content and (frac < MIN_GROUNDED_FRACTION or grounding["anchors_verified"] < MIN_VERIFIED_ANCHORS):
            errors.append(
                f"ungrounded: only {grounding['grounded']}/{len(content)} content labels use the material's own words or carry "
                f"a verified verbatim anchor ({grounding['anchors_verified']} of {len(spec.anchors)} anchors verified). "
                "Ungrounded labels (use names/terms exactly as the material writes them, or drop them): "
                + "; ".join(grounding["ungrounded"][:10])
                + (". Anchors that are not verbatim (copy character-for-character): "
                   + "; ".join(f['quote'][:60] for f in grounding["anchors_failed"][:4]) if grounding["anchors_failed"] else ""))
    return errors, grounding


_STOP = {"the", "and", "for", "with", "from", "into", "that", "this", "than", "over", "under", "your", "their",
         "have", "been", "were", "what", "when", "where", "which", "while", "after", "before", "between", "about",
         "each", "every", "more", "most", "less", "very", "only", "also", "then", "them", "they", "will", "would",
         "could", "should", "does", "into", "onto", "upon", "toward", "towards", "versus", "zone"}


def label_in_material(label: str, material_norm: str) -> bool:
    """A label is grounded when it appears verbatim, or when every significant word in it
    (≥4 letters, not a stopword) appears in the material — paraphrase of the material's
    vocabulary is allowed, invented names and terms are not."""
    n = normalize(label)
    if len(n) >= 4 and n in material_norm:
        return True
    tokens = [t for t in re.findall(r"[a-z0-9][a-z0-9&'.+-]*", n) if len(t) >= 4 and t not in _STOP]
    numbers = re.findall(r"\d[\d,.]*", n)
    if not tokens and not numbers:
        return False
    return all(t in material_norm for t in tokens) and all(x in material_norm for x in numbers)


# ── Style school (affinities: audience + engines + format) ───────────────

def choose_style_school(job: DossierJob, format_key: str) -> str:
    """Best school by summed affinity rank over audience, the plan's engines and the format."""
    try:
        from src.styles.registry import get_style_registry

        reg = get_style_registry()
        scores: dict[str, float] = {}

        def vote(schools, weight: float) -> None:
            for rank, s in enumerate(schools or []):
                key = getattr(s, "value", s)
                scores[key] = scores.get(key, 0.0) + weight * (1.0 if rank == 0 else 0.6)

        vote(reg.get_styles_for_audience(job.options.audience), 1.0)
        for p in (job.plan.phases if job.plan else []):
            vote(reg.get_styles_for_engine(p.engine_key), 0.8)
        vote(reg.get_styles_for_format(format_key), 0.9)
        if scores:
            return max(scores.items(), key=lambda kv: kv[1])[0]
    except Exception as exc:
        logger.info(f"style affinities unavailable ({exc}); default school")
    return "explanatory_narrative"


# ── Plan (Sonnet) ────────────────────────────────────────────────────────

def _plan_user(job: DossierJob, n: int, material: str, replace: Optional[list[tuple[FigureSpec, list[str]]]] = None,
               keep: Optional[list[FigureSpec]] = None) -> str:
    from src.dossier.plan import chosen_option

    opt = chosen_option(job)
    ideas = " | ".join(opt.output_shape.figures) if opt and opt.output_shape.figures else "(none)"
    engines = ", ".join(f"{p.engine_key}@{p.depth}" for p in job.plan.phases) if job.plan else "(none)"
    rules = (
        "LABEL RULES (the wall rejects violations): every string inside `data` is printed in the image — at most "
        f"{MAX_LABEL_WORDS} words and {MAX_LABEL_CHARS} characters each; matrix cells 1-4 words; no sentences, no "
        "parentheticals, no explanations (those belong in caption / why_this_format, never in data). Content labels "
        "(actors, cases, terms, dates, amounts) use the material's own words exactly; structural labels (axis names, "
        "quadrant names, column headers) may be yours. Aim for 8-20 labels per figure; 30 is the maximum. Titles at most "
        f"{MAX_TITLE_CHARS} characters. Each anchor quote is copied character-for-character from the material.\n"
    )
    head = (f"Plan exactly {n} figure(s), each a labelled analytical diagram with a DIFFERENT format.\n{rules}"
            f"AUDIENCE: {job.options.audience} — {AUDIENCE_REGISTER.get(job.options.audience, '')}\n"
            f"ENGINES that produced the analysis: {engines}\n"
            f"Figure ideas from the brief (translate them into diagrams; do not draw scenes): {ideas}\n\n")
    if replace:
        kept = "; ".join(f"`{s.key}` ({s.visual_format})" for s in (keep or [])) or "(none)"
        fixes = "\n".join(f"- `{s.key}` ({s.visual_format}): " + " | ".join(errs[:6]) for s, errs in replace)
        head += (f"YOUR PREVIOUS ANSWER WAS PARTLY REJECTED BY THE WALL. Figures kept as they are: {kept}.\n"
                 f"Return ONLY {len(replace)} replacement figure(s) for the rejected ones, fixing these errors "
                 f"(or choose a different format/content that the material can fill):\n{fixes}\n\n")
    return head + f"CATALOG:\n{catalog_text()}\n\nMATERIAL (the only ground for labels and anchors):\n{material}"


def plan_figures(job: DossierJob, n: int) -> list[FigureSpec]:
    """N FigureSpecs through the wall; rejected ones are re-asked once. May return fewer than N."""
    material = material_text(job)
    material_norm = normalize(material)
    label = f"figure plan ({n} diagrams)"
    raw, _ = call_json(job.id, STEP, label=label, system=SYSTEM, user=_plan_user(job, n, material),
                       tool_name="record_figure_plan", schema=FIGURES_SCHEMA, model_cls=None, max_tokens=12000)
    accepted: list[FigureSpec] = []
    rejected: list[tuple[FigureSpec, list[str]]] = []
    seen_formats: set[str] = set()

    def admit(items: list[dict[str, Any]]) -> None:
        for i, item in enumerate(items, start=len(accepted) + len(rejected) + 1):
            try:
                spec = _coerce_spec(item, i)
            except Exception as exc:
                logger.warning(f"figure spec unreadable: {exc}")
                continue
            errors, grounding = validate_spec(spec, material_norm)
            if spec.visual_format in seen_formats and not errors:
                errors.append(f"format {spec.visual_format} is already used by another figure; choose a different one")
            if errors:
                rejected.append((spec, errors))
                events.emit(job.id, "note", phase=STEP, detail=f"figure wall rejected `{spec.key}` ({spec.visual_format}): " + " | ".join(errors[:3]),
                            payload_json={"kind": "figure_rejected", "key": spec.key, "errors": errors, "grounding": grounding})
            else:
                spec.style_school = choose_style_school(job, spec.visual_format)
                seen_formats.add(spec.visual_format)
                accepted.append(spec)
                events.emit(job.id, "note", phase=STEP,
                            detail=f"figure wall passed `{spec.key}`: {spec.primitive} → {spec.visual_format}, {grounding.get('labels', 0)} labels, "
                                   f"{grounding.get('grounded', 0)} grounded, {grounding.get('anchors_verified', 0)} anchors verified; style {spec.style_school}",
                            payload_json={"kind": "figure_accepted", "key": spec.key, "grounding": grounding})
            # the grounding report travels on the spec for the figure record
            spec.__dict__["_grounding"] = grounding

    admit((raw or {}).get("figures", [])[: n + 2])
    if rejected and len(accepted) < n:
        need = min(n - len(accepted), len(rejected))
        raw2, _ = call_json(job.id, STEP, label=f"figure plan repair ({need})", system=SYSTEM,
                            user=_plan_user(job, need, material, replace=rejected[:need], keep=accepted),
                            tool_name="record_figure_plan", schema=FIGURES_SCHEMA, model_cls=None, max_tokens=12000)
        rejected = []
        admit((raw2 or {}).get("figures", [])[:need])
        for spec, errors in rejected:
            events.emit(job.id, "note", phase=STEP, detail=f"figure_skipped `{spec.key}`: still rejected after repair — " + " | ".join(errors[:2]),
                        payload_json={"kind": "figure_skipped", "key": spec.key, "reason": errors})
    return accepted[:n]


# ── Spec from the spine (pass E2): fill exactly the diagrams the spine commissioned ──

SPINE_SYSTEM = SYSTEM + """

THE SPINE HAS ALREADY DECIDED WHICH DIAGRAMS EXIST. For each commissioned section you receive its claim, the
primitive, the format the structure editor chose, `picture_shows` (which named things appear in what relation),
`caption_says` and why a picture is needed. You FILL each spec: keep the `section_key` and the primitive; keep the
format unless the material cannot fit its data family (then choose another format the same primitive prefers and say
why in `why_this_format`); write the diagram's complete labelled content so that it shows exactly what `picture_shows`
says, with the material's own names; the caption is `caption_says` verbatim or tightened — never a number in it. Do
not invent a diagram the spine did not commission; do not merge two specs."""


def _spec_item_schema(section_keys: list[str]) -> dict:
    item = json.loads(json.dumps(FIGURE_ITEM_SCHEMA))
    item["required"] = ["section_key"] + item["required"]
    item["properties"] = {"section_key": {"type": "string", "enum": section_keys, "description": "the commissioning spine section"}, **item["properties"]}
    item["properties"]["caption"]["description"] = "caption_says verbatim or tightened; at most two sentences; NO digits"
    return item


def spec_figures_schema(section_keys: list[str]) -> dict:
    return {"type": "object", "additionalProperties": False, "required": ["figures"],
            "properties": {"figures": {"type": "array", "minItems": 1, "maxItems": max(1, len(section_keys)), "items": _spec_item_schema(section_keys)}}}


def _spec_text(sections: list[SpineSection]) -> str:
    parts = []
    for sec in sections:
        f = sec.figure
        parts.append(f"### section_key: {sec.key} — “{sec.heading}”\n  claim: {sec.claim}\n  primitive: {f.primitive}\n  format chosen by the spine: {f.visual_format}\n"
                     f"  picture_shows: {f.picture_shows}\n  caption_says: {f.caption_says}\n  why a picture: {f.why_a_picture}")
    return "\n\n".join(parts)


def _spec_user(job: DossierJob, sections: list[SpineSection], material: str,
               replace: Optional[list[tuple[FigureSpec, list[str]]]] = None, keep: Optional[list[FigureSpec]] = None) -> tuple[str, str]:
    """(cacheable prefix, uncached tail) for the spine-driven planner."""
    engines = ", ".join(f"{p.engine_key}@{p.depth}" for p in job.plan.phases) if job.plan else "(none)"
    rules = (
        "LABEL RULES (the wall rejects violations): every string inside `data` is printed in the image — at most "
        f"{MAX_LABEL_WORDS} words and {MAX_LABEL_CHARS} characters each; matrix cells 1-4 words; no sentences, no "
        "parentheticals, no explanations (those belong in caption / why_this_format, never in data). Content labels "
        "(actors, cases, terms, dates, amounts) use the material's own words exactly; structural labels (axis names, "
        "quadrant names, column headers) may be yours. Aim for 8-20 labels per figure; 30 is the maximum. Titles at most "
        f"{MAX_TITLE_CHARS} characters. Each anchor quote is copied character-for-character from the material.\n"
    )
    head = (f"Fill exactly {len(sections)} commissioned diagram spec(s).\n{rules}"
            f"AUDIENCE: {job.options.audience} — {AUDIENCE_REGISTER.get(job.options.audience, '')}\n"
            f"ENGINES that produced the analysis: {engines}\n\nCOMMISSIONED BY THE SPINE:\n{_spec_text(sections)}\n\n"
            f"CATALOG:\n{catalog_text()}\n\nMATERIAL (the only ground for labels and anchors):\n{material}")
    tail = ""
    if replace:
        kept = "; ".join(f"`{s.key}` ({s.visual_format})" for s in (keep or [])) or "(none)"
        fixes = "\n".join(f"- section `{s.section_key or '?'}` `{s.key}` ({s.visual_format}): " + " | ".join(errs[:6]) for s, errs in replace)
        tail = (f"---\nYOUR PREVIOUS ANSWER WAS PARTLY REJECTED BY THE WALL. Figures kept as they are: {kept}.\n"
                f"Return ONLY {len(replace)} replacement figure(s) for the rejected section(s), fixing these errors "
                f"(or choose a different format the primitive prefers if the material cannot fill this one):\n{fixes}")
    return head, tail


def validate_spine_spec(spec: FigureSpec, section: SpineSection, material_norm: str) -> tuple[list[str], dict[str, Any]]:
    """The spec wall plus the spine's laws: primitive as commissioned, caption without digits, <= 2 sentences."""
    errors, grounding = validate_spec(spec, material_norm)
    if section.figure and spec.primitive != section.figure.primitive:
        errors.append(f"primitive must stay {section.figure.primitive!r} as the spine commissioned (got {spec.primitive!r})")
    if has_digit_run(spec.caption):
        errors.append("caption carries a number — captions never carry numbers (use the spine's caption_says)")
    from src.dossier.walls import sentence_count
    if sentence_count(spec.caption) > 2:
        errors.append("caption must be at most two sentences")
    return errors, grounding


def spec_figures(job: DossierJob) -> list[FigureSpec]:
    """Exactly the spine's figure specs, filled and walled; rejected ones re-asked once. May return fewer."""
    sections = job.spine.figure_sections()
    by_key = {s.key: s for s in sections}
    material = material_text(job)
    material_norm = normalize(material)
    head, _ = _spec_user(job, sections, material)
    raw, _ = call_json(job.id, STEP, label=f"figure specs from the spine ({len(sections)})", system=SPINE_SYSTEM, user=head,
                       tool_name="record_figure_plan", schema=spec_figures_schema([s.key for s in sections]), model_cls=None, max_tokens=12000, cache=True)
    accepted: list[FigureSpec] = []
    rejected: list[tuple[FigureSpec, list[str]]] = []
    seen_formats: set[str] = set()
    done_sections: set[str] = set()

    def admit(items: list[dict[str, Any]]) -> None:
        for i, item in enumerate(items, start=len(accepted) + len(rejected) + 1):
            if not isinstance(item, dict):
                continue
            sk = str(item.get("section_key", "")).strip()
            sec = by_key.get(sk)
            try:
                spec = _coerce_spec(item, i)
            except Exception as exc:
                logger.warning(f"figure spec unreadable: {exc}")
                continue
            spec.__dict__["_section_key"] = sk
            if sec is None or sk in done_sections:
                events.emit(job.id, "note", phase=STEP, detail=f"figure wall rejected `{spec.key}`: section_key {sk!r} " + ("was not commissioned" if sec is None else "already filled"),
                            payload_json={"kind": "figure_rejected", "key": spec.key, "errors": ["section_key"]})
                continue
            errors, grounding = validate_spine_spec(spec, sec, material_norm)
            if spec.visual_format in seen_formats and not errors:
                errors.append(f"format {spec.visual_format} is already used by another figure; choose a different one the primitive prefers")
            if errors:
                rejected.append((spec, errors))
                events.emit(job.id, "note", phase=STEP, detail=f"figure wall rejected `{spec.key}` for section {sk} ({spec.visual_format}): " + " | ".join(errors[:3]),
                            payload_json={"kind": "figure_rejected", "key": spec.key, "section_key": sk, "errors": errors, "grounding": grounding})
            else:
                spec.style_school = choose_style_school(job, spec.visual_format)
                seen_formats.add(spec.visual_format)
                done_sections.add(sk)
                accepted.append(spec)
                events.emit(job.id, "note", phase=STEP,
                            detail=f"figure wall passed `{spec.key}` for section {sk}: {spec.primitive} → {spec.visual_format}, {grounding.get('labels', 0)} labels, "
                                   f"{grounding.get('grounded', 0)} grounded, {grounding.get('anchors_verified', 0)} anchors verified; style {spec.style_school}",
                            payload_json={"kind": "figure_accepted", "key": spec.key, "section_key": sk, "grounding": grounding})
            spec.__dict__["_grounding"] = grounding

    admit((raw or {}).get("figures", [])[: len(sections) + 1])
    if rejected:
        need = [(sp, errs) for sp, errs in rejected if sp.__dict__.get("_section_key") not in done_sections]
        for sp, _e in need:
            sp.section_key = sp.__dict__.get("_section_key", "")
        if need:
            head2, tail2 = _spec_user(job, [by_key[sp.__dict__["_section_key"]] for sp, _ in need], material, replace=need, keep=accepted)
            raw2, _ = call_json(job.id, STEP, label=f"figure spec repair ({len(need)})", system=SPINE_SYSTEM, user=head, user_tail=tail2,
                                tool_name="record_figure_plan", schema=spec_figures_schema([sp.__dict__["_section_key"] for sp, _ in need]),
                                model_cls=None, max_tokens=12000, cache=True)
            rejected = []
            admit((raw2 or {}).get("figures", [])[: len(need)])
            for spec, errors in rejected:
                events.emit(job.id, "note", phase=STEP, detail=f"figure_skipped `{spec.key}`: still rejected after repair — " + " | ".join(errors[:2]),
                            payload_json={"kind": "figure_skipped", "key": spec.key, "section_key": spec.__dict__.get("_section_key"), "reason": errors})
    # reading order = the spine's order
    order = {s.key: i for i, s in enumerate(sections)}
    accepted.sort(key=lambda sp: order.get(sp.__dict__.get("_section_key", ""), 99))
    return accepted


def detected_sentence(verdict: Optional[dict[str, Any]], spec: FigureSpec) -> str:
    """What the picture ACTUALLY shows, from the check — the sentence the writer is handed."""
    if not verdict or not verdict.get("checked"):
        return f"unchecked: intended as a {spec.visual_format} titled “{spec.title}”"
    fmt = verdict.get("detected_format") or spec.visual_format
    found = verdict.get("labels_found") or []
    n = verdict.get("n_labels") or (len(found) + len(verdict.get("labels_missing") or []))
    bits = [f"a {fmt}" + ("" if verdict.get("format_ok") else f" (not the {spec.visual_format} that was asked for)"),
            f"{len(found)}/{n} labels legible" + (": " + ", ".join(found[:14]) if found else "")]
    if verdict.get("labels_missing"):
        bits.append("missing: " + ", ".join(verdict["labels_missing"][:8]))
    if verdict.get("prohibited_elements"):
        bits.append("prohibited: " + "; ".join(verdict["prohibited_elements"][:3]))
    if verdict.get("extra_text"):
        bits.append("extra text: " + "; ".join(verdict["extra_text"][:3]))
    return "; ".join(bits)


def enrich_from_spine(fig: Figure, section: Optional[SpineSection]) -> Figure:
    """Stamp the commissioning section's spec and the check's verdict on the record (no judgment)."""
    if section is not None:
        fig.section_key = section.key
        if section.figure:
            fig.picture_shows = section.figure.picture_shows
            fig.caption_says = section.figure.caption_says
    v = fig.compliance or {}
    fig.detected = detected_sentence(v, fig)
    fig.checked_ok = bool(v.get("ok")) if v.get("checked") else None
    return fig


def finding_for_figure(fig: Figure, section: Optional[SpineSection]) -> Optional[Finding]:
    where = {"figure_key": fig.key, "section_key": fig.section_key or (section.key if section else None)}
    if fig.status in ("failed", "skipped"):
        return ledger.mint("figure_unavailable", where=where, source="wall", affordance="none",
                           note=f"The diagram commissioned for this section could not be produced ({fig.status}: {fig.note or 'no reason recorded'}). The prose must carry what it was to show.",
                           quote=fig.caption_says or fig.caption)
    if fig.checked_ok is False:
        v = fig.compliance or {}
        issues = "; ".join(v.get("issues") or [])[:600]
        return ledger.mint("figure_depicts_other", where=where, source="wall", affordance="rerender_figure",
                           note=f"The check found the rendered diagram does not show what its spec says ({issues}). The reader would see something other than the section argues. Cure: redraw from the check's notes.",
                           quote=fig.caption, realization=str(v.get("suggestion") or "") or None)
    return None

def _get(obj: Any, *names: str, default=None):
    for name in names:
        if isinstance(obj, dict) and name in obj and obj[name] is not None:
            return obj[name]
        if hasattr(obj, name) and getattr(obj, name) is not None:
            return getattr(obj, name)
    return default


def _render_once(job_id: str, spec: FigureSpec, prompt: str, aspect: str, provider: str, attempt: int) -> tuple[Any, str]:
    """One image call with the same-family fallback; returns (result, provider_used)."""
    from src.images.adapter import ImageProviderError, generate_image

    chain = [provider] + [p for p in FALLBACK_PROVIDERS if p != provider]
    last: Optional[Exception] = None
    for prov in chain:
        try:
            return generate_image(prompt, provider=prov, size=RENDER_SIZE, aspect=aspect, no_text=False), prov
        except ImageProviderError as exc:
            last = exc
            events.emit(job_id, "note", phase=STEP, detail=f"{spec.key} attempt {attempt}: {prov} failed ({str(exc)[:160]}); trying next provider")
        except ValueError as exc:  # unsupported aspect on this provider → try next
            last = exc
    raise RuntimeError(f"all diagram providers failed: {last}")


def _attempt_score(verdict: Optional[dict[str, Any]]) -> tuple[int, int, int]:
    """Lower is better: (wrong format / prohibited, labels missing+misspelled+illegible, not checked)."""
    if not verdict or not verdict.get("checked"):
        return (1, 999, 1)
    bad_format = 0 if (verdict.get("format_ok") and not verdict.get("prohibited_elements")) else 1
    bad_labels = len(verdict.get("labels_missing") or []) + len(verdict.get("misspelled") or []) + len(verdict.get("illegible") or [])
    return (bad_format, bad_labels, 0)


def _revision_notes(verdict: dict[str, Any]) -> list[str]:
    notes: list[str] = []
    if not verdict.get("format_ok"):
        notes.append(f"The previous image was NOT the required format (it looked like: {verdict.get('detected_format')}). "
                     "Draw the mandated layout exactly as specified.")
    for p in verdict.get("prohibited_elements") or []:
        notes.append(f"Remove: {p}")
    if verdict.get("labels_missing"):
        notes.append("These labels were MISSING — render each of them: " + "; ".join(verdict["labels_missing"][:12]))
    for m in verdict.get("misspelled") or []:
        notes.append(f"Spell exactly “{m.get('expected')}” (the previous image printed “{m.get('seen')}”)")
    if verdict.get("illegible"):
        notes.append("These labels were illegible (too small / overlapped / cut off) — make them large and clear: "
                     + "; ".join(verdict["illegible"][:8]))
    if verdict.get("extra_text"):
        notes.append("Remove invented text that is not in the content: " + "; ".join(verdict["extra_text"][:6]))
    if not verdict.get("title_found"):
        notes.append("The title was missing — render it at the top.")
    if verdict.get("suggestion"):
        notes.append(str(verdict["suggestion"]))
    return notes


def render_figure(job: DossierJob, spec: FigureSpec, out_dir: Path, provider: Optional[str] = None,
                  revision_notes: Optional[list[str]] = None) -> Figure:
    """spec → prompt → render → check → (retry once) → save. Returns the Figure record.

    `revision_notes` (optional) ride the FIRST render too — the cross-check's words when it asks for a redraw.
    Raises only when no image could be produced at all; the caller applies the skip law.
    """
    from src.images.compliance import check_diagram
    from src.images.figure_prompts import build_diagram_prompt
    from src.images.storage import figure_url, save_figure

    provider = provider or DEFAULT_PROVIDER
    aspect = aspect_for(spec.visual_format)
    grounding = spec.__dict__.get("_grounding")
    fig = Figure(**spec.model_dump(), aspect=aspect, grounding=grounding)
    attempts: list[dict[str, Any]] = []
    revision: list[str] = list(revision_notes or [])
    label = f"figure {spec.key}"

    for attempt in range(1, MAX_RENDER_ATTEMPTS + 1):
        prompt = build_diagram_prompt(spec, style_school=spec.style_school or None, aspect=aspect,
                                      revision_notes=revision or None)
        events.emit(job.id, "call_started", phase=STEP, model=provider, label=f"{label} (attempt {attempt})",
                    detail=f"rendering {spec.key} as {spec.visual_format} ({spec.primitive}; {RENDER_SIZE}, {aspect}, "
                           f"{len(collect_labels(spec.data))} labels, style {spec.style_school})",
                    prompt_excerpt=events.excerpt(prompt, 600))
        started = time.time()
        try:
            result, provider_used = _render_once(job.id, spec, prompt, aspect, provider, attempt)
        except Exception as exc:
            events.emit(job.id, "call_failed", phase=STEP, label=f"{label} (attempt {attempt})", detail=f"{spec.key}: render failed: {exc}")
            if attempts:
                break  # keep what we have
            raise
        duration_ms = int((time.time() - started) * 1000)
        image_bytes: bytes = _get(result, "image_bytes", default=b"") or b""
        mime = str(_get(result, "mime_type", default="image/png") or "image/png")
        model_used = str(_get(result, "model", default="") or "")
        cost = float(_get(result, "cost_usd", default=0.0) or 0.0)
        if not image_bytes:
            raise RuntimeError("image provider returned no bytes")
        record(job.id, make_receipt(step=STEP, kind="image", model=model_used or provider_used, label=f"{label} (attempt {attempt})",
                                    duration_ms=duration_ms, prompt_text=prompt, cost_usd=cost))
        events.emit(job.id, "call_finished", phase=STEP, model=model_used or provider_used, label=f"{label} (attempt {attempt})",
                    cost_usd=cost, duration_ms=duration_ms,
                    detail=f"{spec.key} attempt {attempt} rendered by {provider_used} in {duration_ms/1000:.0f}s (${cost:.3f})")

        verdict = check_diagram(image_bytes, spec)
        usage = verdict.get("usage") or {}
        if verdict.get("checked") and usage.get("input_tokens"):
            record(job.id, make_receipt(step=STEP, kind="llm", model=str(verdict.get("model") or ""), label=f"diagram check {spec.key} (attempt {attempt})",
                                        input_tokens=int(usage.get("input_tokens") or 0), output_tokens=int(usage.get("output_tokens") or 0)))
        ext = {"image/jpeg": "jpg", "image/webp": "webp"}.get(mime, "png")
        local = out_dir / f"{spec.key}.attempt{attempt}.{ext}"   # every attempt kept on disk; the winner is copied below
        local.write_bytes(image_bytes)
        meta = {"prompt": prompt, "prompt_sent": _get(result, "prompt_sent", default=prompt), "provider": provider_used,
                "model": model_used, "cost_usd": cost, "size": RENDER_SIZE, "aspect": aspect, "caption": spec.caption,
                "register": "diagram", "scene": "", "compliance": verdict, "latency_ms": duration_ms,
                "dossier_job_id": job.id, "title": spec.title, "visual_format": spec.visual_format,
                "primitive": spec.primitive, "style_school": spec.style_school, "attempt": attempt, "data": spec.data}
        figure_id = None
        try:
            figure_id = save_figure(image_bytes, mime, job_id=job.id, name=f"{spec.key}" + (f"-a{attempt}" if attempt > 1 else ""), meta=meta)
        except Exception as exc:
            events.emit(job.id, "note", phase=STEP, detail=f"{spec.key}: save_figure failed ({exc}); keeping the local copy only")
        rec = {"n": attempt, "provider": provider_used, "model": model_used, "cost_usd": cost, "latency_ms": duration_ms,
               "figure_id": figure_id, "path": str(local), "prompt": prompt, "prompt_chars": len(prompt),
               "compliance": verdict, "revision_notes": list(revision)}
        attempts.append(rec)
        summary = ("ok" if verdict.get("ok") else ("not checked" if not verdict.get("checked") else "not ok: " + "; ".join(verdict.get("issues", [])[:3])))
        events.emit(job.id, "note", phase=STEP, detail=f"diagram check {spec.key} attempt {attempt}: {summary}",
                    payload_json={"kind": "diagram_check", "key": spec.key, "attempt": attempt, "verdict": verdict})
        if verdict.get("ok") or not verdict.get("checked"):
            break
        revision = _revision_notes(verdict)

    best = min(attempts, key=lambda a: _attempt_score(a.get("compliance")))
    for a in attempts:
        a["kept"] = a is best
    # the kept attempt is served under the figure's plain name; the attempts stay beside it
    kept_path = Path(best["path"])
    final = out_dir / f"{spec.key}{kept_path.suffix}"
    final.write_bytes(kept_path.read_bytes())
    fig.figure_id = best["figure_id"]
    fig.path = str(final)
    fig.url = figure_url(best["figure_id"]) if best["figure_id"] else f"/v1/dossier/jobs/{job.id}/figures/{final.name}"
    fig.provider = best["provider"]
    fig.model = best["model"] or None
    fig.prompt = best["prompt"]
    fig.cost_usd = round(sum(a["cost_usd"] for a in attempts), 4)
    fig.compliance = best["compliance"]
    fig.attempts = [{k: v for k, v in a.items() if k != "prompt"} for a in attempts]
    fig.status = "generated"
    v = best["compliance"] or {}
    if v.get("checked") and not v.get("ok"):
        fig.note = "compliance: " + "; ".join(v.get("issues", [])[:3])
    events.emit(job.id, "artifact", phase=STEP, detail=f"figure {spec.key}: {spec.title} — {spec.visual_format} ({spec.primitive}), "
                f"{len(attempts)} attempt(s), kept #{best['n']}" + (f" — {fig.note}" if fig.note else ""),
                payload_json={"kind": "figure", "key": spec.key, "url": fig.url, "path": fig.path, "figure_id": fig.figure_id,
                              "provider": fig.provider, "cost_usd": fig.cost_usd, "visual_format": spec.visual_format,
                              "primitive": spec.primitive, "title": spec.title, "attempts": len(attempts), "kept": best["n"],
                              "compliance": v})
    return fig


# ── The step ─────────────────────────────────────────────────────────────

def _persist_partial(job: DossierJob, figures: list[Figure]) -> None:
    try:
        from src.dossier.store import update_job

        update_job(job.id, figures=figures)
    except Exception as exc:  # bookkeeping never kills the run
        logger.debug(f"partial figure persist skipped: {exc}")


def run_figures(job: DossierJob, docs: list[Document], persist=None) -> list[Figure]:
    n = int(job.options.output.figures or 0)
    if n <= 0:
        events.emit(job.id, "note", phase=STEP, detail="figures_skipped: none requested")
        return []
    spine_driven = job.spine is not None
    if spine_driven and not job.spine.figure_sections():
        events.emit(job.id, "note", phase=STEP, detail="figures_skipped: the spine commissioned no diagram")
        return []
    try:
        specs = spec_figures(job) if spine_driven else plan_figures(job, n)
    except Exception as exc:
        logger.warning(f"figure planning failed: {exc}", exc_info=True)
        events.emit(job.id, "note", phase=STEP, detail=f"figures_skipped: planning failed ({exc.__class__.__name__}: {exc})",
                    payload_json={"kind": "figures_skipped", "reason": str(exc)[:300]})
        return []
    sections_by_key = {s.key: s for s in job.spine.figure_sections()} if spine_driven else {}
    minted: list[Finding] = []
    for sec in (job.spine.figure_sections() if spine_driven else []):
        if sec.key not in {sp.__dict__.get("_section_key") for sp in specs}:
            minted.append(ledger.mint("figure_unavailable", where={"section_key": sec.key}, source="wall", affordance="none",
                                      note=f"The spine commissioned a {sec.figure.visual_format} for “{sec.heading}” ({sec.figure.picture_shows[:120]}); no spec passed the wall. The prose must carry what it was to show.",
                                      quote=sec.figure.caption_says))
    events.emit(job.id, "artifact", phase=STEP, detail=f"figure plan: {len(specs)} diagram spec(s) — "
                + ", ".join(f"{s.key}={s.visual_format}" for s in specs),
                payload_json={"kind": "figure_plan", "figures": [s.model_dump() for s in specs]})
    if not specs:
        events.emit(job.id, "note", phase=STEP, detail="figures_skipped: no spec passed the wall",
                    payload_json={"kind": "figures_skipped", "reason": "no spec passed the wall"})
        return []
    out_dir = job_dir(job.id) / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        import src.images.adapter  # noqa: F401
        images_available = True
    except Exception as exc:
        images_available = False
        events.emit(job.id, "note", phase=STEP, detail=f"figures_skipped: images modules not available ({exc.__class__.__name__}: {exc})",
                    payload_json={"kind": "figures_skipped", "reason": str(exc)})
    figures: list[Figure] = []
    for spec in specs:
        section = sections_by_key.get(spec.__dict__.get("_section_key", ""))
        if not images_available:
            fig = Figure(**spec.model_dump(), status="skipped", note="images modules not available")
        else:
            try:
                fig = render_figure(job, spec, out_dir, job.options.image_provider)
            except Exception as exc:
                logger.warning(f"figure {spec.key} failed: {exc}", exc_info=True)
                events.emit(job.id, "call_failed", phase=STEP, label=f"figure {spec.key}", detail=f"figure_skipped {spec.key}: {exc}",
                            payload_json={"kind": "figure_skipped", "key": spec.key, "reason": str(exc)[:300]})
                fig = Figure(**spec.model_dump(), status="failed", note=str(exc)[:300])
        fig = enrich_from_spine(fig, section)
        finding = finding_for_figure(fig, section)
        if finding is not None:
            minted.append(finding)
        figures.append(fig)
        _persist_partial(job, figures)
    if spine_driven:
        ledger.append(job, minted, persist)
        bits = []
        for f in figures:
            sec = sections_by_key.get(f.section_key)
            head = f"diagram for “{sec.heading[:40]}”" if sec else f"figure {f.key}"
            if f.status != "generated":
                bits.append(f"{head}: {f.status}")
            elif f.checked_ok is None:
                bits.append(f"{head}: drawn, not checked")
            else:
                bits.append(f"{head}: " + ("checked, passes" if f.checked_ok else "checked — " + "; ".join((f.compliance or {}).get("issues", [])[:2])))
        narr = "Drawing the diagrams the argument asked for — " + "; ".join(bits) + "."
        events.emit(job.id, "narration", phase=STEP, narrator=narr, detail=narr)
    return figures


# ── CLI: plan and/or render against a saved job.json (no server needed) ──

def _main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m src.dossier.figures",
                                 description="Plan labelled diagrams from a saved dossier job.json and render them.")
    ap.add_argument("--job", required=True, help="path to a dossier job.json")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--out", required=True, help="output directory (specs, prompts, images, verdicts)")
    ap.add_argument("--job-id", default=None, help="job id to record receipts/events under (default: sample-<id>)")
    ap.add_argument("--provider", default=None)
    ap.add_argument("--plan-only", action="store_true")
    ap.add_argument("--specs", default=None, help="render these saved specs (JSON list) instead of planning")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING, format="%(asctime)s %(name)s %(levelname)s %(message)s")

    job = DossierJob.model_validate(json.loads(Path(args.job).read_text("utf-8")))
    job.id = args.job_id or f"sample-{job.id}"
    job.figures = []
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    if args.specs:
        specs = [FigureSpec.model_validate(s) for s in json.loads(Path(args.specs).read_text("utf-8"))]
        material_norm = normalize(material_text(job))
        for s in specs:
            errors, grounding = validate_spec(s, material_norm)
            s.__dict__["_grounding"] = grounding
            if errors:
                print(f"[{s.key}] wall errors: {errors}")
            if not s.style_school:
                s.style_school = choose_style_school(job, s.visual_format)
    else:
        specs = plan_figures(job, args.n)
    (out / "specs.json").write_text(json.dumps([s.model_dump() for s in specs], ensure_ascii=False, indent=2), "utf-8")
    for s in specs:
        g = s.__dict__.get("_grounding", {})
        print(f"[{s.key}] {s.primitive} → {s.visual_format} | {s.title!r} | {g.get('labels')} labels, "
              f"{g.get('grounded')} grounded, {g.get('anchors_verified')}/{g.get('anchors')} anchors | style {s.style_school}")
    if args.plan_only:
        return 0
    total = 0.0
    for s in specs:
        try:
            fig = render_figure(job, s, out, args.provider)
        except Exception as exc:
            print(f"[{s.key}] FAILED: {exc}")
            continue
        total += fig.cost_usd
        (out / f"{s.key}.prompt.txt").write_text(fig.prompt or "", "utf-8")
        (out / f"{s.key}.verdict.json").write_text(json.dumps({"spec": s.model_dump(), "compliance": fig.compliance,
                                                               "attempts": fig.attempts, "grounding": fig.grounding,
                                                               "cost_usd": fig.cost_usd, "provider": fig.provider,
                                                               "model": fig.model, "path": fig.path}, ensure_ascii=False, indent=2), "utf-8")
        v = fig.compliance or {}
        print(f"[{s.key}] {fig.path} | attempts {len(fig.attempts)} | ok={v.get('ok')} format_ok={v.get('format_ok')} "
              f"found={len(v.get('labels_found') or [])}/{v.get('n_labels')} missing={len(v.get('labels_missing') or [])} "
              f"misspelled={len(v.get('misspelled') or [])} prohibited={v.get('prohibited_elements')} | ${fig.cost_usd:.3f}")
    print(f"image cost: ${total:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
