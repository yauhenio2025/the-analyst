# Phase 0 AOI Exemplar Honesty Closeout Revision After Prompt-Budget Repair

## Verdict

Closeout C: truthful Phase 0 grading is still not possible on the fresh post-repair rerun.

## Fresh attempt

- Fresh job: `job-3503e9e65338`
- Plan: `plan-8dba8c450012`
- Project: `round5-proof-dossier-final-1774100000`
- Thinker: `otto_neurath`
- Workflow: `anxiety_of_influence_thematic_single_thinker`
- Launch mode: `by_ref`

## What the bounded repair fixed

The planned Phase `3.0` repair is real and implemented on the live Otto path, but it was not yet live-validated to completion because the fresh rerun stopped earlier at Phase `1.0`.

- Phase `3.0` document assembly is now target-only rather than target plus full raw Otto corpus.
- Pass-level prompt-budget instrumentation now logs document, shared-context, inner-context, and prompt sizes before each LLM call.
- The executor now fail-fasts locally on the 1M-context path before provider submission when the estimated input crosses the local estimated-token guard.
- Focused regressions for the Phase `3.0` prompt-budget slice passed before the rerun.

Evidence:

- [PROOF_phase0_aoi_execution_backed_after_prompt_budget_repair_corpus_inventory_2026-03-27.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_phase0_aoi_execution_backed_after_prompt_budget_repair_corpus_inventory_2026-03-27.json)
- [PROOF_phase0_aoi_execution_backed_after_prompt_budget_repair_launch_2026-03-27.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_phase0_aoi_execution_backed_after_prompt_budget_repair_launch_2026-03-27.json)
- [PROOF_phase0_aoi_execution_backed_after_prompt_budget_repair_active_boundary_2026-03-27.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_phase0_aoi_execution_backed_after_prompt_budget_repair_active_boundary_2026-03-27.json)

## Why Phase 0 still cannot close

The fresh rerun no longer stops at Phase `3.0`.

Instead, the new local guard exposed a larger upstream truth: the Otto corpus still overruns prompt budget earlier, at Phase `1.0 / Source Thematic Synthesis`.

Observed blocking seam:

- phase: `1.0`
- phase name: `Source Thematic Synthesis`
- engine: `aoi_thematic_synthesis`
- pass: `Pass 1 (Source Theme Discovery)`
- failure kind: local pre-provider prompt-budget guard
- exact failure message on that rerun:
  - `Prompt budget exceeded locally: ~908,141 estimated tokens (3,632,565 chars) >= 900,000 limit. Aborting before provider call.`

Measured live Phase `1.0` pass-budget shape from the fresh rerun:

- `document_text`: `3,627,836` chars
- `shared_context`: `830` chars
- `system_prompt`: `4,729` chars
- total assembled chars before the call: `3,632,565`
- estimated input size: `~908,141` tokens

That means the prompt-budget slice was directionally correct but incomplete:

- making Phase `3.0` target-only removed the previously known `aoi_sin_findings` overflow from the code path
- but this rerun did not reach Phase `3.0`, because the then-active `900,000` local guard stopped earlier at Phase `1.0`

## Execution nuance

This fresh rerun used a parallel opening phase group:

- `0.5` Target Text Profiling
- `1.0` Source Thematic Synthesis

Phase `1.0` faulted immediately on the local guard, but the parallel `0.5` sibling continued running. To avoid further spend after the new blocker was already established, the run was force-cancelled.

So the final run status is `cancelled`, but that must not be misread as the absence of a Phase `1.0` blocker. The bounded seam was already observed before cancellation.

Evidence:

- [PROOF_phase0_aoi_execution_backed_after_prompt_budget_repair_phase1_guard_diagnostic_2026-03-27.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_phase0_aoi_execution_backed_after_prompt_budget_repair_phase1_guard_diagnostic_2026-03-27.json)
- [PROOF_phase0_aoi_execution_backed_after_prompt_budget_repair_force_cancel_2026-03-27.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_phase0_aoi_execution_backed_after_prompt_budget_repair_force_cancel_2026-03-27.json)
- [PROOF_phase0_aoi_execution_backed_after_prompt_budget_repair_terminal_state_2026-03-27.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_phase0_aoi_execution_backed_after_prompt_budget_repair_terminal_state_2026-03-27.json)

## Decision

Do not treat `job-3503e9e65338` as the Phase 0 execution-backed exemplar.

The next blocker is no longer:

- thinker-scoped discovery
- or Phase `3.0 / aoi_sin_findings`

The next blocker is now:

- Phase `1.0 / aoi_thematic_synthesis` still receiving too much raw selected-source corpus for the fixed Otto target under the new honest local budget guard

So no completed-boundary proof, browser proof, or Stage 2 grade can be claimed from this rerun.

## Next bounded repair

The next repair should stay narrow:

- reduce or stage the Phase `1.0 / aoi_thematic_synthesis` source-corpus input contract for the fixed Otto target
- preserve the same project, thinker, workflow, task, and corpus
- keep the new local guard and Phase `3.0` target-only shaping in place
- rerun Phase 0 fresh after the Phase `1.0` repair rather than reusing this cancelled job

Until that repair lands, no honest Phase 0 closure memo can be written.
