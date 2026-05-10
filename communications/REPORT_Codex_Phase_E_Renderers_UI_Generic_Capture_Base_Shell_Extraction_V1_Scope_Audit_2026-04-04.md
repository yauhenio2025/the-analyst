# Report: Phase E Renderers-UI Generic Capture-Base Shell Extraction V1 Scope Audit

Date: 2026-04-04
Reviewer: Codex
Scope Under Review:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_scope.md`

## Verdict

**Approve with corrections.**

The memo is asking the right next question, and the central direction survives direct code inspection: after the readiness slice rejected unchanged promotion of Critic's `currentRendererCapture`, the next honest move is a smaller package-neutral capture-base shell inside `renderers-ui`, not export of Critic-local first-hop, workflow, or typed-selection law.

But three parts of the scope need tightening:

- the "top-level-only" framing is honest only as a deliberately partial first tranche, not as a representative picture of the package capture surface
- the memo understates two real package-side propagation gaps already visible in code:
  - `AccordionRenderer` forwards only part of the runtime into nested sub-renderers
  - `CardRenderer` nested subsection paths do not thread capture config at all
- the verification section overstates current package test reality; `renderers-ui` has no test script or test files today

Focused verification I ran before writing this audit:

- `npm run build` in `/home/evgeny/projects/analyzer-v2/renderers-ui`
- Result: passed
- Additional reality check: `renderers-ui/package.json` defines no `test` script, and `rg --files renderers-ui | rg 'test|spec'` returned no files

## What The Memo Gets Right

- The candidate-language is mostly calibrated correctly. The memo does not overclaim unchanged helper promotion. That is consistent with the actual Critic helper in `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:1-85`, which still depends on:
  - Critic-local `CaptureSelection` typing
  - `_captureViewName`
  - `_firstHopAffordance?.capturable === true`
  - optional `requireWorkflowKey`
  - optional `requireJobId`
  - helper-owned `source_workflow_key`
  - `"<view_name>: <title>"` title law
- The memo is also right that `renderers-ui` already has a package-native raw capture architecture worth converging instead of bypassing. The current top-level package builders all resolve the same raw config inputs and emit the same base fields inline:
  - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/AccordionRenderer.tsx:105-113` and `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/AccordionRenderer.tsx:370-380`
  - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardRenderer.tsx:150-156` and `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardRenderer.tsx:281-294`
  - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardGridRenderer.tsx:181-188` and `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardGridRenderer.tsx:524-545`
- The proposed extracted shell is close to the smallest honest reusable unit. The real shared base in current package code is:
  - raw runtime resolution from `_captureMode`, `_onCapture`, `_captureViewKey`, `_captureSourceType`, optional `_captureJobId`, optional `_captureEntityId`
  - `source_view_key`
  - `source_type`
  - `context_title` composed with the package's `>` chain convention
  - optional `captureEntityId || captureJobId` fallback
- The memo is right to keep these concerns Critic-local:
  - typed `CaptureSelection`
  - `_firstHopAffordance` gating
  - `requireWorkflowKey`
  - `requireJobId`
  - `source_workflow_key`
  - `genealogy_job_id`
  - human-readable `view_name` + `:` title law
  - renderer-specific preview, identity, and specialization logic

## The Memo's Weakest Assumptions

- The top-level-only framing is directionally useful but too cleanly phrased. The current package has **11** inline capture emitters:
  - 3 top-level emitters:
    - `AccordionRenderer`
    - `CardRenderer`
    - `CardGridRenderer`
  - 8 sub-renderer emitters in `SubRenderers.tsx` at:
    - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx:675-689`
    - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx:878-891`
    - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx:1478-1492`
    - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx:2032-2045`
    - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx:2299-2312`
    - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx:2516-2529`
    - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx:2975-2988`
    - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx:3244-3257`
  So the real package weight still lives in `SubRenderers`, not in the three top-level renderers.
- `AccordionRenderer` already fans directly into that deferred `SubRenderers` surface, but its capture forwarding is incomplete. It forwards:
  - `_captureMode`
  - `_onCapture`
  - `_captureJobId`
  - `_captureViewKey`
  - `_parentSectionKey`
  - `_parentSectionTitle`
  at `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/AccordionRenderer.tsx:517-523`
  It does **not** forward:
  - `_captureSourceType`
  - `_captureEntityId`
  That means the package's nested capture surface does not currently receive the full raw runtime shape that the memo describes as package-common.
- `CardRenderer` has a second deferred capture surface beyond the top-level card button. Its nested subsection dispatch path passes only `hint.config` or `{}` into configured or auto-detected sub-renderers:
  - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardRenderer.tsx:348-381`
  No capture config is threaded there. That supports deferral, but it also means the memo should not imply that top-level-only adoption says much about nested package capture behavior.

## Factual Corrections

- The memo's proposed verification is too optimistic about current package harnesses. The package currently exposes only:
  - `build`
  - `watch`
  - `release:pack`
  - `prepublishOnly`
  in `/home/evgeny/projects/analyzer-v2/renderers-ui/package.json`
  It does not define a `test` script, and there are no `test` or `spec` files under `renderers-ui`.
- Because of that, the current honest verification bar for this slice is:
  - package build passes
  - and either:
    - new focused package tests are added as part of the slice
    - or a local package-consumer regression is run after rebuilding the tarball
  The memo should not assume existing package tests are already there.

## Explicit Answers To The Prompted Questions

### 1. Is the new candidate-language calibrated correctly, or does any part still overclaim package-side proof?

Mostly calibrated correctly.

The strongest claim remains honest:

- do not promote `currentRendererCapture` unchanged
- extract only a smaller raw package-neutral shell if anything

The overclaim risk is narrower:

- the memo should not imply that top-level-only adoption materially proves package-wide capture convergence
- it proves only that a first top-level tranche exists

### 2. Is top-level-only adoption a genuinely honest first subset, or does the weight of `SubRenderers` make that framing misleading?

It is an honest first subset, but only if described more tightly.

The honest framing is:

- this is the smallest convenient package-owned tranche
- not:
  - the main package capture surface

Why:

- 8 of 11 current inline emitters live in `SubRenderers`
- `AccordionRenderer` already routes into that deferred surface
- `CardRenderer` has an unthreaded nested subsection surface of its own

So "top-level-only" is acceptable as a bounded first move, but misleading if treated as evidence that the package-common law is mostly top-level already.

### 3. Is the proposed utility/API actually the smallest reusable package-neutral shell?

Broadly yes.

The memo's two-function shape is a defensible smallest shell if it owns only:

- raw runtime resolution
- `>`-based context-title composition from caller-supplied segments
- base-field assembly for:
  - `source_view_key`
  - `source_type`
  - `context_title`
  - optional `captureEntityId || captureJobId`

It should **not** own:

- `parent_context`
- `source_section_key`
- `source_item_index`
- `selected_text`
- `structured_data`
- `depth_level`
- `source_renderer_type`
- nested propagation policy

That last point matters because the current top-level builders and nested surfaces do not propagate runtime uniformly.

### 4. What exact concerns still need to stay Critic-local?

These still need to stay Critic-local based on the current code:

- `CaptureSelection` typing from `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:17-35`
- `CurrentRendererCaptureRuntime` as defined in `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:3-11`
- `_captureViewName` and `"<view_name>: <title>"` title law from `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:35` and `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:81`
- `_firstHopAffordance` fail-closed gating from `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:40-46` and threaded from `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:589-597`
- `requireWorkflowKey` / `requireJobId` policy from `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:13-15` and `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:48-52`
- `source_workflow_key`
- `genealogy_job_id`
- renderer-specific preview text
- renderer-specific identity rules
- renderer-specific `parent_context` policy
- renderer-specific status/readback behavior

### 5. Does the next roadmap recommendation still hold after inspecting the code?

Yes.

The roadmap recommendation still holds and is reinforced by the code:

- the next honest cross-repo move is one bounded `renderers-ui` generic capture-base shell extraction slice

That remains aligned with:

- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

But the completion criteria should be phrased more carefully:

- land one package-neutral shell
- adopt it in the three direct top-level builders
- explicitly defer the larger `SubRenderers` and nested-propagation surfaces
- do not claim package-wide capture convergence yet

## Most Defensible Scope Corrections

- Keep the current bounded extraction target.
- Replace the memo's stronger top-level subset language with:
  - this is a deliberately partial first tranche chosen for boundedness, while most current package emitters still live in `SubRenderers`
- Add one explicit note that package-side nested propagation is still unresolved:
  - `AccordionRenderer` forwards only part of the runtime into nested sub-renderers
  - `CardRenderer` subsection dispatch does not thread capture config at all
- Tighten the success criteria from:
  - "emitted raw selection payloads stay behaviorally equivalent"
  to:
  - emitted raw selection payloads stay behaviorally equivalent for the three direct top-level adopters, while nested surfaces remain explicitly out of scope
- Tighten the verification section to reflect current repo reality:
  - build is current baseline
  - tests or consumer regression must be added if behavioral equivalence is part of the proof claim

## Bottom Line

The scope is worth doing, and it is still the right next Phase E move.

The most honest completed judgment is:

- approve the bounded `renderers-ui` generic capture-base shell extraction direction
- correct the memo so it stops implying that top-level-only adoption says more about the whole package than it really does
- keep first-hop, workflow, typed-selection, and renderer-specific policy local
- and treat this slice as a narrow package-owned shell extraction, not as proof that package capture law is now generally solved
