# Memo: Interface-First Renderer / Output-Family Strategy

Subtitle: Treat future engine growth as a bounded renderer-contract problem rather than a per-engine app-architecture problem

Date: 2026-04-01
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Recent Completion Context:
- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_source_selection_v1_completion.md`
- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_direct_sections_v1_completion.md`
- `communications/MEMO_2026-04-01_phase_e_transient_consumer_identity_plurality_v1_completion.md`

## Purpose

Capture one strategic hypothesis for the next stage of platformization:

- future engine growth should be handled primarily by a bounded set of renderer/output-family contracts, not by app-specific or engine-specific architecture every time

This memo is not claiming that the problem is already solved.

It is proposing a better way to frame the problem:

- work from the limited set of interfaces we can realistically render
- make engines target those interfaces through strict contracts
- let analyzer-v2 own the projection/composition law
- keep hosts thin

## Core Hypothesis

The working assumption is:

- most future engines will not be “arbitrarily alien”
- they may differ in:
  - number of passes/prompts
  - content
  - analytical stance
  - exact placement in the composed UI
- but they will still produce output that can be projected into a bounded set of renderable interface families

If that assumption is true, then the platform problem is smaller than “support any engine combination” sounds.

The hard problem may become:

- define a small number of stable renderer/output families
- define strict data contracts for each family
- make engines declare how they project into those families
- make analyzer-v2 compose those families into one page/app surface

Rather than:

- inventing one new app architecture per engine or per workflow

## Current Code-Backed Basis

This hypothesis is not being invented from thin air.

The current codebase already has several pieces of the right shape:

### 1. Consumer capabilities are renderer-declared, not page-hardcoded

`src/consumers/schemas.py` already models consumer support in terms of:

- `supported_renderers`
- `supported_sub_renderers`

That is the right direction.
It means the contract boundary already thinks in terms of renderer capabilities, not workflow-specific pages.

### 2. Renderers already have explicit schema-bearing definitions

`src/renderers/schemas.py` already models renderer definitions with:

- `renderer_key`
- `category`
- `ideal_data_shapes`
- `input_data_schema`
- `primitive_affinities`
- `config_schema`

And the live top-level renderer catalog is already bounded:

- `accordion`
- `card_grid`
- `evidence_trail`
- `prose`
- `raw_json`
- `stat_summary`
- `tab`
- `table`
- `timeline`

That bounded catalog is strategically important.

It suggests the UI problem may be better treated as:

- “how many stable renderer families do we need?”

not:

- “how many bespoke engine UIs do we need?”

But that statement needs one correction:

- the real rendered interface vocabulary is larger than the 9 top-level renderers
- there are also:
  - 6 view patterns
  - 20 sub-renderers

So the memo should not pretend the existing key list is already the final family set.
The right claim is narrower:

- the space looks bounded enough to justify trying to collapse it into a smaller family taxonomy

### 3. Consumer-specific renderer fallback is already a first-class seam

`src/presenter/manifest_builder.py` already has consumer adaptation through:

- `adapt_renderer_for_consumer(...)`

The current behavior is still simple:

- if unsupported, fallback to `raw_json` when available

That is not the final platform law, but it is the right seam.
It means the system already knows that renderer support is a consumer contract question.

Correction:

- the inversion is not yet complete
- `src/renderers/schemas.py` and `src/renderers/registry.py` still carry legacy `supported_apps` / fallback behavior
- so the codebase is moving toward consumer-declared support, not fully there yet

### 4. Composition already passes through view-generation and renderer-validation seams

The current composition substrate already includes:

- `src/views/generator.py`
- `src/renderers/validator.py`
- `src/presenter/compose_from_intent.py`

So the broad shape already exists:

- engine output
- view generation / renderer targeting
- payload validation
- consumer adaptation
- final served surface

But this needs to be stated more honestly:

- the current substrate is not merely “partly hand-tuned”
- it is still strongly AOI/genealogy-shaped in the presenter/composition layer
- there are multiple workflow-specific branches, hard-coded maps, and separate orchestration paths

So the correct conclusion is:

- the architectural direction is compatible with an interface-first strategy
- the current implementation is still much more workflow-specific than the first draft implied

## Strategic Reframe

The platform should treat future engine growth primarily as a problem of:

1. canonical output families
2. renderer families
3. projection contracts
4. page-composition law
5. lifecycle/persistence law

not as a problem of:

1. per-engine app architecture
2. per-workflow page design
3. host-local analytical reconstruction

This keeps the program aligned with the real destination:

- analyzer-v2 becomes the brain
- hosts become thin shells that route, render, persist, and brand

## Three Separate Problems

The first draft compressed too many things into one “renderer/output-family” story.

The code and reviews suggest three separate problems that should stay distinct:

### 1. Renderer-family boundedness

This is the strongest existing claim.

What is already substantially true:

- the top-level renderer catalog is small
- consumers already declare renderer capabilities
- renderer schemas and validation seams already exist

This is the most mature part of the story.

### 2. Output-family taxonomy

This does **not** yet exist as a first-class live contract.

Today:

- engines do not broadly declare output family
- engines do not broadly declare preferred renderer family
- engines do not broadly declare composability role or placement policy in the way this strategy would need

So output-family taxonomy is not “already there.”
It is a proposed next abstraction layer.

### 3. Composition-law generalization

This is the hardest part.

Today:

- composition still has multiple workflow-shaped entry paths
- some grouping/placement law is still encoded centrally and specifically
- consumer admission and handoff kinds still include explicit hard-coded policy seams

So the main challenge is not taxonomy alone.
It is extracting currently centralized workflow-specific law into reusable metadata plus reusable composition rules.

## Proposed Working Model

### A. Renderer families should stay small and explicit

The safest strategy is to assume we can only support a limited number of durable renderable interfaces.

The current live catalog already points toward a plausible bounded family set:

- container/navigation:
  - `tab`
  - `accordion`
- card/list/comparative:
  - `card_grid`
  - `table`
  - `stat_summary`
  - `evidence_trail`
- narrative:
  - `prose`
- temporal/lineage:
  - `timeline`
- bounded fallback:
  - `raw_json`

The principle should be:

- if a new engine cannot be projected into one of these or one very small number of future renderer additions, that is an exception requiring explicit architectural review

not something every host silently absorbs.

### B. Engines should target canonical output families, not freeform UI payloads

The next contract layer should probably not be:

- “engine outputs renderer-ready JSON directly”

The safer layer is:

- engine output -> canonical semantic artifact
- canonical semantic artifact -> renderer payload

Examples of plausible canonical output families:

- narrative closeout
- sectioned analysis
- findings bank
- grouped cards
- evidence trail
- comparative table / matrix
- timeline / lineage
- summary stats
- containered multi-part page

Those families are semantically richer than raw renderer keys, but still bounded enough to standardize.

Important correction:

- this taxonomy should not be treated as already latent in engine definitions
- today much of that mapping still lives in central presenter code
- so the near-term work is not only “design the taxonomy”
- it is also “extract the mapping law out of central workflow-shaped code”

### C. LLM projection is acceptable only as a bounded adapter

The tempting version of this strategy is:

- “LLMs can format data however we want; it is just one extra call”

That is directionally useful, but only if bounded hard.

The good version is:

- use an LLM to project engine output into one strict target schema
- validate the result against that schema
- fail closed if invalid

The bad version is:

- let an LLM improvise arbitrary UI payloads or page structure

So the rule should be:

- LLM projection is allowed as a bounded schema-filling adapter
- LLM projection is not allowed as freeform UI law

This also needs one harder code-backed caveat:

- the current system already uses multiple LLM steps in the transient path
- and the current validation discipline is not yet as strict as the first draft implied

So “fail closed if invalid” should be treated as a target discipline, not as a blanket description of current reality.

The validator/default-contract gap is real and should be named explicitly in any follow-up tranche.

### D. Composition law becomes the real platform differentiator

If renderer families and output families are bounded, then the main “brain” problem shifts to:

- how multiple outputs combine into one coherent page/app surface

That is where analyzer-v2 should own:

- composability roles
- placement hints
- container choice
- closeout positioning
- fallback/degradation policy
- lifecycle compatibility

In other words:

- per-engine complexity should collapse into per-family composition law

not into more host code.

## What This Would Change In Practice

If the memo’s hypothesis is basically right, then the strategic imperative changes.

The highest-value work is less about proving one more shell and more about extracting reusable contracts from the shells and proofs we already have.

That likely means the next important generalization layer is:

### 1. Canonical output-family taxonomy

Define a small stable list of output families and their schemas.

Each family should answer:

- what semantic role it serves
- what renderer families it can target
- what lifecycle/persistence expectations it has
- what composition roles it can occupy

### 2. Engine-family metadata

Each engine definition should eventually declare enough to project into the output family layer, such as:

- output family
- composability role
- preferred renderer family
- fallback renderer family
- placement hints
- lifecycle / persistence compatibility
- whether projection can be deterministic or needs bounded LLM projection

This should be read as a destination, not as a statement about current breadth of engine metadata.

### 3. Projection layer discipline

The system should make explicit where projection is:

- deterministic
- LLM-assisted but schema-bounded
- not yet safely supported

### 4. Composition-family rules

Define reusable composition policies such as:

- multi-part comparison page
- dossier page
- genealogy page
- report-with-supporting-evidence page
- summary-plus-drilldown page

These should be treated as bounded composition families, not app-local one-offs.

## Why This Helps The Ultimate Vision

The user’s actual end goal is not:

- prove AOI
- prove genealogy
- prove one more shell

The goal is:

- bootstrap or adapt a new app/site quickly for a chosen analytical mix
- let analyzer-v2 own the analysis and page-composition intelligence
- let the host mostly brand, route, render, and persist

This strategy helps because it makes future app creation look more like:

1. choose engine set
2. declare engine/output families
3. choose consumer renderer surface
4. choose composition policy
5. deploy a thin host

instead of:

1. invent new app architecture for each engine/workflow mix

That is much closer to analyzer-v2 being the brain.

## Risks And Caveats

This reframe is promising, but it can go wrong in predictable ways.

### Risk 1: We underestimate output-family diversity

If future engines really do produce shapes that do not fit the bounded family set, the memo’s optimism breaks.

That would mean:

- more renderer families are needed than expected
- or the engine/output-family model is too coarse

### Risk 2: LLM projection becomes soft glue

If bounded LLM projection quietly turns into:

- freeform structure invention
- unstable schema filling
- consumer-specific formatting logic

then the system will look generic while staying brittle.

### Risk 3: Composition law remains workflow-special underneath

Even with bounded renderer families, composition may still hide:

- AOI-specific heuristics
- genealogy-specific heuristics
- route-family-specific heuristics

If that remains true, the memo would overstate generality.

### Risk 4: Lifecycle law may still be request-family-fragile

The recent `persistable_compose_request` slice proves one bounded bridge.

It does not yet prove:

- generic save/reopen across all request families

So output-family generality and lifecycle generality are related but not identical questions.

### Risk 5: We jump to taxonomy before doing extraction surgery

If current engine-to-role / renderer / placement mappings remain hard-coded in central presenter code, then taxonomy design alone will not buy much.

The reviews were right to call this out:

- the next move cannot just be “invent output-family names”
- it must also extract current hard-coded mapping law into metadata or family-level definitions

## Proposed Near-Term Decision

The program should seriously consider shifting part of the next generalization work toward an interface-first contract program.

That means:

### Phase 1: Extraction and coupling inventory

1. inventory the workflow-specific and engine-specific coupling that still lives in:
   - presenter orchestration
   - source-bridge mapping
   - renderer-contract enforcement
2. classify each coupling as one of:
   - family-generic metadata
   - reusable composition law
   - operational / admission policy

### Phase 2: Extract the lowest-risk metadata first

3. move the easiest current hard-coded maps into engine/family metadata first
4. do not try to solve all composition-law generalization in one move

### Phase 3: Only then formalize the family taxonomy fully

5. define the smallest honest output-family taxonomy over the extracted metadata and actual renderer/sub-renderer surface
6. map current AOI/genealogy engines into it
7. identify which mappings are deterministic vs bounded-LLM-projection

The key correction is:

- the next tranche is extraction surgery first, taxonomy design second

## Honest Claim

This memo does not claim:

- the bounded renderer family set is already sufficient
- arbitrary future engines will definitely fit it
- one extra LLM call automatically solves UI generality

It does claim:

- this is likely the right side of the problem to attack
- it is more aligned with analyzer-v2-as-brain than continuing to reason primarily in app-shell terms
- if the assumption is mostly right, the task is materially easier than “support arbitrary engine combinations” sounds

But the corrected optimism level should be:

- the direction is right
- the renderer-family part is the most proven
- the output-family and composition-law parts still require substantial extraction work from workflow-shaped code

## Next Question For Review

The real question for second opinion is:

- does the current codebase and recent proof line support the hypothesis that future engine growth should mainly be handled through a bounded renderer/output-family contract layer, or is that still too optimistic given how much workflow-specific composition law is actually encoded today?
