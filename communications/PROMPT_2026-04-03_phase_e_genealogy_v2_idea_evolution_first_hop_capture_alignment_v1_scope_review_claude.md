# Prompt For Fresh Claude Session

Please review this scope memo critically:

- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_scope.md`

Do not assume the memo is correct.
Test whether its assumptions are calibrated against the landed Critic code, the just-landed current-renderer helper seam, the broader roadmap, and the analyzer-v2-as-brain objective.

## What to do

1. Read the scope memo in full.
2. Read the immediate recent context:
   - `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_completion.md`
3. Scrutinize the memo against the actual codebase, especially:
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.test.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.test.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
4. Read relevant roadmap context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
5. Look through any other recent memo in `communications/` that you think materially affects whether this is the right next step.

## What to focus on

- Does the scope memo describe the current `IdeaEvolutionRenderer` gap honestly?
- Is it right to treat this as the next bounded non-AOI follow-on after the shared helper landed?
- Is the proposed use of the helper narrow and honest, or is it starting to overfit the helper into fake generic law?
- Is `entity_id = idea.idea_id` a sound scope assumption or an overclaim?
- Is the memo calibrated enough about what stays out of scope:
  - no backend change
  - no analyzer change
  - no read-side truth surfacing
  - no generic renderer-package law
- Is the proposed browser proof boundary honest?
- Is there a smaller or more defensible next move?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Critique_2026-04-03.md`

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
