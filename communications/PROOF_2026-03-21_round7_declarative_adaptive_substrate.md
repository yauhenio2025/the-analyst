# Round 7 Proof: Declarative Adaptive Substrate

Date: 2026-03-21

## Scope

This proof closes Round 7 / Declarative Adaptive Substrate Proof for the bounded declarative relationship pilot.

Target contract:

- generic genealogy host route:
  - `/p/:projectId/analysis/intellectual_genealogy?composition_mode=declarative_relationship_surface_v1`
- adaptive target surface:
  - `genealogy_relationship_landscape`
- declarative families in scope:
  - `relationship_profile_dossier`
  - `relationship_comparison_review`
- required claim:
  - the already-proven relationship adaptive pattern can be driven by a repo-tracked declarative spec while signal extraction, builder execution, validation, and trace grammar remain code-owned

## Control Note

Round 7 did not seed a new proof-job pair.

It reused the existing round-3 documentary controls:

- `proof-round3-adaptive-dossier-final-1774002300`
- `proof-round3-adaptive-comparison-final-1774002300`

Reason:

- round 7 is an equivalence proof, not a new relationship-family discovery proof
- round 3 had already established the hardcoded control pair for dossier vs comparison on the generic genealogy route
- round 7 needed to show that the new declarative mode selects the same family from the same structured payloads on the same route

That keeps the proof narrow and honest:

- no new synthetic fixture story was introduced
- the route-real controls were already documented in round 3
- round 7 only adds the new declarative composition token and its equivalence evidence

## Final Proof Fixtures

### Dossier Control

- analyzer-v2 job:
  - `proof-round3-adaptive-dossier-final-1774002300`
- Critic project:
  - `round3-proof-dossier-final-1774002300`
- hardcoded control family:
  - `relationship_profile_dossier`
- declarative expected family:
  - `relationship_profile_dossier`
- expected declarative surface title:
  - `Relationship Dossier`

### Comparison Control

- analyzer-v2 job:
  - `proof-round3-adaptive-comparison-final-1774002300`
- Critic project:
  - `round3-proof-comparison-final-1774002300`
- hardcoded control family:
  - `relationship_comparison_review`
- declarative expected family:
  - `relationship_comparison_review`
- expected declarative surface title:
  - `Relationship Comparison Review`

## Automated Route Proof

The route checks were executed against the local stack:

- analyzer-v2:
  - `http://127.0.0.1:8002`
- Critic API:
  - `http://127.0.0.1:5555`
- Critic webapp:
  - `http://127.0.0.1:3000`

### Dossier Route

Route:

- `/p/round3-proof-dossier-final-1774002300/analysis/intellectual_genealogy?composition_mode=declarative_relationship_surface_v1`

Observed:

- generic workspace restored successfully
- `Composition: declarative adaptive substrate proof` rendered
- `Relationship Dossier` rendered in the top-level view list
- no visible restore failure
- no visible `View not found`

Saved artifacts:

- `communications/PROOF_round7_dossier_final_page_2026-03-21.png`
- `communications/PROOF_round7_dossier_final_page_text_2026-03-21.txt`

### Comparison Route

Route:

- `/p/round3-proof-comparison-final-1774002300/analysis/intellectual_genealogy?composition_mode=declarative_relationship_surface_v1`

Observed:

- generic workspace restored successfully
- `Composition: declarative adaptive substrate proof` rendered
- `Relationship Comparison Review` rendered in the top-level view list
- no visible restore failure
- no visible `View not found`

Saved artifacts:

- `communications/PROOF_round7_comparison_final_page_2026-03-21.png`
- `communications/PROOF_round7_comparison_final_page_text_2026-03-21.txt`

## Trace Proof

### Dossier Trace

Trace endpoint:

- `/v1/presenter/trace/proof-round3-adaptive-dossier-final-1774002300?consumer_key=the-critic&composition_mode=declarative_relationship_surface_v1`

Result:

- `composition_status = applied`
- `adaptive_surface_selection` stage present
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

Rejected-family note:

- the declarative trace only rejected declared families:
  - `relationship_comparison_review`
- it did not emit a fake `relationship_field_map` rejection, because that family is explicitly out of scope for the round-7 declarative spec

Saved trace artifact:

- `communications/PROOF_round7_dossier_final_trace_2026-03-21.json`

### Comparison Trace

Trace endpoint:

- `/v1/presenter/trace/proof-round3-adaptive-comparison-final-1774002300?consumer_key=the-critic&composition_mode=declarative_relationship_surface_v1`

Result:

- `composition_status = applied`
- `adaptive_surface_selection` stage present
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

Rejected-family note:

- the declarative trace only rejected declared families:
  - `relationship_profile_dossier`

Saved trace artifact:

- `communications/PROOF_round7_comparison_final_trace_2026-03-21.json`

## Hardcoded Control Equivalence

Round 7 also reran the same two jobs through both:

- hardcoded control mode:
  - `adaptive_relationship_surface_v1`
- declarative candidate mode:
  - `declarative_relationship_surface_v1`

Recorded equivalence artifact:

- `communications/PROOF_round7_control_equivalence_2026-03-21.json`

Observed equivalence on both jobs:

- same `selected_family`
- same `signal_summary`
- same `rationale`

Observed deliberate non-equivalence:

- declarative rejected-family lists are narrower because they only include families declared in the round-7 spec
- this is intentional and matches the round-7 bounded scope:
  - `relationship_field_map` remains a hardcoded-only family outside the declarative pilot

## Disposition

Round 7 proof passes.

What is now proven:

1. `declarative_relationship_surface_v1` is a real upstream composition mode on the shared generic genealogy route
2. a repo-tracked declarative spec can drive family choice without moving signal extraction, builder execution, validation, or trace grammar out of code
3. the declarative mode is behaviorally equivalent to the hardcoded round-3 relationship control on the two route-real dossier/comparison proof jobs
4. trace inspectability survives the declarative lift through the existing `adaptive_surface_selection` grammar
5. the Critic host remains generic; the only visible host addition is the new proof label

What round 7 did not prove:

1. declarative support for `relationship_field_map`
2. declarative suite composition
3. a general-purpose adaptive interpreter
4. AOI declarative substrate support
5. spec-defined rationale prose or trace-stage naming
