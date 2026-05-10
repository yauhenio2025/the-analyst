# Memo: Phase E Representative Composition Matrix Scope

Subtitle: The first bounded generality proof over the live analyzer-owned compose surfaces already in repo

Date: 2026-03-30
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-30_phase_d_cross_campaign_planner_to_presentation_governance_v1_completion.md`

## Purpose

Define the first bounded Phase E step after the Phase D exit signal was met.

This memo is intentionally not another Phase D governance memo.
The question now is no longer whether analyzer-v2 can govern bounded proofs.
The question is whether analyzer-v2 can already compose and render across a small but representative matrix of live handoff and output families without per-app intelligence.

## Strategic Framing

The right first Phase E move is not:

- another governance family
- a second consumer proof
- arbitrary-engine combinatorics
- generic plugin architecture
- UI productization

The right first Phase E move is:

- a representative composition matrix over the live analyzer-owned compose surfaces already supported in repo

That means proving one common contract law over multiple input/handoff families using the same host boundary and the same served response shape.

The point is not to prove every engine or pass one by one.
The point is to prove that analyzer-owned composition law is already broad enough that new supported shapes can be served without host-specific analytical reconstruction.

## Why This Is The Right Next Slice

The repo already has three materially different live composition families:

- AOI `source_profile` via `POST /v1/presenter/compose-from-source`
- AOI `source_selection` via `POST /v1/presenter/compose-from-selection`
- genealogy `direct_sections` via planner-backed analyzer-owned lowering into `POST /v1/presenter/compose-from-intent`

These are not identical:

- they do not all enter through peer public routes
- the two AOI cases are explicit presenter route families
- the genealogy case is a planner-backed lowering family that terminates at the presenter intent route
- they use different request contracts
- they use different handoff kinds
- they lower different underlying source families and section shapes
- they all converge on the same served response model:
  - `ComposeFromIntentResponse`

That makes them the cleanest first Phase E matrix:

- broad enough to test generality honestly
- narrow enough to avoid inventing new substrate just to stage the proof

## Scope Decision

### In scope

#### 1. One three-case representative composition matrix

Capture and verify one bounded matrix with exactly these three cases:

1. AOI source-profile dossier case
   - route:
     - `POST /v1/presenter/compose-from-source`
   - contract family:
     - `source_profile`
   - workflow:
     - `anxiety_of_influence_thematic_single_thinker`
   - consumer:
     - `the-critic`
   - profile:
     - `dossier`

2. AOI source-selection case
   - route:
     - analyzer-owned planning handoff into `POST /v1/presenter/compose-from-selection`
   - contract family:
     - `source_selection`
   - workflow:
     - `anxiety_of_influence_thematic_single_thinker`
   - consumer:
     - `the-critic`
   - use the evolution-ready four-family selection path, not a narrowed two-family shortcut

3. Genealogy direct-sections case
   - route:
     - persisted planning decision
     - analyzer-owned planner-backed lowering
     - `POST /v1/presenter/compose-from-intent`
   - contract family:
     - `direct_sections`
   - workflow:
     - `intellectual_genealogy`
   - consumer:
     - `the-critic`

The variable in this slice is the composition/handoff family.
The consumer stays fixed deliberately so the proof isolates generality at the analyzer-owned composition layer rather than conflating it with consumer expansion.
That is also the current code reality:

- `the-critic` is not just a clean isolation choice
- it is the currently enforced transient consumer path in the live compose substrate
- widening consumer identity here would conflate Phase E composition proof with new consumer-surface infrastructure

#### 2. One frozen proof record under `communications/`

Capture one frozen proof bundle or dossier entry for each case under `communications/`.

The proof record for each case must include enough artifact truth to make the proof auditable:

- request payload
- response payload
- route identity
- workflow key
- consumer key
- source identity and handoff identity as appropriate
- persisted planning snapshot linkage where the case is planner-backed

Case-specific evidence rules:

- AOI `source_profile`
  - no planning snapshot is required
  - the proof should tie `source_v2_job_id`, `profile`, request, and response on one surface

- AOI `source_selection`
  - the proof should tie persisted `planning_decision_id`, selected-source request payload, and served response

- genealogy `direct_sections`
  - the proof should tie persisted `planning_decision_id`, lowered compose request, and served response
  - because the public `compose-from-intent` request contract does not carry `planning_decision_id`, wrapper-level or bundle-level capture metadata is acceptable if it is clearly labeled as capture metadata rather than request contract truth
  - in practice this case likely needs a fresh planning decision captured as part of the proof campaign so the lowering lineage is explicit and auditable

Do not read live persisted files directly in the matrix definition.
The proof record should be `communications/`-scoped and hash-pinned.

#### 3. One bounded Phase E proof harness or matrix test seam

The slice should add one focused matrix proof seam in analyzer-v2.

It may be:

- one dedicated integration-style test file
- or one small bounded proof harness plus focused tests

But it should not become:

- a new governance family
- a new evaluator architecture
- a generic proof-capture framework

Test execution should stay disciplined:

- prefer pinned proof artifacts and stable linkage assertions over brittle dependence on live ephemeral ids
- if a live capture is required to refresh a case, capture once, freeze it under `communications/`, and then test against the frozen record

The proof seam should assert the same minimum law across all three cases:

- the compose request is analyzer-owned and route-faithful for its family
- the served response shape is `ComposeFromIntentResponse`
- `presentation.view_count == len(generated_view_definitions)`
- the expected resolver version matches the route family:
  - `compose-from-source-v3`
  - `compose-from-selection-v1`
  - `compose-from-intent-v2`
- no host-side workflow-specific semantic reconstruction is required between analyzer-owned handoff and served presentation

#### 4. Focused regression coverage on representative generality

The proof should extend the existing presenter/orchestrator suites, not create a second program of record.

Required coverage:

- each of the three cases succeeds through its natural analyzer-owned route
- each case returns contract-valid `ComposeFromIntentResponse`
- each case satisfies view-count agreement
- the AOI `source_selection` case preserves the four-family evolution-ready payload rather than collapsing to a narrower family subset
- the genealogy case proves analyzer-owned lowering rather than host-side semantic reconstruction
- the host-facing response shape is unchanged across all three cases

There is a smaller fallback step if implementation friction is unexpectedly high:

- a two-case planner-backed matrix over AOI `source_selection` and genealogy `direct_sections`

But that is a fallback, not the default recommendation.
The three-case matrix remains the stronger first proof because it is the smallest matrix that covers:

- both currently live workflows
- the planner-backed handoff families
- the non-planner-mediated `source_profile` route family

### Out of scope

- new consumer surfaces
- new workflow families beyond current AOI and genealogy support
- arbitrary engine/pass graph search
- governance extension before the matrix exists
- generic plugin or evaluator architecture
- UI productization or enforcement policy

## Honest Claim Boundary

If this slice lands cleanly, the honest claim is:

- analyzer-v2 can already compose and render across a small representative matrix of live handoff families without per-app intelligence

The honest non-claim is:

- analyzer-v2 has not yet proven arbitrary engine/pass composition
- analyzer-v2 has not yet proven consumer generality
- analyzer-v2 has not yet proven open-ended workflow-family generality

This is the first Phase E move, not the whole phase.
It is also not a claim that the three cases are arbitrary samples:

- they are the full currently live handoff-family substrate exposed by the present compose layer
- that is why the three-case matrix is the recommended default rather than cherry-picked theater

## Decision Rule

This slice is only worth doing if it avoids collapsing back into Phase D habits.

That means:

- do not solve it by adding a new governance family first
- do not solve it by inventing new infrastructure that current live routes do not need
- do not widen the host
- do not widen the consumer set

If the three-case matrix cannot be proved on the current live compose surfaces without broad new architecture, that is itself the result:

- analyzer-v2 is not yet ready for the Phase E claim

But that should be learned directly through a bounded matrix proof, not inferred from more governance work.
