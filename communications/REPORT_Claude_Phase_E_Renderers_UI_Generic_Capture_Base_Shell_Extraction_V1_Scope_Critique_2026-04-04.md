# Critique: Phase E Renderers-UI Generic Capture-Base Shell Extraction V1 Scope

Date: 2026-04-04
Reviewer: Claude (Opus 4.6)

Scope Under Review:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_scope.md`

Prior Context Reviewed:
- `communications/MEMO_2026-04-04_phase_e_current_renderer_selection_emission_shared_seam_promotion_readiness_v1_completion.md`
- `communications/REPORT_Codex_Phase_E_Current_Renderer_Selection_Emission_Shared_Seam_Promotion_Readiness_V1_Scope_Audit_2026-04-04.md`
- `communications/REPORT_Claude_Phase_E_Current_Renderer_Selection_Emission_Shared_Seam_Promotion_Readiness_V1_Scope_Critique_2026-04-04.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`

Codebase Files Inspected:
- `renderers-ui/package.json`
- `renderers-ui/src/index.ts`
- `renderers-ui/src/types/index.ts`
- `renderers-ui/src/renderers/AccordionRenderer.tsx` (full file, 609 lines)
- `renderers-ui/src/renderers/CardRenderer.tsx` (full file, 517 lines)
- `renderers-ui/src/renderers/CardGridRenderer.tsx` (full file, 608 lines)
- `renderers-ui/src/sub-renderers/SubRenderers.tsx` (capture grep across full file, 3253+ lines; focused read of representative inline builders)
- `the-critic/webapp/src/lib/currentRendererCapture.ts` (full file, 85 lines)
- `the-critic/webapp/src/contexts/CaptureContext.tsx` (lines 1-60)
- `the-critic/webapp/src/components/V2TabContent.tsx` (lines 570-619)

## Verdict

**Approve.**

The scope is honest, bounded, code-backed, and strategically correct. The boundary between what should be extracted and what must stay out is well-drawn and survives direct inspection against the actual inline builders. This is one of the cleaner extraction scopes in the Phase E sequence.

## The Memo's Strongest Points

### 1. The extraction target maps precisely to observed code

I inspected all three proposed adopters' inline capture builders. Their actual inline patterns converge tightly on the proposed shell:

| Renderer | Config reading | Title composition | Identity fallback | Gate |
| --- | --- | --- | --- | --- |
| AccordionRenderer (lines 106-113, 370-381) | `_captureMode`, `_onCapture`, `_captureJobId`, `_captureViewKey`, `_captureSourceType`, `_captureEntityId` | `captureViewKey > section.title` | `captureEntityId \|\| captureJobId \|\| ''` | `captureMode && onCapture` |
| CardRenderer (lines 150-157, 281-300) | identical set | `captureViewKey > parentSectionTitle > title` or `captureViewKey > title` | `captureEntityId \|\| captureJobId \|\| ''` | `captureMode && onCapture` |
| CardGridRenderer (lines 181-188, 534-551) | identical set | `captureViewKey > parentSectionTitle > title` or `captureViewKey > title` | `captureEntityId \|\| captureJobId \|\| ''` | `captureMode && onCapture` |

Every dimension matches the proposed `resolvePackageCaptureBaseRuntime` / `buildPackageCaptureSelectionBase` API shape. The memo is not hypothesizing a shared base — it is describing the one that already exists inline.

### 2. The exclusion list is code-accurate

I verified each excluded concern against the Critic-local helper:

- `_firstHopAffordance`: present in `currentRendererCapture.ts:40,45-46` — absent from all three package renderers
- `_captureViewName`: present in `currentRendererCapture.ts:35` — absent from all three package renderers (they use `_captureViewKey` for title composition)
- `requireWorkflowKey` / `requireJobId`: present in `currentRendererCapture.ts:48-53` — no equivalent in any package renderer
- `source_workflow_key`: built in `currentRendererCapture.ts:82` — absent from all three package renderers
- `CaptureSelection` type: imported in `currentRendererCapture.ts:1` — all package renderers use `Record<string, unknown>` instead (explicitly declared in `SubRenderers.tsx:36`)

The two title composition laws are genuinely divergent:
- Critic-local: `captureViewName: title` (colon-separated, with human-readable view name)
- Package: `captureViewKey > segment > segment` (chevron-chained, with config key)

The memo's exclusion list is not aspirational — it reflects real current architectural divergence.

### 3. The "partial first extraction proof" framing is calibrated correctly

The memo does not claim this solves the whole package capture convergence story. It claims exactly one thing: that the three top-level renderers share a smaller common base that can be factored out. That claim is code-true.

### 4. The readiness completion memo's verdict flows correctly into this scope

The previous readiness slice concluded:
- `currentRendererCapture` is not promotion-ready unchanged
- a smaller package-neutral capture-base shell is the next honest extraction candidate

This scope scopes exactly that smaller shell and nothing more. There is no scope creep from the readiness verdict.

## Pressure Tests

### Test 1: Is the top-level-renderer-only slice a valid partial first proof?

**Yes.**

The three top-level renderers express one clean pattern family: they read capture config from `config._*` props, compose a raw selection, and call `onCapture`. They do not delegate to each other for capture. Each builds its own selection inline.

Extracting the shared base from these three is self-contained and does not require any SubRenderer changes, because the top-level renderers' capture code does not call SubRenderer capture code — the two are independent code paths.

### Test 2: Is deferring SubRenderers still strategically honest given how much raw capture logic lives there?

**Yes, but the memo should be more explicit about why.**

I counted 8+ SubRenderers with their own inline capture builders in `SubRenderers.tsx` (DefinitionList at line 670+, MiniCardList at line 878+, IntensityMatrix at line 1478+, MoveRepertoire at line 2032+, DialecticalPair at line 2516+, PhaseTimeline at line 2975+, RichDescriptionList at line 2299+, AnnotatedProse at line 3244+). These SubRenderers share the same pattern as the top-level renderers:

- identical config key reading (`_captureMode`, `_onCapture`, `_captureJobId`, `_captureViewKey`, `_captureSourceType`, `_captureEntityId`)
- identical `>` title composition
- identical `captureEntityId || captureJobId || ''` identity fallback
- identical `captureMode && onCapture` gating
- additional `_parentSectionKey` and `_parentSectionTitle` forwarded from top-level renderers

This means the proposed package utility would work for SubRenderers too, with zero API changes. The deferral is honest because:

1. it keeps v1 blast radius bounded
2. the SubRenderer adoption would be a mechanical follow-on, not a design change
3. proving the extraction on 3 top-level renderers first lets us validate the API before widening

But the memo should explicitly state that the SubRenderer pattern is already known to match, so the follow-on is mechanical rather than architectural.

### Test 3: Is the proposed package-neutral shell too broad or too narrow?

**Correctly sized.**

Too narrow would be: extracting only config reading without the selection-base builder. That would leave the inline emission code duplicated with no reduction.

Too broad would be: pulling in parent-context policy, depth-level determination, or content-type resolution. Those are renderer-specific concerns that vary per adopter.

The proposed shell extracts exactly the config-to-runtime resolution and the shared selection-base assembly (source_view_key, source_type, context_title, entity_id fallback). That is the actual common denominator I observed across all three renderers.

One observation: `_captureMode` gating is used consistently as the top-level guard (`captureMode && onCapture`) across all three renderers. The proposed `resolvePackageCaptureBaseRuntime` should resolve to `null` when `_captureMode` is falsy or `_onCapture` is absent, matching the current inline pattern. The memo's config listing includes `_captureMode` and `_onCapture`, which implies this, but the runtime interface description does not explicitly state the null-return-on-disabled behavior. This is minor — the implementation will naturally adopt this pattern from the existing code.

### Test 4: Does the proposed utility actually fit the existing package's `Record<string, unknown>` capture style?

**Yes.**

The proposed utility:
- reads `config._*` props (already the existing convention in all three renderers)
- returns a `Record<string, unknown>` selection base (matches `SubRenderers.tsx:36` declaration)
- composes `context_title` with `>` chains (matches `AccordionRenderer.tsx:377`, `CardRenderer.tsx:291`, `CardGridRenderer.tsx:542`)
- uses `captureEntityId || captureJobId || ''` for identity (matches all three adopters)

No Critic-local type imports. No `CaptureSelection` interface dependency. The utility would be a natural package citizen.

### Test 5: Will the emitted payloads stay behaviorally equivalent?

**Yes, with one caveat.**

The extraction replaces inline code with utility calls. The emitted fields should be identical because the utility is a mechanical extraction of the existing inline code, not a redesign.

Caveat: each renderer currently adds renderer-specific fields beyond the shared base (`source_section_key`, `source_item_index`, `source_renderer_type`, `content_type`, `selected_text`, `structured_data`, `depth_level`, `parent_context`). The proposed `buildPackageCaptureSelectionBase` returns only the shared base, and each adopter spreads their renderer-specific fields on top. This is the correct architecture — the utility owns the base, the caller owns the specifics.

## What The Memo Gets Right That Prior Memos Sometimes Did Not

1. **No overclaim about generality**: The memo does not claim this solves renderer-package capture law. It claims one bounded extraction proof.

2. **Explicit fail condition**: "If extraction pressure starts forcing first-hop or workflow/job policy into the package utility, stop and recalibrate."

3. **Explicit deferred scope**: SubRenderers, Critic deletion, universal contract — all explicitly named as out of scope.

4. **Strategic meaning stated honestly**: Both the success meaning ("smaller honest package-owned shell exists") and the failure meaning ("even the smaller shell is not stable enough") are given.

## Minor Observations (Not Corrections)

### 1. The `context_title` composition has a slight variance across the three adopters

- AccordionRenderer: `captureViewKey || 'Analysis'` > `section.title || section.key`
- CardRenderer: `captureViewKey || 'Analysis'` > optional `parentSectionTitle` > `title`
- CardGridRenderer: `captureViewKey || 'Analysis'` > optional `parentSectionTitle` > `title`

The proposed utility should take title segments as an array and join with ` > `, with the first segment defaulting to `captureViewKey || 'Analysis'`. This is what the memo describes ("caller-supplied title segments with the package's current `>` convention"), but worth confirming during implementation.

### 2. `_captureStatusMap` is an AccordionRenderer-only concern

`AccordionRenderer.tsx:114-118` reads `_captureStatusMap` for status dots on sections. This is unrelated to capture emission and correctly absent from the proposed extraction scope.

### 3. The SubRenderer pattern adds `_parentSectionKey` / `_parentSectionTitle`

These are forwarded from top-level renderers (e.g., `AccordionRenderer.tsx:522-523`) into SubRenderers via config, and used for title composition and `parent_context` assembly. They are caller-supplied context fields, not package-utility responsibilities. The proposed utility's title-segment API naturally accommodates this.

## Strategic Implications

### Positive alignment

This scope aligns with the distilled roadmap's anti-drift rules:

- **Rule 1** (prefer upstream intelligence over downstream convenience): The extraction moves shared capture resolution into the analyzer-v2-owned package rather than leaving it duplicated inline.
- **Rule 3** (build substrate, not proof-of-concept per engine): The utility would serve any renderer that needs capture, not just these three.
- **Rule 4** (prefer representative matrices over exhaustive theater): Three adopters spanning three different capture shapes (section, card, card-grid) is representative.

### The follow-on path is visible

If this extraction succeeds:
1. SubRenderer adoption is mechanical (same pattern, same API)
2. The Critic-local `currentRendererCapture` can eventually compose on top of the package base (its `source_type`, `source_view_key`, `context_title` overlap with the package base; it adds `_firstHopAffordance` gating and `source_workflow_key`)
3. But that composition step is a separate future scope, not this one

### Risk profile

This is a low-risk extraction:
- No cross-repo changes required
- No type system changes (stays `Record<string, unknown>`)
- No API contract changes (emitted payload shapes are unchanged)
- Bounded blast radius (3 files)
- Clear rollback path (revert to inline code)

## Bottom-Line Recommendation

**Approve as scoped.**

The extraction boundary is honest, the proposed API maps precisely to the observed inline code, the exclusion list is code-accurate, and the three-adopter slice is a valid partial first proof. The deferral of SubRenderers is strategically clean even though they share the same pattern — proving the extraction on top-level renderers first is disciplined.

No corrections required. The scope is ready for implementation.
