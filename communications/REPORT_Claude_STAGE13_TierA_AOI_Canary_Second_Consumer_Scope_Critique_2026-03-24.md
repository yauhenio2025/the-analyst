# Review (Second Pass): Stage 13 Tier A / AOI Canary Second-Consumer Proof Scope

Date: 2026-03-24
Reviewer: Claude Opus 4.6
Pass: Second (post-revision)
Scope Memo: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_scope.md`
Prior Review: First-pass critique from same date (this file, now overwritten)
Evidence consulted: revised memo, draft next-stages roadmap, canonical roadmap, Stage 13 first/second slice completions, Stage 8/9 host-adoption completion, Host Contract v1 JSON artifact, live codebase in analyzer-v2 / aoi-canary / the-critic

---

## Verdict

**Approved.**

The revised memo closes all four gaps from the first review. The scope is now explicit about `project_id`/`workflow_key` as deliverables, honest about implementation size, bounded on discovery UX, and clear about the state-model migration. The two new requirements (result-contract-first live state, no artifact-fallback masking) add genuine implementation discipline without expanding scope.

No further revisions are needed before implementation begins.

---

## Assessment Of Revisions

### Revision 1 (project_id + workflow_key awareness): Fully addressed

Deliverable 0 now states explicitly:
- `project_id` and `workflow_key` as required discovery scope
- env-driven or URL-param-driven configuration (no project-picker UI)
- workflow_key defaults to the AOI proof workflow

"What aoi-canary does not yet have" now lists both gaps. Prerequisite 3 addresses the data-prep dependency (proof data must be project-attached). This is clean.

### Revision 2 (discovery UX scoping): Fully addressed

The memo now specifies auto-select-latest, not browse-and-pick. Discovery metadata goes in the debug panel. Manual job_id remains secondary. This prevents the discovery UX from becoming its own Tier B project.

### Revision 3 (implementation sizing): Fully addressed

Prerequisite 4 now says "3-5 new files, significant refactor of src/App.tsx, new result-contract types and tests, one focused medium-sized implementation session." This is honest.

### Revision 4 (result_refresh exclusion): Fully addressed

Decision 1 now explicitly lists `result_refresh` alongside transient compose and task-launch in the exclusion set.

### New requirement (result-contract-first state model): Sound

This is a valuable addition. "The live state model should become result-contract-first rather than artifact/page-first" prevents the most likely implementation shortcut where the canary continues to treat `presenter/page` as the real path and merely adds a discovery call on the side.

### New requirement (no artifact-fallback masking): Sound

"Tier A should not be able to mask a failed live result-contract path by silently falling back to artifact content" is concrete enough to guide implementation. It means: if discovery finds a result but `result_presentation` returns `presentation: null` (because `restore_available == false`), the canary must show that state honestly rather than swapping in the frozen Neurath fixture.

---

## Stress-Testing The Revised Assumptions

### Test 1: Do the `results` routes actually work with `consumer_key=aoi-canary`?

**Yes.** Verified through the full call chain:

1. `GET /v1/results/by-job/{job_id}/presentation?consumer_key=aoi-canary`
2. → `get_result_presentation(job_id, consumer_key="aoi-canary")`
3. → `build_result_manifest(job_id, consumer_key="aoi-canary")`
4. → `build_presentation_manifest(job_id, consumer_key="aoi-canary")`
5. → `assemble_page(job_id, consumer_key="aoi-canary")`
6. → `_prepare_page_payloads(job_id, consumer_key="aoi-canary")`
7. → `_get_recommendations(job_id, plan_id, workflow_key, consumer_key="aoi-canary")`

The `consumer_key` is threaded all the way through page assembly, view recommendation, and serve-time renderer contract enforcement. The `aoi-canary` consumer definition (registered in `src/consumers/definitions/aoi-canary.json`) is looked up at serve-time to apply the correct renderer allowlist.

The consumer_key gating to `the-critic` exists **only** in `compose_from_intent.py` (lines 450, 487) for transient compose routes, which are explicitly out of Tier A scope. No gate exists on any result-backed route.

### Test 2: Is the proof-data prerequisite solvable?

**Yes.** The `POST /v1/results/by-job/{job_id}/attach-project` endpoint exists in `src/api/routes/results.py:179` and allows attaching a `project_id` to any existing job. If the Neurath proof job doesn't have a project_id, the implementor can attach one via this endpoint before running the discovery proof. This is a one-call data-prep step.

### Test 3: Does the "auto-select-latest" pattern work with the discovery API?

**Yes.** `GET /v1/results/discovery?project_id=X&workflow_key=Y&consumer_key=aoi-canary&limit=1` returns results sorted by `completed_at DESC, created_at DESC`. The first entry is the latest. The response includes `job_id`, `result_state`, `restore_available`, and HATEOAS `links` to manifest and presentation endpoints.

The canary can implement auto-select-latest as:
1. Call discovery with `limit=1`
2. If empty → show "no results found" state
3. If entry has `restore_available == true` → proceed to manifest + presentation
4. If entry has `restore_available == false` → show manifest metadata (result_state, restore_reason) without rendering

This is a clean state machine.

### Test 4: Is the renderer allowlist adequate?

**Yes.** The canary's consumer definition declares:
- Renderers: `accordion`, `card_grid`, `tab`, `raw_json`
- Sub-renderers: `annotated_prose`, `chip_grid`, `mini_card_list`, `rich_description_list`

The Neurath AOI proof surface (verified in `aoi-canary/src/fixtures/neurath-page.json`) uses `tab` at root with `accordion` and `card_grid` children. The serve-time renderer contract enforcement in `renderer_contract_enforcement.py` will filter any views with unsupported renderers before they reach the canary. No mismatch exists.

### Test 5: Does the canary need the full Host Contract v1 model?

**No.** The memo correctly scopes this to a typed result-backed client covering 3 families:

| Family | Route | Required Inputs |
|--------|-------|-----------------|
| `result_discovery` | `GET /v1/results/discovery` | `project_id`, `workflow_key`, `consumer_key` |
| `result_manifest` | `GET /v1/results/by-job/{job_id}` | `job_id`, `consumer_key` |
| `result_presentation` | `GET /v1/results/by-job/{job_id}/presentation` | `job_id`, `consumer_key` |

The-critic's 11-family Host Contract v1 includes 8 additional families (run_discovery, run_detail, result_refresh, single_view_fetch, source_backed_readiness, cache_snapshot_warmup, source_backed_transient_launch, transient_compose_from_intent) that are all correctly deferred.

### Test 6: Is there hidden the-critic coupling in any dependency?

**No.** The only the-critic structural coupling in analyzer-v2 is:
- `TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"` in `compose_from_intent.py` — out of scope
- `DEFAULT_CONSUMER_KEY = "the-critic"` in `result_contract.py` — a default only; overridden by query param

Neither blocks the canary's result-backed proof path.

### Test 7: Is the "no artifact-fallback masking" rule implementable?

**Yes.** The canary currently has two modes: `artifact` and `live`. The revision requires that in live/discovery mode, a failed result-contract path (e.g., `restore_available == false`, or network error on result_presentation) must surface as an explicit error or intermediate state, not silently fall back to the Neurath fixture.

Implementation is straightforward: the live state machine should carry a `discoveryState` with variants like `discovering`, `discovered_ready`, `discovered_not_restorable`, `error`. The artifact mode remains available as a separate explicit toggle, not as a silent fallback.

---

## Remaining Observations (Informational, Not Blocking)

### Observation 1: The `selected_source_thinker_id` filter is available but likely unnecessary for Tier A

Discovery supports `selected_source_thinker_id` as an optional filter. The Neurath proof surface is already thinker-scoped. If the configured project has only AOI results for one thinker, this filter is unnecessary. If multiple thinkers exist, the auto-select-latest pattern will pick the most recent regardless of thinker.

The memo correctly says "optional thinker filter only if the pinned AOI proof surface actually needs it." This is the right call — leave it out until evidence demands it.

### Observation 2: The `attach-project` endpoint is the cheapest data-prep path

The implementor should know that `POST /v1/results/by-job/{job_id}/attach-project` exists (idempotent, 409 on conflict). This is the one-call fix if the Neurath proof job lacks a `project_id`. The memo's prerequisite 3 covers this conceptually but doesn't name the endpoint. The implementor will find it.

### Observation 3: The discovery `DiscoverySummary` shape is slightly different from `AnalysisResultManifest`

Discovery returns `DiscoverySummary` (lightweight, no artifact detail, no composition_mode), while `/by-job/{job_id}` returns `AnalysisResultManifest` (full artifact families, staleness reasons, etc.). The canary's typed client will need both types. The memo says "new result-contract types" which covers this implicitly.

---

## Judgment: Right First Tranche

Confirmed. The reasoning from the first review stands, and the revisions make it stronger:

1. **aoi-canary already exists** — marginal cost is lower than any alternative proof path.
2. **Result-backed routes are genuinely consumer-neutral** — no hidden the-critic gate.
3. **The state-model migration is scoped honestly** — the memo calls it what it is (medium-sized refactor) and draws a clear boundary (no browsing UI, no refresh, no transient).
4. **The strategic payoff is real** — this is the cheapest way to close the credibility gap before Tier B.
5. **The "no masking" rule prevents implementation shortcuts** — the proof must be honest.

---

## Summary

The revised scope memo is ready for implementation. The bounded claim (second consumer over analyzer-owned result-backed contracts) is achievable, the prerequisites are enumerated, the UX is scoped, the implementation size is honest, and the exclusions are well-drawn. The two new requirements (result-contract-first state model, no artifact-fallback masking) add discipline without expanding scope.
