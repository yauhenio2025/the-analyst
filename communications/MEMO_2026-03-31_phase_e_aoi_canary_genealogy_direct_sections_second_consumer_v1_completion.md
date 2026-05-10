# Memo: Phase E AOI Canary Genealogy Direct-Sections Second-Consumer V1 Completion

Subtitle: One bounded non-AOI compose path is now live-proved inside the existing `aoi-canary` shell

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
Implements:
- `communications/MEMO_2026-03-31_phase_e_non_aoi_direct_sections_second_consumer_scope_recommendation.md`
Relevant Prior Completion:
- `communications/MEMO_2026-03-31_phase_e_aoi_canary_source_profile_dossier_second_consumer_v1_completion.md`
- `communications/MEMO_2026-03-31_phase_e_transient_second_consumer_live_closeout_completion.md`
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
Review Context:
- `communications/REPORT_Claude_Phase_E_Non_AOI_Direct_Sections_Second_Consumer_Scope_Recommendation_Critique_2026-03-31.md`
- `communications/REPORT_Codex_Phase_E_Non_AOI_Direct_Sections_Second_Consumer_Scope_Recommendation_Audit_2026-03-31.md`

## Purpose

Record the completion of one bounded non-AOI second-consumer compose slice on the already-live-proved second consumer:

- `aoi-canary`

The closed path is:

- workflow:
  - `intellectual_genealogy`
- handoff family:
  - `direct_sections`
- route:
  - `POST /v1/presenter/compose-from-intent`
- canary mode:
  - `transient_proof`

This slice answers one specific Phase E question:

- can the same second consumer that already live-proves the bounded AOI transient paths carry one bounded non-AOI compose path without host-local analytical reconstruction?

Documentary note:

- the roadmap documents are now expected to be read alongside this memo as the caught-up strategic record
- the detailed closeout claim here remains narrower than the roadmap horizon:
  - one AOI-branded second-consumer shell now live-proves one bounded non-AOI transient compose path

## Outcome

That bounded question is now answered in the affirmative on its intended bar.

The program now has:

- live current-consumer proof on genealogy `direct_sections`
- live second-consumer proof on bounded AOI transient paths
- and now one live-proved second-consumer non-AOI transient-proof / fixture-backed compose path on:
  - `aoi-canary`
  - genealogy `direct_sections`

This does not mean:

- broad host-neutral generality
- generic consumer architecture
- or de-AOI-ification of the `aoi-canary` shell

The honest closed claim is narrower:

- one AOI-branded second-consumer shell can carry one bounded non-AOI compose path

## What Landed

### 1. Analyzer-side `direct_sections` admission

Analyzer-v2 now admits:

- `consumer_key = aoi-canary`
- `handoff_kind = direct_sections`

through the existing `compose-from-intent` seam.

This landed as a narrow consumer-adapter broadening in:

- `src/presenter/compose_from_intent.py`

What did not change:

- request/response schemas
- workflow law
- planner/lowering route shapes
- AOI second-consumer paths already proved earlier

### 2. Canary-side bounded host broadening

`aoi-canary` now exposes a third transient proof case inside the same `transient_proof` mode:

- `genealogy_direct_sections`

What landed in the canary repo:

- one thin `composeFromIntent()` client
- one new `TransientProofFixture` arm for `direct_sections`
- one pinned `ComposeFromIntentRequest` fixture at:
  - `/home/evgeny/projects/aoi-canary/src/fixtures/transient-genealogy-direct-sections.json`
- planner-backed transient identity via:
  - `planning_decision_id`
- case-aware transient proof validation
- structural render-path generalization:
  - `tab` roots still render through `TabShell`
  - non-`tab` roots render directly through `RendererHost`

The render-path generalization stayed thin:

- no invented AOI wrapper
- no semantic reconstruction
- no planner or lowering fetches in the canary

### 3. Fresh proof artifacts

The fresh `aoi-canary` analyzer proof bundle is now authoritative for this slice:

- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_genealogy_direct_sections_2026-03-31.json`

The older current-consumer genealogy bundle remains source material only:

- `communications/PROOF_phase_e_matrix_genealogy_direct_sections_2026-03-30.json`

The canary fixture now points at the fresh `aoi-canary` analyzer proof bundle rather than the older `the-critic` bundle.

The live closeout artifact set is frozen at:

- `communications/PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.json`
- `communications/PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.har`
- `communications/PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.png`

The frozen proof bar is exact:

- `consumer_key = aoi-canary`
- `workflow_key = intellectual_genealogy`
- `planning_decision_id = planning-decision-5f5b0182f2f9`
- observed request equals the pinned fixture
- root renderer remains `card_grid`
- raw-json leaf set remains empty

### 4. Case-aware validator, not a globally looser one

The transient validator is now case-aware rather than globally relaxed.

AOI proof cases still require:

- `tab` root
- their pinned raw-json leaf sets

The new direct-sections case requires:

- `card_grid` root
- empty raw-json leaf set

So this completion did not win by weakening the entire transient proof discipline.

## Verification

Focused analyzer verification:

- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_source_backed_readiness.py tests/test_aoi_canary_contract.py tests/test_representative_composition_matrix.py`
- result:
  - `56 passed, 2 warnings`

Canary verification:

- `npm --prefix /home/evgeny/projects/aoi-canary run type-check`
  - passed
- `npm --prefix /home/evgeny/projects/aoi-canary run test -- --run`
  - `26 passed`

Live closeout summary records:

- `response_status = 200`
- `resolver_version = compose-from-intent-v2`
- `observed_request_json_equals_pinned_fixture_request = true`
- `observed_root_renderer = card_grid`
- `raw_json_leaf_keys = []`
- `forbidden_analytical_requests_observed = []`
- `allowed_non_analytical_requests` includes one recorded style-token fetch:
  - `GET http://localhost:8001/v1/styles/tokens/explanatory_narrative`
  - `status = -1`
- repo state at capture time:
  - `analyzer_v2_repo_state = DIRTY`
  - `aoi_canary_repo_state = DIRTY`

## Honest Boundary

### What is now true

- `aoi-canary` now live-proves, inside its bounded `transient_proof` / fixture-backed compose scope:
  - AOI `source_selection`
  - AOI `source_profile:dossier`
  - AOI `source_profile:comparison`
  - one bounded non-AOI `direct_sections` path
- the canary still consumes analyzer-owned transient truth through a thin field-level host layer
- the new non-AOI path is backed by:
  - focused tests
  - a fresh `aoi-canary` analyzer proof bundle
  - live browser/network closeout

### What is not yet true

- this does not prove broad host-neutral generality
- this does not prove generic consumer architecture
- this does not prove more than one non-AOI second-consumer path
- this does not prove arbitrary workflow or engine/pass generality
- this does not mean the `aoi-canary` shell is no longer AOI-branded

## Decision

This bounded Phase E slice is complete on its intended bar.

The program has now crossed one important threshold:

- the second consumer is no longer proven only on AOI-local transient surfaces

But the honest documentary claim remains bounded:

- one existing AOI-branded second-consumer shell now live-proves one bounded non-AOI transient compose path

That is stronger than AOI-only parity work, but still not the same thing as broad host-neutral platform generality.
