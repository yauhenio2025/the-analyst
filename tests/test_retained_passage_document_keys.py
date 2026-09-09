"""Independent method callers can supply retained evidence IDs as source keys."""
import pytest

from src.executor.ledger_walls import SourceIndex, parse_rows, verify_rows


@pytest.mark.parametrize('key', ['reporter:src_original/F15', 'em:GEFERFPB/E1.F1'])
@pytest.mark.parametrize('brackets', [False, True])
def test_retained_passage_key_binds_to_its_exact_source(key, brackets):
    quote = 'Political access alone does not establish the cause of returns.'
    declaration = f'[{key}]' if brackets else key
    row = parse_rows(f'- [F1] Claim — anchor: "{quote}" — doc: {declaration}')[0]
    assert row.doc == key and not row.anchor_parse_error
    assert verify_rows([row], SourceIndex({key: quote})).verified == 1
    wrong = parse_rows(f'- [F1] Claim — anchor: "{quote}" — doc: {declaration}')[0]
    assert verify_rows([wrong], SourceIndex({key: 'A different statement.', 'other': quote})).verified == 0
