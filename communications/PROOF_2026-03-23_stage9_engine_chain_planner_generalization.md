# Proof Record: Stage 9 / Engine-Chain Planner Generalization

Date: 2026-03-23  
Program: Dynamic Bespoke Apps Platformization  
Scope Memo: `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_scope.md`

## Proof Shape

This proof record captures the bounded Stage 9 evidence now saved in `communications/`.

The proof was generated from live `plan_composition_task(...)` outputs over the landed Stage 9 contract:

- `TaskPlanningRequest`
- `TaskPlanningDecision`
- `POST /v1/orchestrator/plan-task`

The proof is intentionally mixed:

- genealogy inline and genealogy by-ref decisions were generated through the real Stage 9 planning boundary with real hydration paths and deterministic planner stubs
- AOI handoff was generated through the real Stage 9 planning boundary with a deterministic source-catalog stub
- insufficient-context proof was generated through the live fail-closed planning path without planner stubbing

That keeps the proof honest:

- the new route/hydration/decision seam is real
- the bounded proof does not pretend an external planner dependency was exercised live in this documentation pass

## Saved Decision Artifacts

- `communications/PROOF_stage9_genealogy_inline_plan_decision_2026-03-23.json`
- `communications/PROOF_stage9_genealogy_by_ref_plan_decision_2026-03-23.json`
- `communications/PROOF_stage9_aoi_handoff_plan_decision_2026-03-23.json`
- `communications/PROOF_stage9_insufficient_context_plan_decision_2026-03-23.json`

## What The Artifacts Show

### Genealogy inline

The inline proof shows:

- task intake from the Stage 8-style envelope
- inferred inline source mode from `planning_context`
- canonical genealogy routing
- satisfied hydration status
- embedded persisted `WorkflowExecutionPlan`
- execution-ready `document_ids`
- explicit executor followup contract over `plan_id + document_ids`
- planning without dispatch, but not side-effect free:
  - Stage 9 genealogy planning persists a plan and materializes executor-ready document records as part of the real hydration seam

### Genealogy by-ref

The by-ref proof shows:

- task intake from the Stage 8-style envelope
- registered-corpus planning context
- canonical genealogy routing
- real by-ref hydration boundary
- embedded persisted `WorkflowExecutionPlan`
- execution-ready `document_ids`
- explicit executor followup contract
- the same non-dispatch but persisted-side-effect property as the inline path

### AOI handoff

The AOI proof shows:

- Stage 8-style AOI routing reused inside `plan-task`
- satisfied saved-result hydration
- bounded `AoiCompositionHandoffPlan`
- explicit expected and available AOI source families
- explicit producer engines
- feasible `allowed_profiles` filtered against the resolved Stage 7 source catalog
- explicit `blocked_profiles` for compose presets that would still fail downstream
- explicit compose followup contract
- explicit remaining host-side `profile` selection

The nested `routing_decision` remains generic Stage 8 routing truth. The top-level planning fields are the narrowed Stage 9 planning truth that hosts should follow for real compose readiness.

### Insufficient context

The insufficient proof shows:

- AOI-positive task signals
- saved-result route family
- missing `source_v2_job_id`
- fail-closed `insufficient_context`
- explicit `required_hydration`

## Focused Verification

Focused verification completed during Stage 9 implementation:

- `python -m py_compile src/orchestrator/task_planning_schemas.py src/orchestrator/task_planner.py src/orchestrator/pipeline.py src/orchestrator/by_ref.py src/api/routes/orchestrator.py`
  - result: clean
- `PYTHONPATH=. pytest -q tests/test_task_router.py tests/test_task_planner.py tests/test_registered_corpus_launch.py tests/test_aoi_contract.py tests/test_composition_source_bridge.py tests/test_adaptive_execution_target_normalization.py`
  - result: `50 passed`

## What This Proof Does Not Claim

This proof does **not** claim:

- automatic dispatch from `plan-task`
- host adoption in the-critic
- planner-driven AOI profile selection
- cross-workflow source normalization
- broad objective coverage beyond AOI plus genealogy
- page-law generalization

It proves only the bounded Stage 9 seam that was actually implemented:

- route-task -> hydration -> planning decision normalization
