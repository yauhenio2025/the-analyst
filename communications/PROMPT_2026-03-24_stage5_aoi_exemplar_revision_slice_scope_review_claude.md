# Prompt For Claude: Stage 5 AOI Exemplar Revision Slice Scope Review

Please review the draft memo:

- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_revision_slice_scope.md`

Your task is to test the robustness of the assumptions behind that memo, examine them in light of the bigger picture and the overall program objective, scrutinize the memo’s claims against the live codebase, and inspect any relevant recent memos in `communications/` or adjacent docs before reaching a verdict.

## Bigger-picture objective

The program goal is not merely to improve AOI inside `the-critic`.
The goal is to make `analyzer-v2` the intelligence layer on top of which we can build many kinds of analytical apps, with `the-critic` serving as the main guinea pig and proving the generalizable host/product seams needed for later consumers.

So your critique should evaluate this memo in two frames at once:

1. Is it the right immediate next step for the AOI exemplar?
2. Is it the right immediate next step for the broader analyzer-as-brain platformization effort?

## Review tasks

Please do all of the following:

1. Read the revision-slice scope memo carefully.
2. Read the most relevant recent supporting memos and proof docs, including at minimum:
   - `communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md`
   - `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
   - `communications/PROOF_2026-03-24_stage5_aoi_exemplar_eval_pack.md`
   - `communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_revision.md`
   - `communications/MEMO_2026-03-24_stage3_4_aoi_exemplar_cutover_completion.md`
   - `communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
   - `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`
3. Inspect the codebase claims behind the memo, especially around:
   - AOI selector/provider behavior in:
     - `src/orchestrator/task_planner.py`
   - any AOI selector timeout / provider-path configuration implicated by `llm_provider_failure`
   - AOI planner result handling in:
     - `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
     - `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
     - `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
4. Check whether the memo’s proposed revision scope is truly bounded, or whether it is quietly reopening broader architectural questions.
5. Check whether the memo is appropriately refusing a phase pivot.
6. Identify any missing assumptions, hidden risks, or places where the memo overstates or understates what the next slice needs to do.
7. Pay special attention to whether “selector/provider reliability” is scoped concretely enough, or whether it needs sharper decomposition such as:
   - environment/config
   - timeout budget
   - provider-path fragility
   - bounded fallback policy
8. Pay special attention to whether “planner-outcome visibility” is scoped correctly as a proof-surface stability fix rather than a UI redesign.

## Output requirements

Write your output to:

- `communications/REPORT_Claude_STAGE5_AOI_Exemplar_Revision_Slice_Scope_Critique_2026-03-24.md`

Your output should include:

1. A one-line verdict:
   - `Approved`
   - `Approved after revision`
   - `Not approved`
2. Findings ordered by importance.
3. Clear explanation of whether the memo is aligned with the bigger program objective.
4. Clear explanation of whether the roadmap recalibration is correct:
   - update slightly
   - recalibrate immediate plan
   - do not pivot phases
5. Any concrete revisions you think should be made before implementation.

Please keep the review concrete and evidence-based.
Do not just restate the memo.
