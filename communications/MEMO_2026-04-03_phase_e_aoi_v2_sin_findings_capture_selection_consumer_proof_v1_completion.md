# Memo: Phase E AOI V2 Sin-Findings Capture-Selection Consumer Proof V1 Completion

Subtitle: One live Critic V2 surface now proves that the current analyzer contract is sufficient to create a well-formed capture selection on a specialized findings surface

Date: 2026-04-03
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Most Recent Prior Code Completion:
- `communications/MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_completion.md`
Earlier Code Completions In This Line:
- `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_completion.md`
- `communications/MEMO_2026-04-02_phase_e_job_backed_first_hop_affordance_propagation_v1_completion.md`
- `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_completion.md`
Companion Product Evidence:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
Host Codebase:
- `/home/evgeny/projects/the-critic`

## Purpose

Record what actually landed in the bounded host-side AOI V2 consumer proof after the analyzer-side first-hop affordance, specialized findings-bank family, and mixed-surface nested-handle slices.

This memo is about what is now true on the Critic side.
It is not a claim that the generic renderer package already consumes analyzer affordance metadata, that mixed-surface V2 consumers are solved, or that end-to-end Arsenal mutation parity is now proven.

## What Landed

One bounded host consumer now exists on one current specialized AOI V2 surface:

- `aoi_by_sin_type`

The host now does four concrete things on that surface:

1. acknowledges the already-landed analyzer contract locally:
   - `first_hop_affordance`
   - `finding_id`
2. threads the bounded affordance object through the shared V2 renderer-config seam
3. consumes the contract on one local `aoi_by_sin_type` renderer override
4. turns an eligible card click into a normal `CaptureSelection` using the existing Critic capture pipeline

The proof boundary is intentionally narrow:

- the user enters capture mode
- a card-level capture control appears only when the specialized affordance and non-empty `finding_id` are both present
- clicking that control creates a well-formed `CaptureSelection`
- the existing `CaptureActionBar` shows the resulting breadcrumb, title, preview text, and action buttons

## The Final Boundary

The completed slice proves capture-selection sufficiency only.

What is now true:

- Critic can consume analyzer-emitted `first_hop_affordance` on one live V2 surface
- Critic can consume analyzer-emitted `finding_id` on that same surface
- the bounded host can create a correct `CaptureSelection` from that contract
- the selection reaches the shared capture UI without host-local analytical reconstruction

What is still not true:

- the generic renderer package does not yet consume affordance metadata
- `aoi_by_theme` does not yet have a bounded V2 consumer proof
- end-to-end Arsenal promotion through the `/captures/...` pipeline is not what this slice proves
- current capture persistence does not yet prove that analyzer `entity_id` survives into the stored capture record
- current capture mutation source snapshots do not yet prove truthful non-genealogy workflow provenance

## Implementation Shape

The host implementation stayed local and passive-first.

The landed shape is:

- local `FirstHopAffordance` acknowledgement beside `ViewPayload` in `webapp/src/components/V2TabContent.tsx`
- `_firstHopAffordance` threaded beside the existing private capture metadata in the shared V2 renderer config seam
- one view-key override for `aoi_by_sin_type` in `webapp/src/components/renderers/index.ts`
- one dedicated local renderer:
  - `webapp/src/components/renderers/AoiSinFindingsRenderer.tsx`

That renderer:

- preserves the readable grouped findings surface outside capture mode
- does not redesign the surface into a new UI
- shows the capture control only when all five guard conditions are true:
  - capture mode on
  - `capturable = true`
  - `allowed_destinations` includes `arsenal`
  - `specialized_family = "findings_bank_arsenal_promotion_v1"`
  - non-empty `finding_id`
- uses config-threaded values instead of hard-coded source metadata
- freezes `source_item_index` as a 0-based section-local index
- calls `stopPropagation()` on the card capture button to avoid future accidental card/header side effects

The local override is a bounded v1 stepping stone, not the intended long-term pattern.
The long-term expectation remains:

- generic renderer-package consumption of analyzer affordance metadata

## Verification

Focused host verification passed:

- `CI=1 npm test -- --runInBand --runTestsByPath src/components/renderers/index.test.tsx src/components/renderers/AoiSinFindingsRenderer.test.tsx src/components/V2TabContent.test.tsx src/components/influence/AoiV2ThematicPanel.test.tsx`
  - `40 passed`

Focused browser verification also passed:

- `npx playwright test tests/aoi-v2-sin-capture.spec.ts --project=chromium`
  - `1 passed`

The browser proof asserts exactly at the intended boundary on the live AOI V2 page:

- breadcrumb
- capture title
- preview text
- action buttons in `CaptureActionBar`

One proof-environment note matters for honesty:

- the Playwright spec removes an unrelated CRA dev overlay caused by missing local style-token fetches to `localhost:8001`
- that overlay was not caused by the AOI capture feature itself
- the rendered AOI V2 surface and capture handoff behavior under test were otherwise live and real on the bounded page path

No analyzer-v2 runtime code changed in this slice.

## Calibrated Claim

The honest completed claim is now:

- one current thin host can consume the existing analyzer contract on one specialized AOI V2 findings surface and produce a well-formed `CaptureSelection`
- that proof uses the real shared V2 threading seam, the real shared capture context, and the real shared capture action bar
- the proof does not require direct `/api/arsenal` mutation, host-local analytical reconstruction, or analyzer changes

It does not yet mean:

- the current `/captures` pipeline preserves analyzer item identity end to end
- the current `/captures` pipeline preserves truthful analysis workflow provenance end to end
- the same consumer rule is already proven on mixed surfaces
- the same consumer rule is already proven beyond AOI
- one custom renderer per specialized surface is now the intended architecture

## Why This Matters

This slice closes the exact loop the previous analyzer-only memos left open.

Before this proof, the strongest honest claim was:

- analyzer-v2 can emit bounded first-hop affordance metadata and per-item handles

After this proof, the stronger honest claim is:

- a real current host can already do something concrete with that contract on a live specialized surface

That is materially stronger than another analyzer-only semantic refinement because it proves:

- the current analyzer contract is already consumable
- the host can stay thin at the capture-selection boundary

It is still not a reusable-substrate proof across surface families or workflow families.
But it is the first bounded proof that current analyzer affordance/handle truth is operationally usable on the live Critic V2 path.

## Next Honest Step

The next bounded question should now stay on the same `aoi_by_sin_type` line, but move one step deeper into the existing capture pipeline:

- can the current source-agnostic `/captures` pipeline preserve analyzer item identity and truthful analysis workflow provenance once the host submits the selection it now knows how to create?

The strongest immediate gap is concrete and already visible in the current code:

- `CaptureSelection.entity_id` now exists and is emitted by the bounded renderer proof
- but `CaptureContext.submitCapture(...)` does not send `entity_id` in `POST /api/captures`
- `CaptureCreateRequest`, `CaptureResponse`, and `GenealogyCaptureDB` do not persist it
- `capture_to_arsenal(...)` still hardcodes `workflow_key = "intellectual_genealogy"` in `source_snapshot`

So the next honest step is not:

- another analyzer-only semantics question
- a generic renderer-package generalization
- `aoi_by_theme` mixed-surface consumer work
- end-to-end Arsenal parity

It is:

- one bounded capture-provenance persistence slice on the same AOI V2 `aoi_by_sin_type` path
- carrying `entity_id` and truthful source workflow provenance through the existing `/captures` create-and-route seam
- while keeping analyzer semantics, mixed-surface consumer work, capture-status generalization, and direct Arsenal mutation explicitly deferred
