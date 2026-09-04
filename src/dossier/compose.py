"""Step 8 — compose: the DRAFT written with the exhibits in hand → frames last → HTML / PDF / Markdown.

Spine-driven (pass D, DESIGN_concretization_passes §C.3):
  1. `write_body`   — one call writes every section in the spine's order with the FINISHED tables
                      (every cell) and the figures as ACTUALLY drawn (the check's `detected` sentence)
                      on the desk. Each exhibit is placed exactly once by a token `[[table:key]]` /
                      `[[figure:key]]` right after the sentence that names what the reader will see.
                      Walls: section order = spine order; every exhibit placed exactly once, never at
                      the section's end; anchors verbatim; no number the material does not carry.
                      Retry: section-scoped patches (only the failing sections are re-asked, merged,
                      re-validated); what still fails is repaired by code and recorded.
  2. `write_frames` — the executive summary and the close written LAST against the assembled body, each
                      to the job the spine declared (summary_job ≠ conclusion_job); wall: they must not
                      share their words (8-word shingles), no new numbers, one re-ask.
  3. render         — exhibits are placed at their tokens (blocks), numbered in the spine's order.

Legacy (no spine on the job): the one-call `write_sections` and end-of-section placement, unchanged.
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

from src.dossier import events, findings as ledger
from src.dossier.common import AUDIENCE_REGISTER, analysis_prose, compact_profiles, corpus_text, job_dir
from src.dossier.llm import call_json
from src.dossier.schemas import Anchor, Claim, DossierJob, ExhibitRef, Figure, Finding, Section, Sections, Table
from src.dossier.walls import (
    EXHIBIT_TOKEN, NormalizedCorpus, digit_runs, exhibit_tokens, normalize, numbers_not_in, shingle_overlap, verify_anchor,
)
from src.sources.schemas import Document

logger = logging.getLogger(__name__)

STEP = "compose"
TEMPLATES_DIR = Path(__file__).parent / "templates"
CORPUS_IN_PROMPT_MAX_CHARS = 500_000
FRAMES_MAX_OVERLAP = 0.15          # fraction of the conclusion's 8-word shingles allowed to recur in the summary

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


# ── Legacy path (no spine) ───────────────────────────────────────────────

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


# ── Pass D: the draft with the exhibits in hand ──────────────────────────

DRAFT_SYSTEM = """You are the writing desk of The Analyst. The structure editor has decided what the dossier argues (THE SPINE) and the
exhibits desks have built what it commissioned. You write the body of the dossier — the numbered sections — as a
PROOF of the spine, with the exhibits ON THE DESK. You write for the stated audience, in its register; prose is plain,
concrete and confident; it names the documents by their authors; it never repeats the analysis's headings or jargon.

The spine is law: one section per spine section, in the spine's order, with its `section_key`; each section proves
its claim and hands the reader what the spine says they need next. Each table is given whole (every cell); each
diagram is given as what it ACTUALLY shows (the checked description), not as what it was meant to show.

Exhibits: point at each one exactly once, where the reader should look, with the token `[[table:key]]` or
`[[figure:key]]` written on its own right after the sentence that names what they will see — e.g. "Table 2 decodes
the five terms the ministries use, and what each one does in practice. [[table:government_vocabulary_decoder]] Read
down the last column …". The exhibit's number is fixed (given below) — use it in the pointer sentence. The token is
never the last thing in a section: the prose continues after the exhibit and uses what it showed. Never restate a
caption or a table's note in the prose; never narrate a table's rows; never put in the prose what the reader is about
to read in the exhibit — argue from it. If a diagram does not show what its section argues, do not pretend it does:
say what it does show, and set `mismatch: true` on its exhibit_ref so the cross-check acts on it. A section whose
commissioned table could not be built carries that claim in prose.

Numbers: only numbers the documents and the analysis carry; every number in the prose must be traceable to the
material. Numbers never go in captions.

Anchors: claims that rest on a specific passage carry an anchor — a quote copied character-for-character from the
DOCUMENT TEXT, 40-200 characters, with the right doc_key; a mechanical check refuses anchors that are not verbatim,
and a cut-off fragment does not count. Mark each anchored claim in the prose with {{n}} right after its sentence
(n = the claim's 1-based position in that section's claims list). The section's planned anchors are good starting
points. Write the body only: the summary and the close are written afterwards against what you wrote."""

FRAMES_SYSTEM = """You are the writing desk of The Analyst, writing the FRAMES of a dossier whose body is finished: the title, the
subtitle, the executive summary and the closing 'what this means'. You write them against the ASSEMBLED BODY below,
never before it, and each to the job the spine declared — the summary's job and the conclusion's job are DIFFERENT and
you write each to its job and nothing else. The summary states what the body now argues, in the body's proportions,
with the body's qualifications, so a busy reader can decide without reading further; it never restates a section's
opening line. The close does its own job (a decision rule, the question to ask, what to watch) and never repeats the
summary — a mechanical check refuses a close that shares its sentences with the summary. No fact, name or number the
body does not carry; no anchors here (the body holds them). Plain, concrete, in the audience's register. Title:
<= 12 words, no colon-cliché. Then say in one line each what the summary did and what the close did."""


def draft_schema(section_keys: list[str]) -> dict:
    item = {
        "type": "object", "additionalProperties": False,
        "required": ["section_key", "heading", "paragraphs", "claims", "exhibit_refs"],
        "properties": {
            "section_key": {"type": "string", "enum": section_keys},
            "heading": {"type": "string", "description": "<= 70 chars; the spine's heading or a sharper one"},
            "paragraphs": {"type": "array", "minItems": 1, "maxItems": 6, "items": {"type": "string"},
                           "description": "the prose; {{n}} after an anchored sentence; [[table:key]] / [[figure:key]] right after the pointer sentence"},
            "claims": {"type": "array", "maxItems": 8,
                       "items": {"type": "object", "additionalProperties": False, "required": ["text", "anchor"],
                                 "properties": {"text": {"type": "string"}, "anchor": ANCHOR_SCHEMA}}},
            "exhibit_refs": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["key", "sentence", "mismatch"],
                             "properties": {"key": {"type": "string"}, "sentence": {"type": "string", "description": "the pointer sentence, verbatim from the paragraphs"},
                                            "mismatch": {"type": "boolean", "description": "true when the picture does not show what the section argues"}}}},
        },
    }
    return {"type": "object", "additionalProperties": False, "required": ["sections"],
            "properties": {"sections": {"type": "array", "minItems": 1, "maxItems": len(section_keys), "items": item}}}


FRAMES_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["title", "subtitle", "executive_summary", "conclusion", "summary_job_met", "conclusion_job_met"],
    "properties": {
        "title": {"type": "string"}, "subtitle": {"type": "string", "description": "one line that says what the reader gets"},
        "executive_summary": {"type": "array", "minItems": 1, "maxItems": 3, "items": {"type": "string"}},
        "conclusion": {"type": "array", "minItems": 1, "maxItems": 3, "items": {"type": "string"}},
        "summary_job_met": {"type": "string"}, "conclusion_job_met": {"type": "string"},
    },
}


def exhibit_numbers(job: DossierJob) -> dict[str, int]:
    """Exhibit numbers fixed BEFORE the draft: tables and figures numbered in the spine's section order
    (the section-order and token-once walls make that the reading order)."""
    order = {s.key: i for i, s in enumerate(job.spine.sections)} if job.spine else {}
    nums: dict[str, int] = {}
    for kind, items in (("table", job.tables), ("figure", [f for f in job.figures if f.status == "generated"])):
        ranked = sorted(items, key=lambda x: order.get(getattr(x, "section_key", ""), 99))
        for n, x in enumerate(ranked, start=1):
            nums[f"{kind}:{x.key}"] = n
    return nums


def expected_exhibits(job: DossierJob) -> dict[str, str]:
    """{key: section_key} for every exhibit the draft must place exactly once (generated figures, verified tables)."""
    out: dict[str, str] = {}
    for t in job.tables:
        out[f"table:{t.key}"] = t.section_key
    for f in job.figures:
        if f.status == "generated":
            out[f"figure:{f.key}"] = f.section_key
    return out


def _tables_full(job: DossierJob, nums: dict[str, int]) -> str:
    parts = []
    for t in job.tables:
        head = (f"### Table {nums.get('table:' + t.key, '?')} — key `{t.key}` — for section `{t.section_key or '?'}`\n"
                f"caption: {t.caption}\nproves: {t.proves}\ncolumns: | " + " | ".join(t.columns) + " |")
        rows = []
        for r in t.rows:
            cells = []
            for c in r.cells:
                cells.append((c.value or "").replace("|", "/") + (f" ⟨{c.anchor.doc_key}⟩" if c.anchor else ""))
            rows.append("| " + " | ".join(cells) + " |")
        parts.append(head + "\n" + "\n".join(rows) + (f"\nnote: {t.note}" if t.note else ""))
    return "\n\n".join(parts) if parts else "(no tables)"


def _figures_full(job: DossierJob, nums: dict[str, int]) -> str:
    parts = []
    for f in job.figures:
        if f.status != "generated":
            parts.append(f"- figure `{f.key}` for section `{f.section_key or '?'}`: NOT AVAILABLE ({f.status}: {f.note[:120]}) — do not point at it; carry the point in prose")
            continue
        parts.append(
            f"### Figure {nums.get('figure:' + f.key, '?')} — key `{f.key}` — for section `{f.section_key or '?'}`\n"
            f"title: {f.title}\nformat: {f.visual_format} ({f.primitive})\ncaption (fixed; do not restate it): {f.caption}\n"
            f"meant to show: {f.picture_shows or f.caption_says}\nACTUALLY SHOWS (checked): {f.detected}\n"
            f"check: {'passed' if f.checked_ok else ('failed — ' + '; '.join((f.compliance or {}).get('issues', [])[:3]) if f.checked_ok is False else 'not run')}"
        )
    return "\n\n".join(parts) if parts else "(no figures)"


def _spine_text(job: DossierJob, nums: dict[str, int]) -> str:
    sp = job.spine
    by_section_t = {t.section_key: t for t in job.tables}
    by_section_f = {f.section_key: f for f in job.figures if f.status == "generated"}
    lines = [f"THESIS: {sp.thesis}", f"HANDLE: {sp.handle}", f"READER'S QUESTION: {sp.reader_question}", f"THROUGH-LINE: {sp.through_line}",
             f"(The summary's job — written later, not by you: {sp.summary_job}. The close's job: {sp.conclusion_job}.)", ""]
    for i, s in enumerate(sp.sections, start=1):
        ex = []
        if s.key in by_section_t:
            ex.append(f"Table {nums.get('table:' + by_section_t[s.key].key, '?')} `[[table:{by_section_t[s.key].key}]]`")
        if s.key in by_section_f:
            ex.append(f"Figure {nums.get('figure:' + by_section_f[s.key].key, '?')} `[[figure:{by_section_f[s.key].key}]]`")
        if (s.table and s.key not in by_section_t) or (s.figure and s.key not in by_section_f):
            ex.append("(a commissioned exhibit could not be built — carry the claim in prose)")
        anchors = "; ".join(f"[{a.doc_key}] “{a.quote}”" for a in s.anchors_planned) or "(none)"
        lines.append(f"{i}. section_key `{s.key}` — {s.heading}\n   CLAIM: {s.claim}\n   reader needs next: {s.reader_needs_next}\n"
                     f"   evidence: {s.evidence_kind}; exhibits to place here: {', '.join(ex) or 'none'}\n   planned anchors: {anchors}")
    return "\n".join(lines)


def _draft_user(job: DossierJob, docs: list[Document], nums: dict[str, int]) -> str:
    from src.dossier.plan import chosen_option

    opt = chosen_option(job)
    total = sum(d.char_count for d in docs)
    corpus_part = (f"DOCUMENT TEXT (copy anchors from here):\n\n{corpus_text(docs)}" if total <= CORPUS_IN_PROMPT_MAX_CHARS
                   else "DOCUMENT TEXT: too large to include; take anchors only from the verified anchors in the profiles and the spine.")
    findings_txt = "\n".join(f"- {f.kind} [{f.where.section_key or ''}]: {f.note}" for f in ledger.open_findings(job.findings)) or "(none)"
    return (
        f"ANGLE: {opt.title if opt else job.options.intent}\nAUDIENCE: {job.options.audience} — {AUDIENCE_REGISTER.get(job.options.audience, '')}\n\n"
        f"THE SPINE (write these sections, in this order, one claim each):\n{_spine_text(job, nums)}\n\n"
        f"TABLES ON THE DESK (final; every cell; ⟨doc⟩ marks an anchored cell):\n{_tables_full(job, nums)}\n\n"
        f"DIAGRAMS ON THE DESK (as actually drawn):\n{_figures_full(job, nums)}\n\n"
        f"OPEN FINDINGS FROM THE EXHIBIT DESKS:\n{findings_txt}\n\n"
        f"ANALYSIS PROSE:\n{analysis_prose(job)}\n\nRECONNAISSANCE PROFILES:\n{compact_profiles(job.profiles)}\n\n{corpus_part}"
    )


_CLAIM_MARK = re.compile(r"\{\{\s*(\d+)\s*\}\}")
_EXHIBIT_MENTION = re.compile(r"\b(Table|Figure)\s+\d+\b")


def _prose_only(text: str) -> str:
    """Paragraph text without claim marks, exhibit tokens and 'Table N' mentions (for the number wall)."""
    return _EXHIBIT_MENTION.sub("", EXHIBIT_TOKEN.sub("", _CLAIM_MARK.sub("", text or "")))


def _coerce_body(raw: dict, corpus: NormalizedCorpus) -> tuple[list[Section], dict[str, list[str]]]:
    """Sections from the tool answer with anchors verified in place. Returns (sections, anchor errors per key)."""
    sections: list[Section] = []
    anchor_errs: dict[str, list[str]] = {}
    for s in (raw or {}).get("sections", []) or []:
        if not isinstance(s, dict):
            continue
        key = str(s.get("section_key", "")).strip()
        claims: list[Claim] = []
        for k, c in enumerate(s.get("claims", []) or [], start=1):
            anchor = None
            a = (c or {}).get("anchor") or {}
            quote = str(a.get("quote", "")).strip()
            try:
                anchor = verify_anchor(Anchor(doc_key=str(a.get("doc_key", "")), quote=quote), corpus) if quote else None
            except Exception:
                anchor = None
            if anchor is None:
                anchor_errs.setdefault(key, []).append(f"claim {k}: anchor is not verbatim in any document — “{quote[:90]}”; copy the exact sentence or drop the anchor")
            elif anchor.trimmed:
                anchor_errs.setdefault(key, []).append(f"claim {k}: anchor only matched as a cut-off prefix — “{anchor.quote[:90]}”; copy the whole sentence exactly (a fragment is refused)")
            claims.append(Claim(text=str((c or {}).get("text", "")), anchor=anchor))
        refs = [ExhibitRef(key=str(r.get("key", "")).strip(), sentence=str(r.get("sentence", "")).strip(), mismatch=bool(r.get("mismatch")))
                for r in (s.get("exhibit_refs") or []) if isinstance(r, dict) and str(r.get("key", "")).strip()]
        sections.append(Section(heading=str(s.get("heading", "")).strip() or key, paragraphs=[str(p) for p in s.get("paragraphs", []) or []],
                                claims=claims, section_key=key, exhibit_refs=refs))
    return sections, anchor_errs


def validate_body(sections: list[Section], job: DossierJob, material_norm: str, anchor_errs: Optional[dict[str, list[str]]] = None) -> tuple[dict[str, list[str]], list[str]]:
    """The draft walls. Returns (errors per section_key, whole-draft errors)."""
    per: dict[str, list[str]] = {}
    glob: list[str] = []
    spine_keys = [s.key for s in job.spine.sections]
    got = [s.section_key for s in sections]
    for k in spine_keys:
        if k not in got:
            glob.append(f"section `{k}` is missing")
            per.setdefault(k, []).append("this section was not written; write it (its claim is in the spine)")
    for s in sections:
        if s.section_key not in spine_keys:
            per.setdefault(s.section_key or "?", []).append(f"section_key {s.section_key!r} is not in the spine")
    if [k for k in got if k in spine_keys] != [k for k in spine_keys if k in got]:
        glob.append("sections are not in the spine's order")
    expected = expected_exhibits(job)
    seen: dict[str, list[str]] = {}
    for s in sections:
        for pi, p in enumerate(s.paragraphs):
            for kind, key in exhibit_tokens(p):
                seen.setdefault(f"{kind}:{key}", []).append(s.section_key)
        toks = exhibit_tokens(" ".join(s.paragraphs))
        if toks and s.paragraphs:
            tail = EXHIBIT_TOKEN.sub("", s.paragraphs[-1]).strip()
            last = s.paragraphs[-1].rstrip()
            if last.endswith("]]") and (not tail or last.rfind("]]") > len(last) - 4):
                per.setdefault(s.section_key, []).append("an exhibit token is the last thing in the section — the prose must continue after the exhibit and use what it showed")
        for tk in set(f"{k}:{v}" for k, v in toks):
            if tk not in expected:
                per.setdefault(s.section_key, []).append(f"token [[{tk}]] refers to no exhibit on the desk — remove it (available: {', '.join(sorted(expected)) or 'none'})")
        errs = per.setdefault(s.section_key, [])
        if not s.paragraphs:
            errs.append("no paragraphs")
        new_nums = sorted({n for p in s.paragraphs for n in numbers_not_in(_prose_only(p), material_norm)})
        if new_nums:
            errs.append("numbers the material does not carry: " + ", ".join(new_nums[:8]) + " — use only numbers the documents, tables or analysis state, or remove them")
        for pi, p in enumerate(s.paragraphs):
            for m in _CLAIM_MARK.finditer(p):
                if not (1 <= int(m.group(1)) <= len(s.claims)):
                    errs.append(f"paragraph {pi + 1} marks claim {{{{{m.group(1)}}}}} but the section lists {len(s.claims)} claims")
                    break
    for tk, where in seen.items():
        if tk in expected and len(where) > 1:
            for w in where[1:]:
                per.setdefault(w, []).append(f"[[{tk}]] is placed twice; it belongs once, in section `{expected[tk]}`")
    for tk, sk in expected.items():
        if tk not in seen:
            per.setdefault(sk, []).append(f"[[{tk}]] was never placed — place it in this section right after the sentence that says what the reader will see")
    for k, errs in (anchor_errs or {}).items():
        per.setdefault(k, []).extend(errs)
    return {k: v for k, v in per.items() if v}, glob


def _patch_tail(per: dict[str, list[str]], glob: list[str]) -> str:
    lines = ["---", "THE DRAFT WAS JUDGED WHOLE; ONLY THESE SECTIONS FAILED THE WALL. Return ONLY replacement entries for the sections "
             "listed (same `section_key`, corrected, complete — paragraphs, claims, exhibit_refs); every other section is kept as "
             "you wrote it. A mistake you fix once must stay fixed."]
    for k, errs in per.items():
        lines.append(f"- section `{k}`: " + " | ".join(errs))
    if glob:
        lines.append("Whole-draft notes: " + " | ".join(glob))
    return "\n".join(lines)


def _repair_body_by_code(sections: list[Section], job: DossierJob, per: dict[str, list[str]]) -> tuple[list[Section], list[str], list[Finding]]:
    """Shape trivia repaired by code after the patch, every repair recorded; findings for what a judge must see."""
    notes: list[str] = []
    minted: list[Finding] = []
    spine_keys = [s.key for s in job.spine.sections]
    by_key: dict[str, Section] = {}
    for s in sections:
        if s.section_key in spine_keys and s.section_key not in by_key:
            by_key[s.section_key] = s
        else:
            notes.append(f"section {s.section_key!r} dropped (not in the spine, or a duplicate)")
    ordered = [by_key[k] for k in spine_keys if k in by_key]
    if [s.section_key for s in sections if s.section_key in by_key] != [s.section_key for s in ordered]:
        notes.append("sections re-ordered to the spine's order by code")
    expected = expected_exhibits(job)
    seen: set[str] = set()
    for s in ordered:
        new_pars = []
        for p in s.paragraphs:
            def repl(m: re.Match) -> str:
                tk = f"{m.group(1).lower()}:{m.group(2)}"
                if tk not in expected:
                    notes.append(f"section {s.section_key}: token [[{tk}]] removed (no such exhibit)")
                    return ""
                if tk in seen:
                    notes.append(f"section {s.section_key}: duplicate token [[{tk}]] removed")
                    return ""
                seen.add(tk)
                return m.group(0)
            new_pars.append(EXHIBIT_TOKEN.sub(repl, p))
        s.paragraphs = [p for p in new_pars if p.strip()] or s.paragraphs
    for tk, sk in expected.items():
        if tk in seen:
            continue
        target = by_key.get(sk) or (ordered[-1] if ordered else None)
        if target is None:
            continue
        kind, key = tk.split(":", 1)
        at = 0 if len(target.paragraphs) == 1 else min(1, len(target.paragraphs) - 1)
        target.paragraphs[at] = target.paragraphs[at].rstrip() + f" [[{kind}:{key}]]"
        notes.append(f"section {target.section_key}: [[{tk}]] inserted by code after paragraph {at + 1} (the writer never placed it)")
        minted.append(ledger.mint("exhibit_unpointed", where={"section_key": target.section_key, **({"table_key": key} if kind == "table" else {"figure_key": key})},
                                  source="wall", affordance="rewrite_paragraph",
                                  note=f"The writer never pointed at this {kind}; the desk placed it in its section by the spine's assignment, but no sentence tells the reader what they will see. Cure: rewrite the paragraph with a pointer sentence."))
    # anchors: a still-trimmed anchor is recorded but does not footnote the claim; a miss stays unfootnoted
    for s in ordered:
        for k, c in enumerate(s.claims, start=1):
            if c.anchor is not None and c.anchor.trimmed:
                minted.append(ledger.mint("anchor_fragment", where={"section_key": s.section_key, "anchor_n": k}, source="wall", affordance="reanchor_claim",
                                          note=f"The anchor for claim {k} only matched as a cut-off prefix (“{c.anchor.quote[:80]}”); the reader would see a fragment. The claim is left unfootnoted. Cure: re-anchor it to the whole sentence.",
                                          quote=c.text[:200]))
                notes.append(f"section {s.section_key}: claim {k} left unfootnoted (anchor was a fragment)")
        for r in s.exhibit_refs:
            if r.mismatch and r.key:
                fk = r.key.split(":")[-1]
                minted.append(ledger.mint("figure_depicts_other", where={"section_key": s.section_key, "figure_key": fk}, source="wall", affordance="revise_figure_spec",
                                          note=f"The writer flagged that this exhibit does not show what the section argues ({r.sentence[:160]}). Cure: re-specify the picture from the section's claim.",
                                          quote=r.sentence[:200]))
    return ordered, notes, minted


def write_body(job: DossierJob, docs: list[Document], persist=None) -> tuple[list[Section], list[str]]:
    """The body call, the walls, one section-scoped patch round, the code repairs."""
    corpus = NormalizedCorpus({d.key: d.text for d in docs})
    material_norm = normalize(analysis_prose(job) + "\n" + compact_profiles(job.profiles) + "\n"
                              + "\n".join(c.value for t in job.tables for r in t.rows for c in r.cells)
                              + "\n" + "\n".join(f.caption + " " + json.dumps(f.data) for f in job.figures)) + "\n" + "\n".join(corpus.texts.values())
    nums = exhibit_numbers(job)
    keys = [s.key for s in job.spine.sections]
    user = _draft_user(job, docs, nums)
    raw, _ = call_json(job.id, STEP, label=f"draft body ({len(keys)} sections, exhibits on the desk)", system=DRAFT_SYSTEM, user=user,
                       tool_name="record_draft", schema=draft_schema(keys), model_cls=None, max_tokens=16000, cache=True)
    sections, anchor_errs = _coerce_body(raw, corpus)
    per, glob = validate_body(sections, job, material_norm, anchor_errs)
    events.emit(job.id, "note", phase=STEP, detail=f"draft wall: {len(sections)} sections, {len(per)} with errors" + (f"; whole: {' | '.join(glob)}" if glob else ""),
                payload_json={"kind": "draft_wall", "errors": per, "global": glob})
    if per:
        wanted = set(per.keys()) & set(keys)
        raw2, _ = call_json(job.id, STEP, label=f"draft patch ({len(wanted)} sections)", system=DRAFT_SYSTEM, user=user,
                            user_tail=_patch_tail({k: v for k, v in per.items() if k in wanted}, glob), tool_name="record_draft_patch",
                            schema=draft_schema(sorted(wanted)), model_cls=None, max_tokens=12000, cache=True)
        patched, anchor_errs2 = _coerce_body(raw2, corpus)
        by_key = {s.section_key: s for s in patched if s.section_key in wanted}
        merged = [by_key.get(s.section_key, s) for s in sections]
        for k in wanted:
            if k not in {s.section_key for s in merged} and k in by_key:
                merged.append(by_key[k])
        sections = merged
        per, glob = validate_body(sections, job, material_norm, {k: v for k, v in anchor_errs2.items() if k in wanted})
        events.emit(job.id, "note", phase=STEP, detail=f"draft wall after patch: {len(per)} sections still failing" + (f"; whole: {' | '.join(glob)}" if glob else ""),
                    payload_json={"kind": "draft_wall", "errors": per, "global": glob, "after_patch": True})
    sections, notes, minted = _repair_body_by_code(sections, job, per)
    for i, s in enumerate(sections, start=1):
        s.number = i
        s.table_keys = [k for kind, k in exhibit_tokens(" ".join(s.paragraphs)) if kind == "table"]
        s.figure_keys = [k for kind, k in exhibit_tokens(" ".join(s.paragraphs)) if kind == "figure"]
    ledger.append(job, minted, persist)
    for n in notes:
        events.emit(job.id, "note", phase=STEP, detail=f"draft repair: {n}", payload_json={"kind": "draft_repair"})
    return sections, notes


# ── Frames (summary + conclusion), written last ─────────────────────────

def body_markdown(job: DossierJob, sections: list[Section], nums: dict[str, int]) -> str:
    """The assembled body as the frames writer reads it: prose with the exhibits' captions in place."""
    tables = {t.key: t for t in job.tables}
    figures = {f.key: f for f in job.figures}
    out = []
    for s in sections:
        out.append(f"## {s.number}. {s.heading}")
        for p in s.paragraphs:
            def repl(m: re.Match) -> str:
                kind, key = m.group(1).lower(), m.group(2)
                if kind == "table" and key in tables:
                    t = tables[key]
                    return f"\n\n[Table {nums.get('table:' + key, '?')}. {t.caption} — {len(t.rows)} rows: " + "; ".join((r.cells[0].value if r.cells else "") for r in t.rows) + "]\n\n"
                if kind == "figure" and key in figures:
                    return f"\n\n[Figure {nums.get('figure:' + key, '?')}. {figures[key].caption}]\n\n"
                return ""
            out.append(EXHIBIT_TOKEN.sub(repl, _CLAIM_MARK.sub("", p)))
        out.append("")
    return "\n".join(out)


def validate_frames(raw: dict, body_norm: str) -> list[str]:
    errs = []
    summary = [str(p) for p in (raw or {}).get("executive_summary", []) or []]
    conclusion = [str(p) for p in (raw or {}).get("conclusion", []) or []]
    if not summary or not conclusion:
        return ["executive_summary and conclusion are both required"]
    overlap = shingle_overlap(" ".join(conclusion), " ".join(summary))
    if overlap > FRAMES_MAX_OVERLAP:
        errs.append(f"the close shares {overlap:.0%} of its 8-word phrases with the summary — they do different jobs; rewrite the close to its own job")
    for a in summary:
        for b in conclusion:
            if normalize(a) == normalize(b):
                errs.append("a summary paragraph and a conclusion paragraph are identical")
    new_nums = sorted({n for p in summary + conclusion for n in numbers_not_in(p, body_norm)})
    if new_nums:
        errs.append("numbers the body does not carry: " + ", ".join(new_nums[:8]))
    title = str((raw or {}).get("title", ""))
    if len(title.split()) > 14:
        errs.append("title must be at most 12 words")
    return errs


def write_frames(job: DossierJob, sections: list[Section]) -> dict[str, Any]:
    sp = job.spine
    nums = exhibit_numbers(job)
    body = body_markdown(job, sections, nums)
    body_norm = normalize(body + " " + " ".join(c.value for t in job.tables for r in t.rows for c in r.cells))
    user = (f"AUDIENCE: {job.options.audience} — {AUDIENCE_REGISTER.get(job.options.audience, '')}\n"
            f"THESIS: {sp.thesis}\nHANDLE: {sp.handle}\nREADER'S QUESTION: {sp.reader_question}\n"
            f"THE SUMMARY'S JOB: {sp.summary_job}\nTHE CLOSE'S JOB: {sp.conclusion_job}\n\nTHE ASSEMBLED BODY:\n\n{body}")
    raw, _ = call_json(job.id, STEP, label="frames: summary + close against the body", system=FRAMES_SYSTEM, user=user,
                       tool_name="record_frames", schema=FRAMES_SCHEMA, model_cls=None, max_tokens=6000, cache=True)
    errs = validate_frames(raw, body_norm)
    if errs:
        events.emit(job.id, "note", phase=STEP, detail="frames wall: " + " | ".join(errs), payload_json={"kind": "frames_wall", "errors": errs})
        raw2, _ = call_json(job.id, STEP, label="frames (re-ask)", system=FRAMES_SYSTEM, user=user,
                            user_tail="---\nYOUR FRAMES FAILED THE WALL: " + " | ".join(errs) + "\nReturn the complete corrected frames.",
                            tool_name="record_frames", schema=FRAMES_SCHEMA, model_cls=None, max_tokens=6000, cache=True)
        errs2 = validate_frames(raw2, body_norm)
        if len(errs2) <= len(errs):
            raw = raw2
        if errs2:
            events.emit(job.id, "note", phase=STEP, detail="frames wall after re-ask: " + " | ".join(errs2) + " — kept; the cross-check will see it",
                        payload_json={"kind": "frames_wall", "errors": errs2, "after_reask": True})
    return raw or {}


def compose_draft(job: DossierJob, docs: list[Document], persist=None) -> Sections:
    """Pass D: body with the exhibits in hand, then the frames against the body."""
    sections, notes = write_body(job, docs, persist)
    draft = Sections(title=job.spine.handle or job.options.intent or "Dossier", sections=sections,
                     claims_unanchored=sum(1 for s in sections for c in s.claims if c.anchor is None or c.anchor.trimmed),
                     spine_round_consumed=job.spine.round)
    job.sections = draft
    if persist is not None:
        persist(sections=draft)   # checkpoint: the body is on the record before the frames are bought
    anchored = sum(1 for s in sections for c in s.claims if c.anchor and not c.anchor.trimmed)
    events.emit(job.id, "note", phase=STEP, detail=f"anchor wall (draft): {anchored} claims anchored, {draft.claims_unanchored} left unfootnoted",
                payload_json={"claims_anchored": anchored, "claims_unanchored": draft.claims_unanchored})
    nums = exhibit_numbers(job)
    placed = "; ".join(f"section {s.number} points at " + ", ".join(f"{k.split(':')[0].title()} {nums.get(k, '?')}" for k in [f"{kind}:{key}" for kind, key in exhibit_tokens(' '.join(s.paragraphs))])
                       for s in sections if exhibit_tokens(" ".join(s.paragraphs)))
    narr = f"Writing the dossier with the exhibits on the desk — {len(sections)} sections in the spine's order" + (f"; {placed}" if placed else "") + ". Now the summary and the close, against what was written."
    events.emit(job.id, "narration", phase=STEP, narrator=narr, detail=narr)
    frames = write_frames(job, sections)
    draft.title = str(frames.get("title") or draft.title)
    draft.subtitle = str(frames.get("subtitle", ""))
    draft.executive_summary = [str(p) for p in frames.get("executive_summary", []) or []]
    draft.conclusion = [str(p) for p in frames.get("conclusion", []) or []]
    draft.summary_job_met = str(frames.get("summary_job_met", ""))
    draft.conclusion_job_met = str(frames.get("conclusion_job_met", ""))
    events.emit(job.id, "artifact", phase=STEP, detail=f"draft: {draft.title} — {len(sections)} sections; summary did: {draft.summary_job_met[:90]}; close did: {draft.conclusion_job_met[:90]}",
                payload_json={"kind": "draft", "title": draft.title, "sections": [{"key": s.section_key, "heading": s.heading, "tables": s.table_keys, "figures": s.figure_keys,
                                                                                    "mismatches": [r.key for r in s.exhibit_refs if r.mismatch]} for s in sections],
                              "summary_job_met": draft.summary_job_met, "conclusion_job_met": draft.conclusion_job_met, "repairs": notes})
    return draft


# ── Rendering ────────────────────────────────────────────────────────────

def _render_context(job: DossierJob, docs: list[Document], figure_src: str) -> dict:
    s = job.sections or Sections(title="Dossier")
    doc_by_key = {d.key: d for d in docs}
    tables_by_key = {t.key: t for t in job.tables}
    figures_by_key = {f.key: f for f in job.figures}
    footnotes: list[dict] = []
    fn_index: dict[tuple[str, str], int] = {}
    spine_driven = job.spine is not None and any(sec.section_key for sec in s.sections)
    nums = exhibit_numbers(job) if spine_driven else {}

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

    def number_for(kind: str, key: str) -> int:
        nonlocal table_counter, figure_counter
        if nums:
            return nums.get(f"{kind}:{key}", 0) or (len(placed_tables) if kind == "table" else len(placed_figures))
        if kind == "table":
            table_counter += 1
            return table_counter
        figure_counter += 1
        return figure_counter

    for sec in s.sections:
        blocks: list[dict] = []

        def repl(m: re.Match, sec=sec) -> str:
            idx = int(m.group(1)) - 1
            if 0 <= idx < len(sec.claims) and sec.claims[idx].anchor and not (spine_driven and sec.claims[idx].anchor.trimmed):
                return f'<sup class="fn">{footnote(sec.claims[idx].anchor)}</sup>'
            return ""

        for p in sec.paragraphs:
            pos = 0
            for m in EXHIBIT_TOKEN.finditer(p):
                text = p[pos:m.start()].strip()
                if text:
                    blocks.append({"type": "p", "html": _CLAIM_MARK.sub(repl, html.escape(text))})
                kind, key = m.group(1).lower(), m.group(2)
                if kind == "table" and key in tables_by_key and key not in placed_tables:
                    placed_tables.add(key)
                    blocks.append({"type": "table", **_table_ctx(tables_by_key[key], number_for("table", key), footnote)})
                elif kind == "figure" and key in figures_by_key and key not in placed_figures:
                    placed_figures.add(key)
                    blocks.append({"type": "figure", **_figure_ctx(figures_by_key[key], number_for("figure", key), figure_src)})
                pos = m.end()
            text = p[pos:].strip()
            if text:
                blocks.append({"type": "p", "html": _CLAIM_MARK.sub(repl, html.escape(text))})
        for c in sec.claims:   # claims never referenced in the prose still get their anchors listed
            if c.anchor and not (spine_driven and c.anchor.trimmed):
                footnote(c.anchor)
        # legacy placement (no tokens): exhibits at the section's end
        for key in sec.table_keys:
            t = tables_by_key.get(key)
            if t and key not in placed_tables:
                placed_tables.add(key)
                blocks.append({"type": "table", **_table_ctx(t, number_for("table", key), footnote)})
        for key in sec.figure_keys:
            f = figures_by_key.get(key)
            if f and key not in placed_figures:
                placed_figures.add(key)
                blocks.append({"type": "figure", **_figure_ctx(f, number_for("figure", key), figure_src)})
        rendered_sections.append({"number": sec.number, "heading": sec.heading, "section_key": sec.section_key, "blocks": blocks,
                                  "rendered_paragraphs": [b["html"] for b in blocks if b["type"] == "p"],
                                  "tables": [b for b in blocks if b["type"] == "table"], "figures": [b for b in blocks if b["type"] == "figure"]})
    # legacy only: anything the writer forgot lands in the last section (spine-driven drafts are walled instead)
    if rendered_sections and not spine_driven:
        last = rendered_sections[-1]
        for t in job.tables:
            if t.key not in placed_tables:
                b = {"type": "table", **_table_ctx(t, number_for("table", t.key), footnote)}
                last["blocks"].append(b)
                last["tables"].append(b)
        for f in job.figures:
            if f.key not in placed_figures:
                b = {"type": "figure", **_figure_ctx(f, number_for("figure", f.key), figure_src)}
                last["blocks"].append(b)
                last["figures"].append(b)

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
    if spine_driven:
        walls.append(f"{len(placed_tables)} tables and {len(placed_figures)} diagrams placed at their pointers in the spine's order")
    return {
        "s": {"title": s.title, "subtitle": s.subtitle, "executive_summary": s.executive_summary,
              "sections": rendered_sections, "conclusion": s.conclusion},
        "meta": {"date": datetime.utcnow().strftime("%d %B %Y"), "audience": job.options.audience,
                 "depth": job.options.depth, "job_id": job.id},
        "docs": [{"key": d.key, "label": d.label(), "publication": d.publication, "char_count": d.char_count} for d in docs],
        "footnotes": footnotes, "steps": steps, "engines": engines, "figures_made": _figures_made_ctx(job),
        "spine": _spine_ctx(job), "findings": _findings_ctx(job),
        "strategy": job.plan.strategy_rationale if job.plan else "",
        "alternatives": job.plan.alternatives_considered if job.plan else [],
        "totals": totals, "walls": "; ".join(walls),
    }


def _spine_ctx(job: DossierJob) -> Optional[dict]:
    sp = job.spine
    if sp is None:
        return None
    return {"thesis": sp.thesis, "handle": sp.handle, "summary_job": sp.summary_job, "conclusion_job": sp.conclusion_job,
            "sections": [{"key": s.key, "heading": s.heading, "claim": s.claim, "table": bool(s.table), "figure": bool(s.figure)} for s in sp.sections],
            "notes": sp.notes}


def _findings_ctx(job: DossierJob) -> list[dict]:
    out = []
    for f in job.findings:
        where = ", ".join(f"{k} {v}" for k, v in f.where.model_dump().items() if v is not None)
        fate = f.fates[-1].fate if f.fates else f.status
        out.append({"kind": f.kind.replace("_", " "), "where": where, "note": f.note, "affordance": f.affordance.replace("_", " "),
                    "source": f.source, "fate": fate, "status": f.status})
    return out


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
        src = figure_src.format(key=f.key, name=Path(f.path).name)
    return {"index": index, "key": f.key, "caption": f.caption, "src": src, "status": f.status, "note": f.note,
            "title": getattr(f, "title", "") or "", "visual_format": getattr(f, "visual_format", "") or "",
            "primitive": getattr(f, "primitive", "") or "", "style_school": getattr(f, "style_school", "") or ""}


def _figures_made_ctx(job: DossierJob) -> list[dict]:
    """The 'How this was made' rows for figures: primitive, format, style, attempts, verdict."""
    out = []
    for f in job.figures:
        v = getattr(f, "compliance", None) or {}
        attempts = getattr(f, "attempts", None) or []
        if v.get("checked"):
            found = len(v.get("labels_found") or [])
            n = v.get("n_labels") or (found + len(v.get("labels_missing") or []))
            verdict = f"{'passed' if v.get('ok') else 'flagged'}: format {'ok' if v.get('format_ok') else 'wrong'}, {found}/{n} labels"
            if v.get("prohibited_elements"):
                verdict += ", prohibited elements"
        elif f.status == "generated":
            verdict = "not checked"
        else:
            verdict = f.status + (f": {f.note}" if f.note else "")
        out.append({"key": f.key, "title": getattr(f, "title", "") or f.caption[:60], "primitive": getattr(f, "primitive", "") or "—",
                    "visual_format": getattr(f, "visual_format", "") or "—", "style_school": getattr(f, "style_school", "") or "—",
                    "attempts": len(attempts) or (1 if f.status == "generated" else 0), "verdict": verdict,
                    "provider": getattr(f, "model", None) or f.provider or "—"})
    return out


def _steps_ctx(job: DossierJob) -> list[dict]:
    names = [("reconnaissance", "Read every document; profiled each (thesis, method, anchored claims) and mapped the corpus."),
             ("brief", "Proposed three angles with engines, cost and shape; one was chosen."),
             ("plan", "Turned the angle into an ordered engine sequence for the executor (depth policy enforced)."),
             ("analysis", "Ran the engines through the executor; each phase read the previous phases' prose."),
             ("spine", "Decided what the dossier argues: one claim per section, and the table or diagram each claim needs."),
             ("tables", "Built the tables the spine commissioned; every row verified against verbatim anchors."),
             ("figures", "Drew the diagrams the spine commissioned (primitive → format → labels), rendered and checked each against its spec."),
             ("compose", "Wrote the sections with the exhibits on the desk, placing each at its pointer; then the summary and the close against the body; rendered HTML, PDF and Markdown."),
             ("crosscheck", "Read the dossier as one thing and recorded every finding with its cure; acted on the safe ones."),
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
        if key in ("spine", "crosscheck") and not b["calls"] and not d:
            continue   # a legacy record without the passes
        out.append({"name": key, "what": what, "calls": b["calls"],
                    "tokens": f"{b['in']:,} / {b['out']:,}" if b["calls"] else "—",
                    "cost": f"${b['cost']:.2f}" if b["calls"] else "—",
                    "time": f"{d/1000:.0f}s" if d else "—"})
    return out


def render_html(job: DossierJob, docs: list[Document], figure_src: str = "figures/{name}") -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=select_autoescape(["html", "j2"]))
    tpl = env.get_template("dossier.html.j2")
    ctx = _render_context(job, docs, figure_src)
    try:
        from src.dossier.plate_store import list_plates
        from src.dossier.plates import render_appendix_html
        plates = list_plates(job.id)
        ctx["plates_appendix_html"] = render_appendix_html(plates, src_for=(lambda p: figure_src(p.figure_id) if (figure_src and p.figure_id) else p.url)) if plates else ""
    except Exception as exc:  # plates are optional; the dossier never waits on them
        logger.warning(f"plates appendix skipped: {exc}")
        ctx["plates_appendix_html"] = ""
    return tpl.render(**ctx)


def _md_table(t: dict) -> list[str]:
    lines = [f"**Table {t['index']}. {t['caption']}**", ""]
    lines.append("| " + " | ".join(t["columns"]) + " |")
    lines.append("|" + "---|" * len(t["columns"]))
    for r in t["rows"]:
        cells = [(c["value"].replace("|", "/") + (f" [^{c['fn']}]" if c["fn"] else "")) for c in r["cells"]]
        lines.append("| " + " | ".join(cells) + " |")
    if t["note"]:
        lines += ["", f"*{t['note']}*"]
    lines.append("")
    return lines


def _md_figure(f: dict) -> list[str]:
    head = f"**{f['title']}.** " if f.get("title") else ""
    if f["src"]:
        return [f"![{f.get('title') or 'Figure ' + str(f['index'])}]({f['src']})", "", f"*Figure {f['index']}. {head}{f['caption']}*", ""]
    return [f"*Figure {f['index']} ({f['status']}): {head}{f['caption']}*", ""]


def render_markdown(job: DossierJob, docs: list[Document]) -> str:
    ctx = _render_context(job, docs, "figures/{name}")
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
        for b in sec["blocks"]:
            if b["type"] == "p":
                text = re.sub(r'<sup class="fn">(\d+)</sup>', r"[^\1]", b["html"])
                lines += [html.unescape(text), ""]
            elif b["type"] == "table":
                lines += _md_table(b)
            else:
                lines += _md_figure(b)
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
    if ctx.get("spine"):
        sp = ctx["spine"]
        lines += ["", f"*The spine.* {sp['thesis']}", ""]
        for i, sec in enumerate(sp["sections"], start=1):
            lines.append(f"{i}. **{sec['heading']}** — {sec['claim']}" + (" *(table)*" if sec["table"] else "") + (" *(diagram)*" if sec["figure"] else ""))
        lines += ["", f"Summary's job: {sp['summary_job']} · Close's job: {sp['conclusion_job']}"]
    if ctx.get("figures_made"):
        lines += ["", "| Figure | Primitive | Format | Style | Attempts | Check |", "|---|---|---|---|---|---|"]
        for fm in ctx["figures_made"]:
            lines.append(f"| {fm['title']} | {fm['primitive']} | {fm['visual_format']} | {fm['style_school']} | {fm['attempts']} | {fm['verdict']} |")
    if ctx.get("findings"):
        lines += ["", "| Finding | Where | Cure | Fate |", "|---|---|---|---|"]
        for f in ctx["findings"]:
            lines.append(f"| {f['kind']} ({f['source']}) | {f['where']} | {f['affordance']} | {f['fate']} |")
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
    try:
        from src.dossier.blob_store import put_blob_safe

        for kind, mime in (("html", "text/html"), ("md", "text/markdown"), ("pdf", "application/pdf")):
            if kind in paths:
                put_blob_safe(f"dossier:{job.id}:{kind}", mime, Path(paths[kind]).read_bytes())
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"dossier blob put failed: {exc}")
    return paths


def run_compose(job: DossierJob, docs: list[Document], persist) -> tuple[Sections, dict[str, str]]:
    if job.spine is not None:
        sections = compose_draft(job, docs, persist)
    else:
        sections = write_sections(job, docs)
    job.sections = sections
    persist(sections=sections)
    paths = render_all(job, docs)
    return sections, paths
