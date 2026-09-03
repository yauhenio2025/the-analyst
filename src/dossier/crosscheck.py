"""Pass X — THE CROSS-CHECK: the first judgment made against the real things.

The draft text, the actual table rows and the rendered diagrams are read together as
one dossier, against the spine. The judge answers the owner's questions verbatim —
does each picture depict what its section argues? do each table's rows match the
section's claims? is anything asserted that nothing backs? do captions restate the
prose? do the summary and the close do the same job? — through a typed tool whose
findings each carry ONE affordance.

Code clamps outrank the judge (the `clamp_frame_grace` law): a caption with a digit
run, an exhibit no token placed, a figure whose check failed, a close that shares its
sentences with the summary — these are findings by arithmetic whether or not the
judge names them; the judge's impression is kept beside them. Findings become
targets on the job's ledger (`findings_json`) with append-only fates; code never
closes one by silence — a standing finding the judge does not rule on is recorded
`persists` by code.

Depth: `simple` — report only. `medium+` — ONE round of the safe automatic
realizations (redraw a figure whose check failed with the judge's words, drop an
exhibit nothing points at, rewrite a caption that carries a number), exhibits first,
then the document re-rendered only when something changed (zero-change gate).

Skip law: a judge that fails records `crosscheck_unavailable`; the clamps still run
and the run proceeds.
"""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Optional

from src.dossier import events, findings as ledger
from src.dossier.common import AUDIENCE_REGISTER, job_dir
from src.dossier.llm import call_json
from src.dossier.schemas import AFFORDANCES, FINDING_KINDS, CrossCheckVerdict, DossierJob, Figure, Finding, Section
from src.dossier.walls import EXHIBIT_TOKEN, has_digit_run, exhibit_tokens, normalize, shingle_overlap
from src.sources.schemas import Document

logger = logging.getLogger(__name__)

STEP = "crosscheck"
MAX_FINDINGS = 20
MAX_IMAGES = 3
REDUNDANCY_OVERLAP = 0.15
REALIZE_BY_DEPTH = {"simple": 0, "medium": 1, "advanced": 1}   # rounds of automatic realization (Phase 2 adds the second)
MAX_RERENDERS = 1
REWRITE_AFFORDANCES = {"revise_figure_spec", "rewrite_section", "rewrite_paragraph", "revise_table_rows", "reanchor_claim", "rewrite_caption", "add_table"}
JUDGE_KINDS = [k for k in FINDING_KINDS if k not in ("table_unavailable", "table_rows_dropped", "figure_unavailable", "exhibit_unpointed", "exhibit_unplaced")]
FATE_ENUM = ["resolved", "persists", "regressed", "superseded"]

_CLAIM_MARK = re.compile(r"\{\{\s*(\d+)\s*\}\}")

# ── Tool schema ───────────────────────────────────────────────────────────

WHERE_SCHEMA = {"type": "object", "additionalProperties": False,
                "properties": {"section_key": {"anyOf": [{"type": "string"}, {"type": "null"}]}, "table_key": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                               "figure_key": {"anyOf": [{"type": "string"}, {"type": "null"}]}, "paragraph_index": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
                               "anchor_n": {"anyOf": [{"type": "integer"}, {"type": "null"}]}},
                "required": ["section_key", "table_key", "figure_key", "paragraph_index", "anchor_n"]}
FINDING_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["kind", "where", "quote", "note", "affordance", "realization", "recommended", "target_id"],
    "properties": {
        "kind": {"type": "string", "enum": JUDGE_KINDS},
        "where": WHERE_SCHEMA,
        "quote": {"type": "string", "description": "the offending words, VERBATIM from the page (a sentence, a caption, a cell); the desk checks they are on the page"},
        "note": {"type": "string", "description": "plain language for the desk: the effect on the reader, then the cure"},
        "affordance": {"type": "string", "enum": list(AFFORDANCES)},
        "realization": {"anyOf": [{"type": "string"}, {"type": "null"}], "description": "the drafted change (new caption / picture_shows + caption_says / replacement paragraph / rows to add or drop / the sentence and the passage that re-anchors it); required for every cure that rewrites something"},
        "recommended": {"type": "boolean"},
        "target_id": {"anyOf": [{"type": "string"}, {"type": "null"}], "description": "the id of a standing finding this repeats, else null"},
    },
}
VERDICT_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["hangs_together", "summary", "findings", "prior_fates", "what_changed"],
    "properties": {
        "hangs_together": {"type": "boolean"},
        "summary": {"type": "string", "description": "2-3 sentences, executive-readable, verdict first"},
        "findings": {"type": "array", "maxItems": MAX_FINDINGS, "items": FINDING_SCHEMA},
        "prior_fates": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["target_id", "fate", "rationale"],
                        "properties": {"target_id": {"type": "string"}, "fate": {"type": "string", "enum": FATE_ENUM}, "rationale": {"type": "string"}}}},
        "what_changed": {"anyOf": [{"type": "string"}, {"type": "null"}]},
    },
}

SYSTEM = """You are the cross-check desk of The Analyst — the first reader who sees the dossier the way its reader will: the
text, the tables with their rows, and the pictures as actually drawn, all at once, against the spine the desk planned.
Until now every desk worked on one part. You judge whether the parts hang together. Judge only what is on the page;
answer through the `crosscheck_verdict` tool, nothing else.

Read the spine first. Then, section by section, ask:
— Does each picture depict what its section argues? Compare the image you are shown (and the checked description)
  with the section's claim and the caption. A picture that shows something other than the claim is
  `figure_depicts_other`. Decide the cure honestly: when a better diagram would carry the claim, draft it
  (`revise_figure_spec`, realization = the new picture_shows + caption_says); when the plan is right and the render
  missed it, `rerender_figure` (realization = what the redraw must fix); when no picture can do this job, `drop_figure`
  and say what the prose should carry instead.
— Does each table's row set match the section's claims? One row = the unit the spine named; rows that argue a
  different thing, a claim in the prose that the table beside it contradicts or does not contain, a table no sentence
  points at (`table_unreferenced`), a pointer that says "the table below" where the table is not
  (`exhibit_pointer_wrong`) — name them. Cures: `revise_table_rows` (realization = rows to add/drop, in the table's own
  columns), `add_table` (the spine's intent for a section that argues by comparison and has none), `drop_table`.
— Is anything asserted that nothing backs? A sentence stating a fact, number, name or causal claim with no anchor, no
  table cell and no figure behind it is `claim_unbacked`. An anchor that is a cut-off fragment is `anchor_fragment`; an
  anchor whose quote does not support the sentence it footnotes is `anchor_off_claim`. A number that differs between
  the prose, a cell and a caption is `number_drift`. Cures: `reanchor_claim` (realization = the sentence and the passage
  that actually supports it, verbatim from the documents), `drop_anchor`, `rewrite_paragraph`.
— Does the prose say what the exhibit already says? A paragraph that restates a caption or a table note is
  `caption_restates_text`; a caption that carries the argument (numbers, causes) is `caption_carries_number`
  (`rewrite_caption`). The picture carries what the reader must SEE; the caption says what to take from it; the prose
  argues.
— The whole. A section that proves something other than its spine claim is `section_off_spine`; a close that restates
  the summary is `redundant_summary_conclusion` (`merge_summary_conclusion` or `rewrite_section`); a load-bearing term
  the audience is never told the meaning of is `jargon_unglossed`; a register break is `register_break`; a section
  that argues by comparison with nothing to compare in is `exhibit_missing_where_claim_needs_one`.

Laws: quote the offending words verbatim — the desk checks that they are on the page and drops a finding whose quote
is not. One finding, one cure — the sharpest single instrument. Draft the realization for every cure that rewrites
something; the desk applies it under the same walls the original desk obeyed. Be concrete and unsparing; do not pad
the list to look thorough, and do not swallow a real problem to be polite. A dossier that hangs together gets
`hangs_together: true` and an empty list — that is a legitimate and common verdict.

Your memory: STANDING FINDINGS from the exhibit and writing desks ride the request with their ids. You are the same
desk reading the finished dossier: declare one fate per standing finding (resolved / persists / regressed / superseded
— say why), link a repeat to its target_id instead of minting a duplicate, and say in `what_changed` what the page
shows about them. Never close a finding by silence.

The register: your reader is an executive's analyst with no view of this system's insides. Name sections and exhibits
as the page shows them ("section 3", "Table 2", "the picture in section 4"); name the problem by its effect on the
reader, then the plain cure; no pass names, no keys in prose (keys go in `where`)."""


# ── The page as the judge (and the walls) see it ────────────────────────

def page_text(job: DossierJob) -> dict[str, str]:
    """Normalized text per region: 'summary', 'conclusion', each section_key, 'captions' (all captions + notes + cells)."""
    s = job.sections
    out: dict[str, str] = {}
    if s is None:
        return out
    out["summary"] = normalize(" ".join(s.executive_summary))
    out["conclusion"] = normalize(" ".join(s.conclusion))
    for sec in s.sections:
        out[sec.section_key or f"s{sec.number}"] = normalize(" ".join(EXHIBIT_TOKEN.sub("", _CLAIM_MARK.sub("", p)) for p in sec.paragraphs) + " " + sec.heading)
    caps = [t.caption + " " + t.note + " " + " ".join(c.value for r in t.rows for c in r.cells) for t in job.tables]
    caps += [f.caption + " " + f.title for f in job.figures]
    # a diagram's labels ARE on the page (in the picture): the judge may quote them
    try:
        from src.display.enforcement import collect_labels

        caps += [" ".join(collect_labels(f.data)) for f in job.figures if f.data]
    except Exception:
        pass
    out["captions"] = normalize(" ".join(caps))
    return out


def quote_on_page(quote: str, regions: dict[str, str], section_key: Optional[str]) -> bool:
    q = normalize(re.sub(r"[●•◦▪■◆★→←↑↓]+", " ", quote or ""))
    if len(q) < 8:
        return False
    if section_key and section_key in regions and q in regions[section_key]:
        return True
    return any(q in text for text in regions.values())


def _anchors_text(job: DossierJob) -> str:
    lines = []
    n = 0
    for sec in (job.sections.sections if job.sections else []):
        for k, c in enumerate(sec.claims, start=1):
            if c.anchor is None:
                lines.append(f"- section `{sec.section_key}` claim {k}: NO ANCHOR — “{c.text[:140]}”")
                continue
            n += 1
            flag = " (FRAGMENT — trimmed to a prefix, not footnoted)" if c.anchor.trimmed else ""
            lines.append(f"- section `{sec.section_key}` claim {k}{flag}: “{c.text[:140]}” ⟶ [{c.anchor.doc_key}] “{c.anchor.quote}”")
    return "\n".join(lines) or "(no anchored claims)"


def _draft_text(job: DossierJob) -> str:
    from src.dossier.compose import body_markdown, exhibit_numbers

    s = job.sections
    nums = exhibit_numbers(job)
    tables = {t.key: t for t in job.tables}
    lines = ["## Summary", ""] + list(s.executive_summary) + [""]
    body = body_markdown(job, s.sections, nums)
    # the judge sees every row, not just the first column
    for t in job.tables:
        rows = "\n".join("| " + " | ".join((c.value or "").replace("|", "/") for c in r.cells) + " |" for r in t.rows)
        body = body.replace(f"[Table {nums.get('table:' + t.key, '?')}. {t.caption} — {len(t.rows)} rows: " + "; ".join((r.cells[0].value if r.cells else "") for r in t.rows) + "]",
                            f"[Table {nums.get('table:' + t.key, '?')} (key {t.key}, for section {t.section_key}). {t.caption}\n| " + " | ".join(t.columns) + f" |\n{rows}\nnote: {t.note}]")
    for f in job.figures:
        if f.status == "generated":
            body = body.replace(f"[Figure {nums.get('figure:' + f.key, '?')}. {f.caption}]",
                                f"[Figure {nums.get('figure:' + f.key, '?')} (key {f.key}, for section {f.section_key}) — {f.visual_format}: “{f.title}”. Caption: {f.caption}\n"
                                f"  meant to show: {f.picture_shows}\n  ACTUALLY SHOWS (checked): {f.detected}\n  check: {'passed' if f.checked_ok else ('FAILED — ' + '; '.join((f.compliance or {}).get('issues', [])[:3]) if f.checked_ok is False else 'not run')}]")
    lines += [body, "", f"## {len(s.sections) + 1}. What this means", ""] + list(s.conclusion)
    return "\n".join(lines)


def _spine_text(job: DossierJob) -> str:
    sp = job.spine
    lines = [f"THESIS: {sp.thesis}", f"SUMMARY'S JOB: {sp.summary_job}", f"CLOSE'S JOB: {sp.conclusion_job}", ""]
    for i, sec in enumerate(sp.sections, start=1):
        ex = []
        if sec.table:
            ex.append(f"table (one row = {sec.table.row_unit}; must carry: {'; '.join(sec.table.carries_claims)})")
        if sec.figure:
            ex.append(f"diagram ({sec.figure.visual_format}: {sec.figure.picture_shows}; caption should say: {sec.figure.caption_says})")
        lines.append(f"{i}. `{sec.key}` {sec.heading} — CLAIM: {sec.claim}" + (f" — commissioned: {'; '.join(ex)}" if ex else ""))
    return "\n".join(lines)


def _standing_text(findings: list[Finding]) -> str:
    opened = ledger.open_findings(findings)
    if not opened:
        return "(none)"
    return "\n".join(f"- id {f.id} · {f.kind} · where {json.dumps({k: v for k, v in f.where.model_dump().items() if v is not None})} · {f.note[:220]}" for f in opened)


def _user(job: DossierJob, standing: list[Finding]) -> str:
    return (f"AUDIENCE: {job.options.audience} — {AUDIENCE_REGISTER.get(job.options.audience, '')}\n\n"
            f"THE SPINE:\n{_spine_text(job)}\n\nTHE DOSSIER AS THE READER SEES IT:\n\n{_draft_text(job)}\n\n"
            f"ANCHORS (footnote by claim):\n{_anchors_text(job)}\n\n"
            f"STANDING FINDINGS (declare one fate each; link repeats by target_id):\n{_standing_text(standing)}")


def _images(job: DossierJob) -> list[tuple[bytes, str]]:
    out: list[tuple[bytes, str]] = []
    try:
        from src.images.compliance import _prepare
    except Exception:
        _prepare = None  # type: ignore[assignment]
    for f in job.figures:
        if f.status != "generated" or not f.path or len(out) >= MAX_IMAGES:
            continue
        try:
            data = Path(f.path).read_bytes()
            if _prepare is not None:
                data, mime = _prepare(data)
            else:
                mime = "image/jpeg" if f.path.lower().endswith((".jpg", ".jpeg")) else "image/png"
            out.append((data, mime))
        except Exception as exc:
            logger.info(f"figure {f.key} not shown to the judge ({exc})")
    return out


# ── Code clamps (outrank the judge) ─────────────────────────────────────

def _dupe(existing: list[Finding], kind: str, where: dict[str, Any]) -> Optional[Finding]:
    for f in existing:
        if f.status != "open" or f.kind != kind:
            continue
        w = f.where.model_dump()
        if all(w.get(k) == v for k, v in where.items() if v is not None):
            return f
    return None


def clamp_findings(job: DossierJob, rnd: int) -> list[Finding]:
    """Findings by arithmetic over recorded facts. Never duplicates an open finding of the same kind and place."""
    out: list[Finding] = []
    existing = list(job.findings)
    from src.dossier.compose import expected_exhibits

    placed = set()
    for sec in (job.sections.sections if job.sections else []):
        for kind, key in exhibit_tokens(" ".join(sec.paragraphs)):
            placed.add(f"{kind}:{key}")
        placed.update(f"table:{k}" for k in sec.table_keys)
        placed.update(f"figure:{k}" for k in sec.figure_keys)
    for tk, sk in expected_exhibits(job).items():
        if tk not in placed:
            kind, key = tk.split(":", 1)
            where = {"section_key": sk or None, ("table_key" if kind == "table" else "figure_key"): key}
            if _dupe(existing + out, "exhibit_unplaced", where) is None:
                out.append(ledger.mint("exhibit_unplaced", where=where, source="clamp", round=rnd, affordance="drop_table" if kind == "table" else "drop_figure",
                                       note=f"No sentence in the dossier places this {kind} (no token in any section): the reader would never meet it. Cure: drop it, or point at it from its section."))
    for t in job.tables:
        if has_digit_run(t.caption):
            where = {"section_key": t.section_key or None, "table_key": t.key}
            if _dupe(existing + out, "caption_carries_number", where) is None:
                out.append(ledger.mint("caption_carries_number", where=where, source="clamp", round=rnd, affordance="rewrite_caption",
                                       quote=t.caption, realization=_strip_digits(t.caption),
                                       note="The table's caption carries a number; captions say what the exhibit is, numbers live in the cells and the prose. Cure: rewrite the caption without it."))
    for f in job.figures:
        if f.status != "generated":
            continue
        if has_digit_run(f.caption):
            where = {"section_key": f.section_key or None, "figure_key": f.key}
            if _dupe(existing + out, "caption_carries_number", where) is None:
                out.append(ledger.mint("caption_carries_number", where=where, source="clamp", round=rnd, affordance="rewrite_caption",
                                       quote=f.caption, realization=(f.caption_says if f.caption_says and not has_digit_run(f.caption_says) else _strip_digits(f.caption)),
                                       note="The picture's caption carries a number; the caption says what to take from the picture, never the figures. Cure: rewrite it without the number."))
        if f.checked_ok is False:
            where = {"section_key": f.section_key or None, "figure_key": f.key}
            if _dupe(existing + out, "figure_depicts_other", where) is None:
                issues = "; ".join((f.compliance or {}).get("issues") or [])[:500]
                out.append(ledger.mint("figure_depicts_other", where=where, source="clamp", round=rnd, affordance="rerender_figure",
                                       quote=f.caption, realization=str((f.compliance or {}).get("suggestion") or "") or None,
                                       note=f"The check recorded that the drawn diagram does not match its spec ({issues}); the reader would see something other than the section argues. Cure: redraw from the check's notes."))
    s = job.sections
    if s is not None and s.executive_summary and s.conclusion:
        overlap = shingle_overlap(" ".join(s.conclusion), " ".join(s.executive_summary))
        if overlap > REDUNDANCY_OVERLAP and _dupe(existing + out, "redundant_summary_conclusion", {}) is None:
            out.append(ledger.mint("redundant_summary_conclusion", where={}, source="clamp", round=rnd, affordance="rewrite_section",
                                   quote=s.conclusion[0][:200],
                                   note=f"The close shares {overlap:.0%} of its eight-word phrases with the summary: the reader reads the same thing twice. Cure: rewrite the close to its own job ({job.spine.conclusion_job if job.spine else 'the decision rule'})."))
    return out


def _strip_digits(text: str) -> str:
    out = re.sub(r"\s*\(?\b\d[\d,.:/%-]*\b\)?\s*", " ", text or "")
    return re.sub(r"\s+", " ", out).strip(" ,;:-") or text


# ── The judge's answer, walled ──────────────────────────────────────────

def validate_verdict(raw: dict, job: DossierJob, standing: list[Finding], rnd: int) -> tuple[list[Finding], list[dict], list[str]]:
    """Shape + membership walls over the judge's answer. Returns (findings kept, prior fates, notes about what was dropped)."""
    notes: list[str] = []
    regions = page_text(job)
    section_keys = {s.key for s in job.spine.sections} if job.spine else {s.section_key for s in (job.sections.sections if job.sections else [])}
    table_keys = {t.key for t in job.tables}
    figure_keys = {f.key for f in job.figures}
    standing_ids = {f.id for f in standing}
    kept: list[Finding] = []
    for i, item in enumerate((raw or {}).get("findings", []) or [], start=1):
        if not isinstance(item, dict):
            continue
        kind = str(item.get("kind", ""))
        if kind not in FINDING_KINDS:
            notes.append(f"finding {i}: unknown kind {kind!r} dropped")
            continue
        where = {k: v for k, v in (item.get("where") or {}).items() if v not in (None, "", 0)}
        bad = [f"{k}={v!r}" for k, v in where.items()
               if (k == "section_key" and v not in section_keys) or (k == "table_key" and v not in table_keys) or (k == "figure_key" and v not in figure_keys)]
        if bad:
            notes.append(f"finding {i} ({kind}): where names nothing on the page ({', '.join(bad)}); dropped")
            continue
        quote = str(item.get("quote", "")).strip()
        if kind not in ("exhibit_missing_where_claim_needs_one", "table_unreferenced") and not quote_on_page(quote, regions, where.get("section_key")):
            notes.append(f"finding {i} ({kind}): quote is not on the page (“{quote[:70]}”); dropped")
            continue
        affordance = str(item.get("affordance", "none"))
        if affordance not in AFFORDANCES:
            affordance = "none"
        realization = item.get("realization")
        realization = str(realization).strip() if realization else None
        if affordance in REWRITE_AFFORDANCES and not realization:
            notes.append(f"finding {i} ({kind}): cure {affordance} without a drafted realization; kept as advisory (none)")
            affordance = "none"
        target = item.get("target_id")
        f = ledger.mint(kind, where=where, quote=quote, note=str(item.get("note", "")).strip(), affordance=affordance, realization=realization,
                        source="judge", round=rnd, recommended=bool(item.get("recommended", True)))
        if target and target in standing_ids:
            prior = ledger.by_id(standing, str(target))
            if prior is not None:
                prior.note = (prior.note + f" — cross-check: {f.note}")[:1200]
                if prior.realization is None and realization:
                    prior.realization = realization
                notes.append(f"finding {i} ({kind}) repeats standing {target}; merged into it")
                continue
        kept.append(f)
        if len(kept) >= MAX_FINDINGS:
            break
    fates_raw = [x for x in ((raw or {}).get("prior_fates") or []) if isinstance(x, dict)]
    fates = [{"target_id": str(x.get("target_id", "")), "fate": str(x.get("fate", "persists")), "rationale": str(x.get("rationale", ""))} for x in fates_raw]
    return kept, fates, notes


def _merge_clamps(clamps: list[Finding], judged: list[Finding]) -> tuple[list[Finding], list[str]]:
    """A judge finding on the same fact as a clamp joins the clamp (the recorded fact leads, the impression follows)."""
    notes = []
    out = list(judged)
    for c in clamps:
        for j in list(out):
            if j.kind == c.kind and all(j.where.model_dump().get(k) == v for k, v in c.where.model_dump().items() if v is not None):
                c.note = (c.note + f" — the judge: {j.note}")[:1200]
                if c.realization is None and j.realization:
                    c.realization = j.realization
                out.remove(j)
                notes.append(f"judge's {j.kind} joined the clamp on the same fact")
    return out, notes


def apply_fates(standing: list[Finding], fates: list[dict], rnd: int) -> list[str]:
    """Fate completeness: every standing finding gets the judge's fate, or `persists` by code (never closed by silence)."""
    notes = []
    declared = {f["target_id"]: f for f in fates if f.get("target_id")}
    for f in standing:
        d = declared.get(f.id)
        if d and d["fate"] in FATE_ENUM:
            ledger.record_fate(f, d["fate"], d.get("rationale", ""), by="judge", round=rnd)
        else:
            ledger.record_fate(f, "persists", "the judge did not rule on it; kept open by code", by="code", round=rnd)
            notes.append(f"{f.id} ({f.kind}): no fate declared; persists by code")
    return notes


# ── Safe automatic realizations (medium+) ──────────────────────────────

def _figure_spec_from(fig: Figure):
    from src.dossier.schemas import FigureSpec

    return FigureSpec(**{k: getattr(fig, k) for k in FigureSpec.model_fields})


def realize(job: DossierJob, docs: list[Document], rnd: int, persist=None) -> tuple[list[str], list[str]]:
    """One round: exhibits first (rewrite captions, drop unplaced, redraw ≤ 1 failed figure), then the document.
    Returns (finding ids acted on, notes). Nothing here scores merit."""
    acted: list[str] = []
    notes: list[str] = []
    changed = False
    rerenders = 0
    for f in ledger.open_findings(job.findings):
        if not f.recommended:
            continue
        w = f.where
        if f.kind == "caption_carries_number" and f.affordance == "rewrite_caption" and f.realization and not has_digit_run(f.realization):
            target = next((x for x in job.figures if w.figure_key and x.key == w.figure_key), None) or next((x for x in job.tables if w.table_key and x.key == w.table_key), None)
            if target is not None:
                before = target.caption
                target.caption = f.realization
                ledger.record_fate(f, "executed", f"caption rewritten by code: “{before[:60]}” → “{target.caption[:60]}”", by="code", round=rnd)
                acted.append(f.id)
                changed = True
                notes.append(f"caption of {w.figure_key or w.table_key} rewritten without its number")
        elif f.kind == "exhibit_unplaced" and f.affordance in ("drop_table", "drop_figure"):
            if w.table_key:
                job.tables = [t for t in job.tables if t.key != w.table_key]
            if w.figure_key:
                job.figures = [x for x in job.figures if x.key != w.figure_key]
            ledger.record_fate(f, "executed", "unplaced exhibit dropped by code", by="code", round=rnd)
            acted.append(f.id)
            changed = True
            notes.append(f"dropped unplaced exhibit {w.table_key or w.figure_key}")
        elif f.kind == "figure_depicts_other" and f.affordance in ("rerender_figure", "revise_figure_spec") and w.figure_key and rerenders < MAX_RERENDERS:
            idx = next((i for i, x in enumerate(job.figures) if x.key == w.figure_key), None)
            if idx is None:
                continue
            old = job.figures[idx]
            spec = _figure_spec_from(old)
            revision = [f"THE CROSS-CHECK'S VERDICT ON THE PREVIOUS DRAWING: {f.note}"]
            if f.realization:
                revision.append(f"WHAT THE REDRAW MUST DO: {f.realization}")
            for iss in (old.compliance or {}).get("issues") or []:
                revision.append(f"Previous check: {iss}")
            rerenders += 1
            try:
                from src.dossier.figures import enrich_from_spine, render_figure

                out_dir = job_dir(job.id) / "figures"
                out_dir.mkdir(parents=True, exist_ok=True)
                new = render_figure(job, spec, out_dir, job.options.image_provider, revision_notes=revision)
                new = enrich_from_spine(new, job.spine.section(old.section_key) if job.spine else None)
                new.attempts = (old.attempts or []) + [{"n": 0, "kept": False, "before_crosscheck": True, "compliance": old.compliance, "path": old.path}] + (new.attempts or [])
                new.cost_usd = round(old.cost_usd + new.cost_usd, 4)
                job.figures[idx] = new
                changed = True
                acted.append(f.id)
                if new.checked_ok:
                    ledger.record_fate(f, "resolved", f"redrawn with the cross-check's words; the check now passes ({new.detected[:120]})", by="code", round=rnd)
                else:
                    ledger.record_fate(f, "persists", f"redrawn once; the check still flags it ({'; '.join((new.compliance or {}).get('issues', [])[:2])})", by="code", round=rnd)
                notes.append(f"figure {old.key} redrawn: check {'passes' if new.checked_ok else 'still flagged'}")
                events.emit(job.id, "note", phase=STEP, detail=f"figure_rerendered {old.key}: compliance {'ok' if new.checked_ok else 'still flagged'}",
                            payload_json={"kind": "figure_rerendered", "key": old.key, "compliance_before": old.compliance, "compliance_after": new.compliance, "revision_notes": revision})
            except Exception as exc:
                ledger.record_fate(f, "failed", f"redraw failed: {exc}", by="code", round=rnd)
                notes.append(f"figure {old.key} redraw failed: {str(exc)[:120]}")
    if persist is not None:
        try:
            persist(findings=job.findings, figures=job.figures, tables=job.tables)
        except Exception as exc:
            logger.warning(f"realization persist failed: {exc}")
    if changed:
        from src.dossier.compose import render_all

        paths = render_all(job, docs)
        job.paths = paths
        if persist is not None:
            persist(paths=paths)
        notes.append("document re-rendered")
    else:
        notes.append("the batch changed nothing — the findings stay open (zero-change gate)")
    return acted, notes


# ── The step ────────────────────────────────────────────────────────────

def narration_for(verdict: CrossCheckVerdict, findings: list[Finding], acted: list[str]) -> str:
    opened = ledger.open_findings(findings)
    if not opened and not acted:
        return "Reading the dossier as one thing — the pictures show what the text argues, the rows carry the claims, nothing is asserted bare. It hangs together."
    kinds: dict[str, int] = {}
    for f in opened:
        kinds[f.kind.replace("_", " ")] = kinds.get(f.kind.replace("_", " "), 0) + 1
    listed = ", ".join(f"{k}" + (f" ×{n}" if n > 1 else "") for k, n in list(kinds.items())[:5])
    head = f"Reading the dossier as one thing — {verdict.findings_minted} finding{'s' if verdict.findings_minted != 1 else ''}"
    head += f" ({verdict.clamps} by arithmetic)" if verdict.clamps else ""
    if acted:
        head += f"; acted on {len(acted)}"
    return head + (f". Still open: {listed}." if opened else ". Nothing left open.")


def run_crosscheck(job: DossierJob, docs: list[Document], persist=None) -> Optional[CrossCheckVerdict]:
    if job.sections is None:
        events.emit(job.id, "note", phase=STEP, detail="crosscheck_skipped: nothing composed")
        return None
    rnd = (job.crosscheck.round + 1) if job.crosscheck else 1
    standing = ledger.open_findings(job.findings)
    clamps = clamp_findings(job, rnd)
    for c in clamps:
        events.emit(job.id, "note", phase=STEP, detail=f"clamp: {c.kind} at {json.dumps({k: v for k, v in c.where.model_dump().items() if v is not None})} — {c.note[:140]}",
                    payload_json={"kind": "clamp", "finding": c.model_dump()})
    judged: list[Finding] = []
    fates: list[dict] = []
    summary, hangs, what_changed, judged_ok = "", None, None, False
    if job.spine is None:
        events.emit(job.id, "note", phase=STEP, detail="crosscheck: no spine on the job; clamps only (the judge needs the spine to judge against)")
    else:
        try:
            images = _images(job) if job.options.depth != "simple" else []
            raw, _ = call_json(job.id, STEP, label="cross-check verdict" + (f" ({len(images)} pictures shown)" if images else ""), system=SYSTEM,
                               user=_user(job, standing + clamps), images=images or None, tool_name="crosscheck_verdict", schema=VERDICT_SCHEMA,
                               model_cls=None, max_tokens=8000)
            judged, fates, notes = validate_verdict(raw, job, standing + clamps, rnd)
            for n in notes:
                events.emit(job.id, "note", phase=STEP, detail=f"verdict wall: {n}", payload_json={"kind": "verdict_wall"})
            judged, merge_notes = _merge_clamps(clamps, judged)
            for n in merge_notes:
                events.emit(job.id, "note", phase=STEP, detail=f"verdict wall: {n}")
            summary = str((raw or {}).get("summary", "")).strip()
            hangs = bool((raw or {}).get("hangs_together")) and not clamps and not judged
            what_changed = (raw or {}).get("what_changed") or None
            judged_ok = True
        except Exception as exc:
            logger.warning(f"crosscheck judge unavailable: {exc}", exc_info=True)
            events.emit(job.id, "note", phase=STEP, detail=f"crosscheck_unavailable: {exc.__class__.__name__}: {str(exc)[:300]} — clamps recorded; the run proceeds",
                        payload_json={"kind": "crosscheck_unavailable", "reason": str(exc)[:300]})
    fate_notes = apply_fates(standing, fates, rnd) if judged_ok else []
    for n in fate_notes:
        events.emit(job.id, "note", phase=STEP, detail=f"fate: {n}")
    ledger.append(job, clamps + judged, persist)
    verdict = CrossCheckVerdict(round=rnd, hangs_together=hangs if judged_ok else None, summary=summary, findings_minted=len(clamps) + len(judged),
                                clamps=len(clamps), judged=judged_ok, what_changed=what_changed)
    job.crosscheck = verdict
    if persist is not None:
        persist(crosscheck=verdict, findings=job.findings)
    acted: list[str] = []
    if REALIZE_BY_DEPTH.get(job.options.depth, 0) > 0 and ledger.open_findings(job.findings):
        acted, rnotes = realize(job, docs, rnd, persist)
        for n in rnotes:
            events.emit(job.id, "note", phase=STEP, detail=f"realize: {n}", payload_json={"kind": "realize"})
        verdict.realized = acted
        job.crosscheck = verdict
        if persist is not None:
            persist(crosscheck=verdict)
    narr = narration_for(verdict, job.findings, acted)
    events.emit(job.id, "narration", phase=STEP, narrator=narr, detail=narr)
    events.emit(job.id, "artifact", phase=STEP, detail=f"cross-check: {summary or ('clamps only' if not judged_ok else 'no summary')}",
                payload_json={"kind": "crosscheck", **verdict.model_dump(),
                              "findings": [{"id": f.id, "kind": f.kind, "where": {k: v for k, v in f.where.model_dump().items() if v is not None},
                                            "affordance": f.affordance, "source": f.source, "status": f.status,
                                            "fate": (f.fates[-1].fate if f.fates else None)} for f in job.findings]})
    return verdict
