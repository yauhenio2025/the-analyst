# Memo: Stage 5 AOI Identity Continuity Revision Completion

Date: 2026-03-25

## Summary

The bounded Stage 5 AOI identity-continuity repair slice is now implemented.

This slice closed the specific blocker exposed by the repaired-path `evolution_ready` diagnostic:

- durable `v2_run_references` AOI thinker identity truth
- warm snapshot projection of that truth into local AOI saved results
- planner-backed handoff preserving canonical `source_v2_job_id`
- strict compose validation over `source_analysis_id` plus `source_v2_job_id`

The slice was intentionally narrow.

It did **not** reopen:

- AOI selector/provider behavior
- the Stage 5 case set
- the rubric
- Stage 2 closure criteria
- Tranche 3 sequencing

## What Landed

### Backend continuity repair in `the-critic`

The host backend now repairs and validates the AOI source identity chain across:

- `v2_run_references`
- warmed local snapshot persistence
- planner-backed compose proxy resolution

What is now true:

- warmup can backfill a missing AOI thinker identity onto an existing `v2_run_references` row
- warmup can create a missing `v2_run_references` row for the proof path when none exists locally
- warmed local AOI snapshots now persist the repaired thinker identity
- planner-backed compose now treats `source_v2_job_id` as canonical upstream identity
- if `source_analysis_id` and `source_v2_job_id` are both present and disagree, the host returns `409` rather than silently preferring one

### Frontend handoff repair in `the-critic`

The planner-backed AOI UI now preserves the full source identity chain:

- warm snapshot requests carry thinker identity
- planner-backed navigation into `/compose-from-intent` preserves canonical `source_v2_job_id`
- planner-backed compose requests forward both `source_analysis_id` and `source_v2_job_id`

### Regression coverage

The focused regression pack now covers:

- missing-row `v2_run_references` creation
- existing-row thinker backfill
- warmed snapshot identity projection
- fail-closed mismatch handling between `source_analysis_id` and `source_v2_job_id`
- repeated latest-snapshot/default-resolution continuity after repair
- planner-backed panel navigation preserving canonical `source_v2_job_id`
- planner-backed compose request forwarding of both identities

## Verification

The implemented slice was verified with:

- `PYTHONPATH=. pytest -q tests/test_aoi_v2_routes.py tests/test_aoi_v2_client.py`
- `./webapp/node_modules/.bin/tsc -p ./webapp/tsconfig.json --noEmit`
- `CI=true npm --prefix ./webapp test -- --runInBand --watchAll=false src/components/influence/AoiV2ThematicPanel.test.tsx src/pages/AoiComposeFromIntentPage.test.tsx src/lib/taskLaunchRuntime.test.ts src/lib/composeFromIntentClient.test.ts src/lib/boundedV2Client.test.ts`

Result:

- backend AOI route/client pack: `47 passed`
- frontend TypeScript check: passed
- focused frontend/Jest pack: `110 passed`

## Status Meaning

This completion memo does **not** mean Stage 5 is complete.

It means:

- the current host-side identity-continuity blocker is now addressed in code
- the current proof surface is ready for a fresh live diagnostic on the repaired path

It does **not** yet mean:

- the repaired path has passed live proof
- the frozen Stage 5 four-case pack has been rerun
- Stage 2 can close

## Status Decisions

### Stage 5

Stage 5 remains `In progress`.

Reason:

- the continuity slice is implemented
- but the repaired path has not yet been re-diagnosed live after that repair
- and the frozen four-case rerun has not yet been reconsumed

### Stage 2

Stage 2 remains open.

Reason:

- there is still no successful Stage 5 rerun completion artifact set
- there is still no basis for a documentary closure claim

### Tranche 3

Tranche 3 remains blocked.

Reason:

- the AOI exemplar loop is still not ratified end-to-end
- the next honest move remains inside Stage 5

## Immediate Next Step

The immediate next step is now operational again rather than architectural:

1. rerun the same `evolution_ready` diagnostic spot-check on the repaired path
2. write the updated diagnosis note from fresh artifacts
3. only if that passes end-to-end, rerun the same frozen four-case Stage 5 pack

That next step is scoped in:

- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md`

## Completion Note

This pass changed code and focused tests in `the-critic`.

It did **not** execute the next live diagnostic or the frozen rerun.
