# Memo: Phase 4 / Deliverable D Completion

## Purpose

Record the outcome of **Phase 4 / Deliverable D: Cross-Workflow Generic Workspace Proof** in the Thin Consumer Platformization program.

This memo is the closeout for the tranche scoped in:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase4_cross_workflow_workspace_scope.md`

It should answer:

1. what work actually landed
2. what this tranche did and did not prove
3. what verification is complete versus still pending
4. what the next program step should be

## Scope Closed In This Tranche

This tranche was intended to prove one bounded thing:

- **`AnalysisWorkspacePage` can now serve as the deliberate generic proof surface for both bounded workflows**

More specifically, the tranche was meant to:

- keep genealogy working through the existing generic route
- add AOI single-thinker bounded context to the generic route
- keep both workflows on the shared bounded-v2 contract from Phase 2
- add one explicit AOI handoff into the generic proof route
- keep generic AOI manual `Preview V2` / `Import + Save` out of acceptance

This tranche was **not** intended to prove:

- a dynamic workflow-input system
- generalized form/schema-driven launch UX
- replacement of `GenealogyPage` or the bespoke AOI pages
- multi-thinker AOI on the generic route
- analyzer-v2 API changes
- a broader dynamic-composition or “apps on the fly” claim

## Completed Work

### AOI bounded context now exists on the generic route

`/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`

The generic workspace now reads:

- `selected_source_thinker_id`
- `selected_source_thinker_name`

from URL query params and treats `selected_source_thinker_id` as the authoritative AOI input.

The page now:

- derives `isAoiWorkflow`
- passes `selectedSourceThinkerId` into `useBoundedV2Workspace`
- passes `selectedSourceThinkerId` into `discoverBoundedV2Results`
- shows lightweight page context:
  - `Thinker: {selected_source_thinker_name ?? selected_source_thinker_id}`

### AOI launch, hydrate, and restore behavior now match the proof contract

The generic page now:

- injects `selected_source_thinker_id` and optional `selected_source_thinker_name` into the AOI launch body
- refuses AOI generic launch when thinker context is missing
- refuses AOI hydrate/discovery when thinker context is missing
- renders a bounded guidance state telling the user to open the generic route from a thinker page

The optimistic AOI job now also carries thinker identity, so the short-lived in-flight job record matches the real upstream run shape.

### AOI saved-result behavior is now thinker-scoped on the generic page

The generic page's local result types were expanded to include:

- `selected_source_thinker_id`
- `selected_source_thinker_name`

The page now mirrors the bespoke AOI matching semantics:

- local saved results are filtered by thinker before merge
- upstream discovery is thinker-scoped through `selectedSourceThinkerId`
- merged results are defensively re-filtered by thinker before auto-restore

This closes the previous risk where the generic AOI route could auto-restore the wrong thinker's result.

### Generic AOI manual Preview / Import remains excluded

The generic AOI route now hides the manual `Load from v2` controls rather than trying to patch generic AOI preview/import into acceptance for this tranche.

That keeps the proof narrow:

- generic AOI launch
- thinker-scoped discovery
- thinker-scoped restore

and avoids widening into local metadata-preservation work.

### AOI proof-route handoff now exists

`/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx`

The thinker detail header now includes an explicit handoff to:

- `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=<id>&selected_source_thinker_name=<name>`

This is a proof-route affordance only.

It does **not** replace:

- the bespoke AOI tabs
- AOI default routing
- the richer bespoke surfaces

## What Was Not Touched

- `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
- analyzer-v2 API contracts
- `GenealogyPage`
- the bespoke AOI panel as the primary AOI surface

## Scope-Discipline Note

The working trees still contain unrelated local edits in both repos.

This memo's completion claim is narrower:

- no analyzer-v2 change was required for Deliverable D
- no shared bounded-v2 contract change was required for Deliverable D
- no generalized workflow-input or dynamic-form work was introduced

That should not be misread as a claim that either repo was globally clean.

## Automated Verification Completed

The following verification was rerun successfully from:

- `/home/evgeny/projects/the-critic/webapp`

Command:

- `CI=true npm test -- --watch=false src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx src/pages/AnxietyOfInfluencePages.test.tsx src/lib/boundedV2Client.test.ts src/hooks/useBoundedV2Workspace.test.tsx`

Result:

- `5` suites passed
- `33` tests passed

This verification now covers:

- AOI query-param parsing on the generic route
- AOI launch body composition
- AOI thinker-scoped active-run and result discovery
- AOI thinker-scoped local saved-result filtering and auto-restore
- the explicit AOI handoff to the generic proof route
- the shared bounded-v2 client and hook remaining stable

One caveat remains:

- `useBoundedV2Workspace.test.tsx` still emits pre-existing non-failing React `act(...)` warnings

Those warnings are not new in this tranche and did not cause test failures.

## Manual Verification Status

The manual acceptance checks expected by the Phase 4 scope memo were **not yet recorded** in this tranche.

That means the current status is:

- code-complete
- automated-verification complete
- proof-complete in substance
- still pending one short operator acceptance pass, or an explicit written waiver

The still-open manual items are:

1. one generic genealogy run or restore via `AnalysisWorkspacePage`
2. one generic AOI single-thinker run or restore via `AnalysisWorkspacePage`
3. confirmation that AOI active-run discovery and saved-result restore are thinker-scoped in that operator flow

Separately, the small Phase 2 manual tail remains unresolved unless it is explicitly waived in the next closure step.

## What This Tranche Actually Proved

Phase 4 now proves:

1. `AnalysisWorkspacePage` can act as the same generic host for both bounded workflows
2. AOI single-thinker can use explicit bounded route context without reopening Phase 2
3. the shared bounded-v2 contract from Phase 2 is sufficient for both genealogy and AOI generic-route behavior
4. the AOI generic route can be deliberately exercised from the bespoke AOI surface
5. the tranche stayed narrow and did not drift into a dynamic-form or page-replacement program

## What This Tranche Still Does Not Prove

Phase 4 does **not** yet prove:

1. recorded operator acceptance for the generic genealogy and AOI proof routes
2. closure or waiver of the small Phase 2 manual-verification tail
3. the round-1 proof record required by the execution brief
4. that broader dynamic-composition claims may be reopened

## Acceptance Criteria Disposition

| Criterion | Status |
|---|---|
| Generic route runs/restores `intellectual_genealogy` | PASS |
| Generic route runs/restores AOI single-thinker with bounded thinker context | PASS |
| AOI launch body includes thinker id and optional name | PASS |
| AOI active-run, upstream-result, and local saved-result behavior are thinker-scoped | PASS |
| Both workflows rely on the shared Phase 2 bounded-v2 contract | PASS |
| AOI proof route is reachable from the bespoke AOI surface | PASS |
| No widening into dynamic-form or input-schema work | PASS |
| Bespoke genealogy and AOI pages remain intact | PASS |
| Generic AOI manual Preview / Import remains excluded from acceptance | PASS |

The honest qualifier is:

- all scoped acceptance criteria now pass in code and automated verification
- operator acceptance is still pending or waivable

## Recommended Next Move

The next program step should now be:

- **Round-1 proof record and exit-criterion closure**

That step should stay narrow and should include:

1. record or waive the remaining manual verification tails
2. assemble the exact evidence required by the execution brief
3. write the required proof record at:
   - `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-XX_thin_consumer_platformization_round1.md`

The next step should not reopen Deliverables A through D except for a tiny verification-only aid if the proof record cannot otherwise name exact artifact-proof job ids honestly.

## Final Status Sentence

If the team needs one operational sentence for the state after this tranche, it should be:

- **The cross-workflow `AnalysisWorkspacePage` proof is now real in `the-critic`; the remaining blocked item is the round-1 proof record and evidence closure, not another product feature tranche.**
