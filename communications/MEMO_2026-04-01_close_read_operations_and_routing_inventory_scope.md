# Memo: Close Read Operations And Routing Inventory Scope

Subtitle: Immediate product-discovery tranche to inventory downstream operations, routing destinations, and candidate semantic-affordance hypotheses

Date: 2026-04-01
Program: Dynamic Bespoke Apps Platformization
Reference Dictation:
- `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
Direction Memo:
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
Immediate Analyzer Tranche:
- `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_scope.md`
Current Strategy Context:
- `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`

## Purpose

Define the immediate product-side discovery tranche that should run alongside, but not replace, the current analyzer-side composition metadata extraction tranche.

This memo scopes one bounded inventory effort:

- identify the actual downstream operations already embodied in current apps
- identify the actual artifact destinations already embodied in current apps
- identify which output properties make those operations possible
- derive a first candidate set of semantic-affordance and routing-hint hypotheses for later analyzer work

This is a discovery/documentation tranche, not a product build and not a new analyzer implementation tranche.

## Strategic Decision

The immediate next program should have two parallel tracks:

1. analyzer-side execution:
- `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_scope.md`

2. product-side discovery:
- this inventory tranche

This memo scopes only the second track.

It is the right immediate companion because the revised `Close Read` direction memo now says:

- the missing layer is not only renderer/output law
- it is also downstream operations and artifact routing
- but we should inventory concrete existing patterns before writing a larger `Close Read V1` target-state memo

## What This Tranche Is Trying To Learn

This tranche should answer four concrete questions:

1. What downstream operations already exist in practice?

Examples likely include:

- capture
- add/promote to Arsenal
- route to research todo / research question
- annotate/comment
- accept revision
- route to talking points / outline-like downstream structures
- logic-gap or premise-vulnerability scrutiny

2. What destinations already exist in practice?

Examples likely include:

- Arsenal
- Research / research todo
- outline / talking points
- external research support flows
- future Book Modeler-adjacent destinations inferred by product intent but not yet implemented

3. Which operations are generic versus output-specific?

The inventory should distinguish at least:

- generic capture/annotation operations
- output- or surface-specific follow-up operations
- routing contracts

4. What analyzer-side semantic affordances would likely be sufficient for thin hosts to operationalize those patterns without host-side reconstruction of analysis meaning?

The deliverable is not “analyzer-v2 should own every operation.”
The deliverable is:

- a first candidate set of semantic-affordance and routing-hint hypotheses

This tranche should not attempt to define:

- final analyzer schema shape
- final attachment point
- final serialization format

Those belong after the active extraction tranche clarifies the post-extraction metadata shape.

## In Scope

### 1. Audit the current downstream patterns in `the-critic`

Focus on actual runtime flows, not just memos, especially:

- capture state and destinations
- capture action surfaces
- Arsenal promotion and removal
- research todo / research question flows
- finding revision / acceptance flows
- comment / annotation flows where they affect downstream routing
- any outline/talking-point routing paths
- research-answer flows, including NotebookLM-backed answer handling

The primary runtime audit surface should be broader than two files.
At minimum, include the files that materially govern:

- capture state
- capture actions
- research question formulation
- research todo queue / lookup lifecycle
- findings routing
- outline/talking-point routing
- research-answer comment/routing stubs where present

### 2. Audit the current logic/rhetoric structures in `analyzer-mgmt`

Treat `analyzer-mgmt` as explicitly secondary evidence.

Focus on what is useful as evidence of:

- output richness
- logical vulnerability structures
- premise / attack / missing-link schema shape
- plan-side research intent

This audit should distinguish clearly between:

- runtime interaction patterns
- seeded prompt/schema intent

The expected classification here is:

- mostly product intent and schema richness
- not primary runtime evidence of downstream operation law

### 3. Produce one structured inventory

At minimum, each inventory row should record:

- operation name
- current app/repo
- current source of truth
- current owning layer
- trigger surface
- source granularity
- required output structure or semantic precondition
- destination, if any
- current artifact seam
- whether the operation is generic or output-specific
- whether the operation is clearly runtime-real, merely latent, or only aspirational
- candidate semantic-affordance or routing-hint hypothesis that could support it later

## Explicitly Out Of Scope

- building `Close Read`
- writing the final `Close Read V1` product memo as the main deliverable
- changing analyzer routes or schemas
- adding semantic affordances to analyzer responses yet
- auditing active analyzer-v2 attachment points in detail while the extraction tranche is restructuring them
- host refactors in `the-critic`
- host refactors in `analyzer-mgmt`
- new proof harness work
- lifecycle widening
- output-family taxonomy as the primary deliverable

## Why This Slice Is Next

This slice is next because it is the smallest honest response to the direction memo.

It avoids two bad moves:

1. jumping straight to a new flagship app build without extracting real existing patterns first
2. continuing analyzer-side architecture work without grounding it in the actual downstream product behavior we want

It is also deliberately smaller than a full product memo.

The sequence should be:

1. extraction tranche continues on the analyzer side
2. this inventory tranche documents the real downstream operation/routing surface
3. then a later `Close Read V1` memo can be written from evidence rather than intuition

## Proposed Sources To Audit

### Primary runtime evidence

- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/ResearchTodosPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/research/ResearchCard.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useResearchTodos.ts`
- `/home/evgeny/projects/the-critic/webapp/src/OutlinePanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/OutlineEditorPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/research/researchConstants.ts`
- nearby `the-critic` files that materially govern capture, Arsenal, research todo, comments, and routed artifacts

### Secondary product-intent evidence

- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/plans/[id].tsx`
- `/home/evgeny/projects/analyzer-mgmt/scripts/seed_rhetoric.py`
- `/home/evgeny/projects/analyzer-mgmt/scripts/populate_rhetoric_schemas.py`
- any nearby analyzer-mgmt files that materially define logic-gap or rhetoric structures

### Post-extraction addendum only

After the active extraction tranche lands, a short addendum may inspect likely analyzer-side attachment points such as:

- `src/presenter/schemas.py`
- `src/presenter/manifest_builder.py`
- `src/presenter/presentation_bridge.py`
- any then-current metadata seam exposed by the extraction tranche

## Deliverables

This tranche should produce:

### A. One inventory memo

A memo that records:

- downstream operations observed
- artifact destinations observed
- classification of each operation
- current source-of-truth location for each row
- candidate semantic-affordance and routing-hint hypotheses only

It should stay runtime-first.
It should not attempt to finalize analyzer schema shape.

### B. One inventory matrix artifact

This can live:

- in the memo body
- or as a separate appendix/table file

But it should be structured enough to be reused by later scopes.

### C. One short recommendation section for the tranche after extraction

That recommendation should answer:

- what is the smallest follow-on tranche once composition metadata extraction lands?

Examples might be:

- first semantic-affordance annotation seam
- first routing-hint seam
- first host consumption of analyzer-owned affordances

But this tranche should only recommend, not implement.

## Acceptance Bar

This tranche counts as complete only if all of the following are true:

1. it clearly distinguishes:
- runtime-real downstream operations
- latent product intent
- aspirational future routing

2. it clearly distinguishes:
- generic operations
- output-specific operations
- routing contracts

3. it does not collapse host-local UX behavior into analyzer-owned law prematurely

4. it proposes only candidate semantic-affordance and routing-hint hypotheses, not finalized analyzer schema or analyzer ownership of every downstream interaction

5. it records concrete source-of-truth and artifact-seam columns so the ownership boundary is explicit rather than speculative

6. it is evidence-backed enough that a later `Close Read V1` memo can cite it rather than re-infer the operation/routing surface from scratch

7. any analyzer-side attachment-point discussion is deferred to a post-extraction addendum rather than being treated as part of the primary inventory

## Recommended Verification Surface

This is primarily a code-and-doc audit tranche.
It should validate itself by direct file inspection rather than by new runtime proof.

Recommended inspection surface:

- `the-critic` runtime files governing capture and downstream routing
- `analyzer-mgmt` plan/rhetoric structures
- relevant recent memos in `communications/`

## Honest Claim If Completed

If this tranche closes honestly, the claim should remain narrow:

- we have a code-backed inventory of the downstream operations and artifact-routing patterns that the future `Close Read` flagship will need, plus a first candidate set of semantic-affordance and routing-hint hypotheses and a clearer basis for the tranche after composition metadata extraction

It would **not** yet mean:

- analyzer-v2 already owns operation-family law
- `Close Read` has been fully scoped as a product
- host UX can now be generalized automatically
- the platform is ready for arbitrary downstream action routing
