"""Step 5 — tables: 2-3 evidence tables with verbatim anchors, behind the anchor wall.

Inputs: the analysis prose, the document profiles (whose anchors are already
verified quotes) and — when it fits — the document text itself, so the model
can copy quotes exactly. Every row must keep at least one verified anchor;
rows that fail are dropped and counted (`rows_dropped`). If fewer than two
tables survive, the call is re-asked once with the failed quotes listed.
"""
from __future__ import annotations

import logging

from src.dossier import events
from src.dossier.common import AUDIENCE_REGISTER, analysis_prose, compact_profiles, corpus_text
from src.dossier.llm import call_json
from src.dossier.schemas import DossierJob, Table
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


def run_tables(job: DossierJob, docs: list[Document]) -> list[Table]:
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
            # pad/trim rows to the column count (shape repair, recorded)
            ncol = len(t.columns)
            for r in t.rows:
                if len(r.cells) < ncol:
                    from src.dossier.schemas import Cell
                    r.cells.extend(Cell(value="") for _ in range(ncol - len(r.cells)))
                elif len(r.cells) > ncol:
                    r.cells = r.cells[:ncol]
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
