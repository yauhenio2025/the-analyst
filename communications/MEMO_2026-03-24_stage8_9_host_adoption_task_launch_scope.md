# Memo: Stage 8/9 / Host Adoption Of Analyzer-Owned Task Launch Scope

Subtitle: Put `route-task` And `plan-task` Into Real Current-Consumer Use Before Reopening Lifecycle Or Chasing A Fake Second-Consumer Proof

Date: 2026-03-24
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Recent Stage Memo: `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_completion.md`
Stage 13 Scope: `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_scope.md`
Stage 13 First-Slice Completion: `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_completion.md`
Stage 9 Completion: `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_completion.md`
Stage 8 Completion: `communications/MEMO_2026-03-23_stage8_task_intake_and_workflow_routing_completion.md`
Roadmap Vision: `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
Narrower Product Vision: `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

## Purpose

Define the next honest phase after the bounded second Stage 13 slice landed.

This memo argues that the next stage should be:

- a bounded host-adoption slice over Stage 8 and Stage 9
- not Stage 14 lifecycle
- not another mostly-downstream host-contract tightening pass
- not a fake “second consumer” proof

The concrete next missing seam is:

- analyzer-v2 already owns `POST /v1/orchestrator/route-task`
- analyzer-v2 already owns `POST /v1/orchestrator/plan-task`
- the current host still does not consume either seam anywhere in live code
- so the host still owns too much workflow/surface-launch intelligence locally, even after the Host Contract v1 runtime became real

## Why This Is The Next Honest Move

The last four days closed a disciplined downstream ladder:

1. Stage 10 normalized result-backed readiness across AOI and genealogy
2. Stage 11 made bounded transient semantic page trees real
3. Stage 12 made served renderer law explicit across current AOI and genealogy presentation seams
4. Stage 13 made the current host/runtime contract explicit and then operational across result-backed and transient proof seams

That work was not wasted.

It cleared the host boundary enough that the main remaining weakness is now upstream again:

- the host still decides too much about which analytical path to invoke
- analyzer-owned task routing and planning exist, but they are still unused by the actual consumer

The roadmap and recent memo trail both point here:

- Stage 8 completion explicitly left `route-task` host adoption open
- Stage 9 completion explicitly left `plan-task` host adoption open
- the canonical roadmap says the program should gradually shift from downstream AOI/the-critic work toward upstream planning/orchestration
- Stage 13 second-slice completion still leaves the proof current-consumer-only and AOI source-backed transient launch host-bounded

This should be read as a prioritization judgment after the Stage 13 second slice, not as a claim that the canonical roadmap had already precommitted this exact tranche name or proof shape.

So the next leverage point is not “more host proof theater.”

It is:

- let the current host consume analyzer-owned task-routing/planning truth for one bounded AOI seam and one bounded genealogy seam

## Why This Is Not Stage 14 Yet

Stage 14 is lifecycle:

- launch
- revisit
- save
- share
- compare

That is still premature.

The current program still lacks one stronger proof first:

- the host can ask analyzer-v2 what downstream family should own the next move
- the host can ask analyzer-v2 for the bounded planning outcome over that move
- the host can then execute that followup without page-local analytical decision-making

Until that exists, reopening lifecycle would blur:

- host-contract maturity
- analyzer-owned task intelligence
- transient vs durable runtime law
- AOI-specific proxy exceptions

So lifecycle should remain deferred.

## Why This Is Not Another Stage 13 Slice

Stage 13 has already done the bounded host-contract work that was honest to do inside the current consumer:

- Host Contract v1 is typed
- Host Contract v1 is runtime-authoritative for the bounded 11-family set
- result-backed and transient proof seams share one current host runtime
- the three current proof seams have executable host-surface lookup law

Another purely downstream Stage 13 slice would now risk low-value proof motion:

- more current-consumer-only runtime cleanup
- more documentation of host-owned law that analyzer should increasingly own
- another attempt to look “generic” without actually shifting analytical launch intelligence upstream

That is not the highest-leverage move anymore.

## Why This Is Not A Second-Consumer Push

A second consumer would be a valid Stage 13 exit proof eventually.

But it is not the smallest honest next move.

Right now, a second-consumer attempt would still sit on top of a world where:

- `route-task` is unused by the current host
- `plan-task` is unused by the current host
- the current host still chooses between result-backed, transient, and execution paths through page-local logic

That would risk proving duplication, not maturity.

The more honest order is:

1. make analyzer-owned task routing/planning real in the current host
2. then reconsider whether a second-consumer proof is the next best strengthening move

## Strategic Diagnosis

### What is already real

In analyzer-v2:

- `POST /v1/orchestrator/route-task` returns a bounded advisory routing decision with downstream launch contract metadata
- `POST /v1/orchestrator/plan-task` returns either:
  - a genealogy execution plan plus followup contract
  - an AOI composition handoff plan plus allowed/blocked profiles
  - or bounded `insufficient_context` / `unsupported` outcomes
- Stage 10 readiness is already public and cross-workflow
- Stage 11 transient compose is already real
- Stage 12 served renderer law is already real

In the-critic:

- Host Contract v1 is now typed and runtime-authoritative for the current bounded run/result/readiness/transient family set
- the current host has shared result-backed and transient adapter/runtime layers
- the current host already has analyzer-v2 execution helpers, including existing wrappers around:
  - `orchestrator/analyze`
  - `orchestrator/analyze-by-ref`
  - `executor/jobs`

So the substrate for host adoption is not greenfield.

### What is not yet real

The current host does not consume `route-task` or `plan-task` anywhere.

That means the host still locally owns decisions such as:

- whether this interaction is AOI transient vs genealogy job-backed
- whether a genealogy task should go through inline-documents or by-reference execution
- when to stop at AOI handoff metadata versus when to execute directly
- and some of that logic currently lives in backend launch code as well as in page code

The current host contract also intentionally excludes those analyzer advisory seams.

So the remaining gap is now clear:

- analyzer can already say what the next move should be
- but the host still does not ask

## The Real Next-Phase Problem

The real problem is not:

- “automatic dispatch from analyzer into every downstream route”
- “replace the current host with a generated app”
- “solve lifecycle”
- “make AOI fully host-neutral”

It is:

- “put analyzer-owned task-routing and bounded planning into real host use, so the current consumer stops deciding workflow/surface launch analytically in host-local code”

That is the next durable proof seam.

## Recommended Shape

### Decision 1: frame this as a bounded Stage 8/9 host-adoption slice

This should be framed as:

- a Stage 8/9 host-adoption tranche
- possibly also the first real motion toward Stage 3 AOI task-driven composition
- but not a Stage 14 lifecycle tranche

Expected outcome:

- Stage 8 advances because `route-task` is no longer analyzer-only theory
- Stage 9 advances because `plan-task` is no longer analyzer-only theory
- Stage 13 may become strategically stronger, but this is not a Host Contract v2 memo

### Decision 2: keep Host Contract v1 stable and layer a bounded task-launch contract on top

Do not overload Host Contract v1 with a bunch of new meanings.

Host Contract v1 should stay focused on:

- run/result/readiness/transient delivery families
- identity, ownership, consumer-key, proxy, and scope law

The next phase should instead add one bounded task-launch layer over:

- `route-task`
- `plan-task`

That layer should define:

- request shapes the current host is allowed to send
- how prior routing decisions are threaded into planning
- which planning-context variants the current host may satisfy
- how downstream followup contracts map onto already-existing host/runtime families

This should not become a third disconnected client stack beside:

- `boundedV2Client.ts`
- `composeFromIntentClient.ts`

The honest bounded shape is:

- one shared task-launch runtime layer for `route-task` and `plan-task`
- that layer chains into the existing Host Contract v1 runtime and existing launch helpers for downstream execution or compose
- existing result-backed and transient client modules remain thin wrappers where that is the lowest-churn path

So this can live as a separate typed module in the-critic, but not as an uncontrolled extension of page code and not as a disconnected parallel client family.

### Decision 3: use both `route-task` and `plan-task`, not only one

The host should not skip straight to `plan-task` and leave `route-task` as dead documentary weight.

This is a bounded proof choice, not a claim that analyzer-v2 requires both calls for correctness.

`plan-task` can already recompute routing when prior routing is absent or mismatched.

The bounded honest flow is:

1. host sends task + source constraints to `route-task`
2. host receives analyzer-owned routing rationale and downstream family selection
3. host sends task request + prior routing decision + bounded planning context to `plan-task`
4. host receives analyzer-owned planning outcome
5. host follows the returned downstream contract through existing launch families

That preserves:

- route visibility
- planning visibility
- debugging seams
- bounded analyzer-owned rationale

### Decision 4: prove one AOI task-driven handoff seam

The AOI proof should stay bounded and honest.

This is the thinner of the two proof seams.

Because the host is already on an AOI-specific surface by URL routing, `route-task` does not remove much analytical intelligence there by itself.
So the AOI value in this slice should be framed as:

- contractual consolidation
- analyzer-owned handoff metadata
- analyzer-owned required host preparation
- one bounded proof that the host follows planner truth rather than calling separate readiness/launch helpers ad hoc

Use one selected saved-result source context:

- a real `source_v2_job_id` or resolvable saved-result identity
- one task prompt from the user

The analyzer should then own:

- routing that this is an AOI source-backed transient path
- bounded handoff planning over the live Stage 7 source bridge
- allowed vs blocked profile truth
- required host preparation
- source-family / producer-engine handoff metadata beyond the thinner Stage 10 readiness shape

The host should then:

- stop calling separate readiness-style checks and source-bridge assumptions ad hoc for this proof seam
- display analyzer-returned allowed profiles
- keep user choice among those allowed profiles if more than one is feasible
- launch through the existing `compose-from-source` path only after analyzer planning says the handoff is ready

This is intentionally not:

- planner-driven AOI profile auto-selection
- host-neutral AOI launch
- lifecycle unification

### Decision 5: prove one genealogy task-driven execution seam

The genealogy proof should also stay bounded and current-consumer-grounded.

Use one bounded current host entry path with either:

- registered corpus context
- or inline documents context

The analyzer should then own:

- routing whether the task is genealogy-job-backed
- bounded planning context evaluation
- `WorkflowExecutionPlan` generation
- downstream followup contract truth

The host should then:

- stop choosing between `analyze` and `analyze-by-ref` analytically in host-local code, including backend launch logic
- execute the followup over the returned plan/executor contract using existing host/analyzer execution helpers
- preserve current polling/result restore behavior after the job starts

This is the stronger proof seam in this tranche because it removes real host-owned workflow/document launch decisions.

### Decision 6: keep dispatch explicit and lifecycle regimes separate

This next slice must not smuggle automatic dispatch into analyzer-v2.

Keep the boundary explicit:

- analyzer returns advisory routing and bounded planning decisions
- the host still executes the followup call
- transient and durable job-backed flows remain distinct lifecycle regimes

But be precise about genealogy:

- `route-task` is advisory and read-only
- `plan-task` is advisory with respect to dispatch, but it is not read-only for genealogy
- genealogy `plan-task` can perform hydration/materialization work and generate persisted plans

So the host should treat genealogy `plan-task` as a commit-like launch-preparation step, not as a speculative probe.
That means this slice should avoid:

- repeated best-effort retries without deduplication semantics
- calling genealogy `plan-task` merely to preview possibilities
- UI flows that invoke genealogy planning before the user has actually committed to launch

Do not introduce:

- one union “do everything” analyzer route
- automatic analyzer dispatch from `plan-task`
- fake unification of AOI transient and genealogy execution lifecycle

### Decision 7: land this through shared host runtime, not page-local fetches

The current host now has real shared runtime substrate.

So the next slice should not add:

- raw page-local fetches to `/v1/orchestrator/route-task`
- raw page-local fetches to `/v1/orchestrator/plan-task`

Instead it should add:

- one shared task-launch client/runtime layer
- one bounded typed surface mapping for the proof seams that use it

This keeps the proof honest:

- analyzer owns task-routing/planning truth
- shared host runtime owns transport and bounded dispatch law
- pages own only local UX state and display
- backend host launch code should also consume that shared task-launch/runtime layer where the current genealogy launch path lives

## Bounded Deliverables

The next phase should land at least:

1. one shared typed task-launch client/runtime in the-critic over `route-task` and `plan-task`
2. one bounded task-launch contract artifact describing the host-consumed advisory seams
3. one AOI task-driven handoff proof using analyzer-owned routing + planning as a contractual consolidation seam before `compose-from-source`
4. one genealogy task-driven execution proof using analyzer-owned routing + planning before executor launch
5. one honest unsupported or insufficient-context UI path surfaced from analyzer-owned task decisions

## Proof Bar

The proof bar should require:

1. one AOI task where the host uses analyzer-owned routing + planning as the bounded launch contract for source-backed transient compose rather than stitching together separate readiness and launch assumptions ad hoc
2. one AOI task where analyzer-owned planning returns allowed/blocked profiles, required host preparation, and source-bridge metadata beyond the thinner Stage 10 readiness answer, and the host follows that result
3. one genealogy task where the host no longer decides locally whether the next move is by-reference or inline execution
4. one genealogy task where analyzer-owned planning returns a real `WorkflowExecutionPlan` and downstream followup contract that the host actually executes
5. one unsupported or insufficient-context task where the host surfaces analyzer-owned failure honestly rather than coercing a launch path

## What This Phase Must Not Do

This phase should not:

- reopen lifecycle/session law
- claim Stage 13 is now closed
- require a second consumer
- widen Host Contract v1 into a vague catch-all registry
- make AOI source-backed launch host-neutral
- claim planner-driven AOI profile auto-selection
- replace every current launch path in the-critic at once
- flatten transient and job-backed lifecycle into one route or object model

## Strategic Judgment

There is clearly enough real work for a next phase.

The vision has not been achieved yet.

The strongest current missing seam is no longer:

- renderer law
- thin-host contract formalization
- transient host rendering

It is:

- analyzer-owned task-launch intelligence being absent from the live consumer

So the next honest move is:

- a bounded Stage 8/9 host-adoption slice over `route-task` and `plan-task`

while keeping:

- Stage 14 lifecycle deferred
- second-consumer proof deferred
- and the current-host proof discipline intact
