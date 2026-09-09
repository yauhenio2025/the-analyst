"""One investigation owner across overlapping processes and deployments."""
from contextlib import contextmanager
from contextvars import ContextVar
import hashlib
import time

from src.dossier.common import DossierDraining
from src.executor import db

_OWNER = ContextVar('investigation_execution_owner', default=None)


def assert_owned(job_id):
    owner = _OWNER.get()
    if owner and owner[0] == job_id:
        try:
            owner[1]()
        except Exception as exc:
            # A disconnected former owner must not overwrite the new owner's
            # checkpoint or mark its job failed when a provider finally returns.
            raise DossierDraining('Investigation ownership connection lost; research retained') from exc


@contextmanager
def investigation_owner(job_id, *, should_stop=lambda: False):
    digest = hashlib.sha256(('investigation:' + job_id).encode()).digest()
    connection = handle = None
    token = None
    try:
        if db._is_postgres():
            import psycopg2
            # Private session: returning a still-locked connection to the pool
            # would let an unrelated thread inherit this job's ownership.
            connection = psycopg2.connect(db.DATABASE_URL, connect_timeout=15)
            connection.autocommit = True
            key = int.from_bytes(digest[:8], 'big', signed=True)
            def attempt():
                with connection.cursor() as cursor:
                    cursor.execute('SELECT pg_try_advisory_lock(%s)', (key,))
                    return cursor.fetchone()[0]
            def check():
                with connection.cursor() as cursor:
                    cursor.execute('SELECT 1')
        else:
            import fcntl
            folder = db.SQLITE_PATH.parent / '.investigation-locks'
            folder.mkdir(exist_ok=True)
            handle = (folder / (digest.hex() + '.lock')).open('a')
            def attempt():
                try:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    return True
                except BlockingIOError:
                    return False
            def check():
                fcntl.fcntl(handle.fileno(), fcntl.F_GETFD)
        while True:
            if should_stop():
                raise DossierDraining('Stopped while waiting for the prior investigation owner')
            if attempt():
                break
            time.sleep(.25)
        token = _OWNER.set((job_id, check))
        yield
    finally:
        if token is not None:
            _OWNER.reset(token)
        if connection is not None:
            connection.close()  # PostgreSQL releases the session advisory lock.
        if handle is not None:
            handle.close()  # Includes process-crash recovery through the OS.
