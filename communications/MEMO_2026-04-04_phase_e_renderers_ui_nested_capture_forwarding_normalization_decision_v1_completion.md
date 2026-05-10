# Memo: Phase E Renderers-UI Nested Capture Forwarding-Normalization Decision V1 Completion

Subtitle: The package-internal forwarding decision gate is now closed, and the honest verdict is that one bounded normalization patch is still required before lean `Close Read V1` scoping

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
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_scope.md`
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

Record the outcome of the docs-first decision slice that asked one narrow question:

- are the remaining nested capture-runtime forwarding asymmetries already acceptable for the near-term `Close Read` surfaces that materially matter
- or is one bounded normalization patch still required first

This slice was decision-only.
It was not:

- the normalization patch itself
- package-wide nested-runtime convergence
- host integration
- `Close Read V1` scoping

## What Was Inspected

The decision was grounded in:

- package forwarding sites:
  - `renderers-ui/src/renderers/AccordionRenderer.tsx`
  - `renderers-ui/src/renderers/CardRenderer.tsx`
  - `renderers-ui/src/dispatch/SubRendererDispatch.tsx`
- package utility and verification:
  - `renderers-ui/src/utils/captureBase.ts`
  - `renderers-ui/scripts/check-capture-base.mjs`
- current near-term package-backed genealogy surfaces that materially matter for a lean `Close Read` path:
  - `src/views/definitions/genealogy_target_profile.json`
  - `src/views/definitions/genealogy_tp_*.json`
  - `src/views/definitions/genealogy_per_work_scan.json`
- host seams used only to define the boundary of the verdict:
  - `/home/evgeny/projects/the-critic/webapp/package.json`
  - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
  - `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`
  - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
  - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
  - `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`

## Verdict

The verdict is:

- **one bounded forwarding-normalization patch is still required first**

Why this is the honest result:

- the remaining gaps do materially block near-term `Close Read` surfaces that already matter
- so the package-source gate is **not** clear yet

## Why The Gaps Are Material

### 1. `AccordionRenderer` is not only an abstract metadata issue

The package forwarding site still omits:

- `_captureSourceType`
- `_captureEntityId`

That means nested package captures under genealogy accordions definitely fall back to:

- `source_type: 'analysis'`

instead of receiving the host-threaded genealogy `source_type` from:

- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`

On the current host path, the `_captureEntityId` omission is only a conditional degradation risk, not a
separate proved live divergence: `V2TabContent` currently threads both `_captureJobId` and
`_captureEntityId` from the same `presentation.job_id`, and the package fallback remains
`captureEntityId || captureJobId || ''`. So nested accordion captures do **not** currently emit a
different `entity_id` on that path. The material current break is the `source_type` downgrade, because the
host only derives `genealogy_job_id` fallback when `source_type === 'genealogy'`.

This matters on real near-term genealogy surfaces such as:

- `genealogy_target_profile`
- nested `genealogy_tp_*` accordions

because the host capture flow uses `source_type === 'genealogy'` when deriving `genealogy_job_id` fallback in:

- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`

So this asymmetry is not merely cosmetic.
It degrades routed provenance truth on material genealogy nested surfaces.

### 2. `CardRenderer` is a functional availability blocker

`CardRenderer` nested subsection dispatch still forwards no capture runtime on every subsection branch:

- configured sub-renderer path
- `nested_sections` path
- auto-detected sub-renderer path
- final generic fallback path

This means nested capture controls are absent, not merely imprecise.

That is material because:

- `genealogy_per_work_scan` is a current genealogy `card` surface
- it is `planner_eligible`
- it is explicitly nested
- it is the kind of per-work comparison surface a lean `Close Read` product would plausibly want rather than defer as irrelevant

So the remaining `CardRenderer` gap cannot be honestly hand-waved as acceptable for the near-term product corridor.

## What This Decision Does And Does Not Clear

This decision does clear one thing:

- the package-internal forwarding decision gate is no longer open-ended

It does **not** clear:

- packed-host integration readiness
- host-delivery posture
- app-layer first-hop eligibility policy
- destination-level UI/policy law
- generic renderer-package capture law

Those remain for later slices and later product scoping.

## Likely Follow-On Patch Shapes

Because the verdict is `patch required`, the next scope must name likely patch shapes, not just fields.

The likely bounded implementation shapes are:

1. `AccordionRenderer`
   - extend `captureForward` with:
     - `_captureSourceType`
     - `_captureEntityId`

2. `CardRenderer`
   - thread capture runtime through all subsection dispatch branches:
     - configured renderer path
     - `nested_sections` path
     - auto-detect path
   - do not stop at one branch

3. shared dispatch support as needed
   - if `CardRenderer` `nested_sections` cannot carry runtime without small shared dispatch help, that support should remain package-native and bounded
   - it must stay below:
     - Critic `CaptureSelection`
     - `_firstHopAffordance`
     - workflow/job requiredness
     - `source_workflow_key`
     - `genealogy_job_id`
     - host-specific title law

## Verification

Focused package-local verification rerun passed:

- `npm run build`
  - passed
- `node scripts/check-capture-base.mjs`
  - `capture-base verification passed`

Environment honesty note:

- `node scripts/check-capture-base.mjs` still emits the existing unchanged `MODULE_TYPELESS_PACKAGE_JSON` warning

Verification boundary note:

- the script is utility-behavior evidence only
- it is **not** proof that forwarding itself is correct

No host/browser reruns were required for this decision-only slice.

## Strategic Consequence

The close-read corridor is still shorter than before, but the honest reading is now:

1. dominant package capture-base adoption is complete
2. the forwarding decision gate is now closed
3. the result is `patch required`
4. so the next step is one bounded forwarding-normalization implementation scope
5. only after that does lean `Close Read V1` scoping become the next honest product-facing move

## Next Honest Step

The next bounded step is now:

- one bounded nested capture forwarding-normalization implementation scope

It should:

- fix the concrete `AccordionRenderer` and `CardRenderer` forwarding gaps
- stay package-native
- stay below Critic-local first-hop/workflow/type law
- avoid widening into product design, host delivery, or generic capture-law claims

Only after that slice is complete should the roadmap move to:

- one lean `Close Read V1` scope memo
