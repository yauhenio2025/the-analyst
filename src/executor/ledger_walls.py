"""Ledger walls (study 2026-09-04): parse findings-ledger rows, verify anchors verbatim, check ids.

Shape only, never merit. A row is `- [ID] finding — field: value — anchor: "quote" — … — confidence: x`.
The wall verifies that each anchor appears verbatim in the source after the same normalisation the
dossier's anchor wall uses (`src.dossier.walls.normalize`), trimming from the end word by word to a
floor; that ids are unique; and that every id a text cites exists in the ledger it should exist in.
"""
from __future__ import annotations

import json
import re
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Iterable, Optional

from src.dossier.walls import MAX_QUOTE_CHARS, MIN_TRIMMED_CHARS, MIN_TRIMMED_WORDS, normalize
from src.executor.context_broker import split_ledger

# a row: "- [ID] …" with the id optionally bolded ("- **[ID]**", "- [**ID**]") or the bullet numbered ("1. [ID]")
# … and the bullet itself is optional: DeepSeek writes bare "[F22] …" lines (frontier run, 23:14)
_ROW_RE = re.compile(r"^\s*(?:(?:[-*]|\d+[.)])\s*)?(?:\*\*)?\[\s*(?:\*\*)?([A-Za-z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)*)(?:\*\*)?\s*\](?:\*\*)?\s*(.*)$")
# the anchor is the text between paired quotes after `anchor:` (straight, curly or single), whatever follows
# the closing quote (a page reference, a separator, nothing): DeepSeek writes `anchor: “…” (p. 110) — depends: …`
_ANCHOR_RE = re.compile(r"(?<![\w-])anchor\s*:\s*(?:\"([^\"\n]*)\"|“([^”\n]*)”|'([^'\n]*)'|‘([^’\n]*)’)", re.IGNORECASE)
_QUOTED_SPAN_RE = re.compile(r"(?:\"([^\"\n]{12,})\"|“([^”\n]{12,})”)")
_FIELD_RE = re.compile(r"(?:^|\s[—–]\s|\s-\s)\s*([a-z][a-z_ \-‐‑]{1,24}?)\s*:\s*", re.IGNORECASE)
_CITED_RE = re.compile(r"\[([A-Za-z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)*)\]")
_CONF_RE = re.compile(r"confidence\s*:\s*(high|medium|low)", re.IGNORECASE)
_STATUS_RE = re.compile(r"status\s*:\s*(confirmed|weakened|rejected|added)", re.IGNORECASE)
_DIM_RE = re.compile(r"\bdim\s*:\s*([a-z0-9_]+)", re.IGNORECASE)
_DOC_RE = re.compile(r"(?<![\w-])doc\s*:\s*\[?([A-Za-z0-9_\-.:]+)", re.IGNORECASE)
_DOC_VALUE_RE = re.compile(r"(?:\[([A-Za-z0-9_\-.:]+)\]|([A-Za-z0-9_\-.:]+))")
_EXTRA_ANCHOR_RE = re.compile(r"(?<![\w-])anchor-([a-z0-9]+)\s*:\s*(?:\"([^\"\n]*)\"|“([^”\n]*)”|'([^'\n]*)'|‘([^’\n]*)’)", re.IGNORECASE)
_EXTRA_DOC_RE = re.compile(r"(?<![\w-])doc-([a-z0-9]+)\s*:\s*\[?([A-Za-z0-9_\-.:]+)", re.IGNORECASE)
_FROM_RE = re.compile(r"\bfrom\s*:\s*([^—\n]+)", re.IGNORECASE)
_ANCHOR_TRAILER_RE = re.compile(r"(?:\s|[.,;:!?…]|\([^()\r\n]*\)|\[[^\[\]\r\n]*\]|(?:pp?\.?|pages?)\s*\d+(?:\s*[-–—,:]\s*\d+)*)*", re.I)
_AUX_SECTION_RE = re.compile(r"^\s{0,3}#{2,4}\s*(?:must[ -]keep|counter[- ]evidence|open questions|rejected by the critic|check receipt)\b", re.I)
_LEDGER_SECTION_RE = re.compile(r"^\s{0,3}#{2,4}\s*(?:(?:verified|final)\s+)?findings?\s+ledger\b", re.I)

def _fields(text: str) -> list[re.Match]:
    """Existing separator-delimited fields, excluding quoted prose and metadata values.

    Escaped JSON quotes and nested curly quotations stay opaque. Apostrophes in
    words do not open strings. This is tokenization of the ledger's existing row
    shape, not an interpretation of field contents.
    """
    quoted = [False] * len(text)
    stack: list[str] = []
    escaped = False
    for pos, ch in enumerate(text):
        quoted[pos] = bool(stack)
        if escaped:
            escaped = False
            continue
        if stack and ch == "\\":
            escaped = True
            continue
        if stack:
            if ch == stack[-1]:
                stack.pop()
            elif ch == "“" and stack[-1] == "”":
                stack.append("”")
            elif ch == "‘" and stack[-1] == "’":
                stack.append("’")
        elif ch in ('"', "“", "‘") or (ch == "'" and (pos == 0 or not text[pos - 1].isalnum())):
            stack.append({"“": "”", "‘": "’"}.get(ch, ch))
    structural = {"anchor", "counter-anchor", "counter-doc", "dim", "doc", "status", "confidence", "from",
                  "revised-finding", "finding rewritten to", "original-finding"}
    return [m for m in _FIELD_RE.finditer(text) if not quoted[m.start(1)]
            and (m.start() > 0 or m.group(1).strip().lower() in structural
                 or m.group(1).strip().lower().startswith(("anchor-", "doc-", "trimmed-anchor")))]


def _field_values(text: str) -> list[tuple[str, str, re.Match]]:
    fields = _fields(text)
    return [(m.group(1).strip().lower().replace("‐", "-").replace("‑", "-"), text[m.end():fields[i + 1].start() if i + 1 < len(fields) else len(text)].strip(), m)
            for i, m in enumerate(fields)]


def _revised_finding(text: str) -> str:
    """Read an explicit quoted replacement; never infer one from a critic's reason."""
    matches = [(name, value) for name, value, _ in _field_values(text)
               if name in ("revised-finding", "finding rewritten to")]
    if not matches:
        return ""
    if len(matches) != 1:
        raise ValueError("A critic row has multiple revised-finding fields")
    value = matches[0][1]
    if value.startswith("“") and value.endswith("”"):
        revised, end = value[1:-1], len(value)
    else:
        try:
            revised, end = json.JSONDecoder().raw_decode(value)
        except (ValueError, TypeError) as exc:
            raise ValueError("revised-finding must be a quoted string") from exc
    if value[end:].strip():
        raise ValueError("Unexpected text after revised-finding")
    if not isinstance(revised, str) or not revised.strip() or "\n" in revised or "\r" in revised:
        raise ValueError("revised-finding must be a nonempty, single-line quoted string")
    return revised.strip()


def _replace_finding_head(text: str, finding: str) -> str:
    """Protect field-like replacement prose while preserving the metadata tail."""
    fields = _fields(text)
    tail = text[fields[0].start():] if fields else ""
    return json.dumps(finding, ensure_ascii=False) + tail


def _anchor_literal(value: str) -> tuple[str, int, str]:
    """Decode one quoted anchor, keeping parse ambiguity separate from quote matching.

    ASCII double quotes accept JSON escapes. Existing curly/single-quoted literals
    remain supported. A further same-delimiter quote after the closing literal is
    ambiguous, so it cannot turn the initial prefix into verified evidence.
    """
    quote, end = "", 0
    if value.startswith('"'):
        try:
            quote, end = json.JSONDecoder().raw_decode(value)
        except ValueError:
            pass  # Preserve legacy literal backslashes unless inner quotes are ambiguous.
    if not end:
        match = _ANCHOR_RE.match("anchor: " + value)
        if not match:
            return "", 0, ""
        quote = next(g for g in match.groups() if g is not None)
        end = match.end() - len("anchor: ")
    closing = {"“": "”", "‘": "’"}.get(value[0], value[0])
    if closing in value[end:]:
        return "", end, "ambiguous inner quotation marks; use JSON-escaped double quotes"
    if not _ANCHOR_TRAILER_RE.fullmatch(value[end:]):
        # A malformed inner quote can expose a field separator before the final
        # delimiter. Its remaining bare prose still cannot certify a prefix.
        return "", end, "unexpected text after quoted anchor; use one JSON string followed only by a citation or punctuation"
    return quote.strip(), end, ""


@dataclass
class LedgerAnchor:
    quote: str
    doc: str = ""
    suffix: str = ""
    verified: bool = False
    trimmed: bool = False
    verified_doc: str = ""
    parse_error: str = ""


@dataclass
class LedgerRow:
    id: str
    text: str                       # the full row text after the id
    finding: str = ""
    anchor: str = ""
    dim: str = ""
    doc: str = ""
    confidence: str = ""
    status: str = ""
    lineage: list[str] = field(default_factory=list)
    anchor_verified: bool = False
    anchor_trimmed: bool = False
    anchor_doc: str = ""
    raw: str = ""
    extra_anchors: list[LedgerAnchor] = field(default_factory=list)
    revised_finding: str = ""
    anchor_parse_error: str = ""

    @property
    def anchors(self) -> list[LedgerAnchor]:
        return [LedgerAnchor(self.anchor, self.doc, verified=bool(self.anchor_doc),
                             trimmed=self.anchor_trimmed, verified_doc=self.anchor_doc,
                             parse_error=self.anchor_parse_error), *self.extra_anchors]

    def copy_anchors_from(self, other: LedgerRow) -> None:
        for attr in ("anchor", "doc", "anchor_verified", "anchor_trimmed", "anchor_doc", "extra_anchors", "anchor_parse_error"):
            setattr(self, attr, deepcopy(getattr(other, attr)))

    def has_field(self, name: str) -> bool:
        return any(key == name for key, _, _ in _field_values(self.text))

    def replace_finding(self, finding: str) -> None:
        """Quote a replacement head so its field-like prose remains prose on reparse."""
        self.finding = finding
        self.text = _replace_finding_head(self.text, finding)

    def render(self) -> str:
        text = self.text
        if self.status == "weakened" and self.revised_finding:
            # Deep verification keeps parsed critic rows directly, without apply_rulings.
            # Render the same explicit replacement as .finding; keep the raw receipt intact.
            text = _replace_finding_head(text, self.revised_finding)
        edits = []
        original_length = len(text)
        values = _field_values(text)
        names = {name for name, _, _ in values}
        # Only actual anchor fields may be updated: finding/revision/provenance
        # strings can legitimately contain words such as `anchor:` or `status:`.
        for anchor in self.anchors:
            suffix = f"-{anchor.suffix}" if anchor.suffix else ""
            anchor_names = {f"anchor{suffix}"} | ({"counter-anchor"} if suffix == "-counter" else set())
            for name, value, field_match in values:
                if name not in anchor_names:
                    continue
                _, end, error = _anchor_literal(value)
                if end and not error and not anchor.parse_error:
                    closing = {"“": "”", "‘": "’"}.get(value[0], value[0])
                    literal = json.dumps(anchor.quote, ensure_ascii=False) if value[0] == '"' else value[0] + anchor.quote + closing
                    edits.append((field_match.end(), field_match.end() + end, literal))
            error_name = f"quote-error{suffix}"
            # Keep an ambiguous displayed literal intact and provide a repairable shape diagnostic.
            # Clear a copied diagnostic once a re-anchor supplies a valid literal.
            for i, (name, _, field_match) in enumerate(values):
                if name == error_name:
                    end = values[i + 1][2].start() if i + 1 < len(values) else original_length
                    edits.append((field_match.start(), end, ""))
            if anchor.parse_error:
                diagnostic = f" — {error_name}: {anchor.parse_error}"
                # An ill-formed legacy single-quote value may make the terminal
                # diagnostic opaque to the tokenizer; do not append it repeatedly.
                if error_name in names or not text[:original_length].endswith(diagnostic):
                    text += diagnostic
            doc_names = {f"doc{suffix}"} | ({"counter-doc"} if suffix == "-counter" else set())
            if anchor.doc and not names & doc_names:
                text += f" — doc{suffix}: {anchor.doc}"
            if anchor.trimmed and f"trimmed-anchor{suffix}" not in names:
                text += f" — trimmed-anchor{suffix}: yes"
        if self.dim and "dim" not in names:
            text += f" — dim: {self.dim}"
        for start, end, replacement in sorted(edits, reverse=True):
            text = text[:start] + replacement + text[end:]
        return f"- [{self.id}] {text}".rstrip()


def parse_rows(ledger_text: str) -> list[LedgerRow]:
    """Finding rows in order; requested auxiliary sections contain references, not rulings."""
    rows: list[LedgerRow] = []
    auxiliary = False
    for line in (ledger_text or "").splitlines():
        if _LEDGER_SECTION_RE.match(line):
            auxiliary = False
            continue
        if _AUX_SECTION_RE.match(line):
            auxiliary = True
            continue
        if auxiliary:
            continue
        m = _ROW_RE.match(line)
        if not m:
            continue
        rid, rest = m.group(1), m.group(2).strip()
        row = LedgerRow(id=rid, text=rest, raw=line)
        values = _field_values(rest)
        fields = {name: value for name, value, _ in values}
        anchor_names = ["anchor-counter" if name == "counter-anchor" else name for name, _, _ in values
                        if name == "anchor" or name == "counter-anchor" or (name.startswith("anchor-") and name != "anchor-verified")]
        if len(anchor_names) != len(set(anchor_names)):
            raise ValueError(f"Ledger row {rid} has repeated anchor fields; use distinct anchor/doc suffixes")
        head = rest[:values[0][2].start()].strip() if values else rest
        row.finding = head
        row.revised_finding = _revised_finding(rest)
        cm = _CONF_RE.match("confidence: " + fields.get("confidence", "")); row.confidence = cm.group(1).lower() if cm else ""
        sm = _STATUS_RE.match("status: " + fields.get("status", "")); row.status = sm.group(1).lower() if sm else ""
        dm = _DIM_RE.match("dim: " + fields.get("dim", "")); row.dim = dm.group(1) if dm else ""
        doc_fields: dict[str, list[str]] = {}
        for name, value, _ in values:
            if name == "doc" or name.startswith("doc-") or name == "counter-doc":
                suffix = "counter" if name == "counter-doc" else name[4:] if name.startswith("doc-") else ""
                doc_fields.setdefault(suffix, []).append(value)
        doc_slots = {}
        for suffix, declarations in doc_fields.items():
            if len(declarations) != 1:
                doc_slots[suffix] = ("", "ambiguous document declarations; use one doc field per anchor")
                continue
            # Existing rows also carry unlabeled separator slots such as `— drawn`.
            # They are separate metadata; the doc segment itself must be a full key.
            segment = re.split(r"\s[—–]\s|\s-\s", declarations[0], maxsplit=1)[0].strip()
            match = _DOC_VALUE_RE.fullmatch(segment)
            doc_slots[suffix] = ((next(g for g in match.groups() if g is not None), "") if match else
                                 ("", "invalid document declaration; use one key or [key] without extra text"))
        row.doc, row.anchor_parse_error = doc_slots.pop("", ("", ""))
        if row.status == "weakened" and row.revised_finding:
            row.finding = row.revised_finding
        for name, value, _ in values:
            if name == "anchor":
                suffix = ""
            elif name == "counter-anchor":
                suffix = "counter"
            elif name.startswith("anchor-") and name != "anchor-verified":
                suffix = name[7:]
            else:
                continue
            quote, _, error = _anchor_literal(value)
            if not suffix:
                row.anchor = quote
                row.anchor_parse_error = "; ".join(e for e in (error, row.anchor_parse_error) if e)
            else:
                doc, doc_error = doc_slots.pop(suffix, ("", ""))
                row.extra_anchors.append(LedgerAnchor(quote, doc, suffix, parse_error="; ".join(e for e in (error, doc_error) if e)))
        if not row.anchor and "anchor" not in fields:
            # Preserve legacy quote slots such as promised-at/nearest-delivery.
            # Explicit rewritten/provenance strings cannot introduce evidence.
            legacy = ("" if row.revised_finding else head) + " ".join(value for name, value, _ in values
                                     if name not in ("revised-finding", "finding rewritten to", "original-finding"))
            match = _QUOTED_SPAN_RE.search(legacy)
            if match:
                candidate = next((g for g in match.groups() if g is not None), "").strip()
                if len(candidate.split()) >= 4:
                    row.anchor = candidate
        row.extra_anchors.extend(LedgerAnchor("", doc, suffix, parse_error=error) for suffix, (doc, error) in doc_slots.items())
        row.anchor_trimmed = fields.get("trimmed-anchor", "").lower() == "yes"
        for anchor in row.extra_anchors:
            anchor.trimmed = fields.get(f"trimmed-anchor-{anchor.suffix}", "").lower() == "yes"
        if "from" in fields:
            row.lineage = [x.strip().strip("[]") for x in re.split(r"[,;]\s*", fields["from"]) if x.strip()]
        rows.append(row)
    return rows


def ledger_rows(text: str) -> list[LedgerRow]:
    """Rows of the ledger section of a step output (prose before the heading is ignored)."""
    _, ledger = split_ledger(text)
    return parse_rows(ledger or text if not ledger else ledger)


_SPACED_HYPHEN = re.compile(r"(\w)-\s+(\w)")


class SourceIndex:
    """Normalised documents for verbatim membership tests.

    Each document is indexed twice: as extracted, and with spaced hyphens closed ("market- driven" → "market-driven"),
    because PDF text carries the former and a model naturally copies the latter (paper two, frontier run 23:26).
    A quote verifies if it appears in either; the check stays a membership test, never a similarity score.
    """

    def __init__(self, documents: dict[str, str]):
        self.norm = {k: normalize(v) for k, v in documents.items()}
        self.norm_closed = {k: normalize(_SPACED_HYPHEN.sub(r"\1-\2", v)) for k, v in documents.items()}

    def _has(self, doc_key: str, q: str) -> bool:
        return q in self.norm[doc_key] or q in self.norm_closed[doc_key]

    def find(self, quote: str, prefer: str = "") -> Optional[str]:
        q = normalize(quote)
        if not q:
            return None
        if prefer and prefer in self.norm:
            # a declared key that names one of the documents is binding (a corpus row must quote the document it names)
            return prefer if self._has(prefer, q) else None
        # a declared key that names no document (the executor's work key against the dossier's doc keys) is ignored
        for k in self.norm:
            if self._has(k, q):
                return k
        return None


def verify_quote(quote: str, index: SourceIndex, prefer: str = "") -> tuple[Optional[str], str, bool]:
    """(doc_key or None, the quote that verified (possibly trimmed), trimmed?)."""
    q = (quote or "").strip()
    if not q:
        return None, "", False
    if len(q) > MAX_QUOTE_CHARS:
        q = q[:MAX_QUOTE_CHARS]
    words = q.split()
    trimmed = False
    while True:
        cand = " ".join(words)
        doc = index.find(cand, prefer)
        if doc:
            return doc, cand, trimmed
        if len(words) <= MIN_TRIMMED_WORDS or len(cand) <= MIN_TRIMMED_CHARS:
            return None, q, trimmed
        words = words[:-1]
        trimmed = True


@dataclass
class WallReport:
    rows: int = 0
    with_anchor: int = 0
    verified: int = 0
    trimmed: int = 0
    failed_ids: list[str] = field(default_factory=list)
    duplicate_ids: list[str] = field(default_factory=list)
    missing_cited: list[str] = field(default_factory=list)
    anchors: int = 0
    verified_anchors: int = 0
    cross_document_rows: int = 0
    incomplete_cross_document_ids: list[str] = field(default_factory=list)
    invalid_anchor_ids: list[str] = field(default_factory=list)

    @property
    def anchor_rate(self) -> float:
        return round(self.verified / self.rows, 3) if self.rows else 0.0

    def as_dict(self) -> dict:
        return {
            "rows": self.rows, "with_anchor": self.with_anchor, "verified": self.verified, "trimmed": self.trimmed,
            "anchor_rate": self.anchor_rate, "failed_ids": self.failed_ids[:40],
            "duplicate_ids": self.duplicate_ids[:20], "missing_cited": self.missing_cited[:40],
            "anchors": self.anchors, "verified_anchors": self.verified_anchors,
            "cross_document_rows": self.cross_document_rows,
            "incomplete_cross_document_ids": self.incomplete_cross_document_ids[:40],
            "invalid_anchor_ids": self.invalid_anchor_ids[:40],
        }


def verify_rows(rows: Iterable[LedgerRow], index: SourceIndex, *, require_cross_document: bool = False,
                corpus_dimensions: Iterable[str] = (), corpus_ids: Iterable[str] = ()) -> WallReport:
    """Verify every declared anchor in its declared document; corpus rows need two distinct doc keys.

    Corpus scope comes from the process schema or explicit row lineage, never a judgment of the finding.
    """
    rep = WallReport()
    corpus_dimensions, corpus_ids = set(corpus_dimensions), set(corpus_ids)
    seen: set[str] = set()
    for r in rows:
        rep.rows += 1
        if r.id in seen:
            rep.duplicate_ids.append(r.id)
        seen.add(r.id)
        r.anchor_verified = False
        r.anchor_doc = ""
        anchors = r.anchors
        if any(a.parse_error for a in anchors):
            rep.invalid_anchor_ids.append(r.id)
        cross_document = (require_cross_document or r.dim in corpus_dimensions or r.id in corpus_ids
                          or bool(set(r.lineage) & corpus_ids)
                          or len({a.doc for a in anchors if a.doc}) > 1)
        complete = bool(r.anchor)
        if cross_document:
            rep.cross_document_rows += 1
            complete = complete and all(a.doc for a in anchors) and len({a.doc for a in anchors}) >= 2
            if not complete:
                rep.incomplete_cross_document_ids.append(r.id)
        if r.anchor:
            rep.with_anchor += 1
        for anchor in anchors:
            rep.anchors += 1
            # Within a document, a second quote can inherit the row's document key.
            declared = anchor.doc or r.doc
            if anchor.parse_error:
                doc, quote, trimmed = None, anchor.quote, False
            elif cross_document and declared and declared not in index.norm:
                doc, quote, trimmed = None, anchor.quote, False   # a corpus row must name a document that exists
            else:
                doc, quote, trimmed = verify_quote(anchor.quote, index, prefer=declared)
            anchor.verified, anchor.verified_doc = bool(doc), doc or ""
            anchor.trimmed = anchor.trimmed or trimmed
            if doc:
                anchor.quote = quote
                rep.verified_anchors += 1
                if not anchor.doc and not cross_document:
                    anchor.doc = r.doc or doc
        r.anchor, r.anchor_doc = anchors[0].quote, anchors[0].verified_doc
        r.doc = anchors[0].doc
        r.anchor_trimmed = anchors[0].trimmed
        if complete and all(a.verified for a in anchors):
            rep.verified += 1
            r.anchor_verified = True
            if any(a.trimmed for a in anchors):
                rep.trimmed += 1
        else:
            rep.failed_ids.append(r.id)
    return rep


def cited_ids(text: str) -> list[str]:
    """Every [ID] token in a text, in order, without duplicates."""
    out, seen = [], set()
    for m in _CITED_RE.finditer(text or ""):
        i = m.group(1)
        if i not in seen:
            seen.add(i); out.append(i)
    return out


def check_citations(prose: str, ledger_ids: set[str], also_ok: Optional[set[str]] = None) -> list[str]:
    """Ids the prose cites that exist in neither the final ledger nor the earlier ledgers."""
    ok = set(ledger_ids) | set(also_ok or ())
    return [i for i in cited_ids(prose) if i not in ok and re.match(r"^[A-Z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)*\d+$", i)]


def render_rows(rows: Iterable[LedgerRow], heading: str = "## Findings ledger") -> str:
    return "\n".join([heading] + [r.render() for r in rows])


def reanchor_request(failed: list[LedgerRow]) -> str:
    """The one re-anchor round: the rows whose anchors were not verbatim, returned to the model."""
    lines = [
        "These rows' anchors are NOT verbatim in the source (after normalising whitespace, quotes and hyphenation). "
        "Return ONLY these rows again, same ids, same finding, each with a verbatim anchor copied exactly from the "
        "source (at most 200 characters, no ellipses), or omit a row you cannot anchor. Same row format, under the "
        "heading `## Findings ledger`. Preserve every anchor/doc pair, including anchor-b/doc-b and any further "
        "pairs; cross-document rows still require quotes from at least two distinct documents. No other text.",
        "",
    ]
    lines += [r.render() for r in failed]
    return "\n".join(lines)
