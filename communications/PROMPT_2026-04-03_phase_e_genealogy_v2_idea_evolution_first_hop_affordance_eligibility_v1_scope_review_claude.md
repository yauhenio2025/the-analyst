# Prompt For Fresh Claude Session

Please review this scope memo critically:

- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_scope.md`

Do not assume the memo is correct.
Test whether its assumptions are calibrated against the analyzer code, the current host/helper code, the broader roadmap, and the analyzer-v2-as-brain objective.

## What to do

1. Read the scope memo in full.
2. Read the immediate recent context:
   - `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_scope.md`
   - `communications/REPORT_Codex_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Audit_2026-04-03.md`
   - `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Critique_2026-04-03.md`
3. Scrutinize the memo against the actual codebase, especially:
   - `src/presenter/first_hop_affordance.py`
   - `src/presenter/presentation_api.py`
   - `src/presenter/compose_from_intent.py`
   - `src/views/definitions/genealogy_idea_evolution.json`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx`
4. Read relevant roadmap context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
5. Look through any other recent memo in `communications/` that you think materially affects whether this is the right next step.

## What to focus on

- Does the memo identify the real blocker honestly?
- Is an analyzer-side eligibility prerequisite the right next move before host alignment?
- Is the proposed scope narrow enough to avoid a dishonest global `concept_synthesis` policy expansion?
- Does the memo place the new rule in the right spot:
  - a second branch in `derive_first_hop_affordance(...)`
  - not inside `is_migrated_analytical_leaf_payload()`
- Is the workflow check already sufficiently handled by the existing `enabled` gate upstream?
- Should the memo say more clearly that both transient and job-backed paths inherit the rule through the shared derivation seam, while only the job-backed line needs mandatory end-to-end proof right now?
- Does the memo name the view-key coupling honestly as a deliberate new precedent?
- Should the memo include an explicit consolidation expectation if a second `concept_synthesis` view later proves eligibility?
- Is the memo calibrated enough about what remains out of scope:
  - no host renderer change
  - no `entity_id`
  - no backend change
  - no specialized family
- Is there a smaller or more defensible next move?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Affordance_Eligibility_V1_Scope_Critique_2026-04-03.md`

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
