# Codex Audit: Phase 4 / Deliverable D Scope

## Verdict

The Phase 4 memo is directionally right, but it is slightly too optimistic about what already exists in `the-critic`.

Deliverable D is still fundamentally a `the-critic`-first tranche. The shared bounded-v2 contract already has the right seam for thinker-scoped AOI discovery and restore:

- `webapp/src/lib/boundedV2Client.ts` already supports `selectedSourceThinkerId` on run and result discovery.
- `webapp/src/hooks/useBoundedV2Workspace.ts` already accepts `selectedSourceThinkerId` and uses it for active-run discovery.
- `api/server.py` already enforces `selected_source_thinker_id` for AOI v2 launch and persists thinker identity in saved-result summaries when that identity is present.

So this is not a Phase 2 reopen.

But the generic proving surface itself, `AnalysisWorkspacePage`, does not currently consume that seam. As written today, it cannot correctly run AOI single-thinker via the generic route, and it can mix saved AOI results across thinkers.

My recommendation is:

- accept Deliverable D as the next tranche
- keep it frontend-first in `the-critic`
- tighten the scope so the proof is specifically:
  - generic route query-param parsing
  - AOI launch body wiring
  - thinker-scoped active-run/result/local-result restore behavior
  - one explicit AOI-to-generic handoff
- explicitly exclude generic `import-v2`/manual preview from the proof unless a small Critic-side metadata fix is added

## Blocking Issues

1. `AnalysisWorkspacePage` does not currently carry AOI thinker context into the shared contract.

Evidence:

- `webapp/src/pages/AnalysisWorkspacePage.tsx:82-85` reads only `projectId` and `workflowKey` from route params.
- `webapp/src/pages/AnalysisWorkspacePage.tsx:219-225` calls `useBoundedV2Workspace(...)` without `selectedSourceThinkerId`.
- `webapp/src/pages/AnalysisWorkspacePage.tsx:359-365` calls `discoverBoundedV2Results(...)` without `selectedSourceThinkerId`.
- `webapp/src/pages/AnalysisWorkspacePage.tsx:474-478` builds the generic start body without `selected_source_thinker_id` or `selected_source_thinker_name`.

Why this blocks Deliverable D:

- AOI v2 launch through the generic route will fail, because `api/server.py:19067-19072` rejects AOI generic starts that do not include `selected_source_thinker_id`.
- Even if the page is only restoring existing AOI work, active-run discovery and result discovery are currently project-wide for that workflow, not thinker-scoped.

2. Generic saved-result behavior will currently mix AOI thinkers.

Evidence:

- `webapp/src/pages/AnalysisWorkspacePage.tsx:346-414` merges all local + upstream results for the workflow and auto-loads the first merged result.
- `api/server.py:20154-20172` filters generic saved results only by `project_id + workflow_key`.
- By contrast, the existing AOI-specific surface explicitly filters both upstream and local results by thinker in `webapp/src/components/influence/AoiV2ThematicPanel.tsx:262-340`.

Why this blocks Deliverable D:

- On any project with more than one AOI thinker result, the generic AOI route can auto-restore the wrong thinker's result.
- That fails the memo's own acceptance criterion that AOI discovery in the generic workspace be thinker-scoped rather than mixed.

3. There is no current AOI-to-generic proof-route handoff.

Evidence:

- `webapp/src/pages/AnxietyOfInfluencePages.tsx:662-709` resolves the thinker default tab by navigating only to:
  - `/anxiety-of-influence/:thinkerId/v2-thematic`
  - `/anxiety-of-influence/:thinkerId/hypotheses`
- I found no existing navigation from the AOI surface to `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker`.

Why this blocks Deliverable D:

- The memo requires one deliberate entry path from the bespoke AOI surface into the generic workspace proof route.
- That path does not exist yet and must be implemented; it is not already latent.

## Non-Blocking Risks

1. Query params are the right route seam, but the minimum authoritative contract should be narrower than the memo implies.

What the code says:

- AOI launch truly requires `selected_source_thinker_id` (`api/server.py:19067-19072`).
- `selected_source_thinker_name` is optional display/context metadata and can be canonicalized server-side via `_load_aoi_prior_works(...)` (`api/server.py:18105-18111`).
- `AnalysisWorkspacePage` already has precedent for explicit query-param route context via `useDeepLink` and `?view` / `?section` (`webapp/src/hooks/useDeepLink.ts:1-32`, `webapp/src/pages/ArsenalPage.tsx:192-207`).

Risk:

- If the scope treats both thinker id and thinker name as equally authoritative route contract, implementation may become more brittle than necessary.

Recommended interpretation:

- `selected_source_thinker_id` required
- `selected_source_thinker_name` optional, display-only

2. Manual generic `import-v2` for AOI is not thinker-safe by default.

Evidence:

- The import path creates a local compatibility job without populating thinker identity (`api/server.py:19477-19495`).
- It then persists the presentation using those missing fields (`api/server.py:19507-19525`).
- Saved-result summaries only expose thinker identity if it exists in persisted payloads (`api/server.py:18394-18412`, `api/server.py:19797-19816`).

Why this matters:

- If Deliverable D tries to include generic AOI manual import as part of the proof, imported local snapshots can lose thinker identity and become hard to filter safely later.

This is not a blocker for the main proof if the tranche sticks to launch + restore through normal discovered runs/results.

3. The current automated coverage does not prove the generic AOI route.

What I verified:

- Focused tests passed in `the-critic` webapp:
  - 6 suites passed
  - 30 tests passed
- Those suites cover:
  - `boundedV2Client`
  - `useBoundedV2Workspace`
  - `AnalysisWorkspacePage`
  - `AoiV2ThematicPanel`
  - `AnxietyOfInfluencePages`

Gap:

- `AnalysisWorkspacePage` tests currently exercise generic placeholder workflows, not AOI query-param behavior.
- Existing AOI tests cover the bespoke AOI surface, not the generic proof route.

## Assumptions Tested

1. Deliverable D does not need analyzer-v2 changes for the primary proof.

Confirmed:

- `api/server.py:19055-19184` already supports generic workflow launch with AOI thinker fields.
- `api/server.py:18088-18316` already threads AOI thinker identity into the upstream v2 launch path.

2. The Phase 2 shared contract already supports thinker-scoped AOI discovery.

Confirmed:

- `webapp/src/lib/boundedV2Client.ts:69-101` already passes `selected_source_thinker_id` to upstream run/result discovery.
- `webapp/src/hooks/useBoundedV2Workspace.ts:23-28` and `webapp/src/hooks/useBoundedV2Workspace.ts:300-327` already support thinker-scoped active-run discovery.

3. Local saved-result payloads can already carry thinker identity.

Confirmed:

- Saved-result summaries extract `selected_source_thinker_id` and `selected_source_thinker_name` from persisted payloads in `api/server.py:18394-18412`.
- Result detail also returns those fields in `api/server.py:19797-19816`.
- The cache/refresh save paths preserve thinker identity when it exists on the run reference in `api/server.py:19579-19610` and `api/server.py:19646-19667`.

4. The existing AOI bespoke surface already demonstrates the exact behavior Deliverable D should reuse rather than reinvent.

Confirmed:

- `webapp/src/components/influence/AoiV2ThematicPanel.tsx:140-153` passes thinker context into the shared workspace hook.
- `webapp/src/components/influence/AoiV2ThematicPanel.tsx:262-340` filters both upstream and local saved results by thinker.
- `webapp/src/components/influence/AoiV2ThematicPanel.tsx:383-410` launches AOI with thinker identity.

5. `AnalysisWorkspacePage` currently lacks that reuse wiring.

Confirmed:

- It does not parse thinker query params.
- It does not pass thinker context to the hook.
- It does not filter saved results by thinker.
- It does not include thinker identity in AOI launch body.

6. No dynamic-form system is actually waiting in the wings here.

Confirmed:

- `webapp/src/hooks/useWorkflowMetadata.ts:1-125` is descriptive metadata only.
- There is no generic workflow input-schema/form-definition layer in the reviewed seam.

## Recommended Scope Tightening

1. Keep Deliverable D explicitly frontend-first in `the-critic`.

Do not reopen Phase 2.
Do not start in `boundedV2Client.ts` or `useBoundedV2Workspace.ts` unless a concrete failing test proves they need adjustment.

2. Tighten the AOI route contract.

Use:

- `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=<id>`

Optionally include:

- `selected_source_thinker_name=<name>`

But treat the id as the only authoritative input.

3. Narrow the proof to launch + restore + scoped discovery.

For this tranche, "AOI works on the generic route" should mean:

- generic route can start AOI with one thinker id
- generic route can discover active AOI runs for that thinker
- generic route can restore saved AOI results for that thinker
- generic route can reach that state from one deliberate AOI handoff link

Do not require:

- a generic workflow-input builder
- a route rewrite
- replacing the bespoke AOI page
- replacing the bespoke genealogy page

4. Keep generic manual import/preview out of acceptance unless identity persistence is patched.

If the team wants `Preview V2` / `Import V2` to count for AOI in this tranche, then add one small Critic-side patch so imported AOI snapshots preserve thinker identity before being saved locally.

Otherwise, explicitly exclude that path from the proof.

5. Do not change AOI default routing behavior.

The bespoke AOI page currently chooses between `v2-thematic` and `hypotheses`.
Deliverable D only needs one explicit handoff into the generic route, not a rewrite of that routing logic.

## Implementation Starting Point

Start here first:

1. `webapp/src/pages/AnalysisWorkspacePage.tsx`

Own these changes first:

- parse thinker query params from the URL
- pass `selectedSourceThinkerId` into `useBoundedV2Workspace(...)`
- pass the thinker filter into `discoverBoundedV2Results(...)`
- filter local AOI saved results by thinker before merge/auto-restore
- include thinker identity in AOI generic launch body
- show lightweight page context so the generic AOI route is obviously bounded to one thinker

2. `webapp/src/pages/AnalysisWorkspacePage.test.tsx`
3. `webapp/src/pages/AnalysisWorkspacePage.integration.test.tsx`

Add targeted tests for:

- query-param parsing
- AOI launch request body composition
- thinker-scoped upstream discovery call
- thinker-scoped local saved-result filtering
- auto-restore choosing the correct thinker result

4. One AOI handoff file, preferably:

- `webapp/src/pages/AnxietyOfInfluencePages.tsx`

or, if the handoff should live inside the current v2 panel:

- `webapp/src/components/influence/AoiV2ThematicPanel.tsx`

Add one explicit navigation affordance to the generic route with thinker query params prefilled.

5. Only if import/preview must be included in this tranche:

- `api/server.py`

Patch the local snapshot save/import path so AOI thinker identity is recovered from durable run metadata before saving the fallback cache.

## Bottom Line

The scope is close, but not ready to implement exactly as written.

The correct version is:

- Deliverable D remains a narrow `the-critic` tranche.
- It does not require analyzer-v2 changes for the main proof.
- `AnalysisWorkspacePage` already has the right overall shape because the shared contract underneath it is ready.
- But the page itself still needs explicit AOI thinker-context wiring, thinker-safe saved-result filtering, and a deliberate handoff from the AOI bespoke surface.

If the team tightens the scope that way, Deliverable D is sound.
