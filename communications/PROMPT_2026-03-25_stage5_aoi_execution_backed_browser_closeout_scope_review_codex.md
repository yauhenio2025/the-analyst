# Prompt For Codex: Stage 5 AOI Execution-Backed Browser Closeout Scope Audit

Audit the new browser-closeout scope doc:

- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_scope.md`

Your job is to test the robustness of the assumptions behind that memo against the actual codebase, recent Stage 5 memo/proof trail, and the larger analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “finish the browser artifacts.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- keep Tranche 3 blocked until AOI exemplar ratification is honest rather than inferred

So assess the new memo both as:

1. a bounded Stage 2 browser-closeout scope
2. a broader platform-program prioritization decision

## What to inspect

Read these docs first:

- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_recovery_completion.md`
- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_recovery_summary_2026-03-25.json`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_completion.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

Then inspect the implementation and proof paths the memo relies on:

The Critic:

- `/home/evgeny/projects/the-critic/api/server.py`
  - especially:
    - `GET /api/analysis/{workflow_key}/jobs/{job_id}`
    - `GET /api/analysis/{workflow_key}/results/{project_id}/{analysis_id}`
    - the live local snapshot backfill behavior for completed AOI v2 runs
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.test.ts`

Analyzer-v2:

- `src/orchestrator/task_planner.py`
- `src/presenter/compose_from_intent.py`
- `src/api/routes/presenter.py`

Look through any other recent memo/report/proof files in `communications/` or relevant `docs/` that materially affect the judgment.

## Questions to answer

1. Does the codebase support the scope as written, or does it rely on unverified assumptions about saved-result row selection, warm snapshot identity, or planner-backed compose routing?
2. Is the recovered fresh run technically and documentarily strong enough to count as `execution_backed`, or can this scope still quietly collapse into ambiguous fixture-backed reuse?
3. Is the memo right to freeze “no new AOI launch by default,” or is that too brittle operationally?
4. Are there hidden operational dependencies that make the step riskier or broader than the memo claims:
   - row ordering / selection ambiguity
   - browser URL state drift
   - local snapshot replacement
   - saved-result identity mismatch
   - missing artifact fields
5. Is one successful counted browser closeout on the recovered fresh run enough to support an honest Stage 2 closure decision under the frozen rubric and broader roadmap, or is that still too thin?
6. Is the memo right not to rerun the frozen pack again by default after this slice?
7. Does the memo keep the roadmap honest:
   - Stage 5 seam gate already passed
   - Stage 2 still open for now
   - Tranche 3 still blocked

## Output requirements

Write your audit to:

- `communications/REPORT_Codex_STAGE5_AOI_Execution_Backed_Browser_Closeout_Scope_Audit_2026-03-25.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve with revisions`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether the recovered fresh run is a valid counted `execution_backed` source for this slice.
5. A direct answer to whether one successful browser closeout on that run is enough for Stage 2 closure under the current rubric.
6. Any concrete memo revisions you recommend before execution.

Prioritize bugs, risks, hidden assumptions, evidence-quality gaps, row-selection ambiguity, scope dishonesty, and broader-program mis-sequencing over general summary.
