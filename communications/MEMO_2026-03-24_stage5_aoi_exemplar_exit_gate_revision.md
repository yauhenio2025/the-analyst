# Memo: Stage 5 AOI Exemplar Exit Gate Revision

Date: 2026-03-24
Status: Revision required
Program: Dynamic Bespoke Apps Platformization
Depends on:
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/PROOF_2026-03-24_stage5_aoi_exemplar_eval_pack.md`
- `communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-24.json`

## Summary

The Stage 5 AOI exemplar exit gate was executed and did not pass.

This is not a documentation-only miss.
It is a real proof-surface failure:

- the planner-primary AOI product flow reached `route-task` and `plan-task`
- all four cases produced auditable planning results
- but the required ready cases did not reach planner-backed compose/render
- and the AOI host surface did not stably surface blocked planner outcomes in the UI

Therefore:

- Stage 5 remains open
- Stage 2 remains open
- the program should not advance to broader transient generalization on the claim that the AOI exemplar is now empirically ratified

## What Passed

- the fixed eval pack was run over the real `the-critic` planner-primary AOI surface
- request-level artifact capture exists for all four cases
- the blocked-case fixture is valid and useful
- the current codebase still passes the focused analyzer / frontend / backend confidence pack

## What Failed

### 1. Ready-case planner stability

All three ready cases failed at planning time in the real product-path run:

- `evolution_ready` -> `aoi_selection_blocked` / `llm_provider_failure`
- `engagement_ready` -> `aoi_selection_blocked` / `llm_provider_failure`
- `non_profile_ready` -> `aoi_selection_blocked` / `llm_provider_failure`

This is enough on its own to fail the Stage 5 seam gate.

### 2. Host blocked-state visibility

The required negative case did return the correct blocked plan result:

- `aoi_selection_blocked`
- reason code `no_usable_source_families`

But the AOI panel did not retain that blocked outcome as a stable visible banner/state in the actual UI capture.

That means the product surface currently fails the Stage 5 `operational_behavior` rule even where the planner seam itself behaves correctly.

### 3. Stage 2 closure threshold

All cases in this run are `fixture_backed`.

Even if the Stage 5 seam gate had passed, Stage 2 still would not have been honestly documentary-closable from this pack alone without at least one `execution_backed` ready case.

## Closure Decisions

### Stage 5

Decision: **stay open**

Rationale:

- required ready cases did not pass
- required blocked case did not meet user-visible blocked-state expectations

### Stage 2

Decision: **stay open**

Rationale:

- Stage 5 failed
- no `execution_backed` ready case exists in this pack

## Required Next Step

The next step should be a bounded Stage 5 revision slice, not a jump to Tranche 3 generalization.

That revision slice should focus on exactly two things:

1. AOI host proof-surface stabilization
   - ensure planner-blocked outcomes remain stably visible in `AoiV2ThematicPanel`
   - ensure planner-ready outcomes remain visible long enough to continue into compose

2. AOI selector/provider reliability
   - investigate why the ready-case planner path is returning `llm_provider_failure` in the real product-pack run
   - reduce that operational failure enough to rerun the same four-case pack honestly

The fixed case set and frozen rubric should remain unchanged for the rerun.

## What Should Not Happen Next

Do not:

- mark Stage 5 complete
- mark Stage 2 closed
- treat AOI exemplar completion as empirically finished
- move the main program line to transient-substrate generalization as if the exemplar gate had passed

## Evidence

- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/PROOF_2026-03-24_stage5_aoi_exemplar_eval_pack.md`
- `communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-24.json`
- `communications/PROOF_stage5_aoi_evolution_ready_session_2026-03-24.har`
- `communications/PROOF_stage5_aoi_engagement_ready_session_2026-03-24.har`
- `communications/PROOF_stage5_aoi_non_profile_ready_session_2026-03-24.har`
- `communications/PROOF_stage5_aoi_selection_blocked_session_2026-03-24.har`
