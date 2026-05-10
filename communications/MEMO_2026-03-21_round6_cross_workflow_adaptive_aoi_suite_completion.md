# Memo: Round 6 / Cross-Workflow Adaptive AOI Suite Completion

Date: 2026-03-21
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_scope.md`
Proof Note: `communications/PROOF_2026-03-21_round6_cross_workflow_adaptive_aoi_suite.md`

## Purpose

Record the actual outcome of **Round 6 / Cross-Workflow Adaptive AOI Suite Proof**.

This note closes the documentary gap between:

- the round-6 scope memo
- the implemented round-6 code path
- the route-real proof evidence now saved in the repo

## Bounded Claim Closed In Round 6

Round 6 proved one bounded thing:

- analyzer-v2 can coordinate deterministic runtime family selection for two AOI child surfaces on the same generic page while the Critic host remains generic in substance

The proof route used was:

- `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=<id>&selected_source_thinker_name=<name>&composition_mode=adaptive_aoi_theme_report_suite_v1`

The adaptive target surfaces were:

- `aoi_by_theme`
- `aoi_thematic_report`

The inspectable trace route used for diagnostics was:

- `/v1/presenter/trace/{job_id}?consumer_key=the-critic&composition_mode=adaptive_aoi_theme_report_suite_v1`

## What Landed

### Analyzer-v2

Round 6 extended `src/presenter/bounded_dynamic_composition.py` and `src/presenter/decision_trace.py` with one suite-mode AOI proof branch:

- `adaptive_aoi_theme_report_suite_v1`

That suite mode coordinates:

1. the existing round-5 `aoi_by_theme` selector
2. a new `aoi_thematic_report` selector that reads top-level `structured_data`

The report selector stays deterministic and fail-closed:

- it validates the structural shape of `key_divergences` and `sin_distribution`
- it does not parse free prose into a new inference layer
- it normalizes optional row fields rather than weakening the gate

Round 6 also added two concrete runtime report families:

1. `aoi_report_briefing`
2. `aoi_report_evidence_review`

Those are real renderer-level contracts:

- briefing uses `accordion`
- evidence review uses the existing multi-table `table` contract

Round 6 also widened trace inspectability through:

- `adaptive_surface_suite_selection`

That stage now records both AOI child-surface decisions together rather than reporting only the theme rewrite.

### The Critic

Round 6 did not reopen the host boundary.

The Critic generic workspace only required one additional generic proof label for the new AOI suite token:

- `adaptive AOI suite proof`

No AOI-specific adaptive selection logic was added to the host.

## Proof Evidence Recorded

The route-real proof note is:

- `communications/PROOF_2026-03-21_round6_cross_workflow_adaptive_aoi_suite.md`

That proof note records two final contrast fixtures:

### Dossier + Briefing Case

- analyzer-v2 job:
  - `proof-round5-adaptive-aoi-dossier-final-1774100000`
- Critic project:
  - `round5-proof-dossier-final-1774100000`
- selected theme family:
  - `aoi_theme_dossier`
- selected report family:
  - `aoi_report_briefing`
- visible host surfaces:
  - `Theme Dossier`
  - `Report Briefing`

### Comparison + Evidence Review Case

- analyzer-v2 job:
  - `proof-round5-adaptive-aoi-comparison-final-1774100000`
- Critic project:
  - `round5-proof-comparison-final-1774100000`
- selected theme family:
  - `aoi_theme_comparison_review`
- selected report family:
  - `aoi_report_evidence_review`
- visible host surfaces:
  - `Theme Comparison Review`
  - `Report Evidence Review`

Saved artifacts include:

- host screenshots
- extracted page text
- trace JSON for both proof fixtures

All are stored under `communications/` and referenced in the proof note.

## Important Fixture Caveat

Round 6 still used synthetic but route-real AOI fixtures.

Reason:

- the local workspace still had no organically completed AOI jobs for this workflow
- round 5 had already seeded two route-real AOI proof fixtures with the surface set needed by round 6

So the final round-6 proof reused those same two fixtures rather than inventing a second synthetic AOI pair.

That keeps the claim narrow and honest:

- routes were real
- restore/discovery was real
- trace was real
- the coordinated AOI child-surface contrast was explicit and inspectable

It does not claim that two organically completed AOI jobs with ready-made phase-4 report payloads were available locally at proof time.

## What Round 6 Proved

Round 6 now proves:

1. `adaptive_aoi_theme_report_suite_v1` is a real cross-workflow AOI suite contract, independent of rounds 2 through 5
2. coordinated adaptive suite behavior now generalizes outside genealogy, not just single-surface adaptive family selection
3. analyzer-v2 can coordinate two AOI child-surface rewrites under one shared `aoi_thematic_analysis` parent
4. the generic AOI route can show materially different theme and report surfaces under one suite token while the host stays generic
5. the suite decision remains fail-closed and trace-inspectable through `adaptive_surface_suite_selection`

## What Round 6 Did Not Prove

Round 6 did not prove:

1. a declarative adaptive registry
2. proof-mode stacking
3. a third workflow beyond genealogy and AOI
4. bespoke `AoiV2ThematicPanel` proof behavior
5. whole-page adaptive generation

## Final Verification State

Focused analyzer-v2 verification:

- `PYTHONPATH=. pytest tests/test_presentation_api.py tests/test_manifest_trace.py tests/test_analysis_product_contract.py -q`
- Result: `129 passed`

Focused Critic verification:

- `CI=true npm test -- --watch=false src/lib/boundedV2Client.test.ts src/hooks/useBoundedV2Workspace.test.tsx src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx`
- Result: `4 suites passed, 73 tests passed`

Focused webapp typecheck:

- `npx tsc --noEmit --pretty false --incremental false`
- Result: clean

Route-real proof evidence:

- recorded in `communications/PROOF_2026-03-21_round6_cross_workflow_adaptive_aoi_suite.md`
- artifacts saved under `communications/PROOF_round6_*`

Known non-blocking noise remained unchanged:

- backend deprecation warnings
- frontend `act(...)` warnings in focused hook tests

## Documentary Disposition

This tranche is now:

- code-complete
- focused-test-complete
- route-proof-complete
- documentary-complete

This note closes the round-6 documentary gate.

## Next Program Move

Round 6 closed the “coordinated adaptive suite outside genealogy” variable.

That makes one thing lower-value than it was before:

- another hardcoded workflow-specific proof branch that only adds one more surface family

The next meaningful variable is likely no longer:

- whether adaptive suite behavior can work on a second workflow at all

The next meaningful variable is more likely:

- whether the now-proven adaptive family and suite patterns should be lifted into a small declarative substrate rather than continuing as one-off hardcoded mode branches

So the next stage should probably scope:

- a bounded declarative adaptive-substrate proof, not another AOI-only expansion
