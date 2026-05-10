# Memo: Stage 13 / Minimal Generic Host Contract Scope

Subtitle: Formalize Thin-Host Responsibilities Over Existing Analyzer-Native Run, Result, Readiness, And Transient Launch Seams

Date: 2026-03-24
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Prior Stage Memo: `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_scope.md`
Stage 12 Completion: `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_completion.md`
Stage 11 Completion: `communications/MEMO_2026-03-24_stage11_rich_semantic_page_planning_completion.md`
Stage 10 Completion: `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_completion.md`
Stage 9 Completion: `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_completion.md`

## Purpose

Define the next honest stage after Stage 12 served-renderer-law generalization.

This memo is about the next missing platform seam:

- one explicit minimal host contract over the analyzer-native surfaces that are already real
- one clear owner split between analyzer-v2 and the host app
- one shared host adapter/client layer instead of page-local analyzer glue
- one explicit rule for which interactions are:
  - direct analyzer calls
  - host-owned proxy/persistence hooks
  - local host-only concerns
- one bounded generic-host proof inside the current consumer without rebuilding intelligence locally

It is not about:

- generic auth federation across apps
- a second consumer product launch
- session lifecycle, drafts, sharing, or publishing
- new analyzer planning or renderer-law expansion
- making AOI source-backed compose fully consumer-neutral
- mandatory host adoption of every analyzer-native advisory seam

## Why This Stage Now

The last four stages changed the platform position materially.

What is now true:

1. Stage 9 created a real analyzer-owned `route-task -> hydration -> planning decision` seam
2. Stage 10 created a real analyzer-owned readiness seam over durable AOI and genealogy result truth
3. Stage 11 created a real analyzer-owned transient semantic tree seam that the current host can actually render
4. Stage 12 created a real analyzer-owned served-intent renderer-law seam over current transient and job-backed AOI/genealogy surfaces

That means the next missing seam is no longer mostly inside analyzer-v2.

It is the boundary between:

- analyzer-owned intelligence and presentation truth
- host-owned project context, proxying, persistence hooks, and navigation/rendering shell

The codebase already shows this split clearly.

Analyzer-native host-consumed surfaces are already real:

- `v1/runs/discovery`
- `v1/results/discovery`
- `v1/results/by-job/{job_id}`
- `v1/results/by-job/{job_id}/presentation`
- `v1/results/by-job/{job_id}/refresh-presentation`
- `v1/presenter/view/{job_id}/{view_key}`
- `v1/presenter/compose-from-intent`
- `v1/results/by-job/{job_id}/source-backed-readiness`

Host-owned seams are also already real:

- project context middleware in the-critic
- `cache-v2` snapshot warming routes in the-critic API
- the AOI source-backed compose proxy route that resolves project-local source identity before launching analyzer compose
- page-local URL building and local error handling in the-critic pages and client modules

So the Stage 13 problem is no longer "invent a host contract."

It is:

- formalize and minimally consolidate the host contract that already exists implicitly across analyzer-v2 and the-critic

## Explicit Sequencing Note

Stage 12 remains partial in the roadmap, and Stage 14 lifecycle work remains open.

Choosing Stage 13 now is not a claim that:

- every genealogy served mode is already strict-clean
- Stage 12 no longer has room for later widening
- lifecycle/session work stopped mattering

It is a claim about leverage:

- Stage 12 established the foundational served boundary strongly enough for the current AOI/genealogy proof matrix
- that does **not** mean every current authored or no-`composition_mode` restore path is equally normalized; it means the Stage 12 proof seam is strong enough that the next missing architectural boundary is now the host contract rather than more renderer-law invention
- the remaining Stage 12 work is mostly promotion and widening
- the next missing architectural seam is the under-documented host boundary that sits on top of those analyzer-owned results, readiness, and transient contracts

So the next honest move is Stage 13 before Stage 14.

## Strategic Diagnosis

### What is already real

The host contract is not hypothetical anymore.

It already exists in code across two repos.

In analyzer-v2:

- results and presentation boundaries are public and typed
- source-backed readiness is public and typed
- transient compose and source-backed transient compose contracts are real
- route-task and plan-task exist as analyzer-native advisory seams, even if the host does not yet consume them

In the-critic:

- `webapp/src/lib/boundedV2Client.ts` already acts as a partial generic client for runs, results, presentation, refresh, and single-view fetch
- `webapp/src/hooks/useBoundedV2Workspace.ts` already acts as a substantial shared result-backed workspace adapter over AOI/genealogy proof-mode restore behavior
- `webapp/src/lib/composeFromIntentClient.ts` already acts as a partial transient-launch client
- `webapp/src/components/ViewRenderer.tsx`, `webapp/src/components/V2TabContent.tsx`, and the Stage 11 transient shell already provide a generic rendering host
- `api/middleware.py` already owns project identity injection
- `api/server.py` already owns cache warming and AOI source-backed launch proxy hooks

That means a large part of Stage 13 is formalization and consolidation, not greenfield invention.

### What is not yet real

There is still no one explicit Host Contract v1 that says:

- which analyzer routes a host may call directly
- which launch or persistence actions must stay host-owned
- what context the host must always supply
- how `project_id`, `consumer_key`, `workflow_key`, and selector inputs are threaded
- which identity field is canonical for each family:
  - upstream `job_id` / `v2_job_id`
  - host-local `analysis_id`
- which scope channel is authoritative for each family:
  - analyzer path/query
  - host header
  - both
- where local snapshot caching fits
- where source identity resolution is analyzer-owned truth versus host-owned preparation
- where workflow-specific surface selection is still host-owned in v1
- which host pages may still contain workflow-specific analyzer glue and which should not

The current state is visibly fragmented:

- some the-critic pages use shared clients
- some still build analyzer URLs directly
- AOI source-backed launch uses a host proxy
- genealogy result consumption is still partly page-local
- Stage 10 readiness exists, but the current host does not use it as a first-class launch/readiness contract

So the host contract is real but only partially normalized.

## The Real Stage 13 Problem

The real Stage 13 problem is not:

- "build a second app"
- "solve lifecycle"
- "adopt every orchestrator route"
- "erase all the-critic coupling"

It is:

- "make the existing thin-host contract explicit enough that the current consumer no longer depends on page-local analyzer glue to consume analyzer-native results and launches"

That is the next durable platform seam.

## Bounded Claim For Stage 13

Stage 13 should prove one bounded thing:

- the current host can consume analyzer-v2 through one explicit Host Contract v1 and one shared host adapter layer across the current AOI and genealogy proof seams, while keeping project context, proxy hooks, and local persistence explicitly host-owned and keeping analytical intelligence upstream

This should be framed as the bounded first slice of Stage 13, not full Stage 13 closure.

That is enough to strengthen the thin-host thesis without pretending the platform already has:

- a second consumer
- host-neutral auth
- generic workflow launch UX
- lifecycle/session law

The honest expected ledger state after this slice is still:

- Stage 13 remains `Partial`

because the roadmap exit evidence is stronger:

- second consumer or materially harder generic-host proof without rebuilding intelligence locally

## Recommended Stage 13 Shape

### Decision 1: keep Stage 13 current-consumer-grounded, not falsely host-neutral

The proof host should remain:

- the-critic

The contract should be explicit about current bounded coupling:

- `consumer_key='the-critic'` remains real on the currently proven AOI and result-backed seams
- AOI source-backed transient compose still includes the-critic-specific host preparation
- result and run families accept `consumer_key` as request-level input, but the transient compose families are structurally more constrained:
  - `compose-from-intent`
  - `compose-from-source`
  still enforce `TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"` inside analyzer-v2 rather than exposing consumer neutrality at the public route boundary
- no second consumer is required in this slice

Stage 13 should prove that the contract is explicit and minimal, not that all consumer coupling has disappeared.

### Decision 2: define one explicit Host Contract v1 matrix over current live seams

Stage 13 should produce one contract artifact that is concrete enough for two independent implementors to agree on.

It should enumerate at least these contract families:

1. run discovery and run detail
2. result discovery
3. result manifest
4. result presentation
5. result refresh
6. single-view fetch
7. transient compose-from-intent
8. source-backed readiness
9. source-backed transient launch
10. cache/snapshot persistence hook

For each family, the contract must say:

- owner:
  - analyzer direct
  - host proxy
  - host local only
- canonical identity field:
  - upstream `job_id` / `v2_job_id`
  - host-local `analysis_id`
- identity authority:
  - upstream-authoritative
  - host-local continuity alias only
- required inputs:
  - `project_id`
  - `consumer_key`
  - `workflow_key`
  - `composition_mode`
  - `profile`
  - source selector fields
- authoritative scope channel:
  - analyzer path/query
  - host header
  - mixed
- authoritative response source
- whether host-local identity is being translated into upstream identity before launch
- whether the host may cache/snapshot locally
- whether the host is allowed to substitute a local snapshot for UX continuity
- whether the family is:
  - current must-have Host Contract v1
  - optional advisory v1

This contract should be versioned and explicit.

### Decision 3: make the direct-vs-proxy split a first-class law

The current codebase already implies three distinct interaction classes.

Stage 13 should formalize them rather than hiding them:

Direct analyzer calls:

- runs discovery/detail
- results discovery
- result manifest
- result presentation
- refresh presentation
- single-view fetch
- compose-from-intent
- source-backed readiness

Host proxy or host-preparation calls:

- cache/snapshot warming
- AOI source-backed compose when the host starts from project-local saved-result identity rather than an already resolved `source_v2_job_id`
  - this is not just a thin pass-through
  - it currently includes host-owned identity resolution, cross-reference validation, context matching, payload shaping, and upstream error mapping

Host-local concerns:

- auth/session handling
- project context resolution
- navigation and return paths
- snapshot persistence policy
- local UX state

Stage 13 should not create a generic host proxy over all analyzer traffic.

The point is to document and normalize the existing split, not to erase it.

### Decision 4: consolidate the-critic onto one shared host adapter layer

This stage should not stop at documentation.

It should require a real host-side consolidation in the-critic across the current AOI and genealogy proof seams.

The current duplication is visible in:

- `webapp/src/lib/boundedV2Client.ts`
- `webapp/src/hooks/useBoundedV2Workspace.ts`
- `webapp/src/lib/composeFromIntentClient.ts`
- `webapp/src/pages/GenealogyPage.tsx`
- `webapp/src/components/influence/AoiV2ThematicPanel.tsx`

Stage 13 should pull the contract-covered analyzer interactions behind one shared adapter or hook family so that:

- `consumer_key`
- URL construction
- error normalization
- snapshot/cache followup
- readiness fetching
- direct-vs-proxy routing

stop being page-local decisions.

This should be right-sized honestly.

Stage 13 is **not** starting from a host with no shared adapter substrate.

It is starting from a host where:

- `boundedV2Client.ts` and `useBoundedV2Workspace.ts` already cover a substantial portion of the result-backed contract
- `AnalysisWorkspacePage` is already materially on that shared path

So the real consolidation target is narrower:

- move the remaining contract-covered AOI/genealogy result-backed fetch behavior off page-local or component-local URL construction where it still exists
- document explicitly which remaining direct fetch families stay out of scope in this slice:
  - polish
  - pipeline visualization
  - provenance support fetches

### Decision 5: adopt Stage 10 readiness where it materially belongs

A host contract is weak if it ignores the analyzer-native readiness seam that now exists.

So Stage 13 should adopt `GET /v1/results/by-job/{job_id}/source-backed-readiness` in at least one real host launch surface:

- the current AOI source-backed transient launch path

That should replace any remaining host-side assumption that profile feasibility can be inferred locally.

The host still chooses when to launch.

But feasibility truth should come from the analyzer-owned readiness contract where that seam already exists.

The proof bar should also stay cross-workflow here.

So Stage 13 should require one genealogy readiness consumption case as well, for example:

- a genealogy result-backed surface deciding whether a `composition_mode` is actionable from analyzer-owned readiness truth rather than only local manifest/presentation heuristics

### Decision 6: document host-side surface selection as an explicit v1 concern

The host currently still decides, per workflow experience, which analyzer-native surfaces it combines.

Examples already visible in the code:

- result-backed workspace flows
- AOI source-backed transient launch flows
- workflow-specific navigation between discovery, restore, transient, and local snapshot fallback

Stage 13 should not pretend that this surface-selection law has already moved upstream.

The Host Contract v1 artifact should therefore state explicitly:

- which current workflow experiences still have host-owned surface selection
- which analyzer-native surfaces each of those experiences is expected to combine
- whether that host-side selection is accepted Stage 13 law or explicitly deferred for later analyzer-owned generalization

### Decision 7: keep Stage 13 "routing" narrow and explicit

The roadmap says the host contract must cover routing.

In Stage 13 that should mean:

- host navigation and return-path ownership
- route-to-surface selection between result-backed, transient, and source-backed host experiences
- explicit mapping of which host pages consume which analyzer-native surfaces

It should **not** mean mandatory adoption of:

- `POST /v1/orchestrator/route-task`
- `POST /v1/orchestrator/plan-task`

Those analyzer-native advisory seams remain real and useful, but Stage 13 does not need to force a task-centric host UX before the host contract itself is explicit.

### Decision 8: keep Stage 13 out of lifecycle and out of analyzer-side law widening

Do not widen Stage 13 into:

- session/draft persistence strategy
- sharing/publishing
- permissions or auth federation redesign
- renderer-law promotion of more genealogy modes
- generic transient planning across more workflows

Those are real later stages.

The Stage 13 job is to formalize and minimally consolidate the current host boundary, not to solve the whole platform.

## Proof Bar

Stage 13 should not be approved on prose alone.

The proof bar should require:

1. one explicit saved Host Contract v1 artifact
   - direct vs proxy vs local ownership
   - required inputs
   - current must-have versus optional advisory contract families
2. one shared host adapter/client layer used by both:
   - an AOI result-backed or source-backed surface
   - a genealogy result-backed surface
3. one real AOI launch surface using analyzer-owned readiness instead of local feasibility assumptions
4. one real genealogy readiness consumption case on a result-backed surface, so the proof remains cross-workflow rather than AOI-shaped
5. one explicit proof that current contract-covered host pages no longer construct analyzer URLs ad hoc except for documented out-of-scope cases
6. one reviewable proof that intelligence still lives upstream:
   - the host consumes route/result/readiness/compose contracts
   - the host does not re-derive analytical or renderer-law truth locally

The exit evidence for this bounded slice is not:

- a second app

It is:

- a real generic-host proof inside the current consumer over more than one workflow family, without rebuilding analyzer intelligence locally

That is still only the bounded first slice of Stage 13.

The larger roadmap exit evidence remains open after this slice until either:

- a second consumer adopts the contract
- or the platform demonstrates a materially harder generic-host proof than one bounded consumer-backed integration

## What Stage 13 Is Not

Stage 13 is not:

- Stage 14 lifecycle
- a second-consumer launch
- orchestrator UX adoption
- generic auth
- a claim that AOI source-backed launch is already consumer-neutral
- a claim that the-critic stops owning project context or local snapshot caching

It is the minimal contract formalization step that should make those later moves less bespoke.
