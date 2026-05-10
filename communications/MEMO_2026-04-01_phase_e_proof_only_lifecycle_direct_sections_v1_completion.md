# Memo: Phase E Proof-Only Lifecycle `direct_sections` V1 Completion

Subtitle: The standalone proof harness now carries one bounded analyzer-owned save/reopen lifecycle seam over genealogy `direct_sections`

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
- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_direct_sections_scope.md`
Most Recent Prior Completion:
- `communications/MEMO_2026-04-01_phase_e_transient_consumer_identity_plurality_v1_completion.md`
Relevant Prior Lifecycle Proof:
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_closeout.md`
Review Context:
- `communications/REPORT_Claude_Phase_E_Proof_Only_Lifecycle_Direct_Sections_Scope_Critique_2026-04-01.md`
- `communications/REPORT_Codex_Phase_E_Proof_Only_Lifecycle_Direct_Sections_Scope_Audit_2026-04-01.md`
Proof Artifacts:
- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_saved_session_2026-04-01.json`
- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_reopen_segment_2026-04-01.json`
- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_invalid_session_2026-04-01.json`
- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_session_2026-04-01.har`
- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_rendered_2026-04-01.png`

## Purpose

Record completion of the bounded Phase E slice that re-proved the already-earned analyzer-owned `direct_sections` lifecycle law across the standalone proof harness boundary.

This slice answered one narrow question:

- can the thinner standalone harness at `/home/evgeny/projects/transient-proof-harness` carry `compose -> explicit save -> fresh-navigation reopen by session_id` on the existing genealogy `direct_sections` seam, without recomputation on reopen and without widening the current public save contract?

It did not attempt to invent new lifecycle semantics. March 28 had already proved the underlying analyzer-owned lifecycle law on this seam in the older current-consumer shell. The April 1 slice re-proved that same law across the standalone proof-only harness boundary.

## Outcome

That bounded question is now answered in the affirmative.

The standalone harness can now:

1. compose the pinned genealogy `direct_sections` case under `consumer_key=transient-proof-harness`
2. explicitly save the exact intent-shaped request plus exact raw compose response through `POST /v1/presenter/compose-sessions`
3. receive analyzer-generated `session_id`
4. treat `session_id` as lifecycle identity and `planning_decision_id` as provenance only
5. reopen by fresh navigation to a `sessionId` URL
6. render the saved surface from `GET /v1/presenter/compose-sessions/{session_id}?consumer_key=transient-proof-harness`
7. do so with zero second `POST /v1/presenter/compose-from-intent` on reopen

The honest closed claim remains narrow:

- one fixed proof-only consumer on the standalone harness now carries one bounded analyzer-owned save/reopen lifecycle seam over genealogy `direct_sections`

This does not mean:

- AOI `source_selection` lifecycle is solved
- source-profile lifecycle is solved
- consumer identity no longer matters for lifecycle
- the compose-session save contract is generalized across request families
- generic saved-session app/runtime architecture now exists

## What Landed

### 1. Harness-side save/fetch lifecycle plumbing

The standalone harness gained two lifecycle client functions:

- save compose session
- fetch compose session

They live in:

- `/home/evgeny/projects/transient-proof-harness/src/lib/transientClient.ts`

Important contract discipline that now holds:

- save sends the exact raw `ComposeFromIntentResponse`, not a lossy normalized projection
- harness typing now carries `presentation_hash` and `presentation_content_hash` on the raw compose response
- save includes `planning_decision_id` provenance when available
- save omits `source_v2_job_id` when it is not real for the case
- reopen passes `?consumer_key=transient-proof-harness` explicitly
- duplicate reopen fetches dedupe in-flight by `baseUrl + consumerKey + sessionId`

### 2. Standalone-harness lifecycle flow over one fixed case

The lifecycle UI/state landed only for:

- `consumer_key = transient-proof-harness`
- `proofCase = genealogy_direct_sections`

That bounded gating lives in:

- `/home/evgeny/projects/transient-proof-harness/src/App.tsx`

Everything else remains transient-only in parallel:

- AOI `source_selection`
- proof-only plurality via `transient-proof-probe`

The lifecycle identity law is now explicit in the harness:

- before save:
  - visible identity is provenance (`planning_decision_id`)
- after save:
  - visible primary identity flips to analyzer-generated `session_id`
- on reopen:
  - visible primary identity remains `session_id`
- `planning_decision_id` stays visible only as provenance

### 3. Fresh-navigation reopen with no recomputation

The live proof bar on this harness was intentionally narrower and more concrete than the older current-consumer lifecycle proof:

- one saved-session GET on reopen
- zero second `POST /v1/presenter/compose-from-intent`
- zero hidden in-memory fallback
- fresh navigation to a URL with `sessionId`

That exact law is frozen in:

- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_reopen_segment_2026-04-01.json`

The reopened proof payload preserves the saved response truth on:

- `consumer_key`
- `workflow_key`
- `presentation_hash`
- `presentation_content_hash`
- `resolver_version`

### 4. Generic analyzer save/fetch seam remains unchanged

Analyzer-side work stayed narrow.

No route or schema widening landed. The public save/fetch seam remains:

- `ComposeSessionSaveRequest.compose_request: ComposeFromIntentRequest`
- `PersistedComposeSession.compose_request: ComposeFromIntentRequest`

The analyzer-side addition for this slice was one focused round-trip test for `consumer_key=transient-proof-harness` in:

- `tests/test_compose_sessions.py`

This kept the slice honest:

- the lifecycle broadening was at the host boundary
- not by inventing a new analyzer save contract

### 5. Post-audit identity-display hardening

The first lifecycle capture proved the transport/save/reopen law correctly, but an audit found one real UI miss:

- after save, the primary visible identity still showed `planning_decision_id`
- `session_id` only became primary after reopen

That hardening is now landed in:

- `/home/evgeny/projects/transient-proof-harness/src/App.tsx`
- `/home/evgeny/projects/transient-proof-harness/src/test/App.test.tsx`

The harness now switches the primary identity card to `session_id` immediately after successful save.

Important documentary note:

- the frozen lifecycle artifact family already proves the transport/save/reopen law and the reopened-session identity law
- the post-save primary-identity display correction was verified by focused harness tests/build after the initial artifact capture
- the lifecycle artifact family was not regenerated solely for that display-only hardening

## Verification

Focused analyzer verification for this slice:

- `PYTHONPATH=. pytest -q tests/test_compose_sessions.py tests/test_transient_proof_harness_contract.py`
- result: `8 passed`

Focused harness verification for this slice:

- `npm --prefix /home/evgeny/projects/transient-proof-harness run test -- --run`
- result: `16 passed`

- `npm --prefix /home/evgeny/projects/transient-proof-harness run type-check`
- result: passed

- `npm --prefix /home/evgeny/projects/transient-proof-harness run build`
- result: passed

The live lifecycle proof recorded:

- save includes `planning_decision_id = planning-decision-5f5b0182f2f9`
- save omits `source_v2_job_id`
- analyzer returns `session_id = compose-session-c12c16058f49`
- fresh navigation URL includes `sessionId=compose-session-c12c16058f49`
- reopen makes exactly one `GET /v1/presenter/compose-sessions/{session_id}?consumer_key=transient-proof-harness`
- reopen makes zero second `POST /v1/presenter/compose-from-intent`
- invalid session returns one `404` fetch and zero compose fallback

## Worktree Notes

At live-capture time:

- `analyzer_v2_repo_state = dirty`
- `transient_proof_harness_repo_state = dirty`

The analyzer-v2 worktree already had a large set of unrelated tracked and untracked changes before this slice. Only the files explicitly named in this memo were changed for this lifecycle proof line.

## Honest Boundary

### What is now true

- the standalone harness can compose, save, and reopen one bounded genealogy `direct_sections` surface
- `session_id` is now the lifecycle identity on the harness
- `planning_decision_id` remains provenance only
- reopen is served from analyzer-owned saved session truth
- the public save/fetch seam remains unchanged and intent-shaped
- plurality remains intact in parallel:
  - `transient-proof-harness`
  - `transient-proof-probe`
  - both transient-only proof cases

### What is not yet true

- AOI `source_selection` save/reopen on the standalone harness
- source-profile lifecycle on the standalone harness
- lifecycle over both proof-only consumer identities
- generic save/fetch support across multiple compose request families
- productized saved-session browsing

### What this slice actually proved

The substance of this slice is:

1. the already-proved analyzer-owned `direct_sections` lifecycle seam survives the standalone proof-harness boundary
2. that proof can run on a thinner host with no planner fetch, lowering fetch, or host-side analytical reconstruction
3. `session_id` identity can remain analyzer-owned and explicit on the proof-only harness line
4. invalid saved-session reopen fails closed without compose fallback

This is host-boundary strengthening, not a new lifecycle-theory claim.

## Decision

This bounded Phase E slice is complete on its intended bar.

The program now has:

- one current-consumer lifecycle proof on genealogy `direct_sections` from March 28
- one standalone-harness lifecycle proof on that same genealogy `direct_sections` seam from April 1

The next honest Phase E question is no longer whether the proof-only harness can carry any lifecycle seam at all.

The next bounded step should now be:

- one standalone-harness AOI `source_selection` lifecycle proof
- through an analyzer-owned lowered-request persistence bridge
- without forcing harness-local request reconstruction
- and without distorting the current save contract into a generic union by default

Why that is the next honest slice:

- `direct_sections` lifecycle on the proof-only line is now closed
- the remaining open transient family on that same harness is AOI `source_selection`
- the real unresolved question is now contractual:
  - how can analyzer-owned lifecycle truth for `source_selection` be persisted honestly when the public save seam is still `ComposeFromIntentRequest`-shaped?

So the clean next question is:

- can the proof-only harness now carry AOI `source_selection` lifecycle by relying on analyzer-owned lowered request truth, rather than by widening the save seam carelessly or synthesizing lowered prose locally?
