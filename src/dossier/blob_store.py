"""Durable bytes for figures, plates and dossier files (2026-09-04).

Render wipes the service disk on every deploy, and until today every rendered
figure, plate and dossier.pdf lived only there: three deploys on the morning of
the demo erased them. The dossier text was already in Postgres; now the bytes
are too. Disk stays a cache: writers put bytes here as well as on disk, readers
restore the file from here when the disk copy is gone.

Keys: figure:<figure_id> · figure-meta:<figure_id> · plate:<job_id>:<filename>
      dossier:<job_id>:<html|md|pdf>
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.executor.db import _is_postgres, execute

logger = logging.getLogger(__name__)
_ready = False


def ensure_table() -> None:
    global _ready
    if _ready:
        return
    execute(
        "CREATE TABLE IF NOT EXISTS dossier_blobs ("
        " blob_key TEXT PRIMARY KEY, mime TEXT, size INTEGER, data BYTEA, created_at TEXT)"
    )
    _ready = True


def _bin(data: bytes):
    if _is_postgres():
        import psycopg2

        return psycopg2.Binary(data)
    return data


def put_blob(key: str, mime: str, data: bytes) -> None:
    ensure_table()
    execute(
        "INSERT INTO dossier_blobs (blob_key, mime, size, data, created_at) VALUES (%s, %s, %s, %s, %s)"
        " ON CONFLICT (blob_key) DO UPDATE SET mime = EXCLUDED.mime, size = EXCLUDED.size,"
        " data = EXCLUDED.data, created_at = EXCLUDED.created_at",
        (key, mime or "application/octet-stream", len(data), _bin(data), datetime.now(timezone.utc).isoformat()),
    )


def put_blob_safe(key: str, mime: str, data: bytes) -> bool:
    """Never let durability break a render: log and continue on failure."""
    try:
        put_blob(key, mime, data)
        return True
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"blob put failed for {key}: {exc}")
        return False


def get_blob(key: str) -> Optional[tuple[str, bytes]]:
    ensure_table()
    row = execute("SELECT mime, data FROM dossier_blobs WHERE blob_key = %s", (key,), fetch="one")
    if not row:
        return None
    data = row["data"]
    if isinstance(data, memoryview):
        data = data.tobytes()
    elif isinstance(data, str):
        data = data.encode("latin-1")
    return (row.get("mime") or "application/octet-stream", bytes(data))


def has_blob(key: str) -> bool:
    ensure_table()
    return bool(execute("SELECT 1 AS one FROM dossier_blobs WHERE blob_key = %s", (key,), fetch="one"))


def ensure_file(path: Path, key: str) -> bool:
    """Restore `path` from the blob `key` when the disk copy is missing. True if the file exists afterwards."""
    if path.exists():
        return True
    try:
        found = get_blob(key)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"blob get failed for {key}: {exc}")
        return False
    if not found:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(found[1])
    tmp.replace(path)
    logger.info(f"restored {path.name} from blob {key} ({len(found[1])} bytes)")
    return True


def delete_blob(key: str) -> None:
    ensure_table()
    execute("DELETE FROM dossier_blobs WHERE blob_key = %s", (key,))


def list_keys(prefix: str = "") -> list[dict]:
    ensure_table()
    rows = execute("SELECT blob_key, mime, size, created_at FROM dossier_blobs WHERE blob_key LIKE %s ORDER BY blob_key", (prefix + "%",), fetch="all")
    return rows or []
