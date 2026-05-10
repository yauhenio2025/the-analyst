# Memo: Stage 9 / AOI Handoff Profile Feasibility Hardening Completion

Date: 2026-03-23  
Program: Dynamic Bespoke Apps Platformization  
Primary Scope Memo: `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_scope.md`  
Primary Completion Memo: `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_completion.md`  
Primary Proof Memo: `communications/PROOF_2026-03-23_stage9_engine_chain_planner_generalization.md`

## Result

The Stage 9 AOI handoff contract has been hardened after review.

The review-discovered overstatement was real:

- the first Stage 9 AOI implementation treated "some AOI sources are available" as enough to report:
  - `downstream_readiness = ready_for_aoi_compose_handoff`
  - `allowed_profiles = ["dossier", "comparison"]`

That was too weak because Stage 7 compose feasibility is profile-specific.

The hardening pass closes that contract gap.

The honest Stage 9 AOI state is now:

- `ready_for_aoi_compose_handoff` means at least one bounded AOI compose profile is actually feasible against the live source catalog
- `allowed_profiles` is no longer a schema default pretending both profiles are always safe
- blocked compose presets are surfaced explicitly with per-profile blocker reasons

## Bounded Claim Landed

This follow-up hardening proves one bounded thing:

- Stage 9 AOI handoff readiness is now aligned with real Stage 7 compose feasibility rather than generic source-family availability

That was the only substantive review finding on the Stage 9 implementation.

## What Landed

### Profile feasibility now lives with the source bridge

`src/presenter/composition_source_bridge.py` now exposes:

- `evaluate_compose_profile_feasibility(catalog)`

That helper evaluates each AOI preset against the same source-family requirements that real `compose-from-source` uses.

So profile feasibility is now derived from:

- the live resolved catalog
- the Stage 7 preset contract

not:

- a planner-side guess
- a schema default
- "at least one source family exists"

### Stage 9 AOI planning now fails closed on infeasible profiles

`src/orchestrator/task_planner.py` now:

- computes `allowed_profiles` and `blocked_profiles` from the resolved AOI catalog
- returns `ready_for_aoi_compose_handoff` only when at least one profile is feasible
- raises the existing AOI resolution conflict path when no compose profile is feasible, even if some AOI artifacts exist

That means a partial AOI catalog no longer gets misreported as compose-ready.

### The handoff contract is now operationally truthful

`src/orchestrator/task_planning_schemas.py` now lets `AoiCompositionHandoffPlan` carry:

- `allowed_profiles`
- `blocked_profiles`

The Stage 9 followup contract now also includes:

- the filtered `allowed_profiles`

So the host can tell the difference between:

- a profile that is actually safe to launch
- a profile that would still 409 at compose time

### Stage 9 docs/proof were corrected

The saved AOI proof artifact was regenerated and now shows:

- `allowed_profiles = ["dossier"]`
- `blocked_profiles = {"comparison": ["sin_findings (unavailable)"]}`

The Stage 9 proof and completion notes now also state explicitly that genealogy `plan-task` is advisory in the dispatch sense only, not side-effect free.

## Verification

Targeted hardening verification completed:

- `python -m py_compile src/presenter/composition_source_bridge.py src/orchestrator/task_planning_schemas.py src/orchestrator/task_planner.py tests/test_task_planner.py`
  - result: clean
- `PYTHONPATH=. pytest -q tests/test_task_planner.py tests/test_composition_source_bridge.py`
  - result: `13 passed`

Focused Stage 9 regression verification was also rerun after the hardening:

- `PYTHONPATH=. pytest -q tests/test_task_router.py tests/test_task_planner.py tests/test_registered_corpus_launch.py tests/test_aoi_contract.py tests/test_composition_source_bridge.py tests/test_adaptive_execution_target_normalization.py`
  - result: `50 passed`

## What This Hardening Now Proves

This hardening now proves:

1. Stage 9 AOI handoff readiness is keyed to real per-profile feasibility
2. Stage 9 no longer advertises blocked AOI profiles as if they were downstream-safe
3. partial AOI catalogs with no feasible compose profile now fail through the existing 409 resolution path
4. the Stage 9 handoff contract is closer to something a host can trust operationally

## What This Hardening Does Not Yet Prove

This follow-up does **not** prove:

1. planner-driven AOI profile selection
2. cross-workflow source-backed composition
3. a generic workflow-owned source-material adapter registry
4. host adoption of `plan-task`
5. broad objective coverage beyond AOI plus genealogy

Those remain later-stage work.

## Strategic Position After The Hardening

The important Stage 9 state change is now:

- the AOI planning contract is no longer overstating readiness relative to runtime compose law

That matters because the next stage should build on trustworthy source-backed readiness semantics, not on optimistic AOI-only assumptions.
