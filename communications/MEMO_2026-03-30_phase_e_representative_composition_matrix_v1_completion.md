# Memo: Phase E Representative Composition Matrix V1 Completion

Subtitle: The first bounded generality proof over the full live compose substrate on the current transient consumer surface

Date: 2026-03-30
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Implements:
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_scope.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-30_phase_d_cross_campaign_planner_to_presentation_governance_v1_completion.md`
Review:
- `communications/REPORT_Claude_Phase_E_Representative_Composition_Matrix_Scope_Critique_2026-03-30.md`
- `communications/REPORT_Codex_Phase_E_Representative_Composition_Matrix_Scope_Audit_2026-03-30.md`

## Purpose

Record what actually landed in the first bounded Phase E slice.

This is not another Phase D governance memo.
It records the first direct generality proof over the live compose substrate already in repo.

## Outcome

The representative composition matrix slice is now implemented and verified.

Analyzer-v2 now has one frozen-artifact matrix proof over the full currently live transient compose substrate on the current enforced transient consumer surface:

1. AOI `source_profile`
   - `POST /v1/presenter/compose-from-source`
   - dossier profile
2. AOI `source_selection`
   - planner-backed handoff into `POST /v1/presenter/compose-from-selection`
3. genealogy `direct_sections`
   - planner-backed lowering into `POST /v1/presenter/compose-from-intent`

This slice landed without:

- new public routes
- new request or response schemas
- new governance families
- new evaluator architecture
- new production runtime infrastructure

It is proof by frozen artifacts plus tests.

## What Landed

### 1. Three frozen proof bundles under `communications/`

The matrix is anchored by three committed proof bundles:

- `communications/PROOF_phase_e_matrix_aoi_source_profile_dossier_2026-03-30.json`
- `communications/PROOF_phase_e_matrix_aoi_source_selection_2026-03-30.json`
- `communications/PROOF_phase_e_matrix_genealogy_direct_sections_2026-03-30.json`

These bundles together cover the full currently live handoff-family substrate exposed by the transient compose layer:

- `source_profile`
- `source_selection`
- `direct_sections`

All three bundles include:

- `captured_at`
- `case_key`
- `route_family`
- `workflow_key`
- `consumer_key`
- `source_v2_job_id`
- `compose_call`
- `request_json`
- `response_json`

The two planner-backed bundles also include:

- `planning_decision_id`
- `planning_snapshot`

The genealogy bundle additionally includes:

- `lowering_call`
- `lowering_response_json`

This keeps the lowering seam honest:

- the lowering route is modeled as a real `GET` metadata surface
- not as a fictional JSON request body

### 2. One dedicated matrix test seam

One new test file now owns the matrix proof:

- `tests/test_representative_composition_matrix.py`

That seam validates all three bundles mechanically against the live contracts:

- request JSON validates against the correct live request schema
- response JSON validates against `ComposeFromIntentResponse`
- `presentation.view_count == len(generated_view_definitions)`
- resolver versions match the three route families:
  - `compose-from-source-v3`
  - `compose-from-selection-v1`
  - `compose-from-intent-v2`
- `consumer_key == the-critic`
- workflow keys match the declared cases

### 3. Mechanical no-host-reconstruction checks

The test seam does not treat “no host-side semantic reconstruction” as a slogan.
It encodes it mechanically:

- AOI `source_selection`
  - the final `ComposeFromSelectionRequest` equals the request-truth fields derivable from the frozen `AoiCompositionHandoffPlan`
  - the planner-only source-family law remains on the frozen handoff plan rather than being mixed into the request contract
- genealogy `direct_sections`
  - `lowering_response_json == request_json`
  - `planning_decision_id` is tied across bundle metadata, frozen snapshot, and lowering-call metadata
  - the final compose request is directly derivable from the frozen `DirectSectionsCompositionHandoffPlan`

### 4. One follow-up hardening pass

After the first implementation pass, the matrix test was tightened further.

The planner-backed AOI and genealogy cases now also assert `source_v2_job_id` consistency across:

- bundle-level metadata
- frozen planning snapshot
- the relevant handoff plan

This closed the only low bundle-consistency gap called out after implementation.

## Verification

Focused verification passed:

- `PYTHONPATH=. pytest -q tests/test_representative_composition_matrix.py tests/test_compose_from_intent.py tests/test_task_router.py tests/test_task_planner.py tests/test_run_contract.py`
  - result: `72 passed, 29 warnings`

Important implementation fact:

- no presenter or orchestrator runtime code needed to change for this slice
- the work is documentary proof bundles plus the new matrix test seam

## Honest Boundary

### What is now true

- analyzer-v2 now has one bounded representative composition proof over the full currently live transient compose substrate
- the proof varies composition/handoff family while keeping the host boundary and served response shape fixed
- AOI `source_profile`, AOI `source_selection`, and genealogy `direct_sections` all converge honestly on the same served response model:
  - `ComposeFromIntentResponse`
- the matrix proves representative composition law over the currently live handoff-family substrate without host-specific analytical reconstruction on the current transient consumer surface

### What is not yet true

- transient compose is still structurally single-consumer at runtime:
  - `the-critic` remains the only registered transient consumer adapter
- this does not prove second-consumer transient serving
- this does not prove arbitrary engine/pass composition
- this does not prove open-ended workflow-family generality
- this does not prove consumer generality

### What the calibrated Phase E claim is

The honest claim is:

- analyzer-v2 can already compose and serve a small representative matrix of live handoff families through one common transient response law on the current transient consumer surface

The honest non-claim is:

- analyzer-v2 has not yet proven that the same transient compose substrate serves more than one consumer without host-local analytical reconstruction

That second-consumer seam is the next meaningful bounded Phase E question.

## Decision

The first bounded Phase E slice is complete.

The next honest Phase E step is no longer another same-consumer handoff-family proof.
That question has been answered for the currently live substrate.

The next bounded question is:

- can the same transient compose substrate serve one real second consumer without rebuilding analytical meaning locally?

The smallest honest target for that question is:

- `aoi-canary`

That is the next strategic horizon.
