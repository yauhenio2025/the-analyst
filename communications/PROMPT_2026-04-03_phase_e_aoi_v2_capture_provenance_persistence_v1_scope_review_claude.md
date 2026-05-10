# Prompt For Fresh Claude Session

Please review this memo critically:

- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_scope.md`

Do not assume the memo is correct.
Test whether this is now the right immediate next bounded Phase E slice after the completed AOI V2 `aoi_by_sin_type` capture-selection consumer proof.

## What to do

1. Read the scope memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_sin_findings_capture_selection_consumer_proof_v1_completion.md`
   - `communications/MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_completion.md`
   - `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_completion.md`
   - `communications/REPORT_Codex_Phase_E_AOI_By_Theme_Nested_Finding_Handle_Propagation_V1_Completion_Audit_2026-04-02.md`
   - `communications/REPORT_Claude_Phase_E_AOI_By_Theme_Nested_Finding_Handle_Propagation_V1_Completion_Critique_2026-04-02.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
3. Scrutinize the memo against the actual codebase, especially in Critic:
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/hooks/useCaptureStatus.ts`
   - `/home/evgeny/projects/the-critic/api/server.py`
   - `/home/evgeny/projects/the-critic/api/models_db.py`
   - nearby Critic files that materially govern capture creation, routing, Arsenal mutation, and research-todo creation
4. Check the memo against the analyzer-side context it depends on:
   - `src/presenter/first_hop_affordance.py`
   - `src/aoi/contract.py`
   - nearby analyzer files that materially govern the already-landed `aoi_by_sin_type` specialization and handle truth
5. Read relevant roadmap context in `communications/`, especially:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## What to focus on

- Is capture-provenance persistence really the right immediate next step after the bounded host proof, or is there a smaller or stronger next move?
- Is the memo correct that the current concrete loss is:
  - `entity_id` emitted by the bounded renderer but not sent/persisted
  - truthful analysis workflow provenance not preserved through `/captures`
- Is the memo now broad enough to cover the actual live AOI “Research Question” path in `ResearchFlagDialog`, which creates both a capture and a research todo directly?
- Does the implementation need to preserve the current genealogy fallback where `CaptureContext.submitCapture(...)` treats `entity_id` as a `genealogy_job_id` fallback for genealogy captures?
- Is `source_workflow_key` the right minimal provenance field, or is the memo under-scoping the true need?
- Is the memo honest that `source_workflow_key` is workflow-type truth rather than exact source-run identity?
- Is it honest to defer:
  - generic capture-status law
  - workflow-neutral Arsenal stream taxonomy
  - end-to-end Arsenal mutation parity
  - mixed-surface consumer work
- Should the slice update both route legs:
  - `/captures/{id}/to-arsenal`
  - `/captures/{id}/to-research-todo`
- Should the slice also update the direct `POST /api/research-todos` path used by `ResearchFlagDialog`?
- Is it acceptable for Arsenal and research-todo source snapshots to remain structurally different so long as the new provenance fields are present in both?
- Is it acceptable to leave the current `GenealogyCaptureDB` naming and `genealogy_job_id` indexing untouched in v1?
- Does the memo name the required DB migration clearly enough?
- Does this slice genuinely move the platform toward the larger analyzer-v2-as-brain objective, or is it too Critic-local?
- Is there a more defensible next bounded step than this one?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Phase_E_AOI_V2_Capture_Provenance_Persistence_V1_Scope_Critique_2026-04-03.md`

Please include:

1. Verdict:
   - approve
   - approve with corrections
   - reject
2. The memo's strongest parts
3. The weakest assumptions
4. Code-backed findings
5. Strategic implications for the roadmap
6. Concrete corrections or reframing you recommend

Keep the critique specific and unsentimental.
Do not produce fluff.
