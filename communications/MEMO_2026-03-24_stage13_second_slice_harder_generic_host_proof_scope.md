# Memo: Stage 13 / Second Slice Harder Generic Host Proof Scope

Subtitle: Make Host Contract V1 Executable Across Transient And Result-Backed Surfaces Before Reopening Lifecycle

Date: 2026-03-24
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Prior Memo: `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md`
Stage 13 First-Slice Completion: `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_completion.md`
Stage 12 Completion: `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_completion.md`
Roadmap Vision: `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
Narrower Product Vision: `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

## Purpose

Define the next honest phase after the first Stage 13 host-contract slice.

This memo is about one specific remaining gap:

- Host Contract v1 now exists as typed law, but it is still only partly operational
- 8 of the 11 Host Contract v1 families already sit on the shared `boundedV2Client.ts` path, but the two compose families still sit outside that shared contract layer
- host-side surface selection is now documented, but it is not yet executable platform law
- the roadmap’s Stage 13 exit evidence still requires either:
  - a second consumer
  - or a materially harder generic-host proof without rebuilding intelligence locally

This memo argues that the next phase should be:

- a second Stage 13 slice
- not Stage 14 lifecycle
- not more bespoke AOI work
- not “we are done”

## Why This Is Still The Next Phase

The past 72 hours closed real downstream platform gaps in the right order:

1. Stage 11 made transient semantic page trees real
2. Stage 12 made served renderer law explicit and shared
3. Stage 13 first slice made the host contract explicit and adopted analyzer-owned readiness across bounded AOI and genealogy seams

That leaves one remaining host-contract problem before lifecycle:

- the contract is explicit in prose and types
- but it still is not the single executable path for all must-have v1 families

The live codebase shows this clearly.

What is already contract-driven:

- `webapp/src/lib/hostContractV1.ts`
- `webapp/src/lib/boundedV2Client.ts`
- `webapp/src/hooks/useBoundedV2Workspace.ts`
- `webapp/src/pages/AnalysisWorkspacePage.tsx`

What is still structurally outside that shared path:

- `webapp/src/lib/composeFromIntentClient.ts`
- `webapp/src/pages/AoiComposeFromIntentPage.tsx`
- specifically:
  - `composeFromIntent(...)`
  - `composeFromSource(...)`
- AOI source-backed transient launch remains a dedicated host proxy route in `the-critic/api/server.py`
- host-surface selection still lives mostly as page-local choice plus documentary rules, not one executable contract-driven resolver

What is already on the shared path and therefore **not** the main delta:

- run discovery
- run detail
- result discovery
- result manifest
- result presentation
- result refresh
- single-view fetch
- source-backed readiness
- cache snapshot warmup

So the thin-host thesis is stronger than it was.

But the harder generic-host proof is still not real enough to close Stage 13.

## Why This Is Not Stage 14 Yet

Stage 14 in the roadmap is lifecycle:

- launch
- revisit
- save
- share
- compare

That is explicitly a runtime-object decision about what a dynamic app/session is.

The code and memo trail do not support moving there yet.

What is still missing first:

- one executable Host Contract v1 path across both result-backed and transient families
- one real generic-host proof stronger than “current consumer, bounded page integrations”
- one clearer reduction in page-local host intelligence

Until that exists, Stage 14 would blur:

- host-contract proof
- transient/durable lifecycle law
- AOI proxy special cases

That would repeat the exact sequencing problem the last three stage memos avoided.

So lifecycle should remain deferred.

## Strategic Diagnosis

### What is already real

The current host contract is much stronger than it was 24 hours ago:

- Host Contract v1 is typed and authoritative
- a generated JSON ledger artifact exists
- result-backed run/result/readiness families are mostly consolidated onto `boundedV2Client.ts`
- genealogy blocked-mode readiness now has real `requestedMode` / `displayMode` law
- AOI source-backed launch has explicit `ready | blocked | outside_proof_slice` behavior

That means Stage 13 first slice was not just paperwork.

### What is not yet real

There is still no one executable host contract path that covers the full current must-have v1 surface set.

The repo still shows four residual structural facts:

1. the two compose families are not on the same shared adapter layer as the result-backed families
2. host-surface selection rules exist in the contract artifact, but pages still decide locally which surface family to invoke
3. AOI source-backed launch still crosses a dedicated host proxy seam that is only partly reflected in the shared client runtime
4. the current proof is still “the-critic consuming bounded AOI + genealogy seams,” not a harder generic-host demonstration

That is why Stage 13 is still partial in the roadmap.

## The Real Stage 13 Second-Slice Problem

The real problem is not:

- “launch a second app”
- “remove every `the-critic` constant from analyzer-v2”
- “reopen lifecycle”
- “adopt route-task and plan-task in the host”

It is:

- “make Host Contract v1 executable enough that the current consumer can prove materially harder generic-host behavior across both result-backed and transient seams without rebuilding intelligence locally”

That is the next durable platform seam.

## Recommended Shape

### Decision 1: keep this as Stage 13 second slice, not a new lifecycle stage

This work should explicitly be framed as:

- Stage 13 second slice
- possibly Stage 13-closing if the proof bar is met
- but not assumed Stage 13-closing up front

### Decision 2: make Host Contract v1 operational, not merely descriptive

The typed contract should stop being only:

- documentation
- tests
- generated JSON

and start becoming:

- the executable source of truth for shared host client/runtime behavior

At minimum, the contract runtime should drive:

- family ownership and route selection
- required-input validation for host launch helpers
- readiness capability checks
- surface-family grouping for current proof seams
- consumer-key threading rules, including the current `request_parameter` vs `structural_constant` asymmetry

The shared runtime should not duplicate contract facts in page code.

### Decision 3: unify transient families with the shared host adapter layer

The current split between:

- `boundedV2Client.ts`
- `composeFromIntentClient.ts`

is the clearest remaining sign that Host Contract v1 is not yet operational enough.

This next slice should move toward one shared host adapter layer that covers all current must-have v1 families, but the actual code delta should stay narrow.

The concrete transient gap is only:

- `transient_compose_from_intent`
- `source_backed_transient_launch`

That means the adapter unification work should primarily be:

- move `composeFromIntent(...)` onto the shared contract-aware adapter path
- move `composeFromSource(...)` onto the shared contract-aware adapter path

That does **not** require erasing the AOI host proxy.

It does require making the shared adapter layer honest about:

- which families are analyzer-direct
- which families are host-proxy
- which inputs are required for each
- which families carry `consumer_key` as a request parameter versus structural constant

Page-owned transient UX state should remain page-owned:

- draft sections
- example loading
- form validation messaging
- loading spinners
- response display and navigation

Adapter-owned responsibilities should become shared:

- contract-family dispatch
- URL construction
- request shaping
- required-input checks
- error normalization
- consumer-key threading

### Decision 4: make host-surface selection executable law

Stage 13 first slice documented host-side surface selection as a real concern.

The next slice should operationalize that fact.

For this bounded slice, the honest minimum is not a general resolver registry.

It is one typed lookup over the three current proof surfaces:

- AOI result-backed thematic experience
- AOI source-backed transient launch experience
- genealogy result-backed workspace experience

That typed lookup should drive:

- which contract families are used
- which identity fields are required
- whether readiness applies
- which navigation/launch path the page is allowed to take

This is still host-owned law in v1.

But it should no longer live as scattered page-local branching.

### Decision 5: target a materially harder generic-host proof inside the current consumer

The next proof should remain inside the current consumer.

A second consumer launch is not the smallest honest next move.

But the proof must be harder than Stage 13 first slice.

The right harder proof is:

- one shared contract-driven host adapter/runtime used across:
  - one result-backed generic workspace seam
  - one transient launch seam
- one executable host-surface selector rather than page-local family selection
- one proof that no analytical or renderer-law truth is re-derived in page code

That would be meaningfully stronger than:

- “we wrote down the contract and improved a few pages”

### Decision 6: make the deliverables concrete

This slice should only be considered implementation-ready if it is framed as a small set of concrete outputs:

1. one shared contract-aware host adapter path that now covers:
   - `composeFromIntent(...)`
   - `composeFromSource(...)`
2. one typed host-surface lookup over the three current proof surfaces
3. one runtime integration point where pages dispatch through that lookup instead of choosing families ad hoc
4. one saved proof artifact showing the shared runtime is used across:
   - one result-backed seam
   - one transient seam
5. one saved proof artifact showing the host is not re-deriving analyzer truth locally

### Decision 7: keep AOI source-backed launch explicitly host-bounded

This slice should still not pretend that AOI source-backed launch is already consumer-neutral.

The AOI proxy route in the-critic remains real because it owns:

- project-local identity continuity
- thinker-scoped source resolution
- host-local warmup/cache behavior

The next slice may wrap that seam in a stronger shared adapter/runtime.

It should not erase the distinction between:

- analyzer-owned readiness and compose truth
- host-owned source identity preparation

### Decision 8: keep analyzer API scope narrow

This next slice should be primarily host-side.

Analyzer-v2 changes should be limited to:

- documentation
- proof artifacts
- roadmap updates
- at most one small compatibility fix if implementation reveals a concrete mismatch

This is not the tranche to reopen:

- new presenter routes
- lifecycle contracts
- new orchestrator UX adoption

### Decision 9: preserve the first-slice regression boundary

The second slice should inherit the first-slice regression bar, not replace it with a narrower pack.

At minimum, the regression boundary should include the full first-slice focused host pack:

- `webapp/src/lib/hostContractV1.test.ts`
- `webapp/src/lib/boundedV2Client.test.ts`
- `webapp/src/hooks/useBoundedV2Workspace.test.tsx`
- `webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`
- `webapp/src/pages/AnxietyOfInfluencePages.test.tsx`
- `webapp/src/pages/AnalysisWorkspacePage.test.tsx`
- `webapp/src/pages/AnalysisWorkspacePage.integration.test.tsx`

And then extend it with the transient compose path tests touched by this slice, such as:

- `webapp/src/lib/composeFromIntentClient.test.ts`
- `webapp/src/pages/AoiComposeFromIntentPage.test.tsx`
- any isolation or routing tests that enforce transient/result-backed separation today

The first-slice host result was:

- `131 passed`

The second slice should state explicitly whether it preserves, widens, or replaces that boundary.

## Expected Proof Bar

The next slice should only count as successful if it lands all of the following:

1. Host Contract v1 remains code-authoritative and also becomes runtime-authoritative for the covered families
2. the current shared host adapter layer covers transient compose and source-backed transient launch, not just result-backed families
3. one executable host-surface selection runtime exists for the bounded proof seams instead of page-local family selection
4. one result-backed surface and one transient surface both run through that same contract-driven host runtime
5. saved proof demonstrates that intelligence still lives upstream:
   - analyzer owns result/readiness/compose truth
   - the host only owns project context, proxying, continuity, and navigation shell law

## Expected Ledger Impact

This phase should be scoped so that one of two honest outcomes is possible:

1. if the proof remains weaker than a true generic-host demonstration:
   - `Stage 13` stays `Partial`
2. if the proof is strong enough to satisfy the roadmap’s “materially harder generic-host proof” arm:
   - `Stage 13` can close

The memo should not assume closure in advance.

## What This Phase Is Not

This phase is not:

- Stage 14 lifecycle/session law
- a second-consumer launch
- analyzer-side removal of `TRANSIENT_COMPOSE_CONSUMER_KEY`
- route-task or plan-task host adoption
- host-neutral AOI source-backed launch
- a generic auth project

It is the missing operational host-contract tranche between:

- Stage 13 first-slice formalization
- and any honest lifecycle decision

## Final Judgment

There is clearly enough real work for a next phase.

The vision is not yet complete, even under the narrower UI-composition framing, because:

- the host contract is explicit but not yet fully operational
- transient host families are still outside the main shared contract runtime
- the harder generic-host proof is still missing

So the next honest phase should be:

- Stage 13 second slice
- focused on operational Host Contract v1 plus materially harder generic-host proof
- while keeping Stage 14 lifecycle deferred until that host proof is stronger
