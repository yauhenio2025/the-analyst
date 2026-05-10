# REPORT: Stage 4 Run Lifecycle Authority Critique

Date: 2026-03-17
Reviewer: Claude Opus 4.6

Reviewed memo: `MEMO_2026-03-17_stage4_run_lifecycle_authority_after_stage3.md`

## 1. Verdict

The memo's direction is broadly correct but its framing is architecturally imprecise.

The Critic does not own "run lifecycle authority." It owns **run lifecycle plumbing**. The authority already lives in analyzer-v2 after Stages 1-3. What remains in The Critic is a proxy/routing layer — in-memory dicts, background polling threads, and thin wrapper endpoints — not a competing authority that needs formal displacement.

This distinction matters because it changes the scope and sequencing of Stage 4:

- If it is an authority transfer, you design formal contracts and cut over responsibility.
- If it is plumbing removal, you make a routing decision (push vs direct poll vs retained proxy) and then delete the glue.

The memo also **misorers** the push/status mechanism decision. It positions it 4th (after displacement). It should be **1st**, because the displacement strategy depends entirely on whether frontends talk to v2 directly, through SSE, or through a retained thin proxy.

Recommended correction: rename Stage 4 from "Run Lifecycle Authority" to **"Run Lifecycle Routing Decision + Plumbing Displacement"** and reorder the sub-stages so the mechanism decision comes first.

---

## 2. What The Memo Gets Right

### The March 15-17 arc is correctly reconstructed

The progression is accurately described:

- AOI canary proved semantic ownership beyond genealogy
- Stage 1 built the analysis-product layer (`corpus_ref`, `analysis_artifacts`, first result manifest)
- Stage 2 made the result boundary load-bearing for current read/refresh across three surfaces
- Stage 3 made the same boundary authoritative for saved-result discovery and restore

This is confirmed by the live code. The result boundary in `src/api/routes/results.py` (133 lines) now exposes discovery, manifest, presentation, refresh, and project attachment. The Critic's import and refresh flows have been thinned to wrapper calls around these v2 APIs.

### Run lifecycle is indeed the next logical concern

After displacing result-state authority (Stages 2-3), the remaining displaced logic is execution-time lifecycle. The memo correctly identifies this as the next gap. The live code confirms it: The Critic's `api/server.py` still carries ~977 lines of active lifecycle logic (polling threads, cancel/resume/recover endpoints, import flow).

### Deferral recommendations are correct

The memo correctly defers:

- Another genealogy artifact seam — the current `genealogy.relationship_classification` seam is sufficient
- analyzer-mgmt packaging elevation — the console is already a thin frontend; adding a `/jobs` list page is trivial and doesn't require packaging work
- SDK extraction — premature without a stable lifecycle contract
- Generated bespoke apps — downstream of everything else

### The Critic still carries real lifecycle plumbing

This is confirmed by code inspection:

| Component | Location | Lines | Nature |
|-----------|----------|-------|--------|
| In-memory job registry | `server.py:17498-17502` | 5 | 3 global dicts, non-persistent |
| V2 execution thread | `server.py:17667-18148` | ~482 | Background polling loop |
| Job status endpoint | `server.py:18801-18829` | 29 | Reads from in-memory dict |
| Cancel endpoint | `server.py:18832-18867` | 36 | Sets local flag, doesn't always forward to v2 |
| Recover endpoint | `server.py:18869-18961` | 93 | "Check if v2 actually completed" |
| Resume endpoint + thread | `server.py:18964-19150` | 187 | Calls v2 resume, spawns new poll thread |
| Import endpoint | `server.py:19154-19269` | 116 | Thin wrapper around v2 result boundary |
| Refresh endpoint | `server.py:19272-19334` | 63 | Thin wrapper around v2 refresh |
| Frontend polling | `GenealogyPage.tsx:851-954` | ~100 | 3-second setInterval loop |
| Frontend result fetch | `GenealogyPage.tsx:616-711` | ~96 | Direct v2 fetch for presentations |
| Client sync wrappers | `analyzer_v2_client.py:574-792` | ~218 | Sync wrappers for v2 APIs |

---

## 3. What It Still Overstates Or Misorers

### A. The Critic's lifecycle code is already thin, not heavyweight

The memo frames The Critic as owning "too much" lifecycle logic: "job polling loops, local run registries, retry/recover behavior, resume orchestration, live status translation, run-to-result transition glue."

Code inspection reveals a different picture:

1. **Job polling loops**: Pure plumbing. The Critic backend thread polls v2 at 5s intervals and writes to an in-memory dict. The frontend polls the Critic at 3s intervals. Two layers of polling, zero authority. Eliminating the backend layer is a routing change, not an authority transfer.

2. **Local run registries**: `_GENEALOGY_JOBS` is a non-persistent in-memory dict. It is **weaker** than v2's persistent DB-backed job state. After a Critic restart, all active jobs are lost. V2 already has orphaned-job recovery (`job_manager.py`). The Critic registry is already less authoritative than v2.

3. **Retry/recover behavior**: The "recover" endpoint (`server.py:18869-18961`) does exactly one thing: check whether the v2 job actually completed when the Critic thought it failed. That is not "recovery authority." That is a polling-failure workaround.

4. **Resume orchestration**: The Critic calls `POST /v1/executor/jobs/{job_id}/resume` on v2 (which already exists at `executor.py:262-348`) and then spawns a local poll thread. V2 does the actual resumption (skipping completed phases, using cached passes). The Critic owns the poll thread, not the resume logic.

5. **Live status translation**: **There is none.** Status codes are transparent passthroughs (pending/running/completed/failed, plus Critic-local "cancelled"). Progress is directly embedded from v2 responses. The explorer confirmed no translation layer exists.

6. **Run-to-result transition glue**: After Stages 2-3, result state is authoritative in v2. The Critic persists local snapshots as fallback cache. The transition itself happens in `workflow_runner.py:354-379` (v2) via `_run_auto_presentation`. The Critic's involvement is receiving the completed presentation and caching it locally.

**Bottom line**: The memo describes ~977 lines of actual lifecycle logic in The Critic. Most of it is polling/routing infrastructure, not authority. The v2 executor already owns job state, progress, cancellation, resumption, and result transition. The Critic owns the polling thread and a non-persistent in-memory cache.

### B. The push/status decision is misordered

The memo positions the push/status mechanism decision as sub-stage 4D, after displacement (4C). This is architecturally backwards.

Why it should be first:

- **If you choose direct polling**: The frontend polls v2 directly. You need CORS on v2. The Critic backend polling thread is deleted entirely. Displacement becomes trivial — just remove the proxy layer.

- **If you choose SSE**: V2 adds `GET /v1/executor/jobs/{job_id}/stream`. The frontend subscribes directly. The Critic backend polling thread is deleted. But you need to evaluate Render's SSE connection limits and costs.

- **If you choose retained proxy**: The Critic backend thread stays but thins further. Displacement is incremental. But you haven't actually changed the architecture.

The displacement strategy (4C) depends entirely on the mechanism decision (4D). Running 4C before 4D means you'd thin the Critic without knowing what replaces it, which risks either:
- leaving a thinner-but-still-present proxy (pointless half-step)
- or having to re-architect after the mechanism decision

### C. "Run lifecycle authority" is the wrong framing

The authority already lives in v2. The executor owns:
- Job creation with idempotency (`executor.py:63-180`)
- 5-state machine with persistent DB (`schemas.py:15-21`, `job_manager.py`)
- Progress tracking with structured detail (`schemas.py:71-83`)
- Cancellation with token verification (`job_manager.py:335-394`)
- Resume from checkpoint with phase skip (`executor.py:262-348`, `workflow_runner.py:184-203`)
- Stale job detection and orphan recovery (`job_manager.py`)
- Plan persistence in DB for instance recycles (`plan_context.py`)
- Auto-presentation on completion (`workflow_runner.py:700-746`)

What v2 **lacks** is not authority but **consumer-facing convenience**:
- Unified discovery across active + completed runs (currently split between `/executor/jobs` and `/results/discovery`)
- Push mechanism for real-time updates (currently polling only)
- Lifecycle event audit log (no "why did this state transition happen?")

These are incremental API additions, not an authority transfer.

### D. The two-layer polling problem is not named

The memo doesn't name the actual architectural problem clearly enough.

The current flow is:

```
Frontend (3s poll) → Critic backend → in-memory dict ← Critic thread (5s poll) → v2 executor
```

That is **two layers of polling** with an in-memory cache in between. The in-memory cache is non-persistent and weaker than v2's DB. This is the actual problem: a redundant, fragile intermediary.

The memo's framing of "make v2 authoritative" obscures the fact that v2 is already authoritative. The real fix is removing the intermediary, which is a routing/plumbing decision.

### E. The memo doesn't address CORS or frontend routing concerns

If the goal is to have frontends talk to v2 directly for run lifecycle (which the memo implies), there are practical prerequisites:
- CORS configuration on v2 for Critic frontend origin
- Error handling for v2 downtime (currently the Critic backend absorbs this)
- Authentication model for direct frontend→v2 access
- The Critic backend currently serves as a unified API surface; splitting job lifecycle to v2 and everything else to Critic creates a multi-origin frontend

These are not blockers, but the memo should acknowledge them.

---

## 4. Whether Stage 4 As Proposed Is The Right Next Move

### Yes to the diagnostic, no to the framing and order

The diagnostic is correct: after Stages 1-3, the remaining displaced logic is execution-time lifecycle plumbing. That should be addressed next.

But:

1. **The framing of "authority transfer" is wrong.** Authority already lives in v2. The work is plumbing displacement and API convenience.

2. **The order is wrong.** The push/status mechanism decision (4D) must come before displacement (4C), not after. Everything else follows from that decision.

3. **The scope is inflated.** The memo's four-outcome framing (upstream run discovery, upstream run status authority, upstream run control authority, upstream run-to-result transition truth) describes capabilities that largely already exist in v2. The actual missing pieces are:
   - Unified active+completed run discovery (one API, not two)
   - Push or direct-poll mechanism to eliminate the Critic backend polling thread
   - A decision about whether to keep the Critic as thin proxy or bypass it entirely

4. **The displacement sub-stage (4C) will be smaller than expected.** Once the routing decision is made and the frontend can access v2 run state directly (or through SSE), the Critic lifecycle code to delete is ~977 lines of actual logic, mostly the background polling thread and its error handling. That is not a multi-session tranche; it is a focused deletion pass.

### What about alternatives?

**Alternative A**: Skip Stage 4 entirely and do another artifact seam.

This is tempting because the lifecycle plumbing is already "good enough" — it works, it's thin, it's a known quantity. Another artifact seam would expand the product surface.

I reject this alternative because the two-layer polling architecture is genuinely fragile. The in-memory `_GENEALOGY_JOBS` dict is lost on restart. The resume-poll-thread spawns daemon threads inline. The cancel endpoint doesn't always forward to v2. These are not architectural risks — they are operational fragilities that should be cleaned up before broadening.

**Alternative B**: Do the push/status decision as a standalone pre-stage, then evaluate whether lifecycle displacement or artifact breadth has higher leverage.

This is worth considering. The push/status decision is the actual architectural blocker. Once you know whether it's SSE, direct polling, or retained proxy, you can evaluate displacement scope more precisely. If the answer is "retained polling against v2 directly," displacement becomes a focused CORS + frontend routing change. If the answer is SSE, there's a v2 implementation step first.

I mildly prefer Alternative B over the memo's proposed Stage 4. The push/status decision is genuinely load-bearing and should not be buried inside a broader lifecycle tranche.

---

## 5. What Must Change Before Planning

### 1. Rename and reframe

"Run Lifecycle Authority" implies a transfer of ownership. The correct frame is **"Run Lifecycle Routing Cleanup"** or **"Execution-Time Plumbing Displacement."** The authority already lives in v2.

### 2. Reorder: mechanism decision first

The proposed order should be:

1. Push/status mechanism decision (currently 4D → move to 4A)
2. Small v2 run-contract additions (unified discovery, optional audit log)
3. Frontend routing change (direct v2 access or thinnest proxy)
4. Critic lifecycle code deletion
5. Bounded analyzer-mgmt additions (job list page, cancel button — cheap frontend work)

### 3. Scope the Critic displacement honestly

The memo implies a multi-cycle displacement program ("expand one upstream run capability → cut over one Critic responsibility → verify → repeat"). The actual Critic lifecycle code to displace is:

- `run_genealogy_v2_thread()`: ~482 lines → delete entirely (v2 owns execution)
- Resume poll thread: ~187 lines → delete (frontend polls v2 directly or uses SSE)
- Cancel endpoint: ~36 lines → thin to direct v2 forward (1 line)
- Recover endpoint: ~93 lines → delete (unnecessary if frontend polls v2 directly)
- Job status endpoint: ~29 lines → thin to v2 proxy or delete (frontend calls v2)
- In-memory registries: 5 lines → delete

That is a focused deletion pass, not a multi-cycle iterative displacement.

### 4. Address the CORS/routing question explicitly

The plan must decide: does the Critic frontend call v2 directly for lifecycle APIs, or does it retain a thin proxy? The answer determines the displacement approach.

Evidence from analyzer-mgmt: its frontend already calls v2 directly for executor jobs, presenter status, and result manifests (`frontend/src/lib/api.ts` uses `ANALYZER_V2_URL` directly). So direct frontend→v2 access is an established pattern in this ecosystem. The Critic frontend already does this for some result fetching (`GenealogyPage.tsx:616-624` calls `analyzer-v2.onrender.com` directly).

### 5. Recognize analyzer-mgmt is already closer than the memo implies

The memo says "analyzer-mgmt does not need to become the packaging console yet. It only needs small bounded visibility improvements."

Code inspection shows analyzer-mgmt already has:
- Job detail page with 6 tabs (summary, manifest, decision trace, page structure, steering, result boundary) — `frontend/src/pages/jobs/[id].tsx`, 1407 lines
- Plan listing with embedded job list
- Result boundary visibility
- Direct v2 API calls for executor jobs and presenter status

What it's missing is just:
- A standalone `/jobs` list page (low effort, frontend only)
- Cancel button on job detail page (trivial)
- Result discovery page (medium effort, frontend only)

These are day-of-work additions, not a separate sub-stage.

---

## 6. Recommended Corrected Direction

### Reframed Stage 4: Execution-Time Routing Cleanup

**Goal**: Eliminate the two-layer polling architecture and the Critic's non-persistent in-memory job registry, so that run lifecycle state flows from v2 to frontends without a fragile intermediary.

### Corrected order:

**4A. Push/status mechanism decision** (1-2 days, design + spike)

Evaluate and decide:

| Option | Pros | Cons |
|--------|------|------|
| **Direct polling** (frontend → v2) | Simplest, proven pattern (analyzer-mgmt already does this) | Still polling, no real-time; CORS needed on v2 |
| **SSE** (`GET /v1/executor/jobs/{id}/stream`) | Real-time, clean push model | Render connection limits, implementation cost, long-lived connections |
| **Retained thin proxy** (Critic proxies v2 status) | Minimal change, no CORS | Keeps the two-layer architecture, defers the real cleanup |

**My recommendation**: Start with direct polling (Option 1). It is proven in analyzer-mgmt, requires only CORS configuration on v2, and immediately eliminates the Critic backend polling thread. SSE can be added later as an optimization if polling latency becomes a problem.

**4B. Small v2 run-contract additions** (1-2 days)

Add to `src/api/routes/executor.py` or `results.py`:

1. **Unified run discovery**: Merge active and completed run visibility into one endpoint (or add active-run filtering to `/results/discovery`). Currently split between `GET /v1/executor/jobs` (all states) and `GET /v1/results/discovery` (completed only, requires `project_id`). A consumer shouldn't need two endpoints to answer "what's happening for this project?"

2. **CORS middleware**: Add permissive or configured CORS to the FastAPI app for frontend direct access (if choosing direct polling).

3. **Optional: lifecycle event log**: Add a `job_events` table and `GET /v1/executor/jobs/{id}/events` endpoint. Low priority — the current 5-state model with timestamps is adequate for bounded observability.

**4C. Frontend routing change** (2-3 days)

Update The Critic's `GenealogyPage.tsx` to:
- Poll `GET /v1/executor/jobs/{job_id}` on v2 directly (instead of `GET /api/genealogy/jobs/{job_id}`)
- Call `POST /v1/executor/jobs/{job_id}/cancel` on v2 directly
- Call `POST /v1/executor/jobs/{job_id}/resume` on v2 directly

The Critic backend retains:
- Job initiation (plan creation + job start → these can stay as Critic backend calls to v2 because they're one-shot, not polling)
- Local snapshot caching (fallback only, already demoted)

**4D. Critic lifecycle code deletion** (1-2 days)

Delete:
- `run_genealogy_v2_thread()` and resume poll thread (background polling infrastructure)
- `_GENEALOGY_JOBS`, `_GENEALOGY_JOB_CANCELLATION`, `_V2_JOB_MAPPINGS` (in-memory registries)
- Recover endpoint (unnecessary with direct v2 polling)
- Job status proxy endpoint (frontend calls v2 directly)

Thin:
- Cancel endpoint → one-line forward to v2
- Resume endpoint → one-line forward to v2 + clear local state

Retain:
- Import endpoint (thin wrapper, still useful for project attachment)
- Result caching for fallback (already demoted by Stage 3)

**4E. Bounded analyzer-mgmt additions** (1 day, parallel with anything above)

- Add `/jobs` list page with status filtering (frontend only, calls v2 API)
- Add cancel button on job detail page
- Add `/results` discovery page (frontend only, calls `GET /v1/results/discovery`)

### What this corrected Stage 4 is NOT

- It is not a new authority transfer (authority already lives in v2)
- It is not a multi-cycle iterative displacement (it's a focused routing change + deletion pass)
- It is not an SSE/WebSocket buildout (start with direct polling, optimize later)
- It is not an analyzer-mgmt packaging project (just small observability additions)

### Total estimated scope

~6-10 days of focused work across all sub-stages, not a multi-week program. The memo's framing implies a larger tranche than the code evidence supports.

### After Stage 4

The evaluation gate (4E in the original memo) is still correct. After cleaning up the lifecycle plumbing, the decision becomes clearer:

- **If the system needs more product surface**: do another artifact seam
- **If the system needs richer observability**: add SSE, lifecycle audit, or analyzer-mgmt depth
- **If the system needs broader consumer reach**: consider SDK extraction or thin-consumer tooling

The memo is right that these should wait. But the wait should be shorter than the memo implies, because the lifecycle cleanup is smaller than framed.
