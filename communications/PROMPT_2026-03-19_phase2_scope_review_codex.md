Assess the Phase 2 scoping memo as an implementation-facing codebase audit.

Primary memo:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase2_consumer_contract_scope.md`

Required background:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_post_stage9_next_steps.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/PLAN_2026-03-18_thin_consumer_platformization_implementation.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase0_phase1a_completion.md`

Required codebase inspection targets:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts`
- `/home/evgeny/projects/the-critic/webapp/src/utils/presentationFreshness.ts`

Your task:

1. Verify that the duplicated bounded-v2 lifecycle logic is substantial enough to justify extraction now.
2. Scrutinize the proposed contract boundary:
   - what belongs in `boundedV2Client.ts`
   - what belongs in `useBoundedV2Workspace.ts`
   - what must stay page-local
3. Test the memo's assumptions with non-mutating inspection and any targeted non-mutating test commands you think are useful.
4. Identify likely implementation traps, especially around saved-result restore, refresh/cache behavior, polling transitions, and AOI-specific state.
5. Say whether `GenealogyPage` should stay out of the first adoption set or be pulled in immediately.

Do not implement anything.
Do not edit repo-tracked files other than writing your report.

Write your opinion to this file:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Codex_Phase2_Consumer_Contract_Scope_Audit_2026-03-19.md`

Requirements for the report:

- title it clearly
- present findings first with severity
- include concrete file references
- state whether the proposed scope is implementable without analyzer-v2 changes
- end with a short verdict: proceed, proceed with scope changes, or do not proceed
