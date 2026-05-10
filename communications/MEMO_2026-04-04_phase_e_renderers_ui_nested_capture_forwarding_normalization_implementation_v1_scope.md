# Memo: Phase E Renderers-UI Nested Capture Forwarding-Normalization Implementation V1 Scope

Subtitle: One bounded package-native patch to close the remaining AccordionRenderer and CardRenderer nested capture-forwarding gaps before lean `Close Read V1` scoping

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
Close-Read Corridor Context:
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
Decision Gate:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_completion.md`
Most Recent Prior Completion:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_completion.md`
Review Context:
- `communications/REPORT_Claude_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Decision_V1_Scope_Critique_2026-04-04.md`
- `communications/REPORT_Codex_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Decision_V1_Scope_Audit_2026-04-04.md`
Package Codebase:
- `/home/evgeny/projects/analyzer-v2/renderers-ui`
Host Codebase:
- `/home/evgeny/projects/the-critic/webapp`

## Purpose

Implement the bounded forwarding-normalization patch that the decision gate identified as required before lean `Close Read V1` scoping.

The decision gate verdict was explicit:

- one bounded forwarding-normalization patch is still required first

This scope implements that patch.
It does not:

- widen into product design or `Close Read V1` scoping
- promote Critic-local first-hop/workflow/type law into the package
- change the `captureBase` utility itself
- refresh the packed tarball into `the-critic` (that is a separate downstream step)
- claim package-wide capture convergence

## The Exact Gaps To Close

Code inspection during and after the decision gate reveals three distinct fix sites, not two.

The prior decision memo characterized two gaps:

1. AccordionRenderer: metadata/defaulting precision (missing 2 fields in `captureForward`)
2. CardRenderer: functional availability (no capture forwarding on any subsection branch)

Deeper inspection for this implementation scope reveals a third:

3. AccordionRenderer also has a structural forwarding gap on `nested_sections` and fallback paths

The full picture:

### Gap 1: AccordionRenderer captureForward field precision

**File:** `renderers-ui/src/renderers/AccordionRenderer.tsx`
**Lines:** 516-523

The existing `captureForward` object includes:

- `_captureMode`
- `_onCapture`
- `_captureJobId`
- `_captureViewKey`
- `_parentSectionKey`
- `_parentSectionTitle`

It omits:

- `_captureSourceType`
- `_captureEntityId`

This affects the configured-renderer path (line 529) and the auto-detect path (line 564), which both spread `captureForward` into their sub-renderer configs. Nested sub-renderers on these paths get capture buttons, but `resolvePackageCaptureBaseRuntime` falls back to:

- `source_type: 'analysis'` instead of the host-threaded value (e.g. `'genealogy'`)

On the current host path, `_captureEntityId` omission is a conditional future-risk rather than a separate proved live divergence: `V2TabContent` currently threads both `_captureJobId` and `_captureEntityId` from the same `presentation.job_id`, and the package fallback remains `captureEntityId || captureJobId || ''`. So the material current break on near-term genealogy accordion surfaces is the `source_type` downgrade, which matters because:

- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx` (lines 97-101) uses `source_type === 'genealogy'` to derive `genealogy_job_id` fallback
- wrong `source_type` degrades routed provenance truth, not just cosmetic labels

### Gap 2: AccordionRenderer GenericSectionRenderer path structural absence

**File:** `renderers-ui/src/renderers/AccordionRenderer.tsx`
**Lines:** 555, 569

Two paths in AccordionRenderer's sub-renderer dispatch do NOT spread `captureForward` at all:

- `nested_sections` path (line 555): `<GenericSectionRenderer data={sectionData} subRenderers={hint.sub_renderers} />`
- Fallback path (line 569): `<GenericSectionRenderer data={sectionData} />`

Neither passes any capture config. GenericSectionRenderer does not currently accept a capture prop, so even fixing the call sites would require a bounded extension to GenericSectionRenderer.

This matters on a specific near-term genealogy surface:

- `src/views/definitions/genealogy_target_profile.json` uses `renderer_type: "accordion"` and defines `nested_sections` for at least `conceptual_framework`, `semantic_constellation`, and `inferential_commitments`
- All three hit AccordionRenderer's `nested_sections` path (line 555)
- Sub-renderers resolved by GenericSectionRenderer for those sections (e.g. `mini_card_list`, `prose_block`, `comparison_panel`) receive no capture runtime

### Gap 3: CardRenderer subsection dispatch complete absence

**File:** `renderers-ui/src/renderers/CardRenderer.tsx`
**Lines:** 339-378

All four subsection dispatch branches forward no capture runtime:

1. Configured renderer (line 343): `subConfig = { ...(hint.config || {}) }` — no capture
2. `nested_sections` (line 364): `<GenericSectionRenderer data={sectionData} subRenderers={hint.sub_renderers} />` — no capture
3. Auto-detect (line 373): `<AutoComp data={sectionData} config={{}} />` — no capture
4. Fallback (line 378): `<GenericSectionRenderer data={sectionData} />` — no capture

CardRenderer reads capture runtime for its OWN card-level capture buttons (line 150: `resolvePackageCaptureBaseRuntime(config)`) but does not build a `captureForward` object or thread it downstream.

This matters on a specific near-term genealogy surface:

- `src/views/definitions/genealogy_per_work_scan.json` uses `renderer_type: "card"` with `subsections: ["vocabulary", "methodology", "metaphor", "framing"]`
- Each subsection uses `renderer_type: "nested_sections"` with sub-renderers like `comparison_panel`, `chip_grid`, `prose_block`
- This view is `planner_eligible: true` and tagged `["genealogy", "per-work", "scanning", "nested"]`
- No sub-renderer in any subsection receives capture runtime

## Proposed Implementation

### Fix 1: AccordionRenderer captureForward field extension

Add two config reads and two fields to the existing captureForward:

**Current state** (lines 107-112):

```
const captureMode = config._captureMode as boolean | undefined;
const onCapture = config._onCapture as ...;
const captureJobId = config._captureJobId as string | undefined;
const captureViewKey = config._captureViewKey as string | undefined;
```

**Add:**

```
const captureSourceType = config._captureSourceType as string | undefined;
const captureEntityId = config._captureEntityId as string | undefined;
```

**Current captureForward** (lines 516-523):

```
const captureForward = {
    _captureMode: captureMode,
    _onCapture: onCapture,
    _captureJobId: captureJobId,
    _captureViewKey: captureViewKey,
    _parentSectionKey: section.key,
    _parentSectionTitle: section.title,
};
```

**Extended captureForward:**

```
const captureForward = {
    _captureMode: captureMode,
    _onCapture: onCapture,
    _captureJobId: captureJobId,
    _captureViewKey: captureViewKey,
    _captureSourceType: captureSourceType,
    _captureEntityId: captureEntityId,
    _parentSectionKey: section.key,
    _parentSectionTitle: section.title,
};
```

This normalizes the configured-renderer and auto-detect paths, which already consume captureForward.

### Fix 2: AccordionRenderer GenericSectionRenderer call sites

Thread captureForward into the two GenericSectionRenderer call sites:

**Line 555 (nested_sections):**

```
// Before:
return <GenericSectionRenderer data={sectionData} subRenderers={hint.sub_renderers} />;
// After:
return <GenericSectionRenderer data={sectionData} subRenderers={hint.sub_renderers} captureConfig={captureForward} />;
```

**Line 569 (fallback):**

```
// Before:
return <GenericSectionRenderer data={sectionData} />;
// After:
return <GenericSectionRenderer data={sectionData} captureConfig={captureForward} />;
```

### Fix 3: CardRenderer captureForward construction and threading

Add capture config reads and build a captureForward object, then thread into all four branches.

**Add config reads** near line 150:

```
const captureForwardConfig = captureRuntime ? {
    _captureMode: config._captureMode,
    _onCapture: config._onCapture,
    _captureJobId: config._captureJobId,
    _captureViewKey: config._captureViewKey,
    _captureSourceType: config._captureSourceType,
    _captureEntityId: config._captureEntityId,
} : {};
```

**Thread into all four subsection dispatch branches** within the `matchingSubsections.map` block (lines 339-378):

Each subsection should build its own capture context with parent section info:

```
const subsectionCaptureForward = captureRuntime ? {
    ...captureForwardConfig,
    _parentSectionKey: sub.key,
    _parentSectionTitle: sub.title,
} : {};
```

Then:

1. **Configured renderer** (line 343): `const subConfig = { ...(hint.config || {}), ...subsectionCaptureForward };`
2. **nested_sections** (line 364): `<GenericSectionRenderer data={sectionData} subRenderers={hint.sub_renderers} captureConfig={subsectionCaptureForward} />`
3. **Auto-detect** (line 373): `<AutoComp data={sectionData} config={subsectionCaptureForward} />`
4. **Fallback** (line 378): `<GenericSectionRenderer data={sectionData} captureConfig={subsectionCaptureForward} />`

### Fix 4: GenericSectionRenderer bounded extension

**File:** `renderers-ui/src/dispatch/SubRendererDispatch.tsx`
**Lines:** 102-106, 197

Add optional `captureConfig` prop:

```
export function GenericSectionRenderer({ data, depth = 0, subRenderers, captureConfig }: {
  data: unknown;
  depth?: number;
  subRenderers?: Record<string, { renderer_type: string; config?: Record<string, unknown> }>;
  captureConfig?: Record<string, unknown>;
}) {
```

When resolving sub-renderers (line 197), spread `captureConfig` into the sub-component's config:

```
// Before:
<SubComp data={value} config={subHint.config || {}} />
// After:
<SubComp data={value} config={{ ...(subHint.config || {}), ...(captureConfig || {}) }} />
```

Forward `captureConfig` to recursive GenericSectionRenderer calls (lines 210, 214):

```
<GenericSectionRenderer data={value} depth={depth + 1} captureConfig={captureConfig} />
```

This is the minimum bounded extension. It does not add any gating, normalization, or policy to GenericSectionRenderer — it only passes through raw capture config fields so that sub-renderers can call `resolvePackageCaptureBaseRuntime(config)` and find them.

## What Must Stay Out

This implementation must stay below:

- `_firstHopAffordance` — host-level affordance gating
- `source_workflow_key` — host-level workflow identity
- `genealogy_job_id` — host-level genealogy-specific routing
- `_captureViewName` — host-level view name identity (used by `currentRendererCapture`, not by `captureBase`)
- Critic `CaptureSelection` interface changes
- workflow/job requiredness law
- host-specific title law (the package uses `>` convention; the host uses `: ` convention)
- `currentRendererCapture.ts` changes
- destination lifecycle or taxonomy widening
- `Close Read V1` product design
- generic renderer-package capture law claims

The package utility (`captureBase.ts`) itself should remain unchanged. It already reads the fields being forwarded. The fix is in the forwarding layer, not the utility.

## Verification

### Package-local verification (required)

- `npm run build` in `renderers-ui` — must pass
- `node scripts/check-capture-base.mjs` — must still pass (script tests utility, not forwarding; this confirms no regression)

### Forwarding-specific verification (recommended)

Consider extending `check-capture-base.mjs` or adding a companion script that:

- simulates a config object with all capture fields set
- verifies that GenericSectionRenderer's `captureConfig` prop reaches resolved sub-renderer configs
- verifies that a sub-renderer receiving forwarded config would produce a non-null runtime from `resolvePackageCaptureBaseRuntime`

This is not strictly required but would provide forwarding-level evidence beyond "utility works" and "build passes".

### Host verification (optional, separate step)

If the implementor refreshes the packed tarball into `the-critic`:

- verify `genealogy_target_profile` accordion surfaces show capture buttons on nested sub-renderers (the `conceptual_framework` nested_sections path)
- verify `genealogy_per_work_scan` card subsection surfaces show capture buttons on nested sub-renderers

This is a **separate downstream step**, not part of this implementation scope. The decision to refresh the tarball and rerun Critic verification should be made after the package patch lands cleanly.

## Behavioral Preservation Rules

The implementation must preserve:

- raw `captureMode && onCapture` gating only (no new gates)
- raw string-or-default semantics only (no trim, no non-empty normalization)
- `>` title composition convention (no `: ` adoption)
- empty-segment preservation in title chains
- raw identity fallback: explicit `entityId !== undefined` check, otherwise `captureEntityId || captureJobId || ''`
- no new capture config fields beyond those already defined in `captureBase.ts`

These are the same preservation rules from the `captureBase` shell extraction and `SubRenderers` adoption slices.

## Files To Modify

| File | Change |
|---|---|
| `renderers-ui/src/renderers/AccordionRenderer.tsx` | Add 2 config reads; extend captureForward with 2 fields; thread captureForward into 2 GenericSectionRenderer call sites |
| `renderers-ui/src/renderers/CardRenderer.tsx` | Build captureForward from config; thread into all 4 subsection dispatch branches |
| `renderers-ui/src/dispatch/SubRendererDispatch.tsx` | Add optional `captureConfig` prop to GenericSectionRenderer; spread into resolved sub-renderer configs; forward to recursive calls |

No other files should be modified.

## What This Clears When Done

If this patch lands cleanly:

- the package-internal forwarding gate is fully closed
- all three top-level renderers with sub-renderer dispatch (Accordion, Card) thread complete capture runtime to nested children
- GenericSectionRenderer can carry capture config to its resolved sub-renderers
- the package-source state is sufficient for a lean `Close Read V1` scope memo

What this still does not clear:

- packed-host integration readiness (tarball not refreshed)
- host-delivery posture (still consuming a pre-patch artifact)
- app-layer first-hop eligibility policy (raw package capture != Critic `currentRendererCapture` gating)
- destination-level UI/policy law (CaptureActionBar, allowed_destinations)

## Next Step After This Patch

If this implementation completes cleanly, the next honest step is:

- one lean `Close Read V1` scope memo

That product-facing memo must resolve at minimum:

- host-delivery posture for a still-packed `renderers-ui` dependency line
- app-layer first-hop eligibility policy above the raw package capture utilities
- destination scope (Arsenal and Research as the proved operational backbone)
- engine/output family scope (genealogy and AOI as the proved composition families)

## Success Condition

This slice succeeds if:

- all three fix sites land cleanly in the named files
- `npm run build` passes
- `node scripts/check-capture-base.mjs` still passes
- the completion memo can honestly say: the package-internal capture-forwarding gate is now fully closed
- the roadmap can move to lean `Close Read V1` scoping without ambiguity
