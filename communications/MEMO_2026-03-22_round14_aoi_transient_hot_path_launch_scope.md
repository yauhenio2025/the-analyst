# Memo: Round 14 / AOI Transient Hot-Path Launch Scope

Date: 2026-03-22
Program: Thin Consumer Platformization

## Purpose

Record the next bounded move after round 13.

This memo is meant to answer:

1. what the roadmap says should happen after source-backed transient launch is code-real
2. what round 14 should prove immediately
3. what should remain blocked so the work does not dissolve into draft persistence, workspace unification, or premature default takeover

This memo sits on top of:

- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md`
- `communications/MEMO_2026-03-22_round12_transient_consumer_adoption_completion.md`
- `communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_completion.md`
- `communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_scope.md`
- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`
- `/home/evgeny/projects/the-critic/docs/STAGE9_AOI_CUTOVER_RUNBOOK.md`

## Precondition

Round 14 should not pretend round 13 is more operationally closed than it is.

The round-13 completion note already records:

- code-complete source-backed launch
- focused tests complete
- live browser proof artifacts still pending

Round 14 therefore needs one explicit rule:

- either capture the missing round-13 browser proof artifacts before implementation starts
- or treat round-14 hot-path proof as the artifact bundle that subsumes the missing round-13 browser proof, since a successful real AOI-panel launch into the same source-backed transient path proves the round-13 browser seam as part of round 14

The second path is acceptable, but it must be stated explicitly in the execution plan and proof note.

## Current Program Position

As of round 13 implementation, the program has now made five bounded things real:

1. renderer contract law on the AOI proof surface
2. package-backed generic consumer resolution
3. transient AOI compose-from-intent in analyzer-v2
4. honest transient consumer rendering in the-critic
5. source-backed transient launch from saved AOI result identity into analyzer-owned AOI reconstruction

That means the current contradiction is no longer:

- can analyzer-v2 compose a transient page?
- can the-critic render it honestly?
- can a real saved AOI result feed it?

Those are already closed in code.

The current contradiction is now narrower and more product-facing:

- the transient source-backed path exists
- but it still lives behind a dedicated proof-host route and explicit query-param context
- the real AOI user path does not yet expose that capability as an honest in-flow launch

So the missing seam is no longer source truth.

It is adoption:

- one bounded launch bridge from the real AOI hot path into the already-existing transient path

## Why Round 14 Is The Right Next Move

The round-13 decision rule left two honest forks:

1. bounded transient-to-authored promotion
2. broader transient adoption

Round 14 should choose the second fork first.

Why:

1. draft persistence before one real in-flow launch still keeps the transient surface as a sidecar proof host
2. the repo already has the real AOI entry surface:
   - `AoiV2ThematicPanel`
   - thinker-scoped saved-result discovery
   - the dedicated transient page
3. the current gap is not “can we persist a transient draft?” but “can a real AOI user reach transient composition from the actual AOI panel without deep-link ceremony?”
4. adoption is smaller and safer than persistence because it does not force a premature decision about transient/job lifecycle unification

This is also the better fit with the larger roadmap:

- analyzer-v2 already acts as the composition brain
- the-critic already has the stable AOI hot path
- the next honest step is one bounded handoff between them

not:

- making transient pages durable before they are even in flow

## Current Repo Truth

### What the-critic already has

- `AoiV2ThematicPanel` already owns:
  - thinker-scoped AOI run/result discovery
  - saved-result restore behavior
  - current AOI v2 hot-path rendering
- the dedicated transient route already exists:
  - `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker/compose-from-intent`
- the transient page already knows how to:
  - launch source-backed `dossier`
  - launch source-backed `comparison`
  - render the transient shell

### What is still awkward

- a real user on the thinker page cannot discover this transient source-backed capability naturally
- source context must currently be assembled as route query params by hand or by a proof-specific deep link
- the transient experience is still operationally “off to the side” from the AOI hot path

### What should not change

- `AoiV2ThematicPanel` should remain the normal AOI v2 execution / restore surface
- `V2TabContent` should remain job-backed
- `AoiComposeFromIntentPage` should remain a separate transient lifecycle surface
- analyzer-v2 should not need new orchestration semantics just to support round 14

That means round 14 is not about new backend intelligence.

It is about one real UI handoff.

## Bounded Round-14 Claim

Round 14 should prove one bounded thing:

- a real AOI user can launch the existing source-backed transient compose experience directly from the actual AOI hot path for the current thinker/project, using a concrete saved-result context when available, without embedding transient rendering into the job-backed workspace and without making the transient path the default AOI experience

The required proof surface should remain:

- AOI only
- the-critic only
- the existing source-backed transient route and shell

The required source doctrine should remain:

- normal UI launch uses saved-result identity, not raw `source_v2_job_id` override semantics
- analyzer-v2 still owns source-result-to-compose reconstruction

## What Round 14 Should Realize

### 1. One Real AOI Hot-Path Launch Affordance

Round 14 should add one explicit transient-launch affordance to the real AOI v2 user path.

Required seam:

- inside `AoiV2ThematicPanel`

The user should be able to initiate:

- `Compose dossier`
- `Compose comparison`

from the real AOI surface, without manually constructing the transient proof-host URL.

This seam should not be left ambiguous.

Reason:

- `AoiV2ThematicPanel` already owns saved-result discovery and restore behavior
- the parent AOI page owns thinker/project context, but not the current saved-result selection state
- keeping the launch group panel-local avoids widening round 14 into new page-level orchestration state

### 2. One Honest Context-Handoff Rule

Round 14 should freeze one user-facing source selection rule.

Recommended rule:

- if the user currently has a saved AOI result selected/restored in the AOI panel, launch transient compose from that saved result
- otherwise launch from the newest saved AOI result for the current thinker/project

The handoff should carry:

- `project_id`
- `selected_source_thinker_id`
- advisory `selected_source_thinker_name`
- `source_analysis_id` when a concrete saved result is already selected

The resolution site should be explicit:

- the frontend panel resolves this source identity from its already-loaded saved-results state
- the backend remains the validation and proxy seam, not the place where product-grade “pick newest from the currently visible AOI panel state” is decided

That means round 14 should freeze three UI rules:

1. if a concrete saved result is selected/restored in the panel, use its `source_analysis_id`
2. otherwise choose the newest saved result from the panel’s already-loaded saved-results list
3. if there is no saved result, disable the launch affordance or show a clear empty-state explanation rather than launching into avoidable error

The “newest” fallback should also be deterministic in UI terms before it becomes product law:

- the saved-results list used for fallback must be explicitly sorted by effective completion time
- the current selected source should be explicit panel state, not an accidental side effect of whichever row happened to load first

Normal product launch should **not** expose raw `source_v2_job_id` override as the main UX surface.
That override can remain dev/proof-only.

### 3. One Separate Runtime Surface

Round 14 should keep the transient surface separate at runtime.

That means:

- navigate into the existing transient route
- keep `AoiComposeFromIntentPage` as the transient runtime surface
- keep `AoiComposeFromIntentShell` as the transient renderer surface

Round 14 should also freeze an explicit one-click handoff contract rather than a vague deep-link:

- include `profile=dossier|comparison`
- include the resolved `source_analysis_id`
- include thinker context
- include an explicit return target or equivalent backlink contract
- auto-run the requested transient compose on landing

The important rule is:

- the user should not have to land on the proof host and then click a second dossier/comparison button there just to finish the launch

Round 14 should **not**:

- mount the transient shell inside `AoiV2ThematicPanel`
- make `V2TabContent` transient-aware
- stretch `PagePresentation` to fake transient compatibility

The launch should feel integrated.
The lifecycle law should remain separate.

### 4. One Bounded UX Discipline

Round 14 should make the transient path discoverable but still obviously secondary to the stable AOI workspace.

Recommended UX:

- one compact launch group on the AOI panel
- clear copy that this is a transient composed page
- keep ordinary AOI run/restore behavior unchanged
- preserve a clear return path back to the AOI panel
- navigate immediately and let the transient page show its existing blocking loading state while analyzer-v2 performs planning / compose work

The important rule is:

- real launch affordance, not silent takeover

### 5. One Honest Error / Empty-State Surface

Round 14 should keep failure semantics explicit in the UI handoff.

Likely surface classes:

- no saved AOI result available
  - disabled launch affordance or clear empty-state explanation
- selected saved result cannot resolve source-backed compose
  - surface the current source-backed `404` / `409` semantics after handoff
- transient compose fails upstream
  - keep existing transient page error handling

Do not add a second independent source-resolution logic in the browser.

## What Round 14 Should Not Realize

Round 14 should remain explicitly out of:

- transient draft persistence
- promoting transient pages into saved authored views
- dual-mode `AnalysisWorkspacePage`
- embedding transient rendering inside `AoiV2ThematicPanel`
- making transient compose the default AOI tab or default thinker-page experience
- generic multi-workflow transient launch integration
- genealogy launch integration
- raw `source_v2_job_id` power-user controls as the main product path
- analyzer-v2 direct reach-through into the-critic persistence

Those are real future questions, but they are not the next bounded move.

## Proof Standard

Round 14 should be treated as closed only if all of the following are true:

1. from the real AOI thinker-page hot path, the user can initiate `dossier` transient compose without manual URL construction
2. from the real AOI thinker-page hot path, the user can initiate `comparison` transient compose without manual URL construction
3. when a concrete saved AOI result is already selected in the AOI panel, the handoff preserves that saved-result identity rather than silently switching to some other source
4. the transient surface still renders on its own dedicated route and does not reuse the job-backed workspace shell
5. ordinary AOI v2 run / restore behavior is unchanged when the transient launch is not used
6. `ViewRenderer`, `V2TabContent`, and analyzer-v2 orchestration contracts still require zero runtime widening for this round
7. when no saved AOI result exists for the current thinker/project, the launch affordance fails closed in the AOI panel itself rather than pretending to launch and only then surfacing an avoidable error

Saved proof evidence should include:

- thinker-page screenshot showing the transient launch affordance
- the navigated transient route / query context
- dossier launch screenshot / text snapshot
- comparison launch screenshot / text snapshot
- saved transient response artifacts for the launched runs
- focused regression covering the hot-path handoff behavior

## Why This Is Better Than The Obvious Alternatives

### Not Draft Persistence Yet

Source-backed launch is now real, but the transient path is still a separate lifecycle.

Persisting it immediately would force a larger unresolved question:

- what exactly is the durable object?
  - a transient page snapshot
  - generated view definitions
  - a workspace draft
  - a new result flavor

That is a real design tranche.
It is not the smallest next move.

### Not Default Takeover Yet

The AOI hot path already has a stable job-backed restore and rendering model.

Round 14 should add a secondary transient launch seam to that stable path.
It should not claim that transient composition is already ready to replace the ordinary AOI surface.

### Not Workspace Unification Yet

The program still has two different lifecycle laws:

- job-backed execute / restore / refresh / export
- transient source-backed compose / render / discard

Round 14 should connect them with one bounded handoff.
It should not pretend they are already one surface.

## Decision Rule

If round 14 succeeds, the program should then be in a much stronger position to choose between:

1. bounded transient-to-authored promotion
   - draft persistence
   - curated save / reopen behavior

2. deeper transient adoption
   - more AOI entrypoints
   - clearer shell ergonomics
   - eventual defaulting decisions

But round 14 itself should only prove:

- one real AOI hot-path launch bridge into the already-existing source-backed transient surface

## Final Round-14 Sentence

If the team needs one operational sentence for the next move, it should be:

- **Use round 14 to add one real AOI hot-path launch seam into the existing source-backed transient page, so transient composition becomes reachable from the actual thinker workflow without widening into persistence, workspace unification, or premature default takeover.**
