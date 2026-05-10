# Memo: Next Steps After Stage 9

Date: 2026-03-18

## Purpose

This memo defines the most sensible next strategic program after Stage 9.

It is meant to answer:

- what should happen next now that the AOI by-reference cutover is functionally complete
- whether the next move should be called Stage 10
- what still blocks the broader "dynamic bespoke apps / thin consumers" vision
- what sequence of work would actually move the platform toward that vision

This is a strategy memo, not a closure memo.
It assumes the factual baseline recorded in:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_snapshot_after_stage9.md`

## Executive Judgment

The next move should **not** be:

- invent more AOI semantics
- keep stretching Stage 9
- casually declare a Stage 10 without defining it

The next move should be:

- **post-Stage-9 platformization for genuinely thin apps**

Stage 9 proved that analyzer-v2 can carry more of the live AOI path.
It did **not** prove that we can already generate disposable apps on demand with almost no bespoke host work.

So the next program should focus on the missing platform layers that stand between:

- bounded thin-consumer proof

and:

- real dynamic bespoke apps

## The Core Strategic Reality

Right now the platform has three strong things:

1. a strong **definition catalog**
2. a strong **planner/executor/presenter spine**
3. one meaningful **bounded thin-consumer proof**

Right now the platform is still weak in four places:

1. the **consumer contract**
2. the **artifact economy**
3. **dynamic page/view composition**
4. **host normalization**

Those four weaknesses are why the vision is still only partially realized.

## What Should Not Be The Next Priority

The following are tempting but strategically wrong as the immediate next move:

### 1. More AOI objective enrichment

AOI already proved enough for the current stage boundary.

Adding:

- multi-thinker AOI
- richer AOI sub-surfaces
- new AOI-specific metadata layers

would expand semantics before fixing the platform bottlenecks that still make new apps thicker than they should be.

### 2. A broad style-polish expansion alone

The "beautiful by default" problem is real.
But visual polish by itself does not solve:

- reusable consumer integration
- reusable artifacts
- dynamic composition

So style work alone would improve demos while leaving the substrate problem unresolved.

### 3. A total rewrite of The Critic first

The Critic is still thick.
But a wholesale rewrite is not the right next step.

The right next move is:

- identify and remove the specific plumbing that still prevents new consumers from being truly thin

not:

- rebuild the app from scratch on faith

## Recommended Next Program

The next program should be a four-track platformization pass.

## Track 1: Authority, API, And Observability Boundary

### Goal

Make analyzer-v2 clearly authoritative for bounded run/result lifecycle, with the host acting as a thin launcher and compatibility shell rather than a second lifecycle owner.

### Why this is next

The March 17 run-lifecycle and Stage 5 critiques are persuasive:

- analyzer-v2 already owns most of the real authority
- The Critic still carries unnecessary plumbing
- new consumers should not have to copy that plumbing

### Concrete scope

1. Thin or remove the Critic-side background polling thread and in-memory registries for bounded v2 runs
2. Keep only the minimal host responsibilities that actually belong there:
   - project/document loading
   - start-path assembly
   - local compatibility/cache affordances where explicitly needed
3. Tighten the analyzer-v2-side API and observability surface for:
   - active run discovery
   - completed result discovery
   - cancel/resume
   - refresh/restore
4. Add the missing lightweight observability surfaces in analyzer-mgmt or equivalent tooling so the new authority is easy to inspect

### Outcome

The result should be:

- new bounded consumers do not need to inherit Critic-era polling architecture
- analyzer-v2 is visibly the operational authority, not just the semantic one

Track 1 is deliberately about:

- authority
- routing
- APIs
- observability

It is **not** the consumer-SDK track.

## Track 2: Consumer Contract And Host Adapter

### Goal

Make it cheap and boring to build the next thin app.

### Why this is necessary

Today, even though analyzer-v2 owns more truth, a new consumer still has to reassemble too much:

- client wrappers
- lifecycle management
- restore logic
- compatibility behavior
- generic page rendering setup

That means the platform does not yet provide a real "thin app kit."

### Concrete scope

1. Define a reusable consumer SDK / host-adapter contract for:
   - start
   - poll/discover
   - cancel/resume
   - result discovery
   - presentation restore
2. Make the generic workspace path first-class rather than incidental
3. Minimize workflow-specific frontend code for bounded analyzer-v2-backed surfaces
4. Document the expected split between:
   - analyzer-v2 responsibilities
   - host-shell responsibilities

### Outcome

The next app should not need to rediscover the Critic integration pattern manually.
It should be able to say:

- give me a project shell
- give me a bounded workflow
- render the presentation

and stop there.

Track 2 is deliberately about:

- reusable client behavior
- host responsibilities
- generic workspace reuse
- frontend/host ergonomics

It is **not** the API-authority track.

## Track 3: Build The Artifact Economy That The Vision Actually Needs

### Goal

Move from a shared definition catalog to a genuinely reusable analytical substrate.

### Why this is the deepest missing layer

Right now the system reuses:

- engines
- chains
- workflows
- views
- renderers

But it does **not** yet reuse analytical outputs as first-class cross-job artifacts.

That means the platform is currently good at composing plans, but not yet good at composing results or applications from stable reusable analytical building blocks.

### Concrete scope

1. Introduce stable identity for reusable artifacts beyond job-scoped outputs
2. Support cross-job lookup by input identity and freshness
3. Add staleness/version rules
4. Distinguish clearly between:
   - ephemeral run output
   - reusable analysis product
   - render-ready presentation

### Initial scoping constraint

This track must not begin as a platform-wide abstraction exercise.

The first proof should be limited to:

- exactly **one** artifact class
- exactly **two** jobs
- one freshness rule
- one lookup path

The recommended first artifact proof is:

- `genealogy.relationship_classification`

Reason:

- it already exists as the current bounded genealogy artifact seam
- it is concrete enough to observe
- it avoids generalizing the artifact model before one real reuse case succeeds

Only after that proof works should the artifact model be widened.

### Outcome

Without this layer, "dynamic bespoke apps" will remain mostly a metaphor.
With it, the platform can start to reuse prior analytical work instead of recomputing and rewrapping everything inside isolated jobs.

## Track 4: Move From View Selection To Real Dynamic Composition

### Goal

Let analyzer-v2 assemble new page structures for new analytical situations without depending entirely on a pre-authored fixed catalog.

### Why this matters

The vision of "apps on the fly" requires more than:

- choosing from pre-existing views
- piping them through shared renderers

It requires:

- composing a page hierarchy from intent
- choosing renderers with enforceable contracts
- generating bounded ephemeral view/page structures when the catalog is insufficient

### Concrete scope

1. Add real renderer input contracts and validation
2. Strengthen or add ephemeral view/page composition APIs
3. Allow whole-page composition from:
   - analytical intent
   - engine output summaries
   - audience/style constraints
4. Treat pre-authored view defs as:
   - excellent templates
   - not the only route to page assembly

### Outcome

This is the point where the platform starts to move from:

- "generic consumer over a curated catalog"

toward:

- "LLM-mediated temporary analytical app composition"

## Named Proving Vehicle

The next proof should be anchored on one concrete consumer/workspace path:

- **The Critic's generic `AnalysisWorkspacePage`**

Specifically:

- route: `/p/:projectId/analysis/:workflowKey`
- workflows: `intellectual_genealogy` and `anxiety_of_influence_thematic_single_thinker`

Why this is the right first proving vehicle:

1. it already exists
2. it is meaningfully thinner than the bespoke workflow pages
3. it stresses the real host/consumer boundary without requiring a brand-new app first
4. it can prove cross-workflow genericity inside one existing host shell

The AOI canary remains useful as a secondary regression canary, but it should not be the main forcing function for this next program.

## The Right Proof Target After Stage 9

The next proof should not be another AOI cutover.

The next proof should be:

- one more consumer or workspace path that is meaningfully thinner than The Critic
- over at least two different bounded surfaces
- without downstream semantic repair

The best high-value proof would look like:

1. one generic host shell
2. one common consumer contract
3. analyzer-v2-owned run/result/presentation truth
4. at least one bounded cross-job reusable artifact surface
5. minimal workflow-specific frontend code

That would be much closer to the real north star than another narrow operational rollout.

An execution brief should define this proof more concretely before implementation begins.

## Should This Be Called Stage 10

Not yet.

There is currently no existing Stage 10 definition in the local program documents.

If a stage label is desired, it should be introduced deliberately with a memo that defines:

- objective
- scope
- non-goals
- success criteria
- proof artifacts

Until then, the cleanest label is:

- **Post-Stage-9 Platformization**

or more specifically:

- **Thin Consumer Platformization**

## Proposed Near-Term Sequence

The most defensible order from here is:

1. Write and keep the Stage 9 snapshot/closure record
2. Fix the small residual bookkeeping gap from Stage 9
3. Finish host-thinning for bounded v2 lifecycle
4. Define the reusable consumer contract
5. Start artifact-economy work
6. Only then push harder on dynamic whole-page generation / disposable apps

This order matters because:

- dynamic app generation without a consumer contract creates one-off demos
- a consumer contract without artifact reuse still leaves the substrate shallow
- artifact reuse without host thinning still leaves every app tied to Critic-era glue

See also:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`

## Final Recommendation

The next program should be understood this way:

- Stage 9 made AOI cutover real
- it did not complete the March 13 north-star architecture
- the next high-leverage work is platformization, not more cutover

The real question from here is not:

- "what is Stage 10 called?"

It is:

- "what must become true before a new analysis app can be spun up as a genuinely thin disposable shell?"

The answer is:

- thinner host boundary
- reusable consumer contract
- reusable artifact substrate
- dynamic composition beyond the fixed view catalog

That is the right next program.
