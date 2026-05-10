# Memo: Phase 0 AOI Active-Discovery Repair Completion

Date: 2026-03-27
Status: Repair landed; fresh rerun reached a new bounded Phase 3.0 stop
Program: Dynamic Bespoke Apps Platformization
Supersedes: N/A (this is the repair completion, not the follow-on prompt-budget scope)
Depends on:
- `communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_execution_memo.md`
- `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_revision_after_active_discovery_repair.md`
- `communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_launch_2026-03-27.json`
- `communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_active_boundary_2026-03-27.json`
- `communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_terminal_failure_2026-03-27.json`

## Summary

The bounded analyzer-side active-discovery repair is now landed.

What is now true:

- thinker-scoped live discovery on fresh by-ref AOI launches now works again
- the fresh Phase 0 Otto rerun `job-226f65f43a3b` passed the required active-boundary proof on the real `the-critic` route
- the full affected analyzer test files now pass:
  - `tests/test_run_contract.py`
  - `tests/test_analysis_product_contract.py`

What is also now true:

- Phase 0 still cannot close honestly
- the fresh rerun failed before any durable completed AOI result existed
- the real next blocker is analyzer execution at Phase `3.0 / aoi_sin_findings / Finding Discovery`
- the exact blocker is prompt-budget overflow:
  - `prompt is too long: 1037154 tokens > 1000000 maximum`

So this repair completion closes the discovery seam, but it does not close Phase 0.

## What Landed

### 1. By-ref thinker extraction now reaches discovery correctly

Analyzer discovery normalization now unwraps `by_ref_request_snapshot` before selected-source thinker extraction.

That landed in:

- `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py`

Effect:

- thinker-filtered active discovery no longer drops fresh by-ref AOI jobs during the running window
- the same normalized plan-data path now handles both:
  - `_type = request_snapshot`
  - `_type = by_ref_request_snapshot`

### 2. Focused discovery regressions now cover the repaired seam

The repair is covered at both the run-discovery and result-discovery layers.

Files changed:

- `/home/evgeny/projects/analyzer-v2/tests/test_run_contract.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py`

The new regressions prove:

- active run discovery can filter a fresh by-ref AOI job by `selected_source_thinker_id`
- discovery summaries extract thinker identity from `by_ref_request_snapshot`
- two by-ref jobs with different selected thinkers remain distinguishable

### 3. The fresh rerun proves the seam moved upstream

The fresh Phase 0 attempt used the fixed Otto target and the real Critic launch route.

Fresh run:

- job id: `job-226f65f43a3b`
- plan id: `plan-54b6f075fdf2`
- workflow: `anxiety_of_influence_thematic_single_thinker`

What the rerun proved:

- launch succeeded
- thinker-scoped active discovery hit the fresh job while it was running
- the fresh run then failed upstream before completion

Important documentary nuance:

- when quoting the terminal seam, use `failure_excerpt.phase = 3.0` and `progress.phase_statuses["3.0"] = "failed"`
- do not use `progress.current_phase = 4.0` as the seam locator, because the failure artifact preserves a downstream progress alias while the actual terminal cause is still Phase `3.0 / aoi_sin_findings`

## Verification

Run result:

- `PYTHONPATH=. pytest -q tests/test_run_contract.py tests/test_analysis_product_contract.py`
  - `84 passed`

Proof artifacts:

- `communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_launch_2026-03-27.json`
- `communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_active_boundary_2026-03-27.json`
- `communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_terminal_failure_2026-03-27.json`

## Status Implications

- thinker-scoped live discovery is no longer the main Phase 0 blocker
- no honest completed-boundary proof exists yet for the fresh March 27 rerun
- no truthful planner-primary browser proof exists yet for that rerun
- no Stage 2 closure decision can be written yet
- Phase 0 remains open only because the analyzer still overruns the prompt budget at Phase `3.0`

## Next Honest Step

The next step is not another discovery repair and not another host/browser continuity pass.

The next step is one bounded analyzer-side prompt-budget repair for Phase `3.0 / aoi_sin_findings` on the same fixed Otto corpus and task.

After that repair:

1. rerun Phase 0 fresh
2. require the same active-boundary proof again
3. continue to completed-boundary proof, counted browser proof, and the explicit Stage 2 decision only if the rerun actually completes
