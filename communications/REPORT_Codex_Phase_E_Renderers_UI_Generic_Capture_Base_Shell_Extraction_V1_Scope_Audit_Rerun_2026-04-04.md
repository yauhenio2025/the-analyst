# Report: Phase E Renderers-UI Generic Capture-Base Shell Extraction V1 Scope Audit Rerun

Date: 2026-04-04
Reviewer: Codex
Scope Under Review:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_scope.md`

## Context Check

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_scope.md` — read in full
- `communications/MEMO_2026-04-04_phase_e_current_renderer_selection_emission_shared_seam_promotion_readiness_v1_completion.md` — read in full
- `communications/REPORT_Codex_Phase_E_Current_Renderer_Selection_Emission_Shared_Seam_Promotion_Readiness_V1_Scope_Audit_2026-04-04.md` — read in full
- `communications/REPORT_Claude_Phase_E_Current_Renderer_Selection_Emission_Shared_Seam_Promotion_Readiness_V1_Scope_Critique_2026-04-04.md` — read in full
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md` — read in full
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md` — read in full
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md` — read in full
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` — read in full

## Verdict

**Approve with corrections.**

The memo’s direction is still the right one. The package really does contain a smaller reusable raw capture base beneath the Critic helper, and the next honest move is still a bounded `renderers-ui` extraction rather than unchanged promotion of `currentRendererCapture`. But the memo is a little too clean about how representative the proposed first subset is. The top-level trio is a valid bounded pilot, yet the package’s actual capture weight still lives in `SubRenderers`, and that heavier surface is not just deferred volume. It already shows wiring asymmetry that weakens any broader package-side proof claim.

Focused verification used for this rerun:

- direct file inspection of the required memos and code files
- `rg` over `renderers-ui/src` to enumerate live package capture builders
- no new runtime tests were rerun, because the question here is scope honesty and architectural fit, not behavior change

## Code-Backed Findings

### 1. The scope mostly matches the real package capture architecture

The package-side common denominator is real in the three proposed adopters:

- `renderers-ui/src/renderers/AccordionRenderer.tsx:106-113` reads `_captureMode`, `_onCapture`, `_captureJobId`, `_captureViewKey`, `_captureSourceType`, `_captureEntityId`
- `renderers-ui/src/renderers/AccordionRenderer.tsx:363-380` emits raw selection fields with:
  - `source_view_key`
  - `source_type`
  - `context_title` using the package `>` convention
  - `entity_id` fallback `captureEntityId || captureJobId`
- `renderers-ui/src/renderers/CardRenderer.tsx:150-157` and `renderers-ui/src/renderers/CardRenderer.tsx:274-297` do the same, while leaving `depth_level` and `parent_context` local
- `renderers-ui/src/renderers/CardGridRenderer.tsx:181-188` and `renderers-ui/src/renderers/CardGridRenderer.tsx:524-546` do the same

So the memo is right about the core reusable shell: package-native config reading plus raw shared selection-base assembly is genuinely present.

### 2. The partial first-extraction boundary is honest only if it stays explicitly top-level

The package does not have three inline builders. It has eleven capture builders in the inspected source:

- 3 top-level renderers:
  - `AccordionRenderer`
  - `CardRenderer`
  - `CardGridRenderer`
- 8 capture-enabled sub-renderers inside `renderers-ui/src/sub-renderers/SubRenderers.tsx`
  - `DefinitionList`
  - `MiniCardList`
  - `ComparisonPanel`
  - `IntensityMatrix`
  - `MoveRepertoire`
  - `DialecticalPair`
  - `RichDescriptionList`
  - `PhaseTimeline`

The repeated sub-renderer pattern is visible at:

- `renderers-ui/src/sub-renderers/SubRenderers.tsx:537-542,675-689`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx:727-732,875-892`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx:1379-1384,1475-1492`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx:1867-1872,2029-2045`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx:2144-2149,2296-2312`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx:2379-2384,2517-2531`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx:2814-2819,2972-2988`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx:3067-3072,3241-3256`

So “top-level only” is a bounded subset, but not a representative package-wide one. The memo already says most builders remain in `SubRenderers`; that caveat is correct and needs to stay prominent.

### 3. `SubRenderers` is not just deferred mass; it is also a divergent wiring surface

Two details matter here.

First, `AccordionRenderer` only forwards a partial capture runtime into nested renderers:

- `renderers-ui/src/renderers/AccordionRenderer.tsx:516-523` forwards `_captureMode`, `_onCapture`, `_captureJobId`, `_captureViewKey`, `_parentSectionKey`, `_parentSectionTitle`
- it does **not** forward `_captureSourceType` or `_captureEntityId`

But the sub-renderers expect those fields:

- `renderers-ui/src/sub-renderers/SubRenderers.tsx:537-544`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx:727-734`

Second, `CardRenderer` subsection dispatch does not forward capture runtime into nested sub-renderers at all:

- `renderers-ui/src/renderers/CardRenderer.tsx:348-351`

That means the deferred surface is not merely “more adopters later.” It is a partly inconsistent runtime-threading surface. This strengthens the case for keeping v1 explicitly top-level and makes any broader proof language risky.

### 4. The proposed utility is close to the smallest reusable package-neutral shell

The memo’s proposed split:

1. `resolvePackageCaptureBaseRuntime(config)`
2. `buildPackageCaptureSelectionBase(runtime, params)`

is basically right.

Why it fits:

- package code uses `Record<string, unknown>` or equivalent local typing, not host imports
- package code does not use `_captureViewName`, `_firstHopAffordance`, `_workflowKey`, or `source_workflow_key`
- package code leaves `selected_text`, `source_renderer_type`, `depth_level`, `parent_context`, and renderer-specific identity choices to callers

The correction is semantic, not structural:

- the extracted package utility must preserve package behavior, not import Critic strictness
- it should not silently become fail-closed on missing `_captureViewKey` or `_captureSourceType` the way `currentRendererCapture` is
- it should preserve the package’s current raw fallback style:
  - `source_view_key: ''` if absent
  - `source_type: 'analysis'` if absent
  - `entity_id: captureEntityId || captureJobId`

So the utility shape is right, but the scope should explicitly say “preserve existing package defaulting” to avoid accidental Critic-law creep.

### 5. The prior readiness slice did not prove package extraction; it only proved the ceiling of the Critic helper

The actual helper contract is still Critic-local:

- `the-critic/webapp/src/lib/currentRendererCapture.ts:1-10` imports `CaptureSelection` and defines a typed host-local runtime
- `the-critic/webapp/src/lib/currentRendererCapture.ts:30-52` fail-closes on `_firstHopAffordance`, optional workflow requirement, and optional job requirement
- `the-critic/webapp/src/lib/currentRendererCapture.ts:73-84` emits `context_title` as `"<view name>: <title>"` and injects `source_workflow_key`
- `the-critic/webapp/src/components/V2TabContent.tsx:589-597` is what actually threads `_captureViewName`, `_captureSourceType`, `_captureEntityId`, and `_firstHopAffordance`

The locked tests prove only that local helper behavior:

- `the-critic/webapp/src/lib/currentRendererCapture.test.ts:22-45` locks the fail-closed helper requirements
- `the-critic/webapp/src/lib/currentRendererCapture.test.ts:48-113` locks the `View Name: Title` builder law, `source_workflow_key`, and optional `genealogy_job_id`

That is exactly why the readiness completion memo’s claim was only “narrower-shell candidate identified,” not “package-side proof established.” The new scope memo mostly stays honest on that point, but its candidate-language should stay narrower than package-wide proof.

### 6. The roadmap recommendation still holds

After the code inspection, the next roadmap step is still:

- one bounded `renderers-ui` generic capture-base shell extraction slice

That recommendation still fits the larger roadmap because it thins reusable renderer substrate without pretending generic host law is solved. It remains aligned with the analyzer-v2-as-brain objective precisely because it does **not** export Critic-specific selection typing or first-hop/workflow policy into the shared package.

## Explicit Answers

- Is the candidate-language calibrated correctly, or does any part still overclaim package-side proof?
  - Mostly calibrated, but one part still reads too broad. The memo should not imply that the smaller shell is already package-proved beyond the top-level trio. The code only supports “top-level package candidate clearly visible,” not “broader package proof established,” because `SubRenderers` is the dominant deferred surface and still has wiring inconsistencies.

- Is top-level-only adoption a genuinely honest first subset, or does the weight of `SubRenderers` make that framing misleading?
  - It is an honest first subset if it is framed explicitly as a top-level pilot only. It becomes misleading if it is read as representative of package capture architecture overall. The package has 8 capture-enabled sub-renderers versus 3 top-level builders, so the deferred weight is real.

- Is the proposed utility/API actually the smallest reusable package-neutral shell?
  - Yes, with one correction: it must preserve existing package defaulting and stay below Critic fail-closed semantics. The split between runtime resolution and shared selection-base assembly is the right minimal shape.

- What exact concerns still need to stay Critic-local?
  - `CaptureSelection` typing from `CaptureContext`
  - `_captureViewName` and `View Name: Title` composition
  - `_firstHopAffordance` fail-closed gating
  - `_workflowKey`
  - `source_workflow_key`
  - `requireWorkflowKey`
  - `requireJobId`
  - `genealogy_job_id`
  - renderer-specific `entity_id` specialization beyond raw package fallback
  - renderer-specific `selected_text` and preview shaping
  - mixed-surface and nested-handle gating
  - Critic capture persistence, read-side status/provenance surfacing, and destination semantics

- Does the next roadmap recommendation still hold after inspecting the code?
  - Yes. The next honest move is still the bounded `renderers-ui` capture-base shell extraction. The correction is that the memo should explicitly label it as a top-level package pilot and not treat it as evidence that `SubRenderers` has already been converged or proved.

## Bottom Line

The memo is strategically sound and the extraction target is real. The main corrections are about honesty of framing, not direction of travel.

Approve this scope if the write-up tightens three points:

- say explicitly that v1 is a **top-level package pilot**, not a representative package-wide proof
- say explicitly that `SubRenderers` remains the dominant deferred capture surface, with runtime-threading inconsistencies still untouched
- say explicitly that the extracted package shell must preserve current package defaulting and must not import Critic fail-closed semantics by stealth
