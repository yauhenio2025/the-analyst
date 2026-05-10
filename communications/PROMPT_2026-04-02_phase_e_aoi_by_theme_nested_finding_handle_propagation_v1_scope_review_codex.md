# Prompt For Fresh Codex Session

Please audit this memo critically:

- `communications/MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_scope.md`

Do not treat the memo as presumptively correct.
Test its assumptions against the current codebase, the completed first-hop affordance line, the just-completed `aoi_by_sin_type` specialization closeout, the Close Read operations/routing inventory, and the larger analyzer-v2-as-brain objective.

## Required tasks

1. Read the memo in full.
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
   - `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
3. Check the memo against the relevant analyzer code and tests:
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
   - nearby analyzer files that materially govern AOI findings payload generation and presentation assembly
4. Check the memo against the runtime/product evidence it depends on:
   - `/home/evgeny/projects/the-critic/webapp/src/components/influence/ThemeSynthesisCard.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx`
   - nearby Critic files that materially govern per-finding identity and promotion behavior
5. Read relevant roadmap/review context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Is mixed-surface nested finding-handle propagation on `aoi_by_theme` the right immediate next analyzer-side slice after the completed `aoi_by_sin_type` specialization?
- Is it correct to keep `aoi_by_theme` whole-view affordance generic-only?
- Is attaching `finding_id` only inside `_build_by_theme_payload(...)` actually the best seam, or is a smaller `_finding_card(...)` centralization acceptable so long as surface behavior stays equally narrow?
- Is the memo honest enough about the difference between:
  - pure findings surfaces
  - mixed surfaces with nested findings
- Is `aoi_by_theme` actually the strongest next matrix-broadening surface, or is the memo choosing the wrong target?
- Is the analyzer-side `finding_id` contract framed honestly enough:
  - opaque analyzer handle
  - not Critic `db_id`
  - not mutation parity
  - not a cross-run stability guarantee
- Is the memo honest enough that:
  - the strongest thematic-item identity evidence comes from the legacy Critic thematic UI rather than an already-operational bounded-V2 thematic finding seam
  - legacy persisted payloads may still lack nested handles until rebuilt?
- Is this smaller and stronger than an immediate pivot to outline-routing?
- Does this move the platform toward the broader `Close Read` / analyzer-v2-as-brain objective, or is it too AOI-local?
- What is the smallest defensible correction if the memo is directionally right but overcommits?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_AOI_By_Theme_Nested_Finding_Handle_Propagation_V1_Scope_Audit_2026-04-02.md`

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
