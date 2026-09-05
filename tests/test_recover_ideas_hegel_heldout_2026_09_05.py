"""Pure parsing guards plus optional zero-network replay of the local saved study."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

from src.executor import ledger_walls as lw
from src.executor.process_runner import apply_rulings

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location('hegel_recovery', ROOT / 'scripts/recover_ideas_hegel_heldout_2026_09_05.py')
recovery = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(recovery)
QUOTE = 'A sufficiently long source quotation supporting the finding.'


def line(rid, status='', duplicate=False):
    text = f'- [{rid}] A finding — anchor: {json.dumps(QUOTE)}'
    if duplicate:
        text += ' — anchor: ' + json.dumps(QUOTE)
    return text + (f' — status: {status}' if status else '') + '\n'


def test_remove_only_unapplied_unknown_row_blocks_and_preserve_all_other_bytes():
    ignored = line('I4', duplicate=True) + '  A continuation in the same row block.\n\n'
    before = '## Findings ledger\n' + line('F1', 'confirmed')
    after = '### Misses\n' + line('V.F1', 'added') + '### Must keep\n- [I4]: an auxiliary reference\n'
    raw = before + ignored + after
    clean, removed = recovery.prune_unapplied_rows(raw, {'F1'}, lw)
    assert clean == before + after
    assert [r['id'] for r in removed] == ['I4']
    assert removed[0]['raw_block'] == ignored
    assert removed[0]['block_sha256'] == recovery.sha(ignored.encode())
    assert [r.id for r in lw.parse_rows(clean)] == ['F1', 'V.F1']


@pytest.mark.parametrize('rid,status', [('F1', 'confirmed'), ('F1', ''), ('V.F1', 'added')])
def test_repeated_anchor_in_original_or_addition_still_fails(rid, status):
    raw = '## Findings ledger\n' + line(rid, status, duplicate=True)
    clean, removed = recovery.prune_unapplied_rows(raw, {'F1'}, lw)
    assert clean == raw and removed == []
    with pytest.raises(ValueError, match='repeated anchor'):
        lw.parse_rows(clean)


def test_renamed_ids_are_not_matched_and_originals_remain_carried():
    originals = lw.parse_rows(line('F1') + line('F2'))
    raw = line('D1.F1', 'confirmed') + line('D1.F2', 'weakened') + line('V.F1', 'added')
    clean, removed = recovery.prune_unapplied_rows(raw, {'F1', 'F2'}, lw)
    kept, _, _, report = apply_rulings(originals, lw.parse_rows(clean), lw.SourceIndex({'doc': QUOTE}))
    assert [r['id'] for r in removed] == ['D1.F1', 'D1.F2']
    assert report['carried'] == 2 and report['confirmed'] == report['weakened'] == 0
    assert report['added'] == 1 and {r.id for r in kept}.issuperset({'F1', 'F2'})


def test_duplicate_unknown_ids_are_preserved_for_existing_uniqueness_failure():
    raw = line('I4') + line('I4')
    clean, removed = recovery.prune_unapplied_rows(raw, {'F1'}, lw)
    assert clean == raw and removed == []
    with pytest.raises(RuntimeError, match='duplicate|Duplicate'):
        apply_rulings(lw.parse_rows(line('F1')), lw.parse_rows(clean), lw.SourceIndex({'doc': QUOTE}))


def test_ambiguous_status_is_preserved_including_any_possible_addition():
    raw = line('V.F1', 'confirmed').rstrip() + ' — status: added\n'
    clean, removed = recovery.prune_unapplied_rows(raw, {'F1'}, lw)
    assert clean == raw and removed == []


def test_auxiliary_references_do_not_create_false_duplicates_and_explicit_ledger_resumes():
    raw = line('I4') + '### Must keep\n' + line('I4') + '## Findings ledger\n' + line('V.F1', 'added')
    clean, removed = recovery.prune_unapplied_rows(raw, {'F1'}, lw)
    assert [r['id'] for r in removed] == ['I4']
    assert clean == '### Must keep\n' + line('I4') + '## Findings ledger\n' + line('V.F1', 'added')


def test_local_proposal_reproduces_failure_and_all_five_completed_outputs_without_network():
    run = ROOT / 'data/study/ideas_hegel_heldout_2026_09_05' / recovery.IDENTITY[:16]
    if not (run / 'results.json').is_file():
        pytest.skip('Local ignored study artifacts are unavailable')
    records = json.loads((run / 'results.json').read_text())
    if records.get(recovery.TARGET, {}).get('status') != 'failed':
        pytest.skip('Original failure has already been adopted or is unavailable')
    command = [sys.executable, str(ROOT / 'scripts/recover_ideas_hegel_heldout_2026_09_05.py')]
    # CLI installs a network-denying audit hook and can only replay saved calls.
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=True)
    result = json.loads(completed.stdout)
    assert result['all_byte_identical'] and result['compared_completed_finals'] == 5
    assert result['ignored_target_ids'] == ['I1', 'I3', 'I4']
    assert result['new_paid_calls'] == 0 and result['bundle'] is None
