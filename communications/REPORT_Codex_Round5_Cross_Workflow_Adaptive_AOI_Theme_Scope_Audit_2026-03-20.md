# Audit: Round 5 / Cross-Workflow Adaptive AOI Theme Scope

Date: 2026-03-20
Memo under review: `communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md`

## Findings

### 1. The memo picks the right next program variable, but it understates how genealogy-locked the adaptive backend still is

The strategic call is right. After round 4, the next meaningful variable really is whether adaptive composition generalizes across workflows rather than remaining a genealogy-only success story (`communications/MEMO_2026-03-20_round4_adaptive_surface_suite_completion.md:165-174`, `communications/MEMO_2026-03-20_round4_adaptive_surface_suite_completion.md:214-223`, `communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md:41-83`).

But the implementation surface is broader than the memo’s wording implies.

- `src/presenter/bounded_dynamic_composition.py` still declares itself as “Proof-only runtime composition for genealogy presentations” and only defines genealogy constants, workflow guards, and dispatch branches (`src/presenter/bounded_dynamic_composition.py:1-33`, `src/presenter/bounded_dynamic_composition.py:218-301`).
- `validate_requested_composition_mode()` currently rejects every non-genealogy workflow when any proof mode is requested (`src/presenter/bounded_dynamic_composition.py:218-229`).
- `src/presenter/decision_trace.py` only imports genealogy proof-mode constants and only performs inspectable runtime-composition reconstruction for those modes (`src/presenter/decision_trace.py:15-22`, `src/presenter/decision_trace.py:90-105`).

So the scope direction is correct, but the memo should stop implying that round 5 is basically “one new constant on the existing generic path.” It is still bounded work, but it crosses the module’s current genealogy-only authorization and trace assumptions.

### 2. The generic-host claim only holds if round 5 is explicitly bounded to `AnalysisWorkspacePage`; the bespoke AOI path is not proof-ready

The generic route is genuinely composition-mode capable today.

- `AnalysisWorkspacePage` reads `composition_mode` from the URL, threads it into `useBoundedV2Workspace`, and forwards it to lazy single-view loads (`/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:177-181`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:301-309`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:341-390`).
- `boundedV2Client` already treats `composition_mode` as an opaque token across manifest, presentation, refresh, and single-view paths (`/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts:117-166`).
- `useBoundedV2Workspace` already treats proof-mode freshness and cache behavior generically (`/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:72-76`, `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:165-225`, `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:227-259`).

The bespoke AOI path is different.

- `AoiV2ThematicPanel` does not pass `compositionMode` into `useBoundedV2Workspace` at all (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:123-153`).
- Its lazy single-view fetch bypasses `boundedV2Client` and calls the presenter route directly without `composition_mode` (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:214-239`).
- The existing “Open Generic Workspace” handoff on the thinker page only forwards thinker context, not the proof token (`/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx:738-748`).

That means the memo should say one thing plainly: round 5 proves the generic AOI route, not the bespoke AOI panel. If a clickable proof handoff from the thinker page is desired, that is a small host change, but it is still a real change and should be named as such.

### 3. `aoi_by_theme` does have a stable payload seam, but it is a child surface under `aoi_thematic_analysis`, not a top-level AOI surface

The core payload seam is real and stronger than the memo’s caution suggests.

- `_build_by_theme_payload()` emits a stable grouped object with `_section_order`, `_section_titles`, and one theme-id-keyed object per theme (`src/aoi/contract.py:357-415`).
- The contract tests already lock that shape down, including stable theme-id keys and the current seven-field theme payload (`tests/test_aoi_contract.py:270-296`).
- Presenter assembly already prefers the view-key structured payload over cache lookup and derives accordion sections from it (`tests/test_presentation_api.py:1912-1961`, `tests/test_presentation_api.py:1964-2045`).

But `aoi_by_theme` is not top-level.

- Its view definition is an `accordion` child with `parent_view_key = "aoi_thematic_analysis"` (`src/views/definitions/aoi_by_theme.json:1-91`).
- The parent `aoi_thematic_analysis` surface is the top-level `tab` container (`src/views/definitions/aoi_thematic_analysis.json:1-42`).

So the memo should be explicit that round 5 adapts `aoi_by_theme` in place as a child under the existing parent container. If it leaves that ambiguous, it reads as if the proof might promote the surface to top-level, which would be a larger page-structure change than the scope claims.

### 4. The selector inputs are only partly available on the parent-first seam; `engagement_level` and `reading_signal` are still loose

The `aoi_by_theme` payload exposes enough signal for a bounded selector, but not every signal the memo currently names.

- `theme_count`, `total_finding_count`, `dominant_theme_findings`, `dominant_theme_share`, `second_theme_findings`, and source-document counts are all derivable from the top-level grouped payload (`src/aoi/contract.py:368-415`).
- `dominant_sin_type_per_theme` is also derivable because each finding card preserves both `sin_type` and `sin_type_label` (`src/aoi/contract.py:472-486`).

The weak point is engagement.

- The grouped theme payload does not expose a structured `engagement_level` field. It stores a formatted prose summary in `engagement` (`src/aoi/contract.py:389-397`).
- That summary is generated as prose by `_format_engagement_summary()` (`src/aoi/contract.py:489-509`).
- The memo’s own hard rule says the selector should stay on the top-level `aoi_by_theme` payload and should not reopen raw engine payloads or prose parsing (`communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md:214-234`).

So `distinct_engagement_levels` and the table column `engagement_level` are not cleanly available on the stated seam. They are only recoverable by parsing formatted prose or by reopening upstream engagement metadata, and both of those conflict with the memo’s current discipline.

`reading_signal` is the other gap. I do not see that field defined anywhere in the AOI grouped payload, contract builders, or current host code. It needs a concrete definition or it should be removed from the family contract.

### 5. The runtime families are directionally right, but the comparison family is still not validation-complete

`aoi_theme_dossier` is close to a real runtime contract because it mostly mirrors the existing `aoi_by_theme` accordion family (`src/views/definitions/aoi_by_theme.json:9-51`). The scope is still a little loose, though:

- the WP0 gate checks `overview`, `engagement`, `findings`, and `source_documents`, but the dossier family also relies on `key_claims` (`communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md:175-193`, `communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md:280-288`);
- the actual payload also includes `philosophical_commitments` and `argumentative_moves`, which the memo does not discuss at all (`src/aoi/contract.py:398-409`, `tests/test_aoi_contract.py:281-294`).

The larger problem is `aoi_theme_comparison_review`.

- The memo names required columns, but it does not define the actual `table` contract in the way the live renderer validates it (`communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md:298-310`).
- The `table` renderer expects either a flat row array plus config, or a multi-table container whose entries include explicit `title`, `columns`, and `rows`; the config schema also expects column objects, not just a prose list of column names (`src/renderers/definitions/table.json:7-79`).

That matters because row normalization is still underspecified:

- `theme_name` must come from `_section_titles`;
- `finding_count` and `source_document_count` must be derived from array lengths;
- `dominant_sin_type` must be computed from `findings[]`;
- `overview_excerpt` needs a truncation rule if it remains;
- `engagement_level` and `reading_signal` are not yet contract-safe as described above.

Until those are spelled out precisely, the memo is not yet at a clean fail-closed runtime-family boundary.

### 6. The route contract and thinker-scoped AOI assumptions are stable, but the memo should name the missing test surface more concretely

The route foundation is solid.

- The generic route shape in the memo matches the actual proving vehicle established by the March 18 execution brief (`communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md:32-52`, `communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md:117-139`).
- The generic client and page already thread `selected_source_thinker_id` through discovery, restore, and run launch (`/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts:75-107`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:177-182`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:600-635`).
- Existing tests already cover the stable grouped AOI payload seam and thinker-scoped route filtering (`tests/test_aoi_contract.py:270-296`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.integration.test.tsx:253-340`).

What is still missing is explicit round-5 test intent around the new adaptive mode:

- backend acceptance/rejection of an AOI-only proof mode in `bounded_dynamic_composition.py`;
- AOI trace reconstruction in `decision_trace.py`;
- selector behavior against the top-level `aoi_by_theme` grouped payload;
- generic-host proof-label and single-view forwarding for the AOI mode;
- proof-handoff behavior from `AnxietyOfInfluencePages` if that convenience path stays in scope.

This is not a scope reset, but the memo should call out those test surfaces more concretely because they are the places where the current repo is still silent.

## Open questions

### 1. Is the round-5 proof strictly a generic-route proof, or does the team want a first-class handoff from the bespoke AOI thinker page?

If it is strictly a generic-route proof, the host claim stays clean. If the proof is expected to be reachable from the bespoke page, then the existing handoff needs to forward `composition_mode`, and the memo should say so explicitly.

### 2. Should `engagement_level` remain part of the selector and comparison family at all?

On the current parent-first seam it is prose, not a stable field. The cleanest choices are either:

- remove it from the selector/family contract, or
- explicitly allow a tightly scoped parse of the fixed `Engagement level: ...` prefix and admit that exception in the memo.

### 3. Does the team want the adaptive AOI family to preserve the full current theme payload richness, or only a narrower dossier subset?

The live seam already includes `key_claims`, `philosophical_commitments`, and `argumentative_moves`. If round 5 intentionally drops some of that, the memo should say that it is narrowing the AOI reading surface on purpose rather than just overlooking available structure.

## What looks right

### 1. The round-5 variable is the right one

This really is the next smallest proof that advances the platform thesis after round 4. The March 16 platform-gap memo and March 18 execution brief both point toward proving the same thin workspace across materially different workflow families, not just adding more local genealogy cleverness (`communications/MEMO_2026-03-16_beautiful_by_default_surfaces_platform_gap.md:9-20`, `communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md:32-52`, `communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md:150-155`).

### 2. `aoi_by_theme` is the right first AOI target

It has a real normalized grouped seam, it is high-salience in perceived page shape, and it is semantically different enough from genealogy to make the cross-workflow proof meaningful (`src/aoi/contract.py:357-415`, `src/views/definitions/aoi_by_theme.json:1-91`).

### 3. The generic AOI route and thinker-scoped identity model are already real

The memo is not inventing a new AOI route contract. It is reusing the same generic path and thinker qualifier the current Critic integration already depends on (`/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts:75-107`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:177-182`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:600-635`).

### 4. One adaptive AOI surface with two runtime families is the right proof shape

That is disciplined. It keeps round 5 about cross-workflow generalization, not about opening a multi-surface AOI suite or a declarative adaptive registry (`communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md:204-212`, `communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md:262-320`, `communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md:409-417`).

### 5. Reusing the singular adaptive trace grammar is the right instinct

If round 5 stays single-surface, `adaptive_surface_selection` is the right trace-stage shape. The point is cross-workflow reuse of the same inspectable discipline, not inventing another trace grammar too early (`communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md:347-363`).

## Verdict

Approve after revision.

The memo has the right strategic target and the right AOI surface. The main problems are execution-readiness problems, not scope-direction problems: the backend is still genealogy-locked, the bespoke AOI path is not proof-ready, the child-surface placement needs to be explicit, and the comparison-family selector contract still relies on fields that are not cleanly available on the stated parent-first seam. Tighten those points and this becomes a credible round-5 scope.
