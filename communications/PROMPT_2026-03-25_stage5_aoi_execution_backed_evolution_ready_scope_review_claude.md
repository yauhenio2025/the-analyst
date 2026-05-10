# Prompt For Claude: Stage 5 AOI Execution-Backed Evolution-Ready Scope Critique

Critique the new Stage 5 execution-backed scope and proof-plan docs:

- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md`

Your job is to test the robustness of the assumptions behind those docs against the actual codebase, the recent Stage 5 memo/proof trail, and the broader analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “run one more AOI proof.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- close the AOI exemplar honestly before broader Tranche 3 generalization

So evaluate the new docs both as:

1. a bounded next-step scope for Stage 2 closure evidence
2. a broader program-prioritization decision

## What to inspect

Read these docs first:

- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_completion.md`
- `communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-25.json`
- `communications/PROOF_stage5_aoi_pack_rerun_summary_2026-03-25.json`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_completion.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

Then inspect the code paths the new docs depend on:

The Critic:

- `/home/evgeny/projects/the-critic/api/server.py`
  - especially:
    - `POST /api/influence/thinkers/{thinker_id}/run-thematic-analysis-v2`
    - `start_genealogy_analysis(...)`
    - `GET /api/analysis/{workflow_key}/jobs/{job_id}`
    - `GET /api/analysis/{workflow_key}/results/{project_id}`
    - `GET /api/analysis/{workflow_key}/results/{project_id}/{analysis_id}`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh`
- `/home/evgeny/projects/the-critic/test-stage5-aoi-landing-smoke.js`
- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_client.py`

Analyzer-v2:

- `src/api/routes/presenter.py`
- `src/presenter/compose_from_intent.py`
- `tests/test_task_planner.py`
- `tests/test_compose_from_intent.py`

Look through any other recent memo/report/proof files in `communications/` or `docs/` that materially affect the judgment.

## Questions to answer

1. Is one bounded `execution_backed` `evolution_ready` case really the right next move, or is some other prerequisite still missing?
2. Is `evolution_ready` still the right default upgrade candidate in light of the bigger program objective, or is another ready case more honest/stronger?
3. Is the memo’s definition of `execution_backed` strict enough to prevent disguised fixture reuse?
4. Does the proof plan actually match the codebase:
   - launch route
   - project-id handling
   - polling route
   - result-boundary checks
   - counted planner-backed compose path
5. Is one successful `execution_backed` ready case really enough for an honest Stage 2 closure decision under the frozen rubric, or is the new memo over-reading that bar?
6. Are there hidden operational prerequisites the memo under-specifies:
   - reference-text presence
   - local project/thinker state
   - local DB state
   - analyzer/the-critic environment coupling
   - artifact-capture weaknesses
7. Does the updated roadmap now tell the truth about:
   - Stage 5 having passed on fixture-backed evidence
   - Stage 2 still being open
   - Tranche 3 still being blocked
8. Is the new step appropriately narrow, or is it smuggling in broader platform closure by implication?

## Output requirements

Write your critique to:

- `communications/REPORT_Claude_STAGE5_AOI_Execution_Backed_Evolution_Ready_Scope_Critique_2026-03-25.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve after revision`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether the roadmap/progress read is now honest or still overstated.
5. A direct answer to whether one execution-backed ready case is enough for Stage 2 closure under the current rubric.
6. Any concrete memo/proof-plan revisions you recommend before execution.

Prioritize hidden assumptions, evidence-tier dishonesty, scope leakage, operational precondition gaps, broader-program mis-sequencing, and codebase mismatches over general summary.
