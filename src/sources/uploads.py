"""Local files (PDF / Markdown / text) -> one bundle in the stacks-export shape.

The bundle is stored through the exemplar store (executor DB) under a generated
name, so a job can reference it as {"kind": "exemplar", "name": ...} and the usual
header splitter turns it back into N documents.
"""
from __future__ import annotations

import hashlib
import io
import logging
import re
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

SUPPORTED = {".pdf", ".md", ".markdown", ".txt", ".text"}
MAX_TITLE = 160


def _clean(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _pdf_text(data: bytes) -> tuple[str, dict]:
    from pypdf import PdfReader  # lazy: only needed for PDFs
    reader = PdfReader(io.BytesIO(data))
    pages = []
    for p in reader.pages:
        try:
            pages.append(p.extract_text() or "")
        except Exception as exc:  # a single bad page must not kill the bundle
            logger.warning("pdf page extraction failed: %s", exc)
            pages.append("")
    meta = {}
    try:
        m = reader.metadata or {}
        meta = {"title": (m.get("/Title") or "").strip(), "author": (m.get("/Author") or "").strip(),
                "year": ""}
        created = str(m.get("/CreationDate") or "")
        ym = re.search(r"(19|20)\d{2}", created)
        if ym:
            meta["year"] = ym.group(0)
    except Exception:
        pass
    return "\n\n".join(pages), meta | {"pages": len(reader.pages)}


def _title_from_text(text: str, fallback: str) -> str:
    for line in text.splitlines()[:40]:
        line = line.strip().strip("#").strip()
        if 12 <= len(line) <= MAX_TITLE and not line.endswith((".", ":")) and sum(c.isalpha() for c in line) > 8:
            return line
    return fallback


def _llm_bibliographic(text: str) -> dict:
    """Haiku reads the opening of the document and returns title/creators/year/publication.
    Cheap (~3K tokens) and far more reliable than PDF metadata. Empty dict on any failure."""
    import json
    import os
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return {}
    try:
        import anthropic
        client = anthropic.Anthropic()
        head = text[:6000]
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=300, temperature=0,
            system="You extract bibliographic facts from the opening of an academic or professional document. "
                   "Ignore repository cover pages (ResearchGate, SSRN, publisher banners) and running headers. "
                   "Reply with ONLY a JSON object: {\"title\": str, \"creators\": str (\"Surname, Given; Surname, Given\"), "
                   "\"year\": str (4 digits or \"\"), \"publication\": str (journal/book/venue or \"\")}. Use \"\" when unknown.",
            messages=[{"role": "user", "content": head}],
        )
        raw = "".join(getattr(b, "text", "") for b in msg.content).strip()
        raw = raw[raw.find("{"): raw.rfind("}") + 1]
        out = json.loads(raw)
        return {k: str(out.get(k) or "").strip() for k in ("title", "creators", "year", "publication")}
    except Exception as exc:
        logger.warning("bibliographic extraction skipped: %s", exc)
        return {}


def extract_document(filename: str, data: bytes) -> dict:
    ext = Path(filename).suffix.lower()
    if ext not in SUPPORTED:
        raise ValueError(f"unsupported file type: {ext or filename} (use .pdf, .md or .txt)")
    stem = Path(filename).stem.replace("_", " ").replace("-", " ").strip() or "document"
    if ext == ".pdf":
        raw, meta = _pdf_text(data)
    else:
        raw, meta = data.decode("utf-8", errors="replace"), {}
    text = _clean(raw)
    if len(text) < 200:
        raise ValueError(f"{filename}: too little extractable text ({len(text)} chars) — scanned PDF?")
    bib = _llm_bibliographic(text)
    title = (bib.get("title") or meta.get("title") or "")[:MAX_TITLE] or _title_from_text(text, stem)
    key = "up" + hashlib.sha256(data).hexdigest()[:8].upper()
    return {"key": key, "title": title, "creators": bib.get("creators") or meta.get("author") or "",
            "year": bib.get("year") or meta.get("year") or "", "publication": bib.get("publication") or "",
            "filename": filename, "char_count": len(text), "pages": meta.get("pages"), "text": text}


def build_bundle(files: list[tuple[str, bytes]], title: str = "") -> tuple[str, str, dict]:
    if not files:
        raise ValueError("no files")
    docs = [extract_document(fn, data) for fn, data in files]
    n = len(docs)
    stamp = datetime.now(timezone.utc)
    digest = hashlib.sha256("".join(d["key"] for d in docs).encode()).hexdigest()[:8]
    name = f"upload-{stamp.strftime('%Y%m%d')}-{digest}.txt"
    bundle_title = title.strip() or (docs[0]["title"] if n == 1 else f"{docs[0]['title']} (+{n - 1} more)")
    lines = [f"UPLOAD BUNDLE — {n} items — {stamp.strftime('%Y-%m-%d %H:%M UTC')}",
             "Each item starts with a line of the form:  ===== [n/N] Creator (Year) — Title — Publication — [Library · Key] =====",
             "", "CONTENTS"]
    def header(i, d):
        creators = d["creators"] or "Unknown"
        year = d["year"] or "n.d."
        pub = d.get("publication") or f"uploaded file: {d['filename']}"
        return f"===== [{i}/{n}] {creators} ({year}) — {d['title']} — {pub} — [Upload · {d['key']}] ====="
    lines += [header(i, d) for i, d in enumerate(docs, 1)]
    lines.append("")
    for i, d in enumerate(docs, 1):
        lines += ["", header(i, d), "", d["text"], ""]
    text = "\n".join(lines)
    meta = {"name": name, "title": bundle_title, "document_count": n, "char_count": len(text),
            "documents": [{k: v for k, v in d.items() if k != "text"} for d in docs]}
    return name, text, meta
