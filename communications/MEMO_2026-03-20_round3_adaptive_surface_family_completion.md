# Memo: Round 3 / Adaptive Surface Family Completion

Date: 2026-03-20
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-20_round3_adaptive_surface_family_scope.md`
Execution Plan: `communications/MEMO_2026-03-20_round3_adaptive_surface_family_execution_plan.md`
Proof Note: `communications/PROOF_2026-03-20_round3_adaptive_surface_family.md`

## Purpose

Record the actual outcome of **Round 3 / Adaptive Surface Family Proof**.

This note closes the documentary gap between:

- the round-3 scope memo
- the ratify-and-close execution plan
- the route-real proof evidence now saved in the repo

It is not a new scope memo and it is not a broad roadmap note.

## Bounded Claim Closed In Round 3

Round 3 proved one bounded thing:

- analyzer-v2 can deterministically rewrite one authored genealogy surface into different validated runtime surface families based on already-transformed structured signals, while the same generic Critic host restores the result without workflow-specific host logic

The proof route used was:

- `/p/:projectId/analysis/intellectual_genealogy?composition_mode=adaptive_relationship_surface_v1`

The adaptive target surface was:

- `genealogy_relationship_landscape`

The inspectable trace route used for diagnostics was:

- `/v1/presenter/trace/{job_id}?consumer_key=the-critic&composition_mode=adaptive_relationship_surface_v1`

## What Landed

### Analyzer-v2

Round 3 added one proof-mode adaptive selector in:

- `src/presenter/bounded_dynamic_composition.py`

That selector keeps the proof bounded to one authored location and chooses among exactly three runtime families:

1. `relationship_profile_dossier`
2. `relationship_comparison_review`
3. `relationship_field_map`

Those families are concrete renderer-level contracts, not editorial labels only:

- dossier uses `accordion`
- comparison review uses `table`
- field map uses `accordion`

Round 3 also made the choice inspectable through:

- `adaptive_surface_selection` trace output in `src/presenter/decision_trace.py`

The proof path remains fail-closed on invalid adaptive runtime payloads and keeps diagnostics visible through trace.

### The Critic

Round 3 did not reopen the generic host boundary.

The Critic generic workspace already had proof-mode composition plumbing from round 2. Round 3 only had to prove that the same generic restore path could consume:

- `Relationship Dossier`
- `Relationship Comparison Review`
- `Relationship Field Map`

under the same route shape and the same shared bounded-v2 contract.

## Proof Evidence Recorded

The route-real proof note is:

- `communications/PROOF_2026-03-20_round3_adaptive_surface_family.md`

That proof note records two final contrast fixtures:

### Dossier Case

- analyzer-v2 job:
  - `proof-round3-adaptive-dossier-final-1774002300`
- Critic project:
  - `round3-proof-dossier-final-1774002300`
- selected family:
  - `relationship_profile_dossier`
- visible host surface:
  - `Relationship Dossier`

### Comparison Case

- analyzer-v2 job:
  - `proof-round3-adaptive-comparison-final-1774002300`
- Critic project:
  - `round3-proof-comparison-final-1774002300`
- selected family:
  - `relationship_comparison_review`
- visible host surface:
  - `Relationship Comparison Review`

Saved artifacts include:

- host screenshots
- extracted page text
- trace JSON for both proof fixtures

All are stored under `communications/` and referenced in the proof note.

## Important Fixture Caveat

The proof used two synthetic but route-real fixtures cloned from the existing imported Varoufakis genealogy job:

- `job-import-3e8cb4ed`

Reason:

- the local workspace only had one concrete completed genealogy corpus
- that imported source job still carried the legacy collapsed `work_key='target'` phase-1.5 relationship-card shape

Only the per-work relationship-card cache used by the adaptive selector was replaced for contrast.

So the proof claim remains narrow and honest:

- routes were real
- restore was real
- trace was real
- the adaptive contrast was deterministic and inspectable

It does not claim that two organically distinct production genealogy corpora were available locally at proof time.

## What Round 3 Proved

Round 3 now proves:

1. `adaptive_relationship_surface_v1` is a real proof-mode contract, independent of round-2 regrouping mode
2. analyzer-v2 can select different runtime surface families from structured relationship-card signals without a new inference pass
3. the same generic Critic host route can restore those different contracts without workflow-specific branching
4. the adaptive choice is inspectable in trace with selected family, rejected families, signal summary, and rationale
5. proof-mode result/manifest/presentation/refresh/single-view paths can all stay inside the shared bounded-v2 contract

## What Round 3 Did Not Prove

Round 3 did not prove:

1. coordinated adaptive selection across more than one surface on the same page
2. workflow-wide adaptive composition
3. generalized adaptive composition across multiple workflows
4. a new host shell or workflow-specific Critic page
5. whole-page freeform generation

That next missing variable is exactly what round 4 should isolate.

## Final Verification State

Focused analyzer-v2 verification:

- `PYTHONPATH=. pytest tests/test_presentation_api.py tests/test_manifest_trace.py tests/test_analysis_product_contract.py -q`
- Result: `88 passed`

Focused Critic verification:

- `CI=true npm test -- --watch=false src/lib/boundedV2Client.test.ts src/hooks/useBoundedV2Workspace.test.tsx src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx src/components/V2TabContent.test.tsx src/utils/presentationFreshness.test.ts`
- Result: `6 suites passed, 58 tests passed`

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
- route-proof-complete
- documentary-complete enough for round-4 scoping

This note closes the round-3 documentary gate.

## Next Program Move

The next meaningful stage is not more AOI work, more host plumbing, or another single-surface proof.

The next stage should isolate the next missing variable:

- whether analyzer-v2 can coordinate adaptive family selection across more than one genealogy surface on the same generic route

That is the subject of:

- `communications/MEMO_2026-03-20_round4_adaptive_surface_suite_scope.md`
