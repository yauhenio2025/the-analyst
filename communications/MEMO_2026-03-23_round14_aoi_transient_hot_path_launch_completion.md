# Memo: Round 14 / AOI Transient Hot-Path Launch Completion

Date: 2026-03-23
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md`

## Result

Round 14 implementation is complete.

This memo closes the code and focused verification record for the round-14 AOI hot-path launch seam.

It does **not** claim final live documentary closure yet.

The remaining operational proof step is still:

- launch `Compose dossier` from the real AOI thinker page in a live browser session
- launch `Compose comparison` from the real AOI thinker page in a live browser session
- save the navigated transient URLs, response JSONs, screenshots, and text snapshots
- write the round-14 proof note

So the honest status is:

- code-complete
- focused tests complete
- live hot-path proof artifacts still pending

If round 14 later captures that browser evidence, that proof note may also explicitly subsume the still-pending round-13 browser seam.

## Bounded Claim Landed In Code

Round 14 set out to prove one bounded thing:

- a real AOI user can launch the existing source-backed transient compose experience directly from the actual AOI hot path for the current thinker/project, using a concrete saved-result context when available, without embedding transient rendering into the job-backed workspace and without making the transient path the default AOI experience

That bounded seam is now implemented.

## What Landed

### the-critic AOI panel

`AoiV2ThematicPanel` now owns a real transient launch seam.

It now:

- keeps an explicit `currentSourceResult` instead of inferring source identity from whichever row loaded first
- sorts merged saved AOI results deterministically before display and before auto-load fallback
- uses `source_analysis_id` as the normal product handoff identity
- warms a local snapshot through the existing `cache-v2` endpoint when the chosen saved result lacks `analysis_id`
- patches the warmed `analysis_id` back into both the saved-results row and the current source before navigation
- launches into the existing transient route with:
  - `profile`
  - `source_analysis_id`
  - `autostart=1`
  - `origin=aoi_v2_thematic`
  - `return_to`
- fails closed on snapshot warmup failure instead of silently widening into `source_v2_job_id` product semantics

### the-critic transient page

`AoiComposeFromIntentPage` now supports honest hot-path landing behavior.

It now:

- autostarts source-backed compose exactly once per launch signature
- remains stable under React StrictMode double-invocation
- does not require a second dossier/comparison click after navigation from the AOI panel
- validates `return_to` before using it and falls back to the reconstructed AOI route when invalid
- exposes an explicit `Back to AOI` control through client-side routing rather than raw document navigation
- preserves the existing manual source-backed controls and developer fixture fallback for non-hot-path usage

### Round-14 review hardening

Three post-implementation review findings were fixed before this memo:

1. system-error retry now reuses the last failed source-backed profile instead of always retrying `dossier`
2. clearing a loaded AOI presentation now also clears stale hidden `currentSourceResult` state before the next transient launch
3. the `Back to AOI` control now uses client-side routing

## What Round 14 Did Not Change

Round 14 intentionally did **not** change:

- analyzer-v2 compose orchestration
- the-critic source-backed proxy/backend route
- `ViewRenderer`
- `V2TabContent`
- `AnalysisWorkspacePage`
- draft persistence
- transient/job-backed lifecycle unification

The transient runtime remains a separate route and shell.

## Verification

Focused frontend verification completed:

- `cd /home/evgeny/projects/the-critic/webapp && npx tsc --noEmit --pretty false --incremental false`
  - result: clean
- `cd /home/evgeny/projects/the-critic/webapp && CI=true npm test -- --watch=false src/components/influence/AoiV2ThematicPanel.test.tsx src/pages/AoiComposeFromIntentPage.test.tsx src/routes.test.ts src/transientComposeIsolation.test.ts src/components/ViewRenderer.test.tsx`
  - result: `5 passed`
  - result: `32 tests passed`

The focused Jest slice now covers:

- deterministic AOI saved-result sorting
- explicit current-source handling
- bounded hot-path query construction
- normal-path exclusion of `source_v2_job_id`
- snapshot warmup success and failure
- autostart exactly-once behavior
- invalid `return_to` fallback
- retry behavior for the last failed source-backed profile
- stale source clearing on `Clear`
- route wiring
- transient isolation guard
- unchanged transient `ViewRenderer` compatibility

## Residual Testing Note

One narrow testing caveat remains recorded:

- the AOI panel test suite still emits React `act(...)` warnings during async hydration of the saved-results load path
- the suite passes, and the warnings do not indicate a product regression in the round-14 seam itself

That is test-harness noise, not an open round-14 architecture gap.

## What Round 14 Now Proves

Round 14 now proves in code:

1. the transient source-backed path is no longer only reachable through proof-host deep-link ceremony
2. the real AOI panel can hand off into the transient source-backed path with one click
3. the product launch identity remains `source_analysis_id`, not raw `source_v2_job_id`
4. upstream-only saved results can be bridged honestly through bounded local snapshot warmup
5. the transient route can autostart from the AOI hot path without being embedded into the job-backed workspace
6. hot-path adoption did not require widening analyzer-v2 or thickening the consumer renderer stack

## What Round 14 Did Not Yet Close

This memo does **not** yet close:

1. live browser dossier launch from the real AOI thinker page
2. live browser comparison launch from the real AOI thinker page
3. saved round-14 navigated URL, response JSON, screenshot, and text-snapshot artifacts
4. a round-14 proof note that records whether the round-14 browser proof also subsumes the pending round-13 browser seam

Those are documentary closure tasks, not remaining code gaps.

## Program Position After Round 14

The transient program has crossed another important boundary:

- transient compose is no longer only backend-real
- no longer only consumer-renderable
- no longer only source-backed
- it is now product-reachable from the real AOI hot path

The next program question is therefore not:

- can the AOI user reach transient compose at all?

It is closer to:

- how far should transient composition be allowed to move from sidecar launch into mainstream AOI flow before draft persistence and lifecycle law need to be confronted directly?
