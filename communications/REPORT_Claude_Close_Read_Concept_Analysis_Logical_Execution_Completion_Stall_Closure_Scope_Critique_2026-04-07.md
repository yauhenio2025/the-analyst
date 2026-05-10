# Report: Close Read Concept-Analysis Logical Execution Completion Stall Closure Scope — Critique

Date: 2026-04-09
Reviewer: Claude Opus 4.6
Memo Under Review: `communications/MEMO_2026-04-07_close_read_concept_analysis_logical_execution_completion_stall_closure_scope.md`

## Verdict: reject

The memo's central assumption — that the active blocker is an analyzer-v2 logical execution completion stall — is **falsified by the current live evidence**. The memo was written during a narrow window when both jobs still showed `running`. That window has closed. The live state now shows the opposite of what the memo predicted: analyzer-v2 completed successfully, and the-critic failed at host-side persistence with an explicit database constraint violation.

The earlier April 7 readback-first memo (`MEMO_2026-04-07_close_read_concept_analysis_logical_readback_and_scrutiny_closure_scope.md`) was closer to the correct diagnosis. This superseding memo should not have displaced it.

---

## 1. The Memo's Main Assumption Is Falsified

### Verified live facts (fetched 2026-04-09)

| Resource | Memo's claimed state | Actual current state |
|----------|---------------------|---------------------|
| analyzer-v2 job `job-plan-936b5b61e93f` | `running` (stalled) | **`completed`** at 2026-04-07T03:05:54 |
| the-critic job `concept-1775529506826-c585ea` | `running` | **`failed`** at 2026-04-07T03:05:58 |
| Logical readback (`/api/concept/analyses/innovation?analysis_type=logical`) | 404 (expected while running) | **404** (persisted data never landed) |

The analyzer-v2 job ran for ~27 minutes on a tiny corpus (8 LLM calls, 121K input tokens, 53K output tokens, 12-phase chain). It completed all 12 engines plus the translated host artifact materialization step. Progress detail reads: `"Materializing translated host artifact"` — meaning the auto-presentation pipeline also ran.

The-critic job then failed with an explicit error:

> `Database constraint violation: duplicate key (innovation, logical) already exists in concept_analyses table`

This is a **host-side persistence bug**, not an upstream execution stall.

### Code-backed root cause

The `concept_analyses` table has a unique constraint on `(concept, analysis_type)` only — **without** `project_id`:

```
-- alembic/versions/001_initial_schema.py:144
sa.UniqueConstraint('concept', 'analysis_type', name='uq_concept_analysis_type')
```

But the upsert logic in `_save_concept_analysis_to_db` (server.py:3854-3860) queries by **three** columns including `project_id`:

```python
existing = session.execute(
    select(DBConceptAnalysis).where(
        DBConceptAnalysis.concept == concept,
        DBConceptAnalysis.analysis_type == analysis_type,
        DBConceptAnalysis.project_id == project_id,  # <-- mismatch
    )
).scalar_one_or_none()
```

When the new project `cutover-logical-readback-closure-20260407-023428` attempts to save `(innovation, logical)`:

1. The upsert check queries for `(innovation, logical, cutover-logical-readback-closure-20260407-023428)`
2. No match found (the existing row is from the earlier project `cutover-live-tiny-20260406`)
3. Code attempts INSERT
4. Hits the unique constraint `uq_concept_analysis_type` on `(innovation, logical)`
5. Raises `RuntimeError` (the deployed fail-closed fix correctly propagates this)
6. Job marked `failed`

This is a textbook schema-code mismatch: the upsert check is wider than the unique constraint, causing false misses and constraint violations.

---

## 2. Is the Memo Correct to Supersede the April 7 Readback-First Diagnosis?

**No.**

The readback-first memo (`MEMO_2026-04-07_close_read_concept_analysis_logical_readback_and_scrutiny_closure_scope.md`) diagnosed:

> "The strongest default diagnosis from the current code is... silent host persistence failure on the logical save path"

and correctly identified `_save_concept_analysis_to_db(...)` as the likely failing seam (lines 3842-3901 of server.py).

The only thing the readback-first memo got technically wrong was calling it "silent" — the deployed fail-closed fix (which the superseding memo itself acknowledges) means the failure is now explicit, not swallowed. But the fundamental diagnosis — **host-side persistence failure as the active blocker** — was correct.

The superseding memo's reasoning was:

> "both still report `running` → that narrows the active diagnosis upstream to analyzer-v2 execution completion"

This was a valid inference **at the moment of writing**, but it was a snapshot-in-time assessment that aged poorly within ~30 minutes. The memo should have included a falsification condition: "if analyzer-v2 completes and the-critic still fails, revert to the readback-first diagnosis."

---

## 3. Does the Live Evidence Support "Upstream Completion Stall"?

**No.** The live evidence directly contradicts it:

- analyzer-v2 job completed with all phases done, auto-presentation ran
- 27 minutes for a 12-phase chain on a 2-doc corpus is slow but within the expected range documented in the project memory (183K+ token inputs produce ~0.5 tokens/sec)
- The input was 121K tokens, which at expected throughput would take roughly this long

There is no stall. There is slow-but-normal LLM execution followed by successful completion.

---

## 4. Is the Tranche Properly Bounded?

**The tranche is bounded around the wrong problem.** It proposes:

1. Trace analyzer-v2 execution internals (unnecessary — execution completed)
2. Fix an analyzer-v2-side completion stall (doesn't exist)
3. Rerun proof after fix (the fix target is wrong)

The correctly bounded tranche should be:

1. Fix the `concept_analyses` unique constraint to include `project_id`, OR fix the upsert query to match the constraint
2. Rerun proof on either the current or a clean project
3. Verify readback + scrutiny closure

This is a **one-line schema migration + optional upsert logic fix**, not a multi-phase executor investigation.

---

## 5. Does the Memo Preserve the Roadmap Order?

**Mostly yes, but with an ironic side effect.** The memo correctly defers translated-artifact-authority work. However, by misdiagnosing the blocker as upstream, it would have spent investigation time on analyzer-v2 executor internals rather than the ~30-minute host-side fix. This would have **accidentally** delayed the roadmap corridor more than the readback-first memo would have.

The readback-first memo would have led directly to the constraint fix, closing logical readback quickly, which is the prerequisite for resuming the translated-artifact-authority corridor.

---

## 6. Hidden Alternative Diagnoses the Memo Underweights

### a. **Duplicated proof-project document identity effects** — RELEVANT

The prompt specifically flagged this. The project has 4 documents (2 duplicate pairs). This is messy but is NOT the primary cause of the failure — the constraint violation comes from cross-project collision, not within-project document identity. However, the duplicate documents would cause problems in analysis quality and should be cleaned up in any final certification corpus.

### b. **Host poll/state handling after upstream completion** — THIS IS THE ACTUAL BLOCKER

The memo listed this as a lower-priority alternative. It is in fact the primary blocker. Specifically, the host persistence path fails on `_save_concept_analysis_to_db` due to the schema-code mismatch.

### c. **Workflow-runner completion semantics** — NOT THE ISSUE

The workflow runner completed correctly. The `execute_plan` function in `workflow_runner.py` ran all phase groups, called `_run_auto_presentation`, and set the job to `completed`. No bugs here for this specimen.

### d. **Transformation handoff/finalization** — NOT THE ISSUE

The progress detail confirms auto-presentation/transformation materialization ran. The analyzer-v2 side of the pipeline is clean.

---

## 7. What Exact Corrections Would Make the Memo Implementation-Ready?

The memo cannot be corrected in place because its core framing is wrong. The correct next action is:

### Revert to the readback-first memo as the canonical scope, with these specific amendments:

**Phase 1 — Fix host persistence constraint mismatch (the-critic side)**

One of:
- **Option A (preferred):** Add migration to change unique constraint from `(concept, analysis_type)` to `(concept, analysis_type, project_id)`. This is architecturally correct — different projects should be able to analyze the same concept independently.
- **Option B:** Change the upsert query in `_save_concept_analysis_to_db` to only check `(concept, analysis_type)`, matching the existing constraint. This overwrites across projects, which may be acceptable for the bounded proof.
- **Option C:** Use database-level `ON CONFLICT ... DO UPDATE` instead of select-then-insert. Eliminates the race condition entirely.

**Phase 2 — Rerun fresh logical proof**

On a clean project (single subject + single response doc, no duplicates):
- Launch logical
- Confirm analyzer-v2 job completes
- Confirm the-critic job completes
- Confirm `/api/concept/analyses/innovation?analysis_type=logical` returns data
- Confirm `_analysis_provenance.execution_owner == "analyzer-v2"`

**Phase 3 — Scrutiny closure**

- Launch scrutiny against the persisted logical result
- Confirm scrutiny readback

---

## Evidence Classification

### Verified live facts
- analyzer-v2 job `job-plan-936b5b61e93f`: status=completed, 8 LLM calls, 121K/53K tokens, completed 2026-04-07T03:05:54
- the-critic job `concept-1775529506826-c585ea`: status=failed, error="Database constraint violation: duplicate key (innovation, logical) already exists"
- Logical readback: 404 confirmed
- Project documents: 4 docs (2 duplicate pairs)
- Unique constraint: `uq_concept_analysis_type` on `(concept, analysis_type)` only (alembic migration line 144)
- Upsert query: filters on 3 columns including `project_id` (server.py:3854-3860)

### Code-backed inferences
- The schema-code mismatch (2-column constraint vs 3-column query) deterministically produces the observed duplicate-key violation when a second project tries to save the same (concept, analysis_type)
- The earlier project `cutover-live-tiny-20260406` successfully saved `(innovation, logical)`, creating the row that blocks the new project
- The deployed fail-closed fix (`raise RuntimeError` at line 3899) is working as designed — the failure is now explicit rather than silently swallowed

### Speculative concerns
- The 27-minute execution time for a 12-engine chain on a tiny corpus is slow but may not warrant a dedicated "extreme-duration" investigation — it falls within the documented throughput band for large-context LLM calls. This could be revisited later if it becomes a UX problem, but it is not a correctness bug.
- The duplicate documents in the proof project did not cause this specific failure but would produce lower-quality analysis output and should be avoided in the final certification corpus.
