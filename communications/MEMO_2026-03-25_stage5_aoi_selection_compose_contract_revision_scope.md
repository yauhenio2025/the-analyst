# Memo: Stage 5 AOI Selection-Compose Contract Revision Scope

Date: 2026-03-25
Status: Draft scope memo for implementation review
Program: Dynamic Bespoke Apps Platformization
Depends on:
- `communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_diagnosis.md`
- `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_revision.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json`
- `communications/PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_session.har`

## Summary

The fresh post-snapshot-durability `evolution_ready` rerun proves that:

- selector/provider repair is still holding
- host warm snapshot durability is now holding
- the real planner-backed path still stays on `compose-from-selection`
- canonical `source_v2_job_id` is still preserved
- the host no longer fails on a phantom warmed snapshot id

The new blocker is narrower and later:

- analyzer-side selection-backed transient compose is returning `409 bounded_dynamic_composition_validation_failed`
- the live failure is about missing `structured_data` keys referenced by final AOI transient view `section_renderers`

That means the next honest step is one bounded `analyzer-v2` repair slice on selection-backed transient compose contract alignment, then the same `evolution_ready` diagnostic again before any frozen rerun.

## Bounded Claim

This slice should only fix:

- selection-backed `compose-from-selection` transient compose shaping for the real AOI source-family path
- contract-safe alignment between final `renderer_config.section_renderers` and final `structured_data`
- the specific affected AOI source families exposed by the live rerun:
  - `aoi_thematic_synthesis`
  - `aoi_sin_findings`
- any narrowly necessary normalization/preservation logic needed so bridge-produced AOI payloads survive transient compose without losing required keys

This slice should not reopen:

- host warm snapshot durability
- host identity continuity / `source_v2_job_id` handoff
- analyzer selector/provider behavior
- AOI planning law or planner prompts
- the frozen Stage 5 pack or rubric
- roadmap order

## Scope Decisions

### Decision 1: Treat selection-backed transient compose as the first broken hop

The new live evidence no longer points first to `the-critic`.

The counted path now successfully reaches:

- planner-backed continue
- `/compose-from-intent`
- host `compose-from-selection`

and fails only when analyzer-side transient compose returns contract-validation `409`.

The immediate seam to fix is therefore inside analyzer transient compose, not another host continuity pass.

### Decision 2: Keep the repair inside `analyzer-v2`

The bounded implementation surface should stay primarily inside:

- `src/presenter/compose_from_intent.py`
- `src/presenter/composition_source_bridge.py`
- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/renderer_contract_enforcement.py`
- presenter route/error mapping only if needed for clearer proof, not for a new contract

The `the-critic` host path should be treated as closed baseline unless the analyzer repair reveals a concrete compatibility gap that cannot be solved inside analyzer.

### Decision 3: Preserve the repaired planner-backed path exactly

This slice must keep the counted path assumptions fixed:

- planner-backed launch stays on `compose-from-selection`
- canonical `source_v2_job_id` stays preserved
- `compose-from-source` remains excluded from the counted path
- no legacy/debug fallback is allowed to earn the rerun

The next live rerun must still prove the same branch discipline, not a sidestep.

### Decision 4: Prefer deterministic AOI source-family handling over lossy re-extraction

The current code already resolves planner-selected AOI source families into materialized sections from normalized AOI payloads, then serializes them into stable JSON before transient compose.

So the first implementation branch should be:

- determine whether the affected AOI source families can preserve or deterministically normalize that structured payload directly through transient compose

before choosing:

- another generic extraction pass over already-structured AOI JSON

The memo should not pre-commit to a bypass if the code disproves that path, but it should require the implementor to justify any continued lossy re-extraction on the affected AOI families.

### Decision 5: Make final contract truth the real acceptance line

This slice should be judged at the final served transient payload layer, not only at intermediate shaping.

After consumer adaptation and before response return:

- no AOI transient view may reference `section_renderers` keys that are absent from the final `structured_data`
- the real four-family `evolution_ready` selection shape must validate end to end

The fix does not count if it only makes intermediate payloads look plausible while final contract enforcement still fails.

### Decision 6: Keep the rerun branch rule strict

After the repair:

1. rerun the same live `evolution_ready` diagnostic
2. only if that succeeds end to end, rerun the same frozen four-case Stage 5 pack

If the diagnostic still fails on a new downstream seam, stop again and write a new revision memo rather than consuming the frozen rerun.

## Proposed Deliverables

### 1. Bounded analyzer repair

- one `analyzer-v2` code slice that makes the real planner-selected AOI compose-through-selection path contract-valid
- no API/schema redesign unless a small compatibility correction is strictly necessary

Suggested regression ownership:

- analyzer transient compose path:
  - `/home/evgeny/projects/analyzer-v2/tests/test_compose_from_intent.py`
- analyzer route/contract error mapping:
  - `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py`
  - `/home/evgeny/projects/analyzer-v2/tests/test_served_renderer_contract_policy.py`
- host counted-path smoke only if needed to prove no path drift:
  - `/home/evgeny/projects/the-critic/tests/test_aoi_v2_client.py`
  - `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`

Regression discipline should be explicit:

- at least one analyzer regression must use the real four-family `evolution_ready` selection shape:
  - `thematic_synthesis`
  - `engagement_mapping`
  - `sin_findings`
  - `thematic_report`
- that regression must assert successful `compose-from-selection` response rather than only asserting that the source bridge resolves
- at least one contract-focused regression must prove the repaired AOI thematic-synthesis transient view does not reference missing `structured_data` keys
- at least one contract-focused regression must prove the repaired AOI sin-findings transient view does not reference missing `structured_data` keys
- if the fix preserves structured AOI payloads rather than re-extracting them, at least one regression should make that preservation law explicit instead of only asserting final HTTP status

### 2. Re-diagnostic artifacts

Refresh the live rerun artifacts for:

- HAR
- request JSON
- screenshot
- diagnosis note

The updated diagnosis note must explicitly say it supersedes the current `409` contract-hitting diagnostic if the repair succeeds.

### 3. Closeout outcome

Produce one of:

- a completion note saying the repaired selection-backed compose path now earns the frozen rerun
- a revision note saying the repaired path still does not earn it

## Acceptance Criteria

This scope is successful only if one of these is true:

1. the repaired `compose-from-selection` path passes `evolution_ready` end to end on the counted planner-backed path, proves contract-valid transient AOI output for the real four-family selection shape, and the frozen rerun is honestly earned
2. the repaired path still exposes a new blocker, but the failure is documented with a new revision memo and the frozen rerun is still not consumed

The repair does **not** count as successful if:

- `compose-from-selection` still returns `409 bounded_dynamic_composition_validation_failed` for the real `evolution_ready` shape
- the fix earns success only by dropping back to `compose-from-source`, profile fallback, or other legacy/debug controls
- the fix only patches one AOI source family while the real four-family ready case remains contract-invalid
- the slice silently widens into a broader presenter/planner redesign without evidence that such widening is necessary

## Implementation Note

The first diagnostic fork for the implementor should be:

- reproduce the real four-family `compose-from-selection` request in analyzer-only regression form
- inspect payload shape before and after `_transform_section_prose(...)`
- inspect payload shape again after consumer adaptation and final contract enforcement

That keeps the investigation bounded to the actual failing seam instead of assuming the exact fix before the code is checked.

## Status Implications

Until this slice lands and the diagnostic is rerun successfully:

- Stage 5 remains `In progress`
- Stage 2 remains open
- Tranche 3 remains blocked
