"""SourceSpec → list[Document]. A pasted text carrying stacks headers is auto-split."""
from __future__ import annotations

import logging
import os
import re
from pathlib import Path

from src.sources.schemas import Document, SourceSpec
from src.sources.stacks import export_documents, looks_like_stacks_export, split_stacks_export

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
EXEMPLARS_DIR = Path(os.environ.get("EXEMPLARS_DIR", str(REPO_ROOT / "data" / "exemplars")))
MAX_TITLE_CHARS = 90


def _title_from_text(text: str, fallback: str) -> str:
    for line in text.splitlines():
        line = line.strip().strip("#").strip()
        if len(line) >= 8:
            return line[:MAX_TITLE_CHARS]
    return fallback


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return s[:24] or "doc"


def list_exemplars() -> list[dict]:
    if not EXEMPLARS_DIR.exists():
        return []
    out = []
    for p in sorted(EXEMPLARS_DIR.iterdir()):
        if p.is_file() and p.suffix.lower() in (".txt", ".md") and p.name.lower() != "readme.md":
            text = p.read_text(encoding="utf-8", errors="replace")
            docs = split_stacks_export(text) if looks_like_stacks_export(text) else []
            out.append({
                "name": p.name,
                "char_count": len(text),
                "document_count": len(docs) or 1,
                "documents": [d.meta() for d in docs][:20],
            })
    return out


def load_exemplar(name: str) -> str:
    safe = Path(name).name
    path = EXEMPLARS_DIR / safe
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"exemplar not found: {safe}")
    return path.read_text(encoding="utf-8", errors="replace")


def resolve_sources(specs: list[SourceSpec]) -> list[Document]:
    docs: list[Document] = []
    used: set[str] = set()

    def add(doc: Document) -> None:
        key = doc.key
        i = 2
        while key in used:
            key = f"{doc.key}_{i}"
            i += 1
        doc.key = key
        used.add(key)
        doc.char_count = len(doc.text)
        docs.append(doc)

    for idx, spec in enumerate(specs, start=1):
        if spec.kind in ("paste", "upload", "stacks_export"):
            text = (spec.text or "").strip()
            if not text:
                logger.warning(f"source {idx} ({spec.kind}) has no text; skipped")
                continue
            if looks_like_stacks_export(text):
                for d in split_stacks_export(text):
                    add(d)
            else:
                title = spec.title or _title_from_text(text, f"Pasted document {idx}")
                add(Document(key=_slug(spec.title or f"doc{idx}"), title=title, text=text))
        elif spec.kind == "exemplar":
            if not spec.name:
                raise ValueError("exemplar source needs `name`")
            text = load_exemplar(spec.name)
            if looks_like_stacks_export(text):
                for d in split_stacks_export(text):
                    add(d)
            else:
                add(Document(key=_slug(spec.name), title=spec.title or spec.name, text=text))
        elif spec.kind == "stacks_view":
            if not spec.view_id:
                raise ValueError("stacks_view source needs `view_id`")
            for d in export_documents(view_id=spec.view_id):
                add(d)
        elif spec.kind == "stacks_uids":
            if not spec.uids:
                raise ValueError("stacks_uids source needs `uids`")
            for d in export_documents(uids=spec.uids):
                add(d)
        else:  # pragma: no cover
            raise ValueError(f"unknown source kind: {spec.kind}")
    return docs
