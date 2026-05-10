# Memo: Phase 1A Planner-To-Presentation Bridge Completion

Date: 2026-03-27
Status: Phase 1A implemented and verified; Phase 1 remains open
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Depends on:
- `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`
- `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`

## Summary

Phase 1A is now implemented.

This slice landed the first real post-Phase-1B bridge work:

- Host Contract v2 is now the executable runtime story for planner-advisory plus delivery/runtime families in the current consumer
- AOI planner-backed handoff is now durable through immutable analyzer-owned planning snapshots instead of semantic `location.state`
- transient presenter entry is no longer AOI-shaped at the shared executor boundary for `direct_sections`
- one bounded non-AOI materialization path now exists through that same shared executor

What this does **not** mean:

- Phase 1 is not complete
- planner outputs are still asymmetrical across workflows
- genealogy still does not have a composition-facing planner path
- the end-of-phase browser-exercisable generalized proof still does not exist

So the honest program state is:

- Phase 1B: complete
- Phase 1A: complete
- Phase 1 overall: still partial
- next step: Phase 1C bounded router/planner generalization

## What landed

### 1. Host Contract v2 now owns planner-advisory runtime law

The Critic no longer treats `route-task` / `plan-task` as a floating sidecar beside the host contract.

What is now true:

- Host Contract v2 exists as the authoritative runtime artifact
- planner-advisory families are explicit:
  - `task_route`
  - `task_plan`
  - `planning_decision_fetch`
- `taskLaunchRuntime.ts` now dispatches through the same host-contract runtime used by the existing delivery/runtime families

This closes the Phase 1B contract-split problem in code, not only in prose.

Primary files:

- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`

### 2. AOI planner-backed recovery now uses immutable analyzer-owned planning identity

The AOI compose path no longer depends semantically on task replay or `location.state`.

What is now true:

- `plan-task` can persist immutable planning decisions
- `TaskPlanningDecision` can carry `planning_decision_id`
- analyzer-v2 serves `GET /v1/orchestrator/planning-decisions/{planning_decision_id}`
- the AOI panel now navigates with `planning_decision_id`
- the AOI compose page now recovers its planner-backed state from the persisted snapshot
- `location.state` is now provisional cached display state only, not durable truth

This is the Phase 1B durability rule implemented in code.

Primary files:

- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planning_schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/planning_decision_store.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`

### 3. The shared transient handoff executor is now genuinely reusable for `direct_sections`

Analyzer transient composition is no longer locked to AOI law at the shared executor boundary.

What is now true:

- `compose-from-intent`
- `compose-from-source`
- `compose-from-selection`

now resolve through one shared internal handoff executor keyed by:

- `workflow_key`
- `handoff_kind`

What also changed:

- consumer validation is registry-based
- workflow/handoff capability validation is registry-based
- AOI remains registered for:
  - `direct_sections`
  - `source_profile`
  - `source_selection`
- genealogy is now registered for:
  - `direct_sections`

The important boundary change is not merely weaker validators.
It is that AOI is now one adapter into a shared executor rather than the contract itself.

Primary file:

- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`

### 4. One bounded non-AOI materialization path now exists

Phase 1A required more than contract cleanup.
It required at least one non-AOI path through the new bridge substrate.

That now exists in bounded form:

- `workflow_key = intellectual_genealogy`
- entrypoint: `compose-from-intent`
- handoff kind: `direct_sections`
- executor path: the same shared internal handoff executor used by AOI

This is still materialization-level proof, not yet planner-facing proof.
That distinction matters for the next slice.

## Verification

Analyzer verification passed:

- `PYTHONPATH=. pytest -q tests/test_task_planner.py tests/test_compose_from_intent.py`

The Critic verification passed:

- `CI=true npm test -- --runInBand --watchAll=false src/lib/hostContractRuntime.test.ts src/lib/taskLaunchRuntime.test.ts src/pages/AoiComposeFromIntentPage.test.tsx src/components/influence/AoiV2ThematicPanel.test.tsx`

Verification notes:

- both suites passed
- the Jest run still emitted the existing React `act(...)` console warnings in `AoiV2ThematicPanel.test.tsx`
- there were no failing assertions

## Boundary after Phase 1A

Phase 1A closes these previously-open seams:

- planner-advisory runtime now belongs to the host contract story
- planner-backed AOI recovery no longer depends semantically on `location.state`
- transient presenter entry is no longer structurally AOI-only for the shared `direct_sections` path
- one non-AOI materialization path now exists through the shared handoff executor

Phase 1A does **not** close these still-open seams:

- `route-task` / `plan-task` still produce a composition-facing handoff only for AOI
- genealogy task planning still resolves to `genealogy_execution_plan` plus `/v1/executor/jobs`
- genealogy does not yet have a non-AOI composition-facing planner outcome
- the generalized bridge is not yet proven through a non-AOI browser/harness path

This is why Phase 1A is complete while Phase 1 overall remains partial.

## Next honest step

The next step is Phase 1C:

- bounded router/planner generalization to support one non-AOI composition-facing path

That next slice should not reopen:

- Phase 1B ownership decisions
- AOI-local UI repair
- lifecycle/session semantics
- broad second-consumer or host-neutral proof work

The correct remaining gap is planner asymmetry, not another host-contract memo.
