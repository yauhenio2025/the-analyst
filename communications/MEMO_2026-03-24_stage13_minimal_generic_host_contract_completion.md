# Memo: Stage 13 / Minimal Generic Host Contract Completion

Subtitle: Bounded First Slice Implemented, But Stage 13 Still Remains Partial

Date: 2026-03-24
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Scope Memo: `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md`

## Outcome

The bounded first slice of Stage 13 landed.

What is now true:

- the-critic has one typed Host Contract v1 source of truth in `webapp/src/lib/hostContractV1.ts`
- the analyzer-v2 communications ledger now contains a generated JSON artifact derived from that typed contract rather than a hand-maintained prose matrix:
  - `communications/PROOF_stage13_host_contract_v1_2026-03-24.json`
- AOI source-backed transient launch now uses analyzer-owned readiness before launch when the selected source has canonical upstream `v2_job_id`
- genealogy result-backed explicit `composition_mode` flows now use analyzer-owned readiness through the shared workspace path, with an explicit `requestedMode` / `displayMode` split
- the targeted proof pages are now either verified on the shared bounded client layer already or had their remaining contract-covered gaps closed there

## What Changed

### 1. Typed host contract became authoritative

The contract is now code-owned first.

- `webapp/src/lib/hostContractV1.ts` enumerates the 11 Host Contract v1 families
- it also encodes:
  - consumer-key asymmetry
  - readiness capability table
  - host-owned surface selection rules
  - thinker-scoped AOI source-backed launch requirements, including `selected_source_thinker_id`
- `scripts/generate-stage13-host-contract-v1-json.mjs` serializes that typed contract deterministically into the analyzer-v2 communications folder
- `webapp/src/lib/hostContractV1.test.ts` deep-compares the typed serialization to the checked-in JSON artifact so prose/code drift fails fast

### 2. Shared adapter use was verified and narrowly widened across the proof seams

The bounded client layer is now the real contract-covered fetch substrate across the implemented seams.

- `AoiV2ThematicPanel` now uses:
  - `getBoundedV2SingleView(...)`
  - `getBoundedV2SourceBackedReadiness(...)`
- `AnxietyOfInfluencePages` is verified on:
  - `discoverBoundedV2Runs(...)`
  - `discoverBoundedV2Results(...)`
- `GenealogyPage` is verified on the shared helpers for:
  - run discovery
  - result discovery
  - run detail
  - manifest
  - presentation
  - refresh
  - cache warmup
- `AnalysisWorkspacePage` continues to sit on `useBoundedV2Workspace(...)`, which now owns the genealogy readiness gate

### 3. AOI readiness-backed launch is now explicit

The AOI source-backed launch flow now has three honest states:

1. `ready`
   - readiness check succeeds
   - snapshot warmup proceeds if needed
   - navigation proceeds
2. `blocked`
   - analyzer-derived blocker reasons are shown
   - no warmup
   - no navigation
3. `outside_proof_slice`
   - host-local alias without canonical `v2_job_id`
   - existing launch path preserved
   - readiness intentionally skipped

That preserves the real host-owned AOI proxy/preparation seam instead of pretending AOI source-backed launch is already consumer-neutral.

### 4. Genealogy result-backed readiness is now explicit

The shared result-backed flow now distinguishes:

- `requestedMode`
  - URL or user-selected `composition_mode`
- `displayMode`
  - the mode actually used for downstream manifest/presentation fetches

Behavior now is:

- requested mode ready:
  - `displayMode = requestedMode`
- requested mode blocked:
  - `displayMode = undefined`
  - the URL is preserved
  - the requested blocked mode is reported explicitly
  - the visible content becomes the default/no-mode presentation
  - if the same presentation is already visible, it stays visible instead of being blown away
  - lazy single-view fetches also use `displayMode`, so blocked requested modes do not leak back into downstream single-view requests

AOI result-backed `composition_mode` readiness remains intentionally unsupported in this slice.

## Verification

Focused the-critic verification passed:

- `webapp/src/lib/hostContractV1.test.ts`
- `webapp/src/lib/boundedV2Client.test.ts`
- `webapp/src/hooks/useBoundedV2Workspace.test.tsx`
- `webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`
- `webapp/src/pages/AnxietyOfInfluencePages.test.tsx`
- `webapp/src/pages/AnalysisWorkspacePage.test.tsx`
- `webapp/src/pages/AnalysisWorkspacePage.integration.test.tsx`

Result:

- `131 passed`

There were React `act(...)` warnings in some pre-existing async test patterns during the focused run, but no failing assertions in the Stage 13 pack.

## Post-Review Closure

After the first completion write-up, two concrete follow-up issues were identified and then closed:

1. blocked genealogy `requestedMode -> displayMode` fallback did not yet flow all the way through lazy single-view fetches
2. the generated Host Contract v1 JSON artifact understated the AOI source-backed proxy launch requirements by omitting `selected_source_thinker_id`

Those are now resolved.

What changed in the post-review closeout:

- `AnalysisWorkspacePage` now forwards the effective `displayMode` to lazy single-view fetches, so blocked genealogy modes do not leak back into downstream single-view requests
- `hostContractV1.ts` now records `selected_source_thinker_id` as a required input for `source_backed_transient_launch`
- the generated communications JSON artifact was regenerated from the corrected typed contract
- the shared-adapter proof wording was tightened so it distinguishes real migration work from pages that were already effectively compliant on shared helpers

Focused host verification was rerun after those fixes:

- `./webapp/node_modules/.bin/tsc -p webapp/tsconfig.json --noEmit`
- `CI=true npm --prefix webapp test -- --runInBand --watchAll=false webapp/src/lib/hostContractV1.test.ts webapp/src/lib/boundedV2Client.test.ts webapp/src/hooks/useBoundedV2Workspace.test.tsx webapp/src/components/influence/AoiV2ThematicPanel.test.tsx webapp/src/pages/AnxietyOfInfluencePages.test.tsx webapp/src/pages/AnalysisWorkspacePage.test.tsx webapp/src/pages/AnalysisWorkspacePage.integration.test.tsx`

Result:

- `131 passed`

## Proof Artifacts

- `communications/PROOF_stage13_host_contract_v1_2026-03-24.json`
- `communications/PROOF_stage13_aoi_readiness_backed_launch_2026-03-24.json`
- `communications/PROOF_stage13_genealogy_readiness_backed_result_surface_2026-03-24.json`
- `communications/PROOF_stage13_shared_adapter_path_2026-03-24.md`
- `communications/PROOF_2026-03-24_stage13_minimal_generic_host_contract.md`

## Final Judgment

This is the correct first slice of Stage 13.

It materially strengthens the thin-host claim because:

- the contract is explicit
- the code artifact is authoritative
- readiness adoption is cross-workflow
- the shared host adapter path is broader and less page-local

It still does **not** satisfy full Stage 13 exit evidence.

So the correct program state after this slice is:

- `Stage 13 = Partial`
