# Round 8 Proof: Declarative Adaptive Suite

Date: 2026-03-21

## Scope

This proof closes Round 8 / Declarative Adaptive Suite for the bounded genealogy relationship + conditions suite experiment.

Target contract:

- generic host route:
  - `/p/:projectId/analysis/intellectual_genealogy?composition_mode=declarative_genealogy_relationship_conditions_suite_v1`
- hardcoded control:
  - `adaptive_genealogy_relationship_conditions_v1`
- adaptive target surfaces:
  - `genealogy_relationship_landscape`
  - `genealogy_conditions`
- required bounded claim:
  - a repo-tracked declarative suite spec can drive the already-proven genealogy relationship + conditions suite on the same thin host without giving up fail-closed validation, workflow-scoped authorization, or the existing `adaptive_surface_suite_selection` trace grammar

This proof is intentionally bounded to the two documented round-4 contrast controls only.

It does **not** claim full semantic replacement for every branch the hardcoded suite can reach.

## Fixture Note

This proof reused the existing round-4 route-real documentary controls directly.

Verified local control jobs:

- `proof-round4-adaptive-balance-final-1774012011`
- `proof-round4-adaptive-matrix-final-1774012011`

No new proof fixtures were needed for round 8.

That keeps the round-8 comparison honest:

- same workflow
- same host route family
- same analyzer job ids
- same contrast pair already used to prove the hardcoded suite

## Final Proof Controls

### Balance Case

- analyzer-v2 job:
  - `proof-round4-adaptive-balance-final-1774012011`
- Critic project:
  - `round4-proof-balance-final-1774012011`
- expected hardcoded/declarative outcome:
  - `genealogy_relationship_landscape -> relationship_profile_dossier`
  - `genealogy_conditions -> conditions_balance_sheet`
- expected visible surfaces:
  - `Relationship Dossier`
  - `Conditions Balance Sheet`

### Matrix Case

- analyzer-v2 job:
  - `proof-round4-adaptive-matrix-final-1774012011`
- Critic project:
  - `round4-proof-matrix-final-1774012011`
- expected hardcoded/declarative outcome:
  - `genealogy_relationship_landscape -> relationship_comparison_review`
  - `genealogy_conditions -> conditions_path_dependency_matrix`
- expected visible surfaces:
  - `Relationship Comparison Review`
  - `Conditions Path-Dependency Matrix`

## Local Stack

Route and trace checks were executed against the local stack:

- analyzer-v2:
  - `http://127.0.0.1:8002`
- Critic webapp:
  - `http://127.0.0.1:3000`

Environment note:

- the local analyzer API was restarted before proof closure so the live server picked up the new declarative suite token

## Automated Route Proof

### Balance Route

Route:

- `/p/round4-proof-balance-final-1774012011/analysis/intellectual_genealogy?composition_mode=declarative_genealogy_relationship_conditions_suite_v1`

Observed:

- generic workspace restored successfully on the shared genealogy route
- `Composition: declarative adaptive suite proof` rendered
- `Relationship Dossier` rendered in the top-level view list
- `Conditions Balance Sheet` rendered in the top-level view list

Saved artifacts:

- `communications/PROOF_round8_balance_final_page_2026-03-21.png`
- `communications/PROOF_round8_balance_final_page_text_2026-03-21.txt`

Note:

- the saved page-text capture was taken before lazy child-view hydration completed, so it still ends with `Loading view data...`
- the proof label and the selected top-level suite surfaces were already visible and recorded

### Matrix Route

Route:

- `/p/round4-proof-matrix-final-1774012011/analysis/intellectual_genealogy?composition_mode=declarative_genealogy_relationship_conditions_suite_v1`

Observed:

- generic workspace restored successfully on the shared genealogy route
- `Composition: declarative adaptive suite proof` rendered
- `Relationship Comparison Review` rendered in the top-level view list
- `Conditions Path-Dependency Matrix` rendered in the top-level view list

Saved artifacts:

- `communications/PROOF_round8_matrix_final_page_2026-03-21.png`
- `communications/PROOF_round8_matrix_final_page_text_2026-03-21.txt`

Note:

- the saved page-text capture was also taken before lazy child-view hydration completed
- the proof label and the selected top-level suite surfaces were still visible and recorded

## Trace Proof

### Balance Trace

Trace endpoint:

- `/v1/presenter/trace/proof-round4-adaptive-balance-final-1774012011?consumer_key=the-critic&composition_mode=declarative_genealogy_relationship_conditions_suite_v1`

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
  - `path_signal = 2`
  - `balance_signal = 7`
  - `path_signal_minus_balance_signal = -5`

Recorded rationale:

- relationship:
  - `The Global Minotaur clearly dominates the relationship field (68% of weighted relationship strength, 11 points ahead of the next work), so a single-work dossier is the clearest surface.`
- conditions:
  - `The conditions field reads most clearly as an enabling/constraining balance (3 enabling, 2 constraining, 2 debts, balance=Enabling Dominant), so a balance-sheet surface is the best fit.`

Saved trace artifact:

- `communications/PROOF_round8_balance_final_trace_2026-03-21.json`

### Matrix Trace

Trace endpoint:

- `/v1/presenter/trace/proof-round4-adaptive-matrix-final-1774012011?consumer_key=the-critic&composition_mode=declarative_genealogy_relationship_conditions_suite_v1`

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
  - `path_signal = 5`
  - `balance_signal = 2`
  - `path_signal_minus_balance_signal = 3`

Recorded rationale:

- relationship:
  - `Several relationships remain materially comparable (The Global Minotaur, Talking to My Daughter About the Economy, Adults in the Room), so a comparison review fits better than a single dominant dossier or a broad field map.`
- conditions:
  - `Path dependencies and alternative branches dominate this conditions field (3 dependencies, 2 alternatives, balance=Balanced), so a path-dependency matrix is the clearest surface.`

Saved trace artifact:

- `communications/PROOF_round8_matrix_final_trace_2026-03-21.json`

## Hardcoded Versus Declarative Equivalence

Round 8 also recorded one direct control-equivalence artifact:

- `communications/PROOF_round8_control_equivalence_2026-03-21.json`

That comparison captures the hardcoded control and declarative candidate on the same two route-real jobs.

Observed bounded equivalence:

- same selected family per surface on both controls
- same `signal_summary` content per surface on both controls
- same rationale text per surface on both controls

Declared-family caveat:

- the declarative relationship surface rejects only families declared in its suite spec
- the hardcoded control also rejects `relationship_field_map`
- that asymmetry is intentional and in-scope because `relationship_field_map` remains outside the round-8 declarative pilot

The conditions surface remains fully aligned:

- both hardcoded and declarative paths emit the same selected family, same signals, same rationale, and the same rejected-family reason

## Bounded Disposition

This proof closes the bounded round-8 claim only:

- the declarative suite token is live on the shared genealogy route
- it reproduces the documented round-4 balance and matrix outcomes on the same control jobs
- it preserves the existing suite trace grammar and route failure contract

It does **not** claim:

- declarative support for `relationship_field_map`
- full replacement of every hardcoded genealogy suite branch
- declarative support for broader multi-workflow suites
- a general rule interpreter

Within that narrow claim, round 8 is now route-proof-complete.
