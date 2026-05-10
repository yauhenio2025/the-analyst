# Memo: Stage 5 AOI Exemplar Revision Slice Completion

Date: 2026-03-25
Scope Memo: `communications/MEMO_2026-03-24_stage5_aoi_exemplar_revision_slice_scope.md`
Program: Dynamic Bespoke Apps Platformization

## Summary

The bounded Stage 5 revision slice is now implemented.

What landed is the narrow repair slice that the failed first Stage 5 gate called for:

- AOI selector/provider hardening in `analyzer-v2`
- structured planner-outcome retention in `the-critic`
- one follow-up tightening pass so the host behavior matches the memo more closely under real UI churn

This materially strengthens Stage 5 proof-surface readiness.

It does **not** close Stage 5.
It does **not** close Stage 2.

The next immediate step is now operational, not architectural:

1. run one live `evolution_ready` diagnostic spot-check
2. write the diagnosis note
3. rerun the same frozen four-case Stage 5 pack with the same rubric

## What Landed

### In `analyzer-v2`

- `src/llm/client.py`
  - Anthropic client construction now supports AOI-only retry control without changing default behavior for other callers
- `src/orchestrator/task_planner.py`
  - AOI selector timeout is now env-configurable via `AOI_SELECTION_TIMEOUT_S`
  - the current default is `45.0`
  - AOI selector calls now force `max_retries=0`
  - timeout-shaped failures are classified intentionally before broader provider/connection failures
  - blocked selection traces now preserve:
    - effective timeout
    - retry policy
    - exception class name
    - provider outcome
    - blocked reason code/detail

### In `the-critic`

- `webapp/src/components/influence/AoiV2ThematicPanel.tsx`
  - planner outcome is now retained as structured state rather than relying on transient `pageError`
  - blocked planner outcomes remain stably visible in the AOI panel banner
  - ready planner outcomes remain visible long enough to continue into compose
  - hydrate and saved-result refresh churn no longer clear planner outcome by default
  - planner outcome is still cleared on:
    - new planning attempt
    - explicit dismiss
    - explicit source switch
    - active-job reset

### Follow-up tightening after review

After the first implementation pass, one review correctly called out two remaining non-blocking mismatches:

1. task-text edits were still clearing retained planner outcome
2. the most failure-specific hydrate-after-plan race was still not tested directly

Those are now closed.

What changed:

- task-text edits no longer clear planner outcome in `AoiV2ThematicPanel`
- the AOI panel tests now cover:
  - blocked outcome surviving task-text edits
  - blocked outcome surviving the delayed initial auto-load race where hydrate finishes after planner state is already visible

## Behavioral Outcome

The current Stage 5 proof surface is now materially stronger than the one that failed the first gate run.

Before this slice:

- ready-case planner failures were not well distinguished between timeout-shaped and broader provider failures
- blocked traces did not record enough selector/provider detail for a clean diagnosis note
- the AOI panel could lose blocked planner state during hydrate/refresh churn
- planner outcome still drifted slightly from the memo because task edits cleared it

Now:

- the selector path is bounded, no-retry, and better classified
- blocked trace detail is strong enough for the next diagnosis note
- planner outcome is retained as structured state in the host
- task edits no longer wipe retained planner outcome
- the delayed initial auto-load race has direct regression coverage

That is enough to justify the next step being a live diagnostic and rerun, not another speculative code tranche.

## Verification

Analyzer-focused verification:

- `PYTHONPATH=. pytest -q tests/test_task_router.py tests/test_task_planner.py tests/test_composition_source_bridge.py tests/test_compose_from_intent.py`

Result:

- `56 passed`

Current-consumer verification:

- `/home/evgeny/projects/the-critic/webapp/node_modules/.bin/tsc -p /home/evgeny/projects/the-critic/webapp/tsconfig.json --noEmit`
- `CI=true npm --prefix /home/evgeny/projects/the-critic/webapp test -- --runInBand --watchAll=false src/lib/taskLaunchRuntime.test.ts src/lib/composeFromIntentClient.test.ts src/components/influence/AoiV2ThematicPanel.test.tsx src/pages/AoiComposeFromIntentPage.test.tsx src/transientComposeIsolation.test.ts src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx`
- `PYTHONPATH=. pytest -q tests/test_aoi_v2_client.py tests/test_aoi_v2_routes.py`

Result:

- frontend focused pack: `90 passed`
- backend focused pack: `42 passed`

Known warnings still present but non-failing:

- existing React `act(...)` warnings in async hydrate tests
- existing FastAPI deprecation warnings
- existing SQLAlchemy relationship warnings

## Boundaries

This memo records implementation completion for the bounded revision slice only.

Still not done:

- live `evolution_ready` diagnostic spot-check
- diagnosis note from real rerun artifacts
- rerun of the frozen four-case Stage 5 pack
- Stage 5 closure decision
- Stage 2 closure decision

This slice did not change:

- the Stage 5 rubric
- the Stage 5 case set
- the roadmap order
- the Stage 2 closure bar
- any broader transient-substrate or lifecycle strategy

## Status

The honest ledger after this implementation is:

- Stage 2: still `In progress`
- Stage 3: still `Partial`
- Stage 4: still `Partial`
- Stage 5: still `In progress`, but the revision slice is now implemented

The next honest move is:

- one live diagnostic `evolution_ready` spot-check
- then the same frozen Stage 5 rerun

