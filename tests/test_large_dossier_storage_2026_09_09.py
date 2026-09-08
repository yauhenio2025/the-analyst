"""Frozen source packets and growing checkpoints keep SQL rows small and lossless."""
import json
import random
import string

import pytest

from src.dossier import blob_store, store
from src.dossier.schemas import DossierJob, DossierOptions
from src.executor import db


@pytest.fixture
def storage(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DATABASE_URL", "")
    monkeypatch.setattr(db, "SQLITE_PATH", tmp_path / "dossier.sqlite")
    monkeypatch.setattr(db, "_initialized", False)
    monkeypatch.setattr(blob_store, "_ready", False)
    monkeypatch.setattr(store, "_table_ready", False)
    store.ensure_table()


def varied_source():
    return "".join(random.Random(71).choices(string.ascii_letters + string.digits, k=1800000))


def test_large_frozen_sources_and_updates_use_small_references(storage):
    text = varied_source()
    job = DossierJob(sources=[{"kind": "paste", "key": "frozen", "text": text}],
                     options=DossierOptions(intent="Read the unchanged source"))
    store.create_job(job)
    row = db.execute("SELECT sources_json FROM dossier_jobs WHERE id=%s", (job.id,), fetch="one")
    assert len(row["sources_json"]) < 300
    assert store.get_job(job.id).sources == job.sources
    analysis = {"1": {"final_output": text, "engine_key": "field_investigation_field_read"}}
    store.update_job(job.id, analysis=analysis, sections={"title": "Saved memo", "executive_summary": [text]})
    row = db.execute("SELECT analysis_json,sections_json FROM dossier_jobs WHERE id=%s", (job.id,), fetch="one")
    assert all(len(value) < 300 for value in row.values())
    restored = store.get_job(job.id)
    assert restored.analysis == analysis
    assert restored.sections.executive_summary == [text]
    assert store.list_jobs()[0].title == "Saved memo"


def test_literal_reference_shaped_values_stay_literal(storage):
    value = {store._JSON_BLOB_REF: "literal source metadata", "sha256": "literal", "bytes": 4}
    assert store._loads(store._dumps(value), None) == value
    assert store._loads('{"ordinary":"legacy"}', None) == {"ordinary": "legacy"}


@pytest.mark.parametrize("damage", ["missing", "wrong_hash", "wrong_length"])
def test_broken_large_source_reference_cannot_be_loaded_as_empty_job(storage, damage):
    job = DossierJob(sources=[{"kind": "paste", "text": varied_source()}])
    store.create_job(job)
    row = db.execute("SELECT sources_json FROM dossier_jobs WHERE id=%s", (job.id,), fetch="one")
    reference = json.loads(row["sources_json"])
    if damage == "missing":
        blob_store.delete_blob(reference[store._JSON_BLOB_REF])
    else:
        reference["sha256" if damage == "wrong_hash" else "bytes"] = "wrong" if damage == "wrong_hash" else 2
        db.execute("UPDATE dossier_jobs SET sources_json=%s WHERE id=%s", (json.dumps(reference),job.id))
    with pytest.raises(ValueError):
        store.get_job(job.id)
