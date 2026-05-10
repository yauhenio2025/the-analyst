# Memo: Phase E Genealogy V2 Idea Evolution First-Hop Capture Alignment V1 Scope

Subtitle: One bounded host-only non-AOI follow-on should align `genealogy_idea_evolution` to the already-landed `currentRendererCapture` seam now that analyzer-side generic first-hop affordance eligibility is complete

Date: 2026-04-03
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Most Recent Code Completion:
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_completion.md`
Prerequisite Host Helper Completion:
- `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`
Most Recent Smaller Non-AOI Consumer Completion:
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`
Earlier Scope Review Context:
- `communications/REPORT_Codex_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Audit_2026-04-03.md`
- `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Critique_2026-04-03.md`
Host Codebase:
- `/home/evgeny/projects/the-critic`

## Purpose

Define the actual next bounded step after the analyzer-side blocker was removed.

The question is no longer:

- should analyzer-v2 make `genealogy_idea_evolution` first-hop-affordance-eligible at all

That is now complete.

The next bounded question is:

- can the last materially broader current non-AOI renderer, `IdeaEvolutionRenderer`, consume the already-landed current-renderer capture seam and the now-truthful generic first-hop affordance without forcing helper exceptions or fake generic law claims?

## Why This Is The Right Next Step

`IdeaEvolutionRenderer` is now the clearest remaining current-renderer outlier after the bounded helper seam and the bounded analyzer-side eligibility prerequisite both landed.

The helper seam already covers:

- `AoiSinFindingsRenderer`
- `AoiThemeFindingsMiniCardList`
- `SynthesisRenderer`

The analyzer-side blocker is now gone too:

- `genealogy_idea_evolution` now receives generic `first_hop_affordance`
- that eligibility is bounded and honest:
  - `view_key = "genealogy_idea_evolution"`
  - `engine_key = "concept_synthesis"`
  - leaf only

So the remaining gap is now purely host consumption again.

That makes this the smallest honest next move because:

- it broadens the non-AOI current-renderer matrix one more step
- it reuses the landed helper instead of inventing new substrate
- it stays host-only
- it does not reopen analyzer or backend semantics

## Current Host Gap

The current host gap in [IdeaEvolutionRenderer.tsx](/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx) is broader than just missing affordance gating.

Today the renderer still:

- gates on local `captureMode && onCapture`
- reads only:
  - `_captureJobId`
  - `_captureViewKey`
- hardcodes:
  - `source_type = "genealogy"`
  - `context_title = "${captureViewKey || 'Ideas'} > ${idea.idea_name}"`
- omits:
  - `source_workflow_key`
  - `entity_id`

The implementation delta is therefore broader than a gate swap.
Beyond the current local capture reads, this alignment will newly consume five additional threaded runtime fields through the shared helper path:

- `_captureViewName`
- `_captureSourceType`
- `_workflowKey`
- `_captureEntityId`
- `_firstHopAffordance`

That last point needs one explicit calibration:

- the helper/runtime may carry `_captureEntityId`
- this renderer should **not** use it for emitted `entity_id`
- item-level `entity_id` on this surface should be pinned directly to `idea.idea_id`

The existing helper seam already supports what this renderer needs without helper changes:

- `resolveCurrentRendererCaptureRuntime(...)`
- `buildCurrentRendererCaptureSelection(...)`
- `requireWorkflowKey: true`
- `requireJobId: true`

So the real host question is now:

- can this renderer stop using its local ad hoc selection assembly and instead consume the shared seam honestly while preserving its narrow idea-card boundary?

## Current Surface Boundary

The in-scope surface is:

- Critic view key `genealogy_idea_evolution`
- renderer file:
  - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx`

Current capture coverage is intentionally narrower than the whole page and should stay that way in this slice.

Buttons exist only on:

- idea cards

Buttons do not currently exist on:

- the narrative-structure hero
- bifurcation nodes
- timeline entries
- prior-work trace subrows
- indirect enablers / foundational-pattern cards
- cross-domain transfer cards
- cross-cutting summary blocks

This slice should preserve that narrow coverage exactly.

## Proposed Implementation

### 1. Reuse the landed helper seam

Update `IdeaEvolutionRenderer` to consume:

- `resolveCurrentRendererCaptureRuntime(...)`
- `buildCurrentRendererCaptureSelection(...)`

Do not create a new helper.
Do not widen the helper unless a real gap appears.

### 2. Gate on truthful shared runtime

Replace the renderer-local `captureMode && onCapture` gate with helper-resolved runtime truth.

For this renderer, the honest runtime requirement is:

- capture mode on
- capture handler present
- capture view key present
- capture view name present
- capture source type present
- `_workflowKey` present
- `_captureJobId` present
- `_firstHopAffordance?.capturable === true`

This should use the helper with:

- `requireWorkflowKey: true`
- `requireJobId: true`

### 3. Keep selection coverage explicitly narrow

Do not broaden capture to the entire renderer.

Keep capture available only on the existing idea-card buttons.
Do not add buttons in this slice to:

- the hero summary
- bifurcation nodes
- timeline entries
- prior-work trace subrows
- foundational-pattern cards
- cross-domain transfer cards
- summary blocks

### 4. Align emitted selection truth

On click, emit a normal `CaptureSelection` through the shared helper shell with renderer-local fields.
Use the builder the way it is designed:

- pass `title = idea.idea_name`
- let `buildCurrentRendererCaptureSelection(...)` compose `context_title` internally
- do **not** prebuild the full `context_title` string in the renderer

The emitted selection should then carry:

- `source_type = _captureSourceType`
- `source_view_key = _captureViewKey`
- `source_workflow_key = _workflowKey`
- `source_renderer_type = "idea_evolution"`
- `content_type = "item"`
- `genealogy_job_id = _captureJobId`
- `entity_id = idea.idea_id`
- `depth_level = "L2_element"`

Keep the existing local payload shape unless there is a narrowly justified correction:

- bounded preview text from `idea_name + description`
- structured payload shaped from the current idea/synthesis/traces data

`source_type` must continue to resolve to the exact existing downstream value on this path.
The tests should pin that it still resolves to:

- `"genealogy"`

This is a composability improvement, not a runtime behavior change.
The current host-level source-type heuristic in `V2TabContent` remains unchanged.

### 5. Keep identity claims honest

`entity_id = idea.idea_id` is the smallest honest renderer-local identity available on this surface.

But the memo and tests should say explicitly:

- this is current rendered idea identity, not cross-run stable canonical identity
- it is not a replacement for `genealogy_job_id`
- it does not prove non-AOI read-side identity semantics are solved

### 6. Preserve reading behavior

Do not redesign the renderer.
Preserve:

- V1/V2 normalization behavior
- prose/fallback rendering behavior
- expand/collapse behavior
- current card layout
- existing `CaptureActionBar` handoff boundary

Keep `stopPropagation()` on the capture control so expanding/collapsing the card does not fire accidentally.

### 7. Accept bounded UX deltas only where contract truth requires them

One visible title-shape change is acceptable if this slice lands.

Current local behavior is effectively:

- raw view-key / fallback driven title composition:
  - `captureViewKey || "Ideas"`

The aligned selection should instead use the shared helper shell:

- `"<_captureViewName>: <idea idea_name>"`

That should be named as a small bounded UX artifact, not treated as invisible.
The change is dual:

- human-readable view name instead of raw `view_key` slug
- `:` separator instead of `>`

## What This Slice Is Not

This is not:

- generic current-renderer law
- generic renderer-package law
- backend or persistence work
- analyzer-side eligibility work
- genealogy read-side truth surfacing
- destination-policy consumption
- multi-renderer genealogy cleanup

It is one bounded host-side alignment on the last materially broader current-renderer outlier.

## Test Plan

### Focused renderer tests

`IdeaEvolutionRenderer.test.tsx` currently validates only normalization behavior.
This slice needs real component render infrastructure there, not just another pure-function assertion.
That is fresh test scaffolding work, not a small expansion of the existing file.

Add focused tests that prove:

1. capture buttons appear only on idea cards
2. capture buttons stay absent on the hero and other non-card subsections
3. buttons stay hidden when `_firstHopAffordance` is absent
4. buttons stay hidden when `_firstHopAffordance.capturable === false`
5. buttons stay hidden when `_workflowKey` is missing
6. buttons stay hidden when `_captureJobId` is missing
7. clicking an idea-card capture emits:
   - `source_type = "genealogy"` via config
   - `source_view_key`
   - config-derived `context_title`
   - `source_workflow_key`
   - `genealogy_job_id`
   - `entity_id = idea.idea_id`
   - `source_renderer_type = "idea_evolution"`
   - `content_type = "item"`
   - `depth_level = "L2_element"`
8. capture button `stopPropagation()` prevents accidental card expand/collapse

### Keep adjacent seams green

Keep these green:

- `src/lib/currentRendererCapture.test.ts`
- `src/components/V2TabContent.test.tsx`
- `src/contexts/CaptureContext.test.tsx`

### Browser proof

Add one focused Playwright proof on the live genealogy idea-evolution page for the positive path only.

Verify:

- idea-card capture control appears in capture mode
- clicking it reaches `CaptureActionBar`
- the action bar shows:
  - title
  - preview text
  - depth badge
  - action buttons

Do not require a breadcrumb unless parent context is intentionally added.

Cover the no-affordance negative only in unit tests or mocked / fixture-backed browser proof, not by claiming the untouched live page naturally exposes both states.
Do not expand the live browser claim beyond the positive path.

## Assumptions And Defaults

- `IdeaEvolutionRenderer` is now the smallest honest remaining current-renderer outlier after the helper extraction and the analyzer-side eligibility prerequisite both landed.
- The existing helper is already the right seam to reuse here unless implementation proves otherwise.
- `idea_id` is honest enough for renderer-local emitted `entity_id` on this surface, but not a claim of cross-run stable genealogy identity.
- The value here is one more non-AOI current-renderer data point toward generic selection-emission parameterization, not generic renderer law itself.

## Decision Rule

If the implementation requires widening the helper with renderer-specific branches beyond:

- configurable workflow requirement
- configurable job requirement

then stop and recalibrate rather than forcing a dishonest abstraction.

The intended outcome is:

- one more bounded host-only renderer alignment

not:

- a fake generic capture framework.
