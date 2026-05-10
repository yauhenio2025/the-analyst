# Report: Phase E Renderers-UI Nested Capture Forwarding-Normalization Implementation V1 Scope Audit Rerun

## Context Check

Read in full:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_scope.md`
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_completion.md`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_completion.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`

Inspected directly:

- `renderers-ui/src/renderers/AccordionRenderer.tsx`
- `renderers-ui/src/renderers/CardRenderer.tsx`
- `renderers-ui/src/renderers/CardGridRenderer.tsx`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx`
- `renderers-ui/src/dispatch/SubRendererDispatch.tsx`
- `renderers-ui/src/utils/captureBase.ts`
- `renderers-ui/scripts/check-capture-base.mjs`
- `src/views/definitions/genealogy_target_profile.json`
- `src/views/definitions/genealogy_per_work_scan.json`
- `/home/evgeny/projects/the-critic/webapp/package.json`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`

Additional direct checks performed because they are necessary to judge the live-host claim:

- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/renderers/AccordionRenderer.js`
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/renderers/CardRenderer.js`
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/dispatch/SubRendererDispatch.js`
- `renderers-ui/release-artifacts/the-syllabus-analysis-renderers-0.6.5.tgz`

Focused verification rerun:

- `cd renderers-ui && npm run build` -> passed
- `cd renderers-ui && node scripts/check-capture-base.mjs` -> passed
- Existing unchanged warning still emitted: `MODULE_TYPELESS_PACKAGE_JSON`

## Verdict

`approve with corrections`

The bounded implementation shape is still the right Phase E substrate move and the current source-tree implementation is minimal enough. But the memo is no longer accurate as a description of the current `renderers-ui` source tree, because the named patch is already present there. The memo should be corrected to distinguish:

1. current `renderers-ui` source state
2. stale packed artifact state consumed by `the-critic`
3. live-host consequence

## Findings

### 1. The memo's baseline "current code" claims are stale for the current `renderers-ui` source tree

The source-tree implementation already contains the proposed patch:

- `renderers-ui/src/renderers/AccordionRenderer.tsx:107-114` already reads `_captureSourceType` and `_captureEntityId`.
- `renderers-ui/src/renderers/AccordionRenderer.tsx:518-579` already forwards those fields and already passes `captureConfig={captureForward}` into both `GenericSectionRenderer` call sites.
- `renderers-ui/src/renderers/CardRenderer.tsx:150-158` already builds `captureForwardConfig`.
- `renderers-ui/src/renderers/CardRenderer.tsx:348-400` already threads that config through configured, `nested_sections`, auto-detect, and fallback subsection branches.
- `renderers-ui/src/dispatch/SubRendererDispatch.tsx:102-106` already defines the optional `captureConfig` prop.
- `renderers-ui/src/dispatch/SubRendererDispatch.tsx:188-216` already merges `captureConfig` into resolved sub-renderer config and forwards it through recursion.

So these memo claims are refuted for the current source tree:

- "`AccordionRenderer` configured/auto-detect forwarding still omits `_captureSourceType` and `_captureEntityId`"
- "`AccordionRenderer` `nested_sections` and fallback paths pass no capture config to `GenericSectionRenderer`"
- "`CardRenderer` subsection dispatch forwards no capture runtime on all relevant branches"
- "`GenericSectionRenderer` currently lacks any generic capture-config forwarding prop"

They are no longer true in source. They are only still true in the stale packed host artifact.

### 2. The corrected provenance claim is still materially true on the live host path, but because the host is still on the stale packed artifact

`the-critic` still depends on a packed tarball, not the current source tree:

- `/home/evgeny/projects/the-critic/webapp/package.json:10`

The installed package still has the old behavior:

- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/renderers/AccordionRenderer.js:271-278` builds `captureForward` without `_captureSourceType` or `_captureEntityId`.
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/renderers/AccordionRenderer.js:299-311` still passes no `captureConfig` to `GenericSectionRenderer`.
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/renderers/CardRenderer.js:238-261` still forwards no capture runtime through any subsection branch.
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/dispatch/SubRendererDispatch.js:78-131` still lacks a `captureConfig` prop entirely.

The host still threads genealogy capture runtime like this:

- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:589-595`

That makes the live-host provenance consequence real:

- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:97-114` derives `genealogy_job_id` fallback only when `source_type === 'genealogy'`.
- `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx:109-126` does the same on the research-todo path.

And the installed package's sub-renderers still default missing forwarded type to `'analysis'`:

- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/sub-renderers/SubRenderers.js:519-523`
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/sub-renderers/SubRenderers.js:677-681`
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/sub-renderers/SubRenderers.js:1453-1457`

So the corrected provenance judgment is:

- `source_type` degradation is definitely still current on the live host path.
- `entity_id` degradation is only conditional today, because `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:591-595` currently threads both `_captureJobId` and `_captureEntityId` from `presentation.job_id`.

### 3. The named genealogy views do exercise the exact old gaps, and no other current view definitions materially change that verdict

The two named views are exactly the current `nested_sections` users:

- `src/views/definitions/genealogy_target_profile.json:17-40`
- `src/views/definitions/genealogy_per_work_scan.json:13-50`

`genealogy_target_profile` is an `accordion` with three `nested_sections` sections.
`genealogy_per_work_scan` is a `card` view whose four subsections are all `nested_sections`.

I also searched `src/views/definitions/*.json` for `nested_sections`. No other current view definitions use it. The other `genealogy_tp_*.json` files inspected in that search are accordion views, but they use concrete sub-renderers rather than `nested_sections`, so they do not materially affect the verdict.

### 4. `CardGridRenderer` does not introduce another missed normalization gap

`renderers-ui/src/renderers/CardGridRenderer.tsx:166-346` performs grouping and card rendering only.
`renderers-ui/src/renderers/CardGridRenderer.tsx:523-568` uses card-level capture runtime directly.

It does not call `GenericSectionRenderer`, does not resolve nested sub-renderers, and does not have a `nested_sections` dispatch seam. I do not see a comparable forwarding-normalization gap there.

### 5. The current `GenericSectionRenderer` extension is minimal enough

The current source implementation stays bounded:

- `renderers-ui/src/utils/captureBase.ts:22-54` is unchanged and still only reads existing `_capture*` fields.
- `renderers-ui/src/dispatch/SubRendererDispatch.tsx:102-106` adds only one optional raw pass-through prop.
- `renderers-ui/src/dispatch/SubRendererDispatch.tsx:198` merges `captureConfig` after `subHint.config`, which means forwarded runtime wins over any conflicting private `_capture*` keys. That is the intended forwarding behavior, not hidden package-law widening.
- No `_firstHopAffordance`, `source_workflow_key`, `genealogy_job_id`, `allowed_destinations`, or typed Critic `CaptureSelection` logic moved into `renderers-ui`.

So on the actual implementation shape, the memo's boundedness judgment is basically correct.

### 6. The deferred list remains honest, and the work is still Phase E substrate work rather than product drift

The package layer still only does raw capture gating and raw runtime forwarding:

- `renderers-ui/src/utils/captureBase.ts:22-54`

The host-specific first-hop policy is still unresolved above that layer:

- `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:40-53` gates current custom renderers on `_firstHopAffordance.capturable`.
- `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx:117-135` still shows both destination buttons without consulting `allowed_destinations`.

That means the memo's deferrals are still honest:

- host-delivery posture is still separate
- app-layer first-hop eligibility policy is still separate
- destination policy/taxonomy is still separate

This remains appropriate Phase E substrate work. It has not drifted into product design.

### 7. Verification is still weaker than the memo ideally wants

The rerun commands passed:

- `renderers-ui`: build passed
- `renderers-ui`: `check-capture-base.mjs` passed

But `renderers-ui/scripts/check-capture-base.mjs:11-168` only verifies utility behavior and defaulting. It still does not verify forwarding through:

- `AccordionRenderer`
- `CardRenderer`
- `GenericSectionRenderer`

So the memo is still right that forwarding-specific verification is missing.

## Audit Answers

- `AccordionRenderer` configured/auto-detect omission:
  - refuted in current source
  - confirmed in the live host artifact
- `AccordionRenderer` `nested_sections` and fallback lack `captureConfig`:
  - refuted in current source
  - confirmed in the live host artifact
- `CardRenderer` subsection dispatch lacks capture runtime:
  - refuted in current source
  - confirmed in the live host artifact
- `GenericSectionRenderer` lacks forwarding prop:
  - refuted in current source
  - confirmed in the live host artifact
- `genealogy_target_profile.json` and `genealogy_per_work_scan.json` exercise the named gaps:
  - confirmed
- `CaptureContext.tsx` and `ResearchFlagDialog.tsx` make `source_type === 'genealogy'` materially consequential:
  - confirmed
- `entity_id` degradation is only conditional today:
  - confirmed
- `CardGridRenderer` has another comparable normalization gap:
  - not found
- other current view definitions materially affected by `nested_sections`:
  - not found

## Concrete Corrections Recommended

1. In `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_scope.md`, rewrite the "current gap" sections so they explicitly say whether they refer to:
   - current `renderers-ui` source
   - or the stale packed artifact consumed by `the-critic`

2. Replace the memo's current-state file references for the implementation gaps with the actual present-tense source references:
   - `renderers-ui/src/renderers/AccordionRenderer.tsx:107-114`
   - `renderers-ui/src/renderers/AccordionRenderer.tsx:518-579`
   - `renderers-ui/src/renderers/CardRenderer.tsx:150-158`
   - `renderers-ui/src/renderers/CardRenderer.tsx:348-400`
   - `renderers-ui/src/dispatch/SubRendererDispatch.tsx:102-106`
   - `renderers-ui/src/dispatch/SubRendererDispatch.tsx:188-216`

3. Add an explicit live-host correction note:
   - the source-tree patch is landed
   - the live host is still stale because `/home/evgeny/projects/the-critic/webapp/package.json:10` points to a packed tarball that still contains the old forwarding behavior

4. Update the next-step wording. If the memo is meant to describe current reality rather than historical implementation scope, the immediate operational next step is:
   - refresh/repack `renderers-ui`
   - update the packed dependency consumed by `the-critic`
   - rerun focused host verification on the genealogy `nested_sections` surfaces

5. Keep the lean `Close Read V1` recommendation only with that distinction made explicit:
   - source-tree substrate question: basically cleared
   - live-host delivery question: not yet cleared until the stale packed dependency is refreshed
