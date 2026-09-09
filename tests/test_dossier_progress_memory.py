"""Progress and execution must not hydrate duplicate large source submissions."""
import json

from src.api.routes import dossier
from src.dossier import blob_store, store, investigation
from src.dossier.schemas import DossierJob, DossierOptions
from tests.test_large_dossier_storage_2026_09_09 import storage, varied_source  # noqa: F401


def test_progress_and_execution_skip_original_submission_blob(storage, monkeypatch):
    job = DossierJob(sources=[{'kind': 'paste', 'text': varied_source()}],
        documents=[{'key': 'original', 'executor_doc_id': 'held-document'}],
        options=DossierOptions(intent='Frozen comparison', path={'chain_key': 'field_investigation'}))
    store.create_job(job)
    row = store.execute('SELECT sources_json FROM dossier_jobs WHERE id=%s', (job.id,), fetch='one')
    original_ref = json.loads(row['sources_json'])[store._JSON_BLOB_REF]
    get_blob = blob_store.get_blob
    def guarded(key):
        assert key != original_ref, 'Progress hydrated the entire frozen submission'
        return get_blob(key)
    monkeypatch.setattr(blob_store, 'get_blob', guarded)
    execution = store.get_job_for_execution(job.id)
    assert execution.sources == [] and execution.documents == job.documents
    progress = dossier.get_one(job.id, view='progress')
    assert progress['sources'] == [] and progress['options']['intent'] == 'Frozen comparison'
    monkeypatch.setattr(investigation, 'load_investigation', lambda _: {'kind': 'field_investigation', 'complete': False})
    assert dossier.get_investigation(job.id)['status'] == 'queued'
    monkeypatch.setattr(dossier.dossier_events, 'list_events', lambda *a: [])
    assert dossier.get_events(job.id)['events'] == []
    monkeypatch.setattr(blob_store, 'get_blob', get_blob)
    assert store.get_job(job.id).sources == job.sources
    assert dossier.get_one(job.id)['sources'] == job.sources
