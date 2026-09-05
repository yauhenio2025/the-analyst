"""The bare directive is discarded only when it cannot be a semantic replacement."""
import importlib.util
import json
from pathlib import Path

import pytest

from src.executor import ledger_walls as lw

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('rewrite_recovery',ROOT/'scripts/recover_ideas_hegel_rewrite_2026_09_05.py')
repair=importlib.util.module_from_spec(spec);spec.loader.exec_module(repair)


def rows():
    head='The same original finding.'
    primary='A sufficiently long exact primary quotation.'
    prefix=f'- [F16] {head} — dim: incompatibilities — anchor: {json.dumps(primary)} — anchor-b: '
    original=prefix+json.dumps('A different original secondary quotation.')+' — confidence: medium\n'
    critic=prefix+json.dumps(repair.CORRECTED_ANCHOR)+' — status: weakened — reason: correction'+repair.TERMINAL_FIELD+'\n'
    return original,critic


def test_removes_only_exact_terminal_directive_and_preserves_head_and_explicit_correction():
    original,critic=rows()
    clean,evidence=repair.strip_exact_terminal_field(original,critic,lw)
    assert clean==critic.replace(repair.TERMINAL_FIELD,'')
    parsed=lw.parse_rows(clean)[0]
    assert parsed.finding==lw.parse_rows(original)[0].finding
    assert not parsed.revised_finding and parsed.extra_anchors[0].quote==repair.CORRECTED_ANCHOR
    assert evidence['raw_field']==repair.TERMINAL_FIELD
    assert evidence['field_sha256']==repair.sha(repair.TERMINAL_FIELD.encode())
    assert 'same finding, anchor' not in parsed.finding


@pytest.mark.parametrize('change',[
    lambda s:s.replace('The same original finding.','A changed substantive finding.'),
    lambda s:s.replace('status: weakened','status: confirmed'),
    lambda s:s.replace('anchor‑b corrected','anchor-b corrected'),
    lambda s:s.rstrip()+' — confidence: high\n',
    lambda s:s.replace('same finding, anchor‑b corrected','"A substantive replacement finding."'),
    lambda s:s+s,
    lambda s:s.replace(repair.CORRECTED_ANCHOR,'A different proposed secondary quotation.'),
])
def test_refuses_changed_head_status_literal_position_duplicate_or_correction(change):
    original,critic=rows()
    with pytest.raises(RuntimeError):repair.strip_exact_terminal_field(original,change(critic),lw)


def test_retained_invalid_row_is_not_repaired_by_the_target_transform():
    original,critic=rows()
    original+='- [F1] Another finding — anchor: "A valid enough original source quotation."\n'
    critic+='- [F1] Another finding — anchor: "A valid enough original source quotation." — status: weakened — revised-finding: invalid bare prose\n'
    with pytest.raises(ValueError,match='quoted string'):
        repair.strip_exact_terminal_field(original,critic,lw)
