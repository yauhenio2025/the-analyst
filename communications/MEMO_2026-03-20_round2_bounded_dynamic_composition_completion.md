# Memo: Round 2 / Bounded Dynamic Composition Completion

Date: 2026-03-20
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-19_round2_bounded_dynamic_composition_scope.md`

## Purpose

Record the actual outcome of **Round 2 / Bounded Dynamic Composition Entry**.

This note exists for one practical reason:

- close the documentary gap between the round-2 scope memo and the code now in the repo

It is not a new scope memo and it is not a broad proof record. It is the short completion/proof note the round-3 memo said should exist before the next stage becomes the operative implementation target.

## Bounded Claim Closed In Round 2

Round 2 proved one bounded thing:

- analyzer-v2 can emit a generated runtime genealogy hierarchy on the existing generic route, under explicit renderer/data contracts, and the existing thin Critic host can consume it without workflow-specific composition logic

The proof route used was:

- `/p/:projectId/analysis/intellectual_genealogy?composition_mode=bounded_dynamic_genealogy_v1`

The inspectable trace route used for diagnostics was:

- `/v1/presenter/trace/{job_id}?consumer_key=the-critic&composition_mode=bounded_dynamic_genealogy_v1`

## What Landed

### Analyzer-v2

Round 2 added a bounded runtime composition pass in:

- `src/presenter/bounded_dynamic_composition.py`

That pass generates exactly three runtime parent views:

1. `dynamic_genealogy_briefing`
2. `dynamic_genealogy_trajectory`
3. `dynamic_genealogy_horizon`

Those generated parents regroup exactly seven existing authored genealogy top-level surfaces:

- `genealogy_target_profile`
- `genealogy_relationship_landscape`
- `genealogy_text_profiling`
- `genealogy_idea_evolution`
- `genealogy_tactics`
- `genealogy_conditions`
- `genealogy_portrait`

Round 2 also threaded `composition_mode` through:

- result manifest lookup
- result presentation lookup
- refresh presentation
- presenter page
- presenter manifest
- presenter trace
- single-view lazy loading

The proof path fails closed on invalid runtime composition and keeps diagnostics visible in trace.

### The Critic

Round 2 kept the generic host generic.

`AnalysisWorkspacePage` now:

- restores proof-mode presentations through the same bounded-v2 contract
- treats the loaded presentation tree as tab authority
- supports generated top-level keys not present in authored view definitions
- skips local cache warming in proof mode
- preserves composition mode in single-view lazy loading

`V2TabContent` was also adjusted so regrouped authored branch views still expose their existing deep-dive affordances after they stop being top-level.

## Renderer Contracts Exercised

The generated runtime parents use a narrow, explicit contract:

- top-level renderer: `accordion`
- section `why_this_grouping` rendered with `prose_block`
- section `included_views` rendered with `mini_card_list`

The regrouped authored genealogy children keep their existing renderer contracts and descendants, including authored uses of:

- `accordion`
- `card_grid`
- `tab`
- `prose`

So the bounded claim is not "a whole new renderer library was introduced."

It is:

- one generated runtime hierarchy using explicit proof-only contracts can coexist with existing authored renderer contracts on the same host

## What Round 2 Proved

Round 2 now proves:

1. bounded runtime hierarchy generation can happen upstream in analyzer-v2
2. proof-mode composition can be requested explicitly through `composition_mode`
3. generated runtime payloads can be contract-validated and fail closed
4. the Critic generic workspace can consume the resulting presentation without new workflow-specific routing or rendering logic
5. composition-aware restore, refresh, trace, and lazy single-view loading can all stay inside the shared bounded-v2 path

## What Round 2 Did Not Prove

Round 2 did not prove:

1. generalized adaptive composition across multiple surfaces
2. content-sensitive family selection inside a single authored location
3. a new workflow key or app shell
4. replacement of the authored catalog
5. AOI dynamic composition

That next missing variable is exactly what round-3 is meant to isolate.

## Final Verification State

Focused analyzer-v2 verification:

- `PYTHONPATH=. pytest tests/test_presentation_api.py tests/test_analysis_product_contract.py tests/test_manifest_trace.py -q`
- Result: `75 passed`

Focused Critic verification:

- `CI=true npm test -- --watch=false src/lib/boundedV2Client.test.ts src/hooks/useBoundedV2Workspace.test.tsx src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx src/components/V2TabContent.test.tsx src/utils/presentationFreshness.test.ts`
- Result: `6 suites passed, 49 tests passed`

Focused webapp typecheck:

- `npx tsc --noEmit --pretty false --incremental false`
- Result: clean

Known non-blocking noise remained unchanged:

- backend deprecation warnings
- frontend `act(...)` warnings in focused hook tests
- Jest open-handle warning in the focused webapp suite

## Documentary Disposition

This tranche is now:

- code-complete
- focused-test-complete
- documentary-complete enough for round-3 planning and execution gating

This note is the round-2 completion/proof note the round-3 scope required.

## Next Program Move

The next meaningful stage is not more bounded hierarchy regrouping.

The next stage should isolate the next missing variable:

- content-sensitive surface-family selection on the same generic route

That is the subject of:

- `communications/MEMO_2026-03-20_round3_adaptive_surface_family_scope.md`
