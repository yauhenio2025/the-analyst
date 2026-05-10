# Phase E Renderers-UI Nested Capture Forwarding-Normalization Decision V1 Scope Audit

Date: 2026-04-04
Reviewer: Codex
Target Memo: `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_scope.md`

## Context Check

Read in full:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_scope.md`
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_completion.md`
- `communications/REPORT_Claude_Close_Read_Roadmap_Recalibration_Critique_Rerun_2026-04-04.md`
- `communications/REPORT_Codex_Close_Read_Roadmap_Recalibration_Audit_Rerun_2026-04-04.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`

Code inspected directly:

- `renderers-ui/src/renderers/AccordionRenderer.tsx`
- `renderers-ui/src/renderers/CardRenderer.tsx`
- `renderers-ui/src/renderers/CardGridRenderer.tsx`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx`
- `renderers-ui/src/utils/captureBase.ts`
- `renderers-ui/scripts/check-capture-base.mjs`
- `/home/evgeny/projects/the-critic/webapp/package.json`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`

Environment note:

- The prompt’s relative `the-critic/webapp/...` paths do not exist inside `analyzer-v2`; the actual host codebase at `/home/evgeny/projects/the-critic/webapp` was inspected instead, which matches the host-codebase path named in the target memo.

Focused verification rerun:

- `renderers-ui`: `npm run build` passed
- `renderers-ui`: `node scripts/check-capture-base.mjs` passed
- The existing `MODULE_TYPELESS_PACKAGE_JSON` warning from the verification script remains unchanged

## Verdict

`approve with corrections`

The memo is directionally right. The real remaining package-side uncertainty is the nested forwarding line, not capture-base utility fit, and framing this as a decision gate instead of an automatic patch is correct. The memo also stays below the right decision boundary: package-internal forwarding sufficiency now, host-delivery posture and app-layer first-hop policy later.

The corrections are about precision, not direction:

1. make the `CardRenderer` asymmetry even more explicit: every subsection branch drops capture runtime today, not only one configured-path variant
2. keep the host-path references concrete, because the relevant host seams live in the external `/home/evgeny/projects/the-critic/webapp` repo rather than under the current workspace tree
3. if the eventual answer is “forwarding is already good enough,” say explicitly that this clears only the package-source forwarding gate, not host-integrated delivery readiness on the still-packed dependency line

## Findings

### 1. Forwarding-normalization is correctly framed as a decision gate

The memo explicitly scopes this as a docs-first, code-backed decision slice rather than an automatic normalization patch (`communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_scope.md:41-50`, `:85-111`, `:155-175`). That is the correct framing for the current code.

The package utility is intentionally raw and small:

- `renderers-ui/src/utils/captureBase.ts:22-39` resolves only `_captureMode`, `_onCapture`, `_captureViewKey`, `_captureSourceType`, `_captureJobId`, `_captureEntityId`
- `renderers-ui/src/utils/captureBase.ts:42-53` applies only package defaults for `source_view_key`, `source_type`, `context_title`, and `entity_id`

The package verification script also tests only that raw gate/default behavior, not host policy:

- `renderers-ui/scripts/check-capture-base.mjs:9-158`

That makes a decision memo the honest next step. The open question is not whether the utility can be adopted. It is whether the remaining forwarding gaps are acceptable for a lean `Close Read V1` corridor.

### 2. The memo identifies the two real asymmetries, but one of them should be described even more precisely

The `AccordionRenderer` asymmetry is real and correctly described as a metadata/defaulting problem:

- top-level section capture uses the package helper directly: `renderers-ui/src/renderers/AccordionRenderer.tsx:364-380`
- nested forwarding passes `_captureMode`, `_onCapture`, `_captureJobId`, `_captureViewKey`, and parent-section context, but omits `_captureSourceType` and `_captureEntityId`: `renderers-ui/src/renderers/AccordionRenderer.tsx:515-523`
- nested package consumers do read those omitted fields when available:
  - `renderers-ui/src/renderers/CardGridRenderer.tsx:524-545`
  - `renderers-ui/src/sub-renderers/SubRenderers.tsx:35-38`
  - representative usage: `renderers-ui/src/sub-renderers/SubRenderers.tsx:538-540` and `:671-680`
- because `buildPackageCaptureSelectionBase(...)` falls back to `'analysis'` and then `captureEntityId || captureJobId || ''`, nested capture still appears, but provenance can silently degrade: `renderers-ui/src/utils/captureBase.ts:47-52`

The `CardRenderer` asymmetry is also real, but it is stronger than a generic “nested forwarding gap” label suggests:

- top-level card capture uses the package helper correctly: `renderers-ui/src/renderers/CardRenderer.tsx:150`, `:274-290`
- nested subsection dispatch passes no capture runtime into configured subsection renderers at all: `renderers-ui/src/renderers/CardRenderer.tsx:340-356`
- the `nested_sections` fallback also carries no capture runtime: `renderers-ui/src/renderers/CardRenderer.tsx:362-364`
- the auto-detect path explicitly renders nested sub-renderers with `config={{}}`: `renderers-ui/src/renderers/CardRenderer.tsx:368-374`

So the memo is correct that `CardRenderer` is a functional-availability problem rather than a mere metadata-precision problem. The correction is that the memo should say plainly that the subsection path drops capture runtime on every nested branch, not just on one renderer-specific branch.

### 3. The memo keeps the package-internal boundary honest

This is one of the memo’s strongest parts.

It explicitly keeps these out of the package decision slice:

- `_firstHopAffordance`
- workflow/job requiredness law
- `source_workflow_key`
- host-specific view-name title law
- product-layer destination/UI law

That boundary is supported directly by the host code:

- `V2TabContent` threads package-facing capture runtime plus host-only affordance metadata into renderer config: `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:58-63`, `:588-597`
- `currentRendererCapture` is stricter than the package helper: it trims strings, requires non-empty `sourceViewKey` / `captureViewName` / `sourceType`, and fails closed unless `_firstHopAffordance.capturable === true`: `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:20-46`
- the same helper also emits host-specific `context_title` and `source_workflow_key`: `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:73-83`
- `CaptureActionBar` still always renders both `Send to Arsenal` and `Research Question` actions for any current selection; it does not consult `allowed_destinations`: `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx:117-135`

That means the package memo is right to stop at forwarding sufficiency. The host still owns first-hop gating posture and destination-action presentation.

### 4. The scope fits the larger roadmap and the analyzer-v2-as-brain objective

The larger roadmap set consistently says:

- Phase E is still active
- the current corridor is short
- the remaining renderer-substrate question is now the forwarding line
- any lean `Close Read V1` memo still has to handle host-delivery posture and app-layer first-hop eligibility explicitly

The target memo stays aligned with that:

- it names this as the remaining renderer-substrate decision gate, not generic cleanup: `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_scope.md:52-63`, `:176-198`
- it explicitly defers host-delivery posture and app-layer first-hop eligibility to the later `Close Read V1` memo: `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_scope.md:106-111`, `:187-190`

That is compatible with the “analyzer-v2 as the brain, host as thin shell” objective. The memo does not collapse package substrate work into product design, but it also does not pretend product questions disappeared.

### 5. The memo does not materially overclaim what package work has already proved

The source-side package claim is real:

- the top-level trio uses the package helper
- the dominant inline `SubRenderers` builders now import and use it too: `renderers-ui/src/sub-renderers/SubRenderers.tsx:35-38`, plus eight resolver sites at `:538`, `:721`, `:1366`, `:1848`, `:2119`, `:2348`, `:2777`, `:3024`

The memo does not claim:

- nested runtime convergence
- Critic-local first-hop law promotion into the package
- destination-policy law in the package
- host-integrated closeout

That restraint is important, because the host still consumes a packed renderer artifact rather than the source tree directly:

- `/home/evgeny/projects/the-critic/webapp/package.json:10`

So the only correction needed here is wording precision: where useful, prefer “in `renderers-ui` source” over anything that could be misread as “already absorbed and reverified in the host runtime.”

## Explicit Answers

### Is forwarding-normalization correctly framed as a decision gate rather than an automatic implementation step?

Yes.

That is the correct framing for the current code and the current roadmap position.

### Are the `AccordionRenderer` and `CardRenderer` asymmetries described precisely enough?

Mostly yes.

`AccordionRenderer` is described precisely enough: nested capture still works, but `_captureSourceType` and `_captureEntityId` are not forwarded, so nested selections can silently fall back to package defaults.

`CardRenderer` is close, but should be tightened slightly: the subsection path does not forward capture runtime on any nested branch today, including configured renderer dispatch, `nested_sections` fallback, and auto-detect.

### Does the memo stay honest that host-delivery posture and app-layer first-hop eligibility remain for the later `Close Read V1` scope memo?

Yes.

That deferral is explicit in the memo and supported by the code split between:

- raw package capture-base behavior
- host-local `currentRendererCapture` law
- universal host action-bar behavior

### Does any part of the memo still overclaim what the package work has already proved?

No material overclaim.

The memo stays on source-side package adoption and explicit remaining forwarding gaps. It does not claim host-integrated convergence or solved package-wide capture law.

### Does the next-step recommendation still hold after inspecting both recent memos and the actual code?

Yes.

This is still the next honest package-internal step.

The code confirms that the remaining renderer-substrate uncertainty is now the forwarding line, and the memo keeps later host/product questions in the right later memo. The only needed refinement is to make the stronger `CardRenderer` subsection gap fully explicit so the eventual decision does not flatten two different kinds of risk into one vague “normalization” label.

## Recommended Corrections

1. In the asymmetry section, expand the `CardRenderer` description from “nested subsection dispatch still does not forward capture runtime into nested sub-renderers at all” to language that explicitly covers:
   - configured subsection renderers
   - `nested_sections` fallback
   - auto-detected subsection renderers

2. In the evidence section, make the host-code paths concrete as external-repo paths, for example `/home/evgeny/projects/the-critic/webapp/...`, so the audit target is unambiguous when working from `analyzer-v2`.

3. In the success-condition section, add one sentence clarifying that a “good enough” verdict clears the package-source forwarding gate only. It does not by itself mean the still-packed host dependency line has already been refreshed and reverified.

## Bottom Line

The memo identifies the right remaining package-side question, keeps the decision boundary honest, and still fits the larger roadmap. The next honest step remains a forwarding-normalization decision memo, not automatic normalization and not premature `Close Read` product design.

The corrections above would make the scope tighter, but they do not change its direction.
