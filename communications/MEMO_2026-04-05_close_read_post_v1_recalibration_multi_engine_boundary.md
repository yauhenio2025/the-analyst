# Memo: Close Read Post-V1 Recalibration

Subtitle: From a bounded genealogy pilot to the first honest multi-engine product boundary

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
Current Product Boundary:
- `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`
Recent Implementation Context:
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/closeReadPresentation.ts`
Primary Codebases:
- `/home/evgeny/projects/analyzer-v2`
- `/home/evgeny/projects/the-critic/webapp`

## Purpose

Record one post-V1 product recalibration after the first bounded `Close Read V1` pilot is now live on Critic:

- what the original Close Read vision actually was
- what the genealogy-first V1 memo intentionally narrowed
- why that narrow cut is proving too weak to stand in for the larger destination
- what the next honest product boundary should be

This memo is not a rejection of the bounded V1 pilot.
It treats that pilot as a successful first corridor proof and asks what broader phase-2 product boundary should come next so the pilot is not mistaken for the whole product.

## Bottom Line

The original `Close Read` vision was never:

- one genealogy reader
- one capture-only operation family
- one fixed cluster of four genealogy surfaces

The original vision was:

- a flagship close-reading app
- over one or more inputs
- with selected or planned engine mixes
- with engine/path-dependent follow-up operations
- with downstream routing into `Research`, `Arsenal`, and later `Book Modeler`

The current genealogy-first `Close Read V1` pilot was still an honest and successful first cut.
But it should now be read correctly:

- it proved a bounded host/runtime/product corridor
- it did **not** prove an adequate product boundary for the larger `Close Read` destination

So the next honest move is no longer to treat genealogy-first `Close Read V1` as if it were the settled product.
The next honest move is to redefine the product boundary as:

- a multi-engine `Close Read` trajectory
- beginning with genealogy plus `Anxiety of Influence`
- while explicitly naming logic/premise-scrutiny and other engine families as intended follow-on admission lines rather than background wishes

## What The Original Vision Actually Says

The strongest broad vision sources are unambiguous.

### 1. analyzer-v2 is supposed to orchestrate many engine families, not one workflow silo

`communications/DYNAMIC_BESPOKE_APPS_VISION.md` defines the core thesis as:

- analyzer-v2 is the brain
- apps are ephemeral presentations

That memo explicitly centers:

- engine selection across the wider catalog
- renderer and sub-renderer selection
- tab/subtab composition
- style-school application
- contextual polishing

The implied destination is not “make one genealogy page nicer.”
It is “compose fit-for-purpose analytical applications over many kinds of engine outputs.”

### 2. the Close Read dictation explicitly names mixed analysis, not genealogy-only reading

`communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md` says the target app should support:

- genealogical analysis
- logical analysis
- `Anxiety of Influence`
- possibly other analysis like webs of relations

It also says the missing layer is:

- follow-up operations over outputs
- path-dependent by engine family

Examples named directly in the dictation:

- test logical premises
- identify weak points
- ask for clarification
- capture
- route to `Research`
- route to `Arsenal`
- later feed `Book Modeler`

That is not a genealogy-only reading memo.
It is a multi-engine product memo in embryonic form.

### 3. the direction-change memo already warned that Close Read is about operation families, not only surfaces

`communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md` says the new missing layer is:

- engine-specific follow-up operations over rendered outputs

It also says the flagship direction should allow:

- selected or planned engine mixes
- rendered analytical interfaces
- engine/path-dependent follow-up work
- downstream routing into `Research`, `Arsenal`, and `Book Modeler`

So the recent genealogy-first cut was always narrower than the intended destination.

## What The Genealogy-First V1 Memo Got Right

The frozen V1 memo was still defensible as a bounded first move.

`communications/MEMO_2026-04-05_close_read_v1_product_memo.md` correctly locked:

- one bounded Critic-hosted pilot posture
- one coherent first surface cluster
- one currently proven routed destination pair
- one explicit app-layer eligibility policy over split substrate

That memo was strategically useful because it stopped the work from dissolving into:

- host redesign
- generic capture-law unification
- multi-user architecture
- generalized destination policy

In other words:

- the pilot memo narrowed aggressively on purpose

That was reasonable for the first implementation slice.

## What The Genealogy-First V1 Memo Intentionally Left Out

The problem is not that the V1 memo was dishonest or strategically wrong.
The problem is that it was easy to over-read once the bounded pilot became the only live `Close Read` page.

In practice, the memo froze all of the following out:

- AOI product inclusion
- findings-bank inclusion
- logic/premise-scrutiny follow-up operation families
- broader non-genealogy engine families

That produced a bounded pilot which is:

- technically coherent
- strategically narrow
- materially thinner than the already-existing genealogy section in Critic by design, because the pilot deliberately filtered to a much smaller view set
- and much weaker than the original multi-engine Close Read vision

So the product risk is now clear:

- if we keep treating the genealogy-first pilot as the product itself, we will optimize a narrow reader shell while drifting away from the actual Close Read destination

## Code-Backed Evidence That The Product Surface Is Broader Than Genealogy

The broader direction is not only aspirational.
There is already real runtime evidence for at least one second engine family.

### 1. AOI already exists as a real result-backed reading/work surface in Critic

`/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx` provides:

- stable AOI routes
- thinker-scoped reading surfaces
- a dedicated `v2-thematic` path

`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx` already carries:

- result discovery
- restore/load behavior
- `CaptureProvider`
- `CaptureActionBar`
- `V2TabContent`
- provenance
- source-backed readiness

So AOI is not hypothetical future material.
It is already a real runtime family on the same host.

That said, AOI evidence does **not** yet equal a settled shared Close Read contract.

The current AOI host path is richer and different from the thin genealogy-first Close Read pilot shell.
It carries its own page behaviors, including summary-card and export-oriented controls, and therefore cannot simply be treated as “already merged into Close Read” without a real product decision about coexistence and shell shape.

### 2. AOI also already has bounded compose-from-intent evidence

`/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentExamples.ts` contains:

- dossier-style AOI compose examples
- comparison-style AOI compose examples

That matters because it shows the product is not only about static genealogy restoration.
There is already live thinking in the codebase around:

- engine-driven AOI page assembly
- different presentation patterns over the same analytical family

### 3. the host contract already names both genealogy and AOI as live workflow families

`/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts` names:

- `intellectual_genealogy`
- `anxiety_of_influence_thematic_single_thinker`

and already treats them as real host-surface families.

So the current product environment is already dual-family at minimum.

### 4. logic/premise-scrutiny is part of the intended product direction even if it is less codified here

The dictation is explicit that:

- in the Benanav/logic-oriented parts, premise scrutiny and weak-point identification are part of the intended follow-up operations

This memo does not claim that that operation family is already codified as cleanly as genealogy or AOI in the present code.

It does claim that:

- logic-oriented follow-up work is part of the intended Close Read destination
- therefore it should be treated as an explicit future admission line, not forgotten because the first pilot happened to start from genealogy

## Recalibrated Product Reading

The correct reading after the current pilot is:

### 1. genealogy-first V1 was a pilot posture, not the product thesis

It proved:

- route
- loading
- filtered presentation
- capture/routing continuity

It did not prove:

- that genealogy alone is the right long-term center of gravity
- that the four frozen genealogy surfaces are sufficient
- that AOI and other engines should remain outside the active Close Read boundary

### 2. the first serious product expansion should be AOI, not more genealogy-only narrowing

AOI should be treated as the first admitted non-genealogy family because:

- it is already live on Critic
- it already has real result-backed reading surfaces
- it already has real capture/routing behavior
- it already has compose-from-intent examples
- it maps directly to the original dictation’s mixed-engine Close Read vision

But AOI should be read as:

- the strongest honest next inclusion line

not as:

- proof that a settled shared multi-engine Close Read shell already exists

### 3. the product should be defined by engine families plus operation families, not by one frozen view list

The correct abstraction is:

- engine/output family
- rendered surface family
- permitted follow-up operation family
- downstream routing family

Not:

- one universal page shell with one universal interaction law

That is exactly what the dictation was pointing toward.

## The First Honest Multi-Engine Boundary

The next product boundary should be framed like this:

### Core included families

- genealogy reading/work family
- `Anxiety of Influence` reading/work family

### Core routed destinations

- `Arsenal`
- `Research todo`

### Core operation law

- baseline family: capture-and-route
- per-family follow-on operations admitted only when the engine/output family and host runtime actually support them

### Explicit near-term future admission lines

- logic / premise-scrutiny family
- additional relation-web / argument-map / other engine families where runtime and product value are real

### Still deferred

- full multi-user architecture
- final standalone-host decision
- generic downstream operation law
- Book Modeler integration as live product behavior
- universal destination-policy convergence

This keeps the product honest while preventing the pilot from ossifying into “genealogy-only Close Read.”

## Practical Consequence

The next product memo should no longer ask:

- how do we polish the genealogy-only pilot a bit more?

It should ask:

- what is the first honest multi-engine `Close Read` boundary after the genealogy pilot proved the host/runtime corridor?

That memo should decide, explicitly:

1. how genealogy and AOI coexist inside one Close Read product
2. what exact engine families are included in that boundary
3. what exact host surfaces/pages carry those families
4. what baseline shared operation law holds across them
5. what family-specific follow-on operations are admitted for each
6. what remains common across families
7. what still stays deferred

## What Should Not Happen Next

Do not do any of the following by default:

- treat the current genealogy-first pilot as if it were already the flagship product
- keep polishing genealogy-only prose fallback while leaving AOI outside the active Close Read definition
- jump straight to “standalone Close Read app” language without first defining a credible multi-engine product boundary
- pretend that because logic/premise-scrutiny is not yet packaged as neatly as genealogy, it is therefore outside the intended Close Read destination

## Recommended Next Memo

The next honest memo should be:

- `Close Read Multi-Engine V1.5 Boundary Memo`

Its job should be to define:

- the exact included engine families
- the exact host surfaces/pages for those families
- the first admitted non-genealogy engine family
- the baseline shared operation law
- the family-specific follow-on operations
- the exact deferred concerns
- the first product boundary that looks recognizably like the originally intended Close Read app rather than only a genealogy proof shell

It should also answer one non-trivial design question directly:

- whether Close Read becomes one umbrella with family-specific pages/shells underneath it, or one more unified shell across admitted families

## Verification Note

This is a docs-and-code recalibration memo.
No tests were run in this memo-writing pass.
