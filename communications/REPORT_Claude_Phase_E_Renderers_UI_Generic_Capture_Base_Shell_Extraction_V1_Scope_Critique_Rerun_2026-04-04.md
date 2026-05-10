# Critique: Phase E Renderers-UI Generic Capture-Base Shell Extraction V1 Scope

Date: 2026-04-04
Reviewer: Claude (Opus 4.6, 1M context)
Rerun: Yes — this is a second-pass review after the readiness slice completed

Scope Under Review:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_scope.md`

## Context Check

All required documents read in full:

- `communications/MEMO_2026-04-04_phase_e_current_renderer_selection_emission_shared_seam_promotion_readiness_v1_completion.md` — READ
- `communications/REPORT_Codex_Phase_E_Current_Renderer_Selection_Emission_Shared_Seam_Promotion_Readiness_V1_Scope_Audit_2026-04-04.md` — READ
- `communications/REPORT_Claude_Phase_E_Current_Renderer_Selection_Emission_Shared_Seam_Promotion_Readiness_V1_Scope_Critique_2026-04-04.md` — READ
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md` — READ
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md` — READ
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md` — READ
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` — READ (first 150 lines; strategic framing and audit sections)

All required code files inspected directly:

- `renderers-ui/package.json` — READ
- `renderers-ui/src/renderers/AccordionRenderer.tsx` — READ (full, 609 lines)
- `renderers-ui/src/renderers/CardRenderer.tsx` — READ (full, 517 lines)
- `renderers-ui/src/renderers/CardGridRenderer.tsx` — READ (full, 608 lines)
- `renderers-ui/src/sub-renderers/SubRenderers.tsx` — READ (header + registry + grep of all capture paths)
- `the-critic/webapp/src/lib/currentRendererCapture.ts` — READ (full, 85 lines)
- `the-critic/webapp/src/components/V2TabContent.tsx` — READ (lines 575-625, capture config threading)
- `the-critic/webapp/src/contexts/CaptureContext.tsx` — READ (full, 189 lines)

## Verdict

**Approve.**

No corrections required. The scope memo is honest, bounded, codebase-verified, and strategically aligned. It correctly identifies the smallest extraction unit that the package's existing inline capture builders actually share, and it correctly keeps everything that is Critic-local or host-threaded out of that unit.

## Why This Is The Right Next Step (Strategic Alignment)

### Against the distilled roadmap

The distilled roadmap's anti-drift Rule 1 says: "Prefer upstream intelligence over downstream convenience." This extraction moves raw capture-base logic out of renderer-local inline code and into one shared package utility. That is upstream consolidation within analyzer-v2-owned substrate.

Rule 2 says: "Do not confuse bounded proof with generalized architecture." The scope memo is explicit that this is a "partial first extraction proof, not the whole package proof." It does not claim to solve generic renderer-package capture law.

Rule 4 says: "Prefer representative matrices over exhaustive workflow theater." The three-renderer adopter set (accordion, card, card_grid) already covers the three main top-level presentation patterns. That is representative without being exhaustive.

### Against the fixed-direction roadmap

The Phase E line is where this belongs. The fixed-direction roadmap says current-app work is justified if it "codifies a stable host contract or host runtime rule that future consumers will also need." A package-neutral capture-base shell is exactly that — a utility that any future consumer of `@the-syllabus/analysis-renderers` would benefit from.

### Against the analyzer-v2-as-brain objective

The master roadmap says the destination is: "consumer apps should become thin host shells." Extracting common capture-base logic into the analyzer-v2-owned renderer package (`renderers-ui/`) moves capture-base responsibility upstream into analyzer-v2's jurisdiction. The alternative — leaving 3 (soon 11+) inline capture builders across the package — is the opposite of that objective.

## Code-Backed Verification of the Scope Memo's Claims

### Claim 1: The three top-level renderers share a common raw capture config surface

**Verified.** All three read the same six config fields:

| Field | AccordionRenderer | CardRenderer | CardGridRenderer |
|-------|-------------------|--------------|------------------|
| `_captureMode` | line 106 | line 150 | line 181 |
| `_onCapture` | line 107-109 | line 151-153 | line 182-184 |
| `_captureJobId` | line 110 | line 154 | line 185 |
| `_captureViewKey` | line 111 | line 155 | line 186 |
| `_captureSourceType` | line 112 | line 156 | line 187 |
| `_captureEntityId` | line 113 | line 157 | line 188 |

All three type `onCapture` as `(sel: Record<string, unknown>) => void`. None import Critic-local `CaptureSelection`.

### Claim 2: All three use `>` title composition

**Verified.** The inline builders compose `context_title` using `>` chains:

- AccordionRenderer line 377: `` `${captureViewKey || 'Analysis'} > ${section.title || section.key}` ``
- CardRenderer line 290-292: `` `${captureViewKey || 'Analysis'} > ${parentSectionTitle || ''} > ${title}` `` (with parent-context-aware variant)
- CardGridRenderer line 542-543: `` `${config._captureViewKey || 'Analysis'} > ${parentSectionTitle || ''} > ${title}` ``

This is the package convention. The Critic-local helper uses `:` instead (line 81 of `currentRendererCapture.ts`: `` `${runtime.captureViewName}: ${title}` ``). The scope memo correctly excludes the `:` convention.

### Claim 3: All three use `captureEntityId || captureJobId` identity fallback

**Verified.**

- AccordionRenderer line 379: `entity_id: captureEntityId || captureJobId || ''`
- CardRenderer line 294: `entity_id: captureEntityId || captureJobId || ''`
- CardGridRenderer line 545: `entity_id: String(config._captureEntityId || config._captureJobId || '')`

### Claim 4: The proposed shell stays below Critic-local concerns

**Verified by direct code inspection:**

- `CaptureSelection` import: only in `the-critic/webapp/src/lib/currentRendererCapture.ts:1`. Not in any `renderers-ui` file. The package uses `type CaptureSelection = Record<string, unknown>` locally in `SubRenderers.tsx:36` and `CardGridRenderer.tsx:29`.
- `_firstHopAffordance`: only consumed in `currentRendererCapture.ts:40,45` and threaded from `V2TabContent.tsx:597`. Not read by any package renderer.
- `requireWorkflowKey` / `requireJobId`: only in `currentRendererCapture.ts:13-15,48-53`. No equivalent in any package renderer.
- `source_workflow_key`: only emitted by the Critic helper at line 82. The package renderers never emit this field.
- `genealogy_job_id`: only in `CaptureContext.tsx:27` and the submit logic. Not in any package renderer.
- `_captureViewName`: only consumed by `currentRendererCapture.ts:35`. Package renderers do not use this field.

All six exclusion points are codebase-confirmed.

### Claim 5: The proposed utility fits the package's existing `Record<string, unknown>` capture style

**Verified.** The package's existing type convention for capture selections is established at:
- `SubRenderers.tsx:35-36`: `type CaptureSelection = Record<string, unknown>;`
- `CardGridRenderer.tsx:29`: `type CaptureSelection = Record<string, unknown>;`

Every inline builder in the package emits untyped selection objects. The proposed shell's `Record<string, unknown>` return type is consistent with this convention.

## Pressure-Testing the Proposed V1 Extraction Boundary

### Is top-level-renderer-only adoption a valid partial first proof?

**Yes.** The three top-level renderers are the right starting point because:

1. They are the outermost capture originators — AccordionRenderer in particular is the section-level capture surface that also forwards capture config to sub-renderers via an explicit `captureForward` object (lines 517-524). The sub-renderers receive their capture config from these top-level renderers.

2. They exercise three distinct capture patterns:
   - AccordionRenderer: section-level capture with single `>` depth
   - CardRenderer: card-level capture with parent-context-aware depth (L1 or L2)
   - CardGridRenderer: card-in-grid capture with parent-context-aware depth (L1 or L2)

3. Their capture config reading is identical (same 6 fields, same typing). This makes extraction mechanically clean.

4. The total adopter count (3) is small enough to verify behavioral equivalence exhaustively.

### Is deferring SubRenderers still strategically honest?

**Yes, and I can quantify why.**

I grepped every capture-config destructuring in `SubRenderers.tsx` and found **8 sub-renderers** with inline capture builders:
- DefinitionList (lines 537-542)
- MiniCardList (lines 727-732)
- One at lines 1379-1384
- One at lines 1867-1872
- One at lines 2144-2149
- One at lines 2379-2384
- One at lines 2814-2819
- One at lines 3067-3072

All 8 read the same 6 config fields. All 8 use the same `>` title composition convention. All 8 use the same `captureEntityId || captureJobId` identity fallback.

The deferral is honest for two reasons:

1. **The sub-renderer capture surface is ~2.5x larger than the top-level surface.** Including 8 additional adopters in v1 would triple the verification burden without changing the extraction shape.

2. **Sub-renderer title composition is more varied.** Some sub-renderers compose 3+ level `>` chains (e.g., `captureViewKey > parentSectionTitle > groupName > title` at line 2307). The top-level renderers cap at 2-3 levels. Testing the simpler variants first is the right order.

3. **The sub-renderers receive capture config FROM the top-level renderers.** The forwarding path (AccordionRenderer lines 517-524) means the sub-renderers are downstream consumers of whatever the top-level renderers provide. Extracting the base at the top level first is architecturally sound — the sub-renderers can adopt the same shell in a follow-on without changing the forwarding contract.

That said, the evidence is strong that the sub-renderers WILL fit the same shell. This is a deferred win, not a deferred uncertainty.

### Is the proposed package-neutral shell the right candidate — too broad or too narrow?

**It is correctly sized.**

The shell would own:
- Config reading (6 fields)
- Runtime resolution (gated on `captureMode && onCapture`)
- Title-segment composition with `>`
- Shared selection base (`source_view_key`, `source_type`, `context_title`)
- Identity fallback (`captureEntityId || captureJobId`)

What it would NOT own (correctly excluded):
- Renderer-specific fields: `source_section_key`, `source_item_index`, `source_renderer_type`, `content_type`, `selected_text`, `structured_data`, `depth_level`, `parent_context`
- Forward-threading to sub-renderers (AccordionRenderer's `captureForward` object)
- Capture status map reading (`_captureStatusMap`, AccordionRenderer line 114-118)
- Capture button rendering

This is the right split. The shell owns what's common; each renderer adds what's specific. No renderer-specific concerns leak into the shell, and no shared concerns remain inline.

**One observation about breadth:** The AccordionRenderer also reads `_captureStatusMap` (line 114-118) for capture-status dots. This is renderer-specific and correctly excluded from the shell. The memo does not mention it explicitly, but the exclusion is correct because status-map reading is a read-side concern unrelated to selection assembly.

## Explicit Check Points

### 1. The readiness memo uses candidate-language, not "already proved extraction truth"

**Confirmed.** The readiness completion memo says:
- "the strongest next honest **candidate** for promotion" (line 73)
- "next honest extraction **candidate**" (line 128)
- "if it works" / "if it fails cleanly, that is also valuable" (scope memo lines 161-167)

No premature certainty claims.

### 2. The next scope is explicitly a partial first extraction proof, not the whole package proof

**Confirmed.** The scope memo says at line 33: "It is a **partial first extraction proof**, not the whole package capture convergence story."

The "What Success Looks Like" section (lines 129-143) explicitly lists what the slice does NOT need to prove:
- all package sub-renderers migrated
- Critic can delete `currentRendererCapture`
- one universal capture contract now spans package and host

### 3. The proposed shared shell stays below the listed exclusions

**Confirmed by direct code inspection** (see "Claim 4" above). All six exclusion points are verified absent from any package renderer code:
- Critic `CaptureSelection`: not imported
- `_firstHopAffordance`: not read
- `requireWorkflowKey`: not used
- `requireJobId`: not used
- `source_workflow_key`: not emitted
- `genealogy_job_id`: not referenced

### 4. The proposed utility fits the package's existing `Record<string, unknown>` capture style

**Confirmed.** The package defines `CaptureSelection = Record<string, unknown>` locally in both `SubRenderers.tsx:36` and `CardGridRenderer.tsx:29`. All inline builders emit untyped objects. The proposed shell's return type matches.

### 5. The roadmap wording matches what the docs-first readiness slice actually established

**Confirmed.** The distilled roadmap (updated 2026-04-04) says at line 502:

> Phase D exit signal met; Phase E is active, its first twenty-one bounded proof/code slices plus one bounded readiness-calibration slice are complete [...] and the next honest code gap is one bounded `renderers-ui` generic capture-base shell extraction slice

The state-of-play memo says at line 454:

> the next bounded Phase E scope should now target one bounded `renderers-ui` generic capture-base shell extraction slice, because the helper-level ownership question is now closed and the narrower shared candidate is explicit

Both match exactly what the scope memo proposes.

## Minor Observations (Not Corrections)

### 1. AccordionRenderer capture-config forwarding

AccordionRenderer lines 517-524 build a `captureForward` object that threads capture config into sub-renderers. The extraction shell should NOT try to own this forwarding — it is renderer-specific dispatch behavior. The scope memo implicitly handles this by scoping the shell to "runtime resolution" and "selection base assembly" only. When the sub-renderer follow-on slice comes, the forwarding path will remain renderer-owned.

### 2. CardGridRenderer's capture button lives in `CardWrapper`

The CardGridRenderer's actual capture emission happens in the `CardWrapper` component (lines 524-551), not in the top-level `CardGridRenderer` function. The config is already destructured at the top-level (lines 181-188) but the emission uses `config._captureViewKey` references rather than the local `captureViewKey` variable. The shell will need to be designed so that either pattern (local variable from runtime or direct config property access) works cleanly, or the adoption should normalize to one style.

### 3. Sub-renderer adoption will be the larger follow-on

8 sub-renderers versus 3 top-level renderers means the follow-on slice will be larger in adopter count. The scope memo acknowledges this honestly at line 105: "most inline raw capture builders still live in `SubRenderers`, and that heavier surface remains explicitly deferred."

## Strategic Assessment

This scope memo is the cleanest Phase E extraction scope I've reviewed. It:

1. Derives directly from the readiness-calibration verdict
2. Targets exactly the code surface that the readiness calibration identified
3. Does not overclaim (no "generic renderer capture law solved")
4. Does not underclaim (the three adopters are genuinely representative)
5. Has a clear failure mode ("if extraction pressure starts forcing first-hop or workflow/job policy into the package utility, stop and recalibrate")
6. Advances the analyzer-v2-as-brain objective by consolidating capture-base logic into analyzer-v2-owned shared substrate

The proposed work passes the distilled roadmap's anti-drift filter on all four questions:
1. Does it move intelligence upstream into analyzer-v2? **Yes** — into analyzer-v2-owned `renderers-ui`.
2. Does it reduce host-specific analytical behavior? **Yes** — replaces 3 inline builders with one shared utility.
3. Does it strengthen generic law rather than one more special case? **Yes** — the utility is package-neutral, not renderer-specific.
4. Does it help eventual contract-based generality? **Yes** — establishes the base layer that sub-renderers and future renderers can adopt.

## Final Verdict

**Approve.** Execute as scoped.
