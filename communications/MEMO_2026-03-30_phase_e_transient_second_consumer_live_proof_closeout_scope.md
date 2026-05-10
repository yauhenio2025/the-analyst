# Memo: Phase E Transient Second-Consumer Live Proof Closeout Scope

Subtitle: Close the implemented `aoi-canary` transient slice with one real browser/network proof

Date: 2026-03-30
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Immediate Prior Scope:
- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_scope.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_v1_implementation_completion.md`
Relevant Prior Live Closeout Pattern:
- `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md`
Review Context:
- `communications/REPORT_Claude_Phase_E_Transient_Second_Consumer_Scope_Critique_2026-03-30.md`
- `communications/REPORT_Codex_Phase_E_Transient_Second_Consumer_Scope_Audit_2026-03-30.md`

## Purpose

Define the immediate next bounded step after the Phase E transient second-consumer implementation landed in code.

This is not another second-consumer architecture memo.

The current boundary is narrower:

- the analyzer change is landed
- the canary transient mode is landed
- focused analyzer and canary tests pass
- the existing proof JSON is deterministic replay
- the stronger browser/network proof bar is still open

So the next honest step is:

- one bounded live proof closeout

not:

- another consumer
- another compose family
- a broader consumer-generalization tranche
- or a new architecture line

## Current Code-Backed Boundary

### What now exists

The current codebase already has all of the following:

- analyzer-side handoff-aware transient consumer admission for:
  - `the-critic`
  - `aoi-canary` on AOI `source_selection` only
- continued fail-closed behavior for `aoi-canary` on:
  - `source_profile`
  - `direct_sections`
- one fixture-backed `transient_proof` mode in `aoi-canary`
- one pinned analyzer-owned `ComposeFromSelectionRequest` fixture in the canary repo
- one thin canary-side field-only normalization adapter from analyzer transient response into the local page shell
- one measurable adaptation-quality law:
  - root `tab`
  - no root `raw_json`
  - at most one `raw_json` leaf
  - that one leaf, if present, is the closeout/report leaf only

Primary files carrying that reality:

- `src/presenter/compose_from_intent.py`
- `tests/test_compose_from_intent.py`
- `tests/test_aoi_canary_contract.py`
- `/home/evgeny/projects/aoi-canary/src/App.tsx`
- `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts`
- `/home/evgeny/projects/aoi-canary/src/fixtures/transient-aoi-source-selection.json`
- `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx`
- `/home/evgeny/projects/aoi-canary/src/test/transientClient.test.ts`

### What is still not proved

The program still does not have one recorded live proof that shows:

- `aoi-canary` in `transient_proof` mode
- one real browser/network `POST /v1/presenter/compose-from-selection`
- `consumer_key = aoi-canary`
- one real rendered ready state on the canary from that live response
- one recorded success path proving the live request seam actually used

Important current law that this closeout must preserve:

- the canary replays a pinned analyzer-owned request fixture
- the canary does not derive source selection locally
- the canary does not fetch planner truth or reconstruct analytical meaning
- the analyzer public route shapes stay unchanged
- the claim remains:
  - one bounded live second-consumer closeout on one already-landed AOI path

## Why This Is The Next Honest Step

The implementation question is already answered.

Analyzer-v2 can now admit one second transient consumer on one bounded path, and the canary can render the returned response through a thin host adapter without host-local analytical reconstruction.

What is still missing is evidentiary:

- the original scope wanted a live proof bundle with browser/network evidence
- the implementation pass did not close that bar
- the gap came from an unrelated engine-definition load error during direct live capture, not from a failure of the second-consumer seam itself

So the next step should be:

- close the live-proof tail cleanly on the exact path already implemented

not:

- reopen second-consumer design
- widen to `source_profile`
- widen to non-AOI consumer proof
- or downgrade the claim silently

## Strategic Decision

Do not widen the implementation surface.

The proof target stays:

- consumer:
  - `aoi-canary`
- path:
  - AOI `source_selection`
- route:
  - `POST /v1/presenter/compose-from-selection`
- host mode:
  - `transient_proof`

Why this is the right closeout target:

1. It is the exact bounded path already landed and test-clean.
2. It closes the proof bar that the implementation completion memo explicitly left open.
3. It keeps the question evidentiary rather than architectural.
4. It avoids hiding behind a weaker fallback path or a different consumer.

## Scope Decisions

### Decision 1: This is evidence capture, not new architecture

Do not widen this step into:

- broader consumer registry work
- planner integration inside `aoi-canary`
- a new proof framework
- `source_profile` fallback
- `compose-from-intent` consumer widening
- result-backed `aoi-canary` work

Production changes are allowed only if they are needed to unblock truthful live capture on the already-landed path.

### Decision 2: The acceptance path is the already-landed fixture-backed transient mode

The required live success chain is:

1. open `aoi-canary` in `transient_proof` mode
2. load the pinned `transient-aoi-source-selection.json` fixture
3. issue one real `POST /v1/presenter/compose-from-selection`
4. receive one real `ComposeFromIntentResponse`
5. render the ready state in `aoi-canary`
6. record the browser/network evidence for that live seam

Manual curl probes may remain useful for diagnosis, but they do not count as closeout by themselves.

### Decision 3: Live evidence must prove the exact seam used

The closeout must save evidence that makes the success path auditable.

Minimum proof surface:

- the exact analyzer base URL used
- the exact canary mode used
- the pinned fixture identity
- the exact POST body sent on the wire for `compose-from-selection`
- one browser screenshot showing the rendered ready state
- one fresh-session HAR or equivalent full network capture showing:
  - the real `compose-from-selection` request
  - `consumer_key = aoi-canary`
  - the returned response

The JSON proof summary should tie these together mechanically:

- pinned fixture request truth
- observed live POST body truth
- response truth

and should state explicitly whether:

- `observed_request_json == pinned_fixture.request`

Recommended artifact set:

- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_live_closeout_2026-03-30.md`
- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_live_closeout_2026-03-30.json`
- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_live_closeout_2026-03-30.png`
- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_live_closeout_2026-03-30.har`

### Decision 4: The live closeout must preserve the thin-host claim mechanically

The closeout must make it visible that the canary did not perform hidden analytical upstream work.

The success-path evidence should make clear that the live path did not call:

- `route-task`
- `plan-task`
- planning-snapshot fetch
- `compose-from-source`
- `compose-from-intent`

The only analytical request seam that should appear in the proof success path is:

- `POST /v1/presenter/compose-from-selection`

Allowed non-analytical supporting requests may still appear and should be called out honestly in the proof note, for example:

- style-token fetch such as `GET /v1/styles/tokens/{school}`

Those requests do not weaken the thin-host claim as long as they remain presentation/support surfaces rather than analytical reconstruction seams.

### Decision 5: The quality bar remains the same as the implemented law

The live proof counts only if the rendered state still satisfies the bounded degradation law already enforced in code:

- root renderer is `tab`
- no root `raw_json`
- at most one `raw_json` leaf
- if present, that leaf is the closeout/report leaf only

The live closeout should not silently relax this bar just because the path is browser-backed instead of test-backed.

### Decision 6: The engine-definition blocker is allowed only as a bounded unblocker

The implementation pass recorded one unrelated blocker during direct live capture:

- engine-definition load failure, not a second-consumer contract failure

Allowed response:

- fix or route around that blocker only enough to permit one truthful live success capture on the existing path

Not allowed:

- broad engine-definition cleanup as a new tranche
- widening the proof path to avoid the blocker
- silently reclassifying deterministic replay as live proof

If the blocker turns out to require broader infrastructure work, stop and rescope instead of pretending the closeout is cheap.

## Must Not Widen

- do not reopen second-consumer architecture
- do not widen to `source_profile`
- do not add a non-AOI second-consumer proof
- do not add planner integration to `aoi-canary`
- do not make the canary derive selection locally
- do not change public compose route shapes
- do not downgrade the proof bar from live capture to replay and still call it closed

## Proposed Acceptance Bar

This closeout should count only if all of the following are true:

1. `aoi-canary` in `transient_proof` mode completes one real `compose-from-selection` success path against analyzer-v2
2. a fresh-session HAR or equivalent full network capture is saved for that success path
3. the browser/network evidence shows `consumer_key = aoi-canary` on the actual live request
4. the closeout record freezes the exact observed POST body and ties it mechanically to the pinned fixture request
5. the rendered canary ready state is captured from that live response
6. the success-path evidence shows no hidden upstream analytical requests beyond the intended compose call
7. the rendered page still satisfies the bounded adaptation-quality law:
   - root `tab`
   - no root `raw_json`
   - at most one `raw_json` leaf
8. the closeout record explicitly distinguishes the new live proof from the earlier deterministic replay artifact
9. the proof record is frozen under `communications/`

## Practical Constraints

This slice is not code-complete by definition.
It is evidence-complete or not.

It will likely require:

- one live analyzer instance that can serve the already-landed path
- one live canary run in `transient_proof` mode
- one browser/network capture pass

If a small blocker fix is required to make that possible, that is acceptable.
If a broader system repair is required, that is a different scope.

## Decision

The next bounded Phase E step should be:

- one transient second-consumer live proof closeout over the already-landed `aoi-canary` / AOI `source_selection` path

The strategic reason is simple:

- the implementation and tests already answer the contract question
- the remaining gap is the live documentary bar
- the right move is to close that bar honestly before varying a new Phase E variable
