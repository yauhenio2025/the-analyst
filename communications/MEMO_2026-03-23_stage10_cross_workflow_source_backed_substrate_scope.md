# Memo: Stage 10 / Cross-Workflow Source-Backed Substrate Scope

Subtitle: Workflow-Owned Source Adapters Over Durable Result Truth For AOI And Genealogy

Date: 2026-03-23
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Prior Stage Memo: `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_scope.md`
Stage 9 Completion: `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_completion.md`
Stage 9 Hardening Completion: `communications/MEMO_2026-03-23_stage9_aoi_handoff_profile_feasibility_hardening_completion.md`
Stage 7 Completion: `communications/MEMO_2026-03-23_stage7_aoi_source_to_composition_bridge_completion.md`

## Purpose

Define the next bounded stage after Stage 9 route-plus-hydrate-plus-plan normalization.

This memo is about the next missing downstream generalization seam:

- durable workflow result truth
- workflow-owned source-material adaptation where it exists
- workflow-owned result-backed composition readiness where source reconstruction does not yet exist
- normalized source-backed readiness and inspection
- bounded composition followup across more than one workflow family

It is not about:

- generalized task-driven page planning
- planner-driven surface selection across the whole product space
- universal host-contract cutover
- replacing all workflow-specific selector semantics with one fake shared enum
- broad objective expansion beyond the current AOI plus genealogy slice

## Why This Stage Now

Stages 7, 8, and 9 changed the program position in a very specific way.

Three things are now simultaneously true:

1. analyzer-v2 has one real AOI source-to-composition bridge in `src/presenter/composition_source_bridge.py`
2. analyzer-v2 now has bounded composition-facing task routing and planning seams in `route-task` and `plan-task`
3. the broader source-backed composition substrate is still AOI-specific at the point where durable workflow results become composition-eligible source truth

That means the next missing seam is not another planner wrapper.

It is:

- workflow-owned normalization of durable result truth into reusable composition source truth

The roadmap already names that seam as Stage 10.

## Explicit Sequencing Note

Stages 2-6 are still open in the canonical roadmap.

Scoping Stage 10 now is another intentional bridge-infrastructure pull-forward, just like Stages 7-9 were.

The reason is:

- the program now has real downstream AOI bridge code plus real upstream routing/planning seams
- the next missing connective tissue is the durable result-to-composition substrate between them
- later AOI task-driven composition, broader evaluation, and lifecycle work will be easier to do honestly if this substrate is explicit first

So this memo is not claiming that Stages 2-6 stopped mattering.

It is claiming that Stage 10 is the next bridge-infrastructure seam worth defining explicitly.

## Strategic Diagnosis

The current codebase already contains substantial pieces of the Stage 10 story.

### What is already real

AOI source-backed adapter law is real:

- `src/presenter/composition_source_bridge.py` resolves a formal AOI source catalog, selects preset-relative source families, and materializes deterministic sections for source-backed transient composition
- `src/presenter/compose_from_intent.py` exposes `POST /v1/presenter/compose-from-source`, even though it remains AOI-only and profile-driven

Durable result/presentation restore law is also real:

- `src/analysis_products/store.py` already registers corpora for both:
  - `anxiety_of_influence_thematic_single_thinker`
  - `intellectual_genealogy`
- `src/analysis_products/result_contract.py` already exposes product/result manifests and presentation restore over durable job truth for both workflows
- `src/api/routes/results.py` and `src/api/routes/presenter.py` already expose:
  - manifest reads
  - presentation reads
  - refresh
  - page assembly
  - optional `composition_mode`

Runtime composition law is also real:

- `src/presenter/bounded_dynamic_composition.py` already contains bounded composition modes for:
  - genealogy relationship surfaces
  - genealogy relationship/conditions suites
  - AOI theme/report surfaces

But those three things are not the same thing.

The current repo therefore has:

- one real AOI source-backed adapter path
- one shared result/presentation restore substrate
- one bounded runtime composition substrate

Stage 10 should not blur them together.

### What is not yet real

There is still no shared analyzer-owned source-backed substrate that says:

- given durable workflow result identity
- here is the workflow-owned source catalog or readiness state
- here are the allowed bounded selectors for that workflow
- here is the blocked selector set and why
- here is the downstream composition contract that follows

The AOI bridge is real, but it is AOI-specific.

The genealogy result/presentation substrate is real, but it is not yet a durable-result adapter with source-backed readiness semantics.

So the current system has:

- workflow-specific source-backed truth

It does not yet have:

- a reusable source-backed substrate across workflows
- a concrete genealogy durable-result adapter
- a normalized readiness contract that distinguishes:
  - AOI source reconstruction
  - genealogy restore/runtime composition readiness

## The Real Stage 10 Problem

The real Stage 10 problem is not:

- "make compose-from-source generic overnight"

It is:

- "formalize workflow-owned source adapters over durable result truth so analyzer-v2 can reason about source-backed composition across more than one workflow family without pretending the selector law is already universal"

That distinction matters.

If Stage 10 tries to solve page planning, host cutover, task-driven selector choice, and cross-workflow source normalization all at once, it will blur together:

- Stage 10 source-backed substrate work
- Stage 11 page-planning work
- Stage 13 host-contract work

That would be a stage-ordering mistake.

## Recommended Stage 10 Shape

### Decision 1: add one shared readiness schema with separate workflow-owned implementations

Stage 10 should introduce one normalized analyzer-owned readiness/inspection contract.

The implementation beneath that contract does **not** need to become a formal registry yet.

With only two workflows and very different downstream architectures, the more honest Stage 10 shape is:

- one shared response schema
- one AOI implementation
- one genealogy implementation

If a third workflow lands later, the implementation can then be promoted into a real registry without pretending the abstraction is already stable today.

What should be normalized:

- source readiness
- source families
- allowed selectors
- blocked selectors
- downstream contract kind

What should remain workflow-owned:

- how readiness is computed
- what selector families mean
- which downstream route actually consumes the decision

This avoids forcing a leaky abstraction too early.

### Decision 2: normalize outputs first, and label selector lifecycle phase explicitly

This is the key architectural restraint.

The codebase already shows that selector law is not symmetric:

- AOI source-backed compose still uses bounded `profile` selectors in `src/presenter/schemas.py`
- genealogy result/presentation composition already uses bounded `composition_mode` selectors in `src/presenter/bounded_dynamic_composition.py`

Those selectors also live at different lifecycle phases:

- AOI `profile` is a source-selection-time selector over source families
- genealogy `composition_mode` is a restore/page-runtime-time selector over already-prepared presentation payloads

Stage 10 should therefore **not** force both workflows into one premature public selector enum.

Instead it should normalize:

- adapter output shape
- readiness semantics
- trace semantics
- downstream followup semantics
- selector lifecycle phase

while still allowing workflow-owned selector unions.

### Decision 3: make genealogy the second workflow slice

The most credible bounded second workflow is genealogy.

Reason:

- genealogy already has durable corpus registration in `src/analysis_products/store.py`
- genealogy already has artifact-slot law in `src/analysis_products/store.py`
- genealogy already has bounded runtime composition modes in `src/presenter/bounded_dynamic_composition.py`
- genealogy already has result-manifest and presentation-restore support through `src/analysis_products/result_contract.py`

By contrast:

- `logical` does not yet have a baseline workflow in `src/objectives/definitions/logical.json`

So Stage 10 should stay bounded to:

- AOI
- genealogy

But the genealogy slice must be described honestly.

Genealogy is **not** already a second AOI-style source reconstruction path.

For Stage 10, the genealogy implementation should do something narrower and explicit:

- inspect durable genealogy result truth for a completed job
- evaluate which bounded genealogy `composition_mode` options are actually feasible for that job
- report allowed and blocked `composition_mode` values with blocker reasons
- return a downstream followup contract that points to the existing presenter/result restore routes

It should **not** in this stage:

- extract genealogy outputs into AOI-style transient prose sections
- invent a second transient compose-from-intent pipeline for genealogy
- pretend runtime composition modes are already the same thing as source-family reconstruction

### Decision 4: genealogy followup should point to existing page/result restore, not AOI compose-from-source

The genealogy implementation should explicitly follow up through existing analyzer-owned restore surfaces such as:

- `GET /v1/presenter/page/{job_id}?composition_mode=...`
- `GET /v1/results/by-job/{job_id}/presentation?composition_mode=...`

That keeps the stage honest.

The AOI followup can keep pointing to:

- `POST /v1/presenter/compose-from-source`

These are different downstream architectures, and Stage 10 should say that plainly.

### Decision 5: reuse the durable result/presentation substrate instead of inventing a second restore system

Stage 10 should reuse existing analyzer-owned result truth:

- `build_result_manifest(...)`
- `get_result_presentation(...)`
- `assemble_page(..., composition_mode=...)`
- `validate_requested_composition_mode(...)`

The stage should not invent another workflow-specific restore mechanism for genealogy just because AOI currently has `compose-from-source`.

The right move is:

- add a shared readiness contract with workflow-owned implementations
- let workflow-specific downstream followup point to the existing presenter/result contracts when those already exist

### Decision 6: add a source-backed inspection/readiness boundary

Stage 10 should likely add one analyzer-owned inspection contract for source-backed composition readiness.

For example:

- a presenter- or results-namespaced endpoint that accepts durable result identity plus workflow-owned selector hints and returns normalized source-backed readiness

The important part is not the exact path.

The important part is the boundary:

- hosts can inspect source-backed readiness from analyzer-owned workflow adapters
- analyzer-v2 can return normalized selector truth, blocked selectors, and followup contracts
- analyzer-v2 does not yet have to collapse AOI and genealogy into one public compose route

### Decision 7: carry the AOI/the-critic coupling explicitly instead of understating it

The current AOI source-backed consume path is still materially coupled to the-critic:

- `compose-from-source` is AOI-only
- `compose-from-source` currently hardcodes `consumer_key='the-critic'`
- host-side saved-result identity preparation still matters for the AOI launch path

Stage 10 should therefore not describe the current AOI seam as if it were already host-neutral workflow substrate.

Instead it should say:

- keep the AOI route alive as the bounded current AOI consumption path
- add normalized readiness/inspection above it
- do not claim that Stage 8/9 analyzer-native routing/planning has already replaced the live AOI host flow

That keeps the stage honest and lowers cutover risk.

### Decision 8: do not import Stage 11 or Stage 13 into Stage 10

Still blocked in this stage:

- no generalized semantic page planner
- no broad renderer-family expansion
- no universal thin-host contract
- no task-driven selector planning from open-ended user requests
- no broad objective expansion beyond AOI plus genealogy

Stage 10 is about durable source-backed substrate law.

It is not the stage where the analyzer becomes fully task-to-UI-general.

## Candidate Public Shape

Stage 10 should likely expose one new bounded contract such as:

- source-backed inspection / readiness

with a request that includes:

- `workflow_key`
- `consumer_key`
- durable result identity such as `source_v2_job_id`
- optional workflow-owned selector hint

and a decision response that includes:

- normalized workflow summary
- implementation kind
- source-truth status
- source families
- selector lifecycle phase
- allowed selectors
- blocked selectors
- downstream followup contract
- trace

The selector hint should probably stay a discriminated union.

That lets Stage 10 preserve real asymmetry such as:

- AOI `profile`
- genealogy `composition_mode`

without pretending they are already the same thing.

## Bounded Claim For Stage 10

Stage 10 should prove one bounded thing:

- analyzer-v2 can normalize durable composition readiness truth through workflow-owned implementations over more than one workflow family, using:
  - AOI source reconstruction where that substrate already exists
  - genealogy restore/runtime composition readiness where that is the honest current substrate

and can return an analyzer-owned readiness/followup decision without pretending both workflows already share one downstream architecture

That is enough to move from:

- one AOI-only source bridge

to:

- a real cross-workflow source-backed substrate

without pretending planner-driven page law already exists.

## Proof Bar

Stage 10 should not be treated as complete without evidence for all of the following:

1. one AOI case proving the new adapter substrate wraps the existing AOI bridge rather than silently replacing it
2. one genealogy case proving a second workflow can drive bounded restore/runtime followup from durable analyzer-owned result truth
3. one genealogy-specific fail-closed case where the workflow is valid but some `composition_mode` values are blocked by missing data while others remain feasible
4. saved decision artifacts and focused tests showing workflow-owned selector asymmetry remains explicit rather than hidden behind a fake shared contract

## Exit Evidence

Minimum acceptable exit evidence:

- one shared readiness schema with separate workflow-owned implementations in code
- explicit AOI implementation coverage
- explicit genealogy implementation coverage
- one analyzer-owned inspection/readiness contract
- focused regression tests
- saved proof artifacts for AOI success, genealogy success, and blocked-source failure

## What Stage 10 Should Not Claim

Stage 10 should **not** claim:

1. task-driven selector planning
2. generic page planning across workflows
3. universal host-contract cutover
4. broad objective coverage
5. semantic visual matching
6. planner-to-presentation unification as a solved general problem

Those remain later-stage work.

## Strategic Payoff

If Stage 10 lands in this bounded form, the platform position changes in an important way.

The program would then have:

- Stage 7: one real AOI source-to-composition bridge
- Stage 8: bounded task intake and workflow routing
- Stage 9: bounded route-plus-hydrate-plus-plan normalization
- Stage 10: workflow-owned source-backed substrate across more than one workflow family

That would materially strengthen the bridge between:

- analyzer-side planning/orchestration truth

and:

- durable source-backed composition truth

without forcing a fake premature unification of page planning or host law.
