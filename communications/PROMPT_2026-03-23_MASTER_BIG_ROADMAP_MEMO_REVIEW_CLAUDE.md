# Prompt: Review The Master Big Roadmap Memo

You are reviewing the canonical roadmap memo for the analyzer-v2 / the-critic dynamic bespoke apps program.

Primary document to review:

- `/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Your task is not to summarize it politely.
Your task is to test whether it is strategically sound, codebase-grounded, and sequenced correctly.

## Required review goals

You must do all of the following:

1. test the robustness of the memo’s assumptions
2. examine the memo in light of the larger objective:
   - analyzer-v2 should become the intelligence layer that can eventually go from task -> workflow/engine choice -> UI composition -> rendered analytical experience
3. scrutinize the memo’s claims against the live codebase
4. inspect relevant recent memos in `communications/` and `docs/` in analyzer-v2, plus the relevant master/runbook docs in the-critic
5. identify where the memo is directionally right, where it is overstating progress, where it is underestimating risk, and where the stage ordering is wrong

## Files you should inspect

At minimum, inspect:

- `/home/evgeny/projects/analyzer-v2/communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-21_round9_renderer_contract_validation_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round10_consumer_consolidation_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round12_transient_consumer_adoption_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-23_round14_aoi_transient_hot_path_launch_completion.md`
- `/home/evgeny/projects/analyzer-v2/docs/MEMO_2026-02-19_orchestrator_vision.md`
- `/home/evgeny/projects/analyzer-v2/docs/MEMO_2026-02-23_dynamic_generation_implementation.md`
- `/home/evgeny/projects/analyzer-v2/docs/SEMANTIC_VISUAL_MATCHER_PROPOSAL.md`
- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`
- `/home/evgeny/projects/the-critic/docs/STAGE9_AOI_CUTOVER_RUNBOOK.md`

Also inspect key live code seams:

- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/renderer_contract_enforcement.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/presenter.py`
- `/home/evgeny/projects/analyzer-v2/renderers-ui/src/registry.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`

If you find no relevant “Perspective” docs folder, say so explicitly instead of implying you reviewed one.

## Questions you must answer

1. Is the memo’s strategic assessment honest about what is real versus still aspirational?
2. Is the memo right that the last week’s work was directionally correct?
3. Is the memo underestimating any major missing piece on the path to the full task -> engines -> UI vision?
4. Is the stage breakdown complete enough, or is a major stage missing?
5. Is the ordering right, especially the shift from AOI MVP completion to planning/orchestration?
6. Is the memo still overfitting to AOI / the-critic in a way that could distort platform strategy?
7. What is the single biggest strategic risk if the program follows this roadmap as written?
8. What is the single highest-leverage next stage after documentary closure on rounds 13 and 14?

## Output requirements

Write a serious review memo with:

- verdict:
  - `Approve`
  - `Approve after revision`
  - `Reject`
- findings first, ordered by severity
- then a short strategic assessment
- then a section called `RECOMMENDED MEMO REVISIONS`
- then a section called `BEST NEXT STAGE`

Be direct.
Do not write fluff.

## Save requirement

You must save your review to this exact file path:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Claude_MASTER_BIG_ROADMAP_MEMO_CRITIQUE_2026-03-23.md`

Your response in chat should explicitly confirm that you saved the report there.
