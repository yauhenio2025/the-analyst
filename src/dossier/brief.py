"""Step 2 — the brief, deliverable-first: three DELIVERABLES the requester could commission.

Each option is a promise about use — what you get, what you will understand, what you will be
able to do, what it will not tell you — verified against a concrete shape (sections, tables with a
row unit, figures with a format) and the documents that carry it. Engines are the secondary "how".
Design + prompt spec: communications/DESIGN_brief_deliverables.md §B.

Sonnet proposes; code checks (§B5): use disjointness, concreteness, support refs, row units,
audience vocabulary, lengths, engine keys, weight spread, the recommendation. One repair round,
then code fixes what it can and records what it changed. Prices are arithmetic from each option's
own path, so the three options cost differently.

Lanes (§C): entry = "use" (default) → three options differing by use; "chosen" → translate mode:
the fixed path's one option + the desk's alternative; "material" → the recommendation is executed.
"""
from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from typing import Any, Optional

from src.dossier import events
from src.dossier.catalog import (USE_REGISTER, ban_terms, catalog_purpose_text, estimate_path, jargon_hits,
                                 path_depth_from_steps, plain_name_for, plain_name_lines, purpose_catalog,
                                 resolve_path_request, validate_steps, vocabulary_lines)
from src.dossier.common import AUDIENCE_REGISTER, compact_profiles, engine_catalog
from src.dossier.llm import call_json
from src.dossier.schemas import (DELIVERABLE_KINDS, DEPTHS, FIGURE_FORMATS, STEP_DEPTHS, USE_KINDS, Brief,
                                 BriefDefaults, BriefOption, DossierJob, Path, PathStep, Promise, Recommendation,
                                 Shape, ShapeRef, TableSpec)
from src.sources.schemas import Document

logger = logging.getLogger(__name__)

STEP = "brief"

# ── the tool schema (model-facing: no est_*, no legacy views) ──────────────

CAPS = {
    "deliverable": 110, "understand": 140, "able_to": 120, "question": 120, "not_for": 120, "best_when": 140,
    "heading": 70, "answers": 120, "table_title": 90, "row_unit": 60, "column": 30, "figure_title": 90,
    "scene": 220, "contributes": 120, "because": 220, "carries": 100, "thin": 140,
}
TITLE_MAX_WORDS = 10

_REF = {"type": "object", "additionalProperties": False, "required": ["kind", "index"],
        "properties": {"kind": {"type": "string", "enum": ["section", "table", "figure"]},
                       "index": {"type": "integer", "minimum": 1, "description": "1-based index within shape.sections / tables / figures"}}}
_PROMISE = {"type": "object", "additionalProperties": False, "required": ["text", "supported_by"],
            "properties": {"text": {"type": "string"},
                           "supported_by": {"type": "array", "minItems": 1, "items": _REF,
                                            "description": "the section (S), table (T) or figure (F) that keeps this promise"}}}
_SHAPE = {"type": "object", "additionalProperties": False, "required": ["sections", "tables", "figures"],
          "properties": {
              "sections": {"type": "array", "minItems": 3, "maxItems": 6,
                           "items": {"type": "object", "additionalProperties": False, "required": ["heading", "answers"],
                                     "properties": {"heading": {"type": "string", "description": "<= 70 chars"},
                                                    "answers": {"type": "string", "description": "the question (from questions_answered) this section answers"}}}},
              "tables": {"type": "array", "minItems": 1, "maxItems": 3,
                         "items": {"type": "object", "additionalProperties": False,
                                   "required": ["title", "row_unit", "columns", "rows_expected", "carried_by"],
                                   "properties": {"title": {"type": "string"},
                                                  "row_unit": {"type": "string", "description": "MUST start with 'one row per', e.g. 'one row per claim type'"},
                                                  "columns": {"type": "array", "minItems": 3, "maxItems": 5, "items": {"type": "string"}},
                                                  "rows_expected": {"type": "string", "description": "e.g. '8-10'"},
                                                  "carried_by": {"type": "array", "items": {"type": "string"}, "description": "doc_keys whose text fills the cells"}}}},
              "figures": {"type": "array", "minItems": 0, "maxItems": 3,
                          "items": {"type": "object", "additionalProperties": False, "required": ["title", "format", "scene"],
                                    "properties": {"title": {"type": "string"},
                                                   "format": {"type": "string", "enum": list(FIGURE_FORMATS)},
                                                   "scene": {"type": "string", "description": "a depictable scene, no text in the image, <= 220 chars"}}}},
          }}
_EVIDENCE = {"type": "object", "additionalProperties": False, "required": ["carrying_docs", "thin_or_missing"],
             "properties": {"carrying_docs": {"type": "array", "minItems": 1,
                                              "items": {"type": "object", "additionalProperties": False, "required": ["doc_key", "carries"],
                                                        "properties": {"doc_key": {"type": "string"}, "carries": {"type": "string"}}}},
                            "thin_or_missing": {"type": "array", "items": {"type": "string"}, "description": "what these documents do not carry, <= 140 each"}}}
_PATH = {"type": "object", "additionalProperties": False, "required": ["steps"],
         "properties": {"steps": {"type": "array", "minItems": 1, "maxItems": 4,
                                  "items": {"type": "object", "additionalProperties": False, "required": ["engine_key", "plain_name", "contributes", "depth"],
                                            "properties": {"engine_key": {"type": "string", "description": "from the executable catalog only"},
                                                           "plain_name": {"type": "string", "description": "the reader-register name supplied for this engine, verbatim"},
                                                           "contributes": {"type": "string", "description": "what this step adds to THIS deliverable, in reader terms, <= 120"},
                                                           "depth": {"type": "string", "enum": list(STEP_DEPTHS)}}}}}}


def option_schema(translate: bool = False) -> dict:
    props = {
        "key": {"type": "string", "description": "short snake_case key, e.g. claims_stress_test"},
        "title": {"type": "string", "description": "<= 10 words, reader register"},
        "deliverable_kind": {"type": "string", "enum": list(DELIVERABLE_KINDS)},
        "deliverable": {"type": "string", "description": "what you get, in one line: e.g. 'a 5-section stress test of the four claim types a house makes, with a scorecard of what each commits you to' (<= 110)"},
        "use_kind": {"type": "string", "enum": list(USE_KINDS), "description": "the option's job-to-be-done, from the use register"},
        "you_will_understand": {"type": "array", "minItems": 3, "maxItems": 3, "items": _PROMISE,
                                "description": "exactly 3; each names something concrete from the documents (entity, number, date, verbatim phrase, or [DOC_KEY]); <= 140 each"},
        "you_will_be_able_to": {"type": "array", "minItems": 2, "maxItems": 3, "items": _PROMISE,
                                "description": "2-3, verb-first ('decide …', 'brief …', 'set …'); each points at the T/S/F that supports it; <= 120 each"},
        "questions_answered": {"type": "array", "minItems": 3, "maxItems": 4, "items": {"type": "string"}, "description": "3-4 questions the dossier answers, <= 120 each"},
        "not_for": {"type": "array", "minItems": 1, "maxItems": 3, "items": {"type": "string"},
                    "description": "what these documents cannot deliver: house-internal data, forecasts, actors not in the corpus, single-source limits, sample sizes; <= 120 each"},
        "shape": _SHAPE,
        "evidence_base": _EVIDENCE,
        "path": _PATH,
        "best_when": {"type": "string", "description": "'Pick this when …', <= 140"},
    }
    required = ["key", "title", "deliverable_kind", "deliverable", "use_kind", "you_will_understand", "you_will_be_able_to",
                "questions_answered", "not_for", "shape", "evidence_base", "path", "best_when"]
    if translate:
        props["alternative"] = {"type": "boolean", "description": "false for the option the FIXED path yields; true for the desk's alternative"}
        required.append("alternative")
    return {"type": "object", "additionalProperties": False, "required": required, "properties": props}


def brief_schema(translate: bool = False) -> dict:
    n = 2 if translate else 3
    return {
        "type": "object", "additionalProperties": False, "required": ["options", "recommendation", "defaults"],
        "properties": {
            "options": {"type": "array", "minItems": n, "maxItems": n, "items": option_schema(translate)},
            "recommendation": {"type": "object", "additionalProperties": False, "required": ["option_key", "because", "runner_up", "runner_up_because"],
                               "properties": {"option_key": {"type": "string"},
                                              "because": {"type": "string", "description": "one sentence the reader would accept: what the documents hold, what they lack (<= 220)"},
                                              "runner_up": {"type": "string"},
                                              "runner_up_because": {"type": "string"}}},
            "defaults": {"type": "object", "additionalProperties": False, "required": ["audience", "depth", "figures"],
                         "properties": {"audience": {"type": "string", "enum": ["executive", "researcher", "analyst"]},
                                        "depth": {"type": "string", "enum": list(DEPTHS)},
                                        "figures": {"type": "integer", "minimum": 0, "maximum": 4}}},
        },
    }


# ── the prompt (§B4) ──────────────────────────────────────────────────────

SYSTEM_HEAD = """You are the brief desk of The Analyst. The desk has read a corpus (reconnaissance below) and must offer the requester
exactly THREE DELIVERABLES they could commission — three different USES of the same documents, not three topics and
not three phrasings of one idea. A deliverable is judged by what its reader will UNDERSTAND and be ABLE TO DO
afterwards, and by the honesty of what it will NOT tell them.

Rules (all are checked by code; a violation returns the brief to you for repair):"""

RULES = {
    1: """1. USE FIRST. Each option has one use_kind from the use register. The three use_kinds must differ. If the requester
   stated what they will use the dossier for, all three options serve that use through different deliverables and
   their you_will_be_able_to sets must not overlap. If no use was stated, propose the three uses this corpus and
   this audience most plausibly need, and say in best_when who should pick each.""",
    2: """2. CONCRETE TO THIS MATERIAL. Every you_will_understand line and every you_will_be_able_to line names at least one
   concrete thing from the documents — an entity, a number, a dated event, a verbatim phrase in quotes, or a document
   key in square brackets. A line that would still be true of a different corpus is rejected.""",
    3: """3. VERIFIABLE. Every promise carries supported_by: the section (S), table (T) or figure (F) that keeps it. Every
   table declares its row unit ("one row per …") and expected row count; every figure declares its format. A promise
   that no section/table/figure can keep must be dropped, not softened.""",
    4: """4. HONEST SCOPE. not_for states what these documents cannot deliver: house-internal data, forecasts, actors or
   countries not in the corpus, single-source limits, sample sizes. Never promise "where the next move lands" from
   documents that only periodise the past.""",
    5: """5. AUDIENCE REGISTER. Write in the register given below. For executives: no theory vocabulary; use the plain
   equivalents supplied (e.g. "hidden obligation", not "inferential commitment"); plain_name for every engine is
   supplied — use it verbatim. For analysts and researchers the technical names are allowed.""",
    6: """6. TRADE-OFF. The three options must differ in weight: one light (1 engine, or 2 at surface, ≤2 tables, ≤1 figure),
   one standard, one full (3–4 engines, 3 tables, 2–3 figures) unless the depth preference forbids it. Cost and
   time are computed by code from your path; do not state prices.""",
    7: """7. ENGINES ARE THE HOW. Choose path.steps only from the executable catalog, in run order, 1–4 steps, no repeats.
   Each step's `contributes` says in reader terms what that step adds to THIS deliverable — never what the engine
   is in general. Engines marked NOT FOR THIS CORPUS may not be used.""",
    8: """8. LENGTHS. deliverable ≤110 chars; understand ≤140; able_to ≤120 and verb-first; questions ≤120; not_for ≤120;
   best_when ≤140; headings ≤70; table titles ≤90; row_unit ≤60. Exactly 3 understand, 2–3 able_to, 3–4 questions,
   1–3 not_for, 3–6 sections, 1–3 tables, 0–3 figures.""",
    9: """9. RECOMMEND. Name the option the material carries best and say why in one sentence the reader would accept
   (what the documents hold, what they lack). Name the runner-up and why.""",
}
RULE_7_TRANSLATE = """7. THE PATH IS FIXED: {steps}. Do not change it. Write the ONE option that this path yields for this corpus and
   audience (alternative = false), then ONE alternative the desk would propose instead (alternative = true) with its own
   path and a one-line reason in best_when. If the fixed path does not fit this corpus, say so in that option's not_for
   and recommend the alternative."""


def system_prompt(translate_steps: Optional[str] = None) -> str:
    rules = dict(RULES)
    if translate_steps:
        rules[7] = RULE_7_TRANSLATE.format(steps=translate_steps)
        rules[1] = rules[1].replace("exactly THREE", "TWO").replace("The three use_kinds must differ.", "The two options may share a use_kind.")
        head = SYSTEM_HEAD.replace("exactly THREE DELIVERABLES they could commission — three different USES of the same documents, not three topics and\nnot three phrasings of one idea.",
                                   "TWO DELIVERABLES: the one a FIXED path yields, and the desk's own alternative.")
    else:
        head = SYSTEM_HEAD
    return head + "\n" + "\n".join(rules[i] for i in sorted(rules))


def _same_author(docs: list[Document]) -> Optional[bool]:
    creators = {(d.creators or "").strip().lower() for d in docs if (d.creators or "").strip()}
    if not creators:
        return None
    return len(creators) <= 1


def build_user_prompt(job: DossierJob, docs: list[Document], catalog: dict, audience: str) -> str:
    vocab = vocabulary_lines(audience)
    vocab_block = "\n".join(f'  "{t}" → "{p}"' for t, p in vocab) if vocab else "  (technical names are allowed for this audience)"
    uf = job.options.use_frame
    use_kind = (uf.use_kind if uf and uf.use_kind else None) or "not stated"
    corpus_chars = sum(d.char_count for d in docs)
    depth = job.options.depth
    figures = job.options.output.figures if job.options.output else 2
    use_register = "\n".join(f"  {k:<12} — {v}" for k, v in USE_REGISTER.items())
    return (
        f"AUDIENCE: {audience} — {AUDIENCE_REGISTER.get(audience, '')}\n"
        f"VOCABULARY FOR THIS AUDIENCE (use the right-hand side; never the left, except inside a verbatim quote):\n{vocab_block}\n"
        f"ENGINE PLAIN NAMES FOR THIS AUDIENCE (use verbatim as path.steps[].plain_name):\n{plain_name_lines(catalog)}\n\n"
        f"USE REGISTER (use_kind → what the reader is trying to do):\n{use_register}\n\n"
        f"REQUESTER'S USE: {use_kind} — {job.options.intent or 'no intent given'}\n"
        f"  occasion: {(uf.occasion if uf and uf.occasion else '—')}   reads it: {(uf.who_reads if uf and uf.who_reads else audience)}"
        f"   decision due: {(uf.decision if uf and uf.decision else '—')}\n"
        f"DEPTH PREFERENCE: {depth} (options may sit one level lighter or heavier when the use demands it)\n"
        f"FIGURES PREFERENCE: {figures}\n"
        f"CORPUS: {len(docs)} documents, {corpus_chars:,} characters.\n\n"
        f"RECONNAISSANCE:\n{compact_profiles(job.profiles)}\n"
        "(the candidate_angles are raw material, not options)\n\n"
        f"EXECUTABLE ENGINES (choose path.steps only from these keys; 'use when' and 'yields' are for you, plain_name is for the reader):\n"
        f"{catalog_purpose_text(catalog, audience)}\n\n"
        "Propose the options and a recommendation. Return them through the tool."
    )


# ── the checks (§B5) — pure functions, testable without the network ───────

@dataclass
class CheckContext:
    audience: str
    doc_keys: set[str]
    entities: set[str]
    by_key: dict
    use_kind_given: bool
    ban: tuple[str, ...] = ()
    translate: bool = False


@dataclass
class Issue:
    option_key: str
    field: str
    message: str
    needs_model: bool = True  # True: only the model can fix it (goes into the repair prompt); False: code fixes it


@dataclass
class CheckReport:
    issues: list[Issue] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def model_issues(self) -> list[Issue]:
        return [i for i in self.issues if i.needs_model]

    def lines(self) -> list[str]:
        return [f"option {i.option_key} · {i.field}: {i.message}" for i in self.issues]


_STOP = set("""a an and are as at be but by for from has have if in into is it its of on or over than that the their
then there these this those to under upon was were what when where which while who whom will with you your
our we they them us his her he she not no yes all any each every both more most other some such only own same so
too very can could may might must shall should would about above after again against before below between
during through until within without across per one two three four five six seven eight nine ten""".split())


def _content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z'-]{3,}", (text or "").lower()) if w not in _STOP}


def overlap(a: str, b: str) -> float:
    """Share of content words two texts have in common, relative to the shorter one (0..1)."""
    wa, wb = _content_words(a), _content_words(b)
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / max(1, min(len(wa), len(wb)))


def is_concrete(text: str, doc_keys: set[str], entities: set[str]) -> bool:
    """A doc key in brackets, a known entity, a number/date, or a quoted verbatim phrase."""
    if not text:
        return False
    if any(f"[{k}]" in text for k in doc_keys):
        return True
    if re.search(r"\d", text):
        return True
    if re.search(r"[“\"][^”\"]{4,}[”\"]", text):
        return True
    # a single-quoted verbatim phrase ('national security'); apostrophes (the CEO's) do not open a quote
    if re.search(r"(?:^|[\s(\[—–-])'[^']{4,}'(?=$|[\s.,;:)\]—–-])", text):
        return True
    low = text.lower()
    return any(e in low for e in entities if len(e) >= 4)


def _resolves(ref: ShapeRef, shape: Shape) -> bool:
    n = {"section": len(shape.sections), "table": len(shape.tables), "figure": len(shape.figures)}[ref.kind]
    return 1 <= ref.index <= n


def check_brief(brief: Brief, ctx: CheckContext) -> CheckReport:
    rep = CheckReport()
    opts = brief.options
    # use disjointness
    kinds = [o.use_kind for o in opts]
    if not ctx.translate and len(set(kinds)) < len(kinds):
        dup = [k for k in set(kinds) if kinds.count(k) > 1]
        rep.issues.append(Issue("*", "use_kind", f"options share a use_kind ({', '.join(dup)}); each option must serve a different use from the register"))
    for o in opts:
        if o.use_kind not in USE_KINDS:
            rep.issues.append(Issue(o.key, "use_kind", f"'{o.use_kind}' is not in the use register"))
        if o.deliverable_kind not in DELIVERABLE_KINDS:
            rep.issues.append(Issue(o.key, "deliverable_kind", f"'{o.deliverable_kind}' is not a deliverable kind"))
    if ctx.use_kind_given and not ctx.translate:
        for i in range(len(opts)):
            for j in range(i + 1, len(opts)):
                a = " ".join(p.text for p in opts[i].you_will_be_able_to)
                b = " ".join(p.text for p in opts[j].you_will_be_able_to)
                if overlap(a, b) >= 0.5:
                    rep.issues.append(Issue(opts[j].key, "you_will_be_able_to",
                                            f"options {opts[i].key} and {opts[j].key} let the reader do the same things; give {opts[j].key} a different deliverable whose 'able to' set does not overlap"))
    for o in opts:
        # shape present
        if o.shape is None:
            rep.issues.append(Issue(o.key, "shape", "shape is missing (sections, tables with row_unit, figures with format)"))
            continue
        # concreteness
        for label, plist in (("you_will_understand", o.you_will_understand), ("you_will_be_able_to", o.you_will_be_able_to)):
            for p in plist:
                if not is_concrete(p.text, ctx.doc_keys, ctx.entities):
                    rep.issues.append(Issue(o.key, label, f"not concrete to this material (name an entity, a number, a date, a quoted phrase or a [DOC_KEY]): “{p.text[:90]}”"))
                # support refs
                if not p.supported_by:
                    rep.issues.append(Issue(o.key, label, f"no supported_by on “{p.text[:60]}” — point at the section/table/figure that keeps it"))
                for r in p.supported_by:
                    if not _resolves(r, o.shape):
                        rep.issues.append(Issue(o.key, label, f"reference {r.label()} does not exist in this option's shape ({len(o.shape.sections)} sections, {len(o.shape.tables)} tables, {len(o.shape.figures)} figures)"))
        # row unit / figure format
        for n, t in enumerate(o.shape.tables, start=1):
            if not t.row_unit.strip().lower().startswith("one row per"):
                rep.issues.append(Issue(o.key, f"shape.tables[{n}]", f"row_unit must start with 'one row per' (got “{t.row_unit[:50]}”)"))
        for n, f in enumerate(o.shape.figures, start=1):
            if f.format not in FIGURE_FORMATS:
                rep.issues.append(Issue(o.key, f"shape.figures[{n}]", f"format '{f.format}' is not one of {FIGURE_FORMATS}", needs_model=False))
        # counts
        counts = ((len(o.you_will_understand), 3, 3, "you_will_understand"), (len(o.you_will_be_able_to), 2, 3, "you_will_be_able_to"),
                  (len(o.questions_answered), 3, 4, "questions_answered"), (len(o.not_for), 1, 3, "not_for"),
                  (len(o.shape.sections), 3, 6, "shape.sections"), (len(o.shape.tables), 1, 3, "shape.tables"), (len(o.shape.figures), 0, 3, "shape.figures"))
        for n, lo, hi, name in counts:
            if not lo <= n <= hi:
                rep.issues.append(Issue(o.key, name, f"{n} given; {lo}–{hi} required", needs_model=n < lo))
        # vocabulary (executive)
        if ctx.ban:
            fields = [("title", o.title), ("deliverable", o.deliverable), ("best_when", o.best_when)]
            fields += [("you_will_understand", p.text) for p in o.you_will_understand]
            fields += [("you_will_be_able_to", p.text) for p in o.you_will_be_able_to]
            fields += [("questions_answered", q) for q in o.questions_answered] + [("not_for", x) for x in o.not_for]
            fields += [("shape.sections", s.heading) for s in o.shape.sections] + [("shape.tables", t.title) for t in o.shape.tables]
            fields += [("path.plain_name", s.plain_name) for s in o.path.steps] + [("path.contributes", s.contributes) for s in o.path.steps]
            hits: dict[str, set[str]] = {}
            for name, text in fields:
                for h in jargon_hits(text, ctx.ban):
                    hits.setdefault(h, set()).add(name)
            if hits:
                listed = "; ".join(f"“{h}” in {', '.join(sorted(ws))}" for h, ws in sorted(hits.items()))
                rep.issues.append(Issue(o.key, "vocabulary", f"theory vocabulary on an executive card — replace with the plain equivalents supplied: {listed}"))
        # lengths: the model is asked once to tighten them (a truncated promise is a broken promise); code cuts what remains
        over = [f"{name} ({len(text)}/{cap})" for name, text, cap in _length_fields(o) if len(text) > cap]
        if len(o.title.split()) > TITLE_MAX_WORDS:
            over.insert(0, f"title ({len(o.title.split())} words/{TITLE_MAX_WORDS})")
        if over:
            rep.issues.append(Issue(o.key, "lengths", f"{len(over)} field(s) over their caps — tighten, do not truncate: " + ", ".join(over[:12]) + (" …" if len(over) > 12 else "")))
        # engines
        if not o.path.steps:
            rep.issues.append(Issue(o.key, "path", "path.steps is empty"))
        keys = [s.engine_key for s in o.path.steps]
        unknown = [k for k in keys if k not in ctx.by_key]
        if unknown:
            rep.issues.append(Issue(o.key, "path", f"not executable: {unknown}", needs_model=True))
        if len(keys) != len(set(keys)):
            rep.issues.append(Issue(o.key, "path", "path repeats an engine", needs_model=False))
        if len(keys) > 4:
            rep.issues.append(Issue(o.key, "path", f"{len(keys)} steps; max 4", needs_model=False))
    # weight spread (log only)
    if not ctx.translate and len(opts) >= 3:
        depths = {path_depth_from_steps(validate_steps(list(o.path.steps), ctx.by_key), ctx.by_key) for o in opts}
        if len(depths) < 2:
            rep.notes.append(f"weight spread: all options sit at '{next(iter(depths))}' — no trade-off between them")
    # recommendation
    keys = {o.key for o in opts}
    if brief.recommendation is None or brief.recommendation.option_key not in keys:
        rep.issues.append(Issue("*", "recommendation", "recommendation.option_key must name one of the options", needs_model=False))
    elif not is_concrete(brief.recommendation.because, ctx.doc_keys, ctx.entities):
        rep.notes.append("recommendation.because names no document or entity")
    return rep


def _length_fields(o: BriefOption) -> list[tuple[str, str, int]]:
    out = [("deliverable", o.deliverable, CAPS["deliverable"]), ("best_when", o.best_when, CAPS["best_when"])]
    out += [("you_will_understand", p.text, CAPS["understand"]) for p in o.you_will_understand]
    out += [("you_will_be_able_to", p.text, CAPS["able_to"]) for p in o.you_will_be_able_to]
    out += [("questions_answered", q, CAPS["question"]) for q in o.questions_answered]
    out += [("not_for", x, CAPS["not_for"]) for x in o.not_for]
    if o.shape:
        out += [("shape.sections.heading", s.heading, CAPS["heading"]) for s in o.shape.sections]
        out += [("shape.sections.answers", s.answers, CAPS["answers"]) for s in o.shape.sections]
        out += [("shape.tables.title", t.title, CAPS["table_title"]) for t in o.shape.tables]
        out += [("shape.tables.row_unit", t.row_unit, CAPS["row_unit"]) for t in o.shape.tables]
        out += [("shape.figures.scene", f.scene, CAPS["scene"]) for f in o.shape.figures]
    out += [("path.contributes", s.contributes, CAPS["contributes"]) for s in o.path.steps]
    return out


def truncate(text: str, cap: int) -> str:
    text = (text or "").strip()
    if len(text) <= cap:
        return text
    cut = text[:cap].rsplit(" ", 1)[0]
    return (cut if len(cut) >= cap // 2 else text[:cap]).rstrip(" ,;:—-") + "…"


def apply_code_fixes(brief: Brief, ctx: CheckContext, corpus_chars: int) -> list[str]:
    """What code can settle after the (single) repair round: caps, refs, engines, names, units, the recommendation."""
    notes: list[str] = []
    seen_keys: set[str] = set()
    for i, o in enumerate(brief.options, start=1):
        key = re.sub(r"[^a-z0-9_]+", "_", (o.key or f"option_{i}").strip().lower()).strip("_")[:40] or f"option_{i}"
        while key in seen_keys:
            key = f"{key}_{i}"
        o.key = key
        seen_keys.add(key)
        if o.shape is None:
            o.shape = Shape()
            notes.append(f"{o.key}: shape was missing; empty shape recorded")
        # lengths
        if len(o.title.split()) > TITLE_MAX_WORDS:
            o.title = " ".join(o.title.split()[:TITLE_MAX_WORDS])
            o.notes.append("title cut to 10 words")
        o.deliverable = truncate(o.deliverable, CAPS["deliverable"])
        o.best_when = truncate(o.best_when, CAPS["best_when"])
        o.questions_answered = [truncate(q, CAPS["question"]) for q in o.questions_answered[:4]]
        o.not_for = [truncate(x, CAPS["not_for"]) for x in o.not_for[:3]]
        for p in o.you_will_understand:
            p.text = truncate(p.text, CAPS["understand"])
        for p in o.you_will_be_able_to:
            p.text = truncate(p.text, CAPS["able_to"])
        for s in o.shape.sections:
            s.heading, s.answers = truncate(s.heading, CAPS["heading"]), truncate(s.answers, CAPS["answers"])
        for t in o.shape.tables:
            t.title = truncate(t.title, CAPS["table_title"])
            t.columns = [truncate(c, CAPS["column"]) for c in t.columns[:5]]
            if not t.row_unit.strip().lower().startswith("one row per"):
                unit = re.sub(r"^(one\s+)?(row\s+)?(per\s+)?", "", t.row_unit.strip(), flags=re.IGNORECASE)
                t.row_unit = f"one row per {unit}" if unit else "one row per item"
                o.notes.append(f"table “{t.title[:40]}”: row unit normalised to “{t.row_unit}”")
            t.row_unit = truncate(t.row_unit, CAPS["row_unit"])
            t.carried_by = [k for k in t.carried_by if k in ctx.doc_keys] or t.carried_by
        for f in o.shape.figures:
            f.title = truncate(f.title, CAPS["figure_title"])
            f.scene = truncate(f.scene, CAPS["scene"])
            if f.format not in FIGURE_FORMATS:
                o.notes.append(f"figure “{f.title[:40]}”: format '{f.format}' → scene")
                f.format = "scene"
        o.shape.sections, o.shape.tables, o.shape.figures = o.shape.sections[:6], o.shape.tables[:3], o.shape.figures[:3]
        # promises: refs + concreteness
        for label, plist, lo in (("understand", o.you_will_understand, 1), ("able to", o.you_will_be_able_to, 1)):
            kept = []
            for p in plist:
                good = [r for r in p.supported_by if _resolves(r, o.shape)]
                if len(good) < len(p.supported_by):
                    o.notes.append(f"{label} “{p.text[:40]}”: {len(p.supported_by) - len(good)} unresolvable reference(s) stripped")
                p.supported_by = good
                p.unsupported = not good
                if not is_concrete(p.text, ctx.doc_keys, ctx.entities) and len(plist) - (len(plist) - len(kept) - 1) > lo and len(kept) + (len(plist) - plist.index(p) - 1) >= lo:
                    o.notes.append(f"{label} line dropped as not concrete to this material: “{p.text[:60]}”")
                    continue
                kept.append(p)
            plist[:] = kept[: (3 if label == "understand" else 3)]
        # vocabulary: after the repair round only the record remains
        if ctx.ban:
            texts = [o.title, o.deliverable, o.best_when] + [p.text for p in o.you_will_understand + o.you_will_be_able_to] \
                    + o.questions_answered + o.not_for + [s.heading for s in o.shape.sections] + [t.title for t in o.shape.tables]
            left = sorted({h for t in texts for h in jargon_hits(t, ctx.ban)})
            if left:
                o.notes.append("theory vocabulary still on the card after repair: " + ", ".join(left))
        # engines
        steps = validate_steps(list(o.path.steps), ctx.by_key)
        if len(steps) < len(o.path.steps):
            o.notes.append(f"path: {len(o.path.steps) - len(steps)} unknown/duplicate step(s) dropped")
        if not steps:
            steps = [PathStep(engine_key="deep_summarization", contributes="reads every document closely (fallback: no executable engine was named)")]
            o.notes.append("path: no executable engine named; reading guide substituted")
        for s in steps:
            s.plain_name = plain_name_for(s.engine_key, ctx.audience, ctx.by_key)
            s.contributes = truncate(s.contributes, CAPS["contributes"])
        o.path.steps = steps
        o.path.depth = path_depth_from_steps(steps, ctx.by_key)
        o.evidence_base.thin_or_missing = [truncate(x, CAPS["thin"]) for x in o.evidence_base.thin_or_missing[:4]]
        for cd in o.evidence_base.carrying_docs:
            cd.carries = truncate(cd.carries, CAPS["carries"])
        # estimates from the option's own path
        o.est_cost_usd, o.est_minutes, o.est_llm_calls = estimate_path(o.path, corpus_chars, ctx.by_key)
        o.model_validate(o.model_dump())  # re-derive telling/engines/output_shape
        derived = BriefOption.model_validate(o.model_dump())
        o.telling, o.engines, o.output_shape, o.version = derived.telling, derived.engines, derived.output_shape, derived.version
    # recommendation
    keys = [o.key for o in brief.options]
    rec = brief.recommendation
    if rec is None or rec.option_key not in keys:
        # the model may have used the pre-normalised key
        fallback = None
        if rec is not None:
            norm = re.sub(r"[^a-z0-9_]+", "_", rec.option_key.strip().lower()).strip("_")[:40]
            fallback = norm if norm in keys else None
        brief.recommendation = Recommendation(option_key=fallback or keys[0], because=(rec.because if rec else ""),
                                              runner_up=(rec.runner_up if rec else None), runner_up_because=(rec.runner_up_because if rec else None))
        if not fallback:
            notes.append("recommendation missing or unknown; option 1 recorded as the recommendation")
    brief.recommendation.because = truncate(brief.recommendation.because, CAPS["because"])
    if brief.recommendation.runner_up and brief.recommendation.runner_up not in keys:
        brief.recommendation.runner_up = None
    return notes


# ── the step ──────────────────────────────────────────────────────────────

def _fallback_option(n: int, corpus_chars: int, ctx: CheckContext) -> BriefOption:
    o = BriefOption(
        key=f"option_{n}", title="Straight reading guide", deliverable_kind="reading_guide", use_kind="learn",
        deliverable="A plain reading guide: what each document argues and where they disagree.",
        you_will_understand=[Promise(text="what each document argues, in its own words", supported_by=[ShapeRef(kind="table", index=1)])],
        you_will_be_able_to=[Promise(text="brief a colleague on the corpus", supported_by=[ShapeRef(kind="section", index=1)])],
        questions_answered=["What does each document argue?", "Where do they disagree?", "Which terms recur?"],
        not_for=["no recommendation; no ranking of risks"],
        shape=Shape(sections=[{"heading": "What each document argues", "answers": "What does each document argue?"},
                              {"heading": "Where they disagree", "answers": "Where do they disagree?"},
                              {"heading": "The terms you will hear", "answers": "Which terms recur?"}],
                    tables=[TableSpec(title="The documents, one line each", row_unit="one row per document", columns=["Document", "Argues", "Evidence"], rows_expected="")]),
        path=Path(steps=[PathStep(engine_key="deep_summarization", contributes="reads every document closely", depth="surface")], depth="simple"),
        best_when="Pick this when the desk could not propose anything better (fallback).",
        notes=["fallback option: the model returned fewer options than the contract requires"],
    )
    return o


def run_brief(job: DossierJob, docs: list[Document]) -> Brief:
    audience = job.options.audience or "executive"
    entry = job.options.entry or ("material" if job.options.autopilot else "use")
    corpus_chars = sum(d.char_count for d in docs)
    by_key = {e["engine_key"]: e for e in engine_catalog()}
    catalog = purpose_catalog(audience=audience, corpus_chars=corpus_chars, n_docs=len(docs), same_author=_same_author(docs))
    doc_keys = {d.key for d in docs} | {p.doc_key for p in (job.profiles.profiles if job.profiles else [])}
    entities = {e.strip().lower() for p in (job.profiles.profiles if job.profiles else []) for e in p.entities if e and len(e.strip()) >= 4}
    ctx = CheckContext(audience=audience, doc_keys=doc_keys, entities=entities, by_key=by_key,
                       use_kind_given=bool(job.options.use_frame and job.options.use_frame.use_kind),
                       ban=ban_terms(audience), translate=(entry == "chosen"))

    fixed: Optional[Path] = None
    translate_steps = None
    if entry == "chosen":
        if not job.options.path:
            raise ValueError("entry = 'chosen' but no path was given")
        fixed = resolve_path_request(job.options.path, audience, by_key)
        translate_steps = " → ".join(f"{s.engine_key}@{s.depth} (\"{s.plain_name}\")" for s in fixed.steps)
    system = system_prompt(translate_steps)
    user = build_user_prompt(job, docs, catalog, audience)
    schema = brief_schema(translate=fixed is not None)
    label = "brief: the fixed path + the desk's alternative" if fixed else "brief: three deliverables"

    brief, meta = call_json(job.id, STEP, label=label, system=system, user=user,
                            tool_name="propose_brief", schema=schema, model_cls=Brief, max_tokens=14000)
    brief.entry = entry
    report = check_brief(brief, ctx)
    repaired = False
    if report.model_issues:
        events.emit(job.id, "note", phase=STEP, detail=f"brief: {len(report.model_issues)} rule violation(s); one repair round — " + " | ".join(report.lines()[:6]),
                    payload_json={"kind": "brief_repair", "issues": report.lines()})
        repair_user = (
            user + "\n\n---\nYOUR PREVIOUS ANSWER (below) VIOLATED THESE RULES. Return the COMPLETE corrected brief through the tool, "
            "keeping everything that was right:\n" + "\n".join(f"- {line}" for line in [f"option {i.option_key} · {i.field}: {i.message}" for i in report.model_issues])
            + "\n\nPREVIOUS ANSWER:\n" + json.dumps(brief.model_dump(exclude={"options": {"__all__": {"telling", "engines", "output_shape", "est_cost_usd", "est_minutes", "est_llm_calls", "version", "notes"}}}),
                                                       ensure_ascii=False)[:60000]
        )
        try:
            brief2, _ = call_json(job.id, STEP, label=label + " (rule repair)", system=system, user=repair_user,
                                  tool_name="propose_brief", schema=schema, model_cls=Brief, max_tokens=14000)
            brief2.entry = entry
            report2 = check_brief(brief2, ctx)
            if len(report2.model_issues) <= len(report.model_issues):
                brief, report, repaired = brief2, report2, True
            else:
                report.notes.append("repair round returned more violations than the first answer; first answer kept")
        except Exception as exc:  # the repair never blocks the brief
            logger.warning(f"brief repair failed: {exc}")
            report.notes.append(f"repair round failed: {exc}")

    # the contract: three options (two in translate mode)
    want = 2 if fixed else 3
    brief.options = brief.options[:want]
    while len(brief.options) < want:
        brief.options.append(_fallback_option(len(brief.options) + 1, corpus_chars, ctx))
    if fixed:
        # the fixed path is the requester's; the first option carries it whatever the model wrote
        brief.options[0].alternative = False
        brief.options[0].path = Path(steps=[PathStep(engine_key=s.engine_key, depth=s.depth, plain_name=s.plain_name,
                                                     contributes=next((m.contributes for m in brief.options[0].path.steps if m.engine_key == s.engine_key), ""))
                                            for s in fixed.steps], depth=fixed.depth, chain_key=fixed.chain_key)
        if len(brief.options) > 1:
            brief.options[1].alternative = True
    notes = apply_code_fixes(brief, ctx, corpus_chars)
    brief.notes = report.notes + notes + ([f"unresolved after repair: {line}" for line in report.lines() if line] if report.model_issues else [])
    brief.version = 2
    defaults = brief.defaults or BriefDefaults()
    defaults.audience = job.options.audience or defaults.audience
    defaults.depth = job.options.depth or defaults.depth
    defaults.figures = job.options.output.figures if job.options.output else defaults.figures
    brief.defaults = defaults

    rec = brief.recommendation
    events.emit(job.id, "artifact", phase=STEP,
                detail="brief: " + " / ".join(f"{o.title} [{o.use_kind}, ${o.est_cost_usd:.2f}]" for o in brief.options)
                + (f" — recommended: {rec.option_key}" if rec else ""),
                payload_json={"kind": "brief", "entry": entry, "repaired": repaired,
                              "options": [{"key": o.key, "title": o.title, "use_kind": o.use_kind, "deliverable_kind": o.deliverable_kind,
                                           "deliverable": o.deliverable, "able_to": [p.text for p in o.you_will_be_able_to],
                                           "not_for": o.not_for, "path": [s.engine_key for s in o.path.steps], "depth": o.path.depth,
                                           "est_cost_usd": o.est_cost_usd, "est_minutes": o.est_minutes, "notes": o.notes} for o in brief.options],
                              "recommendation": rec.model_dump() if rec else None, "notes": brief.notes})
    return brief
