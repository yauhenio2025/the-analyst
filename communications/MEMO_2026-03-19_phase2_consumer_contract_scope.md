# Memo: Phase 2 Scope - Consumer Contract / Host Adapter

Date: 2026-03-19

## Purpose

This memo scopes the next immediate tranche after the accepted completion of:

- Phase 0: Stage 9 closure tail
- Phase 1A: Critic bounded-v2 authority cleanup

The next tranche should be:

- **Phase 2 / Deliverable B**
- **Consumer Contract / Host Adapter**

This memo is meant to prevent the next step from drifting into:

- more Stage 9 work
- premature artifact-economy work
- premature AOI launch generalization
- generalized "apps on the fly" claims

It sits beneath:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_post_stage9_next_steps.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/PLAN_2026-03-18_thin_consumer_platformization_implementation.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase0_phase1a_completion.md`

## Why This Is The Right Next Tranche

Phase 0 / Phase 1A already established the prerequisite boundary:

- Stage 9 is functionally closed
- The Critic no longer needs to act as primary lifecycle authority for bounded v2 jobs
- restore-first behavior was manually proved in both the generic workspace and the AOI bounded saved-result path

That means the main remaining blocker is not authority.
It is duplicated consumer logic.

Today, the same bounded-v2 client behavior is still copied across multiple Critic surfaces.
The strongest repeated seam is in:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx`

The duplicated behaviors include:

- `fetchResultPresentation`
- `fetchRunStatus`
- `cacheV2Presentation`
- `refreshStoredV2Presentation`
- local-saved-result restore fallback
- upstream saved-result restore attempt
- result-state notice logic around restore / snapshot / refresh

This duplication is especially visible in the restore-first path.
That makes Deliverable B the correct next move.

## Scope Decision

This tranche should stay intentionally narrow.

### In scope

- build one shared bounded-v2 consumer contract inside `the-critic`
- make `AnalysisWorkspacePage` use it
- make `AoiV2ThematicPanel` use it
- keep the contract centered on bounded run/result/presentation lifecycle behavior
- preserve current restore-first semantics

### Out of scope

- analyzer-v2 schema or API changes unless a concrete blocker appears
- AOI launch UX in `AnalysisWorkspacePage`
- the first artifact-reuse proof
- multi-thinker AOI
- package extraction of the contract outside `the-critic`
- broad page-composition or renderer abstraction
- a generalized dynamic-form system for workflow inputs
- a full migration of `GenealogyPage` unless it becomes a low-risk follow-on after the main proof

## Concrete Deliverable

The deliverable is not "clean up some frontend code."

The deliverable is:

- a shared bounded-v2 client / host-adapter layer that the proving vehicle imports instead of copying inline

The proving vehicle remains:

- `AnalysisWorkspacePage`

The required second bounded consumer for this tranche is:

- `AoiV2ThematicPanel`

`GenealogyPage` should be treated as:

- a comparison surface
- a regression reference
- an optional follow-on adopter only if the first two adoptions are already stable

This matters because the execution brief requires:

- one reusable consumer contract
- used by the proving vehicle
- and used by at least one second bounded surface

That requirement can be met without broadening the tranche further.

## Recommended Shape

The shared contract should be split into two layers inside `the-critic`.

### Layer 1: bounded-v2 client

Recommended file:

- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`

Responsibility:

- wrap network calls to analyzer-v2 and Critic for bounded-v2 lifecycle operations

At minimum it should cover:

- run-by-job fetch
- run discovery fetch
- result manifest fetch
- result presentation fetch
- refresh-presentation
- cache-v2 handoff to Critic

This layer should centralize:

- URL construction
- `consumer_key` / presenter consumer query usage
- response-shape parsing
- consistent transport-level error handling

This layer should **not** make the following part of the Phase 2 minimum:

- generic workflow start wrappers
- AOI launch wrappers
- import helpers
- page-owned cancel / resume UX flows if they do not naturally collapse into the same transport shape

Those can remain page-local in this tranche unless a small, obvious shared wrapper emerges during implementation.

### Layer 2: restore-first host adapter

Recommended file:

- `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts`

Responsibility:

- hold the reusable restore / refresh / saved-result decision logic that is currently copied inline

At minimum it should cover:

- restoring a selected saved result candidate
- choosing upstream restore vs Critic-local snapshot
- background refresh of a cached presentation
- cache-after-restore handoff when upstream presentation is restorable
- result-state notice selection using the existing result-contract helpers
- bounded run polling support for active jobs
- completed-to-preparing transition polling support while restore is still converging
- callback-based integration points for page-owned state updates

The hook must acknowledge one real boundary explicitly:

- it should expose an `onPresentationLoaded`-style callback (or equivalent)

Reason:

- `AoiV2ThematicPanel` updates tab state when presentations load
- `AnalysisWorkspacePage` uses a different tab/deep-link model
- tab ownership must remain page-local even when restore orchestration is shared

The hook should also accept optional bounded filters needed by the second adopter:

- `selected_source_thinker_id`

This layer should not try to own:

- page layout
- tabs
- AOI-specific launch inputs
- saved-results list discovery / merge rules
- workflow-specific presentation chrome
- per-page saved-result list rendering

Those concerns should remain local to the page/component using the contract.

## Existing Shared Surface To Reuse

This tranche should extend what already exists rather than invent a parallel abstraction.

The current shared utility baseline is:

- `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts`
- `/home/evgeny/projects/the-critic/webapp/src/utils/presentationFreshness.ts`

Those should remain the canonical home for:

- result-manifest typing
- run/result helper predicates
- freshness comparison
- restore/snapshot notice text

The new contract layer should import and compose those helpers.
It should not redefine them.

## Explicit Non-Goals Inside The Extraction

To keep this tranche from expanding, the following should stay local even if they are somewhat duplicated:

- active-tab state
- tab default selection
- view lazy-loading via `/v1/presenter/view/...`
- saved-result list discovery and local/upstream merge rules
- workflow-specific saved-result list row types
- AOI-specific launch payload assembly
- AOI thinker-specific list filtering semantics
- genealogy prose fallback / legacy mixed-mode state
- page-specific empty states and explanatory copy

If any of those are extracted during this tranche, the scope is drifting.

## Acceptance Criteria

This tranche should be treated as done only if all of the following are true:

1. `AnalysisWorkspacePage` imports a shared bounded-v2 contract layer instead of carrying its own inline run/result/restore orchestration.
2. `AoiV2ThematicPanel` imports the same shared bounded-v2 contract layer instead of carrying its own inline run/result/restore orchestration.
3. The shared contract preserves restore-first behavior:
   - Critic-local saved presentation can still render when optional upstream fetches fail
   - upstream presentation can still replace the snapshot when restorable and fresher
4. Existing shared result helpers remain canonical:
   - `resultContract.ts`
   - `presentationFreshness.ts`
5. No analyzer-v2 changes are required, or any required change is proven to be a concrete blocker rather than speculative cleanup.
6. The extraction does not silently broaden into generic launch/import unification or GenealogyPage migration.
7. The shared contract preserves the current refresh/cache semantics unless a deliberate memo-level decision changes them later.

## Verification Expectations

The expected verification for this tranche should be:

- targeted frontend tests for the shared client / host-adapter behavior
- updated page/component tests proving the shared layer is used
- one manual restore-first verification of `AnalysisWorkspacePage`
- one manual restore-first verification of `AoiV2ThematicPanel`

Implementation should assume that `AoiV2ThematicPanel` currently lacks meaningful lifecycle-level regression coverage.
So this tranche should establish that coverage through the new shared contract tests rather than waiting for a separate pre-extraction hardening pass.

The verification target is behavioral sameness with less duplicated host logic.
It is not visual redesign.

## Failure Modes To Watch For

The main ways this tranche can go wrong are:

- extracting too much and accidentally turning page-specific UI state into a fake generic abstraction
- trying to unify every saved-result type instead of sharing only the bounded-v2 lifecycle logic
- dragging `GenealogyPage` into the same edit set too early
- broadening into AOI launch generalization before the consumer contract proof exists
- retyping result-manifest logic instead of reusing the existing shared utilities
- simplifying polling to only `pending` / `running` and breaking the post-completion preparation window
- changing snapshot persistence behavior incidentally while moving refresh/cache logic

## Resulting Program Order

If this tranche is executed successfully, the next order should remain:

1. **Phase 2 / Deliverable B**: shared consumer contract in `the-critic`
2. **Phase 3 / Deliverable C**: first artifact reuse proof in `analyzer-v2`
3. **Phase 4 / Deliverable D**: make `AnalysisWorkspacePage` the real cross-workflow proof surface for genealogy + AOI
4. write the proof memo

This means the current tranche should be treated as:

- the contract proof
- not the artifact proof
- not the cross-workflow proof completion
- not a reopened architecture-search phase

## Final Scope Sentence

If the team needs one operational sentence for the next step, it should be:

- **Extract one shared bounded-v2 consumer contract in `the-critic`, make `AnalysisWorkspacePage` and `AoiV2ThematicPanel` use it, and keep everything else out of scope.**
