# Memo: Phase E Renderers-UI Generic Capture-Base Shell Extraction V1 Scope

Subtitle: After the promotion-readiness calibration rejected unchanged helper promotion, the next honest cross-repo move is one bounded top-level package pilot for a package-neutral capture-base shell inside `renderers-ui`, not export of Critic-local first-hop or typed-selection law

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
Immediate Prior Completion:
- `communications/MEMO_2026-04-04_phase_e_current_renderer_selection_emission_shared_seam_promotion_readiness_v1_completion.md`
Relevant Prior Completion:
- `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`
Codebases:
- `/home/evgeny/projects/analyzer-v2/renderers-ui`
- `/home/evgeny/projects/the-critic`

## Purpose

Define the smallest honest package-side follow-on after the readiness verdict:

- `currentRendererCapture` should not be promoted unchanged
- but one smaller package-neutral capture-base shell has been identified as the next honest extraction candidate

This scope should extract only that smaller shell inside `renderers-ui`.
It is a **top-level package pilot** and a **partial first extraction proof**, not the whole package capture convergence story.

## Why This Is The Right Next Step

The readiness slice closed the ownership question honestly.

What is now known:

- the destination package is real and analyzer-v2-owned
- unchanged helper promotion would export Critic-local semantics into the package
- the package already has a raw `config._onCapture` architecture worth converging
- there is still a smaller genuinely shared base beneath both systems

So the next question is no longer:

- should we move `currentRendererCapture` as-is

The next question is:

- can `renderers-ui` extract one package-neutral raw capture-base shell from its existing inline builders without importing Critic-local first-hop, workflow/job, or typed-selection law

## Proposed Bounded Slice

Create one new package utility in `renderers-ui`, tentatively:

1. `resolvePackageCaptureBaseRuntime(config)`
2. `buildPackageCaptureSelectionBase(runtime, params)`

The utility should stay package-native:

- `Record<string, unknown>` payloads only
- no Critic `CaptureSelection` import
- no `_firstHopAffordance` gating
- no `requireWorkflowKey`
- no `requireJobId`
- no `source_workflow_key`
- preserve current package defaulting rather than importing Critic fail-closed behavior

## Exact Shared Responsibility

The extracted shell should own only:

- reading package-common raw capture config:
  - `_captureMode`
  - `_onCapture`
  - `_captureViewKey`
  - `_captureSourceType`
  - optional `_captureJobId`
  - optional `_captureEntityId`
- exposing a package-neutral runtime:
  - `onCapture: (sel: Record<string, unknown>) => void`
  - `sourceViewKey: string`
  - `sourceType: string`
  - `captureJobId?: string`
  - `captureEntityId?: string`
- assembling the raw shared selection base:
  - `source_view_key`
  - `source_type`
  - `context_title`
- composing `context_title` from caller-supplied title segments with the package’s current `>` convention
- optionally applying the package’s existing raw identity fallback:
  - `captureEntityId || captureJobId`
- preserving the package’s current raw defaults:
  - `source_view_key: ''` when absent
  - `source_type: 'analysis'` when absent
  - no helper-owned suppression on missing view key or source type beyond the package’s current `captureMode && onCapture` guard

## Initial Adopters

This v1 should be framed explicitly as a **top-level package pilot only**.

Keep v1 bounded to the clearest package-native top-level builders:

- `renderers-ui/src/renderers/AccordionRenderer.tsx`
- `renderers-ui/src/renderers/CardRenderer.tsx`
- `renderers-ui/src/renderers/CardGridRenderer.tsx`

Do **not** widen v1 to all `SubRenderers` yet.

Why this is the honest first package proof:

- most inline raw capture builders still live in `SubRenderers`, and that heavier surface remains explicitly deferred
- these three renderers express one clean top-level subset of the package raw capture pattern
- they cover section capture, direct card capture, and parent-context-aware card capture
- they are enough for a partial first extraction proof without dragging the whole sub-renderer registry into the same tranche

One realism caveat must stay explicit:

- `SubRenderers` is not only deferred volume; it already has wiring asymmetries
- `AccordionRenderer` does not currently forward `_captureSourceType` or `_captureEntityId` into nested sub-renderers
- `CardRenderer` subsection dispatch does not currently forward capture runtime into nested sub-renderers at all

So this v1 pilot must not be described as representative package-wide proof.
It is only the first clean top-level extraction candidate.

If this bounded top-level extraction works, the next follow-on question can widen honestly to whether the same shell also fits the larger `SubRenderers` builder surface and whether the forwarding asymmetries should be normalized first.

## What Must Stay Out

This slice must not pull the following into `renderers-ui`:

- Critic `CaptureSelection`
- `currentRendererCapture`
- `_firstHopAffordance` fail-closed gating
- `requireWorkflowKey`
- `requireJobId`
- `source_workflow_key`
- `genealogy_job_id`
- human-readable `view_name` + `:` title law
- renderer-specific preview text rules
- renderer-specific `parent_context` policy beyond caller-supplied payload fields
- specialization or nested-handle gating
- any claim that generic renderer-package capture law is now solved

## What Success Looks Like

This slice succeeds if:

- one package-neutral capture-base utility exists in `renderers-ui`
- the three bounded top-level package renderers use it
- emitted raw selection payloads stay behaviorally equivalent
- no Critic-local types or first-hop/workflow semantics leak into the package

This slice does **not** need to prove:

- all package sub-renderers are migrated
- Critic can delete `currentRendererCapture`
- one universal capture contract now spans package and host

## Verification

The proof should include:

- fresh minimal `renderers-ui` test scaffolding or package-consumer harness coverage, because the package does not currently have an established dedicated test harness for this extraction seam
- focused package tests for:
  - runtime resolution
  - title-segment composition with `>`
  - raw identity fallback
  - preservation of current package defaulting for missing `captureViewKey` / `captureSourceType`
  - unchanged emitted payload shape for the three adopters
- Critic-side regression verification only if the packaged tarball is rebuilt and consumed locally

If extraction pressure starts forcing first-hop or workflow/job policy into the package utility, stop and recalibrate instead of widening semantics silently.

## Strategic Meaning

This is still a Phase E substrate-thinning question, but now on the real reusable layer rather than the Critic-local helper.

If it works, it proves:

- there is a smaller honest package-owned shell beneath the current local helper

If it fails cleanly, that is also valuable:

- it would confirm that even the smaller shell is not yet stable enough for promotion and that package/local duality is still the correct architecture
