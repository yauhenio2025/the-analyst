# Report: Close Read V1 Scope Critique

Date: 2026-04-04
Reviewer: Claude Opus 4.6 (1M context)
Review Type: Full scope critique with code-backed verification
Scope Memo Under Review:
- `communications/MEMO_2026-04-04_close_read_v1_scope.md`

---

## Context Check

Every required memo and code file was read in full before this review:

| Document | Status |
|---|---|
| `MEMO_2026-04-04_close_read_v1_scope.md` | Read in full |
| `MEMO_2026-04-04_phase_e_renderers_ui_release_artifact_refresh_and_critic_host_verification_v1_completion.md` | Read in full |
| `MEMO_2026-04-04_close_read_roadmap_recalibration.md` | Read in full |
| `MEMO_2026-04-01_close_read_direction_change_and_implications.md` | Read in full |
| `MEMO_2026-04-01_close_read_operations_and_routing_inventory.md` | Read in full |
| `MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md` | Read in full |
| `APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md` | Read in full |
| `MEMO_2026-03-30_distilled_strategic_roadmap.md` | Read in full |
| `MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md` | Read in full |
| `MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md` | Read in full |
| `MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` | Read strategic sections |
| `src/views/definitions/genealogy_target_profile.json` | Read in full — accordion, 3 `nested_sections` |
| `src/views/definitions/genealogy_per_work_scan.json` | Read in full — card, 4 `nested_sections` subsections |
| `src/views/definitions/genealogy_portrait.json` | Read in full — prose renderer, `planner_eligible: true` |
| `src/views/definitions/genealogy_idea_evolution.json` | Read in full — tab renderer, `planner_eligible: true` |
| `/home/evgeny/projects/the-critic/webapp/package.json` | Read — now points to `0.6.6` tarball |
| `InstalledPackageNestedCapture.test.tsx` | Read in full — 2 proofs, no package mocks |
| `CaptureActionBar.tsx` | Read first 150 lines — shows Arsenal + Research buttons without `allowed_destinations` gating |
| `CaptureContext.tsx` | Read lines 90-120 — `genealogy_job_id` derivation from `source_type === 'genealogy'` |
| `V2TabContent.tsx` | Read lines 560-610 — capture config threading including `_firstHopAffordance` |
| `currentRendererCapture.ts` | Read in full — requires `_firstHopAffordance.capturable === true` at line 45-46 |

---

## 1. Pressure-Testing The Memo's Assumptions

### Is genealogy really the strongest honest center of gravity for V1?

**Yes. This is correct and well-grounded.**

The four named genealogy surfaces span three different renderer types and four distinct analytical passes:

| View | Renderer | Workflow Phase | Current Capture Proof |
|---|---|---|---|
| `genealogy_target_profile` | `accordion` (nested_sections) | Phase 1 chain | Real installed-package proof (0.6.6) — source_type preservation verified |
| `genealogy_per_work_scan` | `card` (nested_sections) | Phase 2 chain | Real installed-package proof (0.6.6) — subsection capture availability verified |
| `genealogy_portrait` | `prose` | Phase 4 final synthesis | Current-renderer capture alignment already proved |
| `genealogy_idea_evolution` | `tab` | Phase 3 concept_synthesis | Current-renderer idea-card capture alignment already proved |

All four are `planner_eligible: true`. All four have `workflow_key: "intellectual_genealogy"`. All four target `the-critic` / `genealogy` page.

No other workflow family has this depth of contiguous proof across nested, prose, card, and tab surfaces. AOI has strong individual proofs (`aoi_by_sin_type`, `aoi_by_theme`) but they span only two renderer patterns, not four, and they sit on a different workflow family.

### Is a bounded Critic-hosted pilot the right default posture?

**Yes. The code evidence overwhelmingly supports this.**

Every relevant runtime seam exists in Critic:
- `CaptureContext.tsx` — capture state management, `submitCapture()` to Arsenal/Research
- `CaptureActionBar.tsx` — visible action bar with Arsenal + Research buttons
- `ResearchFlagDialog.tsx` — research question formulation
- `V2TabContent.tsx` — capture config threading into renderers
- `currentRendererCapture.ts` — current-renderer capture runtime resolution
- The installed `@the-syllabus/analysis-renderers` `0.6.6` — package-native capture on nested surfaces

No alternative host has any of this infrastructure. Building a separate thin-host app would require rebuilding all of these seams from scratch. The scope memo's "default calibration: bias toward a bounded Critic-hosted pilot unless code evidence shows that is dishonest" is the right call.

### Is the memo honest about what current runtime evidence supports for first-hop operations and destinations?

**Yes.** The operations/routing inventory matrix confirms exactly two runtime-real first-hop destination families:

1. **Arsenal** — `CaptureActionBar.handleArsenalClick` → `CaptureContext.submitCapture('arsenal')` → `POST /api/captures` + `POST /api/captures/{id}/to-arsenal`
2. **Research todo** — `CaptureActionBar.handleResearchClick` → `ResearchFlagDialog.handleSave` → `POST /api/captures` + `POST /api/research-todos` + `POST /api/captures/{id}/to-research-todo`

Book Modeler is aspirational only (no runtime seam). The scope memo correctly keeps V1 below it.

### Does the memo resolve app-layer eligibility at the right layer?

**Yes, and this is the memo's strongest contribution.** The scope memo correctly identifies that there are currently TWO capture systems with different eligibility thresholds:

1. **Package-native** (`resolvePackageCaptureBaseRuntime` in `captureBase.ts`) — gates only on `_captureMode === true` and `typeof _onCapture === 'function'`. No `_firstHopAffordance` check. This is what nested accordion/card sub-renderers use after the 0.6.6 refresh.

2. **Current-renderer (Critic-local)** (`resolveCurrentRendererCaptureRuntime` in `currentRendererCapture.ts`) — additionally requires `_firstHopAffordance.capturable === true` (line 45-46), plus `_captureViewName`, plus `_captureSourceType`. This is what the four custom Critic renderers use (`SynthesisRenderer`, `AoiSinFindingsRenderer`, `AoiThemeFindingsMiniCardList`, `IdeaEvolutionRenderer`).

The scope memo's Assumptions section already names this split: "current host capture law is still split across raw package capture, `currentRendererCapture`, and `CaptureActionBar`." The V1 product memo must decide whether:

- Package-native capture availability alone constitutes V1 eligibility (widest — any nested surface with `_captureMode` shows capture buttons)
- Or V1 should require `_firstHopAffordance.capturable === true` even on package-native nested surfaces (narrower — only analyzer-approved surfaces get capture)

This is the right question to force. The scope memo correctly frames it as a product decision that the substrate does not settle.

---

## 2. Bigger Picture And Analyzer-V2-As-Brain Alignment

The close-read roadmap recalibration explicitly sequenced:

1. SubRenderers adoption — done
2. Forwarding decision gate — done
3. Forwarding-normalization implementation — done
4. Release-artifact refresh + Critic host verification — done
5. **Lean `Close Read V1` scope memo — this is that step**

The scope memo is corridor step 5. It is correctly positioned.

Against the anti-drift rules:

- **Rule 1 (prefer upstream intelligence over downstream convenience)**: This is a docs-first scope memo, not a host-convenience patch. It asks the right upstream questions (what should analyzer-v2 own via affordance, what should the host own via eligibility policy).
- **Rule 2 (do not confuse bounded proof with generalized architecture)**: The memo explicitly says V1 is bounded and names extensive deferrals.
- **Rule 4 (prefer representative matrices over exhaustive theater)**: Genealogy as V1 center of gravity is the right representative choice — it covers accordion, card, prose, and tab renderers across four analysis passes.

Against the direction-change memo: the dictation added "operation families over analytical outputs" as a missing layer. The scope memo addresses this through its first-hop operation section (Section 3) and its eligibility policy section (Section 4). It does not try to build the full operation-family taxonomy, which is correct for V1.

---

## 3. Explicit Point-By-Point Checks

| Check | Result | Evidence |
|---|---|---|
| Memo does not treat renderer-substrate work as still blocking product scoping | **Pass** | Opening "Why This Is Now The Next Honest Step" section explicitly states the corridor is clear |
| Memo does not overclaim full product readiness | **Pass** | "This slice should produce one bounded product memo" and extensive deferral list |
| Memo keeps V1 below Book Modeler | **Pass** | Explicitly deferred in Section 5 |
| Memo keeps V1 below destination-internal lifecycle unification | **Pass** | Explicitly deferred in Section 5 |
| Memo keeps V1 below workflow-neutral destination taxonomy | **Pass** | Explicitly deferred in Section 5 |
| Memo keeps V1 below generic renderer-package capture law | **Pass** | Explicitly deferred in Section 5 |
| Memo keeps V1 below multi-user / multi-project architecture | **Pass** | Explicitly deferred in Section 5 |
| Memo grounds V1 in current real destinations only (Arsenal, Research todo) | **Pass** | Section 3 explicitly names only these two |
| Memo names host-delivery posture as explicit product question | **Pass** | Section 1 requires concrete choice |
| Memo names app-layer first-hop eligibility as explicit product question | **Pass** | Section 4 requires concrete policy |

---

## 4. One Observation On The V1 Product Memo's Expected Work

The scope memo asks the implementor to produce a docs-first product memo. The implementor will need to make one materially non-obvious decision in Section 4 (eligibility policy):

**The two-system capture split creates a real product-layer seam.** Currently:

- `genealogy_target_profile` and `genealogy_per_work_scan` — use package-native capture via `resolvePackageCaptureBaseRuntime`. Capture buttons appear whenever `_captureMode` is true. No `_firstHopAffordance` gate.
- `genealogy_portrait` and `genealogy_idea_evolution` — use current-renderer capture via `resolveCurrentRendererCaptureRuntime`. Capture buttons appear only when `_firstHopAffordance.capturable === true`.

So on a single genealogy page, two surfaces might show capture buttons (because the analyzer approves them via `first_hop_affordance`) while two other surfaces might also show capture buttons (because the package always shows them when capture mode is on) — even if the analyzer didn't explicitly approve those surfaces.

The V1 product memo should either:

1. Accept this inconsistency for V1 (pragmatic — nested package capture is already proven and useful)
2. Or propose a lightweight app-layer gate that also checks `_firstHopAffordance` before enabling package-native capture in V2TabContent (more principled — all surfaces respect the same eligibility)

Both are defensible. The scope memo correctly asks for this decision without prescribing the answer.

---

## 5. One Minor Gap

The scope memo's Section 2 says "AOI findings surfaces may be mentioned only if they materially strengthen the first V1." This is fine as guidance. But the V1 product memo should also briefly explain *why* AOI is deferred even though it has real capture proofs (`aoi_by_sin_type`, `aoi_by_theme`), rather than simply not mentioning it. Otherwise a future reader might assume AOI was accidentally omitted. A one-sentence deferral note in the product memo would be sufficient.

This is not a scope memo defect — it's implementation guidance for the product memo author.

---

## Verdict

### **Approve**

The scope memo is:

1. **Correctly positioned** — corridor step 5 after all renderer-substrate prerequisites are cleared
2. **Properly docs-first** — no implementation changes required
3. **Honest about the two open product questions** — host-delivery posture and app-layer eligibility are correctly named as decisions the substrate does not settle
4. **Well-grounded in code reality** — genealogy as center of gravity is backed by four contiguous proved surfaces, Arsenal/Research as destinations are backed by the operations inventory, and the Critic-hosted pilot default is backed by runtime infrastructure evidence
5. **Complete in its deferrals** — Book Modeler, destination lifecycle, taxonomy, generic capture law, multi-user architecture all explicitly excluded
6. **Strategically aligned** — passes all anti-drift rules, correctly scopes V1 as bounded rather than platform-complete

No corrections required.
