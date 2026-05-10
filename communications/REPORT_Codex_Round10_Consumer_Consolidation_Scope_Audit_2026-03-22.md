Verdict: Approve after revision

## Repo-grounded observations

- The memo is correct that package install is no longer the missing step. `the-critic/webapp/package.json:10` already depends on `@the-syllabus/analysis-renderers`, `the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/package.json:3` shows the app currently running against `0.5.5`, and the app imports package-owned styles and utilities directly in `the-critic/webapp/src/index.tsx:6`, `the-critic/webapp/src/contexts/DesignTokenContext.tsx:1`, `the-critic/webapp/src/hooks/useProseExtraction.ts:1`, and `the-critic/webapp/src/types/styles.ts:1`.

- The analyzer-v2 package source is ahead of the package the consumer is actually pinned to. `renderers-ui/package.json:3` is `0.6.3`, `renderers-ui/release-artifacts/` contains `the-syllabus-analysis-renderers-0.6.3.tgz`, and the `the-critic` dependency still points at `../../analyzer-v2/renderers-ui/the-syllabus-analysis-renderers-0.5.5.tgz`, which is missing in this repo checkout.

- The bounded-v2 generic workspace path is real and live. `the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:22-23,42-43` and `the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:8,20` both call `initRenderers()` before rendering `V2TabContent`.

- Analyzer-v2 already owns a meaningful part of presentation semantics on that path. `the-critic/webapp/src/hooks/useViewDefinitions.ts:1-10,108-160` fetches composed view definitions from analyzer-v2, and `the-critic/webapp/src/components/V2TabContent.tsx:487-521` explicitly treats fresh upstream `renderer_config` as the source of truth for legacy payload rendering.

- The practical renderer resolution seam is still consumer-owned. `the-critic/webapp/src/components/renderers/index.ts:31-69` defines the registry, `the-critic/webapp/src/components/renderers/initRenderers.ts:22-40` populates it, and `the-critic/webapp/src/components/ViewRenderer.tsx:89-176` resolves both top-level renderers and sub-renderers through consumer-local code before any package fallback.

- A large share of the generic implementation is already package-backed, but only through thin local shims. `the-critic/webapp/src/components/renderers/AccordionRenderer.tsx:1`, `CardGridRenderer.tsx:1`, `CardRenderer.tsx:1`, `ProseRenderer.tsx:1-4`, `RawJsonRenderer.tsx:1`, `StatSummaryRenderer.tsx:1`, `TableRenderer.tsx:1`, `ConditionCards.tsx:1`, `EvidenceTrail.tsx:1-2`, and `SubRendererDispatch.tsx:1` are effectively pass-through exports from the package.

- Real consumer-owned renderer logic still exists in three places the memo calls out and one extra seam it should name explicitly:
  - `the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:1-218+`
  - `the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:1-220+`
  - `the-critic/webapp/src/components/renderers/NestedSectionsRenderer.tsx:1-260+`
  - `the-critic/webapp/src/components/renderers/SubRenderers.tsx:10-24`, which adds a local nested-sections adapter and alias mappings on top of the package sub-renderer map

- AOI is a clean bounded slice for consolidation. The AOI surfaces are all generic-view-driven:
  - `src/views/definitions/aoi_thematic_analysis.json:2-41` uses `renderer_type: "tab"`
  - `src/views/definitions/aoi_source_documents.json:2-41` uses `renderer_type: "card_grid"`
  - `src/views/definitions/aoi_by_sin_type.json:2-43` uses `renderer_type: "card_grid"`
  - `src/views/definitions/aoi_by_theme.json:2-90` uses `renderer_type: "accordion"` plus package-style sub-renderers like `annotated_prose`, `rich_description_list`, `chip_grid`, and `mini_card_list`
  - `src/views/definitions/aoi_thematic_report.json:2-85` uses `renderer_type: "accordion"` plus `annotated_prose` and `mini_card_list`

- AOI does not currently depend on view-key overrides. The only view-key registrations in the live consumer registry are `genealogy_idea_evolution` and `genealogy_portrait` in `the-critic/webapp/src/components/renderers/initRenderers.ts:37-39`.

- Genealogy remains override-heavy and should stay out of scope. `src/views/definitions/genealogy_idea_evolution.json:2-51` and `src/views/definitions/genealogy_portrait.json:2-37` are exactly the two views that the consumer registry overrides by view key, and `src/views/definitions/genealogy_conditions.json:22-69` still depends on specialized sub-renderer types like `enabling_conditions`, `constraining_conditions`, `timeline_strip`, `move_repertoire`, and `prose_block`.

- The genealogy fallback path is still a drift seam of its own. `the-critic/webapp/src/pages/GenealogyPage.tsx:2061-2198` carries a hardcoded `LEGACY_VIEWS` map, and its fallback `conditions` config does not even match the current analyzer-v2 definition exactly: `alternative_paths` is rendered as `mini_card_list` in the fallback (`GenealogyPage.tsx:2158-2160`) but as `move_repertoire` in the upstream definition (`src/views/definitions/genealogy_conditions.json:52-59`).

- The package is not yet ready to replace the consumer registry outright. `renderers-ui/src/index.ts:4-11` claims the package provides a renderer registry, but the actual public API exports only container renderers, sub-renderers, dispatch helpers, cells, tokens, and hooks (`renderers-ui/src/index.ts:46-85`). There is no exported package-level `registerTypeRenderer`, `registerViewRenderer`, or `resolveRenderer`.

## Findings

### 1. The memo identifies the right contradiction, but it should name the seam more precisely.

The real contradiction is not "package components are absent." The repo already uses the package heavily. The contradiction is that the consumer still owns generic renderer resolution, initialization, and a thin compatibility layer even where the actual renderer bodies come from analyzer-v2.

That distinction matters because a round-10 plan can appear to "consolidate" by deleting a few wrapper files while leaving the real ownership seam unchanged in:

- `the-critic/webapp/src/components/renderers/index.ts:31-69`
- `the-critic/webapp/src/components/renderers/initRenderers.ts:22-40`
- `the-critic/webapp/src/components/ViewRenderer.tsx:89-176`
- `the-critic/webapp/src/components/renderers/SubRenderers.tsx:19-24`

Revision needed: the memo should say that round 10 must attack the consumer-owned generic resolver/init seam, not merely consumer-local wrapper files.

### 2. "Package install is no longer the missing step" is correct, but the memo understates the version-alignment problem.

The package is installed and in use, so publication is not the main scope question anymore. But version drift is not a cosmetic footnote:

- source package version is `0.6.3` in `renderers-ui/package.json:3`
- checked-in consumer install is `0.5.5` in `the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/package.json:3`
- consumer dependency points at a missing `0.5.5` tarball in `the-critic/webapp/package.json:10`

That means the current setup has a reproducibility problem and an ambiguous source of truth problem. Even if the app works in this checkout, a fresh install would not be aligned to the package source the repo is supposedly consolidating around.

Revision needed: version/path alignment should move from "also document whether resolved" to an explicit round-10 closure condition.

### 3. The memo is right that AOI is the correct bounded proof slice.

AOI uses the generic bounded-v2 workspace, generic renderer types, and package-backed sub-renderers. It does not require the genealogy-only view-key overrides that still live in the consumer registry.

That makes AOI the right consolidation surface because it tests the shared workspace path without reopening the currently separate genealogy debts:

- no AOI view-key registrations in `initRenderers.ts:37-39`
- AOI definitions stay within `tab`, `card_grid`, `accordion`, and package-backed sub-renderers in the AOI view definition files listed above
- AOI already has the strongest recent proof trail from round 9

I approve the memo on this point.

### 4. The memo is right to keep genealogy-specific overrides out of scope.

Genealogy is not just "one more consumer override." It is still architecturally different:

- top-level view-key override for `genealogy_idea_evolution`
- top-level view-key override for `genealogy_portrait`
- specialized sub-renderer usage in `genealogy_conditions`
- hardcoded `GenealogyPage` fallback config when upstream definitions are unavailable

Pulling genealogy into round 10 would turn a bounded consolidation tranche into a renderer-framework rewrite plus a bespoke workflow cleanup round. The memo's out-of-scope line is correct and should remain hard.

### 5. This is a real bounded consolidation round, not a disguised framework rewrite, if execution stays narrow.

I would approve the round as bounded only if the implementation target is:

- package-authoritative generic renderer resolution for the AOI in-scope types
- an explicit, minimal consumer override map for true exceptions
- package version/path alignment
- removal of thin generic wrapper ownership from the live AOI path

I would not approve a plan that tries to do any of the following in the same tranche:

- move genealogy bespoke renderers upstream
- invent a broad runtime renderer framework
- generalize every alias and legacy compatibility edge case
- rewrite `V2TabContent` or the whole consumer presentation shell

So the memo's scope is coherent, but only if the implementation plan stays narrower than the memo's aspirational wording.

### 6. The biggest execution trap is that the package does not yet expose the top-level API the memo implicitly points toward.

The package exports renderer components and sub-renderer helpers, but not a top-level generic renderer registry. So the eventual implementation plan has only two realistic bounded options:

1. add a narrow package API for in-scope generic resolution, or
2. keep a very thin consumer registry whose generic entries are package-owned and whose remaining non-generic entries are explicit overrides

What is not realistic in one bounded round is claiming that the consumer registry simply disappears without adding any upstream API.

This is the main revision the memo still needs before planning.

### 7. There is a second execution trap: some "generic" debt is not on the AOI proof path and should not be silently pulled into scope.

The local `NestedSectionsRenderer` and the alias logic in `SubRenderers.tsx` are genuine consumer-owned rendering behavior, but they are not required to prove AOI consolidation. If the plan tries to upstream all of that now, the round expands immediately.

The safe move is:

- keep AOI as the required path
- explicitly mark `nested_sections` and alias compatibility debt as follow-on unless the AOI path requires them

### 8. The proof standard is close, but it is not yet strong enough to rule out cosmetic import churn.

The current proof standard is good on behavioral equivalence:

- AOI still renders correctly
- visible output stays equivalent
- trace/error behavior from round 9 stays intact

But it needs one additional ownership-level proof:

- the in-scope AOI generic types must stop resolving through consumer-owned generic registrations in `initRenderers.ts`

Otherwise a plan could satisfy the memo by deleting some pass-through wrapper files while leaving `AnalysisWorkspacePage` and `AoiV2ThematicPanel` dependent on the same local registry/init seam.

I would strengthen closure to require:

- evidence that AOI generic types no longer depend on consumer generic registrations
- evidence that the remaining consumer-local registrations are only explicit overrides
- evidence that the package version/path mismatch has been resolved

## Bottom line

The memo has the right next move. The real post-round-9 contradiction is consumer ownership of the practical generic renderer seam, not package absence, and AOI is the correct bounded slice for proving that seam can be consolidated without reopening genealogy.

I do not recommend changing the round direction. I do recommend revising the memo before implementation planning so it states three things more explicitly:

1. round 10 is about the consumer-owned generic resolver/init seam, not just wrapper deletion
2. package version/path alignment is a required closure item, not an optional note
3. the package does not yet expose a top-level generic registry API, so the plan must either add one narrowly or keep a thin local registry with only explicit overrides

With those revisions, this remains a real bounded consolidation round rather than a disguised framework rewrite.
