# Audit: Stage 5 AOI Post-Identity-Repair Diagnostic/Rerun Scope

Date: 2026-03-25
Reviewer: Codex
Memo under review: `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md`

## Verdict

Approve with revisions.

## Findings

### 1. Medium: the branch rule is close, but it still needs one explicit guard proving the rerun stays on the repaired planner-backed `compose-from-selection` path

The memo correctly says to stop if planner-backed `compose-from-selection` fails or if the flow falls back to legacy/debug controls (`communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:149-155`). But its artifact requirements (`communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:103-133`) do not explicitly require the saved compose request to prove all of the following:

- `variant = "selection"`
- `source_v2_job_id` is present in the host compose request
- the run stayed on `compose-from-selection`
- `compose_from_source` stayed unused

That gap matters because the current codebase still exposes an outside-the-proof-slice profile/autostart route which intentionally omits canonical `source_v2_job_id`:

- the repaired planner-backed path now includes `source_v2_job_id` in navigation from the AOI panel in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:655-667`
- the compose page forwards that field on planner-backed launch in `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:428-443`
- but the normal profile launch path still navigates without `source_v2_job_id` in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:744-758`
- and autostart still strips `source_v2_job_id` before `compose-from-source` in `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:452-477`

The tests make that distinction explicit:

- normal UI path omits `source_v2_job_id` in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:396-432`
- planner-backed path includes it in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:434-500`
- planner-backed compose forwards it in `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.test.tsx:193-230`

Implication: the memo should require the diagnostic JSON and rerun summary to record the compose endpoint actually used and the exact host compose request fields, otherwise a dishonest or regressed frozen rerun could still slip through on the wrong path.

### 2. Low: the verification section points at the wrong baseline memo for this post-repair stage

The memo says that if no further code changes are made before the spot-check, verification can rely on the confidence pack from the earlier revision-slice completion memo (`communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:223-232`). That is no longer the strongest baseline for this exact decision. The more relevant baseline is the identity-continuity completion memo, which documents the landed source-identity repair, frontend handoff repair, and focused verification pack in `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_completion.md:64-76`.

I also reran the focused checks against the current workspace:

- `PYTHONPATH=. pytest -q tests/test_task_planner.py` -> `16 passed`
- `PYTHONPATH=. pytest -q /home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py /home/evgeny/projects/the-critic/tests/test_aoi_v2_client.py` -> `47 passed`
- `CI=true npm --prefix /home/evgeny/projects/the-critic/webapp test -- --runInBand --watchAll=false src/components/influence/AoiV2ThematicPanel.test.tsx src/pages/AoiComposeFromIntentPage.test.tsx src/lib/boundedV2Client.test.ts` -> `89 passed`
- `/home/evgeny/projects/the-critic/webapp/node_modules/.bin/tsc -p /home/evgeny/projects/the-critic/webapp/tsconfig.json --noEmit` -> passed

Implication: this is a proof-quality issue, not a scope blocker, but the memo should cite the identity-repair completion baseline directly so the documentary trail stays honest.

### 3. Low: the environment guard should name the exact backend proxy setting that previously invalidated the diagnostic trail

The memo says the default target is local `analyzer-v2` plus local `the-critic` (`communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:83-91`) and tells the diagnosis note to record environment changes (`communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:123-133`). That is directionally right, but the recent proof trail showed the failure mode was more specific: `the-critic` warmup was still proxying to onrender until `ANALYZER_V2_URL=http://127.0.0.1:8002` was restored. The authoritative diagnostic JSON records that exact environment change in `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json:7-10`.

Implication: the memo should restate that exact backend proxy baseline for the next live step. Otherwise "local/local" is still too easy to satisfy dishonestly while the backend points somewhere else.

## Direct Answers

1. Does the codebase evidence support treating the AOI identity-continuity blocker as repaired strongly enough to justify the next live diagnostic?

Yes, for the planner-backed selection path specifically.

The backend now repairs and validates source identity across run-ref truth, warmed snapshot persistence, and compose validation in `/home/evgeny/projects/the-critic/api/server.py:18778-18955` and `/home/evgeny/projects/the-critic/api/server.py:20711-20749`. Warmup also repairs or creates AOI `v2_run_references` with thinker identity in `/home/evgeny/projects/the-critic/api/server.py:20109-20151`. The frontend preserves and forwards canonical source identity on the planner-backed path in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:641-687` and `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:414-449`. The focused backend/frontend tests covering those exact behaviors are present and green in `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:626-843`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:434-500`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:643-865`, `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.test.tsx:193-230`, and `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts:260-275`.

2. Is the memo correctly refusing to reopen selector/provider scope by default?

Yes.

The authoritative diagnostic artifact already showed `timeout_s = 45`, `max_retries = 0`, and `provider_outcome = success` in `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json:18-27` and `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json:688-697`. That matches the current analyzer implementation in `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py:38-41`, `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py:727-805`, `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py:1094-1121`, and `/home/evgeny/projects/analyzer-v2/src/llm/client.py:31-56`, plus focused tests in `/home/evgeny/projects/analyzer-v2/tests/test_task_planner.py:565-639`.

3. Is the branch rule strict enough to stop a dishonest frozen-rerun consumption if the repaired path still fails?

Almost, but not quite.

It is strong on stop conditions for visible product-path failure (`communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:135-155`). It still needs one added guard requiring saved proof artifacts to show the repaired planner-backed `compose-from-selection` path explicitly, with `source_v2_job_id` preserved.

4. Are the artifact requirements concrete enough to make the next live decision auditable?

Mostly yes for selector/provider auditing, not yet fully yes for host-path auditing.

The selector trace requirements are concrete and adequate (`communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:114-121`). The missing piece is explicit capture of compose endpoint/variant plus canonical source identity in the host compose request.

5. Does the memo preserve the right program order?

Yes.

- Update the roadmap slightly: yes
- Recalibrate the immediate plan: yes
- Not pivot phases: yes

That matches the current draft roadmap in `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:179-226` and stays aligned with the canonical program objective in `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:39-68`.

6. Is there any hidden dependency or code-path wrinkle that makes the next rerun step riskier, narrower, or broader than the memo claims?

Yes. The step is narrower than it may read unless the memo makes the repaired planner-backed path explicit.

- the repaired identity chain is strongest on planner-backed `compose-from-selection`
- the normal profile/autostart route is still intentionally outside the repaired proof slice and can omit `source_v2_job_id`
- warmup repair depends on going through the real thematic panel flow with thinker identity present

7. Is the memo honest that even after the identity repair, Stage 5 may still fail later for `selection_fit`, usefulness, or render-path reasons?

Yes, substantively. The memo does not pre-claim Stage 5 closure and keeps the rubric frozen (`communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:52-81`). Still, it would be better to add one direct sentence saying that a successful diagnostic only earns the frozen rerun, and that the rerun may still fail later rubric dimensions such as `selection_fit`, `rendered_usefulness`, or blocked-case auditability.

## Program Decision

The program should:

- update the roadmap slightly
- recalibrate the immediate plan
- not pivot phases

That is the correct sequence because the current code and proof trail support one more bounded Stage 5 live decision, not a selector/provider reopen and not a Tranche 3 pivot.

## Recommended Revisions Before Execution

1. Add an explicit artifact rule for the diagnostic and rerun: save whether the host launched `compose-from-selection` or `compose-from-source`, and require the planner-backed proof cases to show `variant = "selection"` plus `source_v2_job_id` in the host compose request.
2. Add an explicit dishonesty stop rule: if the ready-case diagnostic succeeds only through the profile/autostart path or any request trail with missing canonical `source_v2_job_id`, do not consume the frozen rerun.
3. Replace the verification reference to the earlier revision-slice completion memo with the identity-continuity completion memo, or cite both with the identity memo as the authoritative latest baseline.
4. Restate the exact local environment baseline for the next live step: `the-critic` must run with `ANALYZER_V2_URL=http://127.0.0.1:8002`.
5. Add one sentence clarifying that passing the diagnostic only clears the repaired identity blocker and merely earns the frozen rerun; it does not pre-clear later Stage 5 rubric risks.
