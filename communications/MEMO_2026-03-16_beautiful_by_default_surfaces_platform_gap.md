# Memo: What Analyzer-v2 Still Lacks for Beautiful-by-Default Surfaces

Date: 2026-03-16

## Purpose

This memo is a platform diagnosis, not an implementation plan.

It is meant to answer one question:

- if we launched another thin app that mixed AOI-style surfaces with genealogy-style surfaces, what would still stop analyzer-v2 from making that app look beautiful by default?

The point is not to complain that AOI is ugly.

The point is to identify what analyzer-v2 still lacks as a presentation platform, so future apps do not repeat the same pattern:

- semantics land first
- generic renderers technically work
- the output is correct but visually under-composed
- downstream apps are then tempted to patch the problem locally

This memo should help Codex and Claude critique:

- whether the diagnosis is accurate
- which missing pieces are most important
- what should become platform policy versus local AOI/genealogy cleanup

## March 13 Thesis, Restated

The March 13 direction was:

- analyzer-v2 should own semantics and presentation intent upstream
- thin consumers should stay thin
- the system should generalize beyond one legacy app and one semantic shape

AOI plus the canary gave us one bounded proof of that architecture.

But “bounded proof” does not mean “beautiful by default.”

It means:

- one explicitly scoped slice works without downstream semantic repair

The broader question now is:

- what would make that kind of slice come out well-composed by default, not merely correctly rendered?

## Executive Diagnosis

Analyzer-v2 already has a substantial presentation stack.

It does **not** yet behave like a system that emits beautifully composed reading surfaces by default.

The core problem is:

- the platform has patterns, templates, stances, affinities, shared renderers, and delivery polish
- but the live source of truth is still too dependent on hand-authored view JSON plus generic renderer defaults

So analyzer-v2 today is best described as:

- strong semantic engine
- medium presentation scaffolding
- incomplete composition platform

That is why the best-looking surfaces are the ones whose view definitions are already carefully composed, while weaker surfaces still look like “correct payload + generic renderer.”

## Audit Findings

### 1. Most live views still bypass real transformation shaping

Analyzer-v2 currently has:

- 33 view definitions
- 24 transformation definitions
- 6 view patterns
- 7 renderer components
- 1 shared sub-renderer file that carries the registered sub-renderer set

But on the live path, most view definitions still declare:

- `transformation.type = "none"`

That is true for:

- most genealogy views
- all current AOI views
- the lines-of-attack views

So although the transformation layer exists, most presentation quality is still coming from the view definition itself, not from a robust renderer-facing shaping step.

This matters because it means:

- engine output is often only lightly normalized before it reaches live renderer config

### 2. View patterns exist, but they are still mostly advisory

Analyzer-v2 has view patterns in:

- `src/views/patterns`

These are useful and often sensible:

- `accordion_sections`
- `card_grid_simple`
- `card_grid_grouped`
- `prose_narrative`
- `tab_with_children`
- `timeline_sequential`

But patterns are still not the live authoritative contract for page assembly.

In practice, the running system still behaves as if the main source of truth is:

- hand-authored view definition JSON

That means patterns help authors and future generators, but they do not yet guarantee that new capabilities enter the system with a strong surface family.

### 3. Presentation stance is real, but weaker than layout composition

Presentation stance is more complete than it first appears.

Active genealogy, AOI, and lines-of-attack views do carry stance values like:

- `summary`
- `narrative`
- `diagnostic`
- `evidence`
- `comparison`
- `interactive`

And stance does flow through:

- composition resolution
- presentation bridge
- refinement
- polish

But stance is still not strong enough to guarantee a beautiful reading surface.

It influences:

- prompting
- refinement recommendations
- polish context

It does **not** by itself guarantee:

- the right section hierarchy
- the right surface family
- the right renderer/sub-renderer composition

So stance is useful, but it is not yet a sufficient runtime presentation contract.

### 4. Style wiring exists, but automatic activation is still narrow

Analyzer-v2 now has:

- style schools
- engine affinities
- page-level `style_school`
- page-level `polish_state`
- delivery polish

AOI engine affinities are now present.

But automatic ordinary-path delivery activation is still intentionally narrow in `delivery_style.py`:

- one workflow
- one root page
- one consumer

So the system does not yet operate as if “beautiful-by-default presentation” is the normal case for new surfaces.

It still operates more like:

- explicit bounded activation for selected proof slices

That is good discipline for current rollout, but it also means the broader platform behavior is still incomplete.

### 5. Consumer-aware presentation is still bounded, not native

Analyzer-v2 does have consumer definitions.

But the live platform still feels more like:

- a strong primary presentation system adapted for multiple consumers

than:

- a genuinely multi-consumer-native presentation contract from the start

AOI canary proved one bounded thin-consumer slice.

That is important.

But it is still not true that every new capability is authored as a clearly consumer-ready surface family from day one.

### 6. The best-looking surfaces are the ones with explicit editorial composition

This is the most important practical finding.

The surfaces that look best today are not necessarily the ones with the most clever semantics.

They are the ones whose view definitions already resemble a real reading surface.

Examples:

- `aoi_thematic_report`
- stronger genealogy accordion views like:
  - `genealogy_tp_narrative_structure`
  - `genealogy_tp_conceptual_framework`
  - `genealogy_tp_inferential_commitments`
  - `genealogy_tp_chapter_roles`

These look better because they have:

- stronger section hierarchy
- explicit section renderers
- more deliberate matching between field shape and renderer family

The weaker surfaces are the ones where analyzer-v2 is still effectively saying:

- here is a heterogeneous object
- please render it through a generic accordion or card grid

That is why AOI `Full Report` looks better than AOI `Source Documents`, `By Theme`, or `By Sin Type`.

It is also why some genealogy surfaces feel more alive than AOI even when they use the same underlying machinery.

## What Is Missing for “Beautiful by Default”

### 1. A true runtime presentation contract

Analyzer-v2 needs a stronger live contract that says, for each serious surface:

- what kind of reading surface this is
- what renderer family it belongs to
- what section structure is expected
- what sub-renderers are allowed
- what style family it defaults to
- whether polish is activated, optional, or unavailable

Right now those answers are distributed across:

- view JSON
- templates
- stance
- affinities
- delivery-style activation

They need to feel more like one coherent runtime contract.

### 2. Canonical surface families

The platform still relies too heavily on a few generic primitives:

- accordion
- card grid
- prose

Those are not enough.

Analyzer-v2 needs a richer editorial vocabulary that future capabilities can map into directly.

Examples of likely reusable surface families:

- narrative closeout
- source library / bibliography
- grouped evidence review
- taxonomy review
- profile / dossier
- conceptual framework atlas
- conditions / constraints dossier
- comparison surface

The key requirement is:

- AOI and genealogy should both be able to resolve into these families without each app inventing custom page logic

### 3. Real renderer-facing shaping as a normal step

Too many views are still basically:

- engine output
- plus hand-written renderer config

Analyzer-v2 needs the transformation/composition layer to do more real editorial shaping.

That does **not** mean “LLM beautification.”

It means deterministic shaping into renderer-ready structures, such as:

- evidence stacks rather than long prose cards
- source-library rows rather than generic cards
- explicit dossier sections rather than field dumps
- grouped analytic lists rather than nested object blobs

### 4. Stronger shared editorial renderers

The shared renderer system is competent.

It is not yet strong enough as an editorial language.

To get beautiful-by-default surfaces, the shared layer needs more than flexible primitives.

It needs stronger default surface behavior:

- better hierarchy
- better rhythm and spacing
- better long-form evidence handling
- fewer giant mixed-content sections
- fewer card surfaces trying to carry prose they were not meant to carry

### 5. Mandatory capability onboarding

New capabilities cannot be treated as done when only semantics land.

For analyzer-v2 to become a platform that emits beautiful surfaces by default, every new capability should require:

- explicit surface-family choice
- explicit renderer/sub-renderer declaration
- explicit style affinity
- explicit activation/default policy
- one styled proof artifact
- one thin-consumer proof

Without that, the platform will keep reproducing the same problem:

- semantic success
- presentation debt deferred to the next app

### 6. Better distinction between bounded activation and platform defaults

Right now explicit activation is doing too much conceptual work.

We need a cleaner separation between:

- affinity: what style family this engine/view tends to want
- activation: where automatic delivery polish is allowed
- runtime truth: what actually happened on this page/job/consumer

That separation is conceptually present now.

It is not yet a mature platform discipline for every new capability.

## What This Means for a Future Mixed AOI + Genealogy App

If we launched a new app that mixed AOI and genealogy tomorrow, analyzer-v2 could likely make it:

- semantically correct
- thin-consumer compatible
- partially styled

It would **not** yet reliably make it beautiful by default.

The risk would be:

- the best surfaces would look strong
- the weaker surfaces would still feel like generic renderer outputs
- the new app would then be tempted to patch composition locally

That is the exact failure mode we should avoid.

So the right principle is:

- do not solve this by making the next app smarter
- solve it by making analyzer-v2 emit better-composed surfaces upstream

## Provisional Direction

This is not yet the plan, but it is the likely direction:

1. formalize canonical surface families in analyzer-v2
2. make pattern/template metadata matter more at runtime
3. expand deterministic renderer-facing shaping
4. strengthen shared editorial renderers
5. require presentation-readiness onboarding for every new capability
6. broaden style activation only after the surface contract is stronger

That order matters.

If we broaden style activation without stronger composition, we will simply produce more consistently styled mediocrity.

## Questions for Codex and Claude

### 1. Is the central diagnosis correct?

Specifically:

- is the main problem really that patterns/templates/stances/affinities are not yet unified into a strong runtime presentation contract?

Or is the bigger problem somewhere else?

### 2. Which missing layer matters most?

If only one thing can be addressed first, which is most leverageful?

- canonical surface families
- stronger deterministic shaping
- stronger shared editorial renderers
- mandatory onboarding discipline
- broader style activation

### 3. Are surface families the right abstraction?

Should analyzer-v2 move toward explicit canonical surface families?

Or is there a better abstraction for making future mixed-domain apps come out well-composed by default?

### 4. How much of the problem is renderer design versus composition contract?

The current diagnosis says:

- composition contract is the bigger gap
- shared renderer design is the second gap

Is that ordering correct?

### 5. What should become mandatory platform policy?

Which of the following should be treated as required for every new capability?

- explicit surface-family declaration
- explicit style affinity
- explicit activation/default policy
- styled proof artifact
- thin-consumer proof
- runtime truth exposure

### 6. What would count as real evidence that analyzer-v2 is now “beautiful by default”?

Not in theory.

In practice.

What would be the right proof standard for that claim?

## Closing Claim

The current system is already good enough to prove bounded semantic ownership across more than one domain shape.

It is not yet good enough to guarantee that a new thin app mixing AOI and genealogy will come out beautifully by default.

The missing work is not mainly in the next app.

It is in analyzer-v2 becoming a stronger presentation platform:

- not just a semantic engine with renderer support
- but a system that emits fully composed reading surfaces as a first-class product
