import os, tempfile, importlib

def test_exemplar_roundtrip(monkeypatch):
    d = tempfile.mkdtemp()
    monkeypatch.setenv("EXECUTOR_SQLITE_PATH", os.path.join(d, "t.db"))
    monkeypatch.delenv("EXECUTOR_DATABASE_URL", raising=False)
    import src.executor.db as db
    importlib.reload(db)
    import src.sources.exemplar_store as es
    importlib.reload(es)
    es.upsert_exemplar("k.md", "x" * 500, title="K", document_count=1)
    assert es.get_db_exemplar("k.md") == "x" * 500
    names = [e["name"] for e in es.list_db_exemplars()]
    assert "k.md" in names
    assert es.delete_exemplar("k.md") and es.get_db_exemplar("k.md") is None
