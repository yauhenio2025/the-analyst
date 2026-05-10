# Critique: Stage 5 AOI Snapshot Durability Revision Scope

Date: 2026-03-25
Reviewer: Claude Opus 4.6
Target: `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md`

## Verdict

**Approve after revision**

The memo is honest, well-scoped, and correctly identifies the first broken hop. The evidence trail and the code both confirm the diagnosis. Three findings require revision before implementation; the rest are observations.

---

## Findings

### Finding 1 (HIGH): The memo is silent on the root cause of `database is locked` contention

The memo correctly treats `database is locked` as "a bounded continuity problem, not a new architecture question" (Decision 4). That framing is defensible for the scope of the fail-closed fix. But the memo does not address the root cause of the locking at all.

Code inspection confirms that `the-critic` uses SQLite with no evidence of WAL mode, no connection pooling discipline, and no retry logic for transient lock failures anywhere in the codebase. Warm snapshot saves happen concurrently during the same window that produces multiple sibling `gen-v2-*` ids (six siblings were present while the failing id was not). This strongly suggests write contention from overlapping warmup calls.

If the only fix is "return None when the write fails," the same contention pattern will cause intermittent warmup failures on every future planner-backed AOI launch. The fail-closed behavior converts a silent data corruption into a visible user-facing error, which is strictly better, but the user will then see warmup failures at whatever rate SQLite lock contention occurs.

**Recommended revision**: Add an explicit sub-decision acknowledging that the locking root cause may need a small bounded fix (e.g., enabling WAL mode, adding a brief retry with backoff, or serializing warm snapshot writes) alongside the fail-closed behavior. The memo does not need to mandate a specific fix, but it should at least state that a fail-closed-only fix may convert a silent bug into a frequent visible error, and the implementor should evaluate whether a small contention-reduction measure is warranted within the same slice.

### Finding 2 (MEDIUM): `_save_v2_presentation_to_db` is called from three sites, not just the warm snapshot path

Code inspection of `server.py` shows `_save_v2_presentation_to_db` is called from:

1. `cache_v2_presentation` route (~line 20133) — the warm snapshot path this memo targets
2. Genealogy v2 job import path (~line 19965) — stores the returned `analysis_id` as `local_snapshot_analysis_id`
3. Refresh path (~line 20060) — falls back to `_save_v2_presentation_to_db` when no existing rows match

The memo scopes the fix to "warm snapshot save durability" and "returned `source_analysis_id` truth." If the implementor fixes the function itself (to return `None` on write failure), callers 2 and 3 will also change behavior. Caller 2 (import path) sets `local_snapshot_analysis_id` from the return value, so a `None` return on failure would prevent a phantom id there too — which is correct behavior. Caller 3 (refresh path) already ignores the return value.

This is not a scope-expansion problem — fixing the function is the right move. But the memo should acknowledge the multi-caller surface explicitly so the regression pack covers all three callers, not just the warm snapshot path.

**Recommended revision**: Add a note under Deliverable 1 that the regression coverage should verify all callers of `_save_v2_presentation_to_db` behave correctly when it returns `None`, not just the `cache_v2_presentation` route.

### Finding 3 (MEDIUM): The existing backend test suite mocks `_save_v2_presentation_to_db` away

Code inspection of `test_aoi_v2_routes.py` confirms that every test exercising `cache_v2_presentation` uses `unittest.mock.patch` on `_save_v2_presentation_to_db`. This means:

- No test currently exercises the real DB write path
- No test detects the phantom-id return behavior
- No test exercises the `database is locked` scenario

The memo's regression list (Deliverable 1) asks for "save failure / non-persisted returned id" coverage. That is the right ask. But the implementor should know that the existing test infrastructure mocks the function, so the new tests will need to either:

- Test `_save_v2_presentation_to_db` directly with a real (test) database, or
- Test the full `cache_v2_presentation` route without mocking the save function

The memo should note this explicitly so the implementor does not add another mocked test that misses the same gap.

**Recommended revision**: Add a note under the regression section stating that existing tests mock `_save_v2_presentation_to_db` and that new save-failure regression tests must exercise the real function or an unmocked route path, not another mock-based test.

### Finding 4 (LOW): Frontend `warmSnapshotForSource` already has a guard for falsy `analysis_id`, but the server never triggers it

Code at `AoiV2ThematicPanel.tsx` line ~534 throws if `warmup.analysisId` is falsy:

```typescript
if (!warmup.analysisId) {
  throw new Error('Snapshot warmup completed without returning an analysis_id.');
}
```

This means the frontend already has a fail-closed path for "warmup succeeded HTTP-wise but returned no id." The problem is that the server currently always returns a truthy `analysis_id` even on DB failure, so this guard never fires.

Once the server is fixed to return `null`/omit `analysis_id` on write failure, the frontend guard will activate correctly. The frontend error-handling path (`handleTransientComposeLaunch` catch block) sets `pageError` and keeps the user on the panel.

This is good news for the memo's scope: the frontend half of the fail-closed behavior may already be structurally in place. The implementor should verify that the existing frontend error path is adequate rather than assuming new frontend work is needed.

### Finding 5 (LOW): No frontend test covers the `analysisId: undefined` warmup response

Neither `AoiV2ThematicPanel.test.tsx` nor `boundedV2Client.test.ts` tests the case where `cacheBoundedV2Presentation` returns `{ analysisId: undefined }`. The existing warmup-failure test covers the case where the HTTP call itself rejects (network error / non-200), but not the case where the HTTP call succeeds and returns no `analysis_id`.

The memo asks for "frontend handoff/error-path coverage as needed." This specific path should be explicitly called out.

**Recommended revision**: Add to the frontend regression ownership section: a test in `AoiV2ThematicPanel.test.tsx` proving that a warmup response with no `analysis_id` (server returns null/omitted on save failure) keeps the user on the panel without navigating to compose.

### Finding 6 (OBSERVATION): The `_resolve_source_backed_compose_identity` function already has correct fail-closed behavior

Code at `server.py` line ~18891 returns 404 when `source_analysis_id` is not found in the DB. This is the function that produced the observed `404 Saved AOI result not found: gen-v2-3834f733047a`. The downstream compose identity resolution is already fail-closed — the problem is entirely upstream (the phantom id being generated and returned before the write succeeds).

This confirms the memo's analysis: the fix surface is the save/return path, not the compose resolution path.

### Finding 7 (OBSERVATION): The `compose-from-selection` route does not need changes

The compose-from-selection route correctly delegates to `_resolve_source_backed_compose_identity`, which correctly fails closed on missing ids. No changes should be needed in the compose route itself. The memo is correct to scope the fix to the warm snapshot save path.

---

## Answers to Specific Questions

### 1. Does the evidence support treating warm snapshot durability as the first broken hop?

**Yes, strongly.** Both the diagnostic artifacts and the code confirm it. The planner succeeds, identity continuity succeeds, the browser navigates to compose — and then the compose lookup fails because `_save_v2_presentation_to_db` returns a pre-generated `analysis_id` even when the DB write fails. The six sibling ids that were present vs. the one missing id, combined with `database is locked` log entries, makes this a concrete and verifiable diagnosis. There is no reason to reopen planner or identity continuity.

### 2. Is the proposed repair slice honestly bounded?

**Yes, with a small caveat.** The core fix (don't return an `analysis_id` unless the row is durably present) is genuinely bounded. The caveat is Finding 1 above: if the `database is locked` contention itself is not addressed at all, the fail-closed fix will convert a silent bug into a frequent visible error. A brief WAL-mode or retry addition would still be bounded, and the memo should acknowledge that possibility.

### 3. Is the memo strict enough about fail-closed behavior?

**Yes.** Decision 2 is clear and well-specified. The four explicit "do not" clauses (don't hand the browser a synthetic id, don't proceed into compose, surface a failure, keep the user on the planner surface) form a complete fail-closed contract. The existing frontend guard (Finding 4) means the implementor may not need to write much new frontend code for this path.

### 4. Are the proposed regressions concrete enough?

**Yes, with one gap.** The five regression items in Deliverable 1 cover the right scenarios. The gap is that existing tests mock `_save_v2_presentation_to_db`, so the memo should explicitly require that new save-failure tests exercise the real function or an unmocked route (Finding 3). Additionally, the multi-caller surface (Finding 2) should be covered.

### 5. Is the roadmap update honest about progress?

**Yes.** The draft roadmap memo's progress estimates (75-85% for bounded AOI substrate, 55-65% for AOI exemplar ratification, 30-40% for full platform) are honest and well-calibrated. The Tranche 2 sequencing note correctly reflects the current state: the warm snapshot durability seam must close before the frozen rerun can be reconsumed, and Tranche 3 remains blocked. The memo count warning ("the memo count can make the program feel more complete than it is") is an important and accurate self-correction.

### 6. Does the memo preserve the right order?

**Yes.** The ordering is: fix bounded host seam -> rerun `evolution_ready` diagnostic -> only if that passes, rerun the frozen four-case pack -> do not pivot phases. This is the right sequencing. The acceptance criteria are strict: a non-persisted `source_analysis_id` still being returned, or the browser navigating into compose after warmup failure, both count as failures. The memo does not allow premature success claims.

### 7. Is there any hidden code-path wrinkle?

**Two minor wrinkles, neither blocking:**

1. The multi-caller surface for `_save_v2_presentation_to_db` (Finding 2). Fixing the function will affect the import and refresh paths too. This is correct behavior but should be tested.

2. The `database is locked` root cause (Finding 1). The warm snapshot flow creates multiple concurrent snapshots in the same window. If the implementor only adds fail-closed behavior without addressing contention, future launches will fail visibly at whatever rate SQLite lock contention occurs. The implementor should at least check whether WAL mode is enabled and consider a bounded retry.

No wrinkle makes the slice broader than the memo claims. No wrinkle suggests the wrong code surface is being targeted.

---

## Concrete Memo Revisions Recommended Before Implementation

1. **Decision 4 addendum**: Add language acknowledging that the `database is locked` root cause may need a small bounded fix (WAL mode, brief retry, or write serialization) alongside the fail-closed behavior. State that a fail-closed-only fix may convert a silent bug into a frequent visible error, and the implementor should evaluate whether a contention-reduction measure is warranted within the same slice.

2. **Deliverable 1 addendum**: Note that `_save_v2_presentation_to_db` has three callers and the regression pack should verify all three behave correctly when it returns `None`.

3. **Deliverable 1 regression note**: State that existing backend tests mock `_save_v2_presentation_to_db` and that new save-failure tests must exercise the real function or an unmocked route.

4. **Frontend regression addendum**: Add an explicit test case for the `warmup.analysisId` is falsy/undefined path in `AoiV2ThematicPanel.test.tsx`.

None of these revisions change the scope or sequencing. They make the implementor's job clearer and prevent the next test suite from having the same coverage gap that allowed this bug to persist.

---

## Summary

The memo is a well-disciplined scope document. It correctly identifies the broken hop, draws the right boundary around the fix, preserves the right sequencing discipline, and does not smuggle in a larger redesign. The roadmap assessment is honest. The four recommended revisions are all additive clarifications, not scope changes.
