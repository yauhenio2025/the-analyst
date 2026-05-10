# Prompt For Codex: Audit Phase 4 / Deliverable D Scope

Audit the proposed scope for **Phase 4 / Deliverable D: Cross-Workflow Generic Workspace Proof**.

The goal is to test whether the scope memo matches the actual code seam in `the-critic`, whether it stays narrow enough, and whether it hides any contract or routing assumptions that will break implementation.

## Files To Read First

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase3_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_roadmap_after_phase3.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase4_cross_workflow_workspace_scope.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`

Then inspect the real code:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useWorkflowMetadata.ts`
- `/home/evgeny/projects/the-critic/api/server.py`

## Audit Questions

Please answer these by checking the code, not by trusting the memo:

1. Is Deliverable D really frontend-first in `the-critic`, or is there a hidden backend blocker?
2. Is query-param thinker context the right minimum contract for AOI on the generic route?
3. Does `AnalysisWorkspacePage` already have the right shape to support genealogy + AOI without reopening Phase 2?
4. Will local saved-result behavior create thinker-mixing or route confusion?
5. Is any part of the memo drifting toward a dynamic-form system, a route rewrite, or a bespoke-page replacement?
6. What exact files should implementation own first if this scope is accepted?

You may run safe targeted tests or inspection commands if they help validate assumptions.

## Output File

Write your audit to this exact file:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Codex_Phase4_Cross_Workflow_Workspace_Scope_Audit_2026-03-19.md`

## Output Requirements

Your audit must include:

1. `Verdict`
2. `Blocking Issues`
3. `Non-Blocking Risks`
4. `Assumptions Tested`
5. `Recommended Scope Tightening`
6. `Implementation Starting Point`

Please be direct and specific.
If the scope is sound, say so.
If it is not, point to exact code and explain the mismatch.

Do not edit product code in this pass.
Only write the audit memo.
