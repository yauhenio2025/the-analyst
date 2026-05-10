# Prompt For Claude: Phase 1C Bounded Router/Planner Generalization Scope Critique

Critique the newly drafted Phase 1C scope memo:

- `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_scope.md`

Your job is to test the robustness of the assumptions behind that memo against:

- the actual current codebase in `analyzer-v2` and `the-critic`
- the recent March 26-27 roadmap and memo trail
- the bigger program objective of making `analyzer-v2` the analytical brain while downstream apps become thin hosts

## Bigger-picture objective

Evaluate the memo in light of the real target:

- analyzer-v2 should own analytical understanding, routing, planning, composition law, and presentation law
- current apps should be proving harnesses, not long-term workflow-specific controllers
- Phase 1 should generalize the bridge before Phase 2 tries to prove broader host-neutral consumption

So judge the memo both as:

1. a bounded next implementation scope after Phase 1A
2. a program-sequencing decision about what still must happen before Phase 1 can honestly be treated as complete

## What to inspect first

Read these docs before writing your critique:

- `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_scope.md`
- `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md`
- `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-23_stage7_planner_to_presentation_bridge_scope.md`
- `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`

Then search `communications/` and `docs/` for any additional recent memos or reports that materially bear on:

- planner-to-presentation bridge
- host contract / Host Contract v2
- task routing / task planning
- genealogy launch and planner adoption
- persistent planning snapshots
- source identity doctrine

## Code paths to inspect

Analyzer:

- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_routing_schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_router.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planning_schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/planning_decision_store.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`

Host:

- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/api/server.py`

## Questions to answer directly

1. Is the memo correct that the main remaining Phase 1 gap is now planner asymmetry rather than another host-contract gap?
2. Is the memo right that the current non-AOI proof is only materialization-level, not planner-to-presentation proof?
3. Is `genealogy + saved_result + generic direct_sections handoff` the right bounded target, or is the memo choosing the wrong non-AOI seam?
4. Does the code support the memo’s claim that genealogy is currently excluded from `saved_result` routing and still terminates in `genealogy_execution_plan` plus `/v1/executor/jobs`?
5. Is the proposed new generic planner outcome genuinely reusable, or does it risk becoming a genealogy-only shadow contract?
6. Is the memo appropriately strict about not overloading the existing `registered_corpus` task-planned launch path with new composition semantics?
7. Is the memo missing any deeper blocker:
   - thin genealogy saved-result truth
   - missing provenance needed for direct-sections handoff
   - hidden host/runtime dependence
   - mismatch between planner output and shared `compose-from-intent` input law
8. Does the memo stay properly sequenced relative to:
   - completed Phase 1B decisions
   - completed Phase 1A implementation
   - the not-yet-earned Phase 1 end-of-phase browser/harness proof
   - later Phase 2 host-neutral consumption proof?
9. Is it concrete enough to guide implementation safely, or does it still leave critical boundary choices unresolved?

## Output requirements

Write your critique to exactly this file:

- `communications/REPORT_Claude_Phase1C_Bounded_Router_Planner_Generalization_Scope_Critique_2026-03-27.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve after revision`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether this is now the right next honest step.
5. A direct answer to whether the memo stays properly bounded.
6. Any concrete revisions needed before implementation.

Prioritize hidden assumptions, codebase mismatches, scope drift, and roadmap mis-sequencing over general summary.

Do not edit the memo.
Do not make code changes.
This is a documentation/code-path critique only.
