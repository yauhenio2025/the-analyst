# Prompt For Claude: Stage 5 AOI Execution-Backed Browser Closeout Scope Critique

Critique the new browser-closeout scope doc:

- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_scope.md`

Your job is to test the robustness of the assumptions behind that memo against the actual codebase, the recent Stage 5 memo/proof trail, and the broader analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “capture one more browser screenshot.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- close the AOI exemplar honestly before Tranche 3 generalization

So evaluate the new memo both as:

1. a bounded next-step scope for finishing the missing execution-backed browser evidence
2. a broader program-prioritization decision about what should happen before Stage 2 can close and before Tranche 3 can move

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

Then inspect the code paths the memo depends on:

The Critic:

- `/home/evgeny/projects/the-critic/api/server.py`
  - especially:
    - `GET /api/analysis/{workflow_key}/jobs/{job_id}`
    - `GET /api/analysis/{workflow_key}/results/{project_id}/{analysis_id}`
    - the local snapshot backfill path for completed v2 AOI runs
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

Also look through any other recent memo/report/proof files in `communications/` or relevant `docs/` that materially affect the judgment.

## Questions to answer

1. Is using the recovered fresh run `job-6ee8b0621177` / `gen-v2-18853b558ef1` as the counted source still honest for `execution_backed`, or does the recovery step weaken that claim?
2. Does the codebase actually support the memo’s required identity discipline:
   - explicit saved-result row selection
   - planner-backed handoff from that row
   - warm snapshot returning/preserving the right `analysis_id`
   - `/compose-from-intent` preserving the same `source_v2_job_id`
   - `compose-from-selection` using that exact source
3. Is the memo right not to authorize a new AOI launch by default, or is relying on the recovered run too brittle or too easy to mis-document?
4. Does the memo under-specify any operational hazards:
   - row ordering / “latest result” ambiguity
   - local DB drift
   - recovery vs. fresh-launch ambiguity in the artifact trail
   - browser artifact capture weakness
5. Is one successful recovered execution-backed browser case enough for an honest Stage 2 closure decision under the frozen rubric, or does the memo over-read that bar?
6. Does the memo keep the bigger picture honest:
   - Stage 5 seam gate already passed
   - Stage 2 still open until this slice closes
   - Tranche 3 still blocked
7. Is the step appropriately narrow, or is it still smuggling in broader closure by implication?

## Output requirements

Write your critique to:

- `communications/REPORT_Claude_STAGE5_AOI_Execution_Backed_Browser_Closeout_Scope_Critique_2026-03-25.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve after revision`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether using the recovered fresh run is still an honest `execution_backed` counted source.
5. A direct answer to whether one successful browser closeout on that run is enough for Stage 2 closure under the current rubric.
6. Any concrete memo revisions you recommend before execution.

Prioritize hidden assumptions, evidence-tier dishonesty, scope leakage, browser-path ambiguity, artifact weakness, roadmap overclaim, and codebase mismatches over general summary.
