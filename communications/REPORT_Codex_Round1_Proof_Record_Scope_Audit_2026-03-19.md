# Codex Audit: Round-1 Proof Record Scope

## Verdict

Accept with tightening.

The next step is correctly scoped as a **proof/evidence closure tranche**, not another broad product-feature tranche. The cited backend and frontend seams for Deliverables C and D are real in code, and the focused suites still pass. The one real blocker is documentary: the repo does **not** currently contain durable, recordable Deliverable C job ids that a final proof record can honestly cite.

So the scope memo is directionally right, but it should be tightened before execution.

## Blocking Issues

### 1. The final proof record cannot honestly name exact Deliverable C job ids from current durable evidence

The execution brief requires the proof record to name the two genealogy jobs and Job 2's reuse signal.

Current evidence does not support that cleanly:

- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py:270-271`
- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py:326-327`
- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py:391-392`

Those tests generate job ids with `uuid4()`.

- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py:125-130`
- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py:321`
- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py:386`
- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py:453`

Those rows are then deleted in cleanup.

That means the repo currently proves Deliverable C behavior, but it does **not** yet provide a durable documentary seam for “Job 1 = X, Job 2 = Y” in the final proof record.

### 2. The allowed “verification-only aid” is still too loosely bounded

`/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_round1_proof_record_scope.md:123-142` is directionally correct, but “a harness, script, or targeted test path” is still broad enough to let an implementer drift back into Deliverable C product edits.

If this scope is accepted, the memo should name the allowed write surface explicitly and forbid edits to:

- `src/analysis_products/store.py`
- `src/analysis_products/schemas.py`
- `src/analysis_products/result_contract.py`
- any `the-critic` product file

unless the team explicitly reopens Deliverable C as a new tranche.

## Non-Blocking Risks

### 1. The proof record can overclaim Deliverable C unless it states the proof boundary explicitly

The execution brief says Job 2 should reuse the artifact “instead of recomputing it”:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md:84-90`

But the Phase 3 scope explicitly narrowed the proof to stored-artifact reuse, not executor-time skipping:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase3_artifact_reuse_scope.md:93-100`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase3_artifact_reuse_scope.md:134-135`

And the Phase 3 completion memo repeats that limitation:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase3_completion.md:147-153`

That is not a blocker for the proof-record tranche if the proof record says so plainly. It becomes a blocker only if someone tries to mark exit criterion 4 as broader than the implemented proof.

### 2. The Phase 2 waiver recommendation is defensible, but only if it is written as a waiver, not silently dropped

Phase 2 still has an unresolved manual tail:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase2_completion.md:109-119`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase2_completion.md:147-159`

Waiving that tail is technically reasonable because Deliverable D already exercises the same shared contract seam, but the waiver has to be explicit in the proof record.

### 3. The Phase 4 manual checks are higher-value than the Phase 2 manual rerun

Phase 4 is the remaining operator-facing proof tail:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase4_completion.md:166-183`

So the proposed default is correct:

- do the Phase 4 manual checks
- waive the small Phase 2 tail unless a reviewer insists on zero waivers

### 4. Existing React `act(...)` warnings remain noise in the frontend proof suites

They are already acknowledged in the phase memos and still appear in the focused run. They are not a blocker, but they should not be mistaken for fresh regressions.

## Assumptions Tested

### 1. Deliverable C behavior exists in code, not just in memo language

The backend seam is real:

- `/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py:688-722` preserves an existing fresh genealogy artifact instead of overwriting it
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py:788-864` surfaces `reuse_state` and `reused_from_job_id` in slot summaries
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/schemas.py:12-18` exposes those fields in the manifest schema
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py:291-349` includes the artifact summaries in `build_result_manifest`

Focused verification:

- `PYTHONPATH=. pytest tests/test_analysis_product_contract.py -q`
- result: `17 passed`

### 2. Deliverable D behavior exists in code, not just in memo language

The generic workspace seam is real:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:105-108`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:239-245`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:380-445`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:521-569`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:695-818`

Those lines show:

- AOI thinker context from query params
- thinker-scoped discovery and restore
- AOI launch body enrichment
- AOI guidance when thinker context is missing
- generic AOI import controls deliberately hidden

The AOI handoff seam is also real:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx:662-705`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx:738-745`

Focused verification:

- `CI=true npm test -- --watch=false --runTestsByPath src/lib/boundedV2Client.test.ts src/hooks/useBoundedV2Workspace.test.tsx src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx src/pages/AnxietyOfInfluencePages.test.tsx`
- result: `5 suites passed`, `33 tests passed`
- caveat: existing non-failing React `act(...)` warnings remain

### 3. The exact-job-id documentary seam is genuinely absent today

There is no existing round-1 proof record file at the execution-brief location, and the reusable-artifact proof tests do not leave stable job ids behind.

### 4. No new broad implementation tranche is obvious from the cited seams

From the code inspected, the remaining work is closure, manual-disposition, and documentary capture. The only implementation that may still be justified is a proof-only aid for exact Deliverable C evidence.

## Recommended Scope Tightening

1. Narrow the allowed write surface to:
   - the new proof record file
   - one deterministic proof-only backend artifact under `tests/` or `scripts/`
   - no product-code edits elsewhere

2. Change “one tiny verification-only aid” to something explicit like:
   - one deterministic genealogy proof harness that creates exactly two fixed job ids, emits Job 2’s manifest evidence, and is used only to populate the proof record

3. Add an acceptance criterion that the proof record must state the Deliverable C proof boundary:
   - stored-artifact reuse and manifest observability are proved
   - executor-time short-circuiting is **not** being claimed

4. Add an acceptance criterion that the proof record must cite:
   - the exact command or test path used to generate Deliverable C documentary evidence
   - the exact route(s) used for any Phase 4 manual checks
   - explicit `PASS`, `WAIVED`, or `FAIL` for each exit criterion with one-line rationale

5. Keep the Phase 2 default as:
   - explicit waiver unless a reviewer requires zero waivers

6. Keep the Phase 4 default as:
   - perform and record the manual operator checks, because they directly strengthen the cross-workflow proof

## Implementation Starting Point

Do **not** start by editing product code.

Start with these owned files:

- `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-19_thin_consumer_platformization_round1.md`
- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py` or one new adjacent proof-only test/harness file

Use these as read-first evidence anchors:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase2_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase3_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase4_completion.md`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.integration.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.test.tsx`

Recommended execution order:

1. Decide and record the Phase 2 disposition: waiver by default.
2. Perform and record the Phase 4 manual checks, or explicitly waive them.
3. Add the smallest deterministic Deliverable C proof-only harness needed to emit fixed job ids.
4. Re-run the focused backend and frontend proof suites.
5. Write the proof record with concrete exit-criterion dispositions.

## Bottom Line

The scope is fundamentally sound, but it is not yet tight enough to execute safely without drift. The real missing seam is documentary, not product-functional. Tighten the allowed verification aid, force explicit wording around the Deliverable C proof boundary, and then proceed with proof-record closure.
