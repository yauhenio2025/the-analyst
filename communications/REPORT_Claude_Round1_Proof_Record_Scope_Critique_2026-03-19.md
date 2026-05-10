# Review: Round-1 Proof Record Scope

Reviewer: Claude Opus 4.6
Date: 2026-03-19
Subject: `communications/MEMO_2026-03-19_round1_proof_record_scope.md`

---

## 1. Verdict

**The scope memo is sound and correctly framed.** This is genuinely a closure/evidence step, not a disguised feature step. The scope boundaries are drawn in the right places, the deliverable mapping is accurate, and the memo correctly identifies the one real evidence gap (ephemeral job ids in the Phase 3 tests).

Three corrections are needed. None of them invalidate the scope — they sharpen it.

---

## 2. Findings

### Finding 1: The evidence gap is real but narrower than the memo implies

The memo states that "the current test fixture uses runtime-generated job ids and cleans those rows up at the end of the test" (line 66–67). This is accurate:

- `test_analysis_product_contract.py:270-271` generates `job1 = f"job-test-genealogy-reuse-{uuid4().hex[:8]}"` and `job2` similarly
- `_cleanup_genealogy_proof_rows` at line 321 deletes all rows after the test

However, the gap is narrower than the memo suggests. The test suite already has a fully wired deterministic two-job proof that exercises the real `build_result_manifest` → `_summarize_artifacts_for_job` path and asserts `slot_summary.reuse_state == "reused"` and `slot_summary.reused_from_job_id == job1`. The only thing missing is that the job ids are not pre-chosen fixed strings and the rows do not survive the test.

A proof-record harness does **not** need to add new reuse logic, change the store, or add a new API endpoint. It only needs to:

1. Use fixed (or logged) job ids instead of random ones
2. Skip the cleanup, or print/capture the ids before cleanup
3. Emit the manifest JSON to a file or stdout

This is genuinely verification-only and should take ~30 lines of code.

### Finding 2: The Phase 2 manual-tail waiver recommendation is safe

The memo recommends waiving the Phase 2 manual-verification tail by default (lines 109–117). I tested this against the evidence:

- Phase 2 automated coverage: 7 suites / 32 tests covering the shared bounded-v2 client, hook, integration mount, AOI thinker scoping, and import fallback
- Phase 4 exercises the proving vehicle *on top of* the Phase 2 contract (the hook and client were NOT modified in Phase 4)
- Phase 4 tests explicitly assert that `useBoundedV2Workspace` options are passed correctly and that the shared contract mediates all lifecycle operations

The Phase 2 manual tail was about confirming restore-first browser behavior for `AnalysisWorkspacePage` and `AoiV2ThematicPanel`. Since Phase 4's automated tests (`AnalysisWorkspacePage.integration.test.tsx`) exercise the full restore-first mount orchestration against real client mocks, the Phase 2 manual tail is now redundant with Phase 4 automated verification. Waiving it with rationale is safe.

### Finding 3: The Phase 4 manual operator checks are the only manual items worth performing

The memo correctly identifies these (lines 99–105):

1. One generic genealogy run or restore via `AnalysisWorkspacePage`
2. One generic AOI single-thinker run or restore via the generic proof route
3. Confirmation that AOI discovery and restore are thinker-scoped

These are worth performing because they exercise the *actual deployed stack*, not just the test harness. The automated tests use mock fetch and mock hooks — they prove contract correctness, not deployment correctness.

### Finding 4: The "Open Generic Workspace" handoff exists in code

`AnxietyOfInfluencePages.tsx:789` renders the handoff button. The test at `AnxietyOfInfluencePages.test.tsx:248-271` asserts it navigates to:

```
/p/demo-project/analysis/anxiety_of_influence_thematic_single_thinker
  ?selected_source_thinker_id=otto_neurath
  &selected_source_thinker_name=Otto+Neurath
```

This satisfies the Deliverable D requirement that AOI is "reachable from the bespoke AOI surface."

### Finding 5: The memo correctly identifies all execution-brief exit criteria

Cross-referencing the execution brief (lines 188–194) against the scope memo:

| Exit Criterion | Covered by Scope Memo? |
|---|---|
| 1. AnalysisWorkspacePage is canonical generic proof for both workflows | Yes — Phase 4 + Phase 4 manual check |
| 2. Bounded v2 primary path no longer relies on Critic-side polling | Yes — Phase 1A + Phase 2 automated suites |
| 3. Reusable consumer contract exists and is used by proving vehicle | Yes — Phase 2 contract + shared adoption |
| 4. genealogy.relationship_classification reused across two jobs | Yes — Phase 3 + evidence gap fix |
| 5. Short proof record names the two jobs, reuse outcome, workspace success | Yes — the proof record itself |

No exit criterion is missing from the scope.

---

## 3. Assumptions Tested

### Assumption: "This is not a new product-feature tranche"

**Confirmed.** The scope memo does not propose any new API endpoints, new UI components, new workflow support, or new artifact classes. Every item in the "In Scope" section is either:
- a documentary artifact (the proof record itself)
- a disposition decision (waive or rerun manual tails)
- a tiny verification-only harness for evidence capture

The out-of-scope list (lines 158–169) is correctly drawn.

### Assumption: "The Phase 2 manual tail can safely be waived"

**Confirmed.** See Finding 2 above. Phase 4's automated integration tests now cover the exact behavior that the Phase 2 manual check was meant to confirm.

### Assumption: "Current Deliverable C proof surfaces support naming exact genealogy job ids"

**Partially confirmed.** The proof surfaces (`test_analysis_product_contract.py:268-453`) prove the reuse behavior end-to-end with real DB writes. The test asserts all the right things:

- `slot_summary.reuse_state == "reused"` (line 318)
- `slot_summary.reused_from_job_id == job1` (line 319)
- `stored_row["job_id"] == job1` (provenance durability, line 448)

But the job ids are ephemeral and the rows are cleaned up. The proof record cannot cite `job-test-genealogy-reuse-a3f2b1c9` as durable evidence because that id won't exist by the time someone reads the record. A tiny harness that captures or fixes these ids is genuinely needed.

### Assumption: "One tiny verification-only analyzer-v2 aid is the right escape hatch"

**Confirmed.** The alternative — running a real two-job genealogy workflow against the live deployed service — is disproportionate for the proof record step. It would require document upload, LLM execution (30+ minutes per job), and dependency on the live Render deployment. A deterministic test-side harness that writes two jobs with fixed ids, stores one artifact, and emits the manifest JSON is the right shape.

### Assumption: "The memo is not hiding implementation drift behind the verification harness"

**Confirmed.** I inspected the actual write-side guard (`store.py:698-708`) and read-side reuse detection (`store.py:834-845`). Both are complete and correct:

- Write guard: loads existing artifact, checks `_is_current_ready_genealogy_artifact`, returns unchanged if true
- Read side: checks `family == genealogy.relationship_classification`, `state == ready`, `_is_current_ready_genealogy_artifact(row)`, and `row.job_id != current_job_id`

The verification harness only needs to exercise these existing code paths with recordable ids. It does not need to modify them.

---

## 4. Scope Corrections

### Correction 1: Tighten the verification harness shape

The memo says (lines 126-127):

> a deterministic proof-side harness, script, or targeted test path that creates a two-job genealogy reuse proof with fixed, recordable job ids and emits the manifest-level reuse signal

This is slightly too open. "Script" and "harness" could drift into a reusable tool. Tighten to:

> A single new test function in `tests/test_analysis_product_contract.py` that uses deterministic job ids (e.g. `"proof-job-1"`, `"proof-job-2"`) and prints the reuse evidence to stdout before cleanup. The proof record will cite the test function name and its console output.

This keeps the evidence inside the existing test file, uses existing test infrastructure, and does not introduce a new script or entry point.

### Correction 2: Make the proof record cite test evidence, not durable DB rows

The execution brief says (lines 96-109):

> the manifest must explicitly identify that reuse happened
> the manifest must identify the source job that supplied the reused artifact

The scope memo assumes this means citing durable job ids from a persistent database. But the execution brief does not require the proof jobs to still exist in production — it requires the proof record to *name* them. A test that prints the manifest JSON to stdout is sufficient evidence if the proof record cites the test name and captures the output.

This removes the need for the harness to leave rows in the database.

### Correction 3: The Phase 4 manual checks should include one specific AOI handoff verification

The scope memo lists three manual checks (lines 99-105) but does not explicitly name the AOI handoff link verification:

> Click "Open Generic Workspace" from the bespoke AOI thinker detail page and confirm the generic route loads with the correct thinker context

This is already tested automatically (`AnxietyOfInfluencePages.test.tsx:248-271`) but a manual confirmation that the navigation actually works in the deployed app would strengthen the proof record's workspace claim.

---

## 5. Suggested Acceptance Criteria Changes

The current acceptance criteria (lines 187-197) are well-structured. I suggest one addition and one clarification:

### Addition: Criterion 3 should explicitly name the evidence format

Current:
> the proof record names the exact two-job genealogy reuse proof pair and the exact Job 2 reuse signal

Suggested:
> the proof record names the exact two-job genealogy reuse proof pair and cites the exact `reuse_state` and `reused_from_job_id` values from the Job 2 result manifest, with either a captured manifest excerpt or a reference to the deterministic test function that produces this output

### Clarification: Criterion 7 should name the single file that may be modified

Current:
> no Deliverable A-D behavior is reopened except one tiny verification-only aid if exact evidence truly requires it

Suggested:
> no Deliverable A-D behavior is reopened; the only analyzer-v2 code change permitted is a single new test function in `tests/test_analysis_product_contract.py` that captures proof evidence with deterministic job ids

---

## 6. Recommended Next Move

The scope memo is ready to execute with the three corrections above.

Concrete sequence:

1. **Add one deterministic proof test** in `tests/test_analysis_product_contract.py` using fixed job ids (e.g. `proof-round1-job-1`, `proof-round1-job-2`). The test should print the manifest excerpt showing `reuse_state` and `reused_from_job_id` before cleanup.

2. **Run the proof test** and capture its output.

3. **Perform the Phase 4 manual operator checks** (3 items: genealogy restore, AOI restore, AOI handoff).

4. **Write the proof record** at `communications/PROOF_2026-03-XX_thin_consumer_platformization_round1.md` citing:
   - Workflows: `intellectual_genealogy`, `anxiety_of_influence_thematic_single_thinker`
   - The deterministic test function name and its manifest output
   - Final exit-criterion dispositions
   - Phase 2 manual tail: WAIVED (with rationale from Finding 2)

5. **Do not reopen** any Deliverable A-D implementation.

The scope is correct, bounded, and ready to close.
