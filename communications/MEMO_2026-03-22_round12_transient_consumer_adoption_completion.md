# Memo: Round 12 / Transient Consumer Adoption Completion

Date: 2026-03-22
Program: Thin Consumer Platformization

## Result

Round 12 is complete.

This is the final round-12 completion note after the earlier documentary gap was closed with:

- both dossier and comparison browser proof runs
- shell-focused screenshots and text snapshots
- browser-origin request / response JSON artifacts

The bounded claim closed:

- the-critic now has one dedicated AOI transient proof host
- it consumes the round-11 transient presenter contract through a separate frontend type boundary
- it adapts transient views locally into `ComposedView + data`
- it renders them through the existing generic `ViewRenderer` path
- it does all of that without widening the job-backed workspace shell

## What Landed

In the-critic:

- dedicated transient frontend contract
- dedicated typed compose-from-intent client
- repo-tracked dossier / comparison example payloads
- shell-local transient adapter
- dedicated `AoiComposeFromIntentShell`
- dedicated `AoiComposeFromIntentPage`
- literal AOI transient proof-host route
- focused tests for client, adapter, shell, page, route wiring, and isolation boundaries

No analyzer-v2 runtime changes were required for round 12.

## Verification

Closed evidence:

- frontend typecheck clean
- focused Jest slice:
  - 7 suites passed
  - 28 tests passed
- source-backed analyzer transport gate closed on `127.0.0.1:8010`
- browser dossier and comparison proof runs both succeeded on the dedicated route

Saved evidence:

- proof note:
  - `communications/PROOF_2026-03-22_round12_transient_consumer_adoption.md`
- browser artifacts:
  - `/home/evgeny/projects/the-critic/test-screenshots/round12-transient/round12-compose-dossier-shell.png`
  - `/home/evgeny/projects/the-critic/test-screenshots/round12-transient/round12-compose-dossier-shell.txt`
  - `/home/evgeny/projects/the-critic/test-screenshots/round12-transient/round12-compose-comparison-shell.png`
  - `/home/evgeny/projects/the-critic/test-screenshots/round12-transient/round12-compose-comparison-shell.txt`
- browser-origin transient request / response JSONs:
  - `communications/PROOF_round12_dossier_request_2026-03-22.json`
  - `communications/PROOF_round12_dossier_response_2026-03-22.json`
  - `communications/PROOF_round12_comparison_request_2026-03-22.json`
  - `communications/PROOF_round12_comparison_response_2026-03-22.json`

## Important implementation notes

Three details mattered in practice:

1. the local analyzer process already running on `127.0.0.1:8002` was stale and did not expose the round-11 route
2. the transport gate therefore had to be rechecked against a source-backed analyzer instance
3. the dedicated route rendered successfully even with design-token fetch fallback warnings; token fallback did not block the transient page
4. the final browser proof needed shell-focused screenshots plus saved request / response bodies, not just a form-level page capture, to close the round honestly

One narrow testing caveat remains recorded:

- `src/routes.test.ts` is a route-table wiring guard, not a full router-resolution test
- the actual browser proof run is what closed the route-behavior question

## Program meaning

This round moved compose-from-intent from a backend-only proof into a real consumer surface.

The important boundary remains intact:

- analyzer-v2 is the orchestration brain
- the-critic is a thin transient shell
- the old job/result workspace was not stretched to pretend transient pages were ordinary `PagePresentation`s

That is the right platform direction.
