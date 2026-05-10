# Prompt For Fresh Claude Session

Please review this memo critically:

- `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_scope.md`

Do not assume the memo is correct.
Test whether it is now the right immediate analyzer-side tranche after the completed Close Read operations/routing inventory companion and in light of the broader analyzer-v2-as-brain objective.

## What to do

1. Read the scope memo in full.
2. Read the immediate strategic context:
   - `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
3. Scrutinize the memo against the actual codebase, especially:
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
   - nearby presenter / engine-definition files that materially govern metadata resolution for the currently proved engine set
4. Read relevant recent memos and reviews in `communications/`, especially:
   - `communications/REPORT_Claude_Interface_First_Renderer_Output_Family_Strategy_Critique_2026-04-01.md`
   - `communications/REPORT_Codex_Interface_First_Renderer_Output_Family_Strategy_Audit_2026-04-01.md`
   - `communications/REPORT_Claude_Close_Read_Direction_Change_And_Implications_Critique_2026-04-01.md`
   - `communications/REPORT_Codex_Close_Read_Direction_Change_And_Implications_Audit_2026-04-01.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## What to focus on

- Is this still the right next immediate analyzer-side tranche after the completed runtime-first inventory companion?
- Does the memo correctly identify the first extraction target as composition-law metadata rather than admission policy, lifecycle, or taxonomy?
- Does the memo now describe the already-existing partial extraction honestly:
  - bridge-emitted role hints
  - hint-first semantic-role resolution
- Does the memo overstate how much reusable metadata already exists in the current engine definitions?
- Does it commit to the right storage split:
  - `composition_role` in capability definitions
  - pattern/stance/description/rationale as role-level composition metadata
- Does the migrated-engine set and legacy-engine handling look honest and implementable?
- Does the memo correctly preserve the host boundary and existing proof surfaces?
- Does it correctly keep analyzer-side affordance/routing attachment work out of scope until after extraction?
- Is there a smaller or stronger next analyzer-side slice than this one?
- Does the memo frame the relationship between this extraction tranche and the longer-term `Close Read` direction correctly?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Phase_E_Composition_Metadata_Extraction_V1_Scope_Critique_2026-04-01.md`

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
