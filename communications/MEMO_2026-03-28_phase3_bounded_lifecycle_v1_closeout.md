# Phase 3 Bounded Lifecycle V1 Closeout

Date: 2026-03-28
Status: Closed honestly
Outcome: `compose -> save -> reopen by session_id` proved live on the genealogy transient proof surface

## Decision

Phase 3 now closes honestly.

The bounded lifecycle v1 implementation is no longer only code-complete. It is now live-proved on the existing genealogy proof page with a fresh-navigation reopen by `session_id`, exact saved compose-session truth served back from analyzer-owned storage, and no planner or composition replay during reopen.

The lifecycle identity proved here is `session_id`, not `planning_decision_id`.

## Scope And Target

This closeout executed the bounded Phase 3 live-proof scope from:

- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_closeout_scope.md`

Fixed proof target:

- `project_id = round4-proof-balance-final-1774012011`
- `source_v2_job_id = proof-round4-adaptive-balance-final-1774012011`
- `task = Trace the genealogy and intellectual development visible in this saved result.`

## What Passed

### 1. Preflight passed on the fixed genealogy saved result

Artifact:

- `communications/PROOF_phase3_bounded_lifecycle_v1_preflight_2026-03-28.json`

Recorded preflight fields:

- `workflow_key = intellectual_genealogy`
- `status = completed`
- `result_state = ready`
- `presentation_status = completed`
- `restore_available = true`

### 2. Live compose and save succeeded on the proof page

Artifacts:

- `communications/PROOF_phase3_bounded_lifecycle_v1_trace_2026-03-28.json`
- `communications/PROOF_phase3_bounded_lifecycle_v1_rendered_2026-03-28.png`
- `communications/PROOF_phase3_bounded_lifecycle_v1_session_2026-03-28.har`

Observed saved lifecycle identity:

- `session_id = compose-session-0877864dcca7`

The trace artifact includes:

- run detail
- routing decision
- planning decision
- persisted planning snapshot
- analyzer-owned lowered compose request
- compose response
- saved session URL

### 3. Reopen by fresh navigation succeeded without recomputation

Artifacts:

- `communications/PROOF_phase3_bounded_lifecycle_v1_saved_session_2026-03-28.json`
- `communications/PROOF_phase3_bounded_lifecycle_v1_reopen_segment_2026-03-28.json`

The reopen was evaluated only after fresh navigation to:

- `http://127.0.0.1:3456/p/round4-proof-balance-final-1774012011/proof/transient/genealogy-saved-result?session_id=compose-session-0877864dcca7`

The reopen-segment artifact shows:

- exactly one `GET /v1/presenter/compose-sessions/{session_id}`
- zero reopen calls to:
  - `route-task`
  - `plan-task`
  - `planning_decision_fetch`
  - `planning_decision_compose_request`
  - `POST /v1/presenter/compose-from-intent`

Saved-session fidelity fields on the fetched session record:

- `workflow_key = intellectual_genealogy`
- `consumer_key = the-critic`
- `presentation_hash = 7269c27d5591825b19da9d0e82300d20863ee2230fbf91c7f29d54436c050340`
- `presentation_content_hash = 340f49ca60b60855bc786eae96aec9448a636906b86a3b1d65c1851e499a62a2`
- `resolver_version = compose-from-intent-v2`

These fields came from the fetched saved-session record, not from planner replay and not from host-local reconstruction.

### 4. Invalid-session reopen failed closed

Artifact:

- `communications/PROOF_phase3_bounded_lifecycle_v1_invalid_session_2026-03-28.json`

Observed failure text:

- `Proof Error`
- `Compose session 'compose-session-invalid' not found`

The negative artifact also showed:

- no fallback to old in-memory compose state
- no replay of planner/composition endpoints
- no AOI proxy route
- no `/v1/executor/jobs` path

## Bounded Fixes Needed During Closeout

Two small live-proof fixes were required to turn the Phase 3 implementation into a clean closeout:

1. Proof-page label fix

- `GenealogyTransientProofPage` still said `Phase 2 Proof`
- it was updated to `Phase 3 Lifecycle Proof` so screenshot evidence is not mislabeled

2. Reopen fetch dedupe moved from page logic to client runtime

- the first reopen attempt exposed a React dev double-effect seam on fresh navigation
- page-level dedupe suppressed the second effect pass and starved the saved-session render
- the bounded repair was to remove the page-level session-id suppression and dedupe concurrent session fetches in `composeFromIntentClient.getComposeSession(...)`

This preserved the Phase 3 closeout bar:

- one real saved-session GET on reopen
- one successful render path from saved truth
- no planner/composition replay

## Verification

Focused frontend regression after the bounded fixes:

```bash
CI=true npm test -- --runInBand --watchAll=false src/lib/composeFromIntentClient.test.ts src/pages/GenealogyTransientProofPage.test.tsx
```

Result:

- `2` suites passed
- `9` tests passed

## Conclusion

Phase 3 is now closed.

What is now proved live:

- analyzer-owned transient compose sessions can be saved explicitly
- `session_id` is the durable lifecycle identity
- reopen by `session_id` can occur on fresh navigation
- reopen serves saved compose-session truth
- reopen does not rerun planner or presenter composition
- invalid lifecycle identity fails closed

The next honest main line is now Phase 4 governance/evaluation.
