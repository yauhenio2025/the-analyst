"""Ledger walls (study 2026-09-04): parse findings-ledger rows, verify anchors verbatim, check ids.

Shape only, never merit. A row is `- [ID] finding — field: value — anchor: "quote" — … — confidence: x`.
The wall verifies that each anchor appears verbatim in the source after the same normalisation the
dossier's anchor wall uses (`src.dossier.walls.normalize`), trimming from the end word by word to a
floor; that ids are unique; and that every id a text cites exists in the ledger it should exist in.
"""
from __future__ import annotations

import re
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
_FIELD_RE = re.compile(r"(?:^|\s[—–]\s|\s-\s)\s*([a-z][a-z_ \-]{1,24}?)\s*:\s*", re.IGNORECASE)
_CITED_RE = re.compile(r"\[([A-Za-z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)*)\]")
_CONF_RE = re.compile(r"confidence\s*:\s*(high|medium|low)", re.IGNORECASE)
_STATUS_RE = re.compile(r"status\s*:\s*(confirmed|weakened|rejected|added)", re.IGNORECASE)
_DIM_RE = re.compile(r"\bdim\s*:\s*([a-z0-9_]+)", re.IGNORECASE)
_DOC_RE = re.compile(r"\bdoc\s*:\s*([A-Za-z0-9_\-.:]+)")
_FROM_RE = re.compile(r"\bfrom\s*:\s*([^—\n]+)", re.IGNORECASE)


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

    def render(self) -> str:
        return f"- [{self.id}] {self.text}".rstrip()


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
        # finding = text up to the first " — field:" separator
        head = re.split(r"\s[—–]\s(?=[a-z][a-z_ \-]{1,24}\s*:)", rest, maxsplit=1)[0]
        row.finding = head.strip()
        cm = _CONF_RE.search(rest); row.confidence = cm.group(1).lower() if cm else ""
        sm = _STATUS_RE.search(rest); row.status = sm.group(1).lower() if sm else ""
        dm = _DIM_RE.search(rest); row.dim = dm.group(1) if dm else ""
        dcm = _DOC_RE.search(rest); row.doc = dcm.group(1) if dcm else ""
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
        if prefer and prefer in self.norm and self._has(prefer, q):
            return prefer
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

    @property
    def anchor_rate(self) -> float:
        return round(self.verified / self.rows, 3) if self.rows else 0.0

    def as_dict(self) -> dict:
        return {
            "rows": self.rows, "with_anchor": self.with_anchor, "verified": self.verified, "trimmed": self.trimmed,
            "anchor_rate": self.anchor_rate, "failed_ids": self.failed_ids[:40],
            "duplicate_ids": self.duplicate_ids[:20], "missing_cited": self.missing_cited[:40],
        }


def verify_rows(rows: Iterable[LedgerRow], index: SourceIndex) -> WallReport:
    """Mark each row's anchor verified/trimmed in place; report counts and failures."""
    rep = WallReport()
    seen: set[str] = set()
    for r in rows:
        rep.rows += 1
        if r.id in seen:
            rep.duplicate_ids.append(r.id)
        seen.add(r.id)
        if not r.anchor:
            rep.failed_ids.append(r.id)
            continue
        rep.with_anchor += 1
        doc, quote, trimmed = verify_quote(r.anchor, index, prefer=r.doc)
        if doc:
            rep.verified += 1
            r.anchor_verified = True
            r.anchor_doc = doc
            if trimmed:
                rep.trimmed += 1
                r.anchor_trimmed = True
                r.anchor = quote
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
    return [i for i in cited_ids(prose) if i not in ok and re.match(r"^[A-Z][A-Za-z0-9]*\.?F?\d+$", i)]


def render_rows(rows: Iterable[LedgerRow], heading: str = "## Findings ledger") -> str:
    return "\n".join([heading] + [r.render() for r in rows])


def reanchor_request(failed: list[LedgerRow]) -> str:
    """The one re-anchor round: the rows whose anchors were not verbatim, returned to the model."""
    lines = [
        "These rows' anchors are NOT verbatim in the source (after normalising whitespace, quotes and hyphenation). "
        "Return ONLY these rows again, same ids, same finding, each with a verbatim anchor copied exactly from the "
        "source (at most 200 characters, no ellipses), or omit a row you cannot anchor. Same row format, under the "
        "heading `## Findings ledger`. No other text.",
        "",
    ]
    lines += [r.render() for r in failed]
    return "\n".join(lines)
