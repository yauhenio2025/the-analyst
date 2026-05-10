# Memo: Phase E Renderers-UI SubRenderers Capture-Base Shell Adoption V1 Completion

Subtitle: The smaller internal package-native raw capture-base shell now covers the dominant inline `SubRenderers` builder surface without changing current forwarded defaults or normalizing nested runtime propagation

Date: 2026-04-04
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Most Recent Prior Completion:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_completion.md`
Immediate Prior Scope:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_scope.md`
Close-Read Corridor Context:
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
Review Context:
- `communications/REPORT_Codex_Phase_E_Renderers_UI_SubRenderers_Capture_Base_Shell_Adoption_V1_Scope_Audit_2026-04-04.md`
- `communications/REPORT_Claude_Phase_E_Renderers_UI_SubRenderers_Capture_Base_Shell_Adoption_V1_Scope_Critique_2026-04-04.md`
Package Codebase:
- `/home/evgeny/projects/analyzer-v2/renderers-ui`

## Purpose

Record what actually landed after the package-top-level pilot.

This slice asked one narrower question:

- does the already-landed internal `captureBase` utility also fit the current inline `SubRenderers` capture builders while preserving current package behavior and leaving nested forwarding asymmetries untouched

This slice was deliberately bounded.
It was not:

- package-wide nested runtime convergence
- forwarding normalization
- a Critic host change
- promotion of Critic-local first-hop, workflow/job, or typed-selection law into `renderers-ui`

## What Landed

One bounded package-local mechanical refactor is now complete inside `renderers-ui/src/sub-renderers/SubRenderers.tsx`.

The landed behavior is:

1. the existing internal utility at:
   - `renderers-ui/src/utils/captureBase.ts`
   is now adopted across the current inline capture builders in `SubRenderers.tsx`
2. the migrated inline builders are exactly:
   - `DefinitionList`
   - `MiniCardList`
   - `ComparisonPanel`
   - `IntensityMatrix`
   - `MoveRepertoire`
   - `DialecticalPair`
   - `RichDescriptionList`
   - `PhaseTimeline`
3. the utility itself stayed unchanged in role:
   - raw package gate only
   - raw package config reads only
   - raw base selection assembly only
4. renderer-local concerns stayed local:
   - `_parentSectionKey`
   - `_parentSectionTitle`
   - `source_section_key`
   - `source_item_index`
   - `source_renderer_type`
   - `content_type`
   - `selected_text`
   - `structured_data`
   - `depth_level`
   - `parent_context`
   - local title-segment branching
5. the extended lightweight package verification still lives at:
   - `renderers-ui/scripts/check-capture-base.mjs`
6. the known nested forwarding asymmetries remained intentionally untouched:
   - `AccordionRenderer` still omits `_captureSourceType` / `_captureEntityId` when forwarding into nested sub-renderers
   - `CardRenderer` nested subsection dispatch still does not forward capture runtime into nested sub-renderers at all

## Behavioral Boundary Preserved

The honest completed claim is:

- the existing package-native raw capture-base shell now covers both the top-level package trio and the dominant current inline `SubRenderers` builder surface

What this does mean:

- repeated inline base selection assembly is now thinner across the largest remaining package-local builder surface
- the package utility is no longer only proven on the top-level trio
- the package capture-base shell is now used across the exact eight current inline capture-enabled `SubRenderers`

What this does not mean:

- nested runtime coverage is now converged
- nested capture availability has increased on paths with incomplete or missing forwarded runtime
- forwarding asymmetries are normalized
- `SubRenderers` no longer depends on current forwarded defaults
- Critic-local first-hop/workflow/type law has moved into the package
- `currentRendererCapture` is now obsolete
- package-wide capture law is now solved

## Exact Preservation Points

The implementation stayed aligned to the approved preservation bar.

It preserved:

- raw `captureMode && onCapture` gating only
- raw string-or-default semantics only
- no trim or non-empty normalization
- `>` title composition
- no empty-segment filtering
- raw identity fallback:
  - explicit `entityId !== undefined`
  - otherwise `captureEntityId || captureJobId || ''`

It also preserved the deeper builder-specific title patterns already present in `SubRenderers`:

- 2-level chains with no parent section
- 3-level chains with parent section
- 4-level chains such as grouped `MoveRepertoire`
- empty parent-title segment preservation

## Verification

Focused package-local verification passed:

- `npm run build`
  - passed
- `node scripts/check-capture-base.mjs`
  - `capture-base verification passed`

The verification script now covers representative builder-shaped fixtures for:

- unchanged raw gate behavior
- unchanged raw defaults
- unchanged `>` title composition
- empty-segment preservation
- unchanged `entity_id` precedence
- representative 2/3/4-segment title patterns

This slice did **not** rerun Critic consumer regressions because:

- the work stayed package-local
- no local tarball refresh into Critic was part of this slice

Environment honesty note:

- the existing `MODULE_TYPELESS_PACKAGE_JSON` warning from Node remains unchanged when the script imports the built internal module from `dist`

## Calibrated Claim

Before this slice, the strongest honest package-side claim was:

- the smaller package-native shell existed in real code and was proven only on the top-level trio

After this slice, the stronger honest claim is:

- the same smaller package-native shell is now proven across the dominant current inline capture-builder surface in `SubRenderers`

That is a real advance.
But it remains deliberately narrower than package-wide convergence:

- top-level renderers are covered
- the current inline `SubRenderers` builders are covered
- nested forwarding behavior is still whatever the current forwarding layer supplies

So the correct closeout language is:

- **dominant inline `SubRenderers` builder adoption complete**

not:

- nested package capture runtime now converged

## Why This Matters For The Close Read Corridor

This slice shortens the remaining renderer-substrate corridor toward a lean `Close Read V1`.

It removes one more large bucket of repeated package-local capture assembly while keeping the remaining uncertainty honest:

- the remaining renderer-substrate question is no longer whether the package-native shell fits `SubRenderers`
- the remaining renderer-substrate question is whether the current nested runtime forwarding asymmetries are already acceptable for a first lean `Close Read` build or require one bounded normalization decision and possibly one bounded follow-on patch

That is materially closer to product-facing scoping.

## Next Honest Step

The next honest question is now:

- does the current nested capture-runtime forwarding line already stay good enough for a lean `Close Read V1`
- or is one bounded forwarding-normalization slice still required first

That next step should be scoped explicitly as a decision gate.
It should stay below:

- package-wide convergence claims
- Critic-local first-hop/workflow/type law
- destination lifecycle/taxonomy widening
- full `Close Read` productization

If that decision comes back clean, the next product-facing move becomes:

- one lean `Close Read V1` scope memo grounded only in runtime-real first-hop operations and current real destinations
