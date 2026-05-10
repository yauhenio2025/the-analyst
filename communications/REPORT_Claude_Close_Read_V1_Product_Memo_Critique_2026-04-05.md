# Report: Close Read V1 Product Memo Critique

Date: 2026-04-05
Reviewer: Claude Opus 4.6 (1M context)
Review Type: Full product-memo critique with code-backed verification
Product Memo Under Review:
- `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`

---

## Context Check

Every required memo and code file was read before this review:

| Document | Status |
|---|---|
| `MEMO_2026-04-05_close_read_v1_product_memo.md` | Read in full |
| `MEMO_2026-04-04_close_read_v1_scope.md` | Read in full (corrected version) |
| `MEMO_2026-04-04_close_read_roadmap_recalibration.md` | Read in full |
| `MEMO_2026-04-04_phase_e_renderers_ui_release_artifact_refresh_and_critic_host_verification_v1_completion.md` | Read in full |
| `MEMO_2026-04-01_close_read_direction_change_and_implications.md` | Read in full |
| `MEMO_2026-04-01_close_read_operations_and_routing_inventory.md` | Read in full |
| `MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md` | Read in full |
| `APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md` | Read in full |
| `REPORT_Claude_Close_Read_V1_Scope_Critique_2026-04-04.md` | Read in full |
| `REPORT_Codex_Close_Read_V1_Scope_Audit_2026-04-04.md` | Read in full |
| `MEMO_2026-03-30_distilled_strategic_roadmap.md` | Read in full |
| `MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md` | Read in full |
| `MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md` | Read in full |
| `MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` | Read strategic sections |
| `src/views/definitions/genealogy_target_profile.json` | Read in full |
| `src/views/definitions/genealogy_per_work_scan.json` | Read in full |
| `src/views/definitions/genealogy_portrait.json` | Read in full |
| `src/views/definitions/genealogy_idea_evolution.json` | Read in full |
| `/home/evgeny/projects/the-critic/webapp/package.json` | Read — points to `0.6.6` tarball |
| `InstalledPackageNestedCapture.test.tsx` | Read in full |
| `CaptureActionBar.tsx` | Read first 150 lines |
| `CaptureContext.tsx` | Read lines 90-120 |
| `V2TabContent.tsx` | Read lines 560-610 |
| `currentRendererCapture.ts` | Read in full |
| `src/presenter/first_hop_affordance.py` | Grep-verified — `FIRST_HOP_ALLOWED_DESTINATIONS = ("arsenal", "research_todo")` |
| `src/presenter/schemas.py` | Grep-verified — `FirstHopDestination = Literal["arsenal", "research_todo"]` |

---

## 1. Pressure-Testing The Five Frozen Product Decisions

### Decision 1: Bounded Critic-hosted pilot posture

**Correct and code-grounded.**

The memo names four concrete runtime seams that make Critic the only honest V1 host:
- `CaptureContext` — capture state and routing
- `CaptureActionBar` — visible Arsenal/Research action shell
- `V2TabContent` — capture config threading into renderers
- Installed `0.6.6` package — nested genealogy proof

No alternative host has any of this infrastructure. The memo correctly says this "does not mean Critic is the long-term permanent Close Read host" (line 70).

### Decision 2: Exact genealogy-first V1 surface set

**Correct. The primary/supporting distinction is well-calibrated.**

The memo distinguishes:
- Primary: `genealogy_portrait` (Phase 4 final synthesis, prose renderer) and `genealogy_idea_evolution` (Phase 3 concept synthesis, tab renderer)
- Supporting: `genealogy_target_profile` (Phase 1 profiling, accordion/nested_sections) and `genealogy_per_work_scan` (Phase 2 scanning, card/nested_sections)

This distinction matches the view definitions themselves:
- `genealogy_portrait.json` planner_hint says "Essential. Always include as primary view"
- `genealogy_idea_evolution.json` planner_hint says "Essential. Always include as primary view"
- `genealogy_target_profile.json` description says "Currently invisible intermediate product"
- `genealogy_per_work_scan.json` description says "currently only partially surfaced"

The Codex audit recommended exactly this primary/supporting split. The product memo implemented it.

AOI exclusion is handled honestly: "This does not deny that some non-V1 surfaces are already runtime-real or already useful. It only freezes the first product cut around one coherent genealogy cluster" (lines 113-114).

### Decision 3: Exact capture-and-route-only first-hop family

**Correct and honestly bounded.**

The memo limits V1 to one operation family and explicitly lists what is out:
- Outline talking-point routing — out
- Annotations/comments — out
- Findings-specific Arsenal promotion — out
- Research-answer-specific flows — out

Crucially, line 128 says "even where some runtime-real seams already exist elsewhere in Critic." This is the non-erasure clause the review prompt asked for. It acknowledges those seams are real without adopting them into V1.

### Decision 4: Exact app-layer eligibility policy

**This is the memo's strongest and most non-obvious decision. It is correct.**

The four-point policy at lines 145-156 is:

1. First-hop capture is product-approved only on the four named V1 surfaces
2. `genealogy_portrait` and `genealogy_idea_evolution` — gated by analyzer `first_hop_affordance.capturable === true` through `currentRendererCapture`
3. `genealogy_target_profile` and `genealogy_per_work_scan` — accepted via product-memo authority because they are explicitly in V1 and already proven on the installed path
4. No broader inference — package availability elsewhere does not imply V1 eligibility

This is the right design for three reasons:

**First**, it correctly separates substrate capability from product policy. The substrate says "can capture happen?" (yes, the package and host code support it). The product memo says "should capture happen here?" (yes, on these four surfaces only).

**Second**, it honestly handles the two-system split without pretending convergence. Points 2 and 3 acknowledge that the two primary surfaces use `currentRendererCapture` (which gates on `_firstHopAffordance`) while the two supporting surfaces use package-native capture (which does not). Point 4 prevents that package-native availability from being read as blanket eligibility.

**Third**, it matches the code reality I verified:
- `currentRendererCapture.ts` line 45: `if (firstHopAffordance?.capturable !== true) return null;`
- `captureBase.ts` lines 25-26: gates only on `_captureMode !== true` and `!onCapture`
- `first_hop_affordance.py` line 72: defaults `allowed_destinations=list(FIRST_HOP_ALLOWED_DESTINATIONS)` which is `["arsenal", "research_todo"]`

So the analyzer already emits the right affordance for genealogy leaves, and `currentRendererCapture` already consumes it on the two primary surfaces. The product memo is honest that the two supporting surfaces bypass that gate through package-native capture, and accepts this explicitly rather than hiding it.

### Decision 5: Exact Arsenal / Research todo routed destination set

**Correct.**

The memo says "These are the only routed destinations included in Close Read V1" and "This is an intentional product boundary choice, not a claim that other runtime-real artifact seams do not exist" (lines 179-182).

This matches the analyzer's own default: `FIRST_HOP_ALLOWED_DESTINATIONS = ("arsenal", "research_todo")` in `first_hop_affordance.py:11`. And it matches `CaptureActionBar.tsx` which exposes exactly these two actions (Send to Arsenal, Research Question).

The memo also notes why `CaptureActionBar` is acceptable for V1: "it already exposes the two chosen V1 routes" (line 192). This is correct — no new UI work is needed for the destination set.

---

## 2. Explicit Point-By-Point Checks

| Check | Result | Evidence |
|---|---|---|
| Memo does not reopen renderer/package substrate questions | **Pass** | No mention of captureBase.ts changes, forwarding work, or package-source patches. Treats substrate as settled. |
| Memo does not erase other runtime-real first-hop seams | **Pass** | Lines 128, 137, 182 all explicitly acknowledge other seams exist while excluding them |
| Memo distinguishes core V1 entry surfaces from broader proof set | **Pass** | Primary (portrait, idea_evolution) vs supporting/detail (target_profile, per_work_scan) |
| Memo states split eligibility law honestly | **Pass** | Lines 160-168 name all three layers with their actual gating behavior |
| Memo's destination boundary is consistent with host behavior | **Pass** | CaptureActionBar already exposes exactly Arsenal + Research; analyzer defaults match |
| Memo's deferrals prevent accidental overreach | **Pass** | 11 explicit deferrals at lines 199-210, including Book Modeler, lifecycle unification, taxonomy, generic capture law, multi-user architecture |

---

## 3. Bigger Picture Alignment

Against the distilled strategic roadmap's anti-drift rules:

- **Rule 1 (upstream intelligence over downstream convenience)**: The product memo does not add new downstream intelligence. It freezes a product boundary around already-proved upstream capability.
- **Rule 2 (bounded proof vs generalized architecture)**: The memo explicitly says this is "a bounded pilot product, not a converged generic capture law" (line 156).
- **Rule 3 (governance vs architecture)**: Not applicable — this is product scoping, not governance.
- **Rule 4 (representative matrices over exhaustive theater)**: Genealogy-first is a representative choice covering four renderer types (prose, tab, accordion, card) across four workflow phases.

Against the corridor recalibration: this memo is exactly corridor step 5 — "scope one lean Close Read V1 product memo bounded to runtime-real first-hop operations and current real destinations, while explicitly resolving host-delivery posture and app-layer first-hop eligibility policy."

Against the direction-change memo: the dictation added "operation families over analytical outputs" as a missing layer. The product memo addresses this through Decision 3 (capture-and-route as the V1 operation family) and Decision 4 (eligibility policy). It does not try to build the full operation-family taxonomy, which is correct for V1.

---

## 4. One Observation For The Implementation Scope

The product memo's "Immediate Consequence" section says the next move should be "one bounded implementation scope for the Critic-hosted Close Read V1 pilot" that implements this frozen boundary.

That implementation scope will need to decide one practical question the product memo intentionally leaves open: **what, if anything, changes in the current Critic code?** The product memo freezes decisions but does not describe implementation. Three possibilities:

1. **Nothing changes** — the current Critic already serves the four genealogy surfaces with capture on the existing genealogy page. V1 is just a product label on what already works.
2. **A dedicated Close Read entry point** — a new page/route in Critic that surfaces the four V1 views with the frozen eligibility policy.
3. **Lightweight gating** — the existing genealogy page gains a small product-boundary gate that enforces the V1 whitelist.

The product memo correctly defers this to the implementation scope. This is not a gap — it is an intentional separation of product boundary (this memo) from implementation approach (the next memo).

---

## Verdict

### **Approve**

The product memo is:

1. **Precise** — five concrete frozen decisions, not vague aspirations
2. **Code-grounded** — every decision traces to verified runtime behavior in Critic, analyzer-v2, or the installed package
3. **Honest about the substrate split** — does not pretend capture convergence exists; explicitly names the three-layer split and chooses product policy above it
4. **Non-erasive** — acknowledges runtime-real seams outside V1 while intentionally excluding them
5. **Correctly bounded** — 11 explicit deferrals prevent the memo from being read as platform law
6. **Strategically aligned** — corridor step 5, passes all anti-drift rules, correctly sequenced after renderer-substrate completion
7. **Consistent with both prior reviews** — incorporates all corrections from the Claude scope critique and the Codex scope audit

No corrections required.
