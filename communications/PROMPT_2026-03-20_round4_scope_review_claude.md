# Prompt: Claude Critique for Round 4 Adaptive Surface Suite Scope

Review this proposed next-stage scope:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-20_round4_adaptive_surface_suite_scope.md`

Treat this as a strategic and architectural critique grounded in the real codebase and memo trail, not as an abstract brainstorming exercise.

## Program Context To Read

Read these first:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-16_aoi_strategic_reassessment_after_parity_work.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-16_beautiful_by_default_surfaces_platform_gap.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_post_stage9_next_steps.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-19_thin_consumer_platformization_round1.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-20_round2_bounded_dynamic_composition_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-20_round3_adaptive_surface_family.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-20_round3_adaptive_surface_family_completion.md`
- `/home/evgeny/projects/the-critic/communications/NEXT_SESSION_DYNAMIC_COMPOSITION_AUDIT.md`

Then inspect the relevant implementation seams in at least:

- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/decision_trace.py`
- `src/presenter/presentation_api.py`
- `src/views/definitions/genealogy_conditions.json`
- `src/views/definitions/genealogy_cop_enabling_conditions.json`
- `src/views/definitions/genealogy_cop_constraining_conditions.json`
- `src/views/definitions/genealogy_cop_path_dependencies.json`
- `src/views/definitions/genealogy_cop_alternative_paths.json`
- `src/views/definitions/genealogy_cop_counterfactual.json`
- `src/views/definitions/genealogy_cop_synthesis.json`
- `src/views/definitions/genealogy_cop_unacknowledged_debts.json`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`

## What I Want You To Test

Please challenge the memo on these questions:

1. Is round 4 genuinely the right next stage after the round-3 proof, or is there a more important strategic gap still ahead of it?
2. Does a two-surface adaptive suite meaningfully advance the "beautiful-by-default" platform thesis, or is it still too close to infrastructure proofing?
3. Is `genealogy_conditions` the right second surface, or would `genealogy_portrait`, `genealogy_tactics`, or another target be higher leverage?
4. Is the memo right to keep round 4 deterministic and proof-bounded rather than reopening dormant refinement / recommendation machinery?
5. Is the proposed suite still bounded enough to stay honest, or is it already trying to prove too much?
6. Are the two proposed conditions families concrete enough to count as genuinely different surface contracts, or do they still risk collapsing into "same surface with different labels"?
7. Is the suite-level trace/inspectability requirement the right shape?

## Output Requirements

Write your critique to:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Claude_Round4_Adaptive_Surface_Suite_Scope_Critique_2026-03-20.md`

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

- Do not implement code.
- Do not write a replacement plan unless the current memo is fundamentally wrong.
- Ground your critique in the actual repositories and memo trail, not generic product-strategy language.
- If you think the memo should choose a different second adaptive surface, name the exact better target and justify it concretely.
