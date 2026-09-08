"""New immutable/transactional writers must preserve the live compressed blob format."""
from concurrent.futures import ThreadPoolExecutor
import json
from threading import Barrier

import pytest

from src.dossier import blob_store
from src.executor import db
from src.inquiries import service
from src.readings import registry


@pytest.fixture
def storage(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DATABASE_URL", "")
    monkeypatch.setattr(db, "SQLITE_PATH", tmp_path / "compressed.sqlite")
    monkeypatch.setattr(blob_store, "_ready", False)
    blob_store.ensure_table()


def stored(key):
    return db.execute("SELECT mime,size,data FROM dossier_blobs WHERE blob_key=%s", (key,), fetch="one")


def new_reading():
    return {"job_id": "fresh", "phase": "question_development", "engine": "question_development",
            "when": "2026-09-09", "n_rows": 1, "renders": [], "persons": ["Test Author"],
            "texts": ["em:CASE"], "rows": [], "intent": "A revised question",
            "context": {"previous_work": "Preserve the previous research and its qualifications. " * 16000}}


def test_strict_import_preserves_every_kind_of_preexisting_compressed_index(storage):
    keys = ["readings:person:test-author", "readings:surname:author", "readings:text:em:CASE", "readings:job:fresh"]
    previous = [{"job_id": "fresh", "phase": f"prior-{i}", "engine": "prior_method", "when": "2026-09-08",
                 "n_rows": 1, "renders": [], "name": "Test Author", "intent": "prior context " * 300} for i in range(200)]
    for key in keys:
        blob_store.put_blob(key, "application/json; charset=utf-8", json.dumps(previous).encode())
        assert stored(key)["data"].startswith(blob_store._JSON_GZIP_PREFIX)
    reading = new_reading()
    registry.save_reading(reading, strict=True)
    for key in keys:
        rows = json.loads(blob_store.get_blob(key)[1])
        assert rows[:-1] == previous
        assert rows[-1]["phase"] == "question_development"
        assert stored(key)["data"].startswith(blob_store._JSON_GZIP_PREFIX)
    record = stored("reading:fresh:question_development")
    assert record["data"].startswith(blob_store._JSON_GZIP_PREFIX)
    assert record["size"] == len(record["data"])
    assert registry.reading("fresh", "question_development") == reading
    # Replaying the import updates its entry, while retaining all prior phases.
    registry.save_reading(reading, strict=True)
    assert len(json.loads(blob_store.get_blob(keys[-1])[1])) == 201


def test_damaged_compressed_index_rolls_back_all_strict_reading_writes(storage):
    key = "readings:text:em:CASE"
    damaged = blob_store._JSON_GZIP_PREFIX + b"not a valid gzip payload"
    blob_store.put_blob(key, "application/json", damaged)
    before = stored(key)
    with pytest.raises((OSError, EOFError)):
        registry.save_reading(new_reading(), strict=True)
    assert stored(key) == before
    # The reading and person index were written before the failing text lookup.
    assert not blob_store.has_blob("reading:fresh:question_development")
    assert not blob_store.has_blob("readings:person:test-author")
    assert not blob_store.has_blob("readings:job:fresh")


@pytest.mark.parametrize("key", ["inquiry:prepared-test", "inquiry:planning:planning-prepared-test", "question:question-prepared-test"])
def test_large_immutable_records_compress_without_changing_frozen_identity_or_replay(storage, key):
    source = "The œuvre preserves distinctions, whitespace and accents.\n" * 16000
    value = {"input": {"sources": [{"text": source}]}, "method": "frozen", "created_at": "2026-09-09"}
    value["input_fingerprint"] = service.digest(value["input"])
    assert service._put_once(key, value) == value
    record = stored(key)
    assert record["data"].startswith(blob_store._JSON_GZIP_PREFIX)
    assert record["size"] == len(record["data"]) < len(service.encoded(value)) // 4
    assert service.digest(service._get(key)["input"]) == value["input_fingerprint"]
    assert service._put_once(key, {**value, "method": "replacement"}) == value
    assert stored(key) == record


def test_concurrent_large_immutable_writes_keep_one_complete_winner(storage):
    barrier = Barrier(2)
    values = [{"writer": i, "source": (f"Frozen evidence for writer {i}.\n" * 24000)} for i in range(2)]
    def write(value):
        barrier.wait(timeout=10)
        return service._put_once("question:concurrent-large", value)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(write, values))
    assert results[0] == results[1]
    assert results[0] in values
    assert stored("question:concurrent-large")["data"].startswith(blob_store._JSON_GZIP_PREFIX)
