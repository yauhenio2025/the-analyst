# Prompt For Fresh Codex Session

Please audit this memo critically:

- `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_scope.md`

Do not treat the memo as presumptively correct.
Test its assumptions against the current codebase, the just-completed AOI pure-surface host proof line, the earlier `aoi_by_theme` nested-handle analyzer slice, and the larger analyzer-v2-as-brain objective.

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
3. Check the memo against the relevant Critic code and tests:
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/index.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/NestedSectionsRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SubRenderers.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/influence/ThemeSynthesisCard.tsx`
   - nearby Critic files that materially govern the current `aoi_by_theme` V2 rendering path, capture mode, and local override seams
4. Check the memo against the analyzer-side context it depends on:
   - `src/aoi/contract.py`
   - `src/presenter/first_hop_affordance.py`
   - `src/views/definitions/aoi_by_theme.json`
   - `src/presenter/bounded_dynamic_composition.py`
   - nearby analyzer files that materially govern `aoi_by_theme` handles and whole-view affordance truth
5. Read relevant roadmap/review context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Is a mixed-surface AOI V2 consumer proof on `aoi_by_theme` the right immediate next slice after the now-closed pure-surface `aoi_by_sin_type` selection/write/read line?
- Is the memo correct that this is a better next matrix-broadening move than another same-surface `aoi_by_sin_type` refinement?
- Is the memo honest that `aoi_by_theme` whole-view semantics remain generic-only and should stay that way in v1?
- Is the memo correct that analyzer-v2 already supplies the needed nested `finding_id` on rebuilt `aoi_by_theme` payloads?
- Is the memo explicit enough about the adaptive-family complication:
  - `aoi_by_theme` can be rewritten in place
  - only the findings-bearing `accordion` plus nested `mini_card_list` family should be in scope
  - non-findings-bearing variants should fall back unchanged?
- Is the memo now right to prefer a conditional local `mini_card_list` seam over a full `aoi_by_theme` view override?
- Is the memo explicit enough about the guard difference from `aoi_by_sin_type`:
  - generic `capturable === true`
  - plus non-empty per-card `finding_id`
  - and no `specialized_family` requirement?
- Is the memo right to keep generic renderer-package law out of scope for this slice?
- Is capture-selection sufficiency the right proof boundary here, or is the memo undercommitting / overcommitting?
- Is the memo honest enough about older handle-less `aoi_by_theme` payloads remaining passive until rebuild?
- Does the memo correctly distinguish legacy thematic UI evidence from current bounded-V2 proof?
- Is `source_renderer_type = "mini_card_list"` now properly grounded in the current configured sub-renderer path?
- Is there a stronger next move than this one, given the broader roadmap?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_AOI_V2_Mixed_Surface_Nested_Finding_Consumer_Proof_V1_Scope_Audit_2026-04-03.md`

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
