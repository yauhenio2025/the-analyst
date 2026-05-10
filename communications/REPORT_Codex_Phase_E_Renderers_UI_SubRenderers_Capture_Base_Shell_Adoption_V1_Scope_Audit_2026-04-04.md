# Report: Phase E Renderers-UI SubRenderers Capture-Base Shell Adoption V1 Scope Audit

Date: 2026-04-04
Reviewer: Codex
Scope Under Review:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_scope.md`

## Context Check

Read before concluding:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_scope.md`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_completion.md`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_scope.md`
- `communications/REPORT_Codex_Phase_E_Renderers_UI_Generic_Capture_Base_Shell_Extraction_V1_Scope_Audit_Rerun_2026-04-04.md`
- `communications/REPORT_Claude_Phase_E_Renderers_UI_Generic_Capture_Base_Shell_Extraction_V1_Scope_Critique_Rerun_2026-04-04.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Code inspected directly:
- `renderers-ui/package.json`
- `renderers-ui/src/utils/captureBase.ts`
- `renderers-ui/src/renderers/AccordionRenderer.tsx`
- `renderers-ui/src/renderers/CardRenderer.tsx`
- `renderers-ui/src/renderers/CardGridRenderer.tsx`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx`
- `renderers-ui/scripts/check-capture-base.mjs`
- `../the-critic/webapp/package.json`

Focused verification rerun:
- `npm run build` in `renderers-ui` — passed
- `node scripts/check-capture-base.mjs` in `renderers-ui` — passed
- current warning still present and unchanged: `MODULE_TYPELESS_PACKAGE_JSON` when the script imports `dist/utils/captureBase.js`

## Verdict

**Approve with corrections.**

The direction is right. The real remaining inline capture-builder mass is now the eight capture-enabled builders in `renderers-ui/src/sub-renderers/SubRenderers.tsx`, and the current shared utility is already sized correctly for that surface. The memo also correctly keeps forwarding normalization out of scope and preserves the current forwarded defaults rather than pretending to fix them.

The needed corrections are calibration corrections, not a change of direction:

1. tighten the proof language so this slice is described as proving utility fit across the current inline `SubRenderers` builders, not as proving broader nested runtime coverage
2. tighten the verification wording so it explicitly extends and reruns the existing package script, because `renderers-ui` still has no dedicated test runner

## Code-Backed Findings

### 1. The scope matches the real remaining package capture architecture

The package-native utility is real and intentionally small in `renderers-ui/src/utils/captureBase.ts:22-53`.
It owns only:
- capture gating on `_captureMode === true` plus functional `_onCapture`
- raw reads of `_captureViewKey`, `_captureSourceType`, `_captureJobId`, `_captureEntityId`
- shared base assembly for `source_view_key`, `source_type`, `context_title`, and `entity_id`

The top-level pilot is also real:
- `AccordionRenderer` resolves the utility at `renderers-ui/src/renderers/AccordionRenderer.tsx:118` and emits through it at `renderers-ui/src/renderers/AccordionRenderer.tsx:370-380`
- `CardRenderer` resolves it at `renderers-ui/src/renderers/CardRenderer.tsx:150` and emits through it at `renderers-ui/src/renderers/CardRenderer.tsx:274-292`
- `CardGridRenderer` still captures in the inner wrapper, but that wrapper now resolves and emits through the utility at `renderers-ui/src/renderers/CardGridRenderer.tsx:524-550`

After that pilot, the remaining inline builders are concentrated in `SubRenderers`, not elsewhere. A package-wide grep of capture emission shows only:
- the three already-migrated top-level renderers
- eight still-inline builders in `renderers-ui/src/sub-renderers/SubRenderers.tsx`

Those eight builders are exactly:
- `DefinitionList` at `renderers-ui/src/sub-renderers/SubRenderers.tsx:531`
- `MiniCardList` at `renderers-ui/src/sub-renderers/SubRenderers.tsx:721`
- `ComparisonPanel` at `renderers-ui/src/sub-renderers/SubRenderers.tsx:1373`
- `IntensityMatrix` at `renderers-ui/src/sub-renderers/SubRenderers.tsx:1863`
- `MoveRepertoire` at `renderers-ui/src/sub-renderers/SubRenderers.tsx:2138`
- `DialecticalPair` at `renderers-ui/src/sub-renderers/SubRenderers.tsx:2374`
- `RichDescriptionList` at `renderers-ui/src/sub-renderers/SubRenderers.tsx:2810`
- `PhaseTimeline` at `renderers-ui/src/sub-renderers/SubRenderers.tsx:3063`

So the memo is correct that `SubRenderers` is now the dominant deferred inline builder surface.

### 2. `SubRenderers` is the right next bounded surface for substrate thinning, but not for runtime-coverage claims

The eight inline builders all repeat the same raw capture base:
- `DefinitionList` reads capture config at `renderers-ui/src/sub-renderers/SubRenderers.tsx:537-544` and emits inline at `renderers-ui/src/sub-renderers/SubRenderers.tsx:675-692`
- `MiniCardList` does the same at `renderers-ui/src/sub-renderers/SubRenderers.tsx:727-734` and `renderers-ui/src/sub-renderers/SubRenderers.tsx:878-895`
- the same pattern repeats for the other six builders at `1478-1495`, `2032-2048`, `2299-2315`, `2516-2532`, `2975-2989`, and `3244-3260`

That makes `SubRenderers` the right next bounded surface if the goal is:
- removing repeated package-local raw capture-base logic
- proving the utility fits the dominant remaining inline builder set
- strengthening analyzer-owned shared renderer substrate without importing Critic-local law

But this is not the same thing as increasing all nested user-visible capture coverage.

Why:
- `AccordionRenderer` forwards only `_captureMode`, `_onCapture`, `_captureJobId`, `_captureViewKey`, `_parentSectionKey`, and `_parentSectionTitle` at `renderers-ui/src/renderers/AccordionRenderer.tsx:516-523`
- it still does not forward `_captureSourceType` or `_captureEntityId`
- `CardRenderer` nested subsection dispatch still passes a plain `subConfig` with no capture runtime at `renderers-ui/src/renderers/CardRenderer.tsx:343-356`

So the next honest step is still `SubRenderers` adoption first, but only if the memo stays explicit that this is a builder-surface convergence slice, not a runtime-coverage slice.

### 3. Direct utility adoption is honest if it preserves current forwarded defaults exactly

The current `SubRenderers` builders already operate under the forwarded defaults produced by their parents.

That is visible in the inline builders:
- all eight use `captureViewKey || ''`
- all eight use `captureSourceType || 'analysis'`
- all eight use `captureEntityId || captureJobId || ''`
- several intentionally preserve empty title segments in `context_title`

Examples:
- `DefinitionList` builds `context_title` with `parentSectionTitle || ''` at `renderers-ui/src/sub-renderers/SubRenderers.tsx:683-685`
- `MoveRepertoire` uses a four-segment `>` chain at `renderers-ui/src/sub-renderers/SubRenderers.tsx:2306-2308`
- `DialecticalPair` uses a side label segment at `renderers-ui/src/sub-renderers/SubRenderers.tsx:2523-2525`
- `PhaseTimeline` includes the literal `"Phase: "` inside the caller-owned segment at `renderers-ui/src/sub-renderers/SubRenderers.tsx:3251-3253`

Those patterns map cleanly onto `buildPackageCaptureSelectionBase(runtime, { titleSegments })` in `renderers-ui/src/utils/captureBase.ts:42-53`.

So direct utility adoption is honest without bundled forwarding normalization, but only because the memo correctly says to preserve today's forwarded defaults rather than reinterpret them.

### 4. The proposed adopter set is precise and complete

The memo’s eight-adopter list at `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_scope.md:66-77` matches the actual inline capture-enabled builders exactly.

There are not hidden ninth or tenth adopters elsewhere in `SubRenderers`.
The capture-button grep in `renderers-ui/src/sub-renderers/SubRenderers.tsx` returns only the eight inline emission sites listed above.

This is one of the memo’s strongest points: the tranche boundary is real, concrete, and enumerable.

### 5. The memo stays below package-wide convergence claims, but one proof sentence should be tightened

The scope memo is mostly well-calibrated here:
- it explicitly says this slice is not package-wide convergence at `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_scope.md:33-39`
- it explicitly keeps forwarding asymmetry normalization out of scope at `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_scope.md:126-143`
- it explicitly keeps Critic-local first-hop/workflow/type law out at `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_scope.md:145-161`

The correction is at the strategic-proof edge.

The lines at `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_scope.md:207-212` are directionally right, but they should be read as:
- proof that the smaller package shell fits the current inline `SubRenderers` builders
- not proof that nested package capture architecture is now broadly converged

Reason:
- the inline builders can migrate while `AccordionRenderer` still omits `_captureSourceType` and `_captureEntityId`
- and while `CardRenderer` still leaves nested sub-renderers entirely outside capture runtime threading

That distinction should stay explicit in the memo text.

### 6. The top-level pilot did not prove forwarding normalization, package-wide law, or Critic-helper obsolescence

The completion memo was honest about what the top-level pilot proved, and the new scope mostly preserves that honesty.

The top-level pilot proved:
- the utility exists in real package code
- it fits the top-level trio
- the utility can preserve raw package defaulting and `>` title composition

It did not prove:
- `SubRenderers` migration
- forwarding normalization
- package-wide capture convergence
- that Critic can delete `currentRendererCapture`

That is consistent with the host-local helper still being broader and stricter in `../the-critic/webapp/src/lib/currentRendererCapture.ts:1-84`, where the helper still owns:
- typed `CaptureSelection`
- `_captureViewName`
- `_firstHopAffordance` fail-closed gating
- optional workflow/job requiredness
- `source_workflow_key`

The host still threads those fields at `../the-critic/webapp/src/components/V2TabContent.tsx:588-597`, and the helper tests still lock that behavior at `../the-critic/webapp/src/lib/currentRendererCapture.test.ts:21-114`.

So the memo is right to keep the next slice below any claim that the top-level pilot solved the full package/host seam.

### 7. The verification plan is honest in shape, but should be stated more concretely

`renderers-ui/package.json:11-16` still has no `test` script and no dedicated package test runner.
The actual package-local verification surface today is:
- `npm run build`
- `node scripts/check-capture-base.mjs`

That script currently checks the base-shell invariants directly in `renderers-ui/scripts/check-capture-base.mjs:11-118`:
- gate behavior
- raw empty-string preservation
- default fallbacks
- `>` title composition without empty-segment filtering
- explicit `entityId` precedence
- job-id fallback

That means the memo’s bounded verification posture is honest.
But the wording at `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_scope.md:185-201` should be slightly tighter:
- not “extend the script only if needed”
- instead “extend and rerun the existing script for the adopted surface, because that script is the real package-local invariant check we currently have”

This is a calibration correction, not a reason to reject the tranche.

## Roadmap Alignment

The next-step recommendation still holds after code inspection.

It matches the strategic documents:
- the distilled roadmap says the next bounded step should be one bounded `renderers-ui` `SubRenderers` capture-base shell adoption slice, while forwarding normalization remains a later decision at `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:429-443`
- the state-of-play memo says the top-level package pilot is complete and the next bounded scope should target `SubRenderers` while keeping broader concerns deferred at `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:452-486`
- the fixed-direction roadmap says downstream apps are thin hosts and the next cross-repo move is one bounded `SubRenderers` adoption slice, not another host-local widening at `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:14-18` and `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:529-532`
- the master roadmap still frames the destination as analyzer-owned intelligence with consumer apps as thin host shells at `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:48-56`

That strategic fit is real because this slice moves repeated capture-base behavior farther into analyzer-owned shared package code without importing Critic-local law into the package.

## Explicit Answers

- Is `SubRenderers` now the right dominant deferred surface, or is the next honest step actually forwarding normalization first?
  - `SubRenderers` is the right next surface for substrate thinning and utility adoption. Forwarding normalization is not the blocker for this tranche. It remains a separate follow-on decision after the dominant inline builder surface is converged.

- Does the memo preserve current forwarded defaults rather than accidentally promising runtime-threading fixes?
  - Yes. The memo explicitly preserves the current forwarded defaults and explicitly keeps `AccordionRenderer` and `CardRenderer` forwarding asymmetries out of scope.

- Is the proposed adopter set precise and complete for the current inline `SubRenderers` capture builders?
  - Yes. There are exactly eight current inline capture-enabled builders in `SubRenderers`, and the memo names all eight.

- Does the scope stay below package-wide convergence claims?
  - Mostly yes. The only correction is to keep proof language tied to inline-builder adoption, not broader nested runtime coverage.

- Is the verification plan honest enough given there is still no dedicated `renderers-ui` test runner?
  - Yes in shape, but it should be stated more concretely. The slice should explicitly extend and rerun `renderers-ui/scripts/check-capture-base.mjs` alongside `npm run build`.

- What exact concerns still need to remain outside this tranche?
  - forwarding normalization in `AccordionRenderer` and `CardRenderer`
  - export or public-promotion of `captureBase`
  - Critic-local typed `CaptureSelection`
  - `_captureViewName`
  - `_firstHopAffordance`
  - `requireWorkflowKey`
  - `requireJobId`
  - `source_workflow_key`
  - `genealogy_job_id`
  - read-side status expansion and destination-policy widening
  - analyzer/backend widening
  - package-wide convergence claims

- Does the next roadmap recommendation still hold after inspecting the code?
  - Yes. The next honest code gap is still one bounded `renderers-ui` `SubRenderers` capture-base shell adoption slice, followed only then by a decision on whether forwarding normalization still needs its own bounded tranche.

## Bottom Line

Approve this scope after two small corrections:

1. state explicitly that success proves utility fit across the current inline `SubRenderers` builders, not broader nested runtime coverage
2. state explicitly that verification will extend and rerun the existing `renderers-ui/scripts/check-capture-base.mjs` path, because that is the package’s real local invariant check today

With those corrections, the memo is honest, code-backed, and aligned with the analyzer-v2-as-brain direction.
