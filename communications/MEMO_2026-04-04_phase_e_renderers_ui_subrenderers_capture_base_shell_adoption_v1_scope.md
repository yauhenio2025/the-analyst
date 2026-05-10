# Memo: Phase E Renderers-UI SubRenderers Capture-Base Shell Adoption V1 Scope

Subtitle: Now that the top-level package pilot has landed, the next honest cross-repo move is to adopt the same internal `captureBase` utility across the dominant deferred `SubRenderers` capture surface while preserving current forwarded defaults and leaving forwarding asymmetry normalization out of scope

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
Immediate Prior Completion:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_completion.md`
Immediate Prior Scope:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_scope.md`
Relevant Review Context:
- `communications/REPORT_Codex_Phase_E_Renderers_UI_Generic_Capture_Base_Shell_Extraction_V1_Scope_Audit_Rerun_2026-04-04.md`
- `communications/REPORT_Claude_Phase_E_Renderers_UI_Generic_Capture_Base_Shell_Extraction_V1_Scope_Critique_Rerun_2026-04-04.md`
Package Codebase:
- `/home/evgeny/projects/analyzer-v2/renderers-ui`

## Purpose

Define the next bounded package-side follow-on now that the smaller internal `captureBase` shell is no longer a docs candidate and no longer only a top-level extraction hypothesis.

This next slice should answer one narrower question:

- does the already-landed internal utility also fit the current inline `SubRenderers` capture builders without importing Critic-local policy or forcing nested forwarding normalization into the same tranche

This slice is still package-local.
It should not be framed as:

- package-wide convergence
- a fix for the nested forwarding asymmetries
- a reopening of helper-promotion readiness
- a Critic host change

## Why This Is The Right Next Step

The top-level package pilot closed the first package extraction question honestly.

What is now known:

- the smaller package-native shell is real code, not a hypothetical candidate
- it already preserves exact package behavior on the top-level trio
- the dominant remaining inline capture weight is in `renderers-ui/src/sub-renderers/SubRenderers.tsx`
- the package still does **not** have package-wide convergence, because the dominant deferred surface remains untouched

So the next question is no longer:

- does the utility itself exist or fit the top-level package renderers

The next question is:

- can the same utility absorb the eight current inline `SubRenderers` capture builders while preserving current behavior and leaving current runtime-threading asymmetries alone

## Proposed Bounded Slice

Keep the utility itself unchanged unless a small internal naming/typing cleanup is required.

Do **not** export it from `src/index.ts`.

Adopt the already-landed `captureBase` utility inside exactly these `SubRenderers` builders:

1. `DefinitionList`
2. `MiniCardList`
3. `ComparisonPanel`
4. `IntensityMatrix`
5. `MoveRepertoire`
6. `DialecticalPair`
7. `RichDescriptionList`
8. `PhaseTimeline`

Do not widen this slice beyond the current inline builder set in `SubRenderers.tsx`.

## Exact Shared Responsibility

The extracted shell should continue to own only:

- raw package capture gate:
  - `_captureMode === true`
  - `_onCapture` is a function
- package-common raw capture config reads:
  - `_captureViewKey`
  - `_captureSourceType`
  - optional `_captureJobId`
  - optional `_captureEntityId`
- base selection assembly only:
  - `source_view_key`
  - `source_type`
  - `context_title`
  - `entity_id`

The adoption must preserve package behavior exactly:

- no trim or non-empty normalization
- `source_view_key: ''` when absent
- `source_type: 'analysis'` when absent
- `context_title` composed as:
  - `[sourceViewKey || 'Analysis', ...titleSegments].join(' > ')`
- no empty-segment filtering
- `entity_id` precedence remains:
  - explicit `entityId !== undefined`
  - otherwise `captureEntityId || captureJobId || ''`

## What The Sub-Renderers Should Still Own Locally

Even after adoption, each sub-renderer should still own:

- `source_section_key`
- `source_item_index`
- `source_renderer_type`
- `content_type`
- `selected_text`
- `structured_data`
- `depth_level`
- `parent_context`
- local title-segment selection

This is not a second helper-promotion argument.
It is the same raw package shell, applied to the dominant deferred inline-builder surface.

## Forwarding Boundary Must Stay Explicit

This slice must preserve one important separation:

- **adoption of the shared base utility**
- **normalization of nested capture forwarding**

Those are not the same question.

Current asymmetries that must remain explicitly out of scope here:

- `AccordionRenderer` nested forwarding still omits:
  - `_captureSourceType`
  - `_captureEntityId`
- `CardRenderer` nested subsection dispatch still does not forward capture runtime into nested sub-renderers at all

That means this slice should preserve the current forwarded defaults that the `SubRenderers` surface already experiences.
It should not silently “fix” them while adopting the utility.

## What Must Stay Out

This slice must not:

- change `resolvePackageCaptureBaseRuntime(...)` into a Critic-style fail-closed resolver
- add `_captureViewName`
- add `_firstHopAffordance`
- add `requireWorkflowKey`
- add `requireJobId`
- add `source_workflow_key`
- add `genealogy_job_id`
- import Critic `CaptureSelection`
- change `>` title law to `:`
- normalize empty title segments
- normalize or reinterpret forwarded runtime values
- widen to top-level forwarding fixes
- claim package-wide capture convergence

## What Success Looks Like

This slice succeeds if:

- the existing internal `captureBase` utility is now used by the current inline capture builders in `SubRenderers.tsx`
- emitted raw selection payloads remain behaviorally equivalent
- current forwarded defaults remain unchanged
- the package still stays below Critic-local first-hop/workflow/type law

This should be described as proof of utility fit across the current inline `SubRenderers` builders.
It should not be described as broader proof that nested package runtime coverage is now converged.

This slice does **not** need to prove:

- forwarding asymmetry normalization
- deletion of the inline top-level forwarding objects
- package-wide capture law
- Critic helper deletion

## Verification

The verification should stay bounded and honest.

Do **not** introduce heavy package test infrastructure in this slice.

The proof should include:

- `npm run build` in `renderers-ui`
- extension of the existing lightweight package verification script:
  - `renderers-ui/scripts/check-capture-base.mjs`
- rerun of:
  - `node scripts/check-capture-base.mjs`
  after extending it for the adopted inline-builder surface, because `renderers-ui` still has no dedicated test runner and that script is the real package-local invariant check we currently have
- focused code-backed equivalence review across the eight adopters to confirm:
  - same title-segment composition
  - same raw defaults
  - same raw identity fallback
  - same renderer-local fields remain local

If the packaged tarball is rebuilt and consumed locally in Critic, rerun focused host tests only for surfaces that exercise package `SubRenderers` backed by the migrated builders.

The verification posture here should remain:

- no heavy new harness
- no pretend package-wide proof
- enough build and consumer evidence to confirm the utility still preserves current behavior on the adopted surface

## Strategic Meaning

This is the next honest substrate-thinning step after the top-level pilot.

If it works, it proves:

- the smaller package-native shell does not only fit the top-level trio
- it also fits the current inline `SubRenderers` builders that make up the dominant deferred package capture surface

That would materially strengthen the shared-package story without overclaiming full convergence, because the forwarding asymmetries would still remain explicit.

If it fails cleanly, that is also useful:

- it would show that the top-level trio was the ceiling of honest extraction for now
- and that even the smaller shell should remain only partially adopted until runtime-threading is normalized first
