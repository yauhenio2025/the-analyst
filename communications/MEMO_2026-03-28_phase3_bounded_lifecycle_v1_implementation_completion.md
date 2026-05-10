# Memo: Phase 3 Bounded Lifecycle V1 Implementation Completion

Date: 2026-03-28
Status: Phase 3 implementation landed and focused verification passed; live proof closeout still required before Phase 3 can close honestly
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Scope Memo: `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_scope.md`
Depends on:
- `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`
- `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_completion.md`
- `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
- `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md`

## Summary

The bounded Phase 3 lifecycle slice is now implemented in code.

What is now true:

- analyzer-v2 now has one explicit analyzer-owned lifecycle object for transient compose outputs:
  - persisted `compose_session` records keyed by analyzer-generated `session_id`
- analyzer-v2 now exposes explicit presenter save/fetch routes for that lifecycle object:
  - `POST /v1/presenter/compose-sessions`
  - `GET /v1/presenter/compose-sessions/{session_id}`
- Host Contract v2 now exposes lifecycle save/fetch as delivery/runtime law rather than planner-advisory law
- the existing genealogy transient proof page can now:
  - compose
  - explicitly save the transient surface
  - reopen by `?session_id=...`
  - render the saved session truth without recomputing planning or composition in code

What is not yet claimed:

- no live Phase 3 proof artifact has been recorded yet for:
  - compose
  - save
  - reopen by `session_id`
- Phase 3 is therefore not yet documentary-closed
- Phase 4 governance/evaluation is not yet the honest main line

The next honest step is still inside Phase 3:

- one bounded live proof closeout for `compose -> save -> reopen by session_id`

## What landed

### 1. Analyzer-owned compose session persistence now exists

Analyzer-v2 now persists explicit transient compose lifecycle objects in file-backed JSON storage under the presenter layer.

Bounded v1 law now implemented:

- analyzer generates `session_id`
- save is explicit and synchronous
- every save creates a new session
- saved lifecycle truth is analyzer-owned, not browser-owned
- `planning_decision_id` remains provenance only, not lifecycle identity

The canonical saved payload is:

- full `ComposeFromIntentRequest`
- full `ComposeFromIntentResponse`

The duplicated fidelity fields are now derived server-side from `compose_response.presentation`:

- `presentation_hash`
- `presentation_content_hash`
- `resolver_version`

Primary files:

- `/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_session_store.py`

### 2. Presenter save/fetch routes now exist

Analyzer-v2 now exposes the lifecycle object through the presenter namespace rather than the orchestrator namespace.

What these routes enforce:

- request/response `workflow_key` must match on save
- request/response `consumer_key` must match on save
- fidelity fields must be present in the saved response presentation
- `consumer_key` mismatch on reopen fails closed with `409`
- missing `session_id` fails with `404`

Primary file:

- `/home/evgeny/projects/analyzer-v2/src/api/routes/presenter.py`

### 3. Host Contract v2 now carries lifecycle save/fetch as delivery/runtime law

The lifecycle slice did not reopen planner runtime ownership.

What landed:

- Host Contract v2 now includes:
  - `transient_compose_session_save`
  - `transient_compose_session_fetch`
- `session_id` now exists as host-contract identity
- the new lifecycle families sit on the existing:
  - `genealogy_result_backed_workspace_experience`
- lifecycle helpers live in `composeFromIntentClient`, not `taskLaunchRuntime`

This keeps lifecycle with compose delivery/runtime law rather than planner-advisory law.

Primary files:

- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts`
- `/home/evgeny/projects/the-critic/webapp/src/types/transientCompose.ts`

### 4. The existing genealogy proof page now supports save/reopen by `session_id`

The lifecycle proof surface remains the existing non-AOI proof page:

- `/p/:projectId/proof/transient/genealogy-saved-result`

What the page now does:

- compose mode still runs the Phase 2 chain
- after compose, the user can explicitly save the transient session
- save returns analyzer-generated `session_id`
- the page rewrites itself to `?session_id=<id>`
- reopen mode clears prior planning/compose state
- reopen mode fetches only the saved session
- reopen mode renders the saved `compose_response`
- invalid `session_id` fails closed and does not fall back to recomputation or hidden in-page state

Primary file:

- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx`

## Verification

Analyzer verification passed:

- `PYTHONPATH=. pytest -q tests/test_compose_sessions.py tests/test_phase1c_genealogy_direct_sections.py tests/test_task_planner.py -k "compose_session or planning_decision or direct_sections"`

Result:

- `12 passed, 17 deselected, 2 warnings`

Host/runtime verification passed:

- `CI=true npm test -- --runInBand --watchAll=false src/lib/hostContractRuntime.test.ts src/lib/composeFromIntentClient.test.ts src/pages/GenealogyTransientProofPage.test.tsx src/lib/taskLaunchRuntime.test.ts`

Result:

- `23 passed`

Verification notes:

- no blocking discrepancies were found in the follow-up code audit
- one minor UI label residual remains:
  - the proof page header still says `Phase 2 Proof`
- no live browser proof was run in this implementation slice

## Boundary after implementation

What is now true:

- the generalized transient substrate now has one explicit lifecycle object:
  - `compose_session`
- save/reopen law is now implemented on top of the generic non-AOI transient substrate rather than the AOI proxy stack
- lifecycle identity is now separate from planning identity:
  - `session_id` for lifecycle
  - `planning_decision_id` for planning provenance
- reopen-by-`session_id` is now implemented to serve saved presentation truth without recomputation in code

What is not yet true:

- no live proof artifact yet shows:
  - compose success
  - save success
  - deep-link/reload reopen success
  - invalid-session negative case
- Phase 3 cannot yet be marked honestly closed on documentary evidence
- Phase 4 governance/evaluation is still premature until the save/reopen path is live-proved

## Next honest step

The next step is a bounded Phase 3 live proof closeout slice.

That slice should:

- use the existing genealogy proof page
- start from one completed genealogy saved result
- record one real:
  - compose
  - save
  - reopen by `session_id`
- record one fail-closed invalid-session proof
- prove that reopen does not rerun:
  - `route-task`
  - `plan-task`
  - `planning_decision_fetch`
  - lowering
  - `compose-from-intent`

Do not treat this implementation memo as Phase 3 closure.
The main remaining gap is now live save/reopen evidence, not more lifecycle design work and not Phase 4 governance.
