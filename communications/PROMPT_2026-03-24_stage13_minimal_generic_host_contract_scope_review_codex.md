Audit the proposed Stage 13 scope memo against the live analyzer-v2 and the-critic codebases and the broader roadmap.

Primary target:

- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md`

Also consult:

- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_completion.md`
- `communications/PROOF_2026-03-24_stage12_cross_workflow_renderer_law_generalization.md`
- `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_scope.md`
- `communications/MEMO_2026-03-24_stage11_rich_semantic_page_planning_completion.md`
- `communications/PROOF_2026-03-24_stage11_rich_semantic_page_planning.md`
- `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_completion.md`
- `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_completion.md`
- any recent memos in `communications/` or `docs/` from the past 48 hours that materially bear on host/consumer ownership, readiness adoption, result consumption, or thin-host direction

You must:

1. test whether the memo’s assumptions are actually supported by the current code
2. verify that the memo is inferring the next stage from real seams in both repos rather than only from the roadmap label
3. identify any places where the memo overstates how generic the current host contract already is
4. identify any place where the memo overstates how complete or clean the current Stage 12 foundation already is on authored or no-`composition_mode` restore paths
5. identify any contract mismatch between:
   - direct browser-to-analyzer calls
   - host proxy routes
   - local snapshot/cache behavior
   - project/auth context ownership
6. identify any stage-ordering mistake:
   - Stage 13 vs more Stage 12 widening
   - Stage 13 vs Stage 14 lifecycle/session work
7. say explicitly if no additional relevant docs were found beyond the recent roadmap/memo trail

Prioritize inspection of these code seams.

Analyzer-v2:

- `src/api/routes/results.py`
- `src/api/routes/presenter.py`
- `src/api/routes/orchestrator.py`
- `src/analysis_products/result_contract.py`
- `src/analysis_products/source_backed_readiness.py`
- `src/orchestrator/task_router.py`
- `src/orchestrator/task_planner.py`
- `src/presenter/compose_from_intent.py`
- `src/presenter/presentation_api.py`
- `src/presenter/renderer_contract_enforcement.py`
- `src/consumers/definitions/the-critic.json`

the-critic:

- `webapp/src/lib/boundedV2Client.ts`
- `webapp/src/lib/composeFromIntentClient.ts`
- `webapp/src/hooks/useBoundedV2Workspace.ts`
- `webapp/src/pages/GenealogyPage.tsx`
- `webapp/src/pages/AnalysisWorkspacePage.tsx`
- `webapp/src/pages/AnxietyOfInfluencePages.tsx`
- `webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `webapp/src/components/influence/AoiComposeFromIntentShell.tsx`
- `api/server.py`
- `api/middleware.py`
- adjacent tests that show how these seams are currently consumed

Be explicit about these questions:

- is Stage 13 really the next missing seam now that Stage 12 has an explicit served-intent law, or does the memo underplay the remaining Stage 12 risk
- is the proposed Host Contract v1 matrix concrete enough:
  - contract families
  - owner split
  - canonical upstream identity vs host-local identity
  - authoritative scope channel
  - required inputs
  - direct vs proxy vs local rules
- does the memo now describe the consumer coupling asymmetry honestly:
  - run/result families accept request-level `consumer_key`
  - compose families remain structurally the-critic-bound
- does the current code actually support consolidation onto one shared host adapter layer across AOI and genealogy, or are the workflows still too different
- is the memo now right-sized about what consolidation work remains versus what is already covered by `boundedV2Client` and `useBoundedV2Workspace`
- is the memo correct to keep `route-task` and `plan-task` outside required host-v1 adoption
- does the memo handle `project_id`, `consumer_key`, `source_analysis_id`, `source_v2_job_id`, and snapshot caching ownership honestly
- is adopting `source-backed-readiness` in AOI launch plus one genealogy readiness consumption case now enough, or should the proof bar still require broader host adoption
- is the proof bar strong enough without a second consumer
- does the memo clearly separate:
  - host navigation/routing
  - analyzer task routing
  - host-owned persistence hooks
  - analyzer-owned analytical truth
- does the memo now make host-side surface selection explicit enough as a host-owned v1 concern

Output requirements:

- save your audit to:
  - `communications/REPORT_Codex_STAGE13_Minimal_Generic_Host_Contract_Scope_Audit_2026-03-24.md`
- begin with a verdict:
  - `Approve`
  - `Approve after revision`
  - `Do not approve`
- findings first
- summaries second
- be explicit about:
  - code seams
  - contract mismatches
  - hidden assumptions
  - sequencing errors
  - proof weaknesses

Do not modify code.
