"""Walls — shape validators for anchors (the veo2 doctrine: walls hold shape, never merit).

The anchor wall: a quote must appear verbatim (after normalization) in the
document it claims to come from. A quote that fails is trimmed from the end,
word by word, down to a floor; if a verified prefix survives it is kept and
marked `trimmed`. If the quote appears in another document, the doc_key is
corrected. Otherwise the anchor is dropped and the caller decides what the
loss means (a table row without any verified anchor is dropped).
"""
from __future__ import annotations

import re
import unicodedata
from typing import Optional

from src.dossier.schemas import Anchor, Table

MAX_QUOTE_CHARS = 200
MIN_TRIMMED_CHARS = 40
MIN_TRIMMED_WORDS = 6

# ── Arithmetic walls shared by the concretization passes (shape only, never merit) ──

_DIGIT_RUN = re.compile(r"\d[\d,.:/%-]*")
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])[\"'”’)]*\s+(?=[A-Z\"'“‘(\[])")
_ABBREV = re.compile(r"\b(e\.g|i\.e|etc|vs|cf|Mr|Mrs|Ms|Dr|Prof|St|No|approx|Inc|Ltd|Co|U\.S|U\.K|al)\.", re.I)
EXHIBIT_TOKEN = re.compile(r"\[\[\s*(table|figure)\s*:\s*([a-z0-9_\-]+)\s*\]\]", re.I)


def digit_runs(text: str) -> list[str]:
    """Every run of digits (with the punctuation that rides inside numbers) in `text`."""
    return [m.group(0).rstrip(",.:/%-") for m in _DIGIT_RUN.finditer(text or "")]


def has_digit_run(text: str) -> bool:
    """The caption-number law: numbers belong to the prose and the tables, never to a caption."""
    return bool(_DIGIT_RUN.search(text or ""))


def sentence_count(text: str) -> int:
    """How many sentences a claim carries (abbreviations tolerated). Empty text counts as zero."""
    t = (text or "").strip()
    if not t:
        return 0
    t = _ABBREV.sub(lambda m: m.group(0).replace(".", "·"), t)
    parts = [x for x in _SENTENCE_SPLIT.split(t) if x.strip()]
    return max(1, len(parts))


def is_one_sentence(text: str) -> bool:
    return sentence_count(text) == 1


def shingles(text: str, n: int = 8) -> set[str]:
    words = normalize(text).split()
    return {" ".join(words[i:i + n]) for i in range(0, max(0, len(words) - n + 1))}


def shingle_overlap(a: str, b: str, n: int = 8) -> float:
    """Fraction of `a`'s n-word shingles that also occur in `b` (0.0 when either is too short)."""
    sa, sb = shingles(a, n), shingles(b, n)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa)


def exhibit_tokens(text: str) -> list[tuple[str, str]]:
    """[(kind, key)] for every [[table:key]] / [[figure:key]] token in reading order."""
    return [(m.group(1).lower(), m.group(2)) for m in EXHIBIT_TOKEN.finditer(text or "")]


def numbers_not_in(text: str, material_norm: str) -> list[str]:
    """Digit runs in `text` that occur nowhere in the (normalized) material — the no-new-numbers law."""
    out = []
    for run in digit_runs(text):
        core = run.replace(",", "")
        if run not in material_norm and core not in material_norm:
            out.append(run)
    return out

_QUOTE_MAP = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    "–": "-", "—": "-", "‒": "-", "−": "-", "­": "",
    " ": " ", "…": "...",
}
_WS = re.compile(r"\s+")


def normalize(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    # U+00AD is a discretionary word break. Join its explicit line wrap before
    # _QUOTE_MAP removes the marker and leaves a false space inside the word.
    # Ordinary hyphens keep the existing normalization/alternate-index behavior.
    text = re.sub(r"(?<=\w)\u00ad[ \t]*\r?\n[ \t]*(?=\w)", "", text)
    text = "".join(_QUOTE_MAP.get(ch, ch) for ch in text)
    # join words hyphenated across line breaks ("exploit-\native")
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)
    text = _WS.sub(" ", text)
    return text.strip().lower()


class NormalizedCorpus:
    """Normalized document texts keyed by doc_key, built once per step."""

    def __init__(self, docs: dict[str, str]):
        self.texts = {k: normalize(v) for k, v in docs.items()}

    def keys(self) -> list[str]:
        return list(self.texts.keys())

    def contains(self, doc_key: str, quote_norm: str) -> bool:
        text = self.texts.get(doc_key)
        return bool(text) and bool(quote_norm) and quote_norm in text

    def find_any(self, quote_norm: str) -> Optional[str]:
        for k, text in self.texts.items():
            if quote_norm and quote_norm in text:
                return k
        return None


def verify_anchor(anchor: Anchor, corpus: NormalizedCorpus) -> Optional[Anchor]:
    """Return a verified (possibly trimmed / re-keyed) anchor, or None."""
    quote = (anchor.quote or "").strip()
    if not quote:
        return None
    if len(quote) > MAX_QUOTE_CHARS:
        quote = quote[:MAX_QUOTE_CHARS]
    words = quote.split()
    trimmed = False
    while True:
        candidate = " ".join(words)
        norm = normalize(candidate)
        if corpus.contains(anchor.doc_key, norm):
            return Anchor(doc_key=anchor.doc_key, quote=candidate, verified=True, trimmed=trimmed)
        other = corpus.find_any(norm)
        if other:
            return Anchor(doc_key=other, quote=candidate, verified=True, trimmed=trimmed)
        if len(words) <= MIN_TRIMMED_WORDS or len(candidate) <= MIN_TRIMMED_CHARS:
            return None
        words = words[:-1]
        trimmed = True


def verify_table(table: Table, corpus: NormalizedCorpus) -> tuple[Table, dict]:
    """Keep only rows with >= 1 verified anchor. Returns (table, report)."""
    kept = []
    report = {"rows_in": len(table.rows), "rows_dropped": 0, "anchors_dropped": 0,
              "anchors_trimmed": 0, "anchors_rekeyed": 0, "failed_quotes": []}
    for row in table.rows:
        verified_any = False
        new_cells = []
        for cell in row.cells:
            new_anchor = None
            if cell.anchor is not None:
                new_anchor = verify_anchor(cell.anchor, corpus)
                if new_anchor is None:
                    report["anchors_dropped"] += 1
                    if len(report["failed_quotes"]) < 12:
                        report["failed_quotes"].append(
                            {"doc_key": cell.anchor.doc_key, "quote": cell.anchor.quote[:120]})
                else:
                    verified_any = True
                    if new_anchor.trimmed:
                        report["anchors_trimmed"] += 1
                    if new_anchor.doc_key != cell.anchor.doc_key:
                        report["anchors_rekeyed"] += 1
            new_cells.append(cell.model_copy(update={"anchor": new_anchor}))
        if verified_any:
            kept.append(row.model_copy(update={"cells": new_cells}))
        else:
            report["rows_dropped"] += 1
    out = table.model_copy(update={"rows": kept, "rows_dropped": report["rows_dropped"]})
    return out, report
