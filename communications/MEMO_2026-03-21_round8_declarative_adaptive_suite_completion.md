# Memo: Round 8 / Declarative Adaptive Suite Completion

Date: 2026-03-21
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-21_round8_declarative_adaptive_suite_scope.md`
Proof Note: `communications/PROOF_2026-03-21_round8_declarative_adaptive_suite.md`

## Purpose

Record the actual outcome of **Round 8 / Declarative Adaptive Suite Proof**.

This note closes the documentary gap between:

- the round-8 scope memo
- the implemented round-8 code path
- the route-real proof evidence now saved in the repo

## Bounded Claim Closed In Round 8

Round 8 proved one bounded thing:

- a repo-tracked declarative suite spec can coordinate the already-proven genealogy relationship + conditions adaptive suite without giving up workflow-scoped authorization, fail-closed validation, or the existing `adaptive_surface_suite_selection` trace grammar

The proof route used was:

- `/p/:projectId/analysis/intellectual_genealogy?composition_mode=declarative_genealogy_relationship_conditions_suite_v1`

The adaptive target surfaces were:

- `genealogy_relationship_landscape`
- `genealogy_conditions`

The hardcoded control remained:

- `adaptive_genealogy_relationship_conditions_v1`

The inspectable trace route used for diagnostics was:

- `/v1/presenter/trace/{job_id}?consumer_key=the-critic&composition_mode=declarative_genealogy_relationship_conditions_suite_v1`

## What Landed

### Analyzer-v2

Round 8 extended the round-7 declarative substrate with a separate suite-spec path instead of widening the single-surface contract.

That landed as:

- suite-specific spec directory:
  - `src/presenter/adaptive_specs/suite_definitions/`
- suite-specific registry APIs:
  - `get_adaptive_suite_composition_spec()`
  - `load_all_adaptive_suite_specs()`
- one new suite spec:
  - `src/presenter/adaptive_specs/suite_definitions/declarative_genealogy_relationship_conditions_suite_v1.json`

The round-7 single-surface contract remained intact:

- `get_adaptive_composition_spec()`
- `load_all_adaptive_specs()`

Round 8 also kept the schema boundary honest:

- generic suite schema invariants stay generic
- the round-8 exact two-surface genealogy shape is enforced in a dedicated suite-runtime validation path
- suite specs live in their own directory so single-surface discovery stays unambiguous

The new declarative suite token added to the presenter runtime is:

- `declarative_genealogy_relationship_conditions_suite_v1`

That token does **not** introduce a general interpreter.

It still reuses code-owned pieces:

- workflow authorization from `_MODE_WORKFLOW_MAP`
- relationship signal extraction
- relationship builders
- relationship rationale/rejection prose
- conditions signal extraction
- conditions builders
- conditions rationale/rejection prose
- runtime payload validation
- route error mapping
- suite trace-stage naming

Round 8 also closed one real structural seam in the conditions path.

The existing conditions selector was split into:

- code-owned extraction
- family choice
- code-owned hydration

That means hardcoded and declarative suite paths now share:

- the same source-payload normalization
- the same derived conditions metrics
- the same rationale/rejected-family prose

The declarative difference is narrow:

- the family choice step is driven by the repo-tracked suite spec

Round 8 also fixed two infrastructure seams while widening the substrate:

1. accepted-mode suite-spec failures now attribute to a fixed synthetic issue target:
   - `__suite_spec__:declarative_genealogy_relationship_conditions_suite_v1`
2. the older single-surface spec-loader helper no longer hardcodes the relationship view key when reporting accepted-mode spec failures

### Trace

Round 8 did not invent a new suite trace dialect.

It reused:

- `adaptive_surface_suite_selection`

That matters because round 8 was meant to prove bounded declarative suite equivalence, not create a separate trace contract for declarative suites.

For invalid accepted-mode suite-spec failures, the guaranteed diagnostics surface remains:

- `composition_issues`

Stage-level suite details remain best-effort, which matches the existing trace path.

### The Critic

Round 8 did not reopen the host boundary.

The Critic generic workspace only required one additional generic proof label:

- `declarative adaptive suite proof`

No genealogy-specific suite rendering logic was added to the host.

## Proof Evidence Recorded

The route-real proof note is:

- `communications/PROOF_2026-03-21_round8_declarative_adaptive_suite.md`

That proof note reused the round-4 documentary controls directly:

- `proof-round4-adaptive-balance-final-1774012011`
- `proof-round4-adaptive-matrix-final-1774012011`

Those same two jobs were run through the new declarative suite token on the shared genealogy route.

Recorded live outcomes:

### Balance Case

- Critic project:
  - `round4-proof-balance-final-1774012011`
- selected surfaces:
  - `genealogy_relationship_landscape -> relationship_profile_dossier`
  - `genealogy_conditions -> conditions_balance_sheet`
- visible host surfaces:
  - `Relationship Dossier`
  - `Conditions Balance Sheet`

### Matrix Case

- Critic project:
  - `round4-proof-matrix-final-1774012011`
- selected surfaces:
  - `genealogy_relationship_landscape -> relationship_comparison_review`
  - `genealogy_conditions -> conditions_path_dependency_matrix`
- visible host surfaces:
  - `Relationship Comparison Review`
  - `Conditions Path-Dependency Matrix`

Saved artifacts include:

- host screenshots
- extracted page text
- trace JSON for both declarative proof runs
- one control-equivalence JSON comparing hardcoded vs declarative trace outputs on the same jobs

All are stored under `communications/` and referenced in the proof note.

## Important Scope Caveat

Round 8 is not a broad declarative suite registry.

It intentionally does **not** prove:

- declarative `relationship_field_map`
- declarative AOI suites
- declarative multi-workflow suite support
- spec-defined rationale prose
- spec-defined rejected-family prose
- spec-defined trace-stage naming
- arbitrary expression/interpreter expansion

This tranche stayed bounded to a two-surface suite equivalence pilot on the two documented round-4 control cases.

## What Round 8 Proved

Round 8 now proves:

1. `declarative_genealogy_relationship_conditions_suite_v1` is a real composition-mode contract on the shared generic genealogy route
2. a repo-tracked declarative suite spec can coordinate two already-proven adaptive target surfaces while extractor, builder, validator, and trace code stay in the enforcement layer
3. the declarative suite candidate matches the hardcoded round-4 control on the same route-real balance and matrix jobs for:
   - selected family
   - signal summary
   - rationale text
4. accepted-mode suite-spec failures are normalized into the existing bounded-composition validation path rather than creating a new HTTP/error dialect
5. the generic Critic host can restore the declarative suite proof result without workflow-specific UI branching

## What Round 8 Did Not Prove

Round 8 did not prove:

1. full semantic replacement of every hardcoded genealogy suite branch
2. declarative `relationship_field_map`
3. declarative cross-workflow suite support
4. a many-workflow adaptive registry
5. a generalized expression interpreter
6. migration away from the hardcoded suite control mode

## Final Verification State

Focused analyzer-v2 verification:

- `PYTHONPATH=. pytest tests/test_declarative_adaptive_specs.py tests/test_presentation_api.py tests/test_manifest_trace.py tests/test_analysis_product_contract.py -q`
- Result: `185 passed, 12 warnings`

Focused Critic verification:

- `CI=true npm test -- --watch=false src/lib/boundedV2Client.test.ts src/hooks/useBoundedV2Workspace.test.tsx src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx`
- Result: `4 suites passed, 99 tests passed`

Focused webapp typecheck:

- `npx tsc --noEmit --pretty false --incremental false`
- Result: clean

Route-real proof evidence:

- recorded in `communications/PROOF_2026-03-21_round8_declarative_adaptive_suite.md`
- artifacts saved under `communications/PROOF_round8_*`

Known non-blocking noise remained unchanged:

- backend deprecation warnings
- frontend `act(...)` warnings in focused hook tests

## Independent Verification

Round 8 was also independently re-checked after implementation.

That second-pass verification confirmed:

- the suite registry, schema, runtime wiring, trace wiring, and Critic label change all matched the agreed plan
- the focused analyzer-v2 suite still passed at:
  - `185 passed, 12 warnings`
- the focused Critic suite still passed at:
  - `4 suites passed, 99 tests passed`
- the webapp typecheck still completed cleanly

No implementation mismatches were found in the reviewed round-8 paths.

The only explicit verification caveat remained:

- the independent re-check relied on the saved live route-proof artifacts rather than re-running the browser capture itself

That caveat does not reopen the round-8 proof claim because the saved artifacts, trace JSON, and focused automated checks were internally consistent.

## Documentary Disposition

This tranche is now:

- code-complete
- focused-test-complete
- route-proof-complete
- documentary-complete

This note closes the round-8 documentary gate.

## Program Position After Round 8

Round 8 closes the final high-value proof question in the current bounded adaptive/declarative ladder:

- single-surface adaptive family selection
- multi-surface adaptive suite selection
- cross-workflow adaptive surface and suite behavior
- bounded declarative single-surface selection
- bounded declarative suite coordination

That means the program should now pivot away from adding more proof tokens and toward cashing in the ladder on a real platform gap.

The next move should be:

- renderer contract validation and stronger renderer-facing platform law

It should not be:

- another workflow-specific proof token
- another hardcoded adaptive branch
- or another bounded declarative variant unless round-8 implementation exposed a genuine substrate flaw
