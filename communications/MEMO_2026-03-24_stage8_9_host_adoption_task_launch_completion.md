# Stage 8/9 Host Adoption Task Launch Completion

Date: 2026-03-24

## Summary

The bounded host-adoption tranche is implemented in `the-critic`.

What landed:
- a new bounded task-launch layer over analyzer-owned `route-task` and `plan-task`
- one AOI planner-backed handoff seam in the current consumer
- one genealogy registered-corpus task-planned execution seam in the current consumer
- host-boundary enforcement so `launch_contract_mode='task_planned'` cannot silently drift back into mixed legacy behavior

This remains a bounded first adoption slice, not lifecycle work and not a second-consumer proof.

## Code Outcome

Frontend:
- `webapp/src/lib/taskLaunchRuntime.ts` now owns typed `route-task` / `plan-task` request dispatch
- `webapp/src/components/influence/AoiV2ThematicPanel.tsx` now has an explicit planner-backed AOI handoff path
- planner-backed AOI task text is passed to `AoiComposeFromIntentPage` through navigation state, not URL params
- `AoiComposeFromIntentPage.tsx` hydrates that planner-backed task into local `sourceUserIntent`
- planner-backed AOI launches now carry analyzer-returned allowed/blocked profile law into the compose page, where blocked profiles are disabled and fail closed even on autostart

Backend:
- `analyzer/concept_analyzer/analyzer_v2_client.py` now has thin sync wrappers for `route-task` and `plan-task`
- `api/models_genealogy.py` now models `launch_contract_mode='legacy' | 'task_planned'` plus explicit `task`
- `api/server.py` now enforces task-planned genealogy only for the bounded `execution_backend='v2'` + registered-corpus proof path
- task-planned genealogy now follows:
  - `route-task`
  - registered-corpus sync
  - `plan-task`
  - `/v1/executor/jobs` via `start_job_from_plan_sync(...)`
- the legacy genealogy launch paths remain intact outside the explicit proof mode
- explicit negative followup branches are now covered and enforced:
  - `route-task -> unsupported` stops before planning
  - `plan-task -> insufficient_context` stops before executor launch
  - non-`/v1/executor/jobs` followup contracts fail closed

## Boundaries

AOI:
- this is contractual consolidation, not a claim that the host has stopped knowing it is on an AOI page
- snapshot warmup remains host-owned after planning-ready
- planner-backed AOI launch requires canonical `source_v2_job_id`
- local-only AOI alias fallback remains legacy / outside the proof slice

Genealogy:
- proof scope is `registered_corpus` only
- proof scope is `comprehensive` mode only
- explicit planning/execution model overrides are not supported in the task-planned proof path
- `plan-task` is treated as commit-like launch preparation, not speculative probing

## Verification

Passed:
- `/home/evgeny/projects/the-critic/webapp/node_modules/.bin/tsc -p /home/evgeny/projects/the-critic/webapp/tsconfig.json --noEmit`
- frontend host boundary:
  - `11` suites
  - `171` tests passed
- backend focused task-launch + AOI route pack:
  - `40` tests passed

Warnings:
- existing React `act(...)` warnings remain in some async host tests
- existing SQLAlchemy mapper warnings remain in backend tests

No new failures were introduced in the focused verification run.

## Post-Review Closeout

After the initial completion pass, two concrete follow-up gaps were identified and then closed:

1. the AOI planner-backed decision was enforced in `AoiV2ThematicPanel` before navigation, but the compose page still exposed both source-backed profile buttons after handoff
2. the main negative planning branches existed in code but did not yet have focused unit coverage at the runtime/component/backend levels

Those are now resolved.

What changed in the closeout:

- the planner-backed AOI handoff now passes analyzer-returned `allowed_profiles` / `blocked_profiles` through navigation state
- `AoiComposeFromIntentPage` now treats planner-backed profile law as authoritative:
  - blocked source-backed buttons are disabled
  - blocked autostarts fail closed before `compose-from-source`
  - analyzer blocker reasons are surfaced on the page
- `webapp/src/lib/taskLaunchRuntime.test.ts` now covers `route-task -> unsupported` and `plan-task -> insufficient_context` at the runtime layer
- `webapp/src/components/influence/AoiV2ThematicPanel.test.tsx` now covers:
  - `route-task -> unsupported`
  - `plan-task -> insufficient_context`
- `tests/test_aoi_v2_routes.py` now covers:
  - `plan-task -> insufficient_context`
  - bad genealogy followup contracts that are not `/v1/executor/jobs`

Focused verification was rerun after those follow-up fixes:

- `/home/evgeny/projects/the-critic/webapp/node_modules/.bin/tsc -p /home/evgeny/projects/the-critic/webapp/tsconfig.json --noEmit`
- `CI=true npm --prefix /home/evgeny/projects/the-critic/webapp test -- --runInBand --watchAll=false src/lib/hostContractV1.test.ts src/lib/hostContractRuntime.test.ts src/lib/boundedV2Client.test.ts src/lib/composeFromIntentClient.test.ts src/lib/taskLaunchRuntime.test.ts src/hooks/useBoundedV2Workspace.test.tsx src/components/influence/AoiV2ThematicPanel.test.tsx src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx src/pages/AoiComposeFromIntentPage.test.tsx src/transientComposeIsolation.test.ts`
- `PYTHONPATH=/home/evgeny/projects/the-critic pytest -q /home/evgeny/projects/the-critic/tests/test_aoi_v2_client.py /home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`

Result:

- frontend: `11` suites, `171` tests passed
- backend: `40` tests passed

## Strategic Result

This tranche makes the host ask analyzer-v2 for bounded routing/planning truth in two real seams, instead of continuing to keep all launch logic local.

It does not close the broader vision.

It does, however, move the program one step closer to the analyzer actually functioning as the brain for task-driven downstream execution and compose handoff in the current consumer.
