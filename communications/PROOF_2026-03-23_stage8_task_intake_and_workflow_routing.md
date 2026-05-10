# Proof: Stage 8 / Task Intake And Workflow Routing

Date: 2026-03-23  
Program: Dynamic Bespoke Apps Platformization  
Scope Memo: `communications/MEMO_2026-03-23_stage8_task_intake_and_workflow_routing_scope.md`

## Claim

Stage 8 set out to prove one bounded thing:

- analyzer-v2 can accept a composition-facing task envelope without a consumer-supplied workflow key, deterministically choose between bounded workflow outcomes, and return an advisory downstream launch contract that removes analytical workflow choice from the host without dispatching into execution or transient composition

This proof note records the code and focused verification evidence for that claim.

## What Landed

The new advisory routing contract is implemented in:

- `src/orchestrator/task_routing_schemas.py`
- `src/orchestrator/task_router.py`
- `src/api/routes/orchestrator.py`

The new public analyzer route is:

- `POST /v1/orchestrator/route-task`

The route now does all of the following:

1. accepts a bounded `CompositionTaskRequest` without a required `workflow_key`
2. validates structured `source_constraints` through a discriminated union with `extra="forbid"`
3. deterministically routes only among:
   - `aoi_transient_source_backed`
   - `genealogy_job_backed`
   - `unsupported`
4. returns analyzer-native downstream contract kinds:
   - `presenter.compose_from_source`
   - `orchestrator.analyze`
   - `orchestrator.analyze_by_ref`
5. keeps AOI contract law honest:
   - `source_v2_job_id` is the downstream analyzer requirement
   - `source_analysis_id` is only host-side preparation
6. keeps `source_sufficiency_status` narrow:
   - enough source-mode evidence to choose a downstream family
   - not “full payload already assembled”
7. treats `routing_confidence` as rule-strength, not probability
8. fails closed on cross-signal AOI cases instead of silently coercing them into genealogy
9. never dispatches into downstream execution or composition

## Saved Decision Artifacts

The Stage 8 proof standard required saved decision JSONs for representative routing outcomes.
Those artifacts are now saved in `communications/`:

- `communications/PROOF_stage8_aoi_route_decision_2026-03-23.json`
- `communications/PROOF_stage8_genealogy_by_ref_route_decision_2026-03-23.json`
- `communications/PROOF_stage8_genealogy_inline_route_decision_2026-03-23.json`
- `communications/PROOF_stage8_ambiguous_route_decision_2026-03-23.json`
- `communications/PROOF_stage8_insufficient_source_route_decision_2026-03-23.json`
- `communications/PROOF_stage8_aoi_cross_signal_unsupported_route_decision_2026-03-23.json`

These show the bounded route surface in action across:

1. supported AOI transient source-backed routing
2. supported genealogy by-ref routing
3. supported genealogy inline-documents routing
4. ambiguous unsupported routing
5. insufficient-source unsupported routing
6. explicit AOI cross-signal fail-closed unsupported routing

## Focused Verification Evidence

### Stage 8 router verification

Commands run:

- `python -m py_compile src/orchestrator/task_routing_schemas.py src/orchestrator/task_router.py src/api/routes/orchestrator.py tests/test_task_router.py`
- `PYTHONPATH=. pytest tests/test_task_router.py -q`

Observed result:

- compile: clean
- pytest: `13 passed`

The focused router tests prove:

1. malformed and cross-mode `source_constraints` fail at validation time
2. unknown `objective_hint` returns `400`
3. AOI routes over analyzer-native `compose-from-source`
4. `source_analysis_id` is surfaced only as host-side preparation
5. genealogy by-ref and genealogy inline route to the real existing analyzer endpoints
6. AOI-like tasks without saved-result identity fail closed as `unsupported`
7. AOI-positive tasks with corpus/inline source modes fail closed instead of being coerced into genealogy
8. `workflow_hint` is trace-only and never overrides the selected objective
9. the advisory route never dispatches into downstream execution paths

### Regression verification against live downstream seams

Commands run:

- `PYTHONPATH=. pytest tests/test_registered_corpus_launch.py tests/test_aoi_contract.py -q`

Observed result:

- `21 passed`

This confirms the new advisory layer does not drift the existing AOI and registered-corpus downstream contracts it is advising over.

## What This Proof Does Not Claim

This proof does **not** claim:

1. host-side adoption of `route-task`
2. automatic downstream dispatch
3. AOI profile selection moved upstream
4. general open-ended objective coverage
5. LLM-based routing
6. engine/chain planning from the task envelope
7. planner-driven page law

Stage 8 is an analyzer-only advisory routing proof, not a full task-to-execution or task-to-composition system.

## Verdict

The bounded Stage 8 claim is proven at the code-and-contract level:

- analyzer-v2 now owns a real composition-facing advisory routing contract
- the host no longer has to choose the workflow analytically for the bounded AOI/genealogy outcome set
- the router remains honest about downstream asymmetry and host preparation
- the route is advisory only and does not blur lifecycle regimes by dispatching implicitly

This advances roadmap Stage 8 from:

- partial in concept only

to:

- partial in implemented code

It does **not** complete the broader task-intake / workflow-routing stage for the full dynamic-bespoke-app vision.
