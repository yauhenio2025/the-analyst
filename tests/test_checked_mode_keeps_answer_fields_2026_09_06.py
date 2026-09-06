"""The checked mode's reconciliation renumbers rows and dropped the answer shape's own fields (the run-26 frame,
2026-09-06); code carries them back from the checked rows by lineage, never overwriting a field the final row has."""
from src.executor.process_runner import _carry_answer_fields

CHECKED = """- [S1.F1] What would count — dim: strengthen — kind: primary text — where: Robert Brenner, The Low Countries (2001) — held: no — anchor: "q1" — doc: memo — confidence: high
- [S4.F1] The test — dim: decisive_test — question: q? — sources: Robert Brenner, The Low Countries (2001) — decidable-now: no — rank: 1 — anchor: "q2" — doc: memo — confidence: medium
"""
FINAL = """# Reading

- [F1] What would count — dim: strengthen — anchor: "q1" — doc: memo — from: CHECK.S1.F1 — confidence: high
- [F2] The test — dim: decisive_test — rank: 2 — anchor: "q2" — doc: memo — from: CHECK.S4.F1 — confidence: medium
- [F3] A fresh row with no lineage — dim: residual — anchor: "q3" — doc: memo — confidence: low
"""


def test_missing_fields_come_back_from_the_checked_rows_and_present_ones_are_kept():
    out, carried = _carry_answer_fields(FINAL, CHECKED)
    assert carried == 6
    lines = out.splitlines()
    assert lines[2] == '- [F1] What would count — dim: strengthen — anchor: "q1" — doc: memo — from: CHECK.S1.F1 — kind: primary text — where: Robert Brenner, The Low Countries (2001) — held: no — confidence: high'
    assert "— rank: 2 —" in lines[3] and "— rank: 1" not in lines[3] and "— question: q? — sources: Robert Brenner, The Low Countries (2001) — decidable-now: no" in lines[3]
    assert lines[4] == '- [F3] A fresh row with no lineage — dim: residual — anchor: "q3" — doc: memo — confidence: low'
    assert _carry_answer_fields(FINAL, "") == (FINAL, 0)
