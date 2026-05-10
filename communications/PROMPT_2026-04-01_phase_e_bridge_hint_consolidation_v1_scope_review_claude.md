# Prompt For Fresh Claude Session

Please review this memo critically:

- `communications/MEMO_2026-04-01_phase_e_bridge_hint_consolidation_v1_scope.md`

Do not assume the memo is correct.
Test whether it is now the right immediate next analyzer-side tranche after the completed composition metadata extraction closeout and the completed Close Read operations/routing inventory companion.

## What to do

1. Read the scope memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
   - `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
3. Scrutinize the memo against the actual codebase, especially:
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
   - nearby presenter / orchestrator / engine-definition files that materially govern role-hint emission for AOI source-backed and genealogy saved-result compose paths
4. Read relevant recent memos and reviews in `communications/`, especially:
   - `communications/REPORT_Claude_Phase_E_Composition_Metadata_Extraction_V1_Scope_Critique_2026-04-01.md`
   - `communications/REPORT_Codex_Phase_E_Composition_Metadata_Extraction_V1_Scope_Audit_2026-04-01.md`
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## What to focus on

- Is bridge-hint consolidation really the right immediate next code slice after extraction, or is there a smaller or stronger alternative?
- Does the memo correctly identify the remaining duplicated authority seam in:
  - `composition_source_bridge.py`
  - `genealogy_saved_result_bridge.py`
- Does it keep the scope narrower than analyzer-side affordance/routing attachment?
- Does it preserve the right ownership split:
  - canonical capability metadata owns `composition_role`
  - presenter/orchestrator bridges may emit hints, but should not author them independently
- Does the memo handle legacy genealogy aliases honestly enough?
- Does it correctly require canonical capability metadata to be returned for both canonical and legacy keys?
- Does it keep output shapes and proof surfaces stable enough?
- Does the fail-closed requirement look correct for missing/invalid metadata on migrated bridge-backed keys?
- Does the memo overstate how much bridge consolidation is needed now?
- Does it frame the relationship between this cleanup slice, the Close Read inventory, and the later first-hop affordance/routing addendum correctly?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Phase_E_Bridge_Hint_Consolidation_V1_Scope_Critique_2026-04-01.md`

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
