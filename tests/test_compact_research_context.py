"""Research packet serialization retains exact JSON values and honest sizing."""
import copy


def test_compact_context_preserves_every_value_and_matches_input_accounting():
    import json
    from src.dossier.engine_call import _context_block
    from src.dossier.context_packing import input_chars
    packet = {'evidence': [{'citation_id': f'source/F{i}', 'quote': 'He said "state loans".\nA qualification.',
                           'speaker': 'Journalist narration', 'date': None} for i in range(500)]}
    before = copy.deepcopy(packet)
    block = _context_block(packet, [], 'field_investigation_memo')
    serialized = block.split('\n', 1)[1]
    assert json.loads(serialized) == before and packet == before
    assert input_chars([], packet) == len(serialized)
    assert len(serialized) < len(json.dumps(packet, ensure_ascii=False))
