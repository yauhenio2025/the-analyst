# Prompt For Codex: Stage 5 AOI Execution-Backed Evolution-Ready Scope Audit

Audit the new Stage 5 execution-backed scope and proof-plan docs:

- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md`

Your job is to test the robustness of the assumptions behind those docs against the actual codebase, recent Stage 5 memo/proof trail, and the larger analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “run a fresh AOI case.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- keep Tranche 3 blocked until AOI exemplar ratification is honest rather than inferred

So assess the new docs both as:

1. a bounded Stage 2 evidence-upgrade scope
2. a broader platform-program prioritization decision

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

Then inspect the implementation and proof paths the docs rely on:

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

1. Does the codebase support the proof plan as written, or does it rely on unverified assumptions about launch, polling, persistence, or result discovery?
2. Is the definition of `execution_backed` technically enforceable and artifact-auditable, or can the plan still quietly collapse into fixture-backed reuse?
3. Is `evolution_ready` the right default candidate for the upgrade, or is there a stronger or less ambiguous case?
4. Is one successful execution-backed ready case enough to support an honest Stage 2 closure decision under the frozen rubric and the broader roadmap, or is that still too thin?
5. Are there hidden operational dependencies that make the step riskier or broader than the memo claims:
   - seeded project state
   - thinker texts
   - job/result persistence
   - analyzer/the-critic environment configuration
   - smoke-script limits
6. Is the memo right not to rerun the full frozen pack by default after the execution-backed case, or does the stronger proof logically require a broader pack refresh?
7. Does the updated roadmap tell the truth now:
   - keep roadmap order
   - Stage 5 seam gate passed on fixture-backed evidence
   - Stage 2 still open
   - Tranche 3 still blocked pending the stronger closure decision

## Output requirements

Write your audit to:

- `communications/REPORT_Codex_STAGE5_AOI_Execution_Backed_Evolution_Ready_Scope_Audit_2026-03-25.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve with revisions`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether the program should:
   - keep the roadmap order
   - keep Tranche 3 blocked
   - treat one execution-backed ready case as enough for Stage 2 closure under the current rubric
5. Any concrete memo/proof-plan revisions you recommend before execution.

Prioritize bugs, risks, hidden assumptions, evidence-quality gaps, scope dishonesty, and broader-program mis-sequencing over general summary.
