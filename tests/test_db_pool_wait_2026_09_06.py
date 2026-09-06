"""The Postgres pool waits for a connection instead of failing the instant it is empty (live dossier job
dossier-8577d8159b38 failed with PoolError: connection pool exhausted under a deep process run, 2026-09-06)."""
import pytest


def test_getconn_waits_then_returns(monkeypatch):
    from psycopg2.pool import PoolError
    from src.executor import db
    attempts = []
    class FakePool:
        def getconn(self):
            attempts.append(1)
            if len(attempts) < 3:
                raise PoolError("connection pool exhausted")
            return "conn"
    assert db._getconn_waiting(FakePool(), wait_seconds=5) == "conn" and len(attempts) == 3


def test_getconn_gives_up_after_the_wait():
    from psycopg2.pool import PoolError
    from src.executor import db
    class Empty:
        def getconn(self):
            raise PoolError("connection pool exhausted")
    with pytest.raises(PoolError):
        db._getconn_waiting(Empty(), wait_seconds=0.2)


def test_pool_size_default_is_generous():
    from src.executor import db
    assert db.POOL_MAX >= 20
