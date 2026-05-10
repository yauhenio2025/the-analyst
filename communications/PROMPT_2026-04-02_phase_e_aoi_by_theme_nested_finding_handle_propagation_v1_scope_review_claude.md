# Prompt For Fresh Claude Session

Please review this memo critically:

- `communications/MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_scope.md`

Do not assume the memo is correct.
Test whether this is now the right immediate next analyzer-side tranche after the completed findings-bank Arsenal-promotion affordance closeout.

## What to do

1. Read the scope memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_completion.md`
   - `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_scope.md`
   - `communications/MEMO_2026-04-02_phase_e_job_backed_first_hop_affordance_propagation_v1_completion.md`
   - `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_completion.md`
   - `communications/REPORT_Claude_Phase_E_Findings_Bank_Arsenal_Promotion_Affordance_V1_Scope_Critique_2026-04-02.md`
   - `communications/REPORT_Codex_Phase_E_Findings_Bank_Arsenal_Promotion_Affordance_V1_Scope_Audit_2026-04-02.md`
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
   - `src/presenter/schemas.py`
   - `src/presenter/presentation_api.py`
   - `src/presenter/manifest_builder.py`
   - `tests/test_aoi_contract.py`
   - `tests/test_presentation_api.py`
   - `tests/test_manifest_trace.py`
   - nearby analyzer files that materially govern AOI findings payload generation and page assembly
4. Check the memo against the strongest host/runtime evidence:
   - `/home/evgeny/projects/the-critic/webapp/src/components/influence/ThemeSynthesisCard.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx`
   - nearby Critic files that materially govern per-finding AOI identity and promotion behavior
5. Read relevant recent roadmap context in `communications/`, especially:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## What to focus on

- Is mixed-surface nested finding-handle propagation on `aoi_by_theme` really the right immediate next slice after the pure-surface `aoi_by_sin_type` specialization closeout?
- Is it correct to **not** add another whole-view `specialized_family` on `aoi_by_theme`?
- Is this genuinely smaller and stronger than:
  - broadening findings-bank specialization to `aoi_by_theme`
  - pivoting immediately to outline-routing
  - inventing a generic item-level affordance schema
- Does the memo correctly identify `aoi_by_theme` as a mixed surface rather than another pure findings bank?
- Is adding `finding_id` only inside `_build_by_theme_payload(...)` the right scope discipline, or is there a better seam?
- Is it better to keep `_finding_card()` unchanged, or is helper-level centralization actually the smaller implementation as long as surface behavior stays equally narrow?
- Does the memo stay honest about analyzer handle semantics:
  - opaque analyzer handle
  - not Critic's numeric `db_id`
  - not a mutation contract
  - not a cross-run identity guarantee
- Is the memo sufficiently honest that:
  - the strongest thematic-item identity evidence comes from the legacy Critic thematic UI rather than an already-operational bounded-V2 finding action seam
  - legacy persisted AOI payloads may still lack nested `finding_id` until rebuilt?
- Does this slice move the platform toward the larger `Close Read` / analyzer-v2-as-brain objective, or is it too local and AOI-shaped?
- Is there a more defensible next bounded step than this one?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Phase_E_AOI_By_Theme_Nested_Finding_Handle_Propagation_V1_Scope_Critique_2026-04-02.md`

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
