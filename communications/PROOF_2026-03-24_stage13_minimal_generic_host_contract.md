# Proof: Stage 13 Minimal Generic Host Contract / First Slice

Date: 2026-03-24
Status: Implemented / Bounded Slice Only

## What Landed

- a typed Host Contract v1 source of truth in the-critic:
  - `webapp/src/lib/hostContractV1.ts`
- deterministic serialization of that typed contract into the analyzer-v2 communications ledger:
  - `communications/PROOF_stage13_host_contract_v1_2026-03-24.json`
- shared analyzer client adoption on the remaining contract-covered page seams:
  - `AoiV2ThematicPanel`
  - `AnxietyOfInfluencePages`
  - `GenealogyPage`
- cross-workflow readiness adoption on two bounded proof seams:
  - AOI source-backed profile launch
  - genealogy result-backed explicit `composition_mode`
  - including the requested-mode/display-mode split for blocked genealogy modes all the way through lazy single-view fetches

## Acceptance Evidence

- Host Contract v1 JSON artifact:
  - `communications/PROOF_stage13_host_contract_v1_2026-03-24.json`
- AOI readiness-backed launch proof:
  - `communications/PROOF_stage13_aoi_readiness_backed_launch_2026-03-24.json`
- genealogy readiness-backed result-surface proof:
  - `communications/PROOF_stage13_genealogy_readiness_backed_result_surface_2026-03-24.json`
- shared adapter proof:
  - `communications/PROOF_stage13_shared_adapter_path_2026-03-24.md`

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

- `129 passed`

## Honest Boundary

This does **not** close Stage 13.

What remains outside this slice:

- second-consumer or materially harder generic-host proof
- analyzer-side removal of `TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"`
- host-neutral AOI source-backed launch
- broad cleanup of out-of-scope direct fetch families like polish, provenance, pipeline visualization, and export links

The correct ledger state after this slice is still:

- `Stage 13 = Partial`
