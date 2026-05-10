# Memo: Round 9 / Renderer Contract Validation Scope

Date: 2026-03-21
Program: Thin Consumer Platformization

## Purpose

Define the first post-proof-ladder platform tranche after round 8.

This memo is meant to answer:

1. what the next serious platform variable is after the adaptive/declarative proof ladder
2. why renderer contract validation is the right next move
3. how to keep that move bounded and honest against the actual codebase
4. what round 9 should and should not attempt

This memo sits beneath:

- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/MEMO_2026-03-21_round8_declarative_adaptive_suite_completion.md`
- `communications/MEMO_2026-03-16_beautiful_by_default_surfaces_platform_gap.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

## Current Program Position

As of round 8, the program has already proved enough of the adaptive/composition substrate that “one more proof token” is no longer the highest-value move.

What is already closed in substance:

- thin host boundary
- shared bounded-v2 consumer contract
- reusable upstream artifact seam
- cross-workflow generic workspace path
- adaptive single-surface family selection
- adaptive suite selection
- cross-workflow adaptive behavior
- bounded declarative single-surface lift
- bounded declarative suite lift

The roadmap memo was explicit about what should happen after that:

- stop extending the proof-token ladder
- move to renderer contract validation
- then move to consumer consolidation

So round 9 should not be another workflow-specific or composition-specific proof branch.

It should be the first platform-law tranche after the proof ladder.

## Why Renderer Contract Validation Is Next

The codebase already contains most of the pieces of a renderer-contract system.

They are just not yet enforced as one coherent presenter boundary.

**Critically, the renderer schema catalog is already populated.** All 9 registered renderers have `input_data_schema` defined. 7 of 9 have substantive rejecting schemas capable of catching malformed payloads. The remaining 2 (`raw_json` and `evidence_trail`) are intentionally permissive. So round 9 is not a schema-authoring project — the schemas exist. Round 9 is about making those existing schemas enforceable on the serve path.

What already exists:

- repo-tracked renderer definitions:
  - `src/renderers/definitions/*.json`
- renderer registry:
  - `src/renderers/registry.py`
- renderer config/data validator:
  - `src/renderers/validator.py`
- bounded runtime payload enforcement for adaptive/declarative rewrites:
  - `src/presenter/bounded_dynamic_composition.py::_validate_runtime_payload()`
- catalog-level curated view/template contract checks:
  - `src/presenter/view_contract_validator.py`
- narrower renderer-behavior policy checks:
  - `src/presenter/view_behavior_validator.py`

But the live platform is still split.

### Live Seam 1: normal bridge and assembly validation is observational and incomplete

The shared presenter path already validates renderer data in two important places:

- `src/presenter/presentation_bridge.py::_validate_transform_output()`
- `src/presenter/presentation_api.py::_validate_payload_data()`

Both currently run in warn-only mode.

That means malformed renderer-facing payloads can still travel through the normal presenter path without becoming a hard contract failure.

The seam is also narrower than it first appears:

- normal bridge/assembly paths currently validate renderer **data**
- those paths specifically call `validate_renderer_data(...)`
- they do **not** yet validate renderer **config** on the same normal serve path
- there is no corresponding normal-path `validate_renderer_config(...)` call in those seams today

So round 9 is not just “flip one validation mode.”
It is:

- promote normal-path data validation into a real contract boundary
- and add the missing normal-path config-validation seam alongside it

### Live Seam 2: strict validation exists, but only inside bounded composition rewrites

`src/presenter/bounded_dynamic_composition.py::_validate_runtime_payload()` validates three distinct concerns in a single pass:

1. **consumer capability** — whether the consumer supports the renderer/sub-renderer types
2. **renderer config schema** — whether `renderer_config` matches the registry's `config_schema` via `validate_renderer_config()`
3. **renderer data schema** — whether `structured_data` matches the registry's `input_data_schema` via `validate_renderer_data()`

All three produce `CompositionIssue` objects that bubble up to the bounded composition error path.

But these are conceptually distinct enforcement surfaces, and round 9 should keep them separate:

- **Consumer capability validation** (concern 1)
  - Does the consumer support this renderer/sub-renderer at all?
  - Already strict inside bounded composition — produces hard 409 failures.
- **Renderer schema validation** (concerns 2 and 3)
  - Does this payload/config actually match the renderer contract?
  - Inside bounded composition: validated, but the underlying `validate_renderer_data()` and `validate_renderer_config()` calls use default WARN mode — issues are collected but unknown/schema-less renderers pass as `schema_available=False`.
  - On the normal presenter path: only data validation exists in `_validate_payload_data()` and `_validate_transform_output()` with explicit WARN mode, while config validation is absent entirely.

The first is already a hard boundary. The second is where round 9 work concentrates.

So the current bounded-composition law is narrower than “universal renderer-contract strictness”:

- fail-closed on consumer support
- fail-closed on config/data schema violations for renderer types that are actually registry-backed
- not yet fail-closed on “renderer contract missing from registry” as a generic condition

So round 9 is about making renderer schema validation real as a platform boundary, not about rediscovering consumer support checks.

Round 9 should ask whether that law can become a broader presenter boundary, not just an adaptive-mode special case.

#### Policy for views with unregistered renderer types

The current codebase has two active views using renderer types with no registry entry:

- `genealogy_per_work_scan -> card`
- `lines_of_attack_overview -> prose_narrative`

The current renderer validator returns `valid=True` with `schema_available=False` when a renderer has no registry entry or no schema. This means unregistered renderer types silently pass validation.

Round 9 must state a policy:

- **On the enforced proof slice**: views whose renderer type has no registry entry should be treated as **invalid** — the enforcement boundary cannot be credible if unknown renderers pass silently. This is the whole point of making schemas enforceable.
- **Outside the enforced proof slice**: the current tolerant behavior (`schema_available=False → valid=True`) remains unchanged to avoid a broad cleanup dependency.

If a desired proof route exercises views with unregistered renderer types, the only allowed resolution is bounded registry-coverage closure (adding the minimum renderer definitions needed), not exempting those views from enforcement.

#### Enforcement timing

Round 9 enforcement should happen at **serve time, per view**, not at global assembly time:

- When the shared presenter routes assemble a page, each participating `ViewPayload` is validated against its renderer contract.
- Validation happens at the point where `_validate_payload_data()` and `_validate_transform_output()` are called — the code seams already exist.
- One mechanical part of the change is switching `mode=ValidationMode.WARN` to `mode=ValidationMode.STRICT` at those two call sites.
- Additionally, renderer **config** validation must be added to the normal serve path alongside the existing data validation.
- And the route/trace exception plumbing has to preserve the current `409`/inspectable-trace discipline rather than degrading these failures into generic `500`s.

### Live Seam 3: renderer-definition loading is still tolerant

`src/renderers/registry.py` currently logs renderer-load failures and skips bad definitions rather than failing loudly.

That is acceptable for a running server cache.
It is not acceptable if renderer contracts are meant to be serious repo-tracked platform artifacts.

So “fail-loud” in round 9 should mean:

- startup/preflight/CI checks fail hard when repo-tracked renderer definitions are broken

It should not mean:

- crash a running server at arbitrary request time because one definition file was malformed

The recommended implementation:

- **CI/tests**: add a test that `RendererRegistry.load()` succeeds without errors for all repo-tracked definitions — fail the test suite if any definition is broken
- **Runtime**: keep the current tolerant loading (log and skip bad definitions) but add a health/readiness check that reports registry load status

### Live Seam 4: the broader catalog is not yet ready for a naive “strict everywhere” flip

The current repo state shows why round 9 must stay bounded.

Observed local preflight facts:

- renderer schema health currently passes for the registered renderer catalog
- all 9 registered renderers already have `input_data_schema` populated
  - 7 have substantive rejecting schemas
  - `raw_json` is intentionally permissive
  - `evidence_trail` is intentionally lightweight
- the curated view/template contract validator currently reports:
  - `23 total`
  - `16 valid`
  - `7 invalid`
  - `10 skipped`
- two active repo-wide views still use renderer types with no renderer registry definition:
  - `genealogy_per_work_scan -> card`
  - `lines_of_attack_overview -> prose_narrative`
- the current round-8 genealogy proof manifests are **not** yet registry-backed clean:
  - each still carries 8 active views whose renderer types are absent from `src/renderers/definitions/`
  - the missing renderer keys on that proof surface are:
    - `card`
    - `enabling_conditions`
    - `constraining_conditions`
    - `mini_card_list`
    - `move_repertoire`
    - `prose_block`
    - `timeline_strip`
- the current round-6 AOI proof manifests are registry-backed clean

So round 9 cannot honestly be scoped as:

- “flip the entire presenter platform to strict contract enforcement everywhere”

without turning into a broad cleanup program.

That would be the wrong move.

## Recommended Round-9 Claim

Round 9 should prove one bounded thing:

- renderer contracts can become a fail-closed presenter boundary on the shared bounded-v2 route surface for a bounded proof slice without making the consumer smarter or reopening workflow-specific UI logic

And the phrase “bounded proof slice” should be read concretely, not aspirationally:

- AOI is immediately usable because its current proof manifests are registry-backed clean
- genealogy is only admissible after an explicit bounded registry-coverage closure for the renderer keys it actually exercises

This is the platform-law equivalent of the earlier proof rounds:

- not “all renderers, all views, all history”
- but one serious bounded enforcement slice on real routes that matter

## Recommended Proof Standard

Round 9 should **not** add a new composition token.

The proof should instead reuse the strongest existing control routes, but it needs to do so honestly.

### AOI Control: Immediate Clean Proof Surface

- existing route family:
  - `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id=<id>&selected_source_thinker_name=<name>&composition_mode=adaptive_aoi_theme_report_suite_v1`
- documentary controls:
  - the two round-6 AOI suite projects/jobs
- current status:
  - registry-backed clean on the live proof manifests

### Genealogy Control: Gated Secondary Proof Surface

- existing route family:
  - `/p/:projectId/analysis/intellectual_genealogy?composition_mode=declarative_genealogy_relationship_conditions_suite_v1`
- documentary controls:
  - the two round-8 genealogy suite projects/jobs
- current status:
  - not yet registry-backed clean on the live proof manifests
  - usable only if round 9 closes a small registry-coverage gate for the renderer keys exercised by that proof surface

The proof standard should be concrete and verifiable:

**Existing control routes produce identical page presentations under strict enforcement, with zero renderer-contract issues in the trace.**

More specifically:

1. the round-6 AOI control routes return 200 with valid page presentations under strict renderer-contract enforcement on the shared presenter surface
   - trace diagnostics show zero renderer-contract violations
   - page presentation content is identical to what the same routes produce under the current warn-only mode
2. the round-8 genealogy control routes either:
   - satisfy the same three criteria (200, zero violations, identical content) after a bounded registry-coverage closure for their participating renderer keys, or
   - are explicitly documented as still blocked rather than silently counted as “already clean”

That is a better next proof than inventing:

- one more workflow token
- one more family token
- or one more declarative variant

## In Scope

Round 9 should stay constrained to:

1. renderer-definition integrity for repo-tracked renderers
2. bounded-v2 presenter-route enforcement of renderer config/data contracts on assembled `ViewPayload`s
3. inspectable failure surfacing when renderer contracts fail
4. bounded proof closure on the existing round-6 AOI control routes and, if their registry-coverage gate closes, the round-8 genealogy control routes
5. minimal or no Critic logic changes beyond whatever generic error handling is already required by the shared contract
6. bounded registry-coverage cleanup only for renderer keys that are required by an explicitly chosen proof surface

More concretely, round 9 should likely target:

### 1. Renderer Registry Law

Treat repo-tracked renderer definitions as fail-loud platform artifacts, not best-effort suggestions.

That means:

- malformed renderer definitions should fail loudly in startup/preflight/CI validation
- repo-tracked renderer definition breakage should not be silently tolerated as a healthy state
- this does **not** require crashing the server at arbitrary request time

### 2. Serve-Time Contract Enforcement

Make renderer config/data validation real on the shared presenter-serving path, not just on bounded runtime rewrites.

The enforcement seam should be the bounded-v2 serving surface:

- result manifest
- result presentation
- refresh presentation
- page
- single-view
- trace diagnostics

The key question is:

- can a composed `ViewPayload` that fails its renderer contract be rejected before it reaches the consumer

Round 9 should choose one failure policy and stay disciplined about it.

Recommended policy:

- for page/manifest/presentation/refresh routes on the enforced proof slice:
  - reject the whole response with `409` if any participating active view fails renderer contract validation
- for single-view:
  - reject that requested view with `409`
- for trace:
  - keep `200` with inspectable diagnostics

Round 9 should **not** default to:

- silently stripping invalid views from the page
- or downgrading them to `raw_json`

Those fallback behaviors may be useful later, but they would weaken the first serious platform-law proof.

### 3. Bounded Diagnostics

If contract enforcement becomes real, the failure must remain inspectable.

That means round 9 should define:

- where route-level failures surface
- what issue objects look like
- how the trace route preserves diagnostics without inventing a second opaque error dialect

There is also a concrete code seam here:

- current route-level `409` plumbing and trace invalid-state handling are wired around `BoundedCompositionValidationError`
- concretely, `src/api/routes/results.py` and `src/api/routes/presenter.py` only special-case that error shape today
- and `src/presenter/decision_trace.py::build_presentation_trace()` preserves inspectable trace state by catching that same bounded-composition error internally

So round 9 must either:

- reuse that issue/exception shape for renderer-contract failures

or:

- explicitly widen the route and trace plumbing for a new presenter-contract error type

Otherwise the failure mode regresses to route-level `500`s.

That dependency should be treated as in-scope, not left implicit.

### 4. Registry-Backed Proof Slice Only

The proof slice should be limited to routes whose participating renderer families are already registry-backed and exercised by the existing serious proof controls.

If a desired proof route is not yet registry-backed clean, the only allowed widening is:

- the minimal renderer-definition coverage needed to make that specific proof route honest

That keeps round 9 from dissolving into:

- legacy renderer cleanup
- historical catalog migration
- or a many-view backfill project

## Out Of Scope

Round 9 should not attempt:

- a global strictness flip for every active view in the repo
- a full cleanup of all curated view/template mismatches in `view_contract_validator.py`
- immediate hard-gating of the current `view_contract_validator.py` report
- fixing every legacy renderer alias or missing renderer key in the repo beyond the bounded proof surface
- new composition tokens
- new adaptive/declarative proof variants
- new consumer-specific rendering logic
- renderer redesign or visual polish work
- broad view-authoring refactors

Those may matter later, but they are not the round-9 question.

## Important Scoping Discipline

Round 9 should distinguish three different things that the repo currently blends together:

### 1. Renderer Schema Health

This is:

- whether renderer JSON definitions and their JSON Schemas are valid artifacts

This is the easiest layer and should be fail-loud.

### 2. Runtime Payload Contract Validity

This is:

- whether an assembled `ViewPayload` actually matches the renderer contract it claims to use

This is the real round-9 proof target.

### 3. Curated View/Template Contract Fidelity

This is:

- whether the authored view definition and extraction template agree structurally before runtime

The repo already has tooling for this, but the current report is not yet clean.

So round 9 should treat this as:

- valuable preflight context
- not yet the primary fail-closed boundary

That distinction matters.

If round 9 tries to solve all three layers at once, it will become a diffuse cleanup project instead of a bounded platform step.

## Recommended Failure Discipline

Round 9 should likely preserve the presenter route discipline already proved in bounded composition:

- invalid request or unsupported contract mode -> `400` when appropriate
- accepted request with renderer contract failure -> `409`
- trace remains inspectable rather than collapsing into an opaque `500`

The memo is intentionally not freezing the exact error-class names yet.
But the route/trace plumbing dependency is not optional: the implementation must either reuse `BoundedCompositionValidationError` semantics or teach the relevant routes and trace builder about the replacement.

But it should freeze two principles:

- renderer contract failures are platform-law violations, not warning-only log lines
- failure policy on the enforced proof slice is whole-response rejection with inspectable diagnostics, not silent stripping or downgrade

## What Evidence Would Make Round 9 Credible

Before broader renderer-contract claims become credible, round 9 should produce evidence at three levels:

### 1. Catalog Evidence

- renderer definitions validate cleanly
- startup/CI checks fail loudly if a repo-tracked renderer definition breaks

### 2. Automated Contract Evidence

- the shared presenter route surface fails closed on invalid renderer config/data payloads in a bounded test envelope
- normal presenter serving paths validate renderer **config** as well as renderer **data**
- the bounded route surface remains healthy on the selected proof controls
- the passing proof controls show zero renderer-contract issues in trace diagnostics

### 3. Route-Real Proof Evidence

- the round-6 AOI adaptive suite control routes return 200 with valid page presentations under strict enforcement
- the round-8 genealogy declarative suite control routes do the same only if their bounded registry-coverage gate closes
- page presentations under strict enforcement are **identical** to those produced under current warn-only mode — no content regression
- trace diagnostics show **zero** renderer-contract violations on successful proof routes
- trace/diagnostic artifacts show renderer contract enforcement is inspectable, not hidden

## Why This Fits The Big Picture

This round fits the roadmap and vision better than another proof token because it starts cashing in the proof ladder on a real platform boundary.

The big vision was never:

- “more adaptive branches forever”

It was:

- analyzer-v2 as the upstream presentation authority
- consumers staying thin
- deterministic renderer-facing shaping becoming trustworthy platform behavior

Round 9 moves directly at that missing layer.

If it lands, the next move after it should be much clearer:

- consumer consolidation around analyzer-v2-owned renderer/platform law

not:

- another bounded adaptive/declarative variant

## Bottom Line

Round 9 should be a **bounded renderer contract validation proof**, not a registry expansion and not another proof-token tranche.

It should prove that the shared presenter boundary can start enforcing renderer law on real cross-workflow control routes without turning the consumer smarter and without pretending the entire historical catalog is already clean.
