# Report: Stage 9 Engine-Chain Planner Generalization Scope Audit

Verdict: `Approve`

Post-revision note:

- After reviewing the revised `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_scope.md`, the major blockers identified in this audit are now addressed at the memo level.
- The revised memo now treats hydration as a first-class stage concern, defines the normalization delta beyond `WorkflowExecutionPlan`, narrows AOI to bounded Stage 7 handoff metadata, bounds objective coverage to the current AOI/genealogy slice, and strengthens the proof bar beyond saved JSON artifacts alone.
- The findings below remain the rationale for why the earlier draft was not approvable as written.

## Findings

### 1. The memo's core public-input assumption is not supported by the live code: the Stage 8 task envelope is still too thin to drive a real genealogy plan

This is the main contract mismatch in the memo.

`CompositionTaskRequest` is intentionally advisory and shallow in `src/orchestrator/task_routing_schemas.py`. For genealogy it only carries coarse source-mode hints such as:

- `prior_work_external_doc_keys_count`
- `has_target_chapter_external_doc_keys`
- `has_target_work_text`
- `prior_work_count`

It does not carry the concrete planner inputs the existing planners actually need.

The real planning seams still require hydrated corpus context:

- `OrchestratorPlanRequest` requires `thinker_name`, `target_work`, and concrete `prior_works` in `src/orchestrator/schemas.py`
- inline planning requires full target/prior texts through `AnalyzeRequest` in `src/orchestrator/pipeline_schemas.py`
- by-reference planning requires actual registered-corpus bindings and metadata through `AnalyzeByRefRequest` in `src/orchestrator/pipeline_schemas.py`
- `src/orchestrator/by_ref.py` only becomes plannable after it resolves document bindings and rewrites them into an `OrchestratorPlanRequest`

So the actual missing seam is not just:

- `route-task` -> `plan-task`

It is:

- `route-task` -> source/material hydration -> planner input synthesis -> plan output normalization

That is also the clearest stage-ordering mistake in the memo. The memo treats Stage 8 task intake and Stage 9 planner input as if they are already the same layer. They are not.

Required revision:

- Either widen the proposed Stage 9 request shape materially beyond the Stage 8 envelope, or explicitly scope Stage 9 to advisory planning over a still-separate hydration step.

### 2. The memo does not yet define a concrete enough delta between the proposed `TaskPlanningDecision` and the existing `WorkflowExecutionPlan`

The repo already has public planning seams:

- `POST /v1/orchestrator/plan`
- `POST /v1/orchestrator/plan/adaptive`

And `WorkflowExecutionPlan` already contains:

- explicit phases
- chain / engine selections
- overrides
- estimates
- `objective_key`
- optional `decision_trace`

That live plan substrate is in:

- `src/api/routes/orchestrator.py`
- `src/orchestrator/planner.py`
- `src/orchestrator/adaptive_planner.py`
- `src/orchestrator/schemas.py`

So for genealogy, Stage 9 risks collapsing into a wrapper around an already-existing plan object unless the memo names the genuinely new contract surface.

The credible new delta is not simply:

- phases
- chains
- engines

The current planner already emits those.

The credible Stage 9 delta would be things like:

- planning outcome kind
- reused routing decision
- required hydration state
- explicit separation between execution-plan truth and composition-handoff truth
- downstream readiness classification
- bounded composition handoff metadata that `WorkflowExecutionPlan` does not currently contain

Required revision:

- Define exactly what `TaskPlanningDecision` adds beyond `WorkflowExecutionPlan`.
- If the genealogy side is mostly normalization around existing adaptive planning, say that directly.

### 3. The memo underplays how much AOI handoff is still workflow-specific plumbing and host-coupled contract work, not planner generalization

The memo is right that AOI is asymmetric, but the live AOI path is even more specifically coupled than the memo says.

Analyzer-side AOI law is still hardcoded and bounded:

- `compose-from-source` only accepts `workflow_key == anxiety_of_influence_thematic_single_thinker` in `src/presenter/compose_from_intent.py`
- it also only accepts `consumer_key == the-critic` in `src/presenter/compose_from_intent.py`
- `ComposeFromSourceRequest` is still fixed to `workflow_key + consumer_key + source_v2_job_id + profile` in `src/presenter/schemas.py`
- the source bridge is AOI-only, with exactly four source families and two preset selectors in `src/presenter/composition_source_bridge.py`

The host side is also still doing real AOI identity work:

- `/home/evgeny/projects/the-critic/api/server.py` resolves `source_analysis_id` and project/thinker context into `source_v2_job_id`
- that same proxy route forwards the real analyzer call for source-backed compose
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx` still chooses the AOI `profile` in the UI flow
- `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts` calls the-critic's proxy route, not analyzer-v2 directly

There is also no live host adoption of Stage 8 routing:

- repo search found no the-critic use of `POST /v1/orchestrator/route-task`

So the AOI Stage 9 outcome should be described more narrowly as:

- bounded AOI-specific handoff metadata over the Stage 7 bridge

not as:

- generalized engine-chain planner output

This is the place where the memo is calling planner generalization what is still mostly workflow-specific plumbing.

Required revision:

- Say explicitly that the AOI Stage 9 output remains AOI-specific handoff metadata over fixed profile law and host-owned source-identity resolution.

### 4. The planner substrate is real, but the memo overstates how normalized and planner-ready it already is

The memo is correct that Stage 9 is not greenfield. The current planner substrate is real. But some of the readiness language is stronger than the code supports.

What is already real:

- planner-readable capability metadata in `src/orchestrator/catalog.py`
- objective definitions with `baseline_workflow_key` in `src/objectives/definitions/`
- legacy plan generation in `src/orchestrator/planner.py`
- adaptive plan generation in `src/orchestrator/adaptive_planner.py`

What is not yet cleanly normalized:

- planning is still strongly execution-oriented in `src/orchestrator/pipeline.py` and `src/orchestrator/by_ref.py`
- the adaptive planner still needs `normalize_plan_execution_targets()` because generated plans still confuse `chain_key` and `engine_key` and sometimes fabricate invalid compound keys in `src/orchestrator/adaptive_planner.py`
- the adaptive planner prompt requires `chapter_targeting_rationale`, but `PlannerDecisionTrace` has no field for it and the parser drops it; that is a live trace-grammar mismatch between `src/orchestrator/adaptive_planner.py` and `src/orchestrator/schemas.py`

So the current code supports:

- planner substrate exists

It does not yet fully support the stronger reading that:

- engine compatibility / dependency reasoning is already a clean reusable contract
- trace grammar is already stable enough to be lifted directly into a new public planning boundary

Required revision:

- Keep the "reuse, don't replace" framing.
- Lower the memo's readiness language around normalized compatibility/dependency modeling and planner trace cleanliness.

### 5. The memo imports Stage 10 semantics into Stage 9 more than the current codebase can support

The memo says Stage 9 output should name:

- source families
- expected analytical products
- composition handoff requirements

Directionally that is right. But those are not generalized planner-side concepts yet.

In the live code:

- the only concrete source-family vocabulary is AOI-only in `src/presenter/composition_source_bridge.py`
- the newer analysis-product contracts in `src/analysis_products/schemas.py` and `src/analysis_products/result_contract.py` are post-run result/presentation manifests, not planner-to-composition contracts
- the canonical roadmap still places generalized documented source families under Stage 10

So the current system does not yet have a shared planner-level concept of:

- source family per workflow
- expected product family per planning outcome

It has:

- AOI-specific source-family bridge substrate
- post-run artifact/result contracts

That is a stage-ordering issue. The memo is partially borrowing Stage 10 semantics to make Stage 9 sound more composition-ready than the current substrate really is.

Required revision:

- For AOI, it is reasonable for Stage 9 to name bounded producer engines and AOI source families.
- For the memo overall, do not imply that source-family semantics are already generalized planner substrate.

### 6. The memo fits the larger roadmap only if it stays explicit that this is still a bounded AOI/genealogy slice rather than broad planner generalization

The larger program objective is analyzer-v2 as the brain for dynamic bespoke analytical apps. Against that objective, the current Stage 9 slice is still narrow:

- `route-task` only supports `influence_thematic` and `genealogical` in `src/orchestrator/task_router.py`
- there is already a third objective, `logical`, but its `baseline_workflow_key` is `null` in `src/objectives/definitions/logical.json`
- the-critic still does not consume the new Stage 8 route

So the memo fits the larger roadmap if it stays honest that this stage is proving:

- bounded normalization over two workflow families

and not:

- general higher-level planning across the objective space
- host cutover to a thin analyzer-owned task-to-plan loop

Required revision:

- Add one explicit sentence saying that current Stage 9 scope is still bounded to the current AOI/genealogy slice and does not prove broad objective coverage.

### 7. The proof standard is too weak for the actual missing seam

The memo currently asks for saved decision artifacts for:

- one genealogy task
- one AOI task
- one unsupported task

That is not enough, because the main unresolved seam is contract hydration, not planner narration.

Missing proof requirements:

- one genealogy proof that shows how task/routing input becomes planner-usable corpus context before a real plan is synthesized
- one AOI proof that matches the live downstream handoff law, including `source_v2_job_id` and fixed `profile`
- contract tests for the new planning outcome taxonomy
- an explicit decision on whether `plan-task` reruns routing or accepts a prior routing decision

The cleanest contract choice is:

- public `plan-task` accepts the Stage 8 envelope plus an optional prior routing decision

That preserves Stage 8 as a meaningful seam and avoids hiding routing drift inside the planning layer.

Without stronger proof, Stage 9 can produce convincing JSON artifacts while still not actually closing the real route-to-plan seam.

### 8. No relevant Perspective docs folder exists after checking both repos

I checked both:

- `/home/evgeny/projects/analyzer-v2`
- `/home/evgeny/projects/the-critic`

for directories matching `Perspective` or `perspective` and found no relevant docs folder in either repo.

## Verification

Focused verification run during this audit:

- `PYTHONPATH=. pytest -q tests/test_task_router.py`
  - result: `13 passed`
- `PYTHONPATH=. pytest -q tests/test_registered_corpus_launch.py`
  - result: `10 passed`
- `PYTHONPATH=. pytest -q tests/test_aoi_contract.py`
  - result: `11 passed`
- `PYTHONPATH=. pytest -q tests/test_composition_source_bridge.py tests/test_adaptive_execution_target_normalization.py`
  - result: `6 passed`

What these results support:

- Stage 8 routing is real and fail-closed
- registered-corpus by-ref launch seams are real
- AOI single-thinker contract law is real
- the AOI source bridge is real
- adaptive plans still require execution-target normalization repair

## Secondary Summary

The memo has the right strategic instinct. The next missing seam really is between bounded workflow routing and bounded analytical planning. But the live code shows that the seam is still split in two:

- Stage 8 task routing is advisory and metadata-light
- existing planning paths still depend on hydrated corpus/workflow contracts

So the memo should be revised to make that split explicit, to narrow its AOI claims to workflow-specific handoff metadata, and to avoid presenting Stage 10 source-family semantics as if they were already generalized Stage 9 planner substrate.

## Final Assessment

The revised memo is now approvable as a bounded Stage 9 scope document.

It now states the Stage 9 seam more precisely:

- bounded route-to-plan normalization over existing planner substrate
- with an explicit hydration seam
- explicit AOI asymmetry
- and stronger proof requirements than saved JSON artifacts alone
