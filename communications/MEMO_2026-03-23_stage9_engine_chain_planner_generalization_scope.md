# Memo: Stage 9 / Engine-Chain Planner Generalization Scope

Subtitle: Route-Task To Hydration To Planning-Decision Normalization Over The Existing Orchestrator Substrate

Date: 2026-03-23
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Prior Stage Memo: `communications/MEMO_2026-03-23_stage8_task_intake_and_workflow_routing_scope.md`
Stage 8 Completion: `communications/MEMO_2026-03-23_stage8_task_intake_and_workflow_routing_completion.md`

## Purpose

Define the next bounded stage after Stage 8 advisory workflow routing.

This memo is about the next missing seam:

- routed task and objective truth
- hydration of real source and corpus context
- planner input synthesis
- bounded planning-decision normalization

It is not about:

- direct route-task to execution dispatch
- pretending the Stage 8 task envelope already equals planner-ready context
- broad AOI profile replacement
- cross-workflow source normalization
- semantic page planning

## Why This Stage Now

Stage 8 materially changed the program position.

Two things are now simultaneously true:

1. analyzer-v2 can accept a bounded composition-facing task envelope and route it without a consumer-supplied workflow key
2. analyzer-v2 still does not own a clean public contract for turning that routed task into either:
   - a real genealogy execution plan over existing planner substrate, or
   - a bounded AOI composition handoff over the existing Stage 7 bridge

That means the next missing seam is not simply:

- `route-task` -> `plan-task`

It is:

- `route-task` -> hydration -> planner input synthesis -> normalized planning decision

That is the real Stage 9 problem.

## Explicit Sequencing Note

The canonical roadmap still lists Stages 3-6 as not started.

Pulling Stage 7, Stage 8, and now Stage 9 forward is intentional, not an accidental skip.

The reason is simple:

- Stages 3-6 require a more analyzer-owned bridge between task understanding, downstream contracts, and planning truth
- Stage 7 established the first real AOI composition bridge substrate
- Stage 8 established the first real composition-facing task router
- Stage 9 should establish the first real route-plus-hydration-plus-plan seam

So 7-8-9 are bridge-infrastructure stages that later Stage 3-6 work can reuse rather than re-invent.

## Strategic Diagnosis

The current codebase already contains substantial planner substrate:

- `src/orchestrator/planner.py`
- `src/orchestrator/adaptive_planner.py`
- `src/orchestrator/pipeline.py`
- `src/orchestrator/catalog.py`
- `src/orchestrator/schemas.py`
- `src/orchestrator/pipeline_schemas.py`
- `src/objectives/definitions/`

It also now contains two upstream Stage 8 seams:

- `src/orchestrator/task_routing_schemas.py`
- `src/orchestrator/task_router.py`

And it already contains one real Stage 7 composition bridge:

- `src/presenter/composition_source_bridge.py`

So Stage 9 is not a greenfield planner stage.

But the Stage 8 public input is intentionally thin.

`CompositionTaskRequest` is advisory and metadata-heavy. It does not contain the real planner inputs that existing genealogy planning uses, such as:

- `thinker_name`
- `target_work`
- `prior_works`
- actual inline text or chapter text
- actual registered-corpus bindings already resolved into planner-ready context

The real planner seams still live behind richer contracts:

- `OrchestratorPlanRequest`
- `AnalyzeRequest`
- `AnalyzeByRefRequest`

So Stage 9 must not pretend that the Stage 8 task envelope can feed the existing planner directly.

## What Already Exists

The repo already contains real ingredients Stage 9 should reuse rather than replace:

- objective definitions with `baseline_workflow_key`
- planner-readable capability catalog assembly
- adaptive plan generation for genealogy-style execution planning
- workflow-aware execution plans through `WorkflowExecutionPlan`
- by-reference and inline execution launch paths
- AOI source-to-composition bridge substrate
- Stage 8 advisory task router

That means Stage 9 should be framed as:

- planner generalization and normalization over existing substrate

not:

- invent a second planner from nothing

## What Does Not Yet Exist

There is still no analyzer-owned public contract that says:

- here is the composition-facing task request
- here is the routing decision that was reused or recomputed
- here is whether hydration is sufficient to plan
- here is the normalized planning outcome kind
- here is the genealogy execution plan or AOI handoff metadata that follows
- here is whether downstream execution or composition is actually ready

There is also still no clean public distinction between:

- routing truth
- hydration truth
- execution-plan truth
- AOI composition-handoff truth
- later page-planning truth

That missing contract boundary is the Stage 9 seam.

## Strategic Decision

Stage 9 should be:

- analyzer-owned
- route-plus-hydrate-plus-plan, not execute
- explicit about when hydration is missing
- bounded and asymmetric where the codebase is genuinely asymmetric
- grounded in the existing orchestrator and Stage 7 substrate
- fail-closed when the system cannot produce a bounded nontrivial planning outcome

Stage 9 should not try to do all of the following at once:

- automatic downstream dispatch
- AOI task-driven profile replacement
- generalized source-family semantics across workflows
- page-law generalization
- broad objective expansion beyond the current AOI and genealogy slice

## Bounded Claim For Stage 9

Stage 9 should prove one bounded thing:

- analyzer-v2 can take the new Stage 8 task-intake boundary, hydrate the missing source and corpus context when available, and normalize the result into either a real genealogy execution plan or a bounded AOI composition handoff plan, without dispatching execution and without pretending all workflows already share a unified composition substrate

That is enough to turn Stage 8 routing into a real upstream planning seam.

## Recommended Stage 9 Shape

### Decision 1: add a planning boundary, not a dispatch endpoint

Do not make Stage 9 a route that:

- accepts a task
- routes it
- plans it
- executes it
- maybe composes it

That would collapse too many lifecycle regimes at once.

Instead, Stage 9 should introduce a bounded analyzer-owned planning contract, likely under the orchestration namespace, for example:

- `POST /v1/orchestrator/plan-task`

The important part is the boundary:

- the host asks analyzer-v2 for the bounded planning decision
- analyzer-v2 does not execute it
- analyzer-v2 does not compose from it automatically

### Decision 2: do not force a 3-step advisory chain

The system should not require every host to call:

1. `route-task`
2. `plan-task`
3. downstream execution or compose route

That would create avoidable advisory friction.

The cleaner contract is:

- keep `route-task` as a meaningful inspection and debugging seam
- let `plan-task` accept an optional prior routing decision
- if no prior routing decision is supplied, `plan-task` reruns routing internally and records that fact in its trace

That preserves Stage 8 as a real public seam without forcing every host into three round-trips.

### Decision 3: make hydration a first-class stage concern

This is the critical architectural correction.

Stage 9 should explicitly model planner readiness rather than pretending all routed tasks are plannable.

The stage should distinguish:

1. task envelope truth
2. routing truth
3. hydration truth
4. planner output truth

For genealogy, hydration may need to produce planner-ready context from:

- registered-corpus bindings
- inline documents and chapters

For AOI, hydration is narrower and still host-coupled:

- host-side resolution of `source_v2_job_id`
- bounded profile selection outside the planner

If hydration is insufficient, Stage 9 should return:

- `insufficient_context`

not:

- fake planning output
- thinly narrated JSON that looks like a plan but cannot drive anything real

### Decision 4: reuse `WorkflowExecutionPlan`, do not shadow it

The repo already has public plan substrate:

- `POST /v1/orchestrator/plan`
- `POST /v1/orchestrator/plan/adaptive`
- `WorkflowExecutionPlan`

So Stage 9 should not invent a parallel genealogy plan object with duplicate phase and engine fields.

Instead:

- genealogy planning should reuse `WorkflowExecutionPlan` as the embedded execution-plan payload
- the new Stage 9 value should be the normalization layer around it

The real delta beyond `WorkflowExecutionPlan` should be:

- reused or recomputed routing decision
- hydration status
- required hydration and host preparation
- planning outcome kind
- downstream readiness classification
- AOI composition-handoff metadata where genealogy's execution plan is not the right output
- one bounded planning trace that joins those pieces

### Decision 5: keep the stage honest about asymmetry

The downstream families are not symmetric.

Genealogy already has a meaningful nontrivial planner substrate.
AOI does not yet have generalized planner output. It has a bounded Stage 7 bridge plus fixed compose law.

So the honest bounded outcome set is:

1. `genealogy_execution_plan`
2. `aoi_composition_handoff_plan`
3. `insufficient_context`
4. `unsupported`

That asymmetry is acceptable if the contract is explicit.

### Decision 6: keep Stage 9 bounded to the current AOI and genealogy slice

The current Stage 8 router only supports:

- `influence_thematic`
- `genealogical`

The existence of `logical` objective definitions does not change the fact that current task-routing and planning scope is still narrow.

So Stage 9 should explicitly claim:

- bounded normalization over the current AOI and genealogy slice

It should not claim:

- broad objective coverage
- generalized higher-order planning across the objective space

## Proposed Planner Contract

Stage 9 should add a bounded planning contract, for example:

- `TaskPlanningRequest`
- `TaskPlanningDecision`

Recommended public input shape:

```text
TaskPlanningRequest
  task_request: CompositionTaskRequest
  prior_routing_decision: Optional[CompositionTaskRoutingDecision]
  planning_context: Optional[TaskPlanningContext]
```

The important design choice is:

- public input stays anchored on the Stage 8 task envelope
- the request may optionally reuse a prior routing decision
- planner-level context arrives through a separate `planning_context` block rather than being silently assumed to exist

That keeps Stage 8 meaningful while making the input-contract gap explicit.

## Proposed Hydration Layer

Stage 9 should make the hydration seam visible in contract and trace form.

Recommended internal flow:

1. validate or compute routing decision
2. inspect `planning_context`
3. synthesize one bounded planner-ready context
4. either:
   - emit a real planning outcome, or
   - emit `insufficient_context` with explicit missing prerequisites

The planner-ready context should be workflow-specific.

Examples:

- `GenealogyByRefPlanningContext`
- `GenealogyInlinePlanningContext`
- `AoiSourceBackedPlanningContext`

The exact class names can change, but the seam should not.

## Proposed Decision Output

Recommended shape:

```text
TaskPlanningDecision
  normalized_task_summary
  routing_decision: CompositionTaskRoutingDecision
  planning_outcome_kind:
    genealogy_execution_plan |
    aoi_composition_handoff_plan |
    insufficient_context |
    unsupported
  planning_confidence
  hydration_status: satisfied | required | unresolved
  required_hydration: list[...]
  required_host_preparation: list[str]
  downstream_readiness:
    ready_for_genealogy_execution |
    ready_for_aoi_compose_handoff |
    needs_more_context |
    unsupported
  workflow_execution_plan: Optional[WorkflowExecutionPlan]
  aoi_composition_handoff_plan: Optional[AoiCompositionHandoffPlan]
  rejected_planning_alternatives: list[...]
  trace: list[...]
```

That is the actual Stage 9 delta.

`WorkflowExecutionPlan` remains the genealogy execution payload.
`TaskPlanningDecision` is the analyzer-owned normalization layer around route, hydration, readiness, and handoff truth.

## Genealogy Scope

Stage 9 should prove a real nontrivial genealogy planning path.

But it should only do that when the system has enough hydrated context to call the real planner honestly.

That means:

- reuse existing adaptive and legacy planning substrate
- synthesize a real planner request from registered-corpus or inline context
- return an embedded `WorkflowExecutionPlan`
- fail closed with `insufficient_context` when the routed task lacks planner-ready material

Stage 9 should not claim:

- bare-task adaptive planning from the Stage 8 envelope alone
- planner output that looks real but is not backed by planner-usable context

## AOI Scope

AOI Stage 9 output should be described narrowly and concretely:

- bounded AOI-specific handoff metadata over the Stage 7 source bridge

It should not be described as generalized planner output.

What the AOI side should name:

- expected producer engines
- expected AOI source families
- compose entrypoint family
- required host preparation
- bounded downstream prerequisites that remain outside Stage 9

What it should stay explicit about:

- `source_v2_job_id` resolution is still host-side preparation
- `profile` selection is still fixed downstream law
- current source-family vocabulary is AOI-specific, not generalized planner substrate
- current host adoption remains the-critic-coupled

## AOI Handoff Plan Sketch

Stage 9 should include a concrete AOI output shape, for example:

```text
AoiCompositionHandoffPlan
  workflow_key
  consumer_key
  compose_entrypoint_kind: presenter.compose_from_source
  required_host_preparation:
    - resolve source_v2_job_id
    - choose allowed profile
  expected_producer_engines
  expected_source_families
  bridge_contract_targets:
    - CompositionSourceCatalog
    - CompositionSourceSelection
  allowed_profiles:
    - dossier
    - comparison
  handoff_notes
```

This makes the AOI boundary testable.

It also makes the relationship to the live Stage 7 substrate explicit:

- `CompositionSourceCatalog`
- `CompositionSourceSelection`

The AOI handoff plan sits above that bridge.
It does not replace the bridge and it does not replace `profile`.

## What Stage 9 Must Not Do

Stage 9 must not do the following:

1. no consumer-runtime adoption work in the-critic by default
2. no automatic dispatch from `plan-task` into `analyze`, `analyze-by-ref`, or `compose-from-source`
3. no fake unification of AOI and genealogy downstream lifecycle
4. no claim that planner-level source-family semantics are generalized across workflows
5. no Stage 10 source-normalization claims
6. no Stage 11 page-planning claims
7. no AOI task-driven profile replacement yet

## Proof Standard

Stage 9 proof should require more than saved narrated JSON.

Required proof cases:

1. one genealogy task that reaches a real `WorkflowExecutionPlan` through explicit hydration and planner input synthesis
2. one AOI task that produces a bounded AOI handoff plan matching live downstream law, including `source_v2_job_id` preparation and fixed `profile` prerequisites
3. one `insufficient_context` or `unsupported` case that fails closed honestly

Those artifacts should show:

- selected objective and workflow
- whether routing was reused or recomputed
- hydration status
- required hydration and host preparation
- planning outcome kind
- embedded execution plan or AOI handoff metadata
- rejected planning alternatives
- bounded planning trace

Required verification should include:

- contract tests for the new planning outcome taxonomy
- contract tests for optional prior-routing reuse versus rerouting
- at least one live genealogy proof showing route-task to hydration to planner input synthesis to real plan output
- at least one AOI proof showing Stage 9 output still respects the live Stage 7 and compose-from-source law

## Why This Is The Right Next Stage

Stage 8 solved:

- "who owns the next move?"

Stage 9 should solve:

- "is there enough real context to plan?"
- "what bounded planning outcome follows if there is?"

Without Stage 9, the program still has:

- task intake and routing on one side
- execution and composition machinery on the other

but no explicit analyzer-owned contract that joins them honestly.

That is the missing seam if analyzer-v2 is actually going to become the intelligence layer rather than only a bounded router plus bounded presenter.

## Explicit Non-Claims

Stage 9 does not claim:

- full task-to-engine freedom
- broad objective coverage
- cross-workflow source-backed composition
- generic dynamic app generation
- page-law generalization
- removal of AOI host-side identity and profile obligations

It is a bounded route-plus-hydrate-plus-plan stage over the current AOI and genealogy slice.

## Note On Perspective Docs

No relevant Perspective docs folder has been identified in analyzer-v2 or the-critic.
That fact should remain explicit in review and planning so nobody assumes a missing design corpus is silently driving the architecture.
