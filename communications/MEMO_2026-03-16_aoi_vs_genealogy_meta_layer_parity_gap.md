# Memo: AOI vs Genealogy Meta-Layer Parity Gap

Date: 2026-03-16

## Purpose

This memo records a specific platform concern:

- genealogy in analyzer-v2 now has a meaningful objective/operationalization/planner layer
- anxiety of influence does not yet have equivalent abstraction depth

The question is not whether AOI exists in analyzer-v2.

It does.

The question is whether AOI currently sits inside analyzer-v2 and analyzer-mgmt with the same level of abstraction, compositional rigor, and metadata-backed execution discipline that genealogy now has.

The answer is:

- no, not yet

This memo is meant to help Codex and Claude critique:

- whether this diagnosis is accurate
- how much of genealogy's current sophistication is actually live execution logic versus metadata/catalog scaffolding
- what the best path is for closing the AOI gap without preserving the wrong legacy abstractions

## What "Anxiety of Influence" Means Here

In this program, anxiety of influence is not a vague "influence study."

It is a bounded analytical task:

- identify which authors a subject author cites, invokes, or appears to rely on
- reconstruct what those cited authors actually argue
- compare the subject author's usage against those arguments and texts
- identify where the subject is faithful, selective, distorting, appropriating, omitting, or strategically reinterpreting
- surface those deviations with evidence and a clear account of how the interpretation departs from the source

That is the capability family whose abstraction level is being evaluated here.

## Executive Finding

Genealogy has a significantly more developed analyzer-v2 meta-layer than AOI.

That is true in three distinct senses:

1. genealogy has a real objective layer
2. genealogy has a real operationalization layer for many of its key engines
3. genealogy is much more tightly wired from The Critic into analyzer-v2 workflow, orchestration, presenter, and analyzer-mgmt inspection

AOI, by contrast, is split across two different states:

1. a newer analyzer-v2-native thematic AOI slice
2. an older bespoke The Critic influence stack that still carries much of the actual AOI app behavior

So the platform story is asymmetric:

- genealogy is increasingly analyzer-v2-native in both metadata and execution
- AOI is only analyzer-v2-native in a bounded thematic slice, not across the live Critic AOI experience

## Main Audit Findings

### 1. Genealogy's analyzer-mgmt sophistication is not fake

The kinds of screens visible in analyzer-mgmt:

- objectives
- operationalizations
- capability/depth/dimensions tabs
- pipeline visualization

are not just decorative for genealogy.

A meaningful part of that layer is genuinely connected to execution.

Evidence:

- genealogy has a real objective definition in [genealogical.json](/home/evgeny/projects/analyzer-v2/src/objectives/definitions/genealogical.json)
- analyzer-v2 has a real objective registry in [registry.py](/home/evgeny/projects/analyzer-v2/src/objectives/registry.py)
- adaptive planning actually consumes objectives in [orchestrator.py](/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py)
- genealogy has real operationalization files such as:
  - [concept_appropriation_tracker.yaml](/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/concept_appropriation_tracker.yaml)
  - [genealogy_relationship_classification.yaml](/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/genealogy_relationship_classification.yaml)
- operationalizations are actually used by the capability composer in [capability_composer.py](/home/evgeny/projects/analyzer-v2/src/stages/capability_composer.py)
- pipeline visualization is assembled from workflows, chains, engines, operationalizations, and stances in [visualization.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/visualization.py)
- the genealogy workflow itself explicitly composes chains and engines in [intellectual_genealogy.json](/home/evgeny/projects/analyzer-v2/src/workflows/definitions/intellectual_genealogy.json)

So for genealogy, there is a real stack:

- objective
- workflow
- chains
- engines
- stance operationalizations
- depth sequences
- planner hints
- presenter/view surfaces

That sophistication is uneven, but it is real.

### 2. Even for genealogy, the sophistication is partial rather than universal

The genealogy side should not be romanticized.

The meta-layer is real, but still incomplete.

Examples:

- analyzer-v2 currently has only two objective definitions:
  - [genealogical.json](/home/evgeny/projects/analyzer-v2/src/objectives/definitions/genealogical.json)
  - [logical.json](/home/evgeny/projects/analyzer-v2/src/objectives/definitions/logical.json)
- only a bounded subset of engines has operationalization files in [src/operationalizations/definitions](/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions)
- much of analyzer-mgmt remains a registry/catalog browser over definitions, not a guarantee that every runtime surface is fully governed by those abstractions

So the strongest accurate statement is:

- genealogy has a meaningful analyzer-v2 meta-layer
- but that meta-layer is not yet the total law of the platform

### 3. AOI does exist in analyzer-v2, but it does not have equivalent meta-layer depth

AOI is not absent from analyzer-v2.

There are at least two real AOI workflow tracks:

- the older 5-pass workflow in [anxiety_of_influence.json](/home/evgeny/projects/analyzer-v2/src/workflows/definitions/anxiety_of_influence.json)
- the newer bounded thematic workflow in [anxiety_of_influence_thematic_single_thinker.json](/home/evgeny/projects/analyzer-v2/src/workflows/definitions/anxiety_of_influence_thematic_single_thinker.json)

The bounded thematic workflow does have a real presenter/view surface:

- [aoi_thematic_analysis.json](/home/evgeny/projects/analyzer-v2/src/views/definitions/aoi_thematic_analysis.json)
- [aoi_source_documents.json](/home/evgeny/projects/analyzer-v2/src/views/definitions/aoi_source_documents.json)
- [aoi_by_theme.json](/home/evgeny/projects/analyzer-v2/src/views/definitions/aoi_by_theme.json)
- [aoi_by_sin_type.json](/home/evgeny/projects/analyzer-v2/src/views/definitions/aoi_by_sin_type.json)
- [aoi_thematic_report.json](/home/evgeny/projects/analyzer-v2/src/views/definitions/aoi_thematic_report.json)

But compared to genealogy, AOI is missing a major layer of abstraction:

- no AOI objective definition in [src/objectives/definitions](/home/evgeny/projects/analyzer-v2/src/objectives/definitions)
- no AOI operationalization files in [src/operationalizations/definitions](/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions)
- no AOI presence in the operationalization-backed engine coverage layer surfaced by analyzer-mgmt
- no comparable AOI planner-governed objective story

So AOI has:

- workflows
- engines
- views
- some style/view activation work

But it does not yet have:

- a mature meta-layer equivalent to genealogy's objective plus operationalization system

### 4. The Critic makes the asymmetry even more obvious

Genealogy in The Critic is now much more analyzer-v2-native.

Evidence:

- genealogy execution can delegate to analyzer-v2 in [server.py](/home/evgeny/projects/the-critic/api/server.py)
- the genealogy frontend can set `objective_key = "genealogical"` in [GenealogyPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx)
- genealogy stores and consumes analyzer-v2 `PagePresentation` through the presenter path in:
  - [GenealogyPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx)
  - [V2TabContent.tsx](/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx)

AOI in The Critic is still much more bespoke.

Evidence:

- the live AOI frontend is still [AnxietyOfInfluencePage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePage.tsx)
- it is wired to custom `/api/influence/*` endpoints in [server.py](/home/evgeny/projects/the-critic/api/server.py)
- its execution still depends on the local bespoke analyzer in [analyze_influence.py](/home/evgeny/projects/the-critic/analyzer/analyze_influence.py)

So even if analyzer-v2 now contains a bounded AOI thematic slice, the live The Critic AOI app still does not inherit genealogy's level of analyzer-v2-native abstraction.

### 5. The older AOI workflow and the newer AOI thematic slice are conceptually split

This is probably the most important architectural issue.

There are effectively two AOI stories:

1. legacy 5-pass AOI:
   - thinker identification
   - hypothesis generation
   - textual sampling
   - deep engagement
   - synthesis report

2. newer bounded thematic AOI:
   - source thematic synthesis
   - engagement mapping
   - sin findings
   - thematic report

These are not just two views on the same pipeline.

They reflect different abstractions:

- the old one is closer to an app-shaped workflow copied from legacy Critic AOI habits
- the new one is closer to an analyzer-v2-native semantic surface with explicit presenter views

Right now, genealogy feels like one maturing analyzer-v2-native architecture.

AOI feels like:

- a legacy stack
- plus a newer bounded analyzer-v2-native tranche

That split is one major reason parity has not been reached.

## Working Diagnosis

The problem is not simply:

- "AOI needs more views"

The deeper problem is:

- genealogy already has a partially real analyzer-v2 meta-layer
- AOI has not yet been raised to the same level of objective/operationalization/planner discipline

So AOI today is more like:

- workflow and view capability without full meta-layer integration

while genealogy is more like:

- workflow, view, and meta-layer capability partially aligned

## Hypotheses About the Best Closure Path

### Hypothesis 1: Do not treat the old bespoke AOI flow as the long-term canonical abstraction

The legacy 5-pass AOI flow in The Critic may still be useful.

But it is a poor candidate for the canonical analyzer-v2 abstraction if taken over wholesale.

Why:

- it is strongly shaped by old app UX and old API boundaries
- it is still deeply entangled with bespoke Critic state and custom endpoints
- carrying that whole shape forward risks preserving the wrong abstraction boundary

Best implication:

- do not define parity as "port the old bespoke AOI app exactly into analyzer-v2"

### Hypothesis 2: Canonicalize the bounded thematic AOI slice first

The newer thematic AOI workflow is probably the right base abstraction.

Why:

- it already has a clearer analyzer-v2-native workflow
- it already has a presenter-native view family
- it is more bounded and composable
- it is easier to give objective, operationalization, and planner structure to a stable bounded slice than to a sprawling legacy app workflow

Best implication:

- treat `anxiety_of_influence_thematic_single_thinker` as the first-class AOI canonical surface
- make it the anchor for analyzer-v2-native AOI abstraction

### Hypothesis 3: AOI needs its own objective layer before it can reach genealogy parity

If genealogy can trigger adaptive planning through a concrete objective like `genealogical`, AOI likely needs the same.

Possible AOI objective families:

- `influence_fidelity`
- `influence_thematic`
- `source_engagement_audit`

At minimum, an AOI objective should define:

- primary goals
- quality criteria
- preferred engine functions/categories
- planner strategy
- expected deliverables
- baseline workflow
- preferred views

Without that, AOI remains harder to reason about as a first-class analysis family.

### Hypothesis 4: AOI needs an operationalization layer for its key engines

Genealogy gained real depth by making stances engine-specific.

AOI likely needs the same for engines like:

- `aoi_thematic_synthesis`
- `aoi_engagement_mapping`
- `aoi_sin_findings`
- `aoi_thematic_report`

Likely benefits:

- explicit stance progressions per depth
- better planner visibility into what deep versus standard AOI actually means
- stronger analyzer-mgmt introspection
- cleaner pipeline visualization and execution previews

Without this, AOI remains a workflow with engines, but not a mature operationalized family.

### Hypothesis 5: The old 5-pass AOI flow may need to be reframed as intake/discovery, not the full final architecture

The legacy 5-pass flow still captures useful tasks:

- thinker discovery
- reference text collection
- early hypothesis generation

Those may still matter.

But they may belong upstream of the canonical thematic AOI surface rather than as the canonical AOI architecture itself.

Possible reframing:

- legacy AOI discovery/intake stage finds or curates source thinkers and source texts
- canonical thematic AOI performs the actual analyzer-v2-native bounded interpretation audit

If this is right, then the future architecture is not:

- old AOI versus new AOI

It is:

- discovery/intake AOI
- then canonical thematic AOI analysis

## Practical Gaps to Close

If the goal is genealogy-level parity, the main AOI gaps are:

1. Add at least one real AOI objective definition.
2. Add operationalization files for the key AOI thematic engines.
3. Make AOI visible in analyzer-mgmt not just as workflows/views, but as objective/operationalization-bearing analytical capability.
4. Decide whether the old 5-pass AOI flow is:
   - legacy
   - intake/discovery
   - or something to be fully reauthored into analyzer-v2-native form
5. Move The Critic AOI app closer to the analyzer-v2 presenter/runtime path rather than leaving it on the bespoke `/api/influence/*` island.

## Recommended Near-Term Program

The most disciplined next tranche would probably be:

### Direction A: Make AOI meta-layer real

- create one AOI objective definition
- create operationalization files for the four thematic AOI engines
- expose that layer in analyzer-mgmt the same way genealogy operationalizations are exposed

### Direction B: Canonicalize thematic AOI as the analyzer-v2-native AOI surface

- treat the thematic single-thinker flow as the canonical AOI presentation surface
- continue improving its presenter/view quality
- avoid duplicating effort into bespoke AOI rendering paths

### Direction C: Decide the fate of the legacy 5-pass AOI flow

Three plausible choices:

1. retire it gradually
2. preserve it as discovery/intake only
3. fully re-author it into analyzer-v2-native orchestration/presenter terms

My current bias is:

- option 2 is probably best unless there is a very strong reason to preserve the full legacy shape

## Review Questions

These are the questions I would want Codex and Claude to attack:

1. Is the diagnosis right that genealogy's analyzer-mgmt sophistication is partially real execution logic, not just catalog decoration?
2. Is the strongest AOI gap really the absence of objective + operationalization layers, or is the deeper problem still The Critic's bespoke AOI runtime?
3. Should the canonical AOI abstraction be the newer thematic slice, or should the older 5-pass flow be reauthored as the main analyzer-v2 AOI architecture?
4. If the old 5-pass AOI survives, should it become an intake/discovery workflow feeding thematic AOI rather than remaining the main AOI experience?
5. What is the minimum set of AOI objective and operationalization artifacts needed to make analyzer-mgmt sophistication for AOI comparable to genealogy?
6. What would count as real evidence that AOI has reached genealogy-level parity:
   - objective-defined
   - operationalization-backed
   - planner-aware
   - presenter-native
   - thin-consumer proven

## Bottom Line

Genealogy has something AOI still lacks:

- a partially real analyzer-v2 meta-layer that connects objective, workflow, engine, operationalization, planner, presenter, and management UI

AOI is not absent from analyzer-v2.

But AOI is still behind genealogy in exactly that higher-order abstraction layer.

So if the goal is a future mixed AOI + genealogy app that feels equally platform-native, the missing work is not just prettier AOI views.

It is:

- giving AOI the same kind of analyzer-v2 meta-architecture that genealogy has already begun to acquire
