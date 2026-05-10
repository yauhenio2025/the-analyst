# Codex Audit Report

Date: 2026-04-14

Target memo: `communications/MEMO_2026-04-14_close_read_post_publication_stabilization_and_delivery_posture_scope.md`

Verdict: **Approve with corrections**

## Context Check

I read the target memo and the required recent memo chain, especially:

- `communications/MEMO_2026-04-13_close_read_public_host_topology_and_admitted_family_umbrella_publication_completion.md`
- `communications/MEMO_2026-04-13_close_read_roadmap_update_after_public_host_topology_and_admitted_family_umbrella_publication_completion.md`
- `communications/NOTE_2026-04-13_close_read_public_host_topology_evidence.md`
- `communications/NOTE_2026-04-13_close_read_public_route_matrix_and_browser_diagnosis.md`
- `communications/MEMO_2026-04-11_close_read_admitted_concept_operator_surface_and_thin_host_simplification_scope.md`
- `communications/MEMO_2026-04-13_close_read_admitted_concept_operator_surface_and_thin_host_simplification_completion.md`
- `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
- the canonical roadmap memo

I also checked three different truth layers on 2026-04-14:

1. deployed-source-aligned `origin/master` in `the-critic` and `analyzer-v2`
2. current live public behavior on `https://the-critic-1.onrender.com` and `https://the-critic.onrender.com`
3. current local trees in `analyzer-v2`, `the-critic`, and `analyzer-mgmt`

The local trees are materially dirty in all three repos, so they are not trustworthy as deployed truth.

## Conclusion

The memo is directionally right. The next default should still be a bounded stabilization tranche on the live Critic host pair, not standalone extraction and not family expansion.

That said, the memo needs corrections because it understates the leading residual and slightly overstates the repo-tracked config truth.

As of 2026-04-14, the six admitted public routes still hydrate successfully on the live pair, and I did not reproduce any public route `404`, extra family leak, extra concept-submode leak, or stale `Close Read V1` / `genealogy pilot` wording. That means the remaining work is genuinely post-publication stabilization rather than publication-from-zero.

But the leading residual is more specific than the memo says. The live genealogy page still emits two failed requests to:

- `http://localhost:8001/v1/styles/tokens/humanist_craft`

and corresponding `DesignTokens` fallback warnings, while the rest of the page renders correctly.

That is not just generic "console noise." It is a live frontend build/config/runtime-truth defect. The memo should say so explicitly.

## Direct Answers

### 1. Is "bounded Critic-host stabilization first" still the right default, or is standalone extraction now the stronger corridor?

Bounded Critic-host stabilization first is still the right default.

Why:

- `origin/master` in `the-critic` already contains the public `close-read` routes and admitted-family pages.
- the live frontend still serves the April 13 verified bundle line:
  - `main.1d26cf69.js`
- on 2026-04-14, the live public browser pass still hydrated:
  - `/p/:projectId/close-read`
  - `/p/:projectId/close-read/genealogy`
  - `/p/:projectId/close-read/aoi`
  - `/p/:projectId/close-read/aoi/:thinkerId`
  - `/p/:projectId/close-read/concepts`
  - `/p/:projectId/close-read/concepts/:conceptSlug`
- the only reproduced public defect was the genealogy design-token fetch drift to `localhost`

That is not strong evidence that Critic-host entanglement itself has become the blocker. It is stronger evidence that one narrow live-host stabilization pass is still cheaper and more honest than extracting a standalone host now.

There is still real host entanglement in code:

- `webapp/src/routes.tsx` keeps Close Read under `AppLayout`
- `webapp/src/pages/CloseReadPage.tsx` still depends on Critic-local `CaptureProvider`, `ProvenanceProvider`, and host fetch/runtime helpers

But that entanglement is not yet disproving the current host posture. It is a posture question to freeze after stabilization, not before it.

### 2. Is the memo right to keep family expansion out of scope?

Yes.

The live public product still reflects exactly the admitted set:

- Genealogy
- Anxiety of Influence
- Concept Analysis

And the concept family still stays bounded to:

- `inferential`
- `logical`

Evidence:

- live umbrella text on 2026-04-14 still showed exactly those three family cards
- live concept detail still showed inferential and logical only
- I did not see `hypotheses`, `report`, or other extra concept/AOI modes on the public Close Read routes
- `origin/master:webapp/src/pages/closeReadConceptRuntime.ts` explicitly filters to `inferential | logical`

So the memo is right to keep family widening out of this tranche.

### 3. Is the known genealogy console-noise residual actually the leading public defect?

Yes, but the memo should describe it more precisely.

What I reproduced live on 2026-04-14:

- the genealogy page hydrated and rendered
- it produced two `ERR_CONNECTION_REFUSED` request failures to:
  - `http://localhost:8001/v1/styles/tokens/humanist_craft`
- it also logged paired `DesignTokens` warnings that the page was falling back to local tokens

That makes the leading public defect:

- a genealogy-route design-token endpoint misconfiguration or runtime fallback defect

not just:

- unexplained console noise

This distinction matters because the fix and the audit criteria should target the real failure mode:

- no requests from the live public frontend to dev-only hosts such as `localhost`

### 4. Is the proposed repo-owned browser-proof harness appropriately bounded and useful?

Yes, with one correction in framing.

The repo already has browser-test scaffolding in `the-critic`:

- `webapp/playwright.config.ts`
- `test-stage5-aoi-landing-smoke.js`
- `test-stage7-genealogy-cutover-smoke.sh`
- `test-stage9-aoi-cutover-smoke.sh`

So the harness is not inventing browser automation from zero.

But there is still no committed, standard replay harness for the six admitted public Close Read routes on the live public host pair that captures:

- route outcome
- screenshot evidence
- console errors/warnings
- request failures
- bundle fingerprint

So the proposed harness is useful and appropriately bounded if it is framed as:

- one Close Read public-matrix replay artifact extending existing Playwright/smoke scaffolding

and not as:

- a generic cross-app QA framework

### 5. Does the codebase support the memo's claim that the remaining work is post-publication stabilization/posture rather than publication?

Yes.

Evidence from deployed source and live behavior:

- `origin/master` in `the-critic` includes the admitted Close Read routes and pages
- the live asset manifest still serves `main.1d26cf69.js`
- the six admitted routes still hydrate on the live public frontend on 2026-04-14
- stale `Close Read V1` / `genealogy pilot` wording is absent in the live public pages I checked
- no route I tested rendered a public app `404`

So publication is already real in bounded form.

The remaining work is not "publish Close Read."
It is:

- stabilize the public surface
- repair deployment/config truth drift
- then decide whether host posture itself is the next blocker

### 6. Is the memo missing any important residual on the public Close Read surface, deployment/config truth, or repo divergence?

Yes. It is missing at least four important corrections.

#### A. The memo chain overstates repo-tracked frontend env truth

The April 13 evidence note says the tracked frontend env source is:

- `the-critic/webapp/.env`

But `webapp/.env` is not in `origin/master`, and `.gitignore` explicitly ignores `.env`.

That means:

- `webapp/.env` is not tracked documentary truth
- it must not be used as evidence that deployed frontend env is normalized

The tracked documentary source is `render.yaml`, not `webapp/.env`.

#### B. `.env.example` is incomplete for this seam

`origin/master:.env.example` documents `REACT_APP_API_URL` only in a comment and does not document:

- `REACT_APP_ANALYZER_V2_URL`

That makes the repo-facing env story incomplete for the exact defect now visible on the live genealogy route.

#### C. The residual is not just browser noise; it points at live build/runtime truth drift

Important observed combination:

- live browser requests still hit `http://localhost:8001/v1/styles/tokens/humanist_craft`
- live analyzer-v2 token endpoint is healthy at:
  - `https://analyzer-v2.onrender.com/v1/styles/tokens/humanist_craft`
- `origin/master:render.yaml` documents:
  - `REACT_APP_ANALYZER_V2_URL=https://analyzer-v2.onrender.com`
- the deployed bundle still contains both:
  - `REACT_APP_ANALYZER_V2_URL:"https://analyzer-v2.onrender.com"`
  - `http://localhost:8001`

Inference:

- the failure is likely a live build-env/runtime-fallback or duplicated-token-provider-path issue
- it is not evidence of analyzer-v2 service outage

The memo should explicitly require proving the actual live frontend env/build path, not only the service names.

#### D. Repo divergence is large enough that execution must use isolated worktrees

All three local repos are materially dirty:

- `analyzer-v2`
- `the-critic`
- `analyzer-mgmt`

That supports the memo's "align to deployed truth first" rule.
The report should freeze that as an execution prerequisite, not a suggestion.

### 7. Does the memo keep analyzer-v2 and analyzer-mgmt out of scope honestly?

Mostly yes, with one nuance.

`analyzer-mgmt` is honestly out of scope for this tranche:

- I found no live public-route defect pointing at analyzer-mgmt
- the public Close Read routes do not directly depend on analyzer-mgmt surfaces

`analyzer-v2 runtime changes` are also honestly out of scope:

- the live analyzer-v2 token endpoint responds correctly
- no current evidence suggests a backend token-generation outage

But the memo should be careful not to imply that absolutely no analyzer-side source may matter.

Nuance:

- if the root cause lives in the vendored renderer/package path shared from `analyzer-v2/renderers-ui`, fixing it may require package-source follow-up or re-vendoring
- that is not the same thing as reopening analyzer-v2 runtime scope

So the honest scope boundary is:

- keep analyzer-v2 runtime and analyzer-mgmt out
- allow the-critic build-env or vendored-renderer corrections if the live defect requires them

## Evidence

### A. Live public proof still matches the April 13 publication closeout in the important ways

On 2026-04-14:

- `https://the-critic-1.onrender.com/asset-manifest.json` still points to:
  - `main.1d26cf69.js`
- `https://the-critic-1.onrender.com/p/cutover-concept-artifact-closeout-20260411-090918/close-read` returns `200`
- the six admitted public routes still hydrate in a browser session
- stale `Close Read V1` / `genealogy pilot` wording did not appear in the live pages I checked

### B. `origin/master` still lines up with the publication claim

Recent `the-critic` `origin/master` history still shows the exact publication sequence cited in the memo chain:

- `232c368` `Publish Close Read umbrella on public frontend`
- `1d726db` `Vendor renderer package for Close Read publication`
- `5f0260f` `Unblock Close Read family detail pages`
- `10cec95` `Fallback to native AOI presentation in Close Read`
- `4a87971` `Use native AOI thematic surface in Close Read`
- `938c09f` `Remove stale genealogy pilot copy from Close Read`

And `origin/master:webapp/src/routes.tsx` still defines the admitted route set:

- umbrella landing
- genealogy
- AOI index
- AOI thinker page
- concept index
- concept detail

### C. The leading residual is narrowly localized

The only reproduced request failures in the six-route live browser probe were on genealogy:

- `net::ERR_CONNECTION_REFUSED http://localhost:8001/v1/styles/tokens/humanist_craft`
- twice during page load

I did not reproduce similar request failures on:

- umbrella
- AOI index
- AOI detail
- concept index
- concept detail

### D. Family/submode boundaries still hold

Live evidence plus source both still align on the admitted boundary:

- umbrella shows exactly three families
- concept detail remains inferential/logical only
- `origin/master:webapp/src/pages/closeReadConceptRuntime.ts` filters to `inferential | logical`
- I did not see public leakage of extra families, `hypotheses`, or `report`

### E. Repo-facing env truth is weaker than the memo chain says

What is tracked:

- `origin/master:render.yaml`
- `origin/master:.env.example`

What is not tracked:

- `origin/master:webapp/.env` does not exist

And `.gitignore` ignores:

- `.env`
- `.env.local`
- `.env.*.local`

So any memo relying on tracked `webapp/.env` as authoritative documentary truth is overstating the repo truth set.

## Concrete Corrections

Before using the memo as the execution guide, I would correct it in these ways:

1. Replace "genealogy console-noise residual" with a more precise defect statement.
   - Example: "live genealogy route still makes two failed design-token requests to `localhost`, then falls back to local tokens."

2. Expand Phase 0 from host-pair alignment into full live frontend build/env proof.
   - Verify the actual deployed frontend env/build behavior for `REACT_APP_ANALYZER_V2_URL`, not only service names and API URL.
   - Freeze the live bundle fingerprint alongside the route-matrix replay.

3. Remove any implication that tracked `webapp/.env` is authoritative repo truth.
   - Treat `render.yaml` as documentary tracked truth.
   - Treat dashboard/static-site env plus live bundle behavior as live truth.

4. Add one explicit acceptance criterion about dev-host leakage.
   - No admitted public route should request `localhost`, `127.0.0.1`, or other non-public development hosts.

5. Frame the replay harness as an extension of existing `the-critic` Playwright/smoke scaffolding.
   - configurable host and specimen ids
   - six admitted public routes only
   - screenshot capture
   - console and request-failure capture
   - bundle fingerprint capture
   - pass/fail summary

6. Keep analyzer-v2 runtime and analyzer-mgmt out of scope, but explicitly allow:
   - the-critic build-env fixes
   - the-critic vendored renderer/package fixes
   - any minimal package-source follow-up only if needed to remove the live public defect

## Ready To Execute

Yes, after the corrections above.

The memo's corridor is the right one, and it is ready to execute once it stops describing the leading residual as generic console noise and stops leaning on a non-tracked `webapp/.env` as if it were authoritative repo truth.

The honest execution posture is:

- public Close Read publication is already complete in bounded form
- the next tranche is genuine stabilization
- the first stabilization target is live frontend env/build truth on the genealogy route
