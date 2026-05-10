# Prompt For Fresh Codex Session

Please audit this memo critically:

- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`

Do not treat the memo as presumptively correct.
Test its assumptions against the codebase and the recent communications stack.

## Required tasks

1. Read the memo in full.
2. Read the reference dictation:
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
3. Check the memo against the relevant analyzer-v2 seams:
   - `src/presenter/compose_from_intent.py`
   - `src/presenter/presentation_bridge.py`
   - `src/presenter/manifest_builder.py`
   - any nearby presenter files you think materially affect the memo's claims
4. Check the cited downstream-app evidence:
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx`
   - `/home/evgeny/projects/the-critic/communications/NEXT_SESSION_ANNOTATIONS_PANEL.md`
   - `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/plans/[id].tsx`
   - `/home/evgeny/projects/analyzer-mgmt/scripts/seed_rhetoric.py`
   - `/home/evgeny/projects/analyzer-mgmt/scripts/populate_rhetoric_schemas.py`
5. Read the recent roadmap/strategy context:
   - `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
   - `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_scope.md`
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Is the memo right that the missing layer is not only renderer/output family law, but also follow-up operation family law and artifact routing law?
- Does the memo correctly treat `Close Read` as a product north star without prematurely turning it into the next code tranche?
- Is the claim that Critic and analyzer-mgmt already embody these downstream patterns supported by the code?
- Does the memo keep the immediate next analyzer move in the right place, or should the roadmap pivot more sharply?
- Is there a smaller and stronger next step than the memo recommends?
- Does the memo understate any major risks, especially around hard-coded presenter logic, validator discipline, or product sprawl?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Close_Read_Direction_Change_And_Implications_Audit_2026-04-01.md`

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
