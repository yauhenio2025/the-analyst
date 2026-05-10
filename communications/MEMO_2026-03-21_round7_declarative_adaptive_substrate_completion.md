# Memo: Round 7 / Declarative Adaptive Substrate Completion

Date: 2026-03-21
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md`
Proof Note: `communications/PROOF_2026-03-21_round7_declarative_adaptive_substrate.md`

## Purpose

Record the actual outcome of **Round 7 / Declarative Adaptive Substrate Proof**.

This note closes the documentary gap between:

- the round-7 scope memo
- the implemented round-7 code path
- the route-real proof evidence now saved in the repo

## Bounded Claim Closed In Round 7

Round 7 proved one bounded thing:

- one already-proven adaptive relationship pattern can be lifted into a repo-tracked declarative spec without giving up workflow-scoped authorization, fail-closed validation, or the existing adaptive trace grammar

The proof route used was:

- `/p/:projectId/analysis/intellectual_genealogy?composition_mode=declarative_relationship_surface_v1`

The adaptive target surface was:

- `genealogy_relationship_landscape`

The declarative families in scope were:

- `relationship_profile_dossier`
- `relationship_comparison_review`

The inspectable trace route used for diagnostics was:

- `/v1/presenter/trace/{job_id}?consumer_key=the-critic&composition_mode=declarative_relationship_surface_v1`

## What Landed

### Analyzer-v2

Round 7 added a small presenter-side declarative adaptive-spec package:

- `src/presenter/adaptive_specs/keys.py`
- `src/presenter/adaptive_specs/schemas.py`
- `src/presenter/adaptive_specs/registry.py`
- `src/presenter/adaptive_specs/definitions/declarative_relationship_surface_v1.json`

That package stays deliberately thin:

- JSON spec loading is repo-tracked
- Pydantic validation is fail-loud
- legal extractor/builder keys come from one neutral shared key module
- workflow authorization still comes from `_MODE_WORKFLOW_MAP`, not from the JSON spec

Round 7 also extended `src/presenter/bounded_dynamic_composition.py` with one new proof mode:

- `declarative_relationship_surface_v1`

That new mode does **not** introduce a general interpreter.

It reuses code-owned pieces:

- relationship signal extraction
- relationship payload builders
- rationale prose
- rejected-family prose
- runtime payload validation
- route error mapping
- trace-stage naming

The declarative lift in round 7 is narrow:

- choose dossier vs comparison from a validated JSON rule ladder
- then hand off to the same runtime builder/validator path the hardcoded mode already proved

Round 7 also kept the declared-family boundary honest:

- the declarative trace only rejects families declared in the spec
- `relationship_field_map` remains a hardcoded-only family outside the round-7 pilot

### Trace

Round 7 did not invent a new trace grammar.

It reused:

- `adaptive_surface_selection`

That matters because round 7 was meant to prove declarative equivalence, not build a second trace dialect.

For invalid accepted-mode spec failures, the guaranteed diagnostics surface remains:

- `composition_issues`

Stage-level adaptive details remain best-effort, which matches the current trace path.

### The Critic

Round 7 did not reopen the host boundary.

The Critic generic workspace only required one additional generic proof label:

- `declarative adaptive substrate proof`

No workflow-specific substrate rendering logic was added to the host.

## Proof Evidence Recorded

The route-real proof note is:

- `communications/PROOF_2026-03-21_round7_declarative_adaptive_substrate.md`

That proof note reused the round-3 documentary controls:

- `proof-round3-adaptive-dossier-final-1774002300`
- `proof-round3-adaptive-comparison-final-1774002300`

Those same two jobs were run through the new declarative token on the generic genealogy route.

Recorded live outcomes:

### Dossier Case

- Critic project:
  - `round3-proof-dossier-final-1774002300`
- selected family:
  - `relationship_profile_dossier`
- visible host surface:
  - `Relationship Dossier`

### Comparison Case

- Critic project:
  - `round3-proof-comparison-final-1774002300`
- selected family:
  - `relationship_comparison_review`
- visible host surface:
  - `Relationship Comparison Review`

Saved artifacts include:

- host screenshots
- extracted page text
- trace JSON for both declarative proof runs
- one control-equivalence JSON comparing hardcoded vs declarative trace outputs on the same jobs

All are stored under `communications/` and referenced in the proof note.

## Important Scope Caveat

Round 7 is not a full adaptive registry.

It intentionally does **not** prove:

- declarative `relationship_field_map`
- declarative suites
- declarative AOI substrate support
- arbitrary boolean expression trees
- spec-defined rationale prose
- spec-defined trace-stage naming

This tranche stayed bounded to a single-surface two-family equivalence pilot.

## What Round 7 Proved

Round 7 now proves:

1. `declarative_relationship_surface_v1` is a real composition-mode contract on the shared generic genealogy route
2. a repo-tracked declarative spec can drive family selection while extractor, builder, validator, and trace code stay in the enforcement layer
3. the declarative mode matches the hardcoded relationship control on the same round-3 route-real dossier/comparison jobs
4. accepted-mode spec failures are normalized into the existing bounded-composition validation path rather than creating a new HTTP/error dialect
5. the generic Critic host can restore the declarative proof result without workflow-specific UI branching

## What Round 7 Did Not Prove

Round 7 did not prove:

1. declarative suite selection
2. declarative AOI support
3. a many-workflow adaptive registry
4. a generalized expression interpreter
5. migration away from the hardcoded relationship control mode

## Final Verification State

Focused analyzer-v2 verification:

- `PYTHONPATH=. pytest tests/test_declarative_adaptive_specs.py tests/test_presentation_api.py tests/test_manifest_trace.py tests/test_analysis_product_contract.py -q`
- Result: `157 passed`

Focused Critic verification:

- `CI=true npm test -- --watch=false src/lib/boundedV2Client.test.ts src/hooks/useBoundedV2Workspace.test.tsx src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx`
- Result: `4 suites passed, 89 tests passed`

Focused webapp typecheck:

- `npx tsc --noEmit --pretty false --incremental false`
- Result: clean

Route-real proof evidence:

- recorded in `communications/PROOF_2026-03-21_round7_declarative_adaptive_substrate.md`
- artifacts saved under `communications/PROOF_round7_*`

Known non-blocking noise remained unchanged:

- backend deprecation warnings
- frontend `act(...)` warnings in focused hook tests

## Documentary Disposition

This tranche is now:

- code-complete
- focused-test-complete
- route-proof-complete
- documentary-complete

This note closes the round-7 documentary gate.

## Next Program Move

Round 7 closed the first bounded declarative single-surface variable.

That makes the next meaningful question narrower than a broad “registry” push:

- can the same declarative substrate discipline lift one already-proven adaptive **suite** without giving up fail-closed validation or the existing `adaptive_surface_suite_selection` trace grammar

So the next stage should likely scope:

- one bounded declarative suite pilot, probably on the already-proven genealogy relationship + conditions suite

It should **not** jump yet to:

- arbitrary workflow generation
- many-surface declarative composition
- spec-owned rationale prose
- spec-owned trace grammars
