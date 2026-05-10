# Memo: Next Step Scope - Round-1 Proof Record And Exit-Criterion Closure

## Purpose

Define the scope for the next step after **Phase 4 / Deliverable D**.

This is not a new product-feature tranche.
It is the scope for the **round-1 proof record and evidence closure** required by the Thin Consumer Platformization execution brief.

This memo should answer:

1. why this is the next step now
2. what exactly the proof-record tranche should cover
3. what must remain out of scope
4. what evidence is required for the tranche to count as real closure

This memo sits beneath:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase2_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase3_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase4_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_roadmap_after_phase3.md`

## Why This Is The Right Next Step

Deliverables A, B, C, and D are now complete in substance.

What still remains blocked by the execution brief is not another feature.
It is the proof record itself.

The execution brief requires a short proof memo that names:

- the two bounded workflows used in the generic workspace proof
- the two genealogy jobs used in the artifact reuse proof
- the exact Job 2 reuse signal
- the final disposition of each exit criterion

That proof record does not yet exist.

The current state also still has two documentary tails:

1. the small Phase 2 manual-verification tail
2. the Phase 4 manual generic-route verification tail

So the next step should be a closure-and-evidence tranche, not a new platform tranche.

## Current Reality

### What is already done

- Deliverable A: authority boundary
- Deliverable B: shared bounded-v2 consumer contract
- Deliverable C: first artifact reuse proof
- Deliverable D: cross-workflow generic workspace proof

### What is still missing

- the round-1 proof record itself
- a final pass/waive decision for the remaining manual-verification tails

### One important evidence gap

The execution brief asks for the **exact genealogy job ids** used in the artifact reuse proof.

Phase 3 proved reuse through deterministic automated tests, but the current test fixture uses runtime-generated job ids and cleans those rows up at the end of the test.

That means the proof record cannot yet honestly cite exact existing job ids from current written evidence alone.

So the next step must explicitly decide how that evidence will be produced.

## Scope Decision

## In Scope

The next step should stay tightly bounded to one closure artifact:

- **write the round-1 proof record and close the remaining evidence tails**

That closure should include:

1. a final proof memo at:
   - `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-XX_thin_consumer_platformization_round1.md`
2. one explicit disposition for the Phase 2 manual tail:
   - rerun, or
   - written waiver
3. one explicit disposition for the Phase 4 manual tail:
   - rerun, or
   - written waiver
4. exact Deliverable C evidence naming:
   - the two genealogy jobs
   - the Job 2 reuse signal
5. final pass/fail/waived disposition for each execution-brief exit criterion

## Recommended Shape

The default path should be:

### 1. Perform the Phase 4 manual operator checks

These are the manual checks that most directly strengthen the proof:

- one generic genealogy run or restore via `AnalysisWorkspacePage`
- one generic AOI single-thinker run or restore via the generic proof route
- confirmation that AOI active-run discovery and saved-result behavior stay thinker-scoped

### 2. Do **not** reopen Phase 2 implementation

For the Phase 2 manual tail, the recommended default is:

- **waive it explicitly unless a reviewer insists on zero waivers**

Why this is the right default:

1. Phase 2 is already code-complete and strongly covered by automated suites
2. Deliverable D already exercised the proving vehicle on top of that shared contract
3. reopening a broader operator pass for the older contract tranche is lower value than closing the round-1 proof record cleanly

### 3. Produce exact Deliverable C evidence in one small, documentary-safe way

Because the current Phase 3 tests use ephemeral job ids, the safest default is:

- allow **one tiny verification-only analyzer-v2 addition** if needed to make the artifact proof documentary-ready

The preferred shape is:

- a **single new deterministic test function** in:
  - `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py`
- that creates a two-job genealogy reuse proof with fixed, recordable job ids
- and prints or captures the Job 2 manifest evidence needed for the proof record before cleanup

This is acceptable only if it remains:

- verification-only
- narrowly owned by the proof step
- non-substantive with respect to Deliverable C behavior
- confined to the existing backend proof-test file rather than a new standalone script or reusable tool

The proof step should **not** reopen:

- `store.py`
- result contract semantics
- freshness logic
- artifact lookup design
- new analyzer-v2 API routes
- any `the-critic` product file

unless a genuine documentary blocker makes that unavoidable.

### 4. Write one proof record, not a memo stack

The proof record should carry the closure, rather than spawning a new family of product memos.

The proof record should include:

- the two generic-route workflows proved
- the Deliverable C source/target job ids
- the exact `reuse_state` / `reused_from_job_id` evidence for Job 2
- the exact deterministic test name and command used to generate that Deliverable C evidence
- final disposition of exit criteria 1 through 5
- an explicit statement that Deliverable C proves:
  - stored-artifact reuse and manifest observability
  - not executor-time short-circuiting or whole-run recomputation skipping
- a short blocked/unblocked statement about broader dynamic-composition claims

## Out Of Scope

To keep this tranche honest, the following are out of scope:

- any new product feature work in `the-critic`
- analyzer-v2 substrate expansion beyond proof-evidence capture
- any new standalone proof script or reusable verification framework
- new artifact classes
- new bounded workflows
- AOI enrichment
- genealogy surface redesign
- dynamic-form or route work
- any new “apps on the fly” or Stage 10 claims

If the step starts turning back into product implementation, it is drifting.

## Primary Surfaces To Scrutinize

The most important files for this scope are:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase2_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase3_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase4_completion.md`
- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx`

These are the places where the proof obligations, the remaining manual tails, and the exact evidence gap are visible.

## Acceptance Criteria

This next step should be treated as done only if all of the following are true:

1. the round-1 proof record exists at the execution-brief path
2. the proof record names both bounded workflows used in the generic workspace proof
3. the proof record names the exact two-job genealogy reuse proof pair and the exact Job 2 reuse signal
4. the proof record cites the exact deterministic test function and command used to generate Deliverable C documentary evidence
5. the proof record gives final `PASS`, `FAIL`, or `WAIVED` disposition for each execution-brief exit criterion
6. the proof record explicitly states that Deliverable C does **not** claim executor-time reuse skipping beyond the Phase 3 proof boundary
7. the Phase 4 manual operator checks are either performed and recorded, or explicitly waived with rationale
8. the manual proof also verifies the AOI handoff click from the bespoke thinker page into the generic workspace proof route
9. the small Phase 2 manual tail is explicitly resolved:
   - rerun, or
   - waived in writing
10. no Deliverable A-D behavior is reopened except one tiny verification-only aid in `tests/test_analysis_product_contract.py` if exact evidence truly requires it

## Verification Expectations

The expected verification for this tranche should be:

### Automated

- rerun the focused webapp suites that prove Deliverable D
- rerun the shared bounded-v2 contract suites
- if the deterministic Deliverable C evidence test is added, run that exact test path and capture its output

### Manual

- one generic genealogy proof run or restore via `AnalysisWorkspacePage`
- one generic AOI proof-route run or restore via:
  - `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=<id>&selected_source_thinker_name=<name>`
- one explicit click from the bespoke AOI thinker detail page into the generic AOI proof route, confirming the bounded thinker context survives the navigation

### Documentary

- capture the final artifact-proof evidence needed to name:
  - Job 1 id
  - Job 2 id
  - `reuse_state`
  - `reused_from_job_id`

## Failure Modes To Watch For

The main ways this step can go wrong are:

1. treating the proof record as “just write a memo” and failing to close the evidence gap around exact artifact-proof job ids
2. reopening Deliverable C implementation instead of adding, at most, a single deterministic verification-only test in the existing backend proof-test file
3. turning the Phase 2 manual tail into a broad regression campaign instead of making an explicit rerun-or-waive decision
4. writing a proof record that overclaims Deliverable C as executor-time reuse rather than the narrower stored-artifact reuse proof that actually landed
5. writing a proof record that says the program is complete without naming exit-criterion dispositions concretely
6. slipping into new product work instead of closing the round-1 proof honestly

## Final Recommendation

If the team needs one operational sentence for the next step, it should be:

- **Close the remaining manual/evidence tails, make the artifact reuse proof documentary-ready enough to name exact jobs, and write the round-1 proof record required by the execution brief.**
