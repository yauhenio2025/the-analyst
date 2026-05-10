Critique the proposed Stage 13 scope memo against the live codebase, the current roadmap position, and the larger thin-host objective.

Primary target:

- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md`

Also consult:

- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_completion.md`
- `communications/PROOF_2026-03-24_stage12_cross_workflow_renderer_law_generalization.md`
- `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_scope.md`
- `communications/MEMO_2026-03-24_stage11_rich_semantic_page_planning_completion.md`
- `communications/PROOF_2026-03-24_stage11_rich_semantic_page_planning.md`
- `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_completion.md`
- `communications/PROOF_2026-03-23_stage10_cross_workflow_source_backed_substrate.md`
- `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_completion.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- any recent memos in `communications/` or `docs/` from the past 48 hours that materially bear on host/consumer ownership, result consumption, readiness, transient launch, or thin-host direction

You must:

1. test whether the memo’s assumptions are actually supported by the current analyzer-v2 and the-critic code
2. evaluate whether Stage 13 is really the next missing seam now that Stage 12 landed, or whether the memo is underplaying:
   - remaining Stage 12 widening
   - Stage 14 lifecycle work
   - still-open consumer coupling
3. identify any place where the memo overstates how generic the current host contract already is
4. identify any place where the memo overstates how clean Stage 12 already is on authored or no-`composition_mode` restore paths
5. identify any hidden mismatch between:
   - direct analyzer calls
   - host proxy hooks
   - host-local project/auth/persistence responsibilities
6. evaluate whether the memo keeps the boundary honest between:
   - analyzer-owned intelligence
   - host-owned context, proxying, caching, and navigation
7. say explicitly if you do not find any additional relevant docs beyond the usual recent `communications/` and `docs/` materials

Prioritize inspection of:

Analyzer-v2:

- `src/api/routes/results.py`
- `src/api/routes/presenter.py`
- `src/api/routes/orchestrator.py`
- `src/analysis_products/result_contract.py`
- `src/analysis_products/source_backed_readiness.py`
- `src/presenter/compose_from_intent.py`
- `src/presenter/presentation_api.py`
- `src/presenter/renderer_contract_enforcement.py`
- `src/consumers/definitions/the-critic.json`

the-critic:

- `webapp/src/lib/boundedV2Client.ts`
- `webapp/src/lib/composeFromIntentClient.ts`
- `webapp/src/pages/GenealogyPage.tsx`
- `webapp/src/pages/AnalysisWorkspacePage.tsx`
- `webapp/src/pages/AnxietyOfInfluencePages.tsx`
- `webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `webapp/src/components/influence/AoiComposeFromIntentShell.tsx`
- `api/server.py`
- `api/middleware.py`
- any adjacent tests you need to evaluate whether the memo’s claimed host contract is already materially real or still mostly aspirational

Be explicit about these questions:

- is Stage 13 now the right next stage after Stage 12, or is the memo moving too early from renderer-law strengthening into host-contract formalization
- is the proposed Host Contract v1 concrete enough that two implementors would produce compatible code
- does the memo now distinguish explicitly enough between:
  - result/run families where `consumer_key` is request-level input
  - compose families where consumer coupling is still structurally hardcoded
- is the direct-analyzer vs host-proxy vs host-local split correct, or does the memo hide more mixed ownership than it admits
- is the memo right to keep `route-task` and `plan-task` out of required host-v1 adoption, or is that avoiding a seam that is already central
- does the current code support the claim that one shared host adapter layer can cover both AOI and genealogy without rebuilding local intelligence
- is the memo now right-sized about what host consolidation remains:
  - already-shared client/hook substrate
  - remaining contract-covered direct fetches
  - documented out-of-scope polish/visualization/provenance fetches
- is adopting `source-backed-readiness` in the AOI launch surface plus one genealogy readiness consumption case now a strong enough cross-workflow proof move
- does the memo distinguish correctly between:
  - host navigation/routing
  - orchestrator task routing
  - project identity
  - local snapshot persistence
- does the memo now make host-side surface selection explicit enough as a v1 ownership concern
- is the proof bar strong enough without a second consumer, or does it need a harder generic-host demonstration

Output requirements:

- save your critique to:
  - `communications/REPORT_Claude_STAGE13_Minimal_Generic_Host_Contract_Scope_Critique_2026-03-24.md`
- begin with a verdict:
  - `Approve`
  - `Approve after revision`
  - `Do not approve`
- findings first
- summaries second
- be concrete about:
  - code seams
  - owner splits
  - host/analyzer contract mismatches
  - hidden assumptions
  - proof weaknesses

Do not modify code.
