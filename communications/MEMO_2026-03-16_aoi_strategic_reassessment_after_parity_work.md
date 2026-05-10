# Memo: AOI Strategic Reassessment After Parity Work

Date: 2026-03-16

## Purpose

This memo reassesses the AOI program after the last 48 hours of work across:

- `analyzer-v2`
- `the-critic`
- `analyzer-mgmt`

It is meant to answer:

- what the recent AOI work actually changed
- how AOI now fits the broader platform story
- what has become easier as a result
- what still prevents AOI-style apps from being beautiful by default
- what the next program should focus on

This is a strategic reassessment, not a narrow implementation note.

## Executive Judgment

The most important change is this:

- AOI is no longer best understood as a bespoke Critic subsystem with a partial analyzer-v2 experiment beside it

It is now better understood as:

- a real analyzer-v2 capability family
- with a bounded but genuine objective/workflow/operationalization/view stack
- consumed on the live Critic hot path
- inspectable in analyzer-mgmt on substantially the same capability-first footing as genealogy

That is a meaningful architectural shift.

The right summary is:

- AOI is now much closer to **predictable-by-default**
- AOI is **not yet beautiful-by-default**

That distinction matters.

The packaging and hot-path work we just completed makes AOI-style apps much easier to build without downstream semantic repair.

It does **not** yet mean that a new thin consumer will automatically emerge with a highly composed, elegant interface from generic renderer defaults alone.

## The 48-Hour Arc

### 1. March 15 proved bounded semantic ownership outside genealogy

The March 15 memos established the first real bounded proof that the March 13 direction was not genealogy-only.

AOI plus the canary demonstrated that `analyzer-v2` could own a different semantic shape:

- source corpus vs subject corpus
- stable source-document identity
- theme-led navigation
- AOI sin regrouping
- bounded thematic report synthesis

The canary additionally proved that a thin consumer could render AOI without becoming a semantic co-author.

That was the first serious app-agnosticism proof outside The Critic's original bespoke surfaces.

### 2. March 16 shifted the question from existence to parity

Once the bounded proof was established, the next question became:

- is AOI merely present in analyzer-v2, or is it packaged with the same kind of abstraction depth and live-path seriousness as genealogy?

The parity reviews were useful because they separated three different concerns that had been blurred together:

- runtime execution significance
- management/discovery visibility
- presentation quality

That led to a better diagnosis:

- AOI's old problem was not "no engines"
- it was incomplete packaging and incomplete adoption on the live path

### 3. The implementation work closed most of the real packaging gap

The recent tranche materially changed the platform status of AOI:

- AOI now has a bounded objective
- AOI now has four real operationalizations
- capability-only engines are now first-class on browse/admin surfaces
- AOI now has a live Critic v2 thematic surface instead of only a backend possibility
- analyzer-mgmt can now inspect AOI engines and operationalized pass structure without treating them as second-class

This is the point where AOI stopped being mainly a special case and became a serious platform capability.

## What Was Actually Improved

### 1. AOI now has a real analyzer-v2 capability package

In practical terms, AOI now has:

- a canonical bounded workflow
- a bounded objective
- capability definitions for its thematic engines
- operationalization files for those engines
- a presenter-native view family

That gives AOI a platform-owned analytical package, not just app-owned logic.

The important shift is not that files now exist.

The shift is that AOI semantics are now represented in the same kinds of upstream artifacts the platform already used for more mature capability families.

### 2. AOI is now much more execution-connected

Previously, one could still describe AOI in analyzer-v2 as:

- semantically interesting
- partially demonstrable
- but not the main live path

That is no longer the right description.

The Critic now has a real AOI v2 thematic route and presenter path.

So AOI is no longer only something that can be run in principle through analyzer-v2.

It is now something the live app can actually consume as analyzer-v2 output.

That matters because platform abstractions only become strategically trustworthy once they survive real user-facing handoff.

### 3. analyzer-mgmt is now a more honest window into the capability system

Before the recent engine packaging work, capability-only engines were second-class on the most obvious management surfaces.

That created a mismatch:

- the planner and executor could already see capability definitions
- but the ordinary engine browse/detail/admin surfaces still behaved as if legacy JSON engines were the main truth

The discoverability tranche fixed much of that mismatch.

That means analyzer-mgmt is now closer to what it should be:

- a generic management surface over analyzer-v2 capability families

not

- a genealogy-shaped browser that only accidentally tolerates newer engine families

### 4. AOI packaging is now more reusable across apps

This is the most important forward-looking consequence.

Because AOI now has stable upstream workflow/objective/operationalization/view artifacts, a new app can consume AOI in a much thinner way than before.

The app no longer needs to:

- rediscover the AOI semantic phases locally
- invent its own pass story
- invent its own result grouping logic
- reconstruct the same page structure from raw phase outputs

Instead, it can increasingly consume:

- a bounded workflow
- a `PagePresentation`
- a stable view family
- stable source-document and theme identities

That is exactly the kind of upstream semantic ownership the March 13 direction was aiming for.

## How The Four Systems Now Relate

### analyzer-v2

`analyzer-v2` is increasingly the source of truth for:

- AOI workflow semantics
- AOI objective framing
- AOI operationalization depth
- AOI view composition intent
- AOI presentation payloads

This is the main strategic gain.

### The Critic

`the-critic` is still the richest live AOI app surface, but it is becoming more of a consumer and less of a semantic monopolist.

That means:

- The Critic still owns product flow and local UX conventions
- but it increasingly does not need to own AOI meaning from scratch

That is a healthier boundary than before.

### analyzer-mgmt

`analyzer-mgmt` is now closer to a generic capability-management console over analyzer-v2 definitions.

It still does not execute analyses itself.

But it now does a better job of exposing the same capability families that the platform actually knows how to run.

### Thin Consumers / Future Apps

Thin consumers are where the strategic payoff appears.

The canary proved one thing:

- analyzer-v2 can already drive a second AOI-shaped app without that app becoming a semantic co-author

The newer packaging work improves the next version of that claim:

- future AOI-like apps can be thinner, more predictable, and more maintainable than before

## What This Means For Building Future AOI-Style Apps

## Short Answer

Yes, it is now materially easier to build an app such as AOI and have it render in a more predictable way.

No, it is not yet safe to assume such an app will be beautiful by default.

## Why Predictability Is Better Now

Predictability improved because the upstream contracts are better.

The platform now has stronger answers to questions like:

- what is the canonical AOI workflow?
- what are the AOI engines?
- what depth sequences should they run at?
- what stable identifiers should findings and source documents carry?
- what page surface should the presenter target?
- what view family should represent the result?

Those answers used to be split across:

- bespoke Critic logic
- partial analyzer-v2 AOI work
- renderer-specific experiments

Now they are much more centralized.

That means a future AOI-like app is less likely to suffer from:

- semantic drift between backend and frontend
- ad hoc regrouping logic
- inconsistent result shapes
- duplicated AOI-specific interpretation code

## Why Beauty Is Still Not Automatic

This is the key constraint.

The March 16 memo on beautiful-by-default surfaces remains substantially correct:

- the platform is now a strong semantic engine
- it is only a medium-strength composition platform

The main remaining presentation limitations are:

### 1. Most live AOI views still rely on curated view JSON plus generic renderer defaults

That means the system is still heavily dependent on hand-authored view composition rather than a stronger transformation/pattern pipeline.

### 2. Transformations are still under-activated

The transformation layer exists, but most live views still reach the renderer path with `transformation.type = "none"`.

So the final display often depends on:

- careful view authoring
- careful renderer config

rather than a stronger platform-level shaping layer.

### 3. Dynamic composition exists in archaeology, not yet as the normal law of the system

The dynamic composition audit already showed that some of the more advanced composition machinery is:

- built
- partially wired
- but still disabled, under-consumed, or write-only

So the platform has more composition machinery than it currently uses.

### 4. AOI still has no dedicated chain layer

This is not a crisis for the bounded thematic tranche.

The current four-phase AOI workflow can run as standalone operationalized engines, which is good enough for the current proof and live path.

But it does mean AOI is still less compositionally rich than genealogy in one important way:

- genealogy has chain-level composition as part of its mature packaging story
- AOI still does not

That does not block usability.

But it does mean AOI is still the simpler packaged family, not the most compositional one.

## So What Did We Really Buy?

The cleanest statement is this:

We have not yet made AOI beautiful by default.

We have made AOI much less bespoke, much more platform-owned, and much more predictable to deliver.

That is a major improvement because predictability is the prerequisite for beauty at platform scale.

Without stable packaging, every app has to repair meaning locally.

With stable packaging, beauty becomes a presentation-composition problem rather than a semantic-reconstruction problem.

That is exactly the transition we wanted.

## Strategic Reframing

The program should now be described this way:

### What was Phase 1?

Phase 1 was:

- prove AOI can exist as a real analyzer-v2 semantic surface

That has been done.

### What was Phase 2?

Phase 2 was:

- close enough of the packaging and hot-path gap that AOI stops being a platform exception

That is now mostly done as well.

### What is Phase 3?

Phase 3 should be:

- turn predictable AOI surfaces into beautiful-by-default AOI surfaces
- without re-bespoking the downstream apps

That means the next serious work should move upward into:

- transformation shaping
- pattern authority
- renderer-facing surface families
- optional refinement/reactivation where bounded and safe
- stronger presentation contracts for grouped cards, report sections, theme-led comparisons, and other recurring AOI/genealogy surface types

## Recommendations

### 1. Stop framing AOI as the "missing platform child"

That is no longer true in the old sense.

AOI is not fully mature, but it is now firmly inside the shared platform model.

### 2. Treat the current AOI work as a foundation, not the end-state

The objective/operationalization/hot-path tranche was necessary because it moved AOI from:

- interesting bounded proof

to

- reusable platform capability

But that is still infrastructure, not final composition quality.

### 3. Make the next tranche presentation-platform work, not more AOI-specific plumbing

The next serious leverage is unlikely to come from adding more AOI-specific files alone.

The higher-value work is to make the platform better at producing composed surfaces from these now-stable semantic packages.

### 4. Keep chains optional until a real AOI compositional need appears

AOI does not need chains merely to imitate genealogy.

If chains appear, they should appear because AOI genuinely needs a richer composition layer, not because parity language makes their absence feel embarrassing.

### 5. Use the phrase "predictable-by-default before beautiful-by-default"

That is the right strategic description of the current state.

It is honest about what is now strong.

It is also honest about what is still missing.

## Final Assessment

Over the last 48 hours, AOI has crossed an important threshold.

It is no longer just:

- a bespoke Critic feature
- or a bounded analyzer-v2 curiosity

It is now:

- a serious platform-owned capability family
- live enough to trust
- packaged enough to reuse
- inspectable enough to manage

That does not yet mean every future AOI-like app will look excellent with minimal effort.

But it does mean future AOI-like apps can now be built on a far more stable foundation.

That is a significant strategic gain.

The next frontier is no longer:

- can analyzer-v2 own AOI meaning?

The next frontier is:

- can analyzer-v2 turn platform-owned meaning into platform-owned composition quality?
