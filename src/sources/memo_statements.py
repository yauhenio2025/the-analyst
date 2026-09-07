"""A memo against its sources: the fidelity audit's second input mode.

The Stacks' `digest_check` (zotero-stacks `app/digest_check.py`) checks a synthesis memo statement by statement against
the texts it cites. Its inputs are a code-numbered statement list (`no`, `section`, `statement`, `sources` = the labels
the statement cites) and the source texts by uid (`label`, `uid`, `title`, `year`, `creators`, `text`). This module
turns that file into the citation family's evidence index, so `citation_fidelity_audit` reads it through the same
machinery as a citation index (`src/sources/citation_evidence.py`): the memo is the citing author A, one text per
memo; each statement is an indexed passage of A; each cited source is a held witness with its full text as one
`section` window. No judgment happens here; the wall checks anchors and ids, the model judges the readings.

A `role: statements` source carries the Stacks' file as JSON (or the reduced form {"memo": {...}, "statements": [...],
"sources": [...]}). The Stacks' own verdict vocabulary (supported · partly · unsupported · misattributed · unchecked)
is kept in the index metadata for the report; the audit answers in its own (accurate · fair · selective · stretched ·
misattributed · unverifiable).
"""
from __future__ import annotations

import json
import re
from typing import Any

STATEMENT_KEYS = {"statements", "sources"}


def is_statements_file(obj: Any) -> bool:
    return (isinstance(obj, dict) and isinstance(obj.get("statements"), list) and isinstance(obj.get("sources"), list)
            and bool(obj["statements"]) and all(isinstance(s, dict) and "statement" in s for s in obj["statements"]))


def _kind_from_section(section: str) -> str:
    """The memo shape's section names when the Stacks' file carries no `kind` (files before 2026-09-06 18:40)."""
    sec = (section or "").lower()
    if sec.startswith(("still open", "open")):
        return "question"
    if sec.startswith(("next", "reading")):
        return "suggestion"
    return "attribution"


def _text_of(source: dict) -> str:
    """A source's text as one string. The Stacks' first references export (turn 8, 2026-09-07) carried `text` as the
    pair (text, "rendition") their text_of() returns; a list or tuple yields its longest string, a dict its `text`."""
    t = source.get("text")
    if isinstance(t, (list, tuple)):
        strings = [x for x in t if isinstance(x, str)]
        return max(strings, key=len) if strings else ""
    if isinstance(t, dict):
        return str(t.get("text") or "")
    return t or ""


WINDOW_CAP = 80_000          # a source longer than this is windowed (2026-09-07: turn 11's re-read carried three Hintze volumes, 4.6M chars, and the executor refused the prompt)
WINDOW_HALF = 2_500          # chars either side of a hit
WINDOW_MAX_PER_SOURCE = 14
STOP = {"the", "and", "that", "this", "with", "from", "for", "his", "her", "its", "their", "which", "what", "into", "are", "was", "were", "not", "but", "has", "have",
        "had", "also", "than", "then", "there", "here", "about", "over", "such", "more", "most", "some", "any", "all", "one", "two", "how", "why", "when", "where", "who",
        "whom", "will", "would", "could", "should", "may", "might", "can", "does", "did", "been", "being", "they", "them", "these", "those", "very", "only", "just",
        "argues", "argued", "says", "said", "claims", "claim", "text", "essay", "book", "chapter", "reply", "response", "work", "works", "state", "states"}


def _terms(*texts: str, n: int = 12) -> list[str]:
    """The distinctive words of a statement (and its clue): capitalised names first, then long words, stop words out."""
    words = re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'’-]{3,}", " ".join(t for t in texts if t))
    names = [w for w in words if w[0].isupper() and w.lower() not in STOP]
    rest = [w for w in words if not w[0].isupper() and w.lower() not in STOP and len(w) >= 6]
    out: list[str] = []
    for w in names + rest:
        if w.lower() not in {x.lower() for x in out}:
            out.append(w)
    return out[:n]


def lexical_windows(text: str, statements: list[dict], *, half: int = WINDOW_HALF, cap: int = WINDOW_MAX_PER_SOURCE) -> list[dict]:
    """The passages of a long text that the statements point at: for each statement, the spans around the densest hits of
    its terms; overlapping spans merged; at most `cap` windows. Code only — the model reads the windows, never the volume."""
    low = text.lower()
    scored: list[tuple[int, int, str]] = []
    for st in statements:
        terms = _terms(str(st.get("statement") or st.get("hit") or ""), str(st.get("clue") or ""))
        if not terms:
            continue
        hits: list[int] = []
        for t in terms:
            start = 0; tl = t.lower()
            while True:
                i = low.find(tl, start)
                if i < 0 or len(hits) > 400:
                    break
                hits.append(i); start = i + len(tl)
        if not hits:
            continue
        hits.sort()
        # the densest neighbourhoods: count hits within ±half of each hit, keep the best few per statement
        best = sorted(((sum(1 for h in hits if abs(h - c) <= half), c) for c in hits), reverse=True)
        taken: list[int] = []
        for score, c in best:
            if all(abs(c - t) > half for t in taken):
                taken.append(c); scored.append((score, c, f"statement {st.get('no')}"))
            if len(taken) >= 3:
                break
    if not scored:
        return []
    scored.sort(reverse=True)
    spans = sorted((max(0, c - half), min(len(text), c + half), why) for _, c, why in scored[:cap])
    merged: list[list] = []
    for a, b, why in spans:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b); merged[-1][2] = merged[-1][2] + "; " + why if why not in merged[-1][2] else merged[-1][2]
        else:
            merged.append([a, b, why])
    return [{"how": "search", "section": f"chars {a}–{b} (for {why})", "text": text[a:b], "locus": {"start": a, "end": b}} for a, b, why in merged]   # `how` must be page, section or search (the index's law)


def _label_map(sources: list[dict]) -> dict[str, str]:
    out = {}
    for s in sources:
        uid = s.get("uid") or ""
        for lab in {s.get("label") or "", re.sub(r"[^\w]", "", str(s.get("label") or "")).upper()} - {""}:
            out[lab] = uid
    return out


def _windows_for(text: str, source: dict, statements: list[dict], passages: list[dict]) -> list[dict]:
    """A short text travels whole; a long one as the lexical windows of the statements that cite it (every statement when none
    cites it by label), else clipped to its head with a note the audit reports as unverifiable, never as absent."""
    if len(text) <= WINDOW_CAP:
        return [{"how": "section", "section": "whole held text", "text": text}]
    citing_nos = {p["no"] for p in passages if source.get("uid") in p["cites"]}
    sts = [st for st in statements if st.get("no") in citing_nos] or statements
    wins = lexical_windows(text, sts)
    if wins:
        wins[-1] = {**wins[-1], "text": wins[-1]["text"] + f"\n\n[the held text is {len(text):,} chars; only {len(wins)} windows of it were read — a place outside them is unverifiable, not absent]"}
        return wins
    return [{"how": "section", "section": "head of the held text (clipped; no statement term found)", "text": text[:WINDOW_CAP // 4]}]


def statements_to_evidence_index(obj: dict) -> dict:
    """The evidence index for one memo: texts = [the memo as A]; checks = one per cited source with its full text."""
    if not is_statements_file(obj):
        raise ValueError("a statements file needs non-empty `statements` (with `statement`) and `sources` arrays")
    memo = obj.get("memo") or {}
    memo_uid = memo.get("uid") or "memo"
    memo_title = memo.get("title") or "the memo"
    labels = _label_map(obj["sources"])
    labels_by_uid = {s.get("uid"): (s.get("label") or s.get("uid")) for s in obj["sources"] if s.get("uid")}
    passages, unresolved = [], []
    for s in obj["statements"]:
        cited = []
        for lab in s.get("sources") or []:
            uid = labels.get(str(lab)) or labels.get(re.sub(r"[^\w]", "", str(lab)).upper())
            if uid:
                cited.append(uid)
            else:
                unresolved.append({"no": s.get("no"), "label": lab})
        kind = s.get("kind") or _kind_from_section(s.get("section", ""))
        passages.append({"ref_id": f"st{s.get('no')}", "no": s.get("no"), "section": s.get("section", ""), "kind": kind,
                         "hit": " ".join(str(s.get("statement", "")).split()), "cites": cited, "locus": f"statement {s.get('no')}",
                         "pair_ids": [f"st{s.get('no')}/{labels_by_uid.get(u, u)}" for u in cited]})
    # The citing text A is the numbered statement list itself: those are the claims under audit and the words an
    # anchor from A must be found in. The memo's markdown follows as context (a batch of the first run treated the
    # absence of statement markers in the memo as "unverifiable" because the statements travelled only as index
    # passages whose text the metadata strips).
    listing = "\n\n".join(f"[{p['ref_id']}] ({p['section']}; {p['kind']}; cites {', '.join(labels_by_uid.get(u, u) for u in p['cites']) or 'nothing'}) {p['hit']}"
                          for p in passages)
    body = ("THE STATEMENTS UNDER AUDIT (each is A's attribution; quote from these lines as A's anchor)\n\n" + listing
            + ("\n\nTHE MEMO THEY WERE TAKEN FROM (context for a statement's meaning; not a second witness)\n\n" + memo["markdown"]
               if memo.get("markdown") else ""))
    texts = [{"uid": memo_uid, "title": memo_title, "year": memo.get("date") or "", "kind": "memo",
              "text": body, "passages": passages}]
    checks = []
    for s in obj["sources"]:
        text = _text_of(s)
        if not text.strip():
            continue
        checks.append({"copy": {"uid": s.get("uid"), "label": s.get("label"), "title": s.get("title"), "year": s.get("year"),
                                "creators": s.get("creators"), "publication": s.get("publication"), "pages": s.get("pages"),
                                "kind": s.get("kind"), "text_source": s.get("text_source")},
                       "title": s.get("title") or s.get("uid"),
                       "cited_by": [p["no"] for p in passages if s.get("uid") in p["cites"]],
                       "windows": _windows_for(text, s, obj["statements"], passages)})
    if not checks:
        raise ValueError("a statements file needs at least one source with text")
    held = {c["copy"]["uid"] for c in checks}
    pairs = [{"pair_id": pid, "statement": p["no"], "source": u, "label": labels_by_uid.get(u, u), "held": u in held, "kind": p["kind"]}
             for p in passages for pid, u in zip(p["pair_ids"], p["cites"])]
    kinds = {k: sum(1 for p in passages if p["kind"] == k) for k in ("attribution", "question", "suggestion")}
    plan = {"purpose": f"Check every statement of '{memo_title}' against the sources it cites; a statement that cites no source is checked against all supplied sources and marked so.",
            "questions": ["Does the source say what the statement attributes to it, at the cited place or anywhere in the held text?",
                          "Is the attribution accurate, fair, selective, stretched, misattributed, or unverifiable in the held text?"],
            "warnings": ["The memo is a synthesis: a statement may fuse several sources; audit each cited source separately.",
                         "A statement's own words are the memo's, not the source's; never treat the memo as a witness for itself.",
                         "The held texts may be clipped; report a place the audit could not reach as unverifiable, never as absent."],
            "themes": sorted({p["section"] for p in passages if p["section"]}),
            "stacks_verdict_vocabulary": obj.get("verdicts") or "supported | partly | unsupported | misattributed | unchecked",
            "stacks_check_runs": [{k: v for k, v in r.items() if k != "check"} for r in (obj.get("stacks_check_runs") or [])][:8]}
    plan["pair_ids"] = ("Every statement × cited-source pair has an index ID of the form st<statement no>/<source label> "
                        "(listed under pairs); use it as pair-ref. Audit every pair whose source is held; a pair whose source "
                        "is not held is unverifiable. A statement citing no source is checked against every held source once. "
                        "The statements are the numbered [st<no>] lines at the head of the memo document; the memo's prose "
                        "carries no markers, and their absence there is never a reason for unverifiable.")
    plan["kinds"] = ("Each statement carries a kind. attribution: A claims the source says or shows something; audit it as an attribution. "
                     "question (an open question) or suggestion (a next step, a reading): not an attribution; set attribution: none and judge "
                     "grounding only — accurate when the sources supply what the line presupposes, fair when partly, unverifiable when the "
                     "held texts do not; never stretched or misattributed for a question or a suggestion. "
                     f"Counts: {kinds}.")
    return {"role": "evidence_index", "mode": "memo_against_sources", "author": memo_title, "person": "the cited sources",
            "texts": texts, "checks": checks, "unchecked": unresolved, "plan": plan, "pairs": pairs,
            "settings": {"statements": len(passages), "sources": len(checks), "pairs": len(pairs), "source": "stacks digest_check inputs"}}


def batches(obj: dict, size: int = 8) -> list[dict]:
    """The same file cut into slices of `size` statements, every source kept: the one-call modes cap a ledger at a few
    dozen rows, and a memo of fifty statements over four sources is a hundred pairs. Callers merge the ledgers."""
    if not is_statements_file(obj):
        raise ValueError("not a statements file")
    sts = obj["statements"]
    return [{**obj, "statements": sts[i:i + size], "batch": {"index": n, "of": (len(sts) + size - 1) // size,
                                                              "statements": [s.get("no") for s in sts[i:i + size]]}}
            for n, i in enumerate(range(0, len(sts), size), start=1)]


def statements_documents(documents: dict[str, str]) -> dict[str, str]:
    """Rewrite every statements-file document in `documents` as an evidence index (JSON text); others pass through."""
    out = {}
    for key, text in documents.items():
        obj = None
        try:
            obj = json.loads(text)
        except (ValueError, TypeError):
            pass
        out[key] = json.dumps(statements_to_evidence_index(obj), ensure_ascii=False) if is_statements_file(obj) else text
    return out
