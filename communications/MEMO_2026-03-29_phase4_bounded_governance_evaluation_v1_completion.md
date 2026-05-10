# Memo: Phase 4 Bounded Governance/Evaluation V1 Completion

Subtitle: Analyzer-owned evaluation reports, frozen two-case governance pack, deterministic harness, and read-only inspection seam

Date: 2026-03-29
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Implements:
- `communications/MEMO_2026-03-28_phase4_bounded_governance_evaluation_scope.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_completion.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_closeout.md`

## Purpose

Record what actually landed in the first bounded Phase 4 slice.

This memo is a completion memo for the bounded governance/evaluation v1 slice.
It is not a claim that all of Stage 15 is now closed.

## Outcome

The bounded Phase 4 governance/evaluation v1 slice is now implemented and verified.

Analyzer-v2 now has:

- one analyzer-owned `PersistedEvaluationReport` substrate
- one frozen two-case governance pack spanning unlike evidence locations
- one deterministic frozen-pack harness
- one read-only evaluation-report inspection seam

What landed is real and operational.
What did not land yet is equally important:

- no pack-level release gate exists yet
- no human approval or override flow exists yet
- no broader live-rerun governance campaign exists yet

So Stage 15 is now materially advanced, but not closed.

## What Landed

### 1. Analyzer-owned evaluation report substrate

Analyzer-v2 now persists thin governance reports under `src/evaluations/`.

The landed bounded pieces are:

- `src/evaluations/schemas.py`
- `src/evaluations/report_store.py`
- `src/evaluations/frozen_pack_definitions.py`
- `src/evaluations/frozen_pack_harness.py`
- `src/api/routes/evaluations.py`

This slice establishes `PersistedEvaluationReport` as the governance object.
It is not just a memo, not just a HAR, and not just raw frozen proof JSON.

### 2. One frozen two-case composite pack

The first frozen governance pack now exists in code as:

- `phase4_frozen_governance_v1`

It evaluates:

1. AOI exemplar closeout
   - primary subject: `job-744edf255ad5`
2. Genealogy lifecycle closeout
   - primary subject: `compose-session-0877864dcca7`

The AOI case remains explicitly executor-backed and composite.
The genealogy case remains explicitly session-centric, with `planning_decision_id` treated as provenance rather than lifecycle identity.

Frozen proof artifacts are SHA-256 pinned and fail closed on drift.

### 3. Deterministic harness and real persisted reports

The harness command is now real:

- `PYTHONPATH=. python -m src.evaluations.frozen_pack_harness --pack-key phase4_frozen_governance_v1`

It evaluates both cases, persists one report per case, and returns report ids plus verdicts.

During the completion pass, the report store contained current passing reports for the frozen pack, including:

- `evaluation-report-48208f4ba042`
- `evaluation-report-f5f45e18d2d0`

### 4. Read-only inspection seam

Analyzer-v2 now exposes:

- `GET /v1/evaluations/reports/{evaluation_report_id}`
- `GET /v1/evaluations/reports?evaluation_pack_key=...&case_key=...&limit=...`

This is the bounded first inspection seam.
No mutation API for report generation was added in v1.

### 5. Honesty repair on mixed evidence metadata

One important post-implementation correction was required.

The first genealogy `saved_truth_fidelity` check initially mixed stored-object and frozen-artifact evidence under one check-level evidence mode.
That is now repaired.

The genealogy fidelity proof is now split into two honest checks:

- `stored_session_fidelity_fields_present`
- `frozen_saved_session_artifact_valid`

`saved_truth_fidelity` is now a dimension over those two checks rather than a mixed-mode single check.

## Verification

Focused verification passed:

- `PYTHONPATH=. pytest -q tests/test_evaluation_report_store.py tests/test_evaluations_route.py tests/test_frozen_governance_pack.py`
  - result: `8 passed`

The real harness also passed:

- `PYTHONPATH=. python -m src.evaluations.frozen_pack_harness --pack-key phase4_frozen_governance_v1`
  - result: `0` exit status
  - result: one passing AOI report and one passing genealogy report persisted

## Honest Boundary

### What is now true

- analyzer-v2 can normalize unlike AOI and genealogy evidence paths into one shared report substrate
- frozen proof artifacts are now pinned and checked rather than treated as informal sidecars
- persisted governance reports now exist as first-class analyzer-owned objects
- one deliberate read-only inspection seam now exists for those reports
- one deterministic harness can reproduce the frozen two-case report set

### What is not yet true

- there is still no analyzer-owned pack-level gate or release decision object
- there is still no explicit enforcement point over report verdicts
- there is still no broader human review/override flow
- there is still no live-governance policy over fresh reruns beyond this frozen retrospective pack

## Decision

The bounded Phase 4 governance/evaluation v1 slice is complete.

But Phase 4 overall is not closed.

The next honest main line inside Stage 15 should be:

- one bounded analyzer-owned release gate over persisted evaluation reports

It should not be:

- a revival of the older March 19 generic workspace proof line
- a jump straight to human approval UI
- a broad fresh-live-rerun governance campaign

## Next Artifact

The next artifact should be a scope memo for a bounded Stage 15 follow-on:

- one analyzer-owned gate decision object over the frozen evaluation pack
- one deterministic gate harness
- one read-only gate-inspection seam

That is the next real enforcement-point slice after “reports exist.”
