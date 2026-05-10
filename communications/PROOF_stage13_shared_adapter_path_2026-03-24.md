# Proof: Stage 13 Shared Adapter Path

Date: 2026-03-24
Stage: 13 / Minimal Generic Host Contract / First Slice

## Claim

The current host now consumes the bounded Stage 13 proof seams through one shared adapter/client layer, with Stage 13 work either closing the remaining contract-covered gaps or verifying that a page was already compliant.

## Shared Adapter Evidence

- `webapp/src/lib/boundedV2Client.ts` now owns:
  - run discovery
  - result discovery
  - run detail
  - result manifest
  - result presentation
  - result refresh
  - single-view fetch
  - source-backed readiness
  - cache snapshot warmup
- `webapp/src/hooks/useBoundedV2Workspace.ts` is the shared result-backed workspace adapter over:
  - AOI proof-mode restore without readiness overreach
  - genealogy requestedMode/displayMode readiness gating

## Page-Level Consumption After Stage 13

- `webapp/src/components/influence/AoiV2ThematicPanel.tsx`
  - single-view lazy load now uses `getBoundedV2SingleView(...)`
  - AOI readiness-first launch now uses `getBoundedV2SourceBackedReadiness(...)`
- `webapp/src/pages/AnxietyOfInfluencePages.tsx`
  - bare thinker default-tab resolution is verified on `discoverBoundedV2Runs(...)` and `discoverBoundedV2Results(...)`
- `webapp/src/pages/GenealogyPage.tsx`
  - result discovery, run discovery, run detail, manifest, presentation, refresh, and cache warmup are verified on `boundedV2Client`, with any remaining contract-covered gaps closed in this slice
- `webapp/src/pages/AnalysisWorkspacePage.tsx`
  - continues to consume the shared workspace hook and shared single-view helper

## Explicit Out-Of-Scope Direct Fetches Still Remaining

- polish / polish-section
- pipeline visualization
- provenance support fetches
- export links
- unrelated host-local API calls

Those remain outside the bounded Stage 13 proof claim.
