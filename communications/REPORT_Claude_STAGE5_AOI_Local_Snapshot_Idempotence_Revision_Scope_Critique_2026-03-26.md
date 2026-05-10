# Critique: Stage 5 AOI Local Snapshot Idempotence Revision Scope

Date: 2026-03-26
Reviewer: Claude (Opus 4.6, 1M context)
Reviewed document: `communications/MEMO_2026-03-26_stage5_aoi_local_snapshot_idempotence_revision_scope.md`
Verdict: **Approve after revision**

## Verdict Summary

The seam diagnosis is technically correct. The scope is appropriately bounded. The roadmap claims are honest. But the memo prescribes idempotence behaviors that already exist in the codebase and already failed. The root cause is a concurrency gap in the sync/async database session split, not a missing idempotence check. Revisions are needed before implementation to avoid rebuilding the same pattern that already proved insufficient.

---

## Findings (ordered by severity)

### Finding 1 (HIGH): The canonical resolution logic already exists and already failed

The memo prescribes making completed-job backfill, cache-v2, and refresh idempotent. But the codebase already implements this:

- `_resolve_canonical_local_snapshot_analysis_id` (`server.py:19182-19237`) checks `run_ref.local_snapshot_analysis_id` first, validates it resolves via `_load_saved_v2_snapshot_result`, then falls back to `_find_canonical_saved_v2_snapshot` which queries `genealogy_analyses` for existing rows matching `(project_id, workflow_key, v2_job_id, thinker)`.
- `cache_v2_presentation` (`server.py:20625-20638`) calls `_resolve_canonical_local_snapshot_analysis_id` before calling `_save_v2_presentation_to_db`. It only inserts when `canonical_analysis_id` is falsy.
- `_best_effort_ensure_local_snapshot_analysis_id` (`server.py:19308-19321`) calls `_resolve_canonical_local_snapshot_analysis_id` and returns early if a canonical row is found. Only proceeds to insert when no canonical exists.
- `refresh_v2_presentation` (`server.py:20512-20557`) resolves canonical first, tries `_update_v2_presentation_in_db` with the canonical `analysis_id`, and only falls back to `_save_v2_presentation_to_db` when the update returns 0 rows.
- `_collapse_saved_results_for_listing` (`server.py:18642-18684`) already collapses duplicate AOI rows per `v2_job_id` using `_select_canonical_saved_v2_snapshot` when serving the results listing.
- The frontend (`AoiV2ThematicPanel.tsx:448-453`) also collapses duplicates client-side via `collapsedLocalByIdentity` keyed by `v2_job_id`.

Despite all of this, 81 duplicate rows were created and 34 cache-v2 responses in one session returned different `analysis_id`s. **The memo needs to explain why the existing logic failed**, not just prescribe the same behavior as a new requirement. Without this diagnosis, the implementor risks rebuilding the same pattern.

### Finding 2 (HIGH): The root cause is a concurrency gap in the sync/async session split

`_save_v2_presentation_to_db` (`server.py:19396-19534`) always generates a fresh UUID on line 19418:
```python
analysis_id = f"gen-v2-{uuid.uuid4().hex[:12]}"
```

Critically, it uses a **separate synchronous database connection** (`psycopg2.connect` or `sqlite3.connect`, lines 19440-19445) that is completely decoupled from the async SQLAlchemy session used by `_resolve_canonical_local_snapshot_analysis_id`. The async session queries via `select(GenealogyAnalysisDB)` while the sync connection inserts via raw SQL `INSERT INTO genealogy_analyses`. These are different database connections with different transaction scopes.

The failure mode:

1. Request A opens async session, calls `_resolve_canonical_local_snapshot_analysis_id` -> finds no canonical (no rows yet)
2. Request B opens async session, calls `_resolve_canonical_local_snapshot_analysis_id` -> same result (no rows yet, or A's sync insert not yet committed/visible)
3. Request A calls `_save_v2_presentation_to_db` which opens sync connection, generates `gen-v2-aaa`, inserts, commits sync connection
4. Request B calls `_save_v2_presentation_to_db` which opens sync connection, generates `gen-v2-bbb`, inserts, commits sync connection
5. Both then update `run_ref.local_snapshot_analysis_id` via their respective async sessions; last commit wins

The proof evidence confirms this pattern exactly: 34 concurrent `cache-v2` calls all saw no canonical and each created a new row.

The memo should identify this root cause explicitly and prescribe a fix at the right level. Options:
- **(a)** Make `_save_v2_presentation_to_db` check-before-insert within its own sync connection (look for existing row with matching `v2_job_id` before inserting)
- **(b)** Use `v2_run_references.local_snapshot_analysis_id` (which has a unique constraint on `v2_job_id`) as the serialization point: if it already points to a valid row, return early before ever reaching `_save_v2_presentation_to_db`
- **(c)** Add a database-level uniqueness constraint on a materialized `v2_job_id` column in `genealogy_analyses` (strongest but requires migration)

Option (b) is most natural: the `v2_run_references` table already has `UNIQUE(v2_job_id)` and already stores `local_snapshot_analysis_id`. Making it the single gatekeeper would align all three write paths through one serialization point without touching the `genealogy_analyses` schema.

### Finding 3 (MEDIUM): The memo does not address the existing 81 duplicate rows

After the idempotence fix, the 81 existing rows in `genealogy_analyses` with `pass_results._v2_job_id = job-6ee8b0621177` remain. The existing `_find_canonical_saved_v2_snapshot` will pick one via `_select_canonical_saved_v2_snapshot` (`server.py:18608-18629`) using a `max()` with a preference key, so canonical selection should work.

However:
- `_saved_v2_snapshot_has_conflicting_thinkers` (`server.py:18632-18639`) checks whether multiple thinker IDs appear across the group. If any of the 81 rows have inconsistent thinker identity (e.g., from race-condition backfills that didn't populate `selected_source_thinker_id`), this check could return True, causing `_collapse_saved_results_for_listing` to expose all 81 rows instead of one (line 18662).
- The saved-results query scans and processes 81 rows per listing request even though only one is needed.

The memo should either:
- Authorize a one-time cleanup of non-canonical duplicate rows for this `v2_job_id`, or
- Confirm that the existing collapse logic handles 81 candidates correctly and document why cleanup is not necessary for the browser closeout

### Finding 4 (MEDIUM): Frontend cache-v2 call frequency amplifies the concurrency bug

The `warmSnapshotForSource` callback (`AoiV2ThematicPanel.tsx:544-569`) correctly checks `source.analysis_id` before firing cache-v2 (line 545-546). But during panel hydration:

1. `hydratePanel` effect (line 830-866) calls `loadSavedResults({ autoLoadLatest: true })`
2. `loadSavedResults` (line 517-518) calls `loadSelection(mergedResults[0])` for auto-load
3. `loadSelection` (line 421) calls `loadBoundedV2SavedResult` which fetches the result from the local API

The `loadBoundedV2SavedResult` call goes through the Critic API which may trigger `_best_effort_ensure_local_snapshot_analysis_id` on the job-detail path. Meanwhile, if the user clicks a saved result, `warmSnapshotForSource` fires another cache-v2 call. React re-renders, dependency-array changes, or Strict Mode double-effects could multiply these calls.

The memo acknowledges that "34 successful cache-v2 responses" occurred in a single session but does not address the frontend behavior that produces them. The backend fix should make concurrent calls safe, but the memo should note whether any frontend-side request deduplication is also needed (e.g., an in-flight guard on `warmSnapshotForSource` to prevent overlapping cache-v2 calls for the same `v2_job_id`).

### Finding 5 (LOW): The `_update_v2_presentation_in_db` LIKE-based query is fragile

When `canonical_analysis_id` is None, `_update_v2_presentation_in_db` (`server.py:19577-19584`) falls back to a `LIKE '%{v2_job_id}%'` scan against `pass_results`. With 81 matching rows, this may update only one (via `LIMIT 1` in the preceding SELECT used to build the update payload) while leaving 80 stale.

The memo's Decision 4 (refresh should update the canonical row) implicitly requires targeting by `analysis_id`, not LIKE-scanning JSON. If the fix routes all paths through `v2_run_references.local_snapshot_analysis_id` as the canonical pointer (per Finding 2's recommendation), the refresh path would always have a concrete `analysis_id` to target, making the LIKE fallback unnecessary.

### Finding 6 (LOW): `run_ref.local_snapshot_analysis_id` update races are harmless only if all writers agree

Multiple code paths update `run_ref.local_snapshot_analysis_id`:
- `_best_effort_ensure_local_snapshot_analysis_id` (line 19368)
- `cache_v2_presentation` (line 20655)
- `refresh_v2_presentation` (line 20547)
- `_resolve_canonical_local_snapshot_analysis_id` (line 19235)

If the fix ensures all paths converge on the same canonical `analysis_id` for a given `v2_job_id`, last-write-wins is harmless because all writers agree. The memo should note this invariant explicitly: after the fix, all code paths must resolve to the same canonical `analysis_id` for a given `v2_job_id`, not just "some valid" `analysis_id`.

---

## Direct Answers to Review Questions

### 1. Is the memo right that the new blocker is host-local identity churn rather than another planner/compose or analyzer seam?

**Yes.** The proof evidence is unambiguous:
- Upstream `v2_job_id = job-6ee8b0621177` is stable throughout
- The `analysis_id` drifts from `gen-v2-18853b558ef1` to `gen-v2-6849427079a1` to `gen-v2-9e3e5ad74dbb` across reads for the same upstream job
- 81 local rows exist for one upstream run; 34 cache responses returned different ids in one session
- No planner, compose, or analyzer seam is implicated
- The completed-job detail route (`server.py:20200-20209`) and cache-v2 route (`server.py:20640`) are the two paths that create new rows

### 2. Does the codebase support the memo's proposed fix surface?

**Yes, but with an important qualification.** The fix surface (completed-job backfill, cache-v2, refresh, saved-results listing) is correct. The codebase already has idempotence logic for all four paths. The issue is not that the idempotence logic is absent but that it fails under concurrent request execution due to the sync/async session split. The memo needs to prescribe a fix at the concurrency/connection level.

Specifically:
- **Idempotent completed-job backfill**: Logic exists at `server.py:19308-19321`. Fails under concurrency.
- **Idempotent cache-v2 reuse**: Logic exists at `server.py:20625-20652`. Fails under concurrency.
- **Refresh updating canonical row**: Logic exists at `server.py:20512-20557`. Works when `analysis_id` is provided to `_update_v2_presentation_in_db`.
- **Collapsed saved-results**: Logic exists at `server.py:18642-18684` (server-side) and `AoiV2ThematicPanel.tsx:448-453` (client-side). Works correctly.

### 3. Is collapsing the AOI-facing saved-results list to one canonical row per upstream v2_job_id the right repair, or does that risk masking unresolved truth problems?

**It is the right repair.** Multiple local rows for the same upstream `v2_job_id` are genuinely mechanical duplicates, not meaningful analytical variants. They all carry the same `_v2_job_id`, the same presentation payload (or near-identical timing variants fetched from the same immutable upstream manifest), and the same project context. The duplication is a mechanical artifact of concurrent requests all passing the canonical check simultaneously, not a signal of distinct analytical results.

The only masking risk would be if different cache calls captured materially different presentation states. In practice, the cached presentation comes from the same upstream result manifest, which is immutable once `result_state = ready`. So collapsing is safe and correct.

### 4. Is keeping job-6ee8b0621177 as the fixed counted source still the right operational choice?

**Yes.** The upstream run is real, completed, and recovered to ready state. The bug is entirely host-local. Using a different run would reproduce the same concurrency problem on a different identity without adding diagnostic value.

The memo is not "too brittle by freezing that source" - it is correctly isolating the test variable to the host-local idempotence repair.

### 5. Does the memo under-specify hazards?

**Yes**, in five areas:
- **Root cause undiagnosed**: The sync/async session split is the specific architectural gap. (Finding 2)
- **Existing duplicate rows**: 81 pre-existing orphans not addressed. (Finding 3)
- **Frontend request frequency**: 34 concurrent cache-v2 calls in one session amplify the backend bug. (Finding 4)
- **LIKE-based update fragility**: Refresh may update wrong row among 81 candidates. (Finding 5)
- **Auto-loaded presentation after dedup**: After the fix, the auto-loaded row will consistently be the canonical row. The memo says auto-loaded state does not count as row pinning. This is correct, but the operator discipline ("clear, expose list, explicitly click") may feel trivially satisfied when the auto-loaded row happens to be the only row. The memo should clarify that explicit pin discipline requires a deliberate user action even when the canonical row is the only available row.

### 6. Is this slice narrow enough to keep roadmap order honest?

**Yes.** The slice correctly:
- Keeps the Stage 5 seam gate as already passed on the frozen fixture-backed pack
- Keeps Stage 2 open until the browser closeout succeeds on the recovered source
- Keeps Tranche 3 blocked
- Does not reopen planner, compose, or analyzer seams
- Does not consume the frozen four-case pack again
- Does not launch a new AOI run

### 7. Is the step appropriately bounded, or is it still smuggling in broader closure by implication?

**Appropriately bounded.** The memo explicitly separates:
1. Fix the host seam (this slice)
2. Re-attempt browser closeout (after the fix)
3. Write Stage 2 decision (after the re-attempt)

There is no implicit closure smuggling. The acceptance criteria honestly state that the fix alone does not constitute Stage 2 closure.

---

## Recommended Memo Revisions Before Implementation

1. **Add a root cause section** identifying the concurrency gap between async canonical resolution and sync row insertion as the reason the existing idempotence logic failed. Without this, the implementor may rebuild the same check-then-insert pattern that already proved insufficient.

2. **Add a Decision 2a (serialization strategy)**: Specify that `v2_run_references` should serve as the serialization point for idempotence. All three write paths should check `run_ref.local_snapshot_analysis_id` first (via the existing async session), validate that the pointed-to `genealogy_analyses` row still exists, and only proceed to `_save_v2_presentation_to_db` if no valid mapping exists. Additionally, `_save_v2_presentation_to_db` should itself check for an existing row with matching `v2_job_id` within its sync connection before generating a new UUID, as a belt-and-suspenders guard against the remaining concurrency window.

3. **Add a sub-decision to Decision 5 on existing orphan handling**: Either (a) authorize a one-time cleanup of non-canonical duplicate rows for `job-6ee8b0621177` before the re-closeout attempt, or (b) specify that the existing `_collapse_saved_results_for_listing` logic is sufficient and that the 81 orphans are accepted as dead data.

4. **Refine Decision 4**: Specify that refresh should target the canonical row by `analysis_id` from `v2_run_references.local_snapshot_analysis_id`, not by LIKE-scanning JSON. This makes the refresh path consistent with the serialization strategy.

5. **Add a note on concurrent request handling**: Acknowledge that the browser session generated 34 concurrent cache-v2 calls and specify that the fix must handle this concurrency. Note whether frontend-side request deduplication (e.g., an in-flight guard on `warmSnapshotForSource`) is in scope or explicitly deferred.
