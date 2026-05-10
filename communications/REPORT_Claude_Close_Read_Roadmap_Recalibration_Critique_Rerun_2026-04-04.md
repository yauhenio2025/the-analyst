# Review: Close Read Roadmap Recalibration — Critique Rerun

Date: 2026-04-04
Reviewer: Claude Opus 4.6
Target Memo: `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`

---

## Context Check

Every required memo and code file was read in full before this review:

| Document | Status |
|---|---|
| `MEMO_2026-04-04_close_read_roadmap_recalibration.md` | Read in full |
| `MEMO_2026-03-30_distilled_strategic_roadmap.md` | Read in full |
| `MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md` | Read in full |
| `MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md` | Read in full |
| `MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` | Read (first 200 lines — strategic audit, accomplished work, and current position sections) |
| `MEMO_2026-04-01_close_read_operations_and_routing_inventory.md` | Read in full |
| `MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md` | Read in full |
| `APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md` | Read in full |
| `MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_completion.md` | Read in full |
| `MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_scope.md` | Read in full |
| `renderers-ui/src/renderers/AccordionRenderer.tsx` | Read in full (607 lines) |
| `renderers-ui/src/renderers/CardRenderer.tsx` | Read in full (509 lines) |
| `renderers-ui/src/renderers/CardGridRenderer.tsx` | Read in full (607 lines) |
| `renderers-ui/src/sub-renderers/SubRenderers.tsx` | Read first 100 lines (registry, auto-detect); file too large for full read — verified `captureBase` import and usage via grep |
| `renderers-ui/src/utils/captureBase.ts` | Read in full (54 lines) |
| `renderers-ui/scripts/check-capture-base.mjs` | Read in full (168 lines) |
| `the-critic/webapp/src/components/V2TabContent.tsx` | Read capture-threading section (lines 580-610) plus type definitions (lines 1-150) |
| `the-critic/webapp/src/contexts/CaptureContext.tsx` | Read first 100 lines (types, provider, `CaptureSelection` interface) |
| `the-critic/webapp/src/components/CaptureActionBar.tsx` | Read first 100 lines (action handlers, Arsenal/Research routing) |
| `the-critic/webapp/src/lib/currentRendererCapture.ts` | Read in full (85 lines) |

---

## 1. Robustness Of The Memo's Assumptions

### Assumption: The SubRenderers adoption surface is complete

**Verdict: confirmed**

The SubRenderers completion memo documents exactly eight migrated inline builders, and direct code inspection of `SubRenderers.tsx` confirms the `captureBase` import at line 36-38. The package verification script at `check-capture-base.mjs` covers representative fixtures for gate behavior, default semantics, title composition patterns (2/3/4-segment), empty-segment preservation, and entity-id precedence. The adoption is real, not notional.

### Assumption: The remaining uncertainty is the nested runtime-forwarding line

**Verdict: confirmed with precision**

Direct code inspection confirms the two exact asymmetries the completion memo documents:

1. **AccordionRenderer (line 516-523)**: forwards `_captureMode`, `_onCapture`, `_captureJobId`, `_captureViewKey`, `_parentSectionKey`, `_parentSectionTitle` — but **omits** `_captureSourceType` and `_captureEntityId`. These are fields that `V2TabContent` threads at lines 594-595.

2. **CardRenderer**: grep for `captureForward`, `_captureMode`, `_onCapture`, `_captureSourceType`, `_captureEntityId` in the nested subsection dispatch returns **zero matches**. The subsection rendering path (lines 339-378) does not forward any capture runtime into nested sub-renderers at all.

The package utility `resolvePackageCaptureBaseRuntime` gracefully degrades on missing fields: `sourceType` defaults to `undefined` which becomes `'analysis'` in `buildPackageCaptureSelectionBase`, and `captureEntityId` defaults to `undefined` which falls back through `captureJobId || ''`. So the AccordionRenderer case produces semantically defensible (though imprecise) capture selections. The CardRenderer case produces no capture buttons at all on nested sub-renderers.

### Assumption: One decision gate now remains before a lean Close Read V1 scope memo

**Verdict: mostly honest, but slightly understated — see Section 4 below**

---

## 2. Alignment With The Bigger Picture And The Analyzer-v2-As-Brain Objective

The memo is well-aligned with the strategic hierarchy:

- The **distilled strategic roadmap** positions Phase E as the current active phase and identifies the forwarding-normalization decision as the next bounded step. The recalibration memo does not contradict this — it sharpens it by framing the same step as the first prerequisite in a product-facing corridor rather than open-ended substrate work.

- The **fixed-direction roadmap** explicitly states (in the final boundary section): "if the strategic target is now to actually build Close Read, the roadmap should read this not as indefinite substrate work but as a short corridor." The recalibration memo directly implements this guidance.

- The **canonical master roadmap** places the program at roughly 30-40% for the full task-to-bespoke-app destination. The recalibration memo does not overclaim progress against this broader bar. Its corridor stays within the proved engine families (genealogy, AOI) and current real destinations (Arsenal, Research), which is appropriate for a lean V1.

- The **state-of-play memo** confirms that Phases A-D have bounded exits and Phase E is active. The recalibration memo correctly reads the SubRenderers completion as a Phase E advance rather than as a Phase F productization step.

- The **operations/routing inventory** and its matrix appendix provide the runtime evidence base for the "current real destinations" claim. The matrix confirms Arsenal and Research todo as `runtime_real` first-hop destinations with concrete endpoint seams. The memo's proposed lean Close Read V1 bounds (first-hop operations, Arsenal, Research) are exactly the `runtime_real / first_hop` rows in the matrix. This is grounded, not aspirational.

**Assessment: the memo correctly stays inside the proved substrate and does not outrun the evidence.**

---

## 3. Scrutiny Against The Actual Codebase

### Package utility vs Critic-local utility: an honest gap the memo respects

The package utility (`captureBase.ts`) and the Critic-local helper (`currentRendererCapture.ts`) are not equivalent:

| Concern | Package `captureBase` | Critic `currentRendererCapture` |
|---|---|---|
| Gate logic | `_captureMode === true && onCapture is function` | Same plus `sourceViewKey`, `captureViewName`, `sourceType` all non-empty, plus `_firstHopAffordance.capturable === true` |
| String normalization | Raw preservation (no trim, empty strings pass) | `getNonEmptyString`: trim + check |
| Affordance gating | None | `_firstHopAffordance.capturable` required |
| Workflow key | Not read | `_workflowKey` read, optional `requireWorkflowKey` |
| View name | Not read | `_captureViewName` read and required |
| Title composition | `viewKey > ...segments` joined with ` > ` | `captureViewName: title` with `: ` separator |

The memo does **not** claim that the package utility replaces the Critic utility. The SubRenderers completion memo explicitly lists as "does not mean": `currentRendererCapture is now obsolete`. This is honest.

### V2TabContent capture threading: confirmed complete at the entry point

V2TabContent (lines 588-597) threads all necessary fields to the top-level renderer config:
- `_captureMode`, `_onCapture`, `_captureJobId`, `_captureViewKey`, `_captureViewName`
- `_captureSourceType` (workflow-aware: `'genealogy'` vs `'analysis'`)
- `_captureEntityId` (from `presentation.job_id`)
- `_captureStatusMap`, `_firstHopAffordance`

The top-level renderers (Accordion, Card, CardGrid) all call `resolvePackageCaptureBaseRuntime(config)` and correctly consume this threading for their own capture buttons. The asymmetry only appears in the **forwarding to nested children**.

### AccordionRenderer forwarding gap: real but gracefully degraded

AccordionRenderer forwards 6 fields to sub-renderers (line 516-523) but omits `_captureSourceType` and `_captureEntityId`. In the package utility's `buildPackageCaptureSelectionBase`, this means:
- `source_type` defaults to `'analysis'` (acceptable for most surfaces, incorrect for genealogy-type views)
- `entity_id` falls back to `captureJobId || ''` (the job ID is forwarded, so this produces a reasonable but less precise identity)

This is a real imprecision, not a hard break. Nested sub-renderers under accordion sections will show capture buttons and produce capture selections that route correctly to Arsenal/Research — but with less precise provenance metadata.

### CardRenderer subsection gap: functional absence

CardRenderer's subsection dispatch (lines 339-378) does not forward any capture config at all. This means sub-renderers nested inside card subsections will have `resolvePackageCaptureBaseRuntime` return `null`, and no capture buttons will appear.

For a lean Close Read V1, this matters if CardRenderer is used with subsections that themselves contain capturable content. Looking at the codebase, CardRenderer is used for relationship classification cards (genealogy), which have subsections like "analysis", "evidence_base" — content a user might want to capture.

This is the stronger of the two asymmetries and the one that genuinely may require a bounded normalization patch.

---

## 4. Pressure-Testing The "Short Corridor" Framing

### Is it honest that only one renderer-substrate decision gate remains?

**Mostly honest, with one subtle understatement.**

The forwarding-normalization decision is correctly identified as the last meaningful **renderer-package** gate. But the memo slightly understates the difference between the two asymmetries:

- The AccordionRenderer case is a **field-defaulting** question: capture buttons appear, metadata is slightly imprecise.
- The CardRenderer case is a **functional-availability** question: capture buttons do not appear at all on nested subsections.

The memo treats both under the single label "forwarding-normalization decision," which is technically correct (both are forwarding gaps), but the CardRenderer case is qualitatively different and potentially requires a different fix (adding a `captureForward` block to the subsection dispatch, not just adding missing fields).

The scope memo for the forwarding-normalization decision (`MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_scope.md`) does correctly name both asymmetries and explicitly asks whether each needs normalization. So the pair of memos together is honest. But the recalibration memo alone slightly flatters the corridor by making the decision sound like a single uniform question when it has two distinct sub-questions with different fix shapes.

### Is there another blocker the memo understates?

**One additional concern worth naming: affordance gating.**

The package utility does not implement `_firstHopAffordance` gating. The Critic-local utility requires `_firstHopAffordance.capturable === true` before any capture runtime resolves. For Close Read V1, some form of affordance gating will be needed — otherwise every view gets capture buttons regardless of whether the analyzer tagged it as capturable.

This is **not** a renderer-substrate blocker (it's a product-layer question), and the memo correctly positions it below the line. But the corridor description would be more honest if it explicitly acknowledged that the lean Close Read V1 scope memo will need to address affordance gating as a **product-layer gate** even though it's not a package-substrate gate. Without this acknowledgment, a reader might think the corridor steps are: (1) forwarding decision, (2) write scope memo, (3) build — when in reality the scope memo itself will need to resolve the affordance-gating question.

### Is the proposed lean Close Read V1 framing grounded in runtime-real evidence?

**Yes.**

The operations/routing inventory matrix provides concrete evidence for:
- Arsenal promotion: `runtime_real`, concrete endpoints (`POST /api/captures`, `POST /api/captures/{id}/to-arsenal`)
- Research todo routing: `runtime_real`, concrete endpoints (`POST /api/captures`, `POST /api/research-todos`, `POST /api/captures/{id}/to-research-todo`)

The engine families mentioned (genealogy, AOI) are the exact families that have proved composition paths through Phase E. The output families are already rendered by the proved renderer trio (Accordion, CardGrid, Card) plus the proved sub-renderer set.

The memo does **not** claim Book Modeler integration, outline routing, or other aspirational destinations. It bounds to Arsenal and Research, which is exactly the `runtime_real / first_hop` evidence.

---

## 5. Product Pull: Appropriately Sharpened Or Outrunning Proved Substrate?

The memo does a good job of calibrating product pull:

**What it correctly sharpens:**
- Close Read is now an explicit near-term target, not a distant proving-ground abstraction
- The remaining substrate work is framed as a prerequisite in a product-facing corridor
- The program should stop sounding like "platform generality first, product later"

**What it correctly defers:**
- Destination-internal lifecycle unification
- Book Modeler integration
- Workflow-neutral destination taxonomy
- Full multi-user / multi-project architecture
- Generic downstream operation law

**Assessment: product pull is appropriately calibrated.** The memo does not overclaim readiness for full productization. It asks for one more decision gate, then a lean scope memo. That is the right pace.

---

## 6. Explicit Checklist

| Check | Status |
|---|---|
| Memo no longer treats Close Read as a distant proving-ground abstraction only | **Pass** — lines 29-31 explicitly reframe Close Read as "the explicit near-term product target" |
| Memo still keeps full productization deferred | **Pass** — lines 60-68 list five deferred concerns, lines 133-136 list what lean V1 is "not" |
| Memo does not overclaim that nested forwarding is already solved | **Pass** — lines 92-96 frame it as an explicit decision gate, not assumed-solved |
| Path to lean Close Read V1 is bounded to runtime-real first-hop operations | **Pass** — lines 104-108 restrict to first-hop only, current real destinations (Arsenal, Research) |
| Path uses already-proved output families | **Pass** — lines 124-128 name genealogy, AOI, and "logic / premise-scrutiny style follow-up where real runtime evidence exists" |
| Corridor is consistent with current code reality in renderers-ui and the-critic | **Pass** — the two documented forwarding asymmetries match direct code inspection exactly |

---

## 7. Verdict

### **Approve with corrections**

The memo is directionally correct, strategically honest, and appropriately calibrated. The corridor framing is real, the evidence base is grounded, and the deferrals are sensible.

Three concrete corrections are recommended:

### Correction 1: Differentiate the two forwarding asymmetries in the corridor description

**Current text (Corridor Step 2):**
> either the completed SubRenderers adoption proves current forwarding is good enough for a first Close Read build, or one bounded forwarding-normalization slice lands next

**Recommended replacement:**

> The forwarding-normalization decision has two distinct sub-questions with different fix shapes:
>
> 1. AccordionRenderer forwards capture runtime but omits `_captureSourceType` and `_captureEntityId` — this is a **field-defaulting** question where capture buttons still appear but metadata provenance is less precise
> 2. CardRenderer does not forward any capture runtime into nested subsection sub-renderers at all — this is a **functional-availability** question where capture buttons are absent on nested subsection content
>
> The decision may produce different verdicts for each: one might be acceptable as-is for lean Close Read V1 while the other might require a bounded patch.

**Why:** The current text reads as if the forwarding gap is one uniform question. Code inspection shows it is two qualitatively different gaps. The scope memo for the decision (`MEMO_2026-04-04_phase_e_...decision_v1_scope.md`) already names both, but the recalibration memo should too so the corridor description is self-contained.

### Correction 2: Name affordance gating as a product-layer question the scope memo must address

**Current text (Corridor Step 3):**
> Then scope a lean Close Read V1 product memo. That memo should stay bounded to what the runtime evidence already supports: first-hop operations only, current real destinations only...

**Recommended addition after the existing bullet list:**

> The lean Close Read V1 scope memo will also need to resolve one product-layer question that is below the renderer-substrate line but above the scope-memo bar:
>
> - how does Close Read V1 gate capture eligibility per view? The package utility (`captureBase.ts`) does not implement `_firstHopAffordance` gating. The Critic-local helper does. Close Read V1 will need its own affordance-gating policy — either consuming analyzer-emitted `first_hop_affordance` directly or implementing a host-local equivalent.
>
> This is not a renderer-substrate blocker and does not require a pre-scoping substrate slice. But it is a known product-design question the scope memo should address explicitly.

**Why:** Without this note, the corridor suggests the scope memo only needs to assemble proved substrate into a product shape. In practice, the scope memo will also need to decide how affordance gating works for the new app, because the package utility alone does not gatekeep capture eligibility. Naming this now prevents a surprise gap when the scope memo is written.

### Correction 3: Minor — strengthen the deferred list with one more item

**Current deferred list (lines 113-117):**
> It should explicitly defer: destination-internal lifecycle unification, Book Modeler integration, workflow-neutral destination taxonomy, full multi-user / multi-project architecture, generic downstream operation law

**Recommended addition:**

> - generic renderer-package capture law (the package utility stays raw; host-local gating and provenance policy remain host-owned for V1)

**Why:** The memo already implies this, but making it explicit prevents future sessions from assuming that lean Close Read V1 needs the package utility to absorb affordance gating, workflow keys, or typed selection law. The current raw utility is the right ceiling for V1; naming that keeps expectations calibrated.

---

## Summary

The recalibration memo is honest, strategically sound, and grounded in real code evidence. The corridor from current Phase E state to a lean Close Read V1 is materially short. The three corrections above are implementation-relevant clarifications, not directional objections.

The memo passes the critical tests:
- It does not outrun the proved substrate
- It does not overclaim forwarding is solved
- It does not pretend full productization is next
- It correctly separates renderer-substrate gates from product-design questions
- Its evidence base (the operations matrix, the SubRenderers completion, the package utility code) is real and verified against the codebase
