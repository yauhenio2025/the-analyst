# Memo: Phase 4 Bounded Current Governance Status Scope

Subtitle: First analyzer-owned semantic current-governance read seam over the resolution/review/gate chain

Date: 2026-03-29
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-29_phase4_bounded_disposition_resolution_v1_completion.md`
Relevant Prior Memos:
- `communications/MEMO_2026-03-29_phase4_bounded_disposition_resolution_scope.md`
- `communications/MEMO_2026-03-29_phase4_bounded_review_disposition_v1_completion.md`
- `communications/MEMO_2026-03-29_phase4_bounded_release_gate_v1_completion.md`
- `communications/MEMO_2026-03-29_phase4_bounded_governance_evaluation_v1_completion.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`

## Purpose

Define the next bounded Stage 15 slice now that persisted reports, gates, reviews, resolutions, and canonical current-resolution lookup all exist.

This memo is not an implementation plan.
It is the scoping memo for the next concrete governance seam after “current-disposition resolution exists.”

The next step should not be:

- a host-side governance dashboard
- a generic override framework
- downstream deploy/unlock enforcement
- a fresh live-rerun governance campaign
- a nominally new seam that only repackages the existing current-resolution response

The next step should be:

- one bounded analyzer-owned semantic current-governance-status seam over the current resolution/review/gate chain

This slice should remain explicit that the first status seam is:

- derived-only
- read-only
- descriptive in v1
- retrospective frozen-pack governance, not a hidden override/enforcement system

It should also remain honest that the incremental value here is narrower than “first time analyzer-v2 can say anything current in one place,” because the existing current-resolution seam already serves most of that shape.

## Anti-drift filter

This scope passes the fixed-direction prioritization filter because:

1. it keeps governance interpretation upstream in analyzer-v2
2. it builds directly on the newly landed resolution object instead of widening into product UI or override work
3. it adds an authoritative semantic status contract plus retrieval-time chain verification on top of the already-landed current-resolution seam
4. it would still matter if the current host app were replaced later

## Why this is now the right next slice

The March 29 bounded disposition-resolution completion changed the boundary again.

What is now true:

- analyzer-v2 can persist thin evaluation reports as first-class governance objects
- analyzer-v2 can persist thin gate decisions over exact report ids
- analyzer-v2 can persist thin human/operator review decisions over exact gate decisions
- analyzer-v2 can persist thin current-disposition resolutions over exact review decisions
- analyzer-v2 now owns the canonical current-resolution derivation for:
  - `resolution_key + gate_decision_id`
- read-only inspection seams now exist for reports, gates, reviews, and resolutions

Analyzer-v2 already has:

- `GET /v1/evaluations/resolutions/current?resolution_key=...&gate_decision_id=...`

and that route already returns most of the thin current-governance shape through the persisted current resolution.

So the real missing seam is narrower than the prior memo claimed.

What is still missing is a semantic, authoritative current-governance contract that says:

- what the effective governance status is for a bounded declared scope
- which exact resolution, review, and gate chain currently backs that status
- whether that status has been retrieval-time validated against the linked chain
- whether that current stance still carries retrospective mixed-evidence semantics

Right now the system can already say:

- here is the current resolution
- here is the referenced review
- here is the referenced gate

But it still cannot say, through one semantic analyzer-owned seam that is materially more authoritative than raw current-resolution inspection:

- here is the effective current governance status for this scope
- here is the exact validated backing chain
- here is the bounded semantic summary that future consumers should read instead of reinterpreting raw resolution fields themselves

That makes the next missing seam semantic current-governance status rather than more resolution recording.
It does not mean the system is now ready for override semantics or downstream enforcement.

## Current code-backed boundary

### What already exists

- analyzer-owned evaluation report schemas and persistence:
  - `src/evaluations/schemas.py`
  - `src/evaluations/report_store.py`
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
- analyzer-owned resolution schemas, persistence, definitions, and builder:
  - `src/evaluations/resolution_schemas.py`
  - `src/evaluations/resolution_store.py`
  - `src/evaluations/resolution_definitions.py`
  - `src/evaluations/resolution_builder.py`
- read-only report, gate, review, and resolution routes:
  - `src/api/routes/evaluations.py`
- one canonical current-resolution seam already exists:
  - `GET /v1/evaluations/resolutions/current?resolution_key=...&gate_decision_id=...`
  - backed by `load_current_evaluation_disposition_resolution(...)`
- one real persisted resolution now materialized for:
  - `bounded_platform_readiness_resolution_v1`
  - `review-decision-21edf9b955ee`

### What does not yet exist

- no analyzer-owned current-governance-status contract that is materially more authoritative than raw current-resolution inspection
- no retrieval-time chain verification that re-loads and validates the linked review/gate objects behind current resolution
- no thin semantic status object that answers the governance question without asking callers to interpret raw resolution fields themselves
- no served status-level honesty label in the current-status response itself

## Strategic decision

The next Stage 15 slice should be:

- one bounded analyzer-owned semantic current-governance-status seam over the current resolution/review/gate chain

It should not be:

- a host-side approval product
- a generic override platform
- a downstream enforcement seam
- a hidden consumer-local interpretation convention

The default bounded shape should be:

- one thin derived current-governance-status object
- one canonical analyzer-owned derivation over exact current resolution scope
- one read-only semantic retrieval seam for that status
- no new write semantics in the same slice
- no second competing current-selection algorithm

## Scope decision

### In scope

The next slice should land all of the following together.

#### 1. One analyzer-owned semantic current-governance-status object

Add one bounded derived object, for example `CurrentEvaluationGovernanceStatus`, owned analyzer-side.

The default bounded choice should be:

- derived, not persisted as a new write-layer truth object
- additive over the existing current-resolution seam, not a replacement persisted truth layer

It should be built from:

- the canonical current resolution for `resolution_key + gate_decision_id`
- the exact referenced persisted review decision
- the exact referenced persisted gate decision

Required fields should include:

- `resolution_key`
- `gate_decision_id`
- one explicit `effective_governance_status`
- exact `current_resolution_id`
- exact `current_review_decision_id`
- exact `current_gate_decision_id`
- `scope_label`
- `contains_live_revalidation`
- current adopted review disposition
- observed gate verdict
- enough exact linkage fields to keep the derived status self-explanatory:
  - `review_key`
  - `review_definition_version`
  - `gate_key`
  - `gate_definition_version`
  - `evaluation_pack_key`

This object should stay thin.
It should not duplicate full resolution, review, or gate payloads.
It should add status semantics that the raw persisted resolution does not already answer by itself.

Recommended bounded status law:

- `accept` on current resolution maps to `effective_governance_status = approved`
- `reject` maps to `effective_governance_status = blocked`
- `waive` maps to `effective_governance_status = exception_recorded`

That mapping is the main semantic value of the new seam.
Without it, the slice collapses into a near-duplicate wrapper around `/resolutions/current`.

#### 2. One canonical analyzer-owned derivation law

The next slice should define one explicit derivation law for current governance status.

The bounded expectation should be:

- load current resolution through the existing canonical store accessor:
  - `load_current_evaluation_disposition_resolution(...)`
- load the referenced review decision
- load the referenced gate decision
- fail closed with `404` when no current resolution exists for the requested scope
- fail closed with `409` when the current resolution exists but the linked review/gate chain is missing or inconsistent
- fail closed if the chain is inconsistent on:
  - `resolution_key`
  - `review_key`
  - `review_definition_version`
  - `gate_key`
  - `gate_definition_version`
  - `evaluation_pack_key`
- derive `scope_label` from the existing analyzer-owned definitions rather than inventing a freeform status-only label:
  - default bounded choice: use the resolution definition scope label
- do not let callers submit any of those linked fields as freeform status inputs

This slice should remain explicit that status is:

- derived from already recorded governance truth
- descriptive in v1
- not a new enforcement object
- built on the existing current-resolution law rather than introducing a second current-selection algorithm

#### 3. One bounded read-only semantic retrieval seam

There should be one deliberate way to ask analyzer-v2 for effective current governance state.

Recommended bounded shape:

- one read-only current-status route, for example:
  - `GET /v1/evaluations/governance-status/current?resolution_key=...&gate_decision_id=...`

This route should be additive over, not a replacement for:

- `GET /v1/evaluations/resolutions/current?...`

The existing route remains raw current-resolution inspection.
The new route earns its keep only if it adds semantic status interpretation plus retrieval-time chain verification.

The authoritative contract should be:

- exact current scope input:
  - `resolution_key`
  - `gate_decision_id`

This seam should:

- use analyzer-owned current-resolution derivation rather than newest-first caller inference
- serve one thin current-governance-status object
- fail closed when no current resolution exists for the requested scope
- fail closed when the linked chain is missing or inconsistent

This slice should not require:

- host UI
- new mutation routes
- override actions
- deploy/unlock semantics

The lighter alternative was considered:

- extending the existing `EvaluationCurrentDispositionResolutionResponse` directly

The default recommendation remains a separate semantic status route because it keeps raw resolution inspection and derived governance meaning distinct.
But if implementation review proves a route split is unnecessary, the acceptable fallback is:

- extend the existing current-resolution response shape in place

provided it still adds:

- authoritative `effective_governance_status`
- retrieval-time linked-chain verification
- served `scope_label`

## Must land

The next slice should be treated as complete only if all of the following are true:

1. one analyzer-owned semantic current-governance-status object exists
2. one canonical derivation law exists over exact `resolution_key + gate_decision_id`
3. one read-only retrieval seam serves that status
4. the served object cites exact current resolution/review/gate identities
5. the derivation fails closed on missing or inconsistent linked chain state
6. the served object keeps retrospective frozen-pack honesty visible
7. callers no longer need to interpret raw current-resolution fields themselves to answer the current-governance question
8. the slice is materially additive over `/resolutions/current`, not a nominal rename

## Must not widen

- do not add host UI in this slice
- do not add auth or identity-management product
- do not add new resolution/review/gate write semantics
- do not turn status into deploy/unlock enforcement in this slice
- do not let consumers invent their own “current governance” stitching law
- do not revive the March 19 workspace line as the active next step

## Review focus

The most useful review questions for this memo are:

1. whether bounded current-governance status is genuinely the right next Stage 15 seam after persisted resolution now exists
2. whether the first status object should remain derived-only rather than persisted
3. whether `resolution_key + gate_decision_id` remains the right declared scope for the first served current-status seam
4. whether a separate semantic status route is justified, or whether the lighter alternative of extending `/resolutions/current` is better
5. whether this seam would be enough to close the bounded current Stage 15 line, or whether another prerequisite still remains

## Next artifact

If this scope survives review, the next artifact should be a concrete implementation plan for:

- one analyzer-owned semantic current-governance-status object
- one canonical derivation law over current resolution scope
- one read-only current-status route

If this seam lands as a genuinely additive derived contract with semantic status law and fail-closed chain verification, it is the likely bounded closeout seam for the current Stage 15 line.
If it collapses into a thin rename of `/resolutions/current`, Stage 15 should remain open.
