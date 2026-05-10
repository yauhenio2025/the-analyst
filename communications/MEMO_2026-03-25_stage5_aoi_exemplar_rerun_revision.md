# Memo: Stage 5 AOI Exemplar Diagnostic/Rerun Revision

Date: 2026-03-25

## Summary

The bounded Stage 5 AOI diagnostic step was executed honestly.

Result:

- the repaired selector/provider path now succeeds on the authoritative `evolution_ready` diagnostic case
- the repaired planner-backed compose path also stays on `compose-from-selection` with canonical `source_v2_job_id` preserved
- the frozen four-case rerun was **not** earned
- the blocking seam is now host-side warm snapshot durability / saved-result lookup continuity in `the-critic`, not AOI selector/provider reliability in `analyzer-v2`

So this is a revision result, not a completion result.

## What Was Actually Proven

The authoritative `evolution_ready` spot-check now proves:

- local repaired analyzer code is live
- AOI selector timeout is now `45.0s`
- AOI selector retry policy is now `max_retries = 0`
- the selector/provider path can return a real `aoi_composition_handoff_plan`
- the AOI host surface can retain and present the planner-backed ready state long enough to continue into planner-backed compose
- the live counted path really stays on planner-backed `compose-from-selection`
- canonical `source_v2_job_id` is preserved into the host compose request
- `compose-from-source` stays unused on the counted path

This is materially better than both the failed Stage 5 run from 2026-03-24 and the earlier pre-identity-repair diagnostic stop.

## Why The Frozen Rerun Did Not Happen

The authoritative diagnostic attempt then hit an explicit stop-and-revise condition from the scoped plan:

- planner-backed `compose-from-selection` failed after successful planning

Saved evidence:

- `communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md`
- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_session_2026-03-25.har`
- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json`
- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_state_2026-03-25.png`

The exact failure was:

- `404 Saved AOI result not found: gen-v2-3834f733047a`

That failure happened on the real planner-backed compose route, not on a debug path.

## Revised Diagnosis

The current blocked seam is now:

- host-side AOI warm snapshot persistence -> durable local saved-result row -> compose lookup continuity

The saved diagnostic trail shows:

- planning succeeds
- the browser advances to `/compose-from-intent`
- the compose request is issued on `compose-from-selection`
- the compose request carries both `source_analysis_id` and canonical `source_v2_job_id`
- the compose proxy then fails because the warmed `source_analysis_id` does not exist as a durable local saved result

Local backend evidence confirms the durability mismatch:

- the browser was navigated with `source_analysis_id = gen-v2-3834f733047a`
- that `analysis_id` does **not** exist in local `genealogy_analyses`
- several sibling snapshot ids created in the same warmup window do exist
- backend logs in the same window show repeated `database is locked` save failures
- `_save_v2_presentation_to_db(...)` currently returns the generated `analysis_id` even when the DB write fails

So the next honest repair slice is not another generic selector/provider hardening pass and not another identity-continuity pass.
It is a bounded host snapshot-durability slice.

## Status Decisions

### Stage 5

Stage 5 remains `In progress`.

Reason:

- the diagnostic spot-check succeeded far enough to expose the next real blocker
- but the frozen evaluation pack was not rerun
- therefore the Stage 5 gate still has no final pass/fail rerun decision on the repaired path

### Stage 2

Stage 2 remains open.

Reason:

- Stage 5 did not pass
- there is no rerun completion artifact set
- there is still no basis for a Stage 2 documentary closure claim

### Tranche 3

Tranche 3 remains blocked.

Reason:

- AOI exemplar ratification is still incomplete
- the current failure is still inside the exemplar proof path

## Immediate Next Step

Implement one bounded Stage 5 follow-up slice focused on:

- AOI warm snapshot save durability
- returned `source_analysis_id` truth
- compose lookup continuity when local save fails or SQLite is locked
- preserving the same frozen Stage 5 pack and rubric

Then rerun:

1. the same `evolution_ready` diagnostic spot-check
2. only if it succeeds end-to-end, the same frozen four-case Stage 5 pack

## What Did Not Change

- no roadmap phase pivot
- no rubric changes
- no case changes
- no Stage 2 closure bar changes
- no Tranche 3 promotion

## Implementation Note

No repo-tracked application code changed in this operational pass.

This pass consisted of:

- live diagnostic execution
- repaired-path artifact capture
- backend log / local DB inspection
- diagnosis and revision documentation
