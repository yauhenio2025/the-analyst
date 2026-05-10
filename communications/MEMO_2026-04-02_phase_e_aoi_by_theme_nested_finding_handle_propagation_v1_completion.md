# Memo: Phase E AOI By-Theme Nested Finding Handle Propagation V1 Completion

Subtitle: One mixed AOI surface now preserves nested finding identity while keeping whole-view affordance semantics generic

Date: 2026-04-02
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Immediate Scope Memo:
- `communications/MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_scope.md`
Most Recent Prior Code Completion:
- `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_completion.md`
Companion Product Evidence:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`

## Purpose

Record what actually landed in the bounded mixed-surface AOI handle propagation slice after the scope memo and the review corrections on legacy payload honesty, host-evidence calibration, and scope discipline.

This memo is about what is now true on the analyzer side.
It is not a claim that `aoi_by_theme` is now a findings-bank surface, that the current bounded-V2 host path already operationalizes the new handle, or that analyzer-v2 now owns item-level operation behavior generically.

## What Landed

One mixed AOI surface now preserves analyzer-owned nested finding identity:

- AOI `aoi_by_theme`

The landed change is intentionally small:

- nested `findings[]` items on `aoi_by_theme` can now carry `finding_id`

The whole-view contract remains unchanged:

- `FirstHopAffordance` on `aoi_by_theme` stays generic-only
- no new `specialized_family` is emitted on that surface
- no new destination or lifecycle semantics were added

This means the analyzer now distinguishes more cleanly between:

- a pure findings surface:
  - `aoi_by_sin_type`
- a mixed surface with nested findings:
  - `aoi_by_theme`

## The Final Boundary

The completed slice is narrower than a second findings-bank specialization.

What is now true:

- newly built `aoi_by_theme` payloads preserve `finding_id` on nested findings
- the same rebuilt payloads still expose the same mixed theme structure:
  - overview
  - engagement
  - claims
  - commitments
  - moves
  - source documents
  - findings

What is still not true:

- `aoi_by_theme` is not treated as a whole-view findings bank
- `aoi_by_theme` does not gain `specialized_family = "findings_bank_arsenal_promotion_v1"`
- no generic item-level affordance schema was introduced

## Implementation Shape

The implementation took the local-modification route:

- `_finding_card()` remains behaviorally unchanged
- `finding_id` is added only inside `src/aoi/contract.py::_build_by_theme_payload(...)`

That choice keeps the mixed-surface broadening visibly local to `aoi_by_theme` rather than centralizing it in a shared helper.
It also leaves known duplication with the parallel `finding_id` carry-through already present in `src/aoi/contract.py::_build_by_sin_type_payload(...)`.
That duplication is acceptable at this size, but it should be described honestly as a local implementation choice, not as a principled elimination of shared logic.

One small code comment was added at that seam to make the scope boundary explicit:

- preserve per-finding identity on nested theme findings
- without changing the shared finding-card helper
- without changing whole-view semantics

## Host And Legacy Truth

Two calibration points matter for the honest completed claim:

1. **Host evidence**

The strongest downstream evidence for thematic nested finding identity is still the legacy Critic thematic UI:

- `ThemeSynthesisCard.tsx`
- `AnxietyOfInfluencePage.tsx`

That is real evidence that theme-nested findings are meaningful items.
But it is **not** proof that the current bounded-V2 `aoi_by_theme` served surface already consumes `finding_id` operationally.

The current bounded-V2 path still remains generic there.

2. **Legacy payloads**

This slice broadens newly built analyzer contract truth only.

Existing persisted `structured_payloads.aoi_by_theme` blobs loaded from saved output metadata remain handle-less until those jobs are rebuilt through the updated analyzer contract.

No repair-on-load compensation was added.

## Verification

Focused compile/test verification passed:

- `python -m compileall src/aoi/contract.py tests/test_aoi_contract.py tests/test_presentation_api.py`
- `PYTHONPATH=. pytest -q tests/test_aoi_contract.py tests/test_presentation_api.py`
  - `83 passed, 2 warnings`

Broader regression verification also passed:

- `PYTHONPATH=. pytest -q tests/test_manifest_trace.py tests/test_analysis_product_contract.py tests/test_representative_composition_matrix.py tests/test_transient_proof_harness_contract.py tests/test_compose_sessions.py`
  - `130 passed, 13 warnings`

No host code, docs, or proof fixtures were changed in this implementation slice.

## Calibrated Claim

The honest completed claim is now:

- analyzer-v2 can preserve minimal finding-level identity on one mixed analyzer-known AOI surface by carrying `finding_id` through to nested `aoi_by_theme` findings
- that broadens analyzer payload truth beyond the already-proved pure findings surface
- the whole-view first-hop affordance on `aoi_by_theme` remains generic
- the analyzer handle remains opaque and non-equivalent to Critic's numeric `db_id`
- older persisted `aoi_by_theme` payloads remain unchanged until rebuilt

It does **not** yet mean:

- mixed surfaces now have a generalized findings-bank specialization family
- the current bounded-V2 host path already uses the new handle
- current bounded-V2 mixed-surface operations are materially further along
- analyzer-v2 owns generic item-level operation semantics
- outline-routing is solved
- destination lifecycle is upstream-owned

## Why This Matters

This slice answers a harder and more useful question than the previous one, but on one AOI mixed surface only.

`aoi_by_sin_type` proved:

- pure findings surfaces can carry bounded specialized semantics

`aoi_by_theme` now proves:

- one AOI mixed surface can preserve analyzer-owned nested finding identity without pretending the entire view is itself a findings bank

That is a more honest matrix broadening step than simply repeating the same whole-view specialization on another AOI surface.

It is still narrower than a reusable substrate proof.
The implementation is AOI-local, and the current bounded-V2 host path still does not consume `first_hop_affordance` or nested thematic `finding_id`.
So the strongest roadmap reading is:

- one mixed-surface analyzer payload gap is now closed
- the broader analyzer-v2-as-brain claim is only modestly stronger until a thin consumer path or a non-AOI surface re-proves the pattern

## Next Honest Step

The next bounded Phase E question should now be one of these, in order:

1. one bounded consumer-side V2 proof that actually uses the already-landed analyzer contract on a current surface
2. one non-AOI surface proof that tests whether the mixed-surface nested-handle pattern is genuinely reusable
3. only after that, reconsider whether one mixed-surface specialized family is actually defensible on `aoi_by_theme`

Why this ordering is cleaner:

- it tests whether the current analyzer-owned contract is already materially useful to a thin host
- it checks reusable-substrate value before deepening AOI-only analyzer shaping again
- it keeps the program tied to the broader `Close Read` direction rather than letting Phase E drift into analyzer-local semantic accumulation

What should **not** happen next:

- treating this as proof of current bounded-V2 mixed-surface operations
- assuming the reusable pattern is already proven beyond AOI
- pretending this slice proves a generic item-level affordance taxonomy
- broadening destinations again
- jumping to lifecycle
