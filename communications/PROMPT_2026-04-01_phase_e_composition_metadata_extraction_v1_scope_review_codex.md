# Prompt For Fresh Codex Session

Please audit this memo critically:

- `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_scope.md`

Do not treat the memo as presumptively correct.
Test its assumptions against the codebase, the revised strategy stack, and the completed Close Read operations/routing inventory companion.

## Required tasks

1. Read the memo in full.
2. Read the immediate context:
   - `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
3. Check the memo against the relevant analyzer code and metadata seams:
   - `src/presenter/compose_from_intent.py`
   - `src/presenter/composition_source_bridge.py`
   - `src/orchestrator/genealogy_saved_result_bridge.py`
   - `src/engines/capability_definitions/aoi_thematic_synthesis.yaml`
   - `src/engines/capability_definitions/aoi_engagement_mapping.yaml`
   - `src/engines/capability_definitions/aoi_sin_findings.yaml`
   - `src/engines/capability_definitions/aoi_thematic_report.yaml`
   - `src/engines/capability_definitions/genealogy_relationship_classification.yaml`
   - `src/engines/capability_definitions/genealogy_final_synthesis.yaml`
   - `src/engines/definitions/genealogy_pass1b_relationship_classification.json`
   - `src/engines/definitions/genealogy_pass7_final_synthesis.json`
   - `src/orchestrator/genealogy_saved_result_bridge.py`
   - `tests/test_compose_from_intent.py`
   - `tests/test_representative_composition_matrix.py`
   - `tests/test_served_renderer_contract_policy.py`
   - nearby presenter / engine-definition files that materially govern metadata resolution
4. Read relevant recent roadmap/review context:
   - `communications/REPORT_Claude_Interface_First_Renderer_Output_Family_Strategy_Critique_2026-04-01.md`
   - `communications/REPORT_Codex_Interface_First_Renderer_Output_Family_Strategy_Audit_2026-04-01.md`
   - `communications/REPORT_Claude_Close_Read_Direction_Change_And_Implications_Critique_2026-04-01.md`
   - `communications/REPORT_Codex_Close_Read_Direction_Change_And_Implications_Audit_2026-04-01.md`
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Is composition metadata extraction still the right immediate next code tranche?
- Does the memo correctly separate composition-law extraction from:
  - output-family taxonomy
  - consumer admission generalization
  - lifecycle broadening
  - analyzer-side affordance/routing attachment
- Does the memo now account honestly for the partial extraction that already exists via:
  - `composition_role_hint`
  - `role_hint`
  - `_resolve_semantic_role(...)`
- Does the current codebase actually provide a plausible metadata-bearing seam for the proved engine set, or is the memo overstating that readiness?
- Is the committed storage split defensible:
  - `composition_role` in capability definitions
  - pattern/stance/description/rationale as role-level composition metadata
- Are legacy genealogy engine keys handled honestly enough in the scope?
- Does the memo correctly preserve current proof surfaces and avoid unnecessary host changes?
- Is there a smaller and stronger immediate analyzer-side tranche than this one?
- What, if anything, does the completed operations/routing inventory change about the scope or ordering?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_Composition_Metadata_Extraction_V1_Scope_Audit_2026-04-01.md`

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
