# Claude Critique: Round 5 Cross-Workflow Adaptive AOI Theme Scope

Date: 2026-03-20
Scope memo under review: `communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md`

## Verdict

The memo correctly identifies the right next strategic variable -- proving that adaptive composition is not genealogy-specific -- and `aoi_by_theme` is a defensible first cross-workflow target. The payload shape assumptions in the memo are well-grounded: the actual `_build_by_theme_payload` function in `src/aoi/contract.py:357-415` does produce `_section_order`, `_section_titles`, and per-theme objects with `overview`, `engagement`, `findings`, and `source_documents` exactly as the memo describes. However, the memo underestimates the structural surgery required in `bounded_dynamic_composition.py`, mischaracterizes the host situation, and leaves the AOI rendering-path question unaddressed. These are correctable problems, not scope-killing ones.

## What The Memo Gets Right

1. **Strategic sequencing is sound.** Rounds 1-4 proved adaptive composition only within `intellectual_genealogy`. The "genealogy-specific overfitting" doubt is real. Cross-workflow proof is the right next bounded variable.

2. **`aoi_by_theme` is the right AOI surface.** It has stable structured data produced by `_build_by_theme_payload` (contract.py:357-415), it has a materially different semantic shape from genealogy (grouped themes, engagement summaries, sin-type findings, source-document inventories), and it is already a child view under `aoi_thematic_analysis` with `renderer_type: accordion` and well-declared sub-renderers (aoi_by_theme.json).

3. **Payload shape assumptions are accurate.** The memo says `aoi_by_theme.structured_data` should contain `_section_order`, `_section_titles`, and per-theme objects with `overview`, `engagement`, `findings`, `source_documents`. This exactly matches the output of `_build_by_theme_payload` in contract.py:368-415. Each theme also carries `key_claims`, `philosophical_commitments`, and `argumentative_moves` -- richer than the memo states, which is good (more signal for the selector).

4. **The fallback to `aoi_thematic_report` is wise.** If the theme-grouped payload proves insufficient on real jobs, having a named fallback prevents scope drift.

5. **The two-family constraint is disciplined.** Two families (`aoi_theme_dossier` vs `aoi_theme_comparison_review`) with different top-level renderers (`accordion` vs `table`) is the right proof shape. It mirrors the genealogy round-3 pattern without copying it.

6. **Selector signals are grounded in real fields.** `theme_count`, finding counts, engagement levels, source-document counts, and dominant sin types are all derivable from the actual payload produced by contract.py. The selector does not require new inference or engine changes.

## Findings

### Finding 1 (Severity: HIGH) -- `bounded_dynamic_composition.py` is structurally genealogy-locked

The memo says "no backend workflow API changes are required beyond one new `composition_mode`." This significantly understates the work.

`src/presenter/bounded_dynamic_composition.py` is not a generic composition engine. It is a genealogy-specific proof module:

- **Line 1**: The module docstring reads `"""Proof-only runtime composition for genealogy presentations."""`.
- **Line 19**: `GENEALOGY_WORKFLOW_KEY = "intellectual_genealogy"` is the only workflow key referenced anywhere in the module.
- **Lines 29-33**: `_SUPPORTED_COMPOSITION_MODES` contains only three genealogy-specific modes. There is no branching for AOI workflow keys.
- **Lines 218-229**: `validate_requested_composition_mode` explicitly rejects any non-genealogy workflow:
  ```python
  if workflow_key != GENEALOGY_WORKFLOW_KEY:
      raise InvalidCompositionModeError("invalid_composition_mode_for_workflow")
  ```
- **Lines 244-272**: `apply_bounded_dynamic_composition` and all its branch handlers assume genealogy-specific view keys (`genealogy_relationship_landscape`, `genealogy_conditions`).

This means adding one AOI composition mode is not "one new constant." It requires:

1. Updating `_SUPPORTED_COMPOSITION_MODES` to include the new AOI mode.
2. Changing `validate_requested_composition_mode` to accept `anxiety_of_influence_thematic_single_thinker` for the new mode.
3. Adding a new branch in `apply_bounded_dynamic_composition` for the AOI mode.
4. Writing a new AOI-specific selector function (analogous to `_select_adaptive_relationship_surface` for genealogy).
5. Writing AOI-specific runtime family builders (analogous to `_build_relationship_profile_dossier_family` etc.).
6. Updating `get_runtime_composition_stage_name` with a new stage name.
7. Updating `inspect_runtime_composition` with an AOI branch.

The execution plan should name this structural expansion explicitly. It is the main implementation risk.

### Finding 2 (Severity: HIGH) -- The host situation is more complex than "one new proof-label mapping"

The memo says (Section "Keep The Host Generic"): allowed host-side work is "one new generic proof-label mapping" and "one proof-only AOI handoff link."

There are two separate rendering paths for AOI in the Critic:

1. **The bespoke path**: `AnxietyOfInfluencePages.tsx` embeds a `AoiV2ThematicPanel` component (`the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`) which uses `useBoundedV2Workspace` but does NOT pass any `compositionMode`. It has its own result-discovery, tab-selection, and presentation lifecycle entirely within the bespoke thinker-detail layout.

2. **The generic path**: `AnalysisWorkspacePage.tsx` reads `composition_mode` from the URL search params (line 180), passes it through to `useBoundedV2Workspace`, and uses it for API calls to `/v1/presenter/page/{job_id}` and `/v1/presenter/view/{job_id}/{view_key}`. The AOI workflow is already recognized here (line 177: `isAoiWorkflow = workflowKey === 'anxiety_of_influence_thematic_single_thinker'`).

The round-5 memo proposes the proof route as:
```
/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=<id>&composition_mode=adaptive_aoi_theme_surface_v1
```

This is the `AnalysisWorkspacePage` generic route. That path already works for AOI without composition mode (round 1 proved this). Adding a `composition_mode` query param should flow through existing plumbing.

However, the memo also proposes "one proof-only AOI handoff link from the existing bespoke thinker page into the generic proof route." This means adding a link from `AnxietyOfInfluencePages.tsx` to the generic route. That is a bespoke-page modification, which blurs the "keep the host generic" boundary. The execution plan should decide: is this link a one-line `<a href>` or does it require passing thinker context, result discovery state, and saved-result selection? If the latter, it is more than a trivial handoff.

### Finding 3 (Severity: MEDIUM) -- The `aoi_by_theme` view is a child view, not a top-level surface

The `aoi_by_theme.json` view definition declares:
```json
"parent_view_key": "aoi_thematic_analysis",
"position": 1.2,
"planner_eligible": false
```

It is a child of the tab container `aoi_thematic_analysis` (renderer_type: `tab`). In the current presentation manifest, `aoi_by_theme` is one tab within the parent container, alongside `aoi_source_documents` (position 1.1), `aoi_by_sin_type` (position 1.3), and `aoi_thematic_report` (position 1.4).

The genealogy adaptive proofs (rounds 3-4) operated on top-level surfaces like `genealogy_relationship_landscape` and `genealogy_conditions`. Those are structurally different from child views nested inside a tab container.

The round-5 selector needs to operate on the `aoi_by_theme` payload to choose a runtime family. But the runtime family replacement must either:
- Replace the entire child view's renderer within its parent tab, or
- Promote `aoi_by_theme` to a top-level surface and generate a new parent container.

The memo does not address which approach to use. The genealogy proofs used the second approach (generating runtime parent containers via `DERIVATION_KIND_GENERATED_RUNTIME_PARENT`). If round 5 does the same for one AOI child view while leaving the other three children in their original tab container, the resulting page structure could be incoherent -- one AOI child is adaptively promoted while siblings remain under the old tab.

The execution plan must resolve this: does the adaptive family replace the child-view in-place within the tab, or does it promote to top-level?

### Finding 4 (Severity: MEDIUM) -- The `aoi_theme_comparison_review` table family needs careful field mapping

The memo specifies the table family's required columns:
- `theme_name`, `engagement_level`, `finding_count`, `dominant_sin_type`, `source_document_count`, `reading_signal`

Some of these are directly available from the `_build_by_theme_payload` output:
- `theme_name`: available via `_section_titles[theme_id]`
- `finding_count`: `len(payload[theme_id]["findings"])`
- `source_document_count`: `len(payload[theme_id]["source_documents"])`

But `engagement_level` is not a discrete field. The `engagement` value in each theme payload is a formatted prose string (see contract.py:491-509, `_format_engagement_summary`), which concatenates level, position, divergence, severity, and rationale into a single paragraph. Extracting `engagement_level` requires parsing this string or going back to the raw engagement mapping data.

Similarly, `dominant_sin_type` per theme requires scanning `findings[].sin_type` within each theme and computing the mode. This is derivable but not pre-computed.

And `reading_signal` is not defined in the payload at all. The memo does not specify what this field means or where it comes from.

The selector and family builder will need to do non-trivial aggregation work that goes beyond simply reading top-level fields. The memo should acknowledge this or pre-specify the aggregation contract.

### Finding 5 (Severity: MEDIUM) -- The `decision_trace.py` adaptive path is also genealogy-locked

`src/presenter/decision_trace.py:90-93` only dispatches adaptive trace inspection for two specific genealogy composition modes:

```python
if composition_mode in {
    COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
    COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
}:
```

Adding the new AOI mode requires extending this dispatch. The memo correctly says "reuse the existing singular adaptive trace pattern" but does not note that the dispatch code will need modification. This is straightforward work but should be named.

### Finding 6 (Severity: LOW) -- Per-theme payload is richer than memo states

The `_build_by_theme_payload` (contract.py:388-414) produces per-theme objects with seven fields, not four:

1. `overview` (string)
2. `engagement` (formatted string)
3. `key_claims` (list of `{title, description}` dicts)
4. `philosophical_commitments` (list of `{title, description}` dicts)
5. `argumentative_moves` (list of `{title, description}` dicts)
6. `source_documents` (list of title strings)
7. `findings` (list of finding-card dicts with `title`, `subtitle`, `description`, `badge`, `sin_type`, `sin_type_label`, `theme_name`, `source_document_id`, `target_quote`, `source_quote`, `implication_for_argument`)

The memo's pre-execution gate (section "Pre-Execution Verification Gate") only checks for `overview`, `engagement`, `findings`, `source_documents`. This is fine for the verification gate, but the `aoi_theme_dossier` family contract (section "Family 1") lists `key_claims` as a sub-renderer section. Good that the memo includes it in the family spec even though it is not in the gate -- but this inconsistency should be noted.

### Finding 7 (Severity: LOW) -- The `AoiV2ThematicPanel` is a substantial bespoke component, not just a "link target"

`AoiV2ThematicPanel.tsx` (148 lines of imports + 400+ lines of logic) has its own result-discovery, job-submission, presentation rendering, tab management, and export functionality. It is essentially a mini version of `AnalysisWorkspacePage` specialized for AOI. The memo's framing of a "proof-only handoff link" from the bespoke page to the generic route implies a temporary bridge. But in practice, if the generic route + adaptive composition proves successful for AOI, the natural next question is whether `AoiV2ThematicPanel` should be retired in favor of the generic workspace. The scope memo should name this as a future question explicitly, even if it is out of scope for round 5.

## Recommended Corrections

1. **Name the `bounded_dynamic_composition.py` structural expansion explicitly.** The memo should acknowledge that the composition module is currently genealogy-locked and list the specific functions that need AOI branches. This is the main implementation work.

2. **Decide whether the adaptive family replaces the child view in-place or promotes it.** Since `aoi_by_theme` is a child of `aoi_thematic_analysis` (a tab container), the execution plan needs to resolve whether:
   - (a) the family replaces the child view's renderer config within its parent tab, or
   - (b) the family promotes `aoi_by_theme` to top-level and generates a runtime parent.
   Option (a) is simpler and more honest for a first cross-workflow proof. Option (b) mirrors the genealogy pattern but creates page-structure incoherence.

3. **Add `engagement_level` extraction and `dominant_sin_type` computation to the selector spec.** The memo's selector expects these as computed fields, but the actual payload stores `engagement` as a prose string and `sin_type` as a per-finding field. The spec should note that the selector must: (a) parse the engagement level from the formatted string or load from the raw engagement metadata, and (b) compute `dominant_sin_type` by counting `findings[].sin_type` per theme.

4. **Drop or define `reading_signal`.** This field appears in the table family's column spec but is not defined anywhere in the codebase or the memo itself. Either define it concretely (e.g., "a one-sentence summary derived from the theme overview") or remove it from the required columns.

5. **Extend the `decision_trace.py` dispatch explicitly.** The trace path at lines 90-93 needs a new branch for the AOI composition mode. This is small work but should be in the execution checklist.

6. **Clarify the handoff-link scope.** If the "proof-only AOI handoff link" from the bespoke page is just a URL-constructing `<a>` tag, say so. If it requires passing thinker state, say that too. The ambiguity here could turn a one-line change into a meaningful bespoke-page modification.

## Bottom Line

**Approve after revision.** The strategic judgment is correct: cross-workflow adaptive proof is the right next variable, and `aoi_by_theme` is the right target surface. The payload shape assumptions are verified against the actual codebase. But the memo understates the implementation scope in `bounded_dynamic_composition.py` (Finding 1), leaves the child-view-vs-top-level question unresolved (Finding 3), and includes an undefined field in the table family contract (Finding 4). None of these are scope-killing -- they are execution-plan gaps that should be closed before implementation starts. The corrected scope memo, with these six items addressed, would be ready for execution planning.
