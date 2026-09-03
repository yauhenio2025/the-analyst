"""Stacks adapter: export a view or a set of uids as text, and split the export into documents.

Export format (one file, N items). A CONTENTS block lists the headers first;
each item then starts with a header line:

    ===== [n/N] Creator (Year) — Title — Publication — [Library · Key] =====

The stacks service is LOCAL (STACKS_URL); on Render it is unreachable, so the
export functions raise StacksUnavailable with a plain message instead of hanging.
"""
from __future__ import annotations

import logging
import os
import re
from typing import Optional

from src.sources.schemas import Document

logger = logging.getLogger(__name__)

STACKS_URL = os.environ.get("STACKS_URL", "http://localhost:8000").rstrip("/")
EXPORT_TIMEOUT_S = float(os.environ.get("STACKS_EXPORT_TIMEOUT_S", "120"))

HEADER_RE = re.compile(r"^=====\s*\[(\d+)/(\d+)\]\s*(.+?)\s*=====\s*$", re.MULTILINE)
CREATOR_YEAR_RE = re.compile(r"^(?P<creators>.*?)\s*\((?P<year>[^()]*)\)\s*$")
LIBRARY_KEY_RE = re.compile(r"^\[(?P<library>.+?)\s*·\s*(?P<key>[^\]]+)\]$")
SEP = " — "
MIN_BODY_CHARS = 40  # a header followed by less than this is a CONTENTS line


class StacksUnavailable(RuntimeError):
    pass


def looks_like_stacks_export(text: str) -> bool:
    if not text:
        return False
    for m in HEADER_RE.finditer(text):
        # one header with a body is enough
        tail = text[m.end(): m.end() + 400]
        if len(tail.strip()) >= MIN_BODY_CHARS and not tail.lstrip().startswith("====="):
            return True
    return False


def parse_header(body: str) -> dict:
    """'Creator (Year) — Title — Publication — [Library · Key]' → fields (best effort)."""
    parts = [p.strip() for p in body.split(SEP)]
    out = {"creators": "", "year": "", "title": body.strip(), "publication": "", "library": "", "stacks_key": ""}
    if len(parts) >= 2:
        lk = LIBRARY_KEY_RE.match(parts[-1])
        if lk:
            out["library"] = lk.group("library").strip()
            out["stacks_key"] = lk.group("key").strip()
            parts = parts[:-1]
    cy = CREATOR_YEAR_RE.match(parts[0]) if parts else None
    if cy and len(parts) >= 2:
        out["creators"] = cy.group("creators").strip()
        out["year"] = cy.group("year").strip()
        rest = parts[1:]
    else:
        rest = parts
    if len(rest) >= 2:
        out["publication"] = rest[-1]
        out["title"] = SEP.join(rest[:-1])
    elif len(rest) == 1:
        out["title"] = rest[0]
    return out


def split_stacks_export(text: str, key_prefix: str = "") -> list[Document]:
    """Split an export into documents, skipping the CONTENTS block and duplicate headers."""
    matches = list(HEADER_RE.finditer(text))
    docs: dict[str, Document] = {}
    order: list[str] = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip("\n")
        if len(body.strip()) < MIN_BODY_CHARS:
            continue  # CONTENTS entry (or an empty item)
        n, total, header = int(m.group(1)), int(m.group(2)), m.group(3)
        fields = parse_header(header)
        key = f"{key_prefix}{fields['stacks_key'] or ('item' + str(n))}"
        doc = Document(key=key, text=body.strip(), char_count=len(body.strip()), **fields)
        if key in docs and docs[key].char_count >= doc.char_count:
            continue
        if key not in docs:
            order.append(key)
        docs[key] = doc
    return [docs[k] for k in order]


def _post_export(payload: dict) -> str:
    import httpx

    url = f"{STACKS_URL}/api/export"
    try:
        with httpx.Client(timeout=EXPORT_TIMEOUT_S) as client:
            resp = client.post(url, json=payload)
    except Exception as exc:
        raise StacksUnavailable(
            f"stacks export unreachable at {url} ({exc.__class__.__name__}: {exc}). "
            "Stacks is a local service; paste the export text instead."
        ) from exc
    if resp.status_code >= 400:
        raise StacksUnavailable(f"stacks export failed: HTTP {resp.status_code} {resp.text[:200]}")
    ctype = resp.headers.get("content-type", "")
    if "json" in ctype:
        data = resp.json()
        if isinstance(data, dict):
            return str(data.get("text") or data.get("content") or data.get("export") or "")
        return str(data)
    return resp.text


def export_view(view_id: str) -> str:
    return _post_export({"view": view_id, "format": "txt"})


def export_uids(uids: list[str]) -> str:
    return _post_export({"uids": list(uids), "format": "txt"})


def export_documents(*, view_id: Optional[str] = None, uids: Optional[list[str]] = None) -> list[Document]:
    text = export_view(view_id) if view_id else export_uids(uids or [])
    docs = split_stacks_export(text)
    if not docs and text.strip():
        docs = [Document(key="stacks", title=f"stacks export {view_id or ''}".strip(), text=text, char_count=len(text))]
    return docs
