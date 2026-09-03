"""Step 7 — compose: sections (Sonnet, anchored claims) → HTML (Jinja2) → PDF (weasyprint) → Markdown.

The sections call writes the dossier's prose in the audience's register from
the analysis, the tables and the figure captions; each paragraph may carry
claims with verbatim anchors, which pass the same wall as table anchors
(failed anchors are dropped; the sentence stays, unfootnoted, and is counted).
"""
from __future__ import annotations

import html
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.dossier import events
from src.dossier.common import AUDIENCE_REGISTER, analysis_prose, compact_profiles, corpus_text, job_dir
from src.dossier.llm import call_json
from src.dossier.schemas import Anchor, Claim, DossierJob, Section, Sections
from src.dossier.walls import NormalizedCorpus, verify_anchor
from src.sources.schemas import Document

logger = logging.getLogger(__name__)

STEP = "compose"
TEMPLATES_DIR = Path(__file__).parent / "templates"
CORPUS_IN_PROMPT_MAX_CHARS = 500_000

ANCHOR_SCHEMA = {"type": "object", "required": ["doc_key", "quote"], "additionalProperties": False,
                 "properties": {"doc_key": {"type": "string"}, "quote": {"type": "string", "description": "verbatim from the document text, 40-200 chars"}}}
SECTION_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["heading", "paragraphs", "claims", "table_keys", "figure_keys"],
    "properties": {
        "heading": {"type": "string"},
        "paragraphs": {"type": "array", "minItems": 1, "maxItems": 6, "items": {"type": "string"},
                       "description": "the section's prose; mark a footnoted claim by writing {{n}} right after its sentence, where n is the 1-based index into this section's claims"},
        "claims": {"type": "array", "maxItems": 8,
                   "items": {"type": "object", "additionalProperties": False, "required": ["text", "anchor"],
                             "properties": {"text": {"type": "string", "description": "the claim in one sentence"}, "anchor": ANCHOR_SCHEMA}}},
        "table_keys": {"type": "array", "items": {"type": "string"}, "description": "tables to place at the end of this section"},
        "figure_keys": {"type": "array", "items": {"type": "string"}, "description": "figures to place in this section"},
    },
}
SECTIONS_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["title", "subtitle", "executive_summary", "sections", "conclusion"],
    "properties": {
        "title": {"type": "string", "description": "the dossier's title, <= 12 words, no colon-clichés"},
        "subtitle": {"type": "string", "description": "one line that says what the reader gets"},
        "executive_summary": {"type": "array", "minItems": 1, "maxItems": 3, "items": {"type": "string"}},
        "sections": {"type": "array", "minItems": 3, "maxItems": 7, "items": SECTION_SCHEMA},
        "conclusion": {"type": "array", "minItems": 1, "maxItems": 3, "items": {"type": "string"}, "description": "what this means / what to do"},
    },
}

SYSTEM = """You are the writing desk of The Analyst. You compose the dossier from the analysis, the verified tables and the
figure captions, for the stated audience. The dossier has a title, an executive summary, numbered sections and a closing
'what this means'. Prose is plain, concrete and confident; it names the documents by their authors. Claims that rest on
a specific passage carry an anchor: a quote copied character-for-character from the DOCUMENT TEXT, 40-200 characters —
a mechanical check drops anchors that are not verbatim. Mark each anchored claim in the prose with {{n}} right after
its sentence (n = the claim's 1-based position in that section's claims list). Place every table (by key) in exactly one
section and every figure (by key) in one section. Do not repeat the analysis's headings or jargon; write the dossier."""


def _user(job: DossierJob, docs: list[Document]) -> str:
    from src.dossier.plan import chosen_option

    opt = chosen_option(job)
    total = sum(d.char_count for d in docs)
    tables_desc = "\n".join(
        f"- table `{t.key}`: {t.caption} — columns: {', '.join(t.columns)}; rows: "
        + "; ".join((r.cells[0].value if r.cells else "?") for r in t.rows) + (f" — note: {t.note}" if t.note else "")
        for t in job.tables) or "(no tables survived the wall)"
    figs_desc = "\n".join(f"- figure `{f.key}` ({f.status}): {f.caption}" for f in job.figures) or "(no figures)"
    shape = " / ".join(opt.output_shape.sections) if opt and opt.output_shape.sections else "(free)"
    corpus_part = (f"DOCUMENT TEXT (copy anchors from here):\n\n{corpus_text(docs)}" if total <= CORPUS_IN_PROMPT_MAX_CHARS
                   else "DOCUMENT TEXT: too large to include; take anchors only from the verified anchors in the profiles.")
    return (
        f"ANGLE: {opt.title if opt else job.options.intent}\n{opt.telling if opt else ''}\n"
        f"AUDIENCE: {job.options.audience} — {AUDIENCE_REGISTER.get(job.options.audience, '')}\n"
        f"Section headings suggested by the brief: {shape}\n\nTABLES (verified, place each once):\n{tables_desc}\n\n"
        f"FIGURES (place each once):\n{figs_desc}\n\nANALYSIS PROSE:\n{analysis_prose(job)}\n\n"
        f"RECONNAISSANCE PROFILES:\n{compact_profiles(job.profiles)}\n\n{corpus_part}"
    )


def write_sections(job: DossierJob, docs: list[Document]) -> Sections:
    raw, _ = call_json(job.id, STEP, label="dossier sections", system=SYSTEM, user=_user(job, docs),
                       tool_name="record_dossier", schema=SECTIONS_SCHEMA, model_cls=None, max_tokens=16000)
    raw = raw or {}
    corpus = NormalizedCorpus({d.key: d.text for d in docs})
    sections: list[Section] = []
    unanchored = 0
    for i, s in enumerate(raw.get("sections", []), start=1):
        claims: list[Claim] = []
        for c in s.get("claims", []) or []:
            anchor = None
            try:
                a = c.get("anchor") or {}
                anchor = verify_anchor(Anchor(doc_key=str(a.get("doc_key", "")), quote=str(a.get("quote", ""))), corpus)
            except Exception:
                anchor = None
            if anchor is None:
                unanchored += 1
            claims.append(Claim(text=str(c.get("text", "")), anchor=anchor))
        sections.append(Section(number=i, heading=str(s.get("heading", f"Section {i}")),
                                paragraphs=[str(p) for p in s.get("paragraphs", [])],
                                claims=claims, table_keys=[str(k) for k in s.get("table_keys", []) or []],
                                figure_keys=[str(k) for k in s.get("figure_keys", []) or []]))
    out = Sections(title=str(raw.get("title") or job.options.intent or "Dossier"), subtitle=str(raw.get("subtitle", "")),
                   executive_summary=[str(p) for p in raw.get("executive_summary", [])], sections=sections,
                   conclusion=[str(p) for p in raw.get("conclusion", [])], claims_unanchored=unanchored)
    anchored = sum(1 for s in sections for c in s.claims if c.anchor)
    events.emit(job.id, "note", phase=STEP, detail=f"anchor wall (sections): {anchored} claims anchored, {unanchored} left unfootnoted",
                payload_json={"claims_anchored": anchored, "claims_unanchored": unanchored})
    return out


# ── Rendering ────────────────────────────────────────────────────────────

_CLAIM_MARK = re.compile(r"\{\{\s*(\d+)\s*\}\}")


def _render_context(job: DossierJob, docs: list[Document], figure_src: str) -> dict:
    s = job.sections or Sections(title="Dossier")
    doc_by_key = {d.key: d for d in docs}
    tables_by_key = {t.key: t for t in job.tables}
    figures_by_key = {f.key: f for f in job.figures}
    footnotes: list[dict] = []
    fn_index: dict[tuple[str, str], int] = {}

    def footnote(anchor: Anchor) -> int:
        k = (anchor.doc_key, anchor.quote)
        if k not in fn_index:
            d = doc_by_key.get(anchor.doc_key)
            fn_index[k] = len(footnotes) + 1
            footnotes.append({"n": fn_index[k], "doc_key": anchor.doc_key, "quote": anchor.quote,
                              "doc_label": d.label() if d else anchor.doc_key})
        return fn_index[k]

    placed_tables, placed_figures = set(), set()
    rendered_sections = []
    table_counter = figure_counter = 0
    for sec in s.sections:
        paras = []
        for p in sec.paragraphs:
            def repl(m: re.Match) -> str:
                idx = int(m.group(1)) - 1
                if 0 <= idx < len(sec.claims) and sec.claims[idx].anchor:
                    return f'<sup class="fn">{footnote(sec.claims[idx].anchor)}</sup>'
                return ""
            safe = html.escape(p)
            paras.append(_CLAIM_MARK.sub(repl, safe))
        # claims never referenced in the prose still get their anchors listed
        for c in sec.claims:
            if c.anchor:
                footnote(c.anchor)
        sec_tables = []
        for key in sec.table_keys:
            t = tables_by_key.get(key)
            if t and key not in placed_tables:
                placed_tables.add(key)
                table_counter += 1
                sec_tables.append(_table_ctx(t, table_counter, footnote))
        sec_figs = []
        for key in sec.figure_keys:
            f = figures_by_key.get(key)
            if f and key not in placed_figures:
                placed_figures.add(key)
                figure_counter += 1
                sec_figs.append(_figure_ctx(f, figure_counter, figure_src))
        rendered_sections.append({"number": sec.number, "heading": sec.heading, "rendered_paragraphs": paras,
                                  "tables": sec_tables, "figures": sec_figs})
    # anything the writer forgot to place lands in the last section
    if rendered_sections:
        last = rendered_sections[-1]
        for t in job.tables:
            if t.key not in placed_tables:
                table_counter += 1
                last["tables"].append(_table_ctx(t, table_counter, footnote))
        for f in job.figures:
            if f.key not in placed_figures:
                figure_counter += 1
                last["figures"].append(_figure_ctx(f, figure_counter, figure_src))

    totals = job.totals.model_dump()
    totals["minutes"] = round((totals.get("duration_ms") or 0) / 60000, 1)
    steps = _steps_ctx(job)
    engines = []
    if job.plan:
        for p in job.plan.phases:
            ph = job.analysis.get(str(p.phase_number), {})
            models = sorted({x.get("model", "") for x in ph.get("passes", []) if x.get("model")})
            engines.append({"phase": p.phase_number, "engine": p.engine_name or p.engine_key, "depth": p.depth,
                            "passes": len(ph.get("passes", [])) or p.passes, "model": ", ".join(models) or "claude-sonnet-4-6", "why": p.why})
    walls = []
    dropped_rows = sum(t.rows_dropped for t in job.tables)
    if job.tables:
        walls.append(f"{sum(len(t.rows) for t in job.tables)} table rows kept, {dropped_rows} dropped for unverifiable anchors")
    if s.claims_unanchored:
        walls.append(f"{s.claims_unanchored} prose claims left unfootnoted")
    return {
        "s": {"title": s.title, "subtitle": s.subtitle, "executive_summary": s.executive_summary,
              "sections": rendered_sections, "conclusion": s.conclusion},
        "meta": {"date": datetime.utcnow().strftime("%d %B %Y"), "audience": job.options.audience,
                 "depth": job.options.depth, "job_id": job.id},
        "docs": [{"key": d.key, "label": d.label(), "publication": d.publication, "char_count": d.char_count} for d in docs],
        "footnotes": footnotes, "steps": steps, "engines": engines,
        "strategy": job.plan.strategy_rationale if job.plan else "",
        "alternatives": job.plan.alternatives_considered if job.plan else [],
        "totals": totals, "walls": "; ".join(walls),
    }


def _table_ctx(t, index: int, footnote) -> dict:
    rows = []
    for r in t.rows:
        cells = []
        for c in r.cells:
            cells.append({"value": c.value, "fn": footnote(c.anchor) if c.anchor else None})
        rows.append({"cells": cells})
    return {"index": index, "key": t.key, "caption": t.caption, "columns": t.columns, "rows": rows, "note": t.note}


def _figure_ctx(f, index: int, figure_src: str) -> dict:
    src = None
    if f.status == "generated" and f.path:
        src = figure_src.format(key=f.key)
    return {"index": index, "key": f.key, "caption": f.caption, "src": src, "status": f.status, "note": f.note}


def _steps_ctx(job: DossierJob) -> list[dict]:
    names = [("reconnaissance", "Read every document; profiled each (thesis, method, anchored claims) and mapped the corpus."),
             ("brief", "Proposed three angles with engines, cost and shape; one was chosen."),
             ("plan", "Turned the angle into an ordered engine sequence for the executor (depth policy enforced)."),
             ("analysis", "Ran the engines through the executor; each phase read the previous phases' prose."),
             ("tables", "Extracted evidence tables; every row verified against verbatim anchors."),
             ("figures", "Planned figures as depictable scenes; rendered through the image pipeline."),
             ("compose", "Wrote the dossier in the audience's register with footnoted anchors; rendered HTML, PDF and Markdown."),
             ("receipts", "Totalled every model and image call.")]
    by_step: dict[str, dict] = {}
    for r in job.receipts:
        b = by_step.setdefault(r.step, {"calls": 0, "in": 0, "out": 0, "cost": 0.0})
        b["calls"] += 1
        b["in"] += r.input_tokens
        b["out"] += r.output_tokens
        b["cost"] += r.cost_usd
    durations = job.totals.step_durations_ms or {}
    out = []
    for key, what in names:
        b = by_step.get(key, {"calls": 0, "in": 0, "out": 0, "cost": 0.0})
        d = durations.get(key)
        out.append({"name": key, "what": what, "calls": b["calls"],
                    "tokens": f"{b['in']:,} / {b['out']:,}" if b["calls"] else "—",
                    "cost": f"${b['cost']:.2f}" if b["calls"] else "—",
                    "time": f"{d/1000:.0f}s" if d else "—"})
    return out


def render_html(job: DossierJob, docs: list[Document], figure_src: str = "figures/{key}.png") -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=select_autoescape(["html", "j2"]))
    tpl = env.get_template("dossier.html.j2")
    return tpl.render(**_render_context(job, docs, figure_src))


def render_markdown(job: DossierJob, docs: list[Document]) -> str:
    ctx = _render_context(job, docs, "figures/{key}.png")
    s = ctx["s"]
    lines = [f"# {s['title']}", ""]
    if s["subtitle"]:
        lines += [f"*{s['subtitle']}*", ""]
    m = ctx["meta"]
    lines += [f"{m['date']} · {m['audience']} edition · {m['depth']} depth · job {m['job_id']}", ""]
    if s["executive_summary"]:
        lines += ["## Summary", ""] + [p for p in s["executive_summary"]] + [""]
    for sec in s["sections"]:
        lines += [f"## {sec['number']}. {sec['heading']}", ""]
        for p in sec["rendered_paragraphs"]:
            text = re.sub(r'<sup class="fn">(\d+)</sup>', r"[^\1]", p)
            lines += [html.unescape(text), ""]
        for t in sec["tables"]:
            lines += [f"**Table {t['index']}. {t['caption']}**", ""]
            lines.append("| " + " | ".join(t["columns"]) + " |")
            lines.append("|" + "---|" * len(t["columns"]))
            for r in t["rows"]:
                cells = [(c["value"].replace("|", "/") + (f" [^{c['fn']}]" if c["fn"] else "")) for c in r["cells"]]
                lines.append("| " + " | ".join(cells) + " |")
            if t["note"]:
                lines += ["", f"*{t['note']}*"]
            lines.append("")
        for f in sec["figures"]:
            if f["src"]:
                lines += [f"![{f['caption']}]({f['src']})", "", f"*Figure {f['index']}. {f['caption']}*", ""]
            else:
                lines += [f"*Figure {f['index']} ({f['status']}): {f['caption']}*", ""]
    if s["conclusion"]:
        lines += [f"## {len(s['sections']) + 1}. What this means", ""] + s["conclusion"] + [""]
    if ctx["footnotes"]:
        lines += ["## Anchors", ""]
        for fn in ctx["footnotes"]:
            lines.append(f"[^{fn['n']}]: {fn['doc_label']}: “{fn['quote']}”")
        lines.append("")
    lines += ["## How this was made", ""]
    for d in ctx["docs"]:
        lines.append(f"- [{d['key']}] {d['label']}" + (f" — *{d['publication']}*" if d["publication"] else ""))
    lines += ["", "| # | Step | What happened | Calls | Tokens in / out | Cost | Time |", "|---|---|---|---|---|---|---|"]
    for i, st in enumerate(ctx["steps"], start=1):
        lines.append(f"| {i} | {st['name']} | {st['what']} | {st['calls']} | {st['tokens']} | {st['cost']} | {st['time']} |")
    if ctx["engines"]:
        lines += ["", "| Phase | Engine | Depth | Passes | Model | Why |", "|---|---|---|---|---|---|"]
        for e in ctx["engines"]:
            lines.append(f"| {e['phase']} | {e['engine']} | {e['depth']} | {e['passes']} | {e['model']} | {e['why']} |")
        if ctx["strategy"]:
            lines += ["", f"*Strategy.* {ctx['strategy']}"]
    t = ctx["totals"]
    lines += ["", f"**Totals:** {t['llm_calls']} model calls, {t['input_tokens']:,} input tokens, {t['output_tokens']:,} output tokens, ${t['cost_usd']:.2f}, {t['minutes']} min."]
    if ctx["walls"]:
        lines.append(f"Walls: {ctx['walls']}")
    return "\n".join(lines) + "\n"


def render_all(job: DossierJob, docs: list[Document]) -> dict[str, str]:
    out_dir = job_dir(job.id)
    paths: dict[str, str] = {}
    html_text = render_html(job, docs)
    html_path = out_dir / "dossier.html"
    html_path.write_text(html_text, encoding="utf-8")
    paths["html"] = str(html_path)
    events.emit(job.id, "artifact", phase=STEP, detail="dossier.html written", payload_json={"kind": "dossier_html", "path": str(html_path), "url": f"/v1/dossier/jobs/{job.id}/dossier.html"})
    md_path = out_dir / "dossier.md"
    md_path.write_text(render_markdown(job, docs), encoding="utf-8")
    paths["md"] = str(md_path)
    events.emit(job.id, "artifact", phase=STEP, detail="dossier.md written", payload_json={"kind": "dossier_md", "path": str(md_path), "url": f"/v1/dossier/jobs/{job.id}/dossier.md"})
    try:
        from weasyprint import HTML

        pdf_path = out_dir / "dossier.pdf"
        HTML(string=html_text, base_url=str(out_dir)).write_pdf(str(pdf_path))
        paths["pdf"] = str(pdf_path)
        events.emit(job.id, "artifact", phase=STEP, detail="dossier.pdf written", payload_json={"kind": "dossier_pdf", "path": str(pdf_path), "url": f"/v1/dossier/jobs/{job.id}/dossier.pdf"})
    except Exception as exc:  # skip law: the PDF is optional output form
        logger.warning(f"PDF render failed: {exc}", exc_info=True)
        events.emit(job.id, "note", phase=STEP, detail=f"pdf_skipped: {exc}")
    (out_dir / "job.json").write_text(json.dumps(job.model_dump(), ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return paths


def run_compose(job: DossierJob, docs: list[Document], persist) -> tuple[Sections, dict[str, str]]:
    sections = write_sections(job, docs)
    job.sections = sections
    persist(sections=sections)
    paths = render_all(job, docs)
    return sections, paths
