# Prompt For Claude: Phase 0 AOI Sin-Findings Prompt-Budget Revision Scope Critique

Critique the new prompt-budget revision scope doc:

- `communications/MEMO_2026-03-27_phase0_aoi_sin_findings_prompt_budget_revision_scope.md`

Your job is to test the robustness of the assumptions behind that memo against the actual codebase, the recent Phase 0 / Stage 5 memo-and-proof trail, and the broader analyzer-v2 platform objective.

## Bigger-picture objective

The target is not just “make one Anthropic error go away.”

The target remains:

- make `analyzer-v2` the analytical brain for dynamic bespoke apps
- use `the-critic` as the proving ground for host/product seams
- keep Phase 1 and broader planner-to-presentation generalization sequenced behind an honestly closed Phase 0
- avoid spending the main line on stale host/browser blockers once the real seam has moved upstream

So evaluate the memo both as:

1. a bounded implementation scope for the immediate Phase `3.0` prompt-budget blocker
2. a broader program-prioritization decision about what still must happen before Stage 2 can close honestly

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

Then inspect the implementation paths and artifacts the memo relies on:

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

1. Is the memo right that the next honest move is now analyzer-side Phase `3.0` prompt-budget work rather than more discovery or host/browser work?
2. Does the codebase support the memo’s claim that the current failing seam is a real Phase `3.0 / aoi_sin_findings / Finding Discovery` overflow, not a misread of `progress.current_phase = 4.0`?
3. Is the memo appropriately strict about keeping the fixed Otto target unchanged?
4. Does the code support the memo’s claim that current plan shape is part of the seam:
   - `requires_full_documents = true`
   - `document_scope = whole`
   - `chapter_targets = null`
   - `max_context_chars_override = null`
5. Is the historical precedent from `plan-12e3db25fb90` materially relevant, or is the memo over-reading it?
6. Are the allowed repair levers well-bounded and technically plausible:
   - phase-specific pre-digestion or staging
   - bounded context shaping
   - plan-shape revision
   - executor-side fail-fast budget guard
7. Is the memo missing any deeper adjacent seam:
   - prompt composition inflation independent of plan shape
   - hidden document duplication
   - unnecessary upstream-context threading
   - engine-specific multi-pass amplification
8. Does the memo keep Stage 2 / Phase 1 sequencing honest?
9. Is it concrete enough to guide implementation safely, or still too hand-wavy?

## Output requirements

Write your critique to:

- `communications/REPORT_Claude_Phase0_AOI_Sin_Findings_Prompt_Budget_Revision_Scope_Critique_2026-03-27.md`

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

Prioritize hidden assumptions, codebase mismatches, evidence-tier dishonesty, scope creep, and roadmap mis-sequencing over general summary.
