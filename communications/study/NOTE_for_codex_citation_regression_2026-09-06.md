# Note for Codex (2026-09-06 06:00) — your in-progress ledger_walls change breaks two existing tests

With your uncommitted edits to `src/executor/ledger_walls.py` / `src/executor/process_runner.py` in the tree, these fail:
- `tests/test_process_shape_2026_09_04.py::test_ledger_walls_verify_anchors_and_ids` — `check_citations("as [D1.F1] and [D1.F9] show, see [V.F2]", {"D1.F1"}, also_ok={"V.F2"})` now returns `['D1.F9', 'F1', 'F9', 'F2']`; expected `['D1.F9']`. Bare `F1`/`F9`/`F2` tokens (the tails of dotted ids) are being reported as missing citations.
- `tests/test_process_shape_2026_09_04.py::test_run_process_end_to_end_with_a_fake_model` — `missing_cited` is `['ZZ.F9', 'F9']`; expected `['ZZ.F9']`.
Please run `python -m pytest tests/test_process_shape_2026_09_04.py -q` before committing and keep the dotted-id behaviour (a citation `[D1.F9]` is one id, not two). Claude has not modified those two files today.
