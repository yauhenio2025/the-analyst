# Memo: Close Read Multi-Engine V1.5 Coexistence Scope

Subtitle: Implement the first bounded `Close Read` umbrella over genealogy and AOI without forcing a premature unified shell

Date: 2026-04-05
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Current Product Boundary:
- `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`
Immediate Prior Boundary Freeze:
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
Primary Runtime Evidence:
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/closeReadPresentation.ts`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/AppLayout.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
Primary Codebases:
- `/home/evgeny/projects/analyzer-v2`
- `/home/evgeny/projects/the-critic/webapp`

## Purpose

Implement the first bounded coexistence tranche implied by the new multi-engine `Close Read V1.5` boundary.

This scope is not:

- a standalone-host move
- a generic multi-engine shell unification project
- a reopening of whether AOI belongs in `Close Read`
- a reopening of whether AOI compose-from-intent belongs in `Close Read`

It exists to make the new product law real in code:

- `Close Read` becomes the umbrella identity
- genealogy and AOI coexist beneath that umbrella
- the baseline shared law stays:
  - result-backed reading/work
  - provenance
  - capture mode
  - capture-and-route into `Arsenal` / `Research todo`
- family-specific shells remain family-specific

## Scope Summary

This tranche should add:

- one umbrella landing page at `/p/:projectId/close-read`
- one genealogy family page at `/p/:projectId/close-read/genealogy`
- one AOI family index at `/p/:projectId/close-read/aoi`
- one thinker-scoped AOI family page at `/p/:projectId/close-read/aoi/:thinkerId`

This tranche should preserve:

- the existing native genealogy route:
  - `/p/:projectId/genealogy`
- the existing native AOI routes:
  - `/p/:projectId/anxiety-of-influence`
  - `/p/:projectId/anxiety-of-influence/:thinkerId/...`

This tranche should not implement:

- AOI compose-from-intent under `Close Read`
- hypotheses/report/legacy thematic AOI surfaces under `Close Read`
- logic / premise-scrutiny family admission
- a full route migration away from native genealogy or AOI

## Product-Law Inputs Treated As Frozen

These are already decided and must not be reopened here:

- `Close Read` is umbrella identity
- admitted families are:
  - genealogy
  - `anxiety_of_influence_thematic_single_thinker`
- AOI admission level is:
  - result-backed thematic reading/work only
- shared baseline destinations remain:
  - `Arsenal`
  - `Research todo`
- standalone-host questions remain deferred

## Concrete Route Behavior

This memo freezes the route behavior that the boundary memo intentionally left for implementation.

### 1. Umbrella entry route

`/p/:projectId/close-read` becomes the **stable umbrella landing page**.

It should not:

- auto-redirect to genealogy
- auto-redirect to AOI
- remember-last-family in V1.5

This is deliberate.
The umbrella route must become a stable product identity, not only a pass-through alias to the older genealogy pilot.

#### Backward compatibility for old genealogy pilot deep links

The old genealogy pilot lived at:

- `/p/:projectId/close-read`

and it supported root-level genealogy tab deep links such as:

- `/p/:projectId/close-read?tab=...`

For V1.5, those old root deep links should receive a bounded compatibility redirect to:

- `/p/:projectId/close-read/genealogy?tab=...`

This is the one compatibility exception to the new umbrella landing behavior.

Reason:

- old shared links should not silently lose their tab meaning
- but the root route should still become the stable umbrella identity for fresh navigation

### 2. Family child routes

Use these child routes:

- `/p/:projectId/close-read/genealogy`
- `/p/:projectId/close-read/aoi`
- `/p/:projectId/close-read/aoi/:thinkerId`

No extra admitted `Close Read` family routes in V1.5.

### 3. Genealogy family route behavior

`/p/:projectId/close-read/genealogy` should host the existing bounded genealogy `Close Read` reader, migrated out of the umbrella root.

It should preserve:

- current filtered genealogy view logic
- current result-backed boot behavior
- current `?tab=` sync behavior
- current capture/provenance shell

It should not widen into:

- full genealogy workspace parity
- run/import/progress UI

### 4. AOI family route behavior

`/p/:projectId/close-read/aoi` becomes the AOI family index within `Close Read`.

Its job is to show:

- all AOI thinkers already known on the current project
- one status per thinker:
  - usable for `Close Read`
  - not yet usable for `Close Read`

The AOI family index should therefore list **all** AOI thinkers, not only the usable subset.

Usable thinkers get:

- a primary CTA into `/p/:projectId/close-read/aoi/:thinkerId`

Unusable thinkers get:

- a bounded disabled/empty state explaining that the thematic/result-backed AOI surface is not yet available under `Close Read`

Selecting a thinker goes to:

- `/p/:projectId/close-read/aoi/:thinkerId`

`/p/:projectId/close-read/aoi/:thinkerId` renders the AOI thematic family page inside the `Close Read` umbrella context.

In V1.5, that page should expose only the admitted AOI surface:

- result-backed thematic reading/work

Under the `Close Read` umbrella, the AOI thinker route is therefore a **fixed thematic route**, not a mini copy of the native AOI tab family.

That means:

- `v2-thematic` behavior is the only admitted AOI page mode under `/close-read/aoi/:thinkerId`
- native AOI tab-family behavior is **not** preserved under the umbrella route for:
  - `hypotheses`
  - `legacy-thematic`
  - `report`
- if users need those broader AOI tabs, they should stay on the native `/anxiety-of-influence/...` routes in V1.5

It should not expose, inside `Close Read`:

- hypotheses
- report
- legacy thematic
- compose-from-intent

### 5. What happens when only one family is usable

`/p/:projectId/close-read` should still render the umbrella landing page even if only one family currently has usable results.

It should not auto-redirect.

Instead:

- the usable family card should render as active with a primary CTA
- the unavailable family card should render with a bounded explanatory empty/disabled state

This keeps:

- umbrella identity stable
- route behavior predictable
- family availability visible instead of silently inferred by redirect

### 6. Deep-link behavior for unavailable family routes

If a user deep-links into an unavailable family route:

- `/p/:projectId/close-read/genealogy`
- `/p/:projectId/close-read/aoi`
- `/p/:projectId/close-read/aoi/:thinkerId`

the page should show a bounded family-specific unavailable state with:

- a short explanation
- a link back to `/p/:projectId/close-read`
- where appropriate, a link to the existing native family route

Do not silently redirect from an unavailable family route in V1.5.

## Movement Between Umbrella And Family Pages

### Umbrella landing page

The landing page should present two family cards:

- Genealogy
- Anxiety of Influence

Each card should show:

- short family description
- current availability status
- primary CTA into the family route

Optional but acceptable if easy:

- latest usable result timestamp
- latest thinker/result label

### Family switcher on child pages

Every child page under `/close-read/*` should show a small umbrella-local family switcher:

- Genealogy
- Anxiety of Influence

That switcher should navigate between:

- `/p/:projectId/close-read/genealogy`
- `/p/:projectId/close-read/aoi`

This is not the global app nav replacement.
It is the local navigation inside the new `Close Read` umbrella.

### Relationship to native routes

The native routes remain live and unchanged in V1.5.

This tranche may add small secondary links such as:

- `Open full Genealogy workspace`
- `Open full AOI workspace`

But those links are optional.
The required behavior is coexistence, not route migration.

## Stateful Remount Guard

The implementation must carry forward the same state-isolation pattern that the genealogy pilot already needed:

- stateful umbrella and family page bodies should remount on identity changes rather than leaking state across project or thinker transitions

At minimum:

- the umbrella landing page body should key on `projectId`
- the genealogy family page body should key on `projectId`
- the AOI family index body should key on `projectId`
- the AOI thinker page body should key on `projectId + thinkerId`

This is required because the existing V1 genealogy page already proved that Critic route transitions can keep stateful bodies mounted while params change.

## Shared Shell Decisions For V1.5

The new umbrella should unify only the baseline shared shell:

- page title / intro
- family cards / landing
- family switcher
- provenance visibility
- capture mode presence
- `CaptureActionBar`

It should not force one unified page body across genealogy and AOI.

That means:

- genealogy keeps its bounded reader shell
- AOI keeps its thematic/result-backed shell
- the umbrella provides a shared frame above them

## Genealogy Family Implementation Notes

The current `CloseReadPage` implementation should be treated as the starting point for:

- `/p/:projectId/close-read/genealogy`

Expected work:

- move or wrap the current genealogy pilot so it no longer owns the umbrella root route
- preserve current boot/result qualification rules
- preserve current filtered surface set
- preserve current capture and provenance behavior
- preserve bounded compatibility for old root `?tab=` deep links by redirecting them to `/close-read/genealogy?tab=...`

Out of scope:

- rethinking the genealogy surface whitelist
- more fallback shaping work unless required for regression safety

## AOI Family Implementation Notes

AOI admission in V1.5 should be anchored to:

- result-backed thematic reading/work on the existing AOI runtime path

Expected work:

- create a `Close Read` AOI family page/index that discovers usable thinker-scoped AOI thematic results
- create a thinker-scoped child page under the umbrella
- reuse the current AOI thematic runtime where possible
- suppress or omit non-admitted AOI controls inside `Close Read`
- keep the `Close Read` thinker route fixed to thematic/result-backed behavior only; do not reproduce the native AOI tab family under the umbrella

Important:

- do not treat AOI admission as license to import the full AOI section unchanged
- do not add compose-from-intent links/buttons under `Close Read`

## Route And Nav Wiring

Expected route updates:

- keep `/p/:projectId/close-read` but change it from genealogy page to umbrella landing page
- add:
  - `/p/:projectId/close-read/genealogy`
  - `/p/:projectId/close-read/aoi`
  - `/p/:projectId/close-read/aoi/:thinkerId`

Expected nav updates:

- keep `Close Read` in the `Synthesis` nav
- `Close Read` should point to the umbrella landing page
- do not remove:
  - `Anxiety of Influence`
  - `Intellectual Genealogy`
  from nav in this tranche

## Public Interface Changes

Public-facing additions in Critic:

- `Close Read` umbrella landing behavior at `/p/:projectId/close-read`
- two new umbrella child families:
  - `/p/:projectId/close-read/genealogy`
  - `/p/:projectId/close-read/aoi`
- thinker-scoped AOI child route:
  - `/p/:projectId/close-read/aoi/:thinkerId`

Public-facing non-changes:

- existing native genealogy and AOI routes remain live
- no analyzer API/schema change
- no package-level `renderers-ui` change

## Test Plan

### Route and landing tests

- `/p/:projectId/close-read` renders landing page, not genealogy content directly
- landing page shows both family cards
- when only one family is usable, landing page remains stable and does not redirect
- `Close Read` nav item lands on the umbrella route

### Genealogy family tests

- `/p/:projectId/close-read/genealogy` preserves the current bounded genealogy reader behavior
- current genealogy `?tab=` behavior still works under the new family route
- unavailable genealogy route shows a bounded family-specific unavailable state rather than silent redirect

### AOI family tests

- `/p/:projectId/close-read/aoi` lists usable AOI thinkers/results
- selecting a thinker goes to `/p/:projectId/close-read/aoi/:thinkerId`
- thinker page renders the thematic/result-backed AOI surface inside `Close Read`
- hypotheses/report/legacy thematic controls do not appear under the umbrella route
- compose-from-intent entry points do not appear under the umbrella route
- unavailable thinker route shows a bounded unavailable state rather than silent redirect

### Shared baseline tests

- provenance remains available on both family pages where already supported
- capture mode and `CaptureActionBar` remain available on both family pages where results are present
- routed destination baseline remains `Arsenal` / `Research todo`

### Regression reruns

- current Close Read genealogy tests
- AOI thematic result-backed tests
- capture/provenance support tests already backing both families

## Out Of Scope

- AOI compose-from-intent inside `Close Read`
- hypotheses/report/legacy thematic AOI pages inside `Close Read`
- logic / premise-scrutiny family admission
- family-neutral unified shell/body
- native route removal or migration
- destination-policy convergence beyond current `CaptureActionBar`
- standalone-host movement

## Success Criteria

This slice is successful only if:

- `/p/:projectId/close-read` becomes a real umbrella landing page
- users can move from umbrella to genealogy and AOI family pages without ambiguity
- genealogy remains functional under the new child route
- AOI thematic reading/work becomes available under the umbrella without importing the full AOI app estate
- native genealogy and AOI routes remain intact
- the shared baseline law is preserved
- the tranche does not reopen product-boundary questions that the two product memos already froze

## Immediate Follow-On If This Scope Lands Cleanly

If this coexistence tranche lands cleanly, the next honest question is no longer route coexistence.
It becomes one of:

- whether AOI admission should deepen beyond thematic/result-backed reading
- whether logic / premise-scrutiny becomes the next admitted family
- or whether the umbrella has enough real product value to justify a stronger host-level consolidation step

## Verification Note

This is a scope memo only.
No tests were run in this memo-writing pass.
