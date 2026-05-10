# Memo: Round 5 / Cross-Workflow Adaptive AOI Theme Completion

Date: 2026-03-21
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md`
Execution Plan: `communications/PLAN_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_execution.md`
Proof Note: `communications/PROOF_2026-03-21_round5_cross_workflow_adaptive_aoi_theme.md`

## Purpose

Record the actual outcome of **Round 5 / Cross-Workflow Adaptive AOI Theme Proof**.

This note closes the documentary gap between:

- the round-5 scope memo
- the round-5 execution plan
- the route-real proof evidence now saved in the repo

## Bounded Claim Landed In Code

Round 5 landed the bounded implementation claim:

- analyzer-v2 can adapt one AOI child surface, `aoi_by_theme`, in place under `aoi_thematic_analysis`
- the adaptive-composition contract now widens beyond genealogy to a second serious workflow family
- the Critic generic `AnalysisWorkspacePage` remains generic in substance while consuming that AOI adaptive result through the shared bounded-v2 contract

The public proof route shape implemented is:

- `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=<id>&selected_source_thinker_name=<name>&composition_mode=adaptive_aoi_theme_surface_v1`

The inspectable trace route implemented is:

- `/v1/presenter/trace/{job_id}?consumer_key=the-critic&composition_mode=adaptive_aoi_theme_surface_v1`

## What Landed

### Analyzer-v2

Round 5 widened `src/presenter/bounded_dynamic_composition.py` and `src/presenter/decision_trace.py` so the adaptive runtime-composition path is no longer genealogy-locked.

The new AOI proof mode is:

- `adaptive_aoi_theme_surface_v1`

That mode:

- is accepted only for `anxiety_of_influence_thematic_single_thinker`
- rewrites `aoi_by_theme` in place as a child under `aoi_thematic_analysis`
- keeps the existing full-composition presenter/result/refresh/single-view/trace path
- reuses the existing `adaptive_surface_selection` trace grammar rather than inventing a workflow-specific AOI trace stage

The two AOI runtime families implemented are:

1. `aoi_theme_dossier`
2. `aoi_theme_comparison_review`

The selector is deterministic over the already-built `aoi_by_theme` payload:

- `_section_order`
- `_section_titles`
- per-theme `overview`
- per-theme `engagement`
- per-theme `key_claims`
- per-theme `philosophical_commitments`
- per-theme `argumentative_moves`
- per-theme `source_documents`
- per-theme `findings`

It does not reopen AOI engine contracts and it does not add a new inference pass.

### Late Contract Correction

One late implementation correction was necessary before round 5 could be considered code-complete:

- the first AOI dossier builder incorrectly emitted theme sections in ranked order rather than preserving authored `_section_order`

That is now corrected:

- selector-time metadata carries authored order and section titles
- `aoi_theme_dossier` restores `_section_order` and `_section_titles`
- dossier sections now render in authored theme order after `suite_summary`

That matters because the selector’s job is to choose a runtime family, not to reorder editorial structure.

### The Critic

Round 5 did not reopen the host boundary.

The Critic generic workspace only needed one additional generic proof label for the new AOI proof token:

- `adaptive AOI theme proof`

No workflow-specific adaptive selection logic was added to the host.

## Proof Evidence Recorded

The route-real proof note is:

- `communications/PROOF_2026-03-21_round5_cross_workflow_adaptive_aoi_theme.md`

That proof note records two final contrast fixtures:

### Dossier Case

- analyzer-v2 job:
  - `proof-round5-adaptive-aoi-dossier-final-1774100000`
- Critic project:
  - `round5-proof-dossier-final-1774100000`
- selected family:
  - `aoi_theme_dossier`
- visible host surface:
  - `Theme Dossier`

### Comparison Case

- analyzer-v2 job:
  - `proof-round5-adaptive-aoi-comparison-final-1774100000`
- Critic project:
  - `round5-proof-comparison-final-1774100000`
- selected family:
  - `aoi_theme_comparison_review`
- visible host surface:
  - `Theme Comparison Review`

Saved artifacts include:

- host screenshots
- extracted page text
- trace JSON for both proof fixtures

All are stored under `communications/` and referenced in the proof note.

## Important Fixture Caveat

Round 5 still used synthetic but route-real AOI fixtures.

Reason:

- the local workspace had `0` organically completed AOI jobs for `anxiety_of_influence_thematic_single_thinker`

So the final round-5 fixtures were created by:

- seeding explicit AOI route-real jobs
- preserving the real generic AOI route shape
- including the AOI surfaces required by the route and shared bounded-v2 restore path

That keeps the claim narrow and honest:

- routes were real
- restore/discovery was real
- trace was real
- the AOI adaptive contrast was explicit and inspectable

It does not claim that two organically completed AOI jobs were available locally at proof time.

## What Round 5 Proved

Round 5 now proves:

1. `adaptive_aoi_theme_surface_v1` is a real cross-workflow adaptive proof contract, independent of the genealogy proof modes
2. adaptive family selection now generalizes across at least two serious workflow families
3. `aoi_by_theme` can be adaptively rewritten in place under `aoi_thematic_analysis` without page-tree restructuring
4. the adaptive decision remains fail-closed and trace-inspectable through the reused `adaptive_surface_selection` stage
5. the shared bounded-v2 result/manifest/presentation/refresh/single-view contract still carries the whole proof path

## What Round 5 Did Not Prove

Round 5 did not prove:

1. coordinated multi-surface AOI suite behavior
2. adaptive suite behavior across workflows
3. bespoke `AoiV2ThematicPanel` proof readiness
4. a declarative adaptive registry
5. a third workflow beyond genealogy and AOI

## Final Verification State

Focused analyzer-v2 verification:

- `PYTHONPATH=. pytest tests/test_presentation_api.py tests/test_manifest_trace.py tests/test_analysis_product_contract.py -q`
- Result: `116 passed`

Focused Critic verification:

- `CI=true npm test -- --watch=false src/lib/boundedV2Client.test.ts src/hooks/useBoundedV2Workspace.test.tsx src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx`
- Result: `4 suites passed, 64 tests passed`

Focused webapp typecheck:

- `npx tsc --noEmit --pretty false --incremental false`
- Result: clean

Known non-blocking noise remained unchanged:

- backend deprecation warnings
- frontend `act(...)` warnings in focused hook tests

## Documentary Disposition

This tranche is now:

- code-complete
- focused-test-complete
- route-proof-complete
- documentary-complete

This note closes the round-5 documentary gate.

## Next Program Move

Round 5 closed the “single adaptive surface outside genealogy” variable.

That makes one thing lower-value than it was before:

- another single-surface AOI proof

The next meaningful variable after round 5 became:

- whether coordinated adaptive suite behavior also generalizes across workflows, rather than staying a genealogy-only multi-surface success story

That next move is now recorded separately as round 6.
