# Prompt For Claude: Stage 5 AOI Execution-Backed Browser Closeout Rerun Scope Critique

Critique the new browser-closeout-rerun scope doc:

- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_scope.md`

Your job is to test the robustness of the assumptions behind that memo against the actual codebase, the recent Stage 5 memo/proof trail, and the broader analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “try the browser flow one more time.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- close the AOI exemplar honestly before Tranche 3 generalization

So evaluate the memo both as:

1. a bounded next-step scope for the repaired browser rerun
2. a broader program-prioritization decision about what still must happen before Stage 2 can close and before Tranche 3 can move

## What to inspect

Read these docs first:

- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_scope.md`
- `communications/MEMO_2026-03-26_stage5_aoi_local_snapshot_idempotence_revision_completion.md`
- `communications/MEMO_2026-03-26_stage5_aoi_local_snapshot_idempotence_revision_scope.md`
- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_revision.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_recovery_completion.md`
- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_recovery_summary_2026-03-25.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_precompose_pin_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_requests_2026-03-26.json`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

Then inspect the code paths the memo depends on:

The Critic:

- `/home/evgeny/projects/the-critic/api/server.py`
  - especially:
    - `_get_or_create_locked_v2_run_reference(...)`
    - `_ensure_canonical_v2_local_snapshot(...)`
    - `_load_preferred_saved_result_ids_for_listing(...)`
    - `GET /api/analysis/{workflow_key}/jobs/{job_id}`
    - `POST /api/analysis/{workflow_key}/cache-v2/{v2_job_id}`
    - `POST /api/genealogy/refresh-v2/{v2_job_id}`
    - `GET /api/genealogy/results/{project_id}`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts`

Also look through any other recent memo/report/proof files in `communications/` or relevant `docs/` that materially affect the judgment.

## Questions to answer

1. Is the memo right that the next step is now a rerun, not another repair tranche?
2. Is the counted-source identity rule honest:
   - fixed upstream `source_v2_job_id = job-6ee8b0621177`
   - local `source_analysis_id` resolved at preflight from the repaired host
   - preservation of both identities through the counted path
3. Is the memo too permissive or too strict about normal snapshot behavior:
   - reuse without a new warmup call
   - warm/reuse call that still returns the same canonical local id
4. Does the codebase now actually support the memo’s assumptions about:
   - stable row listing
   - post-`Clear` explicit row pinning
   - planner-backed `compose-from-selection` continuity
5. Is the memo under-specifying any remaining hazards:
   - local alias drift despite repaired canonicalization
   - stale saved-result ordering assumptions
   - mismatch between job-detail identity and row-selection identity
   - content-level source-identity drift inside the returned result payload
6. Is this scope still narrow enough to keep roadmap order honest:
   - Stage 5 seam gate already passed
   - Stage 2 still open until rerun is graded
   - Tranche 3 still blocked
7. Is the memo smuggling in Stage 2 closure by implication, or does it keep the closure decision genuinely explicit?

## Output requirements

Write your critique to:

- `communications/REPORT_Claude_STAGE5_AOI_Execution_Backed_Browser_Closeout_Rerun_Scope_Critique_2026-03-26.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve after revision`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether the rerun is now the right next honest step.
5. A direct answer to whether the counted-source identity rule is technically sound.
6. Any concrete memo revisions you recommend before execution.

Prioritize hidden assumptions, evidence-tier dishonesty, source-identity ambiguity, scope leakage, roadmap overclaim, and codebase mismatches over general summary.
