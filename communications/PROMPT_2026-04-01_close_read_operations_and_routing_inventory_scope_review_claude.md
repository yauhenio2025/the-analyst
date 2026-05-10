# Prompt For Fresh Claude Session

Please review this memo critically:

- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_scope.md`

Your task is not to agree with it by default.
Test whether the memo is the right immediate companion tranche after the revised `Close Read` direction memo and alongside the current extraction scope.

## What to do

1. Read the memo carefully.
2. Read the immediate strategic context:
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
   - `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_scope.md`
   - `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
3. Scrutinize the memo against the actual codebase, especially:
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
4. Read relevant recent memos and reviews in `communications/` that bear on this scope, especially:
   - `communications/REPORT_Claude_Close_Read_Direction_Change_And_Implications_Critique_2026-04-01.md`
   - `communications/REPORT_Codex_Close_Read_Direction_Change_And_Implications_Audit_2026-04-01.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## What to focus on

- Is this inventory tranche actually the smallest honest product-side companion to the extraction tranche?
- Does the memo correctly distinguish:
  - runtime-real operations
  - latent product intent
  - aspirational routing
- Does it correctly distinguish:
  - generic operations
  - output-specific operations
  - routing contracts
- Does the memo correctly keep analyzer-v2 attachment-point analysis out of the primary scope while extraction is still active?
- Is the analyzer/host ownership boundary framed correctly?
- Is the proposed output of this tranche concrete enough to inform a later `Close Read V1` memo?
- Is there a smaller or stronger immediate tranche than this one?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Close_Read_Operations_And_Routing_Inventory_Scope_Critique_2026-04-01.md`

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
