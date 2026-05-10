# Prompt For Codex: Stage 5 AOI Exemplar Diagnostic And Rerun Scope Audit

Audit the draft memo:

- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md`

Your job is to test the robustness of the memo’s assumptions against the actual codebase and recent program record, and to judge whether it is the right immediate next step given the broader analyzer-v2 platform goal.

## Bigger-picture objective

The target is not just “rerun AOI.”
The target is still to make `analyzer-v2` the brain for dynamic bespoke analytical apps in general, with `the-critic` acting as the proving ground for host/product seams that can later support other apps and consumers.

So assess the memo both as:

1. a bounded Stage 5 diagnostic-and-rerun plan
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
- any files that define or consume AOI selector timeout/provider behavior

The Critic:
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`

Look through any other recent memo/proof/report files in `communications/` that materially affect the judgment.

## Questions to answer

1. Is the memo correctly keeping roadmap order intact rather than pivoting phases?
2. Is the memo correctly narrowing the next move to:
   - one diagnostic `evolution_ready` spot-check
   - then the same frozen rerun
   and nothing broader?
3. Does the codebase evidence support treating this as an operational proof step rather than another immediate coding slice?
4. Is the branch rule honest enough about when to stop and write a new revision memo instead of forcing a full rerun?
5. Is the memo explicit enough about likely Stage 5 pass / Stage 2 still-open outcomes?
6. Is there any hidden dependency that makes Tranche 3 pressure stronger than the memo admits?
7. Are the required artifacts and deliverables concrete enough for later audit?

## Output requirements

Write your audit to:

- `communications/REPORT_Codex_STAGE5_AOI_Exemplar_Diagnostic_Rerun_Scope_Audit_2026-03-25.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve with revisions`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether the program should:
   - update the roadmap slightly
   - recalibrate the immediate plan
   - not pivot phases
5. Any concrete revisions you recommend before implementation.

Prioritize bugs, risks, hidden assumptions, scope dishonesty, proof-quality weaknesses, and broader-program mis-sequencing over general summary.
