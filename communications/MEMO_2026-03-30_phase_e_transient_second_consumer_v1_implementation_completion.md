# Memo: Phase E Transient Second-Consumer V1 Implementation Completion

Subtitle: The bounded second-consumer transient path is implemented and test-clean, but live proof closeout is still pending

Date: 2026-03-30
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Implements:
- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_scope.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
Relevant Prior Consumer Proof:
- `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md`
Review:
- `communications/REPORT_Claude_Phase_E_Transient_Second_Consumer_Scope_Critique_2026-03-30.md`
- `communications/REPORT_Codex_Phase_E_Transient_Second_Consumer_Scope_Audit_2026-03-30.md`

## Purpose

Record what actually landed in the bounded Phase E transient second-consumer slice.

This memo is intentionally not a full closeout memo.

The implementation is landed and verified.
The live documentary proof bar originally scoped for this slice is not yet fully closed.

So this memo records:

- what now exists in code
- what is now proved at the contract level
- what is still missing before the slice can be called documentary-closed

## Outcome

The bounded transient second-consumer implementation is now landed and test-clean.

Analyzer-v2 now accepts one second transient consumer on one bounded path:

- consumer:
  - `aoi-canary`
- path:
  - AOI `source_selection`
- route:
  - `POST /v1/presenter/compose-from-selection`

This landed without:

- new public route shapes
- new request or response schema families
- new generic consumer registry architecture
- new transient plugin infrastructure
- any widening to `compose-from-source`
- any widening to `compose-from-intent`

The main bounded claim now earned in code is:

- one real second consumer can consume one analyzer-owned transient compose path without host-local analytical reconstruction

## What Landed

### 1. Narrow analyzer-side transient consumer expansion

In `src/presenter/compose_from_intent.py`:

- the flat transient-consumer gate was replaced by a small handoff-aware allowlist
- `the-critic` keeps the current three bounded handoff kinds
- `aoi-canary` is admitted only for:
  - `source_selection`

This means:

- `compose-from-selection` now accepts `consumer_key=aoi-canary`
- `compose-from-source` still fails closed for `aoi-canary`
- `compose-from-intent` still fails closed for `aoi-canary`

That is the intended bounded expansion.

### 2. Fixture-backed transient proof mode in `aoi-canary`

In `/home/evgeny/projects/aoi-canary`:

- `src/App.tsx` now has a third mode:
  - `transient_proof`
- `src/lib/transientClient.ts` now owns:
  - one thin `compose-from-selection` client
  - one field-only normalization adapter from analyzer transient presentation into the canary’s local page shape
  - one measurable proof-surface validator
- `src/fixtures/transient-aoi-source-selection.json` now stores the pinned analyzer-owned request fixture

Important host-boundary facts:

- the canary replays a frozen analyzer-owned `ComposeFromSelectionRequest`
- it does not derive source selection locally
- it does not fetch planning snapshots
- it does not reconstruct analytical meaning from planner truth
- it normalizes analyzer-owned presentation fields mechanically into the local `PagePresentation` shell

### 3. One bounded analyzer-owned replay proof surface

The analyzer repo now contains:

- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json`

This frozen JSON ties together:

- `consumer_key = aoi-canary`
- the pinned AOI `source_selection` request truth
- the bounded second-consumer response surface
- analyzer-side renderer adaptation truth

It also records the key bounded degradation fact:

- root renderer remains `tab`
- one and only one `raw_json` leaf exists
- that leaf is:
  - `compose_intent_04_aoi_thematic_report`

### 4. Mechanical proof-surface enforcement

The bounded renderer-adaptation acceptance bar is now encoded mechanically in both repos.

Analyzer-side:

- `tests/test_aoi_canary_contract.py`

Canary-side:

- `/home/evgeny/projects/aoi-canary/src/test/transientClient.test.ts`
- `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx`

The proof does not rely on vague prose like “degradation stayed bounded.”
It asserts:

- no root `raw_json`
- at most one `raw_json` leaf
- the adapted leaf is the closeout/report view only

## Verification

Analyzer verification passed:

- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_aoi_canary_contract.py`
  - result: `35 passed, 2 warnings`
- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_representative_composition_matrix.py tests/test_aoi_canary_contract.py`
  - result: `38 passed, 2 warnings`

Canary verification passed:

- `npm --prefix /home/evgeny/projects/aoi-canary run type-check`
  - passed
- `npm --prefix /home/evgeny/projects/aoi-canary run test`
  - result: `18 passed`

So the implementation and regression surface are both clean for the bounded slice that actually landed.

## Honest Boundary

### What is now true

- transient compose is no longer structurally single-consumer-only for one bounded AOI path
- `aoi-canary` is accepted at runtime for AOI `source_selection`
- `aoi-canary` is still correctly rejected for:
  - `source_profile`
  - `direct_sections`
- the canary renders the analyzer-owned transient response through a thin field-only adapter
- the host does not need workflow-specific analytical reconstruction
- analyzer-side adaptation handles the one unsupported closeout surface via bounded `prose -> raw_json` fallback

### What is not yet true

- this is not yet a fresh live browser/network closeout for the second-consumer transient slice
- this is not yet a full documentary closeout of the original scope memo’s proof-artifact bar
- this does not prove broad consumer generality
- this does not prove non-AOI second-consumer transient support
- this does not prove arbitrary engine/pass composition

## The Proof-Record Caveat

The one remaining caveat is evidentiary rather than architectural.

The new proof JSON is honest, but it is not a fresh live browser-captured proof bundle.

It is explicitly:

- a deterministic replay surface derived from the frozen Phase E AOI `source_selection` matrix bundle plus the current analyzer-side consumer-adaptation law for `aoi-canary`

Why the stronger proof did not land in this pass:

- a direct fresh live compose probe hit an unrelated engine-definition load error before a clean second-consumer browser capture could be recorded

That blocker appears infrastructural rather than conceptual for this slice.

So the right calibrated reading is:

- the contract-level second-consumer claim is earned
- the planned live documentary closeout is still pending

## Decision

The bounded transient second-consumer implementation slice is complete in code and verification.

But the slice is not yet documentary-closed against its stronger original proof bar.

So the next honest step is not a new consumer, not a new Phase E variable, and not productization.

The next step is:

- one narrow Phase E live proof closeout over the already-landed `aoi-canary` / AOI `source_selection` path

That closeout should capture:

- one real browser/network success path
- the bounded rendered state in `aoi-canary`
- the exact request seam actually used

without reopening the implementation scope unless the unrelated engine-definition blocker forces a small bounded fix.
