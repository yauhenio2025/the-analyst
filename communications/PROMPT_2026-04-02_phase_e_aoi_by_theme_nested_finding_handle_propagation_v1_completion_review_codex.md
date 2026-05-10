# Prompt For Fresh Codex Session

Please audit this completion memo critically:

- `communications/MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_completion.md`

Do not treat the memo as presumptively correct.
Test its assumptions against the actual landed code, the recent Phase E affordance line, the Close Read operations/routing inventory, and the broader analyzer-v2-as-brain objective.

## Required tasks

1. Read the memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_scope.md`
   - `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_completion.md`
   - `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_scope.md`
   - `communications/REPORT_Claude_Phase_E_AOI_By_Theme_Nested_Finding_Handle_Propagation_V1_Scope_Critique_2026-04-02.md`
   - `communications/REPORT_Codex_Phase_E_AOI_By_Theme_Nested_Finding_Handle_Propagation_V1_Scope_Audit_2026-04-02.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
   - `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
3. Check the memo against the relevant analyzer code and tests:
   - `src/aoi/contract.py`
   - `src/views/definitions/aoi_by_theme.json`
   - `src/views/definitions/aoi_by_sin_type.json`
   - `src/presenter/first_hop_affordance.py`
   - `tests/test_aoi_contract.py`
   - `tests/test_presentation_api.py`
   - `tests/test_manifest_trace.py`
   - `tests/test_analysis_product_contract.py`
4. Check the memo against the runtime/product evidence it depends on:
   - `/home/evgeny/projects/the-critic/webapp/src/components/influence/ThemeSynthesisCard.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx`
   - nearby Critic files that materially govern thematic finding identity and Arsenal mutation behavior
5. Read relevant roadmap context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Does the completion memo accurately describe the landed code boundary?
- Is it correct that `aoi_by_theme` now carries nested `finding_id` while whole-view affordance remains generic-only?
- Is the memo sufficiently honest about:
  - the host-evidence line coming from legacy Critic thematic UI rather than current bounded-V2 thematic operations
  - persisted `aoi_by_theme` payloads remaining unchanged until rebuilt
  - analyzer `finding_id` not being equivalent to Critic `db_id`
- Does the memo overstate how much this slice advances mixed-surface semantics?
- Is the stated next honest step defensible, or is there a smaller or cleaner follow-on?
- What is the most defensible roadmap interpretation after this completion?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_AOI_By_Theme_Nested_Finding_Handle_Propagation_V1_Completion_Audit_2026-04-02.md`

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
