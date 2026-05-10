# Memo: Phase 4 Bounded Disposition Resolution Scope

Subtitle: First analyzer-owned current-disposition resolution over persisted review decisions

Date: 2026-03-29
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-29_phase4_bounded_review_disposition_v1_completion.md`
Relevant Prior Memos:
- `communications/MEMO_2026-03-29_phase4_bounded_review_disposition_scope.md`
- `communications/MEMO_2026-03-29_phase4_bounded_release_gate_v1_completion.md`
- `communications/MEMO_2026-03-29_phase4_bounded_governance_evaluation_v1_completion.md`
- `communications/MEMO_2026-03-28_phase4_bounded_governance_evaluation_scope.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`

## Purpose

Define the next bounded Stage 15 slice after persisted review/disposition decisions now exist.

This memo is not an implementation plan.
It is the scoping memo for the next concrete governance seam after “reports exist,” “gate decisions exist,” and “review decisions exist.”

The next step should not be:

- a host-side governance dashboard
- a broad multi-step approval workflow
- a generic override platform
- a silent “latest review wins” convention
- a fresh live-rerun release campaign

The next step should be:

- one bounded analyzer-owned current-disposition resolution seam over persisted review decisions

This slice should also remain explicit that the first resolution object is recording-only in v1.
It records which exact review is currently adopted as the analyzer-owned governance stance.
It does not yet gate downstream behavior, unlock deploys, or alter machine gate/review truth.

## Anti-drift filter

This scope passes the fixed-direction prioritization filter because:

1. it keeps governance state and decision recording upstream in analyzer-v2
2. it builds directly on the newly landed review-decision object rather than widening into host product work
3. it adds the next missing governance object without reopening planner, lifecycle, or AOI-specific seams
4. it would still matter if the current host app were replaced later

## Why this is now the right next slice

The March 29 bounded review/disposition completion changed the boundary again.

What is now true:

- analyzer-v2 can persist thin evaluation reports as first-class governance objects
- analyzer-v2 can persist a thin pack-level gate decision over exact report ids
- analyzer-v2 can persist a thin human/operator review decision over exact gate decisions
- read-only inspection seams now exist for reports, gates, and reviews

What is still missing is the first explicit object that says which exact review decision is the currently adopted governance stance.

Right now the system can say:

- here are the reports
- here is the gate decision
- here are the historical review decisions over that gate

But it still cannot say:

- here is which exact review decision is currently adopted as the governing stance
- here is the explicit analyzer-owned resolution that prevents silent “latest review wins” behavior
- here is the exact resolver identity and note attached to that adoption event

That makes the next missing seam current-governance resolution rather than more review recording.
It does not mean the system is now ready for a broad override or enforcement product.

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
- analyzer-owned review schemas, persistence, definitions, and builder:
  - `src/evaluations/review_schemas.py`
  - `src/evaluations/review_store.py`
  - `src/evaluations/review_definitions.py`
  - `src/evaluations/review_builder.py`
- read-only report, gate, and review routes:
  - `src/api/routes/evaluations.py`
- persisted review decisions already materialized for:
  - `bounded_platform_readiness_review_v1`
  - `gate-decision-745c2cb7e090`

### What does not yet exist

- no analyzer-owned current-disposition resolution object over exact `review_decision_id`
- no persisted record of which review decision is currently adopted as the governing stance
- no bounded mutation path for recording that adoption event
- no read-only inspection seam for persisted resolution records
- no clean separation between:
  - historical review/disposition records
  - the currently adopted governance stance derived from one exact review

## Strategic decision

The next Stage 15 slice should be:

- one bounded analyzer-owned current-disposition resolution seam over persisted review decisions

It should not be:

- a host-side approval product
- a generic multi-pack approval application
- a broad override framework
- a hidden latest-record-wins convention

The default bounded shape should be:

- one persisted resolution object over one exact `review_decision_id`
- one bounded resolution law that adopts that review as the current stance
- one deliberate write path for recording that adoption event
- one authoritative current-resolution lookup law and read-only retrieval seam

## Scope decision

### In scope

The next slice should land all of the following together.

#### 1. One analyzer-owned current-disposition resolution object and store

Add one bounded persistent object, for example `PersistedEvaluationDispositionResolution`, stored analyzer-side in file-backed JSON parallel to reports, gates, and reviews.

Default storage path:

- `src/evaluations/resolutions/`

Required properties should include:

- analyzer-generated `resolution_id`
- `resolution_key`
- `created_at`
- `resolution_definition_version`
- exact `review_decision_id`
- derived `review_key`
- derived `review_definition_version`
- derived `gate_decision_id`
- derived `gate_key`
- derived `gate_definition_version`
- derived `evaluation_pack_key`
- `resolver_identity`
- explicit resolution note
- derived reviewed disposition at resolution time
- derived observed gate verdict at resolution time
- derived `contains_live_revalidation`

This object is the next governance object above the review decision.
It is not just an operator convention about “use the latest review.”

It should stay thin and cite the exact review decision it adopts.
It should not duplicate the full review or full gate payload into a new truth store.

Accumulation policy for v1 should be explicit:

- resolution decisions accumulate historically
- multiple resolutions over the same `gate_decision_id` are allowed
- list results should return newest-first
- “current” is a query-time derivation, not a persisted mutable `is_current` flag
- the authoritative current-resolution scope for this first slice is:
  - `resolution_key + gate_decision_id`
- the current adopted stance for that scope is:
  - the newest persisted resolution whose `resolution_key` and `gate_decision_id` both match
- callers must not infer current stance by reading a generic list endpoint and picking the first row themselves; analyzer-v2 should own one canonical current-resolution accessor

#### 2. One fixed bounded resolution law

The first slice should define one explicit bounded resolution law over review decisions.

It should be encoded in one code-defined resolution definition, for example:

- `src/evaluations/resolution_definitions.py`
- one definition such as `bounded_platform_readiness_resolution_v1`

That definition should target:

- `bounded_platform_readiness_review_v1`

Recommended bounded shape:

- one explicit resolution action that means:
  - adopt this exact review decision as the current governing stance

This first resolution layer is recording-only in v1:

- it records which exact review is currently adopted for the declared scope
- it does not reinterpret the review or gate truth
- it does not yet trigger downstream operational consequences

The resolution law should remain explicit and deterministic about compatibility.

Default bounded expectation:

- a resolution is valid only when the referenced review matches the targeted:
  - `resolution_key`
  - `review_key`
  - `review_definition_version`
  - `gate_key`
  - `gate_definition_version`
  - `evaluation_pack_key`
- the resolver does not reinterpret the review or gate truth
- the resolver adopts one exact review as current and records that adoption event
- any of the three bounded review dispositions may be adopted:
  - adopting `accept` means the current stance is acceptance
  - adopting `reject` means the current stance is rejection
  - adopting `waive` means the current stance is the recorded waiver

This slice must remain honest that resolution is still retrospective frozen-pack governance.
It must not be misrepresented as a fresh live production release approval system.

Because the underlying review already carries mixed-evidence honesty from the gate, the resolution object should also carry:

- derived `contains_live_revalidation: bool`

This is an honesty label copied from the referenced review decision, not an independently resolver-set field.

#### 3. One bounded write path

There should be one deliberate way to create the resolution object.

Recommended bounded shape:

- one analyzer-owned CLI/harness write path that consumes:
  - exact `review_decision_id`
  - `resolver_identity`
  - resolution note

The authoritative contract should be exact review-decision input, not “adopt the latest review lying around.”

The write path should:

- load the referenced review decision
- derive review/gate-linked fields from that review
- fail closed if the referenced review is missing
- fail closed if the review does not match the targeted resolution definition
- fail closed if resolver identity or resolution note is blank

This slice should not require:

- host UI
- auth integration
- multi-user workflow
- an HTTP mutation route
- downstream automatic deploy/unlock semantics

#### 4. One read-only disposition-resolution inspection seam

Add one analyzer-owned retrieval seam for persisted resolution decisions, for example:

- `GET /v1/evaluations/resolutions/{resolution_id}`
- `GET /v1/evaluations/resolutions?review_decision_id=...&gate_decision_id=...&evaluation_pack_key=...&limit=...`
- one canonical current-resolution lookup seam, for example:
  - `GET /v1/evaluations/resolutions/current?resolution_key=...&gate_decision_id=...`

This remains read-only in v1.
No HTTP mutation/generation route is required for creating resolutions in the first slice.

The purpose of the current-resolution lookup seam is to make analyzer-v2, not the caller, authoritative for the “current adopted stance” derivation.

## Must land

The next slice should be treated as complete only if all of the following are true:

1. one analyzer-owned current-disposition resolution object exists
2. one explicit resolution law exists over exact `review_decision_id`
3. one authoritative current-resolution lookup law exists for the bounded declared scope
4. the object cites exact review identity, resolver identity, and resolution note
5. the write path derives review/gate truth fields from the referenced review decision rather than accepting them as freeform resolver inputs
6. the write path fails closed if the referenced review decision is missing or mismatched to the resolution definition
7. one read-only disposition-resolution inspection seam exists

## Must not widen

- do not build host UI in this slice
- do not build auth or identity-management product in this slice
- do not build a generic multi-step approval workflow in this slice
- do not reopen fresh live browser proofs by default
- do not let resolution silently target “latest review” without recording exact `review_decision_id`
- do not turn this into a broad override framework in this slice
- do not revive the March 19 workspace line as the active next step

## Review focus

The most useful review questions for this memo are:

1. whether bounded current-disposition resolution is genuinely the right next Stage 15 seam after persisted review decisions now exist
2. whether the memo is honest enough that the first resolution object is recording-only in v1
3. whether the declared current-resolution scope and canonical lookup seam are tight enough to prevent a silent “latest review wins” convention
4. whether CLI-only write plus read-only HTTP inspection is still the honest first boundary
5. whether stronger linkage to exact review/gate-definition semantics is required in the persisted object

## Next artifact

If this scope survives review, the next artifact should be a concrete implementation plan for:

- one persisted analyzer-owned current-disposition resolution object
- one bounded exact-id write path over review decisions
- one read-only resolution inspection seam

That would be the next real Stage 15 follow-on slice after “review decisions exist.”
