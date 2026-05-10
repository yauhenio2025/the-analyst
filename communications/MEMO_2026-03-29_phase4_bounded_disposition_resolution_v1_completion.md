# Memo: Phase 4 Bounded Disposition Resolution V1 Completion

Subtitle: Analyzer-owned current-disposition resolution, canonical current lookup, and read-only resolution inspection

Date: 2026-03-29
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Implements:
- `communications/MEMO_2026-03-29_phase4_bounded_disposition_resolution_scope.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-29_phase4_bounded_review_disposition_v1_completion.md`

## Purpose

Record what actually landed in the fourth bounded Phase 4 slice.

This memo is a completion memo for the bounded disposition-resolution slice.
It is not a claim that Stage 15 is now fully closed.

## Outcome

The bounded Phase 4 disposition-resolution slice is now implemented and verified.

Analyzer-v2 now has:

- one analyzer-owned `PersistedEvaluationDispositionResolution` substrate
- one fixed bounded resolution definition over `bounded_platform_readiness_review_v1`
- one exact-`review_decision_id` CLI write path for recording the adopted current stance
- one canonical current-resolution lookup law owned by analyzer-v2
- one read-only resolution-inspection seam

What landed is real and operational.
What still does not exist is equally important:

- no analyzer-owned current-governance-status seam that serves the effective current stance without caller-side stitching across resolution, review, and gate objects
- no downstream enforcement or deploy/unlock semantics driven by resolution truth
- no broader override framework
- no host-side governance UI

So Phase 4 is now materially advanced again, but not closed.

## What Landed

### 1. Analyzer-owned disposition-resolution substrate

Analyzer-v2 now persists thin current-disposition resolution objects under `src/evaluations/`.

The landed bounded pieces are:

- `src/evaluations/resolution_schemas.py`
- `src/evaluations/resolution_store.py`
- `src/evaluations/resolution_definitions.py`
- `src/evaluations/resolution_builder.py`

This slice establishes `PersistedEvaluationDispositionResolution` as the first explicit governance object that says which exact persisted review is currently adopted as the analyzer-owned stance for a bounded declared scope.
It is not just an operator convention about “latest review wins.”

### 2. One fixed bounded resolution law

The first bounded resolution definition now exists in code as:

- `bounded_platform_readiness_resolution_v1`

It applies only to:

- `bounded_platform_readiness_review_v1`
- `bounded_platform_readiness_v1`
- `phase4_frozen_governance_v1`

The builder now enforces the correct authority boundary:

- the write path consumes one exact `review_decision_id`
- the resolution definition is the source of truth for the accepted review/gate chain
- all linked fields are derived from the loaded persisted review
- gate loading is not reopened as a required dependency in v1

The write path fails closed on:

- missing review decision
- review/definition mismatch on `review_key`, `review_definition_version`, `gate_key`, `gate_definition_version`, or `evaluation_pack_key`
- blank resolver identity fields
- blank resolution note

### 3. Canonical current-resolution lookup now exists

Analyzer-v2 now owns the “current adopted stance” derivation instead of forcing callers to infer it from newest-first list ordering.

The canonical accessor now lives in the store layer:

- `load_current_evaluation_disposition_resolution(resolution_key, gate_decision_id)`

The bounded current scope in v1 is:

- `resolution_key + gate_decision_id`

The current adopted stance for that scope is:

- the newest persisted resolution whose `resolution_key` and `gate_decision_id` both match

This remains query-time derivation.
No mutable `is_current` flag was introduced.

### 4. Read-only resolution inspection seam

Analyzer-v2 now exposes:

- `GET /v1/evaluations/resolutions/current?resolution_key=...&gate_decision_id=...`
- `GET /v1/evaluations/resolutions/{resolution_id}`
- `GET /v1/evaluations/resolutions?resolution_key=...&review_decision_id=...&gate_decision_id=...&evaluation_pack_key=...&limit=...`

The route ordering was also made explicit so:

- `/resolutions/current` is registered before `/resolutions/{resolution_id}`

That prevents `current` from being swallowed by the path-param route.

### 5. Real persisted resolution now exists

The real harness command is now operational:

- `PYTHONPATH=. python -m src.evaluations.resolution_builder --resolution-key bounded_platform_readiness_resolution_v1 --review-decision-id review-decision-21edf9b955ee --resolver-name Codex --resolver-role operator --resolution-note "..."`

During the implementation pass, it persisted a real resolution:

- `resolution-4738c6e0efab`

That resolution cites:

- exact `review_decision_id = review-decision-21edf9b955ee`
- exact `gate_decision_id = gate-decision-745c2cb7e090`
- `resolution_key = bounded_platform_readiness_resolution_v1`
- derived `adopted_review_disposition = accept`
- derived `observed_gate_verdict = pass`
- derived `contains_live_revalidation = true`

## Verification

Focused verification passed:

- `PYTHONPATH=. pytest -q tests/test_evaluation_resolution_store.py tests/test_evaluation_resolution_routes.py tests/test_bounded_disposition_resolution.py tests/test_evaluation_review_store.py tests/test_evaluation_review_routes.py tests/test_bounded_review_disposition.py tests/test_evaluation_gate_store.py tests/test_evaluation_gate_routes.py tests/test_bounded_release_gate.py`
  - result: `51 passed`

The real resolution builder also passed:

- `PYTHONPATH=. python -m src.evaluations.resolution_builder --resolution-key bounded_platform_readiness_resolution_v1 --review-decision-id review-decision-21edf9b955ee --resolver-name Codex --resolver-role operator --resolution-note "..."`
  - result: `0` exit status
  - result: one persisted current-disposition resolution over the live bounded review/gate chain

The real read-only resolution routes are now available through the app:

- `GET /v1/evaluations/resolutions/current?resolution_key=bounded_platform_readiness_resolution_v1&gate_decision_id=gate-decision-745c2cb7e090`
- `GET /v1/evaluations/resolutions/resolution-4738c6e0efab`
- `GET /v1/evaluations/resolutions?resolution_key=bounded_platform_readiness_resolution_v1&limit=5`

## Honest Boundary

### What is now true

- analyzer-v2 can now persist a concrete current-disposition resolution as a first-class governance object
- analyzer-v2, not the caller, now owns the bounded “current adopted stance” derivation for `resolution_key + gate_decision_id`
- the frozen AOI-plus-genealogy governance pack now has a real human-governance object above reports, gates, and reviews
- one deliberate read-only inspection seam now exists for reports, gates, reviews, and resolutions
- the resolution layer remains honest about retrospective mixed-evidence governance by carrying derived `contains_live_revalidation`

### What is not yet true

- there is still no analyzer-owned current-governance-status seam that serves the effective current stance as one thin derived object
- there is still no downstream consumption or enforcement of the current resolution
- there is still no broader override framework
- there is still no host-side governance dashboard or approval UI

### Residual low-risk debt

- the canonical current accessor currently chooses “newest” by `created_at` string ordering
- that is correct for builder-produced UTC timestamps, but tie-break semantics for equal or manually edited timestamps are not yet hardened
- this is a small hardening follow-up, not a v1 correctness blocker

## Decision

The bounded Phase 4 disposition-resolution slice is complete.

But Phase 4 overall is still not closed.

The next honest main line inside Stage 15 should be:

- one bounded analyzer-owned current-governance-status seam over the current resolution/review/gate chain

It should not be:

- a jump to downstream enforcement
- a broad override product
- a host-side governance dashboard
- a fresh live-rerun governance campaign

## Next Artifact

The next artifact should be a scope memo for a bounded Phase 4 follow-on that adds:

- one analyzer-owned current-governance-status object derived from the current resolution scope
- one authoritative read-only seam for serving that current status
- no new write semantics and no downstream enforcement in the same slice

That is the next real governance seam after “current-disposition resolution exists.”
