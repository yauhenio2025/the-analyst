"""Ledger walls (study 2026-09-04): parse findings-ledger rows, verify anchors verbatim, check ids.

Shape only, never merit. A row is `- [ID] finding — field: value — anchor: "quote" — … — confidence: x`.
The wall verifies that each anchor appears verbatim in the source after the same normalisation the
dossier's anchor wall uses (`src.dossier.walls.normalize`), trimming from the end word by word to a
floor; that ids are unique; and that every id a text cites exists in the ledger it should exist in.
"""
from __future__ import annotations

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
_FIELD_RE = re.compile(r"(?:^|\s[—–]\s|\s-\s)\s*([a-z][a-z_ \-]{1,24}?)\s*:\s*", re.IGNORECASE)
_CITED_RE = re.compile(r"\[([A-Za-z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)*)\]")
_CONF_RE = re.compile(r"confidence\s*:\s*(high|medium|low)", re.IGNORECASE)
_STATUS_RE = re.compile(r"status\s*:\s*(confirmed|weakened|rejected|added)", re.IGNORECASE)
_DIM_RE = re.compile(r"\bdim\s*:\s*([a-z0-9_]+)", re.IGNORECASE)
_DOC_RE = re.compile(r"(?<![\w-])doc\s*:\s*\[?([A-Za-z0-9_\-.:]+)", re.IGNORECASE)
_EXTRA_ANCHOR_RE = re.compile(r"(?<![\w-])anchor-([a-z0-9]+)\s*:\s*(?:\"([^\"\n]*)\"|“([^”\n]*)”|'([^'\n]*)'|‘([^’\n]*)’)", re.IGNORECASE)
_EXTRA_DOC_RE = re.compile(r"(?<![\w-])doc-([a-z0-9]+)\s*:\s*\[?([A-Za-z0-9_\-.:]+)", re.IGNORECASE)
_FROM_RE = re.compile(r"\bfrom\s*:\s*([^—\n]+)", re.IGNORECASE)


@dataclass
class LedgerAnchor:
    quote: str
    doc: str = ""
    suffix: str = ""
    verified: bool = False
    trimmed: bool = False
    verified_doc: str = ""


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

    @property
    def anchors(self) -> list[LedgerAnchor]:
        return [LedgerAnchor(self.anchor, self.doc, verified=bool(self.anchor_doc),
                             trimmed=self.anchor_trimmed, verified_doc=self.anchor_doc), *self.extra_anchors]

    def copy_anchors_from(self, other: LedgerRow) -> None:
        for attr in ("anchor", "doc", "anchor_verified", "anchor_trimmed", "anchor_doc", "extra_anchors"):
            setattr(self, attr, deepcopy(getattr(other, attr)))

    def render(self) -> str:
        text = self.text
        # Carry verified (possibly trimmed) quotes and supplied document keys into the next hand-off.
        for anchor in self.anchors:
            suffix = f"-{anchor.suffix}" if anchor.suffix else ""
            quote_re = _EXTRA_ANCHOR_RE if suffix else _ANCHOR_RE
            def replace(match):
                if suffix and match.group(1).lower() != anchor.suffix:
                    return match.group(0)
                group = next(i for i in range(2 if suffix else 1, len(match.groups()) + 1)
                             if match.group(i) is not None)
                start, end = match.start(group) - match.start(), match.end(group) - match.start()
                return match.group(0)[:start] + anchor.quote + match.group(0)[end:]
            text = quote_re.sub(replace, text)
            if anchor.doc and not re.search(rf"(?<![\w-])doc{re.escape(suffix)}\s*:", text, re.I):
                text += f" — doc{suffix}: {anchor.doc}"
        if self.dim and not _DIM_RE.search(text):
            text += f" — dim: {self.dim}"
        return f"- [{self.id}] {text}".rstrip()


def parse_rows(ledger_text: str) -> list[LedgerRow]:
    """Every `- [ID] …` line of a ledger (all sections), in order."""
    rows: list[LedgerRow] = []
    for line in (ledger_text or "").splitlines():
        m = _ROW_RE.match(line)
        if not m:
            continue
        rid, rest = m.group(1), m.group(2).strip()
        row = LedgerRow(id=rid, text=rest, raw=line)
        am = _ANCHOR_RE.search(rest)
        row.anchor = next((g for g in am.groups() if g is not None), "").strip() if am else ""
        if not row.anchor:
            # no `anchor:` field: a model that quotes the claim in the finding itself ("C1: \"AUKUS is not simply…\"",
            # DeepSeek on the argument map, 23:56) still offers a verbatim span; the wall tests it the same way
            fm2 = _QUOTED_SPAN_RE.search(rest)
            if fm2:
                cand = next((g for g in fm2.groups() if g is not None), "").strip()
                if len(cand.split()) >= 4:
                    row.anchor = cand
        # finding = text up to the first " — field:" separator
        head = re.split(r"\s[—–]\s(?=[a-z][a-z_ \-]{1,24}\s*:)", rest, maxsplit=1)[0]
        row.finding = head.strip()
        cm = _CONF_RE.search(rest); row.confidence = cm.group(1).lower() if cm else ""
        sm = _STATUS_RE.search(rest); row.status = sm.group(1).lower() if sm else ""
        dm = _DIM_RE.search(rest); row.dim = dm.group(1) if dm else ""
        dcm = _DOC_RE.search(rest); row.doc = dcm.group(1) if dcm else ""
        extra_docs = {m.group(1).lower(): m.group(2) for m in _EXTRA_DOC_RE.finditer(rest)}
        row.extra_anchors = [LedgerAnchor(
            quote=next((g for g in m.groups()[1:] if g is not None), "").strip(),
            doc=extra_docs.pop(m.group(1).lower(), ""), suffix=m.group(1).lower(),
        ) for m in _EXTRA_ANCHOR_RE.finditer(rest)]
        # A doc-b without its quote is a broken pair, not a single-anchor row.
        row.extra_anchors.extend(LedgerAnchor("", doc, suffix) for suffix, doc in extra_docs.items())
        fm = _FROM_RE.search(rest)
        if fm:
            row.lineage = [x.strip().strip("[]") for x in re.split(r"[,;]\s*", fm.group(1)) if x.strip()]
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
            doc, quote, trimmed = verify_quote(anchor.quote, index, prefer=anchor.doc or r.doc)
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
