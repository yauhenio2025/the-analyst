# Memo: Close Read Concept-Analysis Family Implementation Scope

Subtitle: Implement the first bounded `Close Read` concept-analysis family cut on the existing Critic umbrella

Date: 2026-04-05
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Vision Context:
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
Close Read Direction Context:
- `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
Current Close Read Boundary:
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md`
Primary Critic Product Evidence:
- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/CloseReadFamilySwitcher.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadLandingPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/types.ts`
- `/home/evgeny/projects/the-critic/api/server.py`

## Purpose

Implement the first bounded `Close Read` concept-analysis family cut already frozen in the boundary memo.

This scope should add concept analysis as a real `Close Read` family under the existing umbrella while keeping the cut intentionally narrow:

- admitted core submodes only:
  - `inferential`
  - `logical`
- result-backed only
- logical-only scrutiny
- no launch/detection UI
- no ammunition / send-to-outline / big-picture / cross-concept

This is an implementation scope, not another product-boundary memo.

## Summary

Add a `Concept Analysis` family beneath the existing `Close Read` umbrella:

- `/p/:projectId/close-read/concepts`
- `/p/:projectId/close-read/concepts/:conceptSlug`

Update the umbrella landing and family switcher so `Concept Analysis` sits alongside:

- `Genealogy`
- `Anxiety of Influence`

The concept family should be powered entirely from existing Critic endpoints:

- `GET /api/concept/analyses`
- `GET /api/concept/analyses/:concept`
- existing scrutiny endpoints for logical-only follow-up

This tranche should not change analyzer-v2, backend schemas, or native legacy concept routes.

## Route And Page Shape

### 1. Close Read umbrella additions

Add a third family beneath the existing umbrella:

- `/p/:projectId/close-read/concepts` = concept-analysis family landing/index
- `/p/:projectId/close-read/concepts/:conceptSlug` = concept detail page

Update:

- umbrella landing cards
- `CloseReadFamilySwitcher`

so `Concept Analysis` appears as a first-class family beside `Genealogy` and `Anxiety of Influence`.

### 2. Family route behavior

The concept family landing/index must:

- fetch `GET /api/concept/analyses`
- group summaries by concept
- group concepts case-insensitively to match the backend’s `func.lower(...)` concept lookup semantics
- keep only concepts with at least one admitted core result:
  - `inferential`
  - `logical`
- exclude concepts that have only:
  - `assumption`
  - `semantic_field`
  - `causal`
  - `metaphorical`
- exclude concepts with zero admitted-submode results

Each concept card should show:

- concept name
- whether `inferential` exists
- whether `logical` exists
- latest available analysis timestamp among admitted core results
- CTA into `/close-read/concepts/:conceptSlug`

If no concepts are usable:

- show a bounded empty state
- link back to `/close-read`
- link to native `/concept-analysis`

### 3. Detail route behavior

The concept detail page must:

- first fetch `GET /api/concept/analyses`
- resolve `:conceptSlug` against that summary list using the same slug encode/decode law as native concept analysis
- only after slug resolution succeeds, fetch `GET /api/concept/analyses/:concept`
- derive admitted core submode availability from the returned per-type object
- show only the admitted core submodes:
  - `inferential`
  - `logical`
- ignore deferred-tier payloads even if the API returns them

Use search params for state:

- `submode=inferential|logical`
- `tab=...`

Default rules:

- if both admitted core results exist, default `submode=inferential`
- if only one admitted core result exists, default to that submode
- if `submode` is missing or invalid, fall back to the default rule above
- if `tab` is invalid for the active submode, fall back to that submode’s default tab

Availability rules:

- missing admitted submodes render as visible unavailable tabs/states
- do not silently omit unavailable admitted core tabs
- if `:conceptSlug` does not resolve to a known concept, show a bounded unavailable state with links to `/close-read` and native `/concept-analysis`
- if the concept exists natively but has zero admitted core results, show the same bounded unavailable state
- if a requested admitted `submode` is syntactically valid but unavailable for that concept, fall back to the concept’s default available core submode while still rendering the missing core submode as unavailable

No compatibility redirect layer is needed beyond normal slug decoding because this family has no old `Close Read` route precedent.

## UI / Runtime Behavior

### 1. Result-backed only

The Close Read concept family must not import the old dashboard/launch posture.

Do not include:

- concept input form
- type selector
- `Run Analysis`
- `Detect Concepts`
- dashboard mode
- running jobs bar
- generic completed-analyses dashboard

Those stay on native `/concept-analysis`.

### 2. Detail rendering strategy

Do not reimplement inferential/logical rendering from scratch.

Do not extract `AnalysisDetail` from `ConceptsPanel.tsx`.
`AnalysisDetail` is the large legacy shell that owns:

- native concept detail routing assumptions
- six-submode tab dispatch
- export controls
- scrutiny state orchestration
- ammunition state
- outline/downstream workflow state

The real extraction seam is lower.

Extract and reuse only:

- `InferentialDetail`
- `LogicalDetail`
- a logical-scrutiny state / polling helper if it can be separated cleanly

The new `Close Read` concept detail page should be a new thin family shell, not a wrapped `AnalysisDetail`.

The Close Read concept detail page should provide a thinner family shell:

- Close Read page header
- family switcher
- concept title / submode tabs
- lightweight concept metadata / family-local provenance panel
- shared Close Read action row
- extracted inferential/logical detail body

Trim legacy concept chrome that is out of scope for this cut:

- JSON / markdown / PDF export controls
- dashboard back-navigation patterns
- launch-time controls
- ammunition modal and corpus exploration controls
- send-to-outline controls
- scrutiny export controls

### 3. Shared Close Read baseline implementation

The concept family must inherit the Close Read baseline functionally, but it does not need to force `V2TabContent` or package-renderer plumbing onto the old concept estate.
The existing concept estate has no `V2TabContent`, no `CaptureProvider`, and no `CaptureActionBar` integration to reuse directly.

Implement the inherited baseline as:

- result-backed concept pages
- page-level provenance visibility using family-local concept metadata already present in the analysis payload:
  - `analysis_type`
  - `framework`
  - `analyzed_at`
  - `source` / `engine_key` where available
- page-level capture mode and `CaptureActionBar` via new concept-family plumbing

Capture in the first cut is net-new work, not reuse.
Implement it as a bounded concept-family adapter over explicit structured items already modeled in inferential/logical results.

Admit capture affordances only on explicit entities such as:

- inferential key quotes / commitment relations / incompatibility items
- logical arguments / vulnerabilities / scrutiny attacks

Do not attempt:

- arbitrary freeform text selection
- generic family-wide capture law for every paragraph block
- capture parity assumptions based on genealogy/AOI runtime reuse

### 4. Logical-only scrutiny reuse

Scrutiny is admitted only on the logical surface.

Reuse the existing logical scrutiny path rather than inventing a new analyzer-v2-native scrutiny contract in this tranche.

That means:

- preserve the existing logical scrutiny controls and state machine
- preserve quick / deep / both scrutiny modes
- preserve polling against the existing scrutiny API endpoints

But trim the broader downstream legacy attack workflow:

- no ammunition modal
- no `Explore Corpus`
- no send-to-outline
- no scrutiny export buttons

So the logical surface keeps:

- scrutiny generation
- scrutiny result viewing
- scrutiny-local weak-point work

and drops:

- ammunition search / analysis
- outline/export downstream actions

## Likely Code Changes

### 1. Close Read route and family shell

Update:

- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/CloseReadFamilySwitcher.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadLandingPage.tsx`

to add the concept family route, family switcher button, and family availability card.

### 2. New concept family pages/runtime

Add a bounded runtime helper and pages, for example:

- `src/pages/closeReadConceptRuntime.ts`
- `src/pages/CloseReadConceptPages.tsx`

Responsibilities:

- concept summary discovery via `/api/concept/analyses`
- case-insensitive grouping/filtering to admitted core submodes
- concept slug encode/decode
- detail-route slug resolution against the summary list before detail fetch
- detail fetch via `/api/concept/analyses/:concept`
- submode/tab search-param fallback logic
- landing/detail unavailable states

### 3. Extracted concept detail components

Refactor `ConceptsPanel.tsx` so Close Read can reuse only the result-backed inferential/logical detail bodies and logical scrutiny plumbing without importing the launch/dashboard shell wholesale.

The intended extraction seam is:

- `InferentialDetail`
- `LogicalDetail`
- optionally a logical-scrutiny helper / hook

The intended non-seam is:

- `AnalysisDetail`

This extraction should keep native `/concept-analysis` behavior unchanged.

## Test Plan

Add focused tests for:

### 1. Routing and family shell

- `Close Read` landing shows a `Concept Analysis` family card
- family switcher includes `Concept Analysis`
- `/close-read/concepts` renders the concept family index
- `/close-read/concepts/:conceptSlug` renders concept detail
- native `/concept-analysis` routes still render unchanged

### 2. Concept family landing/index

- concepts with both admitted core results appear
- concepts with only one admitted core result appear
- concepts with only deferred-tier results do not appear
- concepts with zero admitted-submode results do not appear
- case-insensitive concept grouping is preserved
- empty-state path links back to `/close-read` and native `/concept-analysis`

### 3. Concept detail behavior

- slug resolves through the summary list before detail fetch
- unknown slug shows bounded unavailable state
- native concept with zero admitted core results shows bounded unavailable state
- both-core concept defaults to `inferential`
- one-core concept defaults to the existing core result
- valid-but-unavailable admitted `submode` falls back to the default available core result while still rendering the missing core tab as unavailable
- unavailable admitted core submode renders as unavailable, not omitted
- deferred-tier results returned by the API are ignored by Close Read
- invalid `submode` and invalid `tab` fall back cleanly

### 4. Logical scrutiny cut

- logical submode shows scrutiny controls
- scrutiny polling/result rendering still works
- ammunition UI is absent
- `Explore Corpus` is absent
- send-to-outline UI is absent
- scrutiny export controls are absent
- inferential submode does not show scrutiny controls

### 5. Shared Close Read baseline

- concept family pages show page-level provenance metadata
- capture mode toggle and `CaptureActionBar` are present in the concept family shell through new concept-family plumbing
- explicit structured inferential/logical entities can enter capture mode
- destinations remain limited to `Arsenal` / `Research todo`

## Non-Changes

This tranche should not:

- add analyzer-v2-native concept runtime
- change backend schemas or concept-analysis endpoints
- admit `assumption`, `semantic_field`, `causal`, or `metaphorical`
- add concept launch/detection UI under `Close Read`
- admit ammunition, `big-picture`, `cross-concept`, or send-to-outline
- remove or redirect native concept-analysis routes

## Recommended Review Artifacts

After drafting or revising this scope, request two fresh reviews and save them to:

- `communications/REPORT_Claude_Close_Read_Concept_Analysis_Family_Implementation_Scope_Critique_2026-04-05.md`
- `communications/REPORT_Codex_Close_Read_Concept_Analysis_Family_Implementation_Scope_Audit_2026-04-05.md`
