# Memo: Phase 2 Host-Neutral Transient Proof Scope

Subtitle: Prove the generalized bridge beyond the current AOI / `the-critic` surface without reopening lifecycle

Date: 2026-03-27
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Immediate Prior Completion: `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_completion.md`
Relevant Prior Memos:
- `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
- `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md`
- `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md`
- `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_scope.md`
- `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`

## Purpose

Define the next bounded implementation slice after Phase 1 closes.

This memo is not another bridge-generalization memo.
That work is now done tightly enough for the current roadmap line.

The remaining missing proof is different:

- the AOI browser-exercisable transient proof still lives in `the-critic`
- the new non-AOI genealogy planner-to-presentation proof is still an analyzer-side lowering/integration harness
- `aoi-canary` is still only a result-backed second-consumer proof, not a transient one

So the next honest step is:

- stronger host-neutral transient proof

not:

- more Phase 1 router/planner widening
- another host-contract ownership memo
- AOI-local browser polish
- lifecycle/session work

## Current code-backed boundary

### What Phase 1 already solved

The current codebase now has all of these in place:

- Host Contract v2 as the executable runtime story for planner-advisory plus delivery/runtime law in the current consumer
- immutable `planning_decision_id` snapshots for durable AOI planner-backed recovery
- a shared transient handoff executor keyed by:
  - `workflow_key`
  - `handoff_kind`
- one bounded non-AOI materialization path through `direct_sections`
- one bounded non-AOI planner-to-presentation path:
  - `intellectual_genealogy`
  - `saved_result`
  - canonical `source_v2_job_id`
  - `direct_sections_composition_handoff_plan`
  - persisted planning snapshot
  - thin fail-closed lowering into the existing public `compose-from-intent` boundary

Primary files now carrying that reality:

- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_router.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/planning_decision_store.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/direct_sections_compose_harness.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/genealogy_saved_result_bridge.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`

### What is still not proved

The program still does not have one stronger transient proof beyond the current AOI / `the-critic` surface.

Current proof state:

- AOI:
  - real browser-exercisable transient proof in `the-critic`
- genealogy:
  - real planner-to-presentation proof only through an analyzer integration harness
- `aoi-canary`:
  - real second-consumer proof only for result-backed run/result/presentation contracts

That means the current missing seam is not:

- planner asymmetry
- lack of a reusable transient handoff executor
- lack of planning snapshots

It is:

- whether a thin host-neutral or second-surface transient consumer can consume analyzer-owned planning/presentation law without rebuilding workflow-specific intelligence locally

### Current live constraint that Phase 2 must name explicitly

The current transient compose boundary is not yet open to arbitrary new consumer identities.

Today:

- analyzer transient compose still validates `consumer_key` against `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS`
- that registry is currently only:
  - `{"the-critic"}`
- many presenter-facing schemas still default `consumer_key` to `the-critic`

This means a new proof harness cannot honestly invent a new transient `consumer_key` unless bringing transient consumer registration explicitly into scope.

There is also one setup constraint on the target seam:

- the genealogy saved-result bridge does not start fresh execution
- it reads analyzer-owned durable truth from the executor database:
  - `get_job(...)`
  - `load_phase_outputs(...)`
- so the proof requires one pre-existing completed genealogy job with the expected saved-result truth already present

## Strategic decision

The next bounded target should be:

- one minimal dedicated transient proof harness that sits outside the current AOI page/controller path while reusing the existing `the-critic` transient consumer registration by default

Default target workflow:

- `intellectual_genealogy + saved_result + source_v2_job_id + direct_sections_composition_handoff_plan`

Why this is the right first proof target:

1. It uses the newly generalized non-AOI planner path rather than re-proving AOI-only seams.
2. It uses the thinnest current public presenter boundary:
   - `POST /v1/presenter/compose-from-intent`
3. It avoids smuggling AOI-specific host proxy/continuity alias semantics into what is supposed to be a host-neutral proof.
4. It proves the Phase 1 bridge matters outside the current AOI page/controller shape.

AOI remains important in Phase 2, but as:

- the already-earned current-consumer transient reference path

not as:

- the main place where the new proof burden should land

Explicit default for this slice:

- reuse the current `the-critic` transient consumer registration and runtime surface unless transient consumer registration itself is deliberately brought into scope
- do not assume that “new proof harness” automatically means “new registered transient consumer”

## Scope decision

Phase 2 should add one stronger transient proof surface, not another architecture rewrite.

The proof surface should be:

- a minimal dedicated host-neutral transient proof harness

not:

- a new polished app
- more `the-critic` page-local work
- a rebranded AOI-specific harness

Default rule for proof-vehicle selection:

- do not extend `aoi-canary` into a workflow-specific transient app unless the implementation can show that it consumes the current bridge with no new workflow-local analytical intelligence
- by default, reuse the existing `the-critic` transient consumer registration and runtime surface
- only if the slice explicitly chooses to widen scope to transient consumer registration should it introduce a new transient `consumer_key` / consumer adapter
- otherwise build a new minimal proof harness whose only job is to consume the current contract/runtime law honestly while still presenting itself to analyzer transient compose as `consumer_key=the-critic`

## Must land

### 1. One transient proof surface outside the current AOI / `the-critic` page stack

The new slice must produce one proof vehicle that is not the current AOI page/controller path in `the-critic`.

The harness may still be thin and ugly.
It does not need product polish.

But it must be a real consumer of the current bridge, not another internal analyzer test.

### 2. One real non-AOI transient planner-to-presentation chain consumed by that harness

The minimum required live chain is:

1. `route-task` with explicit `consumer_key`
2. `plan-task(persist_decision=true)` with explicit `consumer_key`
3. `GET planning-decisions/{id}`
4. honest analyzer-owned lowering into the current thin presenter request
5. `POST /v1/presenter/compose-from-intent` with explicit `consumer_key`
6. rendered/consumable transient presentation in the proof harness

This chain must stay on:

- genealogy `saved_result`
- canonical `source_v2_job_id`
- `direct_sections_composition_handoff_plan`

It must not silently fall back to:

- `registered_corpus`
- `/v1/executor/jobs`
- host-local section synthesis

Setup requirement:

- the proof target must be one pre-existing completed genealogy `saved_result`
- the slice does not earn credit by starting fresh genealogy execution and then quietly proving an execution path instead of the saved-result transient path

### 3. The harness must stay host-neutral at the semantic boundary

The harness may own generic consumption concerns such as:

- calling named contract families or analyzer endpoints
- threading `consumer_key`
- carrying `planning_decision_id`
- fetching the persisted planning snapshot
- invoking the thin compose request
- rendering the returned presentation payload

Lowering ownership is explicit in this slice:

- honest lowering from `DirectSectionsCompositionHandoffPlan` into the thin public `ComposeFromIntentRequest` remains analyzer-owned
- the authoritative default lowering point is the existing analyzer-side direct-sections lowering boundary
- the proof harness must consume that lowering result or a thin analyzer-owned proof helper over the same logic
- the proof harness must not reimplement direct-sections lowering semantics locally

The harness must not own workflow-specific analytical intelligence such as:

- source selection
- section extraction
- title derivation from raw analyzer phase outputs
- AOI/genealogy-specific planner reinterpretation
- local reconstruction of grouped parent meaning

Consumer-key rule:

- thread `consumer_key` explicitly at every hop
- do not rely on Pydantic or presenter defaults that happen to fall back to `the-critic`

If truthful consumption would require those local semantic moves, stop and write a revision memo.

### 4. The proof must make the contract boundary auditable

The proof artifact set must make it obvious that the harness consumed the current generalized law rather than bypassing it.

Minimum required evidence should include:

- one live request/response trace for the proof chain
- one rendered-state artifact from the harness
- one explicit negative proof that invalid or missing planning identity fails closed
- one explicit note showing that the proof path does not depend on `the-critic` AOI proxy routes or `/v1/executor/jobs`

## Optional early borrow

If one narrow transient surface token or ephemeral session identifier is strictly required to make the proof honest, it may be introduced early here.

But the rule is:

- ephemeral only
- proof-scoped only
- no draft/session/share semantics
- no automatic promotion into Phase 3 lifecycle law

If the proof does not actually require that token, do not invent it.

## Must not widen

- do not reopen Phase 1 router/planner generalization
- do not reopen Phase 1B ownership doctrine
- do not build a fake “generic host” that hides workflow logic in local glue
- do not turn this into a lifecycle/session tranche
- do not add a new polished end-user app
- do not treat `aoi-canary` result-backed proof as if it already answered the transient question
- do not let the proof quietly depend on `the-critic`-specific AOI proxy behavior
- do not silently widen the slice into new transient consumer registration without naming that as an explicit scope change

## Exit test

Phase 2 is complete only when the program can show, with evidence:

- one transient planner-to-presentation chain outside the current AOI / `the-critic` page stack
- no hidden host-local workflow-specific analytical reconstruction
- one non-AOI live proof surface that consumes the generalized bridge honestly
- stronger transient evidence than the already-closed result-backed `aoi-canary` Tier A proof

## Why this stays Phase 2 and not Phase 3

This slice is still about transient proof, not lifecycle law.

It should answer:

- can a thin non-current-consumer surface consume the bridge honestly?

It should not answer:

- what is a durable analytical session?
- what gets saved, revisited, or shared?
- how long does a transient surface live?

Those remain later questions.
