# Prompt For Claude: Review Round-1 Proof Record Scope

You are reviewing the proposed scope for the **next step after Phase 4** in the Thin Consumer Platformization program.

This is not a new product-feature tranche.
It is the proposed scope for:

- **round-1 proof record and exit-criterion closure**

Your job is to scrutinize the scope memo against the real codebase, the prior completion memos, and the execution brief, and tell me where the scope is wrong, blurry, too wide, too narrow, or hiding documentary assumptions.

## Files To Read First

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase2_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase3_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase4_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_round1_proof_record_scope.md`

Then inspect the real evidence surfaces:

- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.integration.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.test.tsx`

## What To Test

Please test the scope memo's assumptions, not just summarize it.

In particular, check:

1. Is the next step really a proof-record/evidence-closure step rather than another feature step?
2. Is it safe to recommend waiving the small Phase 2 manual tail by default, or is that too optimistic?
3. Do the current Deliverable C proof surfaces actually support naming exact genealogy job ids in a final proof record, or is a tiny verification-only harness likely required?
4. Is the proposed “one small verification-only analyzer-v2 aid” the right escape hatch, or does that hide real implementation drift?
5. Is the memo missing any evidence item required by the execution brief's exit criteria?
6. Is anything in the scope too broad, especially around manual reruns or analyzer-v2 follow-up work?

You may run safe local inspection commands and targeted tests if useful.

## Output File

Write your review to this exact file:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Claude_Round1_Proof_Record_Scope_Critique_2026-03-19.md`

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
