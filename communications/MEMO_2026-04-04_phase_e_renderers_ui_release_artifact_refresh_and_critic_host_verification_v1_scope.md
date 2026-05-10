# Memo: Phase E Renderers-UI Release-Artifact Refresh And Critic Host Verification V1 Scope

Subtitle: Make the already-landed nested forwarding patch live on the current host path by packing a traceable `renderers-ui` artifact, refreshing Critic’s local dependency, and proving the affected nested genealogy surfaces

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
Immediate Prior Completion:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_completion.md`
Package Codebase:
- `/home/evgeny/projects/analyzer-v2/renderers-ui`
Host Codebase:
- `/home/evgeny/projects/the-critic/webapp`

## Purpose

Execute the smallest honest slice that turns the already-landed local `renderers-ui` forwarding patch into live behavior on the current Critic host path.

This slice is **not** another package-source behavior patch.

Its job is to:

- produce a traceable packed artifact from the updated `renderers-ui` source
- make Critic consume that artifact intentionally
- prove the two previously material nested genealogy consequences on the live host path are cleared

It must not widen into:

- broader host-delivery posture redesign
- app-layer first-hop eligibility redesign
- generic package publishing/process work beyond this local artifact handoff
- `Close Read V1` product scoping

## Why This Slice Is Now The Next Honest Step

The bounded forwarding-normalization implementation is already present in local package source.

But Critic still consumes:

- `/home/evgeny/projects/the-critic/webapp/package.json`
- `file:../../analyzer-v2/renderers-ui/release-artifacts/the-syllabus-analysis-renderers-0.6.5.tgz`

and the installed package in:

- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers`

still reflects the older pre-patch artifact.

So the live-host consequence is still real, but it is now a packaging/integration gap, not a remaining source-implementation gap.

## Scope

### 1. Produce a traceable new artifact

Do not overwrite the existing `0.6.5` tarball in place.

Reason:

- `renderers-ui/scripts/release-pack.mjs` explicitly refuses to overwrite an existing tarball for the same version

So this slice should:

- bump `renderers-ui/package.json` version from `0.6.5` to one new patch version
- run `npm run release:pack`
- produce one new tarball under `renderers-ui/release-artifacts/`

The version bump is part of the honesty of the handoff, not incidental churn.

### 2. Refresh Critic’s local package dependency

Update:

- `/home/evgeny/projects/the-critic/webapp/package.json`
- `/home/evgeny/projects/the-critic/webapp/package-lock.json`

to point at the new tarball path.

Then refresh the installed dependency in Critic so that:

- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers`

matches the new artifact rather than the stale `0.6.5` build.

Any lockfile change required for that refresh is in scope.

### 3. Verify the live host consequence on the two material nested genealogy lines

This slice should prove the refreshed host path resolves the two exact consequences that motivated the decision gate:

1. `AccordionRenderer` genealogy nested surfaces
   - nested captures should now preserve `source_type: 'genealogy'` on the live host path instead of silently falling back to `'analysis'`
   - the `_captureEntityId` point should remain calibrated honestly:
     - no separate current live divergence is required to prove success there
     - the material current proof is the `source_type` routing consequence

2. `CardRenderer` nested genealogy surfaces
   - nested subsection capture controls should now be present on the live host path where they were previously absent

The representative current surfaces are still:

- `src/views/definitions/genealogy_target_profile.json`
- `src/views/definitions/genealogy_per_work_scan.json`

## Out Of Scope

Keep these explicitly out:

- any new package-source forwarding logic beyond what is already landed
- `captureBase.ts` changes
- Critic-local `currentRendererCapture`
- `_firstHopAffordance`
- workflow/job requiredness
- `source_workflow_key`
- `genealogy_job_id`
- destination-policy law
- generic renderer-package capture law
- broad host-delivery posture redesign
- lean `Close Read V1` scoping itself

## Verification Plan

### Package / artifact side

Rerun:

- `cd renderers-ui && npm run build`
- `cd renderers-ui && npm run release:pack`

Confirm:

- the new tarball exists in `renderers-ui/release-artifacts/`
- the tarball version matches `renderers-ui/package.json`

### Critic install side

Refresh the dependency in:

- `/home/evgeny/projects/the-critic/webapp`

and confirm the installed package reflects the updated code paths, not the stale artifact. At minimum, spot-check the installed dist for:

- capture forwarding in `node_modules/@the-syllabus/analysis-renderers/dist/renderers/AccordionRenderer.js`
- `captureForwardConfig` in `dist/renderers/CardRenderer.js`
- `captureConfig` support in `dist/dispatch/SubRendererDispatch.js`

### Host behavior side

Use focused host verification, not vague “it should work now” confidence.

At minimum:

- rerun focused host tests around:
  - `V2TabContent`
  - `CaptureContext`
- treat those targeted host tests only as supporting stability evidence; they are not sufficient on their own to prove the package-backed nested renderer fix
- add or extend one bounded proof for each material affected surface:
  - one proof for nested genealogy accordion capture provenance on `genealogy_target_profile`
  - one proof for nested genealogy card-subsection capture availability on `genealogy_per_work_scan`
- each of those proofs must exercise the actual installed `@the-syllabus/analysis-renderers` package path in Critic rather than a mocked renderer/module boundary

If the current repo lacks dedicated proofs for those exact package-backed surfaces, this slice may add the minimum focused host verification needed. It should not turn into a broad test-harness expansion.

## Success Condition

This slice is successful only if all three are true:

1. the updated local package source is packed into a new traceable artifact
2. Critic is actually consuming that new artifact
3. the two material nested genealogy host consequences are cleared on the current host path

It is **not** enough to show only:

- local `renderers-ui` source is correct
- or the tarball exists
- or Critic installs without proving the affected nested surfaces

## Strategic Consequence

If this slice lands cleanly, then the roadmap can move honestly to:

- one lean `Close Read V1` scope memo

with two explicit product-layer inputs still required in that memo:

- host-delivery posture
- app-layer first-hop eligibility policy

But that product memo should only come after this host-consumption gap is closed, not before.
