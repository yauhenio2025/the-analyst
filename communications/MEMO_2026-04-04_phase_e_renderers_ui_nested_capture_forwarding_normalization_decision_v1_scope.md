# Memo: Phase E Renderers-UI Nested Capture Forwarding-Normalization Decision V1 Scope

Subtitle: Now that both the top-level package trio and the dominant inline `SubRenderers` builders use the same package-native `captureBase` shell, the next honest question before lean `Close Read V1` scoping is whether current nested runtime forwarding defaults are already sufficient or whether one bounded normalization slice is still required

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
Most Recent Prior Completion:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_completion.md`
Immediate Prior Scope:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_scope.md`
Relevant Review Context:
- `communications/REPORT_Claude_Close_Read_Roadmap_Recalibration_Critique_Rerun_2026-04-04.md`
- `communications/REPORT_Codex_Close_Read_Roadmap_Recalibration_Audit_Rerun_2026-04-04.md`
Package Codebase:
- `/home/evgeny/projects/analyzer-v2/renderers-ui`
Host Codebase:
- `/home/evgeny/projects/the-critic/webapp`

## Purpose

Define the next bounded renderer-substrate question now that the package-native capture-base shell is proven across the top-level package trio and the dominant current inline `SubRenderers` builder surface.

That question is no longer:

- does the package-native shell fit the main current package builders

That is now answered.

The next question is:

- are the current nested capture-runtime forwarding asymmetries already acceptable for a first lean `Close Read V1`
- or is one bounded normalization slice still required before product-facing scoping is honest

This is a decision-gate slice first.
It should not start as:

- automatic forwarding normalization
- package-wide nested-runtime convergence
- Critic-law promotion
- full `Close Read` productization

## Why This Is The Right Next Step

The renderer-substrate corridor is now materially shorter.

What is already true:

- package-native raw capture-base behavior is now shared by the top-level trio
- the same package-native raw capture-base behavior is now shared by the dominant current inline `SubRenderers` builders
- the remaining uncertainty is no longer base selection assembly
- the remaining uncertainty is the forwarding line itself

That makes this the last honest renderer-substrate gate before a lean `Close Read V1` memo.

## The Exact Remaining Uncertainty

The current known asymmetries are:

1. `AccordionRenderer` nested forwarding still omits:
   - `_captureSourceType`
   - `_captureEntityId`
   - this is primarily a metadata/defaulting precision problem
   - nested capture can still appear, but emitted base fields may silently fall back to package defaults
2. `CardRenderer` nested subsection dispatch still does not forward capture runtime into nested sub-renderers at all
   - this is primarily a functional-availability problem
   - nested capture controls are absent on that path rather than merely imprecise
   - this is true across every subsection branch in that dispatch chain:
     - configured sub-renderer path
     - `nested_sections` path
     - auto-detected sub-renderer path

Because the new package utility preserves current raw defaults exactly, these asymmetries do not currently break the adopted package utility.

But the next question is not utility fit.
It is:

- whether the current defaulted nested behavior is still honest enough for the near-term product corridor toward `Close Read`

## Proposed Bounded Slice

This slice should begin as a docs-first, code-backed decision memo.

It should inspect:

- current nested forwarding in `renderers-ui`
- current nested package consumers that depend on forwarded runtime
- the package-backed Critic surfaces most relevant to a lean `Close Read` path

It should end with one explicit verdict:

1. current nested forwarding is already good enough for lean `Close Read V1` scoping
2. one bounded forwarding-normalization patch is still required first

If the verdict is option 2, the memo must name concretely:

- the exact forwarding patch surface
- the exact fields that need normalization
- the exact fields/policies that must still remain out of the package

If the verdict is option 1, the memo must still say explicitly that this clears only the package-internal forwarding gate.
It does **not** settle:

- packed-host integration readiness
- host-delivery posture
- app-layer first-hop eligibility policy
- destination-level policy/UI law

## What Must Stay Out

This decision slice must stay below:

- Critic `CaptureSelection`
- `_firstHopAffordance`
- workflow/job requiredness law
- `source_workflow_key`
- `genealogy_job_id`
- host-specific view-name title law
- full package-wide convergence claims
- destination lifecycle or taxonomy widening
- `Close Read` product design itself

The decision question is about runtime forwarding sufficiency only.

It is allowed to point forward to the next product-layer memo.
It is not allowed to absorb that memo's job.

## What Evidence The Decision Memo Should Compare

The decision memo should compare:

- what nested package consumers currently receive
- what raw defaults they fall back to today
- whether those defaults materially distort capture availability or emitted package-base selection fields on the nested surfaces that matter for a lean `Close Read V1`

At minimum, it should inspect:

- `renderers-ui/src/renderers/AccordionRenderer.tsx`
- `renderers-ui/src/renderers/CardRenderer.tsx`
- `renderers-ui/src/renderers/CardGridRenderer.tsx`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx`
- current package verification script behavior in:
  - `renderers-ui/scripts/check-capture-base.mjs`
  - this script should be treated only as utility-behavior evidence, not as proof that forwarding itself is correct
- relevant Critic surfaces that rely on package-backed nested renderers in the near-term product corridor
- host seams that will still matter after this decision:
  - `/home/evgeny/projects/the-critic/webapp/package.json`
  - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
  - `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`
  - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`

## Verification Posture

This slice should stay honest and light.

Default posture:

- docs-first
- code-backed
- no automatic package patch

If the slice remains decision-only, verification is:

- direct code inspection
- explicit comparison against the current package defaults and forwarding behavior
- optional rerun of:
  - `npm run build`
  - `node scripts/check-capture-base.mjs`
  if the memo writer wants a fresh package-local sanity check

If the slice converts into an actual normalization patch, that becomes a different completion path and should then add focused package-local verification and, if the tarball is refreshed into Critic, focused host verification on affected nested surfaces.

## Success Condition

This slice succeeds if it leaves the program with one honest answer to this narrow question:

- is there still one real renderer-substrate blocker between the current package state and a lean `Close Read V1` scope memo

That answer must be explicit enough to change the roadmap cleanly:

- either the next memo becomes lean `Close Read V1`
- or the next memo becomes one bounded forwarding-normalization implementation scope

If the answer is "lean `Close Read V1` can be scoped next", the memo must still say that the resulting product memo needs to handle:

- packed-host integration readiness for a still-tarball-consumed `renderers-ui` line
- host-delivery posture for a still-packed `renderers-ui` dependency line
- app-layer first-hop eligibility policy above the raw package capture utilities

## Strategic Meaning

This is not generic platform cleanup for its own sake.

It is the remaining renderer-substrate decision gate in the now-short corridor toward `Close Read`.

That is why it should be next.
