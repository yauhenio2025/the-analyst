# Prompt For Fresh Codex Session

Please audit this memo critically:

- `communications/MEMO_2026-04-01_phase_e_bridge_hint_consolidation_v1_scope.md`

Do not treat the memo as presumptively correct.
Test its assumptions against the current codebase, the recent extraction closeout, the Close Read companion inventory, and the larger analyzer-v2-as-brain objective.

## Required tasks

1. Read the memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
   - `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
3. Check the memo against the relevant analyzer code and tests:
   - `src/presenter/compose_from_intent.py`
   - `src/presenter/composition_source_bridge.py`
   - `src/orchestrator/genealogy_saved_result_bridge.py`
   - `src/engines/discovery.py`
   - `src/engines/composition_roles.py`
   - `src/presenter/composition_role_registry.py`
   - `src/engines/capability_definitions/aoi_thematic_synthesis.yaml`
   - `src/engines/capability_definitions/aoi_engagement_mapping.yaml`
   - `src/engines/capability_definitions/aoi_sin_findings.yaml`
   - `src/engines/capability_definitions/aoi_thematic_report.yaml`
   - `src/engines/capability_definitions/genealogy_relationship_classification.yaml`
   - `src/engines/capability_definitions/genealogy_final_synthesis.yaml`
   - `src/presenter/dynamic_prompt.py`
   - `src/views/generator.py`
   - `tests/test_composition_source_bridge.py`
   - `tests/test_genealogy_saved_result_bridge.py`
   - `tests/test_compose_from_intent.py`
   - `tests/test_representative_composition_matrix.py`
   - `tests/test_transient_proof_harness_contract.py`
   - `tests/test_compose_sessions.py`
4. Read relevant recent roadmap/review context:
   - `communications/REPORT_Claude_Phase_E_Composition_Metadata_Extraction_V1_Scope_Critique_2026-04-01.md`
   - `communications/REPORT_Codex_Phase_E_Composition_Metadata_Extraction_V1_Scope_Audit_2026-04-01.md`
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Is bridge-hint consolidation the right immediate next analyzer-side slice after extraction?
- Does the memo correctly identify the remaining duplicated authority seam, or is it overstating the problem?
- Does it correctly keep analyzer-side affordance/routing attachment out of scope for one more bounded step?
- Does the required helper really need to return canonical capability metadata for both canonical and legacy keys?
- Are the AOI and genealogy bridge seams the right exact targets?
- Is fail-closed behavior for missing/invalid metadata on migrated bridge-backed keys the right bar?
- Does the memo preserve output shapes and proof surfaces honestly enough?
- Is there a smaller and stronger immediate slice than this one?
- What, if anything, should change in the roadmap ordering after the extraction closeout?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_Bridge_Hint_Consolidation_V1_Scope_Audit_2026-04-01.md`

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
