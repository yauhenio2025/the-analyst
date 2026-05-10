# Memo: Phase E Renderers-UI Generic Capture-Base Shell Extraction V1 Completion

Subtitle: One bounded top-level package pilot now proves a smaller package-native raw capture-base shell in `renderers-ui` without promoting Critic-local first-hop, workflow/job, or typed-selection law into the shared renderer package

Date: 2026-04-04
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Most Recent Prior Completion:
- `communications/MEMO_2026-04-04_phase_e_current_renderer_selection_emission_shared_seam_promotion_readiness_v1_completion.md`
Immediate Prior Scope:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_scope.md`
Review Context:
- `communications/REPORT_Codex_Phase_E_Renderers_UI_Generic_Capture_Base_Shell_Extraction_V1_Scope_Audit_Rerun_2026-04-04.md`
- `communications/REPORT_Claude_Phase_E_Renderers_UI_Generic_Capture_Base_Shell_Extraction_V1_Scope_Critique_Rerun_2026-04-04.md`
Package Codebase:
- `/home/evgeny/projects/analyzer-v2/renderers-ui`

## Purpose

Record what actually landed after the docs-first promotion-readiness slice narrowed the honest shared candidate from the Critic-local `currentRendererCapture` helper to one smaller package-native raw capture-base shell.

This slice was deliberately bounded.
It was not:

- unchanged promotion of `currentRendererCapture`
- package-wide capture convergence
- a `SubRenderers` migration
- capture-forwarding normalization
- a Critic host change

## What Landed

One bounded package-local extraction slice is now complete inside `renderers-ui`.

The landed behavior is:

1. a new internal utility now exists at:
   - `renderers-ui/src/utils/captureBase.ts`
2. that utility is intentionally package-native and internal-only:
   - no export from `renderers-ui/src/index.ts`
   - no Critic `CaptureSelection`
   - no `_firstHopAffordance`
   - no workflow/job requiredness options
   - no `source_workflow_key`
   - no `genealogy_job_id`
3. the new utility is now adopted by the three bounded top-level package renderers only:
   - `AccordionRenderer`
   - `CardRenderer`
   - `CardGridRenderer`
4. the extracted shell preserves current package behavior exactly:
   - raw `captureMode && onCapture` gate only
   - raw string-or-default semantics only
   - no trim or non-empty normalization
   - `>` title composition
   - no empty-segment filtering
   - raw `captureEntityId || captureJobId || ''` fallback when no explicit `entityId` is passed
5. a lightweight package-local verification script now exists at:
   - `renderers-ui/scripts/check-capture-base.mjs`
6. the dominant deferred surface remained intentionally untouched:
   - `renderers-ui/src/sub-renderers/SubRenderers.tsx`
7. the known nested forwarding asymmetries also remained untouched:
   - `AccordionRenderer` still does not forward `_captureSourceType` / `_captureEntityId` into nested sub-renderers
   - `CardRenderer` nested subsection dispatch still does not forward capture runtime into nested sub-renderers at all

## The Final Boundary

The honest completed claim is:

- `renderers-ui` now has one real internal raw capture-base utility proven on the clean top-level package trio

What this does mean:

- the narrower shared candidate identified in the readiness memo is no longer only a docs-level hypothesis
- the shared renderer package now owns one real reusable raw capture-base shell in code
- the package utility boundary is now proven on:
  - section capture in `AccordionRenderer`
  - direct card capture in `CardRenderer`
  - card-grid capture in `CardGridRenderer`

What this does not mean:

- package-wide capture convergence is now proven
- `SubRenderers` has been migrated
- forwarding asymmetries have been normalized
- `currentRendererCapture` is now obsolete
- Critic-local first-hop/workflow policy has moved upstream
- generic renderer-package capture law is now solved

## Implementation Shape

The implementation stayed narrowly aligned to the approved scope.

### 1. The utility stayed smaller than the Critic helper

`resolvePackageCaptureBaseRuntime(config)` now:

- returns `null` unless:
  - `config._captureMode === true`
  - `config._onCapture` is a function
- reads only package-common raw config:
  - `_captureViewKey`
  - `_captureSourceType`
  - `_captureJobId`
  - `_captureEntityId`
- preserves raw string-or-default semantics rather than trimming or normalizing values

`buildPackageCaptureSelectionBase(runtime, params)` now:

- accepts only:
  - `titleSegments: string[]`
  - optional `entityId`
- returns only:
  - `source_view_key`
  - `source_type`
  - `context_title`
  - `entity_id`
- preserves current package title law exactly:
  - `[runtime.sourceViewKey || 'Analysis', ...titleSegments].join(' > ')`
- preserves current package identity fallback exactly:
  - `entityId !== undefined`
  - otherwise `runtime.captureEntityId || runtime.captureJobId || ''`

### 2. The three top-level adopters stayed local in the right places

The shell only absorbed the truly shared base.
Each renderer still owns its renderer-specific fields.

That means the utility does **not** own:

- `source_section_key`
- `source_item_index`
- `source_renderer_type`
- `content_type`
- `selected_text`
- `structured_data`
- `depth_level`
- `parent_context`

The adoption pattern is now:

- resolve package runtime once
- build the shared base
- merge renderer-local fields around it
- emit the final raw selection payload through the existing package `Record<string, unknown>` callback

### 3. `CardGridRenderer` stayed honest about where capture really lives

The package pilot did not pretend all three adopters had the same internal structure.

`CardGridRenderer` capture emission still lives in the inner `CardWrapper` path.
That path now uses the shared utility too, but without inventing new prop-threading or changing the card-grid component boundary.

## Verification

Focused package-local verification passed:

- `npm run build`
  - passed
- `node scripts/check-capture-base.mjs`
  - `capture-base verification passed`

This slice did **not** rerun Critic consumer regressions because:

- the work stayed package-local
- no local tarball refresh into Critic was part of this slice

Environment honesty notes:

- the verification script still emits Node's existing `MODULE_TYPELESS_PACKAGE_JSON` warning when importing the built internal module from `dist`
- that warning was left alone because package module-mode changes were out of scope
- pre-existing unrelated worktree modifications in:
  - `renderers-ui/package.json`
  - `renderers-ui/src/index.ts`
  were left untouched

## Calibrated Claim

Before this slice, the strongest honest claim was:

- the smaller package-native shell had been identified as the next honest extraction candidate

After this slice, the stronger honest claim is:

- that smaller shell now exists in real package code and is adopted by the top-level package trio

That is a material advance.
But it remains deliberately partial:

- the top-level trio is now proven
- the dominant `SubRenderers` surface is still deferred
- the runtime-threading asymmetries across nested paths are still unchanged

So the right closeout language is:

- **top-level package pilot complete**

not:

- package-wide capture-base extraction complete

## Why This Matters

This slice matters because it converted a docs-level candidate into one bounded reusable package implementation without importing host-specific law into `renderers-ui`.

That strengthens the analyzer-v2-as-brain direction in a specific, defensible way:

- shared capture-base behavior now lives in analyzer-v2-owned renderer substrate rather than only in repeated inline top-level builders
- the package now has one real internal utility beneath both the package trio and the Critic-local helper
- the next package-side question can now be about the dominant deferred surface, not about whether the utility itself is still hypothetical

## Next Honest Step

The next honest question is no longer:

- does the smaller package-native shell exist in real code

That is now answered.

The next question is:

- can the same internal package utility be adopted across the dominant deferred `SubRenderers` capture surface
- while preserving current forwarded defaults and leaving forwarding asymmetry normalization untouched

That next slice should stay bounded.
It should:

- target the existing inline capture builders in `renderers-ui/src/sub-renderers/SubRenderers.tsx`
- preserve current package defaulting
- preserve current `>` title composition
- preserve current raw identity fallback
- stay below forwarding normalization
- stay below Critic-local first-hop/workflow/type law

What should **not** happen next:

- package-wide convergence language
- a forced forwarding-normalization tranche in the same slice
- helper-promotion language returning through the side door
- generic renderer-package law claims
- host/analyzer/backend widening

## Final Completed Claim

This slice is now complete.

Its finished claim is:

- `renderers-ui` now contains one real internal raw capture-base utility
- that utility is proven on the bounded top-level package pilot of `AccordionRenderer`, `CardRenderer`, and `CardGridRenderer`
- the stronger remaining package-side question is now the dominant deferred `SubRenderers` adoption surface, not whether the utility itself is real
