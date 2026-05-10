# Audit: Stage 5 AOI Snapshot Durability Revision Scope

Date: 2026-03-25
Reviewer: Codex
Memo under review: `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md`

## Verdict

Approve with revisions.

## Findings

### 1. High: the regression section still does not force proof of the real durability bug

The memo correctly asks for coverage of `save failure / non-persisted returned id` and `planner-backed warmup failure stopping before compose navigation` (`communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md:107-120`). But the current host tests that exercise `cache_v2_presentation` still patch `_save_v2_presentation_to_db` away entirely in `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:640-658` and `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:684-702`, so they cannot catch the exact phantom-id behavior described in the diagnostic (`communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md:120-131`).

The frontend side has the same proof gap. The planner-backed happy path is covered in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:434-500`, and a generic warmup rejection path is covered in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:1085-1112`, but there is no planner-backed test proving that a warmup response with no `analysis_id` stays on the panel and never navigates.

Implication: as written, the memo could still be implemented with another mock-heavy green suite that misses the actual failure mode.

Recommended revision before implementation:

- require at least one unmocked backend regression that exercises the real `_save_v2_presentation_to_db(...)` failure path, or tests that helper directly, and proves both `analysis_id` omission and no bad `local_snapshot_analysis_id` mutation
- require one planner-backed frontend regression where warmup returns no `analysis_id` and `Continue with planned composition` does not navigate

### 2. Medium: the fail-closed contract needs to be stated at the shared helper level, not only at the counted planner-backed path

The diagnosis is right that the first broken hop is `_save_v2_presentation_to_db(...)` (`communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md:47-55`). But that helper is not warmup-only. It is used by:

- import path in `/home/evgeny/projects/the-critic/api/server.py:19965-19989`
- refresh fallback path in `/home/evgeny/projects/the-critic/api/server.py:20060-20068`
- warm snapshot cache path in `/home/evgeny/projects/the-critic/api/server.py:20133-20151`

The memo’s Decision 2 is phrased around the planner-backed AOI path (`communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md:57-66`). That is the counted Stage 5 path, but the same warmup helper is also used by the ordinary profile launch, and that non-planner path still omits canonical `source_v2_job_id` in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:723-758`, with the omission explicitly test-enshrined in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:396-431`. The compose page autostart path also strips `source_v2_job_id` before `compose-from-source` in `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:452-477`.

Implication: if the implementor reads the memo as “add planner-backed UI gating” instead of “fix the helper contract so it never returns a lie,” a synthetic `source_analysis_id` can still leak on the non-counted path.

Recommended revision before implementation:

- say explicitly that `_save_v2_presentation_to_db(...)` must never return an `analysis_id` unless the row is durably present, for any caller
- keep the Stage 5 proof obligation planner-backed, but make the save-truth contract global to the helper and warmup route

### 3. Medium: the memo classifies the SQLite lock correctly, but it understates the chance that fail-closed-only will leave the rerun unstable

The diagnosis memo records repeated `database is locked` failures during the same window as the phantom id (`communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md:105-123`). The current helper opens a direct SQLite connection and does a single write attempt before swallowing the exception and returning the pre-generated id in `/home/evgeny/projects/the-critic/api/server.py:19047-19138`.

So Decision 4 is right that this is still a bounded host continuity problem (`communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md:78-85`). But if the only change is “return no id on failure,” the silent corruption becomes a visible intermittent launch failure at whatever rate lock contention continues to occur.

Implication: that is still the right immediate slice, but the memo should acknowledge the bounded possibility that a small contention-reduction measure may be needed inside the same repair if the rerun is to be meaningfully stable.

Recommended revision before implementation:

- add one sentence under Decision 4 saying the implementor should evaluate whether a bounded retry/backoff, serialization, or SQLite-mode check is needed alongside fail-closed behavior

## Direct Answers

### 1. Does the codebase evidence support treating warm snapshot save truth as the first broken hop?

Yes.

The proof artifact shows a planner-backed `compose-from-selection` request carrying both the synthetic `source_analysis_id` and the canonical `source_v2_job_id`, followed by `404 Saved AOI result not found` in `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json:13-23` and `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json:752-798`. The diagnosis memo then ties that exact failure to `_save_v2_presentation_to_db(...)` generating the id before the DB write and still returning it after a lock failure in `communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md:99-131`. The code confirms that behavior in `/home/evgeny/projects/the-critic/api/server.py:19047-19138`, and the warmup route commits that returned id into `run_ref.local_snapshot_analysis_id` in `/home/evgeny/projects/the-critic/api/server.py:20133-20151`.

So the first broken hop is warm snapshot save truth, not selector/provider and not the earlier identity-continuity seam.

### 2. Is the proposed fail-closed behavior strong enough, or is there still a path where a synthetic/non-durable `source_analysis_id` could leak into compose?

It is strong enough only if implemented at the helper/route contract level.

If the fix is truly “no durable row, no returned id,” then both the planner-backed path and the shared warmup helper fail closed. If the fix is read more narrowly as “stop planner-backed navigation on warmup failure,” a synthetic id can still leak on the ordinary profile/autostart route, because that path still uses `warmSnapshotForSource(...)` while omitting `source_v2_job_id` in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:723-758`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:396-431`, and `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:452-477`.

So the memo should be revised to make the helper-level fail-closed guarantee explicit.

### 3. Is the memo right to keep selector/provider and identity continuity out of scope by default?

Yes.

The current proof trail shows `timeout_s = 45`, `max_retries = 0`, `provider_outcome = success`, and preserved `source_v2_job_id` in the counted planner-backed request in `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json:19-32` and `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json:752-787`. That matches the current analyzer selector implementation in `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py:727-805` and the current identity-resolution path in `/home/evgeny/projects/the-critic/api/server.py:18871-18977`.

The focused suites are also green in the current workspace:

- `PYTHONPATH=. pytest -q tests/test_task_planner.py` -> `16 passed`
- `PYTHONPATH=. pytest -q /home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py /home/evgeny/projects/the-critic/tests/test_aoi_v2_client.py` -> `47 passed`
- `CI=true npm --prefix /home/evgeny/projects/the-critic/webapp test -- --runInBand --watchAll=false src/components/influence/AoiV2ThematicPanel.test.tsx src/pages/AoiComposeFromIntentPage.test.tsx src/lib/boundedV2Client.test.ts` -> `89 passed`
- `/home/evgeny/projects/the-critic/webapp/node_modules/.bin/tsc -p /home/evgeny/projects/the-critic/webapp/tsconfig.json --noEmit` -> passed

That is enough to keep selector/provider and identity continuity closed baseline for this slice.

### 4. Are the regression obligations concrete enough to prove:

- save failure does not return a bogus id
- planner-backed navigation does not continue after warmup failure
- repeated warmup/latest-snapshot continuity stays repaired

Not yet.

They name the right behaviors in `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md:107-120`, but they do not yet force the right proof shape. The current backend warmup tests still mock away `_save_v2_presentation_to_db(...)` in `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:640-658` and `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:684-702`, while the current frontend warmup failure test is generic rather than planner-backed in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:1085-1112`. Repeated latest-snapshot continuity is already covered for the identity chain in `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:764-810`, but not for the real save-failure seam.

So the obligations are directionally right but need the revisions in Findings 1 and 2 to become audit-strong.

### 5. Is the rerun branch rule still strict enough to stop dishonest consumption of the frozen Stage 5 pack?

Yes.

The current scope memo says to rerun the same diagnostic first, consume the frozen pack only if that passes end to end, and stop again on any new downstream seam in `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md:96-101` and `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md:140-151`. That remains consistent with the authoritative diagnosis note’s stop decision in `communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md:147-166`.

### 6. Does the revised roadmap now tell the truth about how far along the program really is?

Yes.

The draft roadmap explicitly keeps Tranche 2 in front of Tranche 3, says Stage 5 is still in progress, says Stage 2 remains open, and says the immediate next step is one bounded warm-snapshot repair slice in `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:180-194` and `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:228-236`. The canonical roadmap says the same thing in `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1177-1180` and `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1285-1294`.

So the new progress read is honest, not overstated.

### 7. Is there any hidden dependency or code-path wrinkle that makes the next slice riskier, narrower, or broader than the memo claims?

Yes, three:

- `_save_v2_presentation_to_db(...)` is a shared helper with three callers, so the real contract is slightly broader than “warmup route only” even though the counted Stage 5 path is warmup-centered
- the non-planner profile/autostart path still omits canonical `source_v2_job_id`, so the memo must describe helper-level fail-closed behavior, not only planner-backed gating
- the lock contention root cause may still need a small bounded mitigation or the rerun may become visibly flaky rather than silently corrupt

None of those wrinkles justify reopening analyzer-v2 scope or changing roadmap order. They do justify tightening the memo before implementation.

## Program Decision

The program should:

- keep the roadmap order
- keep Tranche 3 blocked
- treat the current progress read as honest rather than overstated

This remains blocker-retirement inside one still-open exemplar gate, not evidence that the larger platform is near done.

## Recommended Revisions Before Implementation

1. Under deliverables/regressions, require one unmocked backend save-failure test that exercises the real `_save_v2_presentation_to_db(...)` seam and proves no returned id plus no poisoned `local_snapshot_analysis_id`.
2. Under deliverables/regressions, require one planner-backed frontend test where warmup returns no `analysis_id` and `Continue with planned composition` does not navigate.
3. In Decision 2 or Decision 3, state explicitly that the fail-closed save-truth contract applies to every caller of `_save_v2_presentation_to_db(...)`, even though only the planner-backed path counts for Stage 5 proof.
4. In Decision 4, add one sentence requiring the implementor to evaluate whether a bounded contention-reduction measure is needed alongside fail-closed behavior.
