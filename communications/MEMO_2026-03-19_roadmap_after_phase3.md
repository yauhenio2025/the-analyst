# Memo: Roadmap After Phase 3

## Purpose

State the program roadmap after completion of **Phase 3 / Deliverable C**.

This memo should answer:

1. where Thin Consumer Platformization stands right now
2. what remains before the round-1 proof is credible
3. what order the remaining work should happen in
4. what should still remain blocked

This memo sits on top of:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase0_phase1a_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase2_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase3_completion.md`

## Current Program Position

The program now stands here:

| Deliverable | Status |
|---|---|
| A: Authority boundary | Done |
| B: Consumer contract | Done, with a small manual-verification tail still open or waivable |
| C: First artifact reuse proof | Done |
| D: Cross-workflow generic workspace proof | Not started |
| Round-1 proof record | Not started |

Put differently:

- the primary bounded-v2 lifecycle path is thin enough
- the consumer contract is real inside `the-critic`
- the first reusable artifact proof is now real in `analyzer-v2`
- the remaining platform proof now lives mainly in the proving vehicle: `AnalysisWorkspacePage`

## What Has Actually Been Proved So Far

The program has now proved four concrete things:

1. bounded-v2 run/result authority can live upstream instead of primarily in Critic-local in-memory state
2. `the-critic` can stop carrying duplicated bounded-v2 lifecycle code inline
3. one shared consumer contract can already serve the generic workspace and the AOI bounded surface
4. one upstream artifact class, `genealogy.relationship_classification`, is reusable across jobs through a real `corpus_ref` seam with manifest-level reuse visibility

These are substantive substrate wins.
They are still not the full round-1 proof.

## What Is Still Missing

Two things still matter before the broader thin-app story is credible.

### 1. The proving vehicle has not yet completed its job

`AnalysisWorkspacePage` is named as the proving vehicle in the execution brief.
It only counts if it can carry both bounded workflows:

- `intellectual_genealogy`
- `anxiety_of_influence_thematic_single_thinker`

through the same generic host path in a deliberate, testable way.

Right now that is not fully true.

The generic workspace already works for generic genealogy-style flow and generic restore/import behavior.
What is still missing is the bounded AOI launch-and-restore proof through that same path.

### 2. The proof record does not yet exist

The execution brief requires a short proof record tying together:

- the artifact reuse proof
- the cross-workflow workspace proof
- the final exit-criterion disposition

That memo still needs to be written after Deliverable D is complete.

## Roadmap From Here

The roadmap should now stay very short and very sequential.

## Step 0: Close Or Waive The Small Phase 2 Manual Tail

This is still cleanup, not a new phase.

Specifically:

- rerun the final manual restore-first browser checks for the Phase 2 proving surfaces, or
- write an explicit waiver that the automated coverage is sufficient

This should not reopen Deliverable B implementation.

## Step 1: Deliverable D

Return to `the-critic` and complete the proving vehicle.

The goal is narrow:

- make `AnalysisWorkspacePage` the explicit generic workspace proof surface for both bounded workflows

That means:

- genealogy works through the generic route without workflow-specific parameterization
- AOI thematic single-thinker works through the same generic route when provided one bounded thinker context
- both routes still rely on the shared bounded-v2 contract from Phase 2

This is the remaining product-facing proof.

## Step 2: Round-1 Proof Record

After Deliverable D, write the proof memo required by the execution brief.

That memo should name:

- the two workflows proved via `AnalysisWorkspacePage`
- the exact genealogy job ids used for the artifact reuse proof
- the exact Job 2 reuse signal
- the pass/fail/waived disposition of each exit criterion

## Step 3: Reassess The Program Boundary

Only after the proof record exists should the team ask:

- whether Thin Consumer Platformization round 1 is complete
- whether a Stage 10 label is warranted
- whether dynamic-composition work can be reopened

## What Should Stay Blocked

The block list remains the same.
The following should stay blocked until Deliverable D and the proof record are done:

- “apps on the fly” claims
- broad dynamic composition
- generalized bespoke-app generation claims
- broad artifact-economy expansion beyond the first bounded proof
- major AOI enrichment as the main line of work
- a broad host rewrite

## Why Deliverable D Is Next Now

This is now the correct next step because:

1. Deliverable C was the last upstream substrate proof needed before returning to the proving vehicle
2. the remaining thesis is host-side: one generic workspace path can carry both bounded workflows
3. until that proof exists, the program still risks reading as “good substrate pieces” rather than “credible thin-consumer round 1”

## Decision Rule For The Next Sessions

If a future session asks "what should we work on next?", the default answer should now be:

- **Deliverable D / Phase 4 in `the-critic`**

Only depart from that if:

- the small Phase 2 manual tail must be explicitly waived first, or
- Deliverable D uncovers a concrete blocker that requires a scoped follow-up

## Final Roadmap Sentence

If the team needs one operational sentence for the roadmap from here, it should be:

- **Complete the cross-workflow `AnalysisWorkspacePage` proof in `the-critic`, then write the round-1 proof record, and only then reopen broader thin-app claims.**
