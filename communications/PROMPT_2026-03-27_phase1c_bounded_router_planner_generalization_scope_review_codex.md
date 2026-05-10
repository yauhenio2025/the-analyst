# Prompt For Codex: Audit The Phase 1C Bounded Router/Planner Generalization Scope Memo

Audit the new Phase 1C scope memo in the `analyzer-v2` workspace.

## Primary artifact to audit

- `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_scope.md`

## Audit objective

Determine whether this memo is the correct bounded next step after the verified Phase 1A bridge implementation and whether its claims are actually supported by the live codebase and the recent roadmap/memo trail.

## Required work

Before writing your report, do all of the following:

1. Read the Phase 1C memo carefully.
2. Check it against the active strategy and latest Phase 1 docs:
   - `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md`
   - `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
   - `communications/MEMO_2026-03-23_stage7_planner_to_presentation_bridge_scope.md`
3. Search `communications/` and `docs/` for any additional recent memos or reports that materially bear on:
   - planner-to-presentation bridge
   - task routing / task planning
   - genealogy task-planned launch
   - planning snapshots
   - host contract / Host Contract v2
4. Audit the memo’s concrete claims against the live code, especially:
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_routing_schemas.py`
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_router.py`
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planning_schemas.py`
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py`
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/planning_decision_store.py`
   - `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
   - `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx`
   - `/home/evgeny/projects/the-critic/api/server.py`

## Questions to answer explicitly

1. Is the memo correct that the remaining Phase 1 gap is now at the router/planner layer rather than another host-contract or AOI-local seam?
2. Does the code support the memo’s claim that the planner is still asymmetric:
   - AOI gets a composition-facing handoff plan
   - genealogy gets an execution plan and `/v1/executor/jobs` followup?
3. Is the memo right to target `saved_result` genealogy composition planning rather than extending the existing `registered_corpus` task-planned launch path?
4. Is the proposed generic `direct_sections` planner outcome technically coherent with the existing shared transient handoff executor?
5. Would the proposed scope actually produce a non-AOI planner-to-presentation path, or only another analyzer-only proof that still bypasses the planner?
6. Is anything in the memo contradicted by the code?
7. Is anything important missing that would make the scope under-specified or unsafe to implement?
8. Is this scope narrow enough to stay Phase 1C, rather than drifting into browser productization, lifecycle work, or Phase 2 proof?

## Output requirements

Write your audit to exactly this file:

- `communications/REPORT_Codex_Phase1C_Bounded_Router_Planner_Generalization_Scope_Audit_2026-03-27.md`

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
