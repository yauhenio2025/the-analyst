"""Exemplar inputs stored in the executor DB (SQLite locally, Postgres on Render).

Exemplar texts are NOT in git (the repo is public; the papers are copyrighted), so
they are uploaded once via POST /v1/dossier/exemplars and read back from here.
Folder exemplars under EXEMPLARS_DIR are still honoured (see src/sources/resolve.py).
"""
from __future__ import annotations

import logging
import threading
from datetime import datetime, timezone
from typing import Optional

from src.executor.db import execute, init_db

logger = logging.getLogger(__name__)

_ready = False
_lock = threading.Lock()

DDL = """
CREATE TABLE IF NOT EXISTS dossier_exemplars (
    name TEXT PRIMARY KEY,
    title TEXT,
    description TEXT,
    text TEXT NOT NULL,
    char_count INTEGER,
    document_count INTEGER,
    created_at TEXT
)
"""


def ensure_table() -> None:
    global _ready
    if _ready:
        return
    with _lock:
        if _ready:
            return
        init_db()
        execute(DDL)
        _ready = True


def upsert_exemplar(name: str, text: str, title: str = "", description: str = "", document_count: int = 1) -> dict:
    ensure_table()
    now = datetime.now(timezone.utc).isoformat()
    execute("DELETE FROM dossier_exemplars WHERE name = %s", (name,))
    execute(
        "INSERT INTO dossier_exemplars (name, title, description, text, char_count, document_count, created_at) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (name, title or name, description or "", text, len(text), int(document_count or 1), now),
    )
    return {"name": name, "title": title or name, "description": description or "",
            "char_count": len(text), "document_count": int(document_count or 1), "created_at": now, "source": "db"}


def list_db_exemplars() -> list[dict]:
    ensure_table()
    rows = execute(
        "SELECT name, title, description, char_count, document_count, created_at FROM dossier_exemplars ORDER BY created_at DESC",
        (), fetch="all",
    ) or []
    return [dict(r) | {"source": "db"} for r in rows]


def get_db_exemplar(name: str) -> Optional[str]:
    ensure_table()
    row = execute("SELECT text FROM dossier_exemplars WHERE name = %s", (name,), fetch="one")
    return row["text"] if row else None


def delete_exemplar(name: str) -> bool:
    ensure_table()
    if get_db_exemplar(name) is None:
        return False
    execute("DELETE FROM dossier_exemplars WHERE name = %s", (name,))
    return True
