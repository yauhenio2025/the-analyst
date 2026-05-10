# Prompt For Fresh Claude Session

Please review this completion memo critically:

- `communications/MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_completion.md`

Do not assume the memo is correct.
Test whether its claims are appropriately calibrated against the code that actually landed, the broader roadmap, and the larger analyzer-v2-as-brain objective.

## What to do

1. Read the completion memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_scope.md`
   - `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_completion.md`
   - `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_scope.md`
   - `communications/REPORT_Claude_Phase_E_AOI_By_Theme_Nested_Finding_Handle_Propagation_V1_Scope_Critique_2026-04-02.md`
   - `communications/REPORT_Codex_Phase_E_AOI_By_Theme_Nested_Finding_Handle_Propagation_V1_Scope_Audit_2026-04-02.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
3. Scrutinize the memo against the actual codebase, especially:
   - `src/aoi/contract.py`
   - `src/views/definitions/aoi_by_theme.json`
   - `src/views/definitions/aoi_by_sin_type.json`
   - `src/presenter/first_hop_affordance.py`
   - `tests/test_aoi_contract.py`
   - `tests/test_presentation_api.py`
   - `tests/test_manifest_trace.py`
   - `tests/test_analysis_product_contract.py`
4. Check the memo against the strongest host/runtime evidence:
   - `/home/evgeny/projects/the-critic/webapp/src/components/influence/ThemeSynthesisCard.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx`
   - nearby Critic files that materially govern thematic finding identity or Arsenal mutation behavior
5. Read relevant roadmap context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## What to focus on

- Does the completion memo describe the landed boundary honestly?
- Is it correct that `aoi_by_theme` now preserves nested `finding_id` while whole-view affordance remains generic-only?
- Is the memo calibrated enough about host evidence:
  - legacy Critic thematic UI proves nested finding identity
  - current bounded-V2 thematic path does not yet operationalize the handle
- Is the memo honest enough about legacy payloads remaining handle-less until rebuild?
- Does the memo overstate what the analyzer handle means relative to Critic `db_id` or actual Arsenal mutation behavior?
- Does the memo describe the next honest step well, or is it prematurely steering toward mixed-surface specialization?
- Is there a smaller or more defensible next move than the one the memo suggests?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Phase_E_AOI_By_Theme_Nested_Finding_Handle_Propagation_V1_Completion_Critique_2026-04-02.md`

Please include:

1. Verdict:
   - approve
   - approve with corrections
   - reject
2. The strongest parts of the memo
3. The weakest assumptions or overclaims
4. Code-backed findings
5. Strategic implications for the roadmap
6. Concrete corrections or reframing you recommend

Keep the critique specific and unsentimental.
Do not produce fluff.
