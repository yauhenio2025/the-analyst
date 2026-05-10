# Memo: Phase 2 Host-Neutral Transient Proof Completion

Date: 2026-03-28
Status: Phase 2 implemented, verified, and live-proved; Phase 2 now closes honestly
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Scope Memo: `communications/MEMO_2026-03-27_phase2_host_neutral_transient_proof_scope.md`
Depends on:
- `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_completion.md`
- `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
- `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md`

## Summary

Phase 2 is now complete in bounded form.

This slice proves a stronger transient planner-to-presentation chain beyond the current AOI page/controller stack without reopening Phase 1 bridge work and without prematurely widening into Phase 3 lifecycle law.

What is now true:

- analyzer-v2 now owns one explicit lowering surface from persisted planning truth into the thin public `compose-from-intent` request
- Host Contract v2 and `taskLaunchRuntime` now expose that lowering surface as a named planner-advisory family inside the same runtime story as the existing result/readiness families
- `the-critic` now has one dedicated proof page outside the AOI page stack:
  - `/p/:projectId/proof/transient/genealogy-saved-result`
- one real live proof now exists on the intended non-AOI target:
  - `workflow_hint=intellectual_genealogy`
  - `source_mode=saved_result`
  - canonical `source_v2_job_id`
  - `direct_sections_composition_handoff_plan`
  - explicit `consumer_key=the-critic`
- the live proof stays on:
  - run detail preflight
  - `route-task`
  - `plan-task(persist_decision=true)`
  - `planning_decision_fetch`
  - analyzer-owned lowering
  - `POST /v1/presenter/compose-from-intent`
- the live proof does not use:
  - AOI source-backed proxy compose routes
  - `/v1/executor/jobs`
  - host-local section reconstruction
- invalid planning identity fails closed at the new lowering route with `404`

Important bounded limitation:

- this slice still uses the already-registered transient consumer identity:
  - `consumer_key=the-critic`
- it does not claim new transient consumer registration
- it does not claim lifecycle/session/share semantics

The honest program state is now:

- Phase 1: complete
- Phase 2: complete
- next step: Phase 3 bounded lifecycle v1

## What landed

### 1. Analyzer-owned lowering surface

Analyzer-v2 now serves one explicit lowering route for persisted planning truth:

- `GET /v1/orchestrator/planning-decisions/{planning_decision_id}/compose-from-intent-request`

This route:

- loads the immutable planning snapshot
- fails closed unless the snapshot is truthfully lowerable to the thin compose request
- returns the lowerable `ComposeFromIntentRequest`
- preserves explicit `consumer_key` handling

Primary file:

- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`

### 2. Current-consumer runtime follow-through

The new lowering surface is not a sidecar ad hoc fetch.

What is now true:

- Host Contract v2 includes `planning_decision_compose_request`
- `taskLaunchRuntime.ts` exposes the corresponding runtime helper
- the proof page consumes the same planner/runtime law as the rest of the current host surface

Primary files:

- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`

### 3. One thin proof page outside the AOI stack

The first stronger transient proof vehicle is now a dedicated page outside the AOI controller path:

- `/p/:projectId/proof/transient/genealogy-saved-result`

This page is intentionally narrow and proof-oriented.
It is not product UI.

It performs:

1. saved-result preflight
2. `route-task`
3. `plan-task(persist_decision=true)`
4. planning snapshot fetch
5. analyzer-owned lowering
6. `compose-from-intent`
7. transient rendering through the existing shell

Primary file:

- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx`

### 4. One real bounded live proof

The live proof target used on March 28, 2026 was:

- project: `round4-proof-balance-final-1774012011`
- workflow: `intellectual_genealogy`
- completed source job: `proof-round4-adaptive-balance-final-1774012011`
- source plan: `plan-ef57a3fb980c`
- task: `Trace the genealogy and intellectual development visible in this saved result.`

What the saved live trace shows:

- the preflight source job is a completed genealogy saved result with `presentation_status = completed`, `result_state = ready`, and `restore_available = true`
- `route-task` returns:
  - `routing_outcome = genealogy_transient_source_backed`
  - advisory `launch_contract_kind = planner.direct_sections_compose_handoff`
- `plan-task` returns:
  - `planning_decision_id = planning-decision-b1600d054991`
  - `planning_outcome_kind = direct_sections_composition_handoff_plan`
  - `downstream_readiness = ready_for_direct_sections_compose_handoff`
- the persisted planning snapshot round-trips the non-AOI handoff
- the lowered compose request remains thin and keeps:
  - `workflow_key = intellectual_genealogy`
  - `consumer_key = the-critic`
- the final compose response renders a real transient presentation whose presentation payload records:
  - `workflow_key = intellectual_genealogy`
  - `resolver_version = compose-from-intent-v2`

The saved trace also records the structural proof boundary explicitly:

- `observed_no_executor_jobs = true`
- `observed_no_aoi_proxy_compose = true`

## Verification

Analyzer verification passed:

- `PYTHONPATH=. pytest -q tests/test_phase1c_genealogy_direct_sections.py tests/test_genealogy_saved_result_bridge.py`

Result:

- `7 passed`

Host/runtime verification passed:

- `CI=true npm test -- --runInBand --watchAll=false src/lib/hostContractRuntime.test.ts src/lib/taskLaunchRuntime.test.ts src/routes.test.ts src/pages/GenealogyTransientProofPage.test.tsx`

Result:

- `19 passed`

Live proof artifacts:

- `communications/PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json`
- `communications/PROOF_phase2_host_neutral_transient_proof_rendered_2026-03-28.png`
- `communications/PROOF_phase2_host_neutral_transient_proof_session_2026-03-28.har`
- `communications/PROOF_phase2_host_neutral_transient_proof_invalid_planning_identity_2026-03-28.json`

Negative proof:

- invalid `planning_decision_id` at the lowering route returns `404`
- saved evidence:
  - `communications/PROOF_phase2_host_neutral_transient_proof_invalid_planning_identity_2026-03-28.json`

Shutdown check:

- local analyzer and `the-critic` services were stopped after proof
- ports `8002`, `5555`, and `3456` are closed

## Boundary after Phase 2

Phase 2 now closes honestly.

Why the Phase 2 bar is satisfied:

- the stronger transient proof is now outside the AOI page/controller path
- the proof is genuinely non-AOI at the workflow and planning layers
- the proof consumes analyzer-owned planner truth, persisted planning truth, analyzer-owned lowering, and transient presenter law without rebuilding workflow semantics locally
- the proof stays off both AOI proxy compose routes and `/v1/executor/jobs`
- the proof includes a fail-closed negative case on invalid planning identity

What is still not claimed:

- no new transient consumer registration exists yet
- no second registered transient consumer has been added
- no session/draft/reopen lifecycle object exists yet
- no publish/share semantics exist yet
- no automatic persistence of transient presentations exists yet

## Next honest step

The next step is Phase 3 bounded lifecycle v1.

That slice should define one explicit lifecycle object and one explicit save/reopen law on top of the now-proved transient planner-to-presentation substrate.

It should not reopen:

- Phase 1 bridge structure
- Phase 2 proof-vehicle choice
- transient consumer registration
- AOI-specific proxy continuity work as the default lifecycle substrate

The main missing seam is no longer host-neutral transient proof.
It is explicit lifecycle law for dynamic analytical surfaces.
