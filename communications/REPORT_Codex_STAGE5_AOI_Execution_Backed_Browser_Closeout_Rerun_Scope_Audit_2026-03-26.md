# Audit: Stage 5 AOI Execution-Backed Browser Closeout Rerun Scope

Date: 2026-03-26
Auditor: Codex
Memo under review: `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_scope.md`

## Verdict

Approve with revisions.

## Findings

### 1. High: the memo overstates end-to-end preservation of the local counted `source_analysis_id`

The memo makes the local canonical id sound like an end-to-end invariant of the counted path (`communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_scope.md:34-38`, `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_scope.md:127-154`, `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_scope.md:210-215`).

The actual code is stricter about upstream identity than local identity:

- the AOI panel carries both ids into `/compose-from-intent` on the planner-backed path (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:687-699`)
- the compose page forwards both ids into the host `compose-from-selection` POST body (`/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:429-442`)
- the host proxy resolves both ids, but only forwards `source_v2_job_id` to analyzer-v2 (`/home/evgeny/projects/the-critic/api/server.py:21532-21552`)

More importantly, `_resolve_source_backed_compose_identity(...)` validates that `source_analysis_id` and `source_v2_job_id` refer to the same AOI source context, but it does not require the supplied `source_analysis_id` to equal `v2_run_references.local_snapshot_analysis_id` (`/home/evgeny/projects/the-critic/api/server.py:19205-19231`, `/home/evgeny/projects/the-critic/api/server.py:19254-19276`). A stale duplicate local row for the same upstream `job-6ee8b0621177` would still pass the route guard if its persisted `_v2_job_id` matches.

So the counted-source rule is technically sound only if it is written this way:

- `source_v2_job_id = job-6ee8b0621177` is the end-to-end counted truth
- the preflight-resolved canonical `source_analysis_id` is a host-local continuity selector that must stay stable through row pinning, warmup, `/compose-from-intent`, and the host `compose-from-selection` request
- analyzer-v2 is not currently enforcing or echoing that local id downstream

Without that clarification, the memo implies a stronger guarantee than the code actually provides.

### 2. Medium: `/compose-from-intent` URL proof alone is insufficient because planner continuity lives in navigation state, not in query params

The memo correctly requires `/compose-from-intent` URL/query proof (`communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_scope.md:150-153`), but that is not enough to prove the counted planner-primary branch by itself.

`AoiComposeFromIntentPage` reads the two source ids from query params, but the planner-backed continuation depends on `location.state` for:

- `plannerBackedLaunch`
- `plannerSelectedSources`
- `plannerSelectionSummary`
- `plannerResolvedIntentSeed`

See `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:238-259`.

If the compose page is refreshed after navigation, the URL still preserves both source ids, but the planner selection state is gone. That means a bare URL capture does not prove the counted planner-primary handoff survived into the page strongly enough to support the `compose-from-selection` continuation.

There is a second nearby risk: the non-counted profile/autostart path is still live, and the autostart branch explicitly strips `source_v2_job_id` before calling `composeFromSource(...)` (`/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:470-477`). The panel tests also intentionally preserve the looser normal path where dossier launch can navigate with `source_analysis_id` and no `source_v2_job_id` (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:449-485`).

So the memo is right to exclude profile/autostart and `compose-from-source`, but it should require proof of actual planner-backed compose-page state or the actual host `compose-from-selection` request body, not just the landing URL.

### 3. Medium: the rerun is the right next step, but the memo should say more explicitly that the live browser seam itself still needs to be re-earned

The repair is real in code:

- canonical local snapshot resolution and reuse now converge via `v2_run_references` (`/home/evgeny/projects/the-critic/api/server.py:18855-18953`, `/home/evgeny/projects/the-critic/api/server.py:19361-19416`, `/home/evgeny/projects/the-critic/api/server.py:19618-19697`)
- AOI listing now prefers canonical rows for one upstream `v2_job_id` (`/home/evgeny/projects/the-critic/api/server.py:18644-18730`, `/home/evgeny/projects/the-critic/api/server.py:20964-20972`, `/home/evgeny/projects/the-critic/api/server.py:21592-21600`)
- `Clear` now invalidates the active source and planner state until explicit reselection (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:975-981`)

Focused verification also passed during this audit:

- `pytest -q /home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py` -> `51 passed`
- `CI=true npm --prefix /home/evgeny/projects/the-critic/webapp test -- --runInBand --watchAll=false src/components/influence/AoiV2ThematicPanel.test.tsx src/lib/boundedV2Client.test.ts src/pages/AoiComposeFromIntentPage.test.tsx src/lib/composeFromIntentClient.test.ts` -> `106 passed`

The important limit is evidence quality, not code shape. The last failed browser artifact still shows:

- auto-loaded presentation visible
- `Clear` fired
- no planner requests
- no compose requests
- timeout waiting for `.aw-saved-item`

See `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_precompose_pin_2026-03-26.json` and `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_requests_2026-03-26.json`.

That means the memo is right that the next honest move is a rerun, not more repair. But the closeout bundle must prove the repaired live browser seam itself:

- saved-results list visible after `Clear`
- explicit row click on the recovered source
- planner-backed continuation from that row

One browser success without that full chain would still be over-reading the repair.

## Direct Answers

### 1. Does the codebase support the memo’s claim that the next honest move is a rerun, not more repair?

Yes.

The host-side idempotence repair is implemented and route/UI coverage now exists for:

- repeated completed-job detail reuse
- repeated and concurrent `cache-v2` convergence
- repeated and concurrent `refresh-v2` convergence
- canonical-results listing preference
- post-`Clear` explicit reselection before planner launch

That is enough to say the next honest unknown is the repaired live browser seam, not another repair tranche by default.

### 2. Is the identified counted-source rule technically correct?

Partially, with one required clarification.

Correct:

- anchor counted truth on upstream `source_v2_job_id = job-6ee8b0621177`
- preflight-resolve the current canonical local `analysis_id`
- require the host/browser artifacts to keep that exact local id stable through row pinning, warmup, `/compose-from-intent`, and the host `compose-from-selection` request

Not fully correct as currently phrased:

- `source_analysis_id` is not an analyzer-side end-to-end invariant today
- the host compose route does not enforce that the submitted `source_analysis_id` equals `v2_run_references.local_snapshot_analysis_id`

So the rule is technically sound only if the memo names `source_analysis_id` as a host-local continuity selector rather than as downstream analytical truth.

### 3. Is the memo appropriately strict about source continuity, or does it still leave room for silent drift?

It is mostly strict, but it still leaves room for silent drift unless revised in two places:

- require proof of planner-backed compose-page state, not just `/compose-from-intent` URL params
- require the host `compose-from-selection` request artifact itself to show both ids and the planner-selected sources

Without those revisions, the memo is still vulnerable to:

- a stale same-job local alias passing the proxy route
- a compose page reload preserving source ids in URL while losing planner selection state

### 4. Are there hidden cases the memo is missing?

Yes, two materially:

- `source_analysis_id` can drift from canonical local row while still matching the same `source_v2_job_id`; the proxy route will accept that
- `/compose-from-intent` URL continuity does not prove planner continuity, because planner selection state lives in navigation state, not query params

I did not find a new blocker in the specific “job detail fixed but results listing still drifts” case. The listing route is explicitly wired to prefer `v2_run_references.local_snapshot_analysis_id` (`/home/evgeny/projects/the-critic/api/server.py:18675-18679`, `/home/evgeny/projects/the-critic/api/server.py:20964-20972`, `/home/evgeny/projects/the-critic/api/server.py:21592-21600`).

I also did not find evidence that more host repair is already required before rerun. The remaining gap is live browser proof.

### 5. Is keeping the recovered upstream run `job-6ee8b0621177` as the fixed counted source still the right sequencing decision after the repair?

Yes.

The recovered run is still the cleanest counted source:

- it is already execution-backed and durably queryable (`communications/PROOF_stage5_aoi_evolution_ready_execution_backed_recovery_summary_2026-03-25.json`)
- the roadmap already treats the rerun on this source as the next bounded step (`communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:193-196`, `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:238-239`)
- launching another AOI run now would widen documentary ambiguity without answering the repaired-browser question first

### 6. Does the memo keep the roadmap honest?

Yes.

It matches the current roadmap state:

- Stage 5 seam gate already passed on fixture-backed evidence (`communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1177-1180`)
- Stage 2 is still open until this rerun is graded honestly (`communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:195`)
- Tranche 3 remains blocked until that decision is explicit (`communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:196`)

### 7. Does this memo put the grading burden on the real seam, or does it still over-infer closure from one browser success?

Mostly on the real seam.

Decision 6 already forces explicit re-grading against the frozen rubric and asks whether one repaired recovered-case success is enough for repeated bounded AOI transient use (`communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_scope.md:156-169`).

That is the right framing.

The remaining over-inference risk is narrower: the memo still needs tighter artifact requirements so a single browser success cannot be counted unless it proves:

- canonical local row continuity at the host boundary
- planner-backed compose-page continuity
- actual `compose-from-selection` request on the counted source

## Recommended Memo Revisions

1. Revise the identity rule so it explicitly distinguishes the two identities:
   - `source_v2_job_id` is the counted end-to-end source truth.
   - `source_analysis_id` is the repaired host-local continuity selector that must stay stable through AOI panel selection, warmup result, `/compose-from-intent`, and the host `compose-from-selection` POST body.
   - Do not imply that analyzer-v2 will preserve or echo the local id.

2. Tighten the pre-compose proof requirement:
   - Require one artifact from the compose page itself showing planner-backed selection summary is present after navigation.
   - The URL alone is not enough because planner continuity lives in navigation state.

3. Tighten the request artifact requirement:
   - Require the captured host `/api/analysis/anxiety_of_influence_thematic_single_thinker/projects/{project_id}/compose-from-selection` request body to show:
     - `source_v2_job_id = job-6ee8b0621177`
     - `source_analysis_id = <preflight canonical local id>`
     - the exact planner-selected source families
   - Treat analyzer-side payload/content proof as required only for `source_v2_job_id`, not for `source_analysis_id`.

4. Keep the current sequencing language:
   - no new AOI launch by default
   - no new repair tranche by default
   - rerun on `job-6ee8b0621177` is still the right next move

## Bottom Line

The memo is directionally correct.

The repair looks landed, the rerun is now the right next step, the recovered upstream run remains the right counted source, and the roadmap/status claims are honest.

The main revision needed is technical precision: upstream `source_v2_job_id` continuity is truly enforced end to end; local `source_analysis_id` continuity is only enforceable at the host/browser boundary today, so the rerun artifacts must prove that boundary explicitly.
