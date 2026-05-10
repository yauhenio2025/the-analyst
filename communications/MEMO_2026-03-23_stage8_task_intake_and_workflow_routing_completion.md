# Memo: Stage 8 / Task Intake And Workflow Routing Completion

Date: 2026-03-23  
Program: Dynamic Bespoke Apps Platformization  
Scope Memo: `communications/MEMO_2026-03-23_stage8_task_intake_and_workflow_routing_scope.md`  
Proof Memo: `communications/PROOF_2026-03-23_stage8_task_intake_and_workflow_routing.md`

## Result

Stage 8 implementation is complete for the bounded slice that was actually scoped:

- analyzer-owned advisory task intake and workflow routing over existing downstream analyzer contracts

This memo closes the code and focused verification record for that slice.

It does **not** claim that analyzer-v2 now performs:

- task-to-execution dispatch
- task-to-composition dispatch
- open-ended workflow routing
- engine/chain planning from the new task envelope
- AOI profile selection
- host integration of the new route

The honest program state is now:

- Stage 8 advisory router implemented
- focused verification complete
- proof artifacts saved
- roadmap Stage 8 advanced further into partial
- broader planner generalization and host adoption still open

## Bounded Claim Landed

The bounded Stage 8 claim was:

- analyzer-v2 should accept a composition-facing task envelope without a required workflow key, deterministically choose among bounded workflow outcomes, and return an advisory downstream launch contract that removes analytical workflow choice from the host without pretending downstream AOI and genealogy launch shapes are already unified

That claim is now true in code.

## What Landed

### Analyzer-side routing substrate

`src/orchestrator/task_routing_schemas.py` now defines the advisory routing contract:

- `CompositionTaskRequest`
- discriminated `source_constraints`
- `CompositionTaskRoutingDecision`
- explicit routing trace and rejected-candidate records

The route is intentionally strict:

- typed source modes
- `extra="forbid"`
- bounded enums for outcome, contract kind, confidence, and source sufficiency

### Deterministic analyzer router

`src/orchestrator/task_router.py` now owns deterministic routing logic for the bounded Stage 8 outcome set.

It formalizes:

1. task normalization
2. objective candidate scoring
3. source sufficiency evaluation
4. routing decision

The current supported outcome space is intentionally small:

- `aoi_transient_source_backed`
- `genealogy_job_backed`
- `unsupported`

### Analyzer-native AOI contract seam

The Stage 8 implementation closed the key contract seam that mattered most:

- AOI advisory routing is expressed in analyzer-native `compose-from-source` terms
- downstream AOI requires:
  - `workflow_key`
  - `consumer_key`
  - `source_v2_job_id`
  - `profile`
- `source_analysis_id` is treated only as host-side preparation

That keeps the advisory contract honest instead of blending the analyzer-native route with the-critic’s proxy shape.

### Cross-signal fail-closed behavior

Stage 8 also proves an important negative rule:

- AOI-positive task semantics plus a genealogy-shaped source mode does **not** silently fall back to genealogy

The router instead returns:

- `unsupported`
- `source_sufficiency_status = "insufficient"`

That is strategically important because it keeps the routing contract honest rather than opportunistically coercive.

## Verification

Focused verification completed:

- `python -m py_compile src/orchestrator/task_routing_schemas.py src/orchestrator/task_router.py src/api/routes/orchestrator.py tests/test_task_router.py`
  - result: clean
- `PYTHONPATH=. pytest tests/test_task_router.py -q`
  - result: `13 passed`
- `PYTHONPATH=. pytest tests/test_registered_corpus_launch.py tests/test_aoi_contract.py -q`
  - result: `21 passed`

Proof artifacts saved:

- `communications/PROOF_stage8_aoi_route_decision_2026-03-23.json`
- `communications/PROOF_stage8_genealogy_by_ref_route_decision_2026-03-23.json`
- `communications/PROOF_stage8_genealogy_inline_route_decision_2026-03-23.json`
- `communications/PROOF_stage8_ambiguous_route_decision_2026-03-23.json`
- `communications/PROOF_stage8_insufficient_source_route_decision_2026-03-23.json`
- `communications/PROOF_stage8_aoi_cross_signal_unsupported_route_decision_2026-03-23.json`

## What Stage 8 Now Proves

Stage 8 now proves:

1. analyzer-v2 can own a composition-facing task-routing contract instead of requiring the host to choose the workflow analytically
2. the advisory layer can remain deterministic and fail closed
3. the new route can speak analyzer-native downstream contracts without pretending host proxy contracts are the same thing
4. the router can keep downstream asymmetry explicit instead of hiding it in a fake unified launcher
5. the analyzer can provide bounded routing rationale, rejected candidates, and launch preparation without dispatching execution

## What Stage 8 Does Not Yet Prove

Stage 8 does **not** yet prove:

1. task-to-engine/chain planning
2. planner-driven AOI profile selection
3. host adoption of `route-task`
4. downstream dispatch from the new task envelope
5. cross-workflow dynamic composition
6. planner-driven page law

Those are the next stages.

## Program Position After Stage 8

The strategic shift is now clearer:

- task intake and workflow-routing no longer live only in vision docs
- analyzer-v2 now has a real bounded route-task seam in code

But the router still stops at:

- “which downstream family should own the next move?”

It does not yet answer:

- “what nontrivial engine/chain plan should serve that move?”

That is the next missing upstream seam.
