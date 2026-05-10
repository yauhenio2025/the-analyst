# Prompt For Codex: Stage 5 AOI Local Snapshot Idempotence Revision Scope Audit

Audit the new local-snapshot-idempotence scope doc:

- `communications/MEMO_2026-03-26_stage5_aoi_local_snapshot_idempotence_revision_scope.md`

Your job is to test the robustness of the assumptions behind that memo against the actual codebase, recent Stage 5 memo/proof trail, and the larger analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “dedupe some local rows.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- keep Tranche 3 blocked until AOI exemplar ratification is honest rather than inferred

So assess the new memo both as:

1. a bounded host-side repair scope
2. a broader platform-program prioritization decision

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

Then inspect the implementation and proof paths the memo relies on:

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

1. Does the codebase support the memo’s claim that this is a bounded host-side idempotence fix, or does the repair actually need broader contract or UI work than the memo admits?
2. Is the identified seam accurate:
   - completed-job detail backfill minting fresh local ids
   - `cache-v2` minting fresh local ids
   - results-list duplication destabilizing explicit row pinning
3. Is collapsing results to one canonical entry per upstream `v2_job_id` the right seam-level repair, or does that risk hiding underlying local corruption instead of fixing it?
4. Are there hidden cases the memo is missing:
   - stale `v2_run_references.local_snapshot_analysis_id`
   - refresh path widening duplicates
   - project/thinker identity mismatch while reusing a canonical row
   - existing tests that would break on deduped results behavior
5. Is keeping the recovered run `job-6ee8b0621177` as the fixed counted source still the right sequencing decision after this repair?
6. Does the memo keep the roadmap honest:
   - Stage 5 seam gate already passed
   - Stage 2 still open
   - Tranche 3 still blocked
7. Does this memo put regression ownership on the real seam, or should the test plan move elsewhere?

## Output requirements

Write your audit to:

- `communications/REPORT_Codex_STAGE5_AOI_Local_Snapshot_Idempotence_Revision_Scope_Audit_2026-03-26.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve with revisions`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether the seam diagnosis is technically correct.
5. A direct answer to whether the proposed repair is appropriately bounded.
6. Any concrete memo revisions you recommend before implementation.

Prioritize bugs, hidden assumptions, evidence-quality gaps, scope dishonesty, dedupe-vs-canonicalization risks, and broader-program mis-sequencing over general summary.
