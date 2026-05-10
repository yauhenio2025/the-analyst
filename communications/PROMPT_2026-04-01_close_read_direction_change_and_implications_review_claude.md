# Prompt For Fresh Claude Session

Please review this memo critically:

- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`

Your task is not to agree with it by default.
Your task is to test whether the memo's assumptions, reframing, and proposed forward move are actually robust.

## What to do

1. Read the memo carefully.
2. Examine it in light of the larger objective:
   - analyzer-v2 becomes the brain
   - downstream apps become thinner over time
   - the real destination may be a multi-project app like `Close Read`
3. Scrutinize the memo against the actual codebase, especially these seams:
   - `src/presenter/compose_from_intent.py`
   - `src/presenter/presentation_bridge.py`
   - `src/presenter/manifest_builder.py`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx`
   - `/home/evgeny/projects/the-critic/communications/NEXT_SESSION_ANNOTATIONS_PANEL.md`
   - `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/plans/[id].tsx`
   - `/home/evgeny/projects/analyzer-mgmt/scripts/seed_rhetoric.py`
   - `/home/evgeny/projects/analyzer-mgmt/scripts/populate_rhetoric_schemas.py`
4. Read the recent strategy and roadmap context in `communications/`, especially:
   - `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
   - `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_scope.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
5. Decide whether the memo:
   - correctly identifies a missing layer
   - correctly keeps the next implementation move where it is
   - overstates how close we are to `Close Read`
   - misses a smaller or better next tranche

## What to focus on

- Does the memo correctly identify `follow-up operation families` and `artifact routing` as distinct from renderers and output families?
- Does the codebase actually support the claim that Critic and analyzer-mgmt already embody those downstream patterns?
- Is `Close Read` the right north-star framing, or does that risk premature super-app thinking?
- Is keeping `Phase E Composition Metadata Extraction V1` as the next concrete code move still the right call after this dictation?
- Does the memo adequately distinguish:
  - product north star
  - current substrate gaps
  - immediate implementation priority
- Is there a better way to order the next tranches?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Close_Read_Direction_Change_And_Implications_Critique_2026-04-01.md`

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
