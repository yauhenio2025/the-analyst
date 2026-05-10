# Memo: Stage 5 AOI Execution-Backed Evolution-Ready Recovery Completion

Date: 2026-03-25
Status: Fresh live run recovered; counted browser proof still pending
Program: Dynamic Bespoke Apps Platformization
Supersedes: N/A (this is a recovery completion, not the final execution-backed closeout)
Depends on:
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_completion.md`
- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_recovery_summary_2026-03-25.json`

## Summary

One fresh live `execution_backed` AOI `evolution_ready` run was launched through the real `the-critic` route and completed, but the first proof attempt exposed two bounded seams during recovery:

1. analyzer auto-presentation left the finished run stuck in `result_state = preparing` because the workflow runner bypassed the real presentation coordinator and dropped `consumer_key`
2. the-critic completed-job detail responses did not backfill a durable local snapshot `analysis_id` for a completed, restorable v2 AOI run unless the user had already gone through an explicit cache/import path

Both seams are now repaired.

The fresh live run is now durably queryable end to end:

- fresh job id: `job-6ee8b0621177`
- analyzer result id: `result-8fb483dd1184290e6800e988`
- Critic local analysis id: `gen-v2-18853b558ef1`
- selected source thinker: `otto_neurath`
- analyzer manifest state: `ready`
- presentation status: `completed`
- Critic job detail now returns `analysis_id`
- Critic saved-result lookup resolves the same fresh run through the durable local snapshot id

This is meaningful progress, but it is not the final Stage 2 closeout. The counted planner-backed browser compose bundle for this fresh run has still not been captured, so the execution-backed proof plan is not yet complete.

## What Landed

### 1. Analyzer auto-presentation recovery

`analyzer-v2` now routes workflow auto-presentation through the real presentation coordinator instead of an ad hoc path that called presenter preparation without `consumer_key`.

Effect:

- completed runs no longer get stranded in `preparing` for this seam
- the recovered live run now reports:
  - `result_state = ready`
  - `presentation_status = completed`
  - `restore_available = true`

Files changed:

- `src/executor/workflow_runner.py`
- `tests/test_workflow_runner_auto_presentation.py`

Focused verification:

- `PYTHONPATH=. pytest -q tests/test_workflow_runner_auto_presentation.py tests/test_preparation_coordinator.py tests/test_adaptive_planner.py tests/test_plan_revision.py`
- result: `12 passed`

### 2. Critic local snapshot backfill for completed v2 AOI runs

`the-critic` now performs a bounded best-effort local snapshot backfill when a completed, restorable AOI v2 job is read through the normal completed job-detail route.

Effect:

- live completed AOI runs can now surface a durable local `analysis_id` without requiring a prior explicit cache/import action
- the returned `analysis_id` remains honest: if the snapshot save fails, the API still returns `None` rather than synthesizing a fake id
- the recovered fresh job now resolves through:
  - `GET /api/analysis/anxiety_of_influence_thematic_single_thinker/jobs/job-6ee8b0621177`
  - `GET /api/analysis/anxiety_of_influence_thematic_single_thinker/results/round5-proof-dossier-final-1774100000/gen-v2-18853b558ef1`

Files changed:

- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/api/models_genealogy.py`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`

Focused verification:

- `PYTHONPATH=/home/evgeny/projects/the-critic:/home/evgeny/projects/the-critic/api pytest -q /home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
- result: `45 passed`

## Live State After Recovery

The repaired live state is summarized in:

- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_recovery_summary_2026-03-25.json`

Key verified facts:

- Critic job detail for `job-6ee8b0621177` now reports:
  - `status = completed`
  - `v2_job_id = job-6ee8b0621177`
  - `analysis_id = gen-v2-18853b558ef1`
- analyzer result manifest for the same job now reports:
  - `result_id = result-8fb483dd1184290e6800e988`
  - `result_state = ready`
  - `presentation_status = completed`
  - `restore_available = true`
- Critic saved-result lookup by `gen-v2-18853b558ef1` resolves and preserves the same fresh `v2_job_id`

## What This Does Not Yet Prove

This memo does **not** claim final execution-backed AOI exemplar completion.

The missing piece is still the counted planner-backed browser proof bundle on this fresh run:

- planner-backed selection from the fresh saved result row
- `/compose-from-intent` preserving the fresh `source_v2_job_id`
- `compose-from-selection` completing on that same fresh source
- saved request JSON / HAR / screenshot for that counted browser path

Until that bundle exists, the proof remains materially advanced but not closure-grade under the frozen Stage 2 rubric.

## Status Implications

- Stage 5 seam gate remains passed on the already-recorded fixture-backed rerun
- the execution-backed proof attempt is now materially advanced because there is a real fresh run and it is durably restorable/queryable again
- Stage 2 still remains open
- Tranche 3 still remains blocked

## Next Honest Step

Use the recovered fresh result as the counted browser source and capture the missing planner-backed compose artifacts.

If that counted browser path fails on this recovered fresh run, stop and write a revision memo rather than widening scope again inside the same pass.
