# Prompt For Fresh Claude Session

Please review this scope memo critically:

- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_scope.md`

Do not assume the memo is correct.
Test whether its assumptions are calibrated against:

- the just-landed analyzer-side affordance-eligibility prerequisite
- the already-landed `currentRendererCapture` helper seam
- the actual Critic `IdeaEvolutionRenderer` code
- the broader roadmap and the analyzer-v2-as-brain objective

## What to do

1. Read the scope memo in full.
2. Read the immediate recent context:
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`
   - `communications/REPORT_Codex_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Audit_2026-04-03.md`
   - `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Critique_2026-04-03.md`
3. Scrutinize the memo against the actual codebase, especially:
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.test.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.test.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/analyzer-v2/src/presenter/first_hop_affordance.py`
   - `/home/evgeny/projects/analyzer-v2/src/views/definitions/genealogy_idea_evolution.json`
4. Read relevant roadmap context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
5. Look through any other recent memo in `communications/` that you think materially affects whether this is the right next step.

## What to focus on

- Does the scope memo describe the current `IdeaEvolutionRenderer` gap honestly now that analyzer-side affordance eligibility is complete?
- Is it right to treat this as the next bounded non-AOI follow-on after the eligibility prerequisite landed?
- Is the proposed use of `currentRendererCapture.ts` narrow and honest, or is it starting to overfit the helper into fake generic law?
- Does the memo now name the full implementation delta honestly, including the additional config/runtime reads rather than framing this as only a small gate swap?
- Is `entity_id = idea.idea_id` a sound scope assumption or an overclaim?
- Does the memo make clear that `entity_id` should be pinned directly to `idea.idea_id`, not derived from `_captureEntityId` fallback?
- Does the memo describe `source_type` correctly as a composability improvement with the same runtime value, not a behavior change?
- Does the memo describe the `context_title` delta accurately:
  - human-readable view name instead of raw slug
  - `:` separator instead of `>`
- Does the memo state clearly that `buildCurrentRendererCaptureSelection(...)` should receive `title`, not a prebuilt `context_title` string?
- Is the memo calibrated enough about what stays out of scope:
  - no analyzer changes
  - no backend change
  - no read-side truth surfacing
  - no generic renderer-package law
- Is the proposed browser proof boundary honest, with the negative path staying in unit/mock coverage rather than the untouched live page?
- Does the memo acknowledge that the renderer test plan requires fresh component-test scaffolding, not just expansion of the existing normalization test?
- Is there a smaller or more defensible next move?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Post_Eligibility_Scope_Critique_2026-04-03.md`

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
