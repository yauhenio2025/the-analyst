# Review: Stage 11 / Rich Semantic Page Planning Scope (Second Pass)

Reviewer: Claude Opus 4.6 (1M context)
Date: 2026-03-24
Primary document reviewed: `communications/MEMO_2026-03-23_stage11_rich_semantic_page_planning_scope.md` (revised)
Prior review: This file, first pass (2026-03-24)

## Verdict: Approve

The revised memo addresses all four findings from the first review substantively. The scope is now honest about the host-delta work required, the semantic matcher is defined with concrete AOI-local rules, the refactoring depth is explicitly acknowledged, and the fake `timeline_sequential` broadening is deferred.

Two minor issues remain. Neither is blocking.

---

## RESOLUTION OF PRIOR FINDINGS

### Finding 1 (CRITICAL → RESOLVED): `tab` renderer consumer gap

The revision now explicitly acknowledges that the transient host drops child views (lines 113-114, citing `AoiComposeFromIntentShell` and `transientComposeAdapters.ts`) and adds Decision 1's companion host delta: either teach the shell to render child trees or reuse the existing `AnalysisWorkspacePage.tsx` tree rendering.

Code inspection confirms the revision is grounded:

- `transientComposeAdapters.ts:55` counts `view.children?.length` as `ignoredChildCount` and discards them
- `AoiComposeFromIntentShell.tsx:36` shows a visible notice: "round 12 renders only top-level views"
- `AnalysisWorkspacePage.tsx:1035` already renders two-level parent/child tab navigation where parent views are navigation elements and only the active child's content is dispatched to `ViewRenderer`

This means the `tab` renderer type doesn't need a `ViewRenderer`-dispatched component for the hierarchy pattern to work. In `AnalysisWorkspacePage`, parent tab views are rendered as first-row navigation tabs, not as `ViewRenderer` targets. The transient shell can adopt the same approach: parent views as grouping elements, child views as rendered content.

The revision correctly draws the boundary: narrow transient-host delta ≠ universal host contract (Decision 1, lines 223-228).

**Status**: Resolved. One minor follow-up noted below (Finding A).

### Finding 2 (SIGNIFICANT → RESOLVED): Semantic matcher underspecified

Decision 3 now specifies concrete AOI-local matching rules:

- source inventory / corpus listing → `card_grid` family
- multi-facet evidence or findings-bank → `accordion` family
- synthetic closeout / report / implications → `prose` family
- multiple complementary child surfaces under shared analytical heading → `tab_with_children`

It also explicitly acknowledges that current AOI engines do not define `semantic_visual_intent` (line 144) and treats that field as optional future input rather than a present dependency.

This is a real specification. One minor follow-up noted below (Finding B).

**Status**: Resolved.

### Finding 3 (SIGNIFICANT → RESOLVED): Flat-planning refactoring depth

New Decision 6 explicitly lists the six seams the refactor must touch:

- planner prompt and planner output parsing
- section assignment validation
- normalized generated view shape
- payload assembly and child linking
- transient trace structure
- thin AOI host adaptation for returned child views

The memo now says (line 158): "Stage 11 is not a schema swap. It is a real refactor across the compose module and its thin AOI host seam."

**Status**: Resolved.

### Finding 4 (MODERATE → RESOLVED): `timeline_sequential` cosmetic broadening

Decision 5 now explicitly defers `timeline_sequential`: "timeline_sequential should stay deferred unless the current consumer path renders it in a materially distinct way from card_grid" (line 330).

The "What Stage 11 Should Not Claim" list adds item 7: "distinct new leaf families whose current host rendering is only metadata-deep" (line 509).

**Status**: Resolved.

---

## REMAINING FINDINGS (Minor)

### FINDING A — MINOR: Parent-view rendering mechanism needs one more sentence of specificity

The memo says the shell should either "teach `AoiComposeFromIntentShell` to render child trees" or "reuse the existing generic result-tree rendering seam."

But it doesn't specify how the parent `tab` view itself would be rendered. In `AnalysisWorkspacePage.tsx`, parent views are navigation tabs — they're rendered as clickable tab labels, not through `ViewRenderer`. The shared package has no `tab` renderer component, and `ViewRenderer` would fall back to `ProseRenderer` for `renderer_type: "tab"`.

The implementation should be clear about this: parent `tab_with_children` views in the transient path should be rendered as navigation/grouping elements (like the workspace's first-row tabs), not as `ViewRenderer`-dispatched surfaces. This is consistent with how the existing job-backed presenter uses the `tab` renderer type.

This is a minor clarification, not a design problem. The existing workspace code already proves the pattern works.

**Type**: Architectural/codebase issue (non-blocking)

### FINDING B — MINOR: Semantic matching rules are effectively engine-key-based heuristics

The concrete rules in Decision 3 are well-chosen but the matching signal is implicitly engine-key-driven:

- `aoi_engagement_mapping` → "source inventory" → `card_grid`
- `aoi_sin_findings` → "multi-facet evidence" → `accordion`
- `aoi_thematic_report` → "synthetic closeout" → `prose`
- `aoi_thematic_synthesis` → (the flexible one, could be prose or accordion)

In practice, the "semantic matcher" for this bounded Stage 11 slice is an engine-key-to-surface-family lookup table with fallback heuristics from section title/role.

This is fine for a bounded first slice. But the memo should be transparent that this is a rule-based heuristic lookup, not an LLM-powered semantic reasoning layer. That distinction matters for:
- implementation simplicity (this should be fast, not an LLM call)
- future generalization (the lookup table doesn't scale, but that's a later problem)
- proof clarity (the trace should show which rule matched, not imply broad semantic understanding)

**Type**: Proof/evidence issue (non-blocking)

---

## STRATEGIC ASSESSMENT

### Is the revised memo honest about what it can deliver?

**Yes.** The four revisions moved the memo from "aspirationally correct but operationally blocked" to "bounded and implementable." The most important correction is the host-delta acknowledgment — without it, the hierarchy proof would produce child views that no consumer renders.

### Is AOI-first still the right choice?

**Yes, and the revised memo strengthens the case.** The genealogy-as-contract-reference pattern (Decision 7) is correct. The existing `AnalysisWorkspacePage.tsx` already proves parent/child rendering for genealogy — Stage 11 only needs to bring the transient shell up to parity with capabilities the product already has for job-backed results.

### Is the semantic matcher concrete enough to implement?

**Yes, now.** The four concrete rules map cleanly to the current AOI engine set. The implementation should be deterministic rule-based code (not an LLM call), which keeps it fast and auditable.

### Is the proof bar achievable?

**Yes.** All five proof items are structurally sound after the revision:

1. Parent/child page structure — achievable once the planner can emit hierarchy
2. Host-backed child rendering — achievable once the shell delta lands
3. Semantic matching changing surface choice — achievable with the engine-key-based rules
4. Fail-closed rejection — achievable with the validation framework already in the compose path
5. Trace artifacts — achievable by extending the existing trace structure

### Does the memo honestly distinguish hierarchy law / renderer-law / scaffold / host-contract?

**Yes.** The most important distinction is Decision 1's line: "narrow the-critic transient-host delta ≠ generic host contract." This is the correct framing. Stage 11 does companion host work within the current AOI shell without claiming Stage 13 is solved.

### Is there anything missing?

**No blocking gaps.** The memo covers the internal plan shape, the matching rules, the refactoring scope, the host delta, the proof bar, and the scope restraints. The two minor findings (parent-view rendering mechanism, engine-key heuristic transparency) are implementation details, not design gaps.

---

## ADDITIONAL DOCUMENTS CONSULTED

Beyond the documents listed in the prompt, I found no additional relevant documents that surface concerns not already addressed in the revised memo. The consumer-side code inspection confirmed:

- `transientComposeAdapters.ts` explicitly ignores child views (line 55)
- `AoiComposeFromIntentShell.tsx` renders only top-level views with a visible "ignored children" notice (lines 35-39)
- `AnalysisWorkspacePage.tsx` already renders two-level parent/child tab navigation (line 1035)
- `renderers/index.ts` has no `tab` type override; the shared package has no `TabRenderer`
- `ViewRenderer.tsx` falls back to `ProseRenderer` for unknown renderer types (line 245)

All of these confirm the revised memo's claims and support its revised scope.

---

## FILES INSPECTED

### Documents (second pass)
- `communications/MEMO_2026-03-23_stage11_rich_semantic_page_planning_scope.md` — revised primary
- `communications/PROMPT_2026-03-23_stage11_rich_semantic_page_planning_scope_review_claude.md` — updated prompt

### Code seams (second pass, new inspections)
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx` (85 lines — confirmed flat top-level rendering with ignored-child notice)
- `/home/evgeny/projects/the-critic/webapp/src/lib/transientComposeAdapters.ts` (65 lines — confirmed child views counted and discarded at line 55)
- `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx` (251 lines — confirmed ProseRenderer fallback for unknown types at line 245)
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/index.ts` (52 lines — confirmed no `tab` type override, only `nested_sections`)
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx` (grep — confirmed two-level parent/child tab navigation at line 1035, child tree traversal at lines 139-160)
- `renderers-ui/src/registry.ts` (29 lines — re-confirmed no `tab` entry in DEFAULT_TYPE_RENDERERS)

### Code seams (carried from first pass)
- `src/presenter/compose_from_intent.py` — flat-planning at 6 locations confirmed
- `src/presenter/scaffold_contracts.py` — scaffold resolution unused by transient path
- `src/views/patterns/tab_with_children.json` — `renderer_type: "tab"`
- `src/views/patterns/timeline_sequential.json` — `renderer_type: "timeline"`
- `src/renderers/definitions/tab.json` — definition exists, no consumer component
- `src/stages/schemas.py` — `semantic_visual_intent` field exists, absent from AOI engines
