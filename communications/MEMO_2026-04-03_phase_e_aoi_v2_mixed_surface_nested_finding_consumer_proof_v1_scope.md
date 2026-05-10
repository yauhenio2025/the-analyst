# Memo: Phase E AOI V2 Mixed-Surface Nested Finding Consumer Proof V1 Scope

Subtitle: Prove that one current mixed AOI V2 surface can consume the already-landed generic affordance plus nested finding handle contract without overclaiming whole-view findings semantics or generic renderer law

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
Most Recent Code Completion:
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_completion.md`
Immediate Prior Mixed-Surface Analyzer Completion:
- `communications/MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_completion.md`
Related Host-Side Completions On The Pure Findings Line:
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_sin_findings_capture_selection_consumer_proof_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_completion.md`
Companion Product Evidence:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
Host Codebase:
- `/home/evgeny/projects/the-critic`

## Purpose

Define the next bounded Phase E slice after the completed pure-surface AOI `aoi_by_sin_type` selection/write/read loop.

That line is now strong enough:

- one live current host can create a correct `CaptureSelection`
- the current capture pipeline preserves truthful analyzer provenance on the write side
- the same bounded surface can now read persisted truth back after reload

The next honest question is no longer another refinement on the same pure findings surface.
It is:

- can one structurally different current mixed AOI V2 surface consume the already-landed analyzer contract on nested findings without pretending whole-view specialization or generic renderer-package law now exists?

This memo therefore scopes:

- one bounded host-side mixed-surface consumer proof in Critic
- on AOI `aoi_by_theme`
- using already-landed nested `finding_id`
- while keeping whole-view `FirstHopAffordance` generic-only and analyzer-v2 unchanged

## Strategic Decision

The next concrete move should be:

- one bounded AOI V2 mixed-surface nested-finding consumer proof on `aoi_by_theme`

not:

- another same-surface `aoi_by_sin_type` refinement
- another analyzer-only semantic slice
- immediate non-AOI proof
- generic renderer-package affordance consumption
- a mixed-surface specialized-family expansion
- generic item-level affordance taxonomy work

The reason is straightforward:

- the pure findings surface already has the strongest current bounded loop we need
- `aoi_by_theme` already has analyzer-owned nested `finding_id`
- the current bounded-V2 host path still does not operationalize that nested handle
- broadening to one mixed surface teaches more reusable substrate value than another same-line refinement on `aoi_by_sin_type`

This still varies the proof boundary rather than widening analyzer semantics:

- keep the current analyzer contract
- keep the current capture pipeline
- test whether one structurally different mixed surface can now consume it honestly

This also passes the practical prioritization filter from the fixed-direction roadmap:

1. it does not push new analytical decision-making back downstream; it consumes analyzer-owned truth that already exists
2. it reduces the remaining host gap on a current served mixed surface rather than adding another analyzer-only semantic layer
3. it broadens the proof matrix beyond one pure findings surface
4. it would still matter if the current app shell were replaced, because the proof is about the sufficiency of the current analyzer-owned contract on a different surface shape

## Current Evidence Base

Seven concrete repo facts make this the right next slice:

1. analyzer-v2 already carries `finding_id` on rebuilt nested `aoi_by_theme[*].findings[]` items
2. whole-view `FirstHopAffordance` on `aoi_by_theme` intentionally remains generic-only:
   - no `specialized_family`
3. current bounded-V2 host rendering still does not operationalize those nested handles:
   - `hasViewRendererOverride('aoi_by_theme') === false`
4. `V2TabContent.tsx` already threads the runtime metadata the host would need for a bounded consumer proof:
   - `_workflowKey`
   - `_captureViewKey`
   - `_captureViewName`
   - `_captureSourceType`
   - `_onCapture`
   - `_captureMode`
   - `_firstHopAffordance`
5. `aoi_by_theme` is a genuinely mixed surface:
   - current default family is theme-keyed `accordion` content with nested `findings` rendered as `mini_card_list`
   - the adaptive dossier family is also `accordion` with nested `findings` rendered as `mini_card_list`
   - the adaptive comparison-review family is `table` and out of scope
6. legacy Critic thematic UI already proves theme-nested findings are meaningful downstream items:
   - `ThemeSynthesisCard.tsx`
7. the current pure-surface read-side route and hook now exist, but they do not answer the mixed-surface consumer question by themselves
8. the shared package `AccordionRenderer` already forwards:
   - `_captureMode`
   - `_onCapture`
   - `_captureViewKey`
   - `_parentSectionKey`
   - `_parentSectionTitle`
   into configured sub-renderers
9. the shared package `mini_card_list` already emits:
   - `source_renderer_type = "mini_card_list"`
   but it currently only supports one view-level capture `entity_id`, not per-card nested `finding_id`

Two honesty boundaries matter:

1. **Adaptive family variation**

`aoi_by_theme` can be adaptively rewritten in place under runtime surface families.
So this v1 must target only the still-findings-bearing mixed family shape:

- `renderer_type = "accordion"`
- nested `findings` rendered as `mini_card_list`

If `aoi_by_theme` is currently rewritten to a non-findings-bearing family such as a comparison-review table, that variant should remain out of scope and render unchanged.

2. **Legacy payloads**

Older persisted `aoi_by_theme` payloads may still be handle-less until rebuilt.
So a truthful host proof must degrade silently when nested `finding_id` is absent rather than pretending historical universal coverage now exists.

## Scope

### In scope

1. **One bounded `aoi_by_theme` host consumer proof**

Keep the proof local to Critic.
Do not add analyzer changes or backend changes in v1.

The preferred host shape is not a full `aoi_by_theme` view override.
The smallest honest move is one bounded local `mini_card_list` consumer seam on the existing `aoi_by_theme` accordion path.

More concretely:

- keep the current package `accordion` renderer and existing heterogeneous theme-section rendering intact
- intercept only the nested `findings` sub-renderer path
- replace generic `mini_card_list` behavior only when all of these are true:
  - current view is `aoi_by_theme`
  - current family is findings-bearing `accordion`
  - current nested sub-renderer is `mini_card_list`
- leave all other `aoi_by_theme` rendering unchanged, including:
  - non-findings sub-sections on the same accordion view
  - out-of-scope `table` comparison-review variants

This bounded local `mini_card_list` seam is acceptable as a v1 stepping stone.
It is not the intended long-term pattern.

2. **Capture-selection sufficiency on nested findings only**

The proof boundary should stay the same kind of boundary that worked on `aoi_by_sin_type`:

- show a bounded capture control on eligible finding cards
- clicking it creates a correct `CaptureSelection`
- the selection reaches the existing `CaptureActionBar`

But on this mixed surface, the control must appear only on nested thematic findings.

Do not add capture affordances to:

- theme headers
- overview sections
- engagement blocks
- claims
- commitments
- argumentative moves
- source document lists

3. **Keep whole-view semantics generic**

Do not add new analyzer semantics.
Do not require or invent a mixed-surface specialized family.

The host should rely only on:

- generic whole-view `FirstHopAffordance`
- non-empty nested `finding_id`

The capture guard is therefore intentionally weaker than the pure-surface `aoi_by_sin_type` specialization guard.

For this mixed-surface proof, the relevant condition is:

- `capturable === true` at the whole-view level
- non-empty `finding_id` on the individual nested finding card

It must **not** require:

- `specialized_family = "findings_bank_arsenal_promotion_v1"`

That means this slice proves:

- generic capturability plus nested item identity is already sufficient for one mixed-surface selection proof

not:

- `aoi_by_theme` is itself a whole-view findings-bank surface

4. **Stay passive-first and shape-preserving**

Outside capture mode, or when `finding_id` is absent, the surface should remain the same readable `aoi_by_theme` experience.

The proof should preserve the current mixed reading shape:

- theme sections
- existing nested content blocks
- existing findings subsection

The control should be additive and bounded.
It should not redesign the surface.

5. **Use config-threaded host values rather than literals**

As on the pure findings line, the renderer should use the values already threaded through `V2TabContent` rather than hard-coding them:

- `_captureViewKey`
- `_captureViewName`
- `_captureSourceType`
- `_workflowKey`

Freeze indexing and parent context explicitly:

- `source_item_index` is 0-based within the nested `findings` list for that theme section
- `source_section_key` and `parent_context.section_key` are the theme section key
- `parent_context.section_title` is the theme title
- `source_renderer_type = "mini_card_list"`

That `source_renderer_type` is not hypothetical in this scope.
It matches the current configured nested sub-renderer on the in-scope `aoi_by_theme` findings path.

6. **Make the in-scope family gate explicit**

The bounded host seam should not infer “in scope” from generic affordance presence alone.
Generic whole-view affordance may still be present on out-of-scope `aoi_by_theme` variants.

The in-scope gate should therefore be structural:

- `view_key == "aoi_by_theme"`
- current view `renderer_type == "accordion"`
- current nested path is the configured `findings -> mini_card_list` sub-renderer

The out-of-scope adaptive variant is currently:

- `renderer_type == "table"` for theme comparison review

That table variant should fall through unchanged even if generic whole-view affordance is present.

7. **Keep read-side status surfacing out of scope in v1**

The newly landed `POST /api/captures/status/by-entity` seam and the pure-surface read-back proof are useful background, but they are not the thing this next slice must prove.

This v1 should not also broaden into:

- nested mixed-surface status pills
- same-session optimistic status invalidation
- destination deep-linking
- repeat-capture policy

The question here is first:

- can the mixed surface produce a correct capture selection on nested findings at all?

### Explicitly out of scope

- analyzer-v2 code changes
- backend/API changes in Critic
- any new `specialized_family` on `aoi_by_theme`
- generic renderer-package capture law
- capture-status read-back on `aoi_by_theme`
- adaptive non-findings `aoi_by_theme` families such as comparison-review table variants
- non-AOI proof
- destination lifecycle, deep links, or repeat-capture policy

## Acceptance Bar

This slice is successful only if all of the following are true:

1. one current `aoi_by_theme` findings-bearing family can show bounded capture controls on nested finding cards only
   - using the existing `accordion` plus nested `mini_card_list` path
2. the proof relies on existing generic whole-view `FirstHopAffordance` plus non-empty nested `finding_id`, not on a new mixed-surface specialized family
3. a click on an eligible nested finding creates a correct `CaptureSelection` that reaches `CaptureActionBar`
4. non-finding portions of the mixed surface remain passive and unchanged
5. `aoi_by_theme` variants that do not expose nested findings stay on the existing rendering path unchanged
   - especially the adaptive comparison-review `table` variant
6. older or rebuilt-without-handle nested findings remain readable but unclickable
7. no analyzer or backend changes are required

## Test Plan

### Frontend unit tests

Add focused host coverage in Critic for the bounded mixed-surface consumer proof:

- focused local sub-renderer tests
  - the bounded local `mini_card_list` seam activates only on the in-scope `aoi_by_theme` findings path
  - findings-bearing accordion family renders the same readable mixed shape outside capture mode
  - nested finding cards with non-empty `finding_id` show capture controls only in capture mode
  - cards without `finding_id` remain passive
  - non-findings sections never show capture controls
  - emitted `CaptureSelection` uses:
    - config-threaded `source_view_key`
    - config-threaded `source_view_name`
    - config-threaded `source_type`
    - verified `source_renderer_type = "mini_card_list"`
    - 0-based section-local `source_item_index`
  - out-of-scope `aoi_by_theme` comparison-review `table` variant falls back unchanged
- `V2TabContent.test.tsx`
  - stay focused on existing config threading only
  - no new threading should be required

### Browser proof

Add one focused Playwright proof on the AOI V2 page:

- use or stub a bounded `aoi_by_theme` presentation that still exposes nested `findings` cards with `finding_id`
- enter capture mode
- verify the nested finding capture control appears
- click it
- assert on the existing `CaptureActionBar` boundary:
  - breadcrumb
  - title
  - preview text
  - action buttons

Stop at capture-selection creation and shared capture-UI handoff.
Do not treat backend persistence or read-back as the proof target in this slice.

## Why This Is The Right Next Step

The pure findings surface now has a bounded end-to-end loop.
The broader Phase E need is no longer to deepen that same exact line.

This mixed-surface proof is the next honest move because it tests a stronger question:

- whether the same already-landed analyzer-owned contract is sufficient on a structurally different served surface

That is more valuable than:

- one more `aoi_by_sin_type` refinement
- one more analyzer-only semantics change
- a premature generic renderer-package generalization

It is still smaller than:

- non-AOI broadening
- generic mixed-surface capture/status law
- end-to-end destination lifecycle semantics

So this is the right bounded next slice:

- vary the surface shape
- keep the contract fixed
- keep the host proof thin
- keep the claims honest
