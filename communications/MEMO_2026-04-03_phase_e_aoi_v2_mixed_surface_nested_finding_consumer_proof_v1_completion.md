# Memo: Phase E AOI V2 Mixed-Surface Nested Finding Consumer Proof V1 Completion

Subtitle: One bounded Critic-side mixed AOI surface now consumes generic whole-view first-hop truth plus nested `finding_id` to create correct thematic finding captures without widening analyzer semantics

Date: 2026-04-03
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Most Recent Prior Code Completion:
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_completion.md`
Immediate Prior Scope:
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_scope.md`
Review Context:
- `communications/REPORT_Codex_Phase_E_AOI_V2_Mixed_Surface_Nested_Finding_Consumer_Proof_V1_Scope_Audit_2026-04-03.md`
- `communications/REPORT_Claude_Phase_E_AOI_V2_Mixed_Surface_Nested_Finding_Consumer_Proof_V1_Scope_Critique_2026-04-03.md`
Host Codebase:
- `/home/evgeny/projects/the-critic`

## Purpose

Record what actually landed in the bounded Critic-side mixed-surface consumer slice on AOI `aoi_by_theme`.

This memo is about one current mixed AOI V2 surface:

- findings-bearing `accordion`
- nested `findings -> mini_card_list`
- generic whole-view `FirstHopAffordance`
- nested per-card `finding_id`

It is not a claim that:

- generic renderer-package capture law now exists
- all `aoi_by_theme` adaptive families are now in scope
- mixed-surface status surfacing is now solved
- analyzer-v2 needed new semantics for `aoi_by_theme`
- non-AOI generality has now been proven

## What Landed

One bounded Critic-side mixed-surface consumer slice is now complete on `aoi_by_theme`.

The landed behavior is:

1. Critic now has a local dispatcher override for `aoi_by_theme`
2. that dispatcher activates only on the findings-bearing family:
   - `view_key = "aoi_by_theme"`
   - `renderer_type = "accordion"`
   - object payload with `_section_order` and `_section_titles`
   - configured nested `findings -> mini_card_list`
   - at least one ordered theme section carrying a `findings` array
3. out-of-scope adaptive families, including the comparison-review `table` variant, fall through unchanged to the shared default renderer
4. the in-scope path uses a minimal local accordion shim rather than a full bespoke surface fork
5. nested thematic findings now show bounded capture controls only when all are true:
   - capture mode is on
   - generic whole-view `FirstHopAffordance.capturable === true`
   - required threaded host config is present
   - the individual finding card has a non-empty `finding_id`
6. clicking a nested finding now creates a correct `CaptureSelection` with:
   - `source_renderer_type = "mini_card_list"`
   - `entity_id = finding_id`
   - `source_workflow_key = _workflowKey`
   - 0-based section-local `source_item_index`
   - theme-keyed `parent_context`
7. non-findings subsections remain passive
8. outside capture mode, or when nested `finding_id` is absent, the surface stays readable and passive

## Final Boundary

The honest completed claim is:

- one current mixed AOI V2 surface can now consume the already-landed analyzer contract on nested findings without requiring mixed-surface `specialized_family`
- the proof works on generic whole-view `capturable` plus nested `finding_id`
- the proof remains local to the findings-bearing `accordion` family and does not overclaim the out-of-scope comparison-review `table` family

What this does not mean:

- generic sub-renderer injection law now exists in the shared renderer package
- generic mixed-surface status/read-back law now exists
- `aoi_by_theme` is now a whole-view findings-bank surface
- non-AOI surfaces are now proven
- end-to-end destination lifecycle or repeat-capture policy are now solved

## Implementation Shape

The implementation stayed inside Critic.
No analyzer-v2 runtime code changed.
No backend code changed.

The landed shape is:

- one local dispatcher override for `aoi_by_theme`
- one strict structural family gate
- one minimal local accordion shim
- one local thematic-section sub-renderer token
- one local nested-findings sub-renderer token
- no new V2 config threading beyond the small internal `_viewRendererType` discriminator

Two closeout corrections matter for honesty:

1. the first pass preserved the mixed-surface findings path but dropped shared accordion header affordances on the shim path
2. the final pass restored those inherited section-header behaviors on the local accordion path:
   - provenance icon support
   - capture-status dots
   - per-section polish controls
   - collapsed preview text
   - the existing generic section-level capture button
3. the final pass also corrected one residual local-host risk:
   - non-findings subsection renderers on the thematic shim now resolve through Critic’s local sub-renderer registry rather than the package resolver directly
   - that keeps future host-local subsection tokens from being silently bypassed on this shim path

So the final landed claim is stronger than the first implementation pass:

- the mixed-surface proof is not only functionally correct for nested thematic findings
- it is also now honest about inherited section-level behavior on the preserved accordion path

## Verification

Focused host verification passed after the final closeout correction:

- `CI=1 npm test -- --watchAll=false --runInBand --runTestsByPath src/components/renderers/AoiThemeSectionRenderer.test.tsx src/components/renderers/AoiThemeFindingsMiniCardList.test.tsx src/components/renderers/AoiThemeAccordionShim.test.tsx src/components/renderers/AoiThemeMixedSurfaceRenderer.test.tsx src/components/renderers/NestedSectionsRenderer.test.tsx src/components/renderers/index.test.tsx src/components/V2TabContent.test.tsx src/components/influence/AoiV2ThematicPanel.test.tsx`
  - `49 passed`

Focused browser verification also passed:

- `npx playwright test tests/aoi-v2-theme-capture.spec.ts --project=chromium`
  - `2 passed`

Two honesty notes matter:

- the browser proof required booting the Critic frontend with `TSC_COMPILE_ON_ERROR=true DISABLE_ESLINT_PLUGIN=true npm start` because unrelated existing TypeScript issues still exist in:
  - `/home/evgeny/projects/the-critic/webapp/src/components/CrossConceptPanel.tsx`
  - `/home/evgeny/projects/the-critic/webapp/src/components/influence/DualAxisView.tsx`
  - `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx`
- the existing `act(...)` warnings on `AoiV2ThematicPanel` and the repo’s existing Jest open-handle warning remain unchanged

## Calibrated Claim

Before this slice, the strongest honest host-side claim on the current AOI V2 line was:

- Critic could consume the analyzer contract on one pure findings surface, `aoi_by_sin_type`

After this slice, the stronger honest claim is:

- Critic can also consume that already-landed analyzer contract on one structurally different current mixed surface, `aoi_by_theme`, by using generic whole-view capturability plus nested item identity

That is materially stronger because the matrix is no longer:

- one pure AOI findings surface only

It is now:

- one pure AOI findings surface
- one mixed AOI thematic surface

The claim is still deliberately bounded:

- still AOI-only
- still one host
- still one local dispatcher/shim path
- still no generic renderer-package law

## Why This Matters

This slice closes the AOI side of the current consumer matrix far enough to stop doing AOI-only broadening by reflex.

The progression is now:

1. analyzer-v2 emits bounded first-hop affordance truth
2. analyzer-v2 carries bounded findings-bank specialization only where honest
3. analyzer-v2 preserves nested finding handles on one mixed AOI surface without overclaiming whole-view specialization
4. Critic consumes the pure findings surface on `aoi_by_sin_type`
5. Critic preserves and reads back bounded capture truth on that same pure findings line
6. Critic now also consumes one current mixed AOI surface on `aoi_by_theme`

That is enough AOI-side matrix closure to justify a cross-family broadening move.

Reusable-substrate value is therefore stronger than it was before, but still bounded:

- the current analyzer-owned contract is now proven on both a pure and a mixed AOI surface
- but it is still not yet proven on one current non-AOI V2 surface

## Next Honest Step

The next bounded Phase E question should stop broadening AOI-only current-consumer proofs and move to one current non-AOI V2 surface.

The smallest honest next target is:

- `genealogy_portrait` in Critic

Why this is the right next move:

- it is a live current non-AOI V2 surface
- analyzer-v2 already emits generic `FirstHopAffordance` on the eligible genealogy leaf family
- `V2TabContent` already threads `_firstHopAffordance` and `_workflowKey`
- the current host renderer still relies on host-local unconditional capture assumptions instead of consuming that analyzer-owned generic contract explicitly
- the current capture-provenance substrate already supports `source_workflow_key`, but this non-AOI custom renderer does not emit it yet

So the next honest step is not:

- another AOI-only consumer refinement
- generic renderer-package sub-renderer injection law
- generic mixed-surface status law
- another analyzer-only semantic slice

It is:

- one bounded non-AOI current-V2 consumer alignment slice on `genealogy_portrait`
- host-only in Critic
- using already-threaded `_firstHopAffordance` and `_workflowKey`
- without analyzer or backend changes

