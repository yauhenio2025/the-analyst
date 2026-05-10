# Memo: Close Read Direction Change And Implications

Subtitle: What the Close Read dictation changes, what it does not change, and the concrete forward move

Date: 2026-04-01
Program: Dynamic Bespoke Apps Platformization
Reference Dictation:
- `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
Current Strategy Context:
- `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
Current Next Phase Scope:
- `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_scope.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`

## Purpose

Package the implications of the Close Read dictation into one concrete strategic memo:

- what it changes about the program frame
- what it does not change
- where the current codebase already points in this direction
- what the next move should now be

## Bottom Line

The dictation does change the frame in a meaningful way.

It adds a missing product layer:

- not just engine outputs
- not just renderer families
- not just composition law

but also:

- engine-specific follow-up operations over rendered outputs
- routing of resulting artifacts into `Research`, `Arsenal`, and later `Book Modeler`

So the product framing is no longer adequately described as:

- analyzer-v2 generates renderable analytical surfaces for thin hosts

It is better described as:

- analyzer-v2 becomes the brain for products like a future `Close Read` app that coordinate inputs, engine runs, rendered analytical surfaces, follow-up operations, and artifact routing into downstream knowledge and modeling systems

## What The Dictation Changes

### 1. It introduces a missing abstraction layer

The missing layer is:

- operation families over analytical outputs

Examples from the dictation:

- test logical premises
- identify weak points
- ask for clarification
- capture
- route findings to research
- route findings to arsenal
- mobilize further reading or thinkers

These are not the same thing as renderers.
They are downstream actions that become valid only for certain engine/output paths.

### 2. It makes the flagship proving ground more explicit

The actual destination is not `analyzer-mgmt`.
It is not a growing pile of proof harnesses either.

The dictation points to the strongest concrete flagship proving ground we currently have:

- a multi-project, eventually multi-user app for close reading

That app should allow:

- one or more inputs
- optional primary/secondary distinctions
- selected or planned engine mixes
- rendered analytical interfaces
- engine/path-dependent follow-up work
- downstream routing into `Research`, `Arsenal`, and `Book Modeler`

This should be treated as:

- the best current flagship product direction
- not yet the singular destination that replaces the broader platform thesis of dynamic bespoke apps in the plural

### 3. It changes how we should judge architecture work

Architecture work should no longer be judged only by:

- whether it makes renderers or consumers more generic

It should be judged by whether it helps us build credible flagship products and the broader platform:

- `Close Read`

That means the question is no longer only:

- can analyzer-v2 compose and render engine outputs cleanly?

It is also:

- can analyzer-v2 annotate outputs with the semantic affordances that tell hosts which follow-up operations are structurally supportable?
- can it route those outputs or derived artifacts to the right downstream destinations?
- can it support a product where engine results are not terminal pages, but intermediate analytical work surfaces?

## What The Dictation Does Not Change

### 1. It does not make the recent strategy wrong

The recent strategy remains correct on two important points:

- renderer/interface boundedness is still real
- extraction surgery is still a better next implementation move than pretending we already have a generic composition law

The dictation does not make:

- `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`

wrong.

It narrows its sufficiency.

That memo is still useful, but it is now only one layer of the problem.

### 2. It does not make the next analyzer-side extraction tranche unnecessary

The current presenter pipeline is still too workflow-shaped for the `Close Read` destination.

The hard-coded seams in:

- `src/presenter/compose_from_intent.py`

still need extraction.

If we skip that and jump straight to a new product shell, `Close Read` will just become another app whose behavior depends on AOI/genealogy-specific presenter code.

### 3. It does not imply one mega-app must be built immediately

The dictation defines a north star, not necessarily the first implementation form.

The right reading is:

- use `Close Read` as an indicative flagship direction
- do not overbuild the final super-app before the substrate contracts are clearer

## Code-Backed Evidence And Limits

The codebase already contains evidence that the product is about more than rendering outputs.
But the evidence is uneven, and it matters to distinguish:

- app-local product patterns
- analyzer-owned platform law

Those are not the same thing.

### Critic already contains downstream operation patterns

In `the-critic`:

- `webapp/src/contexts/CaptureContext.tsx`
  - already models capture state and downstream destination intents like `arsenal` and `research_todo`
- `webapp/src/pages/FindingsPage.tsx`
  - already operationalizes downstream add/remove flows into Arsenal and adjacent research/finding work
- test flows mention:
  - `Research Question`
  - `Capture`
  - `NotebookLM`
  - Arsenal destinations

This matters because it shows the real app logic is already partly:

- analysis surface -> user action -> routed artifact

not just:

- analysis surface -> final display

But this is still:

- Critic-local runtime logic

not:

- analyzer-v2 ownership of that law

So the strongest honest reading is:

- Critic is product evidence that downstream operation/routing patterns are real
- not proof that analyzer-v2 already owns those patterns upstream

### Analyzer-mgmt carries weaker evidence of latent product intent

In `analyzer-mgmt`:

- `frontend/src/pages/plans/[id].tsx`
  - displays a `Research Question`
- `scripts/seed_rhetoric.py`
  - shows rich structured analysis outputs around rhetoric and logical vulnerability
- `scripts/populate_rhetoric_schemas.py`
  - shows structured schemas for those outputs

This matters because it shows that part of the missing abstraction is already latent.
But it is weaker evidence than the Critic runtime.

It is best read as:

- product intent and structured output richness

not:

- already-hardened runtime follow-up operation law

### Analyzer-v2 is still too composition-shaped

In `analyzer-v2`:

- `src/presenter/compose_from_intent.py`
  - still centrally hard-codes role/pattern/stance decisions
- `src/presenter/presentation_bridge.py`
  - still validates in observational `WARN` mode
- `src/presenter/manifest_builder.py`
  - still contains fallback behavior including `raw_json`
- `src/presenter/renderer_contract_enforcement.py`
  - already enforces strict served-renderer law for selected served surfaces

This matters because the validator story is split, not absent:

- some served surfaces already fail closed
- other presentation and bridge seams still validate observationally
- fallback behavior like `raw_json` still exists in bounded cases

This matters because it shows the missing work is still on the analyzer side, but we should describe it honestly:

- analyzer-v2 has real strict governance in some places
- and real remaining generalization gaps in others

## The New Layer We Need To Name

The right decomposition is now:

### 1. Renderer families

Examples:

- `prose`
- `accordion`
- `card_grid`
- `tab`

This is the bounded interface surface.

### 2. Output families

Examples:

- synthesis
- comparison map
- findings bank
- report closeout
- inventory/listing

These are not yet properly generalized.

### 3. Operation families and semantic affordances

Examples implied by current apps and the dictation:

- capture
- promote to arsenal
- flag as research question
- annotate/comment
- premise attack / logic-gap scrutiny
- clarification
- route to external research support like NotebookLM
- route to downstream modeling substrate

This is the layer the dictation makes impossible to ignore.

But the ownership boundary should be stated carefully:

- analyzer-v2 should likely own semantic affordances and routing annotations
- hosts should operationalize the actual UX and action flows

### 4. Artifact routing families

Likely destinations:

- `Research`
- `Arsenal`
- `Book Modeler`
- lightweight writing/prototype outputs

These need contracts too.

## Strategic Consequence

The corrected product statement is now:

- analyzer-v2 must become the brain not only for analysis generation and composition, but also for annotating analytical outputs with the semantic affordances and routing hints that tell thin hosts which downstream actions are structurally supportable

That is more ambitious than the recent renderer-first framing.

But it does not justify abandoning the current extraction plan.

Instead it changes what that plan is for.

The composition extraction tranche is now justified not just because the code is too hard-coded, but because:

- we need a cleaner substrate before we can honestly define operation-family and routing-family law for `Close Read`

## Recommended Forward Move

## Immediate implementation move

Keep the next implementation tranche exactly where the current roadmap put it:

- `Phase E Composition Metadata Extraction V1`

That remains the right next concrete code move.

Reason:

- it attacks central analyzer coupling
- it is behavior-preserving
- it reduces the cost of later generalization
- it keeps hosts stable

## Immediate strategic/product move

In parallel with that analyzer tranche, start a smaller product-architecture line specifically around downstream operations and routing.

That line should start with one bounded audit tranche, not with a large target-state memo immediately.

### A. Bounded operations and routing inventory

Audit the existing concrete patterns in:

- `the-critic`
- logic-focused Benanav flows
- analyzer-mgmt rhetoric/research structures

The purpose is not archaeology for its own sake.
It is to classify:

- actual follow-up operation families
- actual artifact destinations
- actual interaction patterns we already know we want
- which of those are:
  - generic capture/annotation operations
  - output-specific follow-up operations
  - routing contracts
- which analyzer-side semantic affordances would be sufficient for hosts to operationalize them

### B. Only after that, a `Close Read` product memo

Once the operations/routing inventory is real, write the larger memo:

- `Close Read V1` target-state memo

That later memo should define:

- project model
- input model
- primary/secondary text model
- planner-vs-explicit engine selection
- analysis surface families
- operation families
- routing destinations
- what counts as a lean V1

## What Should Not Be Next

Given this memo, the next move should still not be:

- another proof-only shell exercise
- another lifecycle broadening slice first
- abstract taxonomy design detached from code
- a giant new `Close Read` app build before the analyzer-side extraction tranche
- a premature claim that `Close Read` replaces the broader dynamic bespoke apps destination

Those would either jump too far ahead or solve the wrong layer first.

## Working Conclusion

The dictation changes the flagship product framing more than it changes the next code move.

It tells us:

- the target product is `Close Read`
- the missing layer is operation families plus artifact routing
- Critic and Benanav matter because they already embody those patterns

But it also tells us something disciplinary:

- do not keep generalizing architecture in the abstract without checking it against the real target product

So the correct synthesis is:

1. keep the next analyzer move as composition metadata extraction
2. treat `Close Read` as the strongest current flagship proving ground, not the singular destination
3. begin a focused audit of follow-up operations and artifact routing from Critic and adjacent logic/research flows
4. use that audit, not speculation, to define the next tranche after extraction and the later `Close Read` product memo

That is the most honest way to move toward analyzer-v2 as the brain without drifting into either:

- abstract architecture theater
- or premature product sprawl
