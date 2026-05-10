# Memo: Stage 5 AOI Local Snapshot Idempotence Revision Scope

Date: 2026-03-26
Status: Draft scope memo for implementation review
Program: Dynamic Bespoke Apps Platformization
Depends on:
- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_revision.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_recovery_completion.md`
- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_recovery_summary_2026-03-25.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_precompose_pin_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_requests_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_session_2026-03-26.har`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_state_2026-03-26.png`
Roadmap sources:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

## Summary

The first counted browser-closeout attempt on the recovered fresh AOI run did not fail on planner law, compose routing, or upstream execution truth.

It failed on a narrower host seam:

- completed-job detail reads can mint a fresh local `analysis_id` for the same upstream `v2_job_id`
- repeated `cache-v2` warm/reuse requests can mint more fresh local `analysis_id`s for that same upstream run
- the saved-results list surfaces those duplicate local rows directly
- the AOI panel auto-loads the latest saved result by default

Together, those behaviors make explicit recovered-row pinning unstable enough that the counted browser proof cannot be written honestly.

So the next honest step is one bounded `the-critic` repair slice for local snapshot idempotence and stable saved-result identity for one upstream completed AOI run.

Important nuance:

- the host already has canonical-resolution helpers for local AOI snapshots and listing collapse
- the current failure is that those helpers are not acting as a true serialization boundary under concurrent traffic
- repeated concurrent `cache-v2` requests still race through canonical resolution and then each insert through separate sync DB connections

So this slice is not inventing canonicalization from scratch. It is making the existing canonicalization logic actually hold under concurrent browser/runtime behavior.

## Bounded Claim

This slice should only fix:

- canonical local snapshot reuse for one upstream completed `v2_job_id`
- completed-job detail backfill behavior for local snapshot ids
- `cache-v2` warm/reuse behavior for already-restorable runs
- refreshed-presentation update behavior for the canonical local row
- saved-results list stability for browser row pinning

This slice should not reopen:

- analyzer execution or presenter recovery
- AOI planning law
- compose-from-selection contract logic
- fresh AOI launch sequencing
- the frozen Stage 5 pack
- roadmap order

## Scope Decisions

### Decision 1: Treat one upstream `v2_job_id` as one canonical local snapshot identity

For the counted AOI browser path, one completed upstream run should converge on one durable reusable local snapshot id unless the mapped local row is stale or missing.

The canonical source for this slice remains:

- `source_v2_job_id = job-6ee8b0621177`

The repair should make host-local identity stable enough that:

- repeated completed-job detail reads return the same `analysis_id`
- repeated `cache-v2` requests return the same `analysis_id`
- the saved-results surface stops presenting many interchangeable local rows for the same upstream run

The canonical resolution logic already exists in `the-critic`.
This slice should harden that existing logic rather than layering a second competing notion of “canonical.”

### Decision 2: Make completed-job backfill idempotent before insert

The completed-job detail path currently backfills local snapshot ids through the shared host helper chain.

That path should become idempotent:

- if `v2_run_references.local_snapshot_analysis_id` exists and resolves, reuse it
- if that mapping is empty or stale, look for an existing persisted AOI local row for the same `v2_job_id` and current project context
- only insert a new local row if no durable row already exists for that upstream run

The critical rule is:

- reading a completed job must not mint a new local snapshot id when a valid one already exists

Root-cause diagnosis should be explicit in this slice:

- canonical lookup currently happens in the async SQLAlchemy session
- snapshot creation currently happens through a separate sync DB connection in `_save_v2_presentation_to_db(...)`
- under concurrent requests, multiple callers can all pass canonical lookup before any one insert becomes the agreed serialization point

Implementation should therefore treat `v2_run_references` as the serialization point for canonical local-row creation/reuse.

### Decision 3: Make `cache-v2` reuse the canonical local row instead of rematerializing

The warm/reuse route should follow the same idempotence law.

For an already-restorable upstream result:

- reuse the current durable local snapshot row when it exists
- if the mapping is stale, recover by locating the existing persisted row for the same upstream `v2_job_id`
- only create a fresh local row if no durable local row exists at all

This slice should keep the earlier durability rule intact:

- if no durable local row can be established, fail closed rather than returning a synthetic id

The memo should also acknowledge the traffic pattern that exposed the seam:

- the failed browser attempt recorded `34` successful `cache-v2` responses for the same `v2_job_id`

That concurrency/amplification factor is not a separate architecture problem, but the repair must actually hold under repeated route-level traffic rather than only under single-call unit tests.

### Decision 4: Refresh should update the canonical row, not widen duplication

The refresh/update path should not silently create additional local rows for the same completed upstream run when a canonical row already exists.

If a durable local row exists for the `v2_job_id`, refresh should update that row's persisted presentation payload rather than widening the duplicate set.

If no durable row exists, refresh may create one, but then it becomes the canonical row for later reads and warmups.

Refresh targeting should be exact-row based where possible:

- once canonical local `analysis_id` is known, refresh should target that row directly
- avoid broad JSON `LIKE` scans as the primary update mechanism for canonical-row refresh

### Decision 5: Address the existing duplicate/orphan row set explicitly

The current local DB state already contains many duplicate AOI local rows for the same upstream run.

This slice must state what happens to those rows for the affected source set, especially `job-6ee8b0621177`:

- either a bounded cleanup / demotion path is applied
- or the implementation explicitly leaves them in place but guarantees they no longer influence canonical identity, results listing, or counted browser proof

The closeout must document which choice was made and why that is sufficient.

### Decision 6: Saved-results output should be stable enough for explicit row pinning

The browser closeout does not need a new selection model, but it does need stable host output.

The saved-results surface should therefore stop exposing duplicate local rows for the same upstream `v2_job_id` as if they were distinct AOI sources.

At minimum, the AOI-facing results list used by the panel should collapse to one canonical entry per upstream `v2_job_id`, with deterministic ordering.

That keeps the existing explicit operator discipline meaningful:

- clear any auto-loaded presentation
- expose the saved-results list
- explicitly click the recovered row

The auto-loaded state still does not count as row pinning.
Results-list collapse alone is not enough; the browser rerun must still require deliberate row click-selection after clearing the auto-loaded presentation.

### Decision 7: Keep the counted browser source and roadmap order fixed

Do not launch a new AOI run by default in this slice.

The repair target is the recovered fresh execution-backed source already on record:

- `job-6ee8b0621177`

After the repair:

1. rerun the counted browser-closeout attempt on that recovered source
2. only then write the Stage 2 decision honestly

Do not consume the frozen four-case pack again as part of this slice.

### Decision 8: Put regression ownership on the actual churn seam

The main regression burden belongs on `the-critic`.

Required coverage should directly prove:

- repeated completed-job detail reads for one completed `v2_job_id` return the same `analysis_id`
- repeated `cache-v2` requests for one completed restorable `v2_job_id` return the same `analysis_id`
- refresh updates the canonical persisted row rather than widening duplicate local rows
- saved-results listing collapses duplicate local snapshot rows for one upstream `v2_job_id`
- the AOI browser path can clear auto-loaded presentation, explicitly click the recovered row, and preserve stable source identity through planner-backed handoff

Suggested ownership:

- backend:
  - `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
- frontend/browser-facing behavior:
  - `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`
  - `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts`

At least one backend regression should be unmocked enough to hit the real route behavior across repeated requests rather than only unit-testing helper internals.
At least one backend regression should also exercise repeated or concurrent route-level access strongly enough to prove the serialization rule actually holds under the traffic shape that produced the duplicate rows.

## Proposed Deliverables

### 1. Bounded host repair in `the-critic`

One code slice that makes local snapshot reuse idempotent for a completed AOI v2 run across:

- completed-job detail reads
- `cache-v2`
- refresh/update
- AOI saved-results listing used for browser row pinning

### 2. Focused regression coverage

Run and record focused verification for the repaired seam.

Suggested command set:

- `pytest -q tests/test_aoi_v2_routes.py`
- `CI=true npm --prefix ./webapp test -- --runInBand --watchAll=false src/components/influence/AoiV2ThematicPanel.test.tsx src/lib/boundedV2Client.test.ts`
- `./webapp/node_modules/.bin/tsc -p ./webapp/tsconfig.json --noEmit`

### 3. Re-closeout artifacts

After the repair, rerun the counted browser closeout against the recovered source and either:

- supersede the current revision memo with a completion memo
- or write a fresh revision memo if a new seam still appears

## Acceptance Criteria

This scope is successful only if one of these is true:

1. the repaired host paths converge on one stable local `analysis_id` for `job-6ee8b0621177`, the saved-results surface becomes stable enough for explicit row pinning, and the browser closeout is honestly earned on rerun
2. the repair still exposes a new blocker, but that blocker is documented with a new revision memo rather than hidden behind duplicate local rows

This slice does not count as successful if:

- repeated reads for the same completed `v2_job_id` still mint fresh `gen-v2-*` ids
- repeated `cache-v2` requests still widen local-row duplication
- saved-results output still exposes unstable duplicate rows for one upstream run
- the browser path still cannot prove explicit row pinning because host-local identity churn continues

## Status Implications

Until this slice lands and the browser closeout is rerun successfully:

- Stage 5 remains `In progress`
- Stage 2 remains open
- Tranche 3 remains blocked
