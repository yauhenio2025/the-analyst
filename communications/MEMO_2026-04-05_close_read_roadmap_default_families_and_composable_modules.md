# Memo: Close Read Roadmap — Default Families And Composable Modules

Subtitle: Record the larger `Close Read` destination so the roadmap does not collapse into genealogy/AOI polishing or premature standalone-host work

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
Current Close Read Boundary:
- `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`
- `communications/MEMO_2026-04-05_close_read_post_v1_recalibration_multi_engine_boundary.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
Primary Runtime Evidence:
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadAoiPages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_generic.py`
Primary analyzer-v2 Capability Evidence:
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json`
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_suite.json`
- `/home/evgeny/projects/analyzer-v2/src/engines/definitions/inferential_commitment_mapper.json`
- `/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/inferential_commitment_mapper.yaml`

## Purpose

Record one roadmap-level clarification that should govern the next phase of `Close Read` work:

- what the larger destination actually is
- what the current genealogy/AOI work is and is not
- why the next major phase should not be reduced to UI hardening
- how default interpretive families and bespoke multi-engine compositions fit together

This memo exists so the roadmap does not drift into one of two errors:

1. treating the current Critic-hosted `Close Read` families as the whole destination
2. jumping to standalone-host architecture before the product logic is actually complete

## Bottom Line

The larger `Close Read` destination is not:

- one genealogy reader
- one AOI reader
- one fixed set of hard-coded family pages
- one polished host shell that happens to sit on Critic

The larger destination is:

- a `Close Read` application layer over analyzer-v2
- with a set of strong default interpretive families
- plus the ability to add bespoke multi-engine analytical modules with relatively low incremental effort

That means two things must both be true in the roadmap:

1. we continue to build **default product families** like genealogy, AOI, and concept analysis
2. we treat those families as steps toward a more general **composition layer**, not as the final architecture

So the current work should be read correctly:

- genealogy and AOI are the first serious default families under the `Close Read` umbrella
- they are not the final product shape
- the next serious family admission line is concept analysis
- the longer-term destination is a composable module system over analyzer-v2 capabilities

## What The Original Close Read Direction Actually Requires

The dictation memo is explicit.

`communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md` does not describe a product limited to genealogy and AOI.
It describes a flagship app where one might do:

- genealogical analysis
- logical analysis
- `Anxiety of Influence`
- other analysis such as webs of relations

and then perform path-dependent follow-up operations such as:

- testing logical premises
- identifying weak points
- clarifying arguments
- capturing useful outputs
- routing to `Research`
- routing to `Arsenal`
- later feeding `Book Modeler`

That is already enough to establish the real destination:

- multiple engine families
- multiple follow-up operation families
- multiple routes from rendered outputs into downstream work

So the roadmap should no longer behave as if the open question were merely:

- “how do we polish the current Close Read screens?”

The real question is:

- “how do we keep building from default families toward a composable close-reading system?”

## The Right Architectural Reading

The long-horizon destination is easiest to understand as a three-layer system.

### 1. analyzer-v2 capability layer

This is the underlying analytical brain.
It contains:

- engines
- chains
- operationalization passes
- prompt composition
- capability metadata
- renderer and presentation contracts

This is already real in analyzer-v2.
Examples now visible in code:

- a full `concept_analysis_12_phase` chain:
  - `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json`
- a multi-engine concept suite:
  - `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_suite.json`
- an inferential engine with explicit pass structure:
  - `/home/evgeny/projects/analyzer-v2/src/engines/definitions/inferential_commitment_mapper.json`
  - `/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/inferential_commitment_mapper.yaml`

### 2. Close Read composition layer

This is the still-incomplete layer that the roadmap must keep in view.

Its job is to:

- select one or more engine families
- define the sequence in which they should run
- decide which outputs feed subsequent passes
- decide what UI elements those outputs require
- decide which follow-up operations become available on that module

This is the layer that would make it possible to say:

- first run concept analysis
- then run inferential/semantic analysis on top of it
- then surface the resulting logical weak points
- then expose scrutiny/capture/research operations for that specific composition

This is the decisive longer-horizon layer.
It is what turns Close Read from “a collection of bespoke pages” into “a composable analytical application.”

### 3. host/app surface layer

This is where the user experiences the product:

- genealogy family page
- AOI family page
- concept analysis family page
- future mixed/bespoke module pages

These are not the brain.
They are presentations over the brain plus composition logic.

That is why “analyzer-v2 is the brain; apps are presentations” still matters here.

## What The Current Families Actually Are

The current `Close Read` work should be understood as the first default modules.

### Genealogy

Genealogy is:

- the first bounded `Close Read` family
- the first serious reader/capture/provenance corridor proof
- a default interpretive module

It is valuable because it gave the program:

- result-backed routing
- capture/runtime continuity
- family-specific filtered presentation

But genealogy is not the end state.

### AOI

AOI is:

- the first serious non-genealogy admission line
- a second default interpretive module
- proof that different family pages can coexist under one `Close Read` umbrella

The current AOI route also makes something important visible:

- different families will have materially different page logic and controls
- so the long-term goal is not to force every family into the same shell prematurely

### Why this matters

The roadmap should now treat genealogy and AOI as:

- the first default modules
- not the complete product boundary
- not evidence that every future family must look like them

## Concept Analysis Is The Next Serious Family, Not “Logic” In Isolation

One important correction matters for the roadmap.

The old Critic product family is not best described as:

- “logic analysis”

It is better described as:

- `concept analysis`

with multiple submodes inside it:

- inferential
- logical
- assumption
- semantic field
- causal
- metaphorical

This is visible directly in:

- `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`
- `/home/evgeny/projects/the-critic/api/server.py`

So the roadmap should not say:

- “after genealogy and AOI, admit logic”

It should say:

- “after genealogy and AOI, admit the concept-analysis family”

with logical and inferential analysis as major submodes inside that family.

That is more faithful to:

- the old Critic product
- the original Close Read dictation
- the analyzer-v2 engine inventory

## Why Concept Analysis Is A Strong Next Admission Line

Concept analysis is the right next family for two reasons.

### 1. It already existed as a serious product family in the old Critic

The old Critic concept-analysis area already had:

- stable routes
- concept-specific pages
- inferential and logical submodes
- dedicated UI elements for:
  - synthesis
  - hidden weight
  - commitments
  - incompatibilities
  - tensions
  - practical stakes
  - chains
  - causal maps
  - vulnerabilities

This was not conceptual garnish.
It was already one of the strongest examples of engine-specific follow-up operations in the broader Critic estate.

### 2. analyzer-v2 already contains substantial capability inventory for it

The analyzer-v2 side is not empty.

There is already:

- a 12-phase concept-analysis chain
- a multi-engine concept suite
- inferential engines
- vulnerability-oriented engines
- concept-formalization and chain-building engines

So concept analysis is not merely an aspirational family.
It is a family with real migration and composition material already present.

## The Important Migration Reality

The roadmap also needs one honest nuance.

Not all of old concept analysis has already been cleanly analyzer-v2-ified.

The present state is mixed:

- some generic concept modes already fetch analyzer-v2-composed prompts:
  - `/home/evgeny/projects/the-critic/analyzer/analyze_concept_generic.py`
- old inferential analysis still runs through a legacy dedicated prompt path:
  - `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py`
- old logical analysis still runs through a legacy 12-phase orchestrator path:
  - `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py`

So the next phase should not assume:

- “concept analysis is already a turnkey Close Read family”

Instead it should assume:

- concept analysis is the next serious family
- but it still needs an admission audit and migration map

That is a strong next-stage problem.
It is much stronger than generic UI polish.

## What “Composable Close Read Modules” Means In Practice

The future state should allow two types of work.

### 1. Default modules

These are stable, frequently used, productized family surfaces.
Examples:

- genealogy
- AOI
- concept analysis

Each default module has:

- a stable route family
- a known result-discovery pattern
- a known page shape
- known follow-up operations

### 2. Bespoke modules

These are more advanced, composable analytical constructions built from the same underlying capability inventory.

A bespoke module should be able to say things like:

- start with concept analysis
- then run inferential/semantic engines sequentially
- then run vulnerability or premise-scrutiny passes
- then expose the appropriate downstream operations

The essential ambition is:

- low-friction addition of new interpretive modules
- without hand-building an entirely new app every time

This is the real meaning of a `Close Read` composition layer.

## What The Roadmap Should Not Do

This memo does not say UI hardening is useless.
It says UI hardening is not the strategic center **yet**.

The roadmap should therefore avoid over-centering:

- genealogy/AOI surface polish as the primary next phase
- standalone-host work as the immediate next phase
- generic shell beautification as if the family inventory were already complete

Those are secondary relative to the bigger missing pieces:

- concept-analysis family admission
- composition-layer design
- migration of legacy concept/inferential/logical work into a cleaner analyzer-v2-backed Close Read model

## Roadmap Implications

This memo should inform the roadmap in five concrete ways.

### 1. Do not treat V1.5 coexistence as the end of the product-shape problem

It proves:

- umbrella routing
- family coexistence
- shared baseline law

It does not prove:

- full family inventory
- composable module logic
- standalone Close Read product sufficiency

### 2. The next serious family admission line is concept analysis

Not:

- “logic alone”

But:

- concept analysis as a family
- with inferential/logical submodes central inside it

### 3. The next major docs-first step should be an admission audit for concept analysis

The next strong memo should inventory:

- what the old concept-analysis family actually did
- which parts are already analyzer-v2-backed
- which parts are still legacy-only
- which concept-analysis submodes are the first honest admission cut for `Close Read`
- which follow-up operation families belong there

### 4. After that, the roadmap should move toward a composition-layer memo

Once three serious family lines are visible:

- genealogy
- AOI
- concept analysis

the next roadmap-level question becomes:

- how do we define `Close Read` as a module-composition layer over analyzer-v2 capabilities?

That memo should likely freeze:

- what a module recipe is
- what engine sequencing rules look like
- what output-to-output chaining is allowed
- what UI-generation contract the host can rely on
- what follow-up operation metadata each module must expose

### 5. The standalone-host question remains downstream

A standalone `Close Read` app may still be the right long-horizon destination.
But it should not become the center of gravity before:

- several strong default families exist
- concept analysis is admitted
- the composition logic is materially clearer

Otherwise the program risks rebuilding host architecture before it has fully specified the product.

## Decisions This Memo Freezes

This memo freezes the following roadmap-level readings.

### 1. The larger Close Read destination is dual in form

It includes:

- strong default interpretive families
- and a longer-horizon composition layer for bespoke modules

### 2. genealogy and AOI are default families, not the whole destination

They are:

- real progress
- necessary modules
- insufficient as the final `Close Read` product

### 3. concept analysis is the next serious family candidate

The next major admission question is:

- concept analysis family boundary and migration

not:

- generic visual polish

### 4. UI hardening is subordinate to family completion and composition design

It remains worthwhile.
It is just not the roadmap’s primary unresolved question.

### 5. standalone-host work stays deferred

It remains a real long-horizon possibility.
It is not the next honest center of the roadmap.

## Recommended Next Artifacts

This memo implies the following next roadmap artifacts.

### Immediate next memo

- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md`

Its job should be to:

- inventory the old concept-analysis family
- map it to analyzer-v2 engines/chains/passes
- distinguish already-migrated from legacy-only seams
- propose the first bounded concept-analysis family cut for `Close Read`

### Follow-on memo after that

- `communications/MEMO_2026-04-05_close_read_composable_module_layer_direction.md`

Its job should be to:

- define what a `Close Read` module is
- distinguish default modules from bespoke compositions
- define how analyzer-v2 capability sequencing should inform future host surfaces

## Final Reading

The right strategic reading now is:

- the current genealogy/AOI work is valuable and necessary
- but it is not yet the larger `Close Read` destination
- the product is heading toward a system of:
  - default interpretive families
  - plus composable bespoke analytical modules
- concept analysis is the next serious family line that should inform the roadmap
- UI polish and standalone-host work should remain secondary to that larger completion logic

If the roadmap keeps this distinction clear, the current `Close Read` work remains on course.
If it loses this distinction, the program risks over-polishing a still-partial product while forgetting the composition logic that originally motivated the app.
