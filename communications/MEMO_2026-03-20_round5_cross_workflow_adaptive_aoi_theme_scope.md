# Memo: Next Stage Scope - Round 5 / Cross-Workflow Adaptive AOI Theme Proof

Date: 2026-03-20
Program: Thin Consumer Platformization

## Purpose

Define the next bounded stage after round 4.

This memo answers:

1. what the last five days of work have actually established
2. what meaningful platform variable still remains unproven after round 4
3. what the next proof should be if the goal is still beautiful-by-default thin consumers
4. what the next proof should and should not attempt

This is a scope memo, not an execution plan.

## Basis For This Scope

The governing record for this stage is now:

- `communications/MEMO_2026-03-16_aoi_strategic_reassessment_after_parity_work.md`
- `communications/MEMO_2026-03-16_beautiful_by_default_surfaces_platform_gap.md`
- `communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `communications/PROOF_2026-03-19_thin_consumer_platformization_round1.md`
- `communications/MEMO_2026-03-20_round2_bounded_dynamic_composition_completion.md`
- `communications/MEMO_2026-03-20_round3_adaptive_surface_family_completion.md`
- `communications/MEMO_2026-03-20_round4_adaptive_surface_suite_completion.md`
- `communications/PROOF_2026-03-20_round4_adaptive_surface_suite.md`
- `communications/MEMO_2026-03-20_round4_adaptive_surface_suite_scope.md`
- `communications/REPORT_Claude_Round5_Cross_Workflow_Adaptive_AOI_Theme_Scope_Critique_2026-03-20.md`
- `communications/REPORT_Codex_Round5_Cross_Workflow_Adaptive_AOI_Theme_Scope_Audit_2026-03-20.md`
- `the-critic/communications/NEXT_SESSION_DYNAMIC_COMPOSITION_AUDIT.md`

The strategic through-line across those documents is now clear:

- round 1 proved the thin host and shared contract
- round 2 proved bounded runtime regrouping
- round 3 proved single-surface adaptive family selection
- round 4 proved coordinated multi-surface adaptive composition on one genealogy page

What is still not proven is whether that adaptive-composition story is:

- genuinely platform-level, or
- still effectively a genealogy-only success story

## Current Program Position

As of 2026-03-20:

- the generic Critic host is already a real thin-consumer proof
- adaptive composition no longer depends on workflow-specific host logic
- analyzer-v2 has now proven one singular adaptive proof and one multi-surface adaptive proof

But all adaptive proofs so far are still inside:

- `intellectual_genealogy`

That leaves one meaningful strategic doubt:

- the adaptive-composition contract could still be overfit to genealogy’s semantic shape, view tree, and transformation patterns

That is the next variable to isolate.

## Core Strategic Judgment

The right next proof is not:

- another genealogy-only expansion
- a three-surface genealogy suite
- a generalized adaptive registry
- broad declarative composition infrastructure
- cross-workflow freeform generation
- host-side AOI customization

The right next proof is:

- the first cross-workflow adaptive proof on the existing AOI generic route

Round 5 should isolate one bounded question:

- can the same thin host and the same upstream adaptive-composition discipline operate on a materially different workflow family, with a materially different structured payload shape, without becoming genealogy-specific in disguise

That is the smallest next proof that materially advances the platform thesis after round 4.

## Recommended Label

Use:

- **Thin Consumer Platformization Round 5**

More specifically:

- **Cross-Workflow Adaptive AOI Theme Proof**

Do not call this:

- generalized adaptive composition
- AOI redesign
- a platform-wide adaptive registry

## Round-4 Documentary Gate

Round 5 should not be scoped as active implementation until round 4 is documentary-closed.

Owner of that gate:

- the maintainer preparing round-5 scope and execution planning

Status:

- satisfied by:
  - `communications/PROOF_2026-03-20_round4_adaptive_surface_suite.md`
  - `communications/MEMO_2026-03-20_round4_adaptive_surface_suite_completion.md`

This means round-5 scoping is now legitimate.

## Recommended Activation Contract

Use the existing thinker-scoped AOI generic route with one new proof-only mode:

- `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=<id>&selected_source_thinker_name=<name>&composition_mode=adaptive_aoi_theme_surface_v1`

Hard rules:

- `adaptive_aoi_theme_surface_v1` is independent of:
  - `adaptive_relationship_surface_v1`
  - `adaptive_genealogy_relationship_conditions_v1`
  - `bounded_dynamic_genealogy_v1`
- do not stack proof modes
- do not require any genealogy proof mode to be active simultaneously

The round-5 claim is:

- the generic AOI page can carry one upstream adaptive surface-family proof

not:

- proof modes can be arbitrarily layered across workflows

## Proof Surface Boundary

Round 5 is explicitly bounded to the **generic AOI route**:

- `AnalysisWorkspacePage`

It is **not** a proof of the bespoke AOI panel:

- `the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`

That bespoke panel is not proof-ready for round 5 because:

- it does not pass `compositionMode` into the shared bounded-v2 path
- its lazy single-view fetch bypasses the shared client and omits `composition_mode`
- it has its own AOI-specific presentation lifecycle

Optional convenience work is allowed:

- one explicit proof-only handoff link from the existing AOI thinker page to the generic proof route

If that link is added, it should be scoped as a simple route constructor only. It should forward:

- `selected_source_thinker_id`
- `selected_source_thinker_name`
- `composition_mode=adaptive_aoi_theme_surface_v1`

It should not attempt to transfer bespoke AOI panel state, restore state, or cached results.

## Recommended Proof Target

Round 5 should target exactly one AOI surface:

- `aoi_by_theme`

Why `aoi_by_theme` is the right first cross-workflow target:

1. it is one of the highest-salience AOI reading surfaces
2. it already has a stable normalized payload seam in `src/aoi/contract.py`
3. it is materially different from genealogy’s semantic shape:
   - grouped themes
   - theme-specific engagement summaries
   - source-document inventories
   - bounded findings arrays
4. it can make the AOI route feel genuinely different upstream without reopening the host boundary

Why not start with `aoi_thematic_analysis` as the adaptive target:

- that would reopen parent-container structure too early
- it would blur the distinction between proving one adaptive child surface and redesigning the AOI page

Why not start with `aoi_by_sin_type`:

- it is useful, but lower-salience as a first cross-workflow proof
- it is more obviously a secondary regrouping axis than a primary reading surface

Named fallback if the `aoi_by_theme` signal gate fails:

- `aoi_thematic_report`

## Child-Surface Placement Rule

`aoi_by_theme` is not a top-level AOI view. It is a child of:

- `aoi_thematic_analysis`

So round 5 should adapt it **in place as a child surface under the existing parent tab container**.

Do not:

- promote `aoi_by_theme` to top-level
- generate a new AOI runtime parent
- restructure the AOI page tree around this proof

The adaptive family should replace the child-view payload and render contract for `aoi_by_theme` while preserving its place inside the existing `aoi_thematic_analysis` container.

## Pre-Execution Verification Gate

Before implementation starts, verify on at least two candidate AOI proof jobs that the already-built payload entry:

- `payloads["aoi_by_theme"].structured_data`

is present and stable.

Required shape on both candidate jobs:

1. top-level keys:
   - `_section_order`
   - `_section_titles`
2. one dict payload per theme id named in `_section_order`
3. each theme payload reliably exposes:
   - `overview`
   - `engagement`
   - `key_claims`
   - `philosophical_commitments`
   - `argumentative_moves`
   - `source_documents`
   - `findings`
4. each finding card reliably exposes:
   - `title`
   - `subtitle`
   - `description`
   - `badge`
   - `sin_type`
   - `sin_type_label`

This is the primary seam.

The selector should aggregate across the top-level `aoi_by_theme` payload entry, not by reparsing raw AOI engine prose and not by starting from lower child payloads.

If this gate fails on real payload inspection:

- do not force `aoi_by_theme` anyway
- switch the target to `aoi_thematic_report`
- rename the proof token accordingly before code work starts

## Hard Scope Rules

### 1. Exactly One Adaptive AOI Surface

Round 5 should adapt exactly one AOI surface:

- `aoi_by_theme`

Do not add a second AOI adaptive surface in this tranche.

### 2. Deterministic Selection Over Existing Structured Outputs

The selector must operate on already-built presentation payloads.

It must not:

- add a new inference pass
- parse raw prose in the host
- depend on a new AOI planner
- reopen AOI engine contracts

The selector should aggregate over the top-level `aoi_by_theme` grouped payload:

- `_section_order`
- `_section_titles`
- per-theme `overview`
- per-theme `engagement`
- per-theme `key_claims`
- per-theme `philosophical_commitments`
- per-theme `argumentative_moves`
- per-theme `source_documents`
- per-theme `findings`

not over raw engine JSON and not by reparsing `aoi_sin_findings` prose output.

### 3. Keep The Host Generic

The Critic should remain generic in substance.

Allowed host-side work:

- one new generic proof-label mapping for the new `composition_mode`
- if execution convenience requires it, one proof-only AOI handoff link from the existing thinker page into the generic proof route
- generic proof-route tests covering the new mode token

Not allowed:

- workflow-specific renderer logic in `AnalysisWorkspacePage`
- AOI-specific adaptive selection logic in the host
- bespoke-panel proof work inside `AoiV2ThematicPanel`

### 4. Keep AOI Routing And Thinker Scope Stable

Do not reopen the round-1 AOI generic-route contract.

The round-5 proof must still use:

- `selected_source_thinker_id` as the authoritative AOI route context
- the existing generic workspace AOI restore/discovery rules

Round 5 is about adaptive surface selection, not about changing AOI routing or identity scope.

### 5. Name The Backend Expansion Honestly

Round 5 is not just “one new constant.”

The adaptive backend is still genealogy-locked in:

- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/decision_trace.py`

So this proof explicitly includes bounded cross-workflow widening in those modules:

- proof-mode validation must accept the AOI workflow for the new mode
- supported-mode registries must include the AOI mode
- runtime-composition dispatch must add an AOI branch
- composition inspection and stage naming must add an AOI branch
- trace reconstruction must include the AOI mode in its adaptive inspection path

This is still bounded work, but the memo should not pretend the current composer is already workflow-agnostic.

## Recommended Runtime Families

Round 5 should use exactly two AOI runtime families.

That is enough to prove cross-workflow adaptive selection without widening into an AOI suite.

### Family 1: `aoi_theme_dossier`

Use when one or two themes clearly dominate the AOI result.

Contract:

- renderer: `accordion`
- replace the existing `aoi_by_theme` child view in place
- top-level `structured_data` contains:
  - `suite_summary: string`
  - `_section_order`
  - `_section_titles`
  - one normalized theme dossier object per theme id
- renderer config:
  - leading `suite_summary` rendered via `prose_block`
  - one section per theme id
  - dynamic `_default` theme section renderer with sub-renderers:
    - `overview -> annotated_prose`
    - `engagement -> annotated_prose`
    - `key_claims -> rich_description_list`
    - `philosophical_commitments -> rich_description_list`
    - `argumentative_moves -> rich_description_list`
    - `source_documents -> chip_grid`
    - `findings -> mini_card_list`

Intent:

- the AOI result should read as a small number of dominant thematic dossiers

### Family 2: `aoi_theme_comparison_review`

Use when themes remain distributed enough that comparison is more informative than dossier reading.

Contract:

- renderer: `table`
- replace the existing `aoi_by_theme` child view in place
- top-level `structured_data` is a flat row array
- renderer config must define explicit column objects, not just prose column names

Required columns:

- `theme_name`
- `finding_count`
- `dominant_sin_type`
- `source_document_count`
- `key_claim_count`
- `overview_excerpt`

Recommended column config:

- `{ "key": "theme_name", "label": "Theme", "sortable": true }`
- `{ "key": "finding_count", "label": "Findings", "sortable": true }`
- `{ "key": "dominant_sin_type", "label": "Dominant Sin Type", "sortable": true }`
- `{ "key": "source_document_count", "label": "Sources", "sortable": true }`
- `{ "key": "key_claim_count", "label": "Key Claims", "sortable": true }`
- `{ "key": "overview_excerpt", "label": "Overview", "sortable": false }`

Row derivation rules:

- `theme_name` from `_section_titles[theme_id]`
- `finding_count` from `len(findings)`
- `dominant_sin_type` from the most frequent `sin_type_label` in the theme’s `findings`
- `source_document_count` from `len(source_documents)`
- `key_claim_count` from `len(key_claims)`
- `overview_excerpt` from a deterministic truncation of `overview`

Explicit exclusions for this first proof:

- do not require discrete `engagement_level`
- do not introduce `reading_signal`
- do not parse the prose `engagement` string to recover a missing normalized field

Intent:

- the AOI result should read as a comparative field review across themes rather than a few deep dossiers

At least one family must use a different top-level renderer type.

This requirement is satisfied by:

- `accordion` vs `table`

## Recommended Deterministic Selector

The selector should compute, from the top-level `aoi_by_theme` payload entry:

- `theme_count`
- `total_finding_count`
- `dominant_theme_id`
- `dominant_theme_findings`
- `dominant_theme_share`
- `second_theme_findings`
- `theme_source_document_counts`
- `theme_key_claim_counts`
- `dominant_sin_type_per_theme`

Recommended decision rule:

- choose `aoi_theme_dossier` iff:
  - `theme_count <= 3`, and
  - `dominant_theme_share >= 0.5`
- otherwise choose `aoi_theme_comparison_review`

This keeps the first cross-workflow proof bounded and inspectable.

It does not try to prove a full AOI surface taxonomy.

## Trace And Inspectability

Round 5 should reuse the existing singular adaptive trace pattern:

- `adaptive_surface_selection`

Required details:

- `target_surface = "aoi_by_theme"`
- `selected_family`
- `signal_summary`
- `rejected_families`
- `rationale`

The point is not to invent a new trace grammar.

The point is to prove that the existing adaptive-trace discipline generalizes across workflows.

This does require one bounded widening:

- `src/presenter/decision_trace.py` must include the AOI mode in its adaptive inspection dispatch

## Public Interfaces And Stability Rules

No backend workflow API changes are required beyond one new proof mode on the existing shared presenter/result path.

Thread the new mode through the already-shared paths:

- result manifest
- result presentation
- refresh presentation
- single-view
- trace

Do not widen:

- AOI analyzer contracts
- generic input-schema systems
- cross-mode stacking rules

## Missing Test Surfaces Round 5 Must Cover

The round-5 proof is not documentary-complete unless it adds focused coverage for:

- AOI-mode acceptance in `bounded_dynamic_composition.py`
- AOI adaptive inspection/trace dispatch in `decision_trace.py`
- in-place child-surface rewrite semantics for `aoi_by_theme`
- generic AOI route proof-label and composition-mode forwarding
- lazy single-view forwarding on the generic AOI route
- optional thinker-page proof handoff, if that link is kept in scope

## Proof Record Expectations

Round 5 closure should use the same documentary discipline as round 3 and round 4:

- route-real proof evidence
- explicit saved artifacts
- explicit job ids and route strings
- explicit trace rationale

Required proof record:

- two contrast AOI jobs or synthetic-but-route-real AOI fixtures
- the same generic route shape
- the same `composition_mode`
- the selected thinker id named in the proof note
- the selected family and rationale named for both proof fixtures

## What Round 5 Would Prove

If successful, round 5 would prove:

1. adaptive surface-family selection is not genealogy-specific
2. the existing adaptive-composition discipline generalizes across two materially different workflow families
3. the same thin host can consume cross-workflow adaptive contracts without new workflow-specific host logic
4. the platform story is now about upstream composition across workflows, not just genealogy variance

## What Round 5 Should Not Try To Prove

Round 5 should not try to prove:

1. a multi-surface AOI suite
2. a declarative adaptive family registry
3. cross-workflow suite coordination
4. AOI route redesign
5. generalized app-on-the-fly generation
6. retirement of the bespoke AOI panel

Those are later questions.

The bounded question here is simpler:

- can one serious AOI child surface become adaptively composed on the same thin host boundary that already proved genealogy

## Final Recommendation

The next stage should be:

- **Round 5 / Cross-Workflow Adaptive AOI Theme Proof**

The recommended first proof should:

- stay on the generic AOI route
- target `aoi_by_theme`
- adapt that child surface in place under `aoi_thematic_analysis`
- use one new independent `composition_mode`
- choose between exactly two renderer-level runtime families
- preserve the Critic host as generic in substance

That is the smallest next proof that materially advances the platform thesis after round 4.
