# Memo: Thin Consumer Platformization Execution Brief

Date: 2026-03-18

## Purpose

This memo makes the post-Stage-9 program executable.

It defines:

- the program label
- the named proving vehicle
- the first artifact proof
- the immediate non-goals
- the explicit exit criteria that must be satisfied before broader dynamic-composition work is reopened

This memo sits beneath:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_snapshot_after_stage9.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_post_stage9_next_steps.md`

## Program Label

Use:

- **Thin Consumer Platformization**

Do **not** call this Stage 10 unless and until a later memo deliberately assigns that label.

## Named Proving Vehicle

The proving vehicle for this program should be:

- **The Critic's generic `AnalysisWorkspacePage`**

Concrete path:

- `/p/:projectId/analysis/:workflowKey`

Concrete bounded workflows:

- `intellectual_genealogy`
- `anxiety_of_influence_thematic_single_thinker`

## Why This Is The Right Proving Vehicle

1. It already exists and is live.
2. It is meaningfully thinner than the bespoke workflow pages.
3. It exercises the real host boundary inside an existing production-like app instead of hiding behind a fresh greenfield shell.
4. It can prove that one generic workspace path can carry at least two materially different bounded workflows.
5. It gives the program a forcing function that is concrete enough to test and hard enough to matter.

The AOI canary should remain a secondary regression canary, not the primary proof target for this next program.

## First Artifact Proof

The first artifact-economy proof must be constrained tightly.

Use:

- exactly **one** artifact class
- exactly **two** jobs
- exactly **one** freshness rule
- exactly **one** lookup path

The recommended first artifact class is:

- `genealogy.relationship_classification`

Why this artifact class:

1. It already exists as the currently acknowledged bounded artifact seam.
2. It is narrower and easier to reason about than a whole-page or whole-result reuse model.
3. It is meaningful enough to demonstrate real reuse rather than bookkeeping theater.
4. It avoids prematurely generalizing the artifact economy across every workflow family.

## What The First Artifact Proof Must Show

Job 1:

- computes and stores `genealogy.relationship_classification`
- assigns it a stable reusable identity

Job 2:

- requests the same bounded analytical situation
- resolves the prior artifact through the lookup path
- reuses it if still fresh instead of recomputing it

The first proof is successful only if the second job demonstrates actual reuse rather than a paper design.

## Exact Reuse Observable

The "visible cache hit / reuse signal" must not be satisfied by log-reading or interpretation.

For the second job, the required observable should appear in the analyzer-v2 result manifest for the
`genealogy.relationship_classification` artifact family.

The intended signal is:

- `reuse_state = "reused"`
- `reused_from_job_id = "<job-1-id>"`

If different field names are chosen during implementation, they must still satisfy the same rule:

- the second job's manifest must explicitly identify that reuse happened
- the manifest must identify the source job that supplied the reused artifact

Console logs, screenshots, or internal traces are not sufficient by themselves.

## Program Deliverables

### Deliverable A: Authority / Routing Boundary

The primary bounded v2 path must no longer depend on Critic-side background polling and in-memory run ownership.

At minimum:

- bounded v2 lifecycle truth comes from analyzer-v2
- Critic-side polling-era registries are removed from the primary path or explicitly demoted to legacy-only behavior
- run/result/restore APIs are clear enough that a generic workspace can rely on them directly

### Deliverable B: Consumer Contract / Host Adapter

There must be one reusable contract for thin consumers and host shells.

At minimum it must cover:

- start
- run discovery / polling
- cancel / resume
- result discovery
- presentation restore

The purpose is to prevent the next consumer from re-implementing the Critic integration pattern ad hoc.

### Deliverable C: First Artifact Reuse Proof

The first artifact proof must be implemented for `genealogy.relationship_classification`.

At minimum it must include:

- stable identity
- freshness rule
- lookup path
- hit/miss observability

Nothing broader should be attempted until this bounded proof works.

### Deliverable D: Cross-Workflow Generic Workspace Proof

`AnalysisWorkspacePage` must be able to carry both bounded workflows named above through the same generic consumption model.

The point is not to eliminate every bespoke surface in The Critic immediately.
The point is to prove that one generic workspace path can be the thin host for more than one serious bounded workflow.

## Proof Record Location And Owner

The short proof record for this tranche should live in:

- `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-XX_thin_consumer_platformization_round1.md`

Primary owner:

- the maintainer closing Deliverable D, because the proving vehicle lives in `the-critic` but the proof
  also needs analyzer-v2 artifact evidence

The proof record must name:

- the two bounded workflows used in the workspace proof
- the two genealogy jobs used in the artifact reuse proof
- the exact manifest-level reuse signal from Job 2
- the final disposition of each exit criterion

## Explicit Non-Goals

The following are out of scope for this first execution brief:

- multi-thinker AOI expansion
- generalized dynamic page generation for all workflows
- a full Critic rewrite
- a new standalone app generated from scratch
- broad style-school or polish expansion as the main program
- platform-wide artifact reuse across many artifact classes

## Exit Criteria

This program should not be declared complete until all of the following are true:

1. `AnalysisWorkspacePage` is the canonical generic workspace proof for both bounded workflows listed above.
2. The bounded v2 primary path no longer relies on Critic-side background polling or in-memory run authority.
3. A reusable consumer contract / host adapter exists and is used by the proving vehicle rather than copied inline.
4. `genealogy.relationship_classification` is reused across exactly two jobs through a real lookup path with a visible cache hit / reuse signal.
5. A short proof record names the two jobs, the reuse outcome, and the workspace-path success across both workflows.

## Go / No-Go Rule For Dynamic Composition

Track 4 style work remains blocked until the exit criteria above are met.

In plain terms:

- no reopening of "apps on the fly"
- no broad dynamic-composition push
- no generalized bespoke-app claims

until:

- the host boundary is thin
- the consumer contract is real
- one artifact class is genuinely reusable
- one generic workspace proves the model across two bounded workflows

## Final Recommendation

If the team needs a single operational sentence for the next tranche, it should be:

- **Make `AnalysisWorkspacePage` the forcing-function proof of a thin consumer contract, and prove one real reusable artifact before widening the platform story.**
