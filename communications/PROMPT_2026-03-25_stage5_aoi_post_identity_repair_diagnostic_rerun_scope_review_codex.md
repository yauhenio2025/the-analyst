# Prompt For Codex: Stage 5 AOI Post-Identity-Repair Diagnostic/Rerun Scope Audit

Audit the draft memo:

- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md`

Your job is to test the robustness of the memo’s assumptions against the actual codebase and recent memo/proof trail, and judge whether it is the right immediate next step given the broader analyzer-v2 platform goal.

## Bigger-picture objective

The target is not just “retry the proof.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- refuse premature de-AOI / de-`the-critic` generalization before the exemplar is ratified honestly

So assess the memo both as:

1. a bounded Stage 5 operational scope
2. a platform-program prioritization decision

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

Then inspect the code paths the memo depends on:

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

Analyzer-v2 only as needed to verify the memo’s claim that selector/provider work is now closed baseline:
- `src/orchestrator/task_planner.py`
- `src/llm/client.py`

Look through any other recent memo/report/proof files in `communications/` that materially affect the judgment.

## Questions to answer

1. Does the codebase evidence support treating the AOI identity-continuity blocker as repaired strongly enough to justify the next live diagnostic?
2. Is the memo correctly refusing to reopen selector/provider scope by default?
3. Is the branch rule strict enough to stop a dishonest frozen-rerun consumption if the repaired path still fails?
4. Are the artifact requirements concrete enough to make the next live decision auditable?
5. Does the memo preserve the right program order:
   - update the roadmap slightly
   - recalibrate the immediate plan
   - not pivot phases
6. Is there any hidden dependency or code-path wrinkle that makes the next rerun step riskier, narrower, or broader than the memo claims?
7. Is the memo honest that even after the identity repair, Stage 5 may still fail later for `selection_fit`, usefulness, or render-path reasons?

## Output requirements

Write your audit to:

- `communications/REPORT_Codex_STAGE5_AOI_Post_Identity_Repair_Diagnostic_Rerun_Scope_Audit_2026-03-25.md`

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
5. Any concrete revisions you recommend before execution.

Prioritize bugs, risks, hidden assumptions, scope dishonesty, proof-quality weaknesses, and broader-program mis-sequencing over general summary.
