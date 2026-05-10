# Memo: Stage 5 AOI Exemplar Diagnostic And Rerun Scope

Date: 2026-03-25
Status: Draft scope memo
Program: Dynamic Bespoke Apps Platformization
Depends on:
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_revision.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_revision_slice_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_revision_slice_completion.md`
- `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_completion.md`
- `communications/PROOF_2026-03-24_stage5_aoi_exemplar_eval_pack.md`
- `communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-24.json`
Roadmap sources:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

## Summary

The bounded Stage 5 revision slice and the bounded Stage 5 identity-continuity repair slice are now implemented.

That means the next honest step is no longer another repair pass by default.
It is an operational proof step:

1. run one live `evolution_ready` diagnostic spot-check on the repaired path
2. write the diagnosis note from real request artifacts
3. only if that diagnostic now passes end-to-end, rerun the same frozen four-case Stage 5 pack with the same rubric

Do not change:

- the case set
- the rubric
- the roadmap order
- the Stage 2 closure bar

## Why This Is The Next Honest Step

The program has already done the bounded code repair that the failed first gate justified:

- selector/provider hardening is landed
- planner-outcome retention is landed
- the delayed hydrate race now has direct regression coverage
- the AOI identity-continuity slice is landed
- missing-row `v2_run_references` repair now has direct regression coverage
- repeated latest-snapshot/default-resolution continuity now has direct regression coverage

So the remaining uncertainty is no longer primarily design uncertainty.
It is live-behavior uncertainty on the repaired proof surface.

That should be resolved with one diagnostic run and one honest rerun, not with a new speculative tranche.

## Bounded Claim

The bounded claim for this step is:

- the repaired Stage 5 proof surface should now be pressure-tested live before any more code widening is proposed

This step does **not** claim:

- Stage 5 closure in advance
- Stage 2 closure in advance
- a new AOI architecture
- broader transient-substrate generalization
- lifecycle reopening

## Scope Decisions

### Decision 1: Keep the pack and rubric frozen

Do not change:

- `evolution_ready`
- `engagement_ready`
- `non_profile_ready`
- `selection_blocked`
- the locked non-profile requirement
- the blocked-case requirement
- the rubric dimensions
- the threshold shape

This is the same gate, rerun on a repaired proof surface.

### Decision 2: Use the repaired local product path first

Default target remains:

- local `analyzer-v2`
- local `the-critic`
- the current repaired planner-primary AOI surface
- Critic backend proxy pointed at local analyzer via `ANALYZER_V2_URL=http://127.0.0.1:8002`

Default proof corpus/results remain the same local AOI proof set used in the first Stage 5 run unless one case is intentionally upgraded to `execution_backed`.

Verification baseline for this step is the already-landed slice recorded in:

- `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_completion.md`

### Decision 3: Run one diagnostic `evolution_ready` spot-check before the full rerun

The first live step should be a single `evolution_ready` run over the repaired path.

Purpose:

- confirm that the repaired path still produces `aoi_composition_handoff_plan`
- confirm that planner-backed continue now advances through compose without the old AOI identity-continuity `409`
- confirm that the run stays on the repaired planner-backed `compose-from-selection` path with canonical `source_v2_job_id` preserved end-to-end
- determine whether any remaining failure is still a real product-path defect or only environment/provider-path noise

Required artifacts for the spot-check:

- one browser HAR or equivalent network export from the real `the-critic` session
- one saved JSON excerpt set for:
  - `route-task`
  - `plan-task`
  - host compose launch request if reached
  - analyzer compose response excerpt if reached
- one UI screenshot
- one short diagnosis note

The saved `plan-task` artifact or the diagnosis note must preserve the selector trace fields needed to audit timeout/retry/classification behavior:

- `timeout_s`
- `retry_policy.max_retries`
- `exception_class_name`
- `provider_outcome`
- `blocked_reason_code`
- `blocked_reason_detail`

The diagnosis note must record:

- observed exception class, if any
- emitted reason code
- request elapsed time from real request artifacts
- whether retries occurred, observed directly or inferred from artifacts
- which failure bucket actually applied
- whether the repaired path behaved as expected
- whether planner-backed compose was reached
- whether planner-backed compose succeeded or failed
- whether the host compose launch preserved canonical `source_v2_job_id`
- any environment changes made between attempts, if applicable

### Decision 4: Only then rerun the full four-case pack

After the diagnostic spot-check:

- if the repaired path now behaves credibly enough for the frozen gate, rerun the same four-case pack
- if the spot-check reveals an environment-only issue, fix the environment and repeat the spot-check before consuming the full rerun
- if the repaired path still times out at the `45.0s` selector budget and the evidence remains timeout-shaped rather than schema/product-path shaped, treat that as an environment/provider-path diagnosis first, not as automatic justification for a new code tranche
- if the spot-check reveals a new code/product-path failure that the current revision slice did not actually close, stop and write a new revision memo rather than pretending the full rerun is meaningful

`Credibly enough for the frozen gate` means:

- no unresolved product-path defect is exposed on the repaired planner-backed AOI path, and
- any remaining failure is either environment/provider-path-only or a non-blocking artifact-capture issue that does not change the product-path verdict

Explicit stop-and-revise conditions include:

- planner handoff succeeds but planner-backed `compose-from-selection` fails
- planner-backed handoff or compose request drops canonical `source_v2_job_id`
- planner-backed flow reaches compose only by falling back to legacy/debug profile controls
- blocked reason code/detail is visible in the UI but not preserved in the saved proof artifacts

This keeps the rerun honest.

### Decision 5: Count only the repaired planner-backed path

For both the diagnostic and the frozen rerun, a case only counts if it stays on the repaired planner-backed path:

- `AoiV2ThematicPanel` planner-backed continue
- `/compose-from-intent`
- `compose-from-selection`
- canonical `source_v2_job_id` preserved alongside `source_analysis_id`

The still-existing simple/legacy profile launch path remains intentionally present in the product, but it does **not** count toward this Stage 5 proof step.

### Decision 6: Preserve the blocked-case visibility requirement in both UI and artifacts

For `selection_blocked`, the repaired host surface must prove both:

- blocked reason code/detail remain stably visible in the AOI panel
- blocked reason code/detail remain artifact-visible in the saved proof trail

No compose request should be sent after the blocked planning result.

### Decision 7: Be explicit about the likely Stage 2 outcome

By default, this rerun should be treated as a Stage 5 seam/ops decision first.

Unless at least one ready case is intentionally upgraded to `execution_backed` or stronger, the likely honest outcomes are:

- Stage 5 may pass
- Stage 2 may still remain open

If Stage 2 closure is desired in the same pass, nominate that upgrade explicitly before the rerun.
Default candidate:

- `evolution_ready`

If no such upgrade is prepared, do not force Stage 2 closure language into the closeout.

## Proposed Deliverables

### 1. Diagnostic spot-check artifacts

For `evolution_ready`:

- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_session_2026-03-25.har`
- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json`
- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_state_2026-03-25.png`
- `communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md`

### 2. Full rerun artifacts if the spot-check earns it

Reuse the existing naming pattern with `2026-03-25` for:

- ready-case HAR / request / state artifacts
- blocked-case HAR / request / state artifacts
- one rerun summary JSON
- one rerun proof note

The rerun summary JSON and closeout note must preserve, per case:

- `fixture_strength`
- whether the case remained `fixture_backed` or was upgraded to `execution_backed`
- whether any environment changes occurred between spot-check attempts and rerun
- whether the case stayed on the planner-primary path without legacy/debug fallback

### 3. Closeout memo

Produce one of:

- success: `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_completion.md`
- failure/revision: `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_revision.md`

That memo must decide separately:

- whether Stage 5 passed
- whether Stage 2 closed

It must not collapse a Stage 5 pass into a Stage 2 closure claim unless the recorded per-case evidence actually meets the stronger Stage 2 bar.

## Verification

If no code changes are made before the spot-check, verification can rely on the already-green focused confidence pack recorded in:

- `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_completion.md`

If any code changes are made after the spot-check, rerun:

- `PYTHONPATH=. pytest -q tests/test_task_router.py tests/test_task_planner.py tests/test_composition_source_bridge.py tests/test_compose_from_intent.py`
- `/home/evgeny/projects/the-critic/webapp/node_modules/.bin/tsc -p /home/evgeny/projects/the-critic/webapp/tsconfig.json --noEmit`
- `CI=true npm --prefix /home/evgeny/projects/the-critic/webapp test -- --runInBand --watchAll=false src/lib/taskLaunchRuntime.test.ts src/lib/composeFromIntentClient.test.ts src/components/influence/AoiV2ThematicPanel.test.tsx src/pages/AoiComposeFromIntentPage.test.tsx src/transientComposeIsolation.test.ts src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx`
- `PYTHONPATH=. pytest -q tests/test_aoi_v2_client.py tests/test_aoi_v2_routes.py`

## Acceptance Criteria

This scope is successful only if it leads to one of two honest outcomes:

1. the repaired path passes the diagnostic spot-check and the full frozen rerun is executed with a real Stage 5 decision
2. the repaired path still fails meaningfully enough that a new revision memo is written instead of consuming the full rerun dishonestly

## Assumptions

- The repaired code path is now stable enough to deserve a live diagnostic spot-check.
- No further code widening is presumed in advance.
- The frozen Stage 5 pack and rubric remain authoritative.
- Tranche 3 remains blocked until this rerun produces a real decision.
