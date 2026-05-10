# Proof: Round 12 / AOI Transient Consumer Adoption

Date: 2026-03-22
Program: Thin Consumer Platformization

## Claim Closed

Round 12 proved one bounded thing:

- the-critic can call analyzer-v2 `POST /v1/presenter/compose-from-intent`
- consume the transient response through a separate frontend contract
- adapt each returned transient view into `ComposedView + data` locally
- render the AOI transient page through the existing generic `ViewRenderer` path
- without reusing the job-backed workspace shell and without changing `ViewRenderer` at runtime

## Evidence

### Focused frontend verification

Typecheck:

```bash
cd /home/evgeny/projects/the-critic/webapp
npx tsc --noEmit --pretty false --incremental false
```

Result:

- clean

Focused Jest:

```bash
cd /home/evgeny/projects/the-critic/webapp
CI=true npm test -- --watch=false \
  src/lib/composeFromIntentClient.test.ts \
  src/lib/transientComposeAdapters.test.ts \
  src/components/influence/AoiComposeFromIntentShell.test.tsx \
  src/pages/AoiComposeFromIntentPage.test.tsx \
  src/routes.test.ts \
  src/transientComposeIsolation.test.ts \
  src/components/ViewRenderer.test.tsx
```

Result:

- 7 suites passed
- 28 tests passed

What those tests prove:

- typed `400 / 409 / 502 / 503 / 500` client mapping
- correct nested `409` envelope parsing
- shell-local `TransientComposeView -> ComposedView + data` adaptation
- no invented job-law fields
- blocking request UX on the dedicated page
- dedicated transient route wiring present in the route table
- explicit forbidden-import guard against job-backed workspace reuse
- `ViewRenderer` still renders transient view shapes without runtime changes

### Source-backed transport gate

The long blocking browser boundary was checked against a source-backed analyzer instance because the pre-existing process on `127.0.0.1:8002` was serving an older route table and did not expose `/v1/presenter/compose-from-intent`.

Source-backed analyzer run:

```bash
cd /home/evgeny/projects/analyzer-v2
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8010
```

Observed:

- `OPTIONS /v1/presenter/compose-from-intent` returned `200`
- CORS headers allowed the frontend origin
- `POST /v1/presenter/compose-from-intent` returned `200`
- the returned body included a valid transient page payload

This closed the preflight gate that the browser-facing route was actually usable before the consumer shell depended on it.

### Browser proof host runs

Two browser proof runs were executed against the dedicated route:

- frontend dev server: `http://127.0.0.1:3001`
- analyzer: `http://127.0.0.1:8010`
- route:
  - `/p/morozov-benanav-001/analysis/anxiety_of_influence_thematic_single_thinker/compose-from-intent`

Observed for dossier:

- page loaded with the dossier preset pre-populated
- clicking `Compose transient page` completed successfully with `200`
- the transient shell rendered with:
  - `Style School: explanatory_narrative`
  - `View Count: 2`
  - `Resolver Version: compose-from-intent-v1`
- shell-focused screenshot and text snapshot were saved at:
  - `/home/evgeny/projects/the-critic/test-screenshots/round12-transient/round12-compose-dossier-shell.png`
  - `/home/evgeny/projects/the-critic/test-screenshots/round12-transient/round12-compose-dossier-shell.txt`
- exact browser-origin request / response artifacts were saved at:
  - `communications/PROOF_round12_dossier_request_2026-03-22.json`
  - `communications/PROOF_round12_dossier_response_2026-03-22.json`

Observed for comparison:

- switching to `Load comparison example` and submitting completed successfully with `200`
- the transient shell rendered with:
  - `Style School: explanatory_narrative`
  - `View Count: 3`
  - `Resolver Version: compose-from-intent-v1`
- shell-focused screenshot and text snapshot were saved at:
  - `/home/evgeny/projects/the-critic/test-screenshots/round12-transient/round12-compose-comparison-shell.png`
  - `/home/evgeny/projects/the-critic/test-screenshots/round12-transient/round12-compose-comparison-shell.txt`
- exact browser-origin request / response artifacts were saved at:
  - `communications/PROOF_round12_comparison_request_2026-03-22.json`
  - `communications/PROOF_round12_comparison_response_2026-03-22.json`

Runtime note:

- design-token fetch produced network fallback warnings and the page used fallback tokens
- this did not block page rendering

## Boundaries Kept

Round 12 remained additive and did not widen:

- `AnalysisWorkspacePage`
- `V2TabContent`
- `useBoundedV2Workspace`
- `boundedV2Client`
- `AoiV2ThematicPanel`
- thinker-page tab structure
- runtime `ViewRenderer`

The transient page used:

- a dedicated frontend contract
- a dedicated typed transient client
- a shell-local adapter
- a dedicated proof-host route

## Residual Note

The Jest route check in `src/routes.test.ts` is a file-level wiring guard rather than a full React Router resolution test because the local Jest environment could not cleanly import the router package at runtime from `routes.tsx`. The actual browser proof pass on the dedicated route closed the behavioral question directly.
