# Critique: Stage 13 / Minimal Generic Host Contract Scope

Date: 2026-03-24
Reviewer: Claude Opus 4.6
Target: `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md`

## Verdict: Approve after revision

Stage 13 is the right next stage after Stage 12. The memo is honest, well-structured, and correctly identifies the host boundary as the next missing architectural seam. The seven decisions are mostly sound. But the memo understates several concrete coupling points that the current code reveals, and the proof bar is weaker than the roadmap's own exit evidence requires. The revisions are bounded, not architectural.

---

## Findings

### Finding 1: The roadmap's own exit evidence is stronger than the memo's proof bar

The canonical roadmap at Stage 13 says:

> Exit evidence: second consumer or generic host proof without rebuilding intelligence locally

The memo's proof bar says:

> one real generic-host proof inside the current consumer over more than one workflow family, without rebuilding analyzer intelligence locally

That is the weaker half of the roadmap's disjunction. The memo is honest about this ("no second consumer is required in this slice"), and a bounded-current-consumer proof is reasonable for a first Stage 13 slice. But the memo should say explicitly:

- this is the bounded first slice of Stage 13, not the full exit evidence
- the roadmap exit evidence remains open after this slice until either a second consumer adopts the contract or a materially harder generic-host demonstration exists
- the Stage 13 ledger should stay at "partial" after this slice, not "complete"

Without that framing, the memo risks claiming Stage 13 closure prematurely on one-consumer evidence alone.

### Finding 2: `TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"` is hardcoded deeper than the memo admits

The memo acknowledges that `consumer_key='the-critic'` remains real on current seams. But the coupling goes deeper than the memo says:

- `src/presenter/compose_from_intent.py:52` hardcodes `TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"` as a module-level constant, not a request parameter
- This means the entire transient compose pipeline (compose-from-intent and compose-from-source) is structurally bound to one consumer, not just defaulted
- `src/analysis_products/result_contract.py:33` also defaults `DEFAULT_CONSUMER_KEY = "the-critic"` across all result routes
- The result routes accept `consumer_key` as a query parameter (so they are generically callable), but the compose routes do not — the consumer is baked in

The memo should enumerate this asymmetry explicitly in the Host Contract v1 matrix:

- result/run/presentation routes: consumer_key is a request-level parameter (generically callable)
- compose-from-intent / compose-from-source: consumer_key is hardcoded to `the-critic` at the module level (not generically callable without code change)

That matters for the "two implementors would produce compatible code" criterion in Decision 2. If one implementor reads the compose route signatures, they would not know the consumer is structurally fixed.

### Finding 3: The memo overstates the fragmentation in the-critic's shared client usage

The memo says (section on Decision 4):

> The current duplication is visible in: [lists 6 files including 3 pages]

But the actual code shows a cleaner picture than the memo implies:

**Already fully through shared clients:**
- `GenealogyPage.tsx` — uses `boundedV2Client` exclusively, no direct ANALYZER_V2_URL fetches
- `AnalysisWorkspacePage.tsx` — uses `boundedV2Client` exclusively
- `AnxietyOfInfluencePages.tsx` — uses `boundedV2Client` exclusively

**Have remaining direct ANALYZER_V2_URL fetches:**
- `AoiV2ThematicPanel.tsx` — one direct single-view fetch (line 278)
- `V2TabContent.tsx` — three direct polish fetches (lines 320, 421, 446)
- `PipelineVisualization.tsx` — one direct plan-visualization fetch (line 116)
- `useProvenanceData.ts` — one direct chain-definition fetch (line 94)

The page-level consolidation is already done. The remaining direct fetches are component-level optimization shortcuts and non-presentation paths (polish, visualization, provenance). The memo should reflect this more accurately so Stage 13's consolidation scope is right-sized.

Specifically, the memo should classify which of these remaining direct fetches are:
- in-scope for Stage 13 consolidation (the single-view fetch in AoiV2ThematicPanel is the most obvious)
- documented out-of-scope (polish, visualization, and provenance fetches may not belong in the contract-covered adapter layer)

### Finding 4: The source-backed readiness proof should be explicitly cross-workflow, not just AOI

The memo proposes adopting `source-backed-readiness` in the AOI source-backed transient launch path. That is a good first target.

But the readiness contract itself is already cross-workflow (AOI profile readiness + genealogy composition_mode readiness). The proof bar should require demonstrating readiness consumption on both workflow families to match Stage 13's cross-workflow claim:

- AOI readiness check before source-backed launch (replaces local feasibility assumptions)
- genealogy readiness check before result-backed surface selection (replaces local presence-check assumptions)

If the proof only shows AOI readiness adoption, Stage 13 remains AOI-shaped in exactly the area where the memo claims to be cross-workflow.

### Finding 5: Host-side surface selection intelligence is a real ownership question the memo doesn't fully address

The memo's direct-vs-proxy-vs-local classification is mostly correct. But it doesn't address a real form of host-side analytical intelligence that currently exists:

- `GenealogyPage.tsx` knows to call result presentation with `composition_mode` and to navigate to specific tab surfaces
- `AoiV2ThematicPanel.tsx` knows to route through source-backed compose for AOI transient launch
- `AnxietyOfInfluencePages.tsx` knows which analyzer surfaces to combine for the AOI experience

That is a form of workflow-specific surface-selection intelligence that lives in the host. It's the host deciding "this workflow uses this set of analyzer surfaces in this navigation order."

The memo mentions "route-to-surface selection between result-backed, transient, and source-backed host experiences" in Decision 6, but it doesn't say who owns that selection law or whether it should eventually move upstream.

The Host Contract v1 should be explicit about this:

- is page-level surface selection (which analyzer surfaces to combine for a workflow experience) host-owned or eventually analyzer-owned?
- in v1, is it acceptable for each host page to hardcode its own surface selection, or should the contract enumerate the current surface families per workflow?

This is not a blocking issue for Stage 13, but the contract should document it rather than leaving it as implicit host coupling.

### Finding 6: The compose-from-source proxy is the most complex host preparation, and the memo undersells its specificity

The memo says compose-from-source is a "host proxy" that "resolves project-local source identity before launching analyzer compose." That is true but undersells the complexity.

`api/server.py:20311-20364` in the-critic shows the proxy doing:

1. Validates `selected_source_thinker_id` and `profile` (host-side input validation)
2. Calls `_resolve_source_backed_compose_identity()` which:
   - loads a saved `GenealogyAnalysisDB` record (host-local persistence)
   - validates project/thinker context match (host identity resolution)
   - extracts `_v2_job_id` from host-local `pass_results` (host-to-analyzer identity bridge)
   - validates `V2RunReferenceDB` (host/analyzer cross-reference)
3. Constructs the analyzer payload with hardcoded `consumer_key: "the-critic"` and `workflow_key: AOI_THEMATIC_WORKFLOW_KEY`
4. Proxies to analyzer-v2's `compose-from-source` route
5. Maps analyzer error codes to host-facing responses

That is substantial host-owned preparation logic, not a thin proxy. The Host Contract v1 should enumerate:

- identity resolution is host-owned (map from host-local saved-result identity to analyzer-v2 `source_v2_job_id`)
- the current proxy bridges host-local `GenealogyAnalysisDB.pass_results._v2_job_id` to analyzer-v2's durable result identity — that bridge is the-critic-specific
- the contract should say what a generic host would need to own to perform this preparation (its own saved-result-to-v2-job-id mapping) vs. what analyzer-v2 could eventually own

### Finding 7: `cacheBoundedV2Presentation` in boundedV2Client routes through the-critic API, correctly classified

`boundedV2Client.ts:168-179` shows the cache/snapshot warming call goes through `API_BASE` (the-critic API), not directly to analyzer-v2. The memo correctly classifies this as "host proxy." Verified.

### Finding 8: The direct-vs-proxy split for compose-from-intent vs compose-from-source is correct but asymmetric

The code confirms:

- `composeFromIntent()` calls `ANALYZER_V2_URL/v1/presenter/compose-from-intent` directly (analyzer direct)
- `composeFromSource()` calls `API_BASE/analysis/.../compose-from-source` through the-critic API (host proxy)

The memo correctly classifies these. But the asymmetry should be called out explicitly in the Host Contract v1 — compose-from-intent is a direct analyzer call (no host preparation needed), while compose-from-source requires host preparation (identity resolution). A future "compose-from-source-v2" that accepted analyzer-native `source_v2_job_id` directly would eliminate the proxy need for hosts that don't need project-local identity resolution.

### Finding 9: Stages 1-6 remain open but Stage 13 timing is still correct

The roadmap shows Stages 1-6 partially open or not started. The memo doesn't justify why Stage 13 takes precedence over, say, Stage 2 (complete AOI transient MVP) or Stage 3 (task-driven composition).

But the memo's implicit justification is sound: Stages 7-12 have been running out of order because the downstream platform seams needed to be built first. Stage 13 is the natural consolidation step after that sequence. Stages 1-6 are mostly AOI-specific product/evaluation work, while Stage 13 is architectural formalization. They can proceed in parallel.

The memo should make this explicit rather than leaving it to the reader.

### Finding 10: No additional relevant docs beyond what was listed

I did not find additional documents in `communications/` or `docs/` from the past 48 hours that materially bear on the host/consumer ownership question beyond what the prompt already listed.

---

## Explicit answers to the review questions

### Is Stage 13 now the right next stage after Stage 12?

**Yes.** Stage 12 landed the served-intent renderer-law generalization. The remaining Stage 12 work (broader genealogy promotion) is incremental widening, not a new architectural seam. The host boundary is the next missing seam, and Stage 13 correctly targets it. The memo's "Explicit Sequencing Note" is honest about Stage 12 remaining partial.

### Is the proposed Host Contract v1 concrete enough that two implementors would produce compatible code?

**Almost, but not yet.** The 10 contract families are well enumerated. The per-family metadata (owner, inputs, caching policy) is the right schema. But:

- The compose routes' hardcoded consumer_key is not documented (Finding 2)
- The host-side surface selection intelligence is not addressed (Finding 5)
- The compose-from-source proxy complexity is undersold (Finding 6)

With those additions, two implementors would produce compatible code. Without them, they would diverge on compose ownership and surface selection.

### Is the direct-analyzer vs host-proxy vs host-local split correct?

**Mostly correct.** The classification matches the code. The only material gap is that compose-from-intent is classified as "direct analyzer call" while being structurally bound to one consumer (Finding 2). A more honest classification would be "direct analyzer call with consumer_key structurally constrained." The compose-from-source proxy classification is correct but undersold in complexity (Finding 6).

### Is the memo right to keep route-task and plan-task out of required host-v1 adoption?

**Yes.** Those routes are advisory-only analyzer seams. The host does not currently consume them. Forcing host adoption before the contract itself is explicit would conflate two separate problems. The memo correctly classifies them as "optional advisory v1."

### Does the current code support a shared host adapter covering both AOI and genealogy?

**For result consumption, yes.** `boundedV2Client.ts` already covers both workflows for discovery, manifests, presentation, refresh, and single-view. The page-level client usage is already workflow-agnostic.

**For transient/compose launch, no.** The compose paths are AOI-specific by structure (hardcoded consumer_key, AOI-specific source bridge, AOI-specific proxy). Genealogy does not have a transient compose path at all. The "shared host adapter" claim holds only for the result-backed surface family, not for the transient launch family.

The memo should be explicit about this split rather than implying the adapter will cover all 10 contract families uniformly.

### Is adopting source-backed-readiness in the AOI launch surface the right proof move?

**Right direction, but still too AOI-shaped.** See Finding 4. The proof should demonstrate readiness consumption on both workflows to support the cross-workflow claim.

### Does the memo distinguish correctly between host navigation, orchestrator routing, project identity, and local snapshot persistence?

**Mostly.** The four-way distinction is real. The gap is host-side surface selection (Finding 5) — the memo doesn't say whether "which analyzer surfaces to use for this workflow experience" is navigation (host) or routing (analyzer) or a new intermediate concern.

### Is the proof bar strong enough without a second consumer?

**For a bounded first slice, yes. For Stage 13 closure, no.** The roadmap explicitly requires a "second consumer or generic host proof." The memo's proof bar is the bounded-current-consumer version. That is legitimate as a first slice, but Stage 13 should stay at "partial" until the harder evidence exists. See Finding 1.

---

## Required revisions before approving

1. **Frame this as a bounded first slice of Stage 13**, not the full exit evidence. Say explicitly that Stage 13 stays at "partial" after this slice.

2. **Enumerate the consumer_key coupling asymmetry** in the Host Contract v1 matrix: result/run routes accept consumer_key as a parameter (generic), compose routes have it hardcoded (structurally bound to the-critic).

3. **Right-size the consolidation scope** by reflecting which the-critic files already use shared clients (all three pages do) vs. which have remaining direct fetches (four component-level optimizations). Classify which direct fetches are in-scope vs. documented out-of-scope.

4. **Make the readiness proof cross-workflow**, not just AOI. Require at least one genealogy readiness consumption in the proof bar.

5. **Document host-side surface selection** as an explicit contract concern: in v1, each host page hardcodes which analyzer surfaces it combines. Say whether that is acceptable or whether the contract should enumerate current surface families per workflow.

6. **Expand the compose-from-source proxy description** to acknowledge the full host-owned preparation chain (identity resolution, cross-reference validation, context matching), not just "resolves project-local source identity."

---

## Non-blocking observations

- The memo correctly avoids lifecycle scope creep (Decision 7).
- The memo correctly keeps the proof grounded in the current consumer rather than inventing a hypothetical second app.
- The memo's claim that Stage 13 is "formalization and consolidation, not greenfield invention" is honest and grounded in the code.
- The existing `boundedV2Client.ts` is already a substantial partial implementation of the shared host adapter. The Stage 13 consolidation work is real but bounded.
- The `DEFAULT_CONSUMER_KEY` pattern across result routes means those routes are already generic enough for other consumers to call. The structural consumer coupling is concentrated in the compose layer.

---

## Summary

The memo correctly identifies the right next platform seam. The host contract is already partially real in code, and Stage 13 is correctly scoped as formalization rather than invention. The seven decisions are sound. The required revisions are about honesty of framing (bounded first slice, not full closure), accuracy of the coupling map (compose consumer_key is hardcoded, not parameterized), right-sizing the consolidation scope (pages are already clean), and cross-workflow evidence in the proof bar (readiness should cover genealogy too). None of these require changing the stage's fundamental shape.
