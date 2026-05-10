# Memo: Stage 12 / Cross-Workflow Renderer Law Generalization Completion

Date: 2026-03-24  
Program: Dynamic Bespoke Apps Platformization  
Scope Memo: `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_scope.md`  
Proof Memo: `communications/PROOF_2026-03-24_stage12_cross_workflow_renderer_law_generalization.md`

## Result

Stage 12 is complete for the bounded slice that was actually scoped:

- analyzer-owned served-renderer-law generalization across current transient and job-backed AOI/genealogy presentation seams

This closes the implementation, proof, and focused verification record for that slice.

It does **not** claim that the platform now has:

- universal strict renderer law on every genealogy runtime mode
- strict trace, status, discovery, polish, delivery-style, scaffold-generation, variant-generation, or orchestrator-preview surfaces
- new public presenter/results contracts
- renderer-package work
- Stage 13 host-contract formalization

The honest post-implementation state is now:

- explicit served-intent policy layer landed
- shared assembly helpers now receive intent per helper call
- transient plus current AOI job-backed adaptive surfaces are strict through the same policy seam
- one genealogy served mode is strict
- remaining genealogy runtime modes are shadow, not silent warn
- support and inspection callers are explicitly non-strict
- roadmap Stage 12 remains partial because broader genealogy promotion and later host work are still open

## Bounded claim landed

The bounded Stage 12 claim was:

- replace the old composition-mode-only final enforcement gate with one explicit served-intent policy and use it to apply recursive final renderer law across current AOI and genealogy served presentation seams

That claim is now true in code.

## What landed

### Explicit served-intent policy resolver

`src/presenter/renderer_contract_enforcement.py` now owns the Stage 12 policy seam.

It introduced:

- `ServedIntent`
- `ServedRendererContractPolicy`
- `resolve_served_renderer_contract_policy(...)`

The initial intent matrix is fully enumerated rather than being left to ad hoc caller branching.

That means strictness is now decided from explicit internal artifact intent such as:

- transient compose output
- effective manifest served
- full page presentation served
- single view presentation served
- explicit inspection/support intents for status, trace, polish-source fetch, delivery-style seeding, scaffold generation, variant generation, discovery preview, and orchestrator preview

### Per-helper-call policy threading

Stage 12 did **not** bind policy one time per outer route.

Instead it threaded served intent through the shared helper graph:

- `build_effective_manifest(...)`
- `build_presentation_manifest(...)`
- `assemble_page(...)`
- `assemble_single_view(...)`

That matters because multi-artifact routes like result-presentation and refresh-presentation traverse both:

- effective manifest building
- full page assembly

Those helper calls now carry their own explicit served intents instead of inheriting one accidental route-level law.

### Recursive final-boundary renderer law

The old final gate was one narrow `composition_mode` allowlist.

Stage 12 now applies recursive final-boundary enforcement through the served-intent resolver, with three modes:

- `strict`
- `shadow`
- `warn`

Behavior is now:

- `strict` -> raise `BoundedCompositionValidationError`
- `shadow` -> run the same validator, keep the response non-fatal, and emit diagnostics
- `warn` -> preserve the existing non-fatal path

### Final serve-time sub-renderer law and separate tab child law

Stage 12 is not just top-level renderer validation.

The final enforcement layer now also validates:

- section-level sub-renderer assignments
- nested sub-renderer config and recursion
- consumer support for served sub-renderers
- `tab` child-container alignment separately from accordion-style section-renderer law

The `tab` law is intentionally separate:

- parent tab payloads are checked differently from accordion/nested section-renderer specs
- Stage 11 transient parent tabs and existing authored tab containers can both pass under bounded explicit rules rather than hidden carveouts

### Genealogy cutover is explicit

Stage 12 did not pretend all genealogy served surfaces were strict-ready.

The bounded cutover that landed is:

- `declarative_relationship_surface_v1` -> `strict`
- `bounded_dynamic_genealogy_v1` -> `shadow`
- `adaptive_relationship_surface_v1` -> `shadow`
- `adaptive_genealogy_relationship_conditions_v1` -> `shadow`
- `declarative_genealogy_relationship_conditions_suite_v1` -> `shadow`

So genealogy is no longer silently warn-only across current runtime modes, but it also is not falsely declared fully strict-clean.

### Route-level correction for `POST /v1/presenter/compose`

`src/api/routes/presenter.py` now explicitly maps strict renderer-law failures in `POST /v1/presenter/compose` to `409`.

The catch ordering is also now correct:

- `BoundedCompositionValidationError` is handled before the generic `ValueError` branch

That closes the concrete route bug identified during Stage 12 planning.

## Verification

Compile verification completed:

- `python -m py_compile tests/test_served_renderer_contract_policy.py src/presenter/renderer_contract_enforcement.py src/presenter/manifest_builder.py src/presenter/presentation_api.py src/api/routes/presenter.py src/analysis_products/result_contract.py`

Focused Stage 12 presenter/results verification completed:

- `PYTHONPATH=. pytest -q tests/test_served_renderer_contract_policy.py tests/test_manifest_trace.py tests/test_presentation_api.py tests/test_analysis_product_contract.py tests/test_compose_from_intent.py`

Result:

- `202 passed`

Broader adjacent presenter/results regression completed:

- `PYTHONPATH=. pytest -q tests/test_served_renderer_contract_policy.py tests/test_manifest_trace.py tests/test_presentation_api.py tests/test_analysis_product_contract.py tests/test_compose_from_intent.py tests/test_declarative_adaptive_specs.py tests/test_source_backed_readiness.py`

Result:

- `243 passed`

Saved proof artifacts:

- `communications/PROOF_stage12_aoi_strict_success_2026-03-24.json`
- `communications/PROOF_stage12_genealogy_strict_success_2026-03-24.json`
- `communications/PROOF_stage12_genealogy_shadow_policy_2026-03-24.json`
- `communications/PROOF_stage12_genealogy_strict_fail_closed_2026-03-24.json`
- `communications/PROOF_stage12_compose_route_409_2026-03-24.json`

## Post-Verification Closure

After the initial Stage 12 completion pass, the broader local verification state was also checked.

That broader rerun reported:

- `417 passed, 3 failed`

The three failures were reviewed and are not Stage 12 regressions:

1. two failures in `tests/test_manifest_trace.py::test_aoi_live_controls_keep_served_outputs_identical_with_and_without_renderer_enforcement`
   - both depend on specific live job IDs in `executor.db`
   - the failure shape is `ValueError: Job not found: proof-round5-adaptive-aoi-dossier-final-1774100000`
   - that is a database-state dependency rather than a served-intent or renderer-law regression
2. one failure in `tests/test_variant_generator.py::TestGenerateSubRendererVariants::test_empty_existing_hints`
   - this sits in variant-generation logic rather than the Stage 12 renderer-law seam

The post-implementation review also found no blocking code issues in the bounded Stage 12 claim.

Two residual notes remain, both non-blocking:

1. direct test coverage for the explicit non-strict support intents is still thinner than the strict/shadow route-path coverage
2. the saved genealogy proof artifacts are helper-level synthetic outputs rather than live route calls, which is already stated honestly in the proof record

That does not change the bounded closure claim here:

- Stage 12 is complete for the scoped served-intent renderer-law slice
- the broader rerun did not uncover a Stage 12 regression
- the remaining failures are pre-existing and unrelated to this stage

## What Stage 12 now proves

Stage 12 now proves:

1. renderer-law strictness can be resolved from explicit internal served intent rather than one outer-route or one allowlisted-composition-mode shortcut
2. shared manifest/page/view helpers can serve both strict and non-strict callers without accidental policy leakage
3. AOI strict served surfaces can move onto that shared policy seam without regressing the current AOI proof path
4. genealogy can be promoted honestly via one strict served mode plus visible shadow coverage for the remaining runtime modes
5. final-boundary renderer law can include served sub-renderer/container validation rather than stopping at top-level renderer schemas
6. `POST /v1/presenter/compose` now returns the correct `409` contract failure shape instead of leaking strict failures as generic errors

## What Stage 12 does not yet prove

Stage 12 does **not** yet prove:

1. full strict renderer-law coverage across all genealogy runtime modes
2. strict inspection/support behavior for trace, status, discovery, polish, or preview paths
3. a minimal generic host contract
4. any new cross-workflow transient planning expansion

Those remain later work.

## Known bounded edge

The Stage 12 law is intentionally asymmetric:

- strict on transient compose
- strict on current AOI adaptive served surfaces
- strict on one bounded genealogy served mode
- shadow on the remaining genealogy runtime modes
- warn on explicit inspection/support intents

That is not an accidental half-cutover.

It is the explicit Stage 12 law for the bounded slice that was actually scoped.
