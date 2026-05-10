# Prompt For Codex: Audit Round-1 Proof Record Scope

Audit the proposed scope for the **next step after Phase 4** in the Thin Consumer Platformization program.

This is a scope audit for:

- **round-1 proof record and exit-criterion closure**

The goal is to test whether the scope memo matches the actual remaining obligations in the codebase and program docs, whether it stays narrow enough, and whether it hides any documentary or verification blockers.

## Files To Read First

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase2_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase3_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase4_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_round1_proof_record_scope.md`

Then inspect the real evidence seams:

- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.integration.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.test.tsx`

## Audit Questions

Please answer these by checking the code and memos, not by trusting the scope:

1. Is the next step correctly scoped as proof/evidence closure, or is some real implementation tranche still missing?
2. Can the final proof record honestly name exact Deliverable C job ids from existing evidence, or does the repo currently lack that documentary seam?
3. Is the proposed default of doing the Phase 4 manual checks and waiving the small Phase 2 manual tail technically defensible?
4. Is the “one tiny verification-only aid” boundary tight enough, or is it too vague and likely to reopen Deliverable C?
5. What exact files should the next implementer own first if this scope is accepted?
6. Is anything important missing from the proof-record acceptance criteria?

You may run safe targeted tests or inspection commands if they help validate assumptions.

## Output File

Write your audit to this exact file:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Codex_Round1_Proof_Record_Scope_Audit_2026-03-19.md`

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
