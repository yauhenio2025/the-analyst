# Memo: Stage 3/4/5 / AOI Exemplar Completion Scope

Date: 2026-03-24
Status: Draft scope memo
Program: Dynamic Bespoke Apps Platformization
Prior completions:
- `communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_completion.md`
- `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md`
Roadmap sources:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

## Summary

Stage 13 Tier A is now closed for the bounded result-backed second-consumer proof.

The next honest structural phase is the AOI exemplar tranche:

- canonical Stage 3 / AOI task-driven composition
- canonical Stage 4 / AOI source/engine-selection law
- canonical Stage 5 / AOI evaluation and operational guardrails

This tranche also needs to state what happens to canonical Stage 2, which is still marked `In progress` in the canonical ledger.

The intended reading of this memo is:

- Stage 2 is treated as subsumed by the current source-backed transient substrate and will be documentary-closed as a side-effect of this tranche's evaluation/ops pack
- this memo does not silently skip Stage 2 as competing parallel work

These should be scoped together as one bounded tranche.

The reason is simple:

- Stage 3 without Stage 4 becomes fake task-first UX over fixed profile bundles
- Stage 4 without Stage 5 becomes unstable planning without a real quality gate
- Stage 5 without Stages 3/4 becomes evaluation over the wrong seam

So the next step should not be another Stage 13 host-contract slice.
It should not be lifecycle.
It should not be transient-substrate generalization.

It should be:

- finish AOI as the first real task-first exemplar loop on top of analyzer-v2

while keeping the tranche bounded to one AOI proof path inside `the-critic`.

## Why This Is The Next Honest Step

The program has already proved several important prerequisites:

- planner-backed AOI handoff exists in one live host seam
- analyzer-owned `route-task` and `plan-task` are real and adopted
- source-backed transient compose is real
- Host Contract v1/runtime and the task-launch layer are now credible
- `aoi-canary` closes the cheap result-backed second-consumer proof

But AOI is still not task-first end to end.

The live code still shows the remaining gap clearly:

- `AoiV2ThematicPanel.tsx` has a planner-backed handoff path, but it still presents legacy `dossier` / `comparison` launch controls beside it
- the analyzer-native AOI handoff is already richer than pure allow/block lists, but the effective host-consumed seam is still dominated by `allowed_profiles` / `blocked_profiles`, so the proof path is still organized around two fixed labels
- `AoiComposeFromIntentPage.tsx` still centers `composeFromSource(profile)` over `dossier` / `comparison`, even though planner-backed launch now constrains those choices
- developer fallback fixtures and generic source-backed compose still coexist with the planner-backed seam
- there is no saved AOI evaluation pack, decision rubric, or operational threshold set that would justify treating AOI as a stable platform reference
- host-proxy identity translation and snapshot warmup still sit on the proof path as real host-owned continuity steps

That means the current AOI state is best described as:

- strong bounded proof
- not yet the first finished exemplar app loop

This tranche is the work that closes that gap.

## Bounded Claim

The bounded claim for this tranche is:

- AOI becomes the first real task-first exemplar loop on top of analyzer-v2, with bounded analyzer-owned source/product-selection law and explicit evaluation/ops guardrails, while the host remains mostly shell/continuity rather than analytical decision-maker

This tranche does **not** claim:

- full cross-workflow orchestration
- host-neutral transient composition
- second-consumer transient proof
- lifecycle resolution
- arbitrary engine-graph search
- generic "build any app" closure

It is an exemplar tranche, not the final platform claim.

## Scope Decisions

### Decision 1: Treat canonical Stages 3/4/5 as one bounded AOI tranche

This memo intentionally scopes one tranche across three canonical stages.

That is not because the stage distinctions are unimportant.
It is because they are operationally coupled in the current codebase:

- task-first AOI needs bounded selection law
- bounded selection law needs an evaluation gate
- the evaluation gate needs a single real AOI proof path to measure

The tranche should therefore be reviewed as:

- one AOI exemplar-completion slice

not as three disconnected documents.

### Decision 1A: Stage 2 is subsumed, not ignored

Canonical Stage 2 remains open in the ledger, but this tranche should treat it as a prerequisite being closed as part of AOI exemplar completion rather than as a separate competing phase.

Concretely:

- the source-backed transient MVP substrate from the earlier rounds is good enough to proceed
- the remaining Stage 2 closure work should be absorbed into this tranche's evaluation/ops deliverable
- the eventual closeout for this tranche should say explicitly whether Stage 2 is now documentary-closed as a side-effect

### Decision 2: Keep the proof path narrow

The proof surface should stay inside the current AOI live consumer path in `the-critic`:

- `AoiV2ThematicPanel.tsx`
- `AoiComposeFromIntentPage.tsx`

The tranche should land one planner-primary AOI path there.

It should not widen into:

- a full AOI UI rewrite
- a new second consumer
- cross-workflow composition generalization
- lifecycle persistence semantics

### Decision 3: Planner-primary does not mean full AOI cutover on day one

The tranche should make one AOI proof path planner-primary and task-first.

It does **not** need to delete every legacy control immediately.

The honest bounded move is:

- one clearly marked proof path becomes analyzer-driven and task-first
- legacy controls may remain outside that proof slice during the tranche if they are clearly non-authoritative

What must change is the proof path's authority, not necessarily every button in the product on the first pass.

For this tranche, planner-primary should default to:

- analyzer planning recommends or selects the bounded composition path
- the user may confirm that planner-backed path once
- the host should not then ask the user to make the main analytical choice again through legacy profile-first controls

This memo does not require blind auto-execution with no user confirmation.

### Decision 4: Stage 4 should be interpreted as bounded AOI source/product-selection law

Canonical Stage 4 says "engine/source-selection law."

For this tranche, the minimum honest interpretation is narrower than open-ended engine planning:

- selection among bounded AOI analytical product families and composition inputs

This likely includes choices among already available AOI result/product families such as:

- thematic synthesis
- thematic report
- engagement mapping
- sin findings
- other AOI product bundles already present in the saved-result substrate

This tranche should **not** claim:

- general engine-graph search
- arbitrary workflow composition

If the tranche needs analyzer contract changes, they should be in service of this bounded AOI composition-facing selection law.

### Decision 5: The current host-consumed handoff is not enough

The current planner-backed AOI seam is important, but the effective host-consumed seam is still too thin to close Stage 3/4 honestly.

Why:

- the analyzer-native handoff already contains richer fields such as expected/available source families and expected producer engines
- but the current TypeScript/runtime/UI path mainly consumes `allowed_profiles`, `blocked_profiles`, and notes
- the public `compose-from-source` contract still hard-locks the host to a `profile` label
- so the compose page still does not act like a continuation of analyzer-chosen source/product-selection truth

So this tranche should assume two likely work items:

- consumer-side widening, so the host actually consumes the richer AOI planning metadata already produced upstream
- public compose-contract widening, if the tranche wants a proof case that is genuinely not reducible to the current `dossier` / `comparison` enum

The memo does **not** freeze the exact shape yet.
But it should require at minimum:

- a richer effective AOI planning/handoff path than profile allow/block lists alone

### Decision 5A: A truly non-profile AOI proof case requires public contract widening

The current public source-backed compose contract still accepts only:

- `profile = dossier | comparison`

So if this tranche wants an exit case that is honestly "not reducible to dossier/comparison," it must assume one of these is in scope:

- widen the public `compose-from-source` contract beyond the two-profile enum
- or add a new planner-resolved downstream compose contract that does not reintroduce profile choice at the host boundary

This is an implementation reality, not an optional footnote.

### Decision 6: Stage 5 guardrails are part of the tranche, not a cleanup afterward

This tranche should not stop at "planner seems smarter now."

It must also land a bounded AOI evaluation and operational gate, including:

- repeatable proof tasks
- a saved rubric
- launch-quality checks
- blocked/ambiguous outcome visibility
- latency/cost or at least responsiveness observations
- a small failure taxonomy

This is the evidence line that makes later transient generalization honest.

One distinction should stay explicit:

- AOI already has a real operational readiness gate for source-backed feasibility
- what is still missing is the Stage 5 evaluation pack: rubric, thresholds, responsiveness notes, and failure taxonomy

### Decision 6A: Host continuity residuals are allowed but must be named

For this bounded tranche, the following host-owned continuity steps may remain on the proof path unless explicitly removed:

- host-proxy identity translation before source-backed compose launch
- snapshot warmup before navigation/compose continuity

If they remain, the closeout must say so plainly.
They should be treated as bounded continuity responsibilities, not hidden analytical law.

### Decision 7: Later tranches stay deferred

This tranche should explicitly leave these later lines untouched:

- Stage 13 Tier B transient-inclusive second-consumer proof
- de-AOI / de-`the-critic` transient-substrate generalization
- Stage 6 lifecycle decision
- broader governance/review infrastructure

The AOI exemplar must become stronger first.

## Current Residuals This Tranche Must Remove

The current live AOI path still contains these structural residuals:

1. Planner-backed handoff exists beside legacy profile-first launch.
2. The host still visibly asks the user to think in `dossier` / `comparison` labels.
3. The compose page still exposes source-backed profile buttons as the main action surface.
4. The host currently throws away much of the richer AOI planning metadata and collapses back to profile controls.
5. The public source-backed compose contract is still locked to `dossier | comparison`.
6. There is no saved AOI exemplar eval pack that would justify later platform claims.

The tranche does not need to remove every AOI-specific artifact in the codebase.
It does need to remove those five residuals from the proof path.

## Proposed Deliverables

### 1. One planner-primary AOI proof path

Land one AOI flow where:

- the user starts from a task, not a fixed profile label
- analyzer planning decides the bounded AOI composition path
- the host no longer makes the main analytical choice on that proof path
- the proof path reaches a rendered transient AOI result

For exit honesty, this path should not be reducible to:

- "the host still chose dossier or comparison, just after one extra planner call"

Concrete examples of the kind of task-first proof this tranche should target:

- "Show how Thinker X's concept of Y evolves across the corpus" should let analyzer planning select the relevant AOI source/product mix and present that rationale without asking the user to choose the `dossier` label first
- "Show where Thinker X most directly engages, contests, or reframes peer positions on Y" should let analyzer planning foreground the engagement- and findings-oriented AOI materials without asking the user to choose the `comparison` label first

If the resulting downstream shape is still literally one of the two current public profiles, the closeout should say so plainly.
If the tranche wants a proof case beyond those two shapes, public contract widening is required.

### 2. One bounded AOI source/product-selection contract

Land one analyzer-owned contract that makes these things visible:

- selected AOI inputs or product families
- rejected alternatives
- bounded rationale
- insufficient/ambiguous cases when the task cannot be resolved cleanly

This is the minimum honest Stage 4 slice.

The preferred order is:

1. consume the richer AOI handoff metadata already produced upstream
2. only widen analyzer-side public contracts where that richer planning truth still cannot be expressed honestly at the host boundary

### 3. Compose-page continuity from planner truth

`AoiComposeFromIntentPage.tsx` should become a continuation of analyzer planning truth for the proof path, not a separate profile-first chooser.

That means, for the proof path:

- planner-selected law is visible on the compose page
- planner-blocked alternatives stay blocked
- host-side overrides, if any, are clearly bounded and non-authoritative
- developer fixtures remain outside the proof slice

### 4. AOI exemplar evaluation and ops pack

Land a small but explicit AOI exemplar evaluation pack containing:

- a fixed set of AOI task cases
- at least one ready success case
- at least one blocked or ambiguous case
- at least one case that is not honestly reducible to the old `dossier` / `comparison` split

Also land:

- a scoring/rubric memo
- basic latency/cost or responsiveness notes
- a failure taxonomy for the proof path
- decision thresholds strong enough to say whether AOI exemplar completion is credible or needs revision

This deliverable is also where the remaining canonical Stage 2 closure should be absorbed:

- document AOI transient MVP criteria as they now exist after the source-backed/planner-backed work
- show repeated bounded AOI transient use on real inputs

### 5. Saved proof artifacts

Save evidence that later reviewers can inspect, including:

- task input
- routing/planning outputs
- selected/rejected AOI inputs
- rendered proof-path result
- blocked/ambiguous outcome
- evaluation outcome

## Likely Implementation Seams

This memo is not an implementation plan, but the likely seam set is already visible.

Analyzer-side seams likely include:

- task routing/planning schemas and contracts
- AOI planning logic for richer source/product selection
- source-backed compose or planner-to-compose bridge logic
- evaluation/reporting artifacts
- `src/presenter/schemas.py`
- `src/presenter/composition_source_bridge.py`
- `src/orchestrator/task_planning_schemas.py`
- `src/orchestrator/task_planner.py`

Current-consumer seams likely include:

- `the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `the-critic/webapp/src/lib/composeFromIntentClient.ts`
- `the-critic/webapp/src/lib/hostContractV1.ts`
- `the-critic/api/server.py`
- `the-critic/webapp/src/lib/boundedV2Client.ts`
- possibly thin client/types updates around transient compose if the AOI handoff contract changes

This should still be primarily a `the-critic` plus analyzer-v2 tranche, not a canary tranche.

## Non-Goals

Do not widen this tranche into:

- generic cross-workflow task-driven composition
- second-consumer transient adoption
- lifecycle or persistence semantics
- de-AOI / de-`the-critic` transient generalization
- arbitrary engine-graph orchestration
- "remove all legacy AOI code everywhere"

Those remain later lines of work.

## Exit Evidence

This tranche should count as closed only if it produces:

1. one AOI task-first proof flow where the host does not remain the real profile chooser
2. one saved analyzer planning artifact with selected/rejected AOI source/product rationale
3. one blocked or ambiguous AOI case surfaced honestly in the product flow
4. one saved AOI exemplar evaluation/ops memo with thresholds and failure taxonomy
5. one explicit closeout note saying:
   - whether Stage 2 is now considered documentary-closed as a side-effect
   - which host-owned residuals still remain on the proof path
   - whether the proof path still used the current `dossier | comparison` public contract or widened it
   - what remains open afterward

The exit bar should also remain honest about what it does **not** prove:

- it does not close Stage 13 Tier B
- it does not prove host-neutral transient composition
- it does not resolve lifecycle
- it does not prove generic multi-app platform closure

## Strategic Importance

This tranche is the bridge between:

- bounded proof surfaces

and:

- a real reference app loop that later platform work can generalize from

If AOI exemplar completion does not happen now, the next platform tranches will risk building on:

- a planner seam that is still too profile-first
- a composition seam that is still too AOI-special-cased
- and no real evaluation gate

That would make later generalization easier to claim and harder to trust.

So the next honest structural move is:

- finish AOI as the first task-first exemplar loop

before resuming broader transient-substrate generalization or lifecycle work.
