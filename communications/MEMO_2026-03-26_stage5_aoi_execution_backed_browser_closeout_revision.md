# Memo: Stage 5 AOI Execution-Backed Browser Closeout Revision

Date: 2026-03-26
Status: Browser closeout attempt failed; Stage 2 remains open
Program: Dynamic Bespoke Apps Platformization
Depends on:
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_recovery_completion.md`
- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_recovery_summary_2026-03-25.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_precompose_pin_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_requests_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_session_2026-03-26.har`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_state_2026-03-26.png`

## Summary

I attempted the counted browser closeout on the recovered fresh execution-backed AOI run `job-6ee8b0621177`.

The attempt did not reach a valid counted planner-backed compose proof.

The new blocker is not the planner-primary compose chain itself. The blocker is a host-side identity seam:

- completed-job reads and repeated `cache-v2` requests are minting fresh local snapshot ids for the same upstream `v2_job_id`
- the AOI panel auto-loads the latest saved result by default
- together, those behaviors make stable recovered-row pinning impossible enough that the counted browser bundle cannot be written honestly

So the closeout slice stops here and Stage 2 remains open.

## What Happened

### 1. Preflight identity had already drifted before the browser proof started

The recovered-run summary from 2026-03-25 anchored the local snapshot id as:

- `gen-v2-18853b558ef1`

But the first live preflight read during this closeout attempt already returned a different local snapshot id for the same upstream job:

- `GET /api/analysis/anxiety_of_influence_thematic_single_thinker/jobs/job-6ee8b0621177`
- returned `analysis_id = gen-v2-6849427079a1`

Later in the same session, the same completed-job route stabilized on yet another local snapshot id:

- `analysis_id = gen-v2-9e3e5ad74dbb`

The upstream identity stayed the same:

- `v2_job_id = job-6ee8b0621177`
- thinker remained `otto_neurath`

So the drift is in host-local snapshot identity, not upstream run identity.

### 2. The browser proof failed before row pinning was established

The AOI panel opened with an auto-loaded presentation visible.

Per the scoped plan, I triggered the `Clear` control to expose the saved-results list so the recovered row could be explicitly pinned.

The page did not transition into a stable visible saved-results state within the timeout window, so no honest explicit row pin was established.

The captured browser-state artifact still shows the auto-loaded presentation surface rather than a stable pinned-row selection state:

- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_state_2026-03-26.png`

### 3. The underlying cause is repeated local snapshot churn for the same upstream job

The captured network trace during the failed browser attempt shows repeated successful `cache-v2` responses for the exact same upstream job:

- `34` successful `cache-v2/job-6ee8b0621177` responses in the single attempt
- sample returned analysis ids:
  - `gen-v2-4b515b4fb4c6`
  - `gen-v2-8b5506e46ce9`
  - `gen-v2-8c14c63d219c`
  - `gen-v2-92ae508428f6`
  - `gen-v2-4c74583791ba`

Local DB state confirms that this is not just a logging artifact:

- `v2_run_references.local_snapshot_analysis_id` now points at `gen-v2-9e3e5ad74dbb`
- `genealogy_analyses` now contains `81` rows whose `pass_results._v2_job_id = job-6ee8b0621177`

That means the same recovered execution-backed run is being re-materialized into many host-local snapshot ids instead of reusing one stable durable local snapshot.

## Why The Attempt Does Not Count

This attempt does **not** count as the Stage 2 browser closeout because:

- explicit recovered-row pinning was never established
- local `source_analysis_id` drifted across reads for the same `v2_job_id`
- the host was actively creating new local snapshot ids during the attempt
- no honest counted planner-backed `compose-from-selection` artifact bundle can be claimed on a stable recovered local source under those conditions

So the recovered case also was **not** re-graded against the frozen rubric in this pass.
That grading was not earned.

## Status Implications

- Stage 5 seam gate from the frozen fixture-backed pack remains passed
- the recovered execution-backed run still exists upstream and remains real
- Stage 2 remains open
- Tranche 3 remains blocked

## Next Honest Step

The next step is one bounded host-side repair slice for local snapshot idempotence on completed AOI v2 runs.

That slice should make these behaviors stable for a single upstream `v2_job_id`:

- completed-job detail reads
- `cache-v2` warm/reuse behavior
- AOI panel auto-load plus clear plus saved-result selection interaction

The repair goal is simple:

- one upstream completed run should converge on one durable reusable local snapshot id unless the stored local row is missing or invalid

Only after that repair should the browser closeout be retried.
