# Codex Audit Report

Date: 2026-04-13

Target memo: `communications/MEMO_2026-04-13_close_read_public_host_topology_and_admitted_family_umbrella_publication_scope.md`

Verdict: **Approve with corrections**

## Context Check

I read the target memo and the full required supporting memo chain:

- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`
- `communications/MEMO_2026-04-05_close_read_post_v1_recalibration_multi_engine_boundary.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md`
- `communications/MEMO_2026-04-11_close_read_concept_translated_artifact_authority_live_closeout_completion.md`
- `communications/MEMO_2026-04-13_close_read_admitted_concept_operator_surface_and_thin_host_simplification_completion.md`
- `communications/MEMO_2026-04-13_close_read_roadmap_update_after_admitted_concept_operator_surface_and_thin_host_simplification_completion.md`
- `communications/MEMO_2026-04-13_close_read_public_host_topology_and_admitted_family_umbrella_publication_scope.md`

I also inspected local code in `analyzer-v2`, `the-critic`, and `analyzer-mgmt`, and I verified live public/API behavior against the currently reachable Render hosts on 2026-04-13.

## Conclusion

The memo is strategically correct. It moves the roadmap from admitted concept normalization into public-host publication of the Close Read umbrella, and that matches the larger memo chain: keep `analyzer-v2` as the semantic brain, keep hosts thin, keep the admitted family set narrow, and spend the next tranche on product-surface publication rather than reopening analyzer internals.

It should not be approved unchanged, because its account of current public publication state is too soft and slightly too optimistic. The real deployment picture on 2026-04-13 is more specific:

- Local `the-critic/render.yaml` is configured around `benanav-web` and `benanav-api`.
- The active Render services visible in the selected workspace are `the-critic-1` (static frontend) and `the-critic` (API), both on branch `master`, updated on 2026-04-13.
- `https://benanav-web.onrender.com/` and `https://benanav-api.onrender.com/` both return `404`.
- `https://the-critic-1.onrender.com/` is the live static frontend host. Its root and native routes load, but all tested `close-read` routes hydrate to a React `404 Not Found`.
- The deployed frontend bundle on `the-critic-1` does not include `close-read` routes or a `Close Read` nav entry, even though the local source tree does.
- `https://the-critic.onrender.com/api/...` serves the concept-analysis and scrutiny APIs successfully.
- `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref/result` is live and returns results, even though the current local `analyzer-v2` checkout does not show that route in source.

So the memo is right about what should happen next, but it needs firmer language about what is actually live now.

## Direct Answers

### 1. Does the memo correctly move the roadmap from admitted concept normalization into public-host publication of the Close Read umbrella?

Yes, with corrections. That is the right next tranche.

### 2. Is host-topology ambiguity real enough to justify a Phase 0?

Yes. In fact, the ambiguity is stronger than the memo states. This is not only a question of "which hostname is public?" It is also a question of which deployed service and which frontend bundle are actually serving the product.

### 3. Does the memo keep the admitted family set and submode boundary concrete enough?

Yes. Local source is concrete and aligned with the memo chain:

- `genealogy`
- `AOI` as thematic single-thinker Close Read
- `concept analysis` limited to `inferential` and `logical`

No evidence supports broadening the admitted umbrella beyond that set in this tranche.

### 4. Does the memo keep family-specific pages and native-route coexistence in the right role?

Yes. Local source preserves coexistence instead of forcing premature unification. The umbrella adds a routed surface over admitted families, while native routes remain intact and linked.

### 5. Does the memo keep `analyzer-v2` in the right role?

Yes. The memo keeps concept-artifact authority in `analyzer-v2`, and that is correct. This tranche should not spend budget on new analyzer-side concept semantics.

### 6. Is the shared admitted-family product baseline concrete enough to verify?

Mostly yes locally, not yet publicly. Local code shows a narrow shared baseline around result-backed reading/work, provenance visibility, capture mode, `CaptureActionBar`, and routed destinations. But public verification is blocked by the fact that the deployed frontend bundle has not yet published the Close Read umbrella.

### 7. Does the memo stay honest about local-vs-live and configured-vs-live divergence?

Not fully. It notices ambiguity, but it should explicitly name the current divergences:

- configured hostnames vs actually serving hostnames
- local frontend routes vs deployed frontend bundle
- local `analyzer-v2` checkout vs live `analyzer-v2` result endpoint

### 8. Does the memo overstate or understate the current public product surface?

It slightly overstates it. The routes are already coded locally, but they are not currently published in the live frontend bundle. It also understates that a raw `200` from the static host is not enough; browser hydration still fails on the `close-read` routes.

### 9. If the larger goal remains "`analyzer-v2` as the brain, hosts as thinner shells," is this the right next tranche?

Yes. The next work should be deployment truth, frontend publication, route/nav cutover, and copy normalization. It should not drift back into analyzer-v2 concept-internal work.

## Evidence

### A. Local product boundary is concrete and aligned

In `the-critic` local source, the Close Read umbrella is already implemented as a bounded, admitted-family surface:

- `webapp/src/routes.tsx` defines native routes and the `close-read` umbrella children for `genealogy`, `aoi`, `aoi/:thinkerId`, `concepts`, and `concepts/:conceptSlug`.
- `webapp/src/components/AppLayout.tsx` includes a `Close Read` nav entry in the Synthesis menu.
- `webapp/src/components/CloseReadFamilySwitcher.tsx` freezes the family switcher to `genealogy | aoi | concepts`.
- `webapp/src/pages/CloseReadLandingPage.tsx` implements the umbrella landing page and loads family availability in parallel.
- `webapp/src/pages/CloseReadAoiPages.tsx` keeps AOI Close Read bounded to admitted thinker pages while preserving links back to native AOI routes.
- `webapp/src/components/influence/AoiV2ThematicPanel.tsx` suppresses non-admitted controls in `surfaceMode="close-read"`: no run-analysis button, no transient compose launch, no download PDF, no clear action.
- `webapp/src/pages/closeReadConceptRuntime.ts` limits concept Close Read to `inferential` and `logical`.
- `webapp/src/pages/CloseReadConceptPages.tsx` preserves native concept-analysis links and admits logical-only scrutiny without broadening the family.

The host/API layer also matches the intended thin-host boundary:

- `the-critic/api/server.py` treats concept artifacts as analyzer-owned and read-through.
- `the-critic/api/server.py` serves `/api/concept/analyses/{concept}` by reading through to `analyzer-v2` and persisting refreshed host cache.
- `the-critic/api/server.py` exposes scrutiny launch/results endpoints without moving authority into the host.

This means the memo's product boundary is not speculative. It is already encoded locally.

### B. Live deployment truth does not yet match local source

On 2026-04-13, the selected Render workspace showed these relevant services:

- static site `the-critic-1`
- web service `the-critic`

The same inspection did not show live `benanav-web` or `benanav-api` services in that workspace. Direct checks then showed:

- `https://benanav-web.onrender.com/` returns `404`
- `https://benanav-api.onrender.com/` returns `404`
- `https://the-critic.onrender.com/api/concept/analyses/innovation?analysis_type=logical` returns `200`
- `https://the-critic.onrender.com/api/concept/analyses/innovation?analysis_type=inferential` returns `200`
- `https://the-critic.onrender.com/api/scrutiny/results/innovation` returns `200`

For the frontend:

- `https://the-critic-1.onrender.com/` loads successfully
- native routes such as `/p/.../genealogy`, `/p/.../anxiety-of-influence`, and `/p/.../concept-analysis` load successfully
- tested Close Read routes such as `/p/.../close-read`, `/close-read/genealogy`, `/close-read/aoi`, and `/close-read/concepts` hydrate to a React `404 Not Found`

The deployed `asset-manifest.json` points to a current bundle whose contents do not include `close-read` route strings or a `Close Read` nav item. That same deployed bundle hardcodes `https://the-critic.onrender.com/api` rather than `https://benanav-api.onrender.com`.

So the real live/frontend answer is:

- the product frontend host is currently `the-critic-1`
- the product API host is currently `the-critic`
- the Close Read umbrella is not yet published in the deployed frontend bundle

### C. There is also a secondary local-vs-live analyzer divergence

Live `analyzer-v2` successfully serves:

- `GET /v1/orchestrator/concept-analysis-by-ref/result`

But the current local `analyzer-v2` checkout shows the POST launch route in `src/api/routes/orchestrator.py` and does not show a matching local source implementation for the result route when searched repo-wide.

That does not change the roadmap conclusion, but it does mean the memo should be careful not to imply that all relevant topology truth can be read directly from the local checkout alone.

### D. One small but real publication-scope cleanup remains in local UI copy

`the-critic/webapp/src/pages/CloseReadPage.tsx` still contains stale public-facing copy such as:

- `Close Read V1`
- `genealogy pilot`

That is a minor issue compared with deployment truth, but it belongs in the same publication tranche because the umbrella should not go public carrying pilot-only framing.

## Corrections Required

Before relying on the memo as the operative publication guide, I would make these corrections explicit:

1. Name the actual currently serving hosts, not only the uncertainty.
   - Current live frontend: `https://the-critic-1.onrender.com`
   - Current live API: `https://the-critic.onrender.com`
   - `benanav-web` and `benanav-api` are not currently serving the product on 2026-04-13.

2. State plainly that Close Read is coded locally but not yet published in the deployed frontend bundle.
   - Native routes are live.
   - Close Read routes are not live.
   - Browser verification is required; raw static-host `200` responses are not enough.

3. Keep Phase 0 focused on deployment/cutover truth and frontend publication.
   - Determine the authoritative frontend host and API host.
   - Publish the bundle that actually contains the Close Read nav/routes.
   - Verify SPA routing and browser hydration on each Close Read route.
   - Do not spend this tranche inside analyzer-v2 concept internals.

4. Add copy normalization to publication scope.
   - Remove stale `V1` / `pilot` framing from the public genealogy Close Read surface.

5. Note the secondary analyzer-v2 divergence.
   - Live result retrieval works.
   - Current local source does not fully reflect that live route.

## Final Assessment

Approve the memo with corrections.

As a roadmap move, it is right: the next tranche should be public-host publication of the admitted Close Read umbrella, not new analyzer-v2 concept work. As a statement of present public product state, it needs the corrections above so it does not overstate what is currently live or leave the host/bundle truth too vague.
