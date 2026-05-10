# Memo: Phase E Renderers-UI Nested Capture Forwarding-Normalization Implementation V1 Completion

Subtitle: The package-source normalization patch is already landed locally; the remaining gap is that Critic still consumes a stale packed `renderers-ui` artifact

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
Immediate Prior Scope:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_scope.md`
Decision Gate:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_completion.md`
Most Recent Prior Completion:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_completion.md`
Review Context:
- `communications/REPORT_Claude_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Implementation_V1_Scope_Critique_Rerun_2026-04-04.md`
- `communications/REPORT_Codex_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Implementation_V1_Scope_Audit_Rerun_2026-04-04.md`
Package Codebase:
- `/home/evgeny/projects/analyzer-v2/renderers-ui`
Host Codebase:
- `/home/evgeny/projects/the-critic/webapp`

## Purpose

Record the actual outcome of the bounded forwarding-normalization implementation slice.

The important calibration change from the rerun audit is:

- the package-source patch is no longer hypothetical
- it is already present in the local `renderers-ui` source tree
- the remaining live consequence exists because Critic is still consuming an older packed artifact

So this completion memo closes the package-source implementation slice honestly and resets the next step to the packed-host handoff.

## What Landed In Package Source

The bounded patch is present locally in `renderers-ui`.

### 1. `AccordionRenderer` field forwarding is normalized

`renderers-ui/src/renderers/AccordionRenderer.tsx` now reads and forwards:

- `_captureSourceType`
- `_captureEntityId`

alongside the existing:

- `_captureMode`
- `_onCapture`
- `_captureJobId`
- `_captureViewKey`
- `_parentSectionKey`
- `_parentSectionTitle`

This closes the configured-renderer and auto-detect field-precision gap in package source.

### 2. `AccordionRenderer` structural nested forwarding is normalized

`renderers-ui/src/renderers/AccordionRenderer.tsx` now passes capture forwarding into the two previously missing paths:

- `nested_sections`
- final generic fallback

That forwarding now runs through `GenericSectionRenderer`.

### 3. `CardRenderer` subsection dispatch now forwards capture runtime

`renderers-ui/src/renderers/CardRenderer.tsx` now builds a package-native `captureForwardConfig` and threads subsection capture context through:

- configured renderer path
- `nested_sections` path
- auto-detect path
- final generic fallback path

This closes the functional nested capture-availability gap in package source.

### 4. `GenericSectionRenderer` was extended only as bounded pass-through

`renderers-ui/src/dispatch/SubRendererDispatch.tsx` now accepts optional `captureConfig` and only forwards it through to nested sub-renderers / recursive generic rendering.

It does **not** add:

- `_firstHopAffordance`
- workflow/job requiredness
- Critic `CaptureSelection`
- destination policy
- host-specific title law

So the patch stayed package-native and below Critic-local capture law.

## What Did Not Change

The package-source patch did **not**:

- change `captureBase.ts`
- widen package law toward `currentRendererCapture`
- introduce app-layer first-hop eligibility
- resolve host-delivery posture
- update the packed artifact consumed by Critic

That last point is now the key remaining gap.

## Why The Live Host Consequence Still Exists

The current Critic consumer still points at:

- `/home/evgeny/projects/the-critic/webapp/package.json`
- `file:../../analyzer-v2/renderers-ui/release-artifacts/the-syllabus-analysis-renderers-0.6.5.tgz`

The installed consumer package in:

- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers`

still reflects the older pre-patch artifact.

Code-backed rerun inspection confirmed:

- local `renderers-ui/src/renderers/CardRenderer.tsx` contains `captureForwardConfig`
- installed `the-critic` `node_modules/@the-syllabus/analysis-renderers/dist/renderers/CardRenderer.js` does not
- local `SubRendererDispatch.tsx` has `captureConfig`
- installed `node_modules` `dist/dispatch/SubRendererDispatch.js` does not

So the earlier decision memo’s material host consequence remains true in the live consumer path, but its location has changed:

- the problem is no longer missing package-source implementation
- the problem is stale packed-host consumption

## Verification

Focused package-local verification passed:

- `cd renderers-ui && npm run build`
  - passed
- `cd renderers-ui && node scripts/check-capture-base.mjs`
  - `capture-base verification passed`

Environment note:

- `node scripts/check-capture-base.mjs` still emits the existing unchanged `MODULE_TYPELESS_PACKAGE_JSON` warning

Verification boundary note:

- these checks prove local package-source integrity
- they do **not** prove that Critic is already consuming the updated package

## Verdict

The honest verdict for this slice is:

- **the bounded forwarding-normalization implementation is complete in local package source**
- **the next real gap is packed artifact refresh plus focused Critic host verification**

That is narrower and more honest than saying the implementation slice is still pending.

## Strategic Consequence

The corridor toward `Close Read` now reads:

1. dominant package capture-base adoption is complete
2. the forwarding decision gate is complete
3. the bounded forwarding-normalization patch is also complete in package source
4. the remaining gap is that the current host still consumes a stale packed artifact
5. so the next bounded step is one traceable `renderers-ui` artifact refresh plus focused Critic verification
6. only after that does lean `Close Read V1` scoping become the next honest product-facing move

This still does **not** settle:

- broader host-delivery posture
- app-layer first-hop eligibility policy
- destination-level policy/lifecycle law
- generic renderer-package capture law

## Next Honest Step

The next bounded step should now be:

- one `renderers-ui` release-artifact refresh and Critic host-verification slice

That slice should:

- turn the already-landed local package-source patch into a traceable packed artifact
- refresh Critic’s file-based dependency to that artifact
- rerun focused host verification on the material nested genealogy surfaces
- stay below broader host posture redesign and product scoping
