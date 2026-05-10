# Memo: Round 11 / Bounded Compose-From-Intent Scope

Date: 2026-03-22
Program: Thin Consumer Platformization

## Purpose

Define the next serious round after:

- round 9 renderer-contract enforcement
- round 10 consumer consolidation

This memo is meant to answer:

1. what the roadmap says should come next after contracts and consolidation
2. whether that next move is actually coherent with the current codebase
3. what a bounded round-11 compose-from-intent pilot should prove
4. what must remain explicitly blocked so round 11 does not dissolve into a broad orchestration or app-generation program

This memo sits on top of:

- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_completion.md`
- `communications/MEMO_2026-03-22_round10_consumer_consolidation_completion.md`

## Current Program Position

Rounds 9 and 10 materially changed the platform boundary.

Round 9 proved:

- final served renderer contracts can be enforced at the presenter boundary
- the bounded-composition error envelope is sufficient for fail-closed renderer law
- the AOI proof slice survives strict serve-time enforcement

Round 10 proved:

- the-critic no longer owns the generic bounded-v2 renderer init / registry / dispatch seam for the AOI path
- shared package-backed default renderer resolution is now real in live consumer code
- remaining local ownership is explicit override debt rather than hidden generic infrastructure

That means the platform now has:

- backend serve-time presentation law
- package-backed generic renderer consumption
- a thin generic workspace that is more honest than it was before

What it still does **not** have is the orchestration seam the roadmap has been pointing at:

- there is still no bounded `compose-from-intent` presenter entrypoint

## What The Roadmap Actually Implies Now

The roadmap memo said the post-round-8 path should be:

1. renderer contract validation
2. consumer consolidation
3. bounded compose-from-intent

Rounds 9 and 10 closed the first two in bounded form.

So the coherent next move is no longer:

- another proof token
- another narrow consumer cleanup
- another genealogy-only debt tranche

It is:

- a bounded orchestration seam that cashes in the previous rounds without reopening broad dynamic-app claims

## Why Round 11 Should Be Compose-From-Intent, Not Another Cleanup Round

There is still real debt around sub-renderer law and genealogy.

That debt is real, but it is no longer the highest-leverage next move for the platform as a whole.

Why:

1. round 9 already proved the presenter can enforce final served contracts on a real route
2. round 10 already proved the consumer can consume shared renderer infrastructure on the generic AOI path
3. the next missing program capability is not “one more law seam” but “one bounded orchestration entrypoint”
4. staying too long in cleanup rounds risks local optimization instead of moving toward the larger analyzer-v2 vision

That said, round 11 should only reopen compose-from-intent in a form that is honest about the current repo:

- existing presenter assembly is still job-bound
- existing `PagePresentation` is still job-bound
- existing view generation is single-view and pattern-based
- existing view-pattern coverage is still narrow
- genealogy and current sub-renderer-law questions are still unresolved

So round 11 must be:

- bounded
- AOI-first
- stateless
- ephemeral
- generic-pattern only

## What Already Exists In The Codebase

The main reason round 11 is plausible now is that the primitives are already present.

### Already Real

- `POST /v1/transformations/execute`
  - stateless transformation over raw `data`
- `POST /v1/views/generate`
  - single-view generation from a pattern
  - `save=false` by default, so generation can stay ephemeral
- `POST /v1/renderers/recommend`
  - LLM-powered renderer recommendation
- `GET /v1/views/patterns/*`
  - a small reusable pattern catalog
- `src/presenter/manifest_builder.py::build_effective_manifest()`
  - final served manifest adaptation and renderer-contract enforcement
- round-10 package consumption
  - the-critic can now render the generic AOI path without consumer-owned generic init logic

### Not Yet Real

- there is no `POST /v1/presenter/compose-from-intent`
- current `POST /v1/presenter/compose` is job-bound and means “refine + prepare + assemble for an existing job”
- current `PagePresentation` and `EffectivePresentationManifest` are explicitly job-bound contracts
- there is no transient page-assembly contract for ephemeral composed pages
- current view-pattern coverage is only six generic patterns:
  - `accordion_sections`
  - `card_grid_grouped`
  - `card_grid_simple`
  - `prose_narrative`
  - `tab_with_children`
  - `timeline_sequential`

This means round 11 is not “flip on an endpoint that already exists.”

It is:

- one new page-structure planning step
- plus one bounded transient assembly seam

## The Primary New Component: Page-Structure Planning

This is the most important addition the round needs to admit upfront.

The existing primitives are all single-view or low-level:

- `views/generate` produces one view from one pattern
- `transformations/execute` transforms one payload at a time
- `renderers/recommend` recommends one renderer for one view context

Compose-from-intent needs one higher-level planning step that does **not** exist yet:

- given `N` prose sections with engine provenance and a bounded user intent
- decide how many views to create
- choose which pattern each view should use
- decide whether the page should stay flat or use a bounded parent/child grouping
- decide which prose section feeds which generated view

That planning step is the primary new engineering in round 11.

It is not enough to describe round 11 as “glue” unless the memo explicitly names this page-plan stage.

The right framing is:

- existing primitives remain the building blocks
- one new page-structure planner coordinates them

## The First Missing Seam: A Transient Page-Assembly Helper

The first implementation object is not just a new endpoint and not just a new response schema.

It is a new transient assembly helper that can:

- take ephemeral generated views
- take transformed structured payloads
- build a render-ready view tree
- apply consumer adaptation
- run explicit transient renderer-contract validation
- compute transient manifest identity without pretending there is a real `job_id` or `plan_id`

The current presenter assembly path is too job-backed to reuse directly as-is.

So round 11 should be understood as:

- one new page-structure planner
- one new transient page-assembly helper
- plus orchestration over existing generation / transformation / validation primitives

## Round 11 Should Realize One Bounded Thing

Round 11 should prove:

- analyzer-v2 can accept a small intent + prose envelope and return a valid transient composed page through a new presenter entrypoint, using a new bounded page-plan step, existing renderer recommendation, pattern generation, transformation execution, and explicit transient renderer-contract validation without requiring an execution job or consumer-specific UI logic

That is the right next move because it is:

- larger than another proof token
- smaller than “apps on the fly”
- directly aligned with the roadmap

## Proposed Round-11 Surface

### New Endpoint

- `POST /v1/presenter/compose-from-intent`

### Required Pilot Characteristics

- stateless
- ephemeral
- AOI-only proof slice
- no persistence of generated views by default
- no execution-job creation
- no background preparation pipeline
- no consumer-specific logic in the-critic

### Required Input Discipline

The pilot request should stay narrow.

It should accept:

- `consumer_key`
- `user_intent`
- `prose_sections`
- optional `style_school`
- optional `audience`

Each `prose_section` should remain bounded to:

- `engine_key`
- `title`
- `prose`

Round 11 should **not** try to infer engines from raw user prose.

Engine execution and engine selection are not the pilot.

The pilot begins from:

- already-produced prose sections with known engine provenance

## Contract Choice: Do Not Pretend This Is A Job Page

This is the most important scoping decision.

Round 11 should **not** return the existing job-bound `PagePresentation` by stuffing fake values into:

- `job_id`
- `plan_id`
- `prepared_at`
- execution metadata fields

That would create a dishonest contract and blur the meaning of the current presenter APIs.

Instead, round 11 should introduce a **transient sibling contract** for the new endpoint.

The exact type name can be chosen in planning, but the shape should be:

- presenter-facing and render-ready
- view-tree based
- consumer-adapted
- renderer-contract validated
- explicitly non-persistent
- explicitly non-job-backed

It should also surface:

- generated ephemeral view definitions or their normalized equivalents
- a bounded orchestration trace explaining renderer/pattern choices

### View-Level Shape Choice

The transient contract also needs an explicit view-level shape decision.

The current `ViewPayload` is the closest existing unit, but it carries job-oriented fields such as:

- `phase_number`
- `engine_key`
- `chain_key`
- `raw_prose`

Round 11 should therefore prefer this discipline:

- internal assembly may reuse `ViewPayload` where pragmatic
- the external transient response should serialize to a **narrower non-job-backed view shape**
- the transient response should not expose fake or meaningless job fields just because the internal helper reused an existing model

That keeps the implementation practical without corrupting the public contract.

The point is:

- round 11 should prove orchestration over existing primitives
- not fake job semantics where no job exists

## Bounded Pattern And Renderer Scope

Round 11 should stay inside the generic pattern space that is already credible on the AOI path.

Allowed top-level renderer families for the pilot should be limited to:

- `prose`
- `accordion`
- `card_grid`

Round 11 v1 should **not** rely on top-level `tab` rendering.

Reason:

- the backend consumer contract supports `tab`
- but the current shared package default top-level renderer resolver does not expose a generic `tab` renderer
- and the live generic frontend path should not gain round-11-only special handling just to make the pilot work

If multiple views are generated, the transient page contract can still return multiple top-level views without treating `tab` as an in-scope generic renderer family.

Round 11 should not depend on:

- genealogy view-key overrides
- genealogy-only top-level renderers
- consumer-local custom views
- unresolved genealogy sub-renderer-law questions

The pattern allowlist should remain bounded to the existing generic pattern catalog, likely:

- `prose_narrative`
- `accordion_sections`
- `card_grid_simple`
- `card_grid_grouped`

`timeline_sequential` should be included only if the proof slice actually requires it.
It should not be included by default just because it exists.

`tab_with_children` should remain out of round-11 v1 unless the execution plan deliberately expands the shared generic top-level renderer path to make `tab` honest on the live consumer route.

## Renderer-Contract Enforcement On The Transient Path

Round 11 must not assume that round-9 strict enforcement automatically applies to the new endpoint.

What already exists is:

- a real renderer-contract enforcement seam
- but one that is currently activated on an AOI proof-mode allowlist in the existing job-backed path

So round 11 needs an explicit enforcement decision:

- either widen the existing enforcement seam to cover the new transient endpoint
- or call the underlying renderer validation helpers directly from the transient assembly path

What round 11 must **not** do is assume that merely calling existing presenter code will automatically make the transient route fail closed.

The transient endpoint must also own its failure mapping explicitly.

Low-level primitives such as `transformations/execute` are useful building blocks, but they do not by themselves define the presenter error contract for a new orchestration route.

So round 11 must include:

- presenter-owned normalization of transformation / generation / validation failures
- one explicit transient error shape for invalid composed output
- one explicit transient trace or diagnostics surface for bounded orchestration inspection

## Why AOI Is The Right Proof Slice

AOI is the right round-11 slice for the same reason it was the right slice in rounds 9 and 10:

1. renderer contract enforcement is already proved there
2. consumer consolidation is already proved there
3. the generic bounded-v2 workspace is already real there
4. genealogy still carries unresolved top-level vs sub-renderer-law questions

So round 11 should be:

- AOI-first and AOI-required

not:

- cross-workflow from day one

## What Round 11 Must Explicitly Stay Out Of Scope

To stay implementation-safe, the following must remain blocked:

- genealogy compose-from-intent
- engine selection from freeform user questions
- job creation and execution orchestration
- persistence of generated views by default
- background prep / cache lifecycle work
- auto-polish as part of the first pilot
- style-token unification
- full dynamic hierarchy invention beyond a bounded pattern allowlist
- broad “ephemeral apps” claims

Round 11 is not:

- dynamic app generation

It is:

- one bounded orchestration entrypoint over existing primitives

## Proposed Proof Standard

Round 11 should be judged against a standard that fits a live orchestration seam rather than a deterministic proof-token branch.

### Required Automated Proof

Automated tests should prove:

1. the endpoint orchestrates the existing primitives instead of bypassing them
2. the returned transient page contract is consumer-adapted and renderer-contract valid
3. AOI generic rendering still requires no new the-critic-specific logic
4. generated views remain ephemeral unless an explicit persistence flag is later introduced in a different tranche
5. invalid generated contracts fail through an explicit presenter error shape rather than silently degrading

### Required Documentary Proof

Closure should include at least two AOI control requests:

- one dossier-like / narrative-heavy input
- one comparison-like / structured multi-section input

The documentary proof should show:

- the returned page renders through the generic bounded-v2 path
- zero renderer-contract failures on the final served payload
- a saved orchestration trace that explains the generated pattern / renderer choices

### Proof Input Sourcing

For reproducibility, the documentary proof should reuse real AOI prose sections from the existing control jobs rather than inventing fresh ad hoc prose.

The natural source is the documented AOI control pair reused in rounds 9 and 10:

- `proof-round5-adaptive-aoi-dossier-final-1774100000`
- `proof-round5-adaptive-aoi-comparison-final-1774100000`

Round 11 should extract the relevant AOI prose sections from those saved job outputs and use them as the bounded input corpus for:

- one dossier-like / narrative-heavy request
- one comparison-like / structured multi-section request

Round 11 does **not** need to prove:

- byte-identical output across repeated live runs

LLM-driven orchestration means the stronger equivalence claim belongs in deterministic automated tests with stubbed model edges, not in live documentary output.

## What Round 11 Would Change In Program Terms

If round 11 lands, the program will have crossed an important boundary:

- from proving that analyzer-v2 can select and serve authored surfaces
- to proving that analyzer-v2 can compose a bounded transient page from intent-shaped input without relying on a bespoke app

That is materially closer to the larger vision than another cleanup-only round.

It also sharpens the next question after round 11:

- should the next move widen compose-from-intent beyond AOI and the generic pattern set?
- or should the next move harden the transient composition contract, style/polish coherence, and broader sub-renderer law first?

Those are later questions.

The round-11 question is simpler:

- can we reopen compose-from-intent in one bounded, honest, AOI-first form?

## Why This Is Coherent With The Bigger Picture

The large vision was never:

- endless proof tokens
- endless local cleanup

It was:

- analyzer-v2 as the central intelligence layer
- thin consumers as disposable shells
- composition moving closer to intent rather than only fixed authored view trees

Rounds 9 and 10 made the platform boundary strong enough that a bounded orchestration seam is now the right next test.

So round 11 is coherent with the roadmap if, and only if, it stays:

- stateless
- transient
- AOI-first
- generic-pattern only
- honest about the current job-bound presenter contracts

That is the bounded path from:

- predictable-by-default platform law

toward:

- beautiful-by-default orchestration
