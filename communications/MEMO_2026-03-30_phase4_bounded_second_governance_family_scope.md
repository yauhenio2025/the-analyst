# Memo: Phase 4 Bounded Second Governance Family Scope

Subtitle: Prove the governance stack is reusable beyond one proving-campaign-coupled family

Date: 2026-03-30
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-30_phase4_bounded_current_governance_status_v1_completion.md`
Relevant Prior Memos:
- `communications/MEMO_2026-03-29_phase4_bounded_current_governance_status_scope.md`
- `communications/MEMO_2026-03-29_phase4_bounded_disposition_resolution_v1_completion.md`
- `communications/MEMO_2026-03-29_phase4_bounded_review_disposition_v1_completion.md`
- `communications/MEMO_2026-03-29_phase4_bounded_release_gate_v1_completion.md`
- `communications/MEMO_2026-03-29_phase4_bounded_governance_evaluation_v1_completion.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`

## Purpose

Define the next bounded Stage 15 slice now that reports, gates, reviews, resolutions, canonical current-resolution lookup, and semantic current-governance status all exist for the first declared governance family.

This memo is not an implementation plan.
It is the scoping memo for the next concrete governance step after “semantic current status exists for the first family.”

The next step should not be:

- a host-side governance dashboard
- a generic override product
- downstream deploy/unlock enforcement
- a fresh live-rerun governance campaign
- another new governance object type
- a nominal closeout claim that treats one family as sufficient proof of generality by default

The next step should be:

- one bounded second governance-family slice over a different declared pack/scope using the already-landed report/gate/review/resolution/status substrate

This slice should remain explicit that the value is:

- proving family-level reuse of the governance substrate
- not inventing new governance layers
- not adding live operational enforcement
- not widening into product UI

It should also remain explicit that this slice is substrate-neutral only if it reuses the already-supported evaluator families and governance builders that now exist.
If a proposed second family requires a new evaluator family, new governance object type, or family-specific route/schema law, the slice has widened and should be reconsidered.

## Anti-drift filter

This scope passes the fixed-direction prioritization filter because:

1. it keeps governance structure upstream in analyzer-v2 instead of pushing meaning into consumers
2. it reuses the newly landed governance stack rather than widening into product/UI work
3. it addresses the most honest remaining Stage 15 gap:
   - the current governance family is still proving-campaign-coupled and singular
4. it would still matter if the current host app were replaced later

## Why this is now the right next slice

The March 30 current-governance-status completion changed the boundary again.

What is now true:

- analyzer-v2 can persist evaluation reports over a frozen AOI-plus-genealogy composite pack
- analyzer-v2 can persist gate decisions over exact report ids
- analyzer-v2 can persist review decisions over exact gate decisions
- analyzer-v2 can persist current-disposition resolutions over exact review decisions
- analyzer-v2 now owns canonical current-resolution lookup for:
  - `resolution_key + gate_decision_id`
- analyzer-v2 now serves semantic current-governance status with fail-closed chain verification

So the missing gap is no longer:

- no current-governance semantic seam

That gap is now closed.

What is still missing is narrower and more structural:

- the full governance stack still exists for only one declared family:
  - `phase4_frozen_governance_v1`
  - `bounded_platform_readiness_v1`
  - `bounded_platform_readiness_review_v1`
  - `bounded_platform_readiness_resolution_v1`

That means the current Stage 15 line still proves:

- one correct governance family

It does not yet prove:

- a reusable governance family pattern

So the next honest slice is not another new governance object.
It is one second declared governance family over a different bounded scope using the same substrates and read seams that now already exist.

This memo is intentionally narrower than “prove governance over genuinely new territory.”
The first second-family slice is mainly about proving that the governance stack is not structurally locked to one set of keys, one pack topology, or one declared family chain.

## Current code-backed boundary

### What already exists

- analyzer-owned report substrate and frozen-pack harness:
  - `src/evaluations/schemas.py`
  - `src/evaluations/report_store.py`
  - `src/evaluations/frozen_pack_definitions.py`
  - `src/evaluations/frozen_pack_harness.py`
- analyzer-owned gate substrate and definitions:
  - `src/evaluations/gate_schemas.py`
  - `src/evaluations/gate_store.py`
  - `src/evaluations/gate_definitions.py`
  - `src/evaluations/gate_builder.py`
- analyzer-owned review substrate and definitions:
  - `src/evaluations/review_schemas.py`
  - `src/evaluations/review_store.py`
  - `src/evaluations/review_definitions.py`
  - `src/evaluations/review_builder.py`
- analyzer-owned resolution substrate and definitions:
  - `src/evaluations/resolution_schemas.py`
  - `src/evaluations/resolution_store.py`
  - `src/evaluations/resolution_definitions.py`
  - `src/evaluations/resolution_builder.py`
- analyzer-owned semantic current-governance-status seam:
  - `src/evaluations/governance_status_schemas.py`
  - `src/evaluations/governance_status.py`
- read-only inspection routes:
  - `src/api/routes/evaluations.py`
- one current real family already materialized:
  - pack: `phase4_frozen_governance_v1`
  - gate: `bounded_platform_readiness_v1`
  - review: `bounded_platform_readiness_review_v1`
  - resolution: `bounded_platform_readiness_resolution_v1`

### What does not yet exist

- no second code-defined evaluation pack proving reuse beyond `phase4_frozen_governance_v1`
- no second gate/review/resolution/status family over a different declared scope
- no evidence yet that the full governance stack remains honest when the declared family topology changes
- no broader pack-global currentness seam
- no downstream enforcement or host UI

## Strategic decision

The next Stage 15 slice should be:

- one bounded second governance family over a different declared pack/scope using the already-landed governance stack unchanged as much as possible

It should not be:

- another new persisted governance layer
- a product-facing override workflow
- a live rerun campaign
- a host dashboard
- a pack-global governance abstraction jump

The default bounded choice should be:

- one second code-defined frozen evaluation pack
- one second code-defined gate definition
- one second code-defined review definition
- one second code-defined resolution definition
- one real materialized second current-governance-status read through the existing semantic seam

The default choice should also stay on the already-supported evaluator families.
The second family should be definition/materialization reuse over the current evaluator substrate, not a disguised evaluator-expansion slice.

## Scope decision

### In scope

The next slice should land all of the following together.

#### 1. One second code-defined evaluation pack

Add one second frozen evaluation pack definition under the existing pack substrate.

The default bounded target should be:

- one single-case genealogy lifecycle governance pack built from already-existing frozen evidence and already-existing analyzer-owned persisted truth

Recommended bounded identity:

- `evaluation_pack_key = phase4_genealogy_lifecycle_governance_v1`

Default case choice:

- reuse the existing genealogy lifecycle case identity:
  - `genealogy_lifecycle_march28_session_reopen`

This is the best anti-drift default, not the only technically viable thin target.
A bounded AOI-only family or another already-supported scope could also be technically valid if review shows it is strategically cleaner.
The point of this memo is the family-reuse seam, not an exclusive commitment to one target before review.

Why this is the preferred first second family:

- it is the thinnest existing analyzer-owned lifecycle proof surface
- it is already session-centric and current-host-neutral enough for this bounded governance question
- it changes pack topology from:
  - one mixed two-case composite pack
  - to one single-case session-centric pack
- it proves the governance substrate is not implicitly hardcoded to the current two-case AOI-plus-genealogy family

This slice should stay honest that the value is the new declared governance family, not new analytical evidence collection.
If this family reuses the same compose session, the same pinned frozen artifacts, the same evaluator implementation, and the same dimensions already present inside the first pack, that is still valid for this bounded purpose.
But it should be described honestly as topology/definition reuse proof, not as governance over genuinely new territory.

#### 2. One second gate definition over that pack

Add one second gate definition under the existing gate substrate.

Recommended bounded identity:

- `gate_key = bounded_genealogy_lifecycle_readiness_v1`

The gate should:

- target only `phase4_genealogy_lifecycle_governance_v1`
- require one case:
  - `genealogy_lifecycle_march28_session_reopen`
- require the already-proved genealogy dimensions:
  - `identity_integrity`
  - `saved_truth_fidelity`
  - `reopen_integrity`
  - `boundary_observance`

This slice should not invent new verdict logic.
It should reuse the current bounded gate substrate and verdict policy.
If a proposed second family requires a new verdict policy or a new gate-builder law, it has widened beyond the intended boundary.

#### 3. One second review/disposition definition

Add one second review definition under the existing review substrate.

Recommended bounded identity:

- `review_key = bounded_genealogy_lifecycle_review_v1`

This should:

- target `bounded_genealogy_lifecycle_readiness_v1`
- stay recording-only in v1
- reuse the existing bounded `accept / reject / waive` law
- avoid any new override framework

#### 4. One second disposition-resolution definition

Add one second resolution definition under the existing resolution substrate.

Recommended bounded identity:

- `resolution_key = bounded_genealogy_lifecycle_resolution_v1`

This should:

- target `bounded_genealogy_lifecycle_review_v1`
- stay recording-only in v1
- reuse canonical current-resolution selection for:
  - `resolution_key + gate_decision_id`

#### 5. One real second-family materialization

The slice should materialize one real second-family chain using the already-landed builders/harnesses:

- one report for the second pack
- one gate decision for the second gate
- one review decision for the second review
- one resolution for the second resolution
- one current-governance-status read through the already-landed semantic route/helper

This is required because the slice is about proving family reuse in practice, not only adding dormant definitions.
The materialization should use the existing builders/status seam unchanged except for the new code-defined family definitions and the chosen pack inputs.

### Out of scope

- new persisted governance object types
- host UI
- auth-backed reviewer/resolver identity
- downstream deploy/unlock enforcement
- a pack-global current-governance seam
- fresh live proof capture
- broad family factories or generic meta-definition generators

## Must land

The next slice should be treated as complete only if all of the following are true:

1. a second code-defined evaluation pack exists over a different declared scope than `phase4_frozen_governance_v1`
2. a second gate/review/resolution family exists for that pack
3. the existing report/gate/review/resolution builders can materialize the second family without new governance object types
4. the existing semantic current-governance-status seam can serve the second family without family-specific route/schema redesign
5. the second family changes governance topology enough to make the “single first family only” criticism no longer true in the same way
6. the second family stays on already-supported evaluator families and existing builders rather than smuggling in evaluator-family expansion

## Must not widen

- do not add a new persisted status layer
- do not build a UI
- do not add downstream enforcement
- do not add pack-global “latest governance” law
- do not reopen lifecycle or host-contract work
- do not turn this into a fresh live browser-proof campaign

## Review focus

The most useful review questions for this memo are:

1. whether a second governance family is the right next Stage 15 slice now that current-governance status exists
2. whether keeping Stage 15 open on “one-family-only” grounds is the honest reading of the current boundary
3. whether a single-case genealogy lifecycle family is the right first second-family target, or whether AOI-only or another declared scope would be more honest
4. whether this slice should add only new definitions/materialization, not new governance object types
5. whether landing a second family would materially strengthen the Stage 15 substrate without yet being overstated as full closeout

## Next artifact

If this scope survives review, the next artifact should be a concrete implementation plan for:

- one second code-defined governance pack
- one second gate/review/resolution family
- one real materialized second current-governance-status chain through the already-landed seams

If that second-family slice lands honestly, it should materially strengthen the case that Stage 15 is a reusable substrate rather than a one-family proving harness.
But this memo does not assume that second-family reuse alone automatically closes Stage 15; the broader Phase 4 exit test still reaches beyond “two families exist.”
