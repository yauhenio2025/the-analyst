# Memo: Phase D Cross-Campaign Planner-To-Presentation Governance V1 Completion

Subtitle: The second planner-to-presentation governance family proving anti-coupling across proof campaigns

Date: 2026-03-30
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Implements:
- `communications/MEMO_2026-03-30_phase_d_cross_campaign_planner_to_presentation_governance_scope.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-30_phase_d_planner_to_presentation_governance_family_v1_completion.md`
Review:
- `communications/REPORT_Claude_Phase_D_Cross_Campaign_Planner_To_Presentation_Governance_Scope_Critique_2026-03-30.md`
- `communications/REPORT_Codex_Phase_D_Cross_Campaign_Planner_To_Presentation_Governance_Scope_Audit_2026-03-30.md`

## Purpose

Record what actually landed in the cross-campaign planner-to-presentation governance slice.

This is a Phase D completion memo.
It is still not a claim that analyzer-v2 has reached Phase E generality proof.

## Outcome

The cross-campaign planner-to-presentation governance slice is now implemented and verified.

Analyzer-v2 now has a second upstream governance family over frozen planner-to-presentation composition decision artifacts, using a fresh paired proof campaign distinct from the first family's March 27-30 / March 28 lineage:

- pack:
  - `phase4_planner_to_presentation_cross_campaign_governance_v1`
- gate:
  - `bounded_planner_to_presentation_cross_campaign_readiness_v1`
- review:
  - `bounded_planner_to_presentation_cross_campaign_review_v1`
- resolution:
  - `bounded_planner_to_presentation_cross_campaign_resolution_v1`

This slice sits on top of the already-landed governance substrate without:

- new route shapes
- new persisted governance object shapes
- new gate/review/resolution laws
- new current-selection laws
- new semantic governance-status law

It extended the existing `planner_presentation_decision` evaluator family with:

- two new case spec entries in `_PLANNER_PRESENTATION_CASE_SPECS`
- two new extraction branches in `_extract_planner_presentation_evidence`
- a `bundle_planning_decision_id` binding field on the evidence dataclass for fresh-campaign proof bundles
- a `requires_bundle_binding` gate so binding metadata validation is applied only to fresh-campaign cases

## What Landed

### 1. One fresh paired proof campaign under communications/

Two new frozen proof bundles with distinct artifact identities from the first family:

- AOI:
  - `communications/PROOF_phase_d_cross_campaign_aoi_transient_compose_2026-03-30.json`
  - `planning_decision_id = planning-decision-d6b6bb0cd7ac`
  - `workflow_key = anxiety_of_influence_thematic_single_thinker`
  - `consumer_key = the-critic`
  - `source_v2_job_id = job-744edf255ad5`

- Genealogy:
  - `communications/PROOF_phase_d_cross_campaign_genealogy_transient_compose_2026-03-30.json`
  - `planning_decision_id = planning-decision-5f5b0182f2f9`
  - `workflow_key = intellectual_genealogy`
  - `consumer_key = the-critic`
  - `source_v2_job_id = proof-round4-adaptive-balance-final-1774012011`

Both bundles carry on one frozen proof surface:

- planning decision evidence
- persisted planning snapshot evidence
- compose request evidence (via `compose_from_selection` or `compose_from_intent` wrapper)
- compose response evidence
- stable `planning_decision_id` binding at both bundle level and nested compose wrapper level

The genealogy bundle includes explicit `planning_decision_id` binding metadata inside the `compose_from_intent` wrapper, compensating for the fact that the public `/v1/presenter/compose-from-intent` request contract does not carry that field.

### 2. One second planner-to-presentation governance family

The pack is intentionally bounded to two cases:

- `aoi_compose_selection_current_contract_fresh_campaign`
- `genealogy_direct_sections_compose_current_contract_fresh_campaign`

Both cases reuse `evaluator_key = planner_presentation_decision` and the same four dimensions:

- `handoff_contract_fidelity`
- `planner_presentation_agreement`
- `presentation_contract_fidelity`
- `composition_trace_integrity`

### 3. Evaluator extension with binding validation

The existing evaluator was extended, not replaced:

- New `_PLANNER_PRESENTATION_CASE_SPECS` entries at harness lines 160 and 199
- New extraction branches at harness lines 1678 and 1776
- The AOI dispatch was widened to `case_key in {"aoi_compose_selection_current_contract", "aoi_compose_selection_current_contract_fresh_campaign"}` rather than adding a separate branch
- Fresh-campaign cases validate `bundle_planning_decision_id` (top-level) and `compose_binding_planning_decision_id` (nested wrapper) against the declared `subject_identity`
- Older cases continue to work unchanged with `requires_bundle_binding = False`

### 4. One bounded gate/review/resolution chain

Analyzer-v2 now defines one full second governance chain over that pack:

- `bounded_planner_to_presentation_cross_campaign_readiness_v1`
- `bounded_planner_to_presentation_cross_campaign_review_v1`
- `bounded_planner_to_presentation_cross_campaign_resolution_v1`

The gate requires both fresh-campaign cases and all four composition-facing dimensions.

The review and resolution layers reuse the already-landed bounded laws unchanged:

- review remains `accept / reject / waive`
- resolution remains recording-only in v1
- currentness remains analyzer-owned over:
  - `resolution_key + gate_decision_id`

### 5. One real second-family governance chain

One real cross-campaign governance chain now exists on disk:

- reports:
  - `evaluation-report-14f259bb7d9b`
  - `evaluation-report-a3bbdcfc502f`
- gate:
  - `gate-decision-358bb4899246`
- review:
  - `review-decision-587339b5da96`
- resolution:
  - `resolution-cf3da3461d60`

The unchanged semantic route serves that chain successfully:

- `GET /v1/evaluations/governance-status/current?resolution_key=bounded_planner_to_presentation_cross_campaign_resolution_v1&gate_decision_id=gate-decision-358bb4899246`

Returned result:

- `200`
- `effective_governance_status = approved`

## Verification

Focused verification passed:

- `PYTHONPATH=. pytest -q tests/test_frozen_governance_pack.py tests/test_bounded_release_gate.py tests/test_bounded_review_disposition.py tests/test_bounded_disposition_resolution.py tests/test_evaluation_governance_status.py tests/test_evaluation_governance_status_routes.py`
  - result: `95 passed, 2 warnings`

The real cross-campaign chain is present in:

- `src/evaluations/reports/evaluation-report-14f259bb7d9b.json`
- `src/evaluations/reports/evaluation-report-a3bbdcfc502f.json`
- `src/evaluations/gates/gate-decision-358bb4899246.json`
- `src/evaluations/reviews/review-decision-587339b5da96.json`
- `src/evaluations/resolutions/resolution-cf3da3461d60.json`

Documentary honesty note:

- the repo is already dirty/untracked, so confinement is supported by current content inspection and live behavior rather than a clean baseline diff

## Honest Boundary

### What is now true

- Phase D governance now covers:
  - downstream AOI/genealogy result and lifecycle families
  - standalone governance coverage across the two currently supported evaluator substrates
  - one upstream routing/planning decision family
  - one upstream planner-to-presentation composition family
  - one second upstream planner-to-presentation composition family over a fresh paired proof campaign
- the planner-to-presentation governance law is not artifact-identity-coupled to only the first March 27-30 / March 28 proof lineage
- the same evaluator family, gate law, review law, resolution law, and governance-status derivation survive a second distinct proof campaign without changes to route shapes, schema shapes, or governance-status semantics
- the Phase D exit signal from the distilled roadmap is now met:
  - "one second materially distinct proof campaign showing the governance stack is not only a wrapper around one frozen dossier"

### What is not yet true

- the anti-coupling proof covers different artifact identities and different frozen bundle files, but both campaigns still use the same two workflow families (`anxiety_of_influence_thematic_single_thinker` + `intellectual_genealogy`) and the same consumer (`the-critic`)
- true proof-shape generality across different workflow families remains a Phase E question
- there is still no broader review/override product flow
- there is still no downstream enforcement or unlock/deny seam over current governance status
- this still does not justify saying Phase E generality proof has begun in earnest

### What the calibrated anti-coupling claim is

The honest claim is:

- governance is not artifact-identity-coupled to only one proof lineage

The honest non-claim is:

- governance has not yet been tested across fundamentally different proof shapes, workflow families, or consumer surfaces

That distinction is the boundary between Phase D and Phase E.

## Decision

The cross-campaign planner-to-presentation governance slice is complete.

The Phase D exit signal from the distilled roadmap is now met.

The program's next strategic question is no longer a Phase D governance question. It is a Phase E generality question:

- can analyzer-v2 compose and render across representative engine/output families without per-app intelligence?

That is the right next horizon.
