# Prompt For Claude: Review Stage 13 Second-Slice Harder Generic Host Proof Scope

You are reviewing a newly drafted scope memo, not implementing code.

Your task:

1. read the new scope memo:
   - `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_scope.md`
2. read the recent canonical context:
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
   - `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_completion.md`
   - `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md`
   - `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_completion.md`
   - `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_scope.md`
   - `communications/MEMO_2026-03-24_stage11_rich_semantic_page_planning_completion.md`
   - `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
   - `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
3. inspect the live codebase claims relevant to this memo, especially:
   - `~/projects/the-critic/webapp/src/lib/hostContractV1.ts`
   - `~/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
   - `~/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts`
   - `~/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts`
   - `~/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
   - `~/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
   - `~/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
   - `~/projects/the-critic/api/server.py`
   - `src/presenter/compose_from_intent.py`
   - `src/analysis_products/source_backed_readiness.py`

Your review goals:

- test whether the memo is correct that the next phase should still be Stage 13 second slice rather than Stage 14 lifecycle
- test whether the memo’s “harder generic-host proof” target is specific enough and truly distinct from the first Stage 13 slice
- examine whether the claimed remaining host/runtime gaps are real in code
- pressure-test whether the memo understates or overstates existing generic-host capability
- assess whether the proposed next phase is aligned with the larger analyzer-as-brain / thin-host objective
- identify any missing proof requirements, hidden coupling, or sequencing mistakes

Deliverable requirements:

- produce a critique memo with an explicit verdict:
  - `Approve`
  - `Approve after revision`
  - `Reject`
- findings should focus on:
  - architectural gaps
  - false assumptions
  - codebase mismatches
  - sequencing problems
  - proof-bar weaknesses
- if you think Stage 14 lifecycle is actually the next honest move, say so explicitly and justify it
- if you think the vision is already sufficiently achieved and no next phase is warranted, say so explicitly and justify it

Save your output to:

- `communications/REPORT_Claude_STAGE13_Second_Slice_Harder_Generic_Host_Proof_Scope_Critique_2026-03-24.md`

Do not modify code. Only write the review artifact.
