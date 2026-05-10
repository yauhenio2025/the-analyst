# Memo: Round 12 / AOI Transient Consumer Adoption Scope

Date: 2026-03-22
Program: Thin Consumer Platformization

## Purpose

Record the next bounded move after round 11.

This memo is meant to answer:

1. what the roadmap says should happen after renderer contracts, consumer consolidation, and bounded compose-from-intent are all real
2. what round 12 should prove immediately
3. what should remain blocked so the work does not dissolve into a full frontend rewrite or premature draft-persistence program

This memo sits on top of:

- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_completion.md`
- `communications/MEMO_2026-03-22_round10_consumer_consolidation_completion.md`
- `communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md`
- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`

## Current Program Position

As of round 11, the roadmap sequence that was explicit after round 8 now exists in code:

1. renderer contract enforcement
2. consumer consolidation
3. bounded compose-from-intent

That means the program is no longer blocked on:

- whether analyzer-v2 can produce contract-valid transient AOI pages from intent
- whether the shared generic renderer path can consume those renderer types at the component level

The remaining contradiction is now narrower and more concrete:

- analyzer-v2 can compose a transient page
- but the live consumer shell in the-critic is still job-backed

So the current question is no longer:

- can analyzer-v2 orchestrate a page from intent?

It is now:

- can one real consumer surface adopt the transient compose-from-intent contract honestly, without faking job semantics and without adding workflow-specific UI logic?

## Why Round 12 Is The Right Immediate Move

The roadmap after round 8 said the program should move from proof-branch expansion toward:

- renderer contracts
- consumer consolidation
- bounded compose-from-intent

Rounds 9 through 11 closed those platform seams in substance.

What round 11 did **not** prove was:

- production frontend adoption of the transient page contract
- that the-critic can render a non-job-backed transient page without pretending it is a `PagePresentation`

That is now the smallest honest next move.

It is also the most coherent next move with the larger vision:

- analyzer-v2 as the brain
- consumers as thin shells
- composition from intent becoming a real experience rather than only a backend proof

Until one real consumer surface uses the transient route, compose-from-intent remains infrastructure with no user-facing realization.

## Current Repo Truth

The current the-critic codebase makes one thing very clear:

- `ViewRenderer` is already generic enough to render transient returned views with zero runtime changes
- `V2TabContent` and `AnalysisWorkspacePage` are not transient-ready

Why not:

- `V2TabContent` assumes `presentation.job_id` in multiple places for polish, capture, section-polish, provenance, and renderer config plumbing
- `AnalysisWorkspacePage` is built around job launch, job polling, saved results, refresh, trace fetches, and export links
- the bounded-v2 workspace hooks and client surface are all job/result shaped

There is also an explicit live workstream in the-critic already:

- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`

That memo is about:

- AOI v2 hot-path cutover on the thinker page
- making the existing job-backed AOI v2 surface the default thematic experience

Round 12 should therefore be treated as:

- a parallel bounded transient proof host

not:

- a rewrite of the AOI hot path
- a hidden prerequisite for the current thinker-page cutover

So round 12 should **not** try to prove:

- “the current job-backed workspace was secretly transient-ready all along”

The code says otherwise.

## Bounded Round-12 Claim

Round 12 should prove one bounded thing:

- the-critic can render the round-11 transient compose-from-intent response on one real AOI-only consumer surface through a dedicated thin transient shell, without faking job semantics and without new workflow-specific renderer logic

The required proof surface should be:

- AOI only
- `consumer_key = the-critic`
- the existing round-11 transient route:
  - `POST /v1/presenter/compose-from-intent`

The consumer proof surface should be:

- one dedicated AOI transient shell in the-critic
- not a retrofit of the existing generic job-backed analysis workspace

Route placement is secondary.

The architectural boundary that matters is:

- separate transient shell + separate transient frontend contract

not:

- the exact URL shape used to host that shell

For the proof round, a dedicated route is still the recommended host choice because it keeps the boundary explicit, but the doctrine is shell isolation, not route proliferation.

## What Round 12 Should Realize

Round 12 should land one bounded consumer slice:

### 1. One Dedicated Transient AOI Proof Host

Use one isolated AOI transient proof host in the-critic, for example:

- `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker/compose-from-intent`

That host should be explicitly:

- AOI-only
- transient-only
- non-job-backed

The recommended implementation is a dedicated route, but the real requirement is:

- no inheritance from `AnalysisWorkspacePage`
- no reuse of `useBoundedV2Workspace`
- no reuse of the job/result run lifecycle

### 2. One Thin Transient Consumer Shell

Add one new thin shell component for transient returned pages.

It should:

- accept a separate frontend transient contract, not `PagePresentation`
- adapt each returned backend `TransientIntentView` into the minimal frontend rendering inputs needed by `ViewRenderer`
- render top-level views in order
- reuse the existing generic renderer path through `ViewRenderer` with zero `ViewRenderer` runtime changes
- surface returned trace data inline if needed
- keep loading / error / retry state local to the transient page

The key frontend contract decision for round 12 is:

- do **not** coerce the round-11 response into frontend `PagePresentation`
- do **not** widen `ViewPayload` to be transient-aware
- do **not** thread fake default values for `job_id`, `plan_id`, `phase_number`, `data_quality`, `raw_prose`, or other job-law fields through the existing workspace path

Instead, round 12 should add:

- one dedicated transient frontend contract
- one shell-local adapter from backend `TransientIntentView` to:
  - a shell-local transient view model
  - `ComposedView` + `data` inputs for `ViewRenderer`

It should **not** require:

- `job_id`
- `plan_id`
- result polling
- saved-result restore logic
- export links
- capture context
- provenance plumbing
- section polish
- page polish
- refresh
- single-view lazy loading by job id
- tab synthesis
- child-view orchestration

This is the main architectural choice of round 12:

- add a dedicated transient shell
- do not first generalize the job-backed shell to optionalize every job field

### 3. One Narrow Client Surface

Add one thin the-critic client call for the new presenter route.

That client should:

- submit the round-11 request shape
- return the transient response shape
- preserve the route’s `400 / 502 / 503 / 409` distinction

It should not be smuggled into the bounded-v2 job/result client layer as if it were another run lifecycle method.

It should also define its own typed transient error surface rather than flattening everything into generic `Error` objects.

### 4. One Bounded Input UX

The transient AOI page should include only a minimal bounded input surface:

- `user_intent`
- 1 to 4 prose sections
- optional `style_school`

For proof closure, the source of those prose sections must be explicit:

- ship 2 hardcoded example request payloads derived from the saved round-11 closure requests
  - `communications/PROOF_round11_dossier_request_2026-03-22.json`
  - `communications/PROOF_round11_comparison_request_2026-03-22.json`

Round 12 may include helper affordances such as:

- “load dossier example”
- “load comparison example”

Those are not optional nice-to-haves. They are the bounded proof input source.

What remains out of scope:

- building a job-result browser to pull prose from prior runs
- requiring a user to type multi-thousand-word AOI prose sections from scratch
- reading previous outputs through the job-backed workspace shell

Free-text editing after an example is loaded is acceptable, but full from-scratch authoring is not required for round-12 closure.

### 5. One Explicit Blocking-POST UX Boundary

Round 12 should assume the existing route remains:

- one blocking `POST`
- likely 30 to 90 seconds on real AOI inputs

So the UX contract should be explicit:

- simple loading state only
- no SSE / streaming
- no polling protocol
- no per-stage live progress
- no latency SLA required for closure beyond eventual successful return on the proof inputs

The proof does not require:

- sub-30-second response time
- background-job conversion
- progressive partial rendering

## What Round 12 Should Not Realize

Round 12 should stay explicitly out of:

- retrofitting `AnalysisWorkspacePage` to be dual-mode job-backed + transient
- making `V2TabContent` fully job-optional
- widening `PagePresentation`
- widening frontend `ViewPayload`
- capture/polish/export on transient pages
- provenance and capture integration
- job-based refresh/retry/result restore
- job-id-based single-view fetches
- saved-result persistence
- transient draft promotion
- genealogy transient adoption
- child-view / tab compose-from-intent
- widening beyond AOI

Those are real future questions, but they are not the next bounded move.

## Proof Standard

Round 12 should be treated as closed only if all of the following are true:

1. the new the-critic transient AOI page can submit the saved round-11 dossier request and render the returned transient page successfully
2. the same page can submit the saved round-11 comparison request and render the returned transient page successfully
3. both rendered pages use the existing generic renderer path without adding new workflow-specific renderer overrides
4. the transient page does not require synthetic `job_id` / `plan_id` placeholders
5. the error surface is honest:
   - `400` request issue
   - `502` upstream/orchestration issue
   - `503` dependency unavailable
   - `409` final contract invalid
6. the shell renders from a separate transient frontend contract rather than `PagePresentation`
7. `ViewRenderer` requires no runtime code changes

Saved proof evidence should include:

- page screenshots
- page text snapshots
- the exact request payloads used
- the returned transient response JSONs
- frontend regression proving the dedicated transient shell works without job semantics

Minimum status-to-UX mapping should be fixed in the scope:

- `400` -> inline user-correctable input error
- `502` / `503` -> system error with retry affordance
- `409` -> diagnostic error panel showing returned validation issues

## Why This Is Better Than The Obvious Alternatives

### Not Draft Persistence Yet

Promoting transient pages into saved drafts before one real consumer can even render them would be upside down.

That would widen data-model and lifecycle complexity before the basic adoption seam is proved.

### Not Workflow Widening Yet

AOI is still the only honest transient proof surface because:

- round 9 closed renderer-law there
- round 10 closed default consumer consolidation there
- round 11 closed transient orchestration there

Genealogy still carries more consumer and renderer-specific debt.

### Not Workspace Unification Yet

The existing job-backed workspace is valuable, but it is the wrong first place to absorb the transient contract.

Trying to unify those worlds in round 12 would blur the proof:

- job lifecycle
- saved results
- export / polish / capture
- transient orchestration

That is too many new variables at once.

### Not Hot-Path Cutover Interference

Round 12 should not silently take over the AOI v2 hot-path cutover work tracked in:

- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`

The transient proof host should stay:

- additive
- isolated
- non-blocking for the existing thinker-page AOI cutover

## Decision Rule

If round 12 succeeds, the program should then be in a much stronger position to decide between two genuinely new directions:

1. transient product adoption broadening
   - more workflows
   - better transient shell ergonomics
   - eventual workspace unification

2. transient-to-authored promotion
   - bounded draft persistence
   - user curation/editing of composed pages

But round 12 itself should only prove:

- one real consumer can adopt the transient contract honestly

## Final Round-12 Sentence

If the team needs one operational sentence for the next move, it should be:

- **Use round 12 to prove one real AOI-only consumer can render the round-11 transient compose-from-intent contract through a dedicated thin shell, without faking job semantics and without widening into persistence or workspace unification.**
