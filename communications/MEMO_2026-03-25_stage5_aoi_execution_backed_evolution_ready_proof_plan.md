# Memo: Stage 5 AOI Execution-Backed Evolution-Ready Proof Plan

Date: 2026-03-25
Status: Draft proof plan
Program: Dynamic Bespoke Apps Platformization
Depends on:
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_completion.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh`
- `/home/evgeny/projects/the-critic/test-stage5-aoi-landing-smoke.js`

## Objective

Produce one real `execution_backed` `evolution_ready` AOI case using:

- the real AOI launch route in `the-critic`
- newly produced outputs from a fresh run
- the same counted planner-backed compose path already validated in the passed Stage 5 pack

This plan is intentionally for one case only.
It is not a second frozen-pack rerun.

## Fixed Candidate

Default target:

- project id: `round5-proof-dossier-final-1774100000`
- thinker id: `otto_neurath`
- workflow key: `anxiety_of_influence_thematic_single_thinker`
- ready-case task: `Show how Aaron Benanav's use of Otto Neurath's planning argument evolves across the corpus.`

If this exact target cannot be executed fresh, stop and write a revision note.
Do not silently downgrade to fixture-backed reuse and still call it `execution_backed`.

## Environment Contract

Expected local services:

- analyzer-v2 on `http://127.0.0.1:8002`
- the-critic backend on `http://127.0.0.1:5555`
- the-critic webapp on `http://127.0.0.1:3456`

The Critic must be pointed at the local analyzer.
The Critic start script may choose the next free backend/webapp ports rather than `5555` / `3456`, so the actual resolved ports must be recorded and then used consistently in all commands and artifacts.

If the proof executes on a later date, keep the same filename stems below but replace `2026-03-25` with the actual execution date.

## Preflight

1. Start local analyzer-v2.
   Suggested command:
   `uvicorn src.api.main:app --host 127.0.0.1 --port 8002`

2. Start local the-critic.
   Suggested command:
   `./start`

3. Record the actual resolved ports after startup.
   Do not assume `5555` / `3456` if `./start` selected different ports.

4. Verify the endpoints respond on the resolved ports:
   - `curl -fsS http://127.0.0.1:8002/v1/meta/definitions-version`
   - `curl -fsS -I <resolved_webapp_url>`
   - `curl -fsS <resolved_backend_url>/ || true`

5. Verify selector/provider availability in the live analyzer environment.
   The proof should not start if the analyzer cannot make the AOI selector call.
   Do not print secret values into artifacts; just record whether the provider was available.

6. Verify the AOI proof surface loads in the browser for:
   - `/p/round5-proof-dossier-final-1774100000/anxiety-of-influence/otto_neurath/v2-thematic`

7. Verify reference texts exist for `otto_neurath`.
   As of the current review trail, this is a known blocker rather than a hypothetical one.
   On the default local SQLite fallback used by the-critic in development, `data/the_critic.db` currently shows:
   - thinker row exists for `round5-proof-dossier-final-1774100000` / `otto_neurath`
   - uploaded reference text count is `0`

   Check:

   ```bash
   curl -fsS \
     -H 'X-Project-ID: round5-proof-dossier-final-1774100000' \
     <resolved_backend_url>/api/influence/thinkers/otto_neurath/texts
   ```

   If none exist, upload them through:

   ```text
   POST /api/influence/thinkers/otto_neurath/texts
   ```

   using the appropriate multipart upload route and then verify they are present before continuing.

8. If the fresh launch route still returns `400 No reference texts uploaded for this thinker`, stop.
   That is a real precondition failure for this proof, not a valid execution-backed attempt.

## Execution Plan

### Step 1: Launch a fresh AOI run through the real route

Use the real backend launch route, not a saved-result shortcut:

```bash
curl -fsS \
  -X POST \
  -H 'X-Project-ID: round5-proof-dossier-final-1774100000' \
  <resolved_backend_url>/api/influence/thinkers/otto_neurath/run-thematic-analysis-v2
```

Save the launch response.
It should preserve at least:

- returned `job_id`
- `status`
- `workflow_key`
- `created_at`

On this path, the returned Critic `job_id` is the analyzer-v2 job id.
Do not document this as if it were a separate local identity.

Suggested artifact:

- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_launch_2026-03-25.json`

### Step 2: Validate the active-run boundary while the run is fresh

Run the direct-poll smoke once against the active run id:

```bash
/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh \
  --analyzer-url http://127.0.0.1:8002 \
  --critic-url <resolved_backend_url> \
  --workflow-key anxiety_of_influence_thematic_single_thinker \
  --consumer-key the-critic \
  --project-id round5-proof-dossier-final-1774100000 \
  --thinker-id otto_neurath \
  --run-job-id <fresh_job_id>
```

This invocation is for the active-run boundary only.
Do it before the run is completed, because the script checks active discovery.
Capture the script output into the suggested artifact file rather than leaving it only in terminal scrollback.
Treat this script as supplemental boundary evidence only.
It does not prove the counted planner-backed browser compose path by itself.

Suggested artifact:

- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_active_run_2026-03-25.json`

### Step 3: Poll the fresh run to completion

Poll the generic AOI job detail endpoint until the fresh run completes:

```text
GET /api/analysis/anxiety_of_influence_thematic_single_thinker/jobs/{fresh_job_id}
```

Preserve:

- `job_id`
- `v2_job_id`
- status transition to `completed`
- selected thinker identity
- workflow key

On this path, `job_id` and `v2_job_id` should match.
Record that explicitly rather than implying two distinct fresh ids.

Operational expectation:

- real AOI thematic execution may take roughly `30-120+` minutes wall-clock
- if the run exceeds a bounded wait such as `180` minutes without reaching `completed`, treat it as failed for this proof attempt and write a revision note

If the run fails, stop and write a revision note.

### Step 4: Validate the completed-result boundary

After completion, run the direct-poll smoke again against the completed result:

```bash
/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh \
  --analyzer-url http://127.0.0.1:8002 \
  --critic-url <resolved_backend_url> \
  --workflow-key anxiety_of_influence_thematic_single_thinker \
  --consumer-key the-critic \
  --project-id round5-proof-dossier-final-1774100000 \
  --thinker-id otto_neurath \
  --result-job-id <fresh_job_id> \
  --check-aoi-landing \
  --aoi-expected-tab v2-thematic
```

This invocation is for the completed-result boundary and landing behavior.
Capture the script output into the suggested artifact file.
Treat it as supplemental evidence, not as the counted compose proof.

Suggested artifact:

- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_boundary_2026-03-25.json`

### Step 5: Run the counted planner-backed `evolution_ready` compose flow on the fresh result

Use the real browser AOI flow:

1. open the AOI V2 thematic panel
2. enter the `evolution_ready` task
3. trigger planner-backed handoff
4. continue into `/compose-from-intent`
5. compose via `compose-from-selection`

The counted path explicitly excludes profile/autostart compose branches that can drop `source_v2_job_id`.

The saved request artifact must record:

- `fixture_strength = execution_backed`
- the fresh `source_v2_job_id` matching the launch/completed-boundary job id
- `plan_outcome_kind`
- selected source families
- `compose_endpoint_used`
- `compose_request_variant`
- `source_v2_job_id_preserved`
- `compose_from_source_unused`
- `compose_shell_visible`

Suggested artifacts:

- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_requests_2026-03-25.json`
- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_session_2026-03-25.har`
- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_state_2026-03-25.png`

### Step 6: Grade the case honestly

Apply the same rubric dimensions relevant to a ready case:

- `selection_fit`
- `rationale_clarity`
- `rendered_usefulness`
- `operational_behavior`

Minimum shape for this case remains:

- selected families include `thematic_synthesis`
- selected families include `thematic_report`

Do not lower thresholds because the case is fresh.

## Branch Rules

If all of the following are true:

- the run is freshly produced
- the run reaches a durable completed result
- the planner-backed path stays on `compose-from-selection`
- canonical `source_v2_job_id` is preserved
- the ready case passes the rubric honestly

then:

- write a completion memo
- decide explicitly whether the stronger evidence now closes Stage 2
- update the current roadmaps accordingly

If any of the following happen:

- launch fails
- known preflight prerequisites are missing
- fresh run fails
- no fresh durable result exists
- planner-backed compose fails
- the case only works by falling back to fixture-backed or legacy behavior
- `"database is locked"` or equivalent SQLite contention errors recur during run persistence or subsequent warm-snapshot/compose steps

then:

- write a revision memo
- keep Stage 2 open
- keep Tranche 3 blocked

## Closeout Files

Success path:

- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_completion.md`

Failure path:

- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_revision.md`

The closeout must state separately:

- Stage 5 seam gate status
- Stage 2 closure status
- whether the new case is truly `execution_backed`
- whether one successful fresh case is strong enough to support repeated bounded AOI transient use under the rubric

## Notes

The existing frozen pack should be treated as baseline evidence, not rerun automatically.

This plan is intentionally narrow:

- one fresh AOI ready case
- one stronger-tier proof
- one explicit Stage 2 decision

That is the missing evidence bar.
