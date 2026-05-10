# Memo: Next Stage Scope - Round 7 / Declarative Adaptive Substrate Proof

Date: 2026-03-21
Program: Thin Consumer Platformization

## Purpose

Define the next bounded stage after round 6.

This memo answers:

1. what rounds 1 through 6 have now actually established
2. what meaningful platform variable still remains unproven
3. what the next proof should be if the goal remains beautiful-by-default thin consumers
4. what that proof should and should not attempt

This is a scope memo, not an execution plan.

## Basis For This Scope

The governing record for this stage is now:

- `communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `communications/PROOF_2026-03-19_thin_consumer_platformization_round1.md`
- `communications/MEMO_2026-03-20_round2_bounded_dynamic_composition_completion.md`
- `communications/MEMO_2026-03-20_round3_adaptive_surface_family_completion.md`
- `communications/PROOF_2026-03-20_round3_adaptive_surface_family.md`
- `communications/MEMO_2026-03-20_round4_adaptive_surface_suite_completion.md`
- `communications/PROOF_2026-03-20_round4_adaptive_surface_suite.md`
- `communications/MEMO_2026-03-21_round5_cross_workflow_adaptive_aoi_theme_completion.md`
- `communications/PROOF_2026-03-21_round5_cross_workflow_adaptive_aoi_theme.md`
- `communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_completion.md`
- `communications/PROOF_2026-03-21_round6_cross_workflow_adaptive_aoi_suite.md`
- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/decision_trace.py`

The program sequence is now clear:

- round 1 proved the thin host and shared contract
- round 2 proved bounded runtime regrouping
- round 3 proved single-surface adaptive family selection
- round 4 proved multi-surface adaptive suite composition
- round 5 proved cross-workflow single-surface adaptive composition
- round 6 proved cross-workflow multi-surface adaptive suite composition

## Current Program Position

The behavioral question is no longer the problem.

The codebase now already proves that adaptive composition can be:

- deterministic
- fail-closed
- trace-inspectable
- workflow-scoped
- host-generic in substance

But one structural question remains open:

- can the already-proven adaptive patterns be lifted out of one-off hardcoded mode branches into structured configuration without losing the properties that made the hardcoded proofs trustworthy

That is the next variable to isolate.

## Core Strategic Judgment

The next proof should not be:

- another workflow-specific hardcoded mode branch
- another AOI-only expansion
- another genealogy-only expansion
- a broad adaptive registry vision memo
- a general-purpose interpreter
- arbitrary workflow generation
- whole-page adaptive generation

The next proof should be:

- one **bounded declarative adaptive-substrate proof**

Round 7 should isolate one question only:

- can one already-proven adaptive pattern be expressed through repo-tracked structured configuration while the existing runtime executor, validation path, and trace grammar remain the enforcement layer

That is the smallest next proof that materially advances the platform thesis after round 6.

## Recommended Label

Use:

- **Thin Consumer Platformization Round 7**

More specifically:

- **Declarative Adaptive Substrate Proof**

Do not call this:

- generalized adaptive composition
- adaptive registry rollout
- substrate migration
- adaptive engine platform

## Documentary Gate

Round 7 can now be scoped without qualification.

Round-6 documentary status is closed in:

- `communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_completion.md`

So unlike rounds 5 and 6, there is no still-open prior-round proof note blocking round-7 scoping.

That said, scope should still stay tighter than an implementation plan:

- round 7 should be reviewed critically before code begins

## What Round 7 Should Actually Prove

Round 7 should prove one bounded thing:

- one existing adaptive mode can be re-expressed through structured configuration and still produce behaviorally equivalent family selection, validation, and trace output

Important clarification:

- this is not a proof that *all* adaptive modes should become declarative immediately
- it is not a proof that arbitrary families or rules should be authored in data files
- it is not a proof that hardcoded selector logic should disappear

It is a narrower claim:

- a small declarative substrate can sit on top of the current proven runtime path

## Recommended First Target

The first declarative substrate proof should target:

- `genealogy_relationship_landscape`

under a new proof-only mode on the existing genealogy route.

### Why This Is The Right Pilot

`genealogy_relationship_landscape` is the best first substrate pilot because:

1. it was the first successful adaptive target in round 3
2. it has the cleanest control record for dossier and comparison cases
3. its selector signals are stable and already well-exercised in proof fixtures
4. it avoids the child-surface and thinker-scoping complexity present in AOI
5. it isolates the structural substrate question without entangling the harder suite-coordination question

### Why Not Start With A Suite Mode

A suite mode is the wrong first substrate pilot because it introduces two questions at once:

1. can adaptive selection be declared
2. can suite coordination also be declared

Round 7 should prove only the first.

### Why Not Start With AOI

AOI is already proven behaviorally in rounds 5 and 6, but it is not the cleanest first substrate pilot because:

1. the child-surface constraints are stricter
2. the route carries thinker-specific scoping concerns
3. the report family contracts are newer than the genealogy relationship contracts

Round 7 should prefer the simplest mature adaptive seam, not the most recent one.

## Recommended Activation Contract

Use the existing genealogy generic route with one new proof-only mode:

- `/p/:projectId/analysis/intellectual_genealogy?composition_mode=declarative_relationship_surface_v1`

Hard rules:

- `declarative_relationship_surface_v1` is independent of:
  - `adaptive_relationship_surface_v1`
  - `adaptive_genealogy_relationship_conditions_v1`
  - `adaptive_aoi_theme_surface_v1`
  - `adaptive_aoi_theme_report_suite_v1`
  - `bounded_dynamic_genealogy_v1`
- do not stack proof modes
- do not replace `adaptive_relationship_surface_v1`

This new token exists so round 7 can compare:

- the current hardcoded relationship proof path
- the new declarative-substrate relationship proof path

on the same route and fixtures.

## Boundaries For The Substrate

Round 7 should not attempt a general-purpose rule engine.

The substrate should be closer to:

- structured configuration that the existing proven code path reads

than to:

- a new runtime that replaces the proven code path

That means the substrate should stay bounded to:

1. repo-tracked static configuration
2. workflow-scoped authorization declared in data
3. one named target surface
4. one named signal-extraction callable already implemented in code
5. one ordered decision ladder over supported metric predicates
6. one declared family catalog that points at registered builder templates
7. existing validation and trace code as the authoritative enforcement layer

Round 7 should explicitly reject:

- arbitrary expressions
- Python evaluation from config
- JMESPath or SQL-like selector languages
- user-authored runtime code
- generated config

## Recommended Declarative Shape

The first substrate proof should introduce one repo-tracked composition spec for:

- `declarative_relationship_surface_v1`

Recommended storage shape:

- file:
  - `src/presenter/adaptive_specs/definitions/declarative_relationship_surface_v1.json`
- format:
  - JSON
- loading pattern:
  - one thin presenter-side registry that loads and validates adaptive specs at startup
- schema enforcement:
  - one Pydantic model, reviewed before implementation begins

This registry should be minimal:

- no generalized plugin system
- no lazy remote loading
- no cross-module rule resolution

In round 7, `signal_extractor_key` should remain only a simple dispatch key to one code-owned callable.

That callable may internally do multiple steps, but the spec should not describe those steps. In the current relationship path that still means one code-owned extraction pipeline:

1. extract cards
2. decorate cards
3. aggregate signals

Round 7 should not introduce a second declarative layer for that pipeline.

That spec should declare at least:

- `composition_mode`
- `workflow_key`
- `target_surface`
- `signal_extractor_key`
- `default_family`
- `families[]`
- `decision_rules[]`

### Families

Round 7 should stay bounded to the two relationship families that already have route-real control coverage:

1. `relationship_profile_dossier`
2. `relationship_comparison_review`

Explicitly out of round-7 proof scope:

- `relationship_field_map`

Reason:

- it is implemented and tested in code, but it is not covered by the stated route-real round-3 control pair
- round 7 should not claim declarative equivalence for a family that sits outside its proof standard

Each family entry should declare:

- `family_key`
- `builder_template_key`
- `view_name`

Round 7 should not attempt freeform renderer JSON in the spec.

Instead:

- family builders remain registered code templates
- the spec chooses among them declaratively

That keeps the substrate bounded and keeps strict validation on the existing path.

Round 7 should also keep user-facing rationale and rejected-family prose in code.

That means the v1 spec should **not** declare:

- trace stage names
- description templates
- rationale templates
- rejected-family reason templates

Those remain code-owned so round 7 does not introduce a second templating runtime.

### Decision Rules

The decision ladder should be bounded to supported metric predicates over an already-proven signal set such as:

- `relationship_count`
- `distinct_relationship_types`
- `top_score`
- `second_score`
- `score_gap`
- `top_share`

The decision ladder should remain:

- ordered
- deterministic
- first-match wins
- fallback-aware through one explicit `default_family`

It should not support:

- arbitrary boolean languages
- nested condition trees beyond what is needed for the current relationship proof
- family-specific custom code loaded from config

For round 7, the cleanest shape is:

- one positive dossier rule
- one explicit `default_family = relationship_comparison_review`

This matches the control cases actually being proven.

## Pre-Execution Gate

Before any implementation plan is written, the adaptive-spec schema itself should be treated as a reviewable artifact.

That preflight gate should define and freeze:

- spec file location
- JSON schema / Pydantic model
- legal `signal_extractor_key` values
- legal `builder_template_key` values
- legal comparison operators for `decision_rules`
- required `default_family`

If that schema is still fuzzy, round 7 is not execution-plan ready.

## What Must Stay Hardcoded In Round 7

Round 7 should keep the following in code:

- the signal extraction implementation
- the builder template implementations
- rationale generation
- rejected-family reason generation
- validation calls
- trace emission and trace schema
- route-level error mapping

This is intentional.

The proof is not:

- “can we data-drive everything”

The proof is:

- “can we lift one proven adaptive pattern into bounded structured configuration without weakening the runtime contract”

## Required Equivalence Standard

Round 7 should not be judged by “it kind of works.”

It should be judged against a control.

Use the existing round-3 dossier and comparison proof record as the **semantic control**, but do not make executor-database fixtures a hard dependency of pytest.

The automated equivalence standard should instead use:

- synthetic payloads in pytest that reproduce the round-3 dossier-like signal distribution
- synthetic payloads in pytest that reproduce the round-3 comparison-like signal distribution

The route-real round-3 proof record remains the documentary control:

- `proof-round3-adaptive-dossier-final-1774002300`
- `proof-round3-adaptive-comparison-final-1774002300`

The declarative mode should be considered successful only if, on those synthetic controls:

1. it selects the same runtime family as `adaptive_relationship_surface_v1`
2. it returns the same renderer family shape
3. it remains fail-closed on invalid config or invalid runtime payload
4. it emits trace output through the same `adaptive_surface_selection` grammar
5. its normalized trace details remain equivalent in substance even if the mode token differs

This is an equivalence-style proof, not a novelty proof.

## The Critic Boundary

The Critic host should remain generic.

Allowed frontend change:

- one generic proof-label mapping for `declarative_relationship_surface_v1`

Not allowed:

- workflow-specific host logic
- substrate-specific UI logic
- a separate host execution path for declarative modes

## What Round 7 Would Enable If It Passes

If round 7 passes, the next meaningful option becomes available:

- porting one existing suite mode onto the same declarative substrate shape

But that should be a later proof.

Round 7 itself should not promise:

- migration of all current modes
- broad registry rollout
- removal of hardcoded branches

## Bottom Line

The next coherent program move is:

- one bounded declarative substrate proof on `genealogy_relationship_landscape`

with a new proof-only token:

- `declarative_relationship_surface_v1`

and one narrow question:

- can the already-proven adaptive relationship pattern be declared without losing determinism, fail-closed validation, workflow authorization, or trace inspectability

If the answer is yes, the program can move from proving adaptive behavior to proving a minimal adaptive substrate.
