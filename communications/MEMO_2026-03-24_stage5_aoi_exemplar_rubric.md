# Memo: Stage 5 AOI Exemplar Eval Rubric

Date: 2026-03-24
Status: Frozen rubric for the Stage 5 AOI exemplar exit-gate run
Program: Dynamic Bespoke Apps Platformization

## Purpose

This rubric defines the pass/fail thresholds for the Stage 5 AOI exemplar exit gate before the eval-pack judgment is written down.

The required case set is fixed:

1. `evolution_ready`
2. `engagement_ready`
3. `non_profile_ready`
4. `selection_blocked`

Fixture-strength tiers:

- `fixture_backed`
- `execution_backed`
- `user_initiated`

## Dimensions

### 1. `selection_fit`

Applies to ready-intent cases only.

Pass requires:

- the planner outcome is `aoi_composition_handoff_plan`
- selected source families match the minimum required shape for the case
- no prohibited family is smuggled in
- the case is not reinterpreted after the fact as “really just a legacy profile choice”

Case-specific minimums:

- `evolution_ready`
  - selected families include `thematic_synthesis` and `thematic_report`
- `engagement_ready`
  - selected families include `engagement_mapping` and `sin_findings`
- `non_profile_ready`
  - selected families are exactly:
    - `thematic_synthesis`
    - `engagement_mapping`
    - `thematic_report`
  - `sin_findings` appears in `rejected_sources`
  - `legacy_profile_equivalent` is `null`

Fail examples:

- planner returns `aoi_selection_blocked`
- planner returns a profile-shaped bundle for `non_profile_ready`
- selected/rejected rationale surface is missing or inconsistent with the selected set

### 2. `rationale_clarity`

Applies to all cases.

Pass requires:

- ready cases:
  - non-empty `selection_summary`
  - non-empty per-source `rationale`
  - non-empty per-source `rejection_reason` for rejected families
- blocked case:
  - explicit blocked reason code
  - explicit blocked reason detail
  - trace/audit trail preserved in saved artifacts

Fail examples:

- blocked result exists only in raw logs, not the saved artifact trail
- selected or rejected rationale fields are blank

### 3. `rendered_usefulness`

Applies to ready cases only.

Pass requires:

- the product flow reaches `compose-from-selection`
- the compose response returns a rendered transient shell
- the rendered shell is not an unsupported-renderer fallback
- the rendered content is materially aligned with the requested case shape

Fail examples:

- no compose request is issued
- compose request errors
- rendered shell never appears

### 4. `operational_behavior`

Applies to all cases and is mandatory.

Pass requires:

- the real `the-critic` planner-primary AOI surface is used
- HAR + JSON + screenshot artifacts exist
- no planner-primary case silently falls back to legacy dossier/comparison launch
- blocked case:
  - `plan-task` returns `aoi_selection_blocked`
  - no `compose-from-selection` request is sent afterward
  - blocked reason is stably user-visible in the AOI host UI, not just in the network trace
- ready cases:
  - route/plan succeed through the planner-primary product path
  - planner handoff is surfaced in the AOI host UI
  - planner-backed continuation reaches compose

Fail examples:

- planner returns a result but the host UI does not surface it
- blocked reason is only recoverable from HAR / JSON and not from the AOI page
- a case only “passes” after manual reinterpretation outside the product path

## Threshold Shape

The Stage 5 seam gate passes only if all of the following are true:

- every case passes `operational_behavior`
- every ready case passes `selection_fit`
- every ready case passes `rendered_usefulness`
- the blocked case passes `rationale_clarity`
- the locked non-profile case passes without legacy fallback or post-hoc relabeling

The Stage 2 documentary closure gate passes only if:

- the Stage 5 seam gate passes
- at least one ready case is `execution_backed` or stronger
- the exemplar evidence is strong enough to support repeated bounded AOI transient use rather than fixture-only seam proof

If the Stage 5 seam gate fails, Stage 2 remains open automatically.
