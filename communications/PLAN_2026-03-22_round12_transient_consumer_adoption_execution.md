# Execution Plan: Round 12 / AOI Transient Consumer Adoption

Date: 2026-03-22
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-22_round12_transient_consumer_adoption_scope.md`

## Summary

Execute round 12 as a bounded, additive the-critic frontend tranche.

Public proof host:

- `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker/compose-from-intent`

Bounded claim:

- the-critic can call the existing analyzer-v2 `POST /v1/presenter/compose-from-intent` route
- the returned transient contract is consumed through a separate frontend transient type boundary
- the shell locally adapts each transient view into `ComposedView + data` for `ViewRenderer`
- `ViewRenderer` itself remains unchanged at runtime
- no job/result/workspace law is widened or reused
- the existing AOI v2 hot-path cutover work remains untouched in substance

Round-12 boundary:

- AOI only
- `consumer_key = the-critic`
- flat top-level transient views only
- blocking POST with simple loading state only
- proof inputs come from the saved round-11 dossier/comparison request payloads

No planned analyzer-v2 runtime changes:

- round 12 should be executable as a consumer-only tranche on top of the already-landed round-11 route
- if implementation reveals a backend defect, treat that as a bugfix exception and stop for an addendum rather than silently widening the round

Hard stop conditions:

- if the plan starts widening frontend `PagePresentation` or `ViewPayload`, stop
- if the plan starts modifying `AnalysisWorkspacePage`, `V2TabContent`, `useBoundedV2Workspace`, or `boundedV2Client` for transient support, stop
- if `ViewRenderer` requires runtime changes to support transient rendering, stop
- if the proof host begins altering the AOI thinker-page hot path or its tab order, stop
- if blocking POST pressure causes streaming, polling, or background-job conversion work to enter scope, stop

## Current Starting Point

### Already in analyzer-v2

The round-11 backend seam already exists:

- `POST /v1/presenter/compose-from-intent`
- request model:
  - `ComposeFromIntentRequest`
  - `ComposeFromIntentSectionInput`
- response model:
  - `TransientIntentPagePresentation`
  - `TransientIntentView`
  - `ComposeFromIntentTrace`
  - `ComposeFromIntentResponse`

The route already preserves the required error distinctions:

- `400`
- `409`
- `502`
- `503`

The route already returns a non-job-backed page contract:

- no `job_id`
- no `plan_id`
- no `prepared_at`
- no `raw_prose`

The round-11 documentary proof inputs already exist:

- `communications/PROOF_round11_dossier_request_2026-03-22.json`
- `communications/PROOF_round11_comparison_request_2026-03-22.json`

### Already in the-critic

The leaf renderer seam is already good enough:

- `ViewRenderer` accepts `jobId?: string`
- no runtime `jobId` is required for normal rendering
- there are no AOI-specific renderer overrides in the remaining renderer override tables

The current job-backed stack is explicitly not reusable for transient work:

- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`

The active AOI hot-path workstream must remain protected:

- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx`

## Execution Strategy

Execute round 12 as a literal proof host, not as a generic transient platformization of the-critic.

That means:

1. add one dedicated literal route for the AOI transient proof host
2. add one dedicated transient frontend contract in the-critic
3. add one dedicated transient client that preserves HTTP status distinctions
4. add one shell-local adapter that builds `ComposedView + data` for `ViewRenderer`
5. keep the rendered page flat and ordered
6. keep the request source pinned to repo-tracked copies of the round-11 proof payloads
7. keep the AOI hot-path cutover code path isolated from all runtime changes

The plan deliberately does **not**:

- generalize `:workflowKey` transient routing
- retrofit the job-backed workspace
- add a result browser for old jobs
- add persistence, promotion, or restore
- add live progress instrumentation

## Work Packages

### WP0: Freeze Protected Boundaries Before Coding

Goal:

- make the non-widening rules concrete before any implementation work starts

Protected runtime files for round 12:

- `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx`

Allowed changes in protected areas:

- route table entry in `routes.tsx`
- test updates that prove `ViewRenderer` remains transient-safe

Decisions frozen in WP0:

- use a literal dedicated route path, not a `:workflowKey`-guarded generic transient route
- ship repo-tracked frontend copies of the two round-11 proof requests
- do not add any navigation entrypoint from the thinker-page hot path in round 12
- do not add analyzer-v2 runtime changes unless a concrete bug blocks consumption of the already-documented route contract

### WP1: Add Dedicated Transient Frontend Types, Client, and Proof Fixtures

Goal:

- give the-critic its own transient boundary rather than leaking the round-11 response into job/result types

New files:

- `/home/evgeny/projects/the-critic/webapp/src/types/transientCompose.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentExamples.ts`

Scope:

1. `transientCompose.ts`
   - mirror the analyzer-v2 round-11 transient response types:
     - `TransientComposeRequest`
     - `TransientComposeSectionInput`
     - `TransientComposeView`
     - `TransientComposePresentation`
     - `TransientComposeTraceEntry`
     - `TransientComposeResponse`
   - define a dedicated transient error type:
     - `TransientComposeError`
     - fields:
       - `status`
       - `detail`
       - `label`

2. `composeFromIntentClient.ts`
   - add one direct analyzer-v2 client function:
     - `composeFromIntent(request): Promise<TransientComposeResponse>`
   - use direct `fetch` to `ANALYZER_V2_URL`
   - preserve `400 / 409 / 502 / 503` distinctly
   - do not flatten all failures into generic `Error`
   - recommended status labels:
     - `400` -> `input_error`
     - `409` -> `contract_error`
     - `502` -> `upstream_error`
     - `503` -> `dependency_unavailable`

3. `composeFromIntentExamples.ts`
   - copy the exact request payload content from:
     - `communications/PROOF_round11_dossier_request_2026-03-22.json`
     - `communications/PROOF_round11_comparison_request_2026-03-22.json`
   - export them as repo-tracked frontend constants
   - do not load those JSON files dynamically at runtime
   - do not build a browser for old jobs/results

Important implementation rule:

- this work package owns the transient status semantics for the frontend
- nothing here may depend on `BoundedV2Job`, `V2ResultManifest`, or `PagePresentation`

### WP2: Add the Shell-Local Adapter and Flat Rendering Shell

Goal:

- map the transient backend response into the minimal rendering inputs needed by `ViewRenderer`

New files:

- `/home/evgeny/projects/the-critic/webapp/src/lib/transientComposeAdapters.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx`

Adapter decisions:

1. add a shell-local adapter:
   - `toTransientComposedView(view: TransientComposeView): ComposedView`
   - `toTransientRendererData(view: TransientComposeView): unknown`

2. `toTransientComposedView(...)` should map:
   - `view_key`
   - `view_name`
   - `description`
   - `renderer_type`
   - `renderer_config`
   - `presentation_stance`
   - `position`
   - `visibility`

3. shell-owned default fields for `ComposedView`:
   - `data_source = { result_path: '', scope: 'aggregated' }`
   - `secondary_sources = []`
   - `transformation = { type: 'none' }`
   - `tab_count_field = null`
   - `audience_overrides = {}`
   - `children = []`

4. `toTransientRendererData(...)` should map:
   - if `items` exists and is non-empty: use `items`
   - else use `structured_data`
   - else `null`

5. do **not** invent:
   - `job_id`
   - `plan_id`
   - `priority`
   - `data_quality`
   - `scope`
   - `raw_prose`
   - `phase_number`
   - `chain_key`

Shell behavior:

- render `presentation.views` in sorted order by `position`
- call `ViewRenderer` directly with:
  - adapted `ComposedView`
  - adapted `data`
  - no `jobId`
- wrap results in `DesignTokenProvider` using returned `presentation.style_school`
- keep trace rendering local and minimal:
  - use a simple inline diagnostics panel or `<details>` block
  - show `resolver_version`
  - show trace stages only after success

Unexpected-children rule:

- v1 is flat by contract
- if a transient response unexpectedly contains `children`, do not build tabs
- show a small diagnostic note and continue rendering only top-level views

### WP3: Add the Dedicated AOI Proof Host Page and Literal Route

Goal:

- host the transient shell on an isolated frontend route without altering the AOI hot path

New files:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- optional:
  - `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.css`

Files to modify:

- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`

Route decision:

- add a literal route:
  - `analysis/anxiety_of_influence_thematic_single_thinker/compose-from-intent`
- keep the generic route:
  - `analysis/:workflowKey`
- place the literal route explicitly near the generic analysis workspace entry so the proof host remains visible in the route table

Page responsibilities:

1. local request state
   - selected example: dossier vs comparison
   - editable `user_intent`
   - editable `prose_sections`
   - optional `style_school`

2. local request lifecycle
   - `idle`
   - `loading`
   - `success`
   - `error`

3. blocking POST UX only
   - one submit button
   - one loading state
   - no streaming
   - no polling
   - no staged live progress

4. minimum status-to-UX mapping
   - `400`:
     - inline user-correctable input error
     - keep current form state intact
   - `502` / `503`:
     - system error panel
     - retry affordance
   - `409`:
     - diagnostic error panel
     - render returned validation details in readable form

5. output rendering
   - on success, pass the response into `AoiComposeFromIntentShell`
   - render a small metadata header:
     - workflow key
     - returned style school
     - view count
     - resolver version

Explicit exclusions:

- no `CaptureProvider`
- no `ProvenanceProvider`
- no `PresentationSummaryCard`
- no `PipelineVisualization`
- no refresh button
- no export link
- no saved-result list
- no result restore

Hot-path protection rule:

- do not add a new thinker-page tab
- do not alter `AoiV2ThematicPanel`
- do not change current AOI V2 defaulting behavior
- route-level access is sufficient for round-12 closure

### WP4: Add Focused the-critic Test Coverage

Goal:

- prove the transient path works without changing the job-backed rendering law

New test files:

- `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.test.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/transientComposeAdapters.test.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.test.tsx`

Existing tests to extend:

- `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.test.tsx`

Required tests:

1. client tests
   - success path parses transient response
   - `400` maps to `TransientComposeError.status = 400`
   - `409` maps to `TransientComposeError.status = 409`
   - `502` maps to `TransientComposeError.status = 502`
   - `503` maps to `TransientComposeError.status = 503`

2. adapter tests
   - prose transient view becomes a `ComposedView` plus string `data`
   - card-grid transient view preserves renderer config and structured array/group data
   - no adapter path invents `job_id` or `plan_id`

3. shell tests
   - renders a flat ordered list of transient views
   - calls `ViewRenderer` without `jobId`
   - shows trace metadata locally
   - does not render tabs or child navigation

4. page tests
   - loads dossier example into the form
   - loads comparison example into the form
   - submit success renders returned transient page
   - `400` shows inline input error
   - `502` / `503` show retry-capable system error
   - `409` shows diagnostic panel
   - loading state is blocking and no polling occurs

5. `ViewRenderer` regression
   - keep or extend the transient-view test proving no runtime changes are needed for transient view rendering

### WP5: Manual Proof Capture and Documentary Closure

Goal:

- produce the proof artifacts required by the round-12 scope memo

Required manual runs:

1. dossier example
   - load repo-tracked dossier fixture
   - submit
   - verify successful render

2. comparison example
   - load repo-tracked comparison fixture
   - submit
   - verify successful render

Required saved artifacts:

- page screenshots for dossier and comparison runs
- page text snapshots for dossier and comparison runs
- the exact request payloads used in the-critic
- returned transient response JSONs
- a short proof memo summarizing outcome and observed status behavior

Recommended artifact naming under `communications/` in this repo:

- `PROOF_round12_dossier_request_<date>.json`
- `PROOF_round12_dossier_response_<date>.json`
- `PROOF_round12_comparison_request_<date>.json`
- `PROOF_round12_comparison_response_<date>.json`
- `PROOF_2026-03-22_round12_transient_consumer_adoption.md`

Recommended screenshot location in the-critic:

- `/home/evgeny/projects/the-critic/test-screenshots/round12-transient/`

## Verification Commands

Frontend typecheck:

```bash
cd /home/evgeny/projects/the-critic/webapp
npx tsc --noEmit --pretty false --incremental false
```

Focused frontend regression:

```bash
cd /home/evgeny/projects/the-critic/webapp
CI=true npm test -- --watch=false \
  src/lib/composeFromIntentClient.test.ts \
  src/lib/transientComposeAdapters.test.ts \
  src/components/influence/AoiComposeFromIntentShell.test.tsx \
  src/pages/AoiComposeFromIntentPage.test.tsx \
  src/components/ViewRenderer.test.tsx
```

No planned analyzer-v2 verification changes:

- round 12 should not require new analyzer-v2 runtime tests unless a concrete backend bugfix becomes necessary

## Exit Criteria

Round 12 is complete only when all of the following are true:

1. the-critic renders the dossier proof fixture successfully through the dedicated transient host
2. the-critic renders the comparison proof fixture successfully through the dedicated transient host
3. the route uses a separate transient frontend contract, not `PagePresentation`
4. the shell uses a local adapter to `ComposedView + data`, not `ViewPayload`
5. `ViewRenderer` required no runtime code changes
6. no job/result workspace runtime files were widened for transient support
7. the AOI hot-path cutover code path remained additive and non-blocking
8. the saved proof artifacts exist and match the actual proof runs

## Bottom Line

This round should be executed as a narrow the-critic consumer adoption tranche, not a shared-platform rewrite. The shortest honest path is:

- dedicated literal route
- dedicated transient types/client
- shell-local adapter
- unchanged `ViewRenderer`
- hardcoded round-11 proof fixtures
- focused tests and proof capture

Any move toward workspace unification, job-law reuse, or persistence belongs to a later round.
