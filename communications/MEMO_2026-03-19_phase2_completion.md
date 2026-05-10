# Memo: Phase 2 / Deliverable B Completion

## Purpose

Record the outcome of **Phase 2 / Deliverable B: Consumer Contract / Host Adapter** in the Thin Consumer Platformization program.

This memo is the closeout for the tranche scoped in:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase2_consumer_contract_scope.md`

It should answer four questions:

1. what work actually landed
2. what this tranche did and did not prove
3. what verification is complete versus still pending
4. what the next program step should be

## Scope Closed In This Tranche

This tranche was intended to prove one bounded thing:

- there is now a real shared bounded-v2 consumer contract inside `the-critic`

More specifically, the tranche was meant to:

- extract the repeated bounded-v2 run/result/restore/refresh/poll lifecycle seam
- make `AnalysisWorkspacePage` use that seam
- make `AoiV2ThematicPanel` use that same seam
- keep `GenealogyPage` out of the first adoption set
- avoid widening into launch/import unification, generalized UI abstraction, or analyzer-v2 changes

This tranche was **not** intended to prove:

- artifact reuse
- cross-workflow generic workspace proof completion
- generalized dynamic composition
- a broader Stage 10 style platform claim

## Completed Work

### Shared consumer contract landed in `the-critic`

The frontend now has a real shared bounded-v2 contract layer:

- `webapp/src/types/boundedV2.ts`
- `webapp/src/lib/boundedV2Client.ts`
- `webapp/src/hooks/useBoundedV2Workspace.ts`

The contract now owns the duplicated bounded-v2 lifecycle seam:

- active-run discovery
- run-by-job polling
- result manifest lookup
- result presentation restore
- refresh-presentation
- cache handoff
- restore-first fallback behavior

### Two bounded adopters now use the same contract

The shared contract is now consumed by:

- `webapp/src/pages/AnalysisWorkspacePage.tsx`
- `webapp/src/components/influence/AoiV2ThematicPanel.tsx`

This means the proving pair named in the Phase 2 scope memo is now real in code.

### The extraction stayed within the intended boundary

The implementation did **not** broaden into:

- `GenealogyPage` migration
- generalized launch-path unification
- analyzer-v2 API/schema changes
- dynamic page-composition work

The shared utility layer also remained canonical:

- `webapp/src/utils/resultContract.ts`
- `webapp/src/utils/presentationFreshness.ts`

### Post-implementation tightening work was required and completed

After the initial extraction, the tranche needed three targeted repairs:

1. restore the `completed_at || prepared_at || ''` fallback for upstream-discovered saved results
2. tighten the hook boundary so pages no longer push raw hook-owned state directly
3. fix the generic import fallback so an imported normalized job still enters hook state when there is no preexisting `currentJob`

Those repairs are now in place.

## Automated Verification Completed

The following verification was completed successfully after the final import-fallback repair:

- `CI=true npm test -- --watch=false --runTestsByPath src/lib/boundedV2Client.test.ts src/hooks/useBoundedV2Workspace.test.tsx src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx src/components/influence/AoiV2ThematicPanel.test.tsx src/utils/presentationFreshness.test.ts src/pages/AnxietyOfInfluencePages.test.tsx`
- result: `7` suites passed, `32` tests passed
- `npx tsc --noEmit`
- result: passed

Key regression coverage now exists for:

- the shared bounded-v2 client mapping / transport layer
- the shared restore-first hook behavior
- real page-plus-hook mount orchestration for `AnalysisWorkspacePage`
- thinker-scoped AOI host-adapter wiring
- the no-active-job import fallback bug

## Manual Verification Status

The manual restore-first browser checks expected by the Phase 2 scope memo were **not rerun after the final import-fallback repair**.

That means this tranche currently has:

- strong automated acceptance
- no known failing operator path
- one remaining manual acceptance tail if the team wants strict closure against the original Phase 2 verification expectation

This should be treated as a real but bounded residual, not ignored and not inflated into a blocker.

## What This Tranche Actually Proved

Phase 2 now proves:

1. The shared consumer contract is real, not memo-fiction.
2. The proving vehicle and the AOI bounded surface now import the same bounded-v2 lifecycle layer instead of carrying separate inline implementations.
3. No analyzer-v2 change was required to make the host contract real.
4. The program can keep moving without reopening Phase 0 / Phase 1A or Stage 9 work.

## What This Tranche Still Does Not Prove

Phase 2 does **not** yet prove:

1. reusable artifacts across jobs
2. the cross-workflow `AnalysisWorkspacePage` proof target described in Deliverable D
3. generalized thin-app generation or dynamic composition
4. that the broader platform vision is already complete

In other words:

- this tranche is the **contract proof**
- not the **artifact proof**
- not the **cross-workflow proof**

## Residuals

### Residual 1: Manual restore-first acceptance rerun is still pending

The scoped memo expected:

- one manual restore-first verification of `AnalysisWorkspacePage`
- one manual restore-first verification of `AoiV2ThematicPanel`

Those browser checks were not rerun after the final import-fallback fix.

Recommended disposition:

- perform them as a short operator acceptance pass, or
- explicitly waive them if the team judges the targeted automated coverage sufficient for this tranche

### Residual 2: Test output still emits existing React `act(...)` warnings

The focused frontend suite passes cleanly, but the output still contains existing non-failing `act(...)` warnings around asynchronous mount/poll flows.

This is worth cleaning up later, but it is not a Phase 2 blocker.

## Acceptance Call

This tranche should be treated as:

- **code-complete**
- **automated-verification complete**
- **functionally accepted**

With one important qualifier:

- strict operator acceptance is still pending one short manual restore-first rerun, unless that item is explicitly waived

So the honest closeout status is:

- **Phase 2 / Deliverable B is complete in substance**
- **with a small manual-verification tail**

## Recommended Next Move

The next program step should remain the one already named in the execution brief and implementation plan:

- **Phase 3 / Deliverable C: first artifact reuse proof in `analyzer-v2`**

Specifically:

- artifact class: `genealogy.relationship_classification`
- proof shape: exactly two jobs
- one stable identity
- one freshness rule
- one lookup path
- manifest-level reuse signal on Job 2:
  - `reuse_state = "reused"`
  - `reused_from_job_id = "<job-1-id>"`

Why this is next:

1. The memo trail from the last 24 hours is consistent that Deliverable B was only the contract proof.
2. The execution brief explicitly blocks wider dynamic-composition claims until one artifact class is genuinely reusable.
3. Deliverable D depends on Deliverable C if the team wants the generic-workspace proof to represent a real platform substrate instead of a thinner UI wrapper over ephemeral job outputs.

So the near-term order should be:

1. optionally close or waive the small Phase 2 manual-verification tail
2. start Phase 3 / Deliverable C in `analyzer-v2`
3. only after that move to Deliverable D / cross-workflow generic workspace proof

## Final Status Sentence

If the team needs one operational sentence for the state after this tranche, it should be:

- **The shared thin-consumer contract is now real in `the-critic`; the next real missing proof is reusable artifacts in `analyzer-v2`, not more host extraction.**
