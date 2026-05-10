# Prompt For Claude: Stage 5 AOI Selection-Compose Contract Revision Scope Critique

Critique the draft memo:

- `communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md`

Your job is to test the robustness of the memo’s assumptions against the actual codebase, the recent Stage 5 memo/proof trail, and the broader analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “fix one more transient compose bug.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- refuse premature Tranche 3 generalization before the AOI exemplar is ratified honestly

So evaluate the memo both as:

1. a bounded Stage 5 repair-scope decision
2. a broader-program prioritization decision

## What to inspect

Read these docs first:

- `communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_diagnosis.md`
- `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_revision.md`
- `communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`
- `communications/PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json`
- `communications/PROOF_stage5_aoi_pack_rerun_summary_2026-03-25.json`

Then inspect the code paths the memo depends on:

Analyzer-v2:

- `src/presenter/compose_from_intent.py`
- `src/presenter/composition_source_bridge.py`
- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/renderer_contract_enforcement.py`
- `src/api/routes/presenter.py`
- `tests/test_compose_from_intent.py`
- `tests/test_analysis_product_contract.py`
- `tests/test_served_renderer_contract_policy.py`
- `tests/test_task_planner.py`

The Critic only as needed to verify the memo is right to keep host durability/identity continuity closed baseline:

- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_client.py`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`

Look through any other recent memo/report/proof files in `communications/` or `docs/` that materially affect the judgment.

## Questions to answer

1. Does the evidence support treating analyzer-side selection-backed transient compose as the first broken hop, rather than reopening host durability or identity continuity?
2. Is the proposed repair slice honestly bounded, or is it smuggling in a larger presenter/composition redesign?
3. Is the memo too confident about the likely root cause, or is it appropriately explicit about what is inference versus demonstrated fact?
4. Is the proposed implementation direction sensible:
   - prefer preserving/deterministically normalizing bridge-produced AOI structured payloads
   - avoid lossy generic re-extraction unless justified
5. Are the proposed regressions concrete enough to prove:
   - the real four-family `evolution_ready` selection shape passes
   - AOI thematic-synthesis and sin-findings no longer reference missing `structured_data` keys
   - the counted path still stays on planner-backed `compose-from-selection`
6. Is the roadmap update still honest about overall progress, or is the memo understating/overstating what this new seam means for Stage 5 and Tranche 3?
7. Is there any hidden code-path wrinkle that makes the next slice riskier, broader, or narrower than the memo claims?

## Output requirements

Write your critique to:

- `communications/REPORT_Claude_STAGE5_AOI_Selection_Compose_Contract_Revision_Scope_Critique_2026-03-25.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve after revision`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether the roadmap/progress read is now honest or still overstated.
5. Any concrete memo revisions you recommend before implementation.

Prioritize hidden assumptions, proof-discipline gaps, scope dishonesty, broader-program mis-sequencing, and codebase mismatches over general summary.
