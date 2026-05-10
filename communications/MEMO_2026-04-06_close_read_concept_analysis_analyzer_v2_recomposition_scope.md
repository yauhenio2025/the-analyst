# Memo: Close Read Concept-Analysis analyzer-v2 Recomposition Scope

Subtitle: Rebase the shipped `Close Read` concept family onto analyzer-v2's existing inferential engine and concept-analysis chain rather than continuing to treat Critic-local analyzers as the canonical runtime

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
Close Read Direction Context:
- `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
Current Close Read Product Boundary:
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md`
Immediate Runtime Predecessor:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md`
Primary Critic Runtime Evidence:
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phase_base.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx`
Primary analyzer-v2 Capability Evidence:
- `/home/evgeny/projects/analyzer-v2/src/engines/definitions/inferential_commitment_mapper.json`
- `/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/inferential_commitment_mapper.yaml`
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json`
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_suite.json`

## Purpose

Write the next scoping memo after the fresh-project runtime tranche.

This memo should freeze the next serious architectural move for the `Close Read` concept family:

- stop treating the Critic-local inferential and logical analyzers as the intended long-term execution owner
- rebase execution onto analyzer-v2's already-existing inferential engine and concept-analysis chain
- define the parity, adapter, and contract work needed to make that shift without reopening the `Close Read` product boundary

This is not a memo about inventing inferential/logical capability from scratch.
It is a memo about recomposition and runtime ownership.

## Bottom Line

The right next architectural phase is not:

- more `Close Read` concept UI work
- more local prompt genericization inside Critic as if that were the destination
- a standalone `Close Read` app move
- a generic composition-layer project across all families at once

The right next phase is:

- keep the shipped `Close Read` concept family host surfaces in place
- treat analyzer-v2's inferential engine and concept-analysis chain as the canonical capability definitions
- shift execution ownership from Critic-local analyzers toward analyzer-v2 composition
- define the bounded adapter/parity work required so existing Critic native concept views and `Close Read` concept views continue to render

So the scoping question is no longer:

- "how do we make the old Critic concept analyzers less hardcoded?"

It is:

- "how do we rebind the existing concept-analysis family to analyzer-v2's capability layer without breaking the current host surfaces?"

## What Changes In The Strategic Reading

The earlier fresh-project runtime tranche was still necessary.
It proved two important things:

1. the new `Close Read` concept family host routes and shells are real
2. the immediate blocker on fresh uploaded projects was runtime truth and persistence, not UI

But that tranche was still transitional.
It kept the Critic-local inferential and logical analyzers as the execution owner.

That is not the correct long-horizon state if the roadmap is serious about:

- `analyzer-v2 as the brain`
- `Close Read` as a presentation/composition layer
- default families that later become ingredients in broader bespoke compositions

So the next phase has to shift the conceptual center of gravity:

- from "make old Critic analyzers work on fresh projects"
- to "make analyzer-v2 definitions/chains/passes the canonical execution path for this family"

## What analyzer-v2 Already Has

The key correction is factual:
analyzer-v2 already contains the major concept-analysis capability building blocks.

For inferential analysis:

- engine definition:
  - `/home/evgeny/projects/analyzer-v2/src/engines/definitions/inferential_commitment_mapper.json`
- operationalization/pass structure:
  - `/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/inferential_commitment_mapper.yaml`

For deeper logical/concept analysis:

- twelve-phase chain:
  - `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json`
- suite-level concept grouping:
  - `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_suite.json`

So the next phase should not be framed as:

- "port inferential and logical into analyzer-v2"

That overstates the missing work.

It should be framed as:

- recompose Critic/Close Read execution around analyzer-v2's existing capability definitions
- then adapt output and rendering contracts where necessary

Important nuance:

- `inferential` maps relatively directly to an engine + operationalization at the capability-definition level
- `logical` is not one simple engine swap; it is a chain-level recomposition problem centered on the analyzer-v2 concept-analysis chain

Important correction:

- this does **not** mean inferential is a drop-in runtime swap
- the current Critic inferential host contract is section/UI-shaped:
  - `synthesis`
  - `the_deceptively_simple`
  - `commitment_cascade`
  - `incompatibility_map`
  - `tensions`
  - `practical_stakes`
  - `commitment_packages`
- the visible analyzer-v2 inferential schema is graph/schema-shaped:
  - `key_ideas`
  - `what_youre_signing_up_for`
  - `what_backs_this_up`
  - `either_or_choices`
  - `real_world_implications`
  - and many other canonical sections

So the inferential rebasing problem is still narrower than net-new capability invention, but it is not a field-renaming exercise.
It is a structural translation problem.

## What Critic Still Owns Locally

The reason this needs a dedicated scope memo is that the runtime ownership is still materially local.

Today Critic still owns:

- inferential prompt/runtime:
  - `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py`
- logical orchestration:
  - `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py`
- phase-local machinery and models:
  - `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phase_base.py`
  - `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/`

Important nuance:

- the logical path is not wholly untouched by analyzer-v2 already
- `phase_base.py` already fetches analyzer-v2 prompt templates when available and falls back to hardcoded prompts otherwise

So the remaining logical rebasing work is not primarily:

- prompt integration

It is primarily:

- execution ownership shift
- chain/runtime ownership shift
- result-contract parity and translation

So even after fresh-project runtime truth improves, the concept family still does not yet satisfy the stricter architectural goal:

- capability ownership in analyzer-v2
- thin host surfaces in Critic/Close Read

## Scope Summary

Implement a bounded recomposition tranche for the existing `Close Read` concept family.

This tranche should:

- keep the current `Close Read` concept routes and host shell unchanged
- keep the native Critic concept-analysis routes live
- treat analyzer-v2 inferential and concept-chain definitions as canonical capability sources
- define and implement the minimal execution adapter layer needed so Critic can call analyzer-v2-owned inferential/logical capability paths
- preserve or deliberately translate result contracts so current `Close Read` and native concept views continue to render
- leave broader module-composition work, UI redesign, and standalone-host work deferred

This tranche should not:

- reopen the concept-family product boundary
- admit new concept submodes
- widen `Close Read` concept UI
- try to solve the whole generic composition layer at once
- require every concept-analysis surface to be redesigned around new schemas before anything can ship

## Key Decisions To Freeze

### 1. The next slice is recomposition, not capability invention

Do not scope the next phase as if inferential/logical are missing from analyzer-v2.

Scope it as:

- capability rebinding
- execution ownership shift
- adapter/parity work

### 2. Keep the current host contract fixed

Do not change:

- `/p/:projectId/close-read/concepts`
- `/p/:projectId/close-read/concepts/:conceptSlug`
- current native `/concept-analysis` routes
- current admitted concept submodes under `Close Read`:
  - `inferential`
  - `logical`

The host contract is not the problem in this tranche.

### 3. Treat analyzer-v2 definitions as canonical, not merely inspirational

For this family, analyzer-v2 should stop being treated as a parallel reference implementation.

The scope should freeze:

- inferential engine definition + operationalization are the canonical inferential capability description
- concept-analysis 12-phase chain is the canonical deep concept/logical capability description

Critic-local prompt text and phase logic should be treated as transitional runtime residue to be reduced or wrapped, not as the authoritative future state.

### 4. Separate the inferential and logical rebasing problems

Do not pretend these are one identical migration.

Inferential path:

- closer to an engine/operationalization rebinding problem than the logical path
- but still requires a structural adapter because the current Critic inferential contract and the analyzer-v2 canonical inferential schema are materially different
- also requires one explicit execution-model decision:
  - full multi-pass analyzer-v2 operationalization
  - bounded subset/depth of that operationalization
  - or staged adoption from a shallower v2 depth toward the full sequence

Logical path:

- chain-level recomposition problem
- may still require a bounded adapter layer because the old Critic host expects results shaped by the legacy 12-phase runtime
- is already partly analyzer-v2-backed at the prompt-template layer, so the remaining problem is execution/runtime ownership rather than initial prompt-wiring

The scope should therefore keep separate workstreams for:

- inferential execution rebinding
- logical/chain execution rebinding

### 5. Preserve current host rendering where feasible, adapt only where necessary

The first goal is not a new concept UI.
The first goal is that current host surfaces remain usable while execution ownership moves.

So the scope should freeze this order:

1. determine capability/output overlap between Critic-local results and analyzer-v2 results
2. define the adapter or translated result contract
3. swap execution owner
4. only then decide whether host rendering should be further redesigned

### 6. This is still narrower than composition-layer work

The broader vision still includes:

- bespoke sequential modules
- engine-to-engine compositions
- family-crossing modules

But this tranche should not solve that general problem yet.

It should stay bounded to one family:

- concept analysis

and two admitted host surfaces:

- inferential
- logical

## Implementation Shape

### A. Capability parity audit

Before recomposition is coded, do one direct parity audit between:

- Critic-local inferential output contract
- analyzer-v2 inferential engine/operationalization output

and between:

- Critic-local logical result contract
- analyzer-v2 concept-analysis chain output

This audit must classify:

- fields already aligned
- fields needing translation
- fields only used by native Critic concept views
- fields only used by `Close Read`
- fields safe to deprecate later but not in this tranche
- execution-model differences that affect result shape, not just field names
- source/provenance fields the host UI assumes exist

This audit is a required delivery artifact, not an optional preparatory note.
It must produce two field-by-field matrices:

- inferential translation matrix
- logical translation matrix

Each row must include:

- current host field
- analyzer-v2 source field(s)
- transform/derivation rule
- gap status

For inferential specifically, the audit must not assume structural proximity.
It should explicitly compare:

- Critic's section/UI-shaped contract
- analyzer-v2's graph/schema-shaped contract

and specify the transformation layer required between them.

For logical specifically, the audit must not rely only on the visible analyzer-v2 chain definition files.
It must compare the currently rendered Critic logical host contract against:

- analyzer-v2 chain definitions
- any currently available analyzer-v2 prompt/schema evidence

because the present chain-definition files do not, by themselves, prove full parity with the richer current Critic logical output contract.

This is not a separate product memo.
It is implementation prep required to keep the rebasing honest.

### B. API execution-owner seam

Define one API-side seam where Critic stops calling its local inferential/logical runtime as the primary owner and instead calls analyzer-v2-owned capability paths.

The scope should prefer:

- one bounded integration layer in the API
- not analyzer/database queries from deep inside the host UI
- not new ad hoc route families

The API should remain responsible for:

- project/document loading
- project metadata assembly
- invoking the analyzer-v2 capability path
- persisting translated results into the current host-visible storage/read model

### C. Inferential rebinding

Use analyzer-v2's inferential engine definition and operationalization as the canonical path for inferential concept analysis.

Required outcome:

- a project-aware inferential run for a concept is executed through analyzer-v2 composition, not the old Critic-local inferential prompt as the primary runtime
- Critic persists and renders the resulting analysis through the existing native and `Close Read` concept surfaces

The scope may allow:

- a bounded but structural translation layer from analyzer-v2 output to current Critic result fields and sections

That inferential translation target must hit the full current host contract, not a reduced subset:

- `synthesis`
- `the_deceptively_simple`
- `commitment_cascade`
- `incompatibility_map`
- `tensions`
- `practical_stakes`
- `commitment_packages`

It should not require:

- immediate redesign of all inferential rendering components

The scope should state plainly that inferential recomposition includes an execution-model choice.
analyzer-v2's inferential operationalization is multi-pass:

- `discovery`
- `confrontation`
- `dialectical`
- `integration`

across multiple depth sequences.

So this tranche must freeze whether inferential rebasing means:

- full multi-pass adoption
- a bounded v2 depth profile
- or staged adoption with parity measured at each step

### D. Logical recomposition

Use analyzer-v2's concept-analysis chain as the canonical deep concept/logical path.

Required outcome:

- the logical surface is driven by analyzer-v2's chain composition rather than the old Critic-local phase runtime as the primary owner
- the host can still render admitted logical content, including the currently admitted logical-only scrutiny follow-up

Translate analyzer-v2 logical outputs into the exact current Critic logical persisted/rendered contract.
Preserve or deterministically derive all fields required by:

- native concept pages
- `Close Read`
- logical scrutiny

The target contract is the current `LogicalAnalysis` shape, including:

- `synthesis`
- `argument_inventory`
- `argument_chains`
- `causal_architecture`
- `conditional_web`
- `argumentative_weight`
- `logical_vulnerabilities`
- `textual_shifts`

and all host-required nested fields relied on by rendering and scrutiny.

The scope should assume:

- some adaptation is likely necessary because the old logical host surfaces reflect a legacy result shape and a legacy phase model
- the currently visible analyzer-v2 chain/engine definition layer does not by itself prove full host-contract parity with Critic's logical UI
- `phase_base.py` already gives evidence of partial analyzer-v2 prompt integration, so the remaining architectural gap is execution ownership and output compatibility more than template access

So the logical workstream should explicitly include:

- chain/output parity audit
- adapter/translation decision
- scrutiny compatibility decision

### E. Scrutiny compatibility

The concept-family boundary already admits scrutiny on the logical surface.

So this recomposition scope must answer:

- whether the current scrutiny API stays host-local but consumes analyzer-v2-shaped logical outputs
- or whether a bounded logical-output normalization step is required before scrutiny can run truthfully

The safe default for this tranche is:

- keep scrutiny as a host-local follow-up operation
- but make its input truthfully derive from analyzer-v2-owned logical results rather than from the old local logical runtime

Do not widen this into:

- ammunition
- send-to-outline
- broader attack workflows

### F. Acceptance path

This tranche is not complete unless it proves one real end-to-end concept path through analyzer-v2-owned execution while preserving current host usability.

Minimum acceptance path:

1. choose a live project with enough concept-analysis material
2. run one inferential concept analysis through analyzer-v2-owned execution
3. run one logical concept analysis through analyzer-v2-owned execution
4. confirm the resulting concept appears correctly in:
   - native Critic concept views
   - `Close Read` concept family views
5. confirm one logical scrutiny flow still works truthfully on the rebased result
6. validate that the persisted translated logical output satisfies the full current `LogicalAnalysis` contract, including non-tabbed fields such as:
   - `conditional_web`
   - `argumentative_weight`
   - `textual_shifts`

Execution-owner swap does not ship unless:

- both translation matrices are complete and approved
- the full logical contract validates
- scrutiny reads only translated rebased logical data rather than any old local-runtime-only fields

## Public Interfaces / Non-Changes

Do not change in this tranche:

- `Close Read` routes
- native concept-analysis routes
- concept-family product boundary
- deferred submodes:
  - `assumption`
  - `semantic_field`
  - `causal`
  - `metaphorical`
- genealogy or AOI routes
- standalone-host posture

What may change internally:

- API execution seam
- analyzer invocation path
- stored result translation/adapter layer
- runtime ownership of inferential/logical capability execution

## What This Memo Deliberately Defers

Still deferred:

- full analyzer-v2-native migration of every old concept submode
- family-crossing composition-layer work
- broader bespoke module composition
- renderer redesign around analyzer-v2-native schemas everywhere
- standalone `Close Read` app/host work
- generic downstream operation-law convergence across all families

## Bottom-Line Scope Decision

The next serious scope after fresh-project runtime enablement should be:

- **Close Read concept-analysis analyzer-v2 recomposition**

not:

- more local Critic analyzer patching as if that were the destination
- more `Close Read` concept UI work
- a jump to the general composition layer before one serious family is actually analyzer-v2-owned

That is the next honest phase if the roadmap means what it says about:

- analyzer-v2 as the brain
- apps as presentations
- default families as stepping stones toward composable analytical modules
