# Memo: Stage 13 Tier A / AOI Canary Second-Consumer Proof Scope

Date: 2026-03-24
Status: Revised draft scope memo after review
Program: Dynamic Bespoke Apps Platformization
Roadmap source: `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

## Summary

Implement the first tranche in the draft roadmap:

- Stage 13 exit, Tier A
- using `aoi-canary` as the bounded second-consumer proof target
- result-backed only
- read-only only

This slice is meant to close the cheapest honest part of the “generic host” claim without pretending that transient/source-backed composition is already consumer-neutral.

It is a bounded proof tranche, not a full Stage 13 closure and not a full host-neutrality closure.

## Why This Is The Right First Move

`aoi-canary` already exists:

- registered in analyzer-v2 as consumer `aoi-canary`
- able to render a bounded AOI presenter surface
- thin by construction
- separate from the-critic

So the first cheap second-consumer proof is no longer hypothetical.

But the current canary state is still narrower than a Stage 13 Tier A proof:

- it currently uses presenter convenience endpoints directly from `src/App.tsx`
- it has no Host Contract v1 runtime or equivalent typed result-contract layer
- it is job-id driven rather than analyzer-owned discovery driven
- it has no `project_id` or `workflow_key` concept today, even though discovery requires both for the bounded AOI proof seam
- it only proves one pinned AOI result-backed rendering loop, not an analyzer-owned result-backed contract family

So Tier A should be framed honestly as:

- harden `aoi-canary` from a read-only presenter-page canary into a bounded second-consumer proof over analyzer-owned result-backed contracts

## Bounded Claim

The bounded claim for this tranche is:

- a second consumer can use analyzer-owned result discovery plus result-backed manifest/presentation contracts to render AOI results without rebuilding workflow-specific analytical intelligence locally

This tranche does **not** claim:

- transient compose in a second consumer
- source-backed readiness in a second consumer
- `route-task` / `plan-task` adoption in a second consumer
- generalized host-contract runtime extraction from the-critic into a shared package
- broad renderer support beyond what the AOI canary proof actually needs

## Current State

### What `aoi-canary` already has

- consumer definition:
  - `src/consumers/definitions/aoi-canary.json`
- a separate app repo:
  - `/home/evgeny/projects/aoi-canary`
- a bounded renderer host:
  - tab shell plus accordion, card grid, and raw-json renderer support
- live and artifact modes in:
  - `/home/evgeny/projects/aoi-canary/src/App.tsx`
- existing tests proving:
  - it fetches presenter payloads with `consumer_key=aoi-canary`
  - it renders the pinned AOI Neurath surface without unsupported-renderer fallback

### What `aoi-canary` does not yet have

- no analyzer-owned result discovery flow
- no `project_id` source for discovery
- no `workflow_key` threading for discovery
- no typed result-backed client layer
- no result-contract-first live state model
- no explicit mapping onto the result-backed contract families the draft roadmap wants to prove
- no Host Contract v1-style classification of what it is consuming
- no evidence yet that it can function as a second consumer over analyzer-owned result-backed contract law rather than just over presenter convenience endpoints

## Scope Decisions

### Decision 1: Tier A is result-backed only

This tranche should prove:

- `result_discovery`
- `result_manifest`
- `result_presentation`

It should not attempt:

- `result_refresh`
- `transient_compose_from_intent`
- `source_backed_transient_launch`
- source-backed readiness
- task-launch

Those belong to later tranches.

### Decision 2: Use analyzer `results` routes, not only presenter convenience routes

Tier A closure should require the canary to use analyzer-owned result-backed routes for the bounded surface set:

- `GET /v1/results/discovery`
- `GET /v1/results/by-job/{job_id}`
- `GET /v1/results/by-job/{job_id}/presentation`

Those three routes are the proof seam:

- discovery chooses the result
- manifest provides the result-contract truth
- presentation provides the render payload

It is not enough for Tier A to keep doing a page-centric fetch and merely add another supporting request.

The existing presenter debug fetches in the canary may remain as clearly secondary debug aids if needed:

- `GET /v1/presenter/trace/{job_id}`
- `GET /v1/presenter/status/{job_id}`

But they must not be the primary proof seam.

This is aligned with live analyzer behavior: the result contract still links to presenter debug/support seams internally, so presenter `trace/status` can remain secondary without weakening the result-backed proof.

### Decision 3: No shared runtime extraction in Tier A

Tier A should not try to extract the-critic’s Host Contract runtime into a cross-app shared package.

Instead:

- `aoi-canary` gets one small typed result-backed client layer of its own
- that client layer should be explicitly aligned to the analyzer-side contract families and the Stage 13 ledger
- any resulting drift/mismatch should be treated as evidence about the contract, not as a trigger for premature shared-package work

### Decision 4: Renderer coverage stays bounded

Tier A should only support the renderer/sub-renderer set actually needed for the bounded AOI result-backed proof surface.

Do not widen `aoi-canary` into a fully generic renderer host in this tranche.

If a real mismatch appears between:

- the pinned AOI result-backed surface
- and the canary’s current supported renderer set

then fix that mismatch narrowly and document it.

### Decision 5: No transient or lifecycle reopening

Tier A remains explicitly result-backed and read-only.

That means:

- no transient routes
- no transient persistence questions
- no draft/session/share semantics

Lifecycle stays deferred.

## Proposed Deliverables

### 0. Bounded project/workflow awareness for discovery

Tier A must add one bounded source of discovery scope to the canary:

- `project_id`
- `workflow_key`

For this tranche, env-driven or URL-param-driven configuration is sufficient. Tier A does **not** need a project-picker UI.

The bounded target should be:

- configured `project_id`
- configured `workflow_key` defaulting to the AOI proof workflow
- optional thinker filter only if the pinned AOI proof surface actually needs it

### 1. Small typed result-backed client and state-adapter layer in `aoi-canary`

Likely new module(s) in:

- `/home/evgeny/projects/aoi-canary/src/lib/`

Responsibilities:

- typed fetches for discovery, manifest, and presentation
- result-contract-first live state handling
- consumer key threading with `aoi-canary`
- narrow error handling
- no workflow-specific analytical inference

### 2. Discovery-driven live mode

`aoi-canary` live mode should stop being only manual-job-id driven.

It should gain one bounded analyzer-owned discovery path for the AOI proof surface, likely:

- project-scoped discovery
- AOI workflow filter
- optional thinker filter if needed for the pinned AOI experience

Tier A discovery UX should stay bounded:

- auto-select the latest matching AOI result for the configured `project_id` + `workflow_key`
- show discovery metadata in the debug panel
- keep manual `job_id` override only as a clearly secondary debug path

Tier A does **not** need a browsing/selection UI.

### 3. Manifest/presentation-driven render path

The canary should render through analyzer result-backed contract outputs rather than treating `presenter/page` as the primary live surface.

The bounded target is:

- discovery chooses a result
- result manifest confirms consumer-facing shape
- result presentation provides the render payload
- canary renders it with no workflow-specific semantic logic

The live state model should become result-contract-first rather than artifact/page-first. Tier A should not be able to mask a failed live result-contract path by silently falling back to artifact content.

### 4. Bounded proof artifact set

Save proof artifacts showing:

- a second consumer using analyzer-owned result discovery
- the same second consumer consuming result manifest and result presentation
- no local workflow-specific analytical reconstruction in the consumer
- any residual app-owned logic is shell/rendering continuity only

## Known Prerequisites And Risks

### Known prerequisite 1: `aoi-canary` is not yet on Host Contract infrastructure

This is real work, not a checkbox.

Today the canary:

- calls presenter endpoints directly
- does not classify those calls under the Stage 13 contract family model
- does not carry a typed result-backed contract client of its own
- does not carry discovery scope (`project_id`, `workflow_key`)

So Tier A is not a trivial route swap.

### Known prerequisite 2: renderer support is bounded

The canary currently supports only the bounded renderer set needed for its AOI surface.

That is acceptable for Tier A, but the scope must stay honest:

- this is a bounded AOI result-backed second-consumer proof
- not a proof that the canary can render every analyzer surface already

### Known prerequisite 3: proof data must actually be discoverable

`/v1/results/discovery` is project-scoped. So the proof depends on AOI results that are already attached to the configured `project_id` and discoverable under the chosen `workflow_key`.

If proof data is missing that attachment, Tier A needs a bounded data-prep step rather than silently falling back to manual `job_id` as the primary path.

### Known prerequisite 4: implementation size is medium, not trivial

This tranche likely involves:

- 3-5 new files in `aoi-canary`
- a significant refactor of `src/App.tsx`
- new result-contract types and tests
- live-mode state migration from page/artifact-first toward result-contract-first

This is best treated as one focused medium-sized implementation session, not a one-line wiring change.

### Known risk: accidental scope creep into Tier B

The most likely scope failure would be quietly pulling in:

- transient compose
- readiness
- or task-launch

Tier A should reject that.

## Test Plan

### `aoi-canary` tests

Add or extend tests for:

- typed result discovery client request shaping
- typed result manifest client request shaping
- typed result presentation client request shaping
- project/workflow discovery request shaping
- live-mode flow that prefers analyzer discovery over only manual job-id entry
- consumer-key correctness on all bounded result-backed requests
- no artifact fallback masking live result-contract failure
- manifest-aware UI behavior, not only successful page rendering
- proof that the canary still renders the bounded AOI surface without unsupported-renderer fallback

### Analyzer-side regression checks

Rerun focused analyzer checks relevant to the canary consumer contract, likely including:

- `tests/test_aoi_canary_contract.py`
- any nearby presenter/result contract tests touched by consumer compatibility assumptions

### Acceptance bar

Tier A should be considered complete only if:

- `aoi-canary` can discover a bounded AOI result via analyzer-owned `result_discovery`
- `aoi-canary` consumes analyzer-owned `result_manifest` as the source of result-contract truth
- `aoi-canary` renders through analyzer-owned `result_presentation`
- the proof does not depend on workflow-specific analytical logic living in the canary
- the proof path is discovery-first rather than manual-`job_id`-first
- live failures in the result-contract path are not masked by silent artifact fallback
- the tranche remains result-backed and read-only

## Out Of Scope

- any transient compose support in `aoi-canary`
- any change to `compose-from-intent` or `compose-from-source` consumer allowlists
- Host Contract runtime extraction into a shared cross-app package
- route-task / plan-task in `aoi-canary`
- source-backed readiness in `aoi-canary`
- lifecycle semantics
- broad renderer-host expansion

## Strategic Payoff

If this tranche lands cleanly, the program gets:

- an honest second-consumer proof for bounded result-backed surfaces
- a much cheaper and more concrete Stage 13 advance than trying to solve transient host-neutrality immediately
- better evidence about what the host contract still lacks before Tier B

It also keeps the larger sequence intact:

- Tier A second-consumer proof first
- AOI exemplar completion next
- then the de-AOI / de-`the-critic` transient-substrate tranche
- then Tier B stronger host-neutral proof

## Draft Judgment

This is the correct first scoping move if the draft roadmap is directionally right.

It is:

- bounded
- empirical
- cheap enough to be worth doing now
- strong enough to sharpen the next strategic choices

But it should be reviewed aggressively before implementation, because the main risk is underestimating how much contract work is still implicit inside the current canary.
