"""Generic summaries must not erase typed rows or bypass original support checks."""
import copy
import pytest
from src.dossier.field_investigation import validate_claims
from src.dossier.investigation import recover_answer_rows


def fixture():
    result = {'rows': [], 'final_output': '''## Debate ledger
[E1.F1] Power is contested — dim: debate — claim_kind: field_finding — evidence_ids: source/F1 — anchor: "worker power" — doc: original — confidence: high
## Findings ledger
[F1] Worker power matters — dim: debate — evidence_ids: source/F1 — anchor: "worker power" — confidence: high
'''}
    return recover_answer_rows(result), [{'citation_id': 'source/F1', 'quote_verified': True, 'source_role': 'field'}]


def test_complete_paid_output_keeps_both_ledgers_and_validates_field_summary_support():
    rows, evidence = fixture()
    original = copy.deepcopy(rows)
    result = validate_claims(rows, evidence, required=True, field_map=True)
    assert result['supported'] and result['claim_count'] == 1
    assert result['unclassified_field_summaries'][0]['classification'] == 'unclassified_field_summary'
    assert rows == original and len(rows) == 2
    assert not validate_claims(rows, evidence, required=True)['supported']


@pytest.mark.parametrize('invalid', ['missing', 'unverified', 'primary', 'no_typed', 'invalid_typed', 'typed_missing'])
def test_summary_never_bypasses_original_evidence_or_required_typed_ledger(invalid):
    rows, evidence = fixture()
    if invalid == 'missing': rows[-1]['fields']['evidence_ids'] = 'source/F99'
    elif invalid == 'unverified': evidence[0]['quote_verified'] = False
    elif invalid == 'primary': evidence[0]['source_role'] = 'primary'
    elif invalid == 'no_typed': rows = rows[1:]
    elif invalid == 'invalid_typed': rows[0]['fields']['claim_kind'] = 'thinker_position'
    else: rows[0]['fields']['evidence_ids'] = 'source/F99'
    assert not validate_claims(rows, evidence, required=True, field_map=True)['supported']
