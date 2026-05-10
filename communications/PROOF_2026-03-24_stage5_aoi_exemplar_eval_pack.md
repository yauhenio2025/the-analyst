# Proof: Stage 5 AOI Exemplar Eval Pack

Date: 2026-03-24
Status: Executed
Outcome: Revision required
Program: Dynamic Bespoke Apps Platformization

## Scope

This proof executes the Stage 5 AOI exemplar exit gate against the real planner-primary AOI product flow in `the-critic`.

Acceptance seam under test:

- `route-task`
- `plan-task`
- planner-backed AOI handoff
- `compose-from-selection`
- rendered transient AOI result in `the-critic`

This run used the frozen rubric in:

- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`

## Environment

- analyzer-v2: local
- the-critic: local
- ready proof target:
  - project: `round5-proof-dossier-final-1774100000`
  - source job: `proof-round5-adaptive-aoi-dossier-final-1774100000`
  - thinker: `otto_neurath`
- blocked proof target:
  - project: `stage5-proof-aoi-blocked-20260324`
  - source job: `stage5-aoi-blocked-source-20260324`
  - thinker: `otto_neurath`

Fixture strength labels for this pack:

- all four cases are `fixture_backed`

Operational prep performed for this run:

- prepared the synthetic blocked AOI saved-result fixture in local analyzer data
- prepared matching local project / thinker records in `the-critic`
- verified exact local result discovery scope before running the browser pack

## Artifact Set

Summary:

- `communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-24.json`

Per-case HAR / JSON / screenshot:

- `communications/PROOF_stage5_aoi_evolution_ready_session_2026-03-24.har`
- `communications/PROOF_stage5_aoi_evolution_ready_requests_2026-03-24.json`
- `communications/PROOF_stage5_aoi_evolution_ready_state_2026-03-24.png`
- `communications/PROOF_stage5_aoi_engagement_ready_session_2026-03-24.har`
- `communications/PROOF_stage5_aoi_engagement_ready_requests_2026-03-24.json`
- `communications/PROOF_stage5_aoi_engagement_ready_state_2026-03-24.png`
- `communications/PROOF_stage5_aoi_non_profile_ready_session_2026-03-24.har`
- `communications/PROOF_stage5_aoi_non_profile_ready_requests_2026-03-24.json`
- `communications/PROOF_stage5_aoi_non_profile_ready_state_2026-03-24.png`
- `communications/PROOF_stage5_aoi_selection_blocked_session_2026-03-24.har`
- `communications/PROOF_stage5_aoi_selection_blocked_requests_2026-03-24.json`
- `communications/PROOF_stage5_aoi_selection_blocked_state_2026-03-24.png`

## Verification Commands

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

Observed results:

- analyzer focused pack: `53 passed`
- frontend focused pack: `85 passed`
- backend focused pack: `42 passed`

Warnings remained limited to the pre-existing React `act(...)`, Pydantic deprecation, FastAPI `on_event`, and SQLAlchemy mapper warnings already present in earlier slices.

## Case Results

### 1. `evolution_ready`

Expected:

- ready
- selected sources include `thematic_synthesis` and `thematic_report`

Actual:

- `route-task` succeeded
- `plan-task` returned `aoi_selection_blocked`
- reason code: `llm_provider_failure`
- no compose request was issued
- the AOI page did not surface a stable blocked banner after the plan response

Rubric result:

- `selection_fit`: fail
- `rationale_clarity`: pass in artifact trail, fail in host visibility
- `rendered_usefulness`: fail
- `operational_behavior`: fail

### 2. `engagement_ready`

Expected:

- ready
- selected sources include `engagement_mapping` and `sin_findings`

Actual:

- `route-task` succeeded
- `plan-task` returned `aoi_selection_blocked`
- reason code: `llm_provider_failure`
- no compose request was issued
- the AOI page did not surface a stable blocked banner after the plan response

Rubric result:

- `selection_fit`: fail
- `rationale_clarity`: pass in artifact trail, fail in host visibility
- `rendered_usefulness`: fail
- `operational_behavior`: fail

### 3. `non_profile_ready`

Expected:

- ready
- selected sources exactly:
  - `thematic_synthesis`
  - `engagement_mapping`
  - `thematic_report`
- `sin_findings` rejected
- `legacy_profile_equivalent = null`

Actual:

- `route-task` succeeded
- `plan-task` returned `aoi_selection_blocked`
- reason code: `llm_provider_failure`
- no compose request was issued
- the AOI page did not surface a stable blocked banner after the plan response

Important note:

- an earlier direct API spot check in this workstream had produced a successful non-profile handoff once
- this Stage 5 gate grades the real product-path pack as executed, not the best ad hoc earlier probe

Rubric result:

- `selection_fit`: fail
- `rationale_clarity`: pass in artifact trail, fail in host visibility
- `rendered_usefulness`: fail
- `operational_behavior`: fail

### 4. `selection_blocked`

Expected:

- real planner-primary `aoi_selection_blocked`
- reason code `no_usable_source_families`
- no compose request after plan result
- blocked reason visible in the AOI host UI

Actual:

- `route-task` succeeded
- `plan-task` returned `aoi_selection_blocked`
- reason code: `no_usable_source_families`
- no compose request was issued
- blocked reason was captured in HAR / JSON
- the AOI page did **not** surface a stable blocked banner after the plan response

Rubric result:

- `selection_fit`: not applicable
- `rationale_clarity`: pass in artifact trail
- `rendered_usefulness`: not applicable
- `operational_behavior`: fail

## Gate Decision

### Stage 5 seam gate

Result: **fail**

Reason:

- all four cases reached the planner seam
- all four produced auditable planning results
- but none of the four cases passed the required `operational_behavior` threshold
- the three required ready cases all blocked at planning time with `llm_provider_failure`
- the real blocked case returned the expected `no_usable_source_families` plan result
- the AOI host UI did not carry blocked planner outcomes through as a stable visible banner/state in the actual product flow

This means the exit gate cannot be claimed as closed.

### Stage 2 documentary closure

Result: **remain open**

Reason:

- Stage 5 seam gate failed
- no ready case reached a rendered planner-backed selection flow
- no case in this pack is `execution_backed`

## Quality Boundary

Even if the ready cases had passed, this pack would still have been primarily a seam-and-product-behavior audit over `fixture_backed` sources.

This proof therefore does not claim:

- stronger presentation/polish quality
- execution-backed AOI exemplar maturity
- Stage 2 documentary closure

## Main Findings

1. The planner-primary AOI product flow is not yet stable enough for Stage 5 closure.
2. The LLM selector/provider path is operationally unreliable enough in this environment to block all three required ready cases.
3. The host UI currently fails to surface blocked planner outcomes as a stable visible state, even when the underlying `plan-task` response is present and auditable.
4. The blocked-case fixture itself is valid and useful:
   - `route-task` succeeds
   - `plan-task` returns `no_usable_source_families`
   - no compose request is issued afterward

## Next Honest Move

Do not promote AOI exemplar completion in the roadmap yet.

The next step should be a bounded Stage 5 revision slice that:

1. stabilizes planner-outcome visibility in the AOI host surface
2. diagnoses and reduces `llm_provider_failure` on the ready-case planner path
3. reruns the same fixed eval pack before any move to broader transient-substrate generalization
