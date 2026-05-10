# Report: Codex Audit Of Phase E AOI V2 Mixed-Surface Nested Finding Consumer Proof V1 Scope

Date: 2026-04-03
Subject memo: `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_scope.md`
Verdict: `Approve with corrections`

## Reviewed Materials

- `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_scope.md`
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_scope.md`
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_sin_findings_capture_selection_consumer_proof_v1_completion.md`
- `communications/MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_completion.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Code Reviewed

- `src/aoi/contract.py`
- `src/presenter/first_hop_affordance.py`
- `src/presenter/presentation_api.py`
- `src/presenter/bounded_dynamic_composition.py`
- `src/views/definitions/aoi_by_theme.json`
- `tests/test_presentation_api.py`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/index.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/NestedSectionsRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SubRenderers.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/ThemeSynthesisCard.tsx`

## Verification Run

- `PYTHONPATH=. pytest -q tests/test_presentation_api.py -k "aoi_by_theme or first_hop_affordance or bounded_dynamic_composition_adapts_aoi_theme_surface"`
  - result: `9 passed, 59 deselected`
- `CI=1 npm test -- --runInBand --runTestsByPath src/components/V2TabContent.test.tsx src/components/renderers/index.test.tsx src/components/renderers/NestedSectionsRenderer.test.tsx src/components/influence/AoiV2ThematicPanel.test.tsx`
  - result: `39 passed`
  - note: existing `act(...)` warnings and Jest open-handle warning still print from `AoiV2ThematicPanel` tests

## Bottom Line

The memo is strategically right.

After the pure-surface `aoi_by_sin_type` line is now closed on selection, write-side provenance, and passive read-back, the next honest question is no longer another same-surface refinement. It is whether the already-landed AOI V2 contract can be consumed on one structurally different current mixed surface without inventing new whole-view analyzer semantics. `aoi_by_theme` is the best immediate target because the analyzer already preserves nested `finding_id` there (`src/aoi/contract.py:639-647`), the presenter keeps its whole-view first-hop affordance generic (`src/presenter/first_hop_affordance.py:50-60`, `77-96`), and the current Critic path still has no explicit local `aoi_by_theme` consumer override (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/index.ts:19-27`).

But the memo should be corrected in two important implementation-shape details:

1. the smallest honest host move is not necessarily a full `aoi_by_theme` view override; a smaller bounded seam already exists in Critic through the sub-renderer path
2. the adaptive-family complication needs one sharper warning: generic whole-view `first_hop_affordance` will still be present on out-of-scope `aoi_by_theme` variants such as the comparison-review table, so the host gate cannot rely on affordance presence alone

## Strongest Code-Backed Points

- `aoi_by_theme` really does carry nested `finding_id` on rebuilt analyzer payloads now. `_build_by_theme_payload(...)` preserves `finding_id` on each nested finding card without changing whole-view structure (`src/aoi/contract.py:639-647`). The focused presentation tests confirm those nested ids survive prepared page payloads (`tests/test_presentation_api.py:1437-1481`).

- The memo is correct that `aoi_by_theme` whole-view semantics remain generic-only. `derive_first_hop_affordance(...)` grants generic capturability to eligible migrated leaf payloads, and specialization is added only for `aoi_by_sin_type` when the pure findings-bank handle check passes (`src/presenter/first_hop_affordance.py:50-60`, `87-96`). The dedicated test explicitly keeps `aoi_by_theme` generic-only (`tests/test_presentation_api.py:1397-1434`).

- The current `aoi_by_theme` served shape is exactly the mixed-surface shape the memo describes. The view definition is an `accordion`, and its nested `findings` section is rendered as `mini_card_list`, alongside overview, engagement, claims, commitments, moves, and source documents (`src/views/definitions/aoi_by_theme.json:9-47`).

- The current Critic AOI V2 page already has the shared capture boundary needed for a selection-only proof. `AoiV2ThematicPanel` wraps the results area in `CaptureProvider` and renders `CaptureActionBar` (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:1321-1435`), while `V2TabContent` already threads `_workflowKey`, `_captureViewKey`, `_captureViewName`, `_captureSourceType`, `_captureMode`, `_onCapture`, and `_firstHopAffordance` into renderer config (`/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:568-598`).

- The memo is right that another same-surface `aoi_by_sin_type` refinement would broaden the matrix less honestly. The pure-surface renderer already has a dedicated local consumer and even read-back status handling (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx:80-217`). `aoi_by_theme` is the still-open current mixed-surface gap.

- The adaptive-family complication is real, not hypothetical. `apply_bounded_dynamic_composition(...)` can rewrite `aoi_by_theme` to either a findings-bearing `Theme Dossier` accordion or a non-findings-bearing `Theme Comparison Review` table (`src/presenter/bounded_dynamic_composition.py:743-761`, `2236-2361`). The focused tests verify both outcomes (`tests/test_presentation_api.py:1010-1089`). The current Critic AOI thematic panel also exposes dossier/comparison launch controls (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:1203-1219`).

- The memo is honest about legacy payloads remaining passive until rebuild. Prepared page payloads do not backfill missing nested `finding_id` on saved `aoi_by_theme` payloads (`tests/test_presentation_api.py:1484-1518`).

## Weakest Or Overstated Assumptions

- “One local `aoi_by_theme` view override” is not the smallest current host move. Critic already has a narrower sub-renderer seam. `NestedSectionsRenderer` forwards inherited `_...` metadata plus `_parentSectionKey` and `_parentSectionTitle` into each section sub-renderer (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/NestedSectionsRenderer.tsx:51-55`, `138-189`), and `SubRenderers.tsx` is already the local override hook over package sub-renderers (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/SubRenderers.tsx:19-30`). That means a conditional local `mini_card_list` wrapper for `aoi_by_theme` `findings` sections is smaller and more truthful than replacing the whole view.

- The pure-surface `AoiSinFindingsRenderer` is not a drop-in template for this mixed-surface proof. It synthesizes its own card UI and emits `source_renderer_type = "card_grid"` (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx:200-217`). On `aoi_by_theme`, the honest source shape is the existing nested `mini_card_list`, so copying the sin-type override pattern would over-own the surface and muddy the source-renderer truth the memo wants to preserve.

- The memo should make one sharper implementation warning about adaptive variants. `presentation_api._prepare_page_payloads(...)` applies bounded dynamic composition first and then attaches first-hop affordances (`src/presenter/presentation_api.py:829-840`). Because generic affordance attachment is leaf-based rather than family-based (`src/presenter/first_hop_affordance.py:43-60`), an out-of-scope `Theme Comparison Review` table can still carry a generic `first_hop_affordance`. So “generic affordance present” is not a sufficient gate. The host must also gate on the findings-bearing accordion shape or equivalent parent-section context.

- The legacy thematic UI evidence is useful, but it is not proof of current bounded-V2 operability. `ThemeSynthesisCard` clearly treats nested thematic findings as meaningful downstream items (`/home/evgeny/projects/the-critic/webapp/src/components/influence/ThemeSynthesisCard.tsx:252-360`), but that is supporting product evidence only. It does not prove the current V2 renderer path already consumes nested `finding_id`.

## Factual Discrepancies

- No major code-level contradiction was found in the memo’s strategic recommendation.

- One concrete implementation statement should be corrected: a full local `aoi_by_theme` view override is not the smallest bounded host seam currently available. The codebase already has a narrower sub-renderer interception point for exactly the nested `findings` list path (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/NestedSectionsRenderer.tsx:157-170`, `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SubRenderers.tsx:19-30`).

- One scope statement should be sharpened: the in-scope target is not one single named family, but the findings-bearing `accordion` shape class. In current code that includes both the default `By Theme` surface (`src/views/definitions/aoi_by_theme.json:9-47`) and the adaptive `Theme Dossier` family (`src/presenter/bounded_dynamic_composition.py:2236-2315`, `tests/test_presentation_api.py:1010-1060`). The out-of-scope variant is the `Theme Comparison Review` table (`src/presenter/bounded_dynamic_composition.py:2318-2361`, `tests/test_presentation_api.py:1063-1089`).

## What This Changes For The Larger Roadmap

- This memo remains the best immediate matrix-broadening move inside the reviewed codebase. It would prove that one analyzer-owned contract can already support both:
  - a pure findings-bank surface with specialized whole-view semantics
  - a mixed thematic surface with generic whole-view semantics plus nested item identity

- That is materially better roadmap progress than another `aoi_by_sin_type` refinement because it tests a different surface shape while holding the analyzer contract fixed.

- It still does not prove generic renderer-package capture law, non-AOI reuse, or workflow-neutral item-level affordance taxonomy. Even after a successful `aoi_by_theme` slice, the larger “analyzer-v2 as the brain” claim would still be only AOI-local plus host-local. The memo is right to keep those broader claims out of scope for v1.

- I do not see a stronger immediate next move in the current reviewed context. A non-AOI mixed-surface proof would be broader in theory, but the reviewed materials do not surface an equally ready non-AOI contract with the same combination of generic whole-view affordance plus nested analyzer-owned item identity. `aoi_by_theme` is the ready gap.

## Most Defensible Next Move After This Memo

Proceed with this slice, but tighten the implementation recommendation:

1. Keep the proof boundary at capture-selection sufficiency only.
   - Do not widen into persistence, status read-back, deep-linking, repeat-capture policy, or generic package law.

2. Prefer one bounded local `mini_card_list` consumer seam over a full `aoi_by_theme` view override.
   - Gate on `_captureViewKey === "aoi_by_theme"`.
   - Gate on `_parentSectionKey === "findings"`.
   - Gate on capture mode plus non-empty nested `finding_id`.
   - Preserve the existing accordion shell and all non-findings sections unchanged.
   - Fall through to the package `mini_card_list` renderer for every other case.

3. Treat the in-scope surface as “findings-bearing accordion” rather than “all `aoi_by_theme` variants”.
   - Default `By Theme` accordion: in scope.
   - Adaptive `Theme Dossier` accordion: in scope.
   - Adaptive `Theme Comparison Review` table: out of scope and unchanged.

4. Emit a truthful nested `CaptureSelection`.
   - `source_renderer_type = "mini_card_list"`
   - `source_section_key = <theme_id>`
   - `source_item_index = 0-based index within that theme’s findings list`
   - `parent_context.section_key = <theme_id>`
   - `parent_context.section_title = <theme title>`
   - `entity_id = finding_id`
   - `source_workflow_key = _workflowKey`

5. Add focused proof coverage only at the bounded seam.
   - local renderer/sub-renderer resolution test
   - nested finding capture test for capture mode on/off
   - handle-less nested finding remains passive
   - comparison-review table variant stays unchanged
   - one Playwright proof that clicks a nested thematic finding and asserts on `CaptureActionBar`

## Final Recommendation

Proceed, but revise the memo before implementation.

The strategic direction is right:
`aoi_by_theme` is the correct immediate next mixed-surface proof after the now-closed pure-surface `aoi_by_sin_type` line.
The main correction is implementation shape:
prefer a conditional nested `mini_card_list` consumer seam over a full `aoi_by_theme` view override, and make the adaptive-family gating rule explicit enough that out-of-scope table variants cannot accidentally inherit capture UI just because generic `first_hop_affordance` is present.
