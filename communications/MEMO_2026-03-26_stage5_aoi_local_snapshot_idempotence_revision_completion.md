# Memo: Stage 5 AOI Local Snapshot Idempotence Revision Completion

Date: 2026-03-26
Status: Repair landed; counted browser rerun required
Program: Dynamic Bespoke Apps Platformization
Supersedes: N/A (this is the repair completion, not the browser rerun)
Depends on:
- `communications/MEMO_2026-03-26_stage5_aoi_local_snapshot_idempotence_revision_scope.md`
- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_revision.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_recovery_completion.md`
- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_recovery_summary_2026-03-25.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_precompose_pin_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_requests_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_session_2026-03-26.har`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_state_2026-03-26.png`

## Summary

The bounded `the-critic` local-snapshot-idempotence repair is now implemented.

The repair closes the host seam that blocked the first counted browser-closeout attempt on the recovered fresh execution-backed AOI source:

- completed-job detail reads now converge on one canonical local snapshot path
- repeated generic AOI `cache-v2` requests now converge on that same canonical local snapshot path
- `refresh-v2` and `import-v2` now join the same canonical path instead of widening duplicates
- AOI saved-results listing now prefers the canonical row referenced by `v2_run_references.local_snapshot_analysis_id`
- after `Clear`, the AOI panel now invalidates the active source and retained planner state until the operator explicitly clicks a saved-result row again

This materially advances the exemplar, but it is not the counted browser closeout itself.

Stage 2 remains open until the repaired host behavior is reconsumed on the planner-primary browser path and the recovered execution-backed case is graded honestly.

## What Landed

### 1. Canonical AOI local snapshot convergence in `the-critic`

AOI completed-run read/write paths now route through one async canonical helper chain under `v2_run_references` instead of minting local rows through the old sync insert helper.

Landed behavior:

- `v2_run_references` is now the serialization point for AOI local snapshot reuse/creation
- the helper uses create-or-get semantics for first touch
- Postgres uses row locking on the winning `v2_run_references` row
- SQLite uses write-lock acquisition before canonical lookup/creation
- completed-job backfill, generic AOI `cache-v2`, `refresh-v2`, and `import-v2` now converge on the same canonical local row for one upstream `v2_job_id`
- `refresh-v2` now uses the canonical row directly rather than widening duplicate local rows

Files changed:

- `/home/evgeny/projects/the-critic/api/server.py`

### 2. AOI results-list stability for browser pinning

The AOI-facing saved-results list now prefers the canonical local row mapped by `v2_run_references.local_snapshot_analysis_id` when collapsing duplicate rows for one upstream `v2_job_id`.

The repair intentionally leaves historical duplicate rows in place for now, but makes them inert for:

- canonical identity resolution
- AOI results listing
- the counted browser rerun

Files changed:

- `/home/evgeny/projects/the-critic/api/server.py`

### 3. Post-`Clear` explicit reselection guard in the AOI panel

The AOI panel now treats `Clear` as invalidating the active source and any retained planner decision.

Effect:

- after `Clear`, no source-backed launch path may silently fall back to `savedResults[0]`
- planner-backed actions remain disabled until the operator explicitly clicks a saved-result row
- legacy/debug source-backed launch controls stay disabled too

Files changed:

- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`

## Regression Coverage

Focused regressions now prove the seam at the route and UI levels.

Backend:

- repeated completed-job detail reads reuse the same `analysis_id`
- repeated generic AOI `cache-v2` calls reuse the same `analysis_id`
- overlapping generic AOI `cache-v2` route calls converge on one canonical local row
- overlapping `refresh-v2` route calls converge on one canonical local row
- `refresh-v2` and `import-v2` stay on the canonical path
- AOI listing collapse prefers the canonical row instead of widening duplicate rows

Frontend:

- `Clear` exposes the need for explicit row pinning again
- `Clear` invalidates retained planner state
- planner-backed and legacy/debug source-backed launches stay disabled until explicit reselection
- explicit row click re-enables the source-backed path

Files changed:

- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`

## Verification

Run results:

- `pytest -q /home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
  - `51 passed`
- `PYTHONPATH=/home/evgeny/projects/the-critic pytest -q /home/evgeny/projects/the-critic/tests/test_aoi_v2_client.py`
  - `9 passed`
- `CI=true npm --prefix /home/evgeny/projects/the-critic/webapp test -- --runInBand --watchAll=false src/components/influence/AoiV2ThematicPanel.test.tsx src/lib/boundedV2Client.test.ts`
  - `73 passed`
- `./node_modules/.bin/tsc -p /home/evgeny/projects/the-critic/webapp/tsconfig.json --noEmit`
  - passed

Residual warnings are unchanged:

- existing React `act(...)` warnings in the AOI panel test suite
- existing Pydantic / FastAPI / SQLAlchemy warnings in the Python suite

## Status Implications

- the frozen fixture-backed Stage 5 seam gate remains passed
- the recovered fresh execution-backed AOI source remains the counted upstream source candidate:
  - `source_v2_job_id = job-6ee8b0621177`
- Stage 2 still remains open
- Tranche 3 still remains blocked

## Next Honest Step

The next step is not another repair tranche and not another fresh AOI launch by default.

The next step is the counted planner-primary browser closeout rerun on the repaired host behavior using the recovered upstream source `job-6ee8b0621177`.

That rerun should:

1. preflight-resolve the current canonical local `analysis_id` for the recovered source
2. clear any auto-loaded presentation if present
3. explicitly click the recovered saved-result row
4. stay on the planner-backed `compose-from-selection` path
5. preserve both the recovered `source_v2_job_id` and the preflight-resolved canonical local `source_analysis_id`
6. then write the Stage 2 decision honestly

If that rerun fails on a genuinely new seam, stop and write a new revision memo rather than widening scope inside the same pass.
