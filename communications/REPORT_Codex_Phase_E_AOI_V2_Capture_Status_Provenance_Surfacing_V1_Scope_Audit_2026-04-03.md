# Report: Phase E AOI V2 Capture Status/Provenance Surfacing V1 Scope Audit

Date: 2026-04-03

## Verdict

`approve with corrections`

The memo is pointing at the right immediate next slice.
After the write-side provenance closeout, the next real missing proof is read-side surfacing of that persisted truth back onto the same AOI `aoi_by_sin_type` surface.

The corrections are about precision and scope honesty:

- the current shared seam is not only genealogy-job keyed and section-level; AOI analysis captures persist with `genealogy_job_id = null`, so `/api/captures/by-job/{job_id}` cannot match them at all
- the existing shared seam also does not scope by project and does not return `entity_id` or `source_workflow_key`
- a separate AOI-compatible lookup seam is therefore not just cleaner, but materially smaller and more honest than widening `/api/captures/by-job/{job_id}`
- the reusable substrate value is real but modest; this slice proves analyzer-identity read-back on one bounded surface, not generic capture-status law

Focused verification during this audit also passed:

- `pytest -q tests/test_capture_provenance.py` -> `6 passed`
- `CI=1 npm test -- --runInBand --runTestsByPath src/components/renderers/AoiSinFindingsRenderer.test.tsx src/components/V2TabContent.test.tsx src/components/ResearchFlagDialog.test.tsx` -> `14 passed`

## The Memo's Strongest Code-Backed Points

### 1. `aoi_by_sin_type` is still the right first read-side proof surface

This is the strongest strategic point, and it is code-backed across both repos.

- Analyzer-side stable finding identity is already present on this surface. `src/aoi/contract.py:333-356` generates stable `finding_id`, and `src/aoi/contract.py:676-695` carries it into `aoi_by_sin_type`.
- Analyzer tests prove that `finding_id` is stable and survives onto both AOI findings surfaces. See `tests/test_aoi_contract.py:291-332`.
- Analyzer-side first-hop specialization is still only explicitly upgraded on `aoi_by_sin_type` when handles are complete. See `src/presenter/first_hop_affordance.py:77-123` and `tests/test_presentation_api.py:1355-1394`.
- Critic already has the live bounded capture-selection proof on that exact line. `webapp/src/components/renderers/AoiSinFindingsRenderer.tsx:153-170` emits a `CaptureSelection` with `entity_id` and `source_workflow_key`.

So the memo is right that the next slice should stay on the same bounded line rather than broadening to `aoi_by_theme` or another consumer first.

### 2. The current shared read seam is still genealogy-job keyed and section-level

This is not just directionally true. The code makes it explicit.

- `webapp/src/hooks/useCaptureStatus.ts:24-45` fetches only `GET /api/captures/by-job/{job_id}` and builds a map keyed by `source_view_key::source_section_key`.
- The current generic consumer is section-level only. `webapp/node_modules/@the-syllabus/analysis-renderers/src/renderers/AccordionRenderer.tsx:346-360` reads that map using `statusKey = "${captureViewKey}::${section.key}"`.
- The backend route itself is still keyed only by `GenealogyCaptureDB.genealogy_job_id == job_id`. See `api/server.py:22936-22969`.
- The response model does not carry card identity. `api/server.py:1327-1339` returns only `capture_id`, `source_section_key`, `source_view_key`, `destination`, `research_status`, and `has_answer`.

That means the memo is correct that the current shared seam cannot honestly surface card-level AOI truth on `aoi_by_sin_type`.

### 3. The current AOI capture path persists the exact truth the memo wants to read back

The read-side slice is now justified because the write-side data is actually there.

- Capture creation persists `entity_id` and `source_workflow_key`. See `api/server.py:22645-22676` and `api/models_db.py:2677-2688`.
- Routed Arsenal and routed research-todo snapshots now carry those same fields. See `api/server.py:22758-22771` and `api/server.py:22900-22908`.
- Direct research-todo creation normalizes client snapshot provenance from the linked capture record. See `api/server.py:22631-22642` and `api/server.py:23050-23090`.
- Focused tests lock that down. See `tests/test_capture_provenance.py:115-139`, `tests/test_capture_provenance.py:142-209`, `tests/test_capture_provenance.py:212-290`.

So the memo is right that the missing proof is now read-side visibility, not another write-side correction.

### 4. Keeping the existing genealogy status seam untouched in v1 is correct

This is not just conservative. It avoids corrupting a working contract with different semantics.

- `useCaptureStatus` and the packaged `AccordionRenderer` already form a coherent section-status behavior on accordion surfaces. See `webapp/src/hooks/useCaptureStatus.ts:24-45` and `webapp/node_modules/@the-syllabus/analysis-renderers/src/renderers/AccordionRenderer.tsx:346-360`.
- That behavior is keyed by section and does not need analyzer item identity.
- AOI `aoi_by_sin_type` is card-level and item-identity-backed.

Those are different seams. The memo is right not to pretend one shared route already solves both.

### 5. Passive per-card truth and reload/revisit proof are the right v1 boundary

This is the smallest honest browser/UI claim.

- The current renderer is passive by default and only adds a capture button when capture mode is active and specialization guards pass. See `webapp/src/components/renderers/AoiSinFindingsRenderer.tsx:80-105` and `webapp/src/components/renderers/AoiSinFindingsRenderer.tsx:143-185`.
- Current section-status UI is also passive-only; it renders dots, not mutation rules. See `webapp/node_modules/@the-syllabus/analysis-renderers/src/renderers/AccordionRenderer.tsx:346-360`.
- Same-session status refresh is clearly not already solved. `webapp/src/hooks/useCaptureStatus.ts:28-45` fetches once per `jobId` and then suppresses refetches through `fetchedRef`.

So the memo is right to require reload/revisit truth and to defer optimistic in-session invalidation.

### 6. The memo is honest to defer older rows to silent non-match behavior

This is supported by both schema and tests.

- The provenance columns are nullable on `GenealogyCaptureDB`. See `api/models_db.py:2687-2688`.
- The migration added them as nullable without backfill. See `api/alembic/versions/032_add_capture_provenance_fields.py:18-26`.
- Tests explicitly assert fallback behavior for null provenance rows. See `tests/test_capture_provenance.py:293-335`.

So a truthful v1 should not claim universal historical coverage.

## The Memo's Weakest Or Overstated Assumptions

### 1. The memo should describe the current shared seam as completely non-AOI-compatible, not just imperfect

This is the biggest correction.

For AOI analysis captures, `genealogy_job_id` is intentionally not populated:

- `webapp/src/contexts/CaptureContext.tsx:96-101` only derives `genealogy_job_id` from `entity_id` when `source_type === 'genealogy'`
- `webapp/src/components/ResearchFlagDialog.tsx:109-114` uses the same rule

So for AOI `source_type = "analysis"`, the current `/api/captures/by-job/{job_id}` route is not merely coarse.
It misses those captures entirely, because its only filter is `GenealogyCaptureDB.genealogy_job_id == job_id`.

The memo should say that more strongly.

### 2. The memo slightly overstates how close `/api/captures/by-job/{job_id}` is to being widenable

Widening that route would not be a small tweak.

Today the route:

- is named and shaped around `job_id`
- filters only on `genealogy_job_id`
- returns no `entity_id`
- returns no `source_workflow_key`
- feeds a packaged section-status consumer that only understands `view::section`

That means widening it for AOI card truth would require:

- a different filter model
- a different response contract
- a different frontend grouping model
- a route name whose path parameter no longer describes the lookup honestly

So the memo's recommendation is right, but the justification should be stronger: the existing route is the wrong contract, not merely a slightly narrow one.

### 3. The memo should describe reusable substrate value more modestly

The new lookup seam would teach one real reusable rule:

- analyzer-backed item surfaces should read capture truth by analyzer-owned identity, not by legacy genealogy-job assumptions

That is worth doing.
But it is still not generic capture-status law for:

- section-level surfaces
- mixed surfaces like `aoi_by_theme`
- non-AOI consumers
- workflow-neutral destination semantics

So the memo should frame this as one bounded analyzer-identity read seam, not a generalized capture substrate closeout.

### 4. The memo should name the existing packaged generic consumer explicitly

The current shared section-status behavior does not live in the AOI renderer at all.
It lives in `@the-syllabus/analysis-renderers`:

- `webapp/node_modules/@the-syllabus/analysis-renderers/src/renderers/AccordionRenderer.tsx:346-360`

That matters because it strengthens the memo's deferral:

- do not widen generic renderer-package capture-status behavior in v1

The current section-dot behavior is already shared package behavior.
AOI card truth should stay local in v1.

### 5. Passive per-card surfacing must avoid accidental dedup policy claims

The memo is right to defer deduplication rules, but the implementation shape needs one extra sentence of honesty:

- the backend should return raw matching capture rows
- the UI should derive passive state from "any matching row exists"
- the UI should not imply repeat-capture blocking or one-row-per-destination law

That matters because nothing in the current schema prevents multiple captures against the same `entity_id`.

## Factual Discrepancies I Found

### 1. `/api/captures/by-job/{job_id}` is not project-scoped

The route takes no `Request` and does not filter by `project_id`.
See `api/server.py:22936-22969`.

The memo correctly says new AOI lookup truth should come from the existing project header, but it understates this contrast with the current seam.

### 2. The current shared read seam cannot match AOI analysis captures at all

This is stronger than the memo's phrasing.

- AOI analysis capture creation persists `genealogy_job_id = null` by design unless the source is genealogy. See `webapp/src/contexts/CaptureContext.tsx:96-114` and `webapp/src/components/ResearchFlagDialog.tsx:109-127`.
- The only shared lookup filter is `GenealogyCaptureDB.genealogy_job_id == job_id`. See `api/server.py:22943-22954`.

So AOI read-back is not just missing card granularity; it is completely absent from the current route.

### 3. The current status response contract does not carry the fields AOI card truth would need

Even if the lookup predicate were broadened, the response still omits:

- `entity_id`
- `source_workflow_key`

See `api/server.py:1327-1339`.

So a truthful AOI read seam would still require a new response model or an additive new route.

### 4. The current generic status consumer is the shared Accordion renderer, not the AOI renderer

The memo talks mostly in Critic-local terms, but the actual current section-status surface is:

- `webapp/node_modules/@the-syllabus/analysis-renderers/src/renderers/AccordionRenderer.tsx:346-360`

That strengthens, rather than weakens, the memo's decision to keep generic renderer-package behavior deferred in v1.

## What This Changes For The Larger Roadmap

This memo still points at the right immediate Phase E move.

It fits the roadmap because it varies the next unresolved variable honestly:

- the analyzer contract already emits stable AOI card identity and workflow-type truth
- one live host already consumes that contract at selection time
- the Critic capture pipeline already persists that truth
- the remaining gap is whether a thin host can read persisted analyzer-owned truth back without reconstructing it from local heuristics

That is good Phase E work because it teaches a real thin-host rule:

- read-side surfacing for analyzer-backed item captures should be keyed by analyzer-owned identity, not by host-local section/job assumptions

But the roadmap implication should stay calibrated.
If this slice lands, it does not mean:

- generic capture-status law is solved
- mixed-surface AOI read behavior is solved
- non-AOI read-side consumers are solved
- workflow-neutral destination semantics are solved

It means one bounded read-back loop on one analyzer-known item surface is finally closed.

The strategic consequence after that should be:

- more AOI-only capture/UI work needs stronger justification
- the next good move should either generalize the analyzer-identity lookup principle beyond `aoi_by_sin_type` or return to broader host-neutral generality work

## The Most Defensible Next Move After This Memo

Implement one bounded Critic-only AOI-compatible read seam and keep the current genealogy seam untouched.

The most defensible v1 shape is:

- request keyed by project header plus:
  - `source_workflow_key`
  - `source_view_key`
  - `entity_id[]`
- response returning raw matching capture rows, at minimum:
  - `capture_id`
  - `entity_id`
  - `destination`
  - `research_status`
  - `has_answer`
- optional echoed provenance fields:
  - `source_workflow_key`
  - `source_view_key`
- frontend usage local to AOI `aoi_by_sin_type` only
- passive per-card truth derived by matching `finding_id`
- browser proof boundary:
  - reload
  - revisit
  - fresh fetch
  - not same-session optimistic invalidation

The implementation should explicitly not do these things in v1:

- widen `/api/captures/by-job/{job_id}`
- change `useCaptureStatus.ts`
- change packaged `AccordionRenderer` behavior
- broaden to `aoi_by_theme`
- add deep links
- add recapture blocking
- add dedup policy

With those corrections, the memo is ready.
