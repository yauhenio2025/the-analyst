# Memo: Phase 4 Scope - Cross-Workflow Generic Workspace Proof

## Purpose

Define the scope for **Phase 4 / Deliverable D** in the Thin Consumer Platformization program.

This memo should make the next tranche reviewable before it becomes an implementation plan.

It should answer:

1. why Deliverable D is the next step now
2. what exactly the generic-workspace proof should cover
3. what must remain out of scope
4. what evidence is required for this tranche to count as a real proof

This memo sits beneath:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase3_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_roadmap_after_phase3.md`
- `/home/evgeny/projects/analyzer-v2/communications/PLAN_2026-03-18_thin_consumer_platformization_implementation.md`

## Why This Is The Right Next Tranche

Deliverables A, B, and C are now done in substance.

What remains is the proving vehicle named from the start:

- **The Critic's generic `AnalysisWorkspacePage`**

The round-1 platform story only becomes credible if one generic workspace path can carry both bounded workflows:

- `intellectual_genealogy`
- `anxiety_of_influence_thematic_single_thinker`

without collapsing back into bespoke host logic.

That is why Deliverable D is next.

## Current Code Reality

The current codebase already gives this tranche a real seam.

### What already exists

- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
  - already runs the generic bounded-v2 start/import/restore path
  - already uses the shared Phase 2 contract:
    - `boundedV2Client.ts`
    - `useBoundedV2Workspace.ts`
  - already supports generic saved-result restore and direct v2 preview/import
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
  - already supports `selectedSourceThinkerId` for upstream run discovery and result discovery
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts`
  - already supports `selectedSourceThinkerId` for active-run discovery and restore-first lifecycle handling
- `/home/evgeny/projects/the-critic/api/server.py`
  - the generic `/api/analysis/{workflow_key}/analyze` path already accepts:
    - `selected_source_thinker_id`
    - `selected_source_thinker_name`
  - AOI thematic v2 already validates that `selected_source_thinker_id` is required
- generic saved-result summaries in Critic already carry:
  - `selected_source_thinker_id`
  - `selected_source_thinker_name`
  when that identity is present on the saved result

### What still lives outside the proving vehicle

- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
  - still owns thinker-scoped AOI launch behavior
  - still owns thinker-scoped saved-result filtering semantics
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx`
  - remains the richer bespoke genealogy surface
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useWorkflowMetadata.ts`
  - only provides descriptive metadata
  - does **not** provide a generic input-schema / form-definition system

This matters because Deliverable D should prove one generic workspace path, not widen into a general dynamic-form framework.

## Scope Decision

## In Scope

The tranche should stay tightly bounded to one proof:

- **prove that `AnalysisWorkspacePage` can be the generic host for both bounded workflows**

That proof must include:

1. genealogy through the existing generic path
2. AOI thematic single-thinker through the same generic path, with one explicit bounded thinker context
3. the same shared bounded-v2 contract underneath both workflows
4. one deliberate entry path from the AOI bespoke surface into the generic workspace proof route
5. verification that AOI run/result discovery in the generic workspace is thinker-scoped rather than mixed across the whole project

## Recommended shape

The recommended AOI context seam is:

- explicit URL query parameters on the generic route

For example:

- `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=<id>&selected_source_thinker_name=<name>`

Why this is the right first seam:

1. it is explicit
2. it is reviewable and testable
3. it avoids a hidden navigation-state-only contract
4. it avoids widening into a dynamic input system

For this route contract, treat:

- `selected_source_thinker_id` as the authoritative bounded input
- `selected_source_thinker_name` as optional display/context metadata

The generic workspace should use this bounded context for:

- AOI start request body
- active-run discovery
- upstream result discovery
- local saved-result filtering

Analyzer-v2 changes are not part of the default scope.

One implementation detail is mandatory in this tranche:

- `AnalysisWorkspacePage.handleRunAnalysis` must inject `selected_source_thinker_id` and, when available,
  `selected_source_thinker_name` into the AOI launch body

Without that, the generic AOI launch will fail the existing backend validation.

## Concrete deliverable

At the end of this tranche, the system should be able to demonstrate:

### Workflow 1: genealogy

- `AnalysisWorkspacePage` can run `intellectual_genealogy`
- `AnalysisWorkspacePage` can restore prior genealogy results
- this remains the same generic path already in use

### Workflow 2: AOI thematic single-thinker

- `AnalysisWorkspacePage` can run `anxiety_of_influence_thematic_single_thinker`
- the launch uses one bounded thinker context
- `AnalysisWorkspacePage` can restore AOI results for that thinker through the same generic route
- active-run discovery on the generic page is scoped to the selected thinker
- upstream result discovery on the generic page is scoped to the selected thinker
- local saved-result filtering on the generic page is scoped to the selected thinker

### Entry behavior

There must be one deliberate way to exercise the AOI proof route from the existing AOI surface.

The most likely shape is:

- a bounded handoff or link from the AOI page/panel into the generic workspace route with thinker context prefilled

This tranche does **not** require removing the bespoke AOI surface.

### Explicit exclusion

Generic manual `Preview V2` / `Import + Save` for AOI should stay out of the proof acceptance path unless
the team deliberately adds a small Critic-side metadata-preservation patch. The main proof for this tranche
is generic route launch + scoped discovery + restore, not generic manual import.

## Out Of Scope

To keep the tranche honest, the following are out of scope:

- a general workflow-input / dynamic-form system
- schema-driven launch UX for all workflows
- replacing `GenealogyPage` as the primary bespoke genealogy surface
- replacing the AOI page as the primary bespoke AOI surface
- multi-thinker AOI support in the generic workspace
- analyzer-v2 API or schema changes, unless a concrete blocker proves a minimal change is unavoidable
- broad route reorganization across the whole app
- dynamic composition or “apps on the fly”

If implementation starts expanding into any of those, the tranche is drifting.

## Primary Code Surfaces To Scrutinize

The most important files for this scope review are:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useWorkflowMetadata.ts`
- `/home/evgeny/projects/the-critic/api/server.py`

These are the places where the real proof seam already exists or can accidentally widen.

## Acceptance Criteria

This tranche should be treated as done only if all of the following are true:

1. `AnalysisWorkspacePage` can run and restore `intellectual_genealogy` through the generic route.
2. `AnalysisWorkspacePage` can run and restore `anxiety_of_influence_thematic_single_thinker` through the generic route when provided one explicit thinker context.
3. `AnalysisWorkspacePage.handleRunAnalysis` includes `selected_source_thinker_id` and, when available, `selected_source_thinker_name` in the AOI launch body.
4. AOI active-run discovery, upstream result discovery, and local saved-result filtering in the generic workspace are thinker-scoped.
5. Both workflows rely on the shared bounded-v2 contract from Phase 2 rather than reintroducing duplicated lifecycle code.
6. The AOI proof route is deliberately reachable from the existing AOI surface.
7. The tranche does not broaden into a general workflow-input or dynamic-form system.
8. `GenealogyPage` and the AOI bespoke page remain intact as bespoke surfaces; this tranche is a proof, not a replacement program.
9. Generic AOI manual `Preview V2` / `Import + Save` is either:
   - explicitly excluded from acceptance, or
   - deliberately patched so thinker identity is preserved for local saved-result behavior.

## Verification Expectations

The expected verification for this tranche should be:

- targeted frontend tests for:
  - generic workspace query-parameter / bounded-context parsing
  - AOI launch body composition
  - AOI thinker-scoped discovery wiring
  - AOI thinker-scoped local saved-result filtering
  - handoff from the AOI surface to the generic workspace route
- one manual genealogy proof run or restore via `AnalysisWorkspacePage`
- one manual AOI single-thinker proof run or restore via `AnalysisWorkspacePage`, confirming:
  - launch succeeds with thinker-bounded context
  - saved results shown on the generic page are limited to that thinker
  - active-run discovery is limited to that thinker

The verification target is not:

- “the generic workspace probably could support both”

It is:

- “the same generic route was deliberately exercised for both workflows”

## Failure Modes To Watch For

The main ways this tranche can go wrong are:

- widening into a generic dynamic-form/input-schema system
- using hidden navigation state instead of an explicit bounded route contract
- mixing AOI results from multiple thinkers in the generic workspace
- trying to replace the bespoke genealogy or AOI surfaces instead of proving the generic one
- widening into analyzer-v2 changes when the current Critic route already accepts AOI thinker parameters
- turning the tranche into a route rewrite instead of a proving-vehicle proof

## Recommended Next Decision Rule

If review finds that the generic workspace can support the AOI bounded context with:

- explicit query parameters
- existing shared contract
- no analyzer-v2 changes

then Deliverable D should stay a `the-critic`-first tranche.

Only if code review proves a real blocker should the scope widen beyond that.

## Final Scope Sentence

If the team needs one operational sentence for this tranche, it should be:

- **Make `AnalysisWorkspacePage` the deliberate proof route for genealogy and AOI single-thinker by adding one explicit bounded thinker context to the existing generic path, and keep everything broader out of scope.**
