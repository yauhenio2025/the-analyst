# Memo: Round 8 / Declarative Adaptive Suite Scope

Date: 2026-03-21
Program: Thin Consumer Platformization

## Purpose

Define the scope for the next bounded program step after round 7.

This memo is meant to answer:

1. what the next meaningful structural variable is
2. why that variable is more valuable than another workflow-specific proof branch
3. what round 8 should and should not attempt
4. what evidence would be required before broader declarative-composition claims become credible

This memo sits beneath:

- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_completion.md`
- `communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_completion.md`
- `communications/MEMO_2026-03-20_round4_adaptive_surface_suite_completion.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

## Current Program Position

As of round 7, the program has already proved:

- one thin generic host path across two serious workflows
- one shared bounded-v2 consumer contract
- one reusable upstream artifact seam
- adaptive single-surface family selection
- adaptive multi-surface suite selection
- cross-workflow adaptive single-surface and suite behavior
- one bounded declarative single-surface substrate pilot

What remains unproved is no longer:

- whether adaptive behavior can work outside genealogy
- whether the generic host can carry adaptive divergence
- whether one declarative spec can select one family on one surface

The remaining structural gap is narrower:

- whether the round-7 declarative substrate can lift one already-proven adaptive suite without giving up fail-closed validation, workflow-scoped authorization, or the existing `adaptive_surface_suite_selection` trace grammar

## Why Round 8 Is Next

Round 6 already made another hardcoded workflow-specific proof branch lower-value.
Round 7 then made another declarative single-surface proof lower-value.

So the next honest question is:

- can declarative selection coordinate more than one adaptive target surface under one bounded suite contract

That is the smallest remaining structural variable in the current proof family.

It is also likely the last high-value proof question before the program should pivot from:

- proving more bounded variants

toward:

- renderer contract validation
- consumer consolidation
- bounded compose-from-intent work

## Recommended Round-8 Claim

Round 8 should prove one bounded thing:

- a repo-tracked declarative suite spec can coordinate an already-proven two-surface adaptive genealogy suite without giving up fail-closed validation, workflow-scoped authorization, code-owned rationale/trace enforcement, or the existing `adaptive_surface_suite_selection` trace grammar

The recommended proof target is:

- the already-proven genealogy relationship + conditions suite from round 4

This means the declarative pilot should target exactly:

- `genealogy_relationship_landscape`
- `genealogy_conditions`

## Recommended Proof Contract

Public proof route:

- `/p/:projectId/analysis/intellectual_genealogy?composition_mode=declarative_genealogy_relationship_conditions_suite_v1`

Trace route:

- `/v1/presenter/trace/{job_id}?consumer_key=the-critic&composition_mode=declarative_genealogy_relationship_conditions_suite_v1`

Hardcoded control:

- `adaptive_genealogy_relationship_conditions_v1`

Documentary control jobs:

- the round-4 balance fixture
- the round-4 matrix fixture

Required pre-proof check:

- verify that the two round-4 control fixtures still exist locally before planning execution against them

If those exact route-real controls are no longer present locally, round 8 may seed equivalent route-real controls later, but the proof standard should still be:

- declarative suite candidate versus hardcoded suite control on the same bounded contrast pair

## Why This Target Is The Right One

The genealogy relationship + conditions suite is the right target because:

1. it is already the most documented suite proof in the repo
2. its two surfaces have materially different runtime shapes and selection logic
3. the route, trace grammar, and proof artifacts already exist
4. it isolates the suite declarativization variable without introducing a second workflow or a second major seam

This round should not start with AOI because that would add extra proof variables:

- child-surface suite behavior under `aoi_thematic_analysis`
- AOI report-shape variability
- cross-workflow declarative widening

Those are lower-value before declarative suite behavior is proved on the simpler genealogy control.

## Scope Decision

## In Scope

Round 8 should stay constrained to:

1. one declarative suite proof token
2. one genealogy workflow only
3. one already-proven suite pair only
4. one repo-tracked suite spec shape
5. code-owned extractors, builders, rationale, validation, and trace grammar
6. route-real equivalence proof against the hardcoded round-4 control

The intended proof shape is:

1. declarative suite spec resolves the two target surfaces
2. each target surface still uses code-owned signal extraction
3. per-surface family selection is driven by validated declarative rules
4. suite trace stays `adaptive_surface_suite_selection`
5. runtime payloads are still validated before mutation
6. the generic Critic host still restores the result without workflow-specific UI logic

Round 8 is therefore not a tiny wrapper over round 7.
It still needs bounded new suite-specific machinery:

- one suite-aware spec shape
- one suite-aware executor and inspector path
- one new conditions declarative extractor/builder registration path
- one suite-aware invalid-spec / invalid-surface ownership rule

## Out Of Scope

Round 8 should not attempt:

- declarative AOI suite support
- declarative multi-workflow registries
- declarative `relationship_field_map`
- declarative rationale prose
- declarative rejected-family prose
- declarative trace-stage naming
- arbitrary boolean/expression interpreters
- spec-owned renderer JSON
- broad “adaptive registry” framing

## Declarative Boundary For Round 8

Round 8 should carry forward the round-7 discipline.

The recommended schema approach is:

- keep the existing `AdaptiveCompositionSpec` frozen as the single-surface schema
- add one new bounded suite schema for round 8 rather than widening the single-surface schema in place

In concrete terms, round 8 should prefer:

- one suite-level spec containing:
  - suite mode identity
  - workflow key
  - a list of per-surface sub-spec entries
- where each per-surface entry carries:
  - `target_surface`
  - `signal_extractor_key`
  - `default_family`
  - `families`
  - `decision_rules`

Round 8 should not widen the existing single-surface schema into an awkward hybrid with both singular and plural target fields.

The declarative layer should own only:

- suite mode identity
- workflow key as a checked consistency field
- target surface membership
- per-surface family catalog
- per-surface decision rules
- per-surface default family
- extractor and builder dispatch keys

The declarative layer should not own:

- payload extraction logic
- signal aggregation code
- runtime builder logic
- rationale prose
- rejected-family prose
- trace grammar
- route error mapping
- workflow authorization

In other words:

- the spec should describe what family ladder exists
- the code should still enforce how the suite actually runs

Round 8 should also keep key legality tied to the same shared constants used by runtime dispatch.
It should not create a second registry-local source of truth for:

- signal extractor keys
- builder template keys

## Key Structural Questions Round 8 Must Answer

Round 8 must answer these bounded questions:

### 1. Can suite membership be declared without inventing a general interpreter?

The round-7 single-surface pilot already proved a bounded rule ladder.
Round 8 must show that a small suite wrapper can compose two such surface decisions without becoming a runtime mini-language.

### 2. Can declarative suite selection preserve the existing trace discipline?

The trace shape should remain:

- `adaptive_surface_suite_selection`

with per-surface decisions under one suite stage.

Round 8 should prove that the declarative path reuses that grammar rather than creating a second suite-trace dialect.

### 3. Can declarative suite selection stay fail-closed?

Round 8 must preserve the same failure discipline already proved in hardcoded suite mode:

- invalid mode or workflow pairing -> `400`
- accepted-mode spec or runtime validation failure -> `409`
- trace -> `200` with diagnostics for post-acceptance failures

### 4. Can equivalence be demonstrated without overclaiming?

Round 8 does not need full deep-equality between the hardcoded and declarative traces.
It does need a bounded equivalence standard strong enough to matter:

- same selected family per target surface
- same signal-summary content per target surface
- same rationale text where surfaces/families overlap
- same renderer shape and structured payload family output
- same suite trace grammar

It does not need to claim full semantic replacement of the hardcoded suite control in round 8.

Because declarative `relationship_field_map` remains out of scope, the honest round-8 proof standard is:

- bounded equivalence on the documented dossier/balance and comparison/matrix control cases

not:

- total replacement of every family branch the hardcoded suite token can still reach

### 5. Can the conditions selector stay declarative without widening the rule language?

The conditions branch is the main suite-specific expressivity question.

Round 8 should keep the predicate language bounded and non-interpreter.
That means the code-owned conditions extractor should emit the derived metrics the rule ladder actually needs, for example:

- `path_signal`
- `balance_signal`
- `path_dependencies_count`

Then the declarative rules can stay as constant-threshold checks over those derived metrics.

Round 8 should not widen the declarative predicate language just to encode conditions arithmetic inside the spec.

## Likely Proof Shape

The likely declarative suite pilot should:

1. reuse the existing relationship signal callable already factored in round 7
2. reuse the existing conditions signal seam already proved in round 4
3. add one bounded suite spec that names both target surfaces through per-surface sub-spec entries
4. add one bounded declarative conditions family ladder:
   - `conditions_balance_sheet`
   - `conditions_path_dependency_matrix`
5. keep per-surface builders code-owned
6. keep suite rationale and rejected-family prose code-owned
7. keep the round-7 single-surface declarative schema intact rather than widening it into a polymorphic hybrid

The conditions declarative path will also need one new code-owned extractor/builder registration seam:

- add a conditions signal extractor key to the shared key constants
- register that extractor in the declarative extractor dispatch
- add the two conditions builder-template keys to the shared key constants
- register those builders in a code-owned builder dispatch

The round-8 suite path should not force `AdaptiveConditionsSelection` into the `AdaptiveSurfaceSelection` shape.
It is acceptable for the suite wrapper to keep heterogeneous per-surface selection objects, because `AdaptiveSurfaceSuiteSelection` already models a heterogeneous `surface_decisions` tuple in the hardcoded suite path.

The main integration points that planning must name explicitly are:

- `_SUPPORTED_COMPOSITION_MODES`
- `_MODE_WORKFLOW_MAP`
- `apply_bounded_dynamic_composition()`
- `inspect_runtime_composition()`
- `get_runtime_composition_stage_name()`
- `decision_trace.py` composition-mode inspection allowlist
- result, presenter, refresh, and single-view token threading
- Critic proof-label mapping
- focused backend and frontend route-token tests

One pre-existing implementation bug should also be treated as part of round-8 widening:

- `_load_adaptive_spec_or_raise_validation()` currently hardcodes `ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY` in one spec-load failure issue path

That helper must stop assuming a relationship-only target when suite/spec failures are attributed.

The likely contrast proof pair remains:

- one balance-oriented case
- one matrix-oriented case

That is enough to prove:

- dossier + balance
- comparison + matrix

under the same declarative suite token on the same generic route.

## Hard Stops

If any of the following become necessary, the tranche should stop and rescope:

1. spec-owned rationale prose
2. spec-owned trace grammar
3. declarative cross-surface dependency logic beyond a bounded suite wrapper
4. a general predicate or expression interpreter
5. AOI widening in the same tranche
6. declarativizing more than the two round-4 target surfaces

Those would indicate the team is drifting from:

- bounded declarative substrate proof

toward:

- premature adaptive registry design

## Invalid-Spec And Invalid-Surface Ownership

Round 8 must make suite-level failure attribution explicit before planning.

The memo’s recommended rule is:

- invalid requested mode or workflow pairing remains a route-level `400`
- accepted-mode suite-spec failures normalize into `BoundedCompositionValidationError`
- the guaranteed diagnostics surface on trace remains `composition_issues`
- per-stage suite details are best-effort

For issue ownership:

- suite-spec failures that happen before per-surface inspection should attach to a suite-level synthetic issue target rather than falsely blaming `genealogy_relationship_landscape`
- per-surface validation failures should attach to the actual failing `target_surface`

In other words:

- do not pretend every suite-spec failure is a relationship-surface failure

## What Round 8 Would Prove

If round 8 succeeds, the program can make a stronger but still bounded claim:

- the declarative adaptive substrate is now credible for both single-surface and suite selection on an already-proven workflow route

That would not yet prove:

- a many-workflow declarative registry
- declarative AOI suites
- arbitrary workflow generation
- full compose-from-intent

But it would likely close the last major proof gap in the current adaptive/declarative ladder.

## What Should Probably Come After Round 8

If round 8 lands cleanly, the next program move should probably not be round 9 as another proof-token branch.

The more coherent follow-on sequence would be:

1. freeze the bounded declarative substrate v1 discipline
2. move to renderer contract validation
3. then consumer consolidation
4. then a bounded compose-from-intent pilot

That order matters because:

- more proof-branch work after round 8 risks repetition
- renderer contracts are the main missing safety layer before broader composition expansion
- consumer consolidation is the clearest visible thesis move after the proof ladder is strong enough

## Final Recommendation

If the team needs one operational sentence for round 8, it should be:

- **Use round 8 to prove one bounded declarative suite lift on the already-proven genealogy relationship + conditions pair, keep the proof claim honest about its two documented contrast cases, and then treat that as the likely end of the current proof ladder before pivoting toward renderer contracts and stronger platform law.**
