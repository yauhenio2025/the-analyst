# Prompt For Codex: Stage 5 AOI Source-Content Identity Revision Scope Audit

Audit the new source-content-identity revision scope doc:

- `communications/MEMO_2026-03-26_stage5_aoi_source_content_identity_revision_scope.md`

Your job is to test the robustness of the assumptions behind that memo against the actual codebase, recent Stage 5 memo/proof trail, and the larger analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “patch the AOI output until the memo sounds cleaner.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- keep Tranche 3 blocked until the AOI exemplar is ratified honestly instead of by over-reading one repaired run

So assess the memo both as:

1. a bounded diagnosis/repair scope on the remaining AOI exemplar blocker
2. a broader platform-program prioritization decision

## What to inspect

Read these docs first:

- `communications/MEMO_2026-03-26_stage5_aoi_source_content_identity_revision_scope.md`
- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_completion.md`
- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_scope.md`
- `communications/MEMO_2026-03-26_stage5_aoi_local_snapshot_idempotence_revision_completion.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_recovery_completion.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_preflight_identity_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_precompose_pin_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_requests_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_session_2026-03-26.har`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

Then inspect the implementation paths the memo relies on:

Analyzer:

- `/home/evgeny/projects/analyzer-v2/src/executor/phase_runner.py`
- `/home/evgeny/projects/analyzer-v2/src/executor/context_broker.py`
- `/home/evgeny/projects/analyzer-v2/src/aoi/contract.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/composition_source_bridge.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/view_refiner.py`
- `/home/evgeny/projects/analyzer-v2/src/executor/workflow_runner.py`
- `/home/evgeny/projects/analyzer-v2/src/engines/capability_definitions/aoi_thematic_synthesis.yaml`
- `/home/evgeny/projects/analyzer-v2/src/engines/capability_history/aoi_thematic_synthesis_snapshot.json`
- `/home/evgeny/projects/analyzer-v2/src/stages/capability_composer.py`

Tests:

- `/home/evgeny/projects/analyzer-v2/tests/test_aoi_contract.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_registered_corpus_launch.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_compose_from_intent.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_presentation_api.py`

Also look through any other recent memo/report/proof files in `communications/` or relevant `docs/` that materially affect the judgment.

## Questions to answer

1. Does the codebase support the memo’s claim that the next honest move is a bounded AOI source-content identity slice rather than another host/browser slice?
2. Is the fixed-source rule technically sound:
   - diagnose against recovered `job-6ee8b0621177`
   - keep rerun authorization out of scope by default
   - require explicit closeout on whether the recovered run can be rehabilitated in place
3. Are the likely seam families real and well-bounded?
   - capability example contamination
   - context-broker amplification into downstream raw phase outputs
   - normalization / contract validation gap
   - preview/result/presentation leakage
4. Is the memo appropriately strict about explicit selected-source identity?
   - any explicit `selected_source_thinker = john_oneill` in a nominal Otto run should fail
   - but mere prose mention of O'Neill might be analytically acceptable if framed correctly
5. Is the memo missing any deeper or adjacent seam:
   - wrong source corpus in plan_data
   - wrong prior-work filtering
   - result-contract summary drift independent of normalized artifacts
   - compose/presentation layer introducing the contradiction rather than raw AOI output
6. Does the memo keep Stage 2 / Tranche 3 sequencing honest?
7. Does it put the repair burden on the real seam, or is it still too hand-wavy to guide implementation safely?
8. Does the memo distinguish clearly enough between artifact-safe recovery and prose-safe / closure-grade recovery?

## Output requirements

Write your audit to:

- `communications/REPORT_Codex_STAGE5_AOI_Source_Content_Identity_Revision_Scope_Audit_2026-03-26.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve with revisions`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether this is now the right next honest step.
5. A direct answer to whether the scope is technically bounded and implementation-worthy.
6. Any concrete memo revisions you recommend before execution.

Prioritize bugs, hidden assumptions, evidence-quality gaps, codebase mismatches, source-identity ambiguity, scope dishonesty, and broader-program mis-sequencing over general summary.
