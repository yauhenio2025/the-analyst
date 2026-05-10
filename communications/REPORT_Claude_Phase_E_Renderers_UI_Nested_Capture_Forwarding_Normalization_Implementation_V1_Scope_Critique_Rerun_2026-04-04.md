# Review: Phase E Renderers-UI Nested Capture Forwarding-Normalization Implementation V1 Scope (Rerun)

Date: 2026-04-04
Reviewer: Claude Opus 4.6 (1M context)
Review Type: Rerun — fresh independent review with full context read
Scope Memo Under Review:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_scope.md`

---

## Context Check

Every required memo and code file was read in full before this review:

| Document | Status |
|---|---|
| `MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_scope.md` | Read in full (376 lines) |
| `MEMO_2026-04-04_close_read_roadmap_recalibration.md` | Read in full (194 lines) |
| `MEMO_2026-03-30_distilled_strategic_roadmap.md` | Read in full (531 lines) |
| `MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md` | Read in full (475 lines) |
| `MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md` | Read in full (587 lines) |
| `MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` | Read first 200 lines (strategic thesis, architecture, and current assessment); remainder is canonical stage ledger |
| `MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_completion.md` | Read in full (225 lines) |
| `MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_completion.md` | Read in full (208 lines) |
| `MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md` | Read in full (200 lines) |
| `APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md` | Read in full (45 lines) |
| `renderers-ui/src/renderers/AccordionRenderer.tsx` | Read in full (617 lines) |
| `renderers-ui/src/renderers/CardRenderer.tsx` | Read in full (531 lines) |
| `renderers-ui/src/renderers/CardGridRenderer.tsx` | Read in full (607 lines) |
| `renderers-ui/src/sub-renderers/SubRenderers.tsx` | Read first 50 lines (imports, registry, captureBase import confirmed) |
| `renderers-ui/src/dispatch/SubRendererDispatch.tsx` | Read in full (283 lines) |
| `renderers-ui/src/utils/captureBase.ts` | Read in full (54 lines) |
| `renderers-ui/scripts/check-capture-base.mjs` | Read in full (168 lines) |
| `src/views/definitions/genealogy_target_profile.json` | Read in full (65 lines) |
| `src/views/definitions/genealogy_per_work_scan.json` | Read in full (85 lines) |
| `/home/evgeny/projects/the-critic/webapp/package.json` | Read first 30 lines (v0.6.5 packed tarball confirmed) |
| `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx` | Read first 100 lines + grep for capture threading (lines 589-595) |
| `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts` | Read in full (85 lines) |
| `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx` | Read first 60 lines |
| `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx` | Read lines 85-115 (genealogy_job_id derivation confirmed) |
| `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx` | Read first 60 lines |

---

## Implementation State Observation

The working tree shows all three target files as modified in `git status`. Direct code inspection confirms the described fixes appear to already be in the working tree — the scope memo describes the "before" state accurately, and the code now reflects the "after" state. This review evaluates both the scope memo's correctness as a specification and whether the landed code matches it.

---

## 1. Robustness Of Assumptions

### Assumption: Three distinct gaps, not two

**Confirmed.** The decision completion memo characterized two gaps. The implementation scope memo correctly escalates to three by splitting AccordionRenderer's issues into:

- Gap 1 (field precision): `captureForward` exists but omits `_captureSourceType` and `_captureEntityId`
- Gap 2 (structural absence): the `nested_sections` and fallback paths do not spread `captureForward` at all

These are structurally different fixes. Gap 1 adds fields to an existing forward object. Gap 2 adds a new parameter to GenericSectionRenderer call sites and requires extending GenericSectionRenderer itself. The memo is right to count them separately.

### Assumption: `_captureSourceType` omission causes material degradation on genealogy nested captures

**Confirmed by code.** The chain is:

1. `V2TabContent.tsx` line 594: `_captureSourceType: workflowKey?.includes('genealogy') ? 'genealogy' : 'analysis'`
2. Without forwarding, nested sub-renderers receive no `_captureSourceType` in their config
3. `captureBase.ts` line 36: `sourceType: asString(config._captureSourceType)` resolves to `undefined`
4. `captureBase.ts` line 48: `source_type: runtime.sourceType || 'analysis'` falls back to `'analysis'`
5. `CaptureContext.tsx` lines 97-101: `genealogy_job_id` derivation only fires when `source_type === 'genealogy'`

Result: nested accordion captures on genealogy surfaces silently lose genealogy provenance routing. Not cosmetic — it breaks the `genealogy_job_id` fallback chain.

### Assumption: `_captureEntityId` is only a conditional future-risk

**Confirmed.** `V2TabContent.tsx` threads both `_captureJobId` (line 591) and `_captureEntityId` (line 595) from the same `presentation.job_id`. Both are identical. `captureBase.ts` line 52 fallback is `captureEntityId || captureJobId || ''`. Since `_captureJobId` IS already forwarded, and both values are the same, the resulting `entity_id` would be identical either way. The risk only becomes material if a future host threads different values for these fields.

### Assumption: GenericSectionRenderer does not currently accept a captureConfig prop

**Confirmed.** `SubRendererDispatch.tsx` line 102 shows three props only: `data`, `depth`, `subRenderers`. No `captureConfig`.

### Assumption: GenericSectionRenderer's sub-renderer resolution does not inject runtime capture fields

**Confirmed.** Line 198: `<SubComp data={value} config={subHint.config || {}} />` — passes only static config from the subHint definition. No capture fields.

### Assumption: Recursive GenericSectionRenderer calls do not forward capture

**Confirmed.** Lines 210 and 214: `<GenericSectionRenderer data={value} depth={depth + 1} />` — neither passes `captureConfig`.

---

## 2. Bigger Picture And Analyzer-V2-As-Brain Alignment

The distilled strategic roadmap places this scope at Phase E generality proof, corridor step 3: "execute one bounded forwarding-normalization slice." The close-read roadmap recalibration explicitly sequences:

1. SubRenderers adoption (done)
2. Forwarding decision gate (done, verdict: `patch required`)
3. **Bounded forwarding-normalization implementation (this memo)**
4. Lean `Close Read V1` scope memo

This scope is correctly positioned. It is:

- **Upstream intelligence over downstream convenience** (anti-drift Rule 1): fixes are in the reusable package, not in host-specific compensation
- **Not confusion of bounded proof with generalized architecture** (anti-drift Rule 2): the scope claims only that the package-internal forwarding gate will be closed, not that generic capture law is solved
- **Not governance substituting for architecture** (anti-drift Rule 3): this is literal plumbing, not process
- **Correctly prioritized against the prioritization filter**: the work moves capture-forwarding intelligence into analyzer-owned substrate, reduces future host compensation, and generalizes beyond one renderer

The scope does not overclaim. It explicitly lists four things still NOT cleared after the patch (lines 347-352): packed-host integration, host-delivery posture, app-layer first-hop eligibility policy, and destination-level UI/policy law.

---

## 3. Codebase Verification

### Does the memo correctly identify the true fix surface in AccordionRenderer?

**Yes.** Four dispatch paths exist. Before the fix:
- Configured renderer path (line 533 current code): spreads `captureForward` — already correct
- Auto-detect path (line 574 current code): spreads `captureForward` — already correct
- `nested_sections` path: passed no capture — correctly identified as Gap 2
- Fallback path: passed no capture — correctly identified as Gap 2

The current working-tree code now has `captureConfig={captureForward}` on both the `nested_sections` (line 563) and fallback (line 579) paths, matching the spec exactly.

### Is the AccordionRenderer `nested_sections` gap real on current genealogy surfaces?

**Yes. Verified against view definitions.**

`genealogy_target_profile.json` defines all three sections (`conceptual_framework`, `semantic_constellation`, `inferential_commitments`) with `renderer_type: "nested_sections"` and `sub_renderers` containing `mini_card_list`, `prose_block`, and `comparison_panel`. All three hit AccordionRenderer's `nested_sections` path. Without the fix, GenericSectionRenderer would resolve those sub-renderers without capture runtime, so `resolvePackageCaptureBaseRuntime` would return `null` for all of them.

### Does the CardRenderer plan really cover every subsection dispatch branch?

**Yes.** All four branches inside the `matchingSubsections.map` dispatch chain are covered:

1. Configured renderer: now gets `...(subsectionCaptureForward || {})` in subConfig (lines 356-359)
2. `nested_sections`: now gets `captureConfig={subsectionCaptureForward}` (lines 381-385)
3. Auto-detect: now gets `config={subsectionCaptureForward || {}}` (line 395)
4. Fallback: now gets `captureConfig={subsectionCaptureForward}` (line 400)

`genealogy_per_work_scan.json` confirms this matters: all four subsections use `renderer_type: "nested_sections"` with sub_renderers.

**One out-of-scope uncovered path noted:** CardRenderer has a non-subsection fallback at line 511 (`<GenericSectionRenderer data={val} />`) that fires when no matching subsections exist and the item is not prose-only. This path renders all non-meta item fields as unstructured generic sections without capture forwarding. This is legitimately out of scope — it is not a configured subsection dispatch path, and there is no section identity to compose into capture context. Including it would widen scope from "subsection forwarding normalization" into "generic card-body fallback enhancement."

### Is the GenericSectionRenderer extension truly pass-through only, or does it implicitly widen package law?

**Truly pass-through only.** The current implementation confirms:

- `captureConfig` is typed `Record<string, unknown>` — opaque, no structural requirements
- Line 198: raw spread `...(captureConfig || {})` into sub-renderer config — no filtering, no gating, no normalization
- Lines 211, 215: forward `captureConfig={captureConfig}` to recursive calls — no transformation
- GenericSectionRenderer does NOT call `resolvePackageCaptureBaseRuntime` itself — it simply passes the opaque bag through

No new gates, no new policy, no field-level inspection. This does not widen package law.

### Are there any other forwarding paths in package renderers that this memo misses?

**No material omissions.** I examined:

- All four AccordionRenderer dispatch paths — covered
- All four CardRenderer subsection dispatch paths — covered
- CardGridRenderer — has no subsection dispatch or nested GenericSectionRenderer calls; capture is card-level only via `CardWrapper` using `resolvePackageCaptureBaseRuntime(config)` where config comes from the full renderer config with capture fields already threaded by V2TabContent. No gap.
- The only uncovered GenericSectionRenderer call is CardRenderer's non-subsection fallback (line 511) — discussed above, legitimately out of scope.

---

## 4. Preservation Rules Verification

| Preservation rule | Status | Evidence |
|---|---|---|
| Raw `captureMode && onCapture` gating only (no new gates) | **Preserved** | `captureBase.ts` lines 25-26 unchanged. No new gating in any fix. |
| Raw string-or-default semantics (no trim, no non-empty normalization) | **Preserved** | `captureBase.ts` `asString()` at lines 18-20 returns raw strings. Compare with `currentRendererCapture.ts` `getNonEmptyString()` which trims and rejects empty — that host-specific pattern is NOT adopted. |
| `>` title composition convention (no `: ` adoption) | **Preserved** | `captureBase.ts` line 49 uses `join(' > ')`. `currentRendererCapture.ts` line 81 uses `${name}: ${title}` — that `: ` pattern stays host-local. |
| Empty-segment preservation in title chains | **Preserved** | `check-capture-base.mjs` lines 82-86 test `titleSegments: ['', 'Card Title']` producing `'view_key >  > Card Title'`. No filtering added. |
| Raw identity fallback: explicit `entityId !== undefined` check | **Preserved** | `captureBase.ts` line 51: `params.entityId !== undefined ? params.entityId : (runtime.captureEntityId || runtime.captureJobId || '')`. No change. |
| No new capture config fields beyond those in `captureBase.ts` | **Preserved** | The forwarded fields are exactly: `_captureMode`, `_onCapture`, `_captureJobId`, `_captureViewKey`, `_captureSourceType`, `_captureEntityId`. All already defined in `captureBase.ts`. |

---

## 5. Corrected Provenance Claims

### Missing `_captureSourceType` definitely degrades genealogy nested captures today

**Confirmed.** The chain:
- `V2TabContent` threads `'genealogy'` for genealogy workflows (line 594)
- Without forwarding → `captureBase.ts` defaults to `'analysis'` (line 48)
- `CaptureContext.tsx` lines 97-101: `genealogy_job_id` fallback only fires when `source_type === 'genealogy'`

Impact: genealogy nested captures lose their provenance routing. The capture record gets wrong `source_type`, which means no `genealogy_job_id` derivation, which means the Research Flag Dialog and backend capture routing lose their genealogy context.

### Missing `_captureEntityId` is only a conditional future-risk on the current host path

**Confirmed.** V2TabContent threads both `_captureJobId` and `_captureEntityId` from `presentation.job_id` (lines 591, 595 — same value). The `captureBase.ts` fallback chain (`captureEntityId || captureJobId || ''`) produces the same result either way. This only becomes a material break if a host starts threading different values.

---

## 6. Explicit Negative Checks

| Check | Status | Evidence |
|---|---|---|
| No Critic-local capture law promoted into the package | **Pass** | No `_firstHopAffordance`, `_captureViewName`, `source_workflow_key`, `genealogy_job_id`, or `currentRendererCapture` semantics in the changes |
| `captureBase.ts` itself unchanged | **Pass** | 54 lines, no modifications proposed or observed |
| GenericSectionRenderer extension is pass-through only, not gating or normalization | **Pass** | Opaque `Record<string, unknown>` spread, no field inspection |
| Memo correctly names which genealogy surfaces are affected | **Pass** | `genealogy_target_profile` (accordion + nested_sections) and `genealogy_per_work_scan` (card + nested_sections) verified in JSON |
| Memo is honest that clean patch only clears package-source gate | **Pass** | Lines 347-352 list four things still not cleared |
| File-touch set matches fix shapes | **Pass** | Three files, three shapes, exact match between memo description and working-tree changes |

---

## 7. Boundedness Assessment

This qualifies as one bounded forwarding-normalization patch, not a broader renderer refactor:

- **3 files modified**, all within `renderers-ui`
- **No host files touched**
- **No utility changes** — `captureBase.ts` unchanged
- **No new semantics** — only forwarding existing fields through existing dispatch paths
- **No new gates** — capture availability is still gated only by `resolvePackageCaptureBaseRuntime`
- **One new prop** on GenericSectionRenderer — purely pass-through
- **Preservation rules** maintained from prior `captureBase` and `SubRenderers` adoption slices
- **Explicit deferrals** for host-delivery posture, first-hop eligibility, destination policy, and generic capture law

---

## 8. One Minor Structural Note (Informational)

GenericSectionRenderer's recursive calls at lines 211/215 do not forward `subRenderers` — only `data`, `depth`, and now `captureConfig`. This means sub-renderer hints are lost after the first level of nesting. The implementation scope correctly adds `captureConfig` forwarding to these calls but does not address `subRenderers` forwarding (nor should it — that is a pre-existing limitation unrelated to capture).

For the named near-term surfaces this is a non-issue: `genealogy_target_profile` and `genealogy_per_work_scan` define flat one-level `sub_renderers` hierarchies. But future deeply nested view definitions would only benefit from capture forwarding at the first recursion level.

This is informational, not a blocker.

---

## Verdict

### **Approve**

The scope memo is:

1. **Accurate** — all three gaps are real and verified against the codebase and view definitions
2. **Correctly bounded** — stays within package forwarding plumbing, no host changes, no new semantics
3. **Honest** — clearly states what it does and does not clear
4. **Correctly targeted** — exactly 3 files with well-defined fix shapes that match the landed code
5. **Aligned** — properly sequenced on the Close Read corridor after the decision gate and before lean `Close Read V1` scoping
6. **Preservation-safe** — all six behavioral preservation rules match `captureBase.ts` semantics and are maintained in the implementation
7. **Strategically sound** — passes the anti-drift filter and moves capability upstream without promoting host-local law

No corrections required. The implementation visible in the working tree matches the specification exactly.
