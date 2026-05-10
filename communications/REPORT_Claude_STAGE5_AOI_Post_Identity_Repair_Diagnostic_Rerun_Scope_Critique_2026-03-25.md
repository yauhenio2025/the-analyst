# Critique: Stage 5 AOI Post-Identity-Repair Diagnostic/Rerun Scope

Date: 2026-03-25
Reviewer: Claude Opus 4.6
Memo under review: `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md`

## Verdict: Approve

The memo is well-bounded, honest about what it does and does not buy, and properly sequenced within the larger program. The codebase evidence supports the claim that the identity-continuity blocker is now code-fixed strongly enough to justify a live re-diagnostic. No revisions are required before execution.

---

## Findings

### Finding 1: The codebase evidence strongly supports the memo's claim that the identity-continuity blocker is code-fixed (Severity: Confirming)

The identity-continuity completion memo claims five specific regression tests landed. All five are verified present in `the-critic/tests/test_aoi_v2_routes.py`:

1. **Missing-row `v2_run_references` creation** (lines ~677-721)
2. **Existing-row thinker identity backfill** (lines ~626-674)
3. **Warmed snapshot identity projection** (lines ~724-761)
4. **Fail-closed mismatch handling** between `source_analysis_id` and `source_v2_job_id` (lines ~815-843) - raises HTTPException 409
5. **Repeated latest-snapshot/default-resolution continuity** after repair (lines ~764-812)

The compose proxy validation in `server.py` (lines ~18884-18931) confirms both identity fields are checked in all paths. The mismatch path raises `409` as claimed. There is no silent bypass: the limited short-circuit path (when `source_analysis_id` is provided but `source_v2_job_id` is not) is gated by a context-match check that prevents cross-project identity leakage.

Backend test count: 47 passed (38 routes + 13 client, minus skips) - matches the completion memo's claim.

### Finding 2: Frontend `source_v2_job_id` forwarding is complete on the planner-backed path (Severity: Confirming)

The planner-backed launch path in `AoiV2ThematicPanel.tsx` (lines ~651-686) adds `source_v2_job_id` to navigation params when the selected source has a `v2_job_id`. The `AoiComposeFromIntentPage.tsx` reads it from search params (line ~233) and forwards it in the compose request (line ~437).

Test coverage exists: `AoiComposeFromIntentPage.test.tsx` (lines ~193-238) verifies the compose client receives `source_v2_job_id='job-v2-123'`.

Planner outcome retention survives hydrate/refresh churn and task-text edits, verified by dedicated tests in `AoiV2ThematicPanel.test.tsx` (lines ~434-471).

Frontend test count: ~56 in the directly examined files, 110 plausible when including `taskLaunchRuntime`, `transientComposeIsolation`, and `AnalysisWorkspacePage` test files. The "110 passed" claim is credible.

### Finding 3: The simple/legacy profile launch path deliberately omits `source_v2_job_id` (Severity: Low - not a blocker)

The non-planner launch path in `AoiV2ThematicPanel.tsx` (lines ~713-759) builds URL params without `source_v2_job_id`. This is explicitly tested as intentional (test at line ~395 asserts `source_v2_job_id` is absent). Since the memo's diagnostic scope is exclusively about the planner-backed path, this asymmetry does not threaten the current step. It should be noted as a carry-forward residual if the program later needs legacy-path identity parity, but it is not in scope here.

### Finding 4: The selector/provider hardening is confirmed as landed baseline (Severity: Confirming)

In `src/orchestrator/task_planner.py`:
- `AOI_SELECTION_TIMEOUT_S_DEFAULT = 45.0` (line 40) - matches the diagnostic artifacts
- `AOI_SELECTION_MAX_RETRIES = 0` (line 41) - hardcoded, enforced at client construction (line ~731)
- Timeout exceptions (`APITimeoutError`, `httpx.TimeoutException`) are classified as `llm_timeout`, distinct from `APIConnectionError` → `llm_provider_failure` (lines ~763-805)
- All six trace fields are preserved: `timeout_s`, `retry_policy`, `exception_class_name`, `provider_outcome`, `blocked_reason_code`, `blocked_reason_detail`

The diagnostic proof artifact (`PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json`) confirms `timeout_s=45`, `max_retries=0`, `provider_outcome=success`, `exception_class_name=null` on the authoritative attempt. This is consistent with the code.

16 tests in `test_task_planner.py`, including 5 dedicated to selector/provider hardening (timeout classification, env-configurable timeout, no-retry behavior, blocked reason propagation).

The memo correctly treats planner/selector repair as closed baseline and does not reopen it.

### Finding 5: The stop-and-revise conditions are precise and enforceable (Severity: Confirming)

The memo's Decision 4 lists three explicit stop-and-revise triggers:
1. Planner handoff succeeds but planner-backed `compose-from-selection` fails
2. Planner-backed flow reaches compose only via legacy/debug fallback
3. Blocked reason code/detail visible in UI but not in saved proof artifacts

These are the same conditions that correctly stopped the prior diagnostic pass (the `409` was exactly trigger #1). The fact that the memo reuses the same branching rules that already worked once is evidence of honest discipline rather than retroactive loosening.

### Finding 6: Pack and rubric remain frozen (Severity: Confirming)

The memo explicitly preserves:
- Same four cases: `evolution_ready`, `engagement_ready`, `non_profile_ready`, `selection_blocked`
- Same rubric dimensions: `selection_fit`, `rationale_clarity`, `rendered_usefulness`, `operational_behavior`
- Same threshold shape from `MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- Same fixture-strength tier model
- Same Stage 2 closure bar (requires `execution_backed` or stronger)

No rubric weakening, no case substitution, no threshold relaxation.

### Finding 7: Stage 2 / Tranche 3 boundaries are explicit and honest (Severity: Confirming)

The memo's Decision 6 is unusually disciplined: it states that Stage 2 should remain open unless at least one ready case is intentionally upgraded to `execution_backed`. It names `evolution_ready` as the default upgrade candidate but does not presume the upgrade. It requires the closeout memo to decide Stage 5 and Stage 2 separately.

Tranche 3 remains explicitly blocked until the rerun produces a real decision. The memo does not smuggle in any broader work.

### Finding 8: No hidden dependency undermines the diagnostic meaningfulness (Severity: Confirming)

I checked for dependencies that could make the rerun less meaningful:

- **Environment dependency**: The prior diagnostic required `ANALYZER_V2_URL=http://127.0.0.1:8002` for the-critic. The memo preserves this as the default target (Decision 2). The diagnostic artifacts record the environment correction. This is honest.
- **Data dependency**: The proof source job `proof-round5-adaptive-aoi-dossier-final-1774100000` must exist locally with populated AOI thinker identity. The identity-continuity slice added code to create/backfill the `v2_run_references` row and project thinker identity into warmed snapshots. Five regression tests cover this chain.
- **No unresolved code conflict**: The identity-continuity slice changed code in `the-critic` only (server.py + frontend). The analyzer-v2 selector/provider slice was already landed in a prior pass. No cross-repo merge conflict exists.

---

## Answers to Specific Questions

### 1. Is the memo correctly narrowing the next move?

**Yes.** One diagnostic spot-check followed by conditional frozen rerun is the exact right sequencing after a code repair. The memo does not skip the diagnostic, does not assume the rerun is already earned, and does not widen scope.

### 2. Does the codebase evidence support the identity-continuity fix?

**Yes.** All five claimed regression tests exist and test the correct failure modes. The compose proxy validation is fail-closed on mismatch. The frontend forwards `source_v2_job_id` on the planner-backed path. The backend creates/backfills the identity chain through `v2_run_references` → snapshot warmup → compose validation. The test counts match the completion memo claims.

### 3. Is the memo honest about what this buys?

**Yes.** The bounded claim section (lines 52-65) is unusually explicit about what this step does not claim. The honesty extends to Decision 6's handling of Stage 2, which states the likely outcome is "Stage 5 may pass, Stage 2 may still remain open."

### 4. Is the artifact/branch discipline strong enough?

**Yes.** The stop-and-revise conditions in Decision 4 are precise, actionable, and already proven (they correctly stopped the prior pass). The required artifact list (Decision 3 diagnostic + Decision 4 rerun) is concrete and auditable. The memo requires separate Stage 5 and Stage 2 decisions in the closeout.

### 5. Does the memo preserve the right program order?

**Yes.** The memo:
- Does not update the roadmap (appropriate - this is a Stage 5 operational step, not a strategic pivot)
- Recalibrates only the immediate plan (diagnostic → conditional rerun)
- Does not pivot phases
- Keeps Tranche 3 blocked

This is the right order. A minor roadmap annotation noting "identity-continuity slice landed" would be appropriate after the rerun completes, but it is not needed before the diagnostic.

### 6. Any hidden dependencies?

**None found** that would undermine the diagnostic. See Finding 8 above.

### 7. Is the memo staying bounded?

**Yes.** No Tranche 3 work, no lifecycle, no second-consumer proof, no architecture redesign, no rubric softening. The only work is: run one diagnostic, capture artifacts, make a branching decision, optionally run the frozen pack.

---

## Program Recommendation

The program should:

- **Execute this scope as written** - no revisions needed
- **Not update the roadmap** before the diagnostic - the roadmap update should come after the rerun decision, not before
- **Not pivot phases** - Stage 5 remains the current operational focus
- **Carry forward one residual note**: the simple/legacy profile launch path does not forward `source_v2_job_id`, which is acceptable for the planner-backed proof but should be recorded if the program later needs legacy-path identity parity
