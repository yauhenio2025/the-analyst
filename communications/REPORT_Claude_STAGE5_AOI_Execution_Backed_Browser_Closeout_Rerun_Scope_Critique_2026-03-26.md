# Critique: Stage 5 AOI Execution-Backed Browser Closeout Rerun Scope

Date: 2026-03-26
Reviewer: Claude (Opus 4.6)
Document under review: `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_scope.md`

## Verdict: Approve

The memo is technically sound, well-bounded, and honest about what it is and is not.

The codebase now actually supports the assumptions the memo makes. The rerun is the right next step.

---

## Findings (by severity)

### Finding 1: Job-detail route as identity passthrough (Low severity, requires verification)

The route handler at `the-critic/api/server.py:21389-21392`:

```python
@app.get("/api/analysis/{workflow_key}/jobs/{job_id}")
async def get_analysis_job(workflow_key: str, job_id: str):
    return await get_genealogy_job(job_id)
```

This is a pure passthrough that ignores `workflow_key` and delegates to `get_genealogy_job(job_id)`. The completion memo claims "completed-job detail reads now converge on one canonical local snapshot path," but the route handler itself has no `v2_run_references` interaction.

The repair must live inside `get_genealogy_job()` rather than the route handler. The completion memo's test suite (51 passed) gives reasonable confidence this is the case, but the rerun should verify empirically: the preflight job-detail read must return the same `analysis_id` as `v2_run_references.local_snapshot_analysis_id`. The pre-repair proof showed these diverging (`gen-v2-6849427079a1` from job detail vs `gen-v2-18853b558ef1` from saved-result detail). After the repair, they must agree.

**Recommendation**: The rerun's preflight identity artifact (Decision 5) already requires cross-linking job-detail and saved-result-detail identity. This is sufficient to catch the problem if it persists. No memo revision needed.

### Finding 2: 81 orphan `genealogy_analyses` rows remain in the DB (Low severity, acknowledged)

The closeout revision memo recorded 81 rows with `pass_results._v2_job_id = job-6ee8b0621177` in `genealogy_analyses`. The idempotence completion memo explicitly states these are left in place but made "inert" for canonical identity, results listing, and counted browser proof.

The listing collapse logic at `server.py:20956-20978` uses `_load_preferred_saved_result_ids_for_listing` (lines 18714-18730) to query `v2_run_references.local_snapshot_analysis_id` and then `_collapse_saved_results_for_listing` to select only the canonical row per `v2_job_id`. This should suppress the orphans from the panel's saved-results list.

**Residual risk**: If a future code path reads `genealogy_analyses` directly without going through collapse, it could surface an orphan. The memo's scope excludes cleanup, which is defensible for a rerun scope, but the orphans should be addressed eventually.

**Recommendation**: No revision needed. The memo's deliverable 1 (pre-compose row-pin artifact) will prove whether orphan rows leak into the panel listing.

### Finding 3: Frontend has no client-side dedup for cache-v2 calls (Low severity, mitigated)

`boundedV2Client.ts` at the `cacheBoundedV2Presentation` function (lines 233-271) makes a POST to the cache-v2 route with no client-side deduplication. If the panel triggers multiple warmup calls during the counted path, each one fires independently.

However, the backend now handles this correctly:
- `_get_or_create_locked_v2_run_reference` (lines 18855-18996) uses `BEGIN IMMEDIATE` (SQLite) / `INSERT ON CONFLICT DO NOTHING` + `FOR UPDATE` (Postgres) for proper serialization
- `_ensure_canonical_v2_local_snapshot` (lines 19618-19697) reuses existing canonical row when `run_ref.local_snapshot_analysis_id` is populated
- Test `test_cache_v2_presentation_generic_concurrent_calls_converge_on_one_canonical_snapshot` (lines 1035-1089) spawns 8 concurrent calls and verifies exactly 1 canonical row

The frontend `warmSnapshotForSource` (lines 546-571) also has a fast-path: if `source.analysis_id` already exists, it returns immediately without calling cache-v2 at all (line 548).

**Recommendation**: No revision needed. The backend serialization is proven.

### Finding 4: Transient compose path omits `source_v2_job_id` (Informational, not in scope)

In `AoiV2ThematicPanel.tsx`, `handleTransientComposeLaunch` (lines 744-811) does not add `source_v2_job_id` to the compose URL params, while the planner-backed `launchPlannerBackedCompose` (lines 672-742) does (line 695).

This does not affect the rerun because the memo explicitly requires the planner-backed path (Decision 3: "No profile/autostart path may count"). The transient compose path is not the counted path.

**Recommendation**: No revision needed. Flag for future cleanup but not a rerun hazard.

### Finding 5: Content-level `_v2_job_id` inside the result payload is not explicitly verified (Informational)

The memo requires that `source_v2_job_id = job-6ee8b0621177` is preserved through the counted path. The pre-compose identity bundle (Decision 5) checks this at the URL/query level. But the memo does not require explicit verification that the `pass_results._v2_job_id` field inside the returned saved-result payload also stays `job-6ee8b0621177`.

The proof artifacts confirm this held during the first (failed) attempt: the saved-result detail in the precompose pin artifact shows `pass_results._v2_job_id = job-6ee8b0621177`. The repair did not touch the content payload, so this should persist.

**Recommendation**: No revision needed. The existing artifact requirements are sufficient; `_v2_job_id` inside the payload is set at creation time and not modified by the idempotence repair.

---

## Direct Answers to the Seven Questions

### 1. Is the memo right that the next step is now a rerun, not another repair tranche?

**Yes.**

The idempotence repair is landed and verified:
- 51 backend tests passed (including concurrent convergence tests)
- 73 frontend tests passed (including Clear-then-reselect and planner invalidation)
- TypeScript compiles clean

The codebase now supports stable local snapshot identity through `v2_run_references` as serialization point, with proper locking (SQLite: `BEGIN IMMEDIATE`, Postgres: `FOR UPDATE`). The canonical resolution chain (`_get_or_create_locked_v2_run_reference` -> `_ensure_canonical_v2_local_snapshot`) prevents the duplicate-minting seam that caused the first attempt to fail.

No further code changes are authorized up front, which is appropriate. The memo's stop-and-revise rules (Decision 8) are explicit and reasonable.

### 2. Is the counted-source identity rule technically sound?

**Yes, with one verification caveat.**

The rule (Decision 2) is:
1. Anchor on `source_v2_job_id = job-6ee8b0621177`
2. Resolve current canonical local `source_analysis_id` at preflight
3. Preserve that resolved id through the counted path

This is technically correct because:
- `v2_run_references.local_snapshot_analysis_id` is now the single source of truth for canonical local identity per `v2_job_id`
- The repaired `cache-v2` and `refresh-v2` paths converge on that canonical row
- The listing collapse uses the same `v2_run_references` mapping to select the canonical row
- The frontend's `warmSnapshotForSource` returns the analysis_id from the cache-v2 response (which is the canonical id)

The decision to not hardcode the historical `gen-v2-18853b558ef1` is correct. The old alias was minted before the idempotence repair; the current canonical id might be different if the repair re-established a different row as canonical. Resolving at preflight from the repaired host is the honest approach.

**Verification caveat**: The preflight must empirically confirm that job-detail and saved-result-detail return the same `analysis_id` (see Finding 1). The pre-repair proof showed them diverging. The memo's artifact requirements (Decision 5) already catch this if it persists.

### 3. Is the memo too permissive or too strict about normal snapshot behavior?

**The balance is right.**

Decision 4 accepts two valid behaviors:
- Reuse without a new warmup call (if `source.analysis_id` already set on the saved-result row)
- Warm/reuse that returns the same canonical id

Both are supported by the codebase:
- Frontend `warmSnapshotForSource` fast-path at line 548 handles the first case
- Backend canonical resolution in `_ensure_canonical_v2_local_snapshot` handles the second

The strictness requirement is also right: if either identity (`source_analysis_id` or `source_v2_job_id`) rewrites during the counted path, the attempt does not count. This prevents soft failures from being papered over.

### 4. Does the codebase now actually support the memo's assumptions?

**Yes, on all three claims.**

**Stable row listing**: `GET /api/genealogy/results/{project_id}` at lines 20956-20978 loads preferred analysis IDs from `v2_run_references` (line 20964) and collapses duplicates (line 20969). The 81 orphan rows should not appear in the panel's saved-results list.

**Post-Clear explicit row pinning**: `handleClearLoadedPresentation` at lines 975-981 sets `requiresExplicitSourceSelection = true`, nullifies `currentSourceResult` and `plannerDecision`. The `selectedSource` derivation at line 278 evaluates to `null` when `requiresExplicitSourceSelection` is true. Only `loadSelection` (lines 412-428) re-enables it by setting `requiresExplicitSourceSelection = false` at line 425.

**Planner-backed compose-from-selection continuity**: `launchPlannerBackedCompose` at lines 672-742 passes both `source_analysis_id` (line 690) and `source_v2_job_id` (line 695) to the compose URL params. The routing decision at lines 596-636 also passes both identities through `source_constraints`.

### 5. Is the memo under-specifying any remaining hazards?

**Mostly no. Two minor gaps, neither blocking.**

1. **Job-detail vs saved-result-detail identity convergence** (Finding 1): The memo requires both artifacts but doesn't explicitly state that they must agree. The pre-repair proof showed them disagreeing. In practice, the artifact bundle comparison in Decision 5 would catch this, but making the convergence check an explicit acceptance criterion would be cleaner.

2. **Orphan row interference** (Finding 2): If any code path reads `genealogy_analyses` without going through the collapse helper, an orphan row could surface. The memo's listing-stability assumption depends on all AOI-facing reads going through the collapse path. The tests prove this for the known routes, but an unknown route could bypass it.

Neither gap is severe enough to require a revision. The stop-and-revise rules (Decision 8) would catch both as "the explicit row click binds to a different source than the preflight-resolved canonical source."

### 6. Is this scope still narrow enough to keep roadmap order honest?

**Yes.**

The memo explicitly:
- Keeps Stage 2 open (Decision 7: "Stage 2 remains open until this rerun is graded honestly")
- Keeps Tranche 3 blocked (Decision 7: "Tranche 3 remains blocked until that Stage 2 decision is explicit")
- Does not reopen the frozen four-case Stage 5 pack
- Does not authorize code changes up front (Decision 1)
- Does not launch a new AOI run by default

The Tranche 2 -> Tranche 3 dependency chain is correctly preserved. The roadmap source documents (Big Roadmap Memo, Draft Platformization Roadmap) both require Stage 2 closure as a precondition for Tranche 3, and this memo respects that ordering.

### 7. Is the memo smuggling in Stage 2 closure by implication?

**No.**

The memo is explicitly honest about this. Decision 6 requires the closeout to answer four separate questions:
1. Did the repaired host support the counted planner-primary browser proof?
2. Is the evidence honestly `execution_backed`?
3. Does the recovered case pass the relevant rubric dimensions?
4. Is the evidence strong enough for repeated bounded AOI transient use, or only recovered-case success?

The acceptance criteria (final section) require either honest closure or honest failure documentation. The memo explicitly states: "Do not collapse 'browser rerun passed' into 'Stage 2 definitely closed' without writing those judgments explicitly."

This is the right level of discipline. The Stage 2 decision must be earned by the rerun, not assumed from it.

---

## Concrete Memo Revisions Recommended

**None required.** The memo is well-specified and honest.

Optional (not blocking):
- Decision 5 could add an explicit convergence check: "verify that the job-detail `analysis_id` and the saved-result-detail `id` for the preflight-resolved canonical source agree." This is already implicitly required by the cross-linking artifact but making it explicit would eliminate ambiguity.

---

## Conclusion

The rerun is the right next honest step. The codebase supports the memo's assumptions. The identity rule is technically sound. The scope is bounded correctly. The roadmap order is preserved honestly. The Stage 2 decision is kept genuinely explicit.

Approve the scope as written.
