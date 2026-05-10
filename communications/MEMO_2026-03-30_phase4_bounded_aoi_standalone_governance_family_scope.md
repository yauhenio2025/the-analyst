# Memo: Phase 4 Bounded AOI Standalone Governance Family Scope

Subtitle: Prove the governance chain stands alone on the other already-supported evaluator substrate

Date: 2026-03-30
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-30_phase4_bounded_second_governance_family_v1_completion.md`
Relevant Prior Memos:
- `communications/MEMO_2026-03-30_phase4_bounded_second_governance_family_scope.md`
- `communications/MEMO_2026-03-30_phase4_bounded_current_governance_status_v1_completion.md`
- `communications/MEMO_2026-03-29_phase4_bounded_disposition_resolution_v1_completion.md`
- `communications/MEMO_2026-03-29_phase4_bounded_review_disposition_v1_completion.md`
- `communications/MEMO_2026-03-29_phase4_bounded_release_gate_v1_completion.md`
- `communications/MEMO_2026-03-29_phase4_bounded_governance_evaluation_v1_completion.md`

## Purpose

Define the next bounded Stage 15 slice now that the governance stack is no longer single-family-only at the definition/topology level.

This memo is not an implementation plan.
It is the scoping memo for the next concrete governance step after the genealogy-only second-family proof.

The next step should not be:

- a host-side governance dashboard
- a generic override product
- downstream deploy/unlock enforcement
- a new persisted governance object type
- a new evaluator family
- a premature Stage 15 closeout claim based only on the genealogy-only second-family proof

The next step should be:

- one AOI-only standalone governance family over the already-supported `aoi_exemplar` evaluator substrate using the already-landed report/gate/review/resolution/status chain unchanged as much as possible

## Anti-drift filter

This scope passes the fixed-direction prioritization filter because:

1. it continues to strengthen analyzer-owned governance structure rather than pushing meaning into hosts
2. it reuses the already-landed governance stack rather than widening into UI or operational enforcement
3. it addresses the next honest Stage 15 gap:
   - the current second-family proof is topology reuse over the same genealogy evidence, not a standalone family on the other supported evaluator substrate
4. it would still matter if the current host app were replaced later

## Why this is now the right next slice

The March 30 second-governance-family completion changed the boundary again.

What is now true:

- analyzer-v2 has one composite AOI-plus-genealogy governance family:
  - `phase4_frozen_governance_v1`
- analyzer-v2 also has one standalone genealogy-only governance family:
  - `phase4_genealogy_lifecycle_governance_v1`
- the same gate/review/resolution/status substrate now serves both families unchanged
- the second family proved that the governance stack is not structurally locked to one declared key chain or one pack topology

So the missing gap is no longer:

- single-family-only governance structure

That gap is now closed.

What is still missing is narrower and more honest:

- the new standalone family still sits on the same genealogy lifecycle evidence already present inside the composite family
- analyzer-v2 still does not have a standalone governance family on the other already-supported evaluator substrate:
  - `aoi_exemplar`

That means Stage 15 now proves:

- governance-family topology reuse

It does not yet prove:

- standalone family reuse across both currently supported evaluator substrates

So the next honest bounded slice is one AOI-only standalone family over the already-supported March 27 AOI exemplar evidence.

## Current code-backed boundary

### What already exists

- governance evaluators currently supported by the frozen-pack harness:
  - `aoi_exemplar`
  - `genealogy_lifecycle`
- one composite governance family:
  - `phase4_frozen_governance_v1`
- one standalone genealogy-only family:
  - `phase4_genealogy_lifecycle_governance_v1`
- generic builders and routes that are already parameterized by family keys:
  - frozen-pack harness
  - gate builder
  - review builder
  - resolution builder
  - semantic current-governance-status seam

### What does not yet exist

- no AOI-only standalone evaluation pack
- no AOI-only standalone gate definition
- no AOI-only standalone review definition
- no AOI-only standalone resolution definition
- no real standalone AOI report/gate/review/resolution/status chain

## Strategic decision

The next Stage 15 slice should be:

- one AOI-only standalone governance family over the existing `aoi_exemplar` evaluator

It should not be:

- a new evaluator family
- a broader routing/planning/composition governance harness
- a host-facing governance UI
- downstream enforcement
- a new persisted governance layer

The default bounded choice should be:

- one AOI-only frozen evaluation pack
- one AOI-only gate definition
- one AOI-only review definition
- one AOI-only resolution definition
- one real semantic current-governance-status read through the existing route

## Scope decision

### In scope

#### 1. One AOI-only standalone evaluation pack

Add one standalone AOI pack under the existing pack substrate.

Recommended bounded identity:

- `evaluation_pack_key = phase4_aoi_exemplar_governance_v1`

Default case choice:

- reuse the existing AOI exemplar case identity:
  - `aoi_exemplar_march27_execution_backed`

This should stay on the already-supported evaluator family:

- `evaluator_key = aoi_exemplar`

It should reuse the existing March 27 AOI exemplar frozen evidence already pinned inside the composite family.

#### 2. One AOI-only standalone gate

Add one standalone AOI gate definition under the existing gate substrate.

Recommended bounded identity:

- `gate_key = bounded_aoi_exemplar_readiness_v1`

The gate should:

- target only `phase4_aoi_exemplar_governance_v1`
- require one case:
  - `aoi_exemplar_march27_execution_backed`
- require the existing AOI dimensions:
  - `selection_fit`
  - `rationale_clarity`
  - `rendered_usefulness`
  - `operational_behavior`

It should reuse the current bounded gate verdict policy unchanged.

#### 3. One AOI-only standalone review/disposition definition

Add one review definition under the existing review substrate.

Recommended bounded identity:

- `review_key = bounded_aoi_exemplar_review_v1`

This should:

- target `bounded_aoi_exemplar_readiness_v1`
- stay recording-only in v1
- reuse the existing bounded `accept / reject / waive` law

#### 4. One AOI-only standalone resolution definition

Add one resolution definition under the existing resolution substrate.

Recommended bounded identity:

- `resolution_key = bounded_aoi_exemplar_resolution_v1`

This should:

- target `bounded_aoi_exemplar_review_v1`
- stay recording-only in v1
- reuse canonical current-resolution selection for:
  - `resolution_key + gate_decision_id`

#### 5. One real AOI-only family chain

Materialize one real AOI-only chain using the existing builders and routes:

- one AOI-only report
- one AOI-only gate
- one AOI-only review
- one AOI-only resolution
- one real semantic current-governance-status read through the unchanged route

The value of the slice should be stated honestly:

- this is a standalone-family proof over the other already-supported evaluator substrate
- it is stronger than the genealogy-only topology reuse slice because it uses distinct AOI frozen evidence
- it is still not Stage 15 closure by itself

### Out of scope

- new evaluator families
- new routes or response-model shapes
- new persisted governance object types
- host UI
- broad override/enforcement logic
- claims that routing/planning/composition governance is now broadly closed

## Honest expected outcome

If this slice lands cleanly, the honest claim afterward should be:

- analyzer-v2 governance now supports:
  - one composite AOI-plus-genealogy family
  - one standalone genealogy-only family
  - one standalone AOI-only family
- the same generic governance stack works across both currently supported evaluator families

But even then, the program should still avoid overclaiming.

That would still not automatically mean:

- full Phase 4 closure
- broader governance over routing/planning/composition families
- override product completeness
- downstream enforcement readiness

## Decision

The next bounded governance step should be:

- one AOI-only standalone governance family over the already-supported `aoi_exemplar` evaluator substrate

That is the cleanest next move because it remains definition-led, additive, and architecture-relevant without widening the governance substrate.
