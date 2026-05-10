# Codex Audit: Stage 5 AOI Local Snapshot Idempotence Revision Scope

Date: 2026-03-26
Verdict: Approve with revisions

Reviewed against:

- `communications/MEMO_2026-03-26_stage5_aoi_local_snapshot_idempotence_revision_scope.md`
- the Stage 5 memo/proof trail named in the prompt
- the current `the-critic` implementation and targeted tests

## Findings

### 1. High: the seam diagnosis is right, but the memo is not implementation-safe unless it names a serialization rule for canonical-row creation

The memo correctly identifies the real seam: completed-job detail backfill, `cache-v2`, and duplicate saved-result rows were all widening host-local identity churn for one upstream `v2_job_id`, not exposing a planner/analyzer failure. The proof trail is explicit about the operational shape of the bug: `34` successful `cache-v2` responses and `81` local rows for `job-6ee8b0621177` (`communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_revision.md:67`, `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_revision.md:80`).

The current code already moved in the right direction by resolving a canonical local row before insert in `_resolve_canonical_local_snapshot_analysis_id(...)` and then reusing it from completed-job detail and `cache-v2` (`/home/evgeny/projects/the-critic/api/server.py:19182`, `/home/evgeny/projects/the-critic/api/server.py:19288`, `/home/evgeny/projects/the-critic/api/server.py:20575`). But `_save_v2_presentation_to_db(...)` still generates a fresh `gen-v2-*` id on every insert (`/home/evgeny/projects/the-critic/api/server.py:19418`), and `genealogy_analyses` still has no uniqueness constraint on the upstream job identity because `_v2_job_id` lives inside `pass_results` JSON (`/home/evgeny/projects/the-critic/api/models_db.py:2362`, `/home/evgeny/projects/the-critic/api/models_db.py:2370`, `/home/evgeny/projects/the-critic/api/models_db.py:2380`). Only `v2_run_references.v2_job_id` is unique (`/home/evgeny/projects/the-critic/api/models_db.py:2403`, `/home/evgeny/projects/the-critic/api/models_db.py:2409`).

So the memo is directionally correct but under-specified. A naive "check, then insert" implementation is still race-prone under the exact browser conditions that produced the churn. The memo should explicitly require either:

- serializing on `v2_run_references` before any new local snapshot insert, or
- an equivalent DB-backed uniqueness strategy

Without that revision, the proposed repair can still reproduce duplicate rows under concurrent warmups.

### 2. Medium: collapsing the results list is necessary, but it does not by itself make explicit row pinning honest

The memo is right that the saved-results surface cannot keep presenting many interchangeable local rows. Server-side AOI collapse is now present and conflict-safe (`/home/evgeny/projects/the-critic/api/server.py:18642`, `/home/evgeny/projects/the-critic/api/server.py:20670`, `/home/evgeny/projects/the-critic/api/server.py:21286`). That is the correct seam-level repair for duplicated rows.

But the current AOI panel still auto-loads the newest result on mount (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:517`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:852`) and still derives the active source as `currentSourceResult ?? savedResults[0]` (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:277`). After `Clear`, it only nulls `currentSourceResult` (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:973`), and the existing frontend regression proves the next compose launch falls back to the newest row again (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:1049`).

Directly: the memo is too optimistic when it says stable host output alone is enough for explicit row pinning. No broader contract rewrite is needed, but at least one of these must be added:

- a small UI guard that disables compose after `Clear` until a row is explicitly clicked, or
- a stricter browser-proof/test requirement that captures the explicit click and rejects fallback-to-latest behavior as non-counting

### 3. Medium: the memo should be sharper about exact-row refresh targeting and about whether orphan cleanup is in scope

The current refresh path already resolves canonical identity first and passes `analysis_id` into `_update_v2_presentation_in_db(...)` (`/home/evgeny/projects/the-critic/api/server.py:19537`, `/home/evgeny/projects/the-critic/api/server.py:20513`, `/home/evgeny/projects/the-critic/api/server.py:20532`), and the backend regression covering this passes (`/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:1277`).

That is the right implementation rule. The memo should state it explicitly because the helper still has a fallback wildcard branch when `analysis_id` is absent (`/home/evgeny/projects/the-critic/api/server.py:19567`, `/home/evgeny/projects/the-critic/api/server.py:19625`, `/home/evgeny/projects/the-critic/api/server.py:19643`). The memo also never says whether the pre-existing duplicate rows are cleaned up or merely hidden behind canonical selection. For this slice, hiding them behind deterministic canonical selection is acceptable, but that deferral should be stated plainly so dedupe is not confused with data repair.

### 4. Medium: regression ownership is on the right seam, but the test plan still lacks the one route-level repeated/concurrent proof the memo asked for

The targeted suites pass on the current tree:

- `pytest -q /home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
- `CI=true npm --prefix /home/evgeny/projects/the-critic/webapp test -- --runInBand --watchAll=false src/components/influence/AoiV2ThematicPanel.test.tsx src/lib/boundedV2Client.test.ts`
- `./webapp/node_modules/.bin/tsc -p ./webapp/tsconfig.json --noEmit`

The existing tests do cover canonical reuse, refresh-on-canonical-row, and AOI list collapse (`/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:683`, `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:1113`, `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:1170`, `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:1277`) plus the frontend duplicate-collapse and `Clear` fallback behavior (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:396`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:1049`).

But `tests/test_aoi_v2_routes.py` is still almost entirely helper-level and fake-session based; it does not exercise repeated real route calls through an ASGI client. Since the memo itself asks for at least one backend regression "unmocked enough to hit the real route behavior across repeated requests," that requirement is still not fully met.

### 5. Low: as a program-sequencing memo, this stays honest only if it is treated as a bounded host repair and not as a new architecture tranche

The broader roadmap judgment in the memo is sound. The code and memo trail still support:

- Stage 5 seam gate already passed on the frozen fixture-backed pack (`communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_scope.md:19`, `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md:128`)
- Stage 2 still open until the counted browser rerun is honestly re-earned (`communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_revision.md:27`)
- Tranche 3 still blocked (`communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:194`, `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:239`)

Keeping `job-6ee8b0621177` as the counted source remains the right sequencing decision. Another fresh AOI launch would add more naming churn without testing the seam that actually failed.

## Direct Answers

### Is the seam diagnosis technically correct?

Yes. The memo correctly identifies a host-local identity seam:

- completed-job detail backfill was capable of rematerializing local ids
- `cache-v2` warm/reuse was capable of rematerializing local ids
- duplicate local rows were destabilizing the saved-results surface

That diagnosis is supported by the proof trail and by the current canonical-resolution code in `/home/evgeny/projects/the-critic/api/server.py:19182`, `/home/evgeny/projects/the-critic/api/server.py:19288`, and `/home/evgeny/projects/the-critic/api/server.py:20575`.

### Is the proposed repair appropriately bounded?

Yes, with revisions. This remains a bounded `the-critic` host repair. It does not require analyzer contract changes, planner changes, or a new AOI selection model. But the bounded slice must explicitly include:

1. canonical-row serialization before any new local snapshot insert
2. exact-row refresh updates by canonical `analysis_id`
3. conflict-safe AOI results collapse
4. one browser-facing explicit-pin guard or proof requirement

### Does the repair need broader contract or UI work than the memo admits?

It does not need broader contract work. It does need a little more browser-facing work than the memo admits:

- either a tiny AOI-panel guard after `Clear`
- or stronger browser-proof/test discipline proving the explicit row click

That is still bounded host work, not a redesign.

### Is collapsing results to one canonical entry per upstream `v2_job_id` the right repair?

Yes, if it stays conflict-safe. The current server collapse preserves rows when thinker identities conflict instead of silently merging them (`/home/evgeny/projects/the-critic/api/server.py:18660`). That is the right balance: collapse duplicate AOI rows that are mechanically interchangeable, but do not hide real context conflicts.

### Are the memo’s hidden cases real?

Yes.

- stale `v2_run_references.local_snapshot_analysis_id`
  - handled by clearing stale mappings before canonical lookup (`/home/evgeny/projects/the-critic/api/server.py:19193`)
- refresh widening duplicates
  - handled only if refresh targets the canonical row (`/home/evgeny/projects/the-critic/api/server.py:20513`)
- project/thinker identity mismatch while reusing a canonical row
  - guarded in `/home/evgeny/projects/the-critic/api/server.py:18920`, `/home/evgeny/projects/the-critic/api/server.py:18986`, and `/home/evgeny/projects/the-critic/api/server.py:19155`
- existing tests that would break on deduped behavior
  - no break surfaced; the targeted backend/frontend suites passed

The hidden case the memo still underplays is concurrent duplicate creation under repeated `cache-v2` calls.

### Is keeping `job-6ee8b0621177` as the fixed counted source still the right decision?

Yes. The run remains the right counted source after this repair because it is the exact recovered execution-backed case whose host-local identity drift blocked the browser closeout.

### Does the memo keep the roadmap honest?

Yes. The memo preserves the correct program state:

- Stage 5 seam gate already passed
- Stage 2 remains open
- Tranche 3 remains blocked

The next honest step after this bounded repair is the counted browser rerun on the same recovered source, not a phase reorder.

### Does the memo put regression ownership on the real seam?

Mostly yes. Ownership belongs primarily in `the-critic` backend routes plus the AOI panel/browser seam. The test plan should stay there, but it should be strengthened with one repeated/concurrent real-route regression, not moved elsewhere.

## Recommended Memo Revisions Before Implementation

1. Add an explicit serialization rule: `v2_run_references` must be the canonical lock/mapping point before any new local snapshot insert.
2. Add an explicit rule that refresh updates by canonical `analysis_id`, not by wildcard `%v2_job_id%` matching.
3. State that server-side AOI results collapse is the primary fix and that orphan-row cleanup is deferred unless separately authorized.
4. Add one browser-facing requirement: after `Clear`, counted proof must not rely on fallback-to-latest behavior.
5. Expand regression requirements to include one route-level repeated or concurrent backend test, not only helper-level tests.

## Verification

Executed against the current `the-critic` tree:

- `pytest -q /home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
  - result: `49 passed`
- `CI=true npm --prefix /home/evgeny/projects/the-critic/webapp test -- --runInBand --watchAll=false src/components/influence/AoiV2ThematicPanel.test.tsx src/lib/boundedV2Client.test.ts`
  - result: `73 passed`
  - note: existing React `act(...)` warnings still appear in `AoiV2ThematicPanel` tests
- `./webapp/node_modules/.bin/tsc -p ./webapp/tsconfig.json --noEmit`
  - result: passed
