# Prompt For Codex: Audit The Phase 3 Bounded Lifecycle V1 Scope Memo

Audit the new Phase 3 scope memo in the `analyzer-v2` workspace.

## Primary artifact to audit

- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_scope.md`

## Audit objective

Determine whether this memo is the correct bounded next step after the verified March 28 Phase 2 completion and whether its claims are actually supported by the live codebase and recent roadmap/memo trail.

## Required work

Before writing your report, do all of the following:

1. Read the Phase 3 memo carefully.
2. Check it against the active strategy and the latest completion docs:
   - `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`
   - `communications/MEMO_2026-03-27_phase2_host_neutral_transient_proof_scope.md`
   - `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_completion.md`
   - `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
   - `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
3. Search `communications/` and `docs/` for any additional recent memos or reports that materially bear on:
   - lifecycle
   - session/draft/revisit semantics
   - planning snapshots
   - transient compose
   - saved transient surfaces
   - Host Contract v2
   - older Stage 3 / Stage 14 direction work that may still matter
4. Audit the memo’s concrete claims against the live code, especially:
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/planning_decision_store.py`
   - `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
   - `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
   - `/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py`
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/direct_sections_compose_harness.py`
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`

## Questions to answer explicitly

1. Is the memo correct that the next program gap is now lifecycle law rather than more transient proof widening?
2. Is the memo right to choose the generic direct-sections transient path as the first lifecycle substrate instead of the AOI source-backed proxy path?
3. Does the current code support the memo’s claim that `planning_decision_id` is not enough to serve as truthful lifecycle identity?
4. Is there actually no existing save/reopen object in the live code that the memo is overlooking?
5. Does the proposed ownership split between analyzer session truth and host route/reopen execution match the current Phase 1B doctrine?
6. Is the memo honest about what must be stored to reopen without recomputation?
7. Is the retention rule sufficiently explicit for a bounded v1 slice?
8. Is anything in the memo contradicted by the code?
9. Is anything important missing that would make the scope under-specified or unsafe to implement?

## Output requirements

Write your audit to exactly this file:

- `communications/REPORT_Codex_Phase3_Bounded_Lifecycle_V1_Scope_Audit_2026-03-28.md`

The audit should include:

1. A verdict:
   - `Approve`
   - `Approve with revisions`
   - `Reject`
2. Findings ordered by severity.
3. Concrete code-path verification or contradiction for the memo’s main claims.
4. A judgment on whether this is the right next step in the larger program sequence.
5. Any required revisions to make the memo solid enough for implementation planning.

Do not edit the memo.
Do not make code changes.
This is a documentation/code-path audit only.
