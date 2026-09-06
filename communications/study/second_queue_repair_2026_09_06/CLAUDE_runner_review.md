# Claude runner review

## Claude Review: Second-Queue Repair — 2026-09-06

### Summary

The diff is mechanically sound for its stated purpose. I found two concrete correctness issues and several minor observations.

---

### Concrete Bugs

**Bug 1 — `spec.final_step.tables` access when `spec.final_step` is None**
`process_runner.py`, line 749:
```python
reconcile_tables = bool(corpus_dimensions or (spec.final_step and spec.final_step.tables))
```
The guard `spec.final_step and ...` correctly handles a None `final_step`. However, `spec.final_step.tables` can also be an empty list `[]`, which is falsy and correctly returns `False`. And `spec.final_step.tables` being a non-empty list is truthy. This is correct as written.

**No bug here — this line is correct.**

**Bug 2 — `_check_corpus_synthesis` called unconditionally in the `reconcile_tables` branch even for single-document specs**
`process_runner.py`, approximately line 848:
```python
synthesis = _check_corpus_synthesis(synthesis, sprompt, spec, index, final_corpus_ids, call_fn, strong, ...)
```
`_check_corpus_synthesis` checks `corpus_dimensions` internally (via `spec.dimensions`), but the contract check inside it calls `verify_rows` with `corpus_dimensions` from `spec` — which for a single-document spec with `final_step.tables` set will be an empty set. This is harmless for single-document runs because `corpus_dimensions` will be empty and `final_corpus_ids` will be empty. The synthesis contract check will still run and enforce `failed_ids`, `duplicate_ids`, etc.

**Observed issue**: for a single-document spec triggering `reconcile_tables` solely through `spec.final_step.tables`, `_check_corpus_synthesis` will still call `repair.user += ... "Corpus descendants need anchors from two distinct document keys..."` on failure. That repair instruction is incorrect for a single-document context and may confuse the model during repair. This is a **prompt correctness defect** for the repair path: the repair instruction text is corpus-specific but will be sent to a single-document reconcile call when anchors fail.

File: `process_runner.py`, inside `_check_corpus_synthesis`, the repair user message includes:
```
"Corpus descendants need anchors from two distinct document keys."
```
This will be sent during a single-document table repair. It is factually wrong for that context.

**Bug 3 — `apply_rulings` confirmed branch: unconditional anchor copy overwrites a verified anchor with an unverified critic anchor**
`process_runner.py`, line 659 (after the diff):
```python
if v.anchor_verified:   # retain a critic's fuller support even when the old fragment matched
    r.copy_anchors_from(v)
    r.text = v.text
```
Previously the condition was `v.anchor_verified and not r.anchor_verified`, which only replaced when the original lacked verification. Now it replaces unconditionally when the critic's version is verified. If the original row `r` already had `anchor_verified=True` with a different (also valid) anchor, the critic's anchor silently overwrites it. This is the intended behavior per the comment ("retain a critic's fuller support"), and the test `test_confirmed_reanchor_replaces_a_verbatim_but_incomplete_prefix` confirms the case.

**No bug here — the logic is intentional and tested.** The test correctly covers this path.

---

### Test Coverage Observations

**`test_single_document_table_with_unverified_final_anchor_gets_bounded_repair`**: The test asserts `len(calls) == 4` and `'CODE WALL FAILURES' in calls[-1]`. The `replies` iterator yields `bad` twice (calls 3 and 4), but after two repair attempts `_check_corpus_synthesis` raises `RuntimeError`. The `pytest.raises` catches this. The `calls` list will have 4 entries. This is correct.

**`test_single_document_tables_receive_applied_rulings_and_prose_stays_two_calls`** with `tables=False`: The test asserts `len(calls) == 2`. When `tables=False`, `spec.final_step.tables = []`, so `reconcile_tables = False` and the third reply is never consumed. However, `replies` is constructed with 3 elements. The unused third element causes no error (iterator is simply not exhausted). **No bug**, but the iterator has a spare element for the `tables=False` arm.

**`spec.final_step` in the test fixture**: The `spec()` function's `ProcessStep` for synthesize has `is_final=True` and `tables=['claims'] if tables else []`. If `tables=False`, `spec.final_step.tables` is `[]` (falsy), so `reconcile_tables` is False. This is consistent with the tests in `test_anchor_repairs_2026_09_05.py` which set `spec.final_step.tables = []` explicitly on real specs.

---

### Hash File

The `production_prompt_hashes_3426419.json` replacement is a full 68-entry refresh. The test `test_68_production_prompts_match_declared_law_baseline` validates that the running code matches these hashes. The rename from `test_68_production_prompts_are_unchanged` to `test_68_production_prompts_match_declared_law_baseline` is accurate — the baseline is now the post-change law text, not a stability assertion. **Correct.**

---

### process_composer.py Changes

The `ANCHORING_LAW` addition and `DUTY_TEXT["check_anchors_in_context"]` addition are pure prompt text. Both instruct on fuller anchors and predicate coverage. Neither adds conditional logic. The grammar is consistent with the surrounding text (the joining at `"A finding you cannot "` is a continuation within the paragraph, matching the original flow). **No structural issue.**

---

### Verdict

**Approve with one action item:**

- **Action required**: In `_check_corpus_synthesis`, gate the corpus-specific repair instruction on `corpus_dimension_keys` being non-empty, so a single-document table repair does not receive instruction to supply two distinct document keys. This is the only confirmed correctness defect introduced by the extension of `reconcile_tables` to single-document specs.
