"""Offline propagation regressions: semantic repair is the model's job; walls check bytes/IDs."""
import json
from types import SimpleNamespace

import pytest

from src.executor.ledger_walls import SourceIndex, parse_rows, verify_rows
from src.executor.process_runner import apply_rulings, run_oneshot_checked
from src.operationalizations.schemas import ProcessDimension, ProcessSpec, ProcessStep

SOURCE = 'The committee also transferred money. The pilot may succeed under supervision.'
CAP = SimpleNamespace(engine_key='repair', engine_name='Repair', problematique='Read the claims.')


def row(rid, finding, quote, extra=''):
    return f'- [{rid}] {finding} — dim: claims — anchor: {json.dumps(quote)}{extra}'


def spec(tables=True):
    return ProcessSpec(dimensions=[ProcessDimension(key='claims', name='Claims')], steps=[
        ProcessStep(key='verify', kind='verify', model_tier='mid'),
        ProcessStep(key='synthesize', kind='synthesize', is_final=True,
                    tables=['claims'] if tables else [])])


def test_confirmed_reanchor_replaces_a_verbatim_but_incomplete_prefix():
    rows = parse_rows(row('F1', 'The committee transferred money.', 'The committee also'))
    rulings = parse_rows(row('F1', 'The committee transferred money.', 'The committee also transferred money.', ' — status: confirmed'))
    index = SourceIndex({'doc': SOURCE})
    verify_rows(rows, index)
    kept, _, _, _ = apply_rulings(rows, rulings, index)
    assert kept[0].anchor == 'The committee also transferred money.'
    assert parse_rows(kept[0].render())[0].anchor == kept[0].anchor


@pytest.mark.parametrize('tables', [True, False])
def test_single_document_tables_receive_applied_rulings_and_prose_stays_two_calls(tables):
    read = ('| Claim |\n|---|\n| Success is certain [F1] |\n| Money vanished [F2] |\n\n'
            '## Findings ledger\n' + row('F1', 'Success is certain.', 'The pilot may succeed under supervision.') + '\n'
            + row('F2', 'Money vanished.', 'The committee also transferred money.'))
    critic = ('## Findings ledger\n' + row('F1', 'Success is conditional.', 'The pilot may succeed under supervision.',
              ' — status: weakened — revised-finding: "Success is conditional."') + '\n'
              + row('F2', 'Money vanished.', 'The committee also transferred money.', ' — status: rejected'))
    final = '| Claim |\n|---|\n| Success is conditional [F1] |\n\n## Findings ledger\n' + row(
        'F1', 'Success is conditional.', 'The pilot may succeed under supervision.', ' — from: CHECK.F1')
    replies = iter([read, critic, final]); calls = []
    def fake(system, user, **kwargs):
        calls.append((system, user))
        return {'content': next(replies), 'model_used': kwargs['model_hint']}
    result = run_oneshot_checked(CAP, spec(tables), {'doc': SOURCE}, call_fn=fake)
    assert len(calls) == (3 if tables else 2)
    if tables:
        assert 'Success is conditional.' in calls[2][1]
        assert 'CHECK.F1' in calls[2][1] and 'status: rejected' in calls[2][1]
        assert 'Money vanished' not in result.final_content
        assert 'Success is certain' not in result.final_content
        assert result.calls[-1].step_key == 'reconcile_checked'
        assert result.final_wall['failed_ids'] == []
    else:
        assert '[F2, rejected by the check]' in result.final_content


def test_single_document_table_with_unverified_final_anchor_gets_bounded_repair():
    read = 'A claim [F1].\n\n## Findings ledger\n' + row('F1', 'Transfer.', 'The committee also transferred money.')
    critic = read.replace('money."', 'money." — status: confirmed')
    bad = '| Claim |\n|---|\n| Invented [F1] |\n\n## Findings ledger\n' + row('F1', 'Invented.', 'This string is absent.')
    replies = iter([read, critic, bad, bad]); calls = []
    def fake(system, user, **kwargs):
        calls.append(user)
        return {'content': next(replies), 'model_used': kwargs['model_hint']}
    with pytest.raises(RuntimeError, match='failed after bounded repair'):
        run_oneshot_checked(CAP, spec(), {'doc': SOURCE}, call_fn=fake)
    assert len(calls) == 4 and 'CODE WALL FAILURES' in calls[-1]
    assert 'Only one document is supplied' in calls[-1]
    assert 'Corpus descendants need anchors from two distinct document keys' not in calls[-1]
