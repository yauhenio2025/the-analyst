# Memo: Stage 7 / AOI Source-To-Composition Bridge Completion

Date: 2026-03-23  
Program: Dynamic Bespoke Apps Platformization  
Scope Memo: `communications/MEMO_2026-03-23_stage7_planner_to_presentation_bridge_scope.md`  
Proof Memo: `communications/PROOF_2026-03-23_stage7_aoi_source_to_composition_bridge.md`

## Result

Stage 7 implementation is complete for the bounded AOI slice that was actually scoped:

- AOI source-to-composition bridge behind `compose-from-source`

This memo closes the code and focused verification record for that slice.

It does **not** claim that the full roadmap stage named:

- `STAGE 7: FORMALIZE THE PLANNER-TO-PRESENTATION BRIDGE`

is completely finished.

The honest program state is:

- Stage 7 slice implemented
- focused verification complete
- roadmap Stage 7 advanced to partial
- broader task-intake, workflow-routing, engine-planning, and page-law integration still open

## Bounded Claim Landed

The bounded Stage 7 claim was:

- analyzer-v2 should stop bridging AOI source-backed transient composition through hardcoded inline `profile -> sections` assembly, and instead introduce an analyzer-owned bridge that resolves a formal AOI source catalog, selects source families explicitly, materializes deterministic sections, and preserves the external route contract

That claim is now true in code.

## What Landed

### Analyzer-side bridge substrate

`src/presenter/composition_source_bridge.py` now owns the AOI source-to-composition bridge.

It formalizes:

- `CompositionSourceCandidate`
- `CompositionSourceCatalog`
- `CompositionSourceSelection`
- `CompositionMaterializedSection`
- `CompositionSourceBridgeResult`

The bridge explicitly performs:

1. eager source catalog resolution
2. preset-relative source selection
3. deterministic section materialization

### `compose-from-source-v2`

`src/presenter/compose_from_intent.py` now routes source-backed compose through the bridge and stamps:

- `compose-from-source-v2`

The source-backed trace now begins with:

- `source_catalog_resolution`
- `source_selection`
- `section_materialization`

### Hardening that landed before close-out

The Stage 7 implementation also closed two review-discovered seams before completion:

1. `objective_key` now falls back through merged run/request-snapshot plan data before the AOI workflow default when effective plan context is missing
2. the thematic-report candidate now distinguishes:
   - phase-output metadata lookup failure
   - normalized report-payload failure/success

### What did not change

Stage 7 intentionally did **not** change:

- the public `compose-from-source` request shape
- the public `ComposeFromIntentResponse` success shape
- the-critic runtime behavior
- AOI hot-path launch UX
- cross-workflow composition
- engine planning
- task intake
- richer page-law consumption of planner output

## Verification

Focused verification completed:

- `python -m py_compile src/presenter/composition_source_bridge.py src/presenter/compose_from_intent.py tests/test_composition_source_bridge.py tests/test_compose_from_intent.py`
  - result: clean
- `PYTHONPATH=. pytest tests/test_composition_source_bridge.py tests/test_compose_from_intent.py -q`
  - result: `20 passed, 2 warnings`
- `cd /home/evgeny/projects/the-critic/webapp && CI=true npm test -- --watch=false src/pages/AoiComposeFromIntentPage.test.tsx`
  - result: `15 passed`

## What Stage 7 Now Proves

Stage 7 now proves:

1. analyzer-v2 can represent composition-eligible AOI sources as a formal internal catalog
2. analyzer-v2 can separate source selection from section materialization
3. `compose-from-source` no longer needs inline hardcoded AOI section assembly to remain operational
4. plan/objective context can enrich the bridge trace without overruling live source truth
5. the source-backed transient path can evolve internally without widening the the-critic runtime contract

## What Stage 7 Does Not Yet Prove

Stage 7 does **not** yet prove:

1. composition-facing task intake
2. workflow routing without host-chosen workflow keys
3. planner-driven source selection beyond bounded AOI preset selectors
4. engine/chain-plan handoff into composition
5. cross-workflow source-backed composition
6. planner-driven page law

Those are the next stages.

## Program Position After Stage 7

The important strategic shift is now concrete:

- planner-to-presentation bridging is no longer purely conceptual
- it now has one real analyzer-owned slice in code

The next program move should therefore not be:

- more AOI/the-critic adoption glue

It should be:

- composition-facing task intake and workflow routing on top of the bridge substrate that now exists
