# Memo: Round 10 / Consumer Consolidation Completion

Date: 2026-03-22
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-22_round10_consumer_consolidation_scope.md`

## Purpose

Record the actual outcome of round 10.

This note closes the gap between:

- the round-10 scope memo
- the implemented package / consumer consolidation seam
- the focused frontend and alignment verification that now exists in the repo

## Bounded Claim Closed In Round 10

Round 10 proved one bounded thing:

- the generic bounded-v2 workspace in the-critic no longer depends on a consumer-owned runtime `init / registry / dispatch` seam for generic renderer resolution, while leaving only explicit local overrides for non-generic exceptions

The required proof surface remained:

- the AOI generic bounded-v2 workspace path

The blocked / deferred surface remained:

- genealogy-specific cleanup and broader sub-renderer-law consolidation

## What Landed

### Shared Package Default Resolution

Round 10 added a narrow top-level default renderer resolver to the shared package:

- `renderers-ui/src/registry.ts`

That resolver now owns the default generic type set used on the bounded-v2 workspace path:

- `prose`
- `raw_json`
- `card_grid`
- `accordion`
- `table`
- `stat_summary`
- `card`
- `timeline` as the existing compatibility alias

The new shared package surface is exported from:

- `renderers-ui/src/index.ts`

Round 10 also aligned the shared top-level renderer prop type with the real consumer path by adding the optional scaffold prop in:

- `renderers-ui/src/types/index.ts`

And it exported the existing scaffold utility helpers that the-critic already expected from the package root.

### the-critic Override Seam

Round 10 removed runtime renderer registration from the live path.

The old imperative seam:

- `initRenderers()`
- mutable type registrations
- mutable view-key registrations

is gone from:

- `AnalysisWorkspacePage.tsx`
- `AoiV2ThematicPanel.tsx`
- `GenealogyPage.tsx`

The deleted file was:

- `the-critic/webapp/src/components/renderers/initRenderers.ts`

The explicit remaining local override seam is now:

- `the-critic/webapp/src/components/renderers/index.ts`
- `the-critic/webapp/src/components/renderers/SubRenderers.tsx`
- `the-critic/webapp/src/components/ViewRenderer.tsx`

The resolution order is now structurally explicit:

1. local view-key override
2. local type override
3. package default top-level renderer
4. local sub-renderer override
5. package sub-renderer
6. prose fallback

That means the-critic no longer acts as the hidden generic authority for the AOI path.

### Remaining Local Debt Stayed Narrow

Round 10 intentionally kept only the local concerns that were still legitimate:

- `genealogy_idea_evolution`
- `genealogy_portrait`
- `nested_sections`
- local sub-renderer compatibility aliases
- local card-cell overrides

This kept genealogy and compatibility debt explicit rather than mixed into the generic runtime path.

### Version / Artifact Alignment

Round 10 closed the version-drift seam between analyzer-v2 package source and the-critic consumption.

The shared package was rolled forward to:

- `@the-syllabus/analysis-renderers@0.6.5`

The-critic now depends on:

- `file:../../analyzer-v2/renderers-ui/release-artifacts/the-syllabus-analysis-renderers-0.6.5.tgz`

Round 10 also added one cross-repo alignment check:

- `python scripts/check_renderer_package_alignment.py`

That check now verifies:

- shared package version
- expected tarball path
- the-critic dependency string
- installed package version under `node_modules`

## Verification

Shared package pack:

- `cd renderers-ui && npm run release:pack`
- result:
  - `the-syllabus-analysis-renderers-0.6.5.tgz` created under `renderers-ui/release-artifacts/`

Cross-repo alignment check:

- `python scripts/check_renderer_package_alignment.py`
- result:
  - package source version, artifact path, the-critic dependency, and installed package version all aligned at `0.6.5`

Script syntax check:

- `python -m py_compile scripts/check_renderer_package_alignment.py`
- result:
  - clean

Focused frontend typecheck:

- `cd /home/evgeny/projects/the-critic/webapp && npx tsc --noEmit --pretty false --incremental false`
- result:
  - clean

Focused frontend regression:

- `CI=true npm test -- --watch=false src/components/renderers/index.test.tsx src/components/ViewRenderer.test.tsx src/components/V2TabContent.test.tsx src/components/influence/AoiV2ThematicPanel.test.tsx src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx`
- result:
  - `6 suites passed`
  - `46 tests passed`

Known non-blocking noise remained:

- existing React `act(...)` warnings in `AoiV2ThematicPanel.test.tsx`
- existing Jest open-handle notice after the focused frontend run

## What Round 10 Now Proves

Round 10 now proves:

1. the shared renderer package can own default top-level generic AOI renderer resolution rather than only individual renderer implementations
2. the-critic no longer needs runtime initialization side effects to make the generic bounded-v2 workspace render
3. the remaining local consumer renderer ownership is explicit and auditable
4. package version/path alignment can be made a hard checked condition instead of an informal assumption
5. the AOI generic workspace path survives the structural change under focused regression and typecheck

## What Round 10 Did Not Prove

Round 10 did not prove:

1. live AOI browser proof capture rerun on the round-5/6 documentary controls
2. genealogy consolidation
3. package-wide top-level registry framework generalization
4. moving `nested_sections` into the shared package
5. broader sub-renderer-law cleanup

The strongest remaining operational follow-up would be:

- rerun a live AOI route proof capture on the documented control jobs and save it as explicit round-10 evidence

## Residual Notes

Two narrow residual risks remain documented:

1. the new shared package registry/export seam is covered indirectly through the-critic tests, but does not yet have package-side unit coverage of its own
2. `scripts/check_renderer_package_alignment.py` is intentionally cross-repo and assumes a sibling `the-critic` checkout plus installed `node_modules`; it is a local workflow guard, not a repo-isolated CI primitive

Neither blocks the bounded round-10 claim.

## Program Position After Round 10

The thin-consumer thesis is materially stronger after round 10.

The repo now has:

- shared backend presentation law from round 9
- shared package-backed default generic renderer resolution from round 10
- explicit local override seams instead of mixed consumer-owned generic runtime registration

That means the next serious move should stay on the same platform path:

- stronger sub-renderer / consumer-law consolidation
- or a bounded compose-from-intent seam

It should not revert to another proof-token round.
