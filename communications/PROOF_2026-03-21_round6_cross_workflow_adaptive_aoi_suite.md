# Round 6 Proof: Cross-Workflow Adaptive AOI Suite

Date: 2026-03-21

## Scope

This proof closes Round 6 / Cross-Workflow Adaptive AOI Suite Proof for the bounded AOI suite experiment.

Target contract:

- generic AOI host route:
  - `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=<id>&selected_source_thinker_name=<name>&composition_mode=adaptive_aoi_theme_report_suite_v1`
- adaptive target surfaces:
  - `aoi_by_theme`
  - `aoi_thematic_report`
- required claim:
  - the same generic Critic host can restore two AOI results under the same suite-mode contract while analyzer-v2 deterministically selects different runtime families for both adaptive child surfaces under `aoi_thematic_analysis`

## Fixture Note

This proof reused the same synthetic but route-real AOI fixtures closed in round 5.

That reuse was valid because those fixtures already carried the full AOI surface set needed by round 6:

- phase-3 `aoi_by_theme`
- phase-4 `aoi_thematic_report`

Reason:

- the local workspace still had no organically completed AOI jobs for this workflow
- round-5 closure had already seeded two explicit route-real AOI fixtures
- those fixtures already passed the round-6 seam gate for both adaptive targets

So the round-6 proof kept the route claim narrow and honest:

- analyzer-v2 routes were real
- Critic routes were real
- restore/discovery was real
- the coordinated child-surface adaptive contrast was explicit, deterministic, and inspectable

It does not claim that two organically completed AOI jobs with ready-made phase-4 report payloads were available locally at proof time.

## Final Proof Fixtures

### Dossier + Briefing Case

- analyzer-v2 job:
  - `proof-round5-adaptive-aoi-dossier-final-1774100000`
- Critic project:
  - `round5-proof-dossier-final-1774100000`
- thinker:
  - `otto_neurath` / `Otto Neurath`
- expected selected families:
  - `aoi_by_theme -> aoi_theme_dossier`
  - `aoi_thematic_report -> aoi_report_briefing`
- expected visible adaptive surfaces:
  - `Theme Dossier`
  - `Report Briefing`

### Comparison + Evidence Review Case

- analyzer-v2 job:
  - `proof-round5-adaptive-aoi-comparison-final-1774100000`
- Critic project:
  - `round5-proof-comparison-final-1774100000`
- thinker:
  - `otto_neurath` / `Otto Neurath`
- expected selected families:
  - `aoi_by_theme -> aoi_theme_comparison_review`
  - `aoi_thematic_report -> aoi_report_evidence_review`
- expected visible adaptive surfaces:
  - `Theme Comparison Review`
  - `Report Evidence Review`

## Automated Route Proof

The route checks were executed browser-automated against the local stack:

- analyzer-v2:
  - `http://127.0.0.1:8002`
- Critic API:
  - `http://127.0.0.1:5555`
- Critic webapp:
  - `http://127.0.0.1:3000`

### Dossier + Briefing Route

Route:

- `/p/round5-proof-dossier-final-1774100000/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=otto_neurath&selected_source_thinker_name=Otto%20Neurath&composition_mode=adaptive_aoi_theme_report_suite_v1`

Observed:

- generic workspace restored successfully from upstream result discovery
- `Composition: adaptive AOI suite proof` rendered
- `Theme Dossier` rendered in the AOI child-surface tab row
- `Report Briefing` rendered in the AOI child-surface tab row
- after selecting the report surface, the page rendered:
  - `Report Summary`
  - `Summary`
  - `Engagement Pattern`
  - `Reading Implications`
  - `Key Divergences`
  - `Sin Distribution`

Saved artifacts:

- `communications/PROOF_round6_dossier_final_page_2026-03-21.png`
- `communications/PROOF_round6_dossier_final_page_text_2026-03-21.txt`

### Comparison + Evidence Review Route

Route:

- `/p/round5-proof-comparison-final-1774100000/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=otto_neurath&selected_source_thinker_name=Otto%20Neurath&composition_mode=adaptive_aoi_theme_report_suite_v1`

Observed:

- generic workspace restored successfully from upstream result discovery
- `Composition: adaptive AOI suite proof` rendered
- `Theme Comparison Review` rendered in the AOI child-surface tab row
- `Report Evidence Review` rendered in the AOI child-surface tab row
- after selecting the report surface, the page rendered:
  - `Report Snapshot`
  - `Key Divergences`
  - `Sin Distribution`
  - multi-table headers and rows for the evidence-review contract

Saved artifacts:

- `communications/PROOF_round6_comparison_final_page_2026-03-21.png`
- `communications/PROOF_round6_comparison_final_page_text_2026-03-21.txt`

## Trace Proof

### Dossier + Briefing Trace

Trace endpoint:

- `/v1/presenter/trace/proof-round5-adaptive-aoi-dossier-final-1774100000?consumer_key=the-critic&composition_mode=adaptive_aoi_theme_report_suite_v1`

Result:

- `composition_status = applied`
- `adaptive_surface_suite_selection` stage present

Selected families:

- `aoi_by_theme -> aoi_theme_dossier`
- `aoi_thematic_report -> aoi_report_briefing`

Key selector evidence:

- theme:
  - `theme_count = 2`
  - `total_finding_count = 5`
  - `dominant_theme_name = Calculation Without Prices`
  - `dominant_theme_findings = 4`
  - `dominant_theme_share = 0.8`
- report:
  - `key_divergence_count = 2`
  - `sin_distribution_count = 2`
  - `non_empty_prose_sections = 3`
  - `summary_length = 139`
  - `engagement_pattern_length = 197`
  - `reading_implications_length = 181`

Recorded rationales:

- theme:
  - `Calculation Without Prices carries 4 of 5 findings (80%), so a dossier-led reading is the clearest surface.`
- report:
  - `The report is driven more by briefing prose (3 non-empty prose sections) than by dense divergence matrices (2 divergences, 2 sin categories), so a briefing-led closeout is the best fit.`

Saved trace artifact:

- `communications/PROOF_round6_dossier_final_trace_2026-03-21.json`

### Comparison + Evidence Review Trace

Trace endpoint:

- `/v1/presenter/trace/proof-round5-adaptive-aoi-comparison-final-1774100000?consumer_key=the-critic&composition_mode=adaptive_aoi_theme_report_suite_v1`

Result:

- `composition_status = applied`
- `adaptive_surface_suite_selection` stage present

Selected families:

- `aoi_by_theme -> aoi_theme_comparison_review`
- `aoi_thematic_report -> aoi_report_evidence_review`

Key selector evidence:

- theme:
  - `theme_count = 4`
  - `total_finding_count = 4`
  - `dominant_theme_name = Administrative Coordination`
  - `dominant_theme_findings = 1`
  - `dominant_theme_share = 0.25`
- report:
  - `key_divergence_count = 5`
  - `sin_distribution_count = 3`
  - `non_empty_prose_sections = 3`
  - `summary_length = 123`
  - `engagement_pattern_length = 154`
  - `reading_implications_length = 154`

Recorded rationales:

- theme:
  - `The findings remain distributed across 4 themes with no single theme exceeding 25% of the evidence, so a comparison review is the most legible family.`
- report:
  - `The report carries 5 divergence cards across 3 sin categories, so an evidence-led review is the clearest surface.`

Saved trace artifact:

- `communications/PROOF_round6_comparison_final_trace_2026-03-21.json`

## Disposition

Round 6 proof passes.

What is now proven:

- `adaptive_aoi_theme_report_suite_v1` is a real AOI suite-mode contract, independent of the earlier proof modes
- coordinated adaptive suite behavior now generalizes to a second workflow family rather than remaining genealogy-only
- analyzer-v2 can rewrite two AOI child surfaces under the same `aoi_thematic_analysis` parent without host-specific logic
- the same generic AOI route can expose materially different theme and report surface families under one suite-mode token
- the suite decision remains trace-inspectable through `adaptive_surface_suite_selection` with per-surface selected family, rejected families, signal summary, and rationale

## Operational Notes

- The local analyzer API had to be restarted before the final round-6 route proof so the live server picked up the completed suite-mode branch.
- Round 6 reused the round-5 proof fixtures because they already satisfied the fixture-completeness requirement for both adaptive targets.
