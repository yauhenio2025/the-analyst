# Prompt For Fresh Codex Session

Please audit this memo critically:

- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_scope.md`

Do not treat the memo as presumptively correct.
Test its assumptions against the current codebase, the just-completed AOI V2 `aoi_by_sin_type` host proof, the existing `/captures` implementation in Critic, and the larger analyzer-v2-as-brain objective.

## Required tasks

1. Read the memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_sin_findings_capture_selection_consumer_proof_v1_completion.md`
   - `communications/MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_completion.md`
   - `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_completion.md`
   - `communications/REPORT_Codex_Phase_E_AOI_By_Theme_Nested_Finding_Handle_Propagation_V1_Completion_Audit_2026-04-02.md`
   - `communications/REPORT_Claude_Phase_E_AOI_By_Theme_Nested_Finding_Handle_Propagation_V1_Completion_Critique_2026-04-02.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
3. Check the memo against the relevant Critic code and tests:
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/hooks/useCaptureStatus.ts`
   - `/home/evgeny/projects/the-critic/api/server.py`
   - `/home/evgeny/projects/the-critic/api/models_db.py`
   - nearby Critic files that materially govern capture creation, routing, and persistence
4. Check the memo against the analyzer-side context it depends on:
   - `src/presenter/first_hop_affordance.py`
   - `src/aoi/contract.py`
   - nearby analyzer files that materially govern the specialized `aoi_by_sin_type` contract
5. Read relevant roadmap/review context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Is capture-provenance persistence the right immediate next slice after the completed selection-creation proof on `aoi_by_sin_type`?
- Is the memo correct that the current `/captures` seam drops analyzer provenance in practice?
- Is the memo broad enough to cover the actual live AOI “Research Question” flow in `ResearchFlagDialog`, not only the routed `capture_to_research_todo(...)` leg?
- Does the plan preserve the current genealogy `entity_id -> genealogy_job_id` fallback behavior in `CaptureContext.submitCapture(...)` while adding the new persistence path?
- Is `source_workflow_key` the smallest defensible workflow-truth field, or is the memo under-scoping what actually needs to persist?
- Is the memo honest that `source_workflow_key` gives workflow-type truth rather than exact source-run identity?
- Is it honest to keep these out of scope for v1:
  - `GET /api/captures/by-job/{job_id}` generalization
  - `GenealogyCaptureDB` renaming
  - workflow-neutral Arsenal stream taxonomy
  - end-to-end Arsenal parity
- Should both routed destination paths preserve the new provenance fields?
- Should the direct `POST /api/research-todos` path preserve the same provenance fields too?
- Is it acceptable for Arsenal and research-todo source snapshots to remain asymmetric apart from the required new provenance fields?
- Is the memo honest enough that analyzer `entity_id` is:
  - an opaque analyzer handle
  - not Critic `db_id`
  - not a mutation contract by itself
- Does the memo account explicitly for the required DB migration on `GenealogyCaptureDB`?
- Does this slice teach a reusable substrate, or is it too local to Critic's current implementation?
- What is the smallest defensible correction if the memo is directionally right but overcommits?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_AOI_V2_Capture_Provenance_Persistence_V1_Scope_Audit_2026-04-03.md`

Please include:

1. Verdict:
   - approve
   - approve with corrections
   - reject
2. The memo's strongest code-backed points
3. The memo's weakest or overstated assumptions
4. Any factual discrepancies you found
5. What this changes for the larger roadmap
6. The most defensible next move after this memo

Be concrete. Use code-backed reasoning. Avoid fluff.
