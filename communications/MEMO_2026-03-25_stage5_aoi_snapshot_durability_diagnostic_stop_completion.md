# Memo: Stage 5 AOI Snapshot Durability Diagnostic Stop Completion

Date: 2026-03-25

## Summary

This operational pass is complete.

What was done:

- executed one fresh live `evolution_ready` diagnostic on the repaired local planner-backed AOI path
- captured the required HAR / JSON / screenshot artifacts
- applied the scoped branch rule honestly
- stopped before the frozen four-case rerun when a new downstream host-side blocker appeared

## What This Pass Proved

This pass closed the open question left by the AOI identity-continuity repair slice:

- whether the repaired planner-backed AOI path could now survive selector/provider planning and identity validation strongly enough to reach real planner-backed compose

Answer:

- yes, but not yet strongly enough to earn the frozen rerun

The authoritative diagnostic attempt proved:

- `route-task` succeeds
- `plan-task` succeeds
- the selector trace shows `timeout_s = 45`
- the selector trace shows `max_retries = 0`
- `provider_outcome = success`
- the AOI host surface stays on planner-backed `compose-from-selection`
- canonical `source_v2_job_id` is preserved into the host compose request
- `compose-from-source` stays unused on the counted path
- the earlier `409 source_analysis_id does not belong to the current project + thinker context` blocker is no longer the active failure

## Why This Pass Still Ends In Revision

The same authoritative attempt then hit a real downstream stop condition:

- planner-backed `compose-from-selection` failed after successful planning and successful identity continuity

The concrete failure was:

- `404 Saved AOI result not found: gen-v2-3834f733047a`

Local evidence makes the new blocker narrower and more concrete:

- the browser was handed `source_analysis_id = gen-v2-3834f733047a`
- that id was not durably present in local `genealogy_analyses`
- sibling warmed snapshot ids created in the same window were present
- backend logs in the same window recorded repeated `database is locked` save failures
- `_save_v2_presentation_to_db(...)` currently returns the generated `analysis_id` even when the local DB write fails

So the frozen rerun was not honestly earned.

## Evidence

Primary artifacts:

- `communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md`
- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_session_2026-03-25.har`
- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json`
- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_state_2026-03-25.png`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_revision.md`

This artifact set supersedes the earlier `409`-hitting diagnostic artifacts under the same filenames.
The earlier failure remains preserved in:

- the diagnosis memo trail
- the rerun revision memo trail
- git history

## Program Meaning

The important program update is:

- the Stage 5 blocker is no longer selector/provider reliability
- the Stage 5 blocker is no longer AOI thinker/source identity continuity
- the current blocker is host-side warm snapshot durability and returned `source_analysis_id` truth

That is real progress, but it is still progress inside one open exemplar gate.

This pass should **not** be misread as:

- Stage 5 completion
- Stage 2 closure
- evidence that Tranche 3 should begin
- evidence that the broader platform is close to finished

It is better read as:

- another proof-surface blocker retired
- one more bounded host continuity seam isolated
- the AOI exemplar loop still not ratified end to end

## Status Decisions

### Stage 5

Stage 5 remains `In progress`.

Reason:

- the repaired diagnostic path got further
- but the frozen rerun still was not consumed

### Stage 2

Stage 2 remains open.

Reason:

- there is still no successful frozen Stage 5 rerun completion artifact set
- there is still no basis for documentary closure

### Tranche 3

Tranche 3 remains blocked.

Reason:

- the AOI exemplar is still not ratified as an end-to-end platform reference

## Immediate Next Step

The next honest move is one bounded host-side repair slice already scoped in:

- `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md`

That slice should:

- make warm snapshot persistence fail closed
- ensure a `source_analysis_id` is returned only if it is durably queryable
- preserve the same repaired planner-backed path
- rerun the same `evolution_ready` diagnostic before any frozen four-case rerun is attempted again

## Completion Note

No repo-tracked application code changed in this operational pass.

This was:

- live proof execution
- artifact capture
- local backend log / DB inspection
- diagnosis
- roadmap / memo trail maintenance
