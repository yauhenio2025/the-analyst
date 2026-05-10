# Prompt: Review The Stage 7 Planner-To-Presentation Bridge Scope Memo

You are reviewing the next stage-specific scope memo for the analyzer-v2 dynamic bespoke-apps program.

Primary memo:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-23_stage7_planner_to_presentation_bridge_scope.md`

Canonical roadmap context:

- `/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Your task is to test whether the stage memo is strategically sound, codebase-grounded, and correctly sequenced relative to the roadmap.

## Review goals

You must:

1. test the robustness of the assumptions behind the stage memo
2. examine whether this stage really is the right next stage in light of the bigger objective:
   - analyzer-v2 as the planning + composition brain
   - consumer apps as minimal host shells
3. scrutinize the stage memo’s claims against the live codebase
4. inspect relevant recent memos in analyzer-v2 and the-critic
5. identify where the memo is right, where it is over-scoped, and where it is still under-scoped

## Files you should inspect

At minimum, inspect:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-23_stage7_planner_to_presentation_bridge_scope.md`
- `/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `/home/evgeny/projects/analyzer-v2/communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-23_round14_aoi_transient_hot_path_launch_completion.md`
- `/home/evgeny/projects/analyzer-v2/docs/MEMO_2026-02-19_orchestrator_vision.md`
- `/home/evgeny/projects/analyzer-v2/docs/MEMO_2026-02-23_dynamic_generation_implementation.md`
- `/home/evgeny/projects/analyzer-v2/docs/SEMANTIC_VISUAL_MATCHER_PROPOSAL.md`
- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`

Inspect these code seams directly:

- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/adaptive_planner.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/pipeline.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/pipeline_schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/objectives/definitions/influence_thematic.json`
- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/run_contract.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`

If you find no relevant “Perspective” docs folder, say so explicitly.

## Questions you must answer

1. Is this actually the right next stage after the roadmap revision?
2. Is the memo right to keep this stage AOI-only, or should it force a second-workflow bridge now?
3. Is keeping the public `compose-from-source` route stable the right bounded call?
4. Is the proposed bridge seam correctly located in analyzer-v2 rather than the consumer?
5. Is keeping `profile` for this stage the right scoping decision, or does that preserve too much old coupling?
6. Does the memo define the bridge contract concretely enough to write an execution plan?
7. What is the biggest missing failure mode or architectural risk in the memo?
8. What one revision would most improve the memo before planning?

## Output requirements

Write a review memo with:

- verdict:
  - `Approve`
  - `Approve after revision`
  - `Reject`
- findings first, ordered by severity
- then a short strategic assessment
- then a section called `RECOMMENDED MEMO REVISIONS`
- then a section called `BEST NEXT MOVE`

Be direct.
Do not write fluff.

## Save requirement

You must save your review to this exact file path:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Claude_STAGE7_Planner_To_Presentation_Bridge_Scope_Critique_2026-03-23.md`

Your response in chat should explicitly confirm that you saved the report there.
