# Prompt For Fresh Claude Session

Please review this scope memo critically:

- `communications/MEMO_2026-04-04_phase_e_current_renderer_selection_emission_shared_seam_promotion_readiness_v1_scope.md`

Do not assume the memo is correct.
Test whether its assumptions are calibrated against:

- the just-landed `IdeaEvolutionRenderer` completion
- the already-landed `currentRendererCapture` helper seam and its four adopters
- the actual shared package source tree and its existing package-side capture architecture
- the broader roadmap and the analyzer-v2-as-brain objective

## What to do

1. Read the scope memo in full.
2. Read the immediate recent context:
   - `communications/MEMO_2026-04-04_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_completion.md`
   - `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Post_Eligibility_Scope_Critique_2026-04-03.md`
3. Scrutinize the memo against the actual codebase, especially:
   - `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.test.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiThemeFindingsMiniCardList.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.test.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiThemeFindingsMiniCardList.test.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.test.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.test.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/package.json`
   - `/home/evgeny/projects/analyzer-v2/renderers-ui/package.json`
   - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/AccordionRenderer.tsx`
   - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardRenderer.tsx`
   - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardGridRenderer.tsx`
   - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx`
4. Read relevant roadmap context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
   - `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_scope.md`
   - `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md`
5. Look through any other recent memo in `communications/` that you think materially affects whether this is the right next step.

## What to focus on

- Is this really the right next question now that all four current custom-renderer capture consumers share the local seam?
- Is the memo honest that the next issue is ownership/promotion readiness rather than another renderer proof?
- Is it correct to make this a readiness/calibration slice rather than an immediate shared-package refactor?
- Does the memo state the Critic-local coupling honestly:
  - `currentRendererCapture.ts` imports Critic-local `CaptureSelection`
  - callback typing is Critic-local
- Does the memo state the package boundary truthfully:
  - the source tree already exists at `analyzer-v2/renderers-ui`
  - Critic already consumes it from a local tarball reference
- Does the memo inspect both existing capture architectures honestly:
  - the four Critic-local helper adopters
  - the shared package's raw `config._onCapture` capture builders
- Are the four adopters really enough evidence for a promotion-readiness question, or is one more bounded proof still more defensible?
- Does the memo keep the line clear between:
  - shared runtime-resolution / selection-shell behavior
  - renderer-local identity, preview, gating, and destination compatibility behavior
- Does the memo need a sixth calibration question:
  - if promotion happens, should it replace or supplement the package's existing raw capture pattern?
- Is the verdict trichotomy calibrated enough:
  - promotion-ready
  - not ready
  - ready only for a narrower shell
- Does this slice strengthen the analyzer-v2-as-brain direction, or does it risk just moving Critic-local assumptions into a package?
- Is there a smaller or more defensible next move?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Phase_E_Current_Renderer_Selection_Emission_Shared_Seam_Promotion_Readiness_V1_Scope_Critique_2026-04-04.md`

Please include:

1. Verdict:
   - approve
   - approve with corrections
   - reject
2. The memo's strongest points
3. The weakest assumptions or overclaims
4. Code-backed findings
5. Strategic implications for the roadmap
6. Concrete corrections or reframing you recommend

Keep it specific and unsentimental.
Do not produce fluff.
