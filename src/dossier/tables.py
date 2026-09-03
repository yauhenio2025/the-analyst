"""Step 6 — tables: the evidence tables the SPINE commissioned, behind the anchor wall.

Spine-driven (pass E1): for every spine section with a `table` spec the call
receives the section's claim, the spec (intent, row unit, columns, the claims
the rows must carry) and its planned anchors; the answer is keyed by
`section_key`. Walls: the anchor wall per row (as ever), `section_key`
membership, at most one table per section, `MIN_ROWS` rows. Per-exhibit skip
law: sections whose table fell short are re-asked ONCE with the failed quotes
(the cached prefix makes that cheap); a table still short is a recorded finding
`table_unavailable` and its section proceeds without it. Dropped rows are a
recorded finding too (`table_rows_dropped`).

Legacy path (no spine on the job): 2-3 tables planned from the prose, as before.
"""
from __future__ import annotations

import logging
import re
from typing import Any, Optional

from src.dossier import events, findings as ledger
from src.dossier.common import AUDIENCE_REGISTER, analysis_prose, compact_profiles, corpus_text
from src.dossier.llm import call_json
from src.dossier.schemas import Cell, DossierJob, DossierSpine, Finding, Table
from src.dossier.walls import NormalizedCorpus, verify_table
from src.sources.schemas import Document

logger = logging.getLogger(__name__)

STEP = "tables"
CORPUS_IN_PROMPT_MAX_CHARS = 600_000
MIN_TABLES = 2
MIN_ROWS = 2

ANCHOR_SCHEMA = {"type": "object", "required": ["doc_key", "quote"], "additionalProperties": False,
                 "properties": {"doc_key": {"type": "string"}, "quote": {"type": "string", "description": "verbatim, copied exactly from the document text, 40-200 chars, no ellipses"}}}
CELL_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["value", "anchor"],
               "properties": {"value": {"type": "string"}, "anchor": {"anyOf": [ANCHOR_SCHEMA, {"type": "null"}]}}}
TABLE_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["key", "caption", "columns", "rows", "note"],
    "properties": {
        "key": {"type": "string", "description": "snake_case key"},
        "caption": {"type": "string"},
        "columns": {"type": "array", "minItems": 2, "maxItems": 6, "items": {"type": "string"}},
        "rows": {"type": "array", "minItems": 3, "maxItems": 10,
                 "items": {"type": "object", "additionalProperties": False, "required": ["cells"],
                           "properties": {"cells": {"type": "array", "items": CELL_SCHEMA}}}},
        "note": {"type": "string", "description": "one line: what the pattern in this table shows"},
    },
}
TABLES_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["tables"],
                 "properties": {"tables": {"type": "array", "minItems": 2, "maxItems": 3, "items": TABLE_SCHEMA}}}

SYSTEM = """You are the tables desk of The Analyst. You turn analysis into 2-3 compact evidence tables the reader can scan.
Rules: each row is one thing (a document, an actor, a mechanism, a claim, a period); the first column names it; cells
are short. EVERY ROW must carry at least one anchor: a quote copied character-for-character from the DOCUMENT TEXT
(not from the analysis prose), 40-200 characters, with the right [doc_key]. A mechanical check drops any row whose
anchors are not verbatim, so copy exactly — do not fix typography, do not shorten with ellipses. The number of cells in
each row equals the number of columns. Never introduce a fact that is not in the documents."""

SPINE_SYSTEM = """You are the tables desk of The Analyst. The structure editor has decided what the dossier argues and which
sections need a table to PROVE their claim. You build exactly those tables — one per commissioned section, keyed by
its `section_key` — and nothing else. For each: the row unit and the columns the spine specified (you may sharpen a
column name, never change what a row is); every row carries the claims the spine says the rows must carry; the
`proves` line says in one sentence what the row set shows about the section's claim; the `note` is what the pattern
in the rows shows (never a restatement of the claim). Cells are short; the first column names the row.
EVERY ROW must carry at least one anchor: a quote copied character-for-character from the DOCUMENT TEXT (not from
the analysis prose), 40-200 characters, with the right [doc_key]. A mechanical check drops any row whose anchors are
not verbatim, so copy exactly — do not fix typography, do not shorten with ellipses. The section's planned anchors are
good starting points. The number of cells in each row equals the number of columns. Never introduce a fact that is
not in the documents. Numbers belong in cells, not in captions."""


# ── Legacy path (no spine) ───────────────────────────────────────────────

def _user(job: DossierJob, docs: list[Document], option_title: str, feedback: str = "") -> str:
    total = sum(d.char_count for d in docs)
    corpus_part = (
        f"DOCUMENT TEXT (copy anchors from here):\n\n{corpus_text(docs)}"
        if total <= CORPUS_IN_PROMPT_MAX_CHARS
        else "DOCUMENT TEXT: too large to include; copy anchors ONLY from the verbatim anchors in the reconnaissance profiles below."
    )
    audience = job.options.audience
    shape = ""
    from src.dossier.plan import chosen_option
    opt = chosen_option(job)
    if opt and opt.output_shape.tables:
        shape = "Table ideas from the brief: " + " | ".join(opt.output_shape.tables) + "\n"
    return (
        f"ANGLE: {option_title}\nAUDIENCE: {audience} — {AUDIENCE_REGISTER.get(audience, '')}\n{shape}"
        + (f"\n{feedback}\n" if feedback else "")
        + f"\nANALYSIS PROSE:\n{analysis_prose(job)}\n\nRECONNAISSANCE PROFILES:\n{compact_profiles(job.profiles)}\n\n{corpus_part}"
    )


def _pad_rows(t: Table) -> None:
    """Pad/trim rows to the column count (shape repair, recorded by the caller's report)."""
    ncol = len(t.columns)
    for r in t.rows:
        if len(r.cells) < ncol:
            r.cells.extend(Cell(value="") for _ in range(ncol - len(r.cells)))
        elif len(r.cells) > ncol:
            r.cells = r.cells[:ncol]


def _run_tables_legacy(job: DossierJob, docs: list[Document]) -> list[Table]:
    from src.dossier.plan import chosen_option

    opt = chosen_option(job)
    option_title = opt.title if opt else (job.options.intent or "dossier")
    corpus = NormalizedCorpus({d.key: d.text for d in docs})

    feedback = ""
    final: list[Table] = []
    for attempt in range(2):
        raw, _ = call_json(job.id, STEP, label="tables with verbatim anchors" + (" (re-ask)" if attempt else ""),
                           system=SYSTEM, user=_user(job, docs, option_title, feedback),
                           tool_name="record_tables", schema=TABLES_SCHEMA, model_cls=None, max_tokens=12000)
        tables: list[Table] = []
        for t in (raw or {}).get("tables", []):
            try:
                tables.append(Table.model_validate(t))
            except Exception as exc:
                logger.warning(f"table rejected by schema: {exc}")
        kept, failures = [], []
        for t in tables:
            _pad_rows(t)
            verified, report = verify_table(t, corpus)
            events.emit(job.id, "note", phase=STEP,
                        detail=f"anchor wall [{t.key}]: {len(verified.rows)}/{report['rows_in']} rows kept, "
                               f"{report['rows_dropped']} dropped, {report['anchors_trimmed']} anchors trimmed, {report['anchors_rekeyed']} re-keyed",
                        payload_json={"table": t.key, **report})
            failures.extend(report["failed_quotes"])
            if len(verified.rows) >= MIN_ROWS:
                kept.append(verified)
        final = kept
        if len(final) >= MIN_TABLES:
            break
        if attempt == 0:
            listed = "\n".join(f"- [{f['doc_key']}] “{f['quote']}”" for f in failures[:12]) or "(none listed)"
            feedback = ("PREVIOUS ATTEMPT: too few rows survived the verbatim check. These quotes were NOT found verbatim in the "
                        f"documents — copy exact text this time, shorter quotes (one sentence) are safer:\n{listed}")
            events.emit(job.id, "note", phase=STEP, detail=f"only {len(final)} table(s) survived the wall; re-asking with the failed quotes")
    if len(final) < MIN_TABLES:
        events.emit(job.id, "note", phase=STEP, detail=f"tables_short: only {len(final)} verified table(s) after re-ask")
    events.emit(job.id, "artifact", phase=STEP, detail=f"{len(final)} tables: " + " / ".join(t.caption for t in final),
                payload_json={"kind": "tables", "tables": [{"key": t.key, "caption": t.caption, "rows": len(t.rows), "rows_dropped": t.rows_dropped} for t in final]})
    return final


# ── Spine-driven path (pass E1) ──────────────────────────────────────────

def _snake(value: str, fallback: str) -> str:
    key = re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().lower()).strip("_")
    return key or fallback


def spine_tables_schema(section_keys: list[str], n: int) -> dict:
    item = {
        "type": "object", "additionalProperties": False,
        "required": ["section_key", "key", "caption", "columns", "rows", "note", "proves"],
        "properties": {
            "section_key": {"type": "string", "enum": section_keys, "description": "the spine section this table proves"},
            "key": {"type": "string", "description": "snake_case key, unique"},
            "caption": {"type": "string", "description": "what the table is; no numbers"},
            "columns": {"type": "array", "minItems": 2, "maxItems": 6, "items": {"type": "string"}},
            "rows": {"type": "array", "minItems": 2, "maxItems": 10,
                     "items": {"type": "object", "additionalProperties": False, "required": ["cells"],
                               "properties": {"cells": {"type": "array", "items": CELL_SCHEMA}}}},
            "note": {"type": "string", "description": "one line: what the pattern in the rows shows (not the claim restated)"},
            "proves": {"type": "string", "description": "one sentence: what this row set shows about the section's claim"},
        },
    }
    return {"type": "object", "additionalProperties": False, "required": ["tables"],
            "properties": {"tables": {"type": "array", "minItems": 1, "maxItems": max(1, n), "items": item}}}


def _specs_text(spine: DossierSpine, only: Optional[set[str]] = None) -> str:
    parts = []
    for s in spine.table_sections():
        if only is not None and s.key not in only:
            continue
        t = s.table
        anchors = "\n".join(f"    • [{a.doc_key}] “{a.quote}”" for a in s.anchors_planned) or "    (none planned)"
        parts.append(
            f"### section_key: {s.key} — “{s.heading}”\n  claim: {s.claim}\n  table intent: {t.intent}\n  one row = {t.row_unit}\n"
            f"  columns: {' | '.join(t.columns)}\n  the rows must carry: {'; '.join(t.carries_claims)}\n  planned anchors:\n{anchors}"
        )
    return "\n\n".join(parts)


def _spine_user(job: DossierJob, docs: list[Document]) -> str:
    from src.dossier.plan import chosen_option

    opt = chosen_option(job)
    total = sum(d.char_count for d in docs)
    corpus_part = (f"DOCUMENT TEXT (copy anchors from here):\n\n{corpus_text(docs)}" if total <= CORPUS_IN_PROMPT_MAX_CHARS
                   else "DOCUMENT TEXT: too large to include; copy anchors ONLY from the verbatim anchors in the reconnaissance profiles below.")
    audience = job.options.audience
    spine = job.spine
    return (
        f"ANGLE: {opt.title if opt else (job.options.intent or 'dossier')}\nTHESIS: {spine.thesis}\n"
        f"AUDIENCE: {audience} — {AUDIENCE_REGISTER.get(audience, '')}\n\n"
        f"TABLES COMMISSIONED BY THE SPINE (build exactly these, one per section_key):\n\n{_specs_text(spine)}\n\n"
        f"ANALYSIS PROSE:\n{analysis_prose(job)}\n\nRECONNAISSANCE PROFILES:\n{compact_profiles(job.profiles)}\n\n{corpus_part}"
    )


def _admit(job: DossierJob, raw: dict, wanted: set[str], corpus: NormalizedCorpus, seen_keys: set[str]) -> tuple[dict[str, Table], list[dict], list[Finding], list[str]]:
    """Coerce, wall and key the answered tables by section. Returns (accepted by section, failed quotes, findings, rejects)."""
    accepted: dict[str, Table] = {}
    failures: list[dict] = []
    minted: list[Finding] = []
    rejects: list[str] = []
    for item in (raw or {}).get("tables", []) or []:
        if not isinstance(item, dict):
            continue
        sk = str(item.get("section_key", "")).strip()
        if sk not in wanted:
            rejects.append(f"{item.get('key')}: section_key {sk!r} was not commissioned")
            continue
        if sk in accepted:
            rejects.append(f"{item.get('key')}: section {sk} already has a table (one per section)")
            continue
        try:
            t = Table.model_validate({k: v for k, v in item.items() if k in Table.model_fields})
        except Exception as exc:
            rejects.append(f"{item.get('key')}: {str(exc)[:160]}")
            continue
        t.key = _snake(t.key, f"{sk}_table")
        if t.key in seen_keys:
            t.key = f"{t.key}_{sk}"
        t.section_key = sk
        t.proves = str(item.get("proves", "")).strip()
        _pad_rows(t)
        verified, report = verify_table(t, corpus)
        events.emit(job.id, "note", phase=STEP,
                    detail=f"anchor wall [{t.key} → {sk}]: {len(verified.rows)}/{report['rows_in']} rows kept, "
                           f"{report['rows_dropped']} dropped, {report['anchors_trimmed']} anchors trimmed, {report['anchors_rekeyed']} re-keyed",
                    payload_json={"table": t.key, "section_key": sk, **report})
        failures.extend(report["failed_quotes"])
        if len(verified.rows) >= MIN_ROWS:
            accepted[sk] = verified
            seen_keys.add(t.key)
            if report["rows_dropped"]:
                minted.append(ledger.mint("table_rows_dropped", where={"section_key": sk, "table_key": t.key}, source="wall", affordance="revise_table_rows",
                                          note=f"{report['rows_dropped']} of {report['rows_in']} rows were dropped because no anchor was verbatim; the table proves less than it was asked to. Cure: re-derive the missing rows with exact quotes.",
                                          quote="; ".join(f['quote'][:80] for f in report["failed_quotes"][:3])))
        else:
            rejects.append(f"{t.key}: only {len(verified.rows)} row(s) survived the anchor wall for section {sk}")
    return accepted, failures, minted, rejects


def run_spine_tables(job: DossierJob, docs: list[Document], persist=None) -> list[Table]:
    spine = job.spine
    specs = spine.table_sections()
    wanted = {s.key for s in specs}
    corpus = NormalizedCorpus({d.key: d.text for d in docs})
    user = _spine_user(job, docs)
    schema = spine_tables_schema(sorted(wanted), len(wanted))
    seen: set[str] = set()
    raw, _ = call_json(job.id, STEP, label=f"tables from the spine ({len(wanted)})", system=SPINE_SYSTEM, user=user,
                       tool_name="record_tables", schema=schema, model_cls=None, max_tokens=12000, cache=True)
    accepted, failures, minted, rejects = _admit(job, raw, wanted, corpus, seen)
    missing = [s for s in specs if s.key not in accepted]
    if missing:
        listed = "\n".join(f"- [{f['doc_key']}] “{f['quote']}”" for f in failures[:12]) or "(none listed)"
        tail = ("---\nRE-ASK for the sections whose table did not survive the wall: " + ", ".join(s.key for s in missing)
                + ". Return ONLY those tables (the others are kept). " + (" | ".join(rejects[:6]) + ". " if rejects else "")
                + f"These quotes were NOT found verbatim — copy exact text this time; shorter quotes (one sentence) are safer:\n{listed}")
        events.emit(job.id, "note", phase=STEP, detail=f"{len(missing)} commissioned table(s) fell short of the wall; re-asking once for " + ", ".join(s.key for s in missing))
        raw2, _ = call_json(job.id, STEP, label=f"tables re-ask ({len(missing)})", system=SPINE_SYSTEM, user=user, user_tail=tail,
                            tool_name="record_tables", schema=spine_tables_schema(sorted(s.key for s in missing), len(missing)),
                            model_cls=None, max_tokens=12000, cache=True)
        more, _, minted2, rejects2 = _admit(job, raw2, {s.key for s in missing}, corpus, seen)
        accepted.update(more)
        minted.extend(minted2)
        for s in missing:
            if s.key not in accepted:
                why = next((r for r in rejects2 if s.key in r), "no table returned")
                minted.append(ledger.mint("table_unavailable", where={"section_key": s.key}, source="wall", affordance="add_table",
                                          note=f"The spine asked section “{s.heading}” for a table ({s.table.intent}); none survived the anchor wall ({why}). The section proceeds without it — the writer must carry the claim in prose.",
                                          realization=f"one row = {s.table.row_unit}; columns: {' | '.join(s.table.columns)}"))
                events.emit(job.id, "note", phase=STEP, detail=f"table_unavailable for section {s.key}: {why}",
                            payload_json={"kind": "table_unavailable", "section_key": s.key, "reason": why})
    final = [accepted[s.key] for s in specs if s.key in accepted]
    ledger.append(job, minted, persist)
    line = "; ".join(f"Table for “{spine.section(t.section_key).heading[:40]}” ({len(t.rows)} rows verified" + (f", {t.rows_dropped} dropped" if t.rows_dropped else "") + ")" for t in final) or "no table survived"
    narr = f"Building the exhibits the argument asked for — {line}." + (f" {len(specs) - len(final)} commissioned table(s) could not be anchored and were recorded as findings." if len(final) < len(specs) else "")
    events.emit(job.id, "narration", phase=STEP, narrator=narr, detail=narr)
    events.emit(job.id, "artifact", phase=STEP, detail=f"{len(final)} tables: " + " / ".join(t.caption for t in final),
                payload_json={"kind": "tables", "tables": [{"key": t.key, "section_key": t.section_key, "caption": t.caption, "proves": t.proves,
                                                            "rows": len(t.rows), "rows_dropped": t.rows_dropped} for t in final],
                              "findings": [f.kind for f in minted]})
    return final


def run_tables(job: DossierJob, docs: list[Document], persist=None) -> list[Table]:
    if not job.options.output.tables:
        events.emit(job.id, "note", phase=STEP, detail="tables_skipped: none requested")
        return []
    if job.spine is not None:
        if not job.spine.table_sections():
            events.emit(job.id, "note", phase=STEP, detail="tables_skipped: the spine commissioned no table")
            return []
        return run_spine_tables(job, docs, persist)
    return _run_tables_legacy(job, docs)
