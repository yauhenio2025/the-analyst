# Prompt: Audit The Stage 7 Planner-To-Presentation Bridge Scope Memo Against The Codebase

You are auditing the next stage-specific scope memo for the analyzer-v2 dynamic bespoke-apps program.

Primary memo:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-23_stage7_planner_to_presentation_bridge_scope.md`

Canonical roadmap:

- `/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Your job is to stress-test the memo against the current code and recent memo trail.
Do not just paraphrase it.

## Audit goals

You must:

1. test the robustness of the assumptions behind the memo
2. examine whether the stage fits the larger objective:
   - analyzer-v2 as the planning/composition brain
   - consumers as minimal hosts
3. scrutinize the memo’s claims against the actual codebase
4. review relevant recent memos in analyzer-v2 and the-critic
5. identify concrete mismatches between the memo and live code

## Files to inspect

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
- `/home/evgeny/projects/analyzer-v2/src/executor/plan_context.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/run_contract.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`

If you find no relevant `Perspective` docs folder in either repo, state that explicitly.

## Specific audit questions

1. Does the memo correctly describe the current gap as a planner/result-to-composition bridge rather than a greenfield planning problem?
2. Is the memo right to keep the stage analyzer-owned and consumer-light?
3. Is the memo too conservative by keeping the stage AOI-only?
4. Is leaving the public `profile` request shape in place a smart bounded move, or does it preserve the wrong coupling?
5. Does the proposed `compose-from-source-v2` resolver/version bump make sense?
6. What concrete code seams prove the current `compose-from-source` path is still hardcoded and missing a formal bridge contract?
7. What concrete code seams show that a meaningful host contract already exists and should influence this stage?
8. What is the single biggest thing the memo still gets wrong or leaves underspecified?

## Output requirements

Write an audit memo with these sections:

- `VERDICT`
- `FINDINGS`
- `CODE-GROUNDED CORRECTIONS`
- `WHAT THE MEMO GETS RIGHT`
- `BEST NEXT MOVE`

Findings should be ordered by severity and should cite file paths where useful.

Be blunt and specific.

## Save requirement

You must save the audit to this exact file path:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Codex_STAGE7_Planner_To_Presentation_Bridge_Scope_Audit_2026-03-23.md`

Your response in chat should explicitly confirm that you saved the report there.
