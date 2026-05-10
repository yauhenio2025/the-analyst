# Prompt For Codex: Stage 5 AOI Execution-Backed Browser Closeout Rerun Scope Audit

Audit the new browser-closeout-rerun scope doc:

- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_scope.md`

Your job is to test the robustness of the assumptions behind that memo against the actual codebase, recent Stage 5 memo/proof trail, and the larger analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “rerun the browser path because the tests are green.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- keep Tranche 3 blocked until AOI exemplar ratification is honest rather than implied

So assess the memo both as:

1. a bounded rerun scope on repaired host behavior
2. a broader platform-program prioritization decision

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

Then inspect the implementation and proof paths the memo relies on:

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

1. Does the codebase support the memo’s claim that the next honest move is a rerun, not more repair?
2. Is the identified counted-source rule technically correct:
   - anchor on upstream `job-6ee8b0621177`
   - resolve local canonical `analysis_id` at preflight
   - require preservation of both identities through `/compose-from-intent` and `compose-from-selection`
3. Is the memo appropriately strict about source continuity, or does it still leave room for silent drift?
4. Are there hidden cases the memo is missing:
   - local alias repaired in job detail but not in results listing
   - panel auto-load/clear behavior still obscuring row pinning
   - source identity preserved in URL but not in downstream payload/content
   - route-level idempotence holding in tests but not in the real browser request pattern
5. Is keeping the recovered upstream run `job-6ee8b0621177` as the fixed counted source still the right sequencing decision after the repair?
6. Does the memo keep the roadmap honest:
   - Stage 5 seam gate already passed
   - Stage 2 still open
   - Tranche 3 still blocked
7. Does this memo put the grading burden on the real seam, or does it still over-infer closure from one browser success?

## Output requirements

Write your audit to:

- `communications/REPORT_Codex_STAGE5_AOI_Execution_Backed_Browser_Closeout_Rerun_Scope_Audit_2026-03-26.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve with revisions`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether the rerun is now the right next step.
5. A direct answer to whether the counted-source identity rule is appropriately bounded and technically sound.
6. Any concrete memo revisions you recommend before execution.

Prioritize bugs, hidden assumptions, evidence-quality gaps, source-identity ambiguity, scope dishonesty, and broader-program mis-sequencing over general summary.
