# Report: Phase E Transient Consumer Identity Generality Scope Audit

Verdict: Approve with corrections

The memo is directionally acceptable as the next smallest bounded Phase E slice, but only if its claim is narrowed. The current repo does support one real remaining anti-coupling question at the proof-only line: transient compose admission is still manually gated by consumer key in code, and the existing standalone harness is still singular on `transient-proof-harness`. But the memo currently overstates what a second proof-only consumer would prove. With the proposed same renderer surface, this is mostly a presenter admission plus end-to-end `consumer_key` propagation check, not a materially stronger renderer-adaptation proof.

## Core Findings

### 1. Transient consumer admission is still hard-coded in presenter code, not driven by consumer definition JSON alone.

This is the most important code seam mismatch in the memo.

- `src/presenter/compose_from_intent.py:158-183` hard-codes `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` and `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER`.
- `src/presenter/compose_from_intent.py:565-585` enforces those maps during request validation.
- `src/consumers/registry.py:45-62` does load consumer definitions from `src/consumers/definitions/*.json`, but that registry is not the admission authority for transient compose routes.

So adding a second proof-only consumer definition under `src/consumers/definitions/` is necessary, but not sufficient. The honest implementation scope is:

- one new proof-only consumer JSON definition
- one explicit presenter allowlist change for exactly `source_selection` and `direct_sections`
- no `source_profile` admission for the new key

### 2. The existing proof-only harness already proves the important shell boundary strongly enough that a second proof-only key would be weak if framed too broadly.

The current proof line already establishes all of the following outside both existing shells:

- one separate repo and harness
- one separate proof-only consumer identity
- both transient route families now relevant here:
  - `compose-from-selection`
  - `compose-from-intent`
- both returned top-level shape classes now relevant here:
  - `tab`
  - `card_grid`

The live closeouts are strong on that bar:

- `communications/PROOF_phase_e_transient_proof_harness_source_selection_live_closeout_2026-03-31.json:21-69` records exact pinned-request equality, `response_status = 200`, `response_presentation_consumer_key = transient-proof-harness`, `observed_root_renderer = tab`, and no forbidden analytical requests.
- `communications/PROOF_phase_e_transient_proof_harness_genealogy_direct_sections_live_closeout_2026-03-31.json:21-48` records the same kind of closure for `direct_sections`, with `observed_root_renderer = card_grid`.
- `tests/test_transient_proof_harness_contract.py:27-76` verifies both frozen proof bundles still match current request/response contract truth for `consumer_key = transient-proof-harness`.

That means a second proof-only consumer is not worthless, but it is only a narrow residual anti-coupling check. If the memo keeps implying a broader generality win, it oversells the slice.

### 3. `source_profile` and readiness can honestly remain fail-closed for the proposed new key.

The current code makes this straightforward.

- `src/presenter/compose_from_intent.py:180-183` only registers `source_profile` support for `the-critic` and `aoi-canary`.
- `tests/test_compose_from_intent.py:1197-1208` already proves `transient-proof-harness` is rejected on `compose-from-source`.
- `src/analysis_products/source_backed_readiness.py:147-160` reuses the same transient handoff capability gate when evaluating AOI follow-up readiness.
- `tests/test_source_backed_readiness.py:295-319` already proves readiness stays blocked for `transient-proof-harness` on AOI `source_profile`.

So the memo is correct that the new proof-only key can stay fail-closed on `source_profile`. It should say this more explicitly as a direct consequence of the current gate structure, not as an aspirational boundary.

### 4. The same harness cannot vary only consumer identity today; that is still prospective, not current fact.

Right now the harness is singular on `transient-proof-harness`.

- `/home/evgeny/projects/transient-proof-harness/src/App.tsx:36-44` hard-codes `CONSUMER_KEY = 'transient-proof-harness'` and binds the app to exactly two proof-case fixtures.
- `/home/evgeny/projects/transient-proof-harness/src/App.tsx:84-87` rejects any response whose `presentation.consumer_key` does not equal that constant.
- `/home/evgeny/projects/transient-proof-harness/src/fixtures/transient-source-selection.json:19-22` and `/home/evgeny/projects/transient-proof-harness/src/fixtures/transient-genealogy-direct-sections.json:17-20` hard-code `consumer_key = transient-proof-harness` inside the pinned requests.
- `/home/evgeny/projects/transient-proof-harness/src/test/App.test.tsx:127-186` and `/home/evgeny/projects/transient-proof-harness/src/test/transientClient.test.ts:123-179` assert exact fixture request bodies, not a consumer-parameterized request builder.

So the memo should not talk as if the same harness already varies only consumer identity. The honest statement is:

- the same harness can be broadened to do so

And the acceptance bar should require that the implementation keep the following fixed while introducing explicit consumer selection:

- same `planning_decision_id`
- same `workflow_key`
- same compose route family per case
- same `source_v2_job_id` where present
- same expected root renderer
- same expected raw-json leaf set

Fresh proof artifact names and fixture identities will necessarily change, but the analytical variable should remain only `consumer_key`.

### 5. The memo overstates the “admission/adaptation” part of the claim if the new consumer uses the same renderer support surface.

`adapt_renderer_for_consumer` is generic and only does meaningful work when the consumer lacks the requested renderer.

- `src/presenter/manifest_builder.py:105-128` shows the adaptation rule: if a consumer supports the renderer, no fallback occurs; otherwise the fallback is `raw_json` if available.
- `src/consumers/definitions/transient-proof-harness.json:6-17` and `src/consumers/definitions/aoi-canary.json:6-17` already expose the same supported renderer and sub-renderer surfaces.

If the proposed `transient-proof-probe` uses the same renderer capability surface as `transient-proof-harness`, then this slice does not materially test new adaptation law. It tests:

- a second admitted proof-only identity
- end-to-end identity propagation through the same request/response surface
- the same already-proved renderer law under a second proof-only key

That is still a valid bounded claim. It is just narrower than “admission/adaptation generality” suggests.

### 6. This slice is smaller than jumping directly to lifecycle on the proof-only harness, but not because it is stronger.

On strategic weight alone, lifecycle on the proof-only line would be the stronger next proof. But it is not obviously the smaller one in the current codebase.

- The roadmap order in `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1140-1142` and `:1172-1186` places lifecycle after stronger host-neutral proof.
- That stronger host-neutral proof now exists in bounded form, so lifecycle is no longer strategically off-limits.
- But the existing compose-session substrate is typed specifically around `ComposeFromIntentRequest`, not a union that also covers `ComposeFromSelectionRequest`:
  - `src/presenter/schemas.py:736-758`
  - `src/api/routes/presenter.py:479-499`
  - `src/presenter/compose_session_store.py:30-60`

That means a proof-only lifecycle slice over the same AOI `source_selection` plus genealogy `direct_sections` pair would either:

- widen the lifecycle save/fetch contract
- or drop the AOI `source_selection` case

Either move is broader than the current memo admits. So the proposed second proof-only identity is still the smaller bounded next step, but it is not the stronger substantive proof. The memo should reflect that tradeoff honestly.

### 7. The broader roadmap mostly supports this direction, but one roadmap document still shows stale “next slice” text.

The current documentary stack is not perfectly uniform.

- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:383-398` explicitly says the next bounded Phase E question is one additional proof-only consumer identity over the same harness and same two seams.
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:334-356` also now points to that same next question.
- But `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:256-260` still contains an older stale “next bounded slice should be `source_profile:comparison`” subsection.

So the memo is broadly aligned with the current strategic direction, but it should not pretend the roadmap stack is perfectly synchronized. There is minor documentary lag inside the strategic memo set.

## Decision

Approve with corrections.

This is still the next smallest honest bounded Phase E slice if the goal is to isolate one remaining proof-only anti-coupling variable without widening lifecycle or source-profile law. But the memo must narrow what the slice proves.

The honest resulting claim is:

- analyzer transient proof on the standalone harness is not singular to one proof-only consumer key; with one additional explicit presenter admission and one additional proof-only consumer definition, the same already-proved harness surface can carry two proof-only consumer identities over the same AOI `source_selection` and genealogy `direct_sections` seams while `source_profile` remains fail-closed

It should not claim:

- broad generic consumer registration
- materially stronger renderer-adaptation generality
- lifecycle law
- source-profile generality
- or that consumer identity no longer matters in general

## Required Corrections

1. State explicitly that transient compose admission remains hard-coded in `src/presenter/compose_from_intent.py`; consumer JSON alone is not the admission seam.
2. Narrow “admission/adaptation” language to “manual proof-only consumer admission plus end-to-end consumer identity propagation over the same already-proved renderer surface.”
3. Add an explicit acceptance criterion that `source_profile` and AOI source-backed readiness remain blocked for the new proof-only consumer.
4. Add an explicit acceptance criterion that the harness must introduce consumer selection transparently and keep all non-identity analytical variables fixed.
5. Add an explicit acceptance criterion that fresh fixtures and live closeouts under the new key preserve:
   - same `planning_decision_id`
   - same `workflow_key`
   - same route family
   - same expected root renderer
   - same raw-json leaf set
6. Add one sentence acknowledging that lifecycle on the proof-only line is a stronger later step, but not the smaller one yet because the current compose-session save/fetch contract is `ComposeFromIntentRequest`-shaped.
7. If the memo cites the broader roadmap, acknowledge the stale subsection in the distilled roadmap rather than presenting the memo stack as perfectly synchronized.

## Verification

Focused verification passed on the current repo state:

- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_source_backed_readiness.py tests/test_transient_proof_harness_contract.py tests/test_compose_sessions.py`
  - `60 passed, 2 warnings`
- `npm --prefix /home/evgeny/projects/transient-proof-harness run test -- --run`
  - `7 passed`
