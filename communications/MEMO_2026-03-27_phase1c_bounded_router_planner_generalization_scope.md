# Memo: Phase 1C Bounded Router/Planner Generalization Scope

Subtitle: Add one non-AOI composition-facing planner path over the new bridge

Date: 2026-03-27
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Immediate Prior Completion: `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md`
Phase 1 Boundary Decision: `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
Relevant Prior Memos:
- `communications/MEMO_2026-03-23_stage7_planner_to_presentation_bridge_scope.md`
- `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`

## Purpose

Define the next bounded implementation slice after Phase 1A.

This memo is not another host-contract decision memo.
That work is already done in Phase 1B and implemented in Phase 1A.

The remaining Phase 1 gap is now narrower and clearer:

- the shared presenter handoff executor is reusable
- the host/runtime story is unified enough for the current surface set
- but `route-task` / `plan-task` still do not produce one non-AOI composition-facing handoff

So the next honest slice is:

- bounded router/planner generalization

not:

- more AOI repair
- another host/runtime rewrite
- lifecycle/session work
- second-consumer / Phase 2 proof work

## Current code-backed boundary

### What Phase 1A already solved

The current codebase now has all of these in place:

- Host Contract v2 with explicit `planner_advisory` and `delivery_runtime` layers
- immutable analyzer-owned planning snapshots fetched by `planning_decision_id`
- AOI planner-backed recovery that no longer depends semantically on `location.state`
- a shared transient handoff executor keyed by:
  - `workflow_key`
  - `handoff_kind`
- bounded non-AOI support for:
  - `workflow_key = intellectual_genealogy`
  - `handoff_kind = direct_sections`
  - `compose-from-intent`

Primary live files:

- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planning_schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/planning_decision_store.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`

### What is still asymmetric

The planner layer is still split in a way that blocks honest Phase 1 completion.

Current planner outcomes:

- AOI saved-result path:
  - routable
  - composition-facing
  - returns `aoi_composition_handoff_plan`
  - persists a stable `planning_decision_id`
- genealogy task-planned path:
  - routable
  - not composition-facing
  - returns `genealogy_execution_plan`
  - followup contract still points to `/v1/executor/jobs`

Current router constraint:

- genealogy still rejects `saved_result` source mode
- genealogy only routes for:
  - `registered_corpus`
  - `inline_documents`

Current host implication:

- the already-live genealogy task-planned path in `the-critic` backend is still an execution-launch adapter
- there is not yet one non-AOI planner path that lands on the new shared presenter bridge

That means the non-AOI proof from Phase 1A is still only materialization-level.
It is not yet planner-to-presentation proof.

### What bridge infrastructure is still missing

The missing work is not only a new planner branch.

The current genealogy path also lacks a result-to-sections bridge analogous in role to AOI's current source bridge.

Important current constraint:

- `src/presenter/composition_source_bridge.py` is AOI-specific today
- there is not yet a genealogy saved-result bridge that can extract bounded `ComposeFromIntentSectionInput` truth from durable genealogy result/view/artifact state

So Phase 1C must explicitly include one new bounded section-extraction layer.

Decision:

- do **not** refactor the existing AOI bridge into a full cross-workflow substrate in this slice
- do build one bounded genealogy saved-result section extractor, or one bounded generic result-to-sections adapter with genealogy as the first non-AOI implementation

Allowed analyzer-owned evidence sources for that extractor remain:

- bounded result metadata
- analyzer-owned presentation/view truth
- analyzer-owned artifacts or phase outputs already attached to the saved result

Not allowed:

- host-local semantic reconstruction
- re-running the genealogy analysis pipeline
- silently widening into a broad new cross-workflow extraction framework

## Strategic decision

The next bounded target should be:

- one genealogy result-backed composition-facing planner path over canonical `source_v2_job_id`

This slice should **not** overload the existing `registered_corpus` task-planned launch path with new semantics.

Why this is the right target:

1. It matches the Phase 1B identity doctrine:
   - canonical analyzer truth should be `source_v2_job_id`
2. It uses the same durable saved-result / planning-snapshot law already proven on the AOI side
3. It avoids conflating:
   - planning for analysis execution
   - planning for composition handoff
4. It generalizes the bridge beyond AOI without requiring a polished new app surface first

## Scope decision

Phase 1C should add one generic planner outcome for reusable `direct_sections` handoff, then exercise it first on bounded genealogy saved-result input.

This should be generic in contract shape, even if genealogy is the only new workflow using it in this slice.

Do **not** add a genealogy-specific shadow contract that merely repeats AOI’s old problem under a new name.

## Must land

### 1. Genealogy must become routable for one bounded `saved_result` composition path

`route-task` should accept one bounded genealogy `saved_result` path when canonical upstream result identity is present.

Required result:

- genealogy is no longer structurally excluded from `saved_result` source mode
- the router can distinguish:
  - genealogy task-planned execution over `registered_corpus` / `inline_documents`
  - genealogy composition-facing planning over `saved_result`

Must not widen:

- do not remove or weaken the current `registered_corpus` and `inline_documents` routes
- do not add open-ended source-mode support across every workflow

### 2. `plan-task` must add one generic composition-facing handoff outcome for `direct_sections`

Add one new planner outcome for the shared presenter bridge.

The new outcome should be generic, not genealogy-only.

Working shape:

- `planning_outcome_kind = direct_sections_composition_handoff_plan`

Required model:

- add one new planner payload model:
  - `DirectSectionsCompositionHandoffPlan`

The handoff payload should be sufficient to drive `compose-from-intent` without page-local reinterpretation.

Minimum required payload:

- `workflow_key`
- `objective_key`
- `consumer_key`
- canonical `source_v2_job_id`
- `compose_entrypoint_kind = presenter.compose_from_intent`
- one `resolved_intent_seed` or equivalent planner-owned composition directive
- materialized `prose_sections` ready for the shared `direct_sections` executor
- section ordering and provenance metadata
- bounded rationale / summary trace for why those sections were selected

This outcome should be representable inside the existing immutable planning snapshot system.

Resolved-intent policy for this slice:

- `resolved_intent_seed` remains required on the planner handoff model
- for genealogy saved-result composition, the planner should derive it from `task_request.task` first
- if the bounded genealogy proof does not need a richer directive than the user task already provides, the planner may emit one deterministic workflow-owned default seed rather than widening `SavedResultPlanningContext`
- do not widen `SavedResultPlanningContext` beyond canonical saved-result identity unless implementation proves `task_request` is insufficient

### 3. The public presenter boundary stays thin in this slice, so a lowering adapter is required

Decision:

- do **not** widen the public `POST /v1/presenter/compose-from-intent` request schema in this slice
- keep the current thin public request shape:
  - `workflow_key`
  - `consumer_key`
  - `user_intent`
  - bare `prose_sections[{engine_key,title,prose}]`
- allow richer planner-owned section metadata to exist only:
  - in the new planner handoff model
  - in the persisted planning snapshot
  - in the bounded proof adapter or harness that lowers that model into the current public request

Implementation implication:

- the first Phase 1C proof must include one thin lowering adapter or harness that executes:
  - `direct_sections_composition_handoff_plan`
  - into
  - `compose-from-intent`

The planner handoff may carry richer section ordering / role / provenance metadata than the public route accepts, but that metadata must be lowered honestly at the adapter boundary rather than pushed into page-local semantics.

Presenter constraint for the first proof:

- the first non-AOI proof must fit the current thin request honestly
- that means the returned genealogy `prose_sections` must already be classifiable from bounded analyzer-owned section truth
- and the first proof must avoid or neutralize any AOI-branded grouped-parent behavior that would make the result dishonest for a genealogy path

Default bounded rule:

- prefer constraining the first proof to a section set that the current public `compose-from-intent` request can consume honestly
- if that proves impossible without misleading AOI-specific presenter behavior, stop and write a revision memo instead of silently widening the public route

### 4. The first live use of that generic handoff outcome should be genealogy `saved_result`

The planner should be able to derive the direct-sections handoff from analyzer-owned durable genealogy result truth.

Allowed evidence sources:

- bounded result metadata
- analyzer-owned presentation/view truth
- analyzer-owned artifacts already attached to the saved result

Not allowed:

- host-local reconstruction of semantic sections
- re-running the genealogy analysis pipeline
- silently pivoting the composition-facing path back to `registered_corpus` execution launch

If the current genealogy saved-result truth is too thin to support honest direct-sections materialization, stop and write a revision memo instead of silently widening the slice.

Operational gate for this first proof:

- the first genealogy saved-result composition proof must succeed with analyzer-owned result/view/artifact truth that can materialize no more than 4 direct sections
- those sections must be produced without re-running analysis and without host-local semantic reconstruction

### 5. Immutable planning snapshots and runtime contracts must support the new outcome end to end

The persisted planning snapshot system added in Phase 1A must round-trip the new handoff outcome too.

That means:

- the new planner outcome can be persisted with `persist_decision=true`
- `GET /v1/orchestrator/planning-decisions/{planning_decision_id}` returns the exact direct-sections handoff snapshot
- no part of the new non-AOI handoff may depend semantically on in-memory page state

This is not only a planner-branch change.
It includes bounded schema/runtime follow-through.

Must land in scope:

- `task_routing_schemas.py`
  - expand the bounded routing/launch literals needed for a composition-facing genealogy saved-result path
- `task_planning_schemas.py`
  - add `direct_sections_composition_handoff_plan` to `PlanningOutcomeKind`
  - add one new `DownstreamReadiness` literal for the composition-facing direct-sections handoff
  - add `DirectSectionsCompositionHandoffPlan`
  - add one optional field on `TaskPlanningDecision` for that new handoff model
- `planning_decision_store.py`
  - generalize snapshot summary extraction so it is no longer AOI-only
- `taskLaunchRuntime.ts`
  - add the new planning outcome typing and persisted-snapshot consumption typing
- `hostContractV2.ts` and related runtime wiring
  - include the minimal planner-advisory/runtime follow-through needed for the proof surface to consume `planning_decision_fetch` if that proof surface is genealogy result-backed

Decision:

- this bounded schema/runtime follow-through is part of Phase 1C
- it does not reopen Phase 1B
- it is the minimum end-to-end contract work required to make the new planner outcome executable rather than theoretical

### 6. One thin executable adapter or harness is mandatory, not optional

This slice must add one thin execution layer sufficient to prove that the new planner outcome is actually consumable by the shared bridge.

Allowed forms:

- a focused analyzer integration harness
- a thin host/runtime adapter
- a deliberate proof-only path reusing existing runtime helpers

Not allowed:

- a polished new genealogy compose UI
- a broad consumer redesign
- a second-consumer product rollout

The goal is to make the path executable, not pretty.

Mandatory execution law:

- the adapter or harness must execute the returned planner handoff into the current `compose-from-intent` boundary
- it must not stop at planner JSON

Default preference:

- prefer a focused analyzer integration harness first, because there is no existing host-side genealogy composition consumer today
- a thin current-host adapter is allowed if needed, but it must reuse current runtime helpers rather than inventing new page-local semantics

## Must not widen

- do not reopen Phase 1B ownership decisions
- do not redesign Host Contract v2 again
- do not turn the genealogy task-planned backend path into a catch-all mixed execution/compose surface
- do not reopen lifecycle/session/share semantics
- do not add arbitrary open-ended workflow generation
- do not add browser polish or productization work that can wait for the proof slice
- do not claim Phase 2 host-neutral proof in this memo

## Acceptance tests

This scope is complete only if the implementation can demonstrate all of the following:

1. `route-task` no longer rejects the bounded genealogy `saved_result` composition path when canonical `source_v2_job_id` is present.
2. `plan-task` can return the new generic `direct_sections` handoff outcome for at least one bounded genealogy saved-result case.
3. the new planner outcome persists and reloads through `planning_decision_id` without loss of meaning.
4. the returned handoff payload can drive the shared `compose-from-intent` executor without AOI-only fields or AOI-only adapter logic.
5. the existing genealogy `registered_corpus` task-planned path still returns `genealogy_execution_plan` and still points to `/v1/executor/jobs`.
6. the slice yields one executable non-AOI planner-to-presentation proof path, even if it is only through a deliberate harness and not yet through a polished browser surface.
7. the first proof uses no more than 4 analyzer-owned direct sections and does not rely on host-local semantic reconstruction.

## Files that should anchor the implementation

Analyzer:

- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_routing_schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_router.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planning_schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/planning_decision_store.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/composition_source_bridge.py`
- `/home/evgeny/projects/analyzer-v2/src/executor/output_store.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/presentation_api.py`

Host / proof-side context:

- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/api/server.py`

## Final judgment

The next honest move after Phase 1A is not another contract memo and not Phase 2.

It is this bounded Phase 1C generalization:

- add one reusable non-AOI composition-facing planner outcome
- prove it first on genealogy saved-result truth
- keep the current execution-plan path intact
- stop before browser/product polish and broader host-neutral proof

That is the smallest slice that actually advances the planner-to-presentation bridge rather than merely restating it.
