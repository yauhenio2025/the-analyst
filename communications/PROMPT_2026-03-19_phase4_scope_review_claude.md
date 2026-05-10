# Prompt For Claude: Review Phase 4 / Deliverable D Scope

You are reviewing the proposed scope for **Phase 4 / Deliverable D: Cross-Workflow Generic Workspace Proof**.

Your job is to scrutinize the scope memo against the real codebase and tell me where the plan is wrong, blurry, too wide, too narrow, or hiding assumptions.

## Files To Read First

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase3_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_roadmap_after_phase3.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase4_cross_workflow_workspace_scope.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`

Then inspect the real proving-vehicle code in `the-critic`:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useWorkflowMetadata.ts`
- `/home/evgeny/projects/the-critic/api/server.py`

## What To Test

Please test the scope memo's assumptions, not just summarize it.

In particular, check:

1. Is the generic workspace already close enough that Deliverable D can stay `the-critic`-first?
2. Is explicit query-param thinker context the right seam, or is that hiding a better/worse contract?
3. Does the generic route already accept the AOI bounded parameters it needs?
4. Can generic AOI discovery really be thinker-scoped with the current shared client/hook and current local result payloads?
5. Is there any hidden blocker that would force analyzer-v2 changes?
6. Is the scope still too broad in any place?
7. Is anything important missing from the proof definition or acceptance criteria?

You may run safe local inspection commands and targeted tests if useful.

## Output File

Write your review to this exact file:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Claude_Phase4_Cross_Workflow_Workspace_Scope_Critique_2026-03-19.md`

## Output Requirements

Your report must include these sections:

1. `Verdict`
2. `Findings`
3. `Assumptions Tested`
4. `Scope Corrections`
5. `Suggested Acceptance Criteria Changes`
6. `Recommended Next Move`

Please be concrete.
If you think the scope is right, say so plainly.
If you think it is wrong, point to exact files/lines and explain why.

Do not edit product code in this pass.
Only write the review memo.
