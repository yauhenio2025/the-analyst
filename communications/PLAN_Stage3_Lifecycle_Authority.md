# Stage 3 Implementation Plan: Lifecycle Authority and Consumer Simplification

Date: 2026-03-16

## Objective

Make `analyzer-v2` the canonical restore/state authority for all bounded v2 consumer surfaces. Delete or radically shrink the corresponding lifecycle glue in The Critic.

This plan covers three implementation phases:

| Phase | Name | Repos | Dependency |
|-------|------|-------|------------|
| 1 | Observability | analyzer-v2, analyzer-mgmt | None |
| 2 | Restore Authority | analyzer-v2, the-critic | Phase 1 (observability needed to verify) |
| 3 | Import/Refresh Simplification | the-critic | Phase 2 (restore authority must work first) |

Phase 4 (evaluation gate / next artifact seam decision) is not an implementation phase. It is a decision point after Phase 3.

---

## Current Baseline

### analyzer-v2 result contract (what exists today)

| Component | File | Lines | What It Does |
|-----------|------|-------|--------------|
| Result manifest builder | `src/analysis_products/result_contract.py` | 211-296 | Computes `AnalysisResultManifest` with result_state, staleness_reasons, product_warnings, artifact_families |
| Result presentation | `src/analysis_products/result_contract.py` | 299-328 | Returns manifest + assembled `PagePresentation` if prep is completed |
| Refresh presentation | `src/analysis_products/result_contract.py` | 331-358 | Forces re-preparation, returns fresh manifest + presentation |
| 3 API endpoints | `src/api/routes/results.py` | 26-71 | GET manifest, GET presentation, POST refresh |
| 5 schema models | `src/analysis_products/schemas.py` | 12-74 | `ArtifactSlotSummary`, `ArtifactFamilySummary`, `AnalysisResultLinks`, `AnalysisResultManifest`, `AnalysisResultPresentationResponse`, `RefreshPresentationResponse` |
| Effective plan context | `src/executor/plan_context.py` | 23-57 | Fallback chain: `plan_data` → file-backed plan → missing |

### The Critic lifecycle surfaces (what must be deleted or reduced)

| Component | File | Lines | LOC | Purpose |
|-----------|------|-------|-----|---------|
| Snapshot builder | `api/server.py` | 18220-18236 | ~17 | `_build_v2_presentation_record()` — wraps PagePresentation for DB storage |
| Snapshot save | `api/server.py` | 18239-18328 | ~90 | `_save_v2_presentation_to_db()` — inserts into `genealogy_analyses` table |
| Snapshot update | `api/server.py` | 18331-18420 | ~90 | `_update_v2_presentation_in_db()` — updates existing snapshot by v2_job_id |
| Import pipeline | `api/server.py` | 19126-19386 | ~260 | Three-stage: metadata fetch → compose/ensure → save to local DB |
| Refresh proxy | `api/server.py` | 19389-19459 | ~70 | Fetches page from v2, updates in-memory cache + DB snapshot |
| Frontend restore (genealogy) | `webapp/src/pages/GenealogyPage.tsx` | 640-676 | ~37 | Reads `_presentation` from snapshot, falls back to v2 |
| Frontend restore (AOI) | `webapp/src/components/influence/AoiV2ThematicPanel.tsx` | 320-358 | ~38 | Same snapshot-first pattern |
| Frontend restore (workspace) | `webapp/src/pages/AnalysisWorkspacePage.tsx` | 396-438 | ~42 | Same snapshot-first pattern |

**Total deletion target across all phases: ~645 LOC** (backend: ~527, frontend: ~118).

Not all will be deleted — some will be reduced to thin cache operations. But the authority shifts to analyzer-v2.

### What is NOT in scope

| Item | Why Deferred |
|------|-------------|
| Polling thread displacement | Requires upstream push mechanism (SSE/webhook) that does not exist |
| Retry/recovery orchestration | Depends on polling displacement |
| Resume flow simplification | Depends on polling displacement |
| AOI document corpus ownership | Separate prerequisite; Critic still owns `ProjectDocumentDB` |
| SDK extraction | Product layer not yet stable enough |
| analyzer-mgmt packaging elevation | Not yet the right time |
| Another genealogy artifact seam | Evaluate after lifecycle displacement |

---

## Phase 1: Observability

**Goal**: Make the analysis-product layer visible to operators without DB inspection.

**Repos**: analyzer-v2 (primary), analyzer-mgmt (bounded companion)

### 1.1 Admin API endpoints in analyzer-v2

Create `src/api/routes/admin.py` with these endpoints:

```
GET /v1/admin/artifacts/by-job/{job_id}
```
Returns: list of artifact rows for the job (family, slot, state, artifact_ref, source_output_id, created_at, updated_at). Calls `list_job_artifacts()` from `store.py:547`.

```
GET /v1/admin/corpora/by-job/{job_id}
```
Returns: corpus registration detail (corpus_ref, workflow_key, member_manifest, qualifiers). Calls `lookup_job_corpus()` from `store.py:423`.

```
GET /v1/admin/corpora/by-ref/{corpus_ref}
```
Returns: corpus detail + list of jobs sharing this corpus_ref.

```
GET /v1/admin/product-health
```
Returns: aggregate counts — total corpora, total artifacts by family, artifacts by state (ready/pending/stale/unavailable), recent registration failures (last 24h if available).

**Implementation**: These are read-only queries against `analysis_corpora` and `analysis_artifacts` tables. No new writes. The store already has most of the query logic; this is mostly routing.

**Register in `src/api/main.py`**: Add `admin_router` alongside existing routers.

### 1.2 Structured logging for artifact lifecycle

In `src/analysis_products/store.py`, upgrade existing `logger.warning()` calls on artifact write failures to structured log events:

```python
logger.info("artifact_write", extra={
    "event": "artifact_write",
    "job_id": job_id,
    "family": family,
    "slot": slot,
    "status": "success" | "failed",
    "error": str(e) if failed,
})
```

Same for corpus registration in `register_job_corpus()` (store.py:354) and `ensure_job_corpus()` (store.py:402).

### 1.3 Expand /health endpoint

In `src/api/main.py:320-360`, add to the health response:

```python
"analysis_products": {
    "corpora_count": <int>,
    "artifacts_count": <int>,
    "artifacts_ready": <int>,
}
```

This requires one lightweight DB query. Keep it fast (no aggregation by family).

### 1.4 Bounded analyzer-mgmt integration

In `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/jobs/[id].tsx`:

Add a new tab or section: "Analysis Product". When expanded:

1. Call `GET ${ANALYZER_V2_URL}/v1/results/by-job/${jobId}` (direct fetch, not through mgmt-api)
2. Display: `result_state`, `artifacts_ready`, `staleness_reasons`, `product_warnings`
3. Display: artifact family table (family, state, ready/pending/stale/unavailable slot counts)
4. Add a "Refresh Presentation" button that calls `POST ${ANALYZER_V2_URL}/v1/results/by-job/${jobId}/refresh-presentation`

This is ~200 lines of React. No mgmt-api backend changes needed.

Add TypeScript types to `frontend/src/types/index.ts`:
- `AnalysisResultManifest` (mirror the Pydantic model)
- `ArtifactFamilySummary`
- `ArtifactSlotSummary`

### Phase 1 Verification

- [ ] `GET /v1/admin/artifacts/by-job/{job_id}` returns artifact rows for a real completed job
- [ ] `GET /v1/admin/corpora/by-job/{job_id}` returns corpus detail
- [ ] `GET /v1/admin/product-health` returns aggregate counts
- [ ] `GET /health` includes `analysis_products` section
- [ ] Structured log events appear in server output for artifact writes
- [ ] analyzer-mgmt job page shows artifact families and result state
- [ ] analyzer-mgmt "Refresh Presentation" button triggers refresh and updates display

---

## Phase 2: Restore Authority

**Goal**: Make `analyzer-v2` the primary restore source for all three bounded v2 surfaces. Demote Critic snapshot to fallback cache.

**Repos**: analyzer-v2 (contract expansion), the-critic (consumer switchover)

### 2.1 Expand result presentation response

The current `get_result_presentation()` (result_contract.py:299-328) returns `PagePresentation` only when `presentation_status == "completed"`. This is correct.

But the consumer needs to know: **should I use this as my restore source, or fall back to local snapshot?**

Add to `AnalysisResultManifest` in `schemas.py`:

```python
restore_available: bool  # True if presentation is assembled and servable
restore_reason: Optional[str]  # Why restore is/isn't available
```

Compute in `build_result_manifest()`:
- `restore_available = True` if: presentation_status == "completed" AND result_state in ("ready", "stale")
- `restore_available = False` if: presentation not prepared, or job failed
- `restore_reason`: one of "presentation_ready", "preparation_not_run", "preparation_failed", "job_failed"

This gives consumers a clear signal: "ask me for the page" vs "use your cache."

### 2.2 Complete AOI and workspace switchover to /v1/results/* endpoints

**Current state**: Only `GenealogyPage.tsx` uses `/v1/results/by-job/{v2JobId}`. AOI and workspace still use presenter status + Critic refresh proxy.

**Target state**: All three surfaces use `/v1/results/by-job/{v2JobId}` for freshness and `/v1/results/by-job/{v2JobId}/presentation` for restore.

#### GenealogyPage.tsx (already done — verify only)

Lines 548-626: Already calls `/v1/results/by-job/{v2JobId}` for freshness. Verify `restore_available` is consumed.

#### AoiV2ThematicPanel.tsx

**Current** (lines 320-358): Reads from Critic snapshot first, falls back to v2 presenter page.

**Change to**:
1. Call `GET ${ANALYZER_V2_URL}/v1/results/by-job/${v2JobId}` to get manifest
2. If `manifest.restore_available`: call `GET ${ANALYZER_V2_URL}/v1/results/by-job/${v2JobId}/presentation` to get `PagePresentation`
3. If not available: fall back to Critic snapshot (existing path)
4. For freshness: use `manifest.presentation_content_hash` comparison
5. For refresh: call `POST ${ANALYZER_V2_URL}/v1/results/by-job/${v2JobId}/refresh-presentation`

#### AnalysisWorkspacePage.tsx

**Current** (lines 396-438): Same Critic-snapshot-first pattern.

**Same change as AOI**: v2 result presentation first, Critic snapshot as fallback.

### 2.3 Demote Critic snapshot persistence to cache-only

After Phase 2.2, the three frontend surfaces prefer v2 as restore source. The Critic's snapshot persistence should change from "primary store" to "offline cache."

**In `api/server.py`**:

The callers of `_save_v2_presentation_to_db()` are at lines:
- 18030-18038 (after job completion)
- 19077-19085 (after resume completion)
- 19369-19377 (after import compose)
- 19442-19450 (during refresh fallback)

These callers should remain — they still write the cache. But their semantics change:

1. Add a comment or log line marking these as cache writes, not primary persistence
2. The `_build_v2_presentation_record()` function (18220-18236) should add a `_cached_at` timestamp so the frontend can distinguish "fresh v2 restore" from "stale cache restore"

**No deletions in this phase.** The snapshot functions stay. What changes is that the frontend prefers v2 and treats the snapshot as fallback.

### 2.4 Add `stale_snapshot_warning` to frontend restore path

When the frontend falls back to Critic snapshot (because v2 restore is unavailable), it should display a visible indicator:

- "Showing cached result — server restore unavailable"

This makes the authority boundary visible to users, not just developers.

### Phase 2 Verification

- [ ] `AnalysisResultManifest` includes `restore_available` and `restore_reason`
- [ ] AoiV2ThematicPanel.tsx calls `/v1/results/by-job/{v2JobId}` for manifest + presentation
- [ ] AnalysisWorkspacePage.tsx calls `/v1/results/by-job/{v2JobId}` for manifest + presentation
- [ ] All three surfaces prefer v2 restore when `restore_available == true`
- [ ] All three surfaces fall back to Critic snapshot when `restore_available == false`
- [ ] Stale snapshot warning is visible when using cache fallback
- [ ] GenealogyPage.tsx still works (regression check)
- [ ] Fresh job: v2 restore path is used, no snapshot dependency
- [ ] Imported legacy job: snapshot fallback is used, warning is shown
- [ ] `npx tsc --noEmit` in the-critic/webapp passes
- [ ] `pytest tests/test_analysis_product_contract.py tests/test_presentation_api.py` passes

---

## Phase 3: Import/Refresh Simplification

**Goal**: Reduce Critic import and refresh glue now that v2 is the restore authority.

**Repo**: the-critic (primary), analyzer-v2 (minor)

**Prerequisite**: Phase 2 must be verified. The frontend must be confirmed working with v2 as restore source.

### 3.1 Simplify refresh proxy

**Current** (`server.py:19389-19459`):
1. GET `/v1/presenter/page/{v2_job_id}` from v2
2. Update `_GENEALOGY_JOBS` in-memory dict
3. Update DB snapshot via `_update_v2_presentation_in_db()`

**After Phase 2**: The frontend calls v2 refresh directly. The Critic proxy is only needed for:
- Updating the in-memory `_GENEALOGY_JOBS` cache (for the current server process)
- Updating the DB snapshot cache

**Change**: Reduce the refresh proxy to a thin cache-invalidation endpoint:

```python
@app.post("/api/genealogy/refresh-v2/{v2_job_id}")
def refresh_v2(v2_job_id: str):
    """Invalidate local cache after frontend triggers v2 refresh directly."""
    # Invalidate in-memory cache
    for job_id, job_data in _GENEALOGY_JOBS.items():
        if job_data.get("v2_job_id") == v2_job_id:
            job_data.pop("result", None)
            break
    # Optionally update DB snapshot from v2
    # (or just mark it stale and let next read refresh)
    return {"status": "cache_invalidated"}
```

This reduces `server.py:19389-19459` (~70 LOC) to ~15 LOC.

The generic wrapper at line 19945-19948 simplifies accordingly.

### 3.2 Simplify import pipeline

**Current** (`server.py:19126-19386`):
1. Fetch v2 job metadata (60s timeout)
2. Conditional compose: ensure + background wait OR compose OR direct page fetch
3. Create in-memory job entry
4. Save full PagePresentation to `genealogy_analyses` DB

**After Phase 2**: Since v2 is now the restore authority, the import pipeline does not need to persist the full PagePresentation locally. It only needs to:
1. Verify the v2 job exists and is completed
2. Trigger presentation preparation on v2 if not already done
3. Register the v2 job in the Critic's local job tracking (so the frontend can find it)
4. Optionally cache the snapshot (for offline/fast restore)

**Change**: Replace the compose-then-save-locally pipeline with:

```python
@app.post("/api/genealogy/import-v2/{v2_job_id}")
def import_v2(v2_job_id: str, ...):
    # 1. Verify job exists and is completed
    job_meta = analyzer_v2_client.get_job_sync(v2_job_id)
    if job_meta["status"] != "completed":
        return error("Job not completed")

    # 2. Ensure presentation is prepared (trigger if needed)
    result = analyzer_v2_client.get_result_presentation(v2_job_id)
    if not result["manifest"]["restore_available"]:
        # Trigger preparation
        analyzer_v2_client.refresh_presentation(v2_job_id)
        result = analyzer_v2_client.get_result_presentation(v2_job_id)

    # 3. Register in local tracking
    job_id = f"genealogy-imported-{...}"
    _GENEALOGY_JOBS[job_id] = {
        "v2_job_id": v2_job_id,
        "v2_plan_id": job_meta.get("plan_id"),
        "output_mode": "v2_presentation",
        "status": "completed",
    }

    # 4. Cache snapshot (reduced: just the manifest reference, not full presentation)
    _save_v2_import_reference_to_db(project_id, v2_job_id, job_meta)

    return {"job_id": job_id, "v2_job_id": v2_job_id, "status": "imported"}
```

This reduces `server.py:19126-19386` (~260 LOC) to ~60 LOC.

The key difference: the Critic no longer persists the full `PagePresentation` blob on import. It stores only enough metadata to find the v2 job later. The actual restore comes from v2.

### 3.3 Add result-presentation endpoint to analyzer_v2_client

In `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_client.py`, add:

```python
def get_result_manifest_sync(self, job_id: str, consumer_key: str = "the-critic") -> dict:
    """GET /v1/results/by-job/{job_id}"""
    ...

def get_result_presentation_sync(self, job_id: str, consumer_key: str = "the-critic") -> dict:
    """GET /v1/results/by-job/{job_id}/presentation"""
    ...

def refresh_result_presentation_sync(self, job_id: str, consumer_key: str = "the-critic") -> dict:
    """POST /v1/results/by-job/{job_id}/refresh-presentation"""
    ...
```

These are thin HTTP wrappers (~40 LOC total).

### 3.4 Update completion handler to use result contract

**Current** (`server.py:18022-18038`): After v2 job completion, calls `_save_v2_presentation_to_db()` with full PagePresentation.

**Change**: After completion, verify result is available via manifest instead of fetching + persisting full presentation:

```python
# After job completion:
manifest = analyzer_v2_client.get_result_manifest_sync(v2_job_id)
if manifest.get("restore_available"):
    # v2 has the result — just note the reference locally
    _save_v2_import_reference_to_db(project_id, v2_job_id, manifest)
else:
    # Fallback: trigger preparation and cache snapshot (existing behavior)
    ...
```

### Phase 3 Verification

- [ ] Refresh proxy reduced to cache invalidation (~15 LOC vs ~70)
- [ ] Import pipeline reduced to verify + register + reference (~60 LOC vs ~260)
- [ ] Import works for new completed v2 jobs (uses v2 restore)
- [ ] Import works for legacy jobs without preparation (triggers preparation, then uses v2 restore)
- [ ] Frontend still loads correctly after import (v2 is restore source)
- [ ] Frontend still loads correctly after refresh (v2 is refresh source)
- [ ] Stale/legacy imported jobs show cache fallback warning
- [ ] `npx tsc --noEmit` in the-critic/webapp passes
- [ ] Manual test: run genealogy analysis → complete → view page → refresh → verify v2 is restore source
- [ ] Manual test: import a completed v2 job → verify page loads from v2

---

## Phase 4: Evaluation Gate

After Phases 1-3 are verified, answer these questions before proceeding:

1. **Is the Critic measurably thinner?** Count remaining lifecycle LOC. Target: snapshot/import/refresh surfaces reduced by ~400 LOC.
2. **Is v2 restore reliable?** Check: how many real jobs have `restore_available == true`? Any systematic failures?
3. **Are there new bottlenecks?** Does v2 restore add noticeable latency vs Critic snapshot restore? (v2 must assemble PagePresentation on read; snapshot is pre-assembled.)
4. **Is the next highest-leverage move another lifecycle cycle or an artifact seam?**
   - If Critic still carries too much lifecycle glue → plan Cycle 2 (recovery/resume simplification, requires SSE/webhook prerequisite)
   - If lifecycle is manageable → consider `genealogy_per_work_scan` artifact seam
5. **Should polling displacement be planned?** This requires an upstream push mechanism. Scope it as a separate future stage if deemed worthwhile.

---

## Cross-Phase Dependencies

```
Phase 1 (Observability)
    │
    ▼
Phase 2 (Restore Authority)
    │  ← Observability endpoints needed to verify restore is working
    ▼
Phase 3 (Import/Refresh Simplification)
    │  ← Restore authority must be verified before simplifying import
    ▼
Phase 4 (Evaluation Gate)
```

Phases 1 and 2 have some internal parallelism:
- Phase 1.1-1.3 (analyzer-v2 admin endpoints) and Phase 2.1 (schema expansion) can be done concurrently
- Phase 1.4 (analyzer-mgmt integration) can run in parallel with Phase 2 analyzer-v2 work
- Phase 2.2 (frontend switchover in the-critic) depends on Phase 2.1 (schema expansion in analyzer-v2)

---

## Files Changed Summary

### analyzer-v2

| File | Change |
|------|--------|
| `src/api/routes/admin.py` | **NEW** — 4 admin endpoints (~120 LOC) |
| `src/api/main.py` | Register admin router, expand /health |
| `src/analysis_products/schemas.py` | Add `restore_available`, `restore_reason` to manifest |
| `src/analysis_products/result_contract.py` | Compute restore_available in build_result_manifest() |
| `src/analysis_products/store.py` | Add structured log events, add query for corpora-by-ref |

### the-critic

| File | Change |
|------|--------|
| `webapp/src/pages/GenealogyPage.tsx` | Verify + minor: consume `restore_available` |
| `webapp/src/components/influence/AoiV2ThematicPanel.tsx` | **MAJOR**: Switch from snapshot-first to v2-result-first restore |
| `webapp/src/pages/AnalysisWorkspacePage.tsx` | **MAJOR**: Switch from snapshot-first to v2-result-first restore |
| `analyzer/concept_analyzer/analyzer_v2_client.py` | Add 3 result contract methods (~40 LOC) |
| `api/server.py` | Reduce refresh proxy (~70→15 LOC), reduce import pipeline (~260→60 LOC), update completion handler |

### analyzer-mgmt

| File | Change |
|------|--------|
| `frontend/src/pages/jobs/[id].tsx` | Add analysis product tab (~200 LOC) |
| `frontend/src/types/index.ts` | Add result manifest types (~30 LOC) |

---

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| v2 restore adds latency vs snapshot | Medium | PagePresentation is already cached in presentation_cache; assembly is fast for completed jobs |
| Legacy imported jobs have no v2 restore | Certain | Snapshot fallback remains for these; stale_snapshot_warning makes it visible |
| Concurrent users see different restore sources during rollout | Low | Phase 2 is all-or-nothing per surface; no partial switchover |
| analyzer-v2 down during restore | Low | Snapshot fallback kicks in automatically; already the current behavior |
| Import pipeline simplification breaks compound workflows | Low | Verify with both genealogy and AOI imports before merging |

---

## Success Criteria

Stage 3 is complete when:

1. All three frontend surfaces prefer v2 as restore source
2. Critic snapshot persistence is demoted to cache-only
3. Import pipeline no longer persists full PagePresentation locally
4. Refresh proxying is reduced to cache invalidation
5. Operators can inspect artifact/corpus state via admin endpoints + analyzer-mgmt
6. **Net Critic lifecycle LOC reduction: ~400 lines**
7. All existing tests pass + new regression coverage for restore path
