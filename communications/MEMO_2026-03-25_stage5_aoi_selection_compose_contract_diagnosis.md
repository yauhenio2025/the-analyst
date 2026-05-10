# Memo: Stage 5 `evolution_ready` Post-Snapshot-Durability Diagnostic Note

Date: 2026-03-25

## Purpose

Record the live `evolution_ready` rerun executed after the Stage 5 AOI snapshot-durability repair, and decide whether the frozen four-case Stage 5 pack was honestly earned.

## Supersession Note

This note supersedes the earlier `404`-based diagnostic conclusion in:

- `communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md`

That `404` seam is no longer the live blocker after the snapshot-durability repair landed.

Repo baseline for this diagnostic:

- `analyzer-v2`: `01427880e1c4c5ddb896b8b0c7fb8c74f6b228c9`
- `the-critic`: `6b41312b6d46fea1c112ac629f90dc43268e5ed0`

## Authoritative Artifacts

- `communications/PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_session.har`
- `communications/PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json`
- `communications/PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_state.png`
- `communications/PROOF_stage5_aoi_pack_rerun_summary_2026-03-25.json`

## Authoritative Attempt

Environment used:

- `the-critic` backend proxy set to `ANALYZER_V2_URL=http://127.0.0.1:8002`
- authoritative run executed on local ports `5555/3456` with analyzer on `8002`

Outcome:

- `route-task` succeeded
- `plan-task` succeeded and returned `aoi_composition_handoff_plan`
- planner-backed continue reached `/compose-from-intent`
- host compose stayed on `compose-from-selection`
- canonical `source_v2_job_id` stayed preserved
- `compose-from-source` stayed unused
- planner-backed compose then failed with `409`

So the frozen four-case Stage 5 pack was **not** earned and was correctly not run.

## What The Artifacts Show

### 1. The snapshot-durability repair held

The new live browser URL carried:

- `source_analysis_id=gen-v2-548ad4b1de3d`

Unlike the earlier `404` diagnostic, that id now exists locally in `the-critic` SQLite:

- `genealogy_analyses.id = gen-v2-548ad4b1de3d`
- `project_id = round5-proof-dossier-final-1774100000`
- `workflow_key = anxiety_of_influence_thematic_single_thinker`

That means the bounded Stage 5 durability slice did the job it was supposed to do:

- no phantom warm-snapshot id
- no saved-result lookup miss on the returned id
- no regression back to the old host-side durability seam

### 2. The repaired planner-backed AOI path is still the one actually being used

The authoritative request trail shows:

- `planning_outcome_kind = aoi_composition_handoff_plan`
- `planner_selection_trace.timeout_s = 45`
- `planner_selection_trace.retry_policy.max_retries = 0`
- `planner_selection_trace.provider_outcome = success`
- `planner_selection_trace.exception_class_name = null`
- final URL stayed on `/compose-from-intent`
- host compose endpoint used: `compose-from-selection`
- host compose request `variant = selection`
- `source_v2_job_id = proof-round5-adaptive-aoi-dossier-final-1774100000`
- `compose-from-source` is absent from the request trail

This means the current failure is not:

- selector/provider reliability
- planner selection blocking
- legacy fallback
- the earlier AOI identity-continuity `409`
- the host warm-snapshot durability `404`

### 3. The new blocker is analyzer-side bounded dynamic composition contract failure

The authoritative compose request was:

- `POST /api/analysis/anxiety_of_influence_thematic_single_thinker/projects/round5-proof-dossier-final-1774100000/compose-from-selection`

The host returned:

- status `409`
- detail `bounded_dynamic_composition_validation_failed`

The returned issue set is specific and repeatable:

- `compose_intent_01_aoi_thematic_synthesis`
  - missing `structured_data.themes`
  - missing `structured_data.source_documents`
  - missing `structured_data.selected_source_thinker`
- `compose_intent_03_aoi_sin_findings`
  - missing `structured_data.findings_overview`
  - missing `structured_data.severity_classification`
  - missing `structured_data.target_provenance`
  - missing `structured_data.source_provenance`
  - missing `structured_data.discrepancy_and_consequence`

The UI surfaced that as a contract error rather than a not-found error, which is the correct new live behavior.

### 4. The most plausible bounded seam is the selection-backed transient compose transform path

Observed code facts:

- `the-critic` now correctly proxies planner-backed compose-through-selection at `the-critic/api/server.py:20766`
- analyzer `compose_from_selection(...)` resolves planner-selected source families into materialized sections at `analyzer-v2/src/presenter/compose_from_intent.py:256`
- the source bridge materializes those sections from already-normalized AOI payloads by serializing stable JSON into `section.prose` at `analyzer-v2/src/presenter/composition_source_bridge.py:520`
- analyzer transient compose then still runs `_transform_section_prose(...)` over those section payloads before final contract enforcement at `analyzer-v2/src/presenter/compose_from_intent.py:851`

Working hypothesis:

- the current `409` is most likely caused by lossy or misaligned transformation of bridge-produced structured AOI JSON during the transient compose step, leaving `renderer_config.section_renderers` keys that no longer exist in the resulting `structured_data`

This is an inference from the live error payload plus the current code path. It is not yet proven by a deeper internal trace artifact.

## Failure Bucket Decision

For the authoritative post-snapshot-durability attempt, the failure bucket is:

- `analyzer selection-backed transient compose contract alignment`

It is not:

- host snapshot durability
- saved-result lookup continuity
- selector/provider reliability
- blocked AOI selection
- the earlier identity-continuity seam

## Branch Decision

Do **not** consume the frozen four-case Stage 5 pack.

Reason:

- the agreed stop condition was to halt on any new downstream seam exposed by the live `evolution_ready` rerun
- that seam has now appeared at `compose-from-selection` contract validation

## Immediate Next Step

The next bounded slice should stay narrow and focus on analyzer transient compose only:

- repair the selection-backed `compose-from-selection` path so planner-selected AOI source families produce contract-valid transient views
- keep the snapshot-durability repair closed baseline; do not reopen it
- do not reopen selector/provider, AOI identity continuity, the frozen pack definition, or roadmap order

The repair target should explicitly cover:

- `aoi_thematic_synthesis` source-family shaping under transient compose
- `aoi_sin_findings` source-family shaping under transient compose
- contract-safe alignment between generated `section_renderers` and final `structured_data`

Bounded implementation direction:

- prefer preserving or deterministically normalizing the bridge-produced structured AOI payloads over re-extracting them lossy through the generic dynamic transform path, if that proves sufficient
- if a full bypass is too broad, add a narrowly scoped normalization layer for the affected AOI source families before final contract enforcement

Minimum regression proof for the next slice:

- one analyzer regression covering `compose-from-selection` with the real four-family `evolution_ready` selection shape and asserting `200`, not `409`
- one contract-focused regression proving the affected AOI thematic-synthesis and sin-findings transient views do not reference missing `structured_data` keys
- one host-level smoke/regression showing the repaired live path still stays on planner-backed `compose-from-selection` with preserved `source_v2_job_id`

Then repeat:

1. the same live `evolution_ready` diagnostic rerun
2. only if that passes end to end, the same frozen four-case Stage 5 pack

## Status Implications

- Stage 5 remains `In progress`
- the frozen rerun was not earned
- Stage 2 remains open
- Tranche 3 remains blocked
