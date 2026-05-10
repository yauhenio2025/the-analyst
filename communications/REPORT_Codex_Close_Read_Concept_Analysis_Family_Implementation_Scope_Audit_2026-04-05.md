# Close Read Concept Analysis Family Implementation Scope Audit

## Context Check

- Read in full: [MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md)
- Read in full: [MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md)
- Read in full: [MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md)
- Read in full: [MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md)
- Read in full: [MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md)
- Read in full: [MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md)
- Read in full: [MEMO_2026-04-05_close_read_v1_product_memo.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-04-05_close_read_v1_product_memo.md)
- Read in full: [MEMO_2026-04-01_close_read_direction_dictation_reference.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md)
- Read in full: [MEMO_2026-04-01_close_read_direction_change_and_implications.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md)
- Read in full: [DYNAMIC_BESPOKE_APPS_VISION.md](/home/evgeny/projects/analyzer-v2/communications/DYNAMIC_BESPOKE_APPS_VISION.md)

## Verdict

Approve with corrections.

The memo gets the big product boundary right. It keeps the family admission at `inferential` plus `logical`, keeps the tranche result-backed-only, preserves native concept routes, and stays ahead of composition-layer or standalone-host drift. The route choice also fits the current `Close Read` umbrella shape.

The corrections are implementation-critical, not cosmetic. As written, the memo understates how non-`Close Read` the current concept detail runtime still is, especially around capture/provenance and around the extraction seam below `ConceptsPanel`.

## Findings

1. The scope overstates first-cut inheritance of the current `Close Read` baseline, especially capture. The live genealogy `Close Read` page gets provenance and capture from a `PagePresentation` corridor with `CaptureProvider`, `ProvenanceProvider`, `ProvenanceSummary`, `ProvenanceToggle`, `V2TabContent`, and `CaptureActionBar` [CloseReadPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadPage.tsx#L500). The concept detail runtime has none of that shared substrate; it is plain bespoke DOM plus local state in `AnalysisDetail` and its children [ConceptsPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx#L1722). The memo is right that lightweight provenance can be added from `analysis_type`, `framework`, and `analyzed_at`, but the test-plan claim that explicit inferential/logical entities can already enter capture mode is not implementation-ready from current code. There is no existing concept-side capture adapter, no shared `surfaceMode="close-read"` seam like AOI has [CloseReadAoiPages.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadAoiPages.tsx#L285), and inferential/logical payloads only expose thin metadata in the current types [types.ts](/home/evgeny/projects/the-critic/webapp/src/types.ts#L1259). This should be rewritten as: provenance is in-scope; capture is either a narrower follow-on inside the tranche or an explicit stretch item with a dedicated adapter.

2. `AnalysisDetail` is the wrong extraction seam. The memo names `AnalysisDetail`, `InferentialDetail`, and `LogicalDetail` together as reusable detail components [implementation scope memo](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md#L166). But `AnalysisDetail` is not just presentation. It hardcodes native `/concept-analysis/:slug/:analysisType/:tab` navigation [ConceptsPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx#L1729), owns legacy export buttons and close/back shell [ConceptsPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx#L2240), includes all six submodes including deferred ones [ConceptsPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx#L2334), and carries the ammunition modal and scrutiny orchestration [ConceptsPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx#L1857). The practical seam is lower: keep `AnalysisDetail` native-route-local, extract `InferentialDetail`, `LogicalDetail`, `ScrutinyDisplay`, and a logical-scrutiny hook/state helper, then let a new Close Read concept page own the family shell, submode state, search-param law, provenance strip, and no-ammunition policy.

3. The detail-page fallback law is not yet concrete enough for direct links. The memo correctly defines defaulting for missing or invalid `submode` and `tab` [implementation scope memo](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md#L130), but current slug resolution is not a free decode. Native concept detail resolution requires the known concept list first via `slugToConcept(slug, knownConcepts)` [conceptSlug.ts](/home/evgeny/projects/the-critic/webapp/src/utils/conceptSlug.ts#L24) and the current full-page route does exactly that off the loaded summary list [ConceptsPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx#L1178). The backend detail endpoint also expects the real concept name, not the slug [server.py](/home/evgeny/projects/the-critic/api/server.py#L4095). The scope should therefore explicitly say that the detail route must first resolve the slug against `/api/concept/analyses` before fetching `/api/concept/analyses/:concept`, and it must define behavior for:
- unresolved slug
- concept exists natively but has zero admitted core results
- requested `submode` is syntactically valid but unavailable for that concept

4. The memo is directionally right on logical-only scrutiny, but it should name the actual trim seam more explicitly. Current scrutiny generation and polling are separable and worth reusing [ConceptsPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx#L1880), but the rendered scrutiny surface still exposes `Explore Corpus` when `onExploreCorpus` is supplied [ConceptsPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx#L4046), and the ammunition modal contains the send-to-outline workflow [ConceptsPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx#L2888). The memo should say the Close Read extraction must make corpus/ammunition/outline callbacks optional and absent by default, not merely “hidden later.”

## Explicit Answers

- Is the scope right to place the concept family under `/close-read/concepts` and `/close-read/concepts/:conceptSlug`, or does the current route architecture suggest a better bounded choice?

Yes. The current umbrella already uses short family-noun children under `/close-read` for genealogy and AOI [routes.tsx](/home/evgeny/projects/the-critic/webapp/src/routes.tsx#L255). `concepts` is more consistent with that family routing than reusing native `/concept-analysis`, and using `submode` plus `tab` as search params is more aligned with current `Close Read` state handling than path-segmenting the detail route like native concept analysis does [CloseReadPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadPage.tsx#L211).

- Does the landing/index behavior correctly filter to admitted core submodes using the existing `/api/concept/analyses` summary endpoint?

Yes. The summary endpoint already returns every completed concept analysis with `concept`, `analysis_type`, `analyzed_at`, and optional `synthesis` [server.py](/home/evgeny/projects/the-critic/api/server.py#L4051), [types.ts](/home/evgeny/projects/the-critic/webapp/src/types.ts#L1486). Grouping by concept and retaining only concepts with at least one `inferential` or `logical` result is fully supportable without backend changes.

- Is the detail-page availability and submode fallback law concrete enough?

Not yet. It is close, but it still needs explicit law for slug resolution, for concepts with only deferred-tier results, and for valid-but-unavailable requested submodes. Without that, direct-link behavior will be ambiguous in a way the current native concept route avoids by loading the known concept list first [ConceptsPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx#L1184).

- Does the scope overstate the feasibility of inheriting the Close Read baseline, especially provenance/capture, given the current non-V2 concept detail runtime?

Yes. It is fair on lightweight provenance and unfair on capture parity. Current concept detail is not already on the Close Read baseline corridor.

- Is extracting `AnalysisDetail` / `InferentialDetail` / `LogicalDetail` from `ConceptsPanel` the right seam, or does the scope miss a more practical reuse boundary?

It misses the better seam. `InferentialDetail` and `LogicalDetail` are good candidates. `AnalysisDetail` is not; it owns too much native concept shell and deferred workflow state.

- Does the scope correctly constrain scrutiny to the logical surface and trim the broader ammunition workflow?

Yes in product intent. It still needs one implementation correction: make the ammunition/corpus/outline path structurally optional or removed in the extracted logical scrutiny runtime, not just absent from the page chrome.

- Does the scope keep the right order of work, or does it drift prematurely into composition-layer or standalone-host concerns?

It keeps the right order. The memo stays on the bounded family-admission tranche and does not drift into composition-layer or standalone-host work.

## Required Corrections

1. Replace the `AnalysisDetail` extraction target with a lower seam:
   - extract `InferentialDetail`
   - extract `LogicalDetail`
   - extract `ScrutinyDisplay` plus a logical-scrutiny hook/helper
   - keep a new Close Read concept shell separate from native concept detail

2. Rewrite baseline inheritance so it distinguishes:
   - guaranteed in this slice: result-backed pages, family-local provenance strip, family switcher, admitted-submode tabs, logical scrutiny core
   - not yet inherited for free: full capture parity with current genealogy/AOI Close Read

3. Add explicit detail-route boot law:
   - resolve `conceptSlug` against the summary list first
   - then fetch `/api/concept/analyses/:concept`
   - unknown slug or deferred-only concept gets a bounded unavailable state with links to `/close-read` and native `/concept-analysis`
   - requested unavailable admitted submode falls back to the concept’s default available submode while still rendering the missing core submode as unavailable

4. Make the logical scrutiny trim explicit in the scope text:
   - scrutiny generation, polling, and result display stay
   - `onExploreCorpus`, ammunition modal, and send-to-outline stay out
   - scrutiny export buttons should also be treated as out unless explicitly re-admitted

## Bottom Line

The memo is fundamentally pointed in the right direction. If the corrections above are folded in, it becomes a solid implementation-ready tranche. If they are not, the likely failure mode is a partial transplant of the native `ConceptsPanel` shell that quietly re-imports more legacy concept estate than the boundary memo allowed.
