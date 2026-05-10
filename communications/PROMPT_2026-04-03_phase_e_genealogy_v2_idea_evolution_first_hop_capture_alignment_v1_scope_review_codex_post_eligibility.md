# Prompt For Fresh Codex Session

Please audit this scope memo critically:

- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_scope.md`

Do not assume the memo is correct.
Test its assumptions against the actual code, the just-landed analyzer-side affordance-eligibility prerequisite, the already-landed current-renderer helper seam, the broader roadmap, and the analyzer-v2-as-brain objective.

## Required tasks

1. Read the scope memo in full.
2. Read the immediate recent context:
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`
   - `communications/REPORT_Codex_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Audit_2026-04-03.md`
   - `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Critique_2026-04-03.md`
3. Check the memo against the relevant host/runtime code:
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.test.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.test.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
4. Check the prerequisite analyzer-side contract truth too:
   - `/home/evgeny/projects/analyzer-v2/src/presenter/first_hop_affordance.py`
   - `/home/evgeny/projects/analyzer-v2/tests/test_first_hop_affordance.py`
   - `/home/evgeny/projects/analyzer-v2/src/views/definitions/genealogy_idea_evolution.json`
5. Read relevant roadmap context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
6. Look through any other recent memo in `communications/` that you think materially affects whether this is the right next step.

## Questions to answer

- Is `genealogy_idea_evolution` now really the smallest honest next bounded step after the analyzer-side eligibility blocker was removed?
- Does the memo describe the current host gap accurately:
  - local `captureMode && onCapture`
  - current reads only of `_captureJobId` and `_captureViewKey`
  - hardcoded `source_type`
  - hardcoded title composition
  - missing `source_workflow_key`
  - missing `entity_id`
- Does the memo now describe the full implementation delta honestly, including the five additional threaded config/runtime reads this alignment will start consuming?
- Is it correct to keep capture coverage limited to existing idea-card buttons only?
- Is reusing `currentRendererCapture.ts` on this surface the right move, or would that overfit the helper?
- Are `requireWorkflowKey: true` and `requireJobId: true` the right runtime requirements here?
- Is `entity_id = idea.idea_id` an honest emitted identity claim, or does that overstate what this surface proves?
- Does the memo make clear that `entity_id` should be taken directly from `idea.idea_id`, not from `_captureEntityId` fallback?
- Does the memo state correctly that `source_type` should still resolve to the same runtime value (`\"genealogy\"`) and that the improvement is composability rather than behavior change?
- Does the memo describe the `context_title` change accurately, including both the human-readable-name shift and the separator shift?
- Does the memo instruct the implementor to pass `title` into `buildCurrentRendererCaptureSelection(...)` rather than composing `context_title` locally?
- Does the memo stay narrow enough about what this slice would *not* solve?
- Is the browser-proof boundary still honest, with the no-affordance negative staying in unit/mock coverage rather than the untouched live page?
- Does the memo acknowledge that the renderer test plan requires fresh component-test scaffolding rather than a small additive extension of the existing normalization test?
- Is there a smaller or cleaner next move than this?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Post_Eligibility_Scope_Audit_2026-04-03.md`

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
