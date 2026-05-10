# Prompt For Codex: Audit The Phase 3 Lifecycle Live Proof Closeout Scope

Audit the new Phase 3 live-proof closeout scope memo in the `analyzer-v2` workspace.

## Primary artifact to audit

- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_closeout_scope.md`

## Audit objective

Determine whether this memo is the correct immediate next step after the bounded Phase 3 lifecycle implementation landed and whether its claims are actually supported by the live codebase and recent roadmap/memo trail.

## Required work

Before writing your report, do all of the following:

1. Read the live-proof closeout memo carefully.
2. Check it against the active strategy and the latest implementation/roadmap docs:
   - `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_implementation_completion.md`
   - `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_scope.md`
   - `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`
   - `communications/MEMO_2026-03-27_phase2_host_neutral_transient_proof_scope.md`
   - `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_completion.md`
   - `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
3. Search `communications/` and `docs/` for any additional recent memos or reports that materially bear on:
   - lifecycle closeout
   - save/reopen proof
   - compose sessions
   - planning snapshots versus lifecycle identity
   - governance/evaluation sequencing
4. Audit the memo’s concrete claims against the live code, especially:
   - `/home/evgeny/projects/analyzer-v2/src/presenter/compose_session_store.py`
   - `/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py`
   - `/home/evgeny/projects/analyzer-v2/src/api/routes/presenter.py`
   - `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.test.tsx`

## Questions to answer explicitly

1. Is a bounded Phase 3 live proof closeout now the right next step, rather than a jump to Phase 4 governance/evaluation?
2. Is the memo right to keep the closeout on the existing genealogy proof page and generic direct-sections transient substrate?
3. Does the code support the memo’s claim that save/reopen is implemented but not yet live-proved?
4. Is the memo right that `session_id`, not `planning_decision_id`, is the truthful lifecycle identity for closeout?
5. Does the required evidence shape actually prove “no recomputation on reopen,” or is anything important missing?
6. Is the memo honest about what still remains out of scope?
7. Is anything in the memo contradicted by the code?
8. Is anything important missing that would make the closeout under-specified or unsafe to execute?

## Output requirements

Write your audit to exactly this file:

- `communications/REPORT_Codex_Phase3_Bounded_Lifecycle_V1_Live_Proof_Closeout_Scope_Audit_2026-03-28.md`

The audit should include:

1. A verdict:
   - `Approve`
   - `Approve with revisions`
   - `Reject`
2. Findings ordered by severity.
3. Concrete code-path verification or contradiction for the memo’s main claims.
4. A judgment on whether this is the right next step in the larger program sequence.
5. Any required revisions to make the memo solid enough for execution.

Do not edit the memo.
Do not make code changes.
This is a documentation/code-path audit only.
