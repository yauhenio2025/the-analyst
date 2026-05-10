# Memo: Close Read Concept-Analysis analyzer-v2 Runtime Authority And analyzer-mgmt Visibility Scope

Subtitle: Make analyzer-v2 the canonical runtime and translated-artifact authority for `Close Read` concept analysis, and make the relevant composition assets first-class visible/editable objects in analyzer-mgmt

Date: 2026-04-06
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
- `communications/MEMO_2026-03-26_analyzer_v2_as_brain_direction_audit.md`
Close Read Direction Context:
- `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
Current Close Read Product Boundary:
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md`
Immediate Runtime Predecessors:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md`
- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_recomposition_scope.md`
Primary Live Deployed Evidence Checked On 2026-04-06:
- `https://analyzer-v2.onrender.com/v1/meta/definitions-version`
- `https://analyzer-v2.onrender.com/v1/engines`
- `https://analyzer-v2.onrender.com/v1/chains`
- `https://analyzer-v2.onrender.com/v1/operationalizations`
- `https://analyzer-v2.onrender.com/v1/workflows`
- `https://analyzer-v2.onrender.com/v1/transformations`
- `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref`
- `https://analyzer-mgmt-frontend.onrender.com/engines/inferential_commitment_mapper`
- `https://analyzer-mgmt-frontend.onrender.com/chains/concept_analysis_12_phase`
- `https://analyzer-mgmt-frontend.onrender.com/operationalizations/inferential_commitment_mapper`
- `https://analyzer-mgmt-frontend.onrender.com/workflows`
- `https://analyzer-mgmt-frontend.onrender.com/implementations`
- `https://analyzer-mgmt-frontend.onrender.com/transformations`
Primary Local Implementation Evidence:
- `/home/evgeny/projects/analyzer-v2/src/engines/definitions/inferential_commitment_mapper.json`
- `/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/inferential_commitment_mapper.yaml`
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json`
- `/home/evgeny/projects/analyzer-v2/src/workflows/definitions/`
- `/home/evgeny/projects/analyzer-v2/src/transformations/definitions/`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/engines/[key].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/workflows/[key].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/implementations/index.tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/implementations/[key].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/transformations/[key].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/jobs/[id].tsx`

## Purpose

Freeze the next serious tranche after the analyzer-v2 recomposition work:

- deploy concept-analysis runtime authority into analyzer-v2 as the live server truth
- make the concept-analysis composition assets first-class visible/editable objects in analyzer-mgmt on Render
- reduce Critic from contract-owning recomposition layer to thin client for launch, polling, retrieval, and rendering

This memo is not about inventing new concept-analysis capability categories.

It is about taking the capability types we already have:

- engines
- operationalizations / passes / stances / depths
- chains
- workflows
- transformations

and making them the actual deployed authority for the `Close Read` concept family.

## Bottom Line

The live deployed Render state already proves the key strategic point:

- analyzer-v2 already has the relevant inferential and concept-analysis capability primitives
- analyzer-mgmt already has the right management surface categories for engines, chains, operationalizations, workflows, and transformations
- what is missing is not a new substrate type
- what is missing is live runtime authority and live visibility for the concept-analysis composition layer

So the next serious move is:

1. deploy concept workflows to analyzer-v2
2. deploy concept host-contract transformations to analyzer-v2
3. expose them in analyzer-mgmt as first-class editable assets
4. then strip Critic back to a thin client

That is the honest route to:

- analyzer-v2 as the brain
- analyzer-mgmt as the operator/editor console
- Critic / future `Close Read` as the host

## What The Live Render Stack Already Proves

### 1. The capability bricks are already deployed

On Render, analyzer-v2 already exposes:

- `inferential_commitment_mapper` in `/v1/engines`
- `inferential_commitment_mapper` in `/v1/operationalizations`
- `concept_analysis_12_phase` in `/v1/chains`
- the component concept engines used by that chain in `/v1/engines`

So the live deployed server already supports the core claim:

- inferential does not need to be invented
- logical/concept deep analysis does not need to be invented
- the problem is composition, launch surface, transformation, and contract authority

### 2. analyzer-mgmt has the right surface categories, but not yet reliable concept visibility

On Render, analyzer-mgmt already serves working pages for:

- engines
- chains
- operationalizations
- workflows
- implementations
- transformations

And the specific concept-relevant pages already load for:

- `/engines/inferential_commitment_mapper`
- `/chains/concept_analysis_12_phase`
- `/operationalizations/inferential_commitment_mapper`

But the review-backed correction is important:

- analyzer-mgmt is directionally the right console
- it is **not yet** concrete enough to be called the canonical operator surface without repair

On the live Render stack as checked in this tranche, concept visibility is still inconsistent:

- existing concept assets can exist in analyzer-v2 while failing to render in analyzer-mgmt
- chain-backed workflow visibility is not yet explicit enough
- workflow-to-transformation linkage is not yet explicit enough

So we do not need a new admin application or a new type system for this tranche.
But we **do** need an analyzer-mgmt visibility-repair subphase before analyzer-mgmt can honestly be called the canonical operator console for concept runtime.

### 3. The missing layer is visible and specific

On Render today:

- `/v1/workflows` contains no concept-analysis workflow for the `Close Read` concept family
- `/v1/transformations` contains no concept host-contract extraction templates
- `/v1/orchestrator/concept-analysis-by-ref` returns `404`

So the missing layer is not abstract.
It is exactly:

- workflow wrappers
- host-contract transformations
- bounded orchestrator launch seam
- deployed visibility for those assets

## Strategic Reading

The previous recomposition scope was right, but incomplete as a deployment strategy.

It correctly identified that the next move was:

- analyzer-v2 recomposition rather than capability invention

But the stricter roadmap requirement is not merely:

- local rebased code exists

It is:

- analyzer-v2 on Render is the actual runtime authority
- analyzer-mgmt on Render is the visible/editable authority surface
- Critic is no longer silently carrying contract materialization and runtime semantics locally

So this tranche is the operational completion of the recomposition story.

## Scope Summary

Implement one bounded authority-and-visibility tranche.

This tranche should:

- deploy bounded concept-analysis workflows into analyzer-v2
- deploy bounded concept host-contract transformations into analyzer-v2
- repair analyzer-mgmt visibility for existing concept assets before relying on it as the canonical operator console
- expose those workflows and transformations in analyzer-mgmt as first-class edit/view objects
- make analyzer-v2 responsible for producing and serving translated host-contract artifacts
- reduce Critic to a thin consumer of those artifacts

This tranche should not:

- introduce any new analyzer-v2 substrate types beyond engines, operationalizations, chains, workflows, and transformations
- widen the `Close Read` product boundary
- add new concept submodes
- redesign the native Critic or `Close Read` concept UI
- open the broader generic module-composition project across all families
- introduce a separate `Close Read admin` surface outside analyzer-mgmt

## Key Decisions To Freeze

### 1. No new substrate types

Do not solve this by inventing a new concept-runtime abstraction outside the existing analyzer-v2 vocabulary.

Stay inside:

- engines
- operationalizations
- chains
- workflows
- transformations

If more expressiveness is needed, use those types more deliberately.

### 2. analyzer-v2 becomes the runtime authority

For the admitted concept submodes:

- `inferential`
- `logical`

analyzer-v2 should own:

- execution
- composition
- host-contract extraction
- provenance
- translated artifact persistence or retrievability

Critic should stop owning those as the canonical runtime truth.

### 3. Inferential should be owned through engine + operationalization + workflow + transformation

The inferential stack should be represented in analyzer-v2 as:

- engine:
  - `inferential_commitment_mapper`
- operationalization:
  - existing stance/depth structure
- workflow:
  - bounded single-concept by-ref inferential run
- transformation:
  - inferential host-contract extraction into the current 7-section host shape

This makes inferential visible and editable across the correct analyzer-v2 layers instead of hiding the composition inside Critic.

### 4. Logical should be owned through chain + workflow + transformation

The logical stack should be represented in analyzer-v2 as:

- chain:
  - `concept_analysis_12_phase`
- workflow:
  - bounded single-concept by-ref logical run
- transformation:
  - logical host-contract extraction into the full current `LogicalAnalysis` contract

This is the right way to keep logical composition legible in analyzer-mgmt without collapsing it into one fake mega-engine.

### 5. The translation layer belongs in analyzer-v2

The host-contract extraction step should be a first-class analyzer-v2 transformation, not a hidden Critic-local adapter.

That means:

- raw analyzer outputs remain analyzer-owned artifacts
- translated host-contract outputs also become analyzer-owned artifacts
- Critic fetches the translated artifact rather than materializing it locally

### 6. analyzer-mgmt should be the canonical visibility/editability console

After deploy, the concept-analysis runtime should be inspectable in analyzer-mgmt through the existing surfaces:

- engines
- operationalizations
- chains
- workflows / implementations
- transformations

For this tranche, concept assets should become first-class there, not buried as incidental backend objects.

At minimum the live Render analyzer-mgmt should expose:

- the inferential engine page
- the inferential operationalization page
- the concept-analysis chain page
- the new concept inferential workflow page
- the new concept logical workflow page
- the new inferential host-contract transformation page
- the new logical host-contract transformation page

And the correction from review should be frozen explicitly:

- the canonical composition view must be concrete, not rhetorical
- if `workflows/[key]` is not chain-aware enough for chain-backed concept workflows, then `implementations/[key]` must be the canonical composition page for this tranche
- workflow detail or implementation detail must show explicit workflow-to-transformation linkage
- existing concept assets already live in analyzer-v2 must render correctly in analyzer-mgmt before new concept workflows/templates are treated as operationally visible

### 7. Critic becomes a thin client

After this tranche, Critic should be reduced to:

- document sync initiation if still required by host integration
- launch request
- polling / status retrieval
- translated artifact retrieval
- rendering
- bounded host-local scrutiny UI where still admitted

Critic should no longer be the place where concept-analysis meaning is reconstructed or normalized into host contracts.

### 8. Scrutiny stays narrow, but must operate on analyzer-owned translated logical output

This tranche does not widen scrutiny into:

- ammunition
- corpus exploration
- send-to-outline
- broader attack workflows

But it does require one strict architectural truth:

- admitted logical scrutiny must read the translated analyzer-v2-backed logical contract, not any old Critic-local logical runtime path

## Implementation Sequence

### Phase A: Deploy the missing analyzer-v2 runtime layer

### Phase A.0: Land the local-only analyzer-v2 assets in git and deploy them

Before any Render authority claim can be made:

- commit the local-only concept runtime files
- push them
- deploy analyzer-v2 from committed code

This correction is mandatory because local file existence is not equivalent to deployed authority.
As of this memo review cycle, the relevant concept runtime files were still not all landed in live Render.

Deploy to Render:

- concept inferential workflow
- concept logical workflow
- concept inferential host-contract transformation
- concept logical host-contract transformation
- bounded by-ref orchestrator seam for concept runs

Success condition:

- those assets are visible through live analyzer-v2 endpoints, not just local code

### Phase A.5: Repair analyzer-mgmt visibility for concept assets already live in analyzer-v2

Before Phase B can honestly succeed, analyzer-mgmt must correctly render concept assets that already exist on the live analyzer-v2 API.

Required repair targets:

- existing concept-capability engine pages
- existing concept chain pages
- transformations list/detail visibility
- chain-backed workflow visibility

Required visibility corrections:

- chain-backed concept workflows must have a concrete readable composition page
- workflow-to-transformation linkage must be explicit
- existing concept assets already present in the analyzer-v2 API must no longer fail or disappear in analyzer-mgmt

### Phase B: Make the new concept assets first-class in analyzer-mgmt

Use existing analyzer-mgmt surfaces, not new types.

Required visibility:

- workflows/implementations list shows the new concept workflows
- workflow or implementation detail page exposes the underlying engine/chain composition
- transformations list/detail shows the new host-contract extraction templates
- cross-links make it obvious how inferential/logical concept runs are composed

Recommended bounded augmentation:

- surface workflow-to-transformation linkage more explicitly on workflow detail pages
- surface workflow-to-transformation linkage more explicitly on implementation or workflow detail pages
- ensure concept runs can be inspected through existing job/result-boundary pages once run ids exist

### Phase C: Shift translation authority out of Critic

Make analyzer-v2 the producer of:

- raw concept-analysis outputs
- translated host-contract artifacts

Then change Critic to:

- fetch those translated artifacts
- persist only local host read models if still operationally necessary
- stop materializing semantic contracts as the authority layer

### Phase D: Thin the Critic client

After analyzer-v2 serves the translated artifact truth:

- remove or sharply reduce Critic-local recomposition code
- keep only thin launch/retrieval/render seams
- keep the current host shells stable

This phase must stay explicitly bounded to the two admitted concept submodes:

- `inferential`
- `logical`

And it must explicitly defer:

- cross-corpus concept analysis
- legacy concept cache retirement beyond the admitted submode seams
- broader concept-estate cleanup outside the admitted `Close Read` family path

## analyzer-mgmt Visibility Law

The point is not merely that the assets should exist in analyzer-v2.
They must also be visible and editable in analyzer-mgmt in a way that matches the real composition logic.

For inferential, a human operator should be able to inspect:

- engine definition
- operationalization / stance-depth design
- workflow wrapper
- host-contract transformation

For logical, a human operator should be able to inspect:

- chain definition
- constituent engine lineup
- workflow wrapper
- host-contract transformation

This satisfies the user requirement that the system remain legible in terms of:

- engines
- passes / stances / depths
- chains
- transformations

rather than disappearing behind host-local glue code.

## Public Interfaces / Non-Changes

Do not change:

- current `Close Read` concept routes
- current native Critic concept routes
- current admitted submodes:
  - `inferential`
  - `logical`

Do not expose raw analyzer-v2-native concept schemas directly to the frontend in this tranche.

Do not create a new admin app for concept runtime management.

Do not widen this into the broader composition-layer project across all families.

## Acceptance Criteria

### Live analyzer-v2 authority

On Render:

- `/v1/workflows` includes the new concept workflows
- `/v1/transformations` includes the new concept host-contract extraction templates
- the bounded concept by-ref orchestrator route exists and responds as a live endpoint
- inferential and logical concept runs can be launched through analyzer-v2 as the authority runtime

### Live analyzer-mgmt visibility

On Render:

- existing concept assets already live in analyzer-v2 render correctly in analyzer-mgmt
- the new concept workflows are visible on workflows/implementations pages
- the new concept transformations are visible on transformations pages
- the underlying inferential engine page and logical chain page remain the canonical edit/inspection anchors
- workflow-to-transformation linkage is explicit
- chain-backed workflow composition is readable through a concrete canonical page
- a human can inspect the composition without reading Critic code

### Thin-host truth

In Critic:

- concept runs no longer depend on Critic-local semantic translation as the authority layer
- Critic renders analyzer-produced translated artifacts
- logical scrutiny reads translated logical output only
- this thinning claim applies only to the admitted `inferential` and `logical` seams in this tranche

## Risks And Hard Stops

### 1. Do not fake analyzer-v2 authority

If the Render analyzer still lacks:

- the workflows
- the transformations
- the orchestrator seam

then the tranche is not done, even if local code exists.

### 2. Do not hide composition logic in host glue

If the composition remains understandable only by reading Critic code, the analyzer-mgmt visibility goal has failed.

### 3. Do not solve this by inventing a new type

If the proposed fix requires a new top-level analyzer construct rather than better use of:

- engines
- operationalizations
- chains
- workflows
- transformations

the tranche has drifted.

## Decision

The next concrete phase should be frozen as:

`Close Read concept-analysis analyzer-v2 runtime authority + analyzer-mgmt visibility`

That is the right next move because it converts a correct local architectural direction into:

- live deployed analyzer authority
- live operator visibility
- thinner host semantics

without reopening product boundaries or drifting into premature genericity.
