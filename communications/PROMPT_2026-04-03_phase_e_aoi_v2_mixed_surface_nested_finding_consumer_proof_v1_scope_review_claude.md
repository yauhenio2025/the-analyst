# Prompt For Fresh Claude Session

Please critique this memo rigorously:

- `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_scope.md`

Do not assume the memo is correct.
Stress-test its assumptions against the codebase, recent completion memos, the larger roadmap, and the broader analyzer-v2-as-brain objective.

## Required tasks

1. Read the memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_scope.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_sin_findings_capture_selection_consumer_proof_v1_completion.md`
   - `communications/MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
3. Inspect the relevant Critic code and tests:
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/index.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/NestedSectionsRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SubRenderers.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/influence/ThemeSynthesisCard.tsx`
   - any nearby files that materially govern `aoi_by_theme`, nested `mini_card_list` rendering, and capture-mode handoff
4. Inspect the analyzer-side context the memo depends on:
   - `src/aoi/contract.py`
   - `src/presenter/first_hop_affordance.py`
   - `src/views/definitions/aoi_by_theme.json`
   - `src/presenter/bounded_dynamic_composition.py`
   - nearby files that materially govern mixed-surface `finding_id` and generic whole-view affordance truth
5. Read the roadmap context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Is this the right next bounded Phase E move after the pure-surface AOI line has selection creation, write-side provenance truth, and read-side truth surfacing?
- Does the memo broaden the matrix honestly, or is it still too AOI-local to count as meaningful substrate proof?
- Is `aoi_by_theme` actually the strongest current mixed-surface target, given the current code and adaptive-family behavior?
- Is the memo correct to keep whole-view semantics generic-only and refuse a mixed-surface specialized family in v1?
- Is the memo specific enough about the in-scope family variant:
  - findings-bearing `accordion`
  - nested `findings`
  - `mini_card_list`
  - fallback unchanged for out-of-scope adaptive variants?
- Is the memo now right to recommend the smaller conditional `mini_card_list` seam rather than a full `aoi_by_theme` view override?
- Is the guard condition calibrated correctly for this mixed surface:
  - generic `capturable === true`
  - plus non-empty per-card `finding_id`
  - without requiring `specialized_family`?
- Is the proof boundary calibrated correctly at capture-selection creation plus `CaptureActionBar` handoff?
- Is the memo honest enough about legacy payloads that still lack nested `finding_id`?
- Does the memo overstate what current bounded-V2 host rendering can already do with `aoi_by_theme`?
- Is `source_renderer_type = "mini_card_list"` now grounded concretely enough in the current configured sub-renderer path?
- Given the larger roadmap, is there a stronger next move than this one?

## Output requirements

Write your critique to this exact file:

- `communications/REPORT_Claude_Phase_E_AOI_V2_Mixed_Surface_Nested_Finding_Consumer_Proof_V1_Scope_Critique_2026-04-03.md`

Please include:

1. Verdict:
   - approve
   - approve with corrections
   - reject
2. The memo's strongest points
3. The memo's weakest assumptions or calibration problems
4. Any factual mismatches with the codebase
5. What this changes for the broader roadmap
6. The most defensible next move after this memo

Be direct, specific, and code-backed.
