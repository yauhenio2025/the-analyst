# Execution Plan: Round 4 / Adaptive Surface Suite Proof

Date: 2026-03-20
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-20_round4_adaptive_surface_suite_scope.md`

## Purpose

Turn the revised round-4 scope into a work-package execution plan.

This builds directly on the round-3 implementation. The main new variable is adding a second adaptive surface (`genealogy_conditions`) to operate alongside the existing relationship-landscape selector, coordinated under a single suite-mode proof token.

## Current Starting Point

### Already in code

Round 3 landed the following in `src/presenter/bounded_dynamic_composition.py`:

- `COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1` constant
- `_select_adaptive_relationship_surface()` — deterministic selector over per-item relationship cards
- three family builders: dossier / comparison / field-map
- `AdaptiveSurfaceSelection` dataclass with `as_trace_details()`
- `inspect_runtime_composition()` for trace diagnostics
- `_validate_runtime_payload()` for consumer capability + renderer contract validation
- helper functions: `_append_runtime_section`, `_extract_relationship_cards`, `_decorate_relationship_card`

Round-3 trace integration in `src/presenter/decision_trace.py`:

- `adaptive_surface_selection` stage with details, diff, and fail-closed handling
- composition_details populated from `inspect_runtime_composition()`
- stage-reason text includes selected family name on success

Critic host (already generic):

- `AnalysisWorkspacePage.tsx:175` reads `composition_mode` from search params
- `AnalysisWorkspacePage.tsx:80-88` maps mode strings to proof labels (two entries)
- `boundedV2Client.ts:123-162` threads `composition_mode` to manifest/presentation/refresh/single-view
- All restore, freshness, and skip-cache logic is mode-agnostic

### What round 4 needs to add

1. A new composition mode constant and routing branch
2. A conditions selector reading `payloads["genealogy_conditions"].structured_data`
3. Two conditions family builders (`conditions_balance_sheet`, `conditions_path_dependency_matrix`)
4. Suite-level coordination: both selectors run, both families replace their target surfaces
5. Suite-level trace with per-surface decision blocks
6. Tests for suite selection, validation, trace
7. One new Critic proof-label entry (generic string, no workflow logic)

## Work Packages

### WP0: Pre-Execution Signal Verification Gate

**Goal**: Verify that real genealogy job payloads expose enough structured signal on `genealogy_conditions` for the selector to work.

**Method**:

1. Pick at least one completed genealogy job (Varoufakis or Markus)
2. Call `GET /v1/presenter/page/{job_id}?consumer_key=the-critic`
3. Find the `genealogy_conditions` payload in the response
4. Check:
   - `structured_data` is present and is a dict (not null, not prose-only)
   - `structured_data` contains at least: `enabling_conditions`, `constraining_conditions`, `path_dependencies`
   - those fields are arrays with countable items
   - `meta` field is present or the arrays are sufficient to derive counts
5. Record findings

**Decision gate**:

- If structured_data is rich enough: proceed with conditions as second target
- If structured_data is prose-only or absent: switch to `genealogy_tactics` fallback per scope memo, rename proof token, and adjust WP1-WP3 accordingly

**No code changes in this WP.**

### WP1: Add Suite Mode Constant and Conditions Selector

**Goal**: Add the new composition mode, conditions selector, and conditions family builders.

**File**: `src/presenter/bounded_dynamic_composition.py`

**Changes**:

1. Add constant:
   ```python
   COMPOSITION_MODE_ADAPTIVE_SUITE_V1 = "adaptive_genealogy_relationship_conditions_v1"
   ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY = "genealogy_conditions"
   CONDITIONS_BALANCE_SHEET = "conditions_balance_sheet"
   CONDITIONS_PATH_DEPENDENCY_MATRIX = "conditions_path_dependency_matrix"
   ```

2. Add to `_SUPPORTED_COMPOSITION_MODES`

3. Add `_select_adaptive_conditions_surface(payloads)`:
   - Read `payloads["genealogy_conditions"].structured_data`
   - Extract signal from `meta` (preferred) or derive from arrays:
     - `enabling_conditions_count` = `len(structured_data.get("enabling_conditions", []))`
     - `constraining_conditions_count` = `len(structured_data.get("constraining_conditions", []))`
     - `path_dependencies_count` = `len(structured_data.get("path_dependencies", []))`
     - `alternative_paths_count` = `len(structured_data.get("alternative_paths", []))`
     - `unacknowledged_debts_count` = `len(structured_data.get("unacknowledged_debts", []))`
     - `counterfactual_present` = bool(structured_data.get("counterfactual_analysis"))
     - `synthesis_present` = bool(structured_data.get("synthetic_judgment"))
     - `overall_balance` from meta or derived from enabling vs constraining counts
   - Selection logic:
     - if `path_dependencies_count + alternative_paths_count > enabling_conditions_count + constraining_conditions_count`: choose `conditions_path_dependency_matrix`
     - else: choose `conditions_balance_sheet`
   - Return `AdaptiveSurfaceSelection` with signal_summary, rationale, rejected_families

4. Add `_build_conditions_balance_sheet_payload(base_payload, selection)`:
   - Top-level renderer: `accordion`
   - Sections per scope memo: `conditions_snapshot` (key_value_table), `enabling_pressures` (mini_card_list), `constraining_pressures` (mini_card_list), `unacknowledged_debts` (mini_card_list), `synthetic_judgment` (prose_block), `counterfactual_stakes` (prose_block)
   - Field mappings from scope memo section "Family 1"
   - Use `_append_runtime_section` for each section
   - Set `derivation_kind = DERIVATION_KIND_RUNTIME_SURFACE_FAMILY`

5. Add `_build_conditions_path_dependency_matrix_payload(base_payload, selection)`:
   - Top-level renderer: `table`
   - Multi-table: two logical tables as sections in an accordion:
     - "Path Dependencies" with columns: description, chain_depth, chain_summary, if_absent, is_acknowledged
     - "Alternative Paths" with columns: branching_point, path_not_taken, why_not_taken, implications
   - Since the scope says `table` top-level renderer but also says "multi-table container", use `accordion` with two table sections (this is how the platform models multi-table — one accordion with table sub-renderers)
   - Actually, re-reading the scope: "top-level renderer: table" + "multi-table container, not one merged flat row type". The cleanest way: use `accordion` as the top-level container with two `table` sub-renderer sections. This still counts as "the table family" because each section is a table. But the scope says renderer is `table`. Let's use `table` for the primary table (path dependencies) and include alternative paths as a second section — OR use the simpler approach: top-level `accordion` with two table sub-renderers. The scope says "At least one conditions family must use a different top-level renderer from the other. This requirement is satisfied by `table` vs `accordion`." So the balance sheet gets accordion, matrix gets table. For multi-table under table renderer: use the first table (path_dependencies) as the primary table, and add alternative_paths as a supplementary accordion section below. OR: simplify to a single merged table with a `table_group` column. Let me keep it simple: `table` renderer for path_dependencies rows. Alternative paths rows get their own separate section if we need multi-table. Actually the simplest: just use `table` with path_dependencies rows. Alternative paths can be a supplementary note. The scope says "Required tables: 1. Path Dependencies, 2. Alternative Paths" but also says "multi-table container, not one merged flat row type." The best approach: accordion with two table sub-renderers, matching the multi-table intent. BUT then both families are accordion, violating the scope constraint. Resolution: use the scope's own words — "This requirement is satisfied by `table` vs `accordion`." So path_dependency_matrix should be `table`. Use a single table with all rows, adding a `category` column to distinguish path-dep vs alternative-path rows. This is the pragmatic option. The `table` renderer already supports this. Field mappings:
     - For path dependency rows: `category="Path Dependency"`, `description`, `chain_depth`, `chain_summary`, `if_absent`, `is_acknowledged`
     - For alternative path rows: `category="Alternative Path"`, `branching_point` → `description`, `path_not_taken` → `chain_summary`, `why_not_taken` → `if_absent`, `implications` → `is_acknowledged` (overloaded)
   - No. That overloads semantics. Better: just show path_dependencies as the table. Alternative paths are supplementary. The scope explicitly says "This family should not depend on cross-schema row merging." So: path_dependencies table only. Alternative paths get a separate section if the conditions family is later enhanced but are not required for the v1 proof.
   - Final decision: `table` renderer, rows from `structured_data.path_dependencies` only. Columns: `description`, `chain_depth`, `chain_summary`, `if_absent`, `is_acknowledged`. This keeps it clean and avoids cross-schema merging.

6. Add `_apply_adaptive_suite(payloads, consumer_key)`:
   - Run `_select_adaptive_relationship_surface(payloads)` (already exists)
   - Run `_select_adaptive_conditions_surface(payloads)` (new)
   - Build relationship family payload (reuse existing builders)
   - Build conditions family payload (new builders)
   - Validate both payloads
   - Replace both in `payloads` dict
   - Return True

### WP2: Wire Suite Routing Through Composition Dispatcher

**Goal**: Connect the new mode to all existing routing points.

**Files**:

- `src/presenter/bounded_dynamic_composition.py`
  - `apply_bounded_dynamic_composition()`: add branch for `COMPOSITION_MODE_ADAPTIVE_SUITE_V1`
  - `get_runtime_composition_stage_name()`: return `"adaptive_surface_suite_selection"` for suite mode
  - `inspect_runtime_composition()`: handle suite mode — run both selectors, return combined details

- `src/presenter/decision_trace.py`
  - Import the new suite constant
  - At line 89, extend the `if composition_mode ==` check to also handle suite mode
  - The trace stage should contain an array of per-surface decision blocks instead of a single selection
  - The suite details dict should have shape:
    ```python
    {
        "suite_surfaces": [
            {  # relationship selection
                "target_surface": "genealogy_relationship_landscape",
                "selected_family": "...",
                "signal_summary": {...},
                "rejected_families": [...],
                "rationale": "..."
            },
            {  # conditions selection
                "target_surface": "genealogy_conditions",
                "selected_family": "...",
                "signal_summary": {...},
                "rejected_families": [...],
                "rationale": "..."
            }
        ]
    }
    ```
  - Stage reason should mention both selected families

No changes needed in:
- `src/api/routes/presenter.py` — already threads `composition_mode` generically
- `src/api/routes/results.py` — already threads `composition_mode` generically
- `src/presenter/presentation_api.py` — `apply_bounded_dynamic_composition()` is called at line 781, new mode routes through the same call

### WP3: Analyzer-v2 Test Coverage

**Goal**: Prove suite selection, validation, trace, and route-level behavior.

**Files**:

- `tests/test_presentation_api.py` — add suite-mode route tests
- `tests/test_manifest_trace.py` — add suite-mode trace tests
- `tests/test_analysis_product_contract.py` — add suite-mode result-contract tests

**Required tests**:

A. **Suite selection tests** (unit-level):
   1. Conditions selector returns `conditions_balance_sheet` when enabling+constraining counts dominate
   2. Conditions selector returns `conditions_path_dependency_matrix` when path_dep+alternative counts dominate
   3. Conditions selector fails closed when `genealogy_conditions` payload is missing
   4. Conditions selector fails closed when `structured_data` is None/empty
   5. Suite coordinator runs both selectors and replaces both surfaces

B. **Suite route tests** (integration-level):
   1. Manifest preserves `adaptive_genealogy_relationship_conditions_v1` mode
   2. Presentation threads the suite mode into page assembly
   3. Refresh threads the suite mode into page assembly
   4. Single-view route threads the suite mode
   5. Invalid suite mode returns 409 at route level

C. **Suite trace tests**:
   1. Trace returns `adaptive_surface_suite_selection` stage
   2. Stage details contain two decision blocks (one per surface)
   3. On validation failure: `composition_status = invalid`, diagnostics visible, authored manifest retained
   4. Trace diff shows both surfaces changed from authored baseline

D. **Conditions family validation tests**:
   1. Balance-sheet payload passes renderer config + data validation
   2. Path-dependency-matrix payload passes renderer config + data validation
   3. Invalid renderer/data contract returns BoundedCompositionValidationError

### WP4: Critic Host — One New Proof Label

**Goal**: The Critic recognizes the new suite mode for its generic proof-label display.

**File**: `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`

**Change**:

At `getCompositionProofLabel()` (line 80-88), add one case:

```typescript
const ADAPTIVE_SUITE_V1 = 'adaptive_genealogy_relationship_conditions_v1';

// inside getCompositionProofLabel:
if (compositionMode === ADAPTIVE_SUITE_V1) {
  return 'adaptive suite proof';
}
```

That is the only host change. No workflow-specific logic, no route branching, no deep-link rules.

### WP5: Manual Contrast-Job Proof

**Goal**: Produce human-verifiable evidence that two genealogy jobs diverge at two surfaces on the same route.

**Manual route**:

```
/p/:projectId/analysis/intellectual_genealogy?composition_mode=adaptive_genealogy_relationship_conditions_v1
```

**Required checks**:

1. One authored genealogy restore without proof mode (baseline)
2. One suite-mode restore for a job where relationship-landscape should select dossier AND conditions should select balance-sheet
3. One suite-mode restore for a job where relationship-landscape should select something different AND/OR conditions should select path-dependency-matrix
4. Trace inspection per suite-mode job — verify both decision blocks are present

**Preferred contrast pair**: Two genealogy jobs with different analytical profiles (Markus-like vs Varoufakis-like).

**Record for each**:
- job_id
- route used
- relationship family selected
- conditions family selected
- trace rationale for each surface

### WP6: Round-4 Proof Note

**Goal**: Close the stage cleanly.

**File**: `communications/PROOF_2026-03-20_round4_adaptive_surface_suite.md`

**Record**:

1. Proof token: `adaptive_genealogy_relationship_conditions_v1`
2. Two target surfaces: `genealogy_relationship_landscape`, `genealogy_conditions`
3. Contrast jobs used and selected families for each
4. Bounded claim: analyzer-v2 can choose validated runtime surface families for two genealogy surfaces on the same generic route, using deterministic signals from already-built structured payloads, and the existing generic host restores the result unchanged
5. Test results
6. Trace evidence

## Execution Order

```
WP0 (gate)
  │
  ├─ pass → WP1 + WP2 (can be done together)
  │           │
  │           └─ WP3 (tests)
  │               │
  │               └─ WP4 (Critic label — one line)
  │                   │
  │                   └─ WP5 (manual proof)
  │                       │
  │                       └─ WP6 (proof note)
  │
  └─ fail → switch second target to genealogy_tactics
            rename proof token
            revise WP1-WP3 for tactics
```

WP0 must complete before any code work. WP1 and WP2 are logically one unit (both touch the same module). WP3 depends on WP1+WP2. WP4 is a one-line change that can land anytime after WP2. WP5 requires everything else to be working. WP6 closes the stage.

## Acceptance Checklist

Treat round 4 as complete only if:

1. [ ] WP0 gate passed: conditions structured_data verified on a real job
2. [ ] Suite mode constant registered and routed
3. [ ] Conditions selector runs deterministically over structured_data
4. [ ] Two conditions families build valid payloads with correct renderer contracts
5. [ ] Suite coordinator replaces both surfaces in a single composition pass
6. [ ] Suite-level trace shows per-surface decision blocks
7. [ ] Fail-closed behavior on missing/invalid payloads
8. [ ] Critic proof label appears for suite mode
9. [ ] Two contrast genealogy jobs select different family combinations
10. [ ] Proof note written with trace evidence

## What Not To Do

- Do not add a third adaptive surface
- Do not reopen relationship-landscape families
- Do not stack suite mode on top of round-2 or round-3 modes
- Do not add workflow-specific Critic host logic beyond the proof label
- Do not introduce an LLM inference pass for the conditions selector
- Do not merge path-dependency and alternative-path data into one flat table type
- Do not generalize the suite mechanism beyond the two named surfaces
