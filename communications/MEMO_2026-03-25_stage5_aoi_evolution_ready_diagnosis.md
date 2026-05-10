# Memo: Stage 5 `evolution_ready` Diagnostic Note

Date: 2026-03-25

## Purpose

Record the fresh post-identity-repair `evolution_ready` diagnostic spot-check required by the Stage 5 AOI exemplar diagnostic/rerun plan, and decide whether the frozen four-case rerun was honestly earned.

## Supersession Note

This note supersedes the earlier `409`-hitting diagnostic artifact set that previously lived at the same HAR / JSON / PNG paths.

The earlier diagnostic outcome remains preserved in:

- `communications/MEMO_2026-03-25_stage5_aoi_diagnostic_stop_completion.md`
- `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_scope.md`

Repo baseline for this post-identity-repair diagnostic:

- `analyzer-v2`: `01427880e1c4c5ddb896b8b0c7fb8c74f6b228c9`
- `the-critic`: `6b41312b6d46fea1c112ac629f90dc43268e5ed0`

## Authoritative Artifacts

- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_session_2026-03-25.har`
- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json`
- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_state_2026-03-25.png`

## Attempt Trail

### Attempts 1-3: superseded pre-repair / pre-current-baseline trail

- Attempt 1 hit a stale local analyzer process still serving the old `10.0s` selector timeout.
- Attempt 2 fixed analyzer-side planning but still had `the-critic` warmup proxying to onrender.
- Attempt 3 proved selector/provider repair but stopped at the then-real host identity-continuity `409`.

Those attempts are no longer the live baseline for this step because the bounded identity-continuity repair slice has since landed.

### Attempt 4: authoritative post-identity-repair diagnostic attempt

Environment used:

- `the-critic` backend proxy set to `ANALYZER_V2_URL=http://127.0.0.1:8002`
- preferred ports `5555/3456` were occupied, so this authoritative attempt ran on `5556/3457`

Outcome:

- `route-task` succeeded
- `plan-task` succeeded and returned `aoi_composition_handoff_plan`
- planner-backed continue reached `/compose-from-intent`
- the host compose request stayed on `compose-from-selection`
- canonical `source_v2_job_id` was preserved in the compose request
- `compose-from-source` stayed unused
- planner-backed compose then failed with `404`

So the repaired planner-backed path is still not credible enough to consume the frozen rerun.

## What The Artifacts Show

### 1. The repaired planner-backed AOI path is really being used

The authoritative request trail shows:

- `planning_outcome_kind = aoi_composition_handoff_plan`
- `planner_selection_trace.timeout_s = 45`
- `planner_selection_trace.retry_policy.max_retries = 0`
- `planner_selection_trace.provider_outcome = success`
- `planner_selection_trace.exception_class_name = null`
- host compose endpoint used: `compose-from-selection`
- host compose request `variant = selection`
- `source_v2_job_id = proof-round5-adaptive-aoi-dossier-final-1774100000`
- `compose-from-source` is absent from the request trail

Measured latencies from the saved artifact:

- planner selection latency: `11521 ms`
- composition latency: `4946 ms`
- total user-visible latency: `27140 ms`

This means the current failure is no longer selector/provider reliability and no longer the old AOI identity-continuity seam.

### 2. The new blocker is now warm snapshot durability / saved-result lookup continuity

The authoritative request trail shows:

- browser advanced to `/compose-from-intent`
- the compose request was `POST /api/analysis/anxiety_of_influence_thematic_single_thinker/projects/round5-proof-dossier-final-1774100000/compose-from-selection`
- response status was `404`
- response detail was:

`Saved AOI result not found: gen-v2-3834f733047a`

The UI surfaced that as:

`Source result not found: Saved AOI result not found: gen-v2-3834f733047a`

No legacy/debug fallback was used.

### 3. Local backend evidence matches the `404`

The returned `source_analysis_id` in the authoritative browser URL was:

- `gen-v2-3834f733047a`

Direct local DB inspection showed:

- `genealogy_analyses.id = gen-v2-3834f733047a` does **not** exist
- other warmed snapshot ids created during the same window do exist:
  - `gen-v2-1d44f1978baf`
  - `gen-v2-9c2d9e9295ff`
  - `gen-v2-2fbac9d9ba55`
  - `gen-v2-cebe629a03ac`
  - `gen-v2-3b4fcb80dc0d`
  - `gen-v2-f7c02e313a49`

Backend logs during the same window show repeated:

- `Failed to save v2 presentation to database: database is locked`

The current server implementation also makes the risk concrete:

- `_save_v2_presentation_to_db(...)` generates an `analysis_id` before attempting the DB write
- if the DB write fails, the exception is logged but the function still returns that generated `analysis_id`

So the stopped path is now:

- planner resolves the AOI handoff correctly
- warm snapshot creates a generated local `analysis_id`
- the browser is navigated with that `analysis_id`
- durable local save can fail under DB lock
- compose lookup then fails because the returned `analysis_id` was never actually persisted

## Failure Bucket Decision

For the authoritative attempt, the failure bucket is:

- `host warm snapshot durability / saved-result lookup continuity`

It is not:

- selector timeout
- selector provider failure
- legacy fallback
- blocked planner selection
- the earlier AOI identity-continuity `409`

## Branch Decision

Do **not** consume the full frozen four-case rerun.

Reason:

- the plan explicitly treats planner-backed `compose-from-selection` failure after successful planning as a stop-and-revise condition

## Immediate Next Step

The next bounded slice should fix the host-side warm snapshot durability seam across:

- warm snapshot persistence
- returned `source_analysis_id` truth
- compose lookup continuity under local DB lock / failed save conditions

Then repeat:

1. this same `evolution_ready` diagnostic spot-check
2. only if it succeeds end-to-end, the same frozen four-case Stage 5 rerun

## Status Implications

- Stage 5 remains `In progress`
- the frozen rerun was not earned
- Stage 2 remains open
- Tranche 3 remains blocked
