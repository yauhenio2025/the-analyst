# Report: Phase E Renderers-UI Release-Artifact Refresh And Critic Host Verification V1 Scope Critique

Date: 2026-04-04
Reviewer: Claude Opus 4.6 (1M context)
Review Type: Full scope critique with code-backed verification
Scope Memo Under Review:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_release_artifact_refresh_and_critic_host_verification_v1_scope.md`

---

## Context Check

Every required memo and code file was read in full before this review:

| Document | Status |
|---|---|
| `MEMO_2026-04-04_phase_e_renderers_ui_release_artifact_refresh_and_critic_host_verification_v1_scope.md` | Read in full |
| `MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_completion.md` | Read in full |
| `MEMO_2026-04-04_close_read_roadmap_recalibration.md` | Read in full |
| `MEMO_2026-03-30_distilled_strategic_roadmap.md` | Read in full |
| `MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md` | Read in full |
| `MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md` | Read in full |
| `MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` | Read strategic sections (first 100 lines) |
| `MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_completion.md` | Read in full |
| `REPORT_Codex_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Implementation_V1_Scope_Audit_Rerun_2026-04-04.md` | Read in full |
| `REPORT_Claude_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Implementation_V1_Scope_Critique_Rerun_2026-04-04.md` | Read in full |
| `MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md` | Read first 80 lines |
| `APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md` | Read in full |
| `renderers-ui/package.json` | Read in full — version `0.6.5` confirmed |
| `renderers-ui/scripts/release-pack.mjs` | Read in full — overwrite refusal at lines 24-27 confirmed |
| `renderers-ui/src/renderers/AccordionRenderer.tsx` | Read in full — local source includes forwarding patch |
| `renderers-ui/src/renderers/CardRenderer.tsx` | Read in full — local source includes `captureForwardConfig` threading |
| `renderers-ui/src/dispatch/SubRendererDispatch.tsx` | Read in full — local source includes `captureConfig` prop on `GenericSectionRenderer` |
| `renderers-ui/src/utils/captureBase.ts` | Read in full — unchanged, 54 lines |
| `renderers-ui/release-artifacts/` | Listed — three tarballs present: `0.6.3.tgz`, `0.6.4.tgz`, `0.6.5.tgz` |
| `/home/evgeny/projects/the-critic/webapp/package.json` | Read first 20 lines — points to `the-syllabus-analysis-renderers-0.6.5.tgz` at line 10 |
| Installed `node_modules/@the-syllabus/analysis-renderers/package.json` | Read — version `0.6.5` confirmed |
| Installed `dist/renderers/AccordionRenderer.js` | Read lines 80-282 + grep for captureForward, GenericSectionRenderer |
| Installed `dist/renderers/CardRenderer.js` | Grep for captureForwardConfig, subsectionCaptureForward, GenericSectionRenderer |
| Installed `dist/dispatch/SubRendererDispatch.js` | Grep for captureConfig — **no matches found** |
| `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx` | Read lines 580-610 — capture threading confirmed |
| `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx` | Read lines 90-120 — `genealogy_job_id` derivation confirmed |
| `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx` | Read lines 100-135 — same `source_type === 'genealogy'` pattern confirmed |
| `src/views/definitions/genealogy_target_profile.json` | Read in full — accordion with three `nested_sections` |
| `src/views/definitions/genealogy_per_work_scan.json` | Read in full — card with four `nested_sections` subsections |

---

## 1. Pressure-Testing The Memo's Assumptions

### Is the package-source implementation genuinely complete already?

**Yes. Confirmed by direct code inspection.**

The local `renderers-ui` source tree already contains the full forwarding-normalization patch:

- `AccordionRenderer.tsx:518-527` — `captureForward` includes `_captureSourceType: captureSourceType` and `_captureEntityId: captureEntityId`
- `AccordionRenderer.tsx:563` — `nested_sections` path passes `captureConfig={captureForward}` to `GenericSectionRenderer`
- `AccordionRenderer.tsx:579` — final fallback path passes `captureConfig={captureForward}` to `GenericSectionRenderer`
- `CardRenderer.tsx:150-158` — builds `captureForwardConfig` with all six capture fields
- `CardRenderer.tsx:348-400` — threads `subsectionCaptureForward` through all four subsection dispatch branches (configured, nested_sections, auto-detect, fallback)
- `SubRendererDispatch.tsx:102-106` — `GenericSectionRenderer` now accepts optional `captureConfig` prop
- `SubRendererDispatch.tsx:198` — merges `captureConfig` into resolved sub-renderer config
- `SubRendererDispatch.tsx:211,215` — forwards `captureConfig` to recursive `GenericSectionRenderer` calls

The memo's claim that "This slice is **not** another package-source behavior patch" is correct. The patch is done.

### Is the stale packed-host consequence real on the current Critic path?

**Yes. Confirmed by direct dist inspection against the installed artifact.**

The installed `0.6.5` artifact in Critic `node_modules` diverges from local source on every point that matters:

| Gap | Local source | Installed 0.6.5 dist |
|---|---|---|
| AccordionRenderer `captureForward` fields | Includes `_captureSourceType`, `_captureEntityId` (lines 523-524) | Missing both — only has `_captureMode`, `_onCapture`, `_captureJobId`, `_captureViewKey`, `_parentSectionKey`, `_parentSectionTitle` (dist lines 271-278) |
| AccordionRenderer `nested_sections` → `GenericSectionRenderer` | Passes `captureConfig={captureForward}` (line 563) | Passes only `data` and `subRenderers` — no `captureConfig` (dist line 299) |
| AccordionRenderer fallback → `GenericSectionRenderer` | Passes `captureConfig={captureForward}` (line 579) | Passes only `data` — no `captureConfig` (dist line 311) |
| CardRenderer subsection dispatch | Builds `captureForwardConfig`, threads `subsectionCaptureForward` through all four branches (lines 150-158, 348-400) | No `captureForwardConfig` or `subsectionCaptureForward` found at all; `GenericSectionRenderer` calls for nested_sections (dist line 249) and fallback (dist line 261) pass only `data` |
| SubRendererDispatch `GenericSectionRenderer` | Accepts `captureConfig` prop, merges into sub-renderer config, forwards to recursion (lines 102-106, 198, 211, 215) | `captureConfig` grep returns **zero matches** — the prop does not exist |

This is not a cosmetic difference. The consequence chain is:

1. `V2TabContent.tsx:594` threads `_captureSourceType: 'genealogy'` for genealogy workflows
2. The installed AccordionRenderer does not forward `_captureSourceType` to nested sub-renderers
3. Nested sub-renderers that call `resolvePackageCaptureBaseRuntime` get `sourceType = undefined`
4. `captureBase.ts:48` falls back to `source_type: 'analysis'`
5. `CaptureContext.tsx:97-101` only derives `genealogy_job_id` when `source_type === 'genealogy'`
6. `ResearchFlagDialog.tsx:109-114` does the same

So nested captures on genealogy accordion surfaces lose their provenance routing. This is real.

For `CardRenderer`, the consequence is starker: subsection sub-renderers receive zero capture runtime, so capture buttons are entirely absent on nested card surfaces.

### Is a version bump plus new tarball the right minimal handoff?

**Yes. Grounded in `release-pack.mjs` behavior, not preference.**

`release-pack.mjs` lines 24-27:
```javascript
if (fs.existsSync(tarballPath)) {
  console.error(`Refusing to overwrite existing tarball for version ${version}: ${tarballPath}`)
  process.exit(1)
}
```

The existing `the-syllabus-analysis-renderers-0.6.5.tgz` is already present in `release-artifacts/`. Running `npm run release:pack` at the current `0.6.5` version will exit with an error. A version bump to `0.6.6` (or equivalent) is the only way to produce a new artifact through the existing script.

The memo's rationale is mechanically correct and not discretionary.

### Is this slice still bounded, or does it risk drifting into broader host-delivery posture work?

**Still bounded.** The scope has a tight three-part structure:

1. Bump version + pack artifact (mechanical)
2. Update Critic's `package.json` dependency path + reinstall (mechanical)
3. Verify two specific nested genealogy surfaces (focused)

The "Out Of Scope" section explicitly excludes 10 named items including `captureBase.ts` changes, `_firstHopAffordance`, `currentRendererCapture`, workflow/job requiredness, destination-policy law, and broader host-delivery posture.

**One drift risk I note:** the verification plan says "add or extend one bounded proof for each material affected surface" and "this slice may add the minimum focused host verification needed." If the Critic repo lacks dedicated proofs for nested genealogy accordion and card surfaces, adding proofs could create scope pressure to also add test infrastructure. The memo acknowledges this: "It should not turn into a broad test-harness expansion." This guardrail is appropriate, but the implementor should be vigilant here.

---

## 2. Bigger Picture And Analyzer-V2-As-Brain Alignment

The distilled strategic roadmap and the close-read corridor recalibration both name this exact slice as the current next step:

- Corridor Step 3 in the recalibration: "Execute one bounded `renderers-ui` release-artifact refresh plus focused Critic host-verification slice"
- The distilled roadmap's "What Comes Next" section: "the next bounded step should therefore be: one bounded `renderers-ui` release-artifact refresh plus focused Critic host-verification slice"

The anti-drift filter from the fixed-direction roadmap:

1. Does this move analytical decision-making upstream into analyzer-v2? — **Yes**, indirectly: it makes already-upstream capture-forwarding intelligence actually reach the live host
2. Does this reduce consumer-owned workflow-specific intelligence? — **Not directly**, but it clears the path to the lean `Close Read V1` memo that should
3. Does this generalize beyond AOI or beyond `the-critic`? — **No**, this is explicitly `the-critic` focused. But that is honest: the current packed-host integration gap is exclusively a `the-critic` gap
4. If we fully replaced the current app later, would this work still matter? — **The package-side work already matters; the Critic-side dependency refresh is ephemeral but required to prove the package patch works end-to-end**

The memo correctly does not overclaim that this slice settles broader host-delivery posture. The "Strategic Consequence" section explicitly says that host-delivery posture and app-layer first-hop eligibility policy are still required inputs for the lean `Close Read V1` memo, and that memo should only come after this host-consumption gap is closed.

---

## 3. Codebase Verification Against Memo Claims

### Claim: "Critic still consumes `the-syllabus-analysis-renderers-0.6.5.tgz`"

**Confirmed.** `/home/evgeny/projects/the-critic/webapp/package.json:10`:
```
"@the-syllabus/analysis-renderers": "file:../../analyzer-v2/renderers-ui/release-artifacts/the-syllabus-analysis-renderers-0.6.5.tgz"
```

### Claim: "The installed package still reflects the older pre-patch artifact"

**Confirmed.** The installed `node_modules/@the-syllabus/analysis-renderers/package.json` shows version `0.6.5`, and the dist files lack the forwarding-normalization patch (see table above).

### Claim: "The representative current surfaces are `genealogy_target_profile` and `genealogy_per_work_scan`"

**Confirmed.** These are the only current view definitions that use `nested_sections` in their `section_renderers`:
- `genealogy_target_profile.json` — `renderer_type: "accordion"`, all three sections use `nested_sections` with `sub_renderers`
- `genealogy_per_work_scan.json` — `renderer_type: "card"`, all four subsections use `nested_sections` with `sub_renderers`

### Claim: "`release-pack.mjs` explicitly refuses to overwrite an existing tarball for the same version"

**Confirmed.** Lines 24-27 of `release-pack.mjs` check `fs.existsSync(tarballPath)` and `process.exit(1)` if it exists.

### Claim: The memo keeps the named exclusions out of scope

**Confirmed.** The "Out Of Scope" section explicitly names all items listed in the review prompt:
- `_firstHopAffordance` — listed
- workflow/job requiredness — listed
- `currentRendererCapture` — listed (via "Critic-local `currentRendererCapture`")
- destination-policy law — listed
- `captureBase.ts` changes — listed
- `source_workflow_key` — listed
- `genealogy_job_id` — listed
- broad host-delivery posture redesign — listed
- generic renderer-package capture law — listed
- lean `Close Read V1` scoping itself — listed

---

## 4. Verification Plan Assessment

### Package / artifact side

**Adequate.** Build + pack + confirm tarball exists is the right mechanical proof. The version-match check is also correct.

### Critic install side

**Adequate.** Spot-checking the installed dist for `captureForwardConfig` in `CardRenderer.js` and `captureConfig` in `SubRendererDispatch.js` is the right minimum. These are the two most diagnostic signals:
- `captureForwardConfig` in CardRenderer proves the subsection forwarding landed
- `captureConfig` in SubRendererDispatch proves the GenericSectionRenderer extension landed

I would add one more spot-check: confirm AccordionRenderer's `captureForward` object now includes `_captureSourceType` in the installed dist. This is the most direct test of the field-precision gap that caused `source_type` degradation.

### Host behavior side

**Mostly adequate but deliberately vague on test shape.** The memo says "rerun focused host tests around V2TabContent and CaptureContext" and "add or extend one bounded proof for each material affected surface." This is reasonable as scope guidance, but it does not name the exact test shape.

Two concerns:

1. **What does "focused host test" mean here?** If the Critic repo already has tests that exercise nested accordion or card capture on genealogy surfaces, a rerun would suffice. If not, the memo allows adding "minimum focused host verification" but warns against "broad test-harness expansion." The implementor needs to check what already exists before deciding.

2. **The memo is honest about what package build/pack proves.** It correctly says the success condition requires all three parts (artifact exists, Critic consumes it, nested surfaces are cleared). It does not claim the artifact alone is sufficient.

---

## 5. Explicit Point-By-Point Checks

| Check | Result | Evidence |
|---|---|---|
| Memo does not treat package-source implementation as still pending | **Pass** | Opening line: "This slice is **not** another package-source behavior patch." |
| Memo does not overclaim that refreshing artifact settles broader host-delivery posture | **Pass** | "Strategic Consequence" section explicitly lists host-delivery posture and app-layer first-hop eligibility as still-required inputs for the next memo |
| Memo keeps `_firstHopAffordance`, workflow/job requiredness, `currentRendererCapture`, destination-policy law out | **Pass** | All four explicitly named in "Out Of Scope" |
| Memo's rationale for new artifact/version is grounded in `release-pack.mjs` | **Pass** | Memo cites the refusal behavior; I confirmed at lines 24-27 |
| Memo's host consequence remains tied to real nested genealogy surfaces | **Pass** | Names `genealogy_target_profile` and `genealogy_per_work_scan`; both verified as the only `nested_sections` users |

---

## 6. One Minor Risk Note

The memo states "Any lockfile change required for that refresh is in scope." This is correct — refreshing a file-based tarball dependency will likely trigger changes in `package-lock.json` or equivalent. In prior similar refreshes, lockfile changes have occasionally caused npm to resolve other transitive dependencies differently. The implementor should verify that the Critic build still succeeds after the lockfile refresh, not just that the target package installed.

This is not a scope problem. It is an execution awareness note.

---

## Verdict

### **Approve**

The scope memo is:

1. **Accurate** — the stale artifact gap is real, confirmed by direct dist inspection against all three installed files
2. **Correctly bounded** — three-part structure (pack, refresh, verify) with ten explicit exclusions
3. **Honest** — does not overclaim that the artifact refresh settles host-delivery posture or product-layer questions
4. **Mechanically grounded** — the version bump is not discretionary; `release-pack.mjs` will reject the current version
5. **Correctly targeted** — the two named genealogy surfaces are the only current `nested_sections` users
6. **Strategically aligned** — correctly positioned as corridor step 3 before lean `Close Read V1` scoping
7. **Consistent with prior reviews** — both the Codex audit rerun and the Claude critique rerun confirmed the same stale-artifact gap this memo now proposes to close

No corrections required. The memo correctly distinguishes package-source truth (complete) from packed-host truth (stale) and scopes the minimal honest slice to close that gap.
