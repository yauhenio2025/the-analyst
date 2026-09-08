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

import gzip
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.executor.db import _is_postgres, execute

logger = logging.getLogger(__name__)
_ready = False
_JSON_GZIP_PREFIX = b"\x00analyst-json-gzip-v1\x00"
_JSON_COMPRESS_THRESHOLD = 512 * 1024


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


def encode_blob_data(mime: Optional[str], data: bytes) -> bytes:
    """Encode stored bytes consistently, including writes inside callers' transactions."""
    # Large JSON checkpoints become hex bytea literals under psycopg2. A 9.5 MB
    # investigation write was running when the production database backend was
    # killed. Compress before SQL adaptation; callers still
    # receive the exact original bytes and MIME type through get_blob.
    if (mime or "").split(";", 1)[0].strip() == "application/json" and len(data) >= _JSON_COMPRESS_THRESHOLD:
        compressed = _JSON_GZIP_PREFIX + gzip.compress(data, compresslevel=3, mtime=0)
        if len(compressed) < len(data):
            data = compressed
    return data


def decode_blob_data(mime: Optional[str], data: bytes | memoryview | str) -> bytes:
    """Restore original bytes; damaged compressed records fail instead of becoming empty data."""
    if isinstance(data, memoryview):
        data = data.tobytes()
    elif isinstance(data, str):
        data = data.encode("latin-1")
    data = bytes(data)
    if (mime or "").split(";", 1)[0].strip() == "application/json" and data.startswith(_JSON_GZIP_PREFIX):
        data = gzip.decompress(data[len(_JSON_GZIP_PREFIX):])
    return data


def put_blob(key: str, mime: str, data: bytes) -> None:
    ensure_table()
    data = encode_blob_data(mime, data)
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
    mime = row.get("mime") or "application/octet-stream"
    return (mime, decode_blob_data(mime, row["data"]))


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
