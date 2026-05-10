# Memo: Stage 8 / Task Intake And Workflow Routing Scope

Subtitle: Bounded Advisory Task Router Over Existing Downstream Contracts

Date: 2026-03-23
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Prior Stage Memo: `communications/MEMO_2026-03-23_stage7_planner_to_presentation_bridge_scope.md`
Stage 7 Completion: `communications/MEMO_2026-03-23_stage7_aoi_source_to_composition_bridge_completion.md`

## Purpose

Define the next stage-specific scope after the bounded Stage 7 AOI source-to-composition bridge landed.

This memo is about the next missing upstream seam:

- composition-facing task intake
- analyzer-owned workflow routing

It is **not** about another AOI consumer adoption slice.

## Why This Stage Now

Stage 7 changed the strategic position materially.

Two things are now simultaneously true:

1. analyzer-v2 now has a real AOI source-to-composition bridge behind `compose-from-source`
2. the system still requires the caller to arrive with an already-chosen workflow family and downstream route shape

So the next missing seam is no longer:

- can analyzer-v2 turn known AOI source truth into composition-ready material?

It is:

- can analyzer-v2 accept a composition-facing task/request and decide which workflow family should own the next move, without the consumer app deciding that analytically?

That is the real Stage 8 problem.

## Strategic Diagnosis

The current stack is still too workflow-explicit at the intake boundary.

Today the host still has to know too much:

- whether to launch AOI source-backed transient compose
- whether to launch an AOI job-backed path
- whether to launch genealogy execution
- which workflow key to pass

That was acceptable for the proof ladder that got the program here.
It is not acceptable as the long-term host contract.

Stage 8 should therefore attack this specific problem:

- remove consumer-owned analytical workflow choice from the intake boundary

## What Already Exists

The repo already contains real planning substrate plus partial routing ingredients:

- `src/orchestrator/planner.py`
- `src/orchestrator/adaptive_planner.py`
- `src/orchestrator/pipeline.py`
- `src/orchestrator/catalog.py`
- `src/orchestrator/schemas.py`
- `src/api/routes/orchestrator.py`
- `src/objectives/definitions/`

The repo also now contains real composition substrate:

- `src/presenter/compose_from_intent.py`
- `src/presenter/composition_source_bridge.py`
- `src/api/routes/presenter.py`

And the consumer side now has a real thin transient host path:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`

So Stage 8 should not be framed as greenfield routing from nothing.

But it should also not be overstated.

What exists today is mostly:

- planner-after-selection substrate
- objective-conditioned planning
- workflow-specific downstream launch contracts

What does **not** yet exist is a genuine composition-facing task router.

## What Does Not Yet Exist

There is still no host-callable contract that says:

- here is the analytical task
- here are the source constraints
- here are the audience/depth/style expectations
- analyzer-v2 will decide which workflow family should own the next move

That missing contract is the Stage 8 seam.

There is also still no unified downstream launch shape.

Current downstream contracts remain materially asymmetric:

- AOI transient source-backed launch is saved-result-oriented, fast, and transient
- genealogy launch is corpus/document-oriented, slower, and job-backed

Stage 8 must acknowledge that asymmetry instead of pretending both outcomes are peers in lifecycle or payload shape.

## Strategic Decision

Stage 8 should be:

- analyzer-owned
- route-first, not full-dispatch-first
- advisory, not dispatching
- bounded to a small routing outcome set
- host-contract-focused
- explicitly fail-closed

Stage 8 should **not** try to do all of the following at once:

- full engine/chain planning
- planner-driven page law
- cross-workflow source-backed composition
- lifecycle reopening
- dynamic app/session creation

Those belong to later stages.

## Bounded Claim For Stage 8

Stage 8 should prove one bounded thing:

- analyzer-v2 can accept a composition-facing task envelope without a consumer-supplied workflow key, route that task to a bounded workflow outcome set with explicit rationale and confidence, and return an advisory downstream launch contract that removes analytical workflow choice from the host without pretending that downstream AOI and genealogy launch shapes are already unified

That is enough to move the host boundary upstream without pretending the full dynamic-bespoke-app vision is already done.

## Recommended Stage 8 Shape

### Decision 1: make Stage 8 an advisory routing contract, not a union execution endpoint

Do **not** make Stage 8 a giant “do everything from task” route that sometimes:

- composes transient pages
- sometimes starts jobs
- sometimes returns errors

That would blur lifecycle regimes prematurely.

Instead, Stage 8 should introduce a bounded analyzer-owned routing contract that decides:

- which workflow family applies
- what downstream launch mode applies
- what source contract is required
- what host preparation is still required before an existing downstream endpoint can be called

Then the host can call the already-existing downstream endpoint described by that launch contract.

### Decision 2: the outcome set must contain more than one real routeable class

If Stage 8 only ever routes to AOI, it is not honest workflow routing.

The bounded outcome set should therefore include at least:

1. `aoi_transient_source_backed`
2. `genealogy_job_backed`
3. `unsupported`

This is the smallest routing space that proves the host is no longer choosing the workflow family.

These outcomes are intentionally asymmetric:

- `aoi_transient_source_backed`
  - saved-result identity, transient compose, seconds-scale
- `genealogy_job_backed`
  - corpus/document launch, job-backed execution, minutes-scale

That asymmetry is acceptable in Stage 8 as long as the contract is honest about it.

### Decision 3: keep the host contract thin, but do not pretend it is already unified

The host should not have to decide:

- `workflow_key`
- which planner family to use
- whether the task is “really AOI” or “really genealogy”

The host should provide:

- the task
- source constraints
- audience/depth/style expectations
- optional workflow hints

And it should receive back:

- the routing decision
- the routing confidence
- the required downstream launch contract
- the workflow-specific preparation still required

That is the honest Stage 8 claim:

- the host no longer decides the workflow analytically
- the host may still need to perform workflow-specific downstream preparation explicitly returned by analyzer-v2

### Decision 4: keep routing deterministic, explicit, and fail closed

Stage 8 is not a place for magic silent heuristics.

For this bounded 3-outcome space, routing should be deterministic.

Do **not** use an LLM router in Stage 8.

The router should use:

- bounded task semantics
- source-constraint sufficiency checks
- objective classification
- `baseline_workflow_key` from objective definitions
- explicit fail-closed thresholds

If the task does not map cleanly, the router should:

- return bounded failure / low-confidence output
- explain why
- avoid pretending certainty

## Proposed Public Contract

Stage 8 should add one analyzer-owned route under the orchestration namespace:

- `POST /v1/orchestrator/route-task`

The boundary matters more than the exact name:

- the host should ask analyzer-v2 to route the task
- the host should not route it analytically itself
- the route should be advisory

Stage 8 should **not** dispatch directly into:

- `compose-from-source`
- `analyze`
- `analyze-by-ref`

It should advise over those existing downstream endpoints.

## Proposed Request Envelope

Add a bounded task-intake schema, for example:

- `CompositionTaskRequest`

The request should include:

- `task`
  - free-text analytical ask
- optional `objective_hint`
- optional `audience`
- optional `desired_depth`
- optional `style_expectations`
- optional `source_constraints`
  - bounded source-family or identity hints
  - thinker/work/result constraints when present
- optional `workflow_hints`
- optional `consumer_key`

The important point is:

- no required `workflow_key`

If a caller already knows the workflow key, that may remain an optional hint.
It must not remain the primary required intake key for this stage.

This intake envelope should stay lightweight and advisory.

It should **not** try to unify:

- AOI saved-result transient launch payloads
- genealogy raw-document or by-ref execution payloads

Those remain downstream launch contracts for this stage.

## Proposed Response Contract

Add a bounded routing response, for example:

- `CompositionTaskRoutingDecision`

It should include at minimum:

- normalized task summary
- selected `objective_key`
- selected `workflow_key`
- routing outcome
  - `aoi_transient_source_backed`
  - `genealogy_job_backed`
  - `unsupported`
- routing confidence
- `launch_contract_kind`
- required downstream source contract
- `required_fields`
- `required_host_preparation`
- `source_sufficiency_status`
- downstream launch contract
- rejected workflow candidates with rationale
- trace entries for routing

The strongest Stage 8 routing signal should be:

- selected `objective_key`
- then `objective.baseline_workflow_key`

That mapping already exists in the objective definitions and should be used directly in this stage.

The host should be able to follow the response without analytically deciding the workflow itself, while still performing any workflow-specific preparation that the returned launch contract explicitly names.

## Concrete Stage 8 Routing Policy

For this stage, the router should be bounded and explicit.

### AOI routing outcome

Route to `aoi_transient_source_backed` only when:

- task semantics match AOI thematic single-thinker analysis
- the available source constraints are sufficient for an AOI source-backed path

The downstream launch contract should describe:

- selected workflow key
- required thinker/source identity constraints
- that the follow-on path is source-backed transient compose
- that the host is expected to call the existing source-backed transient path rather than a new Stage 8 dispatcher

### Genealogy routing outcome

Route to `genealogy_job_backed` only when:

- task semantics match genealogy-style execution
- the request has enough source/task structure to justify genealogy execution

The downstream launch contract should describe:

- selected workflow key
- required execution launch contract
- whether the host should use the existing `analyze` or `analyze-by-ref` path
- that the follow-on path is job-backed execution rather than source-backed transient compose

This outcome should be described honestly as:

- proof that the router can choose a non-AOI workflow family
- not proof that genealogy already has a composition-equivalent transient path

### Unsupported outcome

Return `unsupported` when:

- confidence is too low
- source constraints are insufficient
- the task does not map cleanly to the bounded workflow set

Do not silently coerce ambiguous tasks into AOI just because AOI transient compose currently exists.

## Relationship To Existing Endpoints

The intended Stage 8 flow is:

1. host calls `route-task`
2. analyzer-v2 returns an advisory routing decision plus downstream launch contract
3. host calls one of the existing downstream endpoints:
   - source-backed transient compose path
   - `analyze`
   - `analyze-by-ref`

Stage 8 should not duplicate those endpoints.

## What Stage 8 Must Not Do

Stage 8 should **not** do any of the following:

1. no direct engine/chain-plan synthesis yet
2. no planner-driven page law yet
3. no cross-workflow source-backed composition yet
4. no union execution/compose route that hides lifecycle differences
5. no app-specific workflow routing code
6. no fake “general routing” that only ever chooses AOI

It also should not pretend that:

- Stage 7’s AOI source-to-composition bridge already generalizes downstream composition across workflows
- current AOI and the-critic coupling is just incidental residue

## Relationship To Adjacent Roadmap Stages

### Relationship to Stage 7

Stage 7 made source-backed composition structurally legible once the workflow path is already known.

Stage 8 should remove the next host burden:

- choosing the workflow family in the first place

But Stage 7 remains AOI-only, the-critic-shaped, and composition-bounded.
It is not evidence that cross-workflow routing or downstream contract unification is already solved.

### Relationship to Stage 9

Stage 8 is **not** the general engine/chain planner stage.

It may use:

- objective definitions
- workflow metadata
- bounded routing heuristics

But it should not pretend to be full engine-plan synthesis.

### Relationship to Stage 13

Stage 8 is the first point where a minimal host contract starts to become explicit rather than implicit.

That is a feature, not a bug.

But the host contract is not solved here.
Current host thinness remains partial and workflow-shaped.

Real current coupling still includes:

- AOI-specific thinker identity propagation
- AOI-specific source-backed proxy contracts
- workflow-specific corpus shaping for AOI vs genealogy

Stage 8 should make those seams explicit rather than pretending they are already resolved.

## Recommended Proof Standard

Stage 8 proof should require at least:

1. one AOI task request routed to `aoi_transient_source_backed` without a consumer-supplied workflow key
2. one genealogy task request routed to `genealogy_job_backed` without a consumer-supplied workflow key
3. one ambiguous or borderline task that either routes with explicit discriminative rationale or fails closed as `unsupported`
4. one insufficient-source case that fails closed specifically because required source or corpus bindings are missing
5. saved routing traces showing:
   - selected workflow
   - rejected workflow candidates
   - confidence
   - source-contract reasoning
   - required host preparation

Proof should also require that the returned routing decision maps onto the **real current downstream contracts**, not just a plausible abstract route label:

- AOI routing must map onto the existing source-backed transient launch seam
- genealogy routing must map onto the existing `analyze` or `analyze-by-ref` seam

## Key Open Questions For Review

1. Is an advisory routing-only stage the right bounded move, or should Stage 8 directly dispatch into downstream paths?
2. Is `aoi_transient_source_backed` plus `genealogy_job_backed` plus `unsupported` the right bounded outcome set?
3. Should the new route live under `orchestrator`, `presenter`, or a new intake namespace?
4. Does the current codebase contain enough objective/workflow metadata to make this stage implementation-ready after revision?
5. What should count as “sufficient source constraints” for AOI vs genealogy in the first bounded router?

## Evidence Note

No relevant `Perspective` docs folder was found in either analyzer-v2 or the-critic during the Stage 8 review cycle.

## Recommendation

Stage 8 should be approved only if it stays disciplined:

- analyzer-owned advisory routing contract
- no consumer-owned analytical workflow choice
- more than one real workflow outcome
- explicit fail-closed behavior
- explicit downstream launch-contract asymmetry
- no fake leap into full engine planning or dynamic app/session generation

That is the right next upstream move after the bounded Stage 7 bridge.
