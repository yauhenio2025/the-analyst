Approve with revisions

# Stage 13 Tier A / AOI Canary Second-Consumer Scope Audit

Audited memo:
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_scope.md`

## Overall Verdict

The memo is directionally right.

It correctly identifies `aoi-canary` as a real but not yet sufficient second-consumer proof target, it picks the right Tier A boundary by staying result-backed and read-only, and it does not pretend Host Contract v1 runtime reuse already exists across apps.

The main problem is scoping precision. The memo still reads a little too much like a small endpoint migration. In live code, this is a small-but-real client/state-model refactor inside `aoi-canary`, plus one discovery prerequisite that the memo does not state explicitly: the canary currently has no source of `project_id`, while `/v1/results/discovery` requires one.

## Concrete Findings

1. High: the memo is honest about `aoi-canary`'s current state.

`aoi-canary` is still a presenter-page canary, not a result-contract consumer.

- Live mode fetches `GET /v1/presenter/page/{job_id}`, `GET /v1/presenter/manifest/{job_id}`, `GET /v1/presenter/trace/{job_id}`, and `GET /v1/presenter/status/{job_id}` inline from `/home/evgeny/projects/aoi-canary/src/App.tsx:67`.
- The current test only proves presenter-route fetches with `consumer_key=aoi-canary`, not result discovery or result presentation: `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:43`.
- The README still describes live mode as presenter fetches: `/home/evgeny/projects/aoi-canary/README.md:18`.
- The app's local types are page/manifest/trace shapes, not result-contract shapes: `/home/evgeny/projects/aoi-canary/src/types/presentation.ts:14`.

The memo is also right that the canary remains a legitimate thin second-consumer candidate rather than a disguised workflow app.

- The consumer definition is bounded and AOI-specific, with a narrow renderer list: `/home/evgeny/projects/analyzer-v2/src/consumers/definitions/aoi-canary.json:2`.
- The renderer host only dispatches by `renderer_type`, passes through payload/config, and exposes unsupported-renderer fallback; it does not reconstruct AOI semantics: `/home/evgeny/projects/aoi-canary/src/components/RendererHost.tsx:10`.
- Analyzer-side contract coverage already verifies the pinned AOI surface fits the canary's supported renderer/sub-renderer set without raw-json fallback: `/home/evgeny/projects/analyzer-v2/tests/test_aoi_canary_contract.py:44`.

2. High: `results`-route adoption is the right Tier A proof seam; staying on presenter routes would be too weak.

The live analyzer now has an explicit server-owned result layer.

- The public result surface is `GET /v1/results/discovery`, `GET /v1/results/by-job/{job_id}`, and `GET /v1/results/by-job/{job_id}/presentation`: `/home/evgeny/projects/analyzer-v2/src/api/routes/results.py:50`.
- The result schema carries `result_state`, `restore_available`, `restore_reason`, `staleness_reasons`, `product_warnings`, and `artifact_families`, which presenter routes do not expose as the primary contract: `/home/evgeny/projects/analyzer-v2/src/analysis_products/schemas.py:41`.
- `get_result_presentation(...)` first builds the manifest contract, then only returns `presentation` when restore/presentation state is actually valid: `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py:382`.
- By contrast, `GET /v1/presenter/page/{job_id}` is still a direct page-assembly endpoint: `/home/evgeny/projects/analyzer-v2/src/api/routes/presenter.py:148`.

So the memo is correct that Tier A should prove discovery plus manifest plus presentation, not only "can the canary still render a page tree."

One nuance should be made explicit: the result contract is a server-owned wrapper over presenter delivery, not a separate renderer runtime. That is visible in the result contract itself.

- Manifest links still point to presenter debug/support seams such as `page_url` and `trace_url`: `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py:221`.

That means the memo's "results primary, presenter trace/status secondary" split is honest and technically aligned with live code.

3. High: the memo correctly avoids pretending Host Contract v1/runtime reuse already exists across apps.

Host Contract v1 is real, but it is still a `the-critic` implementation, not a cross-app shared runtime.

- The first Stage 13 completion memo explicitly says "`the-critic` has one typed Host Contract v1 source of truth": `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_completion.md:16`.
- The second Stage 13 completion memo explicitly says the stronger runtime proof is still current-consumer-only: `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_completion.md:78`.
- The canonical roadmap still records Stage 13 as partial because "second-consumer / host-neutral proof is still open": `/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1178`.
- The same roadmap reiterates the remaining gap directly: "proof is still current-consumer-only and AOI source-backed transient launch remains explicitly host-bounded": `/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1241`.

The code matches that ledger.

- Host Contract v1 and runtime live in `the-critic`, not in analyzer-v2 or a shared package: `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:1` and `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractRuntime.ts:1`.
- Transient families remain structurally bound to `consumer_key='the-critic'` in Host Contract v1: `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:187`.
- Analyzer-side AOI readiness still blocks non-`the-critic` source-backed followup: `/home/evgeny/projects/analyzer-v2/src/analysis_products/source_backed_readiness.py:144`.

So the memo is right to keep Tier A away from transient routes, source-backed readiness, and shared runtime extraction.

4. Medium: the memo understates the practical prerequisites inside `aoi-canary`.

The biggest omitted prerequisite is discovery identity.

- `GET /v1/results/discovery` requires `project_id`: `/home/evgeny/projects/analyzer-v2/src/api/routes/results.py:150`.
- `aoi-canary` currently exposes only analyzer URL, `job_id`, and mode, both in env docs and in the UI: `/home/evgeny/projects/aoi-canary/README.md:23` and `/home/evgeny/projects/aoi-canary/src/App.tsx:207`.

That means discovery-driven live mode is not just "swap to `/v1/results/discovery`." The app needs a bounded source of `project_id` first. The memo mentions project-scoped discovery, but not how the app will obtain that scope.

The second omitted prerequisite is state shape.

- The current app state is centered on `PagePresentation | artifact`, not on `DiscoverySummary -> AnalysisResultManifest -> AnalysisResultPresentationResponse`: `/home/evgeny/projects/aoi-canary/src/App.tsx:23`.
- In live mode, the app renders artifact state whenever a live page is not yet present: `/home/evgeny/projects/aoi-canary/src/App.tsx:135`.

That fallback is fine for a canary, but it is too ambiguous for a proof tranche. A Tier A proof should not be able to show artifact content while the result-backed contract path is still loading or has failed.

The third omitted prerequisite is data discoverability.

- Discovery is project-filtered and only returns completed jobs matching that scope: `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py:478`.
- If proof jobs are imported or otherwise missing `project_id`, the only current recovery path is `POST /v1/results/by-job/{job_id}/attach-project`: `/home/evgeny/projects/analyzer-v2/src/api/routes/results.py:179`.

The memo should say this explicitly so the tranche does not silently depend on hand-curated data state.

## Scope / Sequence Assessment

This is the right first implementation tranche now.

That judgment is stronger after the Stage 8/9 host-adoption completion, not before it.

- The earlier host-adoption scope memo argued that a second-consumer push would be premature while `route-task` and `plan-task` were still unused in the current host: `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_scope.md:109`.
- The completion memo now records that those bounded host-adoption seams have landed in `the-critic`: `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_completion.md:7`.

So the strategic objection that a second consumer would "prove duplication, not maturity" has been materially reduced. The current consumer now does consume bounded analyzer-owned task truth in real seams, which makes a bounded second-consumer result proof a reasonable next strengthening move.

The memo also keeps the Tier A / Tier B boundary basically correct.

- Draft Tier A is result-backed, read-only, and based on discovery/manifest/presentation: `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:136`.
- Draft Tier B is explicitly later, includes transient surfaces, and requires broader planner-to-presentation proof across more than one workflow family: `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:244`.

So this scope is not too narrow if it really proves all three result families. It only becomes too narrow if implementation quietly reduces Tier A to "fetch `/presentation` by known job ID and ignore discovery/manifest semantics."

It is not too broad as written. It only becomes Tier B drift if it starts pulling in any of the following:

- transient compose
- source-backed readiness or source-backed launch
- `route-task` / `plan-task`
- shared-runtime extraction from `the-critic`
- multi-workflow proof expectations

## Missing Assumptions / Hidden Prerequisites

- The memo should state how `aoi-canary` gets `project_id` for discovery. Right now there is no such input.
- The memo should state that proof data must already be discoverable by `project_id`, or else the tranche needs an explicit attach/seed step.
- The memo should state that `aoi-canary` needs result-contract types and a result-oriented state model, not only endpoint rewiring.
- The memo should state that live proof mode must stop silently showing artifact content while the result-backed path is unresolved.
- The memo should state that Tier A closure requires consuming actual manifest semantics, not merely unwrapping `presentation` and discarding the rest of the contract.

## Recommended Revisions Before Implementation

1. Add one explicit prerequisite subsection under "Current State" or "Known Prerequisites" covering:
- required `project_id` source for discovery
- requirement that proof jobs are project-attached and discoverable
- canary state-model migration from page-first to result-contract-first

2. Tighten Decision 2 so it says Tier A closure requires the canary to use:
- `result_discovery` for selection
- `result_manifest` for state and contract truth
- `result_presentation` for rendering

3. Add one sentence saying presenter routes may remain only as debug/support seams because the result contract still links to presenter page/trace internally; they are not the proof seam.

4. Expand deliverable 1 from "small typed result-backed client layer" to "small typed result-backed client and state adapter layer." That matches the real gap more honestly.

5. Expand the test plan to require:
- no artifact fallback masking live result-backed failures
- project/thinker discovery request shaping where applicable
- manifest-aware UI behavior, not only successful page rendering
- focused analyzer regressions around the result contract, not only `/home/evgeny/projects/analyzer-v2/tests/test_aoi_canary_contract.py`

## Final Judgment

Approve with revisions.

The memo has the right tranche, the right Tier A seam, and the right refusal to overclaim shared runtime or transient neutrality. It just needs sharper prerequisite language so implementation stays honest about the real work: bounded, but more than a trivial route swap.
