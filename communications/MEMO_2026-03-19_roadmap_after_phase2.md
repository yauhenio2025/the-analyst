# Memo: Roadmap After Phase 2

## Purpose

State the program roadmap after the completion of **Phase 2 / Deliverable B**.

This memo should answer:

1. where the Thin Consumer Platformization program stands right now
2. what remains to be proved before the larger platform story is credible
3. what order the remaining work should happen in
4. what should explicitly remain blocked

This memo sits on top of:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_post_stage9_next_steps.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/PLAN_2026-03-18_thin_consumer_platformization_implementation.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase0_phase1a_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase2_completion.md`

## Current Program Position

The program now has the following status:

- **Stage 9 / AOI cutover**: functionally closed
- **Deliverable A / authority boundary**: completed enough to proceed
- **Deliverable B / consumer contract**: completed in substance
- **Deliverable C / artifact reuse proof**: not started
- **Deliverable D / cross-workflow generic workspace proof**: not started
- **Round-1 proof record**: not started

Put differently:

- the host boundary is much thinner than before
- the shared consumer contract is now real
- the critical missing proof is now upstream artifact reuse

## What Has Actually Been Proved So Far

The program has now proved three concrete things:

1. bounded-v2 lifecycle truth can live upstream instead of being primarily Critic-owned
2. The Critic can stop copying the same bounded-v2 consumer logic inline
3. one thin consumer contract can already serve two bounded surfaces inside the same app

These are meaningful substrate wins.
They are not yet the full platform proof.

## What Is Still Missing Before The Bigger Vision Is Credible

The missing layers are now narrower and clearer than they were 24 hours ago.

### 1. Reusable artifact identity is still unproved

The code already has:

- a named artifact family for genealogy relationship classification
- artifact-family summaries in result manifests
- corpus registration and artifact-family freshness/state machinery

But it does **not** yet prove:

- that a later job can resolve and reuse an earlier artifact through a real lookup path
- that reuse is visible in the result contract rather than inferred from logs

Until that exists, the platform still behaves like:

- thinner host shells over job-scoped outputs

not:

- a reusable analysis-product substrate

### 2. The generic workspace has not yet proved cross-workflow sufficiency

`AnalysisWorkspacePage` now participates in the contract proof.
It has **not** yet proved that it can be the canonical thin host for both:

- `intellectual_genealogy`
- `anxiety_of_influence_thematic_single_thinker`

through one deliberately exercised generic path.

### 3. The proof record does not yet exist

The execution brief required a round-1 proof memo tying together:

- artifact reuse evidence
- cross-workflow workspace evidence
- exit-criterion disposition

That is still future work.

## Roadmap From Here

The roadmap should remain deliberately sequential.

## Step 0: Close Or Waive The Small Phase 2 Tail

This is not a new phase.
It is just cleanup discipline.

Specifically:

- rerun the two manual restore-first checks after the final import-fallback repair, or
- write an explicit waiver if the automated coverage is judged sufficient

This should not reopen the implementation of Deliverable B.

## Step 1: Deliverable C

Implement the first reusable-artifact proof in `analyzer-v2`.

Bound it tightly:

- artifact class: `genealogy.relationship_classification`
- jobs: exactly 2
- freshness rule: exactly 1
- lookup path: exactly 1
- required observable on Job 2:
  - `reuse_state = "reused"`
  - `reused_from_job_id = "<job-1-id>"`

For this first proof, the intended seam is:

- contract-level reuse of the stored artifact on the existing `corpus_ref` seam

not:

- a broad executor-time “no recompute” proof for the underlying phase-1.5 engine path

This is the most important next proof because it decides whether the platform is merely a better host integration or an actual reusable analysis-product substrate.

## Step 2: Deliverable D

Once Deliverable C is real, return to `the-critic` and complete the proving vehicle.

Goal:

- make `AnalysisWorkspacePage` the explicit generic workspace proof surface for both bounded workflows

This should include:

- genealogy through the generic path
- AOI thematic through the generic path
- the same shared consumer contract

This is where the host-side proof becomes fully credible.

## Step 3: Round-1 Proof Record

After Deliverables C and D, write the round-1 proof record required by the execution brief.

That memo should name:

- the two genealogy jobs used in the artifact proof
- the reuse signal from Job 2
- the two workflows carried by `AnalysisWorkspacePage`
- the final pass/fail/deferred disposition of each exit criterion

## Step 4: Reassess The Program Boundary

Only after the proof record exists should the team ask:

- whether Thin Consumer Platformization round 1 is complete
- whether a broader Stage 10 label is warranted
- whether dynamic composition work should be unblocked

## What Should Stay Blocked

The memo trail is consistent on this.
The following should remain blocked until Deliverables C and D are actually complete:

- “apps on the fly” claims
- broad dynamic composition
- generalized bespoke-app generation claims
- platform-wide artifact economy expansion beyond the first bounded proof
- major new AOI enrichment as the main line of work
- a broad host rewrite

## Why Deliverable C Must Come Before Deliverable D

This order is not arbitrary.

If Deliverable D happens before Deliverable C, the program risks proving only that:

- one UI shell can read two workflow families

That is useful, but weaker than the intended thesis.

The stronger thesis is:

- the host is thin
- the consumer contract is real
- one artifact class is upstream-reusable
- one generic workspace can ride on top of that substrate across two workflows

That is why the artifact proof should come first.

## Decision Rule For The Next Sessions

If a future session asks "what should we work on next?", the default answer should now be:

- **Deliverable C / Phase 3 in `analyzer-v2`**

Only depart from that if:

- the small Phase 2 manual tail must be closed first, or
- Deliverable C uncovers a concrete blocker that must be resolved before the artifact proof can proceed

## Final Roadmap Sentence

If the team needs one operational sentence for the roadmap from here, it should be:

- **Finish the first real reusable-artifact proof in `analyzer-v2`, then use that substrate to complete the cross-workflow `AnalysisWorkspacePage` proof, and only then reopen the broader thin-app platform story.**
