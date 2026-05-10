# Memo: Stage 5 AOI Snapshot Durability Revision Scope

Date: 2026-03-25
Status: Draft scope memo for implementation review
Program: Dynamic Bespoke Apps Platformization
Depends on:
- `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_diagnostic_stop_completion.md`
- `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_completion.md`
- `communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_revision.md`
- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json`
- `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_session_2026-03-25.har`

## Summary

The fresh post-identity-repair `evolution_ready` diagnostic proves that:

- selector/provider repair is holding
- planner-backed compose is staying on `compose-from-selection`
- canonical `source_v2_job_id` is preserved
- the old AOI identity-continuity `409` is no longer the blocker

The new blocker is narrower:

- the host warm snapshot path can return a generated `source_analysis_id` that is not durably queryable during compose

That means the next honest step is one bounded `the-critic` repair slice on warm snapshot durability, then the same `evolution_ready` diagnostic again before any frozen rerun.

## Bounded Claim

This slice should only fix:

- warm snapshot save durability
- returned `source_analysis_id` truth
- compose lookup continuity when local save fails or SQLite is locked
- the planner-backed warmup failure path that should stop before compose navigation if local save truth cannot be established
- any bounded lock-contention mitigation needed so fail-closed behavior does not merely convert silent corruption into repeated visible warmup failures

This slice should not reopen:

- analyzer selector/provider behavior
- AOI planning law
- AOI identity continuity / `source_v2_job_id` handoff
- the frozen Stage 5 pack or rubric

## Scope Decisions

### Decision 1: Treat warm snapshot save truth as the first broken hop

The diagnostic evidence points first to host warm snapshot persistence, not to planner logic and not to compose identity resolution.

The immediate seam to fix is:

- `_save_v2_presentation_to_db(...)` and the surrounding warmup path in `the-critic`

This is the first broken hop because the current code can return a generated `analysis_id` even when the DB write fails.

The fail-closed rule should be stated at the shared helper level, not only at the counted planner-backed AOI path, because that helper is also used by adjacent host save paths.

### Decision 2: Fail closed on warm snapshot persistence

On the planner-backed AOI path, `the-critic` must not return or navigate with a `source_analysis_id` unless the corresponding `genealogy_analyses.id` row is durably present.

If warm snapshot save fails:

- do not hand the browser a synthetic `analysis_id`
- do not proceed into compose with that id
- surface a host-side warmup failure instead
- keep the user on the planner-backed AOI surface rather than navigating into `/compose-from-intent` with a bogus id

The same shared-helper law should also hold for the other current callers:

- import/save paths must not retain a synthetic `analysis_id` after a failed DB write
- refresh/save paths must not report a new persisted snapshot id unless the row is durably present

### Decision 3: Keep the repair inside `the-critic`

The evidence points to host persistence / lookup truth, not analyzer behavior.

So the slice should stay inside:

- local snapshot warmup / save path
- local compose identity resolution path
- direct regression coverage for save-failure continuity

### Decision 4: Treat DB lock as a bounded continuity problem, not as a new architecture question

The live proof trail already shows local `database is locked` warnings during warm snapshot save.

This slice should therefore harden the current host save path enough that:

- a lock-induced save failure cannot leak a bogus `source_analysis_id` into compose
- the same saved-result lookup path either resolves honestly or fails before compose navigation

The implementor should explicitly evaluate whether one bounded mitigation is needed so fail-closed behavior does not just turn the current bug into frequent visible warmup failures, for example:

- WAL mode if that is appropriate for the local SQLite setup
- or one very brief bounded retry around the local save path

This is still a continuity hardening question, not a lifecycle or architecture reopening.

### Decision 5: Preserve the repaired planner-backed path and reuse the same branch discipline

This slice should keep all of the already-repaired path assumptions fixed:

- selector/provider repair remains closed baseline
- planner-backed launch remains on `compose-from-selection`
- canonical `source_v2_job_id` remains preserved
- `compose-from-source` remains excluded from the counted path

After the repair:

1. rerun the same `evolution_ready` diagnostic
2. only if that succeeds end-to-end, rerun the same frozen four-case Stage 5 pack

If the diagnostic still fails on a new downstream seam, stop again and write a new revision memo rather than consuming the frozen rerun.

## Proposed Deliverables

### 1. Bounded host repair

- one `the-critic` code slice ensuring warm snapshot save truth and fail-closed behavior
- direct regression coverage for:
  - save failure / non-persisted returned id
  - returned warm snapshot id only when the row is durably queryable
  - repeated warmup continuity under the repaired path
  - latest-snapshot/default-resolution continuity after a repaired warmup
  - planner-backed warmup failure stopping before compose navigation
  - helper-level fail-closed behavior across the current save callers: warm snapshot, import, and refresh

Suggested regression ownership:

- backend: `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
- frontend handoff/error-path coverage as needed in:
  - `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`
  - `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts`

Regression discipline should be explicit:

- at least one backend save-failure regression must be unmocked enough to exercise the real `_save_v2_presentation_to_db(...)` path or an unmocked route path that reaches it
- the planner-backed no-navigation regression on warmup failure must be explicit on the frontend, not only inferred from request absence

### 2. Re-diagnostic artifacts

Reuse the existing `2026-03-25` diagnostic filenames for:

- HAR
- request JSON
- screenshot
- diagnosis note

The updated diagnosis note must explicitly say it supersedes the current `404`-hitting diagnostic if the repair succeeds.

### 3. Closeout outcome

Produce one of:

- a completion note that says the repaired path now earns the frozen rerun
- a revision note that says the repaired path still does not earn it

## Acceptance Criteria

This scope is successful only if one of these is true:

1. the repaired path passes `evolution_ready` end to end, proves warm snapshot durability truth on the counted planner-backed path, and the frozen rerun is honestly earned
2. the repaired path still exposes a new blocker, but the failure is documented with a new revision memo and the frozen rerun is still not consumed

The repair does **not** count as successful if:

- a non-persisted `source_analysis_id` is still returned
- the browser still navigates into planner-backed compose after warm snapshot failure
- the path succeeds only by falling back to `compose-from-source` or other legacy/debug controls
- the fix merely turns silent corruption into repeated visible warmup failures without any assessed lock-contention response

## Status Implications

Until this slice lands and the diagnostic is rerun successfully:

- Stage 5 remains `In progress`
- Stage 2 remains open
- Tranche 3 remains blocked
