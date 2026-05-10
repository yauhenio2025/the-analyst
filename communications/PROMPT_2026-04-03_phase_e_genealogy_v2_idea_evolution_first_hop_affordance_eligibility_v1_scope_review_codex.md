# Prompt For Fresh Codex Session

Please audit this scope memo critically:

- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_scope.md`

Do not assume the memo is correct.
Test its assumptions against the actual analyzer code, the current host/helper code, the broader roadmap, and the analyzer-v2-as-brain objective.

## Required tasks

1. Read the scope memo in full.
2. Read the immediate recent context:
   - `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_scope.md`
   - `communications/REPORT_Codex_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Audit_2026-04-03.md`
   - `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Critique_2026-04-03.md`
3. Check the memo against the relevant analyzer/presenter code:
   - `src/presenter/first_hop_affordance.py`
   - `src/presenter/presentation_api.py`
   - `src/presenter/compose_from_intent.py`
   - `src/views/definitions/genealogy_idea_evolution.json`
   - any nearby analyzer tests needed to verify current affordance eligibility
4. Check the memo against the relevant host/runtime code:
   - `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx`
5. Read relevant roadmap context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Is the blocker diagnosis correct that `genealogy_idea_evolution` is not first-hop-affordance-eligible today?
- Is a small analyzer-side eligibility slice really the smallest honest next move?
- Is the memo right to reject a global `concept_synthesis` allowlist broadening?
- Is the implementation site calibrated correctly:
  - second branch in `derive_first_hop_affordance(...)`
  - not hidden inside `is_migrated_analytical_leaf_payload()`
- Is the proposed view-specific or view+engine-specific eligibility rule calibrated enough?
- Is the workflow check already sufficiently handled by the existing `enabled` gate upstream?
- Should this eligibility inherit across both transient and job-backed presenter paths through the shared derivation seam, while keeping mandatory end-to-end proof only on the job-backed line?
- Does the memo name the new view-key coupling honestly as a design precedent?
- Should the memo include an explicit consolidation expectation if a second `concept_synthesis` view later proves eligibility?
- Is the memo honest enough about what stays out of scope:
  - no host renderer change
  - no `entity_id`
  - no backend change
  - no specialized family
- Is there a smaller or cleaner next move than this?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Affordance_Eligibility_V1_Scope_Audit_2026-04-03.md`

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
