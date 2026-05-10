# Proof: Stage 10 / Cross-Workflow Source-Backed Substrate

Date: 2026-03-23  
Program: Dynamic Bespoke Apps Platformization  
Scope Memo: `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md`

## What This Proof Covers

This proof records the bounded Stage 10 claim that is now true in code:

- analyzer-v2 can inspect source-backed readiness across AOI and genealogy from durable result identity
- the inspection contract is read-only
- AOI and genealogy keep workflow-owned selector law
- ordinary readiness blockers return explicit readiness states instead of leaking the existing presentation-route `409` behavior

It does **not** claim:

- generic selector law across all workflows
- AOI runtime `composition_mode` support
- host-neutral AOI followup
- generalized page planning
- Stage 9 / `plan-task` integration in this slice

## Saved Decision Artifacts

### AOI partially-ready readiness decision

Saved artifact:

- `communications/PROOF_stage10_aoi_readiness_decision_2026-03-23.json`

What it shows:

- AOI readiness now reports feasible vs blocked `profile` selectors
- `dossier` is feasible
- `comparison` is blocked because `sin_findings` is unavailable
- followup stays on `POST /v1/presenter/compose-from-source`
- readiness is `partially_ready`, not falsely `ready`, because not every AOI profile is feasible

### Genealogy mixed-feasibility readiness decision

Saved artifact:

- `communications/PROOF_stage10_genealogy_partial_readiness_decision_2026-03-23.json`

What it shows:

- genealogy readiness now reports bounded `composition_mode` feasibility over durable result truth
- the requested `bounded_dynamic_genealogy_v1` mode is blocked
- other genealogy runtime modes remain feasible
- followup stays on `GET /v1/results/by-job/{job_id}/presentation?composition_mode=...`
- readiness is `partially_ready`, which is the intended semantics for “requested selector blocked, but alternatives are still usable”

### Genealogy blocked-before-preparation readiness decision

Saved artifact:

- `communications/PROOF_stage10_genealogy_blocked_readiness_decision_2026-03-23.json`

What it shows:

- genealogy readiness short-circuits on result-manifest state before runtime inspection
- `presentation_status=running` and `restore_reason=preparing` block every inspected genealogy mode
- the readiness route returns `blocked` with explicit blocker reasons instead of leaking `409`

## Read-Only Guarantee Evidence

Stage 10 required one additional proof beyond saved readiness JSON:

- the genealogy readiness route must not create new `genealogy.relationship_classification` artifacts

Focused evidence exists in the automated test:

- `tests/test_source_backed_readiness.py::test_genealogy_readiness_uses_read_only_payload_prep_and_does_not_create_relationship_artifacts`

That test proves:

- the readiness service threads `read_only=True` into internal genealogy payload preparation
- the presenter artifact persistence hook is not called

This matters because ordinary genealogy payload prep can opportunistically persist relationship-classification artifacts when `read_only=False`.

## Focused Verification Record

Verification run:

- `python -m py_compile src/presenter/bounded_dynamic_composition.py src/analysis_products/schemas.py src/analysis_products/source_backed_readiness.py src/api/routes/results.py tests/test_source_backed_readiness.py`
- `PYTHONPATH=. pytest -q tests/test_source_backed_readiness.py tests/test_analysis_product_contract.py tests/test_presentation_api.py tests/test_composition_source_bridge.py tests/test_task_planner.py`
- `PYTHONPATH=. pytest -q tests/test_declarative_adaptive_specs.py tests/test_manifest_trace.py`

Results:

- compile: clean
- tests: `225 passed`

## Bounded Conclusion

Stage 10 now proves one bounded thing:

- analyzer-v2 owns a real, read-only, cross-workflow source-backed readiness seam above durable result truth and below followup composition, with AOI remaining profile-based and genealogy remaining restore/runtime-based
