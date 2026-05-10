# Memo: Stage 12 / Cross-Workflow Renderer Law Generalization Scope

Subtitle: Fail-Closed Served Renderer Contract Law Over Current AOI And Genealogy Presentation Surfaces

Date: 2026-03-24
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Prior Stage Memo: `communications/MEMO_2026-03-23_stage11_rich_semantic_page_planning_scope.md`
Stage 11 Completion: `communications/MEMO_2026-03-24_stage11_rich_semantic_page_planning_completion.md`
Stage 10 Completion: `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_completion.md`
Stage 9 Completion: `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_completion.md`

## Purpose

Define the next honest stage after Stage 11 bounded semantic transient planning.

This memo is about the next missing platform seam:

- fail-closed served renderer contract law beyond one AOI proof mode
- a concrete served-policy layer beyond `composition_mode`
- recursive final contract enforcement across current presentation surfaces
- sub-renderer law where container renderers actually depend on section-level renderer contracts
- explicit child-container law for `tab`-style parent views
- cross-workflow renderer-law evidence over the workflows that already have real presentation truth
- stronger CI and preflight checks so renderer law stops being partly implicit and partly route-specific

It is not about:

- broader semantic grouping law beyond the bounded Stage 11 slice
- new renderer invention
- renderer-package or host UI work
- generic host-contract formalization
- expanding transient compose beyond the current AOI-first seam
- broad workflow coverage beyond the workflows that already have real durable presentation truth

## Why This Stage Now

The most recent stage sequence changed the downstream position materially.

Three things are now simultaneously true:

1. Stage 9 normalized route-plus-hydrate-plus-plan truth over AOI and genealogy
2. Stage 10 normalized cross-workflow source-backed readiness truth over AOI profile selection and genealogy runtime restore/composition readiness
3. Stage 11 upgraded transient compose into bounded semantic parent/child planning with recursive transient contract semantics

But the renderer-law boundary is still visibly partial.

Today the repo still shows a structural split:

- `src/presenter/compose_from_intent.py` now enforces recursive final payload contracts directly for transient compose
- `src/presenter/manifest_builder.py` only fail-closes final payload contracts when `src/presenter/renderer_contract_enforcement.py` says the current `composition_mode` is on a narrow allowlist
- `src/presenter/presentation_api.py` still performs assembly-time payload validation in warn-only mode

So Stage 11 broadened what analyzer-v2 can plan and serve transiently, but it did not make the renderer boundary universally real across the current platform surfaces.

That is why the next stage should be Stage 12 rather than Stage 13.

The minimal generic host contract should sit on top of stronger cross-workflow renderer law, not on top of a world where the final serve boundary is still partly enforced and partly advisory.

## Explicit Sequencing Note

Stages 2-6 and Stage 13 remain open in the canonical roadmap.

Pulling Stage 12 into explicit scope now is not a claim that those stages stopped mattering.

It is a claim about ordering:

- Stage 10 made result-backed readiness explicit
- Stage 11 made transient page-tree semantics explicit
- the next platform gap is still analyzer-side served renderer law
- a thin-host contract is not yet the highest-leverage move if the served renderer boundary is still only AOI-strong

So this memo is intentionally about Stage 12 first, not a premature Stage 13 host-contract jump.

## Strategic Diagnosis

The current codebase already contains substantial pieces of Stage 12.

### What is already real

Renderer metadata and validator substrate are real:

- `src/renderers/definitions/*.json` already provide `input_data_schema`, config schemas, and container metadata
- `src/renderers/validator.py` already validates renderer config and data against those schemas
- `src/presenter/renderer_contract_enforcement.py` already exposes recursive payload-tree contract enforcement helpers

Consumer support metadata is also real:

- `src/consumers/definitions/*.json` already declare `supported_renderers` and `supported_sub_renderers`
- `src/presenter/runtime_override_validator.py` already knows how to clean or reject unsupported renderer and sub-renderer overrides

Sub-renderer and container contract reasoning already exists in pieces:

- `src/presenter/view_contract_validator.py` already validates section and nested renderer assignments against extraction shape
- `src/presenter/presentation_api.py` already synthesizes container payloads from child payloads for job-backed presentation trees
- Stage 11 now synthesizes deterministic parent-tab payloads for transient trees

Cross-workflow presentation truth is also real:

- AOI and genealogy both already have durable result-manifest and presentation-restore surfaces
- genealogy and AOI both already have bounded runtime composition modes
- Stage 10 already proved that both workflows can report readiness over real result identity

So Stage 12 is not greenfield renderer work.

### What is not yet real

There is still no honest platform law that says:

- every current served presentation surface that matters is fail-closed on final renderer contract violations
- the final contract boundary is driven by a real served-policy layer rather than one narrow `composition_mode` allowlist
- section-level and nested sub-renderer law is part of the final served boundary where config-bearing container renderers depend on it
- `tab`-style parent containers have an explicitly different child-container law from accordion-style section-renderer law
- cross-workflow CI proves renderer-law strength on more than one workflow family

The repo therefore has:

- strong renderer metadata
- partial enforcement helpers
- some AOI-specific or transient-specific hardening
- no serve-time sub-renderer law yet
- genealogy normalization and warn-mode handling that show pre-existing shape-risk on job-backed surfaces

It does not yet have:

- cross-workflow served renderer law as a platform rule

## The Real Stage 12 Problem

The real Stage 12 problem is not:

- "add more renderers"
- "make the host generic"
- "turn every workflow into Stage 11 transient compose"

It is:

- "turn renderer contracts from partial AOI/transient proof machinery into fail-closed served law across the current AOI and genealogy presentation matrix"

That distinction matters.

If Stage 12 is framed too broadly, it will blur together:

- renderer-law strengthening
- Stage 13 host-contract formalization
- future workflow expansion
- future richer surface-planning work

If it is framed narrowly and honestly, it can prove something durable:

- that analyzer-v2 owns a real renderer boundary on the surfaces it already serves

## Bounded Claim For Stage 12

Stage 12 should prove one bounded thing:

- analyzer-v2 can enforce fail-closed final renderer law, including sub-renderer/container law where necessary, across the current AOI and genealogy served presentation surfaces without requiring new host work and without pretending every workflow or every renderer family is equally mature

That is enough to make Stage 12 a real platform-strengthening step rather than another AOI-only proof token.

## Recommended Stage 12 Shape

### Decision 1: keep Stage 12 analyzer-owned and served-boundary-focused

Stage 12 should be centered in analyzer-v2.

The primary surfaces are existing served presentation paths such as:

- result manifest construction
- result presentation restore
- presenter page assembly
- bounded runtime composition outputs that flow through those surfaces
- the Stage 11 transient compose path where the same renderer contract law should remain coherent

This stage should not require:

- new host routes
- new renderer packages
- generic app-shell changes

### Decision 2: replace composition-mode-only strictness with an explicit served-contract policy

The current enforcement selector is too thin:

- `is_renderer_contract_enforced_mode(composition_mode)`

That is no longer enough after Stage 10 and Stage 11.

Stage 12 should introduce a richer served-contract context or policy, driven by facts such as:

- workflow key
- consumer key
- route kind or serve path kind
- composition mode when present
- transient vs job-backed presentation

The policy should be concrete enough that two separate implementation passes would produce the same decisions.

The expected shape should be something close to:

- `resolve_served_renderer_contract_policy(*, workflow_key, consumer_key, route_kind, composition_mode, is_transient) -> ServedRendererContractPolicy`

Where `ServedRendererContractPolicy` carries at least:

- `mode: strict | shadow | warn`
- `coverage_key`
- `reason`

The initial Stage 12 decision matrix should be explicit:

- transient compose route kinds -> `strict`
- current AOI runtime/adaptive served surfaces already under bounded contract proof -> `strict`
- genealogy runtime composition modes -> `shadow` first, then promote specific modes to `strict` only when focused evidence shows they are clean
- default authored or restore surfaces that are still historically normalization-heavy -> `warn` unless explicitly promoted

The point is not to make enforcement infinitely dynamic.

The point is to stop pretending one AOI composition mode is the only place where final renderer law matters while still keeping the first Stage 12 cutover honest.

### Decision 3: make genealogy cutover explicit rather than pretending warn-only surfaces are already strict-ready

This is the highest-risk workflow in Stage 12.

`src/presenter/presentation_api.py` already contains substantial genealogy-specific normalization and repair logic, which is evidence that genealogy payloads have historically needed shape cleanup before serving.

So Stage 12 should not imply:

- "turn every genealogy served surface strict all at once"

The stage should instead carry an explicit cutover strategy:

1. introduce the served-policy layer for all relevant AOI and genealogy serve paths
2. run genealogy surfaces in `shadow` mode where needed so violations are visible in tests and proof without silently pretending they are already clean
3. fix or narrow the genealogy mode set until at least one real non-AOI surface can be promoted to `strict`
4. only then widen strict coverage mode by mode

That keeps Stage 12 honest:

- renderer-law strengthening is real
- genealogy breakage risk is acknowledged
- pre-existing warn-only behavior is not hand-waved away

### Decision 4: make final enforcement recursive and shared across transient and job-backed paths

Stage 11 already made transient compose recursive in:

- consumer adaptation
- served-payload normalization
- final contract validation
- hashing and count semantics

Stage 12 should extend that same seriousness to job-backed served paths.

That means:

- final payload trees should be validated recursively, not only top-level
- manifest/result/page assembly should fail closed where the served-contract policy says `strict` applies
- manifest/result/page assembly should record policy and violations when `shadow` applies
- the job-backed path should stop relying on warn-only assembly validation as the effective final boundary

Stage 12 should also stay explicit that job-backed renderer law is still not fully symmetric with Stage 11 transient semantics today.

This slice is the first bounded generalization pass over that partial substrate, not a claim that every manifest/content/hash/container seam is already fully universal.

### Decision 5: make serve-time sub-renderer law a new final-boundary build, not a wiring exercise

This is the most important architectural correction inside Stage 12.

Serve-time sub-renderer law does not really exist today.

What exists today are design-time and input-time helpers:

- authored view-contract validation
- runtime override cleaning

Stage 12 should treat final served sub-renderer law as a new build that reuses those helpers as templates, not as a nearly-finished boundary that only needs a switch flipped.

For config-bearing container renderers such as accordion or nested-sections-style payloads, final served law should include:

- referenced section renderer exists
- referenced section renderer is valid for the parent container
- referenced section renderer or nested renderer is supported by the consumer
- renderer config or sub-renderer config patch satisfies the relevant schema
- recursively nested section-renderer maps fail closed rather than only being cleaned opportunistically

This stage should reuse existing validator substrate where possible:

- `src/presenter/runtime_override_validator.py`
- `src/presenter/view_contract_validator.py`
- renderer and consumer registries

It should not invent a second disconnected sub-renderer validation system.

### Decision 6: keep `tab` child-container law separate from accordion-style section-renderer law

`tab` is not structurally the same thing as `accordion`.

`src/renderers/definitions/tab.json` currently declares:

- `available_section_renderers: []`

So Stage 12 should not pretend that tab parents participate in the same section-renderer contract model as accordion.

The honest rule is:

- accordion and nested-sections-style containers need serve-time section/sub-renderer law
- Stage 11-style `tab` parents need serve-time child-container law over:
  - synthetic container `structured_data`
  - child payload legality
  - payload-tree integrity

Those are related, but they are not one validation model.

### Decision 7: keep the workflow matrix honest and bounded to AOI plus genealogy

The stage name in the roadmap is broad.

The first honest implementation slice should still stay bounded to workflows that already have real result/presentation truth:

- AOI
- genealogy

That is enough to satisfy the roadmap exit criterion in an honest first step:

- multiple workflows with fail-closed served renderer law

It is not enough to claim universal platform coverage across every workflow family.

### Decision 8: do not reopen Stage 11 grouping law or invent new surface families here

Stage 12 should validate and harden the surfaces that already exist.

It should not turn into:

- broader semantic matcher work
- new hierarchy depth
- new planning families
- renderer-package expansion

Those are different problems.

### Decision 9: add stronger preflight and CI checks, not just route-time failures

The roadmap is right that route-time enforcement alone is not enough.

Stage 12 should also add:

- cross-workflow contract tests over live served outputs
- checks that consumer support declarations and final adapted renderer choices stay aligned
- checks that container and sub-renderer contracts are valid for the surfaces actually emitted
- schema-health and contract-matrix checks in focused CI

The goal is:

- fail earlier in tests and audits
- not only at runtime after a user requests a page

### Decision 10: keep public route shape stable unless diagnostics force a narrow addition

This stage is primarily contract hardening, not API redesign.

Prefer:

- existing results and presenter routes
- stronger internal enforcement
- stronger trace or error detail if needed

Do not make Stage 12 depend on a new public platform endpoint unless implementation proves that one narrow diagnostic route is necessary.

### Decision 11: proof bar must be live, cross-workflow, and include a non-AOI fail-closed case

Saved JSON alone is not enough if it only shows happy-path surfaces.

The proof bar should require at least:

1. one AOI served surface that passes final recursive renderer law under the new policy
2. one genealogy or other non-AOI served surface that now passes final recursive renderer law under the new policy
3. one real fail-closed case from a previously warn-only non-AOI surface where a renderer or sub-renderer mismatch is now blocked at the final served boundary
4. focused CI evidence that the enforcement matrix is no longer one-AOI-mode-deep
5. if some genealogy surfaces remain in `shadow`, explicit proof of that policy state rather than pretending universal strict cutover

## What Stage 12 Should Not Claim

Stage 12 should not claim that analyzer-v2 now has:

- fully universal renderer law across every workflow
- a solved minimal generic host contract
- broad semantic planner generalization
- generic transient compose across workflows
- complete removal of all AOI-specific presentation assumptions

The honest claim is narrower:

- the current served renderer boundary is stronger, recursive, cross-workflow, and fail-closed where the program has actually promoted surfaces to `strict`, with explicit `shadow` or `warn` cutover states where it has not

## Expected Outcome

If Stage 12 lands in this bounded form, the platform position becomes much cleaner:

- Stage 9 owns planning truth
- Stage 10 owns readiness truth
- Stage 11 owns bounded semantic transient tree planning
- Stage 12 would make the renderer boundary real across the current served surfaces

That is the right position to reach before trying to formalize the minimal generic host contract in Stage 13.
