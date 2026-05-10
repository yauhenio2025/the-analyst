# Audit: Round 6 / Cross-Workflow Adaptive AOI Suite Scope

Date: 2026-03-21
Memo under review: `communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_scope.md`

## Verdict

Approve after narrowing.

`adaptive_aoi_theme_report_suite_v1` is the right bounded next proof shape if the second surface remains `aoi_thematic_report` and Gate B passes on the exact proof jobs or synthetic-but-route-real fixtures. Keep `aoi_thematic_report` as the preferred second surface. Do not promote `aoi_by_sin_type` to the primary target yet.

The main revision needed is contract precision, not strategic direction. `aoi_report_briefing` is close to a validator-ready runtime family. `aoi_report_evidence_review` is not yet concrete enough as written, because the live AOI report seam is still a keyed report-sections object, while the proposed evidence family requires a new multi-table container and new derived row fields (`src/aoi/contract.py:82-87`, `src/aoi/contract.py:329-354`, `src/renderers/definitions/table.json:7-27`).

Round 6 should remain scoped-but-gated. The round-5 documentary gate is real and currently still red (`communications/MEMO_2026-03-21_round5_cross_workflow_adaptive_aoi_theme_completion.md:7`, `communications/MEMO_2026-03-21_round5_cross_workflow_adaptive_aoi_theme_completion.md:113-160`).

## Findings

### 1. `aoi_thematic_report` is still the right second surface, but the memo should narrow the report-family contract before implementation

The memo’s strategic call is sound.

- `aoi_thematic_report` is already a real AOI child surface under `aoi_thematic_analysis`, sourced from phase 4 rather than the phase-3 findings regrouping (`src/views/definitions/aoi_thematic_report.json:62-86`, `src/views/definitions/aoi_thematic_analysis.json:1-42`).
- The normalized AOI contract already emits a stable top-level report object with `summary`, `engagement_pattern`, `key_divergences`, `sin_distribution`, and `reading_implications` (`src/aoi/contract.py:82-87`, `src/aoi/contract.py:329-354`).
- That makes it a stronger next proof than `aoi_by_sin_type`, which is another phase-3 regrouping over the same findings family already exercised by `aoi_by_theme` (`src/views/definitions/aoi_by_sin_type.json:20-44`, `src/aoi/contract.py:418-430`).

But the memo currently bundles two different levels of difficulty into one “report” target.

- `aoi_report_briefing` is close to the current seam. It keeps an `accordion` top-level renderer and extends the same keyed-object shape the live report surface already uses (`communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_scope.md:303-336`, `src/views/definitions/aoi_thematic_report.json:9-60`, `src/renderers/definitions/accordion.json:7-18`).
- `aoi_report_evidence_review` is not just a second family. It is a real transform from a keyed report object into a `table` multi-table container with new snapshot rows and derived excerpt fields (`communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_scope.md:338-377`, `src/renderers/definitions/table.json:7-27`).

The memo should therefore narrow the contract explicitly:

- define the exact `structured_data = {"tables": [...]}` shape
- define the exact per-table `columns` and `rows`
- define how `summary_excerpt`, `engagement_excerpt`, and `implications_excerpt` are derived from the current report payload
- define empty-value behavior so runtime validation fails closed instead of relying on ad hoc coercion

Without that tightening, the second surface is still the right one, but the second family is not yet implementation-ready.

### 2. The new proof token is the right shape, but round 6 reopens more shared-path plumbing than the memo’s top-level framing implies

The memo is right to insist on one new independent proof token rather than mode stacking. That matches how the existing proof modes are authorized and guarded today (`src/presenter/bounded_dynamic_composition.py:15-45`, `communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_scope.md:122-145`).

But this is not just one new constant.

- `bounded_dynamic_composition.py` currently only has one AOI proof branch, and it is single-surface only (`src/presenter/bounded_dynamic_composition.py:257-320`, `src/presenter/bounded_dynamic_composition.py:518-542`, `src/presenter/bounded_dynamic_composition.py:727-877`).
- The suite trace grammar currently activates only for `adaptive_genealogy_relationship_conditions_v1` (`src/presenter/bounded_dynamic_composition.py:293-303`, `src/presenter/bounded_dynamic_composition.py:316-321`).
- `decision_trace.py` only imports the existing AOI single-surface token and only probes inspectable composition for the current three proof modes (`src/presenter/decision_trace.py:15-23`, `src/presenter/decision_trace.py:91-109`).
- The generic host only knows the current four proof labels, including `adaptive_aoi_theme_surface_v1` (`/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:77-96`).
- The Critic client tests also enumerate the currently allowed tokens for manifest, presentation, refresh, and single-view forwarding (`/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts:126-189`).

The memo does acknowledge some of this in “Round 6 is not just a new constant” (`communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_scope.md:283-292`). That judgment is correct. The memo should just be a little more explicit that the reopened surface includes:

- new suite dispatch in analyzer-v2
- suite inspectability in trace
- shared-path threading through manifest, presentation, refresh, and single-view
- one new generic host proof label
- shared client and page tests for the new token

### 3. The named fallback to `aoi_by_sin_type` is sensible, but it is not actually a ready fallback scope yet

The memo is right to name `aoi_by_sin_type` as the fallback if Gate B fails. It is mechanically more grounded than the report surface because:

- it already has a live child view definition
- it already has a normalized grouped payload
- the `card_grid` renderer already accepts a category-keyed object shape (`src/views/definitions/aoi_by_sin_type.json:1-44`, `src/aoi/contract.py:418-430`, `src/renderers/definitions/card_grid.json:7-29`)

But the memo only names the fallback target. It does not define:

- the runtime families for `aoi_by_sin_type`
- the selector for choosing between those families
- the trace expectations for that alternative suite

So `aoi_by_sin_type` is a legitimate fallback direction, but not an implementation-ready fallback scope as written. If the team decides it should replace `aoi_thematic_report` as the primary second surface, the memo needs one more pass that defines the corresponding sin-type runtime families and selection rules before code work starts.

### 4. The gate status is correct and should stay red until round 5 is route-proof-complete

The memo’s gate judgment is defensible and consistent with the prior rounds.

- Round 4 was treated as documentary-complete only after its route-real proof note and saved artifacts existed (`communications/MEMO_2026-03-20_round4_adaptive_surface_suite_completion.md:203-212`, `communications/PROOF_2026-03-20_round4_adaptive_surface_suite.md:82-239`).
- Round 5 explicitly says `Proof Note: pending`, `route-proof-pending`, and `documentary-incomplete` (`communications/MEMO_2026-03-21_round5_cross_workflow_adaptive_aoi_theme_completion.md:7`, `communications/MEMO_2026-03-21_round5_cross_workflow_adaptive_aoi_theme_completion.md:113-142`).
- The same memo states that the local workspace currently has `0` completed AOI jobs for this workflow and that round-5 closure still requires synthetic-but-route-real fixtures plus the final proof note (`communications/MEMO_2026-03-21_round5_cross_workflow_adaptive_aoi_theme_completion.md:119-131`).

So the round-6 disposition should remain exactly what the memo says:

- scoping is legitimate
- implementation is not yet a green light

I do not see a repo-grounded reason to relax that gate.

### 5. The memo is mostly right about the generic host, but the wording should mean “no new AOI-specific host work,” not “the host has no AOI-specific code”

The generic route is the right proving vehicle. The March 18 execution brief made `AnalysisWorkspacePage` the named proving vehicle for both genealogy and AOI (`communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md:30-52`).

And for round 6 specifically, I do not see evidence that the Critic host needs new AOI-specific rendering logic beyond one new proof-label mapping and generic token-threading tests.

But the current generic host is not workflow-agnostic in the literal sense.

- `AnalysisWorkspacePage` has explicit AOI detection, requires `selected_source_thinker_id`, filters saved results by thinker, and injects thinker scope into AOI run launch (`/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:181-186`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:451-467`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:592-639`).
- `useBoundedV2Workspace` also threads `selectedSourceThinkerId` into active-run discovery for AOI (`/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:320-347`).
- The bespoke `AoiV2ThematicPanel` remains an AOI-specific host surface with its own local assumptions, but the round-6 memo correctly excludes it from the proof boundary (`communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_scope.md:146-164`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:22-24`).

So the memo’s host claim is acceptable if it is read precisely:

- the proving vehicle remains the generic route
- no new AOI-specific host logic should be added for round 6

It would be inaccurate if read as:

- the Critic host currently contains no AOI-specific behavior at all

## Checks Performed

- Read the round-6 scope memo in full: `communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_scope.md`.
- Cross-checked program position and gate assumptions against:
  - `communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
  - `communications/PROOF_2026-03-19_thin_consumer_platformization_round1.md`
  - `communications/MEMO_2026-03-20_round4_adaptive_surface_suite_completion.md`
  - `communications/PROOF_2026-03-20_round4_adaptive_surface_suite.md`
  - `communications/MEMO_2026-03-21_round5_cross_workflow_adaptive_aoi_theme_completion.md`
  - `communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md`
  - `communications/PLAN_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_execution.md`
- Inspected current analyzer-v2 runtime-composition and trace surfaces:
  - `src/presenter/bounded_dynamic_composition.py`
  - `src/presenter/decision_trace.py`
  - `src/presenter/presentation_api.py`
  - `src/presenter/manifest_builder.py`
- Inspected AOI normalized contract and view/renderer seams:
  - `src/aoi/contract.py`
  - `src/views/definitions/aoi_thematic_analysis.json`
  - `src/views/definitions/aoi_by_theme.json`
  - `src/views/definitions/aoi_thematic_report.json`
  - `src/views/definitions/aoi_by_sin_type.json`
  - `src/renderers/definitions/accordion.json`
  - `src/renderers/definitions/table.json`
  - `src/renderers/definitions/card_grid.json`
  - `src/renderers/validator.py`
- Inspected current Critic generic-route and client plumbing:
  - `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
  - `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
  - `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts`
  - `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- Checked current tests for AOI contract shape and proof-token threading:
  - `tests/test_aoi_contract.py`
  - `tests/test_aoi_canary_contract.py`
  - `tests/test_manifest_trace.py`
  - `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts`
  - `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.integration.test.tsx`

## What Seems Correct

- `adaptive_aoi_theme_report_suite_v1` is the right next proof shape if the proof remains bounded to exactly two AOI child surfaces and does not attempt proof-mode stacking (`communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_scope.md:122-145`, `src/presenter/bounded_dynamic_composition.py:15-45`).
- `aoi_thematic_report` is the better second surface than `aoi_by_sin_type` for the program thesis because it proves coordination across unlike AOI child surfaces and a distinct phase seam, not just another regrouping of the same findings family (`communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_scope.md:166-202`, `src/views/definitions/aoi_thematic_report.json:62-86`, `src/views/definitions/aoi_by_sin_type.json:20-44`).
- The existing AOI tree structure does support in-place child replacement under `aoi_thematic_analysis`. Runtime payloads preserve `source_parent_view_key`, and `_build_view_tree()` re-nests children by that key without requiring a new runtime parent (`src/presenter/bounded_dynamic_composition.py:1605-1606`, `src/presenter/bounded_dynamic_composition.py:1651-1652`, `src/presenter/presentation_api.py:2181-2217`).
- The existing suite-style trace grammar is the right thing to reuse. Round 4 already proved that `adaptive_surface_suite_selection` can record per-surface decisions cleanly, and `decision_trace.py` already knows how to summarize `surface_decisions` when a suite-mode token is active (`communications/PROOF_2026-03-20_round4_adaptive_surface_suite.md:137-239`, `src/presenter/bounded_dynamic_composition.py:117-127`, `src/presenter/decision_trace.py:221-267`).
- The generic host already forwards `composition_mode` through result manifest, presentation, refresh, and single-view paths. That means round 6 can stay host-generic in substance if the new token is added to the same shared plumbing and test matrix (`/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts:117-166`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:374-394`).

## Risks / Open Questions

- Is the team willing to narrow `aoi_report_evidence_review` to a very explicit table contract now, or should round 6 deliberately use two `accordion`-family report contracts first and leave cross-renderer heterogeneity for a later AOI tranche? The current memo wants heterogeneity, but that is where most of the hidden transform work lives.
- If Gate B fails and `aoi_by_sin_type` becomes the second target, what are the two sin-type runtime families and the deterministic selector? The current memo names the fallback target but does not yet scope the fallback family contracts.
- Are the intended proof fixtures guaranteed to contain both a valid `aoi_by_theme` payload and a valid phase-4 `aoi_thematic_report` payload on the same jobs? The round-5 completion memo says there are still no completed AOI jobs locally, so this matters before implementation starts (`communications/MEMO_2026-03-21_round5_cross_workflow_adaptive_aoi_theme_completion.md:119-127`).
- Should the memo explicitly state that round 6 reopens shared-path tests in both repos, not just backend selector logic? The current client and integration tests still enumerate only the existing tokens (`/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts:126-189`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.integration.test.tsx:617-724`).
