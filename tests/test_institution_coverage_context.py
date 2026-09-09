from src.dossier.reporter_context import pack_reporter_context


def test_many_candidate_coverage_rows_roundtrip_without_erasing_exceptions():
    rows = [{'hostname': f'institute-{i}.example', 'name': f'Institute {i}',
             'considered': True, 'selected_for_search': False, 'sources_found': 0,
             'bodies_acquired': 0, 'absence_claim_supported': False,
             'search_outcome': {'queries_attempted': 0, 'queries_answered': 0}}
            for i in range(244)]
    rows[0].update(selected_for_search=True, sources_found=22, bodies_acquired=10,
                   search_outcome={'queries_attempted': 3, 'queries_answered': 3})
    rows[1]['classification_note'] = None  # Missing elsewhere must remain missing.
    packet = {'field_collections': [{'kind': 'reporter', 'institutional_context': {'coverage': rows}}]}
    _, packed, receipt = pack_reporter_context('memo', [], packet, packet_sha256='frozen')
    table = packed['field_collections'][0]['institutional_context']['coverage']
    assert [{**table['defaults'], **row} for row in table['rows']] == rows
    assert packet['field_collections'][0]['institutional_context']['coverage'] == rows
    assert receipt['packed_chars'] < receipt['original_chars'] * .5
    assert receipt['omitted_metadata'][0]['value'] == rows
    _, planning, _ = pack_reporter_context('plan', [], packet, packet_sha256='frozen')
    assert planning['field_collections'][0]['institutional_context']['coverage'] == rows
