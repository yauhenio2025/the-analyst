Read the Phase 2 scoping memo and assess whether the scope is correct, too narrow, too broad, or missing critical risks.

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

1. Test whether the memo's extraction seam is real in the code, not just plausible on paper.
2. Identify the strongest arguments against this scope.
3. Identify any hidden coupling that would make the contract harder than the memo implies.
4. Check whether the memo accidentally leaves out an essential adopter, essential API, or essential verification step.
5. Be strict about non-goals. If the memo is allowing too much or too little, say so.

Do not implement anything.
Use non-mutating inspection only.

Write your opinion to this file:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Claude_Phase2_Consumer_Contract_Scope_Critique_2026-03-19.md`

Requirements for the report:

- title it clearly
- findings first, ordered by severity
- include file references where relevant
- state explicitly whether you agree that Phase 2 / Deliverable B should be the next tranche
- end with a short verdict: proceed, proceed with scope changes, or do not proceed
