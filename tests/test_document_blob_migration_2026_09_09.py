"""Hash backfills must read chunked documents inside their migration transaction."""
import random
import string

from src.dossier import blob_store
from src.executor import db, document_store


def test_startup_backfill_uses_migration_cursor_without_nested_schema_initialization(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DATABASE_URL", "")
    monkeypatch.setattr(db, "SQLITE_PATH", tmp_path / "migration.sqlite")
    monkeypatch.setattr(db, "_initialized", False)
    monkeypatch.setattr(blob_store, "_ready", False)
    text = "".join(random.Random(19).choices(string.ascii_letters + string.digits, k=1_600_000))
    doc_id = document_store.store_document("Unchanged source", text)
    row = db.execute("SELECT text_encoding FROM executor_documents WHERE doc_id=%s", (doc_id,), fetch="one")
    assert row["text_encoding"] == "blob-json-v1"
    db.execute("UPDATE executor_documents SET content_hash='' WHERE doc_id=%s", (doc_id,))
    monkeypatch.setattr(db, "_initialized", False)
    monkeypatch.setattr(blob_store, "_ready", False)
    schema_calls = []
    with monkeypatch.context() as patch:
        def nested_schema_init():
            schema_calls.append(True)
            raise AssertionError("migration attempted schema initialization on a second connection")
        patch.setattr(blob_store, "ensure_table", nested_schema_init)
        db.init_db()
    assert schema_calls == []
    restored = document_store.get_document(doc_id)
    assert restored["content_hash"] == document_store.compute_content_hash(text)
    assert restored["char_count"] == len(text)
    assert restored["text"] == text
