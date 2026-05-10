# Round 3 Proof: Adaptive Surface Family

Date: 2026-03-20

## Scope

This proof closes Round 3 / Adaptive Surface Family Proof for the bounded genealogy surface experiment.

Target contract:

- generic host route:
  - `/p/:projectId/analysis/intellectual_genealogy?composition_mode=adaptive_relationship_surface_v1`
- adaptive target surface:
  - `genealogy_relationship_landscape`
- required claim:
  - the same generic Critic host can restore two genealogy results under the same `composition_mode`, while analyzer-v2 deterministically selects different upstream relationship surface families from content signals

## Fixture Note

This proof used two synthetic but route-real genealogy fixtures derived from the existing imported Varoufakis genealogy job `job-import-3e8cb4ed`.

Reason:

- the local workspace only had one concrete completed genealogy corpus
- that imported source job still carried the legacy collapsed `work_key='target'` shape for phase 1.5 relationship outputs, which prevented direct adaptive per-work card selection on the real imported row

So the proof fixtures were created by cloning the real job, preserving the broader genealogy run shape, and replacing only the per-work relationship-card cache used by the adaptive selector.

This keeps the proof honest:

- analyzer-v2 routes were real
- Critic import/restore routes were real
- the generic workspace route was real
- the contrast itself was deterministic and explicit

## Final Proof Fixtures

### Dossier Case

- analyzer-v2 job:
  - `proof-round3-adaptive-dossier-final-1774002300`
- Critic project:
  - `round3-proof-dossier-final-1774002300`
- expected family:
  - `relationship_profile_dossier`
- expected surface title:
  - `Relationship Dossier`

### Comparison Case

- analyzer-v2 job:
  - `proof-round3-adaptive-comparison-final-1774002300`
- Critic project:
  - `round3-proof-comparison-final-1774002300`
- expected family:
  - `relationship_comparison_review`
- expected surface title:
  - `Relationship Comparison Review`

## Automated Route Proof

The "manual" route checks were executed browser-automated against the local stack:

- analyzer-v2:
  - `http://127.0.0.1:8002`
- Critic API:
  - `http://127.0.0.1:5555`
- Critic webapp:
  - `http://127.0.0.1:3000`

### Dossier Route

Route:

- `/p/round3-proof-dossier-final-1774002300/analysis/intellectual_genealogy?composition_mode=adaptive_relationship_surface_v1`

Observed:

- generic workspace restored successfully
- `Composition: adaptive surface proof` rendered
- `Relationship Dossier` rendered in the top-level view list
- no `View not found`
- no visible load failure

Saved artifacts:

- `communications/PROOF_round3_dossier_final_page_2026-03-20.png`
- `communications/PROOF_round3_dossier_final_page_text_2026-03-20.txt`

### Comparison Route

Route:

- `/p/round3-proof-comparison-final-1774002300/analysis/intellectual_genealogy?composition_mode=adaptive_relationship_surface_v1`

Observed:

- generic workspace restored successfully
- `Composition: adaptive surface proof` rendered
- `Relationship Comparison Review` rendered in the top-level view list
- no `View not found`
- no visible load failure

Saved artifacts:

- `communications/PROOF_round3_comparison_final_page_2026-03-20.png`
- `communications/PROOF_round3_comparison_final_page_text_2026-03-20.txt`

## Trace Proof

### Dossier Trace

Trace endpoint:

- `/v1/presenter/trace/proof-round3-adaptive-dossier-final-1774002300?consumer_key=the-critic&composition_mode=adaptive_relationship_surface_v1`

Result:

- `composition_status = applied`
- `selected_family = relationship_profile_dossier`

Key selector evidence:

- `relationship_count = 3`
- `distinct_relationship_types = 3`
- `dominant_work_title = The Global Minotaur`
- `top_score = 15`
- `second_score = 4`
- `score_gap = 11`
- `top_share = 0.68`

Recorded rationale:

- `The Global Minotaur clearly dominates the relationship field (68% of weighted relationship strength, 11 points ahead of the next work), so a single-work dossier is the clearest surface.`

Saved trace artifact:

- `communications/PROOF_round3_dossier_final_trace_2026-03-20.json`

### Comparison Trace

Trace endpoint:

- `/v1/presenter/trace/proof-round3-adaptive-comparison-final-1774002300?consumer_key=the-critic&composition_mode=adaptive_relationship_surface_v1`

Result:

- `composition_status = applied`
- `selected_family = relationship_comparison_review`

Key selector evidence:

- `relationship_count = 3`
- `distinct_relationship_types = 3`
- `dominant_work_title = The Global Minotaur`
- `top_score = 15`
- `second_score = 12`
- `score_gap = 3`
- `top_share = 0.43`

Recorded rationale:

- `Several relationships remain materially comparable (The Global Minotaur, Talking to My Daughter About the Economy, Adults in the Room), so a comparison review fits better than a single dominant dossier or a broad field map.`

Saved trace artifact:

- `communications/PROOF_round3_comparison_final_trace_2026-03-20.json`

## Disposition

Round 3 proof passes.

What is now proven:

- `adaptive_relationship_surface_v1` is a real upstream composition mode, independent of round-2 regrouping mode
- analyzer-v2 deterministically selects different relationship surface families from structured relationship-card signals
- the same generic Critic host route can restore both results without workflow-specific host branching
- the proof mode is inspectable through `adaptive_surface_selection` trace output

## Operational Notes

- The local Critic webapp `.env` pointed at the Render deployment by default, so the proof run used explicit local `REACT_APP_API_URL` and `REACT_APP_ANALYZER_V2_URL` overrides.
- The local Critic SQLite database also needed the current `v2_run_references` columns present in the running model before import could complete.

Those were local-environment concerns, not round-3 product-contract failures.
