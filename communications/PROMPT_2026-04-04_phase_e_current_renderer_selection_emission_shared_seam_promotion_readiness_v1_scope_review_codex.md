# Prompt For Fresh Codex Session

Please audit this scope memo critically:

- `communications/MEMO_2026-04-04_phase_e_current_renderer_selection_emission_shared_seam_promotion_readiness_v1_scope.md`

Do not assume the memo is correct.
Test its assumptions against the actual code, the just-landed four-adopter helper state, the real shared package source tree and package-side capture architecture, the broader roadmap, and the analyzer-v2-as-brain objective.

## Required tasks

1. Read the scope memo in full.
2. Read the immediate recent context:
   - `communications/MEMO_2026-04-04_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_completion.md`
   - `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Post_Eligibility_Scope_Critique_2026-04-03.md`
3. Check the memo against the relevant host/runtime code:
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
4. Check the shared package source and capture architecture too:
   - `/home/evgeny/projects/the-critic/webapp/package.json`
   - `/home/evgeny/projects/analyzer-v2/renderers-ui/package.json`
   - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/AccordionRenderer.tsx`
   - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardRenderer.tsx`
   - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardGridRenderer.tsx`
   - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx`
5. Read relevant roadmap context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
   - `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_scope.md`
   - `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md`
6. Look through any other recent memo in `communications/` that you think materially affects whether this is the right next step.

## Questions to answer

- Is this really the right next bounded Phase E question after `IdeaEvolutionRenderer` alignment landed?
- Does the memo describe the current seam honestly:
  - one local helper
  - four adopters
  - still-divergent local identity / preview / gating behavior
- Does the memo state the package-boundary facts correctly:
  - source tree already exists in `analyzer-v2/renderers-ui`
  - Critic already consumes it from a local tarball reference
- Is the helper's Critic-local `CaptureSelection` type dependency a real blocker to promotion, a manageable coupling, or evidence that the helper should remain local?
- Is it correct to treat this as a readiness / calibration slice instead of immediate shared-package extraction?
- Does the memo inspect the second capture architecture already living in the shared package, or does it under-scope the comparison set?
- Are the current helper options still honest:
  - `requireWorkflowKey`
  - `requireJobId`
- Would promotion now likely force new renderer-specific flags or branches?
- Should promotion, if it happens, replace or supplement the package's existing raw `config._onCapture` capture pattern?
- Is the memo right to ask for a verdict among:
  - promotion-ready
  - not ready; keep local
  - ready only for a narrower shell
- Would this next step actually strengthen host-thinning evidence, or risk moving Critic-local assumptions into a package and calling that generality?
- Is there a smaller or cleaner next move than this?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_Current_Renderer_Selection_Emission_Shared_Seam_Promotion_Readiness_V1_Scope_Audit_2026-04-04.md`

Please include:

1. Verdict:
   - approve
   - approve with corrections
   - reject
2. The memo's strongest code-backed points
3. The memo's weakest or overstated assumptions
4. Any factual discrepancies you found
5. What this would change for the larger roadmap
6. The most defensible next move after this memo

Be concrete.
Use code-backed reasoning.
Avoid fluff.
