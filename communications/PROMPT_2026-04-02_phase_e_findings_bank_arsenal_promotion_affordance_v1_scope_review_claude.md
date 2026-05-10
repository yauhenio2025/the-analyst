# Prompt For Fresh Claude Session

Please review this memo critically:

- `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_scope.md`

Do not assume the memo is correct.
Test whether this is now the right immediate next analyzer-side tranche after the completed job-backed first-hop affordance propagation closeout.

## What to do

1. Read the scope memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-02_phase_e_job_backed_first_hop_affordance_propagation_v1_completion.md`
   - `communications/MEMO_2026-04-02_phase_e_job_backed_first_hop_affordance_propagation_v1_scope.md`
   - `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
   - `communications/REPORT_Codex_Phase_E_Job_Backed_First_Hop_Affordance_Propagation_V1_Scope_Audit_2026-04-02.md`
   - `communications/REPORT_Claude_Phase_E_Job_Backed_First_Hop_Affordance_Propagation_V1_Scope_Critique_2026-04-02.md`
3. Scrutinize the memo against the actual codebase, especially:
   - `src/presenter/schemas.py`
   - `src/presenter/first_hop_affordance.py`
   - `src/presenter/presentation_api.py`
   - `src/presenter/manifest_builder.py`
   - `src/presenter/decision_trace.py`
   - `src/views/definitions/aoi_by_sin_type.json`
   - `src/views/definitions/aoi_by_theme.json`
   - `tests/test_presentation_api.py`
   - `tests/test_manifest_trace.py`
   - `tests/test_analysis_product_contract.py`
   - `tests/test_compose_from_intent.py`
   - nearby presenter / view-definition files that materially govern the AOI findings surfaces
4. Check the memo against the strongest host/runtime evidence:
   - `/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - nearby Critic files that materially govern finding promotion to Arsenal
5. Read relevant recent memos and roadmap context in `communications/`, especially:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## What to focus on

- Is a findings-bank Arsenal-promotion family really the right next immediate slice after job-backed propagation?
- Is `aoi_by_sin_type` the right single analyzer-known surface, or is the memo choosing the wrong AOI findings surface?
- Is this genuinely smaller and stronger than:
  - broad findings semantics across all `aoi_sin_findings` surfaces
  - outline-routing
  - destination lifecycle
- Is it correct to keep the base generic first-hop contract unchanged and add only one specialized marker on top?
- Is `specialized_family = "findings_bank_arsenal_promotion_v1"` now defined strongly enough, or does it still overclaim what the analyzer contract really guarantees?
- Is adding one minimal per-card handle via `finding_id` the right correction, or should the family still be weakened / renamed instead?
- Does the memo define the semantic difference between:
  - base generic capture semantics
  - finding-level promotion semantics
- Does the memo stay honest about analyzer ownership:
  - analyzer declares semantic affordance
  - hosts operationalize UX
- Is the memo right to keep this specialized family job-backed only and leave transient compose unchanged?
- Is `aoi_by_theme` correctly kept out of scope?
- Does the memo understate any need for item-level structure guarantees on the `aoi_by_sin_type` payload?
- Is the memo honest enough about item identity stability, especially across re-executions?
- Does the memo preserve hash and trace honesty clearly enough?
- Is the memo consistent with the larger `Close Read` / analyzer-v2-as-brain direction, or is it too local and Critic-shaped?
- Is there a smaller or more defensible next semantics slice than this one?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Phase_E_Findings_Bank_Arsenal_Promotion_Affordance_V1_Scope_Critique_2026-04-02.md`

Please include:

1. Verdict:
   - approve
   - approve with corrections
   - reject
2. The strongest parts of the memo
3. The weakest assumptions
4. Code-backed findings
5. Strategic implications for the roadmap
6. Concrete corrections or reframing you recommend

Keep the critique specific and unsentimental.
Do not produce fluff.
