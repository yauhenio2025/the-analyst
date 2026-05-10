# Report: Stage 5 AOI Exemplar Revision Slice Scope Audit

Date: 2026-03-24
Auditor: Codex
Verdict: **Approve with revisions**

## Findings

1. The memo is directionally right, but `planner-outcome visibility` is still underspecified relative to the actual UI failure mode.

- In `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:587-601`, `aoi_selection_blocked` is converted into a thrown `Error` and flattened into `pageError` instead of being retained as structured planner state.
- `loadSelection()` clears `pageError` on any saved-result load in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:372-380`, and initial hydrate auto-runs `loadSavedResults({ autoLoadLatest: true })` in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:773-809`, so background hydration can erase the blocked banner.
- Ready outcomes are stored in `plannerDecision`, but selected-source identity changes clear that state in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:270-272`.
- Current coverage only proves immediate surfacing, not retention against hydrate/refresh churn, in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:580-629`.

This means the memo should define the host workstream as structured planner-state retention across background hydrate/source refresh, not just generic “visibility.”

2. The memo’s `selector/provider reliability` bucket is still too coarse for the code as written.

- The AOI selector timeout is hard-coded to `10.0` seconds in `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py:38-41`.
- `get_anthropic_client()` sets HTTP timeouts but does not set `max_retries` in `/home/evgeny/projects/analyzer-v2/src/llm/client.py:31-52`, so Anthropic SDK defaults still apply; local installed SDK shows `DEFAULT_MAX_RETRIES = 2` in `/home/evgeny/.local/lib/python3.13/site-packages/anthropic/_constants.py:8-14`.
- `_call_aoi_selection_llm()` maps only `httpx.TimeoutException` and builtin `TimeoutError` to `llm_timeout` in `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py:738-748`; everything else is collapsed into `llm_provider_failure` in `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py:749-757`.
- Anthropic’s timeout-like exception is `APITimeoutError`, a subclass of `APIConnectionError`, with the exact `"Request timed out or interrupted..."` text seen in the Stage 5 proof; see `/home/evgeny/.local/lib/python3.13/site-packages/anthropic/_exceptions.py:71-80` and `/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-24.json:13`.

So the next slice should distinguish at least four sub-buckets explicitly:

- credentials / env unavailability
- timeout budget
- SDK retry policy / transport behavior
- exception classification / reason-code mapping

3. The evidence still supports a bounded proof-surface problem rather than a deeper architectural failure.

- The planner seam resolves the AOI catalog, returns explicit `aoi_selection_blocked` results, and preserves blocked trace metadata in `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py:431-500` and `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py:973-1042`.
- The blocked-case fixture behaves correctly in the proof pack: real `aoi_selection_blocked`, correct reason code, no compose request, auditable artifact trail, in `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-24_stage5_aoi_exemplar_eval_pack.md:175-199`.
- The selection-backed compose seam already exists end to end:
  - analyzer compose path: `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py:256-280`
  - critic proxy path: `/home/evgeny/projects/the-critic/api/server.py:20568-20617`
  - critic client path: `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts:110-149`
  - compose page planner-backed rendering: `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:550-592`
- Those paths are already exercised by focused tests in `/home/evgeny/projects/analyzer-v2/tests/test_compose_from_intent.py:658-686`, `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:583-617`, and `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.test.tsx:163-228`.

This is not evidence that the roadmap should jump to Tranche 3. It is evidence that the current Tranche 2 seam needs one honest repair-and-rerun slice.

4. The pack and rubric should remain frozen.

- The rubric’s `operational_behavior` requirement is exactly what caught the real host-surface failure in `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md:94-126`.
- The blocked fixture is valid and useful, not a fake negative, in `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-24_stage5_aoi_exemplar_eval_pack.md:175-199`.

Changing the pack now would hide the actual proof-surface gap instead of fixing it.

5. The memo is honest about Stage 2 remaining open, and that honesty should be preserved.

- The canonical roadmap still keeps Stage 2 in progress and explicitly blocks Tranche 3 on a successful Stage 5 rerun in `/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1167-1170` and `/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1255-1259`.
- Earlier tranche-scope language expected Stage 2 closure as a side-effect in `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md:28-29` and `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md:115-121`.
- The current revision-slice memo correctly backs away from that and keeps Stage 2 open unless the rerun truly earns it in `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_revision_slice_scope.md:150-159`.

6. The current proof artifacts warn against over-reading the latency field as raw selector latency.

- The ready case shows a `plan-task` request at `15:20:53.452Z` and response at `15:21:25.245Z`, roughly 31.8s, in `/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_evolution_ready_requests_2026-03-24.json:20` and `/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_evolution_ready_requests_2026-03-24.json:175`.
- The synthetic blocked case shows a `plan-task` request at `15:23:31.247Z` and response at `15:23:31.269Z`, roughly 22ms, in `/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_selection_blocked_requests_2026-03-24.json:20` and `/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_selection_blocked_requests_2026-03-24.json:175`.
- But the summary reports roughly `45.4s` for `planner_selection_latency` in both cases, including the blocked one, in `/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-24.json:186-189` and `/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-24.json:752-755`.

That field is useful as a capture-window metric, but not as pure planner timing for selector diagnosis.

## Direct Answers

1. Is the memo correctly keeping the roadmap order intact rather than pivoting phases?

Yes. The canonical and draft roadmaps both say the immediate move is a bounded Stage 5 revision slice and that Tranche 3 stays blocked until the same pack is rerun successfully. See `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:181-223` and `/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1167-1170`.

2. Is the memo correctly narrowing the next move to selector/provider reliability and planner-outcome visibility and nothing broader?

Mostly yes, but both workstreams need tighter definitions before implementation. The memo is right not to broaden scope into Tranche 3, lifecycle, or new architecture.

3. Does the codebase evidence support treating the failure as a bounded proof-surface problem rather than a deeper architectural failure?

Yes. The route, planner, blocked-path semantics, and compose-from-selection bridge all exist and are tested. The observed break is on selector-call reliability plus host retention of planner outcomes, not on the existence of the seam itself.

4. Is the `selector/provider reliability` bucket still too vague?

Yes. It should explicitly distinguish:

- env / credential absence
- timeout budget
- SDK retry behavior
- transport/provider failures
- timeout-classification bugs that currently collapse into `llm_provider_failure`

5. Is the `planner-outcome visibility` scope concrete enough to guide implementation?

No. It should say that the host must retain the full planner decision, including blocked reason code/detail and ready handoff metadata, across initial hydrate and saved-result refresh until explicit dismissal, new planning attempt, or explicit source change.

6. Is keeping the Stage 5 case pack and rubric frozen the right decision?

Yes. The current pack and rubric exposed the real failure class. Relaxing them would reduce audit value.

7. Is the memo honest about Stage 2 remaining open?

Yes. That is the correct call and should not be softened before a successful rerun with stronger-than-fixture evidence.

8. Is there any hidden dependency that makes Tranche 3 pressure stronger than the memo admits?

No phase-pivoting dependency surfaced. The hidden dependencies I found are local to this slice:

- Anthropic timeout/retry/classification behavior in the selector path
- background saved-result hydration clearing planner state in the host

The broader AOI- and `the-critic`-specific compose contract remains a known Stage 7/13 residual, but it is not what failed here and does not justify pulling Tranche 3 forward.

## Roadmap Recommendation

- Update slightly: yes.
- Recalibrate the immediate plan: yes.
- Do not pivot phases: yes.

The required update is not a roadmap reorder. It is a tighter Stage 5 slice definition.

## Concrete Revisions Before Implementation

1. Rewrite the memo’s selector/provider section so the diagnosis note must record:

- observed exception class
- emitted reason code
- request elapsed time from HAR/request timestamps
- whether retries occurred or were implicitly allowed
- whether the issue was env, timeout budget, retry/transport behavior, or reason-code mapping

2. Rewrite the memo’s planner-visibility section to require:

- structured retention of the full `TaskPlanningDecision` in the AOI panel
- blocked outcome rendering from structured planner state, not only a generic error string
- no background hydrate/source-refresh path may clear planner outcome state implicitly
- explicit clear rules: only new planning attempt, explicit dismissal, or explicit source switch

3. Add test obligations to the slice, while keeping the same test files/commands:

- a frontend test proving blocked outcome visibility survives initial auto-load / saved-result hydrate
- a frontend test proving ready handoff visibility survives the same churn long enough to continue into compose
- a planner test proving Anthropic timeout-class exceptions are classified intentionally

4. Clarify in the memo that latency diagnosis must use actual request timing, not just the summary’s `planner_selection_latency` field.
