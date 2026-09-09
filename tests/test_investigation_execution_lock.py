import subprocess
import sys
import time
from contextlib import contextmanager
from types import SimpleNamespace

import pytest

from src.dossier import execution_lock as locks, runner, store
from src.dossier.common import DossierDraining
from src.executor import db


@pytest.mark.parametrize('backend', ['sqlite', 'postgres'])
def test_overlapping_process_waits_for_owner_before_reading_latest_checkpoint(tmp_path, monkeypatch, backend):
    url = 'postgresql:///postgres' if backend == 'postgres' else ''
    if url:
        psycopg2 = pytest.importorskip('psycopg2')
        try:
            psycopg2.connect(url, connect_timeout=2).close()
        except psycopg2.OperationalError:
            pytest.skip('Local PostgreSQL unavailable')
    monkeypatch.setattr(db, 'DATABASE_URL', url)
    monkeypatch.setattr(db, 'SQLITE_PATH', tmp_path / 'test.sqlite')
    checkpoint = tmp_path / 'checkpoint'
    checkpoint.write_text('unfinished')
    child = r'''
import sys,time
from pathlib import Path
from src.executor import db
from src.dossier.execution_lock import investigation_owner,assert_owned
p=Path(sys.argv[1]);db.SQLITE_PATH=p/'test.sqlite';db.DATABASE_URL=sys.argv[2]
count=0
def stop():
 global count
 count+=1
 if count>=2:(p/'waiting').write_text('yes')
 return False
with investigation_owner(sys.argv[3],should_stop=stop):
 assert_owned(sys.argv[3])
 (p/'seen').write_text((p/'checkpoint').read_text())
'''
    job_id = 'test-' + tmp_path.name
    process = None
    try:
        with locks.investigation_owner(job_id):
            process = subprocess.Popen([sys.executable, '-c', child, str(tmp_path), url, job_id])
            deadline = time.monotonic() + 8
            while not (tmp_path / 'waiting').exists() and process.poll() is None and time.monotonic() < deadline:
                time.sleep(.02)
            assert (tmp_path / 'waiting').exists() and not (tmp_path / 'seen').exists()
            checkpoint.write_text('paid reading completed')
        assert process.wait(timeout=8) == 0
        assert (tmp_path / 'seen').read_text() == 'paid reading completed'
    finally:
        if process is not None and process.poll() is None:
            process.terminate()
            process.wait(timeout=8)


def test_runner_reloads_completion_after_acquiring_ownership(monkeypatch):
    job = SimpleNamespace(options=SimpleNamespace(path=SimpleNamespace(chain_key='field_investigation')),
                          status='analysis', step='analysis')
    reads = []
    monkeypatch.setattr(runner, 'get_job', lambda _: reads.append(job.status) or job)
    @contextmanager
    def acquire(*args, **kwargs):
        job.status = 'done'
        yield
    monkeypatch.setattr(locks, 'investigation_owner', acquire)
    monkeypatch.setattr(runner, 'load_documents', lambda _: pytest.fail('Completed investigation must not run again'))
    runner._run('already-finished')
    assert reads == ['analysis', 'done']


def test_lost_owner_cannot_write_over_another_instances_result(monkeypatch):
    writes = []
    def disconnected():
        raise ConnectionError('Ownership connection closed')
    token = locks._OWNER.set(('job', disconnected))
    monkeypatch.setattr(store, 'execute', lambda *args, **kwargs: writes.append(args))
    try:
        with pytest.raises(DossierDraining, match='ownership connection lost'):
            store.update_job('job', status='done')
        assert writes == []
    finally:
        locks._OWNER.reset(token)


def test_shutdown_before_acquisition_stops_without_claiming(tmp_path, monkeypatch):
    monkeypatch.setattr(db, 'DATABASE_URL', '')
    monkeypatch.setattr(db, 'SQLITE_PATH', tmp_path / 'test.sqlite')
    with pytest.raises(DossierDraining, match='waiting'):
        with locks.investigation_owner('job', should_stop=lambda: True):
            pytest.fail('Draining instance must not start research')
    with locks.investigation_owner('job'):
        locks.assert_owned('job')
