# Memo: Stage 5 / AOI Exemplar Exit Gate Scope

Date: 2026-03-24
Status: Draft scope memo
Program: Dynamic Bespoke Apps Platformization
Depends on:
- `communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md`
- `communications/MEMO_2026-03-24_stage3_4_aoi_exemplar_cutover_completion.md`
Roadmap sources:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

## Summary

Stage 3/4 Milestone A is now implemented.

The next honest step is not more AOI architecture.
It is the Stage 5 exit gate over the planner-primary AOI seam that now exists.

This step should decide whether the AOI exemplar is stable enough to stand as the first real task-first reference app loop on top of analyzer-v2.

It should also decide whether canonical Stage 2 can now be documentary-closed as a side-effect.

The acceptance seam is already fixed:

- `route-task`
- `plan-task`
- planner-backed AOI handoff with explicit selection law
- `compose-from-selection`
- rendered transient AOI result in `the-critic`

This scope is therefore an evidence-and-evaluation tranche.
It is not a new structural rewrite unless the evaluation itself exposes one small proof-surface compatibility gap that must be fixed.

## Why This Is The Next Honest Step

The program now has the right Stage 3/4 substrate:

- AOI routing is generic rather than profile-instructive
- AOI planning now owns bounded selection
- the planner path is no longer forced back through `dossier | comparison`
- blocked AOI selection outcomes are explicit and fail closed
- blocked-path selector provenance is now saved strongly enough for audit
- the host consumes planner-selected and rejected source law on the proof path

What is still missing is the evidence line that makes AOI a finished exemplar rather than a strong engineering slice:

- fixed eval cases
- a saved rubric
- thresholds
- operational observations
- explicit blocked/ambiguous case handling review
- one honest decision about whether Stage 2 is now actually closed

Without that gate, the program would move to later transient generalization on top of a seam that is technically strong but not yet empirically ratified.

## Bounded Claim

The bounded claim for this tranche is:

- the new planner-primary AOI seam is stable enough, observable enough, and honest enough to serve as the first exemplar reference loop for later platform work

This tranche does **not** claim:

- cross-workflow generalization
- second-consumer transient adoption
- lifecycle closure
- removal of all host continuity residuals
- arbitrary engine-graph planning
- a final “build any app” platform closure

## Scope Decisions

### Decision 1: Evaluate the landed seam, do not redesign it by default

This is an exit-gate tranche, not a second Stage 3/4 architecture memo.

Default assumption:

- the Milestone A planner-primary seam is the thing being evaluated

Allowed exception:

- one small compatibility or observability fix may be landed if the eval run exposes a real proof-surface mismatch

Not allowed:

- reopening the public contract shape just because the eval pack is hard
- broad UI redesign
- lifecycle expansion
- jumping ahead to de-AOI / de-`the-critic` transient generalization

### Decision 2: Keep the proof surface narrow

The only product surface that should count for this exit gate is the current planner-primary AOI path in `the-critic`:

- `AoiV2ThematicPanel.tsx`
- `AoiComposeFromIntentPage.tsx`

Legacy profile-first controls may still exist in collapsed debug areas, but they do not count toward acceptance.

### Decision 3: Use a fixed four-case AOI eval pack

The eval pack should contain exactly four required case types:

1. one evolution-focused ready case
2. one engagement-focused ready case
3. one locked non-profile ready case
4. one real planner-primary `aoi_selection_blocked` case

The locked non-profile case should remain:

- `thematic_synthesis + engagement_mapping + thematic_report` without `sin_findings`

If the tranche cannot support that case honestly, the tranche should fail rather than relabel a profile-shaped case as novel.

Readiness-discovery caveat for the locked non-profile case:

- the current readiness surface still reports profile-shaped selectors rather than arbitrary source-family combinations
- so this locked eval case should run through direct planner-to-compose continuation from `plan-task` into `compose-from-selection`
- it should not be counted as a readiness-discovery proof unless one small readiness-surface compatibility fix is intentionally added during the tranche

### Decision 4: Save the full planning and launch trail for each case

For each eval case, save artifacts that allow later review of:

- task input
- route decision
- plan decision
- selected sources
- rejected sources
- planner rationale
- planner provenance:
  - prompt version
  - model
  - timeout
  - provider outcome
  - validator version
- compose request payload
- rendered result or blocked state
- responsiveness notes:
  - planner selection latency
  - composition latency
  - total user-visible latency
- whether the case was proof-fixture-backed or stronger than that

The point is not just to save screenshots.
It is to make the planner and compose seam auditable.

Because the current code exposes this trail but does not persist it automatically, the tranche should require one concrete capture method.

Default capture method:

- one browser-network HAR or equivalent network export per case from the real `the-critic` session
- one saved JSON request/response excerpt set per case for:
  - `route-task`
  - `plan-task`
  - host `compose-from-selection` request payload
  - analyzer `compose-from-selection` response excerpt

For this memo, "planner rationale" should mean only:

- `selection_summary`
- selected-source `rationale`
- rejected-source `rejection_reason`

### Decision 5: Stage 2 closure must be decided explicitly here

This tranche should not silently assume that Stage 2 is now closed.

The closeout must say one of:

- Stage 2 is now documentary-closed as a side-effect of the AOI exemplar eval pack
- Stage 2 remains open because the eval evidence is still too weak or too fixture-bound

That decision should be tied to explicit evidence, not convenience.

Concrete non-closure examples:

- all ready cases are only fixture-backed
- the locked non-profile case cannot be demonstrated honestly on the planner-primary path
- the required negative case is not a real `aoi_selection_blocked` selector-path outcome
- the eval pack cannot show repeated bounded AOI transient use strongly enough to support the old Stage 2 MVP claim

### Decision 6: Remaining host residuals are allowed, but must be carried into the exit record

These host-side residuals are still allowed on the proof path for this exit gate:

- host-proxy identity translation
- snapshot warmup

Planner-backed refresh/deep-link continuity is also still allowed to remain broken in this tranche.

But the closeout must record all three explicitly if they remain:

- host-proxy identity translation
- snapshot warmup
- planner-backed refresh/deep-link discontinuity

### Decision 7: No hidden legacy fallback may count toward acceptance

The exit gate should fail if any required proof case succeeds only because the host or analyzer silently fell back to the old profile-first path.

That means:

- no planner-primary case may pass by routing back into legacy dossier/comparison controls as the authoritative choice
- no planner-primary case may require reinterpreting the result as “really just a profile case” after the fact
- the required negative case must remain a real `aoi_selection_blocked` outcome in the planner-primary path

### Decision 8: Fixture strength must be labeled with one shared tier model

Every eval case must be labeled using one of these tiers:

1. `fixture_backed`
   - recomposition over saved outputs from a prior controlled proof run
2. `execution_backed`
   - fresh end-to-end run against a known corpus with newly produced outputs
3. `user_initiated`
   - fresh run triggered from a real user-facing task rather than a proof script

For this exit gate:

- `fixture_backed` cases are acceptable for seam audit
- but Stage 2 should not be documentary-closed unless at least one ready case is `execution_backed` or stronger

### Decision 9: The rubric must be written before grading and must use explicit pass/fail thresholds

The rubric should be saved before the case pack is graded.

Each required dimension must have an explicit pass/fail boundary that a later reviewer could apply independently:

- selection fit
- rationale clarity
- rendered usefulness
- operational behavior

Minimum threshold shape:

- every case must pass `operational_behavior`
- every ready case must pass `selection_fit` and `rendered_usefulness`
- the locked non-profile ready case must pass without legacy fallback and without being reclassified as profile-shaped after the fact
- the `aoi_selection_blocked` case must pass on honest blocked visibility and auditability rather than on rendered richness

## Proposed Deliverables

### 1. AOI exemplar evaluation pack

One saved pack with four fixed cases:

- evolution-focused
- engagement-focused
- locked non-profile
- one real `aoi_selection_blocked` selector-path case

### 2. AOI exemplar rubric memo or rubric section

The tranche should save one rubric with explicit dimensions:

- selection fit
- rationale clarity
- rendered usefulness
- operational behavior

Thresholds must be concrete enough to support a closeout decision.
The rubric should be written before the eval pack is graded, not after.

### 3. Saved proof artifacts

For each case, save:

- task input
- routing/planning artifacts
- selected/rejected source artifact
- planner provenance artifact
- host compose request artifact
- analyzer compose response excerpt
- rendered output or blocked state artifact
- responsiveness notes:
  - planner selection latency
  - composition latency
  - total user-visible latency
- fixture-strength tier

### 4. One explicit exit-gate closeout note

The closeout note must state:

- whether Stage 2 is now documentary-closed
- whether the planner-primary path is credible enough to treat AOI as a real exemplar reference
- whether any ready case still mapped to `legacy_profile_equivalent`
- which host residuals remained
- whether refresh/deep-link continuity remained out of scope
- what still remains open before later transient generalization

## Non-Goals

This tranche should not widen into:

- new public contract families
- second-consumer transient proof
- de-AOI / de-`the-critic` substrate generalization
- lifecycle or persistence semantics
- broader governance infrastructure
- removing all AOI legacy UI everywhere

## Exit Evidence

This tranche should count as complete only if it produces:

1. one saved eval pack with the four fixed AOI case types
2. one saved rubric with thresholds and an explicit pass/fail judgment
3. one real `aoi_selection_blocked` planner-primary case surfaced honestly
4. one locked non-profile ready case that is not quietly collapsed back into legacy profile law
5. one closeout note that explicitly decides:
   - Stage 2 closure or non-closure
   - remaining host residuals
   - refresh/deep-link status
   - whether the cases were `fixture_backed`, `execution_backed`, or `user_initiated`

The closeout should also remain explicit about what this does **not** prove:

- it does not close Stage 13 Tier B
- it does not prove host-neutral transient composition
- it does not resolve lifecycle
- it does not prove general multi-app platform closure

## Strategic Importance

This is the tranche that turns the newly landed AOI planner seam from:

- an implemented architectural cutover

into:

- an empirically supported exemplar loop

If this gate is skipped, the next program steps will risk generalizing from a seam that is technically stronger but still under-evaluated.

So the next honest step is:

- run the Stage 5 AOI exit gate over the seam that now exists

before moving the main line on to broader transient-substrate generalization.
