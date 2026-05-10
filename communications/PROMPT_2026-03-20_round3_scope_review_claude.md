# Prompt: Claude Critique for Round 3 Adaptive Surface Family Scope

Review this proposed next-stage scope:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-20_round3_adaptive_surface_family_scope.md`

Treat this as a strategic and architectural critique grounded in the real codebase, not as an abstract brainstorming exercise.

## Program Context To Read

Read these first:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-16_aoi_strategic_reassessment_after_parity_work.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-16_beautiful_by_default_surfaces_platform_gap.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_post_stage9_next_steps.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-19_thin_consumer_platformization_round1.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_round2_bounded_dynamic_composition_scope.md`
- `/home/evgeny/projects/the-critic/communications/NEXT_SESSION_DYNAMIC_COMPOSITION_AUDIT.md`

Then inspect the relevant implementation seams in:

- `src/presenter/presentation_api.py`
- `src/presenter/decision_trace.py`
- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/presentation_bridge.py`
- `src/presenter/store.py`
- `src/presenter/variant_generator.py`
- `src/views/definitions/`
- `src/transformations/definitions/`
- `the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `the-critic/webapp/src/components/V2TabContent.tsx`

## What I Want You To Test

Please challenge the memo on these questions:

1. Is this genuinely the right next stage after the last 96 hours of work, or is there a more important missing step before it?
2. Does this stage actually advance the platform from "predictable-by-default" toward "beautiful-by-default," or is it still too infrastructure-shaped?
3. Is `genealogy_relationship_landscape` the right proving target, or would `dynamic_genealogy_trajectory`, `genealogy_conditions`, or another surface be higher leverage?
4. Is the memo right to prefer deterministic family selection over reactivating dormant refinement / recommendation machinery?
5. Is the proof too small to matter, or too large to stay honest?
6. What would make this memo tighter, safer, or more strategically correct?

## Output Requirements

Write your critique to:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Claude_Round3_Adaptive_Surface_Family_Scope_Critique_2026-03-20.md`

Use this structure:

1. `Summary`
   - 1 short paragraph with your overall judgment
2. `Corrections Needed`
   - flat list, most important first
3. `What The Memo Gets Right`
4. `Recommended Scope Adjustments`
5. `Verdict`
   - say whether you would approve this as the next scoping memo after revision, approve as-is, or redirect it entirely

## Important Constraints

- Do not write implementation code.
- Do not produce a full replacement plan unless the current memo is fundamentally wrong.
- Ground your critique in the actual repositories and memo trail, not generic product-strategy language.
- If you think the memo should choose a different proving target, say exactly which one and why.
