# Memo: Phase 4 Bounded Review Disposition Scope

Subtitle: First analyzer-owned review/disposition record over persisted release-gate decisions

Date: 2026-03-29
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-29_phase4_bounded_release_gate_v1_completion.md`
Relevant Prior Memos:
- `communications/MEMO_2026-03-29_phase4_bounded_release_gate_scope.md`
- `communications/MEMO_2026-03-29_phase4_bounded_governance_evaluation_v1_completion.md`
- `communications/MEMO_2026-03-28_phase4_bounded_governance_evaluation_scope.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_closeout.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`

## Purpose

Define the next bounded Stage 15 slice after the release-gate substrate now exists.

This memo is not an implementation plan.
It is the scoping memo for the next concrete governance seam after “reports exist” and “gate decisions exist.”

The next step should not be:

- a host-side approval dashboard
- a broad multi-step workflow for human review
- a generic override platform
- a fresh live-rerun release campaign
- a publish/share program

The next step should be:

- one bounded analyzer-owned review/disposition seam over persisted gate decisions

## Anti-drift filter

This scope passes the fixed-direction prioritization filter because:

1. it keeps governance decision-making upstream in analyzer-v2
2. it builds directly on the newly landed gate object rather than widening back into host product work
3. it adds the next missing governance object without reopening older planner, lifecycle, or AOI-specific seams
4. it would still matter if the current host app were replaced later

## Why this is now the right next slice

The March 29 bounded release-gate completion changed the boundary again.

What is now true:

- analyzer-v2 can persist thin evaluation reports as first-class governance objects
- analyzer-v2 can persist a thin pack-level gate decision over exact report ids
- the frozen governance pack now has a deterministic pass/fail/error enforcement layer
- read-only inspection seams now exist for both reports and gates

What is still missing is the first explicit review/disposition object above the machine gate.

Right now the system can say:

- here are the reports
- here is the gate decision

But it still cannot say:

- here is the explicit persisted human/operator disposition over that gate decision
- here is whether the gate was accepted, rejected, or explicitly waived in a bounded recording-only sense
- here is the exact rationale and reviewer identity attached to that disposition

That makes the next missing seam governance-authority recording rather than more evidence generation.

## Current code-backed boundary

### What already exists

- analyzer-owned evaluation report schemas and persistence:
  - `src/evaluations/schemas.py`
  - `src/evaluations/report_store.py`
- code-defined frozen governance packs:
  - `src/evaluations/frozen_pack_definitions.py`
- deterministic frozen-pack report harness:
  - `src/evaluations/frozen_pack_harness.py`
- analyzer-owned gate schemas, persistence, definitions, and builder:
  - `src/evaluations/gate_schemas.py`
  - `src/evaluations/gate_store.py`
  - `src/evaluations/gate_definitions.py`
  - `src/evaluations/gate_builder.py`
- read-only report and gate routes:
  - `src/api/routes/evaluations.py`
- persisted gate decisions already materialized for:
  - `bounded_platform_readiness_v1`
  - `phase4_frozen_governance_v1`

### What does not yet exist

- no analyzer-owned review/disposition object over exact `gate_decision_id`
- no persisted record of whether a gate was accepted, rejected, or explicitly waived
- no bounded mutation path for recording that review/disposition
- no read-only inspection seam for persisted review/disposition records
- no clean separation between:
  - machine gate truth
  - human/operator review disposition over that gate truth

## Strategic decision

The next Stage 15 slice should be:

- one bounded analyzer-owned review/disposition seam over persisted gate decisions

It should not be:

- a host-side approval product
- a generic multi-pack review application
- a broad override framework
- a new live-proof campaign

The default bounded shape should be:

- one persisted review/disposition object over one exact `gate_decision_id`
- one bounded disposition law
- one deliberate write path for recording that decision
- one read-only retrieval seam

## Scope decision

### In scope

The next slice should land all of the following together.

#### 1. One analyzer-owned review/disposition object and store

Add one bounded persistent object, for example `PersistedEvaluationReviewDecision`, stored analyzer-side in file-backed JSON parallel to reports and gates.

Default storage path:

- `src/evaluations/reviews/`

Required properties should include:

- analyzer-generated `review_decision_id`
- `created_at`
- `review_definition_version`
- exact `gate_decision_id`
- derived `gate_key`
- derived `gate_definition_version`
- derived `evaluation_pack_key`
- `reviewer_identity`
- explicit `disposition`
- explicit rationale
- derived observed gate verdict at decision time
- derived `contains_live_revalidation`
- ordered blocking or waiver reasons where relevant

This object is the next governance object above the gate decision.
It is not just a memo comment and not just an operator convention.

It should stay thin and cite the exact gate decision it is about.
It should not duplicate the full gate payload into a second truth store.

Accumulation policy for v1 should be explicit:

- review/disposition decisions accumulate historically
- multiple decisions over the same `gate_decision_id` are allowed
- list results should return newest-first
- there is no full multi-review workflow or “active reviewer” model in v1

#### 2. One fixed bounded disposition law

The first slice should define one explicit bounded disposition law over gate decisions.

It should be encoded in one code-defined review definition, for example:

- `src/evaluations/review_definitions.py`
- one definition such as `bounded_platform_readiness_review_v1`

That definition should target:

- `bounded_platform_readiness_v1`

Recommended bounded shape:

- `accept`
- `reject`
- `waive`

The law should remain explicit and deterministic about when each is valid.

Default bounded expectation:

- `accept` records that the persisted gate decision is adopted as-is and is valid only when the observed gate verdict is `pass`
- `reject` records that the gate decision is not accepted as sufficient for progression
- `waive` records one explicit bounded exception against a non-passing gate outcome with written rationale

The disposition law should be explicit about alignment:

- `accept` is valid only when the observed gate verdict is `pass`
- `reject` is valid for any observed gate verdict
- `waive` is valid only when the observed gate verdict is not `pass`, requires non-empty rationale, and remains recording-only in v1

`waive` must not silently change machine gate truth.
It records an explicit bounded exception against that truth.

The slice must remain honest that this is still retrospective frozen-pack governance.
It must not be misrepresented as a fresh live production release approval.

Because the underlying gate may aggregate mixed live-revalidated and frozen-artifact report evidence, the review/disposition object should also carry:

- derived `contains_live_revalidation: bool`

This is an honesty label copied from the referenced gate decision, not an independently reviewer-set field.

#### 3. One bounded write path

There should be one deliberate way to create the review/disposition object.

Recommended bounded shape:

- one analyzer-owned CLI/harness write path that consumes:
  - exact `gate_decision_id`
  - `reviewer_identity`
  - `disposition`
  - rationale

The authoritative contract should be exact gate-decision input, not “decide over the latest gate lying around.”

The write path should:

- load the referenced gate decision
- derive `gate_key`, `gate_definition_version`, `evaluation_pack_key`, observed gate verdict, and `contains_live_revalidation` from that gate
- fail closed if the disposition violates the disposition-to-verdict alignment law
- fail closed if `waive` is attempted without non-empty rationale

This slice should not require:

- host UI
- auth integration
- multi-user workflow
- an HTTP mutation route

#### 4. One read-only review/disposition inspection seam

Add one analyzer-owned retrieval seam for persisted review/disposition decisions, for example:

- `GET /v1/evaluations/reviews/{review_decision_id}`
- `GET /v1/evaluations/reviews?gate_decision_id=...&gate_key=...&evaluation_pack_key=...&limit=...`

This remains read-only in v1.
No HTTP mutation/generation route is required for creating decisions in the first slice.

## Must land

The next slice should be treated as complete only if all of the following are true:

1. one analyzer-owned review/disposition object exists
2. one explicit disposition law exists over exact `gate_decision_id`
3. the object cites exact gate identity, reviewer identity, disposition, and rationale
4. the write path derives gate truth fields from the referenced gate decision rather than accepting them as freeform reviewer inputs
5. the write path fails closed if the referenced gate decision is missing, mismatched, or violates the disposition-to-verdict alignment law
6. one read-only review/disposition inspection seam exists

## Must not widen

- do not build host UI in this slice
- do not build auth or identity-management product in this slice
- do not build a generic multi-step approval workflow in this slice
- do not reopen fresh live browser proofs by default
- do not let review/disposition silently target “latest gate” without recording exact `gate_decision_id`
- do not let `waive` become a hidden generic override framework in this slice
- do not revive the March 19 workspace line as the active next step

## Review focus

The most useful review questions for this memo are:

1. whether bounded review/disposition is genuinely the right next Stage 15 seam after the gate
2. whether the memo now defines `waive` tightly enough as a recording-only bounded exception path
3. whether CLI-only write plus read-only HTTP inspection is the honest first boundary
4. whether any stronger linkage to exact gate verdict/review-definition semantics is required in the persisted object
5. whether this scope stays retrospective and frozen-pack-scoped enough, rather than drifting into a generic approval product

## Next artifact

If this scope survives review, the next artifact should be a concrete implementation plan for:

- one persisted analyzer-owned review/disposition object
- one bounded explicit-id write path over gate decisions
- one read-only review/disposition inspection seam

That would be the next real Stage 15 follow-on slice after “gate decisions exist.”
