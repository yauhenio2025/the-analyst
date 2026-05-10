# Round 5 Proof: Cross-Workflow Adaptive AOI Theme

Date: 2026-03-21

## Scope

This proof closes Round 5 / Cross-Workflow Adaptive AOI Theme Proof for the bounded AOI adaptive-surface experiment.

Target contract:

- generic AOI host route:
  - `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=<id>&selected_source_thinker_name=<name>&composition_mode=adaptive_aoi_theme_surface_v1`
- adaptive target surface:
  - `aoi_by_theme`
- required claim:
  - the same generic Critic host can restore two AOI results on the same thinker-scoped route while analyzer-v2 deterministically selects different runtime families for `aoi_by_theme`

## Fixture Note

This proof used two synthetic but route-real AOI fixtures.

Reason:

- the local workspace had `0` organically completed AOI jobs for `anxiety_of_influence_thematic_single_thinker`
- round 5 therefore could not close against naturally available AOI result pairs

So the proof fixtures were seeded explicitly with the AOI surface set required by the route:

- `aoi_source_documents`
- `aoi_by_theme`
- `aoi_by_sin_type`
- `aoi_thematic_report`

This keeps the claim narrow and honest:

- analyzer-v2 routes were real
- Critic routes were real
- result discovery and restore were real
- the adaptive AOI contrast was explicit, deterministic, and inspectable

It does not claim that two organically completed AOI jobs were available locally at proof time.

## Final Proof Fixtures

### Dossier Case

- analyzer-v2 job:
  - `proof-round5-adaptive-aoi-dossier-final-1774100000`
- Critic project:
  - `round5-proof-dossier-final-1774100000`
- thinker:
  - `otto_neurath` / `Otto Neurath`
- expected selected family:
  - `aoi_theme_dossier`
- expected visible adaptive surface:
  - `Theme Dossier`

### Comparison Case

- analyzer-v2 job:
  - `proof-round5-adaptive-aoi-comparison-final-1774100000`
- Critic project:
  - `round5-proof-comparison-final-1774100000`
- thinker:
  - `otto_neurath` / `Otto Neurath`
- expected selected family:
  - `aoi_theme_comparison_review`
- expected visible adaptive surface:
  - `Theme Comparison Review`

## Automated Route Proof

The route checks were executed browser-automated against the local stack:

- analyzer-v2:
  - `http://127.0.0.1:8002`
- Critic API:
  - `http://127.0.0.1:5555`
- Critic webapp:
  - `http://127.0.0.1:3000`

### Dossier Route

Route:

- `/p/round5-proof-dossier-final-1774100000/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=otto_neurath&selected_source_thinker_name=Otto%20Neurath&composition_mode=adaptive_aoi_theme_surface_v1`

Observed:

- generic workspace restored successfully from upstream result discovery
- `Composition: adaptive AOI theme proof` rendered
- `Theme Dossier` rendered in the AOI child-surface tab row
- the selected adaptive surface rendered:
  - `Theme Summary`
  - `Calculation Without Prices`
  - `Planning as Public Knowledge`

Saved artifacts:

- `communications/PROOF_round5_dossier_final_page_2026-03-21.png`
- `communications/PROOF_round5_dossier_final_page_text_2026-03-21.txt`

### Comparison Route

Route:

- `/p/round5-proof-comparison-final-1774100000/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=otto_neurath&selected_source_thinker_name=Otto%20Neurath&composition_mode=adaptive_aoi_theme_surface_v1`

Observed:

- generic workspace restored successfully from upstream result discovery
- `Composition: adaptive AOI theme proof` rendered
- `Theme Comparison Review` rendered in the AOI child-surface tab row
- the selected adaptive surface rendered:
  - comparison table headers for `Theme`, `Findings`, `Dominant Sin Type`, `Sources`, `Key Claims`, `Overview`
  - four comparison rows across the thematic field

Saved artifacts:

- `communications/PROOF_round5_comparison_final_page_2026-03-21.png`
- `communications/PROOF_round5_comparison_final_page_text_2026-03-21.txt`

## Trace Proof

### Dossier Trace

Trace endpoint:

- `/v1/presenter/trace/proof-round5-adaptive-aoi-dossier-final-1774100000?consumer_key=the-critic&composition_mode=adaptive_aoi_theme_surface_v1`

Result:

- `composition_status = applied`
- `adaptive_surface_selection` stage present

Selected family:

- `aoi_by_theme -> aoi_theme_dossier`

Key selector evidence:

- `theme_count = 2`
- `total_finding_count = 5`
- `dominant_theme_id = theme_calculation_without_prices`
- `dominant_theme_name = Calculation Without Prices`
- `dominant_theme_findings = 4`
- `dominant_theme_share = 0.8`
- `second_theme_findings = 1`

Recorded rationale:

- `Calculation Without Prices carries 4 of 5 findings (80%), so a dossier-led reading is the clearest surface.`

Saved trace artifact:

- `communications/PROOF_round5_dossier_final_trace_2026-03-21.json`

### Comparison Trace

Trace endpoint:

- `/v1/presenter/trace/proof-round5-adaptive-aoi-comparison-final-1774100000?consumer_key=the-critic&composition_mode=adaptive_aoi_theme_surface_v1`

Result:

- `composition_status = applied`
- `adaptive_surface_selection` stage present

Selected family:

- `aoi_by_theme -> aoi_theme_comparison_review`

Key selector evidence:

- `theme_count = 4`
- `total_finding_count = 4`
- `dominant_theme_id = theme_administrative_coordination`
- `dominant_theme_name = Administrative Coordination`
- `dominant_theme_findings = 1`
- `dominant_theme_share = 0.25`
- `second_theme_findings = 1`

Recorded rationale:

- `The findings remain distributed across 4 themes with no single theme exceeding 25% of the evidence, so a comparison review is the most legible family.`

Saved trace artifact:

- `communications/PROOF_round5_comparison_final_trace_2026-03-21.json`

## Important Late Fix

The first live round-5 proof attempt exposed one real presenter seam bug:

- live accordion payloads no longer carried `_section_order` and `_section_titles` in `structured_data` after authored payload construction
- the AOI adaptive selector was still reading those keys directly from `structured_data`

Round-5 proof closure therefore required one final contract repair in `src/presenter/bounded_dynamic_composition.py`:

- recover authored AOI section order and titles from `renderer_config.sections` when those meta keys have been stripped from the live accordion payload

That fix is now covered by the live-path regression in:

- `tests/test_presentation_api.py`

The proof recorded here is the post-fix route result.

## Disposition

Round 5 proof passes.

What is now proven:

- `adaptive_aoi_theme_surface_v1` is a real AOI adaptive proof contract, independent of the genealogy proof modes
- adaptive family selection now generalizes across workflow families, not just inside genealogy
- `aoi_by_theme` can be adaptively rewritten in place under `aoi_thematic_analysis` without promoting it to top level
- the Critic host remains generic in substance; it only consumes the returned presentation tree and shared composition-mode plumbing
- the adaptive decision remains trace-inspectable through the reused `adaptive_surface_selection` grammar

## Operational Notes

- The local analyzer API had to be restarted before the final route proof so the live server picked up the completed AOI adaptive code.
- These same AOI proof fixtures were then suitable for round-6 reuse because they already carried both the phase-3 thematic payload and the phase-4 `aoi_thematic_report` payload.
