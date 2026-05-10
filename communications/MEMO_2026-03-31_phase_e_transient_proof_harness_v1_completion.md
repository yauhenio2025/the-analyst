# Memo: Phase E Transient Proof Harness V1 Completion

Subtitle: One proof-only transient consumer contract plus one standalone minimal harness is now live-proved

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
- `communications/MEMO_2026-03-31_phase_e_host_neutral_transient_harness_scope.md`
Relevant Prior Completion:
- `communications/MEMO_2026-03-31_phase_e_aoi_canary_genealogy_direct_sections_second_consumer_v1_completion.md`
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
- `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`
Review Context:
- `communications/REPORT_Claude_Phase_E_Proof_Only_Transient_Consumer_And_Minimal_Harness_Scope_Critique_2026-03-31.md`
- `communications/REPORT_Codex_Phase_E_Proof_Only_Transient_Consumer_And_Minimal_Harness_Scope_Audit_2026-03-31.md`

## Purpose

Record completion of the bounded Phase E slice that moved transient proof beyond both existing app shells by adding:

- one proof-only consumer contract:
  - `consumer_key = transient-proof-harness`
- one standalone minimal harness repo:
  - `/home/evgeny/projects/transient-proof-harness`
- two exact proof cases:
  - AOI `source_selection`
  - genealogy `direct_sections`

This slice answered one specific Phase E question:

- can the already-proved transient substrate be consumed outside both `the-critic` and `aoi-canary`, through one new proof-only consumer identity and one separate fixture-backed harness, without host-local analytical reconstruction?

## Outcome

That bounded question is now answered in the affirmative on its intended bar.

The program now has live-proof on the same transient substrate across:

- the current consumer surface
- the AOI-branded second-consumer surface
- and now one separate proof-only consumer plus standalone harness surface

The honest closed claim is still narrow:

- one proof-only transient consumer contract plus one minimal standalone harness can consume one AOI transient path and one non-AOI transient path over analyzer-owned truth

This does not mean:

- broad analyzer-side generality
- generic consumer architecture
- broad host-neutral productization
- or that consumer identity no longer matters in general

## What Landed

### 1. One bounded proof-only consumer contract

Analyzer-v2 now defines a new proof-only consumer:

- `src/consumers/definitions/transient-proof-harness.json`

Transient admission is also wired explicitly in the presenter seam, not only in consumer JSON:

- `src/presenter/compose_from_intent.py`

That admission is intentionally bounded:

- admitted:
  - `source_selection`
  - `direct_sections`
- fail-closed:
  - `source_profile`

The analyzer-side negative readiness story also stayed honest:

- `source_backed_readiness` was not broadened
- `consumer_key = transient-proof-harness` remains blocked on AOI `source_profile`

### 2. One standalone minimal harness repo

The new harness is:

- `/home/evgeny/projects/transient-proof-harness`

It is:

- proof-only
- fixture-backed
- structurally thin
- separate from both:
  - `/home/evgeny/projects/aoi-canary`
  - `/home/evgeny/projects/the-critic`

It reimplements only the minimum local proof surface:

- transient compose client
- field-level response normalization
- case-aware surface validation
- `RendererHost`
- `TabShell`

It does not:

- import from `aoi-canary`
- depend on `aoi-canary`
- fetch planning decisions
- fetch lowering routes
- discover results
- derive requests locally
- reconstruct workflow semantics locally

### 3. Fresh consumer-specific proof lineage

Fresh analyzer proof bundles were generated from real analyzer behavior under the new consumer identity:

- `communications/PROOF_phase_e_transient_proof_harness_source_selection_2026-03-31.json`
- `communications/PROOF_phase_e_transient_proof_harness_genealogy_direct_sections_2026-03-31.json`

These are authoritative for the harness slice.

The harness runtime does not load full analyzer proof bundles at runtime.
It uses minimal extracted fixture/proof metadata instead:

- `/home/evgeny/projects/transient-proof-harness/src/fixtures/transient-source-selection.json`
- `/home/evgeny/projects/transient-proof-harness/src/fixtures/transient-genealogy-direct-sections.json`

That keeps the runtime boundary honest while still making frozen analyzer-owned proof metadata the single source of truth for:

- expected root renderer
- expected raw-json leaf set
- pinned request identity

### 4. Two live closeouts

The source-selection live closeout is frozen at:

- `communications/PROOF_phase_e_transient_proof_harness_source_selection_live_closeout_2026-03-31.json`
- `communications/PROOF_phase_e_transient_proof_harness_source_selection_live_closeout_2026-03-31.har`
- `communications/PROOF_phase_e_transient_proof_harness_source_selection_live_closeout_2026-03-31.png`

The direct-sections live closeout is frozen at:

- `communications/PROOF_phase_e_transient_proof_harness_genealogy_direct_sections_live_closeout_2026-03-31.json`
- `communications/PROOF_phase_e_transient_proof_harness_genealogy_direct_sections_live_closeout_2026-03-31.har`
- `communications/PROOF_phase_e_transient_proof_harness_genealogy_direct_sections_live_closeout_2026-03-31.png`

The frozen live bar is exact.

For AOI `source_selection`:

- `consumer_key = transient-proof-harness`
- `workflow_key = anxiety_of_influence_thematic_single_thinker`
- `response_status = 200`
- `resolver_version = compose-from-selection-v1`
- `response.presentation.consumer_key = transient-proof-harness`
- observed request equals the pinned fixture
- root renderer remains `tab`
- raw-json leaf set remains `["compose_intent_04_aoi_thematic_report"]`
- forbidden analytical upstream requests remain empty

For genealogy `direct_sections`:

- `consumer_key = transient-proof-harness`
- `workflow_key = intellectual_genealogy`
- `response_status = 200`
- `resolver_version = compose-from-intent-v2`
- `response.presentation.consumer_key = transient-proof-harness`
- observed request equals the pinned fixture
- root renderer remains `card_grid`
- raw-json leaf set remains `[]`
- forbidden analytical upstream requests remain empty

## Verification

Analyzer verification:

- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_source_backed_readiness.py tests/test_transient_proof_harness_contract.py tests/test_representative_composition_matrix.py`
- result:
  - `58 passed, 2 warnings`

Harness verification:

- `npm --prefix /home/evgeny/projects/transient-proof-harness run type-check`
  - passed
- `npm --prefix /home/evgeny/projects/transient-proof-harness run test -- --run`
  - `7 passed`

## Worktree Notes

At live-capture time:

- `analyzer_v2_repo_state = dirty`
- `transient_proof_harness_repo_state = dirty`
- `transient_proof_harness_commit_sha = c11fa0f0297d0c62135fbbbaf45bc325d4ceb8ff`

Documentary note:

- the harness repo is a real git worktree, not a non-git scratch directory
- the current local `analyzer-v2` worktree still shows the newly added analyzer-side files and proof artifacts as untracked in `git status`

This memo records proof closure, not git-index cleanliness.

## Honest Boundary

### What is now true

- analyzer-v2 now serves one additional proof-only consumer identity on:
  - AOI `source_selection`
  - genealogy `direct_sections`
- a separate standalone harness can consume those paths without dependency on `aoi-canary`
- the harness remains fixture-backed and structurally thin
- both proof cases are now backed by:
  - fresh analyzer proof bundles
  - focused analyzer tests
  - focused harness tests
  - live browser/network closeouts

### What is not yet true

- this does not prove broad generic consumer registration
- this does not prove source-profile generality on the new harness
- this does not prove lifecycle law on the new harness
- this does not prove a reusable host runtime package
- this does not prove that consumer identity is now irrelevant in general

## Decision

This bounded Phase E slice is complete on its intended bar.

The program has now crossed a stronger threshold than the earlier `aoi-canary`-only second-consumer line:

- the already-proved transient substrate is no longer evidenced only inside the current-consumer shell and the AOI-branded second-consumer shell

But the honest documentary claim remains bounded:

- one proof-only transient consumer contract plus one standalone minimal harness can carry one AOI transient path and one non-AOI transient path over analyzer-owned truth

The next honest Phase E question is therefore no longer harness boundary.
It is bounded consumer-identity plurality at the analyzer admission layer, before any broader lifecycle widening.
