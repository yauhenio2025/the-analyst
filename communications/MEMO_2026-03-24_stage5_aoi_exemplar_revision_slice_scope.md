# Memo: Stage 5 AOI Exemplar Revision Slice Scope

Date: 2026-03-24
Status: Draft scope memo
Program: Dynamic Bespoke Apps Platformization
Depends on:
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/PROOF_2026-03-24_stage5_aoi_exemplar_eval_pack.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_revision.md`
Roadmap sources:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

## Summary

The first Stage 5 AOI exemplar exit-gate run failed.

That does **not** justify a pivot to Tranche 3 or a reorder of the roadmap.
It justifies one bounded revision slice inside the existing AOI exemplar tranche.

This revision slice should do two things only:

1. diagnose and harden AOI selector/provider reliability on the ready-case planner path
2. stabilize planner-outcome visibility in the `the-critic` AOI host surface

Then it should rerun the same frozen four-case Stage 5 pack with the same rubric.

No new architecture line should begin until that rerun is honestly passed.

## Why This Is The Next Honest Step

The failed gate already told us something useful:

- `route-task` is working in the product path
- `plan-task` is being reached for all required cases
- the blocked-case fixture is valid and auditable
- the current failure is not “the architecture was wrong”
- the current failure is:
  - selector/provider reliability on ready cases
  - planner-outcome visibility on the AOI host surface

That means the correct response is a local repair slice, not a program-level pivot.

## Bounded Claim

The bounded claim for this slice is:

- the Stage 5 gate should be rerun only after the two specific failure classes exposed by the first run are addressed strongly enough to make the same frozen pack meaningful again

This slice does **not** claim:

- Stage 5 completion in advance
- Stage 2 closure in advance
- broader transient-substrate generalization
- lifecycle work
- second-consumer transient proof
- a new planner architecture

## Scope Decisions

### Decision 1: Keep the same roadmap order

Do not pivot phases.

Keep:

- AOI exemplar completion before Tranche 3 transient-substrate generalization
- Stage 2 closure tied to Stage 5 evidence
- the same fixed four-case pack
- the same frozen rubric

This slice is a recalibration of the immediate plan only.

### Decision 2: Split the failure into two workstreams

The first gate run exposed exactly two revision workstreams:

1. selector/provider reliability
2. host visibility / UI-state retention

Both should stay bounded and concrete.

### Decision 3: Diagnose selector/provider reliability before widening behavior

The ready-case failures all returned `aoi_selection_blocked` with `llm_provider_failure`.

Leading evidence-backed working hypothesis from the existing evidence:

- `AOI_SELECTION_TIMEOUT_S = 10.0` is currently hardcoded in `src/orchestrator/task_planner.py`
- the Stage 5 artifacts showed roughly `32s` wall-clock on the blocking `plan-task` response
- likely retry amplification, if SDK defaults remained in effect
- the provider exception appears to have been raised as a connection-level/interruption error rather than an `httpx.TimeoutException`
- so the current implementation likely classified a timeout-shaped provider failure as `llm_provider_failure` rather than `llm_timeout`

This revision slice must turn that hypothesis into a concrete diagnosis and response plan.

The selector/provider work should be split into explicit buckets:

1. environment/config
   - missing provider credentials are not the leading hypothesis
   - invalid credentials or other provider-side config issues remain logically possible, but are not indicated by the current artifacts
   - local proof-environment instability
2. timeout budget
   - current AOI selector timeout is too tight for the real local run
   - `AOI_SELECTION_TIMEOUT_S` should be made env-configurable, matching the existing `AOI_SELECTION_MODEL` pattern
3. SDK retry behavior
   - whether retries occurred, observed directly or inferred from artifacts
   - whether Anthropic SDK defaults amplified the wall-clock duration
4. transport / provider-path fragility
   - dropped connection / interrupted request handling
   - provider-side connection instability
5. retry policy
   - whether one bounded retry is warranted or whether fail-closed/no-retry remains the right policy
6. reason-code classification
   - current exception mapping should distinguish timeout exceptions from broader connection/provider failures
   - timeout-shaped provider failures should not be collapsed blindly into `llm_provider_failure`
   - this likely means catching provider timeout / connection exceptions more explicitly rather than relying only on the current `httpx.TimeoutException` branch

This should be decided from evidence, not guesswork.

Default rule:

- do not widen selector behavior or relax the eval pack until the failure class is understood

Allowed outcomes:

- environment-only fix
- bounded timeout adjustment
- env-configurable selector timeout
- bounded provider-path hardening
- bounded retry-policy decision
- bounded reason-code classification hardening

Not allowed:

- replacing the selector with deterministic fallback just to pass the pack
- relabeling blocked ready cases as acceptable

### Decision 4: Stabilize planner-outcome visibility in the AOI panel

The first run showed:

- the blocked planner result existed in the network/artifact trail
- `setPageError(...)` was reached on the blocked path
- but the AOI page did not retain that state as a stable visible banner long enough for the gate
- one of the many later `setPageError(null)` / hydration / source-refresh paths appears to be clearing it

This slice should treat that as a proof-surface bug.

This is a state-retention problem, not a state-production problem.

The required host behavior is:

- ready planner outcome:
  - the structured planner outcome is the source of truth
  - `pageError` may mirror that state, but must not replace it
  - the handoff summary stays visible long enough for the user to continue into compose
  - it is not immediately cleared by a later hydrate/source refresh cycle
- blocked planner outcome:
  - the structured planner outcome is the source of truth
  - `pageError` may mirror that state, but must not replace it
  - the reason code and detail remain stably visible in the AOI panel error/banner state
  - the reason code and detail remain artifact-visible in the saved proof trail
  - they are not immediately overwritten or cleared by later hydrate/source refresh/update paths

Planner outcome may be cleared only by:

- a new planning attempt
- explicit dismissal
- explicit source switch

This is not a UX redesign task.
It is a structured stability/retention fix on the existing proof surface.

### Decision 5: Keep the Stage 5 pack and rubric frozen

Do not change:

- the four case types
- the locked non-profile case
- the blocked-case requirement
- the rubric dimensions
- the threshold shape

The same pack must be rerun after the bounded fixes.

Otherwise the program will be changing the test because the test failed.

### Decision 6: Stage 2 remains explicitly out of reach unless the rerun earns it

Do not soften the Stage 2 bar.

Even if the rerun passes Stage 5 seam behavior, Stage 2 should still remain open unless:

- at least one ready case is `execution_backed` or stronger
- the rerun evidence is stronger than fixture-only seam proof

This slice should not attempt to “solve” that by rewriting the criterion.

## Proposed Deliverables

### 1. Selector/provider diagnosis note

One short memo or section that states which failure class was actually observed:

- environment/config
- timeout budget
- SDK retry behavior
- transport / provider-path fragility
- retry policy decision
- reason-code classification gap

and records:

- observed exception class
- emitted reason code
- request elapsed time from real request artifacts
- whether retries occurred, observed directly or inferred from artifacts
- which failure bucket actually applied
- what bounded fix was applied, if any

Latency diagnosis must use real request timing from HAR/request artifacts, not only the summary JSON `planner_selection_latency` field.

### 2. Bounded proof-surface fix

One small implementation slice over:

- AOI planner outcome retention in `AoiV2ThematicPanel`
- structured planner outcome retained separately from generic `pageError` text
- structured retention across hydrate/source refresh in the host UI
- stable blocked banner behavior
- blocked reason code/detail retained in the saved proof artifacts, not only the live UI
- stable ready-handoff visibility long enough to continue into compose
- and only the selector/provider hardening truly needed for rerun

### 3. Focused verification rerun

Exact commands:

Analyzer:

```bash
PYTHONPATH=. pytest -q tests/test_task_router.py tests/test_task_planner.py tests/test_composition_source_bridge.py tests/test_compose_from_intent.py
```

The Critic frontend:

```bash
/home/evgeny/projects/the-critic/webapp/node_modules/.bin/tsc -p /home/evgeny/projects/the-critic/webapp/tsconfig.json --noEmit
CI=true npm --prefix /home/evgeny/projects/the-critic/webapp test -- --runInBand --watchAll=false src/lib/taskLaunchRuntime.test.ts src/lib/composeFromIntentClient.test.ts src/components/influence/AoiV2ThematicPanel.test.tsx src/pages/AoiComposeFromIntentPage.test.tsx src/transientComposeIsolation.test.ts src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx
```

The Critic backend:

```bash
PYTHONPATH=. pytest -q tests/test_aoi_v2_client.py tests/test_aoi_v2_routes.py
```

Additional test obligations inside the same focused pack:

- a frontend test proving blocked outcome visibility survives initial auto-load / saved-result hydrate churn
- a frontend test proving ready handoff visibility survives the same churn long enough to continue into compose
- an analyzer test proving timeout exceptions are distinguished intentionally from broader connection/provider failures
- an analyzer test for any env-configurable timeout behavior introduced by the slice

### 4. Same-pack rerun

Rerun the exact same Stage 5 artifact pack:

- `evolution_ready`
- `engagement_ready`
- `non_profile_ready`
- `selection_blocked`

using the same HAR / JSON / screenshot capture method and the same rubric.

### 5. One honest rerun decision memo

After rerun, write one of:

- completion memo if the gate truly passes
- second revision memo if it still does not

## Exit Conditions

This revision slice is complete only when:

1. the selector/provider failure class is explicitly identified
   - including env vs timeout budget vs SDK retry behavior vs transport/provider fragility vs classification
2. the AOI panel visibly retains planner outcomes stably enough for capture
   - with structured planner outcome retained separately from generic page-error text
3. the same frozen Stage 5 pack is rerun
4. the roadmap can honestly say either:
   - Stage 5 now passes
   - or Stage 5 still does not pass

## Non-Goals

- no Tranche 3 work
- no Stage 7 expansion
- no lifecycle work
- no aoi-canary work
- no contract widening beyond what the bounded fix truly requires
- no change to the fixed eval pack
