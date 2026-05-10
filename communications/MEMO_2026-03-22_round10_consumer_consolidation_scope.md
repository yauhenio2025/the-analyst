# Memo: Round 10 / Consumer Consolidation Scope

Date: 2026-03-22
Program: Thin Consumer Platformization
Roadmap Reference: `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
Prior Completion: `communications/MEMO_2026-03-21_round9_renderer_contract_validation_completion.md`

## Purpose

Define the next bounded tranche after round 9.

This memo is meant to answer:

1. whether round 10 should follow the roadmap’s consumer-consolidation step
2. what the real consumer-consolidation gap is in the current codebase
3. what bounded proof slice should be used so round 10 stays structural rather than sprawling
4. what should remain blocked so the work does not dissolve into a full webapp rewrite or a disguised compose-from-intent round

## Program Position After Round 9

Round 9 moved the proof ladder to a real platform boundary:

- serve-time renderer contract enforcement exists
- the AOI proof slice survives strict backend renderer law
- the bounded-composition error and trace envelope remains intact
- genealogy strictness was explicitly blocked rather than hand-waved

That matters for roadmap sequencing.

The roadmap memo says that after:

1. declarative substrate proof
2. renderer contract validation

the next serious move should be:

- consumer consolidation

not:

- another proof token
- another bounded adaptive/declarative variant
- immediate broad compose-from-intent work

So round 10 should stay on that roadmap path.

## The Older Vision Framing Is Now Partly Outdated

The large vision memo correctly identified the main thesis:

- the-critic should become a thin consumer shell over analyzer-v2-owned presentation logic and renderer assets

But one part of its renderer-package framing is now stale.

The old formulation said the missing step was:

- publish and install `@the-syllabus/analysis-renderers`

That is no longer the real gap.

Today, the repo state is:

- `the-critic/webapp/package.json` already depends on `@the-syllabus/analysis-renderers`
- the-critic already imports package-owned:
  - styles
  - design-token utilities
  - prose extraction hook
  - several renderer and sub-renderer exports through local wrappers or direct imports
- analyzer-v2 already contains the package source under `renderers-ui/`

So round 10 should **not** be framed as:

- “can the package be published/installed?”

The real question is now:

- can the-critic stop owning the generic renderer path in practice, rather than only in aspiration?

## The Real Contradiction In The Current Codebase

The package is installed, and much of the generic renderer implementation is already package-backed.

So the current gap is not best described as:

- generic renderer bodies are still missing from the package

The more accurate contradiction is:

- the live generic renderer resolver / init / dispatch seam is still consumer-owned
- one real generic renderer seam still remains local
- the package version actually consumed by the-critic is stale relative to the analyzer-v2 source of truth

Current the-critic seam:

- `AnalysisWorkspacePage.tsx` still calls `initRenderers()`
- `V2TabContent.tsx` still renders through local `ViewRenderer`
- `ViewRenderer.tsx` still resolves through a local registry
- `src/components/renderers/index.ts` still owns type/view-key resolution
- `src/components/renderers/initRenderers.ts` still registers the live renderer map
- `src/components/renderers/SubRenderers.tsx` still layers local aliases and fallbacks on top of the package

And the local renderer tree is mixed rather than cleanly gone:

- many generic renderer files are already thin re-export shims for package components
- some files are consumer-owned wrappers around package utilities
- some files still contain real local behavior:
  - `NestedSectionsRenderer.tsx`
  - `IdeaEvolutionRenderer.tsx`
  - `SynthesisRenderer.tsx`

There is also a real package-version drift seam:

- `renderers-ui/package.json` is at `0.6.3`
- the-critic currently resolves `@the-syllabus/analysis-renderers` at `0.5.5`
- the-critic dependency points at a stale tarball path rather than the current package artifact

So the contradiction is not “package absent.”

It is:

- package partially consumed
- consumer-owned generic resolver/init/dispatch still on the critical path
- `NestedSectionsRenderer` and local sub-renderer aliasing still leave real generic behavior in the consumer
- remaining consumer overrides not clearly separated from generic renderer debt
- package-version drift makes the intended source of truth ambiguous

## What Round 10 Should Actually Prove

Round 10 should prove one bounded thing:

- the generic bounded-v2 workspace in the-critic can stop depending on a consumer-owned generic resolver/init seam, while leaving only an explicit, narrow consumer-owned override seam for truly local exceptions

In concrete terms, round 10 should aim to realize:

1. the package becomes the source of truth for the in-scope generic renderer family on the bounded-v2 workspace path
2. the-critic-local generic resolver/init plumbing stops being the hidden owner of generic renderer dispatch
3. remaining local overrides are made explicit as exceptions rather than mixed into the generic renderer registry
4. the package version/path used by the-critic is aligned with the package source actually being consolidated around before closure is claimed

This is a consolidation tranche, not a feature tranche.

## Proposed Bounded Proof Slice

Required proof surface:

- the generic bounded-v2 workspace path in the-critic on the AOI proof slice
- route family already proven in round 9:
  - `adaptive_aoi_theme_report_suite_v1`

Why AOI should be the required slice:

1. round 9 already proved it is the cleanest serve-time enforcement surface
2. it exercises the generic workspace path rather than the bespoke genealogy page
3. it avoids mixing consumer consolidation with the still-open genealogy override and sub-renderer-law questions
4. it lets round 10 prove the thin-consumer thesis on a real live path without reopening blocked architectural debt

Secondary surfaces should be treated as optional follow-on verification only if they fall out naturally.

Round 10 should **not** require:

- removing `GenealogyPage.tsx`
- eliminating genealogy-specific view-key overrides in the same tranche
- lifting genealogy sub-renderer or bespoke renderer behavior into the package

## The Real Scope Question

The real round-10 scope question is not:

- can a few thin wrapper files be deleted?

That would be too small to count as real consolidation.

The real question is:

- does the-critic keep owning the registry/dispatch mechanism while the package provides implementations?
- or does the package absorb more of that registry/dispatch responsibility on the generic bounded-v2 path?

One constraint is already visible in the current code:

- `@the-syllabus/analysis-renderers` does not yet expose a top-level renderer registry API comparable to the-critic’s `registerTypeRenderer`, `registerViewRenderer`, or `resolveRenderer`

So round 10 cannot honestly assume that the local registry simply disappears without an explicit upstream API decision.

## The Likely Structural Move

The likely structural move is not “delete all local renderer files.”

It is:

- make the package authoritative for the generic renderer family used on the bounded-v2 path
- attack the consumer-owned generic resolver/init seam directly
- keep a very small consumer-owned override seam for cases that are truly still local

That probably means the round-10 implementation should trend toward:

1. package-authoritative generic renderer resolution for the in-scope renderer types
2. package-authoritative sub-renderer resolution where the package is already authoritative
3. an explicit consumer override map for remaining view-key exceptions and local compatibility seams
4. removal from the live in-scope path of wrapper files or registrations that are only pass-through ownership noise

What this memo intentionally does **not** decide yet is the exact implementation seam:

- whether the package exports a narrow registry/helper that the-critic consumes
- whether the-critic keeps a thin local registry whose generic entries are package-owned and whose non-generic entries are explicit overrides
- whether `ViewRenderer` remains in the-critic but becomes a thinner host over package helpers

Those are execution-plan questions.

The scope decision is narrower:

- the generic renderer path should stop being implicitly consumer-owned through local resolver/init plumbing

## What Must Stay Out Of Scope

Round 10 should not turn into any of the following:

- a full renderers-ui catalog rewrite
- a package-authoring sweep across every renderer/sub-renderer/cell
- a full removal of all the-critic local renderer files in one tranche
- a bespoke genealogy cleanup round
- a CSS/token redesign round
- a compose-from-intent round
- a generic webapp refactor unrelated to renderer ownership

It should also stay away from a fake consolidation claim where:

- the package is “used” only through unchanged local wrapper/registry ownership
- view-key-specific overrides remain mixed into the same generic registration path
- the version drift between analyzer-v2 package source and the-critic package dependency remains ambiguous

## Hard Stops

Stop and rescope if round 10 starts requiring:

- migration of bespoke genealogy renderers into the shared package
- elimination of `GenealogyPage.tsx`
- consumer-specific UI redesign outside the generic workspace seam
- package ownership of workflow-specific logic rather than renderer logic
- a package API expansion so broad that the tranche becomes an unbounded renderer-framework rewrite

Do not claim round-10 closure unless package-version/path alignment is resolved first:

- the-critic must consume the current intended analyzer-v2 package artifact rather than a stale tarball reference

## Proof Standard

The round-10 proof claim should be concrete and visible.

Closure should require all of the following on the required AOI proof slice:

1. the generic bounded-v2 workspace still renders the AOI control jobs correctly
2. the visible presentations remain equivalent after consolidation
3. the route/trace/error behavior established in round 9 remains unchanged
4. the live in-scope AOI generic renderer path no longer depends on consumer-owned generic registrations as its hidden authority
5. any remaining the-critic-local renderer ownership is explicitly documented as override debt, not silently left inside the generic path
6. the package version/path consumed by the-critic matches the analyzer-v2 package source the tranche claims to consolidate around

The proof should also document:

- which local renderer files were removed from the live path
- which local overrides intentionally remain
- how the resolver/init ownership changed on the in-scope AOI path
- how the package-version drift was resolved

## Why This Is Coherent With The Roadmap

This round is the roadmap’s consumer-consolidation step, but updated to match the real codebase.

It is coherent because:

- round 9 established stronger backend platform law first
- round 10 now attacks the next visible contradiction in the thin-shell thesis
- the work stays on the generic shared workspace path instead of drifting into bespoke workflow UI
- it improves the real consumption boundary before reopening bigger orchestration work

It also prevents a bad pattern:

- claiming analyzer-v2 owns renderer infrastructure while the-critic still owns the practical generic renderer path

## What Comes After Round 10 If It Lands

If round 10 lands cleanly, the next roadmap question becomes sharper:

- is the next move stronger sub-renderer / consumer-law consolidation?
- or is the boundary now clean enough to reopen a bounded compose-from-intent pilot?

Round 10 should therefore be treated as:

- a visible thin-consumer thesis round

not:

- another proof-token branch
