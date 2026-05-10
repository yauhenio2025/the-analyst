# Prompt For Claude: Stage 5 AOI Source-Content Identity Revision Scope Critique

Critique the new source-content-identity revision scope doc:

- `communications/MEMO_2026-03-26_stage5_aoi_source_content_identity_revision_scope.md`

Your job is to test the robustness of the assumptions behind that memo against the actual codebase, the recent Stage 5 memo/proof trail, and the broader analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “fix a weird John O'Neill string.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- keep Tranche 3 blocked until the AOI exemplar is ratified honestly rather than by inference

So evaluate the memo both as:

1. a bounded diagnosis/repair scope for the remaining AOI exemplar blocker
2. a broader program-prioritization decision about what still must happen before Stage 2 can close

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

Then inspect the code paths the memo relies on:

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

1. Is the memo right that the next honest move is now analyzer-side/source-content diagnosis/repair rather than more host/browser work?
2. Is keeping `job-6ee8b0621177` as the fixed diagnosis source still the honest sequencing choice?
3. Does the memo distinguish clearly enough between:
   - hard selected-source identity contradiction
   - analytically acceptable mention of John O'Neill as an intermediary interpreter
   - mere preview/example leakage
4. Are the proposed seam families technically plausible?
   - capability-definition sample/example contamination
   - context-broker amplification from contaminated Phase 1.0 raw output into Phases 2.0-4.0
   - AOI normalization not defending against contradictory explicit identity
   - raw phase preview persistence leaking contradiction into result/presentation surfaces
5. Is the memo too broad or too narrow about likely repair loci?
6. Does the memo keep the roadmap honest:
   - browser proof already passed structurally
   - Stage 2 still open
   - Tranche 3 still blocked
7. Does the memo force an explicit answer on whether the recovered run can be rehabilitated in place, or whether a fresh rerun becomes necessary after repair?
8. Does the memo now account for the difference between:
   - artifact-level rehabilitation
   - prose-level rehabilitation
   - and the possibility that downstream report prose may require bounded partial re-execution even if structured metadata can be corrected in place?

## Output requirements

Write your critique to:

- `communications/REPORT_Claude_STAGE5_AOI_Source_Content_Identity_Revision_Scope_Critique_2026-03-26.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve after revision`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether this is now the right next honest step.
5. A direct answer to whether the memo stays properly bounded.
6. Any concrete memo revisions you recommend before implementation.

Prioritize hidden assumptions, over-broad repair framing, evidence-tier dishonesty, codebase mismatches, and roadmap overclaim over general summary.
