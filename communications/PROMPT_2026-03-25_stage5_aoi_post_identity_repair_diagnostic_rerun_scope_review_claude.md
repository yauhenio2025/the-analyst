# Prompt For Claude: Stage 5 AOI Post-Identity-Repair Diagnostic/Rerun Scope Critique

Review the draft memo:

- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md`

Your job is to test the robustness of that memo’s assumptions, examine them against the codebase and the recent memo/proof trail, and judge whether this is the right immediate next step in light of the larger analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “run another AOI proof.”

The target remains:

- make `analyzer-v2` the brain for dynamic bespoke analytical apps in general
- use `the-critic` as the current proving ground for host/product seams
- avoid promoting Tranche 3 or broader generalization before the AOI exemplar is honestly ratified

So assess the memo both as:

1. a bounded Stage 5 operational scope
2. a platform-program sequencing decision

## What to inspect

Read these docs first:

- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_completion.md`
- `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_diagnostic_stop_completion.md`
- `communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_revision.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_revision_slice_completion.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_revision_slice_scope.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`
- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json`

Then inspect the code behind the memo’s claims, especially:

The Critic backend:
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_client.py`

The Critic frontend:
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts`

Analyzer-v2 only as needed to verify the memo’s claim that planner/selector work is now closed baseline:
- `src/orchestrator/task_planner.py`
- `src/llm/client.py`

Look through any other recent memo/report/proof files in `communications/` that materially affect the judgment.

## Questions to answer

1. Is the memo correctly narrowing the next move to one fresh repaired-path diagnostic and, only if earned, the same frozen rerun?
2. Does the codebase evidence support the memo’s claim that the AOI identity-continuity blocker is now code-fixed strongly enough to deserve a live re-diagnostic?
3. Is the memo honest about what this next step does and does not buy us?
   - it can re-earn the rerun
   - it does not imply Stage 5 or Stage 2 closure in advance
4. Is the artifact/branch discipline strong enough to prevent a dishonest rerun consumption if the repaired path still fails?
5. Does the memo preserve the right program order:
   - update the roadmap slightly
   - recalibrate the immediate plan
   - do not pivot phases
6. Is there any hidden dependency in the codebase or recent communications trail that would make this rerun step less meaningful than the memo claims?
7. Is the memo staying properly bounded, or is it accidentally smuggling in broader AOI or Tranche 3 work?

## Output requirements

Write your critique to:

- `communications/REPORT_Claude_STAGE5_AOI_Post_Identity_Repair_Diagnostic_Rerun_Scope_Critique_2026-03-25.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve after revision`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether the program should:
   - update the roadmap slightly
   - recalibrate the immediate plan
   - not pivot phases
5. Any concrete revisions you recommend before execution.

Prioritize hidden assumptions, scope dishonesty, code/behavior mismatches, proof-discipline risks, and broader-program mis-sequencing over general summary.
