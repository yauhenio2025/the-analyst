# Proof: Stage 13 / Second Slice Harder Generic Host Proof

Date: 2026-03-24
Scope Memo: `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_scope.md`

## What Landed

The bounded second Stage 13 slice is now real in code.

The-critic now has one shared host-contract runtime layer at:

- `webapp/src/lib/hostContractRuntime.ts`

That runtime makes Host Contract v1 operational for the current must-have families by centralizing:

- owner-aware dispatch
- required-input validation
- structural vs request-parameter consumer-key handling
- typed host-surface lookup

Host Contract v1 remains declarative and serializable in:

- `webapp/src/lib/hostContractV1.ts`

The generated analyzer-side proof artifact was refreshed from that typed source of truth:

- `communications/PROOF_stage13_host_contract_v1_2026-03-24.json`

## Stronger Generic-Host Evidence

This slice materially strengthens the thin-host proof in three concrete ways.

First, the two remaining transient gaps now run through the same contract-driven runtime family model as the result-backed helpers:

- `composeFromIntent(...)`
- `composeFromSource(...)`

Those wrappers now dispatch through the shared runtime instead of carrying their own transport/consumer-key policy locally.

Second, the three bounded proof surfaces now have executable host-surface lookup law rather than documentary-only rules:

- `aoi_result_thematic_experience`
- `aoi_source_backed_transient_launch_experience`
- `genealogy_result_backed_workspace_experience`

That runtime lookup is now used to govern:

- AOI source-backed readiness applicability in `AoiV2ThematicPanel.tsx`
- genealogy result-backed readiness-first gating in `useBoundedV2Workspace.ts`

This remains intentionally bounded:

- `AnalysisWorkspacePage` is not now universally surface-driven for every workflow
- the typed lookup is currently consumed in the genealogy proof seam and AOI proof controls, primarily to govern readiness applicability and allowed family use

Third, one remaining page-local contract seam also moved onto the shared runtime path:

- AOI snapshot warmup now uses `cacheBoundedV2Presentation(...)` instead of a direct page-owned host API call

## Important Correction

Implementation exposed one real contract mismatch from the first Stage 13 slice.

`source_backed_transient_launch` had been recorded as if `source_analysis_id|source_v2_job_id` were required inputs.
The live the-critic host proxy does not require those selectors; it can resolve the latest AOI source result from:

- `project_id`
- `selected_source_thinker_id`
- `profile`

So the typed contract and generated artifact were corrected to match the live route truth, while preserving `selected_source_thinker_id` as a real required input.

## Verification

TypeScript:

- `./webapp/node_modules/.bin/tsc -p /home/evgeny/projects/the-critic/webapp/tsconfig.json --noEmit`
- result: passed

Focused host regression:

- `CI=true npm --prefix /home/evgeny/projects/the-critic/webapp test -- --runInBand --watchAll=false src/lib/hostContractV1.test.ts src/lib/hostContractRuntime.test.ts src/lib/boundedV2Client.test.ts src/lib/composeFromIntentClient.test.ts src/hooks/useBoundedV2Workspace.test.tsx src/components/influence/AoiV2ThematicPanel.test.tsx src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx src/pages/AoiComposeFromIntentPage.test.tsx src/transientComposeIsolation.test.ts`
- result: `10` suites, `160` tests passed

Residual note:

- existing React `act(...)` warnings remain in several async tests, but there were no failures
- `transientComposeIsolation.test.ts` still mostly protects the older forbidden-import boundary; it stays compatible with the shared runtime layer, but it should not be overstated as a complete dispatch-mode separation proof by itself

## Judgment

This is a materially harder generic-host proof than the first Stage 13 slice.

It is still not a Stage 13 closeout.

What is now true:

- Host Contract v1 is both code-authoritative and runtime-authoritative for the bounded current surface set
- result-backed and transient families now share the same contract-driven execution model
- host-surface selection is no longer purely page-local prose for the three proof seams

What is still not true:

- there is no second consumer
- AOI source-backed transient launch is still explicitly host-bounded
- Stage 14 lifecycle law is still unopened

So the honest ledger state remains:

- `Stage 13 = Partial`
