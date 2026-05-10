# Round 5 Execution Plan: Cross-Workflow Adaptive AOI Theme Proof

Date: 2026-03-20
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md`

## Summary

Execute round 5 as a gated proof tranche on the existing generic AOI route.

Public proof contract:

- `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=<id>&selected_source_thinker_name=<name>&composition_mode=adaptive_aoi_theme_surface_v1`

Bounded claim:

- analyzer-v2 can adapt one AOI child surface (`aoi_by_theme`) in place under its existing parent tab container (`aoi_thematic_analysis`)
- the same adaptive composition discipline proven on genealogy generalizes to a materially different workflow
- the Critic host stays generic in substance
- proof behavior stays deterministic, inspectable, and fail-closed

Hard stop condition:

- if WP0 shows the top-level `aoi_by_theme` payload is not stable enough on the actual candidate proof jobs, abort this branch before implementation and pivot the target to `aoi_thematic_report` in a short memo correction

## Current Starting Point

### Already in code

The adaptive composition module (`src/presenter/bounded_dynamic_composition.py`) provides:

- three genealogy composition modes
- `AdaptiveSurfaceSelection` dataclass and `as_trace_details()`
- `_validate_runtime_payload()` for consumer capability + renderer contract validation
- `_append_runtime_section()` for building accordion sections
- `_has_runtime_value()` for value presence checking

The trace module (`src/presenter/decision_trace.py`) provides:

- `adaptive_surface_selection` and `adaptive_surface_suite_selection` stages
- composition_details populated from `inspect_runtime_composition()`
- stage-reason text composition

The Critic host (`AnalysisWorkspacePage.tsx`) provides:

- `composition_mode` read from URL search params (line 175)
- `getCompositionProofLabel()` mapping three modes to proof labels (lines 80-88)
- generic `useBoundedV2Workspace` threading `composition_mode` through manifest/presentation/refresh/single-view
- AOI workflow detection at line 172 (`isAoiWorkflow`)

### What is genealogy-locked and must widen

1. **Module docstring** (line 1): `"Proof-only runtime composition for genealogy presentations."` — needs to become workflow-general
2. **`_SUPPORTED_COMPOSITION_MODES`** (lines 29-33): only contains genealogy modes
3. **`validate_requested_composition_mode`** (line 228): `if workflow_key != GENEALOGY_WORKFLOW_KEY` — must accept AOI workflow for AOI modes
4. **`apply_bounded_dynamic_composition`** (lines 258-272): dispatch only has genealogy branches
5. **`get_runtime_composition_stage_name`** (lines 275-281): only returns genealogy stage names
6. **`inspect_runtime_composition`** (lines 284-301): only dispatches for genealogy modes
7. **`decision_trace.py`** (lines 90-93): adaptive inspection dispatch only covers genealogy modes

## Work Packages

### WP0: AOI Signal Verification Gate

Run a read-only inspection against the same two candidate AOI proof jobs intended for the final round-5 proof.

Default candidate-proof shape:

- Job A should produce a dominant-theme case (one or two themes with most findings)
- Job B should produce a distributed-theme case (three or more themes with even findings)
- If natural contrast jobs do not exist locally, create synthetic-but-route-real proof fixtures later, and use those exact fixtures for WP0 and final proof

Pass criteria for `aoi_by_theme` on both candidate jobs:

1. `payloads["aoi_by_theme"].structured_data` exists
2. top-level keys: `_section_order`, `_section_titles`
3. one dict per theme id with all 7 fields:
   - `overview` (string)
   - `engagement` (formatted string)
   - `key_claims` (list of `{title, description}`)
   - `philosophical_commitments` (list of `{title, description}`)
   - `argumentative_moves` (list of `{title, description}`)
   - `source_documents` (list of title strings)
   - `findings` (list of finding cards)
4. each finding card exposes: `title`, `subtitle`, `description`, `badge`, `sin_type`, `sin_type_label`

Treat these as hard pre-selection failures:

- `_section_order` missing
- `_section_order` empty
- `_section_titles` missing
- `_section_titles` missing an entry for any theme id named in `_section_order`
- a theme id named in `_section_order` has no matching payload object

If WP0 fails:

- stop the `aoi_by_theme` branch before code changes
- pivot to `aoi_thematic_report`
- rename the proof token before implementation begins

### WP1: Widen Composition Module For Cross-Workflow Dispatch

**Goal**: Make `bounded_dynamic_composition.py` accept AOI workflow + mode without breaking genealogy.

**File**: `src/presenter/bounded_dynamic_composition.py`

**Changes**:

1. Update module docstring:
   ```python
   """Proof-only runtime composition for presentations."""
   ```

2. Add constants:
   ```python
   from src.aoi.constants import AOI_WORKFLOW_KEY

   COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1 = "adaptive_aoi_theme_surface_v1"
   ADAPTIVE_AOI_THEME_VIEW_KEY = "aoi_by_theme"
   AOI_THEME_DOSSIER = "aoi_theme_dossier"
   AOI_THEME_COMPARISON_REVIEW = "aoi_theme_comparison_review"
   ```

3. Add to `_SUPPORTED_COMPOSITION_MODES`

4. Add workflow-mode mapping:
   ```python
   _MODE_WORKFLOW_MAP = {
       COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1: GENEALOGY_WORKFLOW_KEY,
       COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1: GENEALOGY_WORKFLOW_KEY,
       COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1: GENEALOGY_WORKFLOW_KEY,
       COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1: AOI_WORKFLOW_KEY,
   }
   ```

5. Replace the `validate_requested_composition_mode` workflow check:
   ```python
   # Before:
   if workflow_key != GENEALOGY_WORKFLOW_KEY:
       raise InvalidCompositionModeError(...)

   # After:
   expected_workflow = _MODE_WORKFLOW_MAP.get(composition_mode)
   if expected_workflow and workflow_key != expected_workflow:
       raise InvalidCompositionModeError("invalid_composition_mode_for_workflow")
   ```

6. Add AOI branch in `apply_bounded_dynamic_composition`:
   ```python
   if composition_mode == COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1:
       return _apply_adaptive_aoi_theme_surface(
           payloads=payloads,
           consumer_key=consumer_key,
       )
   ```

7. Add AOI branch in `get_runtime_composition_stage_name`:
   ```python
   if composition_mode == COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1:
       return "adaptive_surface_selection"
   ```
   (Reuse the same stage name — the point is to prove the existing trace grammar generalizes.)

8. Add AOI branch in `inspect_runtime_composition`:
   ```python
   if composition_mode == COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1:
       selection = _select_adaptive_aoi_theme_surface(payloads)
       return selection.as_trace_details()
   ```

### WP2: AOI Theme Selector And Family Builders

**Goal**: Add the deterministic selector and two family builders.

**File**: `src/presenter/bounded_dynamic_composition.py`

**A. Selector: `_select_adaptive_aoi_theme_surface(payloads)`**

1. Read `payloads["aoi_by_theme"]` — fail closed if missing
2. Read `structured_data` — fail closed if None/empty
3. Extract `_section_order`, `_section_titles`, and per-theme payloads
4. Fail closed before selection if:
   - `_section_order` is missing or empty
   - `_section_titles` is missing
   - `_section_titles` lacks an entry for any theme id in `_section_order`
   - a theme id in `_section_order` has no matching payload object
4. Compute signal summary:
   - `theme_count = len(_section_order)`
   - per theme: `finding_count = len(theme_payload["findings"])`
   - `total_finding_count = sum of all finding_counts`
   - rank themes deterministically by:
     1. `finding_count` descending
     2. `source_document_count` descending
     3. `key_claim_count` descending
     4. `theme_name` ascending
     5. `theme_id` ascending
   - `dominant_theme_id` = first ranked theme
   - `dominant_theme_findings` = count of dominant theme's findings
   - `dominant_theme_share = dominant_theme_findings / total_finding_count` (or 1.0 if total is 0)
   - `second_theme_findings` = second-ranked theme's finding count (or `0`)
   - per theme: `dominant_sin_type` = most frequent `sin_type_label` in that theme's findings, with alphabetical tie-break on label, or `"—"` if no findings
   - per theme: `source_document_count = len(theme_payload["source_documents"])`
   - per theme: `key_claim_count = len(theme_payload["key_claims"])`
5. Decision rule:
   - if `total_finding_count == 0`, choose `AOI_THEME_DOSSIER`
   - otherwise choose `AOI_THEME_DOSSIER` iff: `theme_count <= 3` AND `dominant_theme_share >= 0.5`
   - otherwise choose `AOI_THEME_COMPARISON_REVIEW`
6. Return `AdaptiveSurfaceSelection` with signal_summary, rationale, rejected_families

**B. Family builder: `_build_aoi_theme_dossier_payload(base_payload, selection)`**

- Top-level renderer: `accordion`
- Build `structured_data` with:
  - `suite_summary`
    - deterministic derivation rule:
      - if `total_finding_count > 0`:
        - `"{dominant_theme_name} carries {dominant_theme_findings} of {total_finding_count} findings across {theme_count} themes, so the surface is rendered as a dossier-led thematic reading."`
      - otherwise:
        - `"{theme_count} themes are present with no bound findings, so the surface is rendered as a dossier-led thematic reading."`
    - where:
      - `dominant_theme_name` comes from `_section_titles[dominant_theme_id]`
      - `dominant_theme_findings`, `total_finding_count`, and `theme_count` come from the selector signal summary
  - `_section_order` from original payload
  - `_section_titles` from original payload
  - one normalized theme object per theme id containing: `overview`, `engagement`, `key_claims`, `philosophical_commitments`, `argumentative_moves`, `source_documents`, `findings`
- Build `renderer_config` with:
  - `suite_summary` as the first accordion section via `prose_block`
  - one section per theme id after `suite_summary`
  - `_default` section renderer with sub-renderers matching the authored `aoi_by_theme.json` config:
    - `overview -> annotated_prose`
    - `engagement -> annotated_prose`
    - `key_claims -> rich_description_list` (title_field: "title", description_field: "description")
    - `philosophical_commitments -> rich_description_list`
    - `argumentative_moves -> rich_description_list`
    - `source_documents -> chip_grid`
    - `findings -> mini_card_list` (title_field: "title", subtitle_field: "subtitle", description_field: "description", badge_field: "badge")
- Set `view_name = "Theme Dossier"`
- Set `derivation_kind = DERIVATION_KIND_RUNTIME_SURFACE_FAMILY`
- Preserve `source_parent_view_key = "aoi_thematic_analysis"` (in-place child replacement)

**C. Family builder: `_build_aoi_theme_comparison_review_payload(base_payload, selection)`**

- Top-level renderer: `table`
- Build one row per theme from the original structured_data:
  - `theme_name` from `_section_titles[theme_id]`
  - `finding_count` from `len(findings)`
  - `dominant_sin_type` from most frequent `sin_type_label` in findings (or "—" if no findings)
  - `source_document_count` from `len(source_documents)`
  - `key_claim_count` from `len(key_claims)`
  - `overview_excerpt` from deterministic truncation of `overview`:
    - start from `overview.strip()`
    - if empty, use `"—"`
    - if length `<= 150`, use as-is
    - if length `> 150`, use first `147` chars + `...`
- Build `renderer_config` with columns:
  ```python
  {"key": "theme_name", "label": "Theme", "sortable": True}
  {"key": "finding_count", "label": "Findings", "sortable": True}
  {"key": "dominant_sin_type", "label": "Dominant Sin Type", "sortable": True}
  {"key": "source_document_count", "label": "Sources", "sortable": True}
  {"key": "key_claim_count", "label": "Key Claims", "sortable": True}
  {"key": "overview_excerpt", "label": "Overview", "sortable": False}
  ```
- Set `structured_data` to the row array
- Set `view_name = "Theme Comparison Review"`
- Set `derivation_kind = DERIVATION_KIND_RUNTIME_SURFACE_FAMILY`
- Preserve `source_parent_view_key = "aoi_thematic_analysis"` (in-place child replacement)

**D. Apply function: `_apply_adaptive_aoi_theme_surface(payloads, consumer_key)`**

1. Run `_select_adaptive_aoi_theme_surface(payloads)`
2. Build the selected family payload
3. Validate with `_validate_runtime_payload(payload, consumer_key=consumer_key)`
4. If validation fails: raise `BoundedCompositionValidationError`
5. Replace `payloads[ADAPTIVE_AOI_THEME_VIEW_KEY]` with the new payload
6. Return True

### WP3: Widen Decision Trace For AOI

**Goal**: Make the trace dispatch include the AOI mode.

**File**: `src/presenter/decision_trace.py`

**Change at lines 90-93**:

```python
# Before:
if composition_mode in {
    COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
    COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
}:

# After:
if composition_mode in {
    COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
    COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
    COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1,
}:
```

Import the new constant at the top of the file.

The existing `inspect_runtime_composition()` call at line 101 already delegates to `bounded_dynamic_composition.py`, which WP1 already widened. So the trace dispatch only needs the new mode added to the set.

### WP4: Analyzer-v2 Test Coverage

**Goal**: Prove AOI adaptive selection, validation, trace, and route-level behavior.

**Files**:

- `tests/test_presentation_api.py`
- `tests/test_manifest_trace.py`
- `tests/test_analysis_product_contract.py`

**Required tests**:

A. **AOI selector tests** (unit-level):
1. Selector returns `aoi_theme_dossier` when `theme_count <= 3` and `dominant_theme_share >= 0.5`
2. Selector returns `aoi_theme_comparison_review` when themes are distributed
3. Selector fails closed when `aoi_by_theme` payload is missing
4. Selector fails closed when `structured_data` is None/empty

B. **AOI route tests** (integration-level):
1. Manifest preserves `adaptive_aoi_theme_surface_v1` mode
2. Presentation threads the AOI mode into page assembly
3. Refresh threads the AOI mode into page assembly
4. Single-view route threads the AOI mode
5. Invalid AOI mode returns 400 at route level
6. Genealogy modes on AOI workflow reject with 400
7. AOI mode on genealogy workflow rejects with 400
8. Validation failure inside the AOI adaptive builder returns 409
9. Missing `_section_titles` entry for a referenced theme id fails closed

C. **AOI trace tests**:
1. Trace returns `adaptive_surface_selection` stage for AOI mode
2. Stage details contain `target_surface = "aoi_by_theme"`
3. On adaptive payload/family validation failure after mode acceptance: `composition_status = invalid`, diagnostics visible, authored manifest retained
4. Invalid mode and wrong workflow/mode pairing still return 400 on trace

D. **In-place child replacement tests**:
1. After dossier selection: `payloads["aoi_by_theme"].source_parent_view_key == "aoi_thematic_analysis"`
2. After comparison selection: same parent preservation
3. Parent tab container `aoi_thematic_analysis` is not modified
4. Zero-findings payload still selects dossier without treating the surface as structurally invalid

E. **No-regression tests**:
1. `bounded_dynamic_genealogy_v1` still works
2. `adaptive_relationship_surface_v1` still works
3. `adaptive_genealogy_relationship_conditions_v1` still works

### WP5: Critic Host — One New Proof Label

**Goal**: The Critic recognizes the new AOI suite mode for its generic proof-label display.

**File**: `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`

**Change at `getCompositionProofLabel()` (lines 80-88)**:

```typescript
const ADAPTIVE_AOI_THEME_SURFACE_V1 = 'adaptive_aoi_theme_surface_v1';

if (compositionMode === ADAPTIVE_AOI_THEME_SURFACE_V1) {
  return 'adaptive AOI theme proof';
}
```

That is the only host change. No workflow-specific logic, no route branching.

### WP6 (Optional): Thinker-Page Proof Handoff Link

**Goal**: Add a convenience link from the bespoke AOI thinker page to the generic proof route.

**File**: `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx`

**Scope**: One route-constructor `<a>` or `<Link>` that builds:
```
/p/{projectId}/analysis/anxiety_of_influence_thematic_single_thinker
  ?selected_source_thinker_id={thinkerId}
  &selected_source_thinker_name={thinkerName}
  &composition_mode=adaptive_aoi_theme_surface_v1
```

This should NOT:
- transfer bespoke panel state
- transfer restore state or cached results
- require any new bespoke component logic

If this proves more complex than a one-line link, skip it for now. The generic route works directly from the browser.

### WP7: Route-Real Contrast-Job Proof

**Goal**: Produce recorded route-real evidence that two AOI jobs diverge at the `aoi_by_theme` surface on the same generic route.

**Proof route**:
```
/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker
  ?selected_source_thinker_id=<id>
  &selected_source_thinker_name=<name>
  &composition_mode=adaptive_aoi_theme_surface_v1
```

**Required checks**:

1. One authored AOI restore without proof mode (baseline)
2. One proof-mode AOI restore where `aoi_by_theme` selects `aoi_theme_dossier`
3. One proof-mode AOI restore where `aoi_by_theme` selects `aoi_theme_comparison_review`
4. Trace inspection per proof-mode job — verify selection details present

**Record for each**:
- job id
- selected source thinker
- route used
- selected family
- trace rationale

### WP8: Round-5 Proof Note And Completion Memo

**Goal**: Close the stage cleanly.

**Files**:
- `communications/PROOF_2026-03-20_round5_cross_workflow_adaptive_aoi_theme.md`
- `communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_completion.md`

**Record**:
1. Proof token: `adaptive_aoi_theme_surface_v1`
2. Target surface: `aoi_by_theme` (child of `aoi_thematic_analysis`)
3. Contrast jobs and selected families
4. Bounded claim: the adaptive composition discipline generalizes across two materially different workflow families
5. Test results
6. Trace evidence

## Execution Order

```
WP0 (gate)
  │
  ├─ pass → WP1 + WP2 (same file, do together)
  │           │
  │           └─ WP3 (trace widening, tiny)
  │               │
  │               └─ WP4 (tests)
  │                   │
  │                   ├─ WP5 (Critic label — one line)
  │                   ├─ WP6 (optional handoff link)
  │                   │
  │                   └─ WP7 (manual proof)
  │                       │
  │                       └─ WP8 (proof note)
  │
  └─ fail → pivot to aoi_thematic_report
            rename proof token
            revise WP1-WP4 accordingly
```

## Acceptance Checklist

1. [ ] WP0 gate passed: `aoi_by_theme` structured_data verified on candidate proof jobs
2. [ ] Composition module accepts AOI workflow for AOI mode
3. [ ] AOI selector runs deterministically over `aoi_by_theme` payload
4. [ ] Two AOI families build valid payloads (dossier=accordion, comparison=table)
5. [ ] In-place child replacement preserves `source_parent_view_key = "aoi_thematic_analysis"`
6. [ ] Trace returns `adaptive_surface_selection` with `target_surface = "aoi_by_theme"`
7. [ ] Fail-closed behavior on missing/invalid payloads, including partial `_section_titles`
8. [ ] No regressions to genealogy proof modes
9. [ ] Critic proof label appears for AOI mode
10. [ ] Two contrast AOI jobs select different families on the same generic route
11. [ ] Proof note written with trace evidence
12. [ ] Route-real proof artifacts saved under `communications/`

## What Not To Do

- Do not add a second AOI adaptive surface
- Do not promote `aoi_by_theme` to top-level
- Do not restructure the AOI page tree
- Do not modify `AoiV2ThematicPanel` for proof purposes
- Do not add workflow-specific Critic host logic beyond the proof label
- Do not introduce an LLM inference pass for the AOI selector
- Do not stack this mode on top of any genealogy proof mode
- Do not reopen AOI engine contracts or normalization logic
