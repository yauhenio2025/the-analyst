# Memo: Recommended Next Broader Phase E Question After AOI Comparison Closeout

Subtitle: A bounded recommendation to test one non-AOI compose path inside the existing `aoi-canary` shell via genealogy `direct_sections`

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
Most Recent Completed Scope:
- `communications/MEMO_2026-03-31_phase_e_aoi_canary_source_profile_comparison_second_consumer_scope.md`
Relevant Prior Completions:
- `communications/MEMO_2026-03-31_phase_e_aoi_canary_source_profile_dossier_second_consumer_v1_completion.md`
- `communications/MEMO_2026-03-31_phase_e_transient_second_consumer_live_closeout_completion.md`
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
Relevant Proof Artifacts:
- `communications/PROOF_phase_e_matrix_genealogy_direct_sections_2026-03-30.json`
- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_live_closeout_2026-03-31.json`
- `communications/PROOF_phase_e_aoi_canary_source_profile_dossier_live_closeout_2026-03-31.json`
- `communications/PROOF_phase_e_aoi_canary_source_profile_comparison_live_closeout_2026-03-31.json`

## Status Note

This memo is a recommendation memo, not yet a roadmap-ratified next step.

The currently written roadmap documents still stop at:

- `aoi-canary`
- AOI `source_profile:comparison`

as the next bounded Phase E slice.

That slice is now complete in code and proof artifacts, but the roadmap documents have not yet been updated to name the post-comparison step.

So this memo does one thing only:

- recommend the next broader bounded Phase E question explicitly, with current codebase anchors and stop conditions

It should be reviewed before being treated as the new official roadmap step.

## Purpose

Define the smallest honest Phase E question that is broader than the now-closed AOI-local preset work, without jumping to:

- a third consumer
- generic consumer architecture
- or a broad host-neutral productization tranche

The recommended next question is:

- can the same already-live-proved second consumer, `aoi-canary`, serve one bounded non-AOI transient path through the existing analyzer-owned `direct_sections` substrate without host-local analytical reconstruction?

The recommended proof target is:

- consumer:
  - `aoi-canary`
- workflow:
  - `intellectual_genealogy`
- analyzer-owned handoff family:
  - `direct_sections`
- public compose route:
  - `POST /v1/presenter/compose-from-intent`

This is broader than the finished AOI work because the varied variable is no longer:

- AOI source-profile preset choice

It is now:

- non-AOI workflow / handoff-family compatibility on the same second consumer

The claim this would support must stay narrow:

- bounded non-AOI compose compatibility inside the existing `aoi-canary` shell

not:

- broad host-neutral generality
- or proof that the current second consumer is no longer AOI-branded in its shell assumptions

## Current Code-Backed Boundary

### What is already true

Analyzer-v2 now has:

- live current-consumer coverage on:
  - AOI `source_profile`
  - AOI `source_selection`
  - genealogy `direct_sections`
- second-consumer live proof on `aoi-canary` for:
  - AOI `source_selection`
  - AOI `source_profile:dossier`
  - AOI `source_profile:comparison`

The representative composition matrix already proves that the live analyzer-owned compose substrate includes:

- AOI `source_profile` via `compose-from-source`
- AOI `source_selection` via `compose-from-selection`
- genealogy `direct_sections` via planner-backed lowering into `compose-from-intent`

The existing bounded genealogy proof surface already gives the needed analyzer-owned truth:

- `communications/PROOF_phase_e_matrix_genealogy_direct_sections_2026-03-30.json`

That bundle already pins:

- `source_v2_job_id = proof-round4-adaptive-balance-final-1774012011`
- `planning_decision_id = planning-decision-5f5b0182f2f9`
- `lowering_response_json == request_json`
- current-consumer `compose-from-intent` response truth

But that lineage is still explicitly current-consumer lineage:

- `consumer_key = the-critic`

So it is usable as analyzer-owned substrate truth and fixture source material, but not as the final proof artifact for `aoi-canary`.
The second-consumer slice would still need one fresh consumer-specific proof bundle and one fresh live closeout on:

- `consumer_key = aoi-canary`

The returned direct-sections page shape on that current proof is importantly different from the AOI canary proofs:

- root renderer is `card_grid`
- raw-json leaf set is empty

That means the next broader question is not only analyzer admission.
It also tests whether the second consumer’s transient shell can accept one non-AOI returned page shape honestly, without turning into a semantic reconstruction layer.

### What is still missing

The current explicit gaps are:

- `src/presenter/compose_from_intent.py`
  - workflow-level compatibility already supports `direct_sections` on `intellectual_genealogy`
  - the remaining analyzer gap is consumer-adapter admission:
    - `aoi-canary` still fails closed on `direct_sections`
- `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts`
  - there is no thin `composeFromIntent()` client yet
  - `validateTransientProofSurface(...)` currently hard-fails any non-`tab` root
- `/home/evgeny/projects/aoi-canary/src/App.tsx`
  - transient proof cases are still AOI-only
  - transient request dispatch is still only:
    - `source_selection`
    - or `source_profile`
  - transient fixture identity assumes either:
    - `planning_decision_id`
    - or `source_v2_job_id:profile`
  - root rendering hard-fails any non-`tab` root
- `/home/evgeny/projects/aoi-canary/src/fixtures/`
  - there is no pinned `ComposeFromIntentRequest` fixture for genealogy `direct_sections`

### Why this is the smallest honest broader variable

This is the smallest honest broader Phase E question because:

1. it keeps the same second consumer fixed:
   - `aoi-canary`
2. it keeps the same analyzer-owned response contract fixed:
   - `ComposeFromIntentResponse`
3. it reuses an already-proved analyzer-owned non-AOI transient path instead of inventing a new one
4. it does not require source-backed readiness work, because `direct_sections` is not a `compose-from-source` followup seam
5. it broadens beyond AOI-local preset work without prematurely widening to:
   - a third consumer
   - generic consumer registration
   - planner integration in the canary
   - or non-bounded host-neutral product work

## Recommended Strategic Decision

Keep the second consumer fixed and broaden only one variable:

- from AOI-only transient proof on `aoi-canary`
- to one bounded non-AOI transient proof on the same consumer

The recommended exact target is:

- `aoi-canary`
- genealogy `direct_sections`
- fixture-backed final `ComposeFromIntentRequest`
- one live browser/network closeout on `POST /v1/presenter/compose-from-intent`

The honest success claim for that target is:

- one AOI-branded second-consumer shell can carry one bounded non-AOI compose path without host-local analytical reconstruction

not:

- broad consumer neutrality
- or broad host-neutral non-AOI generality

Do not broaden further in the same slice to:

- a third consumer
- generic consumer architecture
- non-fixture planner integration in the canary
- or more than one non-AOI workflow

## Proposed Scope

### 1. Analyzer-side admission

Broaden the transient consumer gate so `consumer_key=aoi-canary` admits:

- `handoff_kind = direct_sections`

Keep everything else unchanged and fail-closed where already out of scope.

This is a bounded analyzer change because:

- the current route already exists
- the request schema already exists
- the current workflow-level gate already exercises this handoff kind on:
  - `intellectual_genealogy`
- the second consumer already exercises the returned response family on AOI surfaces

So the analyzer-side code change should stay narrow:

- one consumer-adapter broadening at the existing registration seam

not:

- a workflow-law redesign
- or a new capability architecture

### 2. Canary-side bounded host broadening

Add one new transient proof case inside the existing `transient_proof` mode:

- `genealogy_direct_sections`

Do not add:

- a new top-level app mode
- planner fetches
- planning-decision fetches
- source catalog discovery
- or host-local derivation of compose requests

Instead:

- add one pinned `ComposeFromIntentRequest` fixture copied from analyzer-owned lowering truth
- add one thin `composeFromIntent()` client
- extend the `TransientProofFixture` discriminated union with one explicit direct-sections arm
- extend transient dispatch with one explicit third branch that calls `composeFromIntent()`
- generalize proof labels, status copy, and strategy copy so they are case-aware instead of AOI-only

The canary host broadening should remain thin:

- it must stop assuming the root renderer is always `tab`
- it may render:
  - `tab` roots through `TabShell`
  - non-`tab` roots directly through `RendererHost`
- it must not reconstruct page semantics locally
- it must not wrap non-AOI output in an invented AOI semantic shell

The current blockers here are not hypothetical.
They are already hard-coded:

- `validateTransientProofSurface(...)` rejects any non-`tab` root
- `App.tsx` renders an error state for any non-`tab` root

### 3. Proof input and lineage truth

The proof input should stay fixture-backed on the canary side.

The recommended default proof lineage is the existing bounded genealogy bundle:

- `source_v2_job_id = proof-round4-adaptive-balance-final-1774012011`
- `planning_decision_id = planning-decision-5f5b0182f2f9`

The canary fixture should contain:

- the final `ComposeFromIntentRequest`
- the pinned `planning_decision_id`
- display metadata needed by the current shell
- a pointer to the analyzer proof bundle identity

The canary should not fetch:

- the planning decision
- the lowering route
- or the saved result

It should replay only the final pinned request fixture.

Analyzer-owned lineage truth should remain documented in the proof note and linked bundle, not re-derived in the host.

For transient identity, the direct-sections case should follow the same pattern as the existing planner-backed `source_selection` case:

- use `planning_decision_id`

not:

- `source_v2_job_id:profile`

### 4. Exact proof bar

The bounded proof bar should be mechanical.

Expected proof conditions:

- observed live request equals the pinned `ComposeFromIntentRequest` fixture
- `consumer_key = aoi-canary`
- `workflow_key = intellectual_genealogy`
- no forbidden analytical upstream calls appear in the browser session
- allowed non-analytical support traffic is disclosed honestly
- returned root renderer remains the analyzer truth:
  - `card_grid`
- raw-json leaf set remains the analyzer truth:
  - empty

That last pair matters because it prevents a fake “success” that only works by:

- wrapping the returned page in a host-invented `tab` shell
- or tolerating broader renderer degradation than the current analyzer truth requires

### 5. Boundaries and stop conditions

This recommendation is intentionally bounded.

If implementation starts requiring:

- broad canary shell redesign
- host-side semantic remapping of non-AOI content
- planner integration in the canary
- multiple non-AOI workflows in one slice
- or a generic consumer/plugin architecture

then the right outcome is:

- stop
- write down the blocker honestly
- and rescope

## Public Interfaces

No new API routes or schema families should be added.

Expected unchanged public surfaces:

- `POST /v1/presenter/compose-from-intent`
- `ComposeFromIntentRequest`
- `ComposeFromIntentResponse`
- `GET /v1/orchestrator/planning-decisions/{id}/compose-from-intent-request`

Behavioral broadening only:

- `POST /v1/presenter/compose-from-intent` should accept `consumer_key=aoi-canary` on the bounded `direct_sections` path

## Test / Proof Expectations

### Analyzer regressions

The next scope should require tests that prove:

- `aoi-canary` succeeds on `direct_sections`
- `aoi-canary` still succeeds on:
  - `source_selection`
  - `source_profile:dossier`
  - `source_profile:comparison`
- unsupported combinations still fail closed by test:
  - non-AOI widening beyond the chosen path
  - any broader consumer admission not explicitly added

### Canary regressions

The next scope should require tests that prove:

- one new `genealogy_direct_sections` proof case is selectable
- default proof case remains `source_selection`
- the direct-sections fixture is replayed verbatim
- transient identity for the direct-sections case uses `planning_decision_id`
- transient dispatch uses an explicit `composeFromIntent()` branch
- root rendering can accept the analyzer-truth non-tab root without semantic reconstruction
- root renderer remains `card_grid`
- raw-json leaf set remains empty
- earlier AOI proof cases remain intact

### Live proof

Acceptance should require:

- one real browser session reaches ready state on the bounded direct-sections path
- observed wire request equals the pinned fixture
- no forbidden analytical upstream calls appear in the captured proof window
- a proof note, JSON summary, screenshot, and HAR are frozen under `communications/`

## Why this is a recommendation, not yet a roadmap fact

This recommendation follows from the now-closed AOI comparison slice.

But it is not yet written into the roadmap documents.

The roadmap documents still need catch-up updates that record:

- AOI `source_profile:comparison` is complete
- AOI-local preset work on the second consumer is now closed

Only after those updates should the program treat one non-AOI second-consumer scope as the official next bounded Phase E question.

## Decision

The recommended next broader Phase E question is:

- can `aoi-canary` carry one bounded non-AOI transient proof on genealogy `direct_sections` through the existing `compose-from-intent` seam, using a pinned analyzer-owned final request fixture and without host-local analytical reconstruction?

That is the smallest honest broader variable after AOI `source_profile:comparison` closes.

It is broader than more AOI-local preset work.
It is narrower than generic consumer architecture.
And it is explicit enough to audit before it becomes the official next roadmap step.

The honest claim after completion would still be:

- one bounded non-AOI compose path works inside the existing `aoi-canary` shell

not:

- broad host-neutral generality
- or full de-AOI-ification of the second consumer host
