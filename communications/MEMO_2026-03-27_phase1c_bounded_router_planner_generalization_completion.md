# Memo: Phase 1C Bounded Router/Planner Generalization Completion

Date: 2026-03-27
Status: Phase 1C implemented and verified; Phase 1 now closes honestly
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Scope Memo: `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_scope.md`
Depends on:
- `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`
- `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
- `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md`

## Summary

Phase 1C is now implemented.

This slice closes the remaining Phase 1 planner asymmetry without reopening Phase 1B or widening into Phase 2:

- `route-task` now supports one bounded genealogy `saved_result` composition-facing branch over canonical `source_v2_job_id`
- `plan-task` now emits one generic `direct_sections_composition_handoff_plan` and persists it through the existing immutable `planning_decision_id` snapshot law
- analyzer-v2 now has one bounded genealogy saved-result bridge that derives truthful direct sections from durable analyzer-owned result truth only
- the first non-AOI planner-to-presentation proof now exists through a thin fail-closed lowering harness into the existing public `compose-from-intent` boundary
- the existing genealogy `registered_corpus -> genealogy_execution_plan -> /v1/executor/jobs` path remains unchanged

The honest program state is now:

- Phase 1B: complete
- Phase 1A: complete
- Phase 1C: complete
- Phase 1 overall: complete
- next step: Phase 2 stronger host-neutral transient proof

## What landed

### 1. Router and planner contracts now support one bounded non-AOI composition-facing path

The planner is no longer AOI-only at the composition-facing outcome layer.

What is now true:

- `RoutingOutcome` includes `genealogy_transient_source_backed`
- `LaunchContractKind` includes advisory `planner.direct_sections_compose_handoff`
- genealogy `saved_result` routing now succeeds only when canonical `source_v2_job_id` is present
- `PlanningOutcomeKind` includes `direct_sections_composition_handoff_plan`
- `DownstreamReadiness` includes `ready_for_direct_sections_compose_handoff`
- `TaskPlanningDecision` can now carry `direct_sections_composition_handoff_plan`

Important boundary:

- the new router launch contract remains advisory and still points to `plan-task`
- it does not dispatch directly to `compose-from-intent`

Primary files:

- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_routing_schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_router.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planning_schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py`

### 2. Genealogy saved-result truth now has one bounded analyzer-side section bridge

Phase 1C required more than new enums.
It required one honest non-AOI way to derive presentation-ready direct sections without host-local semantic reconstruction.

That now exists in bounded form:

- `genealogy_saved_result_bridge.py` derives direct sections only from analyzer-owned saved-result truth
- it validates that the saved genealogy run exists and is completed
- it reads durable phase outputs rather than re-running the genealogy workflow
- it derives bounded section titles from workflow-owned defaults / engine metadata
- it caps the handoff at `4` sections and currently uses a preferred bounded pair:
  - `Relationship Comparison Map`
  - `Genealogy Report`

Not allowed and not used:

- host-local section reconstruction
- analyzer re-execution
- AOI bridge widening disguised as generalization

Primary file:

- `/home/evgeny/projects/analyzer-v2/src/orchestrator/genealogy_saved_result_bridge.py`

### 3. Planning snapshots and the lowering harness now round-trip the new handoff honestly

The new non-AOI handoff is not a planner JSON dead end.

What is now true:

- planning snapshot persistence now extracts summary fields from either:
  - `aoi_composition_handoff_plan`
  - `direct_sections_composition_handoff_plan`
- persisted planning decisions round-trip the new non-AOI handoff outcome through `planning_decision_id`
- the new lowering harness converts the richer internal handoff into the current thin public `ComposeFromIntentRequest`
- lowering is fail-closed if role-sensitive meaning would be lost

This is the key proof boundary:

- the public `compose-from-intent` request stayed thin
- richer planner metadata stayed internal
- the new proof works by honest lowering, not by silently widening the presenter API

Primary files:

- `/home/evgeny/projects/analyzer-v2/src/orchestrator/planning_decision_store.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/direct_sections_compose_harness.py`

### 4. Presenter and host-runtime follow-through landed without reopening Phase 1B

The non-AOI path now has the runtime/schema follow-through it needed.

What changed:

- non-AOI grouped parent labels are workflow-neutral rather than AOI-branded
- genealogy engine keys now resolve cleanly through the presenter’s role/classification path
- Host Contract v2 now includes `planning_decision_fetch` on the genealogy result-backed surface
- `taskLaunchRuntime.ts` now understands:
  - `genealogy_transient_source_backed`
  - `direct_sections_composition_handoff_plan`

Primary files:

- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`

## Verification

Analyzer verification passed:

- `PYTHONPATH=. pytest -q tests/test_task_router.py tests/test_task_planner.py tests/test_compose_from_intent.py tests/test_phase1c_genealogy_direct_sections.py tests/test_genealogy_saved_result_bridge.py`

Result:

- `69 passed`

Host/runtime verification passed:

- `CI=true npm test -- --runInBand --watchAll=false src/lib/hostContractRuntime.test.ts src/lib/taskLaunchRuntime.test.ts`

Result:

- `14 passed`

Verification notes:

- Python emitted only existing deprecation warnings
- there were no failing assertions
- no new live browser proof was run in this slice because the scoped end-of-phase proof vehicle was the deliberate analyzer-side lowering/integration harness

## Boundary after Phase 1C

Phase 1 now closes honestly.

Why the Phase 1 exit bar is now satisfied:

- the transient/planner-to-presentation substrate is no longer structurally single-workflow-only:
  - AOI has a composition-facing handoff plan
  - genealogy now has one bounded composition-facing `direct_sections` handoff plan
- the transient/planner-to-presentation substrate is no longer structurally single-consumer-only at the contract boundary:
  - consumer validation is registry/adaptor-based rather than `consumer_key == the-critic`
- one reusable handoff contract exists:
  - the shared workflow/handoff executor plus the generic `direct_sections` handoff path
- one non-AOI planner-to-presentation path now exists:
  - genealogy `saved_result -> route-task -> plan-task(persist_decision=true) -> planning_decision_fetch -> lowering -> compose-from-intent`
- host ownership decisions were already locked in Phase 1B and implemented in Phase 1A
- the generalized bridge now has both:
  - one real browser-exercisable AOI integration path
  - one deliberate non-AOI analyzer integration harness

What is still not claimed:

- no stronger host-neutral transient proof exists yet beyond the current AOI/the-critic browser surface plus the deliberate analyzer harness
- no lifecycle/session semantics are reopened here
- no second transient browser consumer is claimed here

## Next honest step

The next step is Phase 2:

- stronger host-neutral transient proof beyond the current AOI/the-critic surface

That next slice should not reopen:

- Phase 1B ownership doctrine
- Phase 1A host-contract/runtime unification
- Phase 1C planner asymmetry repair
- lifecycle/session semantics

The main missing proof is now consumption beyond the current consumer, not more bridge reshaping.
