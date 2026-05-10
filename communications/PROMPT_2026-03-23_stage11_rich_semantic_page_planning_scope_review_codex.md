Audit the proposed Stage 11 scope memo against the live codebase and the larger roadmap.

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
- any recent communications/docs memos that materially bear on compose-from-intent, semantic planning, renderer contracts, or thin-host direction

You must:

1. test whether the memo’s assumptions are actually supported by the current code
2. evaluate whether the memo fits the larger program objective rather than only the local AOI path
3. identify any places where the memo overstates how ready the current presenter/page-planning substrate already is
4. identify any hidden AOI/the-critic coupling the memo is underplaying
5. identify any stage-ordering mistake or false symmetry in the proposed Stage 11 slice
6. say explicitly if you find no additional relevant docs beyond the usual `docs/` and `communications/` materials

Prioritize inspection of:

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
- any the-critic code that materially bears on the host-contract or AOI-coupling claims

Be explicit about these questions:

- is the proposed Stage 11 seam really “hierarchical semantic page planning,” or is the memo just renaming a slightly richer compose-from-intent allowlist?
- does the repo actually have enough reusable hierarchy/scaffold law to support this stage honestly, or would the planner still be inventing structure the presenter does not really own?
- is AOI-first the right bounded implementation target, or does it defer the cross-workflow proof burden too far?
- is the semantic matcher requirement concrete enough to be implemented inside analyzer-v2 without quietly depending on the external visualizer proposal?
- is the proof bar strong enough to distinguish semantic planning from generic layout churn?
- does the revised memo now describe the transient-host requirement honestly, or is it still smuggling Stage 13 host work into Stage 11 without naming it?
- are the AOI-local semantic rules concrete enough to drive real planning now, given the absence of AOI `semantic_visual_intent`

Output requirements:

- save your audit to:
  - `communications/REPORT_Codex_STAGE11_Rich_Semantic_Page_Planning_Scope_Audit_2026-03-23.md`
- begin with a verdict:
  - `Approve`
  - `Approve after revision`
  - `Do not approve`
- findings first
- keep summaries secondary
- be explicit about:
  - code seams
  - contract mismatches
  - hidden assumptions
  - proof requirements
  - any place where the memo is calling reusable substrate what is still AOI-specific plumbing

Do not modify code.
