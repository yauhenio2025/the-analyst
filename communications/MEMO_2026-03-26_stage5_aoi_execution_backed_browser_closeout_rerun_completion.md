# Memo: Stage 5 AOI Execution-Backed Browser Closeout Rerun Completion

Date: 2026-03-26
Status: Browser rerun completed; Stage 2 remains open
Program: Dynamic Bespoke Apps Platformization
Depends on:
- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_scope.md`
- `communications/MEMO_2026-03-26_stage5_aoi_local_snapshot_idempotence_revision_completion.md`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_preflight_identity_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_precompose_pin_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_requests_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_session_2026-03-26.har`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_state_2026-03-26.png`

## Summary

The counted planner-primary browser closeout rerun on the repaired host behavior is now complete.

The structural browser proof passed:

- the recovered upstream source stayed fixed on `source_v2_job_id = job-6ee8b0621177`
- preflight resolved the current canonical local alias as `source_analysis_id = gen-v2-9e3e5ad74dbb`
- the AOI panel auto-loaded a presentation on entry, `Clear` was used, and the recovered row was then explicitly clicked
- the path stayed on planner-backed `compose-from-selection`
- `/compose-from-intent` preserved both source ids
- the host `compose-from-selection` request body preserved both source ids and the four planner-selected source families
- the host returned `200` and rendered a five-view transient shell

So the repaired host/browser identity law now holds strongly enough for an honest counted execution-backed browser proof.

However, Stage 2 still remains open.

The reason is no longer missing browser evidence. The remaining blocker is content integrity inside the recovered execution-backed AOI source itself:

- the saved AOI result for nominal Otto Neurath source `job-6ee8b0621177` / `gen-v2-9e3e5ad74dbb` still contains Phase 1.0 preview content with `selected_source_thinker = john_oneill`
- the same recovered payload still describes Benanav's project as an operationalization of John O'Neill's reconstruction of Otto Neurath

That contradiction is not convincingly explained by the current proof. So the rerun is structurally successful, but the exemplar still is not honest enough yet for Stage 2 closure or repeated bounded AOI transient use.

## What The Rerun Proved

### 1. Explicit row pinning and repaired host reuse now work

The rerun satisfied the browser-boundary identity requirements:

- preflight job detail returned:
  - `v2_job_id = job-6ee8b0621177`
  - `analysis_id = gen-v2-9e3e5ad74dbb`
- the saved-results list showed the recovered row after `Clear`
- the explicit clicked row was the recovered source:
  - `job-6ee8b0621177`
  - supporting local alias `gen-v2-9e3e5ad74dbb`

This closes the earlier host-side local snapshot idempotence seam for the counted browser path.

### 2. The normal host snapshot step preserved the same local alias

The rerun did not rewrite the local alias during browser consumption.

HAR evidence shows:

- `cache-v2` fired `8` times on the normal host step
- all `8` responses returned:
  - `status = cached`
  - `v2_job_id = job-6ee8b0621177`
  - `analysis_id = gen-v2-9e3e5ad74dbb`

So the repaired host now converges on the same canonical local snapshot id under repeated browser traffic.

### 3. The counted planner-primary path preserved end-to-end source identity

The compose page carried both source identities:

- `source_v2_job_id = job-6ee8b0621177`
- `source_analysis_id = gen-v2-9e3e5ad74dbb`

The host `compose-from-selection` POST body also preserved both identities and the planner-selected source families:

- `thematic_synthesis`
- `engagement_mapping`
- `sin_findings`
- `thematic_report`

The response returned `200` and rendered a transient shell with:

- `workflow_key = anxiety_of_influence_thematic_single_thinker`
- `view_count = 5`
- `resolver_version = compose-from-selection-v1`

So the counted execution-backed browser bundle is now real and documentary-sound on the product path.

## Why Stage 2 Still Does Not Close

The browser proof answers the structural question.

It does **not** resolve the content-level source-identity contradiction in the recovered AOI payload.

The recovered saved result still contains evidence that the source thinker inside the Phase 1.0 thematic synthesis content is John O'Neill rather than Otto Neurath, even though:

- the run identity is `job-6ee8b0621177`
- the host/browser identity is `otto_neurath`
- the planner-selected compose path is now behaving correctly

That means:

- `operational_behavior` is now strong
- the execution-backed browser evidence itself is honest
- but `selection_fit` / `rendered_usefulness` cannot be treated as closure-grade yet because the recovered source payload still carries an unresolved thinker-identity contradiction

So the repeated bounded-use bar is not met.

## Status Implications

- the Stage 5 fixture-backed seam gate remains passed
- the execution-backed browser closeout rerun itself now passes structurally
- Stage 2 remains open
- Tranche 3 remains blocked

## Next Honest Step

The next step is one bounded diagnosis and repair slice on AOI source-thinker content integrity for the recovered execution-backed source.

That next slice should explain and, if needed, repair why a nominal Otto Neurath AOI run still emits content preview/state that names John O'Neill inside the recovered payload, even though the repaired host/browser path now preserves the correct source identities end to end.
