# Scope Critique: Round 6 / Cross-Workflow Adaptive AOI Suite Proof

Reviewer: Claude Opus 4.6
Date: 2026-03-21
Subject: `communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_scope.md`

---

## Verdict

**Conditionally approve with two required revisions and one structural warning.**

The memo correctly identifies the next meaningful platform variable — coordinated multi-surface adaptive composition across workflows — and makes a defensible case for proving it on AOI. The scope discipline is tight and the boundary rules are mostly well-drawn. But the memo overestimates how straightforward the `aoi_thematic_report` seam is, under-specifies the suite orchestration mechanics relative to what the code actually requires, and leaves one important ambiguity in the trace grammar that could become a subtle integration regression.

---

## Findings

### 1. `aoi_thematic_report` vs `aoi_by_sin_type` — The Second Target Choice

**The memo's argument is strategically correct but operationally risky.**

The memo argues `aoi_thematic_report` is the right second AOI target because it comes from a distinct phase-4 engine and proves coordination across unlike child surfaces. This is the right strategic instinct. Two views over the same phase-3 finding set (which is what `aoi_by_theme` + `aoi_by_sin_type` would give you) would indeed not prove much about suite coordination — it would just be the same payload with two regrouping strategies.

However, the `aoi_thematic_report` payload shape is materially harder to work with than the memo acknowledges:

1. **The structured payload lives at `payloads["aoi_thematic_report"].structured_data`, which is populated from `_normalize_thematic_report()` in `src/aoi/contract.py` (line 87).** That function stores `report_sections` as the value of `structured_payloads["aoi_thematic_report"]`. So the actual runtime shape is `structured_data.summary`, `structured_data.engagement_pattern`, etc. — a flat dict of 5 keys, not a section-ordered grouped payload like `aoi_by_theme`. The memo's Gate B correctly names these 5 keys, so this is not a factual error — but it is a structural asymmetry the memo does not address.

2. **`key_divergences` is not a stable card list.** It is built by `_build_key_divergence_cards()` (contract.py line 433-444) as a **fallback** — it is used only when `report_sections.key_divergences` is not present in the LLM's parsed output. When the LLM does produce `key_divergences` directly in `report_sections`, the shape depends entirely on what the LLM emitted. The normalization code at line 350 does `report_sections.get("key_divergences") or _build_key_divergence_cards(findings)`, meaning if the LLM returns even a partial truthy value, the fallback builder is skipped. The memo's Gate B treats this as a stable card list with `title/subtitle/description/badge` — that is only guaranteed when the fallback builder runs. On real LLM output, you may get prose strings, dicts with different keys, or mixed structures.

3. **`sin_distribution` has the same instability.** The fallback builder (`_build_sin_distribution`, line 447-458) produces `{sin_type, count, description}` — but the normalization code at line 351 again prefers the LLM's raw `report_sections.sin_distribution` output over the deterministic builder.

**This means Gate B as written is necessary but may not be sufficient.** The gate checks for the existence of keys but should also check for the structural shape of `key_divergences` and `sin_distribution` values — are they actually lists of dicts with the expected fields? If the LLM emitted prose or a partial structure, the gate should fail and trigger the fallback to `aoi_by_sin_type`.

**Recommended revision**: Strengthen Gate B to validate not just key existence but value shape: `key_divergences` must be a non-empty list where each item has at least `title` and `description`, and `sin_distribution` must be a list where each item has at least `sin_type` and `count`. If shape validation fails, treat it as a gate failure.

### 2. Suite Orchestration Mechanics — The Real Hidden Complexity

The memo proposes reusing `adaptive_surface_suite_selection` from round 4. This is the right call in principle, but there is a meaningful structural difference the memo does not surface.

**Round 4's suite coordinated two top-level surfaces.** Both `genealogy_relationship_landscape` and `genealogy_conditions` are top-level views that appear directly in the manifest. The suite selector ran two independent selectors and composed them into `AdaptiveSurfaceSuiteSelection.surface_decisions`.

**Round 6 proposes coordinating two child surfaces under the same parent.** Both `aoi_by_theme` and `aoi_thematic_report` are children of `aoi_thematic_analysis`. This means the suite apply function must:

1. Find and rewrite two **child** payloads in `payloads` dict
2. **Not touch** the parent `aoi_thematic_analysis` payload
3. Ensure both rewrites preserve `source_parent_view_key = "aoi_thematic_analysis"`
4. Ensure the parent tab container's child ordering is not disrupted

The existing `_apply_adaptive_aoi_theme_surface()` (lines 518-542) already handles one child-surface rewrite. Extending this to a second child surface is mechanically straightforward — but the memo should explicitly note that the **suite apply function for AOI must compose two child-surface rewrites**, not two top-level surface rewrites as in round 4. This is not a blocker, but it is a difference in kind that implementors need to understand.

The existing `AdaptiveSurfaceSuiteSelection` dataclass (lines 118-127) and its `as_trace_details()` method are generic enough to carry this — the tuple of decisions does not care whether decisions target top-level or child surfaces. So the trace grammar does generalize. The apply function is the part that needs new work.

### 3. The Generic-Host-Only Claim Is Sound

The memo claims round 6 should remain generic-host-only. I verified this by inspecting the Critic side:

- `AnalysisWorkspacePage.tsx` (line 83-96) has `getCompositionProofLabel()` which is a pure string map. Adding one new mode token is trivially generic.
- The page does not contain any workflow-specific renderer logic or surface-specific adaptive logic.
- `AoiV2ThematicPanel.tsx` does **not** pass `compositionMode` into the bounded-v2 path (confirmed at line 6-7 and props interface at line 54-58). This means the bespoke panel cannot accidentally consume the proof mode.

The claim that round 6 is generic-host-only is **correct** and well-supported by the code.

### 4. Report-Family Contracts — Specificity Assessment

The two proposed report families are specified at different levels of concreteness:

**`aoi_report_briefing` (accordion)** — well specified. The section order, section renderers, and sub-renderer assignments are complete and follow the same pattern already proven in `aoi_theme_dossier`. The addition of `suite_summary` as a leading prose block mirrors the existing pattern. This is implementable as-is.

**`aoi_report_evidence_review` (table)** — adequately specified but has one gap. The memo says the table should be a "multi-table container" with three required tables: `Report Snapshot`, `Key Divergences`, `Sin Distribution`. But the existing `table` renderer in the codebase is a **single flat table** renderer, not a multi-table container. Round 4's `conditions_path_dependency_matrix` used a single table with one flat row array.

This means either:

- (a) The `aoi_report_evidence_review` family needs to use a different top-level layout (e.g., accordion with table sub-renderers for each section), or
- (b) The implementation needs to flatten three logical tables into one, or
- (c) The table renderer needs multi-table support

Option (a) would make both report families use `accordion`, violating the memo's own "at least one report family should use a different top-level renderer type" rule. Option (c) is out of scope. Option (b) is achievable but loses the nice logical separation.

**Recommended revision**: Either redesign `aoi_report_evidence_review` as a single flat table (one row per divergence/distribution entry, with a `section` column to distinguish the logical groups), or accept that both families may use `accordion` with different section-level sub-renderers. The "multi-table container" claim is not currently supported by the renderer catalog and should not be stated as if it is.

### 5. Suite Trace Shape — Correct Reuse of Round-4 Pattern

The proposed trace shape — `adaptive_surface_suite_selection` with `surface_decisions: []` containing one item per adaptive target — is a direct reuse of the existing `AdaptiveSurfaceSuiteSelection.as_trace_details()` at line 121-127. This generalizes cleanly.

The decision_trace.py trace dispatch (lines 221-226) already handles `adaptive_surface_suite_selection` as a stage name and renders per-surface selected families in the stage reason text (lines 239-256). The trace grammar will work without modification to `decision_trace.py` as long as:

1. The new suite composition mode returns `"adaptive_surface_suite_selection"` from `get_runtime_composition_stage_name()`
2. The inspect function returns an `AdaptiveSurfaceSuiteSelection` with two decisions

Both are mechanically trivial. **The trace reuse claim is correct.**

### 6. Documentary Gate — Correctly Framed

The memo states round 6 is scope-ready but implementation-gated until round 5's proof note exists. Round 5's completion memo confirms code-complete and test-complete but route-proof-pending. This gate is correctly framed — scoping can proceed, but implementation should not start until round 5 has its proof record.

One clarification: the memo says "round 5 is not yet route-proof-complete because the synthetic-but-route-real AOI fixtures and proof note have not yet been written." This is accurate based on the round-5 completion memo which explicitly states 0 completed AOI jobs exist locally. The gate is honest.

---

## What Looks Right

1. **The strategic thesis is correct.** Coordinated multi-surface suite composition across workflows is the right next variable to isolate after round 5 proved single-surface cross-workflow generalization.

2. **The scope boundary is tight.** Two AOI child surfaces, deterministic selection, no new inference passes, no host-side workflow logic, no parent container restructuring.

3. **Keeping `aoi_by_theme` as the first target** is correct. Reuse of proven round-5 work avoids rework.

4. **The fallback to `aoi_by_sin_type`** is named and gated. This is honest risk management.

5. **The trace grammar reuse** is sound. `AdaptiveSurfaceSuiteSelection` and the suite stage in `decision_trace.py` generalize without modification.

6. **The independent composition mode** (`adaptive_aoi_theme_report_suite_v1`) correctly avoids mode-stacking.

7. **The documentary gate** is correctly positioned. Scoping now, implementing after round-5 closure.

---

## What Needs Tightening

### A. Gate B Shape Validation (Required)

Gate B checks key existence but not value shape. `key_divergences` and `sin_distribution` in the `aoi_thematic_report` payload are only guaranteed to have the expected card/distribution shape when the normalization fallback builders run. When the LLM produces its own `report_sections`, the shape is unpredictable. Gate B must validate structural shape (list of dicts with expected fields), not just key presence.

### B. Table Renderer Multi-Table Claim (Required)

The `aoi_report_evidence_review` family is described as a "multi-table container" with three named tables. The existing `table` renderer does not support multi-table containers. Either flatten to a single table, switch to accordion with table sub-renderers, or acknowledge that both families may use the same top-level renderer type.

### C. Child-Surface Suite Asymmetry (Clarification)

The memo should explicitly note that the AOI suite coordinates **child surfaces under a shared parent**, unlike the genealogy suite which coordinates top-level surfaces. This changes the apply function's mechanics (must find children in the payloads dict and preserve parent references) even though the trace grammar is unchanged. This is not a blocker — the round-5 `_apply_adaptive_aoi_theme_surface` already handles child-surface rewrite semantics — but an implementor unfamiliar with the distinction between round 4 and round 6's structural context could miss it.

### D. Selector B Pre-Selection Failure Mode (Minor)

The memo proposes a selector for `aoi_thematic_report` that counts `key_divergence_count` and `sin_distribution_count`. But if Gate B's shape validation fails (items are prose, not dicts), these counts are meaningless. The selector should explicitly handle the case where the payload exists but is structurally degenerate — either by failing closed to a default family or by treating structurally invalid data as count-zero.

### E. `suite_summary` Generation for Report Families (Minor)

The memo specifies `suite_summary` as a section in the briefing family but does not specify how it is generated. The `aoi_theme_dossier` builder uses a deterministic sentence template. The report families should have an equivalent specified — what text goes in `suite_summary` for a report briefing vs. a report evidence review?

---

## Recommended Revision

1. **Strengthen Gate B**: Add structural shape validation for `key_divergences` (must be `list[dict]` with `title` and `description`) and `sin_distribution` (must be `list[dict]` with `sin_type` and `count`). Fail the gate if shapes do not match.

2. **Revise `aoi_report_evidence_review`**: Either redesign as a single flat table with a `section` discriminator column, or switch to `accordion` with `table` sub-renderers per logical section. Drop the "multi-table container" claim.

3. **Add a one-sentence note** in the "Name The Backend Expansion Honestly" section: "Unlike the genealogy suite which coordinates top-level surfaces, the AOI suite coordinates child surfaces under a shared parent. The apply function must compose two child-surface rewrites while preserving `source_parent_view_key` on both."

4. **(Optional)** Specify `suite_summary` derivation rules for both report families, following the pattern already established in `aoi_theme_dossier`.

Items 1 and 2 are required before this scope memo should be treated as execution-ready. Items 3 and 4 are strongly recommended but not blocking.
