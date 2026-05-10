# Report: Claude Review Of Phase E Transient Second-Consumer Live Proof Closeout Scope

Date: 2026-03-30
Reviewer: Claude (Opus 4.6)
Memo Under Review: `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md`

## Verdict: Approve

The memo is the right next step, accurately bounded, and honest about the current state. The proof target is correct, the evidentiary gap is real, and the scope discipline is strong. No revisions are required before proceeding.

---

## What The Memo Gets Right

### 1. The distinction between implementation-complete and documentary-closed is precise and code-grounded

The memo's core structural claim — "the contract-level second-consumer claim is earned, the live documentary closeout is still pending" — is exactly accurate.

Code-verified:

- `src/presenter/compose_from_intent.py:158-167` now carries `"aoi-canary": frozenset({_HANDOFF_KIND_SOURCE_SELECTION})` in the `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` map. This is not a hypothetical — the gate is real, the code is landed, and `aoi-canary` is now admitted at runtime for exactly one bounded handoff kind.
- The canary repo carries a real `transient_proof` mode in `App.tsx`, a real `composeFromSelection()` client in `transientClient.ts`, a real fixture at `fixtures/transient-aoi-source-selection.json`, and three dedicated transient proof tests in both `App.test.tsx` and `transientClient.test.ts`.
- Both repos' verification suites pass: 38 Python tests, 18 canary tests.

The implementation completion memo (`MEMO_2026-03-30_phase_e_transient_second_consumer_v1_implementation_completion.md`) was honest that the proof JSON is `capture_method: "deterministic_adaptation_from_frozen_phase_e_matrix_bundle"` — not a live browser/network capture. The frozen proof record at `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json` confirms this derivation chain explicitly.

So the gap this memo targets is real: code and tests prove the contract, but no live browser/network evidence yet proves the actual running seam.

### 2. The proof target stays exactly on the already-landed path

The memo is disciplined about keeping the same target:

- consumer: `aoi-canary`
- path: AOI `source_selection`
- route: `POST /v1/presenter/compose-from-selection`
- host mode: `transient_proof`

This matches exactly what landed in the implementation completion. The memo does not attempt to widen to `source_profile`, does not introduce a new consumer, does not introduce a new compose family, and does not upgrade the canary's analytical capabilities. It also correctly does not downgrade the target from `source_selection` to a simpler path.

### 3. The thin-host verification requirement is mechanically precise

Decision 4 (lines 196-211) requires the closeout to make visible that the canary did not perform hidden upstream analytical work. The enumerated list of forbidden request seams (`route-task`, `plan-task`, planning-snapshot fetch, `compose-from-source`, `compose-from-intent`) is exactly the right set. The only expected request seam is `POST /v1/presenter/compose-from-selection`.

This is verifiable: a HAR capture or network log will show exactly which endpoints the canary hit. The canary's `transientClient.ts:71-85` confirms that the only outbound call is `fetchJson<ComposeFromIntentApiResponse>(\`${baseUrl}/v1/presenter/compose-from-selection\`, ...)`. The fixture replay path means the request body comes from the pinned fixture, not from local derivation.

### 4. The quality bar stays mechanical and already-encoded

Decision 5 (lines 212-221) correctly keeps the bounded degradation law:

- root `tab`
- no root `raw_json`
- at most one `raw_json` leaf
- that leaf is the closeout/report leaf only

This is already enforced in two independent code locations:

- Analyzer-side: `tests/test_aoi_canary_contract.py:103-127` — `test_aoi_canary_transient_source_selection_proof_stays_within_bounded_raw_json_fallback()` asserts exactly these invariants against the frozen proof JSON.
- Canary-side: `transientClient.ts:123-151` — `validateTransientProofSurface()` mechanically checks the same invariants at runtime.

The memo correctly requires that the live closeout not silently relax this bar.

### 5. The blocker-handling rule is correctly scoped

Decision 6 (lines 223-239) addresses the engine-definition load error that blocked direct live capture during the implementation pass. The allowed response — "fix or route around that blocker only enough to permit one truthful live success capture" — is appropriately narrow. The prohibited responses — broad engine-definition cleanup, widening the proof path to avoid the blocker, or silently reclassifying replay as live proof — are exactly the right exclusions.

The escape hatch is also correctly placed: "If the blocker turns out to require broader infrastructure work, stop and rescope instead of pretending the closeout is cheap." This prevents the closeout from silently accreting into a new architecture tranche.

### 6. The acceptance bar is complete and falsifiable

The seven acceptance criteria (lines 253-264) are all mechanically verifiable:

1. Real `compose-from-selection` success path — checkable via network artifact
2. `consumer_key = aoi-canary` on the actual live request — checkable via HAR/JSON
3. Rendered canary ready state captured from live response — checkable via screenshot
4. No hidden upstream analytical requests — checkable via complete network log
5. Bounded adaptation-quality law holds — checkable via response inspection
6. Explicit distinction from earlier deterministic replay — checkable in the proof note
7. Proof record frozen under `communications/` — checkable by file existence

No criterion is vague or subjective. Each maps to a concrete artifact or inspection.

---

## Answers To The Prompt Questions

### 1. Is a live-proof closeout the right next step, or should the program move on and treat the replay proof as sufficient?

The live-proof closeout is the right next step.

The program's own documentary standard established by the original scope memo (`MEMO_2026-03-30_phase_e_transient_second_consumer_scope.md`, section 5) called for "one real live proof bundle under `communications/`" with "one browser/network artifact set." The implementation completion memo explicitly left that bar open. Silently downgrading the proof standard from "live browser/network capture" to "deterministic replay from a frozen matrix bundle" would be dishonest and would set a bad precedent for future Phase E slices.

Furthermore, the replay proof is technically weaker: it proves that the response _would_ match the adaptation law if the compose route were called live, but it does not prove that the running system actually serves that response end-to-end through the canary's transient mode. The live proof closes that gap at very low marginal cost if the blocker is small.

The prior Stage 13 Tier A closeout (`MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md`) established the same pattern: implementation first, then one bounded live-proof closeout. Following the same discipline here is the right call.

### 2. Is the memo honest about the current boundary?

Yes. The three-part boundary claim is accurate:

- **Contract-level implementation claim earned**: Verified. The `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` gate admits `aoi-canary` on `source_selection`. The canary's `transient_proof` mode, client, and fixture are all landed and tested.
- **Browser/network proof still pending**: Verified. The proof JSON's `capture_method` field explicitly says `deterministic_adaptation_from_frozen_phase_e_matrix_bundle`, not live capture.
- **Blocker appears unrelated to the second-consumer contract question**: Plausible. The completion memo attributes the blocker to an "unrelated engine-definition load error." This memo correctly does not claim certainty about the blocker's root cause but appropriately scopes the allowed fix to "enough to permit one truthful live success capture."

### 3. Is the memo disciplined enough about keeping the exact same proof target?

Yes. The proof target is pinned to exactly:

- `aoi-canary`
- AOI `source_selection`
- `compose-from-selection`
- `transient_proof`

The memo repeats this target in the Strategic Decision (lines 129-137), in Decision 2 (lines 161-172), in the acceptance bar (lines 253-264), and in the final Decision (lines 282-291). There is no scope creep to `source_profile`, `compose-from-intent`, or non-AOI paths.

The "must not widen" section (lines 241-249) is comprehensive and does not contain loopholes.

### 4. Is the memo accurate about what must be shown to prove thin-hostness in live evidence?

Yes. Decision 4 correctly identifies that thin-hostness is proved by showing the canary's live network traffic contains only the intended `compose-from-selection` call and does not contain hidden upstream analytical requests. The enumerated forbidden seams are correct.

The canary's code confirms this: `transientClient.ts` makes exactly one outbound call (`composeFromSelection()`), and the fixture replay means the request body is not locally derived. A HAR capture would show this conclusively.

One minor observation: the canary also makes a `GET /v1/styles/tokens/{school}` call (visible in the test mocks). This is a CSS styling call, not an analytical request, and should not be treated as a thin-hostness violation. The proof note should acknowledge this call exists but correctly classify it as non-analytical.

### 5. Is the blocker-handling rule scoped correctly?

Yes, with one observation.

The rule ("fix or route around only enough to permit one truthful live success capture") is appropriately narrow. The escape hatch ("if broader infrastructure work is required, stop and rescope") prevents silent scope creep.

**Observation**: The memo does not specify a time budget or effort cap for the blocker fix. If the engine-definition load error turns out to require more than a trivial fix, the "stop and rescope" instruction is the right response. But the implementation session should be prepared to make this judgment call early rather than spending significant effort diagnosing the blocker before deciding whether to rescope.

### 6. Does the memo stay calibrated against the bigger program objective?

Yes. The memo explicitly frames itself as:

- live documentary closeout of one landed second-consumer path
- not a new generality variable
- not a new architecture tranche

This matches the distilled strategic roadmap (`MEMO_2026-03-30_distilled_strategic_roadmap.md`), which explicitly says the next bounded Phase E slice should be "one bounded live-proof closeout over the already-landed `aoi-canary` transient path." The fixed-direction roadmap also supports this: the Phase E generality proof is the active horizon, and closing the evidentiary tail on the already-landed slice is the right next micro-step before varying a new Phase E variable.

The memo correctly applies the anti-drift filter:

1. Does this move intelligence upstream? — Indirectly. It closes the evidence on a path that already moved intelligence upstream.
2. Does this reduce host-specific analytical behavior? — Neutral. The canary-side code is already landed.
3. Does this strengthen generic law? — Yes. It elevates the second-consumer claim from "contract-level test" to "live browser/network proof."
4. Does this help eventual contract-based generality? — Yes. Live evidence of thin-host consumption by a second consumer is direct generality proof.

---

## Observations (Not Revisions)

### Observation 1: The canary's style-token fetch should be documented in the proof

The canary test mocks show a `GET /v1/styles/tokens/{school}` call that currently returns 404. When the live proof runs, this call may succeed or fail. Either way, the proof note should acknowledge its existence and classify it as a non-analytical styling fetch that does not violate thin-hostness.

### Observation 2: The recommended artifact set is well-chosen but could be leaner

The memo recommends four separate proof artifacts (`.md`, `.json`, `.png`, `.har`). All four are useful, but the `.har` file alone would contain the complete request/response evidence that the other artifacts partially duplicate. The implementation session should decide whether the `.json` summary is still worth maintaining as a separate artifact or whether the HAR plus the markdown proof note suffice. This is a practical implementation choice, not a scope concern.

### Observation 3: The fixture identity is the same as the matrix proof bundle

The pinned fixture in `transient-aoi-source-selection.json` references `proof_bundle_identity: "communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json"`, which itself was `derived_from_bundle: "communications/PROOF_phase_e_matrix_aoi_source_selection_2026-03-30.json"`. The live proof should make this derivation chain visible in the proof note, so future review can trace the provenance from the original matrix bundle through to the live capture.

### Observation 4: The precedent from Stage 13 Tier A closeout is the right structural template

The earlier `MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md` followed the same pattern: implementation done, live proof pending, one bounded closeout step. The current memo correctly references this as "Relevant Prior Live Closeout Pattern." The structural similarity is appropriate — both are evidence-capture steps, not architecture steps.

---

## Strategic Assessment

This memo passes the distilled strategic roadmap's four-question heuristic:

1. **Does this move intelligence upstream into analyzer-v2?** — It closes the evidentiary record on a path that already did.
2. **Does this reduce host-specific analytical behavior?** — It proves the canary operates as a thin host on the live compose path.
3. **Does this strengthen generic law rather than one more special case?** — Live proof of a second consumer strengthens the generality claim.
4. **Does this help eventual contract-based generality?** — Yes. Browser/network evidence of thin-host consumption by a second consumer is the most direct generality evidence the program can produce at this point.

The memo is also correctly sequenced against the broader Phase E horizon. The first slice proved handoff-family breadth. The second slice proved second-consumer admission. This third micro-slice closes the evidentiary gap on the second slice. After this, the program can honestly vary a new Phase E variable (broader consumer matrix, non-AOI second-consumer path, or production-path hardening).

---

## Bottom Line

The memo is honest, well-bounded, and correctly scoped as an evidence-capture step. The proof target is precisely the already-landed path. The acceptance bar is mechanical and falsifiable. The blocker-handling rule is appropriately narrow with a correct escape hatch. The memo does not hide behind a weaker proof or widen into new architecture.

Proceed with execution.
