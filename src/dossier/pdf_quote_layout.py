"""Conservative prose-column matching with offsets into the unchanged PDF text."""
from __future__ import annotations

import hashlib
import re
from collections import Counter

from src.dossier.investigation import quote_span

_TABLE_LABEL = re.compile(r"(?:^|\s{2,})(?:table|tab\.)\s*(?:\d|[IVX]+\b)", re.I)


def column_views(body: str, lo: int, hi: int):
    """Return mapped columns only for one strong, repeated prose gutter.

    This is a layout restriction, not a license to skip unmatched words. A line
    crossing the gutter becomes an unmatchable barrier in both derived views.
    Labeled tables, numeric rows, short cells and ambiguous gutters are rejected.
    """
    if any(c in body[lo:hi] for c in "\v\f\x1c\x1d\x1e\x85\u2028\u2029"):
        return []
    rows, counts, eligible = [], Counter(), 0
    cursor = lo
    for raw in body[lo:hi].splitlines(keepends=True):
        line = raw.rstrip("\r\n")
        rows.append((cursor, line, raw[len(line):]))
        cursor += len(raw)
        if _TABLE_LABEL.search(line) or "|" in line:
            return []
        if len(line.strip()) < 35:
            continue
        found = False
        for gap in re.finditer(r" {2,}", line):
            if len(line[:gap.start()].strip()) < 15 or len(line[gap.end():].strip()) < 15:
                continue
            counts.update(range(gap.start() + 1, gap.end()))
            found = True
        eligible += found
    if not counts:
        return []
    peak = max(counts.values())
    best = sorted(x for x, n in counts.items() if n == peak)
    if peak < 8 or peak < eligible * .6 or any(b != a + 1 for a, b in zip(best, best[1:])):
        return []
    # A competing gutter with almost as much support indicates multiple columns
    # or a table. A wider contiguous gutter remains one candidate.
    strong = sorted(x for x, n in counts.items() if n >= 8)
    if any(b != a + 1 for a, b in zip(strong, strong[1:])):
        return []
    cut = best[-1]

    def split_allowed(line):
        return any(g.start() <= cut < g.end() for g in re.finditer(r" {2,}", line))

    paired = [(line[:cut].strip(), line[cut:].strip()) for _, line, _ in rows
              if len(line) > cut and split_allowed(line) and line[:cut].strip() and line[cut:].strip()]
    if len(paired) < 8:
        return []
    for col in (0, 1):
        pieces = [pair[col] for pair in paired]
        # Sentence continuations distinguish sustained prose from lists/cells.
        continuations = sum(p[0].islower() and len(p.split()) >= 4 for p in pieces)
        numeric = sum(sum(c.isdigit() for c in p) > max(3, len(p) // 8) for p in pieces)
        if continuations < 4 or continuations < len(pieces) * .2 or numeric > len(pieces) * .15:
            return []
    out = []
    for col in (0, 1):
        chars, positions = [], []
        for start, line, ending in rows:
            if len(line) > cut and not split_allowed(line) and line[:cut].strip() and line[cut:].strip():
                chars.append("\x00")
                positions.append(None)
                continue
            left, right = (0, min(cut, len(line))) if col == 0 else (min(cut, len(line)), len(line))
            while left < right and line[left].isspace():
                left += 1
            while right > left and line[right - 1].isspace():
                right -= 1
            chars.extend(line[left:right])
            positions.extend(range(start + left, start + right))
            chars.extend(ending)
            positions.extend(range(start + len(line), start + len(line) + len(ending)))
        out.append(("".join(chars), positions,
                    {"gutter_column": cut, "column": col + 1, "support_lines": peak}))
    return out


def pdf_column_quote(quote, body, ranges, page_spans, *, review=None, pdf_sha256=None):
    """Find an exact quote in one column/page and one actually inspected window."""
    # Text geometry cannot distinguish an unlabelled prose table from article
    # columns. Require a separate PDF layout review before interpreting a gutter.
    if (not isinstance(review, dict) or review.get("reviewed_from_pdf") is not True or
            not pdf_sha256 or review.get("pdf_sha256") != pdf_sha256 or
            review.get("body_sha256") != hashlib.sha256(body.encode()).hexdigest()):
        return None
    approvals = {p["page"]: p for p in review.get("pages", [])
                 if isinstance(p, dict) and p.get("kind") == "prose_columns" and p.get("columns") == 2}
    for page in page_spans:
        approval = approvals.get(page["page"])
        if approval is None:
            continue
        lo, hi = approval.get("reviewed_start"), approval.get("reviewed_end")
        if (type(lo) is not int or type(hi) is not int or
                not 0 <= page["start"] <= lo < hi <= page["end"] <= len(body)):
            continue
        if not any(a < hi and lo < b for a, b in ranges):
            continue
        for view, positions, layout in column_views(body, lo, hi):
            if layout["gutter_column"] != approval.get("gutter_column"):
                continue
            found = quote_span(quote, view, [(0, len(view))])
            if found is None:
                continue
            indices = positions[found[0]:found[1]]
            if not indices or any(i is None for i in indices):
                continue
            if any(b <= a for a, b in zip(indices, indices[1:])):
                continue
            if not any(a <= min(indices) and max(indices) < b for a, b in ranges):
                continue
            spans = []
            for i in indices:
                if spans and i == spans[-1]["end"]:
                    spans[-1]["end"] += 1
                else:
                    spans.append({"start": i, "end": i + 1})
            for span in spans:
                span["text"] = body[span["start"]:span["end"]]
            return {"quote_spans": spans,
                    "source_quote": "".join(s["text"] for s in spans),
                    "quote_start": min(indices), "quote_end": max(indices) + 1,
                    "quote_match": "pdf_column_layout",
                    "quote_layout": {**layout, "page": page["page"], "normalization": found[2],
                                     "method": "reviewed_prose_gutter_v1",
                                     "review_method": review.get("method"),
                                     "reviewed_start": lo, "reviewed_end": hi,
                                     "body_sha256": review["body_sha256"], "pdf_sha256": pdf_sha256}}
    return None
