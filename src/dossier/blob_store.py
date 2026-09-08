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
import hashlib
import json
import logging
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.executor.db import _is_postgres, execute, get_connection

logger = logging.getLogger(__name__)
_ready = False
_JSON_GZIP_PREFIX = b"\x00analyst-json-gzip-v1\x00"
_JSON_COMPRESS_THRESHOLD = 512 * 1024
_CHUNK_SIZE = 512 * 1024
_CHUNK_ENCODING = "chunks-v1"
_SCHEMA_LOCK = threading.Lock()


def ensure_table() -> None:
    """Initialize storage before entering a caller-owned transaction."""
    global _ready
    if _ready:
        return
    with _SCHEMA_LOCK:
        if _ready:
            return
        with get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS dossier_blobs ("
                    " blob_key TEXT PRIMARY KEY, mime TEXT, size INTEGER, data BYTEA, created_at TEXT,"
                    " storage_encoding TEXT NOT NULL DEFAULT '')"
                )
                if _is_postgres():
                    cursor.execute("ALTER TABLE dossier_blobs ADD COLUMN IF NOT EXISTS storage_encoding TEXT NOT NULL DEFAULT ''")
                else:
                    columns = {row[1] for row in cursor.execute("PRAGMA table_info(dossier_blobs)").fetchall()}
                    if "storage_encoding" not in columns:
                        cursor.execute("ALTER TABLE dossier_blobs ADD COLUMN storage_encoding TEXT NOT NULL DEFAULT ''")
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS dossier_blob_chunks ("
                    " blob_key TEXT NOT NULL REFERENCES dossier_blobs(blob_key) ON DELETE CASCADE,"
                    " chunk_index INTEGER NOT NULL, data BYTEA NOT NULL,"
                    " PRIMARY KEY (blob_key, chunk_index))"
                )
                conn.commit()
            except Exception:
                conn.rollback()
                raise
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


def _sql(sql: str) -> str:
    return sql if _is_postgres() else sql.replace("%s", "?")


def _bytes(value) -> bytes:
    return value.encode("latin-1") if isinstance(value, str) else bytes(value)


def put_blob_in_cursor(cursor, key: str, mime: str, raw_data: bytes, *, overwrite: bool = True) -> bool:
    """Write atomically in the caller's transaction; False means an existing winner.

    The caller must ensure_table() before its transaction and commit or roll back
    afterwards. Lock the parent row before changing chunks, including when two
    writers race to create an immutable blob.
    """
    mime = mime or "application/octet-stream"
    raw_data = bytes(raw_data)
    encoded = encode_blob_data(mime, raw_data)
    chunked = len(encoded) > _CHUNK_SIZE
    if chunked:
        manifest = {"version": 1, "encoded_size": len(encoded),
                    "encoded_sha256": hashlib.sha256(encoded).hexdigest(),
                    "decoded_size": len(raw_data), "decoded_sha256": hashlib.sha256(raw_data).hexdigest(),
                    "chunk_count": (len(encoded) + _CHUNK_SIZE - 1) // _CHUNK_SIZE}
        data = json.dumps(manifest, separators=(",", ":")).encode("ascii")
    else:
        data = encoded
    conflict = ("DO UPDATE SET mime=EXCLUDED.mime, size=EXCLUDED.size, data=EXCLUDED.data,"
                " created_at=EXCLUDED.created_at, storage_encoding=EXCLUDED.storage_encoding") if overwrite else "DO NOTHING"
    cursor.execute(_sql(
        "INSERT INTO dossier_blobs (blob_key,mime,size,data,created_at,storage_encoding)"
        " VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (blob_key) " + conflict + " RETURNING blob_key"
    ), (key, mime, len(encoded), _bin(data), datetime.now(timezone.utc).isoformat(), _CHUNK_ENCODING if chunked else ""))
    if cursor.fetchone() is None:
        return False
    cursor.execute(_sql("DELETE FROM dossier_blob_chunks WHERE blob_key=%s"), (key,))
    if chunked:
        for index, start in enumerate(range(0, len(encoded), _CHUNK_SIZE)):
            cursor.execute(_sql("INSERT INTO dossier_blob_chunks (blob_key,chunk_index,data) VALUES (%s,%s,%s)"),
                           (key, index, _bin(encoded[start:start + _CHUNK_SIZE])))
    return True


def get_blob_in_cursor(cursor, key: str) -> Optional[tuple[str, bytes]]:
    """Read one consistent manifest/chunk snapshot, even at READ COMMITTED."""
    cursor.execute(_sql(
        "SELECT b.mime,b.size,b.data,b.storage_encoding,c.chunk_index,c.data"
        " FROM dossier_blobs b LEFT JOIN dossier_blob_chunks c ON c.blob_key=b.blob_key"
        " WHERE b.blob_key=%s ORDER BY c.chunk_index"
    ), (key,))
    rows = cursor.fetchall()
    if not rows:
        return None
    mime, stored_size, data, encoding = rows[0][:4]
    mime = mime or "application/octet-stream"
    data = _bytes(data)
    if not encoding:
        if len(rows) != 1 or rows[0][4] is not None:
            raise ValueError("legacy blob has unexpected chunks")
        return mime, decode_blob_data(mime, data)
    if encoding != _CHUNK_ENCODING:
        raise ValueError(f"unsupported blob storage encoding: {encoding}")
    try:
        manifest = json.loads(data)
        if not isinstance(manifest, dict) or type(manifest.get("version")) is not int or manifest["version"] != 1:
            raise ValueError("unsupported manifest version")
        for field in ("encoded_size", "decoded_size", "chunk_count"):
            if type(manifest.get(field)) is not int or manifest[field] < 0:
                raise ValueError(f"invalid {field}")
        size = manifest["encoded_size"]
        count = manifest["chunk_count"]
        if (size <= _CHUNK_SIZE or stored_size != size or
                count != (size + _CHUNK_SIZE - 1) // _CHUNK_SIZE or len(rows) != count):
            raise ValueError("chunk count or encoded length mismatch")
        chunks = []
        for index, row in enumerate(rows):
            if row[4] != index or row[5] is None:
                raise ValueError("missing or unordered chunk")
            chunk = _bytes(row[5])
            if len(chunk) != min(_CHUNK_SIZE, size - index * _CHUNK_SIZE):
                raise ValueError("chunk length mismatch")
            chunks.append(chunk)
        encoded = b"".join(chunks)
        if hashlib.sha256(encoded).hexdigest() != manifest.get("encoded_sha256"):
            raise ValueError("encoded checksum mismatch")
        decoded = decode_blob_data(mime, encoded)
        if len(decoded) != manifest["decoded_size"] or hashlib.sha256(decoded).hexdigest() != manifest.get("decoded_sha256"):
            raise ValueError("decoded checksum or length mismatch")
        return mime, decoded
    except (ValueError, TypeError, KeyError, OSError, EOFError) as exc:
        raise ValueError(f"invalid chunked blob {key}: {exc}") from exc


def put_blob(key: str, mime: str, data: bytes) -> None:
    ensure_table()
    with get_connection() as conn:
        try:
            put_blob_in_cursor(conn.cursor(), key, mime, data)
            conn.commit()
        except Exception:
            conn.rollback()
            raise


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
    with get_connection() as conn:
        try:
            found = get_blob_in_cursor(conn.cursor(), key)
            conn.commit()
            return found
        except Exception:
            conn.rollback()
            raise


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
    with get_connection() as conn:
        try:
            # The FK cascade shares this statement's row lock and transaction.
            conn.cursor().execute(_sql("DELETE FROM dossier_blobs WHERE blob_key=%s"), (key,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise


def list_keys(prefix: str = "") -> list[dict]:
    ensure_table()
    rows = execute("SELECT blob_key, mime, size, created_at FROM dossier_blobs WHERE blob_key LIKE %s ORDER BY blob_key", (prefix + "%",), fetch="all")
    return rows or []
