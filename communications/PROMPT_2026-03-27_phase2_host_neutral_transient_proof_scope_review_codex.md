# Prompt For Codex: Audit The Phase 2 Host-Neutral Transient Proof Scope Memo

Audit the new Phase 2 scope memo in the `analyzer-v2` workspace.

## Primary artifact to audit

- `communications/MEMO_2026-03-27_phase2_host_neutral_transient_proof_scope.md`

## Audit objective

Determine whether this memo is the correct bounded next step after the verified Phase 1C implementation and whether its claims are actually supported by the live codebase and recent roadmap/memo trail.

## Required work

Before writing your report, do all of the following:

1. Read the Phase 2 memo carefully.
2. Check it against the active strategy and the latest Phase 1 docs:
   - `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_completion.md`
   - `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
   - `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
   - `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md`
   - `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_scope.md`
3. Search `communications/` and `docs/` for any additional recent memos or reports that materially bear on:
   - host-neutral proof
   - transient compose
   - planning snapshots
   - Host Contract v2
   - `aoi-canary`
   - genealogy saved-result direct-sections planning
4. Audit the memo’s concrete claims against the live code, especially:
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_routing_schemas.py`
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_router.py`
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planning_schemas.py`
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py`
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/planning_decision_store.py`
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/direct_sections_compose_harness.py`
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/genealogy_saved_result_bridge.py`
   - `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
   - `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
   - `/home/evgeny/projects/the-critic/api/server.py`
   - `/home/evgeny/projects/aoi-canary/src/App.tsx`
   - `/home/evgeny/projects/aoi-canary/src/lib/resultsClient.ts`

## Questions to answer explicitly

1. Is the memo correct that the remaining program gap is now stronger host-neutral transient proof rather than more Phase 1 bridge work?
2. Is a minimal dedicated proof harness really the right default vehicle, or does the current codebase suggest a better bounded option?
3. Is the memo right to target genealogy `saved_result` transient proof first rather than AOI proxy-backed transient proof or another execution-oriented genealogy seam?
4. Does the current code support the memo’s claim that the proof can stay off:
   - `the-critic` AOI proxy routes
   - `/v1/executor/jobs`
   - host-local section synthesis?
5. Is the memo honest about what `aoi-canary` already proves and what it does not?
6. Is anything in the memo contradicted by the code?
7. Is anything important missing that would make the scope under-specified or unsafe to implement?
8. Is the optional ephemeral token/session borrow properly bounded, or is it likely to blur Phase 2 into Phase 3 lifecycle work?
9. Is this scope narrow enough to stay Phase 2 rather than drifting into productization, another contract rewrite, or lifecycle design?

## Output requirements

Write your audit to exactly this file:

- `communications/REPORT_Codex_Phase2_Host_Neutral_Transient_Proof_Scope_Audit_2026-03-27.md`

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
