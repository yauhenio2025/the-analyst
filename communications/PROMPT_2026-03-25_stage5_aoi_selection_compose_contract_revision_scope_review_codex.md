# Prompt For Codex: Stage 5 AOI Selection-Compose Contract Revision Scope Audit

Audit the draft memo:

- `communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md`

Your job is to test the robustness of the memo’s assumptions against the actual codebase and recent Stage 5 memo/proof trail, and judge whether it is the right immediate next step given the larger analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “repair one more AOI compose failure.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- keep Tranche 3 blocked until the AOI exemplar is ratified honestly

So assess the memo both as:

1. a bounded Stage 5 operational/implementation scope
2. a platform-program prioritization decision

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

The Critic only as needed to verify the memo’s claim that host durability/identity continuity should remain closed baseline:

- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_client.py`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`

Look through any other recent memo/report/proof files in `communications/` or `docs/` that materially affect the judgment.

## Questions to answer

1. Does the codebase evidence support treating analyzer-side `compose-from-selection` contract alignment as the first broken hop?
2. Is the memo right to keep host warm-snapshot durability and identity continuity out of scope by default?
3. Is the proposed bounded implementation direction technically coherent, or is it masking a broader transient compose design problem?
4. Are the regression obligations concrete enough to prove:
   - the real four-family `evolution_ready` selection shape now returns `200`
   - the repaired AOI thematic-synthesis and sin-findings transient views are contract-valid
   - the counted path still uses planner-backed `compose-from-selection` with preserved `source_v2_job_id`
5. Is the rerun branch rule still strict enough to stop dishonest consumption of the frozen Stage 5 pack?
6. Does the revised roadmap now tell the truth about how far along the program really is?
7. Is there any hidden dependency or code-path wrinkle that makes the next slice riskier, narrower, or broader than the memo claims?

## Output requirements

Write your audit to:

- `communications/REPORT_Codex_STAGE5_AOI_Selection_Compose_Contract_Revision_Scope_Audit_2026-03-25.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve with revisions`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether the program should:
   - keep the roadmap order
   - keep Tranche 3 blocked
   - treat the new progress read as honest or still overstated
5. Any concrete revisions you recommend before implementation.

Prioritize bugs, risks, hidden assumptions, scope dishonesty, proof-quality weaknesses, and broader-program mis-sequencing over general summary.
