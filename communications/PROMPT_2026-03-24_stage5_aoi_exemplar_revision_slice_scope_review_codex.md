# Prompt For Codex: Stage 5 AOI Exemplar Revision Slice Scope Audit

Audit the draft memo:

- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_revision_slice_scope.md`

Your job is to test the robustness of the memo’s assumptions against the actual codebase and recent program record, and to judge whether it is the right immediate next step given the broader analyzer-v2 platform goal.

## Bigger-picture objective

The target is not just “fix AOI in the-critic.”
The target is to make `analyzer-v2` the brain for dynamic bespoke analytical apps in general, with `the-critic` acting as the proving ground for host/product seams that can later support other apps and consumers.

So assess the memo both as:

1. an AOI revision-slice plan
2. a platform-program prioritization decision

## What to inspect

Read these docs first:

- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_revision_slice_scope.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/PROOF_2026-03-24_stage5_aoi_exemplar_eval_pack.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_revision.md`
- `communications/MEMO_2026-03-24_stage3_4_aoi_exemplar_cutover_completion.md`
- `communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

Then inspect the code behind the memo’s claims, especially:

Analyzer-v2:
- `src/orchestrator/task_planner.py`
- any files that define or use AOI selector timeout/provider behavior
- any files that shape `aoi_selection_blocked` outcomes

The Critic:
- `webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `webapp/src/lib/taskLaunchRuntime.ts`
- `webapp/src/pages/AoiComposeFromIntentPage.tsx`
- any nearby tests that already encode expected planner outcome behavior

## Questions to answer

1. Is the memo correctly keeping the roadmap order intact rather than pivoting phases?
2. Is the memo correctly narrowing the next move to:
   - selector/provider reliability
   - planner-outcome visibility
   and nothing broader?
3. Does the codebase evidence support treating the failure as a bounded proof-surface problem rather than a deeper architectural failure?
4. Is the “selector/provider reliability” bucket still too vague?
   - Should the memo more explicitly distinguish timeout tuning, env/config issues, provider transport failures, or bounded retry policy?
5. Is the “planner-outcome visibility” scope concrete enough to guide implementation?
6. Is keeping the Stage 5 case pack and rubric frozen the right decision?
7. Is the memo honest about Stage 2 remaining open?
8. Is there any hidden dependency that makes Tranche 3 pressure stronger than the memo admits?

## Output requirements

Write your audit to:

- `communications/REPORT_Codex_STAGE5_AOI_Exemplar_Revision_Slice_Scope_Audit_2026-03-24.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve with revisions`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether the roadmap should:
   - update slightly
   - recalibrate the immediate plan
   - not pivot phases
5. Any concrete revisions you recommend before implementation.

Prioritize bugs, risks, behavioral mismatches, hidden assumptions, and scope dishonesty over general summary.
