# Report: Codex Audit Of Phase E Transient Second-Consumer Live Proof Closeout Scope

Scope memo:
- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md`

Related materials reviewed:
- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_v1_implementation_completion.md`
- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_scope.md`
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
- `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json`
- `communications/PROOF_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout.md`

Code reviewed:
- `src/presenter/compose_from_intent.py`
- `src/api/routes/presenter.py`
- `src/analysis_products/source_backed_readiness.py`
- `src/consumers/definitions/aoi-canary.json`
- `tests/test_compose_from_intent.py`
- `tests/test_aoi_canary_contract.py`
- `tests/test_representative_composition_matrix.py`
- `/home/evgeny/projects/aoi-canary/src/App.tsx`
- `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts`
- `/home/evgeny/projects/aoi-canary/src/fixtures/transient-aoi-source-selection.json`
- `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx`
- `/home/evgeny/projects/aoi-canary/src/test/transientClient.test.ts`
- `/home/evgeny/projects/aoi-canary/README.md`

Verification run:
- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_aoi_canary_contract.py tests/test_representative_composition_matrix.py`
  - result: `38 passed, 2 warnings`
- `npm --prefix /home/evgeny/projects/aoi-canary run type-check`
  - result: passed
- `npm --prefix /home/evgeny/projects/aoi-canary run test -- --run`
  - result: `18 passed`

Re-review note:
- reviewed again after the scope memo was revised to incorporate the earlier evidentiary corrections
- no tests were rerun for this docs-only memo revision

## Verdict

`Approve`

## Bottom Line

One live-proof closeout over the already-landed `aoi-canary` / AOI `source_selection` path is still the right next Phase E step.
The deterministic replay proof still should not count as sufficient closure, because the current proof artifact explicitly records `capture_method = deterministic_adaptation_from_frozen_phase_e_matrix_bundle` rather than a browser/network capture (`communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json:2-5`), and the implementation completion memo still states that live documentary closeout is pending (`communications/MEMO_2026-03-30_phase_e_transient_second_consumer_v1_implementation_completion.md:176-201`).

After revision, the memo now incorporates the previously missing evidence requirements directly:
- it requires freezing the exact observed POST body and tying it mechanically to the pinned fixture request (`communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md:178-199`);
- it requires a fresh-session HAR or equivalent full capture (`communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md:183-189`, `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md:270-283`);
- it explicitly allows non-analytical supporting requests such as style-token fetches and requires them to be called out honestly rather than treated as disqualifying noise (`communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md:223-227`).

That closes the main scope-level gaps from the earlier audit.

## Strongest Confirmed Claims

- The landed runtime boundary is exactly as narrow as the memo says. `aoi-canary` is admitted only for `source_selection`, while `compose-from-source` and `compose-from-intent` still fail closed for that consumer (`src/presenter/compose_from_intent.py:158-167`, `src/presenter/compose_from_intent.py:530-605`, `tests/test_compose_from_intent.py:831-900`).
- The canary-side transient slice is genuinely implemented. `App.tsx` contains a third `transient_proof` mode, and that mode issues a single `compose-from-selection` call using the pinned fixture request, then validates the bounded raw-json surface mechanically (`/home/evgeny/projects/aoi-canary/src/App.tsx:784-844`, `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts:71-150`).
- The current proof record is explicitly replay-oriented rather than live-oriented. The frozen JSON names a deterministic adaptation capture method and the implementation memo repeats that it is not a fresh browser/network closeout (`communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json:2-5`, `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_v1_implementation_completion.md:186-201`).
- The bounded degradation law is real and mechanically enforced across both repos: root `tab`, no root `raw_json`, at most one `raw_json` leaf, and that leaf is the report closeout (`tests/test_aoi_canary_contract.py:103-127`, `/home/evgeny/projects/aoi-canary/src/test/transientClient.test.ts:126-158`).
- There is still no frozen transient live-closeout artifact set in `communications/`; the named live-closeout files proposed by the memo do not yet exist. That matches the memo’s claim that the live documentary bar is still open.
- Focused verification is currently clean on the exact seams the memo relies on: analyzer tests passed `38`, canary type-check passed, and canary tests passed `18`.

## Audit Questions

### 1. Is one live-proof closeout over the already-landed `aoi-canary` / AOI `source_selection` path the right next Phase E step, or should replay already count as sufficient closure?

The live-proof closeout is the right next step.

The matrix slice already answered the handoff-family question on the current transient consumer surface, and the implementation slice already answered the bounded second-consumer contract question in code.
What remains open is evidentiary:
the current proof record is replay-derived, and no browser/network closeout artifact exists yet (`communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md:160-196`, `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_v1_implementation_completion.md:203-221`, `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json:2-5`).

Replay should not be upgraded to closure by itself.
The memo is right to keep the documentary bar open.

### 2. Is the memo honest about the current claim boundary: code-complete and test-clean, deterministic replay proof exists, fresh browser/network live proof does not yet exist?

Yes.

Code-complete and test-clean:
- confirmed by the analyzer allowlist, the canary transient mode, and the passing focused verification (`src/presenter/compose_from_intent.py:158-167`, `/home/evgeny/projects/aoi-canary/src/App.tsx:784-844`).

Deterministic replay proof exists:
- confirmed by the frozen proof JSON and its tests (`communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json:1-42`, `tests/test_aoi_canary_contract.py:103-127`).

Fresh browser/network live proof does not yet exist:
- confirmed by the implementation memo’s caveat and by the absence of the proposed live-closeout artifact set in `communications/` (`communications/MEMO_2026-03-30_phase_e_transient_second_consumer_v1_implementation_completion.md:182-201`).

One small documentary caution:
the canary README has not yet been updated to list `transient_proof` under Modes even though the code and tests clearly show it exists (`/home/evgeny/projects/aoi-canary/README.md:13-23`, `/home/evgeny/projects/aoi-canary/src/App.tsx:34-35`, `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:183-229`).
That is doc lag, not contrary code evidence.

### 3. Is the memo correct to keep the exact same proof path fixed instead of widening to `source_profile`, non-AOI transient proof, or broader consumer architecture?

Yes.

Keeping the exact path fixed is the right choice for both strategy and codebase accuracy.

Why `source_selection` should stay fixed:
- it is the only path currently admitted for `aoi-canary` at transient runtime (`src/presenter/compose_from_intent.py:166-167`, `src/presenter/compose_from_intent.py:600-605`);
- it is the planner-backed AOI path already carried by the Phase E matrix (`tests/test_representative_composition_matrix.py:69-106`);
- it preserves the already-landed fixture-backed canary flow (`/home/evgeny/projects/aoi-canary/src/fixtures/transient-aoi-source-selection.json:1-42`).

Why widening to `source_profile` is wrong here:
- runtime still rejects `aoi-canary` for `compose-from-source` (`tests/test_compose_from_intent.py:836-838`);
- readiness still hardcodes `compose-from-source` as blocked for any consumer other than `the-critic` (`src/analysis_products/source_backed_readiness.py:144-176`).

Why widening beyond AOI or into broader consumer architecture is wrong:
- it would vary a new Phase E variable before the current one is documentary-closed;
- the memo correctly states that this is evidence capture on an already-landed path, not a new architecture line (`communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md:27-48`, `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md:124-145`).

### 4. Does the required live evidence set mechanically prove the thin-host claim, or are any key assertions still too narrative?

Yes, after revision the evidence set is now mechanically strong enough for the bounded claim.

What is already mechanically strong in the memo:
- exact analyzer base URL;
- exact canary mode;
- screenshot of the ready state;
- HAR/network evidence of the real `POST /v1/presenter/compose-from-selection`;
- explicit absence of `route-task`, `plan-task`, `compose-from-source`, and `compose-from-intent` on the success path (`communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md:174-210`, `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md:253-264`).

The revised memo now names the exact missing pieces:
- exact observed POST body on the wire;
- fresh-session HAR or equivalent full capture;
- explicit statement of whether `observed_request_json == pinned_fixture.request` (`communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md:178-199`);
- explicit handling of allowed non-analytical support traffic such as style-token fetches (`communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md:223-227`).

That is enough to make the thin-host claim auditable rather than mostly inferred from implementation context.

### 5. Is the blocker-handling rule bounded correctly, or does it risk turning closeout into broad engine-definition cleanup?

The rule is bounded correctly on paper.

The memo explicitly allows only enough repair to unblock one truthful live capture on the existing path, and it explicitly says to stop and rescope if the blocker demands broader infrastructure work (`communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md:223-239`).
That is the right policy.

The remaining risk is practical, not conceptual:
“engine-definition load failure” is a broad enough label that an implementation session could drift unless it pins the unblocker to one reproducible failing `compose-from-selection` probe on this exact AOI path.

So the blocker rule is acceptable, but it should be executed with one more discipline:
- record the exact failing command, route, and stack signature before any fix;
- allow only the smallest change needed to make that one live probe succeed.

That keeps the closeout from quietly becoming engine-registry cleanup.

### 6. Does the memo keep the strategic claim calibrated: live documentary closeout of an already-landed second-consumer path, not a new architecture proof, not broad consumer generality?

Yes.

This is one of the memo’s strongest qualities.
It repeatedly states:
- the implementation question is already answered;
- the remaining gap is evidentiary;
- the path stays `aoi-canary` + AOI `source_selection` + `compose-from-selection` + `transient_proof`;
- the work must not widen into new consumer architecture or broader consumer generality (`communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md:101-145`, `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md:241-249`, `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md:280-290`).

I do not see strategic overclaim in the memo.

## Strategic Disagreement

- None.

## Scope Corrections

- None after the revision reviewed here.

## Implementation Caution

- The current documentary surface is slightly uneven. The code and tests prove `transient_proof` mode exists, but the canary README still documents only `artifact` and `live` modes (`/home/evgeny/projects/aoi-canary/src/App.tsx:34-35`, `/home/evgeny/projects/aoi-canary/README.md:13-23`). Do not let doc lag create false doubt during closeout review.
- `source_profile` is not a harmless fallback in practice. If the live proof tries to escape into `compose-from-source`, it will reopen extra analyzer coupling through readiness/followup law (`src/analysis_products/source_backed_readiness.py:144-176`). Keep the live closeout on the already-landed `source_selection` path.
- The canary transient proof path is intentionally thin. It makes one compose call and validates renderer degradation, but it does not fetch planner truth or other analyzer seams (`/home/evgeny/projects/aoi-canary/src/App.tsx:784-844`). That is good for the claim, but it means the live artifact record must do more documentary work because the app itself is intentionally minimal.

## Final Recommendation

Proceed with this closeout scope.

The next Phase E move should remain one live documentary proof over the already-landed `aoi-canary` / AOI `source_selection` transient path.
Do not widen the path.
Do not reclassify replay as closure.
The revised memo is now properly calibrated and mechanically specific enough to proceed as written.
