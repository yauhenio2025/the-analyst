Review the proposed Stage 11 scope memo as a skeptical strategic reviewer.

Primary target:

- `communications/MEMO_2026-03-23_stage11_rich_semantic_page_planning_scope.md`

Also consult:

- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md`
- `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_completion.md`
- `communications/PROOF_2026-03-23_stage10_cross_workflow_source_backed_substrate.md`
- `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_completion.md`
- `communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/REPORT_Claude_MASTER_BIG_ROADMAP_MEMO_CRITIQUE_2026-03-23.md`
- `communications/REPORT_Codex_MASTER_BIG_ROADMAP_MEMO_AUDIT_2026-03-23.md`
- `docs/SEMANTIC_VISUAL_MATCHER_PROPOSAL.md`
- recent communications/docs memos that materially bear on compose-from-intent, page planning, semantic surface selection, renderer law, or thin-host direction

Inspect the codebase claims against the live code, especially:

- `src/presenter/compose_from_intent.py`
- `src/presenter/view_refiner.py`
- `src/presenter/scaffold_contracts.py`
- `src/presenter/decision_trace.py`
- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/presentation_api.py`
- `src/presenter/schemas.py`
- `src/views/schemas.py`
- `src/views/patterns/tab_with_children.json`
- `src/views/patterns/accordion_sections.json`
- `src/views/patterns/timeline_sequential.json`
- `src/views/generator.py`
- `src/analysis_products/source_backed_readiness.py`
- `src/api/routes/presenter.py`
- `src/api/routes/results.py`
- `src/engines/definitions/`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/transientComposeAdapters.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/index.ts`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- any relevant the-critic seams that bear on the host-coupling claim

Your job:

1. test the robustness of the memo’s assumptions
2. examine the memo in light of the bigger-picture objective:
   - analyzer-v2 as the intelligence layer for dynamic bespoke analytical apps
3. scrutinize the memo’s claims against the current presenter/view/results code
4. identify what is right
5. identify what is overstated, missing, wrongly ordered, or strategically risky
6. say explicitly if you find no additional relevant docs beyond the usual `docs/` and `communications/` materials

Be especially skeptical about:

- whether AOI-first is the right bounded shape, or whether the memo is ducking the harder cross-workflow question too long
- whether the proposed hierarchical planner is concrete enough to implement rather than just renaming “richer layout”
- whether the semantic matcher layer is specified tightly enough to be real inside analyzer-v2 rather than hand-waving toward the separate proposal
- whether the memo is honestly distinguishing:
  - hierarchy law
  - renderer-law expansion
  - scaffold semantics
  - host-contract concerns
- whether adding `tab_with_children` plus one more pattern family is enough to justify the roadmap’s “richer semantic surfaces” claim
- whether the stage is underplaying the depth of current AOI coupling in `compose_from_intent.py`
- whether the memo is now drawing the host boundary honestly:
  - narrow transient-host work allowed
  - universal host contract still deferred
- whether the semantic matcher rules are concrete enough for current AOI sections, given that AOI engines do not presently define `semantic_visual_intent`

Output requirements:

- save your critique to:
  - `communications/REPORT_Claude_STAGE11_Rich_Semantic_Page_Planning_Scope_Critique_2026-03-23.md`
- begin with a verdict:
  - `Approve`
  - `Approve after revision`
  - `Do not approve`
- focus on findings first, ordered by importance
- be concrete about:
  - code seams
  - memo assumptions
  - bigger-picture fit
  - stage-ordering risks
  - proof/evidence requirements
- distinguish:
  - strategic issues
  - architectural/codebase issues
  - proof/evidence issues

Do not modify code.
