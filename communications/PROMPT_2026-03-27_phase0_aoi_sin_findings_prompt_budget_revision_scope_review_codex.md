# Prompt For Codex: Phase 0 AOI Sin-Findings Prompt-Budget Revision Scope Audit

Audit the new prompt-budget revision scope doc:

- `communications/MEMO_2026-03-27_phase0_aoi_sin_findings_prompt_budget_revision_scope.md`

Your job is to test the robustness of the assumptions behind that memo against the actual codebase, recent Phase 0 / Stage 5 memos and proof artifacts, and the larger analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “trim the prompt until the provider stops complaining.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as a proving harness, not the destination architecture
- finish Phase 0 honestly before Phase 1 becomes the main implementation line
- avoid mistaking old repaired host seams for the current blocker once the real seam has moved into analyzer execution

So assess the memo both as:

1. a bounded diagnosis/repair scope for the immediate Phase `3.0` blocker
2. a broader platform-program prioritization decision

## What to inspect

Read these docs first:

- `communications/MEMO_2026-03-27_phase0_aoi_sin_findings_prompt_budget_revision_scope.md`
- `communications/MEMO_2026-03-27_phase0_aoi_active_discovery_repair_completion.md`
- `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_revision_after_active_discovery_repair.md`
- `communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_execution_memo.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_active_boundary_2026-03-27.json`
- `communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_terminal_failure_2026-03-27.json`

Then inspect the implementation paths the memo relies on:

Analyzer:

- `/home/evgeny/projects/analyzer-v2/src/executor/context_broker.py`
- `/home/evgeny/projects/analyzer-v2/src/executor/phase_runner.py`
- `/home/evgeny/projects/analyzer-v2/src/executor/workflow_runner.py`
- `/home/evgeny/projects/analyzer-v2/src/executor/engine_runner.py`
- `/home/evgeny/projects/analyzer-v2/src/engines/capability_definitions/aoi_sin_findings.yaml`
- `/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/aoi_sin_findings.yaml`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/plans/plan-54b6f075fdf2.json`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/plans/plan-12e3db25fb90.json`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py`

Tests:

- `/home/evgeny/projects/analyzer-v2/tests/test_run_contract.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_adaptive_planner.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_adaptive_execution_target_normalization.py`

Also look through any other recent memo/report/proof files in `communications/` or relevant `docs/` that materially affect the judgment.

## Questions to answer

1. Does the codebase support the memo’s claim that the next honest move is a bounded analyzer-side prompt-budget repair rather than more host/browser or discovery work?
2. Is the memo correct to frame the real blocker as Phase `3.0 / aoi_sin_findings / Finding Discovery`, not Phase `4.0`?
3. Is the fixed-target rule technically sound and honestly sequenced?
4. Are the likely seam families real and well-bounded?
   - plan shape / plan-generation law
   - upstream context assembly
   - full-document execution settings
   - Phase `3.0` engine input contract
   - missing fail-fast budget guard
5. Is the `plan-12e3db25fb90` precedent relevant enough to justify treating planning/config as part of the seam?
6. Is the memo missing any deeper or adjacent seam:
   - duplicate document loading
   - over-large capability prompt context
   - hidden multi-pass amplification
   - analyzer/provider config mismatch
7. Does the memo keep Stage 2 / Phase 1 sequencing honest?
8. Is the scope technically bounded and implementation-worthy, or still too vague?
9. Does the memo force an explicit enough closeout on where the real seam lived after implementation?

## Output requirements

Write your audit to:

- `communications/REPORT_Codex_Phase0_AOI_Sin_Findings_Prompt_Budget_Revision_Scope_Audit_2026-03-27.md`

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

Prioritize bugs, hidden assumptions, evidence-quality gaps, codebase mismatches, scope dishonesty, and broader-program mis-sequencing over general summary.
