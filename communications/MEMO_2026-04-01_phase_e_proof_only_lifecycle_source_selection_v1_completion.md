# Memo: Phase E Proof-Only Lifecycle `source_selection` V1 Completion

Subtitle: The standalone proof harness now carries one bounded analyzer-owned save/reopen lifecycle seam over AOI `source_selection`

Date: 2026-04-01
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
- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_source_selection_scope.md`
Most Recent Prior Completion:
- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_direct_sections_v1_completion.md`
Review Context:
- `communications/REPORT_Claude_Phase_E_Proof_Only_Lifecycle_Source_Selection_Scope_Critique_2026-04-01.md`
- `communications/REPORT_Codex_Phase_E_Proof_Only_Lifecycle_Source_Selection_Scope_Audit_2026-04-01.md`
Proof Artifacts:
- `communications/PROOF_phase_e_proof_only_lifecycle_source_selection_saved_session_2026-04-01.json`
- `communications/PROOF_phase_e_proof_only_lifecycle_source_selection_reopen_segment_2026-04-01.json`
- `communications/PROOF_phase_e_proof_only_lifecycle_source_selection_invalid_session_2026-04-01.json`
- `communications/PROOF_phase_e_proof_only_lifecycle_source_selection_session_2026-04-01.har`
- `communications/PROOF_phase_e_proof_only_lifecycle_source_selection_rendered_2026-04-01.png`

## Purpose

Record completion of the bounded Phase E slice that broadened standalone-harness lifecycle from genealogy `direct_sections` to AOI `source_selection`.

This slice answered one narrow question:

- can the standalone proof harness save and reopen AOI `source_selection` honestly through the existing analyzer-owned compose-session seam, by using analyzer-owned lowered request truth rather than reconstructing that request in the host?

It did not attempt to solve generic lifecycle architecture.

It did not attempt to solve:

- `source_profile` lifecycle
- lifecycle across every compose request family
- generic saved-session browsing
- server-side generalized request-family persistence

## Outcome

That bounded question is now answered in the affirmative.

The standalone harness at `/home/evgeny/projects/transient-proof-harness` can now:

1. compose the pinned AOI `source_selection` case under `consumer_key=transient-proof-harness`
2. receive one analyzer-owned persistable lowered compose request on that response
3. save the exact lowered request plus exact raw compose response through `POST /v1/presenter/compose-sessions`
4. include truthful AOI provenance:
   - `planning_decision_id`
   - `source_v2_job_id`
5. receive analyzer-generated `session_id`
6. switch the primary visible lifecycle identity to that `session_id`
7. reopen by fresh navigation to a `sessionId` URL
8. render from `GET /v1/presenter/compose-sessions/{session_id}?consumer_key=transient-proof-harness`
9. do so with zero second compose calls on reopen

The honest closed claim remains narrow:

- one fixed proof-only consumer on the standalone harness now carries one bounded analyzer-owned save/reopen lifecycle seam over AOI `source_selection`

This does not mean:

- `source_profile` lifecycle is solved
- lifecycle is generalized across all compose request families
- the public save seam is now request-family-agnostic
- server-side persistence enforces every host-side equality guarantee automatically

## What Landed

### 1. One analyzer-owned persistence field for `compose-from-selection`

Analyzer-v2 now surfaces one analyzer-owned lowered request for AOI source-selection persistence:

- `src/presenter/schemas.py`
- `src/presenter/compose_from_intent.py`

The bounded contract shape is:

- `ComposeFromIntentResponse.persistable_compose_request: Optional[ComposeFromIntentRequest]`

Important discipline:

- the field is populated for `compose-from-selection`
- it carries the exact lowered `ComposeFromIntentRequest` used for the compose call
- it remains absent / `None` for plain `compose-from-intent`

This keeps the existing save/fetch seam stable:

- `ComposeSessionSaveRequest.compose_request` is still `ComposeFromIntentRequest`
- `PersistedComposeSession.compose_request` is still `ComposeFromIntentRequest`

What changed is the response truth available to the harness, not the request family persisted by the analyzer.

### 2. Standalone-harness lifecycle broadening on one bounded AOI case

The standalone harness lifecycle gate now covers:

- `consumer_key = transient-proof-harness`
- `proofCase = genealogy_direct_sections`
- `proofCase = source_selection`

That work landed in:

- `/home/evgeny/projects/transient-proof-harness/src/App.tsx`
- `/home/evgeny/projects/transient-proof-harness/src/lib/transientClient.ts`

For AOI `source_selection`, the save law is now explicit:

- save uses `response.persistable_compose_request`
- save does not send the original `ComposeFromSelectionRequest` fixture as `compose_request`
- save includes:
  - `planning_decision_id`
  - `source_v2_job_id`

Lifecycle identity law remains unchanged:

- before save:
  - visible identity is provenance
- after save:
  - visible primary identity flips to analyzer-generated `session_id`
- on reopen:
  - visible primary identity remains `session_id`
- `planning_decision_id` and `source_v2_job_id` remain provenance only

### 3. Fresh-navigation reopen with no recomputation

The reopened proof bar on this harness is the same concrete bar used on the direct-sections lifecycle line:

- fresh navigation to a URL with `sessionId`
- one saved-session GET
- zero second `POST /v1/presenter/compose-from-selection`
- zero `POST /v1/presenter/compose-from-intent`
- zero hidden in-memory fallback

That law is frozen in:

- `communications/PROOF_phase_e_proof_only_lifecycle_source_selection_reopen_segment_2026-04-01.json`

The reopened saved truth preserves:

- `consumer_key = transient-proof-harness`
- `workflow_key = anxiety_of_influence_thematic_single_thinker`
- `resolver_version = compose-from-selection-v1`
- `presentation_hash = b7e781aaeb362e7e19d6142c9ff90f8f7ffc224b02f16c0d344d21d562c2305b`
- `presentation_content_hash = 7d8af7a84e0cfc9919352938a517f7c662e131e18c1234c2d58fc7cdd111564d`

### 4. Saved-request equality is now frozen mechanically

The saved-session proof family now records all three relevant request forms:

- original `ComposeFromSelectionRequest`
- analyzer-owned `persistable_compose_request`
- saved `compose_request`

The frozen saved-session proof records:

- `planning_decision_id = planning-decision-d6b6bb0cd7ac`
- `source_v2_job_id = job-744edf255ad5`
- `session_id = compose-session-b427f18617af`
- `saved_compose_request_equals_analyzer_persistable_compose_request = true`

This is the key documentary bar for the slice:

- the host did not reconstruct the lowered request
- it persisted the analyzer-owned lowered request exactly

### 5. One residual hardening gap remains analyzer-side

This slice is complete on its scoped bar, but one narrower hardening gap remains:

- `src/presenter/compose_session_store.py` does not itself enforce `compose_request == compose_response.persistable_compose_request` when that response field is present

So today the equality guarantee is carried by:

- harness behavior
- harness tests
- analyzer response-field tests
- frozen proof artifacts

It is not yet an analyzer-side save-store validation rule.

That is a real residual seam, but it does not block this proof-only V1 closeout.

## Verification

Focused analyzer verification for this slice:

- `PYTHONPATH=. pytest -q tests/test_compose_sessions.py tests/test_compose_from_intent.py tests/test_source_backed_readiness.py tests/test_transient_proof_harness_contract.py -k "compose_session or compose_from_selection or transient_proof_harness or source_profile"`
- result: `23 passed, 45 deselected, 2 warnings`

Focused harness verification for this slice:

- `npm --prefix /home/evgeny/projects/transient-proof-harness run test -- --run`
- result: `21 passed`

- `npm --prefix /home/evgeny/projects/transient-proof-harness run type-check`
- result: passed

- `npm --prefix /home/evgeny/projects/transient-proof-harness run build`
- result: passed

The live proof recorded:

- saved request equals analyzer-owned `persistable_compose_request`
- save contains `planning_decision_id`
- save contains `source_v2_job_id`
- reopen uses exactly one saved-session GET
- reopen makes zero second compose POSTs
- invalid session returns one `404` and zero compose fallback

## Worktree Notes

At capture time:

- `analyzer_v2_repo_state = dirty`
- `transient_proof_harness_repo_state = dirty`

The analyzer-v2 worktree already had unrelated tracked and untracked changes before this slice. Only the files explicitly named in this memo were changed for the AOI source-selection lifecycle line.

## Honest Boundary

### What is now true

- the standalone harness can now save and reopen AOI `source_selection`
- the save path uses analyzer-owned lowered request truth rather than host-local reconstruction
- `session_id` is now the lifecycle identity on the harness for both:
  - genealogy `direct_sections`
  - AOI `source_selection`
- `planning_decision_id` and `source_v2_job_id` remain provenance only
- reopen is served from analyzer-owned saved-session truth
- the public save/fetch seam remains intent-shaped

### What is not yet true

- `source_profile` lifecycle on the standalone harness
- lifecycle on `transient-proof-probe`
- generic request-family persistence across save/fetch
- analyzer-side enforcement that persisted lowered request truth matches the response field whenever present
- productized session browsing or multi-session UX

### What this slice actually proved

The substance of this slice is:

1. AOI `source_selection` can now cross the standalone proof-harness lifecycle boundary honestly
2. analyzer-owned lowered request truth can be carried to save without host reconstruction
3. the existing analyzer save/fetch seam is sufficient for this one bounded AOI lifecycle case
4. reopened AOI saved truth can render with zero recomposition

This is one bounded host-boundary strengthening slice, not general lifecycle closure.

## Decision

This bounded Phase E slice is complete on its intended bar.

The program now has:

- one current-consumer lifecycle proof on genealogy `direct_sections`
- one standalone-harness lifecycle proof on genealogy `direct_sections`
- one standalone-harness lifecycle proof on AOI `source_selection`

The next honest Phase E question is no longer whether the proof-only harness can carry AOI `source_selection` lifecycle.

The next broader question is:

- whether lifecycle should broaden further to source-backed `source_profile` on the proof-only line at all, or whether lifecycle broadening should stop until the analyzer save contract is cleaner and more general

That next question should be scoped explicitly rather than assumed.
