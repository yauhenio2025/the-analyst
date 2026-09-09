"""Lost accepted responses and concurrent uploads do not create another paid job."""
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi import HTTPException

from src.api.routes import dossier
from src.dossier.schemas import CreateDossierRequest
from src.dossier import store
from tests.test_large_dossier_storage_2026_09_09 import storage  # noqa: F401


def test_lost_response_and_simultaneous_retry_return_one_job(storage, monkeypatch):
    starts = []
    monkeypatch.setattr(dossier.runner, 'start', lambda job_id: starts.append(job_id))
    from src.actions import register
    monkeypatch.setattr(register, 'record_event', lambda *a, **k: None)
    req = CreateDossierRequest(sources=[{'kind':'paste','text':'Original source. ' * 40}], intent='Read worker organising',
                               idempotency_key='stacks:isolated-inquiry', autopilot=True, spend_cap_usd=15)
    with ThreadPoolExecutor(max_workers=3) as pool:
        replies = list(pool.map(lambda _: dossier.create(req), range(3)))
    assert len({r['job_id'] for r in replies}) == 1 and len(starts) == 1
    assert len(store.list_jobs()) == 1
    # A later retry after process-local state disappears still uses the DB receipt.
    assert dossier.create(req)['job_id'] == replies[0]['job_id']
    changed = req.model_copy(update={'intent':'A different commission'})
    with pytest.raises(HTTPException) as exc:
        dossier.create(changed)
    assert exc.value.status_code == 409 and len(starts) == 1
