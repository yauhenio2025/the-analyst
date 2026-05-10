# Prompt For Fresh Codex Session

Please audit this memo critically:

- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_scope.md`

Do not treat the memo as presumptively correct.
Test its assumptions against the codebase and the recent communications stack.

## Required tasks

1. Read the memo in full.
2. Read the immediate context:
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
   - `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_scope.md`
3. Check the memo against the relevant product/runtime evidence:
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/ResearchTodosPage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/research/ResearchCard.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/hooks/useResearchTodos.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/OutlinePanel.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/OutlineEditorPanel.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/research/researchConstants.ts`
   - nearby `the-critic` files that materially govern capture, Arsenal, research-todo, comments, and routed artifacts
   - `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/plans/[id].tsx`
   - `/home/evgeny/projects/analyzer-mgmt/scripts/seed_rhetoric.py`
   - `/home/evgeny/projects/analyzer-mgmt/scripts/populate_rhetoric_schemas.py`
4. Read relevant recent roadmap/review context:
   - `communications/REPORT_Claude_Close_Read_Direction_Change_And_Implications_Critique_2026-04-01.md`
   - `communications/REPORT_Codex_Close_Read_Direction_Change_And_Implications_Audit_2026-04-01.md`
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Is this inventory tranche the right immediate product-side companion to the extraction tranche?
- Does the memo correctly avoid conflating host-local behavior with analyzer-owned law?
- Does the memo correctly defer analyzer-side attachment-point analysis until after extraction?
- Is the proposed inventory structure concrete enough to be useful later?
- Does the memo understate any material risks or overstate any current runtime evidence?
- Is there a smaller and stronger immediate tranche than this one?
- Does the memo set up the later `Close Read V1` memo in the right order, or too early?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Close_Read_Operations_And_Routing_Inventory_Scope_Audit_2026-04-01.md`

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
