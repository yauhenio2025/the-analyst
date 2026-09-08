"""Bounded SQL writes preserve complete blobs and transactional snapshots."""
from concurrent.futures import ThreadPoolExecutor
import gzip
import json
import os
from threading import Barrier, Event

import pytest

from src.dossier import blob_store as blobs
from src.executor import db


@pytest.fixture
def storage(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DATABASE_URL", "")
    monkeypatch.setattr(db, "SQLITE_PATH", tmp_path / "chunked.sqlite")
    monkeypatch.setattr(blobs, "_ready", False)
    blobs.ensure_table()


def payload():
    return os.urandom(2 * blobs._CHUNK_SIZE + 73)


def stored(key="large"):
    return db.execute("SELECT * FROM dossier_blobs WHERE blob_key=%s", (key,), fetch="one")


def chunks(key="large"):
    return db.execute("SELECT * FROM dossier_blob_chunks WHERE blob_key=%s ORDER BY chunk_index", (key,), fetch="all")


def test_large_binary_uses_bounded_chunks_and_small_manifest(storage):
    data = payload()
    blobs.put_blob("large", "application/octet-stream", data)
    row, parts = stored(), chunks()
    assert row["storage_encoding"] == "chunks-v1"
    assert len(row["data"]) < 1024
    assert row["size"] == len(data)
    assert len(parts) == 3
    assert all(len(part["data"]) <= 512 * 1024 for part in parts)
    assert blobs.get_blob("large") == ("application/octet-stream", data)
    assert blobs.list_keys("large")[0]["size"] == len(data)


def test_compressed_json_is_chunked_after_codec_and_restored_exactly(storage):
    data = json.dumps({"evidence": os.urandom(1_000_000).hex(), "unicode": "œuvre 中文"}, ensure_ascii=False).encode()
    encoded = blobs.encode_blob_data("application/json", data)
    assert blobs._CHUNK_SIZE < len(encoded) < len(data)
    blobs.put_blob("large", "application/json", data)
    assert stored()["size"] == len(encoded)
    assert chunks()[0]["data"].startswith(blobs._JSON_GZIP_PREFIX)
    assert blobs.get_blob("large") == ("application/json", data)


@pytest.mark.parametrize("size", [0, blobs._CHUNK_SIZE, blobs._CHUNK_SIZE + 1])
def test_storage_boundary_and_empty_blob(storage, size):
    data = b"x" * size
    blobs.put_blob("large", "application/octet-stream", data)
    assert bool(chunks()) == (size > blobs._CHUNK_SIZE)
    assert blobs.get_blob("large")[1] == data


@pytest.mark.parametrize("corruption", ["missing", "shifted_index", "short", "same_length_bytes", "stored_size", "encoded_hash", "decoded_hash", "decoded_size", "count", "unknown_encoding"])
def test_corrupt_manifest_or_chunks_fail_loudly(storage, corruption):
    blobs.put_blob("large", "application/octet-stream", payload())
    if corruption == "missing":
        db.execute("DELETE FROM dossier_blob_chunks WHERE blob_key='large' AND chunk_index=1")
    elif corruption == "shifted_index":
        db.execute("UPDATE dossier_blob_chunks SET chunk_index=9 WHERE blob_key='large' AND chunk_index=1")
    elif corruption in ("short", "same_length_bytes"):
        n = 3 if corruption == "short" else blobs._CHUNK_SIZE
        db.execute("UPDATE dossier_blob_chunks SET data=%s WHERE blob_key='large' AND chunk_index=1", (b"z" * n,))
    elif corruption == "stored_size":
        db.execute("UPDATE dossier_blobs SET size=size+1 WHERE blob_key='large'")
    elif corruption == "unknown_encoding":
        db.execute("UPDATE dossier_blobs SET storage_encoding='future' WHERE blob_key='large'")
    else:
        manifest = json.loads(stored()["data"])
        field = {"encoded_hash": "encoded_sha256", "decoded_hash": "decoded_sha256", "decoded_size": "decoded_size", "count": "chunk_count"}[corruption]
        manifest[field] = "0" * 64 if "hash" in corruption else manifest[field] + 1
        db.execute("UPDATE dossier_blobs SET data=%s WHERE blob_key='large'", (json.dumps(manifest).encode(),))
    with pytest.raises(ValueError, match="blob"):
        blobs.get_blob("large")


def test_overwrite_and_delete_leave_no_old_chunks(storage):
    blobs.put_blob("large", "application/octet-stream", payload())
    blobs.put_blob("large", "text/plain", b"short")
    assert not chunks()
    assert blobs.get_blob("large") == ("text/plain", b"short")
    blobs.put_blob("large", "application/octet-stream", payload())
    blobs.delete_blob("large")
    assert not chunks() and not blobs.has_blob("large")
    assert blobs.get_blob("large") is None


def test_failed_chunk_write_rolls_back_parent_chunks_and_other_caller_writes(storage):
    old = payload()
    blobs.put_blob("large", "application/octet-stream", old)
    db.execute("CREATE TRIGGER reject_chunk BEFORE INSERT ON dossier_blob_chunks WHEN NEW.chunk_index=1 BEGIN SELECT RAISE(ABORT,'injected chunk failure'); END")
    with pytest.raises(Exception, match="injected chunk failure"):
        blobs.put_blob("large", "application/octet-stream", payload())
    assert blobs.get_blob("large")[1] == old
    with db.get_connection() as conn:
        try:
            cursor = conn.cursor()
            blobs.put_blob_in_cursor(cursor, "other", "text/plain", b"should roll back")
            blobs.put_blob_in_cursor(cursor, "large", "application/octet-stream", payload())
        except Exception:
            conn.rollback()
    assert not blobs.has_blob("other")
    assert blobs.get_blob("large")[1] == old


def test_cursor_helpers_do_not_commit_callers_transaction(storage):
    with db.get_connection() as conn:
        cursor = conn.cursor()
        data = payload()
        assert blobs.put_blob_in_cursor(cursor, "large", "application/octet-stream", data)
        assert blobs.get_blob_in_cursor(cursor, "large")[1] == data
        conn.rollback()
    assert blobs.get_blob("large") is None and not chunks()


@pytest.mark.parametrize("overwrite", [False, True])
def test_concurrent_writers_keep_one_complete_value(storage, overwrite):
    barrier = Barrier(2)
    values = [payload(), payload()]
    def write(data):
        barrier.wait(timeout=10)
        with db.get_connection() as conn:
            cursor = conn.cursor()
            won = blobs.put_blob_in_cursor(cursor, "large", "application/octet-stream", data, overwrite=overwrite)
            result = blobs.get_blob_in_cursor(cursor, "large")[1]
            conn.commit()
            return won, result
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(write, values))
    if not overwrite:
        assert sum(won for won, _ in results) == 1
        assert results[0][1] == results[1][1]
    else:
        assert all(won for won, _ in results)
    assert blobs.get_blob("large")[1] in values
    assert len(chunks()) == 3


@pytest.mark.parametrize("mutation", ["overwrite", "delete"])
def test_one_query_read_retains_snapshot_during_concurrent_mutation(storage, mutation):
    old, new = payload(), payload()
    blobs.put_blob("large", "application/octet-stream", old)
    selected, changed = Event(), Event()
    def change():
        assert selected.wait(10)
        if mutation == "overwrite":
            blobs.put_blob("large", "application/octet-stream", new)
        else:
            blobs.delete_blob("large")
        changed.set()
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(change)
        with db.get_connection() as conn:
            cursor = conn.cursor()
            class SnapshotCursor:
                calls = 0
                def execute(self, sql, params):
                    self.calls += 1
                    cursor.execute(sql, params)
                    self.first = cursor.fetchone()
                    selected.set()
                    assert changed.wait(10)
                def fetchall(self):
                    return [self.first] + cursor.fetchall()
            snapshot = SnapshotCursor()
            assert blobs.get_blob_in_cursor(snapshot, "large")[1] == old
            assert snapshot.calls == 1
            conn.commit()
        future.result(timeout=10)
    assert blobs.get_blob("large") == (("application/octet-stream", new) if mutation == "overwrite" else None)


def test_old_table_migrates_without_touching_raw_or_gzip_records(storage, monkeypatch):
    db.execute("DROP TABLE dossier_blob_chunks")
    db.execute("DROP TABLE dossier_blobs")
    db.execute("CREATE TABLE dossier_blobs(blob_key TEXT PRIMARY KEY,mime TEXT,size INTEGER,data BYTEA,created_at TEXT)")
    raw = b'{"source":"still literal"}'
    for key, value in [("plain", raw), ("gzip", blobs._JSON_GZIP_PREFIX + gzip.compress(raw))]:
        db.execute("INSERT INTO dossier_blobs(blob_key,mime,size,data) VALUES(%s,%s,%s,%s)", (key, "application/json", len(value), value))
    monkeypatch.setattr(blobs, "_ready", False)
    blobs.ensure_table()
    assert blobs.get_blob("plain")[1] == blobs.get_blob("gzip")[1] == raw
