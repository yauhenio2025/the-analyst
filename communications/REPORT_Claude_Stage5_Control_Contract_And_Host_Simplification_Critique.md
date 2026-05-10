# REPORT: Stage 5 Control Contract and Host Simplification Critique

Date: 2026-03-17
Reviewer: Claude Opus 4.6

Reviewed memo: `MEMO_2026-03-17_stage5_direction_control_contract_and_host_simplification.md`

---

## 1. Verdict

The Stage 5 direction is correct but the memo overstates the scope of what remains and misorers the work.

The central diagnosis is right: after Stages 2-4 moved read/restore/discovery/live-run truth upstream, the remaining displaced logic is launch/poll/control plumbing in The Critic, not another read boundary. A host-thinning pass before broadening is the correct sequencing.

But the memo describes ~5 sub-stages (5A-5E) that imply a substantial tranche. Code inspection reveals a smaller, more focused target. The actual core action is one thing: **delete `run_genealogy_v2_thread()` and its in-memory registries**, because the frontend already polls analyzer-v2 directly and the completion-side snapshot warming is already handled by the frontend. Everything else either follows from that deletion or is already largely done.

The order is also wrong. 5E (real-environment hardening) is placed last, but it should come **first** — you need to verify the current direct-poll architecture works end-to-end before deleting the fallback polling thread.

**Bottom line**: Approve Stage 5 as the next move, but scope it tighter and reorder it. It is a focused cleanup pass, not a multi-cycle stage.

---

## 2. What The Memo Gets Right

### The Stage 2-4 arc reconstruction is accurate

The memo correctly identifies what each stage accomplished:

- **Stage 2**: Result read/refresh boundary (`/v1/results/by-job/*`). Confirmed: routes exist in `src/api/routes/results.py` (133 lines), backed by `result_contract.py` (552 lines). Consumer cutover confirmed across all three bounded surfaces.

- **Stage 3**: Saved-result discovery/restore (`/v1/results/discovery`, attach-project, `restore_available`/`restore_reason` gating). Confirmed: discovery returns `DiscoverySummary` list filtered by project/workflow/thinker. Restore is explicitly gated — `get_result_presentation()` only returns a presentation when `restore_available=True`. The Critic frontend loads discovery from analyzer-v2 first and falls back to local snapshots.

- **Stage 4**: Live-run contract (`/v1/runs/by-job/{job_id}`, `/v1/runs/discovery`). Confirmed: `run_contract.py` (293 lines) joins executor state, preparation state, and result transition state. The Critic frontend now polls `ANALYZER_V2_URL/v1/runs/by-job/{jobId}` directly at 3-second intervals (GenealogyPage.tsx, AoiV2ThematicPanel.tsx). Cancel token is stored in `V2RunReferenceDB` and forwarded to v2 on cancellation.

This arc is real and verified in code.

### The remaining gap is correctly diagnosed as control/host plumbing

The memo says: "What remains displaced is no longer primarily read truth. What remains displaced is the control-side and host-side plumbing." This is confirmed by code inspection.

The frontend now reads run state from analyzer-v2 directly. The result boundary is upstream-first. Discovery is upstream-first. What remains in The Critic is:

| Component | Location | Lines | Nature |
|-----------|----------|-------|--------|
| In-memory registries | `server.py:17498-17502` | 5 defs | Non-persistent, lost on restart |
| V2 execution thread | `server.py:17817-18300` | ~483 | Background polling loop + launch + retry |
| Cancel endpoint | `server.py:19144-19188` | ~45 | Forwards with cancel_token (Stage 4 fix) |
| Recover endpoint | `server.py:19191-19283` | ~93 | Polling-failure workaround |
| Resume endpoint | `server.py:19286-19329` | ~44 | Forwards to v2 |
| Import endpoint | `server.py:19332-19437` | ~106 | Thin wrapper: attach + fetch + cache |
| Refresh endpoint | `server.py:19467-19529` | ~63 | Thin wrapper: v2 refresh + cache update |
| Cache endpoint | `server.py:19532-19571` | ~40 | Warm local snapshot from upstream |
| Snapshot persistence | `server.py:18477-18648` | ~172 | Save/update presentation to DB |

Total: ~1050 lines of lifecycle/plumbing code. The memo correctly identifies this as the next target.

### Deferral recommendations are correct

All four deferrals are supported by evidence:

1. **Another artifact seam**: The remaining dominant hot path is lifecycle plumbing, not missing artifact identity. The existing `genealogy.relationship_classification` seam is sufficient for the current bounded consumers.

2. **analyzer-mgmt packaging elevation**: analyzer-mgmt already has a 1469-line job detail page with 6 tabs, result boundary integration, and run boundary integration. It is missing discovery pages and cancel/resume buttons, but those are day-of-work additions, not packaging work.

3. **SDK extraction**: Premature without a stable lifecycle contract free of redundant polling infrastructure.

4. **Full launch/corpus-ownership transfer**: The Critic still owns document loading, project identity, and the start flow. Moving this is much larger than control-contract cleanup.

### Snapshot/cache demotion direction is correct

The snapshot layer is already thin. Snapshots are stored in `genealogy_analyses.pass_results` (JSON column). They are saved:
- On job completion (by the polling thread)
- On import (by the import endpoint)
- On refresh (by the refresh endpoint)
- On explicit cache-warm (by the cache endpoint)

They are NOT pre-warmed. They are NOT automatically refreshed. The frontend already prefers upstream presentation over cached snapshots. The memo's recommendation to make the cache-only role explicit is correct but the actual code change is small.

---

## 3. What It Still Overstates Or Misorders

### A. The residual lifecycle thickness is overstated

The memo lists:
- "launcher glue"
- "control forwarding"
- "legacy v2 compatibility routes"
- "leftover in-memory registries and polling-era code"
- "snapshot/import/refresh/cache scaffolding that is now narrower than before but still thicker than the target architecture"

Code inspection reveals:

1. **"Legacy v2 compatibility routes"** — these are already thin. The cancel endpoint is ~45 lines and forwards with cancel_token. The resume endpoint is ~44 lines and forwards to v2. The import endpoint is ~106 lines but is a thin wrapper around the v2 result boundary. These are already "obviously thin" forwarding proxies. Making them "decisively secondary" (5C) is mostly a naming exercise, not an architecture change.

2. **"Launcher glue"** — the start endpoint (`start_genealogy_analysis()`, lines 18966-19005) is synchronous post-Stage-4: it calls v2, saves the run reference with cancel_token, creates an in-memory entry, spawns the polling thread, and returns the v2 job_id. If you remove the polling thread spawn, this endpoint is already thin (~40 lines of real logic).

3. **"Snapshot/import/refresh/cache scaffolding"** — this is ~380 lines total. The import/refresh/cache endpoints are thin wrappers that forward to v2 and optionally update the local DB. The snapshot persistence functions are ~172 lines. This code is not "thick" — it's a fallback cache layer operating correctly as a fallback cache layer.

The memo's framing implies a substantial multi-block cleanup program (5A through 5E). The actual work is more focused: delete the polling thread and its in-memory registries. Everything else is either already thin or is a documentation/naming cleanup.

### B. 5A before 5E is wrong

The memo places "delete obsolete v2 intermediary code paths" (5A) first and "add minimum real-environment hardening" (5E) last.

This is backwards. Evidence:

- The Stage 3 completion memo states: "I did not run end-to-end UI flows for this closeout."
- The Stage 4 completion memo states: "I did not run end-to-end UI flows."
- Stage 4 introduced the most important architectural change: frontends polling analyzer-v2 directly for live run status.

You should not delete the Critic polling thread (which serves as an implicit fallback path) until you have verified that the direct-poll path works correctly in deployed environments. If you delete first and discover a CORS issue, a timeout problem, or a progress-field mismatch in production, you have removed the fallback.

**5E must come first.** Verify the new architecture works, then delete the old plumbing.

### C. 5B and 5C are already largely done

**5B (tighten the control contract)**: The memo proposes consolidating into "start, cancel, resume, import, refresh, cache-upsert." That is already exactly what exists. The Stage 4 cancel_token fix was the last hard control-contract issue. What remains is:
- Remove the recover endpoint (polling-failure workaround that's no longer needed if the frontend polls v2 directly)
- That's it

**5C (make legacy Critic read endpoints decisively secondary)**: The frontends already read from v2 directly. The compatibility read endpoints exist but are not used by bounded v2 surfaces. Making them "decisively secondary" means either deleting them or adding deprecation notices — a small documentation-level change, not an architectural one.

### D. The auto-retry concern is not addressed

`run_genealogy_v2_thread()` includes an auto-retry mechanism (lines 18202-18263) that detects "instance recycled" or "process terminated" errors from v2 and automatically re-starts the analysis (up to 2 retries, 10-second wait between retries).

If you delete the thread, this retry capability disappears. V2 has its own orphan recovery (`job_manager.py` startup recovery), but the behavior is different:
- Critic-side retry: immediate re-start, transparent to user
- V2-side orphan recovery: requires v2 restart, longer delay, different user experience

The memo should acknowledge this tradeoff and decide explicitly: is the Critic-side auto-retry still valuable, or is v2's orphan recovery sufficient?

**Evidence**: V2 already has `_recover_in_flight_jobs()` in `job_manager.py` that runs at startup, and `_fail_stale_running_jobs()` that detects jobs stuck for too long. These cover the recovery case. But they are startup-time recovery, not mid-execution retry. The Critic's auto-retry is live retry during execution, which is a different (arguably more valuable) capability.

### E. The memo doesn't name what specifically should be deleted vs thinned

The memo says `run_genealogy_v2_thread()` should be "either deleted code or code explicitly marked local/non-v2 legacy only." But this thread does more than poll:

1. **Document loading and upload to v2** (lines 17849-17912) — still needed
2. **V2 launch** (lines 17922-17999) — still needed (plan creation, job start)
3. **Polling loop** (lines 18046-18289) — genuinely redundant (frontend polls v2 directly)
4. **Progress translation** (lines 18107-18125) — genuinely redundant
5. **Completion handling with snapshot save** (lines 18127-18189) — partially redundant (frontend already triggers cache-upsert)
6. **Auto-retry on infrastructure failure** (lines 18202-18263) — tradeoff (see above)

The correct action is not "delete the thread" but "thin the thread to a synchronous start-and-return path": keep document loading and v2 launch, remove polling and completion handling, decide on retry.

---

## 4. Whether Stage 5 As Proposed Is The Right Next Move

### Yes, with scope and order corrections

The diagnostic is correct: after Stages 2-4, the remaining displaced logic is control/host plumbing, and thinning it is higher-leverage than broadening the artifact surface.

But the proposed five sub-stages (5A-5E) overframe what is actually a focused cleanup pass:

1. **The polling thread is the real target.** `run_genealogy_v2_thread()` is ~483 lines, most of which is polling infrastructure that is now redundant because the frontend polls v2 directly. Deleting or thinning this thread is the core of Stage 5.

2. **The in-memory registries go with the thread.** `_GENEALOGY_JOBS`, `_GENEALOGY_JOB_CANCELLATION`, and `_V2_JOB_MAPPINGS` are maintained by the thread. If the thread is removed, these become unnecessary (the persistent `V2RunReferenceDB` table already stores the durable linkage).

3. **The recover endpoint goes with the thread.** The recover endpoint exists to handle cases where the Critic polling thread lost contact with v2 but the v2 job actually completed. Without the polling thread, this scenario doesn't arise.

4. **Everything else is already thin or is naming/deprecation work.** Cancel, resume, import, refresh, and cache endpoints are already thin forwarding proxies. Making them "obviously thin" is a documentation concern, not an implementation concern.

### What about alternatives?

**Alternative: Do another artifact seam instead.** Rejected for the same reason the memo gives — the polling thread is genuinely fragile (non-persistent in-memory state, no locking on `_GENEALOGY_JOBS`, daemon threads spawned inline). Cleaning this up before broadening is the correct order.

**Alternative: Do end-to-end verification as a standalone pre-stage, then decide between thinning and broadening.** This is worth considering. The end-to-end verification (proposed 5E) is small enough to be a pre-stage rather than a sub-stage. If it reveals problems with the direct-poll architecture, the scope of Stage 5 changes significantly.

**I mildly prefer the pre-stage approach.** Verify first, then thin. But either way, the thinning should happen before broadening.

---

## 5. What Must Change Before Planning

### 1. Reorder: end-to-end verification first

Before deleting anything, verify:
- Direct frontend→v2 run polling works in deployed environment (CORS is configured on both sides, but has anyone actually tested the deployed flow?)
- Frontend completion transition works: job completes → frontend detects completion via v2 run contract → frontend fetches result presentation from v2 → frontend triggers local cache-upsert
- Cancel with forwarded cancel_token works end-to-end
- Resume works end-to-end (frontend → Critic → v2 resume → frontend polls v2 for resumed job)

This is the single highest-value pre-step. If it fails, the scope of Stage 5 changes.

### 2. Address the auto-retry tradeoff explicitly

The memo must decide: is Critic-side auto-retry on "instance recycled" errors still valuable?

Options:
- **Delete it**: v2's orphan recovery handles the case eventually, but with more delay and different UX
- **Move it to the frontend**: frontend detects infrastructure failure from v2 run contract and re-triggers start via Critic
- **Keep a thin backend retry loop**: instead of a full polling thread, keep a lightweight watcher that only handles retry, not progress/status

My recommendation: delete it. V2's own orphan recovery (`_recover_in_flight_jobs()`, `_fail_stale_running_jobs()`) plus resume capability is sufficient. The Critic-side retry was a workaround for an earlier state where v2 had weaker recovery. That's no longer the case.

### 3. Scope the thread thinning honestly

The correct action for `run_genealogy_v2_thread()` is not full deletion but thinning to a synchronous path:

**Keep:**
- Document loading and upload to v2 (lines 17849-17912)
- V2 launch — plan creation + job start (lines 17922-17999)

**Delete:**
- Polling loop (lines 18046-18289)
- Progress translation (lines 18107-18125)
- Completion handling (lines 18127-18189) — frontend handles this
- Auto-retry infrastructure (lines 18202-18263) — v2 recovery handles this
- In-memory state management (lines 18025-18044) — V2RunReferenceDB handles this

**Result:** The thread becomes a synchronous function, not a background thread. Document loading → v2 launch → save run reference → return v2 job_id. No more daemon threads, no more in-memory registries, no more polling.

### 4. Recognize 5B/5C/5D are small cleanup, not separate sub-stages

These should not be framed as distinct blocks:
- **5B** (tighten control contract): Delete recover endpoint, verify remaining endpoints are thin forwarding proxies. ~2 hours of work.
- **5C** (make legacy reads secondary): Add deprecation comments or response headers to legacy endpoints. ~1 hour of work.
- **5D** (demote snapshots further): The snapshots are already fallback-only. The cache-upsert is already opportunistic. Making this "explicit in code and route naming" is a naming exercise. ~1 hour of work.

These are cleanup tasks that follow from the thread deletion, not separate architectural work.

### 5. Add the missing analyzer-mgmt discovery gap to the plan

The memo says analyzer-mgmt packaging elevation should wait. That's correct for packaging. But analyzer-mgmt is currently missing basic observability that the run contract already supports:

- No `/jobs` list page (backend `GET /v1/executor/jobs` exists, no frontend consumer)
- No discovery methods in `api.ts` for `/v1/runs/discovery` or `/v1/results/discovery`
- No cancel/resume buttons on job detail page
- The `runBoundary.getRun()` method exists but is only used in the result-boundary tab

These are day-of-work frontend additions. They should be part of Stage 5, not deferred to some future "analyzer-mgmt elevation" stage. They are the bounded verification harness for the new architecture, and they cost almost nothing.

---

## 6. Recommended Corrected Direction

### Rename: Stage 5: Host Plumbing Cleanup

Not "Control Contract and Host Simplification" — the control contract is already thin. The work is plumbing cleanup.

### Corrected order:

**5A. End-to-end verification (first, non-negotiable)**

Verify the current deployed architecture works:
- Start a real analysis in The Critic
- Confirm frontend polls v2 directly and renders progress
- Confirm completion transitions correctly
- Confirm cancel with cancel_token works
- Confirm resume works
- Confirm result discovery and restore work after reload
- Document any failures

If this reveals problems, fix them before proceeding. If it reveals the direct-poll path has gaps, the scope of 5B changes.

Estimated scope: 1-2 focused sessions.

**5B. Thin the execution thread (the actual core of Stage 5)**

Convert `run_genealogy_v2_thread()` from a background polling thread to a synchronous start-and-return function:
- Keep: document loading, plan creation, v2 job start, run reference persistence
- Delete: polling loop, progress translation, completion handling, auto-retry, in-memory state management
- Delete: `_GENEALOGY_JOBS`, `_GENEALOGY_JOB_CANCELLATION`, `_V2_JOB_MAPPINGS`
- Delete: recover endpoint (no longer needed without polling thread)
- Delete: resume poll thread spawning (frontend triggers resume, polls v2 directly for status)

This is the largest single change. Estimated scope: 2-3 focused sessions.

**5C. Clean up control endpoint surface (follows from 5B)**

After the thread is thinned:
- Cancel endpoint stays (thin: forward to v2 with cancel_token from V2RunReferenceDB)
- Resume endpoint stays (thin: forward to v2, return)
- Import endpoint stays (thin: attach + fetch + cache)
- Refresh endpoint stays (thin: v2 refresh + cache update)
- Cache-upsert endpoint stays (thin: fetch + save)
- Recover endpoint deleted (5B already handles this)
- Add deprecation markers to any legacy read endpoints that are no longer primary

Estimated scope: 1 focused session.

**5D. Add bounded analyzer-mgmt observability (parallel with 5B/5C)**

- Add `api.runs.discover()` and `api.results.discover()` to `frontend/src/lib/api.ts`
- Create `/jobs/index.tsx` page with active/recent run listing
- Add cancel and resume buttons to job detail page
- This is the verification harness for the new architecture

Estimated scope: 1 focused session.

**5E. Snapshot layer cleanup (last)**

- Verify snapshot persistence is only triggered by explicit cache-upsert, import, and refresh — not by the deleted polling thread
- Remove any snapshot write paths that were only reachable from the deleted thread
- Verify the cache-only role is explicit in code comments and route naming

Estimated scope: <1 session.

### Total estimated scope

5-7 focused sessions. Not a multi-week program. The largest item (5B) is a focused deletion pass once the end-to-end verification (5A) confirms the new architecture works.

### What this corrected Stage 5 is NOT

- It is not a control-contract redesign (the control contract is already thin)
- It is not a snapshot architecture migration (snapshots are already fallback-only)
- It is not an analyzer-mgmt packaging elevation (just basic discovery pages)
- It is not a multi-cycle iterative displacement program (it's one focused deletion + cleanup)

### After Stage 5

The evaluation gate the memo describes is still correct. After cleaning up the polling thread and in-memory registries, the next decision becomes:

- **If the system needs more product surface**: another artifact seam
- **If the system needs broader consumer reach**: SDK extraction or thin-consumer tooling
- **If the system needs richer admin observability**: analyzer-mgmt depth
- **If the system needs production hardening**: push mechanism (SSE), proper health checks

But those are genuinely post-Stage-5 decisions. The memo is right that they should wait.

### The key risk the memo should have named

The single biggest risk in Stage 5 is not "residual lifecycle thickness." It is **whether the deployed direct-poll path actually works end-to-end**. Neither Stage 3 nor Stage 4 ran end-to-end UI flows. The code is correct by construction and type-checked, but the deployed runtime has not been verified.

If 5A (end-to-end verification) reveals that direct frontend→v2 polling has issues in production (timeout behavior, error handling, progress field mapping, CORS edge cases), then Stage 5 becomes "fix those issues" rather than "delete the polling thread."

That is why 5A must come first.
