# Phase 0 AOI Exemplar Honesty Closeout Revision After Active-Discovery Repair

## Verdict

Closeout C: truthful Phase 0 grading is still not possible on the fresh post-repair rerun.

## Fresh attempt

- Fresh job: `job-226f65f43a3b`
- Project: `round5-proof-dossier-final-1774100000`
- Thinker: `otto_neurath`
- Workflow: `anxiety_of_influence_thematic_single_thinker`
- Launch mode: `by_ref`

## What the bounded repair fixed

The active-discovery seam is repaired.

- Thinker-scoped live-run discovery now includes the fresh by-ref AOI job during the pending window.
- The fresh active-boundary smoke passed on `job-226f65f43a3b`.
- The repair is the analyzer-side discovery normalization change that now unwraps `by_ref_request_snapshot` for thinker extraction, plus focused regression coverage for run discovery and result discovery.

Evidence:

- [PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_corpus_inventory_2026-03-27.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_corpus_inventory_2026-03-27.json)
- [PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_launch_2026-03-27.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_launch_2026-03-27.json)
- [PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_active_boundary_2026-03-27.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_active_boundary_2026-03-27.json)

## Why Phase 0 still cannot close

The fresh rerun failed on the real analyzer execution path before any durable completed AOI result existed.

- Completed phases: `0.5`, `1.5`, `1.0`, `2.0`
- Failed phase: `3.0`
- Terminal job status: `failed`
- Terminal error: `Phases [3.0] failed`

Exact blocking cause from analyzer logs:

- phase: `3.0`
- engine: `aoi_sin_findings`
- pass: `Finding Discovery`
- Anthropic rejected the call with `invalid_request_error`
- exact message: `prompt is too long: 1037154 tokens > 1000000 maximum`

That means this fresh post-repair attempt did not produce:

- a durable completed AOI result
- a valid completed-boundary proof
- a truthful planner-primary browser proof
- a Stage 2 closure-grade or bounded-proof grade

Evidence:

- [PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_terminal_failure_2026-03-27.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_terminal_failure_2026-03-27.json)

## Decision

Do not treat `job-226f65f43a3b` as the Phase 0 execution-backed exemplar.

The main blocker is no longer thinker-scoped live discovery. The blocker is now a bounded analyzer execution seam: Phase `3.0 / aoi_sin_findings` overruns the 1M-token ceiling on the Otto corpus after the fresh repaired run reaches the real synthesis path.

## Next bounded repair

The next repair should stay narrow:

- reduce or stage the `aoi_sin_findings` prompt/context payload for the Otto AOI path so Phase `3.0` stays under the 1M-token limit
- preserve the same fixed project, thinker, workflow, and task
- rerun Phase 0 fresh after that repair, not by reusing this failed job

Until that repair lands, no honest Phase 0 closure memo can be written.
