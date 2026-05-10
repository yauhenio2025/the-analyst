# Memo: Phase 4 Bounded Release Gate Scope

Subtitle: First concrete enforcement point over persisted frozen governance reports

Date: 2026-03-29
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-29_phase4_bounded_governance_evaluation_v1_completion.md`
Relevant Prior Memos:
- `communications/MEMO_2026-03-28_phase4_bounded_governance_evaluation_scope.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_closeout.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_completion.md`
- `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`
- `communications/MEMO_2026-03-19_phase4_cross_workflow_workspace_scope.md` as an older, still-superseded workspace line and not the active next step

## Purpose

Define the next bounded Stage 15 slice after the governance/evaluation report substrate now exists.

This memo is not an implementation plan.
It is the scoping memo for the next concrete enforcement-point slice.

The next step should not be:

- a human approval UI
- a broad review/override application
- a fresh live-rerun governance campaign
- a revival of the March 19 generic workspace proof line
- a broadened publish/share program

The next step should be:

- one bounded analyzer-owned release gate over persisted evaluation reports

## Anti-drift filter

This scope passes the fixed-direction prioritization filter because:

1. it moves governance decision-making further upstream into analyzer-v2
2. it does not add new consumer-owned workflow logic
3. it generalizes across the two already-frozen bounded cases rather than reopening AOI-only work
4. it would still matter if the current host app were replaced later

## Why this is now the right next slice

The March 29 bounded governance/evaluation v1 completion changed the boundary.

What is now true:

- analyzer-v2 can persist thin evaluation reports as first-class governance objects
- the AOI exemplar and genealogy lifecycle cases can now be normalized into one shared report substrate despite unlike evidence paths
- the frozen governance pack is real, pinned, and reproducible
- a read-only report-inspection seam now exists

What is still missing is the first concrete enforcement point.

Right now the system can say:

- here are the reports

But it still cannot say:

- here is the bounded gate decision derived from those reports
- here is the exact required-case matrix
- here is the deterministic pass/fail/error outcome for the pack as a whole

That makes the next missing seam operational rather than structural.

## Current code-backed boundary

### What already exists

- analyzer-owned evaluation report schemas:
  - `src/evaluations/schemas.py`
- analyzer-owned report persistence:
  - `src/evaluations/report_store.py`
- code-defined frozen pack definitions:
  - `src/evaluations/frozen_pack_definitions.py`
- deterministic frozen-pack harness:
  - `src/evaluations/frozen_pack_harness.py`
- read-only report routes:
  - `src/api/routes/evaluations.py`
- stable upstream truth reused by the reports:
  - `src/analysis_products/result_contract.py`
  - `src/analysis_products/source_backed_readiness.py`
  - `src/presenter/compose_session_store.py`
  - `src/orchestrator/planning_decision_store.py`
  - `src/executor/db.py`
  - executor read-layer functions and routes
- persisted passing reports already materialized for:
  - `aoi_exemplar_march27_execution_backed`
  - `genealogy_lifecycle_march28_session_reopen`

### What does not yet exist

- no analyzer-owned gate-decision object
- no persisted pack-level verdict over a specific report set
- no deterministic rule table that says which case-level verdicts and dimensions are required for bounded pass
- no read-only gate-inspection seam
- no concrete enforcement point that turns “reports exist” into “the bounded pack passes/fails/errors”

## Strategic decision

The next Stage 15 slice should be:

- one bounded analyzer-owned release gate over persisted evaluation reports

It should not be:

- a human approval product
- a host-side review dashboard
- a generic override system
- a new live-proof campaign

The default bounded shape should be:

- one gate decision object over one named frozen pack
- one deterministic rule set
- one core gate builder over explicit persisted `evaluation_report_id` inputs
- one convenience harness that can materialize fresh reports and then call that core gate builder
- one read-only retrieval seam

## Scope decision

### In scope

The next slice should land all of the following together.

#### 1. One analyzer-owned gate decision object and store

Add one bounded persistent object, for example `PersistedEvaluationGateDecision`, stored analyzer-side in file-backed JSON parallel to evaluation reports.

Default storage path:

- `src/evaluations/gates/`

Required properties:

- analyzer-generated `gate_decision_id`
- `created_at`
- `gate_key`
- `gate_definition_version`
- `evaluation_pack_key`
- exact input report ids by `case_key`
- `contains_live_revalidation`
- required verdict policy
- required dimensions by `case_key`
- inlined gate rule table
- per-case verdict summary
- overall gate verdict
- ordered blocking reasons

This object is the first enforcement-point object.
Not the raw report.
Not the memo.
Not the harness console output.

It should stay thin and cite the report ids and decision rules it used.
It should not duplicate full report payloads into a second truth store.

Accumulation policy for v1 should be explicit:

- gate decisions accumulate historically
- multiple gate decisions for the same `gate_key` and `evaluation_pack_key` are expected
- list results should return newest-first
- there is no single “active gate” constraint in v1

#### 2. One fixed bounded gate definition

Add one code-defined gate, for example:

- `bounded_platform_readiness_v1`

It should apply only to:

- `phase4_frozen_governance_v1`

The first rule set should be deterministic and explicit.

Default rule:

- AOI case report must be `pass`
- genealogy case report must be `pass`
- AOI required dimensions:
  - `selection_fit`
  - `rationale_clarity`
  - `rendered_usefulness`
  - `operational_behavior`
- genealogy required dimensions:
  - `identity_integrity`
  - `saved_truth_fidelity`
  - `reopen_integrity`
  - `boundary_observance`
- all required dimensions on both reports must be `pass`
- any missing required dimension yields gate `error`
- any required `error` yields gate `error`
- any required `fail` yields gate `fail`
- only all-required-pass yields gate `pass`

The gate should remain explicitly retrospective and frozen-pack-scoped.
It must not be misrepresented as a fresh live release decision over arbitrary current head behavior.

Because the input reports may mix live revalidation checks with pinned frozen-artifact checks, the gate decision should carry:

- `contains_live_revalidation: bool`

This is an honesty label, not a widening of the evidence model.

#### 3. One deterministic gate harness

There should be one deliberate way to materialize the gate decision.

Recommended bounded shape:

- one core gate builder that consumes:
  - `gate_key`
  - `evaluation_pack_key`
  - exact input report ids by `case_key`
- one analyzer-owned convenience harness that:
  - materializes the frozen report set for the named pack
  - passes the returned report ids into that core gate builder
  - persists one gate decision over those exact report ids
  - prints the resulting `gate_decision_id` and overall verdict

The authoritative contract should be explicit input report ids, not “use whichever latest reports happen to be lying around.”
Generate-then-gate should remain the default convenience path because it is cleaner for deterministic bounded runs, but it should be implemented as a wrapper over the explicit-id core contract.

The gate decision must record the exact report ids it used so replay and audit stay honest.

#### 4. One read-only gate inspection seam

Add one analyzer-owned retrieval seam for the new gate decisions, for example:

- `GET /v1/evaluations/gates/{gate_decision_id}`
- `GET /v1/evaluations/gates?gate_key=...&evaluation_pack_key=...&limit=...`

This remains read-only in v1.
No API mutation/generation route is required for gate creation.

## Must land

The next slice should be treated as complete only if all of the following are true:

1. one analyzer-owned gate decision object exists
2. one fixed gate definition exists over `phase4_frozen_governance_v1`
3. the gate cites exact input report ids and required dimensions
4. the gate fails closed if required reports are missing, mismatched, non-passing, or missing required dimensions
5. one deterministic harness materializes the gate decision
6. one read-only gate-inspection seam exists

## Must not widen

- do not build human approval UI in this slice
- do not build a generic override system in this slice
- do not reopen fresh browser proofs by default
- do not let the gate silently consume arbitrary latest reports without recording exact input ids
- do not revive the March 19 workspace proof line as the active next step
- do not use the gate as a substitute for unfinished contract work elsewhere

## Primary code and evidence surfaces to scrutinize

The main surfaces for this scope are:

- `/home/evgeny/projects/analyzer-v2/src/evaluations/schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/evaluations/report_store.py`
- `/home/evgeny/projects/analyzer-v2/src/evaluations/frozen_pack_definitions.py`
- `/home/evgeny/projects/analyzer-v2/src/evaluations/frozen_pack_harness.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/evaluations.py`
- the persisted evaluation reports under:
  - `/home/evgeny/projects/analyzer-v2/src/evaluations/reports/`
- the prior Phase 4 scope and completion memos
- the fixed-direction and canonical roadmap memos

If review finds that the right next step is a review/override seam before a gate decision, that should be stated explicitly.
But the default should be:

- one bounded analyzer-owned gate over the now-existing reports

not:

- a jump straight to UI review or human override

## Acceptance bar

The scope is correct only if the later implementation can honestly deliver:

- one analyzer-owned gate decision object
- one fixed deterministic gate over the frozen two-case pack
- one core explicit-id gate builder plus one generate-then-gate harness wrapper
- one read-only inspection seam for gate decisions
- no dependence on fresh live reruns or UI work

## Next-step intent

If this scope survives review, the next artifact should be a concrete implementation plan for:

- bounded analyzer-owned gate decisions
- one deterministic gate harness over `phase4_frozen_governance_v1`
- one read-only gate-inspection seam

That would be the next real Stage 15 follow-on slice after “evaluation reports exist.”
