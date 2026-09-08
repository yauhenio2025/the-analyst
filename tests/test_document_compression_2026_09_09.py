"""Large source packets must round-trip without oversized PostgreSQL text inserts."""
import sqlite3

import pytest

from src.executor import db, document_store as documents


@pytest.fixture
def storage(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DATABASE_URL", "")
    monkeypatch.setattr(db, "SQLITE_PATH", tmp_path / "documents.sqlite")
    monkeypatch.setattr(db, "_initialized", False)
    db.init_db()


def source():
    return 'Riley’s œuvre preserves whitespace, quotes "", 中文, and source anchors.\n\n' * 16000


def test_large_document_roundtrip_preserves_source_identity(storage):
    text = source()
    doc_id = documents.store_document("Frozen research packet", text, role="dossier_source")
    raw = db.execute("SELECT * FROM executor_documents WHERE doc_id=%s", (doc_id,), fetch="one")
    assert raw["text_encoding"] == "json-gzip-base64-v1"
    assert len(raw["text"]) < len(text) // 10
    assert raw["char_count"] == len(text)
    assert raw["content_hash"] == documents.compute_content_hash(text)
    assert documents.get_document_text(doc_id) == text
    decoded = documents.get_document(doc_id)
    assert decoded["text"] == text
    assert "text_encoding" not in decoded
    assert documents.list_documents()[0]["char_count"] == len(text)


def test_registered_documents_decode_and_reuse_original_hash(storage):
    text = source()
    payload = [{"external_doc_key": "frozen", "binding_role": "target", "title": "Frozen text",
                "text": text, "content_hash": documents.compute_content_hash(text)}]
    first = documents.sync_external_documents(consumer_key="stacks", external_project_id="test", documents=payload)
    second = documents.sync_external_documents(consumer_key="stacks", external_project_id="test", documents=payload)
    assert first[0]["doc_id"] == second[0]["doc_id"]
    assert second[0]["sync_status"] == "unchanged"
    resolved = documents.load_registered_documents(consumer_key="stacks", external_project_id="test", external_doc_keys=["frozen"])
    assert resolved["frozen"]["text"] == text
    assert resolved["frozen"]["content_hash"] == payload[0]["content_hash"]


@pytest.mark.parametrize("change", ["invalid_payload", "wrong_hash", "wrong_length", "unknown_encoding"])
def test_corrupt_compressed_sources_fail_loudly(storage, change):
    doc_id = documents.store_document("Frozen text", source())
    assignments = {"invalid_payload": "text='broken base64'", "wrong_hash": "content_hash='wrong'",
                   "wrong_length": "char_count=3", "unknown_encoding": "text_encoding='future-unsupported'"}
    db.execute(f"UPDATE executor_documents SET {assignments[change]} WHERE doc_id=%s", (doc_id,))
    with pytest.raises(ValueError):
        documents.get_document_text(doc_id)


def test_legacy_literal_text_and_hash_migrate_without_interpretation(tmp_path, monkeypatch):
    path = tmp_path / "legacy.sqlite"
    text = "json-gzip-base64-v1: this was always literal source text"
    with sqlite3.connect(path) as conn:
        conn.execute("CREATE TABLE executor_documents (doc_id TEXT PRIMARY KEY,title TEXT NOT NULL,author TEXT,"
                     "role TEXT,text TEXT NOT NULL,char_count INTEGER,content_hash TEXT,created_at TEXT)")
        conn.execute("INSERT INTO executor_documents VALUES ('old','Old text',NULL,'target',?,?,NULL,'2026-09-08')", (text,len(text)))
    monkeypatch.setattr(db, "DATABASE_URL", "")
    monkeypatch.setattr(db, "SQLITE_PATH", path)
    monkeypatch.setattr(db, "_initialized", False)
    db.init_db()
    row = documents.get_document("old")
    assert row["text"] == text
    assert row["content_hash"] == documents.compute_content_hash(text)


def test_hash_backfill_decodes_compressed_content(storage):
    text = source()
    doc_id = documents.store_document("Frozen text", text)
    db.execute("UPDATE executor_documents SET content_hash='' WHERE doc_id=%s", (doc_id,))
    db._migrate_sqlite()
    assert documents.get_document(doc_id)["content_hash"] == documents.compute_content_hash(text)
