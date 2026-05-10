# Memo: Phase 0 / Phase 1A Completion

Date: 2026-03-19

## Purpose

This memo closes the immediate tranche defined as:

- Phase 0: Stage 9 closure tail
- Phase 1A: Critic bounded-v2 authority cleanup

It also records the final acceptance check for this tranche:

- manual restore-first verification in the generic `AnalysisWorkspacePage`
- manual AOI saved-result restore verification in the bounded AOI v2 surface

This memo sits beneath:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_snapshot_after_stage9.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_post_stage9_next_steps.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/PLAN_2026-03-18_thin_consumer_platformization_implementation.md`

## Scope Closed In This Tranche

### Phase 0

- Stage 9 tail items were converted from ambient residuals into explicit dispositions.
- The Stage 9 runbook now links the snapshot and next-step memos.
- The closure record is now discoverable from operational docs rather than only from scattered program notes.

### Phase 1A

- The Critic bounded-v2 backend path now treats durable stored upstream identity as the first-class authority path.
- `V2RunReferenceDB` is now the primary lookup surface for v2-backed job detail, cancel, and resume semantics.
- Critic-local in-memory state remains only as legacy/local compatibility for non-v2 jobs and imported-local aliases.
- Public route shapes were preserved.

### Explicit Non-Scope Kept

- No analyzer-v2 schema or API changes were made in this tranche.
- AOI launch UX was not added to `AnalysisWorkspacePage`.
- Frontend contract extraction was not started in this tranche.

## Completed Work

### Code / Docs Completed

- `/home/evgeny/projects/the-critic/api/server.py`
  - bounded-v2 detail / cancel / resume now resolve durable upstream identity first
  - refresh / cache paths prefer durable metadata where present
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
  - route coverage added for durable-ref-backed detail, cancel, resume, local compatibility, and imported-local alias behavior
- `/home/evgeny/projects/the-critic/docs/STAGE9_AOI_CUTOVER_RUNBOOK.md`
  - Stage 9 closure dispositions recorded explicitly
  - snapshot + next-step memos linked from the runbook/evidence surface
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_snapshot_after_stage9.md`
  - closure checklist converted to explicit fixed / waived dispositions

### Automated Verification Completed

- `pytest -q tests/test_aoi_v2_routes.py`
- Result: `25 passed`

## Manual Restore Verification

### Why This Verification Was The Right Acceptance Check

The tranche was explicitly restore-first.

So the final acceptance question was not "do more route tests pass?"
It was:

- can the generic workspace still restore a bounded v2 result after the host-thinning cleanup?
- can the AOI bounded surface still restore a saved result after the same cleanup?

### Verification Method

Manual verification was performed locally on 2026-03-19 against a disposable Critic setup:

- a disposable copy of the local Critic SQLite DB was prepared
- one AOI saved-result fixture was added to that disposable copy because the working local DB contained genealogy saved results but no AOI saved-result rows
- the local Critic API and webapp were then run against that disposable DB
- the analyzer-v2 URL was intentionally pointed at an unreachable local address during verification so the check would prove restore-first behavior from Critic-local saved presentations rather than depending on live upstream recovery

This means the final verification was stricter than a normal happy-path restore check:

- upstream optional fetches failed
- restore still succeeded from Critic-local saved state

### Verified Generic Workspace Restore

Route:

- `/p/markus-2/analysis/intellectual_genealogy`

Observed restored surface:

- `Gyorgy Markus`
- `Target Work Profile`
- `Conceptual Framework`

Outcome:

- restore succeeded
- the generic workspace rendered the saved bounded-v2 presentation with no page-level JavaScript exception

### Verified AOI Saved-Result Restore

Route:

- `/p/morozov-benanav-001/anxiety-of-influence/john-oneill/v2-thematic`

Observed restored surface:

- `John O'Neill`
- `V2 Thematic Analysis`
- `The Market: Ethics, Knowledge and Politics`

Outcome:

- restore succeeded
- the AOI bounded v2 surface rendered the saved presentation with no page-level JavaScript exception

### Local Verification Artifacts

Disposable local screenshots were captured during verification:

- `/tmp/restore-verification-genealogy.png`
- `/tmp/restore-verification-aoi.png`

These are local operator artifacts, not durable repo evidence.

## What This Verification Actually Proved

This tranche can now make the following narrower but defensible claim:

- bounded-v2 host thinning in The Critic did not break restore-first behavior for the generic workspace path
- bounded-v2 host thinning did not break restore-first behavior for the AOI bounded saved-result path
- Critic-local saved presentations remain sufficient to restore usable analysis surfaces even when optional upstream fetches are unavailable

## Residuals

Two residuals remain, but neither should block tranche closure.

### Residual 1: Upstream-Optional Console Noise

During the deliberately upstream-disconnected verification run, the pages still emitted console noise from optional fetch attempts:

- workflow metadata fetch
- view definition fetch
- analyzer-v2 discovery / refresh attempts
- design-token fetch

This did **not** prevent restore.
It does mean the current restore-first behavior is operationally correct but still noisier than an ideal thin-consumer steady state when upstream is unavailable.

### Residual 2: AOI Verification Used A Disposable Saved-Result Fixture

The local working DB had no AOI saved-result row available for direct restore verification.
So AOI verification used a disposable local saved-result fixture inserted into a disposable DB copy.

That is acceptable for tranche closure because:

- the route surface was real
- the frontend surface was real
- the verification exercised the actual restore code path
- the working DB was left intact after verification

## Acceptance Call

This tranche should be treated as:

- **accepted**
- **closed for Phase 0 / Phase 1A**

More precisely:

- code shape is accepted
- Stage 9 closure tail handling is accepted
- restore-first acceptance verification has now been completed

This should **not** reopen broad Stage 9 work.

## Recommended Next Move

Move forward into the next thin-consumer platformization step rather than extending this tranche.

The next sensible focus is:

- Deliverable B / Phase 2
- extract the repeated bounded-v2 consumer contract / host adapter behavior now that the authority boundary and restore-first proof are in place
