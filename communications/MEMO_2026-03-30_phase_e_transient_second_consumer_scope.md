# Memo: Phase E Transient Second-Consumer Scope

Subtitle: The next bounded generality proof after the representative composition matrix

Date: 2026-03-30
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
Relevant Prior Consumer Proof:
- `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md`

## Purpose

Define the next bounded Phase E step after the representative composition matrix landed.

The first bounded Phase E question is now answered:

- analyzer-v2 can already compose across the full currently live handoff-family substrate on the current transient consumer surface

The next bounded question is different:

- can the same transient compose substrate serve one real second consumer without host-local analytical reconstruction?

## Strategic Framing

The right next move is not:

- another same-consumer composition matrix
- another governance family
- a generic consumer plugin architecture
- arbitrary engine/pass combinatorics
- a full multi-consumer product surface

The right next move is:

- one bounded transient second-consumer proof over the already-proved transient compose substrate

This does reopen a seam that historically appeared earlier in the older stage ledger.
That is acceptable.
The reason it is the right next Phase E question now is simple:

- the first matrix already proved handoff-family breadth on `the-critic`
- the remaining bounded unresolved variable is consumer-surface generality

## Why This Is The Right Next Slice

Three repo facts now matter together:

1. the transient compose substrate still hard-enforces one registered consumer adapter:
   - `the-critic`
2. analyzer-v2 already carries a real second consumer definition:
   - `aoi-canary`
3. `aoi-canary` already has a bounded result-backed second-consumer proof, but not a transient one

That means the next honest step is not to invent a new consumer.
It is to use the existing second consumer and prove one bounded transient path through it.

## Scope Decision

### In scope

#### 1. One bounded second transient consumer target

The default target is:

- `aoi-canary`

Why:

- it already exists
- it is active in the analyzer consumer registry
- it already has a bounded result-backed second-consumer proof
- it is AOI-focused, which keeps the proof surface narrow

This slice should not widen to:

- `visualizer`
- `analyzer-mgmt`
- a new synthetic consumer

#### 2. One bounded transient proof path

The default proof path should be:

- AOI `source_selection`

That means:

- current planner-backed AOI handoff law
- existing `POST /v1/presenter/compose-from-selection`
- one transient response rendered by `aoi-canary`

Why this is the right default:

- it is the richer analyzer-owned transient AOI path
- it proves planner-backed serving rather than only a host-picked profile preset
- it reuses the evolution-ready four-family selection shape already ratified in the matrix proof

Fallback only if the default path exposes unrelated consumer UI debt:

- AOI `source_profile` dossier

That fallback is weaker and should not be treated as equally cheap.
It is acceptable only as a bounded unblocker.
It is not the preferred target.
It also carries extra analyzer-side uncoupling work if the proof wants the readiness/followup story to stay honest, because `source_backed_readiness` still reports `compose-from-source` as blocked for any consumer other than `the-critic` in v1.

#### 3. One bounded analyzer-side transient consumer expansion

The analyzer-side change should stay narrow.

Allowed:

- add `aoi-canary` to the bounded transient consumer allowlist/registration surface used by transient compose validation

Not allowed:

- replacing the closed set with generic consumer discovery
- a new transient consumer plugin system
- pretending the current code is already consumer-neutral

The memo should stay honest about the actual code boundary:

- this slice requires real analyzer-side runtime work
- the current transient compose substrate is not already consumer-general
- for the default `source_selection` path, that work is primarily at the transient compose consumer gate
- for any `source_profile` fallback or readiness-facing acceptance story, analyzer-side uncoupling is slightly larger because `source_backed_readiness` still hardcodes `compose-from-source` to `the-critic` in v1

#### 4. One bounded consumer-adaptation truth

The proof should accept analyzer-side consumer adaptation where it already exists.

This matters because `aoi-canary` currently declares:

- `accordion`
- `card_grid`
- `tab`
- `raw_json`

and does not declare top-level `prose`.

That means a bounded second-consumer transient proof may honestly include:

- analyzer-side renderer adaptation from unsupported `prose` to `raw_json`

That is acceptable for this slice if:

- the adaptation happens analyzer-side
- the host does not reconstruct analytical meaning locally
- the proof states clearly that the claim is contract-serving and thin-hostness, not polished consumer parity
- the adaptation is limited to narrow unsupported surfaces rather than becoming the dominant rendered outcome

#### 5. One real live proof bundle under `communications/`

This slice should end with one frozen proof record under `communications/`.

Recommended artifact set:

- one proof note describing the target, environment, and outcome
- one JSON summary tying together:
  - `consumer_key = aoi-canary`
  - `planning_decision_id` if planner-backed
  - compose request/response truth
  - any analyzer-side adaptation truth
- one browser/network artifact set sufficient to show:
  - the transient request path
  - the rendered second-consumer state

The proof should stay bounded:

- one real transient canary success path
- optionally one fail-closed negative path if it is cheap and directly relevant

#### 6. Focused analyzer and canary verification

This slice is cross-repo in practice.

Analyzer-side verification should cover:

- transient consumer allowlist/registration acceptance
- unchanged request/response schema families
- any analyzer-side renderer adaptation used for the canary proof path

Canary-side verification should cover:

- thin-host request/response handling over the chosen transient path
- no host-side analytical reconstruction
- truthful rendering of the analyzer-owned transient response

### Out of scope

- non-AOI second-consumer transient proof
- more than one second consumer
- generalized transient consumer marketplace/registry architecture
- lifecycle expansion
- new governance families
- arbitrary engine/pass matrices
- UI productization or consumer-polish work beyond what is needed for honest proof

## Honest Claim Boundary

If this slice lands cleanly, the honest claim is:

- analyzer-v2 transient compose is no longer structurally single-consumer-only for one bounded AOI transient path

The honest non-claim is:

- analyzer-v2 has not yet proven broad consumer generality
- analyzer-v2 has not yet proven non-AOI transient second-consumer support
- analyzer-v2 has not yet proven arbitrary engine/pass composition
- analyzer-v2 has not yet proven consumer-neutral product UX

## Proposed Acceptance Bar

This slice should count only if all of the following are true:

1. analyzer-v2 accepts `consumer_key = aoi-canary` on the chosen transient proof path
2. the public transient route shape stays unchanged
3. the served response shape stays unchanged
4. the host renders the analyzer-owned transient response without workflow-specific analytical reconstruction
5. any unsupported-renderer fallback used by the proof happens analyzer-side, not in consumer-local analytical glue
6. any `prose -> raw_json` adaptation remains a limited bounded fallback, not the dominant rendered outcome
7. the proof record is frozen under `communications/`
8. focused analyzer and canary verification pass

## Practical Constraints

This slice is not artifact-only in the way the matrix proof was.

It will likely require:

- analyzer repo changes
- `aoi-canary` repo changes
- one live local or deployed proof capture

That is acceptable.
It is still the smallest honest next move.

## Decision

The next bounded Phase E step should be:

- one transient second-consumer proof over `aoi-canary`

The default proof target should be:

- AOI `source_selection`

The strategic reason is simple:

- Phase E has now proved handoff-family breadth on one consumer
- it has not yet proved that the transient compose substrate serves more than one consumer

That second-consumer seam is the right next variable to test.
