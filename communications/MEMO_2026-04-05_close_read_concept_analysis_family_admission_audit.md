# Memo: Close Read Concept-Analysis Family Admission Audit

Subtitle: Inventory the old concept-analysis family, map it to analyzer-v2, and define the first honest concept-family admission question for `Close Read`

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
- `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`
- `communications/MEMO_2026-04-05_close_read_post_v1_recalibration_multi_engine_boundary.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
Primary Critic Product Evidence:
- `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_generic.py`
- `/home/evgeny/projects/the-critic/analyzer/save_engine_results.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p03_argument_formalization.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p09_vulnerability_analysis.py`
Primary analyzer-v2 Capability Evidence:
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json`
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_suite.json`
- `/home/evgeny/projects/analyzer-v2/src/engines/definitions/assumption_excavation.json`
- `/home/evgeny/projects/analyzer-v2/src/engines/definitions/concept_semantic_field.json`
- `/home/evgeny/projects/analyzer-v2/src/engines/definitions/concept_causal_mechanisms.json`
- `/home/evgeny/projects/analyzer-v2/src/engines/definitions/concept_metaphorical_ground.json`
- `/home/evgeny/projects/analyzer-v2/src/engines/definitions/inferential_commitment_mapper.json`
- `/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/inferential_commitment_mapper.yaml`

## Purpose

Establish the next serious `Close Read` family admission question correctly.

The point of this memo is not to write implementation scope yet.
Its job is to:

- inventory what the old Critic `concept analysis` family actually was
- distinguish that family from a narrower “logic only” framing
- map the old family to the current analyzer-v2 engine / chain inventory
- identify where the present state is already analyzer-v2-backed versus still legacy-only
- define the exact admission questions the next boundary memo must settle

This memo should keep the roadmap from making two mistakes:

1. treating genealogy + AOI as if they already cover the major interpretive families implied by `Close Read`
2. treating “logic” as the next family in isolation when the old product reality was broader and explicitly concept-centered

## Bottom Line

The old Critic product family is best understood as:

- `concept analysis`

not:

- “logical analysis only”

Inside that family, the old product already exposed multiple submodes:

- `inferential`
- `logical`
- `assumption`
- `semantic_field`
- `causal`
- `metaphorical`

So the next serious `Close Read` admission line should be framed as:

- the **concept-analysis family**

with logical and inferential analysis as central submodes inside it.

This family is a strong next candidate because:

- it already existed as a serious product family in Critic
- it already embodied engine-specific follow-up work more strongly than most other old surfaces
- analyzer-v2 already contains substantial concept-analysis capability inventory
- but the migration state is mixed enough that a clean family admission still needs an audit rather than being assumed
- and some of its most important downstream operations still live entirely in the old Critic estate

## Why This Audit Is The Right Next Artifact

The roadmap now has three distinct horizons:

1. the current `Close Read` umbrella with genealogy and AOI family pages
2. the next major family admission line
3. the longer-horizon composition layer for bespoke multi-engine modules

The open question is not:

- whether the current Close Read route exists
- whether the AOI coexistence tranche works
- whether some UI hardening would help

The open question is:

- what the next serious family should be
- what exact family boundary it has
- how much of it already lives in analyzer-v2 versus legacy Critic code

That makes a docs-first **admission audit** the right next move.

## What The Old Product Family Actually Was

The old Critic route structure already makes the family shape visible:

- `/p/:projectId/concept-analysis`
- `/p/:projectId/concept-analysis/:concept/:type`
- `/p/:projectId/concept-analysis/:concept/:type/:tab`

This is defined in:

- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`

The core UI also treats the family as concept-centered, not logic-centered:

- `ConceptsPanel.tsx` defaults to concept-specific navigation and then chooses an `analysisType`
- the available types include:
  - `inferential`
  - `logical`
  - `assumption`
  - `semantic_field`
  - `causal`
  - `metaphorical`

This is visible in:

- `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx`

So the correct roadmap reading is:

- concept analysis is a top-level product family
- logical and inferential analysis are major branches inside it
- they are not the whole family by themselves

## What Functionality The Old Family Already Encoded

The old concept-analysis family was not merely another reading page.
It already encoded a serious example of engine/path-dependent follow-up work.

Across its submodes, it surfaced things like:

- inferential definition and commitment cascades
- incompatibility maps and unresolved tensions
- argument inventories and chain building
- causal architecture
- vulnerability and weak-point analysis
- premise attack lines and downstream scrutiny

That matters strategically because it aligns closely with the original Close Read dictation:

- concept-centered analysis
- logical / inferential follow-up work
- weak-point identification
- further operations based on the shape of the engine output

So if `Close Read` is supposed to become more than a bounded reader, the old concept-analysis family is not optional background.
It is one of the strongest precedents for the kind of engine-specific functionality the app is ultimately supposed to support.

Just as importantly, the old family already had constitutive downstream operations rather than mere read-only tabs.
Those included:

- premise-by-premise scrutiny generation
- quick / deep / both scrutiny modes
- scrutiny job lifecycle and persisted scrutiny results
- corpus-ammunition search and LLM ammunition analysis
- send-to-outline routing and export-oriented downstream handling

So the right strategic reading is not:

- “concept analysis had some interesting displays”

It is:

- concept analysis was already one of the clearest old examples of engine-specific analysis plus engine-specific follow-up work

## Current Migration Reality

The present state is mixed, and more precisely it is a three-way split rather than a simple binary.

### Critic-side reality

The old family currently mixes three execution models.

#### 1. Legacy-local dedicated paths

Inferential analysis still runs through a dedicated local script:

- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py`

That script uses a hardcoded inferential-role prompt modeled on commitment analysis.
It is not yet simply invoking a clean analyzer-v2 family contract.

Logical analysis still runs through a local multi-pass orchestrator:

- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py`

This path is serious and structured, but it is still housed in the old Critic analyzer layer rather than already admitted as a clean Close Read family.
It also matters that this path is more legacy-bridged than fully analyzer-v2-driven.
Its internal phase design uses analyzer-v2-style engine keys, but runtime execution is still owned locally by Critic.

So the right reading is:

- inferential and logical both still belong to the legacy-local execution bucket
- they are not identical paths, but neither is yet a clean analyzer-v2-native Close Read family runtime

#### 2. Old Analyzer / external analyzer bridge for assumption analysis

Assumption analysis is neither purely local legacy nor fully analyzer-v2-backed generic runtime.
It currently runs through:

- `/home/evgeny/projects/the-critic/api/server.py`

via:

- `run_assumption_analysis(...)`

which submits an external analyzer job using:

- `engine="assumption_excavation"`

and records:

- `source: "visualizer_engine"`

So the right reading is:

- assumption analysis is already attached to an analyzer-side engine contract
- but it is still bridged through older external analyzer plumbing rather than already living as a clean analyzer-v2-native family runtime inside Close Read

#### 3. analyzer-v2-backed generic modes

Some concept modes already use analyzer-v2 prompt composition:

- semantic field
- causal
- metaphorical

through:

- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_generic.py`
- `/home/evgeny/projects/the-critic/api/server.py`

More concretely, the current runtime maps them to:

- `concept_semantic_field`
- `concept_causal_mechanisms`
- `concept_metaphorical_ground`

So the concept-analysis family is already partially on the migration path.
It is not a pure greenfield problem.

### analyzer-v2 reality

analyzer-v2 already contains substantial concept-analysis capability material.

But this memo needs to be explicit about one distinction:

- definition existence is not the same thing as runtime use

The presence of chains and engines in analyzer-v2 is evidence of definitional alignment and likely migration direction.
It is not, by itself, proof that Critic or Close Read already uses those definitions as the active runtime path.

#### 1. Full 12-phase chain

There is already a dedicated:

- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json`

This chain includes:

- semantic constellation
- structural landscape
- argument formalization
- chain building
- taxonomy
- causal architecture
- conditional web
- argumentative weight
- vulnerability analysis
- cross-text comparison
- quote retrieval
- synthesis

This is a strong signal that analyzer-v2 already has a serious concept-analysis shape, not just isolated engines.

#### 2. Separate multi-engine concept suite

There is also a looser:

- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_suite.json`

This suggests analyzer-v2 can support both:

- a deep fixed-sequence concept-analysis chain
- and a lighter selective concept suite

That distinction may matter later for:

- default family design
- bespoke module composition

#### 3. Inferential engine and pass structure

The analyzer-v2 side also has:

- `/home/evgeny/projects/analyzer-v2/src/engines/definitions/inferential_commitment_mapper.json`
- `/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/inferential_commitment_mapper.yaml`

This means inferential analysis is not merely a legacy local prompt idea.
There is already a proper analyzer-v2 capability definition with staged depth.

#### 4. Explicit analyzer-v2 concept engines beyond inferential

analyzer-v2 also already names several concept-family engines directly:

- `assumption_excavation`
- `concept_semantic_field`
- `concept_causal_mechanisms`
- `concept_metaphorical_ground`

This matters because the next boundary memo should not speak vaguely about “concept capability inventory.”
It should name which concept submodes already have explicit analyzer-v2 definitions and which still remain runtime-bridged.

#### 5. Strong overlap with the old logical orchestrator

The old Critic logical path already references analyzer-v2-style engine keys in its internal phase design.
For example:

- `concept_argument_formalization`
- `concept_vulnerability_*`

visible in:

- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p03_argument_formalization.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p09_vulnerability_analysis.py`

So the old logical path is not disconnected from analyzer-v2.
It is better understood as:

- a partially migrated / partially shadow-local concept-analysis estate

This is exactly why an admission audit is needed.

## Adjacent Neighbors The Next Boundary Memo Must Classify

The old concept-analysis estate was not isolated to the six submodes alone.
It also sat next to several materially related neighbors:

- `big-picture` inferential analysis
- `cross-concept` / cross-corpus concept analysis
- send-to-outline routing and export-oriented downstream handling

These are visible in:

- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx`

The next boundary memo does not have to admit all of these.
But it does have to classify them explicitly as one of:

- included in the first concept-analysis family cut
- adjacent but not admitted
- deferred for later family expansion

If it does not do that, the concept-family boundary will remain fuzzy.

## What This Audit Must Determine

This memo does not freeze the family boundary yet.
It identifies the exact questions the next boundary memo has to answer.

### 1. Exact family framing

The next memo must confirm:

- concept analysis is the correct family frame

and reject the too-narrow shorthand:

- “just admit logic”

unless code/product evidence genuinely proves that only a small subset is worth admitting.

### 2. Exact first admitted submodes

The next memo must decide which concept-analysis submodes are the first honest `Close Read` cut.

Candidate set from old Critic reality:

- `inferential`
- `logical`
- `assumption`
- `semantic_field`
- `causal`
- `metaphorical`

The likely default hypothesis is:

- first admitted core:
  - `inferential`
  - `logical`
- likely secondary/supporting or later:
  - `assumption`
  - `semantic_field`
  - `causal`
  - `metaphorical`

But this memo does not freeze that yet.
It marks it as the key audit question.

### 3. Exact analyzer-v2 readiness versus legacy dependency

The next memo must say clearly, by submode:

- already analyzer-v2-backed enough for admission
- partially analyzer-v2-backed but still legacy-dependent
- still primarily legacy-only

This is the central migration truth the roadmap needs.
It must also distinguish:

- analyzer-v2 definition existence
- current runtime use in Critic

Those are related, but not interchangeable.

### 4. Exact host/page posture under Close Read

The next memo must decide whether the concept-analysis family under `Close Read` should be:

- one family landing page plus concept detail pages
- one concept-analysis dashboard page under the umbrella
- one thinner admitted subset of the existing `ConceptsPanel`

The point is not to decide UI polish.
The point is to decide the correct product shape for admission.

### 5. Exact family-specific follow-up operations

The next memo must identify which operations are constitutive for concept analysis.

Likely candidates include:

- premise scrutiny / weak-point identification
- vulnerability surfacing
- lines of attack style follow-on work
- corpus-ammunition search
- LLM ammunition analysis
- send-to-outline style downstream routing
- capture-and-route into `Arsenal` / `Research`

That matters because concept analysis is likely the first family where `Close Read` cannot honestly remain just a reading shell.

### 6. Exact deferrals

The next memo must still keep some things out of scope:

- fully generic composition-layer implementation
- standalone `Close Read` host
- complete analyzer-owned follow-up-operation law
- admission of every historical `ConceptsPanel` submode at once

## Working Default Hypotheses

This memo does not freeze final product law, but it does record the most plausible working hypotheses.

### Hypothesis 1

The next serious `Close Read` family is concept analysis.

### Hypothesis 2

The first bounded concept-analysis cut should probably center:

- inferential analysis
- logical analysis

because those are the most structurally aligned with the original Close Read dictation around premise-testing, weak-point identification, and downstream attack surfaces.

### Hypothesis 3

The first concept-analysis family admission will almost certainly require a mixed migration posture:

- reuse some current Critic host/product logic
- while progressively binding more of the family to analyzer-v2 capability contracts

### Hypothesis 4

Concept analysis is likely the first family where `Close Read` must explicitly support more than “bounded reading + capture.”

It will likely require admitted follow-up operations that are stronger and more engine-specific.

### Hypothesis 5

This family should be admitted before the roadmap shifts its center of gravity toward standalone-host work or generic composition-layer implementation.

## What This Memo Does Not Yet Decide

This memo does not decide:

- the final concept-analysis family route structure under `Close Read`
- the exact first admitted submode set
- whether the first host shape is dashboard-first or concept-detail-first
- whether the old `ConceptsPanel` should be wrapped, trimmed, or substantially reinterpreted
- the exact migration strategy from legacy local analyzers to analyzer-v2 family contracts
- whether scrutiny and ammunition are part of the first admitted cut or staged immediately after it
- whether `big-picture`, `cross-concept`, and send-to-outline remain adjacent or partly admitted

Those are the next memo’s decisions.

## Recommended Next Artifact

The next artifact after this audit should be a boundary memo, for example:

- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md`

That memo should freeze:

1. exact admitted concept-analysis submodes
2. exact host/page posture under `Close Read`
3. exact baseline shared law versus family-specific follow-up operations
4. exact analyzer-v2-backed versus legacy-bridged seams
5. exact deferrals

Only after that should the roadmap move into implementation scope for concept analysis inside `Close Read`.

## Final Reading

The right strategic reading now is:

- genealogy and AOI were the right first default families
- they do not exhaust the intended `Close Read` product
- concept analysis is the next serious family line
- it must be audited as a **family**, not reduced to “logic”
- the current state is promising but mixed, and specifically split across legacy-local, external-bridge, and analyzer-v2-backed paths
- the old family already included constitutive follow-up operations like scrutiny and ammunition
- therefore the next honest step is a concept-analysis family admission audit, not UI polishing and not standalone-host planning

That keeps the roadmap aligned with:

- the original Close Read dictation
- the old Critic product reality
- the actual analyzer-v2 capability inventory
