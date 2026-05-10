# Stage 13 Tier A / AOI Canary Live Proof Closeout Scope Audit

Source memo: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md`

## Overall verdict

The memo is directionally correct and mostly honest. Tier A should not yet be treated as fully closed, and the next immediate step really is a bounded live-proof closeout rather than AOI exemplar work or another Stage 13 architecture tranche. The live code matches the memo's core claim: `aoi-canary` already implements the result-backed second-consumer path, while the remaining gap is documentary proof over real discoverable AOI data rather than new product architecture. The memo should still be tightened in three places before implementation: stronger evidence requirements, clearer `attach-project` limits, and one discovery-scope prerequisite around selecting a reproducible proof result.

## Evidence consulted

Target memo plus immediate strategy trail:

- `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md`
- `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_scope.md`
- `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_completion.md`

Live code and contract surfaces:

- `src/api/routes/results.py`
- `src/analysis_products/result_contract.py`
- `src/analysis_products/source_backed_readiness.py`
- `src/executor/job_manager.py`
- `tests/test_aoi_canary_contract.py`
- `/home/evgeny/projects/aoi-canary/src/App.tsx`
- `/home/evgeny/projects/aoi-canary/src/lib/resultsClient.ts`
- `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx`
- `/home/evgeny/projects/aoi-canary/README.md`
- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractRuntime.ts`

No additional `docs/` material beyond the recent roadmap/memo trail and the result-contract feature/changelog entries changed the audit materially.

## Concrete findings

### 1. The memo is honest that Tier A is implemented but not yet documentary-closed

This is consistent across the strategy trail and the code. The prior completion memo explicitly says the bounded implementation landed but "the live proof artifact set against project-attached AOI data still needs to be captured." The draft roadmap and canonical roadmap both repeat that Tranche 1 is implemented but still open pending live proof closeout. The live app code also supports that framing: the result-backed path exists already, so the remaining work is evidence capture rather than another implementation tranche.

References: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md:14-26`, `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md:17-20`, `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:159-168`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1178`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1243-1247`, `/home/evgeny/projects/aoi-canary/src/App.tsx:486-667`.

### 2. Discovery-first is the correct Tier A acceptance path, and manual `job_id` is correctly debug-only

The current `aoi-canary` live path does exactly what the memo says: when no debug `job_id` is set, it resolves `project_id` and `workflow_key`, calls `GET /v1/results/discovery`, takes the first result, then calls manifest and presentation in order. Manual `job_id` bypass remains available, but only as a separate branch. The tests explicitly verify that the live proof path uses discovery/manifest/presentation and that the manual path bypasses discovery.

References: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md:79-90`, `/home/evgeny/projects/aoi-canary/src/App.tsx:421-466`, `/home/evgeny/projects/aoi-canary/src/App.tsx:486-667`, `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:115-184`, `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:327-391`, `src/api/routes/results.py:150-176`, `src/executor/job_manager.py:283-321`, `src/analysis_products/result_contract.py:478-542`.

### 3. The memo correctly treats this as proof closeout rather than a new architecture tranche

That boundary is real in code, not just rhetorical. The transient/source-backed path is still structurally tied to `the-critic`: analyzer transient compose hard-locks `consumer_key='the-critic'`, source-backed readiness still reports a blocker when another consumer key is used for compose-from-source followup, and Host Contract v1 still marks transient families as structural-constant or host-proxy owned. So if this memo widened into transient second-consumer support, task-launch adoption, or shared runtime extraction, it would stop being Tier A closeout and start doing later-tranche work.

References: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md:58-77`, `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:220-257`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1237-1247`, `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_completion.md:67-81`, `src/presenter/compose_from_intent.py:52`, `src/presenter/compose_from_intent.py:445-490`, `src/analysis_products/source_backed_readiness.py:144-176`, `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:187-230`, `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractRuntime.ts:99-117`.

### 4. The memo's route-shape description is accurate, but it should be clearer about secondary debug calls

The result-contract route family in the memo is correct: discovery, manifest, presentation, plus `attach-project`. The app no longer uses `/v1/presenter/page/*` as its primary live seam. But the current live app still calls `/v1/presenter/trace/*` and `/v1/presenter/status/*` as secondary debug aids after manifest loading begins, and those calls are intentionally non-blocking. The closeout memo should say this explicitly so the implementor does not misread trace/status failures as proof failure.

References: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md:18-24`, `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md:57-59`, `src/api/routes/results.py:50-97`, `src/analysis_products/result_contract.py:221-237`, `/home/evgeny/projects/aoi-canary/src/App.tsx:495-535`, `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:186-252`.

### 5. `attach-project` is a correct bounded pre-proof move, but the memo understates its limits

The endpoint exists exactly as described and is a good out-of-band setup step when a real AOI result exists but lacks `project_id`. But it only fixes missing project attachment. It does not create a proof result, override an existing conflicting project attachment, or solve a bad project/workflow choice. The memo should say that directly so operators do not treat `attach-project` as a catch-all fallback.

References: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md:108-114`, `src/api/routes/results.py:179-201`, `src/analysis_products/result_contract.py:550-588`.

### 6. One negative-state proof is required, but the memo should rank the acceptable options instead of treating them as equally strong

The memo is right that at least one negative proof is necessary because the bounded claim includes explicit failure without silent artifact fallback. The code supports that claim: live mode exposes `config_missing`, `discovery_empty`, `manifest_unavailable`, and `presentation_error`, and the tests verify that negative states do not render the artifact-backed AOI page or silently fetch presentation when manifest truth says not to. But `config_missing` is the weakest documentary proof because it only demonstrates absent setup, not a failing live seam. A better proof case is `discovery_empty`, `manifest_unavailable`, or `presentation_error`, because those exercise the actual result-contract path.

References: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md:92-107`, `/home/evgeny/projects/aoi-canary/src/App.tsx:26-36`, `/home/evgeny/projects/aoi-canary/src/App.tsx:334-418`, `/home/evgeny/projects/aoi-canary/src/App.tsx:545-609`, `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:297-325`, `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:510-572`, `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:574-620`, `src/analysis_products/result_contract.py:240-271`, `src/analysis_products/result_contract.py:391-419`.

### 7. The proposed evidence set is close, but it is not quite strong enough yet for the "no hidden presenter-page substitution" claim

Screenshots and debug-panel captures prove visible behavior, but not absence of hidden route usage. Since the Stage 13 claim here is specifically that a second consumer uses analyzer-owned `result_discovery`, `result_manifest`, and `result_presentation`, the closeout artifact set should require at least one raw request-level artifact: curl output, saved JSON, or browser network capture that shows the actual ready-state requests with `consumer_key=aoi-canary` and no `/v1/presenter/page/*` dependency on the success path. Without that, the memo risks proving UI state while under-proving the contract seam.

References: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md:140-170`, `/home/evgeny/projects/aoi-canary/src/lib/resultsClient.ts:45-99`, `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:115-184`, `src/analysis_products/result_contract.py:221-237`.

### 8. There is one hidden discovery-scope prerequisite that the memo should name explicitly

The current app resolves only `project_id` and `workflow_key` from env/URL, then asks analyzer for the newest matching result with `limit=1`. The client library supports `selected_source_thinker_id`, but the app does not currently thread it through live scope. That is fine if the closeout only needs "one real AOI proof path." It is not fine if the proof is meant to reproduce a specific thinker-scoped canary such as the Neurath path named in the README. In that case, the memo should say that the proof project must make the intended result newest by analyzer ordering, or permit one small thinker-filter compatibility fix if live proof shows that ordering alone is not reproducible enough.

References: `/home/evgeny/projects/aoi-canary/README.md:1-23`, `/home/evgeny/projects/aoi-canary/README.md:44-52`, `/home/evgeny/projects/aoi-canary/src/App.tsx:421-433`, `/home/evgeny/projects/aoi-canary/src/App.tsx:647-653`, `/home/evgeny/projects/aoi-canary/src/lib/resultsClient.ts:8-15`, `/home/evgeny/projects/aoi-canary/src/lib/resultsClient.ts:45-60`.

## Scope and sequence assessment

The bounded live proof artifact set really is the next missing seam. The roadmap now separates Tier A result-backed second-consumer proof from later AOI exemplar and transient-substrate work, and the code matches that split.

Tier A should not already be considered closed without more live proof. The current evidence is implementation plus focused tests, not a saved proof that a real project-attached AOI result is discoverable and renderable by a second consumer through the live analyzer contract.

The remaining work should not be folded into AOI exemplar completion. Tranche 2 is about task-first AOI flow, source/profile/engine-selection law, and evaluation/ops guardrails. Folding this closeout into that larger tranche would blur a smaller Stage 13 documentary gap and make it easier to move the main line without actually proving the second-consumer seam cleanly.

Once the live closeout exists, moving the roadmap's main line to AOI exemplar completion is justified. But the closeout note should still say explicitly that Stage 13 overall remains partial because Tier B and transient/host-neutral proof remain open.

References: `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:120-168`, `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:170-218`, `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:220-280`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1172-1178`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1235-1247`.

## Missing assumptions or hidden prerequisites

- The proof needs one AOI result that is not only attached to a real `project_id`, but also still restorable through the analyzer result contract and compatible with the canary's bounded renderer surface. References: `src/analysis_products/result_contract.py:349-419`, `tests/test_aoi_canary_contract.py:44-93`.
- If `attach-project` is required, someone must already know the target `job_id` from outside discovery. Discovery cannot select a job that is still undiscoverable. References: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md:108-114`, `src/api/routes/results.py:150-201`.
- The proof record should capture `consumer_key=aoi-canary` explicitly, not just `project_id`, `workflow_key`, and `job_id`, because the Stage 13 claim is second-consumer-specific. References: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md:118-126`, `/home/evgeny/projects/aoi-canary/src/lib/resultsClient.ts:45-99`.

## Recommended revisions before implementation

1. Require one raw request-level artifact for each of discovery, manifest, and presentation, with query strings visible enough to show `consumer_key=aoi-canary`.
2. Add one sentence that `presenter/trace` and `presenter/status` may still run as secondary, non-blocking debug aids and do not define proof success.
3. Tighten the negative-proof guidance so `discovery_empty`, `manifest_unavailable`, or `presentation_error` are preferred over `config_missing`.
4. Expand the `attach-project` note: it is bounded pre-proof setup only, and it does not solve missing AOI proof data, bad discovery scope, or conflicting existing project attachment.
5. Add the discovery-scope prerequisite explicitly: either choose a project where analyzer ordering already selects the intended AOI proof result, or allow one small thinker-filter proof-surface fix if that proves necessary.
6. In the final closeout note, state both of these at once: Tier A is closed, and Stage 13 overall remains partial because Tier B and transient second-consumer proof are still open.

## Bottom line

The memo is basically right. The immediate next step should be a bounded live-proof closeout for the result-backed `aoi-canary` seam, not a broader architecture tranche and not a jump straight into AOI exemplar work. The remaining edits are about making the proof note harder to misread, not about changing the fundamental sequence.
