# Prompt: Audit The Master Big Roadmap Memo Against The Codebase

You are auditing the canonical roadmap memo for the analyzer-v2 / the-critic dynamic bespoke apps program.

Primary document to audit:

- `/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Your job is to stress-test the memo against reality.
Do not just paraphrase it.
Check whether its claims, stage ordering, and missing-piece analysis are actually supported by the current code and memo trail.

## Required audit goals

You must:

1. test the robustness of the assumptions behind the memo
2. examine whether the memo fits the bigger-picture goal:
   - analyzer-v2 eventually becomes the planning and composition brain
   - consumer apps become minimal host shells
3. scrutinize the memo’s claims against the actual codebase
4. review relevant recent memos in analyzer-v2 and the-critic
5. identify concrete mismatches between the memo and the live repos

## Files to inspect

At minimum, inspect:

- `/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
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

Inspect these code seams directly:

- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/presenter.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/views.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/workflows.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/renderer_contract_enforcement.py`
- `/home/evgeny/projects/analyzer-v2/renderers-ui/src/registry.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/index.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/api/server.py`

If you find no relevant “Perspective” docs folder in either repo, state that explicitly.

## Specific audit questions

1. Which claims in the memo are strongly supported by code?
2. Which claims are directionally right but overstated?
3. Is the memo’s estimate that the program is much farther on downstream composition than upstream planning correct?
4. Does the stage breakdown miss any concrete platform requirement?
5. Are any proposed stages in the wrong order based on the code as it exists?
6. Is the memo too optimistic about “minimal app expectations,” given what the-critic still owns?
7. What concrete code seams prove the platform is still AOI-bounded?
8. What concrete code seams show the next real problem is planning/orchestration rather than more renderer/consumer work?

## Output requirements

Write an audit memo with these sections:

- `VERDICT`
- `FINDINGS`
- `CODE-GROUNDED CORRECTIONS`
- `WHAT THE MEMO GETS RIGHT`
- `BEST NEXT STAGE`

Findings should be ordered by severity and should cite file paths where useful.

Be blunt and specific.
If the memo is right, say so.
If a claim is unsupported, say so.

## Save requirement

You must save the audit to this exact file path:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Codex_MASTER_BIG_ROADMAP_MEMO_AUDIT_2026-03-23.md`

Your response in chat should explicitly confirm that you saved the report there.
