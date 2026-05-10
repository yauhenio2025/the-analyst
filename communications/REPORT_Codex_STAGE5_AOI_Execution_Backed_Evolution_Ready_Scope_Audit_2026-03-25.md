# Codex Audit: Stage 5 AOI Execution-Backed Evolution-Ready Scope

Verdict: `Approve with revisions`

## Findings

### 1. High: `execution_backed` is not runtime-enforced; it is only auditable if the proof bundle proves freshness end to end

- The scope memo defines `execution_backed` as a fresh real AOI run whose newly produced outputs are then used by planner-backed compose, and says reuse of previously saved outputs does not count ([communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md#L98), [communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md#L107)).
- The proof-plan memo likewise assumes a launch artifact plus boundary/poll artifacts can establish that stronger tier ([communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md#L154), [communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md#L119)).
- But analyzer-v2 `compose-from-selection` only requires a non-empty `source_v2_job_id`; it does not verify that the job id was freshly launched for this proof run ([src/presenter/compose_from_intent.py](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L256), [src/presenter/compose_from_intent.py](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L547)).
- The source bridge simply resolves catalog material from whatever `source_v2_job_id` is supplied and existing artifacts for that job ([src/presenter/composition_source_bridge.py](/home/evgeny/projects/analyzer-v2/src/presenter/composition_source_bridge.py#L295), [src/presenter/composition_source_bridge.py](/home/evgeny/projects/analyzer-v2/src/presenter/composition_source_bridge.py#L319)).
- The Critic can also synthesize a missing local run-reference row from a supplied `source_v2_job_id` plus project/thinker context, which is useful operationally but is not freshness proof ([api/server.py](/home/evgeny/projects/the-critic/api/server.py#L18778)).
- Existing proof artifacts reinforce that this is documentary, not enforced: they carry `fixture_strength` as a plain artifact field and repeatedly use the same saved `source_v2_job_id` in fixture-backed runs ([communications/PROOF_stage5_aoi_evolution_ready_requests_2026-03-25.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_evolution_ready_requests_2026-03-25.json#L4), [communications/PROOF_stage5_aoi_evolution_ready_requests_2026-03-25.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_evolution_ready_requests_2026-03-25.json#L29), [communications/PROOF_stage5_aoi_evolution_ready_live_rerun_post_selection_compose_fix_2026-03-25_requests.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_evolution_ready_live_rerun_post_selection_compose_fix_2026-03-25_requests.json#L4), [communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-25.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-25.json#L5)).

Judgment: the step is still valid, but only if the final proof bundle explicitly cross-links fresh launch response, active discovery, completed run detail, completed result detail, and the counted planner-backed compose request to the same newly created job id. Without that, the plan can quietly collapse back into saved-result reuse while still looking plausible.

### 2. High: the proof plan misstates the identity model by treating the Critic job id and upstream `v2_job_id` as separate fresh ids

- The scope memo asks for a launch artifact preserving both a fresh local job id and a fresh upstream `source_v2_job_id` ([communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md#L154)).
- The proof plan repeats that framing by polling a generic AOI job detail endpoint until the fresh run exposes the fresh upstream `v2_job_id` ([communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md#L119)).
- In the current implementation, for v2-backed AOI starts, `job_id = upstream["v2_job_id"]`; the Critic does not create an independent local live-run id for normal reads ([api/server.py](/home/evgeny/projects/the-critic/api/server.py#L19609)).
- The generic job endpoint then just delegates to `get_genealogy_job(job_id)` ([api/server.py](/home/evgeny/projects/the-critic/api/server.py#L20641)).

Judgment: the docs should say plainly that, on this path, the Critic-visible `job_id` is the analyzer-v2 job id. Keeping the current “fresh local id then fresh upstream id” wording overstates the seam and risks an artificially strong-looking audit trail.

### 3. High: the proof plan understates the operational dependencies required for a clean run

- AOI launch hard-fails if the thinker has no uploaded reference texts ([api/server.py](/home/evgeny/projects/the-critic/api/server.py#L14083)).
- Planner-backed AOI selection hard-fails with `llm_provider_failure` if the selector client is unavailable; the error text explicitly points to `ANTHROPIC_API_KEY` ([src/orchestrator/task_planner.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py#L727)).
- The proof-plan commands assume fixed local ports `8002`, `5555`, and `3456` ([communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md#L98)).
- The Critic start script does not guarantee `5555` and `3456`; it probes for the next free ports and only uses those preferred ports when available ([start](/home/evgeny/projects/the-critic/start#L24), [start](/home/evgeny/projects/the-critic/start#L97), [start](/home/evgeny/projects/the-critic/start#L129)).

Judgment: the memo needs an explicit prerequisites/preflight section. During this audit, the local stack was not listening on `127.0.0.1:8002`, `127.0.0.1:5555`, or `127.0.0.1:3456`, so the proof plan could not be executed as written without additional setup.

### 4. Medium: the counted path is narrower than the memo currently makes explicit

- The actual counted planner-backed path in the AOI panel preserves `source_v2_job_id` through route-task, plan-task, warm snapshot, and navigation into `/compose-from-intent` ([AoiV2ThematicPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L542), [AoiV2ThematicPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L641)).
- The planner-backed compose page then calls `composeFromSelection` with both `source_analysis_id` and `source_v2_job_id` ([AoiComposeFromIntentPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L414)).
- But the profile autostart branch explicitly drops `source_v2_job_id` by setting it to `undefined` ([AoiComposeFromIntentPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L452)).

Judgment: `evolution_ready` is still the right default upgrade candidate, but the proof-plan should explicitly forbid the profile/autostart path for this step. The counted path is planner-backed `compose-from-selection` only.

### 5. Medium: the smoke-script coverage is narrower than the proof plan implies, and the live UI’s normal discovery path is analyzer-direct

- The smoke script’s main checks are analyzer `/v1/runs/discovery`, `/v1/results/discovery`, `/v1/runs/by-job/{job_id}`, and `/v1/results/by-job/{job_id}` plus presentation ([test-stage5-direct-poll-smoke.sh](/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh#L153), [test-stage5-direct-poll-smoke.sh](/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh#L187)).
- Its AOI browser check only verifies that the thinker page lands on the `v2-thematic` tab ([test-stage5-direct-poll-smoke.sh](/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh#L255), [test-stage5-aoi-landing-smoke.js](/home/evgeny/projects/the-critic/test-stage5-aoi-landing-smoke.js#L58)).
- The live workspace itself discovers active runs and polls job details through analyzer-direct helpers, not through the Critic generic routes ([useBoundedV2Workspace.ts](/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts#L483), [boundedV2Client.ts](/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts#L58), [boundedV2Client.ts](/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts#L108)).

Judgment: the smoke script is useful for boundary checks, but it is not sufficient by itself to prove the full counted browser flow. If the memo wants Critic-generic job/result polling as part of the evidence bundle, that must be captured separately and named as supplemental evidence, not implied by the smoke.

### 6. Medium: the Critic generic endpoints are looser audit seams than the memo language suggests

- `/api/analysis/{workflow_key}/jobs/{job_id}` ignores `workflow_key` and delegates directly ([api/server.py](/home/evgeny/projects/the-critic/api/server.py#L20641)).
- `/api/analysis/{workflow_key}/results/{project_id}/{analysis_id}` likewise delegates directly ([api/server.py](/home/evgeny/projects/the-critic/api/server.py#L20853)).
- Result detail lookup itself is only by `analysis_id` and `project_id`, not by workflow ([api/server.py](/home/evgeny/projects/the-critic/api/server.py#L20321)).

Judgment: this is not a blocker for the bounded execution-backed proof, but the docs should not oversell these routes as stronger workflow-scoped audit seams than they actually are.

### 7. Medium: one clean execution-backed ready case is enough for the frozen Stage 2 gate, but still thin for broader program confidence

- The frozen rubric says Stage 2 passes only if Stage 5 passes, at least one ready case is `execution_backed` or stronger, and the evidence is strong enough to support repeated bounded AOI transient use ([communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md#L128)).
- The roadmap docs already say the Stage 5 seam gate passed on fixture-backed evidence, Stage 2 remains open, and Tranche 3 stays blocked until one bounded execution-backed ready case is captured and the closure decision is written honestly ([communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L193), [communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md](/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md#L1295)).

Judgment: one successful execution-backed `evolution_ready` case is enough for an honest Stage 2 closure decision under the current frozen rubric, but only if the proof bundle proves freshness and preserves the counted planner-primary path. It is not enough to justify broader “AOI exemplar is now robust in general” rhetoric.

## Direct Answers

- Keep roadmap order: yes.
- Keep Tranche 3 blocked: yes, until the stronger closure decision is written from an actually fresh proof bundle.
- Treat one execution-backed ready case as enough for Stage 2 closure under the current rubric: yes, but only if the final artifacts prove freshness, preserve planner-backed `compose-from-selection`, and avoid any fallback/profile path that drops `source_v2_job_id`.
- Rerun the full frozen pack after the execution-backed case by default: no. The Stage 5 seam gate already passed on fixture-backed evidence. The stronger step is a bounded Stage 2 evidence upgrade, not an automatic new reason to rerun the whole pack. Rerun only if the fresh execution-backed run exposes seam drift in launch, persistence, discovery, or compose behavior.

## Recommended Revisions Before Execution

1. Rewrite the identity language so the docs say that, on this v2-backed AOI route, the Critic `job_id` is the analyzer-v2 job id. Remove the implication that the proof will observe two distinct fresh ids.
2. Add a preflight checklist:
   - seeded project `round5-proof-dossier-final-1774100000`
   - thinker `otto_neurath` exists with uploaded reference texts
   - analyzer-v2 reachable at the configured URL
   - Critic API and webapp actually running on the resolved ports
   - selector provider available with `ANTHROPIC_API_KEY`
3. Tighten the evidence bundle requirements so it must preserve:
   - launch response with fresh job id and timestamp
   - active analyzer discovery showing that same job while still active
   - completed run detail and completed result detail for that same job
   - browser/network artifact showing planner-backed `compose-from-selection` using that same `source_v2_job_id`
4. State explicitly that the counted path excludes profile/autostart compose. Use only the planner-backed handoff path from AOI V2 thematic panel into `/compose-from-intent`.
5. Reword the smoke-script section so it is described as a boundary check, not as the sole proof of the counted browser path.
6. Add one sentence acknowledging that the Critic generic job/result routes are compatibility seams, while analyzer-direct discovery/poll remains the live host authority for active/completed run state.

## Audit Execution Notes

- Targeted relevant tests passed:
  - `PYTHONPATH=. pytest -q tests/test_task_planner.py tests/test_compose_from_intent.py` -> `43 passed`
  - `pytest -q tests/test_aoi_v2_routes.py tests/test_aoi_v2_client.py` -> `51 passed`
- I did not execute the live proof plan during this audit because the local services were not up on the ports assumed by the memo at the time of review.
