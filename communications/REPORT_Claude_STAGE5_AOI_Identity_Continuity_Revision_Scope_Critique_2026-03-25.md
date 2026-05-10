# Critique: Stage 5 AOI Identity Continuity Revision Scope

Date: 2026-03-25
Reviewer: Claude (Opus 4.6)
Memo under review: `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_scope.md`

---

## Verdict: Approve

The memo correctly identifies the next blocker, scopes the fix narrowly, and avoids smuggling in broader work. One finding below deserves attention before implementation but does not change the verdict.

---

## Findings

### Finding 1 (Medium): The `cache_v2_presentation` warmup path already tries to persist thinker identity — the problem is upstream of warmup

Severity: Medium — affects implementation strategy, not scope approval.

The memo frames the problem as "snapshot warmup does not persist AOI thinker identity." The code tells a slightly different story.

`cache_v2_presentation` at `the-critic/api/server.py:20001-20016` already passes `selected_source_thinker_id` and `selected_source_thinker_name` through to `_save_v2_presentation_to_db`, but only if `run_ref is not None` and the run_ref itself has those fields populated. The `_build_v2_presentation_record` function at `:18925-18941` conditionally includes the thinker fields only when truthy.

The diagnostic evidence confirms the warmed snapshot had blank thinker identity fields. But the code path for `cache_v2_presentation` is:
1. Look up `V2RunReferenceDB` by `v2_job_id`
2. Read `selected_source_thinker_id` from that run_ref
3. Pass it to the presentation save

So the actual root cause is one of:
- (a) No `V2RunReferenceDB` record exists locally for the proof job `proof-round5-adaptive-aoi-dossier-final-1774100000`, or
- (b) The run_ref exists but its `selected_source_thinker_id` column is NULL

The proof job was likely imported or seeded without AOI thinker identity on the V2RunReferenceDB row, because the original import/execution path for genealogy-style jobs did not always populate those fields.

**Implication for implementation**: The fix may not need to change warmup logic at all. It may need to ensure the V2RunReferenceDB record for the source job has AOI thinker identity populated — either at import time, or via a backfill when the planner resolves the AOI source. The implementor should diagnose this fork before coding.

### Finding 2 (Low): The `_matches_saved_aoi_result_context` validation path is strict by design — the memo is right that the gap is identity persistence, not validation logic

`_matches_saved_aoi_result_context` at `:18721-18730` does `_extract_saved_thinker_identity(pass_results)` and checks equality against the requested `thinker_id`. If `pass_results` has no `selected_source_thinker_id` key, extraction returns `None`, which never equals the requested thinker_id, producing the 409.

This is correct validation behavior. The memo is right to frame the fix as data-plumbing, not validation relaxation.

### Finding 3 (Low): The `_resolve_source_backed_compose_identity` fallback chain has a second path through `source_v2_job_id` that might bypass the broken `source_analysis_id` path — but the frontend doesn't use it in this flow

The compose page (`AoiComposeFromIntentPage.tsx:232-233`) reads both `source_analysis_id` and `source_v2_job_id` from URL params. In the diagnostic proof (`PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json:12`), the final URL shows `source_analysis_id=gen-v2-c03d584f4a4f` but no `source_v2_job_id` param.

The `_resolve_source_backed_compose_identity` function at `:18790-18874` has a fallback path: if only `source_v2_job_id` is provided (no `source_analysis_id`), it goes through `_validate_source_compose_run_reference` which checks the V2RunReferenceDB directly. That path would fail for the same root cause (missing thinker identity on run_ref), but it's worth noting for the implementor that fixing the identity on the run_ref might unblock both paths simultaneously.

### Finding 4 (Low): Regression coverage requirement is good but slightly under-specified on which test project owns the coverage

The memo requires backend tests proving warmup preserves thinker identity and compose validation accepts it. These tests live in `the-critic`, not in `analyzer-v2`. The memo's Decision 5 doesn't explicitly state which repo gets the tests. Since the identity continuity seam is entirely host-side, all new regression tests should live in `the-critic/tests/test_aoi_v2_routes.py` (which already has 1400+ lines of relevant coverage, including `_resolve_source_backed_compose_identity` tests at `:534-568`). The memo should clarify this.

### Finding 5 (Informational): No hidden dependency that would make this slice less meaningful

I checked:
- The planner/selector repair is landed and proven by the diagnostic (`timeout_s=45`, `max_retries=0`, `provider_outcome=success`). No reason to reopen that.
- The frontend compose page correctly propagates `source_analysis_id` from URL params. No frontend-side identity loss.
- The `_build_v2_presentation_record` and `_save_v2_presentation_to_db` code paths are straightforward — the thinker identity fields are simply absent in the data, not corrupted.
- There is no evidence of a Tranche 3 dependency or lifecycle dependency hiding in this seam.

### Finding 6 (Informational): The memo is honest about what this does and does not buy

The memo explicitly says:
- Does not imply Stage 5 is close to passing
- After continuity is fixed, `selection_fit`, usefulness, or render-path issues may surface
- The rubric, pack, and Stage 2 bar are unchanged

This is the right epistemic posture. The completion condition (":145-147") requiring either a successful diagnostic + rerun or a fresh revision memo is appropriately honest.

---

## Answers to Specific Questions

### 1. Is the memo correctly narrowing to host-side identity continuity rather than reopening selector/provider work?

**Yes.** The diagnostic proof is unambiguous: `provider_outcome=success`, `timeout_s=45`, `exception_class_name=null`. The selector/provider path is healthy. The 409 failure is downstream in the compose validation path. Reopening selector work would be scope creep.

### 2. Does the codebase evidence support the memo's claim that the blocker is specifically snapshot warmup / persisted identity / compose validation continuity?

**Yes, with a nuance.** The blocker is specifically that `V2RunReferenceDB.selected_source_thinker_id` (or equivalently `pass_results.selected_source_thinker_id` on the generated local snapshot) is not populated for the proof source job. The warmup code at `server.py:20014` reads from `run_ref.selected_source_thinker_id`, which is NULL. The code path is clear and the fix surface is narrow.

### 3. Is the memo honest about what this slice does and does not buy?

**Yes.** The memo is explicitly honest that the frozen rerun may still surface other issues. It does not claim Stage 5 passage or Stage 2 closure.

### 4. Is the regression-coverage requirement strong enough?

**Mostly yes.** The memo's three coverage requirements (warmup persists identity, compose accepts warmed snapshot, truth in both `pass_results` and `v2_run_references`) are the right tests. The gap is that it doesn't specify which repo/test file owns them. Recommendation: add a note that these tests belong in `the-critic/tests/test_aoi_v2_routes.py`.

### 5. Does the memo preserve the right program order?

**Yes.** The memo explicitly:
- Keeps the rubric and case set frozen (Decision 1)
- Does not reopen planner/selector work (Decision 3)
- Does not begin Tranche 3
- Does not change the Stage 2 closure bar
- Treats this as a recalibration of the immediate plan, not a pivot

### 6. Is there any hidden dependency that would make this slice less meaningful?

**No.** The identity continuity gap is self-contained in the host-side warmup/persist/validate chain. Fixing it unblocks the compose path without requiring changes to analyzer-v2, the planner, or the frontend compose page.

### 7. Does the memo stay appropriately bounded?

**Yes.** The out-of-scope list is complete. There is no accidental smuggling of Tranche 3, lifecycle, or architectural work. The fix surface is one seam: how thinker identity propagates from the V2RunReferenceDB through snapshot warmup into the local `pass_results` that compose validation reads.

---

## Program Sequencing Recommendation

The program should:
- **Update the roadmap slightly**: Record that the Stage 5 blocker has moved from selector/provider to host identity continuity. One line in the status ledger.
- **Recalibrate the immediate plan**: This slice is the next step. After it, repeat the diagnostic + frozen rerun.
- **Not pivot phases**: Stage 5 → Stage 2 → Tranche 3 order is preserved.

---

## Concrete Revision Recommendations

1. **Clarify the root cause fork for the implementor**: Add a note to the memo (or the implementation handoff) that the implementor should first check whether the V2RunReferenceDB record for `proof-round5-adaptive-aoi-dossier-final-1774100000` exists locally and whether its `selected_source_thinker_id` is populated. The warmup code already propagates from run_ref — if the run_ref is empty, the fix is ensuring the run_ref has identity, not changing warmup logic.

2. **Specify test ownership**: Add that regression tests for this seam belong in `the-critic/tests/test_aoi_v2_routes.py`, not in `analyzer-v2`.

These are implementation-guidance clarifications, not scope changes. The memo is approved as-is for implementation.
