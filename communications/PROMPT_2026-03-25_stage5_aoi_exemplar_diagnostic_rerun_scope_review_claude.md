# Prompt For Claude: Stage 5 AOI Exemplar Diagnostic And Rerun Scope Critique

Review the draft memo:

- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md`

Your job is to test the robustness of the memo’s assumptions, pressure-test them against the actual codebase and recent program record, and judge whether this is the right immediate next step in light of the broader analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “get one AOI rerun to pass.”
The target is still to make `analyzer-v2` the brain for dynamic bespoke analytical apps in general, with `the-critic` acting as the proving ground for host/product seams that can later support other apps and consumers.

So assess the memo both as:

1. a bounded Stage 5 rerun plan
2. a platform-program prioritization decision

## What to inspect

Read these docs first:

- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_revision_slice_completion.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_revision_slice_scope.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/PROOF_2026-03-24_stage5_aoi_exemplar_eval_pack.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_revision.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

Then inspect the code behind the memo’s claims, especially:

Analyzer-v2:
- `src/orchestrator/task_planner.py`
- `src/llm/client.py`

The Critic:
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`

Look through any other recent memo/proof/prompt files in `communications/` that materially affect the judgment.

## Questions to answer

1. Is the memo correctly keeping roadmap order intact rather than pivoting phases?
2. Is “diagnostic spot-check, then frozen rerun” the right next move now that the revision slice is implemented?
3. Is the branch rule honest enough:
   - proceed to full rerun only if the spot-check makes that meaningful
   - otherwise write a new revision memo
4. Is the memo sufficiently explicit about likely outcomes for Stage 5 vs Stage 2?
5. Is the `evolution_ready` spot-check the right first case?
6. Is there any hidden dependency in the codebase or recent memo trail that makes this rerun less meaningful than the memo claims?
7. Does the memo preserve the broader platform objective, or is it overfitting to AOI proof maintenance?

## Output requirements

Write your critique to:

- `communications/REPORT_Claude_STAGE5_AOI_Exemplar_Diagnostic_Rerun_Scope_Critique_2026-03-25.md`

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
5. Any concrete revisions you recommend before implementation.

Prioritize hidden assumptions, scope dishonesty, proof-quality risks, behavioral mismatches, and broader-program mis-sequencing over general summary.

