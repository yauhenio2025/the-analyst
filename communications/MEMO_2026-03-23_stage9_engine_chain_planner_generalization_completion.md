# Memo: Stage 9 / Engine-Chain Planner Generalization Completion

Date: 2026-03-23  
Program: Dynamic Bespoke Apps Platformization  
Scope Memo: `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_scope.md`  
Proof Memo: `communications/PROOF_2026-03-23_stage9_engine_chain_planner_generalization.md`

## Result

Stage 9 implementation is complete for the bounded slice that was actually scoped:

- analyzer-owned route-plus-hydrate-plus-plan normalization over the current AOI and genealogy slice

This memo closes the code and focused verification record for that slice.

It does **not** claim that analyzer-v2 now performs:

- automatic dispatch from `plan-task`
- open-ended objective coverage
- planner-driven AOI profile selection
- cross-workflow source-family normalization
- page-law generalization
- host adoption of the new planning route

The honest program state is now:

- Stage 9 planning boundary implemented
- focused verification complete
- proof artifacts saved
- roadmap Stage 9 advanced further into partial
- broader cross-workflow planning and composition work still open

## Bounded Claim Landed

The bounded Stage 9 claim was:

- analyzer-v2 should accept the new Stage 8 task boundary plus planner-ready hydration context, rerun or validate routing, and normalize the result into either a real genealogy execution plan or a bounded AOI composition handoff plan without dispatching execution

That claim is now true in code.

## What Landed

### Stage 9 planning contract

`src/orchestrator/task_planning_schemas.py` now defines the public Stage 9 planning boundary:

- `TaskPlanningRequest`
- discriminated `TaskPlanningContext`
- `TaskPlanningDecision`
- `AoiCompositionHandoffPlan`
- explicit planning trace and rejected-planning records

The new contract keeps three layers separate:

1. routing truth
2. hydration truth
3. planning truth

### Analyzer-owned `plan-task`

`src/orchestrator/task_planner.py` now owns Stage 9 planning orchestration, and `src/api/routes/orchestrator.py` exposes:

- `POST /v1/orchestrator/plan-task`

The route now:

- builds an effective Stage 8-style routing input from task envelope plus optional planning context
- reruns canonical routing
- validates or ignores a supplied prior routing decision
- returns:
  - `genealogy_execution_plan`
  - `aoi_composition_handoff_plan`
  - `insufficient_context`
  - `unsupported`

### Genealogy planning over real hydration seams

Stage 9 did not invent a second genealogy planner.

Instead it reuses the existing substrate by adding shared plan-only helpers in:

- `src/orchestrator/pipeline.py`
- `src/orchestrator/by_ref.py`

That lets `plan-task` produce:

- a persisted `WorkflowExecutionPlan`
- execution-ready `document_ids`
- an explicit executor followup contract

without starting execution.

That boundary is advisory in the dispatch sense only. It is not side-effect free:

- inline genealogy planning uploads/materializes executor-ready documents
- inline and by-ref genealogy planning persist a draft plan
- repeated genealogy planning calls can therefore create additional stored plans and hydrated document records even when no execution follows

### AOI handoff normalization over Stage 7

Stage 9 stays narrow on AOI.

It now returns bounded AOI handoff metadata over the existing Stage 7 source bridge rather than pretending AOI already has generalized planner output.

The handoff explicitly names:

- source families
- producer engines
- feasible compose profiles derived from the resolved source catalog
- blocked profiles that would still fail Stage 7 compose requirements
- compose entrypoint
- remaining host preparation

But Stage 9 still leaves:

- `source_v2_job_id` resolution to the host
- `profile` selection to the host

## Verification

Focused verification completed:

- `python -m py_compile src/orchestrator/task_planning_schemas.py src/orchestrator/task_planner.py src/orchestrator/pipeline.py src/orchestrator/by_ref.py src/api/routes/orchestrator.py`
  - result: clean
- `PYTHONPATH=. pytest -q tests/test_task_router.py tests/test_task_planner.py tests/test_registered_corpus_launch.py tests/test_aoi_contract.py tests/test_composition_source_bridge.py tests/test_adaptive_execution_target_normalization.py`
  - result: `50 passed`

Proof artifacts saved:

- `communications/PROOF_stage9_genealogy_inline_plan_decision_2026-03-23.json`
- `communications/PROOF_stage9_genealogy_by_ref_plan_decision_2026-03-23.json`
- `communications/PROOF_stage9_aoi_handoff_plan_decision_2026-03-23.json`
- `communications/PROOF_stage9_insufficient_context_plan_decision_2026-03-23.json`

## What Stage 9 Now Proves

Stage 9 now proves:

1. analyzer-v2 can own a public planning boundary above existing routing and below execution
2. the thin Stage 8 task envelope can be combined with explicit planning context to produce planner-ready outcomes
3. genealogy planning can return a persisted execution plan plus executor-ready `document_ids` without automatic dispatch
4. AOI planning can stop honestly at handoff metadata over the Stage 7 source bridge
5. the analyzer can distinguish `unsupported` from `insufficient_context` instead of flattening both into one unsupported result

## What Stage 9 Does Not Yet Prove

Stage 9 does **not** yet prove:

1. broad objective coverage
2. planner-driven AOI profile selection
3. host adoption of `plan-task`
4. automatic plan dispatch into execution or compose
5. cross-workflow source-family normalization
6. page-law generalization

Those remain later stages.

## Program Position After Stage 9

The strategic position is now materially stronger:

- Stage 8 no longer stops at advisory workflow choice
- Stage 9 now closes the next missing seam:
  - route-task -> hydration -> planning decision

But the broader platform gap remains:

- the system still does not have generalized planner-to-composition behavior across workflows
- AOI still stops at bounded handoff metadata
- broader source-normalization and page-planning work remain open
