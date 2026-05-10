# Proof: Stage 12 / Cross-Workflow Renderer Law Generalization

Date: 2026-03-24  
Program: Dynamic Bespoke Apps Platformization  
Scope Memo: `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_scope.md`

## Proof target

Stage 12 was scoped to prove one bounded thing:

- analyzer-v2 now owns an explicit served-intent renderer-law boundary across current transient and job-backed AOI/genealogy presentation seams, with strict/shadow/warn decided per internal helper call rather than by outer route accident

This proof record is intentionally explicit about artifact basis:

- the AOI strict-success artifact uses a live saved job
- the genealogy strict/shadow artifacts use real helper outputs over synthetic payloads so the non-AOI strict/shadow split is deterministic and reproducible

## Saved artifacts

- `communications/PROOF_stage12_aoi_strict_success_2026-03-24.json`
- `communications/PROOF_stage12_genealogy_strict_success_2026-03-24.json`
- `communications/PROOF_stage12_genealogy_shadow_policy_2026-03-24.json`
- `communications/PROOF_stage12_genealogy_strict_fail_closed_2026-03-24.json`
- `communications/PROOF_stage12_compose_route_409_2026-03-24.json`

## What the artifacts show

### 1. AOI strict served success is now routed through the shared served-policy layer

`PROOF_stage12_aoi_strict_success_2026-03-24.json` records a live saved AOI proof job under:

- `served_intent = effective_manifest_served`
- `composition_mode = adaptive_aoi_theme_report_suite_v1`
- `policy.mode = strict`

It also records the resulting manifest hash, content hash, resolver version, and top-level view keys.

This is the positive proof that Stage 12 did not regress the current AOI strict path while moving strictness out of the old one-off allowlist framing.

### 2. One real genealogy served mode is now strict

`PROOF_stage12_genealogy_strict_success_2026-03-24.json` records a real `build_effective_manifest(...)` output for:

- `served_intent = effective_manifest_served`
- `composition_mode = declarative_relationship_surface_v1`
- `policy.mode = strict`

This is the bounded non-AOI promotion that Stage 12 was supposed to land.

### 3. Remaining genealogy runtime modes are shadow, not silently warn

`PROOF_stage12_genealogy_shadow_policy_2026-03-24.json` records a real helper call for:

- `served_intent = effective_manifest_served`
- `composition_mode = adaptive_relationship_surface_v1`
- `policy.mode = shadow`

It also records the real validation issue list returned without raising.

That is the explicit genealogy cutover strategy in executable form:

- one bounded strict genealogy slice
- remaining genealogy runtime modes visible under shadow
- no silent warn fallback for current registered genealogy composition modes

### 4. Non-AOI strict fail-closed evidence exists

`PROOF_stage12_genealogy_strict_fail_closed_2026-03-24.json` records the paired strict genealogy failure case for the same invalid payload shape under:

- `served_intent = effective_manifest_served`
- `composition_mode = declarative_relationship_surface_v1`
- `policy.mode = strict`

The saved artifact records `raised = true` plus the issue list.

This is the required non-AOI fail-closed proof case.

### 5. `POST /v1/presenter/compose` now maps strict renderer-law failures to `409`

`PROOF_stage12_compose_route_409_2026-03-24.json` records a real route-function output for `POST /v1/presenter/compose` with:

- `status_code = 409`
- bounded-composition issue details preserved in the response body

This closes the route-level correctness gap that existed before Stage 12.

## Focused verification

Compile verification:

- `python -m py_compile tests/test_served_renderer_contract_policy.py src/presenter/renderer_contract_enforcement.py src/presenter/manifest_builder.py src/presenter/presentation_api.py src/api/routes/presenter.py src/analysis_products/result_contract.py`

Focused Stage 12 presenter/results verification:

- `PYTHONPATH=. pytest -q tests/test_served_renderer_contract_policy.py tests/test_manifest_trace.py tests/test_presentation_api.py tests/test_analysis_product_contract.py tests/test_compose_from_intent.py`

Result:

- `202 passed`

Broader adjacent presenter/results regression:

- `PYTHONPATH=. pytest -q tests/test_served_renderer_contract_policy.py tests/test_manifest_trace.py tests/test_presentation_api.py tests/test_analysis_product_contract.py tests/test_compose_from_intent.py tests/test_declarative_adaptive_specs.py tests/test_source_backed_readiness.py`

Result:

- `243 passed`

## Honest boundary

Stage 12 does **not** prove:

- all genealogy runtime modes are now strict
- trace/status/discovery/polish support paths should fail closed
- host-contract formalization
- renderer-package work

It proves the narrower and more important thing:

- renderer-law strength is now decided from one explicit served-intent policy over shared helper seams, not from route accident and not from one AOI-only mode check
