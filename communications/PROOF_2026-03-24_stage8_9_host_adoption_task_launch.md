# Stage 8/9 Host Adoption Task Launch Proof

Date: 2026-03-24

## Proof Claims

1. The current consumer now uses analyzer-owned `route-task` and `plan-task` in one AOI source-backed handoff seam.
2. The current consumer now uses analyzer-owned `route-task` and `plan-task` in one genealogy registered-corpus execution seam.
3. The genealogy proof path no longer falls back to `orchestrator/analyze-by-ref` after planning.
4. Planner-backed AOI task text is not threaded through URL query params.

## Code Evidence

AOI:
- `the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`

Genealogy:
- `the-critic/analyzer/concept_analyzer/analyzer_v2_client.py`
- `the-critic/api/models_genealogy.py`
- `the-critic/api/server.py`

Focused tests:
- `the-critic/webapp/src/lib/taskLaunchRuntime.test.ts`
- `the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`
- `the-critic/webapp/src/pages/AoiComposeFromIntentPage.test.tsx`
- `the-critic/tests/test_aoi_v2_client.py`
- `the-critic/tests/test_aoi_v2_routes.py`

## Verification

Frontend:
- `CI=true npm --prefix webapp test -- --runInBand --watchAll=false ...`
- result: `11 suites`, `165 tests` passed

Backend:
- `PYTHONPATH=/home/evgeny/projects/the-critic pytest -q tests/test_aoi_v2_client.py tests/test_aoi_v2_routes.py`
- result: `38 passed`

Build checks:
- `tsc --noEmit` passed
- `py_compile` passed

## Boundaries Confirmed

- AOI planner-backed task is passed through navigation state rather than query params.
- Genealogy `launch_contract_mode='task_planned'` is rejected unless the bounded v2 registered-corpus proof conditions hold.
- AOI legacy launch controls still exist beside the planner-backed proof path.
- Genealogy legacy launch modes still exist outside the explicit task-planned proof mode.
