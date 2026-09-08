"""Large durable JSON checkpoints must not become huge PostgreSQL bytea literals."""
import gzip
import hashlib
import json

import pytest

from src.dossier import blob_store


@pytest.fixture
def blobs(monkeypatch):
    rows = {}
    monkeypatch.setattr(blob_store, 'ensure_table', lambda: None)
    monkeypatch.setattr(blob_store, '_bin', lambda data: data)
    def execute(sql, params=(), fetch='none'):
        if sql.startswith('INSERT'):
            key, mime, size, data, created = params
            rows[key] = {'mime': mime, 'size': size, 'data': data}
        elif sql.startswith('SELECT'):
            return rows.get(params[0])
        else:
            pytest.fail('unexpected storage query')
    monkeypatch.setattr(blob_store, 'execute', execute)
    return rows


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
        blob_store.put_blob(key, mime, data)
        assert blobs[key]['data'] == data
        assert blob_store.get_blob(key) == (mime, data)
    assert blob_store.get_blob('missing') is None


def test_existing_compressed_memoryview_and_file_restore_keep_original_bytes(blobs, tmp_path):
    raw = b'{"quote":"preserved whitespace\\n"}'
    blobs['legacy-compressed'] = {'mime': 'application/json',
                                  'data': memoryview(blob_store._JSON_GZIP_PREFIX + gzip.compress(raw))}
    assert blob_store.get_blob('legacy-compressed') == ('application/json', raw)
    target = tmp_path / 'restored.json'
    assert blob_store.ensure_file(target, 'legacy-compressed')
    assert target.read_bytes() == raw


def test_damaged_compressed_data_is_reported_instead_of_returned_as_research(blobs):
    blobs['damaged'] = {'mime': 'application/json', 'data': blob_store._JSON_GZIP_PREFIX + b'broken'}
    with pytest.raises((OSError, EOFError)):
        blob_store.get_blob('damaged')
