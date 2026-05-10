# Memo: Stage 13 / Second Slice Harder Generic Host Proof Completion

Date: 2026-03-24
Scope Memo: `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_scope.md`
Prior Completion: `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_completion.md`

## Summary

The bounded second Stage 13 slice is complete.

The-critic now has a shared Host Contract v1 runtime layer that:

- keeps the typed contract declarative in `hostContractV1.ts`
- executes owner-aware dispatch and required-input validation in `hostContractRuntime.ts`
- pulls the two remaining transient families under the same contract-driven runtime model as the result-backed families
- turns the three current proof seams into executable host-surface lookup law

This landed without changing analyzer public APIs.

## What Changed

Runtime authority is now explicit for the bounded current surface set.

Key implementation outcomes:

- `composeFromIntent(...)` now executes the `transient_compose_from_intent` family through the shared runtime
- `composeFromSource(...)` now executes the `source_backed_transient_launch` family through the shared runtime while remaining host-proxy owned
- `boundedV2Client.ts` wrappers now resolve through the same runtime instead of carrying route/owner policy independently
- `useBoundedV2Workspace.ts` now uses a typed host-surface key to govern genealogy proof-seam readiness applicability rather than a page-local capability assumption
- `AoiV2ThematicPanel.tsx` now derives AOI source-backed readiness applicability from the typed host-surface lookup and uses the shared cache-warmup wrapper

## Contract Correction

Implementation exposed one real mismatch in the first-slice Host Contract v1 ledger.

`source_backed_transient_launch` had recorded `source_analysis_id|source_v2_job_id` as hard required inputs.
The live host proxy route does not require those selectors; it can resolve the latest AOI source result when they are omitted.

So the contract was corrected to:

- keep `project_id`, `selected_source_thinker_id`, and `profile` as required inputs
- treat `source_analysis_id` and `source_v2_job_id` as optional continuity selectors

The generated JSON artifact was regenerated accordingly:

- `communications/PROOF_stage13_host_contract_v1_2026-03-24.json`

## Verification

TypeScript:

- `./webapp/node_modules/.bin/tsc -p /home/evgeny/projects/the-critic/webapp/tsconfig.json --noEmit`
- passed

Focused host regression:

- `CI=true npm --prefix /home/evgeny/projects/the-critic/webapp test -- --runInBand --watchAll=false src/lib/hostContractV1.test.ts src/lib/hostContractRuntime.test.ts src/lib/boundedV2Client.test.ts src/lib/composeFromIntentClient.test.ts src/hooks/useBoundedV2Workspace.test.tsx src/components/influence/AoiV2ThematicPanel.test.tsx src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx src/pages/AoiComposeFromIntentPage.test.tsx src/transientComposeIsolation.test.ts`
- result: `10` suites, `160` tests passed

Non-blocking residual:

- existing React `act(...)` warnings remain in several async tests

## Status

This slice materially advances Stage 13, but it does not close it.

What is now stronger:

- one shared contract-driven runtime covers both result-backed and transient must-have families
- host-surface selection is executable for the three current proof seams, though the workspace hook currently consumes that law primarily for readiness applicability rather than as a universal surface runtime
- the host no longer owns transient dispatch law in a separate client stack

Boundary note:

- `transientComposeIsolation.test.ts` still primarily enforces the older forbidden-import boundary; it now remains compatible with the shared runtime shape, but it is not yet a full dispatch-mode separation proof on its own

What still keeps Stage 13 open:

- the proof is still current-consumer-only
- AOI source-backed transient launch remains explicitly host-bounded
- no second-consumer or truly host-neutral proof exists yet

So the honest ledger remains:

- `Stage 13 = Partial`
