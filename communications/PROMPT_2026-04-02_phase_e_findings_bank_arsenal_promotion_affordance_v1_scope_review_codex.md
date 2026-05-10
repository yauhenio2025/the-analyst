# Prompt For Fresh Codex Session

Please audit this memo critically:

- `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_scope.md`

Do not treat the memo as presumptively correct.
Test its assumptions against the current codebase, the completed generic first-hop affordance line, the Close Read operations/routing inventory, and the larger analyzer-v2-as-brain objective.

## Required tasks

1. Read the memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-02_phase_e_job_backed_first_hop_affordance_propagation_v1_completion.md`
   - `communications/MEMO_2026-04-02_phase_e_job_backed_first_hop_affordance_propagation_v1_scope.md`
   - `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
   - `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
   - `communications/REPORT_Claude_Phase_E_Job_Backed_First_Hop_Affordance_Propagation_V1_Scope_Critique_2026-04-02.md`
   - `communications/REPORT_Codex_Phase_E_Job_Backed_First_Hop_Affordance_Propagation_V1_Scope_Audit_2026-04-02.md`
3. Check the memo against the relevant analyzer code and tests:
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
4. Check the memo against the runtime/product evidence it depends on:
   - `/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - nearby Critic files that materially govern finding promotion to Arsenal
5. Read relevant roadmap/review context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Is a findings-bank Arsenal-promotion affordance family the right immediate next analyzer-side slice after job-backed propagation?
- Is `aoi_by_sin_type` the strongest single analyzer-known surface, or is the memo picking the wrong target?
- Is it correct to keep the generic first-hop affordance contract unchanged and add only one specialized marker?
- Is `specialized_family = "findings_bank_arsenal_promotion_v1"` now tied to a strong enough contract, or is it still too weak / redundant / host-shaped?
- Is adding one minimal per-card handle via `finding_id` the right correction, or should the family still be weakened / renamed instead?
- Does the memo clearly distinguish:
  - generic selection capture semantics
  - finding-level promotion semantics
- Does the memo stay honest about analyzer vs host ownership?
- Is keeping this job-backed only the right discipline, or should transient compose also be touched?
- Does the memo correctly keep `aoi_by_theme` out of scope?
- Does the chosen surface actually provide enough stable structure to justify analyzer-owned specialized semantics?
- Is the memo honest enough about finding identity stability, especially across re-executions?
- Does the memo preserve contract-hash and trace-diff honesty clearly enough?
- Is this smaller and stronger than the alternative of a bounded outline-routing family?
- Does this scope move the platform toward the broader `Close Read` / analyzer-v2-as-brain objective, or is it too Critic-local?
- What is the smallest defensible correction if the memo is directionally right but overcommits?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_Findings_Bank_Arsenal_Promotion_Affordance_V1_Scope_Audit_2026-04-02.md`

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
