"""Large durable JSON checkpoints must not become huge PostgreSQL bytea literals."""
import gzip
import hashlib
import json

import pytest

from src.dossier import blob_store
from src.executor import db


@pytest.fixture
def blobs(monkeypatch, tmp_path):
    monkeypatch.setattr(db, 'DATABASE_URL', '')
    monkeypatch.setattr(db, 'SQLITE_PATH', tmp_path / 'blobs.sqlite')
    monkeypatch.setattr(blob_store, '_ready', False)
    blob_store.ensure_table()
    class Rows:
        def __getitem__(self, key):
            return db.execute('SELECT mime,size,data FROM dossier_blobs WHERE blob_key=%s', (key,), fetch='one')

        def __setitem__(self, key, row):
            db.execute('INSERT INTO dossier_blobs(blob_key,mime,size,data) VALUES(%s,%s,%s,%s)',
                       (key, row['mime'], len(row['data']), row['data']))
    return Rows()


def test_large_json_is_compressed_before_database_adaptation_and_restored_exactly(blobs):
    data = json.dumps({'evidence': [{'quote': 'Capitalist and preindustrial contexts.\n', 'source_role': 'primary'}] * 12000}, ensure_ascii=False).encode()
    blob_store.put_blob('investigation:test', 'application/json', data)
    stored = blobs['investigation:test']
    assert stored['data'].startswith(blob_store._JSON_GZIP_PREFIX)
    assert stored['size'] == len(stored['data']) < len(data) // 4
    mime, restored = blob_store.get_blob('investigation:test')
    assert mime == 'application/json'
    assert restored == data
    assert hashlib.sha256(restored).digest() == hashlib.sha256(data).digest()


def test_legacy_json_and_binary_blobs_still_round_trip(blobs):
    for key, mime, data in [('legacy', 'application/json', b'{"saved":"before compression"}'),
                             ('image', 'image/png', b'\x89PNG' + b'x' * 600000),
                             ('existing-gzip', 'application/octet-stream', gzip.compress(b'raw gzip asset'))]:
        # Insert the pre-chunking physical format directly to test old records.
        blobs[key] = {'mime': mime, 'data': data}
        assert blobs[key]['data'] == data
        assert blob_store.get_blob(key) == (mime, data)
    assert blob_store.get_blob('missing') is None


def test_existing_compressed_memoryview_and_file_restore_keep_original_bytes(blobs, tmp_path):
    raw = b'{"quote":"preserved whitespace\\n"}'
    blobs['legacy-compressed'] = {'mime': 'application/json',
                                  'data': memoryview(blob_store._JSON_GZIP_PREFIX + gzip.compress(raw))}
    assert blob_store.decode_blob_data('application/json', memoryview(blobs['legacy-compressed']['data'])) == raw
    assert blob_store.get_blob('legacy-compressed') == ('application/json', raw)
    target = tmp_path / 'restored.json'
    assert blob_store.ensure_file(target, 'legacy-compressed')
    assert target.read_bytes() == raw


def test_damaged_compressed_data_is_reported_instead_of_returned_as_research(blobs):
    blobs['damaged'] = {'mime': 'application/json', 'data': blob_store._JSON_GZIP_PREFIX + b'broken'}
    with pytest.raises((OSError, EOFError)):
        blob_store.get_blob('damaged')
