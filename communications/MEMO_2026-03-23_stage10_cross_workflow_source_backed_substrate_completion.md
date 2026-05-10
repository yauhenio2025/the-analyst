# Memo: Stage 10 / Cross-Workflow Source-Backed Substrate Completion

Date: 2026-03-23  
Program: Dynamic Bespoke Apps Platformization  
Scope Memo: `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md`  
Proof Memo: `communications/PROOF_2026-03-23_stage10_cross_workflow_source_backed_substrate.md`

## Result

Stage 10 implementation is complete for the bounded slice that was actually scoped:

- one shared read-only readiness contract over durable AOI and genealogy result truth

This memo closes the code and focused verification record for that slice.

It does **not** claim that analyzer-v2 now has:

- generic selector law across workflows
- AOI runtime `composition_mode` readiness
- host-neutral AOI followup
- planner-driven selector choice
- generalized page planning
- broad workflow coverage beyond AOI plus genealogy

The honest program state is now:

- Stage 10 readiness boundary implemented
- focused verification complete
- proof artifacts saved
- roadmap Stage 10 advanced to partial
- broader selector, host, and page-planning work still open

## Bounded Claim Landed

The bounded Stage 10 claim was:

- analyzer-v2 should expose one read-only results-layer readiness seam that can report workflow-owned selector feasibility over durable result identity for both AOI and genealogy without flattening them into fake shared selector law

That claim is now true in code.

## What Landed

### Shared readiness contract

`src/analysis_products/schemas.py` now defines the public Stage 10 readiness boundary:

- `SourceBackedReadinessDecision`
- `AoiSourceBackedReadinessDetail`
- `GenealogySourceBackedReadinessDetail`
- explicit requested-selector, followup-readiness, and overall-readiness status fields
- readiness trace entries

The key structural correction is now explicit in the contract:

- selector feasibility
- downstream followup feasibility
- overall readiness

are related, but not collapsed into one status.

### Analyzer-owned readiness service and route

`src/analysis_products/source_backed_readiness.py` now owns Stage 10 readiness inspection, and `src/api/routes/results.py` exposes:

- `GET /v1/results/by-job/{job_id}/source-backed-readiness`

The route now:

- accepts durable result identity plus workflow-owned selector hints
- returns `ready`, `partially_ready`, or `blocked`
- returns `200` for ordinary readiness blockers
- keeps `400` for malformed selector requests
- keeps `404` for missing jobs

### AOI readiness over live Stage 7 truth

Stage 10 reuses the existing AOI source bridge instead of inventing a second AOI contract.

It now computes readiness from:

- `resolve_source_catalog(...)`
- `evaluate_compose_profile_feasibility(...)`

That means:

- AOI readiness is based on real per-profile feasibility, not generic source-family presence
- `allowed_selectors` and `blocked_selectors` now reflect the same preset law that Stage 7 compose actually uses
- non-`the-critic` consumers can still be source-feasible while followup remains blocked, which now rolls up honestly to `partially_ready`

### Genealogy readiness over restore/runtime truth

Stage 10 does **not** pretend genealogy is AOI-style source reconstruction.

Instead it now:

- gates on ordinary manifest truth first
- short-circuits when preparation is incomplete or restore is unavailable
- builds genealogy payloads only through internal `read_only=True` presenter prep
- evaluates each bounded genealogy `composition_mode` on a copied payload map
- returns feasible vs blocked runtime modes with blocker reasons

The public followup stays on:

- `GET /v1/results/by-job/{job_id}/presentation?composition_mode=...`

### Read-only guarantee

This slice was only acceptable if it stayed read-only.

That guarantee now exists in code:

- the genealogy readiness path never calls public presentation routes to infer feasibility
- payload preparation is forced through `read_only=True`
- runtime inspection works on copied payload maps
- readiness inspection does not persist new `genealogy.relationship_classification` artifacts

## Verification

Focused verification completed:

- `python -m py_compile src/presenter/bounded_dynamic_composition.py src/analysis_products/schemas.py src/analysis_products/source_backed_readiness.py src/api/routes/results.py tests/test_source_backed_readiness.py`
  - result: clean
- `PYTHONPATH=. pytest -q tests/test_source_backed_readiness.py tests/test_analysis_product_contract.py tests/test_presentation_api.py tests/test_composition_source_bridge.py tests/test_task_planner.py`
  - result: `163 passed`
- `PYTHONPATH=. pytest -q tests/test_declarative_adaptive_specs.py tests/test_manifest_trace.py`
  - result: `62 passed`

Total focused verification:

- `225 passed`

Proof artifacts saved:

- `communications/PROOF_stage10_aoi_readiness_decision_2026-03-23.json`
- `communications/PROOF_stage10_genealogy_partial_readiness_decision_2026-03-23.json`
- `communications/PROOF_stage10_genealogy_blocked_readiness_decision_2026-03-23.json`

## Post-Implementation Review

The post-implementation review pass found no blocking issues in the bounded Stage 10 claim.

The reviewer specifically confirmed that:

- AOI readiness reuses live Stage 7 source-catalog and profile-feasibility logic rather than inventing a second feasibility law
- genealogy readiness gates on manifest truth before runtime inspection and keeps ordinary data blockers in `200` readiness semantics rather than reusing the presentation route's `409` behavior
- the read-only guarantee holds because genealogy readiness threads `read_only=True` through payload preparation and inspects copied payload maps only
- the proof-bar cases now exist in focused tests, including AOI partial readiness, genealogy blocked-before-preparation, genealogy mixed feasibility, and no-artifact mutation checks

The only residual note from review was narrow and non-blocking:

- `src/analysis_products/source_backed_readiness.py` imports the private presenter helper `_prepare_page_payloads`; that is acceptable for this bounded slice but is worth cleaning up later if the readiness seam becomes heavier platform infrastructure

The review also noted that full-repo regression was not rerun in the reassessment pass.

That does not change the bounded closure claim here:

- Stage 10 is complete for the scoped readiness seam
- no additional code changes were required after review

## What Stage 10 Now Proves

Stage 10 now proves:

1. analyzer-v2 can expose one shared readiness contract while keeping selector law workflow-owned
2. AOI source-backed readiness can be normalized above the Stage 7 bridge without claiming host neutrality
3. genealogy readiness can be normalized above durable result truth without pretending genealogy is an AOI-style source reconstruction workflow
4. selector feasibility and followup feasibility can be separated cleanly in one analyzer-owned response
5. ordinary readiness blockers can return `200` readiness results instead of reusing the existing `409` presentation-route semantics
6. genealogy readiness inspection can stay read-only even when genealogy payload prep normally has opportunistic artifact-persistence behavior

## What Stage 10 Does Not Yet Prove

Stage 10 does **not** yet prove:

1. generic selector law across workflow families
2. AOI runtime `composition_mode` readiness
3. planner-driven selector choice
4. generalized page planning
5. broader workflow coverage beyond AOI plus genealogy
6. host adoption of the new readiness route

Those remain later stages.

## Program Position After Stage 10

The strategic position is now materially stronger again:

- Stage 9 already closed `route-task -> hydration -> planning decision`
- Stage 10 now closes the next downstream inspection seam:
  - durable result identity -> workflow-owned readiness truth -> explicit followup contract

But the broader platform gap remains:

- selector law is still workflow-owned rather than generalized
- AOI still has explicit `the-critic` consumer coupling on followup
- rich page planning and wider workflow coverage remain open
