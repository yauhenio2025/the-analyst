# Prompt For Claude: Stage 5 AOI Snapshot Durability Revision Scope Critique

Critique the draft memo:

- `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md`

Your job is to test the robustness of the memo’s assumptions against the actual codebase, recent memo/proof trail, and the broader analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “fix one more AOI bug.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- refuse premature Tranche 3 generalization before the AOI exemplar is ratified honestly

So evaluate the memo both as:

1. a bounded Stage 5 repair-scope decision
2. a broader-program prioritization decision

## What to inspect

Read these docs first:

- `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_diagnostic_stop_completion.md`
- `communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_revision.md`
- `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_completion.md`
- `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`
- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json`

Then inspect the code paths the memo depends on:

The Critic backend:

- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_client.py`

The Critic frontend:

- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.test.tsx`

Analyzer-v2 only as needed to confirm the memo is right to treat selector/provider work as closed baseline:

- `src/orchestrator/task_planner.py`
- `src/llm/client.py`

Look through any other recent memo/report/proof files in `communications/` that materially affect the judgment.

## Questions to answer

1. Does the evidence support treating warm snapshot durability and returned `source_analysis_id` truth as the first broken hop, rather than reopening planner or identity continuity?
2. Is the proposed repair slice honestly bounded, or is it smuggling in a larger persistence/lifecycle redesign?
3. Is the memo strict enough about fail-closed behavior if warm snapshot save fails?
4. Are the proposed regressions concrete enough to prove:
   - no non-persisted id is returned
   - no planner-backed navigation continues after warmup failure
   - repeated warmup/latest-snapshot continuity does not regress
5. Is the roadmap update now honest about how far along the program really is?
6. Does the memo preserve the right order:
   - fix the bounded host seam
   - rerun the same `evolution_ready` diagnostic
   - only then decide whether the frozen pack is earned
   - do not pivot phases
7. Is there any hidden code-path wrinkle that makes the next slice riskier, broader, or narrower than the memo claims?

## Output requirements

Write your critique to:

- `communications/REPORT_Claude_STAGE5_AOI_Snapshot_Durability_Revision_Scope_Critique_2026-03-25.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve after revision`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether the roadmap is now honest about progress or still overstated.
5. Any concrete memo revisions you recommend before implementation.

Prioritize hidden assumptions, proof-discipline gaps, scope dishonesty, broader-program mis-sequencing, and codebase mismatches over general summary.
