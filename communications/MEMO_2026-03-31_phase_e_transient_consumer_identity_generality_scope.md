# Memo: Phase E Transient Consumer Identity Plurality Scope

Subtitle: One additional admitted proof-only consumer identity over the already-proved proof harness

Date: 2026-03-31
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Most Recent Completion:
- `communications/MEMO_2026-03-31_phase_e_transient_proof_harness_v1_completion.md`
Relevant Prior Scope:
- `communications/MEMO_2026-03-31_phase_e_host_neutral_transient_harness_scope.md`
Relevant Proof Artifacts:
- `communications/PROOF_phase_e_transient_proof_harness_source_selection_2026-03-31.json`
- `communications/PROOF_phase_e_transient_proof_harness_genealogy_direct_sections_2026-03-31.json`
- `communications/PROOF_phase_e_transient_proof_harness_source_selection_live_closeout_2026-03-31.json`
- `communications/PROOF_phase_e_transient_proof_harness_genealogy_direct_sections_live_closeout_2026-03-31.json`

## Purpose

Define the next bounded Phase E question now that the program has already proved:

- the current-consumer matrix over the live transient handoff families
- the full bounded `aoi-canary` transient second-consumer line
- one proof-only transient consumer contract plus one standalone minimal harness over:
  - AOI `source_selection`
  - genealogy `direct_sections`

The next honest question is no longer:

- another shell boundary proof
- another `aoi-canary` route broadening
- another harness repo
- or broad generic consumer architecture

It is:

- is the transient substrate still effectively special-cased to one proof-only consumer identity, or can the hard-coded analyzer admission surface tolerate one additional admitted proof-only consumer key over the exact same harness and exact same two proof cases?

The claim this slice would support must stay narrow:

- analyzer transient admission is not coupled only to `transient-proof-harness`; one second proof-only consumer identity can ride the same minimal harness and same two already-proved transient seams, with end-to-end `consumer_key` propagation remaining intact

not:

- broad generic consumer registration
- source-profile generality on proof-only consumers
- lifecycle generality
- or a reusable general host runtime

## Current Code-Backed Boundary

### What is already true

Analyzer-v2 now serves transient proof across three consumer identities:

- `the-critic`
- `aoi-canary`
- `transient-proof-harness`

But only one of those is a standalone proof-only consumer contract outside both earlier shells:

- `transient-proof-harness`

The current proof-only harness slice already proves:

- one AOI path:
  - `source_selection`
- one non-AOI path:
  - `direct_sections`
- one separate harness boundary
- one separate proof-only consumer key

### What is still missing

The remaining honest gap is not harness independence anymore.

The remaining honest gap is:

- consumer-identity plurality at the analyzer admission layer

Right now:

- transient admission is still hard-coded in:
  - `src/presenter/compose_from_intent.py`
  - specifically `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS`
- source-profile follow-up gating is still hard-coded separately in:
  - `src/presenter/compose_from_intent.py`
  - specifically `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER`
- AOI source-profile readiness still reuses that same capability truth through:
  - `src/analysis_products/source_backed_readiness.py`
- the current proof-only harness still proves only one such proof-only consumer identity:
  - `transient-proof-harness`

So the stronger remaining question is:

- can the same minimal harness and same two already-proved transient seams survive one additional admitted proof-only consumer identity without widening routes, schemas, readiness, or lifecycle?

## Strategic Decision

The next bounded Phase E slice should keep the proof harness fixed and vary only consumer identity.

Keep fixed:

- the standalone harness repo:
  - `/home/evgeny/projects/transient-proof-harness`
- the two proof cases:
  - AOI `source_selection`
  - genealogy `direct_sections`
- the compose routes:
  - `compose-from-selection`
  - `compose-from-intent`
- the request/response schemas
- the renderer support surface
- fixture-backed operation

Vary:

- one additional admitted proof-only consumer identity

The exact recommended target is:

- add one second proof-only consumer definition:
  - suggested key: `transient-proof-probe`
- admit it only on:
  - `source_selection`
  - `direct_sections`
- make the existing harness selectable between:
  - `transient-proof-harness`
  - `transient-proof-probe`

Why this is the right next bounded variable:

1. the harness boundary is already proved
2. the workflow pair is already proved
3. the compose routes are already proved
4. the remaining open variable is whether analyzer-side proof-only consumer identity is still effectively singular on the current hard-coded admission line
5. this is still narrower and cleaner than jumping to lifecycle or generic consumer architecture
6. this is the thinnest useful step before a structurally stronger question must follow

## Proposed Scope

### 1. One additional proof-only consumer identity

Add one second proof-only consumer definition alongside `transient-proof-harness`.

It should:

- be proof-oriented
- use the same renderer capability surface as `transient-proof-harness`
- stay neutral and non-productized
- be admitted only on:
  - `source_selection`
  - `direct_sections`

This slice must name the real code seams explicitly:

- add one new consumer definition file in:
  - `src/consumers/definitions/`
- add one bounded new entry in:
  - `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS`
- add no entry in:
  - `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER`

It should not:

- admit `source_profile`
- widen readiness behavior
- widen lifecycle behavior
- trigger a generic registry refactor

### 2. Keep the same harness and parameterize only consumer identity

Do not create another repo and do not build another shell.

Keep:

- `/home/evgeny/projects/transient-proof-harness`

Broaden it only enough to select between:

- `transient-proof-harness`
- `transient-proof-probe`

The harness should still:

- replay pinned fixtures only
- use `planning_decision_id` as local identity only
- normalize structurally only
- validate against frozen proof metadata
- render:
  - `tab` through `TabShell`
  - non-`tab` through `RendererHost`

It must not:

- derive requests locally
- fetch planning decisions
- fetch lowering routes
- discover results
- reconstruct semantics

### 3. Fresh proof lineage under the new identity

Do not reuse the old proof-only harness artifacts as final proof under the new consumer key.

Generate fresh artifacts under the new identity:

- one analyzer proof bundle for AOI `source_selection`
- one analyzer proof bundle for genealogy `direct_sections`
- one live closeout per case

Use the existing harness and same lineage anchors:

- AOI `source_selection`
  - `source_v2_job_id = job-744edf255ad5`
  - `planning_decision_id = planning-decision-d6b6bb0cd7ac`
- genealogy `direct_sections`
  - `planning_decision_id = planning-decision-5f5b0182f2f9`

### 4. Keep fail-closed boundaries exact

This slice should prove one additional admitted proof-only consumer identity, not broader route or lifecycle law.

So the following must remain fail-closed:

- `source_profile` for the new proof-only consumer
- readiness on AOI `source_profile` for the new proof-only consumer
- any broader workflow widening
- any new consumer-architecture generalization work

## Acceptance Bar

The slice should count as complete only if all of the following are true:

1. analyzer-v2 admits the new proof-only consumer only on:
- `source_selection`
- `direct_sections`

1a. analyzer tests assert the admission shape explicitly at the hard-coded seam:
- the new key is present in `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS`
- the admitted set is exactly:
  - `source_selection`
  - `direct_sections`

2. analyzer-v2 still blocks the new proof-only consumer on:
- `source_profile`

2a. analyzer tests also assert there is no `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER` entry for the new key

2b. `tests/test_source_backed_readiness.py` includes an explicit negative regression proving AOI `source_profile` remains blocked for the new key

3. the existing `transient-proof-harness` consumer remains unchanged and still passes

4. the same standalone harness can successfully exercise both consumer identities without code branching by workflow beyond the existing fixture-kind dispatch

5. fresh analyzer proof bundles under the new consumer key exist for:
- AOI `source_selection`
- genealogy `direct_sections`

6. fresh live closeout artifacts under the new consumer key exist for both cases

7. each fresh live closeout records:
- exact observed request
- request equality to the pinned fixture
- `response_status = 200`
- exact `response.presentation.consumer_key`
- observed root renderer
- observed raw-json leaf set
- forbidden analytical upstream requests observed

8. the new consumer keeps the same bounded render law:
- AOI case preserves a `tab` root plus its freshly observed raw-json leaf set
- genealogy case preserves a `card_grid` root plus empty raw-json leaf set

9. the completion memo must state the claim honestly as plurality, not generality:
- this proves allowlist plurality plus end-to-end `consumer_key` propagation on the same harness surface
- it does not prove definition-driven admission or materially stronger renderer-adaptation generality

## Out Of Scope

This slice should not include:

- `source_profile` on the new proof-only consumer
- readiness broadening
- lifecycle save/reopen on the new proof-only harness
- generic consumer registration refactors
- new harness repos
- productization of the proof harness

## Honest Decision Rule

If implementation starts requiring:

- generic registry refactors
- broader lifecycle law
- planner/result discovery in the harness
- or renderer-surface expansion

stop and rescope.

That would no longer be a bounded consumer-identity plurality slice.

## Recommended Next Claim

If this slice closes honestly, the stronger but still bounded program claim becomes:

- analyzer transient admission is not coupled only to one proof-only consumer identity; the same minimal harness can carry two proof-only consumer keys over the same AOI and non-AOI transient seams, with correct end-to-end `consumer_key` propagation

The next broader gap after that would likely be:

- broader lifecycle law on the proof-only line

not:

- immediate generic consumer architecture
