# Memo: Round 13 / AOI Source-Backed Transient Launch Scope

Date: 2026-03-22
Program: Thin Consumer Platformization

## Purpose

Record the next bounded move after round 12.

This memo is meant to answer:

1. what the roadmap says should happen after transient compose-from-intent is both backend-real and consumer-visible
2. what round 13 should prove immediately
3. what should remain blocked so the work does not dissolve into draft persistence, workspace unification, or another broad orchestration branch

This memo sits on top of:

- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md`
- `communications/MEMO_2026-03-22_round12_transient_consumer_adoption_completion.md`
- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`
- `/home/evgeny/projects/the-critic/docs/STAGE9_AOI_CUTOVER_RUNBOOK.md`

## Current Program Position

As of round 12, the program has already proved four important things in sequence:

1. renderer contract law is real on the bounded AOI surface
2. the generic consumer renderer path is package-backed rather than Critic-owned at runtime
3. analyzer-v2 can compose a transient AOI page from intent without jobs or persisted generated views
4. one real consumer can render that transient response honestly through a dedicated shell

That means the current contradiction is no longer:

- can analyzer-v2 compose a bounded transient page?
- can the-critic render that transient page without faking job semantics?

Those are already true.

The current contradiction is narrower:

- the round-12 consumer proof host still depends on hardcoded proof payloads
- but the repo now already has real thinker-scoped AOI v2 saved-result discovery and persistence
- so there is still no honest source-backed bridge from a real AOI result into transient composition

In other words:

- the transient shell is real
- the source analyses are real
- the missing seam is the launch bridge between them

## Why Round 13 Is The Right Next Move

The round-12 decision rule said that after transient consumer adoption the next genuine fork would be:

1. transient product adoption broadening
2. transient-to-authored promotion

Round 13 should choose the first path.

Why:

1. round 12 only proved consumer rendering with hardcoded round-11 example inputs
2. draft persistence before a real source-backed launch path would still be upside down
3. the current codebase already has the AOI saved-result and thinker-identity seams needed to attempt a bounded source bridge
4. source-backed launch is the smallest honest step from “proof host” toward “real user path”

This is also the better fit with the roadmap vision.

The larger program was always moving toward:

- analyzer-v2 as the composition brain
- thin consumers over real analytical outputs
- bespoke transient pages composed from actual analysis context, not only pre-authored catalogs or canned fixtures

Round 13 should therefore realize:

- one real source-backed transient launch seam

not:

- persisted transient drafts
- transient/job workspace unification
- more workflows
- broader app-generation claims

## Current Repo Truth

The repo now has an unusually clear separation of concerns:

### What analyzer-v2 already does

- `POST /v1/presenter/compose-from-intent` accepts a bounded AOI request with explicit prose sections
- planner, generation, transformation, consumer adaptation, and final renderer-law validation are already closed there
- the transient response contract and consumer shell are already documentary-proven

### What analyzer-v2 does not know

- analyzer-v2 does not own the-critic’s saved AOI result database
- the round-11 route accepts explicit prose sections; it does not know how to resolve “latest saved result for thinker/project” from Critic persistence
- stretching analyzer-v2 to reach into Critic persistence directly would be a new coupling, not a cleanup

### What analyzer-v2 already does own

- analyzer-v2 already owns the durable AOI upstream result substrate keyed by `job_id`
- normalized AOI artifacts already exist for:
  - thematic synthesis
  - engagement mapping
  - sin findings
- AOI report normalization already exists in analyzer-v2 metadata / phase-output paths even though it is not yet a Stage-1 artifact family

That means analyzer-v2 is already the right place to reconstruct compose-ready AOI sections once it is handed the correct upstream `v2_job_id`.

### What the-critic already has

- thinker-scoped AOI v2 launch is real
- thinker-scoped AOI run/result discovery is real
- persisted AOI v2 result identity is real:
  - `selected_source_thinker_id`
  - `selected_source_thinker_name`
- the AOI v2 panel already knows how to locate the newest saved result for a thinker/project
- the transient proof host route and shell already exist in the webapp

That means the next honest bridge is not:

- browser-only raw result parsing as permanent platform law
- deriving compose sections from saved `PagePresentation` payloads and hoping `raw_prose` is complete
- analyzer-v2 direct database reach-through

It is:

- a two-step bounded bridge:
  1. the-critic resolves which saved AOI result / `v2_job_id` should be used
  2. analyzer-v2 reconstructs compose-ready sections from its own durable AOI artifacts and phase outputs

## Bounded Round-13 Claim

Round 13 should prove one bounded thing:

- the-critic can launch the existing AOI transient compose experience from one real saved AOI v2 result for the current thinker/project, through a bounded source-backed bridge that resolves result identity in the-critic and performs source-result-to-compose mapping in analyzer-v2, without relying on hardcoded proof payloads and without widening into draft persistence or workspace unification

The required proof surface should remain:

- AOI only
- `consumer_key = the-critic`
- the existing transient consumer shell from round 12

The bounded launch source should be:

- one saved AOI v2 result already associated with the current project + thinker

The bridge should remain bounded to two explicit composition profiles:

- `dossier`
- `comparison`

Those profiles are the honest bounded continuation because they correspond to the round-11 and round-12 proof surfaces already in the repo.

## What Round 13 Should Realize

### 1. One Narrow Critic-Side Result Resolver

Round 13 should add one narrow source-backed compose bridge on the-critic’s backend, but its responsibility should be limited to result discovery and proxying.

Recommended shape:

- one dedicated Critic API endpoint that:
  - accepts project + thinker context
  - resolves a saved AOI v2 result
  - chooses a concrete upstream `v2_job_id`
  - forwards a bounded source-backed compose request to analyzer-v2
  - returns the transient response unchanged except for honest transport/error wrapping

The key revision is:

- the-critic should not be the permanent home of AOI result-to-compose mapping

Its job is:

- resolve source identity where the saved result already lives
- pass the stable upstream handle onward

For reproducibility and multi-result safety, the bridge should support:

- default newest completed/restorable AOI v2 result for the current thinker/project
- optional explicit source selection override via saved result id or `v2_job_id`

### 2. One Analyzer-Owned Source Mapping Route

Round 13 should add one bounded analyzer-v2 route or helper path parallel to `compose-from-intent`, not widen the round-11 request into a union.

The analyzer-owned request should be keyed by:

- `workflow_key`
- `consumer_key`
- `source_job_id` (the upstream AOI `v2_job_id`)
- `profile`
- optional `user_intent`
- optional `style_school`

This route should own the actual source-result-to-compose mapping.

That means analyzer-v2, not the-critic, should:

- load AOI normalized artifacts and phase outputs for `source_job_id`
- reconstruct the bounded compose sections
- call the existing compose-from-intent orchestration internally
- return the same transient response contract

This is the right architectural split because analyzer-v2 already owns:

- AOI contract normalization
- AOI artifact families
- phase-output metadata
- compose-from-intent orchestration

### 3. One Code-Owned AOI Source Profile Mapping

Round 13 should not ask the browser or an LLM to guess how AOI upstream results become compose sections.

It should add one deterministic analyzer-owned profile mapping from durable AOI upstream outputs to the existing round-11 request shape.

Freeze two source profiles:

- `dossier`
  - sections built from:
    - thematic synthesis normalized artifact
    - thematic report normalized/metadata-backed output
- `comparison`
  - sections built from:
    - engagement mapping normalized artifact
    - sin findings normalized artifact
    - thematic report normalized/metadata-backed output

This chooses the analyzer-side path explicitly:

- do not treat saved `PagePresentation` `raw_prose` as the primary source contract

Reason:

- the saved Critic result persists `_presentation`, `v2_job_id`, and thinker identity
- `raw_prose` on saved presentation views is renderer-facing and may be null or incomplete
- the durable AOI upstream truth already exists in analyzer-v2 artifacts / phase outputs keyed by `v2_job_id`

The important requirement is:

- deterministic profile-to-section mapping
- no prompt-generated section selection
- no partial best-effort filling when a required source output is missing

If the upstream job cannot provide the material required for the selected profile, the route should fail honestly.

### 4. One Real Source-Backed Consumer Path

Round 13 should replace hardcoded proof payloads as the primary closure path.

The dedicated transient page from round 12 should remain the proof host, but it should now be able to launch from real AOI result context rather than only from baked example payloads.

Recommended bounded UX:

- keep the dedicated transient host route
- add source-backed launch actions for:
  - `Compose dossier from latest AOI V2 result`
  - `Compose comparison from latest AOI V2 result`
- require current project + thinker context
- allow an explicit source-result override for reproducible proof runs when needed
- keep the round-12 hardcoded examples only as developer fallback / diagnostic fixtures, not as the primary closure path

This keeps the shell isolation from round 12 while closing the source realism gap.

### 5. One Honest Error Surface

Round 13 should keep the error doctrine explicit.

Likely status classes:

- `400`
  - malformed profile / missing thinker context / bad request
- `404`
  - no saved AOI v2 result found for the current project + thinker
- `409`
  - saved result exists but cannot resolve to a valid upstream `v2_job_id`
  - or the upstream job exists but cannot satisfy the requested bounded source profile
  - or analyzer-v2 returns final renderer-contract invalid
- `502`
  - upstream orchestration / malformed analyzer response
- `503`
  - analyzer dependency unavailable

The important program rule is:

- do not hide “missing source material” behind a silent fallback to hardcoded examples
- do not silently fall back from analyzer-owned source reconstruction to saved presentation `raw_prose`

### 6. One Bounded Proof Input Discipline

Round 13 closure should be source-backed, not fixture-backed.

That means the proof should name:

- the specific thinker
- the specific project
- the specific saved AOI result or `v2_job_id` used as source
- the selected profile:
  - `dossier`
  - `comparison`

The source-backed bridge may still preserve the round-12 example payloads in the codebase as dev fixtures.
But closure should no longer depend on them.

## What Round 13 Should Not Realize

Round 13 should stay explicitly out of:

- transient draft persistence
- promoting transient pages into saved authored views
- dual-mode `AnalysisWorkspacePage`
- widening `PagePresentation`
- making `V2TabContent` transient-aware
- generic multi-workflow source-backed composition
- arbitrary section picking from saved results
- browser-side permanent parsing of AOI result internals as the platform law
- analyzer-v2 direct reach into the-critic persistence layer
- genealogy source-backed launch
- making the transient surface the default AOI thinker-page experience

Those are real future questions, but they are not the next bounded move.

## Proof Standard

Round 13 should be treated as closed only if all of the following are true:

1. a real saved AOI v2 result for the current thinker/project can launch the `dossier` transient compose path successfully
2. a real saved AOI v2 result for the current thinker/project can launch the `comparison` transient compose path successfully
3. those two launches do not use hardcoded proof payloads as the source of truth
4. the source-backed bridge is deterministic and code-owned
5. missing source material for a selected profile fails honestly rather than falling back silently
6. the existing transient shell renders the returned response without widening the job-backed workspace
7. `ViewRenderer` still requires zero runtime changes

Saved proof evidence should include:

- the source result identity used for dossier
- the source result identity used for comparison
- the resolved upstream `v2_job_id` used for dossier
- the resolved upstream `v2_job_id` used for comparison
- the exact source-backed launch request(s)
- the returned transient response JSONs
- screenshots and text snapshots of the rendered transient shell
- focused regression on the source-backed path

## Why This Is Better Than The Obvious Alternatives

### Not Draft Persistence Yet

Round 12 already said persistence before real consumer adoption would be upside down.

After round 12, the same logic still applies in a narrower form:

- persistence before a real source-backed launch path would just persist a proof fixture workflow

That is the wrong next layer.

### Not Workspace Unification Yet

The old workspace and the transient shell still represent different lifecycle laws:

- job-backed restore / refresh / export / capture / provenance
- transient compose / return / discard

Round 13 should bridge source into the transient path, not pretend those lifecycles are already one thing.

### Not Generic Multi-Workflow Source Bridging Yet

AOI is still the honest first source-backed surface because:

- round 9 closed renderer law there
- round 10 closed consumer consolidation there
- round 11 closed transient composition there
- round 12 closed transient consumer adoption there
- the thinker-scoped result identity and discovery seams are already real there

Genealogy still carries more source/rendering debt and should stay out of scope.

### Not Analyzer Reach-Through Yet

The consumer persistence seam currently lives in the-critic.

Pretending analyzer-v2 can already fetch Critic saved results directly would be a new coupling disguised as cleanup.

The bounded round-13 move should respect where the source data actually lives today:

- the-critic resolves saved-result identity
- analyzer-v2 resolves durable upstream AOI content by `v2_job_id`

## Decision Rule

If round 13 succeeds, the program should then be in a much stronger position to choose between:

1. bounded transient-to-authored promotion
   - draft persistence
   - user curation of composed pages

2. broader transient adoption
   - more source-backed AOI entrypoints
   - better transient shell ergonomics
   - eventual hot-path launch integration

But round 13 itself should only prove:

- one real source-backed AOI launch bridge

## Final Round-13 Sentence

If the team needs one operational sentence for the next move, it should be:

- **Use round 13 to replace hardcoded transient proof inputs with one real AOI source-backed launch seam, so a saved thinker-scoped AOI result can feed the existing transient compose shell honestly without widening into persistence or workspace unification.**
