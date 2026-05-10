# Memo: Stage 11 / Rich Semantic Page Planning Scope

Subtitle: AOI-First Hierarchical Semantic Surface Planning Over Existing Presenter Contracts

Date: 2026-03-23
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Prior Stage Memo: `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md`
Stage 10 Completion: `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_completion.md`
Stage 9 Completion: `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_completion.md`
Round 11 Compose Memo: `communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md`
Semantic Matcher Proposal: `docs/SEMANTIC_VISUAL_MATCHER_PROPOSAL.md`

## Purpose

Define the first honest Stage 11 slice after Stage 10 source-backed readiness.

This memo is about the next missing downstream seam:

- richer page planning over composition-ready source material
- semantic surface choice based on analytical meaning, not only data shape
- bounded hierarchy/container planning over the existing presenter/view contract
- stronger traceable law between transient planning and the surfaces the presenter already knows how to serve

It is not about:

- generic cross-workflow compose-from-intent
- universal host-contract cutover
- universal renderer-law rollout
- arbitrary renderer invention
- broad task-to-page planning from open-ended user requests
- replacing authored/runtime composition across the whole product

## Why This Stage Now

Stages 9 and 10 materially changed the downstream position:

1. analyzer-v2 can now normalize route-plus-hydrate-plus-plan truth
2. analyzer-v2 can now normalize results-layer readiness truth over AOI and genealogy
3. the only live transient page planner is still the bounded AOI `compose-from-intent` / `compose-from-source` seam
4. that planner is still explicitly flat even though the presenter already contains real hierarchy, scaffold, and runtime-composition machinery elsewhere

So the next missing seam is not another readiness layer.

It is:

- semantic page planning that can target richer yet valid presenter surfaces under contract law

The roadmap already names that as Stage 11.

## Explicit Sequencing Note

Stages 2-6 and Stages 12-13 are still open in the canonical roadmap.

Pulling Stage 11 into explicit scope now is another bridge-infrastructure move, not a claim that those stages stopped mattering.

The reason is:

- Stage 9 now exposes upstream planning truth
- Stage 10 now exposes downstream readiness truth
- the next missing bridge is the page-planning seam between composition-ready material and the actual surfaces the host can consume

At the same time, this stage must stay restrained:

- Stage 11 should not pretend renderer law is already universal across workflows
- Stage 11 should not pretend AOI/the-critic coupling is solved
- Stage 11 should not claim a generic cross-workflow transient planner when only one real transient planner path exists today
- Stage 11 may require narrow the-critic companion work to render analyzer-produced child views, but that is not the same as claiming a generic host contract is solved

## Strategic Diagnosis

The current codebase already contains substantial pieces of the Stage 11 story.

### What is already real

The presenter/view contract already supports hierarchy:

- `src/views/schemas.py` already exposes:
  - `parent_view_key`
  - `child_display_mode`
  - `surface_role`
  - `tab_count_field`
  - `scaffold_contract`

The pattern catalog already supports richer structures than the transient planner currently uses:

- `src/views/patterns/tab_with_children.json`
- `src/views/patterns/accordion_sections.json`
- `src/views/patterns/timeline_sequential.json`

The presenter already has real hierarchy-aware and semantic-adjacent machinery:

- `src/presenter/view_refiner.py` already reasons about:
  - hierarchy overrides
  - promotion and collapse
  - renderer overrides
  - top-level grouping
- `src/presenter/scaffold_contracts.py` and `src/presenter/decision_trace.py` already resolve and trace scaffold semantics
- `src/presenter/bounded_dynamic_composition.py` already generates parent/child runtime surfaces for genealogy and AOI proof modes
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx` already renders parent/child result trees with first-row parent tabs and second-row child tabs

The transient planner itself is also already real:

- `src/presenter/compose_from_intent.py` already owns:
  - page-structure planning
  - generated view creation
  - transformation orchestration
  - consumer adaptation
  - final renderer-contract validation

But the current transient host seam is narrower than the generic result-restore host seam:

- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx` still renders transient compose output as a flat list of top-level views
- `/home/evgeny/projects/the-critic/webapp/src/lib/transientComposeAdapters.ts` explicitly ignores returned child views instead of preserving the tree

So Stage 11 is not greenfield page planning.

### What is not yet real

The transient planner is still much narrower than the presenter contract it sits on top of.

Today `src/presenter/compose_from_intent.py` still hardcodes:

- AOI-only workflow/consumer bounds
- a flat plan:
  - exactly one top-level view per input section
  - no parents
  - no children
  - no tabs
- a small pattern allowlist:
  - `prose_narrative`
  - `accordion_sections`
  - `card_grid_simple`
  - `card_grid_grouped`
- a narrow renderer family:
  - `prose`
  - `accordion`
  - `card_grid`

It also does not yet consume the semantic signal layer that already exists elsewhere:

- `semantic_visual_intent` exists in engine definitions and stage schemas
- the semantic matcher proposal already describes the missing meaning-to-form seam
- but none of the current AOI engines define `semantic_visual_intent`, and the current transient page planner still chooses patterns without a real semantic matching layer

The flatness is also not isolated to one data structure.

It is embedded across the transient compose path:

- request validation
- planner system prompt
- planner output shape parsing
- row/index validation
- generated view normalization
- payload assembly
- transient host adaptation

So Stage 11 is not a schema swap.

It is a real refactor across the compose module and its thin AOI host seam.

So the repo already has:

- hierarchy-capable presenter law
- scaffold-capable semantics
- runtime composition families
- semantic-intent metadata in the engine layer

But it does not yet have:

- a page planner that can target those richer contracts honestly

## The Real Stage 11 Problem

The real Stage 11 problem is not:

- "let the LLM invent richer pages"

It is:

- "replace the flat section-to-view planner with a bounded semantic surface planner that can choose valid hierarchy and surface family under existing presenter law"

That distinction matters.

If Stage 11 is framed as open-ended creativity, it will reintroduce exactly the risk the roadmap warns against:

- loose renderer behavior without stronger law

The bounded version is narrower and more defensible:

- each input section still has traceable ownership
- hierarchy is explicit and validated
- allowed surfaces come from a contract-backed allowlist
- semantic matching is required, but only inside a bounded family of safe choices

## Recommended Stage 11 Shape

### Decision 1: keep the public compose routes stable, but allow narrow transient-host companion work

Stage 11 should continue to use the existing public presenter entrypoints:

- `POST /v1/presenter/compose-from-intent`
- `POST /v1/presenter/compose-from-source`

The public route shape is not the missing seam.

The missing seam is the internal page-planning contract.

So the stage should:

- keep the public routes stable
- materially revise the internal planning contract
- bump the transient resolver/version tokens so richer planning behavior is explicit and auditable
- explicitly allow a narrow the-critic transient-host delta so analyzer-produced child views can actually be rendered instead of being dropped

That narrow host delta should stay bounded to the current AOI transient shell, for example by either:

- teaching `AoiComposeFromIntentShell` plus `transientComposeAdapters.ts` to preserve and render child trees, or
- reusing the existing generic result-tree rendering seam already present in `AnalysisWorkspacePage.tsx`

That matches the Stage 7 pattern where the route stayed stable while the internal resolver contract advanced.

It does **not** mean:

- generic host neutrality
- a universal cross-app contract
- Stage 13 is solved early

### Decision 2: replace flat planner rows with a bounded hierarchical semantic page plan

The current `_PlannerRow` shape is too flat for Stage 11.

The stage should introduce an internal plan shape that can express:

- top-level surfaces
- optional parent containers
- child leaf surfaces
- per-surface semantic role
- allowed pattern selection
- explicit section assignment

The bounded rule should stay strict:

- every input section must still map to exactly one generated leaf surface
- no source section may be silently dropped
- no source section may be split across multiple generated leaves in this stage
- parent surfaces may group leaves, but they do not invent a second opaque content source
- hierarchy depth should stay bounded to one parent/child layer in this stage

That gives Stage 11 richer structure without opening unconstrained tree planning.

### Decision 3: make semantic matching a required sub-layer, but define it with AOI-local rules rather than depending on engine-level semantic coverage

This is the main architectural correction.

The roadmap and `docs/SEMANTIC_VISUAL_MATCHER_PROPOSAL.md` are right:

- matching by data shape alone is not enough for the "bespoke" claim

But Stage 11 should implement the analyzer-side bounded version of that idea, not the full external visualizer proposal.

Because the current AOI engines do not yet provide `semantic_visual_intent`, the Stage 11 matcher cannot depend on that field as its primary substrate.

What should land instead is a bounded analyzer-side semantic surface router that works from AOI-local signals that already exist now, such as:

- source profile and source-family identity from the Stage 7 bridge
- section engine key
- section title and bounded section role
- planner hints and pattern metadata
- optional `semantic_visual_intent` only when it exists on future engines

The matcher should therefore use explicit rules like:

- source inventory / corpus listing semantics -> `card_grid` family
- multi-facet evidence bank or findings-bank semantics -> `accordion` family
- synthetic closeout / report / implications semantics -> `prose` family
- multiple complementary child surfaces that belong under one shared analytical heading -> `tab_with_children`

That gives Stage 11 a real matching substrate instead of a rhetorical pointer to the external proposal.

What should not be claimed:

- full cross-product semantic-visualizer integration
- universal semantic coverage across all engines
- AOI dependence on `semantic_visual_intent` that does not currently exist

Stage 11 only needs a required bounded semantic-matching layer inside the current analyzer-owned compose path.

### Decision 4: reuse existing presenter/view law instead of inventing a second layout contract

Stage 11 should compile its richer plan into the same view/payload contract the presenter already understands.

That means reusing fields and seams such as:

- `parent_view_key`
- `child_display_mode`
- `surface_role`
- `tab_count_field`
- existing generated `ViewDefinition` normalization
- existing consumer adaptation
- existing contract validation
- existing decision-trace infrastructure

It should also take advantage of semantics the presenter already knows how to express:

- derived `composite_overview` scaffolds on dense parent surfaces
- existing declared scaffold families where there is already explicit contract support

Stage 11 should not create a second ad hoc layout vocabulary beside the view schema.

### Decision 5: broaden the surface family only through host-backed, contract-backed choices

The stage must move beyond the current three-renderer flat planner.

But it should do so in a bounded way.

The most honest Stage 11 move is:

- keep the existing bounded leaf families
- add explicit parent-container planning through `tab_with_children`
- require that any newly admitted family be both:
  - analyzer-contract-backed
  - materially rendered by the current AOI transient host
- keep every added pattern/renderer pair behind explicit allowlisting and final contract validation

That means Stage 11 should **not** count metadata-only variety as proof.

For example:

- `timeline_sequential` should stay deferred unless the current consumer path renders it in a materially distinct way from `card_grid`

The stage should **not**:

- open the whole renderer registry
- allow arbitrary nested containers
- allow planner-authored renderer types without contract-backed pattern resolution

So the required broadened family in this first Stage 11 slice is:

- real child-view tab/container planning

not:

- a long list of nominally different pattern keys that still collapse to the same host rendering

The broadened family should still be small, named, host-backed, and fail-closed.

### Decision 6: treat Stage 11 as a real compose-module refactor, not a planner-schema swap

The compose module’s flat assumptions are distributed, not localized.

So Stage 11 should be described honestly as a refactor touching multiple seams, including:

- planner prompt and planner output parsing
- section assignment validation
- normalized generated view shape
- payload assembly and child linking
- transient trace structure
- thin AOI host adaptation for returned child views

This should be explicit in the scope so implementation effort is not understated.

### Decision 7: keep Stage 11 AOI-first, and use genealogy as a contract reference rather than a second transient planner consumer

This is the most important scope restraint.

Stage 10 just proved cross-workflow readiness over AOI and genealogy.

That does **not** mean Stage 11 should now claim generic cross-workflow semantic page planning.

The current codebase reality is:

- AOI has the live transient compose path
- genealogy has authored/result-restore/runtime-composition richness, but not a second transient planner path

So the bounded Stage 11 implementation should stay AOI-first:

- richer semantic planning inside `compose-from-intent` / `compose-from-source`

Genealogy should still inform the design:

- it is evidence that the presenter can already serve valid parent/child structures
- it is evidence that richer semantic surfaces are not hypothetical

But genealogy should be treated as:

- a contract reference
- not a second transient planner target in this stage

### Decision 8: make hierarchy and semantic reasoning visible in trace, not only in final output

Stage 11 should expand the transient trace so the richer planner is auditable.

At minimum the trace should expose:

- semantic surface matching
- hierarchy/container planning
- generated view normalization
- transformation execution
- consumer adaptation
- contract validation

This stage also needs stronger fail-closed planning validation, including errors such as:

- orphan child surface
- duplicate section assignment
- unknown or blocked pattern selection
- invalid parent/container choice
- blocked hierarchy depth
- semantic matcher output that resolves to no allowed surface family

That keeps richer planning inspectable rather than magical.

### Decision 9: do not import Stage 12 or Stage 13 too early

Still blocked in this stage:

- universal renderer-law rollout across workflows
- host-neutral AOI compose followup
- generic cross-workflow transient planning
- planner-driven selector choice from open-ended tasks
- broad workflow coverage beyond the current AOI transient seam

Stage 11 is about richer semantic page planning under existing presenter law.

It is not the stage where analyzer-v2 solves:

- universal renderer law
- universal host law
- full platform-neutral transient composition

## Candidate Internal Shape

The likely Stage 11 internal seam is a bounded semantic page-plan object, for example:

- `SemanticPagePlan`
- `SemanticPagePlanSurface`

with fields along the lines of:

- `surface_key`
- `surface_role`
- `pattern_key`
- `parent_surface_key`
- `source_section_indexes`
- `section_semantic_role`
- `child_display_mode`
- `semantic_rationale`
- `matcher_evidence`

The exact class names do not matter.

The important part is the contract:

- richer than `_PlannerRow`
- still bounded
- still traceable back to source sections
- still compilable into existing generated `ViewDefinition` output

## Bounded Claim For Stage 11

Stage 11 should prove one bounded thing:

- analyzer-v2 can take the existing AOI transient composition seam and upgrade it from flat section-to-view planning into bounded hierarchical semantic surface planning over the presenter contracts it already knows how to validate and serve

That is enough to move from:

- flat transient AOI pages

to:

- richer but still fail-closed semantic pages

without pretending the platform already has generic cross-workflow page planning.

## Proof Bar

Stage 11 should not be treated as complete without evidence for all of the following:

1. one live AOI source-backed case proving the planner can emit a valid parent/child page structure rather than only flat top-level views
2. one live host-backed case proving those returned child views are actually rendered by the current AOI transient host rather than ignored
3. one live case proving semantic matching changes the chosen surface family or grouping decision based on concrete AOI-local semantic rules rather than raw structure alone
4. one fail-closed case proving invalid hierarchy, unsupported child hosting, or blocked semantic-family selection is rejected rather than silently flattened or ignored
5. saved trace artifacts showing semantic matching and hierarchy decisions explicitly

## Exit Evidence

Minimum acceptable exit evidence:

- richer internal page-plan contract in code
- stable public compose routes with updated transient resolver/version stamping
- bounded parent/child hierarchy support in transient composition
- bounded semantic matcher support in the planning path using concrete AOI-local rules
- narrow the-critic transient-host support for returned child views
- broadened but still explicit host-backed surface allowlist
- focused regression tests
- saved proof artifacts for success and fail-closed planning cases

## What Stage 11 Should Not Claim

Stage 11 should **not** claim:

1. generic compose-from-intent across workflows
2. full external semantic visual matcher integration
3. universal renderer law
4. host-neutral AOI compose flow
5. task-to-page generality from `route-task` or `plan-task`
6. arbitrary deep layout trees or free-form renderer invention
7. distinct new leaf families whose current host rendering is only metadata-deep

Those remain later-stage work.

## Strategic Payoff

If Stage 11 lands in this bounded form, the platform position improves in the precise place that is still visibly thin.

The system would then have:

- Stage 9: route-plus-hydrate-plus-plan normalization
- Stage 10: source-backed readiness normalization
- Stage 11: richer semantic page planning over existing presenter contracts

That would materially strengthen the bridge between:

- analyzer-owned planning and readiness truth

and:

- the richer surfaces a thin host can actually consume

without overstating current cross-workflow or host-neutral generality.
