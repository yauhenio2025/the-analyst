# Review: Close Read Public Host Topology And Admitted Family Umbrella Publication Scope

**Reviewer**: Claude (Opus 4.6, 1M context)
**Date**: 2026-04-13
**Verdict**: **APPROVE WITH CORRECTIONS**

---

## Context Check

I read every required memo in full:

| # | Memo | Read |
|---|------|------|
| 1 | `MEMO_2026-03-30_distilled_strategic_roadmap.md` | Yes -- 6-phase strategy, anti-drift rules, current Phase E active question |
| 2 | `MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` | Yes -- canonical program ledger, 7 required layers, 16 stages, decision revisions through 2026-04-05 |
| 3 | `MEMO_2026-04-04_close_read_roadmap_recalibration.md` | Yes -- 4-step honest corridor, V1 product scoping readiness |
| 4 | `MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md` | Yes -- default vs. bespoke modules, concept analysis as next serious family |
| 5 | `MEMO_2026-04-05_close_read_v1_product_memo.md` | Yes -- 5 product decisions, genealogy-first V1, capture-and-route |
| 6 | `MEMO_2026-04-05_close_read_post_v1_recalibration_multi_engine_boundary.md` | Yes -- multi-engine trajectory, AOI admission, V1.5 boundary |
| 7 | `MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md` | Yes -- 5 frozen decisions, genealogy + AOI, shared baseline, deferrals |
| 8 | `MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md` | Yes -- exact route behavior, landing page law, family switcher, stateful remount |
| 9 | `MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md` | Yes -- inferential + logical first, 3-way migration split, scrutiny-on-logical |
| 10 | `MEMO_2026-04-11_close_read_concept_translated_artifact_authority_live_closeout_completion.md` | Yes -- 4-layer proof, fresh specimens, analyzer-v2 is semantic authority |
| 11 | `MEMO_2026-04-13_close_read_admitted_concept_operator_surface_and_thin_host_simplification_completion.md` | Yes -- 3 deployed pushes, operator-surface hardening, thin-host-law clarification |
| 12 | `MEMO_2026-04-13_close_read_roadmap_update_after_admitted_concept_operator_surface_and_thin_host_simplification_completion.md` | Yes -- Corridor A complete, Corridor B next, dominant uncertainty shifted to public product surface |

I also inspected all required code files, all required live URLs, the Render service list, and all three codebases.

---

## Executive Summary

The memo correctly identifies the right next corridor: the product-layer publication gap. The concept seam is genuinely closed. The admitted family set is correctly frozen. The strategic direction is preserved. The boundary discipline is sound.

However, the memo's core diagnostic claim -- that Close Read routes "returned 404" on the public frontend host -- is based on **checking the wrong host**. The actual deployed topology diverges from what `render.yaml` declares, and the real frontend is already serving the React SPA at routes including Close Read. This changes the shape of the work from "figure out where the frontend lives and make routes reachable" to "document the real topology and verify the already-reachable pages work correctly."

The memo should be corrected on the topology facts, but its structure, boundary discipline, and strategic placement are sound.

---

## Critical Finding: The Deployed Topology Is Not What render.yaml Says

### What render.yaml declares

```
benanav-api  (web_service)   -> https://benanav-api.onrender.com
benanav-web  (static_site)   -> https://benanav-web.onrender.com
```

### What actually exists on Render

From the live Render service list (verified 2026-04-13):

| Service Name | Type | URL | Repo/Branch | Updated |
|---|---|---|---|---|
| `the-critic` | web_service (Python) | `https://the-critic.onrender.com` | yauhenio2025/the-critic, master, rootDir: `api` | 2026-04-13 |
| `the-critic-1` | static_site | `https://the-critic-1.onrender.com` | yauhenio2025/the-critic, master, publishPath: `webapp/build` | 2026-04-13 |

**There are no services named `benanav-api` or `benanav-web` on Render.** Those names exist only in the stale `render.yaml`. The actual services were created manually on the Render dashboard with different names.

### What each host actually serves today

| Host | Status | Evidence |
|---|---|---|
| `benanav-web.onrender.com` | **404 on everything** (including root) | Service doesn't exist on Render |
| `benanav-api.onrender.com` | **404 on everything** | Service doesn't exist on Render |
| `the-critic.onrender.com` | **Live API** -- concept analyses, scrutiny, all backend endpoints return 200 | Verified with 5 API calls returning rich JSON data |
| `the-critic-1.onrender.com` | **Live React SPA** -- serves HTML shell with React app for all routes including Close Read | Verified: root and `/p/.../close-read` both return React app HTML |
| `analyzer-v2.onrender.com` | **Live API** -- orchestrator, concept-analysis-by-ref, all endpoints return 200 | Verified with 2 concept artifact lookups |

### The memo's 404 diagnosis was against the wrong host

The memo states: "checked Close Read project URLs on `benanav-web.onrender.com` returned 404." This is true, but `benanav-web.onrender.com` is not the live frontend. The live frontend is `the-critic-1.onrender.com`, and it **does** serve the React SPA for Close Read routes.

### Environment variable configuration

The `the-critic-1` static site has **no Render-configured env vars** (none appear in the Render API response). This means the build uses the committed `.env` file:

```
REACT_APP_API_URL=https://the-critic.onrender.com/api       # Correct
REACT_APP_ANALYZER_V2_URL=https://analyzer-v2.onrender.com  # Correct
```

Both point to live, healthy services. The `render.yaml` env vars (`REACT_APP_API_URL: https://benanav-api.onrender.com`) are **never used** because the actual Render service was not created from render.yaml.

### Consequence for the memo

The "Close Read routes are not reachable on the public frontend host" claim is almost certainly wrong. The SPA shell loads at `the-critic-1.onrender.com/p/{projectId}/close-read`, the `_redirects` catch-all (`/* /index.html 200`) is working, the API URLs are correctly configured, and the React Router definitions include all six Close Read routes. The Close Read umbrella may already be publicly functional.

**Phase 0 (topology audit) is still necessary** -- but its output should be "the real topology is already healthier than assumed" rather than "we need to fix a broken publication path."

---

## Detailed Answers to Each Required Question

### 1. Does the memo correctly move the roadmap from admitted concept normalization into public Close Read product publication, or is that transition premature?

**The transition is correct and not premature.** The evidence chain is thorough:

- Corridor A (concept authority, scrutiny, translated-artifact, operator-surface normalization) is genuinely closed across 4 memos with live proof specimens
- The concept seam has been proved on a fresh project (`cutover-concept-artifact-closeout-20260411-090918`) with exact job IDs, artifact hashes, and validation status documented
- Both the-critic readback and analyzer-mgmt operator surface have been hardened and deployed
- The roadmap update memo explicitly re-anchors the dominant uncertainty to "can the already-coded pages become a real public product surface"

The remaining work before this transition would have been: re-proving concept authority (unnecessary), widening the concept submode set (premature), or reopening operator-surface questions (already closed). None of those is more urgent than resolving the basic publication story.

### 2. Is the public-host-topology audit genuinely the first necessary step, or is the memo overreacting to one host mismatch?

**The audit is genuinely necessary, but the memo underestimates how much it already knows.** The situation is not "one host mismatch" -- it is a complete divergence between the declared topology (`render.yaml`) and the live topology (Render dashboard):

- `render.yaml` declares services that don't exist on Render
- The live services have different names, different URLs, and were configured independently
- `render.yaml` has the wrong `REACT_APP_API_URL` (pointing to `benanav-api.onrender.com` which doesn't exist)
- The memo tested the wrong host and concluded the routes are unreachable

The audit IS the right first step. But my inspection already provides the answer: the live topology is `the-critic.onrender.com` (API) + `the-critic-1.onrender.com` (frontend) + `analyzer-v2.onrender.com` (brain). The render.yaml should be updated to match reality or deleted if services are managed via Render dashboard.

### 3. Does the memo keep the larger direction clear enough?

**Yes.** The four-layer strategic architecture is preserved throughout:

| Layer | Role | Status per memo | Verified |
|---|---|---|---|
| analyzer-v2 | The brain | Semantic authority for concept, genealogy, AOI workflows | Yes -- all orchestrator/executor endpoints live |
| analyzer-mgmt | Operator console | Job inspection, concept-artifact cards, engine/workflow management | Yes -- 23 management sections, concept-artifact on job pages |
| the-critic webapp | Current Close Read product shell | Routes, pages, runtime code all present locally | Yes -- 24 Close Read files, 6 routes, 3 family runtimes |
| Broader standalone extraction | Later | Explicitly deferred | Yes -- consistent across all 12 memos |

The memo does not drift toward premature standalone-host work, does not try to make analyzer-mgmt the end-user surface, and does not reopen concept-authority internals.

### 4. Is the admitted family set correctly frozen here, or is the memo still too loose about family admission?

**Correctly frozen. The boundary is tight.** The admitted set is:

- Genealogy
- AOI thematic / result-backed (`anxiety_of_influence_thematic_single_thinker`)
- Concept analysis: `inferential` + `logical` only

Explicitly excluded (and verified not reopened):
- Concept `assumption`, `semantic_field`, `causal`, `metaphorical`
- Compose-from-intent under Close Read
- Cross-concept
- Any new family

This matches the decision chain: V1 memo froze genealogy-only -> V1.5 boundary memo added AOI -> concept family boundary memo added inferential + logical -> all subsequent memos preserved this exact set. There is no drift or looseness.

### 5. Does the memo keep family-specific pages and native-route coexistence in the right role, or is it drifting toward premature shell unification?

**Correctly positioned. No shell-unification drift.** The memo explicitly states:

- "Family-specific page bodies may stay family-specific"
- "This is not a generic shell unification project"
- "native family routes remain live" (Decision 3)
- The V1.5 coexistence memo established that family pages stay family-specific; the current memo inherits this

Verified in code: the `routes.tsx` file maintains both umbrella routes (`/p/:projectId/close-read/*`) and native routes (`/p/:projectId/genealogy`, `/p/:projectId/anxiety-of-influence/*`, `/p/:projectId/concept-analysis/*`). The `CloseReadFamilySwitcher` is a lightweight nav component, not a unifying shell.

### 6. Is the shared admitted-family baseline concrete enough to implement and audit?

**Yes. It is testable and already partially implemented.** The baseline is:

- Result-backed reading/work: Verifiable -- each family page requires at least one result to render
- Provenance visibility: Implemented in `CloseReadPage.tsx` (genealogy) via `ProvenanceProvider`
- Capture mode: Implemented via `CaptureProvider` wrapping each family page
- `CaptureActionBar`: Present and functional on genealogy surfaces
- Routed destinations: Arsenal + Research todo only

This is narrow enough to audit against code, but broad enough to be meaningful. The concept family pages (`CloseReadConceptPages.tsx`) don't yet carry capture/provenance infrastructure -- that could be a Phase 3 normalization item.

### 7. Does the memo stay honest about local-vs-live and configured-vs-live topology divergence?

**Partially. The memo correctly identifies the problem class but gets the specific diagnosis wrong.**

The memo is honest that:
- Local code and live deployment might diverge
- `render.yaml` and actual public behavior might diverge
- "Do not assume that `benanav-web` is current just because `render.yaml` says so"

The memo is incorrect that:
- It checked `benanav-web.onrender.com` and `the-critic.onrender.com` and concluded both return 404 for Close Read
- In reality, `benanav-web` doesn't exist on Render at all
- The actual frontend at `the-critic-1.onrender.com` was never checked
- The API endpoint at `the-critic.onrender.com` does serve API responses (it's a Python service, not a frontend), so of course it returns 404 for SPA routes

The memo would have benefited from doing what this review did: checking the actual Render service list, not just probing assumed URLs.

### 8. Is there any place where the memo overstates or understates what the public product surface already proves today?

**The memo significantly understates the current state.** Specifically:

**Understated**:
- The public frontend at `the-critic-1.onrender.com` is live and serving the React SPA
- The SPA catch-all redirect is working (React app loads for deep Close Read routes)
- API URLs are correctly configured in the deployed build
- All backend APIs (the-critic + analyzer-v2) are healthy and returning rich data
- The Close Read pages may already be fully functional as a public product surface

**Not understated (accurate)**:
- The topology documentation is genuinely incomplete
- The `render.yaml` is genuinely stale and misleading
- No one has verified the Close Read pages render correctly with data on the public host

**Neither overstated nor understated**:
- The admitted family set
- The strategic direction
- The boundary discipline

### 9. If you were protecting roadmap discipline, is this the right next corridor before broader Close Read extraction or a new family/submode line?

**Yes, unambiguously.** The reasoning:

1. You cannot credibly discuss standalone extraction if you haven't verified the current host actually works
2. You cannot credibly admit new families if the existing admitted families aren't provably reachable
3. The concept-authority corridor is genuinely closed -- continuing to work inside it would be drift
4. The publication gap is a real gap (even though it's smaller than the memo thinks)
5. Resolving publication truth creates a clean decision point for the next corridor

This tranche is the correct "clearing of the ledger" before the roadmap can branch into either extraction or expansion. Trying to skip it would leave the roadmap carrying ambiguity about what the public product surface actually is.

---

## Corrections Required

### Correction 1: Fix the host topology claim

**Current claim**: Close Read routes return 404 on `benanav-web.onrender.com` and `the-critic.onrender.com`.

**Corrected claim**: `benanav-web.onrender.com` does not exist as a Render service. `the-critic.onrender.com` is the API backend (not the frontend). The actual frontend is `the-critic-1.onrender.com`, which serves the React SPA including Close Read routes. The SPA HTML shell loads correctly at Close Read deep-link URLs.

### Correction 2: Update the topology documentation

The actual live topology (verified against Render service list 2026-04-13):

```
Frontend:     the-critic-1.onrender.com    (static_site, publishPath: webapp/build)
API Backend:  the-critic.onrender.com      (web_service, rootDir: api, uvicorn server:app)
Brain:        analyzer-v2.onrender.com     (web_service, uvicorn src.api.main:app)
```

`render.yaml` is stale and declares non-existent services (`benanav-api`, `benanav-web`). It should either be updated to match the live topology or removed if services are managed via Render dashboard.

### Correction 3: Re-scope Phase 0 and Phase 2

**Phase 0** should become: document the live topology (already done above), verify the React SPA renders Close Read pages correctly with real data on `the-critic-1.onrender.com`, and update or remove the stale `render.yaml`.

**Phase 2** may already be complete: if the SPA renders correctly at `the-critic-1.onrender.com/p/{projectId}/close-read`, then the routes are already "published." Phase 2 would shrink to verifying correctness rather than fixing a broken publication path.

### Correction 4: Add explicit env-var topology note

The `.env` file committed to the repo has correct URLs for the live topology:
```
REACT_APP_API_URL=https://the-critic.onrender.com/api
REACT_APP_ANALYZER_V2_URL=https://analyzer-v2.onrender.com
```

The `render.yaml` has incorrect URLs (`https://benanav-api.onrender.com`) but these are never used because the static site was not created from render.yaml. This should be explicitly documented to prevent future confusion.

---

## What Remains Valid

Despite the topology correction, the memo's core structure and boundary discipline are sound:

1. **The corridor choice is correct** -- publication-layer truth before expansion or extraction
2. **The admitted family freeze is correct** -- genealogy + AOI thematic + concept (inferential, logical)
3. **The shared baseline is concrete** -- result-backed, provenance, capture, Arsenal/Research todo
4. **The deferrals are correct** -- no standalone host, no new families, no concept internals
5. **The strategic direction is preserved** -- analyzer-v2 as brain, hosts as thin shells
6. **Phase 3 (product-law normalization) is still needed** -- even if routes are reachable, the shared baseline consistency across families should be verified
7. **Phase 4 (bounded proof) is still needed** -- verify all three families render correctly with real data on the public host

---

## Verified Live Evidence Summary

| What | Where | Status |
|---|---|---|
| Frontend SPA at root | `the-critic-1.onrender.com/` | React app loads |
| Frontend SPA at Close Read | `the-critic-1.onrender.com/p/.../close-read` | React app loads |
| Logical concept analysis (API) | `the-critic.onrender.com/api/concept/analyses/innovation?analysis_type=logical` | 200, rich data, 8 arguments |
| Inferential concept analysis (API) | `the-critic.onrender.com/api/concept/analyses/innovation?analysis_type=inferential` | 200, rich data, stability=0.38 |
| Scrutiny results (API) | `the-critic.onrender.com/api/scrutiny/results/innovation` | 200, 1 result, 5 lines of attack |
| Analyzer-v2 logical artifact | `analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref/result` | 200, validation passed, full translated artifact |
| Analyzer-v2 inferential artifact | `analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref/result` | 200, validation passed, full translated artifact |
| `benanav-web.onrender.com` (any route) | N/A | 404 -- service does not exist on Render |
| `benanav-api.onrender.com` (any route) | N/A | 404 -- service does not exist on Render |

---

## Final Verdict

**APPROVE WITH CORRECTIONS.**

The memo identifies the right next corridor, maintains exemplary boundary discipline, correctly freezes the admitted family set, preserves the strategic direction, and stays honest about what has and hasn't been proved. The transition from concept normalization to publication-layer work is well-supported and not premature.

The required corrections are factual, not structural:
1. The public frontend host is `the-critic-1.onrender.com`, not `benanav-web.onrender.com`
2. The Close Read SPA shell already loads at the correct URLs on the real host
3. `render.yaml` is completely stale and should be updated or removed
4. The work scope is likely smaller than the memo anticipates -- verification and documentation rather than fixing a broken publication path

With these corrections applied, the implementation sequence (Phase 0 through Phase 4) becomes tighter: Phase 0 is mostly answered, Phase 2 may already be done, and the real remaining work concentrates on Phase 3 (product-law normalization) and Phase 4 (bounded proof with real data on the public host).
