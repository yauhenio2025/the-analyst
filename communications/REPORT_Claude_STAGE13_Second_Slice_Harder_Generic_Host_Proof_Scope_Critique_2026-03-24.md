# Critique: Stage 13 Second-Slice Harder Generic Host Proof Scope

Date: 2026-03-24
Reviewer: Claude Opus 4.6
Scope Memo Under Review: `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_scope.md`
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

---

## Verdict: Approve After Revision

The memo's diagnosis is honest and the codebase evidence supports the stated gaps. The sequencing decision — Stage 13 second slice before Stage 14 lifecycle — is correct. But three aspects need tightening before this memo can function as an executable scope document.

---

## 1. Is This Still Stage 13 Second Slice Rather Than Stage 14?

**Yes. The memo is correct here.**

The roadmap's Stage 13 exit evidence is explicit:

> second consumer or generic host proof without rebuilding intelligence locally

The first slice delivered typed Host Contract v1, a generated JSON artifact, cross-workflow readiness adoption, and broader shared-adapter coverage. That is real formalization work — but it does not satisfy either arm of the exit evidence. No second consumer exists. The "generic host proof" arm is still bounded to "verified current consumer pages on existing shared client helpers."

Stage 14 lifecycle (launch/revisit/save/share/compare) is a fundamentally different architectural concern. Attempting it before the host contract runtime is operational would blur two different questions:

1. "Can the host contract drive operational behavior?"
2. "What is a dynamic surface as a persistent runtime object?"

The memo is right that those should remain sequential, not collapsed.

---

## 2. Is The Harder Proof Target Specific Enough?

**Partially. The proof bar is well-formulated but the deliverable shape is vague.**

The memo correctly identifies four structural gaps visible in the codebase:

### Gap 1: Transient families outside the shared adapter layer — CONFIRMED

`composeFromIntentClient.ts` (lines 121-178) constructs URLs directly to `ANALYZER_V2_URL` and `API_BASE` without going through `boundedV2Client.ts`. The `composeFromIntent()` function builds a direct `fetch()` call to the analyzer compose route, while `composeFromSource()` builds a direct `fetch()` call to the host proxy route. Neither uses the `buildAnalyzerUrl()` helper or the `CONSUMER_KEY` constant from `boundedV2Client.ts`.

This is a real structural split, not a paperwork gap. The two client modules do not share URL construction, error normalization, or consumer-key threading.

### Gap 2: Page-local surface selection — CONFIRMED

`AoiComposeFromIntentPage.tsx` (line 23) hardcodes `AOI_CONSUMER_KEY = 'the-critic'` locally. `AoiV2ThematicPanel.tsx` chooses between result-backed workspace interaction and source-backed transient launch through page-local branching rather than through any contract-driven surface resolver. `AnalysisWorkspacePage.tsx` makes composition-mode choices locally (lines 73-101 with `getCompositionProofLabel()`).

Surface selection exists as scattered page-local constants and branching, not as a contract-driven resolver.

### Gap 3: AOI proxy seam partly outside shared client — CONFIRMED

`the-critic/api/server.py` (line 20311) hosts a dedicated `compose-from-source` proxy route. The client calls this through `composeFromIntentClient.ts:composeFromSource()` (line 155), which builds the URL to `API_BASE` directly. This proxy performs real host-owned work:

- `_resolve_source_backed_compose_identity()` does project/thinker-scoped identity resolution
- Cross-reference validation against saved results
- Thinker context matching
- Error mapping for 404/409 cases

This is not a thin pass-through. The proxy genuinely owns host-side preparation logic. The memo is correct that this should not be erased — but it should be tracked under the shared adapter framework.

### Gap 4: No materially harder generic-host proof — CONFIRMED

The Stage 13 first slice essentially said: "we wrote down the contract, improved readiness adoption, and moved some page fetches onto the shared client." The proof is still "the-critic consuming bounded AOI + genealogy seams through existing shared helpers." That is necessary but not sufficient for the roadmap's exit bar.

**However, the memo is vague about what "materially harder" means in concrete terms.** The recommendations (Decisions 1-7) describe principles rather than specific deliverables. For an executable scope document, the memo should specify:

- What the unified adapter layer's public API surface looks like (e.g., a typed function that accepts a family key and dispatches to the correct backend)
- What the host-surface resolver's inputs and outputs are (e.g., `(workflowKey, surfaceContext) => ContractFamilySet`)
- How "no analytical truth re-derived in page code" will be verified concretely (e.g., a grep-based check, a test assertion, or a code-review checklist)

---

## 3. Are The Claimed Gaps Real In Code?

**Yes, all four are real and the memo does not overstate them.**

I verified each claim against the live codebase:

| Claim | Evidence | Verdict |
|---|---|---|
| `composeFromIntentClient.ts` is structurally separate from `boundedV2Client.ts` | Different URL construction, different error handling, no shared constants | Real gap |
| Host-surface selection is page-local | `AoiV2ThematicPanel.tsx` and `AoiComposeFromIntentPage.tsx` make their own surface decisions | Real gap |
| AOI proxy route is only partly reflected in shared client | `composeFromSource()` calls `API_BASE` directly; `boundedV2Client.ts` has no compose family | Real gap |
| Host Contract v1 is typed but not runtime-authoritative | `hostContractV1.ts` exports static data and lookup functions but nothing dispatches through it at runtime | Real gap |

The memo also does **not** overstate. It carefully acknowledges what is already real:

- `hostContractV1.ts` exists with 11 typed families, readiness capabilities, and surface selection rules
- `boundedV2Client.ts` covers the result-backed families comprehensively (run discovery, results, manifest, presentation, refresh, single-view, readiness)
- `useBoundedV2Workspace.ts` is a substantial shared workspace hook already used by `AnalysisWorkspacePage`
- Cross-workflow readiness adoption landed in the first slice

So the memo's positioning — "stronger than it was, but not yet operational enough" — is honest.

---

## 4. Does The Memo Understate Or Overstate Generic-Host Capability?

**The memo is slightly conservative — which is the right error direction.**

What the memo could have noted more explicitly:

1. **`boundedV2Client.ts` already covers 8 of the 11 Host Contract v1 families.** Only `transient_compose_from_intent`, `source_backed_transient_launch`, and `cache_snapshot_warmup` are outside it. The first two are in `composeFromIntentClient.ts`; the third is in `boundedV2Client.ts` already (`cacheBoundedV2Presentation()`). So the structural split is narrower than "transient families are outside the shared layer" might imply — it is specifically `composeFromIntent` and `composeFromSource`.

2. **`useBoundedV2Workspace` already imports from `hostContractV1.ts`.** Line 23 of `useBoundedV2Workspace.ts` imports `isHostReadinessCapabilitySupported`. So the contract is not purely documentary — one consumer of the workspace hook already consults it at runtime. The gap is that this pattern does not extend to family selection or transient launch dispatch.

3. **`AoiV2ThematicPanel.tsx` already imports from both `boundedV2Client.ts` and `hostContractV1.ts`.** Lines 8-12 show it using `discoverBoundedV2Results`, `getBoundedV2SingleView`, `getBoundedV2SourceBackedReadiness` from the bounded client, and `isHostReadinessCapabilitySupported` from the host contract. So the AOI result-backed panel is already substantially on the shared path.

These facts do not invalidate the scope memo. They mean the delta is smaller and more focused than the memo's framing might suggest. The real remaining work is:

- Unify `composeFromIntentClient.ts` functions into (or alongside) the shared adapter layer
- Make family/surface selection contract-driven rather than page-local
- Make `hostContractV1.ts` dispatch-authoritative, not just lookup-authoritative

---

## 5. Alignment With The Larger Analyzer-As-Brain / Thin-Host Objective

**Strong alignment.**

The roadmap's Layer F (Thin host consumption) says the consumer app should need only:

> route + auth + project context + generic rendering host + a small number of stable launch and persistence hooks

The scope memo's target — one executable contract-driven host adapter covering all must-have v1 families — is directly on that vector. Making the host contract operational rather than merely descriptive is the natural next step after formalization.

The memo also correctly stays within the narrower UI-composition framing from `DYNAMIC_BESPOKE_APPS_VISION.md` rather than attempting the broader task-planning vision. That is appropriate for a host-contract tranche.

---

## 6. Missing Proof Requirements, Hidden Coupling, Or Sequencing Mistakes

### 6.1 Missing: The cache_snapshot_warmup family is already in `boundedV2Client.ts`

The memo lists `transient_compose_from_intent` and `source_backed_transient_launch` as the families outside the shared adapter (Decision 3). But `cache_snapshot_warmup` is listed in the contract as `host_proxy` owner, and it is already in `boundedV2Client.ts` (line 187, `cacheBoundedV2Presentation()`). The memo should acknowledge that `cache_snapshot_warmup` is already on the shared path — the gap is specifically the two compose families.

### 6.2 Missing: Consumer-key threading asymmetry

The host contract has two consumer-key patterns: `request_parameter` (most families) and `structural_constant` (transient compose and source-backed launch, hardcoded to `the-critic` inside analyzer-v2). The scope memo should explicitly state whether the unified adapter layer needs to handle this asymmetry or whether it remains transparent at the host level. Currently `boundedV2Client.ts` uses `CONSUMER_KEY = 'the-critic'` as a module constant (line 15), while `composeFromIntentClient.ts` does not set a consumer key at all (the page passes it in the request body). A unified adapter needs a clear rule for this.

### 6.3 Hidden coupling: AoiComposeFromIntentPage.tsx hardcodes more than surface selection

`AoiComposeFromIntentPage.tsx` (lines 22-24) hardcodes:

```typescript
const AOI_WORKFLOW_KEY = 'anxiety_of_influence_thematic_single_thinker';
const AOI_CONSUMER_KEY = 'the-critic';
```

And the page builds compose requests, manages draft state, handles examples, and constructs source-backed requests inline. The surface-selection problem is only part of the coupling. Even after a surface resolver exists, this page will still own substantial compose-specific UX state management. The scope memo should be explicit about what moves into the shared adapter (dispatch, URL construction, error normalization, consumer-key threading) versus what remains page-owned (draft state, UX interactions, example loading).

### 6.4 Sequencing risk: Host-surface resolver may be premature for two proof seams

The memo asks for "one executable host-surface selection runtime" (Decision 4). But the current proof matrix has only three surfaces (AOI result thematic, AOI source-backed transient launch, genealogy result-backed workspace). A resolver over three statically known surfaces risks being over-engineered for this slice. The honest minimum might be:

- A typed lookup function that returns the correct family set given a surface key
- Not a general-purpose runtime resolver with dynamic registration

The memo should clarify whether this is a lookup or a resolver. The distinction matters for implementation scope.

### 6.5 No regression risk assessment

The scope memo does not mention which existing test suites need to pass after the second slice. Given that Stage 13 first slice included verification across 131 tests in the-critic, the second slice should specify which test packs constitute the regression boundary.

---

## 7. Should Stage 14 Lifecycle Be The Next Move Instead?

**No. The memo is correct to defer it.**

Stage 14 asks "what is a dynamically composed app as a runtime object?" That question presupposes that the host contract can drive operational behavior. If the contract is still partly descriptive and transient families still sit outside the shared adapter, then lifecycle decisions would be made on top of an incomplete substrate.

The specific risk of jumping to Stage 14 now:

1. Lifecycle decisions would need to be made separately for result-backed families (which use the shared adapter) and transient compose families (which do not) — that would cement the structural split rather than closing it.
2. Session/draft semantics for transient compose would depend on a proxy route that is not yet tracked under the shared contract runtime — that would create a hidden coupling that future lifecycle changes would have to work around.

So Stage 13 second slice should come first.

---

## 8. Is The Vision Already Sufficiently Achieved?

**No.**

The vision's Layer F requires that "consumer apps are thin host shells." The current state is:

- 8 of 11 contract families are on the shared adapter path
- 2 compose families use a separate client module with separate URL/error handling
- Surface selection is page-local
- The host contract is typed and lookup-queryable but not dispatch-authoritative

That is materially better than 72 hours ago, but it does not satisfy "thin host shell" because the compose families — which are the distinctive capability that makes this a dynamic-composition platform rather than just a result-viewing platform — still live outside the shared contract runtime.

---

## 9. Recommended Revisions Before Approval

1. **Sharpen Decision 3**: State explicitly that only `composeFromIntent` and `composeFromSource` functions need to move into/alongside the shared adapter layer, since `cache_snapshot_warmup` is already there. Acknowledge the consumer-key asymmetry (`request_parameter` vs `structural_constant`) and specify how the unified adapter handles it.

2. **Sharpen Decision 4**: Clarify whether the host-surface selection runtime is a typed lookup function (static mapping from surface key to family set) or a general-purpose resolver. For three proof surfaces, a lookup is the honest minimum.

3. **Add a concrete deliverable list**: The seven decisions are good principles but do not tell a future implementor exactly what to build. Add a minimal deliverable table, e.g.:
   - One shared contract-aware adapter module covering compose families
   - One typed surface-selection lookup function
   - One integration point where the host contract drives dispatch rather than only being queryable
   - One regression-test pack for the proof boundary

4. **Add regression boundary**: Specify which the-critic test suites must pass after the second slice to maintain the Stage 13 first-slice guarantees (the 131-test pack from the first slice completion memo).

5. **Clarify the page-vs-adapter boundary for compose state**: `AoiComposeFromIntentPage.tsx` owns draft management, example loading, and UX state. The memo should be explicit that those remain page-owned while only dispatch/URL/error/consumer-key threading move into the shared adapter.

---

## 10. Summary

| Dimension | Assessment |
|---|---|
| Correct next phase (not Stage 14) | Yes |
| Distinct from first Stage 13 slice | Yes — first slice was formalization, this is operationalization |
| Gaps are real in code | All four confirmed |
| Understates capability | Slightly — should note that 8/11 families are already shared |
| Overstates capability | No |
| Aligned with vision | Strongly aligned |
| Proof bar adequate | Adequate but needs sharper deliverable criteria |
| Missing requirements | Consumer-key asymmetry handling, regression boundary, page-vs-adapter scope |
| Sequencing mistakes | None found |
| Hidden coupling | `AoiComposeFromIntentPage` UX state coupling noted but not blocking |

**Verdict: Approve after the five revisions above are addressed.**

The memo's strategic diagnosis is honest, the codebase evidence is confirmed, and the sequencing is correct. The revisions needed are about sharpening the deliverable scope, not about changing the direction.
