# Memo: Phase E Renderers-UI Release-Artifact Refresh And Critic Host Verification V1 Completion

Subtitle: The already-landed `renderers-ui` forwarding patch is now live on Critic through a new `0.6.6` packed artifact and real installed-package host proofs

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
Implements:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_release_artifact_refresh_and_critic_host_verification_v1_scope.md`
Immediate Prior Completion:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_completion.md`
Review Context:
- `communications/REPORT_Claude_Phase_E_Renderers_UI_Release_Artifact_Refresh_And_Critic_Host_Verification_V1_Scope_Critique_2026-04-04.md`
- `communications/REPORT_Codex_Phase_E_Renderers_UI_Release_Artifact_Refresh_And_Critic_Host_Verification_V1_Scope_Audit_2026-04-04.md`
Package Codebase:
- `/home/evgeny/projects/analyzer-v2/renderers-ui`
Host Codebase:
- `/home/evgeny/projects/the-critic/webapp`

## Purpose

Record completion of the bounded cross-repo handoff slice that turned already-correct `renderers-ui` source into live Critic behavior.

This slice was intentionally narrower than generic package publishing or product scoping.
Its job was only to:

- pack one traceable new local `renderers-ui` artifact
- refresh Critic's file-based dependency to that artifact
- prove the two material nested genealogy consequences on the real installed host path

It did not widen into:

- new package-source forwarding work
- Critic-side first-hop policy redesign
- destination-policy redesign
- `Close Read V1` scoping itself

## Outcome

That bounded handoff is now complete.

The current truth is now:

- local `renderers-ui` source already contained the required forwarding patch
- a new `0.6.6` tarball now carries that patch in packed form
- Critic now consumes that new tarball through both manifest and lockfile
- the installed package under Critic `node_modules` now reflects the forwarding additions
- the two material nested genealogy host consequences are now proven on the real installed package path

So the active gap is no longer:

- package-source forwarding behavior
- or packed-host drift

The next honest step is now:

- one lean `Close Read V1` scope memo

## What Landed

### 1. One new traceable `renderers-ui` artifact

`renderers-ui/package.json` was bumped from `0.6.5` to `0.6.6`.

`npm run release:pack` then produced:

- `renderers-ui/release-artifacts/the-syllabus-analysis-renderers-0.6.6.tgz`

The emitted artifact identity from `release-pack.mjs` is:

- `version = 0.6.6`
- `tarball_name = the-syllabus-analysis-renderers-0.6.6.tgz`
- `tarball_sha256 = 86f5eeeebb4d30282f2f8d3aa71429e3e5e8bfdb44b64d52eed6295d089a661f`

That closes the artifact-traceability requirement honestly.

### 2. Critic was intentionally refreshed onto the new packed artifact

Critic now points at the new tarball in:

- `/home/evgeny/projects/the-critic/webapp/package.json`

and the install state was refreshed through:

- `/home/evgeny/projects/the-critic/webapp/package-lock.json`
- `npm install` in `/home/evgeny/projects/the-critic/webapp`

The installed package now reports:

- `@the-syllabus/analysis-renderers = 0.6.6`

So this slice did not stop at changing nearby source truth.
It restored packed-host truth.

### 3. The installed dist now reflects the forwarding patch

The minimum installed-dist checks all flipped from stale to correct:

- `node_modules/@the-syllabus/analysis-renderers/dist/renderers/AccordionRenderer.js`
- `node_modules/@the-syllabus/analysis-renderers/dist/renderers/CardRenderer.js`
- `node_modules/@the-syllabus/analysis-renderers/dist/dispatch/SubRendererDispatch.js`

Those installed files now contain the expected forwarding signatures:

- `_captureSourceType` / `_captureEntityId` forwarding in `AccordionRenderer`
- `captureForwardConfig` in `CardRenderer`
- `captureConfig` pass-through in `SubRendererDispatch`

That is the exact point where the earlier stale-artifact gap is now closed.

### 4. Two real installed-package host proofs now exist

The bounded host-proof tranche landed in:

- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/InstalledPackageNestedCapture.test.tsx`

The important boundary is:

- these proofs do not mock `@the-syllabus/analysis-renderers`
- they exercise Critic's real installed package path

Proof 1: `genealogy_target_profile`

- nested accordion capture is present
- the handed-off selection preserves `source_type: 'genealogy'`

Proof 2: `genealogy_per_work_scan`

- nested card-subsection capture is present
- the handoff reaches `CaptureActionBar`

So the proof surface now matches the material consequences that justified the previous decision and implementation tranches.

## What Did Not Change

This slice did **not**:

- add any new package-source forwarding logic
- change `captureBase.ts`
- redesign Critic's `CaptureActionBar`
- make `CaptureActionBar` honor `allowed_destinations`
- change `_firstHopAffordance` law
- redesign host-delivery posture beyond the local tarball handoff already in use
- scope or build `Close Read V1`

Those remain separate questions.

## Verification

### Package side

- `cd /home/evgeny/projects/analyzer-v2/renderers-ui && npm run release:pack`
  - passed

### Host install side

- `cd /home/evgeny/projects/the-critic/webapp && npm install`
  - passed

### Focused host verification

- `CI=1 npm test -- --watchAll=false --runInBand --runTestsByPath src/components/renderers/InstalledPackageNestedCapture.test.tsx src/components/V2TabContent.test.tsx src/contexts/CaptureContext.test.tsx`
  - `3 suites passed, 14 tests passed`

Environment notes:

- the existing Jest open-handle warning is unchanged
- no new host/browser verification tranche was required beyond the installed-package proofs for this slice

## Verdict

The honest verdict is:

- **the packed-host handoff is complete**
- **the stale-artifact gap is closed**
- **the renderer-substrate corridor is now materially clear enough to move to product scoping**

## Strategic Consequence

The corridor toward `Close Read` now reads:

1. package-native capture-base extraction is complete
2. dominant `SubRenderers` adoption is complete
3. forwarding decision is complete
4. forwarding-normalization implementation is complete in package source
5. release-artifact refresh plus focused Critic host verification is now also complete
6. the next honest step is now one lean `Close Read V1` scope memo

That next memo must still resolve, explicitly:

- host-delivery posture
- app-layer first-hop eligibility policy

But it no longer needs to wait on renderer-substrate drift or stale packed-host consumption.

## Next Honest Step

The next bounded step should now be:

- one lean `Close Read V1` scope memo

That memo should stay grounded in:

- runtime-real first-hop operations
- current real destinations:
  - Arsenal
  - Research todo
- already-proved host surfaces

and it should keep these deferred:

- destination-internal lifecycle unification
- workflow-neutral destination taxonomy
- generic renderer-package capture law
- multi-user / multi-project product architecture
- Book Modeler and other non-runtime-real destinations
