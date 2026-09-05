"""Prompt composition for the process shape (study 2026-09-04): extract → verify → synthesize.

Three prompts, one per step kind, composed from an engine's capability definition (the
problematique) and its operationalization's ProcessSpec (text-facing dimensions with method
cards, the steps, the synthesis brief). The findings ledger is the only hand-off, so the
extraction and verification prompts ask for ledgers and nothing else; the synthesis prompt
asks for the reading a reader needs, citing rows by id, followed by the final ledger.

Walls (code) check anchors and ids afterwards; nothing here judges meaning.
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from src.operationalizations.schemas import ProcessDimension, ProcessSpec, ProcessStep

LEDGER_HEADING = "## Findings ledger"

ANCHORING_LAW = (
    "**Anchoring law**: every row rests on a short verbatim quote from the text (at most 200 characters, "
    "copied exactly, in double quotation marks, no ellipses, typography untouched). "
    "Write each anchor value as one JSON string, escaping internal double quotation marks and backslashes "
    "without changing the quoted text. A finding you cannot "
    "anchor is a hypothesis: say so in the row or leave it out. Do not invent citations, dates, names or "
    "numbers that are not in the text. Everything you write is checked against the source by code and by "
    "a critic; a row whose anchor is not verbatim is dropped."
)

TEXT_NOT_AUTHORS = (
    "**About the text, not the authors**: say what the text presupposes, cites, borrows, dismisses, "
    "brackets or renames, with the sentence that does it. Do not say what the authors intended, knew, "
    "feared, concealed, or where they trained; if provenance or motive is your inference, tag the row "
    "`provenance: hypothesis` and keep the sentence about the text."
)

CORPUS_ANCHORS = (
    "**Corpus anchors**: preserve every anchor/document pair through verification and synthesis. A cross-document "
    "row requires at least two distinct source keys: `anchor: \"<quote A>\" — doc: <A> — "
    "anchor-b: \"<quote B>\" — doc-b: <B>`. For further documents use anchor-c/doc-c, and so on. "
    "Code verifies each quote only in its named document. Keep the corpus dimension key on these rows."
)

CORPUS_READING = (
    "## Reading the whole corpus\n\n"
    "The unit of analysis is the complete supplied collection. Begin with a compact position map: "
    "name every document, its central claim, distinctive argumentative role, and an important qualification. "
    "Then develop the main reading through supported cross-document relations, applying the engine's "
    "questions below to continuities, revisions, divergences and independent argument routes. This "
    "corpus order governs the section order below. Give each assessed document anchored representation "
    "in the final findings; explicitly identify any document you cannot assess and why.\n\n"
    "For each cross-document claim, preserve document-keyed quotations for every document it covers "
    "(at least two). Identify each passage's object, scope and inferential role, then explain what "
    "persists or changes. Shared vocabulary alone does not establish "
    "inheritance or change. Distinguish a repeated or reargued claim from one subsequently presupposed. "
    "Check earlier formulations before naming an innovation or disappearance. Separate composition "
    "dates, edition dates and argumentative development; do not infer an order between same-year texts "
    "from their input order. Where development is not established, describe continuity or divergence "
    "with that limit. End with a judgment about the position across the collection."
)


class ProcessPrompt(BaseModel):
    """A composed prompt for one step invocation."""

    engine_key: str
    step_key: str
    kind: str
    dimension_key: str = ""
    doc_key: str = ""
    system: str
    user: str
    model_tier: str = "strong"
    label: str = ""
    id_prefix: str = ""
    expected_rows: int = 0


def dim_prefix(dim: ProcessDimension) -> str:
    return dim.id_prefix or dim.key.upper()


def document_prefix(prefix: str, documents: dict[str, str], doc_key: str) -> str:
    """A stable per-input ordinal keeps findings and critic additions unique across documents."""
    return f"{prefix}.DOC{list(documents).index(doc_key) + 1}" if len(documents) > 1 and doc_key else prefix


def _framing(cap_def, spec: ProcessSpec, title: str) -> str:
    problematique = (getattr(cap_def, "problematique", "") or "").strip()
    first = problematique.split("\n\n")[0].strip() if problematique else ""
    lines = [f"# {cap_def.engine_name} — {title}", ""]
    if first:
        lines += ["## The method", "", first, ""]
    if spec.description:
        lines += [spec.description.strip(), ""]
    return "\n".join(lines).rstrip()


def _method_card(dim: ProcessDimension, prefix: str = "") -> str:
    prefix = prefix or dim_prefix(dim)
    lines = [f"### {dim.name} (rows `[{prefix}.F<n>]`)", ""]
    if dim.method_card:
        lines += ["**Method card**", "", dim.method_card.strip(), ""]
    if dim.indicators:
        lines += ["**Indicators to hunt for**", ""] + [f"- {i}" for i in dim.indicators] + [""]
    if dim.questions:
        lines += ["**Questions**", ""] + [f"- {q}" for q in dim.questions] + [""]
    if dim.answer_shape:
        lines += ["**Answer shape**", "", f"`{dim.answer_shape.strip().replace(dim_prefix(dim) + '.F', prefix + '.F')}`", ""]
    return "\n".join(lines).rstrip()


def _source_block(documents: dict[str, str]) -> str:
    if len(documents) == 1:
        (k, v), = documents.items()
        return f"SOURCE [{k}]:\n\n{v}"
    parts = [f"SOURCE [{k}]:\n\n{v}" for k, v in documents.items()]
    return "\n\n=====\n\n".join(parts)


# ── Extract ───────────────────────────────────────────────────────────────

def compose_extract_prompt(
    cap_def, spec: ProcessSpec, step: ProcessStep, dim: ProcessDimension, documents: dict[str, str],
    *, doc_key: str = "", prior_ledgers: str = "",
) -> ProcessPrompt:
    """One dimension, one document (or, for corpus dimensions, the per-document ledgers)."""
    prefix = document_prefix(dim_prefix(dim), documents, doc_key)
    rows_hint = f"8 to {step.max_rows}" if step.max_rows > 8 else str(step.max_rows)
    corpus_dim = dim.scope == "corpus"
    sections = [
        _framing(cap_def, spec, f"extraction: {dim.name}"),
        "## Your task",
        (
            "Read the source with the one question set below and return only a findings ledger: "
            "anchored rows, no essay, no headings of your own, no summary of the text. "
            "Other extractions cover the other dimensions; do not stray into them."
            if not corpus_dim else
            "Read the per-document ledgers below (they are anchored findings extracted from each document) "
            "and return only a findings ledger of cross-document findings. Every row carries one anchor "
            "from each document it relates, with its [doc_key]."
        ),
        _method_card(dim, prefix),
        ANCHORING_LAW,
        CORPUS_ANCHORS if corpus_dim else "",
        TEXT_NOT_AUTHORS,
        "## Output (exactly this, nothing before it)",
        "\n".join([
            LEDGER_HEADING,
            f"- [{prefix}.F1] <the finding in one sentence> — dim: {dim.key} — anchor: \"<verbatim quote>\""
            + (" — doc: <doc_key>" if len(documents) > 1 else "")
            + (' — anchor-b: "<verbatim quote from another document>" — doc-b: <other_doc_key>' if corpus_dim else "")
            + " — <the typed fields of the answer shape> — confidence: high|medium|low",
            f"- [{prefix}.F2] …",
            f"({rows_hint} rows, ids consecutive; one finding per row; the typed fields follow the answer shape above)",
            "### Counter-evidence",
            "- <what in the text cuts against a row, anchored, naming the row id>",
            "### Open questions",
            "- <what the text cannot settle for this dimension>",
        ]),
    ]
    system = "\n\n".join(s for s in sections if s)
    if corpus_dim:
        user = prior_ledgers or "(no per-document ledgers)"
    else:
        user = _source_block(documents if not doc_key else {doc_key: documents[doc_key]})
    return ProcessPrompt(
        engine_key=cap_def.engine_key, step_key=step.key, kind="extract", dimension_key=dim.key,
        doc_key=doc_key, system=system, user=user, model_tier=step.model_tier,
        label=f"{cap_def.engine_key} | {step.key} | {dim.key}" + (f" | {doc_key}" if doc_key else ""),
        id_prefix=prefix, expected_rows=step.max_rows,
    )


# ── Verify ────────────────────────────────────────────────────────────────

DUTY_TEXT = {
    "check_anchors_in_context": (
        "For every row, find the anchor in the source and read the sentences around it. Rule the row "
        "`confirmed` (the anchor supports the finding as stated), `weakened` (the anchor supports a narrower "
        "or more hedged finding: rewrite the finding to what the text supports) or `rejected` (the anchor does "
        "not support it, or the finding is not about the text). Give one line of reason: what the anchor says, "
        "what the row claimed. Preserve the speaker, negation, conditions and scope. An exhaustive claim "
        "such as 'only', 'entirely', 'all' or 'never' needs support for that scope, not merely one matching example. "
        "For a weakened row, put the replacement in the row's finding and in an explicit "
        '`revised-finding: "<replacement>"` field (a JSON quoted string). Do not put the replacement only in the reason.'
    ),
    "reject_biography": (
        "Reject any row whose finding is about the authors rather than the text: their motives, careers, "
        "school, what they knew or concealed, proportion estimates with no textual basis. A row may keep a "
        "provenance hypothesis only if its finding is about a sentence of the text."
    ),
    "reject_summary": (
        "Reject rows that summarise or paraphrase the text instead of mapping it (a row that restates a claim "
        "without naming its grounds, warrant, scheme, attack type or gap is a summary)."
    ),
    "reconcile_ids": (
        "Reconcile the inventories across dimensions: one list of claims (C1, C2, C2.1 …), one of grounds "
        "(G1 …), one of suppressed premises (S1 …), one of inferences (I1 …). Where two extractions found the "
        "same claim or ground under different words, keep one row, cite the merged ids in `merged:`, and "
        "rewrite cross-references so every C/G/S/I id used anywhere exists once."
    ),
    "merge_duplicates": (
        "Merge duplicate findings across dimensions: keep the better-anchored row, list the merged ids in "
        "`merged:`; mark the others `rejected — duplicate of <id>`."
    ),
    "rerun_critical_questions": (
        "For the three inferences that carry the most weight, run the scheme's critical questions yourself "
        "against the source and record the answers as rows (addressed at \"<anchor>\" | unaddressed), even "
        "where an extraction already named the scheme."
    ),
    "hunt_misses": (
        "Hunt for misses: for each dimension, what does the text support that no row contains? Add each as a "
        "new row `[V.F<n>]` with `dim:` and a verbatim anchor and `status: added`. Aim at the findings the "
        "reading would be poorer without, not at volume."
    ),
    "name_must_keep": (
        "End with `### Must keep`: the three to five row ids the synthesis must not lose, one line each on why."
    ),
}


def compose_verify_prompt(
    cap_def, spec: ProcessSpec, step: ProcessStep, documents: dict[str, str], ledgers_text: str,
    *, doc_key: str = "",
) -> ProcessPrompt:
    duties = step.duties or ["check_anchors_in_context", "merge_duplicates", "hunt_misses", "name_must_keep"]
    prefix = document_prefix("V", documents, doc_key)
    if len(documents) > 1 and not doc_key:
        prefix = "V.CORPUS"
    duty_lines = []
    for i, d in enumerate(duties, 1):
        duty_lines.append(f"{i}. {DUTY_TEXT.get(d, d).replace('V.F', prefix + '.F')}")
    cards = "\n\n".join(_method_card(d) for d in spec.dimensions if d.scope == "document" or (len(documents) > 1 and not doc_key))
    sections = [
        _framing(cap_def, spec, "verification"),
        "## Your task",
        "You are the critic. Extractions on the source produced the ledgers below. Check every row against "
        "the source, in order of the duties, and return one verified ledger. You are not writing the reading; "
        "you are deciding what the reading may rest on. Be adversarial about anchors and about over-reading, "
        "and generous in the hunt for misses.",
        "## Duties, in order",
        "\n".join(duty_lines),
        "## The dimensions the extractions answered",
        cards,
        ANCHORING_LAW,
        CORPUS_ANCHORS if len(documents) > 1 else "",
        TEXT_NOT_AUTHORS,
        "## Output (exactly this, nothing before it)",
        "\n".join([
            LEDGER_HEADING,
            "- [<original id>] <finding, rewritten if weakened> — dim: <key> — anchor: \"<verbatim>\""
            + (" — doc: <doc_key>" if len(documents) > 1 else "")
            + " — <typed fields kept> — status: confirmed|weakened|rejected — reason: <one line> — confidence: high|medium|low",
            f'- [{prefix}.F1] <a miss> — dim: <key> — anchor: "<verbatim>"'
            + (" — doc: <doc_key>" if len(documents) > 1 else "") + " — status: added — confidence: …",
            '(For cross-document rows keep both `anchor: "<A>" — doc: <A> — anchor-b: "<B>" — doc-b: <B>`.)'
            if len(documents) > 1 and not doc_key else "",
            "(every input row appears once with a status; rejected rows keep their id and reason so the receipt is complete)",
            "### Must keep",
            "- <id>: <why>",
            "### Counter-evidence",
            "- <anchored, naming the row it cuts against>",
            "### Open questions",
            "- <what the text cannot settle>",
        ]),
    ]
    system = "\n\n".join(s for s in sections if s)
    src = _source_block(documents if not doc_key else {doc_key: documents[doc_key]})
    user = f"{src}\n\n=====\n\nEXTRACTION LEDGERS:\n\n{ledgers_text}"
    return ProcessPrompt(
        engine_key=cap_def.engine_key, step_key=step.key, kind="verify", doc_key=doc_key,
        system=system, user=user, model_tier=step.model_tier,
        label=f"{cap_def.engine_key} | {step.key}" + (f" | {doc_key}" if doc_key else ""), id_prefix=prefix,
    )


# ── Synthesize ────────────────────────────────────────────────────────────

def compose_synthesize_prompt(
    cap_def, spec: ProcessSpec, step: ProcessStep, documents: dict[str, str], verified_ledger_text: str,
    *, rejected_text: str = "",
) -> ProcessPrompt:
    reader = step.reader or "an expert reader who must decide what this text establishes"
    cards = "\n\n".join(
        f"**{d.name}**: {d.method_card.strip()}" for d in spec.dimensions if d.method_card
    )
    tables = ""
    if step.tables:
        tables = "\n".join(f"- {t}: rows <ids>" for t in step.tables)
    sections = [
        _framing(cap_def, spec, "the reading"),
        "## Your task",
        f"Write the reading for {reader}. Its material is the verified findings ledger below (rows a critic "
        "confirmed against the source, with the misses the critic added) and the source itself. This is the "
        "engine's product: it is read by the dossier's desks (spine, tables, figures) and by a person, not by "
        "another pass.",
        CORPUS_READING if len(documents) > 1 else "",
        "## What the reading contains, in order",
        (step.brief or "").strip(),
        "## Method cards (what the tradition asks you to do)",
        cards,
        ANCHORING_LAW,
        CORPUS_ANCHORS if len(documents) > 1 else "",
        TEXT_NOT_AUTHORS,
        "## Rules",
        "\n".join([
            "- One line of argument through the material, in the order a reader needs it; not a list under dimension headings.",
            "- Cite findings inline by id, e.g. `[D1.F3]` or `[V.F2]`, and quote their anchors where the sentence needs the text's own words.",
            "- No claim without a row. If the ledger lacks what a sentence needs, either leave the sentence out or add the row to the final ledger with a verbatim anchor.",
            "- Rows the critic rejected are listed under REJECTED; do not reintroduce them.",
            "- No process narration: never mention passes, extractions, ledgers, critics or dimensions as process; the reader sees a reading.",
            "- Length: as long as the argument needs and no longer (typically 10-18K characters before the ledger).",
        ]),
        "## Output",
        "\n".join([
            "The reading (headed sections in the reader's terms), then:",
            LEDGER_HEADING,
            "- [F1] <finding> — dim: <key> — anchor: \"<verbatim>\""
            + (" — doc: <doc_key>" if len(documents) > 1 else "")
            + " — from: <the row ids it rests on> — confidence: high|medium|low",
            '(Cross-document rows also retain `anchor-b: "<verbatim B>" — doc-b: <B>` and all further pairs.)'
            if len(documents) > 1 else "",
            "(renumber F1..Fn in the order the reading uses them; 12-30 rows; every row the reading cites appears here)",
            "### Counter-evidence",
            "- <anchored>",
            "### Open questions",
            "- <what the text cannot settle>",
            "### Tables" if tables else "",
            tables,
        ]).rstrip(),
    ]
    system = "\n\n".join(s for s in sections if s)
    user = f"{_source_block(documents)}\n\n=====\n\nVERIFIED FINDINGS LEDGER:\n\n{verified_ledger_text}"
    if rejected_text:
        user += f"\n\n=====\n\nREJECTED BY THE CRITIC (do not reintroduce):\n\n{rejected_text}"
    return ProcessPrompt(
        engine_key=cap_def.engine_key, step_key=step.key, kind="synthesize", system=system, user=user,
        model_tier=step.model_tier, label=f"{cap_def.engine_key} | {step.key}", id_prefix="F",
    )


# ── One-shot with the rewritten questions (frontier condition (a)) ─────────

def compose_oneshot_prompt(cap_def, spec: ProcessSpec, documents: dict[str, str]) -> ProcessPrompt:
    """The whole shape in one prompt on one model: every method card and question set, then the reading
    the synthesis brief asks for, with the ledger. The study's condition (a)."""
    final = spec.final_step
    reader = (final.reader if final else "") or "an expert reader who must decide what this text establishes"
    cards = "\n\n".join(_method_card(d) for d in spec.dimensions if d.scope == "document" or len(documents) > 1)
    sections = [
        _framing(cap_def, spec, "the reading (one call)"),
        "## Your task",
        f"Read the source with the question sets below, in your own order, and write the reading for {reader}. "
        "Work through the questions to find the material; do not answer them one by one in the output.",
        CORPUS_READING if len(documents) > 1 else "",
        "## Dimensions",
        cards,
        "## What the reading contains, in order",
        ((final.brief if final else "") or "").strip(),
        ANCHORING_LAW,
        CORPUS_ANCHORS if len(documents) > 1 else "",
        TEXT_NOT_AUTHORS,
        "## Output",
        "\n".join([
            "The reading (one line of argument, headed sections in the reader's terms, verbatim quotes where the sentence needs them), then:",
            LEDGER_HEADING,
            "- [F1] <finding> — dim: <key> — anchor: \"<verbatim>\""
            + (" — doc: <doc_key>" if len(documents) > 1 else "") + " — confidence: high|medium|low",
            "(12-30 rows in the order the reading uses them)",
            "### Counter-evidence",
            "### Open questions",
        ]),
    ]
    system = "\n\n".join(s for s in sections if s)
    return ProcessPrompt(
        engine_key=cap_def.engine_key, step_key="oneshot", kind="synthesize", system=system,
        user=_source_block(documents), model_tier="strong", label=f"{cap_def.engine_key} | oneshot", id_prefix="F",
    )
