# Proof Record: Thin Consumer Platformization — Round 1

Date: 2026-03-19
Program: Thin Consumer Platformization
Execution Brief: `communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`

---

## Bounded Workflows Used In The Generic Workspace Proof

The two bounded workflows proved on `AnalysisWorkspacePage`:

1. **`intellectual_genealogy`** — existing generic-route workflow
2. **`anxiety_of_influence_thematic_single_thinker`** — AOI single-thinker bounded context added in Phase 4

Both workflows route through:

- `/p/:projectId/analysis/:workflowKey`

Both consume the shared bounded-v2 consumer contract:

- `webapp/src/lib/boundedV2Client.ts`
- `webapp/src/hooks/useBoundedV2Workspace.ts`
- `webapp/src/types/boundedV2.ts`

---

## Deliverable C Artifact Reuse Evidence

### Proof Test

```
pytest tests/test_analysis_product_contract.py::test_round1_proof_record_artifact_reuse_evidence -s
```

### Exact Evidence (captured from test output)

```json
{
  "proof_test": "test_round1_proof_record_artifact_reuse_evidence",
  "job_1": "proof-round1-job-1",
  "job_2": "proof-round1-job-2",
  "shared_corpus_ref": "corp-8301438f9667672c27c27335",
  "artifact_family": "genealogy.relationship_classification",
  "slot": "Prior Work round1-proof",
  "slot_state": "ready",
  "reuse_state": "reused",
  "reused_from_job_id": "proof-round1-job-1",
  "write_guard_preserved_job_id": "proof-round1-job-1"
}
```

### What This Proves

- Job 1 (`proof-round1-job-1`) computed and stored `genealogy.relationship_classification`
- Job 2 (`proof-round1-job-2`) shares the same `corpus_ref` (same analytical situation)
- Job 2's result manifest reports `reuse_state = "reused"` and `reused_from_job_id = "proof-round1-job-1"`
- The write-side guard preserved Job 1's artifact row — Job 2's store attempt returned Job 1's row unchanged
- The freshness rule works: stale-fingerprint artifacts are excluded from reuse (proved by `test_result_manifest_slot_omits_reuse_when_fingerprint_is_stale`)

### What This Does Not Prove

- Executor-time phase skipping (Job 2 may still re-generate prose; the proof is that the stored artifact is not overwritten and the contract surfaces reuse)
- Multi-artifact or multi-slot reuse
- AOI artifact reuse
- Cross-workflow artifact reuse

---

## Exit Criterion Dispositions

### Criterion 1: AnalysisWorkspacePage is the canonical generic workspace proof for both bounded workflows

**PASS.**

Evidence:

- `AnalysisWorkspacePage.tsx` handles both `intellectual_genealogy` and `anxiety_of_influence_thematic_single_thinker` through the same generic consumption model
- AOI bounded context uses URL query params (`selected_source_thinker_id`, `selected_source_thinker_name`)
- AOI launch, discovery, and restore are all thinker-scoped on the generic route
- Automated tests: `AnalysisWorkspacePage.test.tsx` (9 tests), `AnalysisWorkspacePage.integration.test.tsx` (2 tests) — 11 tests total covering both workflows

### Criterion 2: The bounded v2 primary path no longer relies on Critic-side background polling or in-memory run authority

**PASS.**

Evidence:

- Phase 1A (authority boundary) moved lifecycle truth to analyzer-v2
- The shared bounded-v2 consumer contract calls `discoverBoundedV2Runs` and `getBoundedV2Run` against analyzer-v2 `/v1/runs/` endpoints
- Result discovery and presentation restore go through `/v1/results/` endpoints
- No Critic-side background polling registry is used in the primary bounded-v2 path
- Automated tests: `boundedV2Client.test.ts` (5 tests), `useBoundedV2Workspace.test.tsx` (12 tests)

### Criterion 3: A reusable consumer contract / host adapter exists and is used by the proving vehicle

**PASS.**

Evidence:

- The shared consumer contract lives in `webapp/src/lib/boundedV2Client.ts`, `webapp/src/hooks/useBoundedV2Workspace.ts`, `webapp/src/types/boundedV2.ts`
- Two adopters: `AnalysisWorkspacePage.tsx` and `AoiV2ThematicPanel.tsx`
- The contract owns: active-run discovery, run-by-job polling, result manifest lookup, presentation restore, refresh-presentation, cache handoff, restore-first fallback
- Automated tests: 7 suites / 33+ tests across the contract layer

### Criterion 4: genealogy.relationship_classification is reused across exactly two jobs through a real lookup path with a visible cache hit / reuse signal

**PASS.**

Evidence:

- Deterministic proof test: `test_round1_proof_record_artifact_reuse_evidence`
- Job 1: `proof-round1-job-1` — computes and stores the artifact
- Job 2: `proof-round1-job-2` — resolves the prior artifact through `corpus_ref` lookup
- Job 2 manifest: `reuse_state = "reused"`, `reused_from_job_id = "proof-round1-job-1"`
- The reuse signal appears in the result manifest (`ArtifactSlotSummary.reuse_state`, `ArtifactSlotSummary.reused_from_job_id`), not in console logs or internal traces
- Supporting tests: `test_result_manifest_slot_exposes_reuse_hit_for_same_corpus`, `test_result_manifest_slot_omits_reuse_when_fingerprint_is_stale`, `test_store_relationship_classification_preserves_source_provenance_on_reuse`

### Criterion 5: A short proof record names the two jobs, the reuse outcome, and the workspace-path success across both workflows

**PASS.** This document is that proof record.

---

## Manual Verification Dispositions

### Phase 2 manual-verification tail

**WAIVED.**

Rationale:

1. Phase 2 has 7 automated suites / 32 tests covering the shared bounded-v2 client, hook, integration mount, AOI thinker scoping, and import fallback
2. Phase 4 exercises the proving vehicle on top of the Phase 2 contract without modifying the hook or client
3. Phase 4's integration tests (`AnalysisWorkspacePage.integration.test.tsx`) exercise the full restore-first mount orchestration against real client mocks — this covers the exact behavior the Phase 2 manual check was designed to confirm
4. No new risk was introduced between Phase 2 completion and this proof record

### Phase 4 manual operator checks

**STATUS: PENDING — requires operator decision.**

The three outstanding manual checks are:

1. One generic genealogy run or restore via `AnalysisWorkspacePage` at `/p/:projectId/analysis/intellectual_genealogy`
2. One generic AOI single-thinker run or restore via the generic proof route at `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=<id>&selected_source_thinker_name=<name>`
3. One click of "Open Generic Workspace" from the bespoke AOI thinker detail page, confirming the generic route loads with the correct thinker context

These may be performed and recorded here, or explicitly waived with rationale.

---

## Automated Verification Summary

### analyzer-v2

```
pytest tests/test_analysis_product_contract.py tests/test_run_contract.py tests/test_presentation_api.py
→ 55 passed, 0 failures
```

Key new test:

```
pytest tests/test_analysis_product_contract.py::test_round1_proof_record_artifact_reuse_evidence -s
→ 1 passed, deterministic evidence captured
```

### the-critic (from Phase 4 completion memo)

```
CI=true npm test -- --watch=false \
  src/pages/AnalysisWorkspacePage.test.tsx \
  src/pages/AnalysisWorkspacePage.integration.test.tsx \
  src/pages/AnxietyOfInfluencePages.test.tsx \
  src/lib/boundedV2Client.test.ts \
  src/hooks/useBoundedV2Workspace.test.tsx
→ 5 suites passed, 33 tests passed
```

---

## Dynamic Composition Gate

The execution brief's go/no-go rule states that broader dynamic-composition work (Track 4) remains blocked until all exit criteria above are met.

Current status:

- Exit criteria 1–4: **PASS**
- Exit criterion 5: **PASS** (this document)
- Phase 4 manual checks: **PENDING** (operator decision)

Once the Phase 4 manual checks are performed or waived, all exit criteria will be satisfied and the go/no-go gate may be revisited.

---

## Files Changed In This Proof Step

- `tests/test_analysis_product_contract.py` — added one deterministic proof test function (`test_round1_proof_record_artifact_reuse_evidence`)
- `communications/PROOF_2026-03-19_thin_consumer_platformization_round1.md` — this document

No Deliverable A–D behavior was reopened.
