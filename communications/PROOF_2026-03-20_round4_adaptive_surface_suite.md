# Round 4 Proof: Adaptive Surface Suite

Date: 2026-03-20

## Scope

This proof closes Round 4 / Adaptive Surface Suite Proof for the bounded genealogy suite experiment.

Target contract:

- generic host route:
  - `/p/:projectId/analysis/intellectual_genealogy?composition_mode=adaptive_genealogy_relationship_conditions_v1`
- adaptive target surfaces:
  - `genealogy_relationship_landscape`
  - `genealogy_conditions`
- required claim:
  - the same generic Critic host can restore two genealogy results under the same suite-mode contract while analyzer-v2 deterministically selects different runtime families for both target surfaces

## Fixture Note

This proof used two synthetic but route-real genealogy fixtures.

They were built by combining:

- the round-3 relationship proof fixtures:
  - `proof-round3-adaptive-dossier-final-1774002300`
  - `proof-round3-adaptive-comparison-final-1774002300`
- the real imported phase-3 conditions prose from:
  - `job-import-3e8cb4ed`

Reason:

- the local workspace still only had one concrete completed genealogy corpus
- the round-3 fixtures already carried the needed contrastive relationship-card cache
- the imported source job carried the real phase-3 conditions prose, but not the normalized top-level `genealogy_conditions` structured payload needed for suite selection

So the round-4 fixtures were created by:

- preserving the broader round-3 relationship contrast exactly
- cloning the real imported phase-3 conditions outputs into each new job
- adding only the top-level `structured_payloads["genealogy_conditions"]` proof payload on the latest conditions pass

This keeps the proof claim narrow and honest:

- analyzer-v2 routes were real
- Critic routes were real
- upstream restore/discovery was real
- the multi-surface contrast was explicit, deterministic, and inspectable

It does not claim that two organically distinct completed genealogy corpora with ready-made top-level conditions payloads were available locally at proof time.

## Final Proof Fixtures

### Balance Case

- analyzer-v2 job:
  - `proof-round4-adaptive-balance-final-1774012011`
- Critic project:
  - `round4-proof-balance-final-1774012011`
- expected relationship family:
  - `relationship_profile_dossier`
- expected conditions family:
  - `conditions_balance_sheet`
- expected visible surfaces:
  - `Relationship Dossier`
  - `Conditions Balance Sheet`

### Matrix Case

- analyzer-v2 job:
  - `proof-round4-adaptive-matrix-final-1774012011`
- Critic project:
  - `round4-proof-matrix-final-1774012011`
- expected relationship family:
  - `relationship_comparison_review`
- expected conditions family:
  - `conditions_path_dependency_matrix`
- expected visible surfaces:
  - `Relationship Comparison Review`
  - `Conditions Path-Dependency Matrix`

## Automated Route Proof

The route checks were executed browser-automated against the local stack:

- analyzer-v2:
  - `http://127.0.0.1:8002`
- Critic API:
  - `http://127.0.0.1:5555`
- Critic webapp:
  - `http://127.0.0.1:3000`

### Balance Route

Route:

- `/p/round4-proof-balance-final-1774012011/analysis/intellectual_genealogy?composition_mode=adaptive_genealogy_relationship_conditions_v1`

Observed:

- generic workspace restored successfully from upstream result discovery
- `Composition: adaptive suite proof` rendered
- `Relationship Dossier` rendered in the top-level view list
- `Conditions Balance Sheet` rendered in the top-level view list
- after selecting the conditions surface, the page rendered:
  - `Conditions Snapshot`
  - `Enabling Pressures`
  - `Constraining Pressures`

Saved artifacts:

- `communications/PROOF_round4_balance_final_page_2026-03-20.png`
- `communications/PROOF_round4_balance_final_page_text_2026-03-20.txt`

### Matrix Route

Route:

- `/p/round4-proof-matrix-final-1774012011/analysis/intellectual_genealogy?composition_mode=adaptive_genealogy_relationship_conditions_v1`

Observed:

- generic workspace restored successfully from upstream result discovery
- `Composition: adaptive suite proof` rendered
- `Relationship Comparison Review` rendered in the top-level view list
- `Conditions Path-Dependency Matrix` rendered in the top-level view list
- after selecting the conditions surface, the page rendered:
  - `Path Dependencies`
  - `Alternative Paths`
  - the matrix rows and table headers for the adaptive path-dependency contract

Saved artifacts:

- `communications/PROOF_round4_matrix_final_page_2026-03-20.png`
- `communications/PROOF_round4_matrix_final_page_text_2026-03-20.txt`

## Trace Proof

### Balance Trace

Trace endpoint:

- `/v1/presenter/trace/proof-round4-adaptive-balance-final-1774012011?consumer_key=the-critic&composition_mode=adaptive_genealogy_relationship_conditions_v1`

Result:

- `composition_status = applied`
- `adaptive_surface_suite_selection` stage present

Selected families:

- `genealogy_relationship_landscape -> relationship_profile_dossier`
- `genealogy_conditions -> conditions_balance_sheet`

Key selector evidence:

- relationship:
  - `relationship_count = 3`
  - `distinct_relationship_types = 3`
  - `dominant_work_title = The Global Minotaur`
  - `top_score = 15`
  - `second_score = 4`
  - `score_gap = 11`
  - `top_share = 0.68`
- conditions:
  - `overall_balance = enabling_dominant`
  - `enabling_conditions_count = 3`
  - `constraining_conditions_count = 2`
  - `path_dependencies_count = 1`
  - `unacknowledged_debts_count = 2`
  - `alternative_paths_count = 1`

Recorded rationale:

- relationship:
  - `The Global Minotaur clearly dominates the relationship field (68% of weighted relationship strength, 11 points ahead of the next work), so a single-work dossier is the clearest surface.`
- conditions:
  - `The conditions field reads most clearly as an enabling/constraining balance (3 enabling, 2 constraining, 2 debts, balance=Enabling Dominant), so a balance-sheet surface is the best fit.`

Saved trace artifact:

- `communications/PROOF_round4_balance_final_trace_2026-03-20.json`

### Matrix Trace

Trace endpoint:

- `/v1/presenter/trace/proof-round4-adaptive-matrix-final-1774012011?consumer_key=the-critic&composition_mode=adaptive_genealogy_relationship_conditions_v1`

Result:

- `composition_status = applied`
- `adaptive_surface_suite_selection` stage present

Selected families:

- `genealogy_relationship_landscape -> relationship_comparison_review`
- `genealogy_conditions -> conditions_path_dependency_matrix`

Key selector evidence:

- relationship:
  - `relationship_count = 3`
  - `distinct_relationship_types = 3`
  - `dominant_work_title = The Global Minotaur`
  - `top_score = 15`
  - `second_score = 12`
  - `score_gap = 3`
  - `top_share = 0.43`
- conditions:
  - `overall_balance = balanced`
  - `enabling_conditions_count = 1`
  - `constraining_conditions_count = 1`
  - `path_dependencies_count = 3`
  - `unacknowledged_debts_count = 0`
  - `alternative_paths_count = 2`

Recorded rationale:

- relationship:
  - `Several relationships remain materially comparable (The Global Minotaur, Talking to My Daughter About the Economy, Adults in the Room), so a comparison review fits better than a single dominant dossier or a broad field map.`
- conditions:
  - `Path dependencies and alternative branches dominate this conditions field (3 dependencies, 2 alternatives, balance=Balanced), so a path-dependency matrix is the clearest surface.`

Saved trace artifact:

- `communications/PROOF_round4_matrix_final_trace_2026-03-20.json`

## Disposition

Round 4 proof passes.

What is now proven:

- `adaptive_genealogy_relationship_conditions_v1` is a real upstream suite-mode contract, independent of round-2 and round-3 proof modes
- analyzer-v2 can coordinate deterministic adaptive family selection for two distinct top-level genealogy surfaces on the same page
- the selected families can diverge across both target surfaces under the same generic Critic route shape
- the Critic host remains generic in substance; it only consumes the returned presentation tree and shared composition-mode plumbing
- the suite decision is inspectable in trace through `adaptive_surface_suite_selection` with per-surface selected family, rejected families, signal summary, and rationale

## Operational Notes

- The local analyzer API needed a restart after the new suite-mode constant landed, because the existing `uvicorn` process had not reloaded the new composition mode.
- The local Critic webapp still logs the pre-existing style-token fetch fallback against `localhost:8001`; that did not block route restoration or proof capture.
