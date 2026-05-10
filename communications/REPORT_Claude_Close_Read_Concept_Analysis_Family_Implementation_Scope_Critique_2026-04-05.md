# Review: Close Read Concept-Analysis Family Implementation Scope

Date: 2026-04-05
Reviewer: Claude (Opus 4.6)
Scope Document: `communications/MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md`

---

## Context Check

Confirmed read of all required materials:

- `MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md` -- the scope under review
- `MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md` -- the frozen boundary decisions
- `MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md` -- the initial inventory and migration truth
- `MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md` -- roadmap framing, default families vs composition layer
- `MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md` -- the V1.5 dual-family boundary freeze
- `MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md` -- the umbrella coexistence implementation that preceded this
- `MEMO_2026-04-05_close_read_v1_product_memo.md` -- V1 product boundary (genealogy-first pilot)
- `MEMO_2026-04-01_close_read_direction_dictation_reference.md` -- the original user dictation
- `MEMO_2026-04-01_close_read_direction_change_and_implications.md` -- strategic implications of the dictation
- `DYNAMIC_BESPOKE_APPS_VISION.md` -- broader vision context

Confirmed direct inspection of:

- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/CloseReadFamilySwitcher.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadLandingPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadAoiPages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx` (partial, ~5600+ lines)
- `/home/evgeny/projects/the-critic/webapp/src/types.ts`
- `/home/evgeny/projects/the-critic/api/server.py` (relevant concept and scrutiny endpoints)

---

## Verdict

**Approve with corrections.**

The scope is implementation-ready. It correctly preserves the result-backed-only posture, correctly keeps launch/detection on native routes, and correctly inherits the Close Read baseline. The proposed route model is coherent. The logical-only scrutiny cut is honest and well-bounded.

Three corrections are needed, none of which require architectural changes. They are spec-level clarifications to prevent implementation drift.

---

## Detailed Findings

### 1. Route model: concrete and coherent

**Assessment: Sound.**

The proposed routes:

- `/p/:projectId/close-read/concepts` (family landing/index)
- `/p/:projectId/close-read/concepts/:conceptSlug`

follow the same pattern already proven by:

- `/p/:projectId/close-read/genealogy`
- `/p/:projectId/close-read/aoi`
- `/p/:projectId/close-read/aoi/:thinkerId`

The existing `routes.tsx` (line 256-277) already uses an `<Outlet />` wrapper for the `close-read` subtree with child routes. Adding `concepts` and `concepts/:conceptSlug` as additional children is mechanically straightforward. The pattern is consistent.

One observation: the scope does not mention a backward-compatibility redirect layer and explicitly says none is needed ("No compatibility redirect layer is needed beyond normal slug decoding because this family has no old Close Read route precedent"). This is correct. Unlike the genealogy family, which had to handle old `?tab=` deep links from the former root, the concept family is net-new under Close Read.

### 2. Result-backed-only posture: correctly preserved

**Assessment: Sound.**

The scope's "Result-backed only" section (lines 148-160) explicitly excludes concept input form, type selector, Run Analysis, Detect Concepts, dashboard mode, running jobs bar, and generic completed-analyses dashboard. These all stay on native `/concept-analysis`.

The codebase confirms these are real concerns. `ConceptsPanel.tsx` is a monolithic ~5600+ line component that mixes launch, detection, dashboard, and detail rendering in a single file. The scope correctly identifies that Close Read should not import this file wholesale but should extract only the presentational detail components.

### 3. Landing/index inclusion law: correct and sufficiently explicit

**Assessment: Sound, with one correction needed.**

The four-way classification is clear:

| Scenario | Shown? |
|----------|--------|
| Both core results (`inferential` + `logical`) | Yes |
| Only one core result | Yes |
| Only deferred-tier results (`assumption`, `semantic_field`, `causal`, `metaphorical`) | No |
| Zero admitted-submode results | No |

This is the right law. It prevents the Close Read concept index from becoming a generic discovery dashboard while still showing concepts that have partial core coverage.

**Correction 1: The scope should specify how concepts are grouped from the API response.**

The `GET /api/concept/analyses` endpoint (server.py line 4051) returns a flat list of `ConceptAnalysisSummary` objects, each with `concept`, `analysis_type`, `file_path`, `analyzed_at`, and `synthesis`. To apply the inclusion law, the implementation must group by `concept`, then filter to those groups where at least one item has `analysis_type` in `["inferential", "logical"]`.

This is implied but not stated. The scope says "group summaries by concept" and "keep only concepts with at least one admitted core result." That is clear enough in intent, but the implementation must handle case-insensitive concept matching -- the API does case-insensitive concept lookup (server.py line 4112: `func.lower(DBConceptAnalysis.concept) == func.lower(concept)`), and the grouping logic on the frontend should do likewise. The scope should note this, because concept names come from user input and casing inconsistency is a known drift vector in this codebase (`conceptToSlug`/`slugToConcept` utilities already exist in ConceptsPanel.tsx line 3).

### 4. Detail-page submode/tab fallback law: concrete enough to implement safely

**Assessment: Sound.**

The fallback rules are explicit:

- Both core results -> default `submode=inferential`
- Only one core result -> default to that
- Invalid `submode` -> fall back to default rule
- Invalid `tab` -> fall back to submode's default tab

Search-param state (`submode=inferential|logical`, `tab=...`) is the right approach. It mirrors the existing `useTabUrl` pattern already proven in `CloseReadPage.tsx`.

The "unavailable admitted core submode renders as visible unavailable tabs/states" rule is the correct posture. It keeps the product legible rather than silently adapting to whatever data happens to exist.

### 5. Reuse of existing ConceptsPanel detail layer: the scope is honest but needs sharper extraction guidance

**Assessment: Mostly sound. One correction needed.**

The scope correctly identifies `AnalysisDetail`, `InferentialDetail`, and `LogicalDetail` as the components to extract. Code inspection confirms:

- `AnalysisDetail` (line 1722): The routing/tab dispatch shell for concept detail. It owns scrutiny state, ammunition state, and tab navigation.
- `InferentialDetail` (line 3027): Renders inferential analysis tabs (synthesis, hidden weight, commitments, incompatibilities, tensions, practical stakes).
- `LogicalDetail` (line 4324): Renders logical analysis tabs (arguments, chains, vulnerabilities, scrutiny).
- `AssumptionDetail` (line 4805), `SemanticFieldDetail` (line 4992), `GenericV2Detail` (line 5598): Not needed for first cut.

**Correction 2: The scope understates the extraction complexity for `AnalysisDetail`.**

`AnalysisDetail` is not a clean presentational component. It is a 3000+ line function that owns:

- scrutiny state machine (scrutinyJobs, scrutinyResults, scrutinyLoading, scrutinyProgress)
- scrutiny API polling (against `/api/scrutiny/results/:concept`)
- localStorage caching for scrutiny results
- ammunition modal state and corpus loading
- outline routing state
- export controls (JSON, Markdown, PDF)
- the full tab dispatch (`InferentialDetail` vs `LogicalDetail` vs `AssumptionDetail` etc.)

The scope says "Extract and reuse the existing presentational concept detail components" and "do not carry over the full legacy shell." But `AnalysisDetail` IS the full legacy shell. `InferentialDetail` and `LogicalDetail` are the actual presentational components. The scope should make this distinction sharper:

- `InferentialDetail` and `LogicalDetail` are the extraction targets
- `AnalysisDetail` is NOT extracted -- it is replaced by a new thin Close Read concept detail shell
- The new shell owns submode/tab state (via search params), fetches the concept data, and renders `InferentialDetail`/`LogicalDetail` based on the active submode
- Scrutiny state and polling are lifted out of `AnalysisDetail` and placed in the new shell (for logical submode only)
- Ammunition, export, and outline state are not carried

This matters for implementation safety. If the scope is read as "extract AnalysisDetail", an implementor might import the 3000-line function and try to suppress its non-Close-Read pieces. That would be fragile. The scope should say: the extraction boundary is `InferentialDetail` and `LogicalDetail` as pure presentational components, plus the scrutiny polling/state logic as a separable concern for the logical submode.

Additionally, `ConceptsPanel.tsx` does NOT use `V2TabContent`, `CaptureProvider`, or `CaptureActionBar` anywhere. I confirmed this by searching the file. This means the existing concept detail layer has zero overlap with the Close Read capture baseline. The new Close Read concept shell will need to add `CaptureProvider` and `CaptureActionBar` from scratch, wrapping the extracted inferential/logical detail bodies. The scope's capture section acknowledges this implicitly ("page-level capture mode and CaptureActionBar"), but it should be explicit that the old concept estate has no capture infrastructure to reuse.

### 6. Logical-only scrutiny cut: honest and well-bounded

**Assessment: Sound.**

The scope correctly identifies that scrutiny should be admitted only on the logical surface, and that it should wrap the existing Critic scrutiny path rather than requiring a new analyzer-v2-native contract.

The code confirms the scrutiny plumbing is real and contained:

- Scrutiny endpoints: `POST /api/scrutiny/premises` (server.py line 6709), `GET /api/scrutiny/job/:id` (line 6753), `GET /api/scrutiny/results/:concept` (line referenced in ConceptsPanel)
- Scrutiny runs as background threads on the server (line 6532: `run_scrutiny_thread`)
- Quick/deep/both modes are supported (lines 6532-6691)
- Scrutiny results are stored in both localStorage and database

The scope correctly excludes:

- Ammunition modal and corpus exploration (`handleExploreCorpus` at line 2070, ammunition state at lines 1857-1869)
- Send-to-outline
- Full downstream attack workflow

The delineation is clean: scrutiny generation + result viewing + scrutiny-local weak-point work stays; ammunition + outline + export drops.

### 7. Provenance/capture assumptions: the scope is honest

**Assessment: Sound, no overreach.**

**Correction 3: Make capture integration explicit as net-new work.**

The scope says "page-level capture mode and CaptureActionBar" and "capture in the first cut should be bounded to explicit structured items." This is the right posture. It correctly avoids claiming that the old concept estate already has capture infrastructure.

But the admission audit already noted that the old concept estate "still lives entirely in the old Critic estate" and is not V2TabContent-based. The scope should make this implication concrete: capture affordances on inferential/logical items (key quotes, commitment relations, arguments, vulnerabilities) will need explicit `onCapture` callback integration on the extracted detail components. This is new plumbing, not reuse.

The scope's list of capturable entities is sensible:
- inferential: key quotes, commitment relations, incompatibility items
- logical: arguments, vulnerabilities, scrutiny attacks

These correspond to real structured items visible in the `InferentialDetail` and `LogicalDetail` components. The scope does not overclaim and does not attempt arbitrary freeform text selection.

Add to the "Shared Close Read baseline implementation" section: "The existing `ConceptsPanel` has no capture infrastructure. `CaptureProvider` and `CaptureActionBar` integration is net-new work for the concept family. The implementor should wrap the concept detail shell in `CaptureProvider` and add `onCapture` callbacks to the specific inferential/logical structured items listed above."

### 8. Separation between current work, later composition, and standalone-host deferral

**Assessment: Sound.**

The scope stays cleanly within its lane:

- **Current work**: concept family routes, landing/index, detail page with inferential/logical submodes, logical-only scrutiny, Close Read baseline
- **Later composition-layer work**: not mentioned, not encroached upon
- **Standalone-host deferral**: not mentioned, not encroached upon

The Non-Changes section (lines 323-333) is explicit about what this tranche does not do. It does not add analyzer-v2-native concept runtime, does not change backend schemas, does not admit deferred submodes, does not add launch/detection UI, and does not remove native routes.

The scope also correctly does not attempt to force `V2TabContent` or package-renderer plumbing onto the concept estate. This is the right call given that `ConceptsPanel.tsx` is entirely independent of the V2TabContent/renderer pipeline.

---

## Summary of Corrections

### Correction 1: Specify case-insensitive concept grouping

The landing/index logic must group API results by concept case-insensitively. Note the existing `conceptToSlug`/`slugToConcept` utilities and the API's `func.lower()` lookup. The scope should add one sentence in the "Family route behavior" section: "Concept grouping must be case-insensitive to match the API's case-insensitive lookup semantics."

### Correction 2: Sharpen the extraction boundary

Replace the current extraction guidance with:

- **Extraction targets**: `InferentialDetail` and `LogicalDetail` as presentational components
- **NOT extracted**: `AnalysisDetail` (the 3000+ line shell is replaced, not wrapped)
- **Separately extracted**: scrutiny polling/state logic, lifted into the new Close Read concept detail shell for the logical submode only
- **Not carried**: ammunition state, export controls, outline routing, dashboard navigation

Also add: "The old concept estate does not use `V2TabContent`, `CaptureProvider`, or `CaptureActionBar`. Capture integration on concept detail components is net-new work in this tranche."

### Correction 3: Make capture integration explicit as net-new work

Add to the "Shared Close Read baseline implementation" section: "The existing `ConceptsPanel` has no capture infrastructure. `CaptureProvider` and `CaptureActionBar` integration is net-new work for the concept family. The implementor should wrap the concept detail shell in `CaptureProvider` and add `onCapture` callbacks to the specific inferential/logical structured items listed above."

---

## Stress-Test Against Broader Vision

The scope is well-aligned with:

- **Original dictation**: The dictation explicitly names logical analysis, premise testing, and weak-point identification as core Close Read activities. This scope delivers exactly that through the logical submode + scrutiny cut.
- **Default families roadmap**: The roadmap memo explicitly identifies concept analysis as the third serious family after genealogy and AOI. This scope implements that next step.
- **V1.5 coexistence model**: The scope follows the same umbrella + family-specific pages pattern, adds to the family switcher, preserves native routes. Consistent.
- **Migration truth**: The scope does not overstate analyzer-v2 readiness. It correctly uses the legacy Critic endpoints and scrutiny plumbing rather than pretending a clean analyzer-v2 concept runtime exists.

The scope does not drift into product-boundary ambiguity, standalone-host planning, or composition-layer work. It is a concrete implementation scope for a bounded family cut.

---

## Final Assessment

This scope is ready for implementation after incorporating the three corrections above. The corrections are all spec-level clarifications, not architectural changes. No structural rework is needed.

The scope is notably disciplined about what it excludes. It resists the temptation to import the full 5600-line `ConceptsPanel` wholesale, and it resists the temptation to build a new analyzer-v2-native concept runtime. Both of those decisions are correct for a first bounded cut.

**Verdict: Approve with corrections.**
