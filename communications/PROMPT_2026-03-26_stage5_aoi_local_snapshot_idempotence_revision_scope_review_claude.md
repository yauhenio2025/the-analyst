# Prompt For Claude: Stage 5 AOI Local Snapshot Idempotence Revision Scope Critique

Critique the new local-snapshot-idempotence scope doc:

- `communications/MEMO_2026-03-26_stage5_aoi_local_snapshot_idempotence_revision_scope.md`

Your job is to test the robustness of the assumptions behind that memo against the actual codebase, the recent Stage 5 memo/proof trail, and the broader analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “stabilize one browser test.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- close the AOI exemplar honestly before Tranche 3 generalization

So evaluate the new memo both as:

1. a bounded next-step scope for repairing host-local snapshot identity churn
2. a broader program-prioritization decision about what should happen before Stage 2 can close and before Tranche 3 can move

## What to inspect

Read these docs first:

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
    - `_best_effort_ensure_local_snapshot_analysis_id(...)`
    - `_save_v2_presentation_to_db(...)`
    - `_update_v2_presentation_in_db(...)`
    - `GET /api/analysis/{workflow_key}/jobs/{job_id}`
    - `POST /api/genealogy/cache-v2/{v2_job_id}`
    - `POST /api/genealogy/refresh-v2/{v2_job_id}`
    - `GET /api/genealogy/results/{project_id}`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts`

Also look through any other recent memo/report/proof files in `communications/` or relevant `docs/` that materially affect the judgment.

## Questions to answer

1. Is the memo right that the new blocker is host-local identity churn rather than another planner/compose or analyzer seam?
2. Does the codebase actually support the memo’s proposed fix surface:
   - idempotent completed-job backfill
   - idempotent `cache-v2` reuse
   - refresh updating the canonical row
   - deduped saved-results output stable enough for explicit row pinning
3. Is collapsing the AOI-facing saved-results list to one canonical row per upstream `v2_job_id` the right repair, or does that risk masking unresolved truth problems?
4. Is keeping `job-6ee8b0621177` as the fixed counted source still the right operational choice, or is the memo being too brittle by freezing that source?
5. Does the memo under-specify any hazards:
   - stale local row references
   - project/thinker mismatch while reusing a row
   - auto-loaded presentation behavior after dedupe
   - broader side effects on non-AOI genealogy results
6. Is this slice narrow enough to keep roadmap order honest:
   - Stage 5 seam gate already passed
   - Stage 2 still open until browser closeout succeeds
   - Tranche 3 still blocked
7. Is the step appropriately bounded, or is it still smuggling in broader closure by implication?

## Output requirements

Write your critique to:

- `communications/REPORT_Claude_STAGE5_AOI_Local_Snapshot_Idempotence_Revision_Scope_Critique_2026-03-26.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve after revision`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether the seam diagnosis is technically correct.
5. A direct answer to whether the proposed repair is appropriately bounded.
6. Any concrete memo revisions you recommend before implementation.

Prioritize hidden assumptions, evidence-tier dishonesty, scope leakage, canonicalization-vs-masking risks, roadmap overclaim, and codebase mismatches over general summary.
