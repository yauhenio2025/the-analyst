# Report: Phase E Renderers-UI Release-Artifact Refresh And Critic Host Verification V1 Scope Audit

## Context Check

Required memo inputs read in full:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_release_artifact_refresh_and_critic_host_verification_v1_scope.md` — read in full
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_completion.md` — read in full
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md` — read in full
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md` — read in full
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md` — read in full
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md` — read in full
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` — read in full
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_completion.md` — read in full
- `communications/REPORT_Codex_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Implementation_V1_Scope_Audit_Rerun_2026-04-04.md` — read in full
- `communications/REPORT_Claude_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Implementation_V1_Scope_Critique_Rerun_2026-04-04.md` — read in full
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md` — read in full
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md` — read in full

Required code and artifact inputs inspected directly:

- `renderers-ui/package.json` — inspected directly
- `renderers-ui/scripts/release-pack.mjs` — inspected directly
- `renderers-ui/src/renderers/AccordionRenderer.tsx` — inspected directly
- `renderers-ui/src/renderers/CardRenderer.tsx` — inspected directly
- `renderers-ui/src/dispatch/SubRendererDispatch.tsx` — inspected directly
- `renderers-ui/src/utils/captureBase.ts` — inspected directly
- `renderers-ui/release-artifacts/the-syllabus-analysis-renderers-0.6.5.tgz` — inspected directly
- `/home/evgeny/projects/the-critic/webapp/package.json` — inspected directly
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/package.json` — inspected directly
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/renderers/AccordionRenderer.js` — inspected directly
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/renderers/CardRenderer.js` — inspected directly
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/dispatch/SubRendererDispatch.js` — inspected directly
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx` — inspected directly
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx` — inspected directly
- `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx` — inspected directly
- `src/views/definitions/genealogy_target_profile.json` — inspected directly
- `src/views/definitions/genealogy_per_work_scan.json` — inspected directly

Additional direct verification performed:

- `cd renderers-ui && npm run build` — passed
- `cd renderers-ui && node scripts/check-capture-base.mjs` — passed
- `cd renderers-ui && node scripts/release-pack.mjs` — failed exactly as expected because `0.6.5` already exists and overwrite is refused
- `cd /home/evgeny/projects/the-critic/webapp && npm test -- --runInBand --watch=false src/contexts/CaptureContext.test.tsx src/components/ResearchFlagDialog.test.tsx src/components/V2TabContent.test.tsx` — passed

## Verdict

`approve with corrections`

The scope names the right bounded next step and stays aligned with the short corridor toward lean `Close Read V1`. The needed corrections are in the verification plan, not the strategic framing.

## Confirmed Facts

### 1. The forwarding patch is already present in local `renderers-ui` source

Confirmed.

- `renderers-ui/src/renderers/AccordionRenderer.tsx:107-114` already reads `_captureSourceType` and `_captureEntityId`.
- `renderers-ui/src/renderers/AccordionRenderer.tsx:518-579` already forwards those fields and already passes `captureConfig={captureForward}` into both `GenericSectionRenderer` call sites.
- `renderers-ui/src/renderers/CardRenderer.tsx:150-158` already builds `captureForwardConfig`.
- `renderers-ui/src/renderers/CardRenderer.tsx:348-400` already threads that config through configured, `nested_sections`, auto-detect, and fallback subsection paths.
- `renderers-ui/src/dispatch/SubRendererDispatch.tsx:102-106` already defines `captureConfig`.
- `renderers-ui/src/dispatch/SubRendererDispatch.tsx:198-215` already forwards `captureConfig` through sub-renderer dispatch and recursion.
- `renderers-ui/src/utils/captureBase.ts:22-54` remains unchanged, which matches the memo's boundedness claim.

So the memo's baseline in `communications/MEMO_2026-04-04_phase_e_renderers_ui_release_artifact_refresh_and_critic_host_verification_v1_scope.md:26-58` is accurate: the current gap is packaging/integration, not remaining source implementation.

### 2. Critic still points at the stale `0.6.5` artifact

Confirmed.

- `renderers-ui/package.json:3` is still `0.6.5`.
- `/home/evgeny/projects/the-critic/webapp/package.json:10` still points at `file:../../analyzer-v2/renderers-ui/release-artifacts/the-syllabus-analysis-renderers-0.6.5.tgz`.
- `/home/evgeny/projects/the-critic/webapp/package-lock.json:15` and `/home/evgeny/projects/the-critic/webapp/package-lock.json:3441-3444` still resolve that exact tarball.
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/package.json:3` is also still `0.6.5`.

This makes the scope's artifact-refresh step at `...scope.md:62-92` necessary and honest.

### 3. The installed `node_modules` dist still reflects the old omission paths

Confirmed.

The local source and installed dist are now materially different:

- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/renderers/AccordionRenderer.js:271-278` still builds `captureForward` without `_captureSourceType` or `_captureEntityId`.
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/renderers/AccordionRenderer.js:297-311` still passes no `captureConfig` to `GenericSectionRenderer`.
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/renderers/CardRenderer.js:238-261` still forwards no capture runtime through the subsection paths.
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/dispatch/SubRendererDispatch.js:78-78` still defines `GenericSectionRenderer` without `captureConfig`.
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/dispatch/SubRendererDispatch.js:124-131` still passes only `subHint.config || {}` and does not recurse with forwarded capture config.

I also directly compared tarball contents against the installed package on the three key files and they matched exactly, so the stale host package is not just "some old install"; it is consistent with the current `0.6.5` artifact.

### 4. `release-pack.mjs` really forces a new version/tarball instead of overwriting

Confirmed in both code and execution.

- `renderers-ui/scripts/release-pack.mjs:21-27` computes the tarball path for the current version and exits if it already exists.
- `renderers-ui/scripts/release-pack.mjs:60-66` also requires the packed filename to match the version-derived tarball name and emits a traceable SHA-256.
- Running `cd renderers-ui && node scripts/release-pack.mjs` on the current tree produced: `Refusing to overwrite existing tarball for version 0.6.5`.

So the scope is correct that a version bump is not optional churn. It is structurally required by the release script.

### 5. The two material host consequences are still the right ones

Confirmed.

The representative surfaces still directly exercise the missing live-host behavior:

- `src/views/definitions/genealogy_target_profile.json:17-40` is an `accordion` whose relevant sections all use `nested_sections`.
- `src/views/definitions/genealogy_per_work_scan.json:13-50` is a `card` surface whose four subsections all use `nested_sections`.
- `src/views/definitions/genealogy_per_work_scan.json:80` confirms the per-work scan remains `planner_eligible`.

The host still makes genealogy `source_type` materially consequential:

- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:589-595` threads `_captureSourceType: 'genealogy'` for genealogy workflows and `_captureEntityId` from `presentation.job_id`.
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:97-102` derives `genealogy_job_id` fallback only when `source_type === 'genealogy'`.
- `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx:109-114` does the same on the direct research-todo save path.

That means the scope is right to keep the live proof focused on:

- genealogy nested accordion provenance truth
- genealogy nested card-subsection capture availability

## Strategic Judgment

The scope still fits the roadmap honestly.

It matches the corridor frozen across the April 4 roadmap docs:

1. the forwarding patch is already landed in local package source
2. the remaining gap is artifact refresh plus host verification
3. only after that does lean `Close Read V1` scoping become the next honest product-facing step

The scope also stays bounded in the right way:

- it explicitly defers host-delivery posture redesign
- it explicitly defers app-layer first-hop eligibility redesign
- it does not pretend package refresh equals broader package/host convergence

I do not see broader host-delivery redesign hidden inside the requested slice.

## Required Corrections

### 1. Make `package-lock.json` explicit in the refresh/verification steps

The scope says lockfile changes are in scope at `...scope.md:92`, but the refresh section at `...scope.md:78-92` should name the file directly:

- `/home/evgeny/projects/the-critic/webapp/package-lock.json`

Reason:

- the lockfile is currently stale in exactly the same way as `package.json`
- leaving it implicit weakens the "Critic is actually consuming the new artifact" proof

### 2. Add `AccordionRenderer.js` to the installed-dist verification minimum

The current install-side minimum at `...scope.md:148-151` only names:

- `dist/renderers/CardRenderer.js`
- `dist/dispatch/SubRendererDispatch.js`

That should be expanded to include:

- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/renderers/AccordionRenderer.js`

Reason:

- one of the two material consequences is specifically the genealogy accordion provenance fix
- the old installed omission is visible there at `AccordionRenderer.js:271-311`

### 3. Tighten the host-verification plan so it must hit the actual installed package path

The current host-verification wording at `...scope.md:157-166` is directionally right but too loose.

Why it needs tightening:

- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.test.tsx:22-41` mocks `./ViewRenderer`, so those tests do not exercise the installed renderer package.
- `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.test.tsx:21-57` mocks `@the-syllabus/analysis-renderers`, so those tests also do not exercise the installed package.
- The targeted host tests I reran all passed, but they prove surrounding host seams only. They do not prove the stale/live nested renderer behavior on `genealogy_target_profile` or `genealogy_per_work_scan`.
- A direct search under `/home/evgeny/projects/the-critic/webapp/tests` found no existing Playwright proof keyed to `genealogy_target_profile` or `genealogy_per_work_scan`.

Concrete correction:

- keep the `V2TabContent` and `CaptureContext` reruns as supporting checks
- but require at least one proof per material surface that reaches the actual package-backed render path

Bounded acceptable shapes:

- one focused component/integration test that does not mock `ViewRenderer` or `@the-syllabus/analysis-renderers`, using the actual genealogy view payloads
- or one focused Playwright/browser proof per surface on the live host path

Without that correction, the plan risks proving only host seam continuity while missing the exact stale-package gap this memo is supposed to close.

## Verification Reruns

### Package-side

- `cd renderers-ui && npm run build` — passed
- `cd renderers-ui && node scripts/check-capture-base.mjs` — passed
- Existing unchanged warning still emitted: `MODULE_TYPELESS_PACKAGE_JSON`

### Artifact-side

- `cd renderers-ui && node scripts/release-pack.mjs` — failed exactly as expected with overwrite refusal on `0.6.5`

### Host-side

- `cd /home/evgeny/projects/the-critic/webapp && npm test -- --runInBand --watch=false src/contexts/CaptureContext.test.tsx src/components/ResearchFlagDialog.test.tsx src/components/V2TabContent.test.tsx` — passed

Interpretation:

- these tests are worth keeping in the slice
- they are not sufficient proof of the live nested renderer fix unless the package-backed render path is exercised in addition

## Bottom Line

The memo's main call is correct:

- refresh the artifact
- refresh the Critic dependency
- verify the two live genealogy consequences
- do not widen into broader host redesign

Approve it with three concrete corrections:

1. name `/home/evgeny/projects/the-critic/webapp/package-lock.json` explicitly
2. add installed `AccordionRenderer.js` to the minimum dist spot-check list
3. require at least one actual package-backed proof per affected surface, not only mocked `V2TabContent` and host-seam tests
